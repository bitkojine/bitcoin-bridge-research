"""Content-addressed source evidence: freeze what the claims actually cite.

The repository's promise is that a claim's status cannot outrun its evidence.
A mutable URL cannot back that promise, so `archive_source` fetches a source,
stores the exact bytes under `evidence/sources/<id>/<sha256>.<ext>`, and records
the hash, size, retrieval time, and extracted text in a manifest. Claim
treatments carry a passage `locator` and a verbatim `quote`; validation checks
that quote against the frozen text offline.

Only `run_archive` touches the network. `validate`, tests, and CI are offline
and deterministic.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "evidence" / "sources"
MANIFEST_PATH = EVIDENCE_DIR / "manifest.json"

USER_AGENT = "Mozilla/5.0 (compatible; bitcoin-bridge-research archive; +https://github.com/bitkojine/bitcoin-bridge-research)"
MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024

_EXTENSIONS = {
    "text/html": ".html",
    "application/xhtml+xml": ".html",
    "application/pdf": ".pdf",
    "text/plain": ".txt",
    "application/xml": ".xml",
    "text/xml": ".xml",
    "application/json": ".json",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").split())


class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "head"}
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def extract_text(content_type: str, data: bytes) -> str | None:
    content_type = (content_type or "").lower()
    if "pdf" in content_type or data[:5] == b"%PDF-":
        try:
            import io

            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(data))
            return "\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception:
            return None
    if "html" in content_type or data.lstrip()[:6].lower() in {b"<!doct", b"<html"}:
        parser = _TextExtractor()
        parser.feed(data.decode("utf-8", "replace"))
        return normalize("".join(parser.parts))
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", "replace")


def extension_for(url: str, content_type: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".pdf", ".html", ".htm", ".txt", ".xml", ".json", ".mediawiki", ".md"}:
        return ".html" if suffix == ".htm" else suffix
    for key, value in _EXTENSIONS.items():
        if key in (content_type or "").lower():
            return value
    return ".bin"


def fetch(url: str, timeout: float = 40.0, max_bytes: int = MAX_DOWNLOAD_BYTES) -> dict:
    scheme = urlparse(url).scheme.lower()
    if scheme not in {"http", "https"}:
        raise ValueError(f"unsupported source URL scheme: {scheme or '(missing)'}")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        declared_size = response.headers.get("Content-Length")
        if declared_size and int(declared_size) > max_bytes:
            raise ValueError(f"source exceeds {max_bytes} byte download limit")
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"source exceeds {max_bytes} byte download limit")
        return {
            "data": data,
            "content_type": response.headers.get("Content-Type", ""),
            "final_url": response.geturl(),
        }


def archive_source(source: dict, timeout: float = 40.0) -> dict:
    source_url = source.get("archive_url") or source["url"]
    fetched = fetch(source_url, timeout=timeout)
    data = fetched["data"]
    content_type = fetched["content_type"]
    digest = sha256_bytes(data)
    extension = extension_for(fetched["final_url"] or source_url, content_type)
    directory = EVIDENCE_DIR / source["id"]
    directory.mkdir(parents=True, exist_ok=True)
    artifact = directory / f"{digest}{extension}"
    artifact.write_bytes(data)
    base = EVIDENCE_DIR.parents[1]

    entry = {
        "source_id": source["id"],
        "status": "frozen",
        "url": source["url"],
        "archive_url": source_url,
        "final_url": fetched["final_url"],
        "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sha256": digest,
        "bytes": len(data),
        "content_type": content_type,
        "path": str(artifact.relative_to(base)),
    }
    text = extract_text(content_type, data)
    if text:
        text_digest = sha256_bytes(text.encode("utf-8"))
        text_path = directory / f"{digest}.txt"
        text_path.write_text(text, encoding="utf-8")
        entry["text_path"] = str(text_path.relative_to(base))
        entry["text_sha256"] = text_digest
        entry["text_chars"] = len(text)
    return entry


def unavailable_entry(source: dict, error: str, previous: dict | None) -> dict:
    entry = {
        "source_id": source["id"],
        "status": "unavailable",
        "url": source["url"],
        "attempted_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "error": error,
    }
    if previous and previous.get("status") == "frozen":
        frozen = {k: v for k, v in previous.items() if k != "last_attempt"}
        frozen["last_attempt"] = {"at": entry.pop("attempted_at"), "error": error}
        frozen["status"] = "frozen"
        return frozen
    return entry


def load_manifest(path: Path | None = None) -> dict:
    path = path or MANIFEST_PATH
    if not path.exists():
        return {"meta": {}, "snapshots": []}
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(manifest: dict) -> dict[str, dict]:
    return {entry["source_id"]: entry for entry in manifest.get("snapshots", [])}


def run_archive(model: dict, timeout: float = 40.0, manifest_path: Path | None = None) -> dict:
    path = manifest_path or MANIFEST_PATH
    previous = by_id(load_manifest(path))
    entries = []
    for source in model.get("sources", []):
        try:
            entries.append(archive_source(source, timeout=timeout))
        except Exception as error:  # network failure is recorded, never hidden
            message = f"{type(error).__name__}: {error}"
            entries.append(unavailable_entry(source, message, previous.get(source["id"])))
    entries.sort(key=lambda item: item["source_id"])
    frozen = sum(1 for item in entries if item["status"] == "frozen")
    manifest = {
        "meta": {
            "generated_on": datetime.now(timezone.utc).date().isoformat(),
            "frozen": frozen,
            "unavailable": len(entries) - frozen,
        },
        "snapshots": entries,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def _check_frozen_files(entry: dict) -> list[str]:
    problems: list[str] = []
    artifact = ROOT / entry["path"]
    if not artifact.exists():
        return [f"snapshot {entry['source_id']} artifact is missing: {entry['path']}"]
    actual = sha256_file(artifact)
    if actual != entry["sha256"]:
        problems.append(
            f"snapshot {entry['source_id']} hash mismatch: recorded {entry['sha256'][:12]}, found {actual[:12]}"
        )
    if artifact.stat().st_size != entry.get("bytes"):
        problems.append(f"snapshot {entry['source_id']} byte size differs from the manifest")
    text_path = entry.get("text_path")
    if text_path:
        text_file = ROOT / text_path
        if not text_file.exists():
            problems.append(f"snapshot {entry['source_id']} extracted text is missing: {text_path}")
        elif sha256_file(text_file) != entry.get("text_sha256"):
            problems.append(f"snapshot {entry['source_id']} extracted-text hash mismatch")
    return problems


def verify_snapshots(model: dict, manifest: dict) -> list[str]:
    """Every frozen snapshot must be byte-stable on disk, and every source a
    claim cites must be frozen."""
    entries = by_id(manifest)
    problems: list[str] = []
    for entry in manifest.get("snapshots", []):
        if entry.get("status") == "frozen":
            problems.extend(_check_frozen_files(entry))
    for claim in model.get("claims", []):
        for treatment in claim.get("treatments", []):
            source_id = treatment.get("source_id")
            entry = entries.get(source_id)
            if entry is None:
                problems.append(
                    f"claim {claim['id']} cites {source_id} which has no evidence snapshot"
                )
                continue
            if entry.get("status") != "frozen":
                problems.append(
                    f"claim {claim['id']} cites {source_id} whose snapshot is "
                    f"{entry.get('status')}: {entry.get('error', '')}".strip()
                )
    return problems


def verify_pin_cites(model: dict, manifest: dict) -> list[str]:
    """Require a literal locator before the quote in the frozen text.

    This verifies passage placement, not whether the passage entails the claim.
    """
    entries = by_id(manifest)
    problems: list[str] = []
    for claim in model.get("claims", []):
        for treatment in claim.get("treatments", []):
            source_id = treatment.get("source_id")
            label = f"claim {claim['id']} treatment {source_id}"
            locator = treatment.get("locator")
            if not locator:
                problems.append(f"{label} has no pin-cite locator")
            quote = treatment.get("quote")
            if not quote:
                problems.append(f"{label} has no pin-cite quote")
                continue
            entry = entries.get(source_id) or {}
            text_path = entry.get("text_path")
            if not text_path:
                problems.append(f"{label} cannot verify its quote: no frozen text")
                continue
            text_file = ROOT / text_path
            if not text_file.exists():
                problems.append(f"{label} cannot verify its quote: frozen text missing")
                continue
            text = normalize(text_file.read_text(encoding="utf-8"))
            normalized_quote = normalize(quote)
            normalized_locator = normalize(locator) if locator else ""
            quote_at = text.find(normalized_quote)
            if quote_at < 0:
                problems.append(f"{label} pin-cite quote is not present in the frozen source text")
                continue
            locator_at = text.rfind(normalized_locator, 0, quote_at) if normalized_locator else -1
            if locator and locator_at < 0:
                problems.append(f"{label} pin-cite locator is not present before its quote")
    return problems


def snapshot_coverage(manifest: dict) -> dict:
    entries = by_id(manifest)
    frozen = [e for e in entries.values() if e.get("status") == "frozen"]
    unavailable = [e["source_id"] for e in entries.values() if e.get("status") != "frozen"]
    return {"total": len(entries), "frozen": len(frozen), "unavailable": sorted(unavailable)}


def check_drift(manifest: dict, timeout: float = 40.0) -> list[dict]:
    """Re-fetch frozen sources and report any whose bytes changed (network)."""
    drift: list[dict] = []
    for entry in manifest.get("snapshots", []):
        if entry.get("status") != "frozen":
            continue
        try:
            fetched = fetch(entry.get("archive_url") or entry["url"], timeout=timeout)
            current = sha256_bytes(fetched["data"])
            if current != entry["sha256"]:
                drift.append({
                    "source_id": entry["source_id"],
                    "recorded": entry["sha256"],
                    "current": current,
                })
        except Exception as error:
            drift.append({
                "source_id": entry["source_id"],
                "recorded": entry["sha256"],
                "error": f"{type(error).__name__}: {error}",
            })
    return drift
