from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "domain-map.pdf"

INK = HexColor("#17243A")
MUTED = HexColor("#5B6675")
ORANGE = HexColor("#F7931A")
BLUE = HexColor("#2367A8")
GREEN = HexColor("#24735A")
PALE_BLUE = HexColor("#EAF3FB")
PALE_ORANGE = HexColor("#FFF2DE")
LINE = HexColor("#D8DEE7")
PAPER = HexColor("#FBFCFE")
WHITE = colors.white

base = getSampleStyleSheet()
STYLES = {
    "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=27,
                            leading=31, textColor=INK, spaceAfter=13),
    "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=13,
                               leading=18, textColor=BLUE, spaceAfter=15),
    "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=19,
                         leading=23, textColor=INK, spaceAfter=9),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11,
                         leading=14, textColor=BLUE, spaceBefore=5, spaceAfter=4),
    "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Helvetica", fontSize=8.7,
                           leading=12, textColor=INK, spaceAfter=6),
    "small": ParagraphStyle("small", parent=base["BodyText"], fontName="Helvetica", fontSize=7.1,
                            leading=9.3, textColor=INK),
    "tiny": ParagraphStyle("tiny", parent=base["BodyText"], fontName="Helvetica", fontSize=6.3,
                           leading=8.2, textColor=MUTED),
    "table_header": ParagraphStyle("table_header", parent=base["BodyText"], fontName="Helvetica-Bold",
                                   fontSize=7.1, leading=9.3, textColor=WHITE),
    "equation": ParagraphStyle("equation", parent=base["Code"], fontName="Courier-Bold", fontSize=10,
                               leading=13, alignment=TA_CENTER, textColor=INK, spaceAfter=5),
    "callout": ParagraphStyle("callout", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=13,
                              leading=17, alignment=TA_CENTER, textColor=INK),
}


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def callout(text: str) -> Table:
    table = Table([[p(text, "callout")]], colWidths=[170 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.7, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return table


def matrix(headers: list[str], rows: list[list[str]], widths: list[float]) -> Table:
    data = [[p(x, "table_header") for x in headers]]
    data.extend([[p(str(x), "small") for x in row] for row in rows])
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, HexColor("#F5F7FA")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    if doc.page > 1:
        canvas.setFillColor(INK)
        canvas.setFont("Helvetica-Bold", 7)
        canvas.drawString(20 * mm, A4[1] - 12 * mm, "BITCOIN BRIDGE DOMAIN MAP")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, f"PAGE {doc.page}")
        canvas.setStrokeColor(LINE)
        canvas.line(20 * mm, A4[1] - 15 * mm, A4[0] - 20 * mm, A4[1] - 15 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 6.5)
    canvas.drawString(20 * mm, 10 * mm, "Generated from domain/model.json")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Model {doc.model_version}")
    canvas.restoreState()


def company_label(name: str) -> str:
    return f'<font color="#2367A8"><b>{name}</b></font>'


def build_pdf(model: dict) -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=17 * mm,
        title=model["meta"]["title"], author="Bitcoin Bridge Research"
    )
    doc.model_version = model["meta"]["version"]
    companies = model["companies"]
    sources = {item["id"]: item for item in model["sources"]}
    story = [
        Spacer(1, 28 * mm),
        p("GENERATED RESEARCH OUTPUT", "h2"),
        p(model["meta"]["title"], "title"),
        p("The mathematical map, institutional requirements, and companies occupying the bridge", "subtitle"),
        Spacer(1, 8 * mm),
        callout(model["meta"]["thesis"]),
        Spacer(1, 10 * mm),
        p("Generation contract", "h2"),
        p("Every capability, equation, definition, bridge, company and evidence link on the following pages was read from the repository's structured domain model. Editing the model and rebuilding changes this document."),
        p(f"Model version: <b>{model['meta']['version']}</b><br/>Snapshot generated on: <b>{model['meta']['generated_on']}</b>", "small"),
        PageBreak(),
        p("1. The mathematical map", "h1"),
        p("Bitcoin supplies narrow, machine-verifiable guarantees. The model requires every equation to define its terms and state both what it establishes and what it does not establish."),
    ]

    capability_rows = []
    for item in model["bitcoin_capabilities"]:
        terms = "<br/>".join(f"<b>{key}</b> = {value}" for key, value in item["terms"].items())
        exclusions = ", ".join(item["does_not_establish"])
        capability_rows.append([
            f"<b>{item['name']}</b><br/><font name='Courier'>{item['formula']}</font>",
            terms,
            f"<b>Establishes:</b> {item['establishes']}<br/><b>Does not establish:</b> {exclusions}",
        ])
    story += [matrix(["Capability and formula", "Terms", "Boundary"], capability_rows,
                     [43 * mm, 57 * mm, 70 * mm]), PageBreak(),
              p("2. What finance and law require", "h1"),
              p("The bridge market exists because institutional capital needs facts and controls that are intentionally outside Bitcoin's consensus rules."),
              p("Traditional-finance requirements", "h2")]

    finance_rows = [[f"<b>{x['name']}</b>", x["id"]] for x in model["finance_requirements"]]
    legal_rows = [[f"<b>{x['name']}</b>", x["id"]] for x in model["legal_requirements"]]
    story += [matrix(["Requirement", "Stable model identifier"], finance_rows, [120 * mm, 50 * mm]),
              Spacer(1, 7 * mm), p("Legal requirements", "h2"),
              matrix(["Requirement", "Stable model identifier"], legal_rows, [120 * mm, 50 * mm]),
              Spacer(1, 8 * mm),
              callout("Bitcoin evidence + institutional records = financeable Bitcoin"), PageBreak(),
              p("3. The bridge territory", "h1"),
              p("Companies are grouped by the bridge classifications encoded in the model. A company may occupy more than one bridge."),]

    bridge_rows = []
    for bridge in model["bridges"]:
        names = sorted(company_label(c["name"]) for c in companies if bridge["id"] in c["bridges"])
        bitcoin = ", ".join(bridge["bitcoin_capabilities"]) or "-"
        institutional = ", ".join(bridge["finance_requirements"] + bridge["legal_requirements"]) or "-"
        bridge_rows.append([f"<b>{bridge['name']}</b>", bitcoin, institutional, ", ".join(names) or "No company recorded"])
    story += [matrix(["Bridge", "Bitcoin capabilities", "Institutional requirements", "Companies"], bridge_rows,
                     [34 * mm, 40 * mm, 54 * mm, 42 * mm]), PageBreak(),
              p("4. Evidence-backed claims", "h1"),
              p("Claims are published with an explicit status and source set. Validation rejects unknown statuses and missing source references."),]

    claim_rows = []
    for claim in model["claims"]:
        linked = "<br/>".join(
            f"<b>{sources[t['source_id']]['title']}</b> ({t['treatment']})<br/>{sources[t['source_id']]['url']}"
            for t in claim["treatments"]
        )
        replaced = f"<br/>Superseded by: {', '.join(claim['superseded_by'])}" if claim.get("superseded_by") else ""
        claim_rows.append([f"<b>{claim['status'].upper()}</b>", claim["text"] + replaced, linked])
    story += [matrix(["Status", "Claim", "Sources"], claim_rows, [29 * mm, 76 * mm, 65 * mm]),
              Spacer(1, 8 * mm), p("Current scope", "h2"),
              p(f"The model currently contains <b>{len(model['bitcoin_capabilities'])}</b> Bitcoin capabilities, "
                f"<b>{len(model['finance_requirements'])}</b> finance requirements, "
                f"<b>{len(model['legal_requirements'])}</b> legal requirements, "
                f"<b>{len(model['bridges'])}</b> bridge categories, "
                f"<b>{len(companies)}</b> companies, <b>{len(model['sources'])}</b> sources, and "
                f"<b>{len(model['claims'])}</b> evidence-linked claims."),
              callout("This PDF demonstrates the engine, not a finished market census. Its visible gaps are model gaps that can now be improved through versioned contributions.")]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return OUTPUT
