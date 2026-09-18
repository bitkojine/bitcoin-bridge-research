from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build() -> Path:
    model = json.loads((ROOT / "domain/model.json").read_text(encoding="utf-8"))
    rules = json.loads((ROOT / "domain/rules.json").read_text(encoding="utf-8"))
    assessment = json.loads(
        (ROOT / "domain/assessments/custody-readiness.json").read_text(encoding="utf-8")
    )
    manifest_path = ROOT / "evidence" / "sources" / "manifest.json"
    evidence = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {
        "meta": {},
        "snapshots": [],
    }
    case_studies = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "domain" / "cases").glob("*.json"))
    ]
    payload = {
        "model": model, "rules": rules, "assessment": assessment,
        "evidence": evidence, "case_studies": case_studies,
    }
    output = ROOT / "dist/knowledge.js"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "window.KNOWLEDGE = " + json.dumps(payload, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    return output


if __name__ == "__main__":
    print(build())
