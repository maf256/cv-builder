#!/usr/bin/env python3
"""Build the Phase 1 report.

Usage: build_report.py <report-data.json> [output.html]

Validates the data, computes the scores defined in references/analysis-rubric.md,
writes them back into the JSON under "scores", and fills assets/report-template.html.
Writes report.html (standalone) and report-chat.html (themed for inline display).
Standard library only.
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "report-template.html"
MARKER = "/*__CV_DATA__*/"
EMBED_OFF, EMBED_ON = "/*__EMBED__*/false", "/*__EMBED__*/true"

MAX_SUMMARY = 160
MAX_FIX = 90
MAX_QUESTIONS = 8
MAX_QUESTION = 90
MAX_OPTION = 60

CATEGORY_WEIGHTS = {"must": 50, "experience": 20, "nice": 15, "education": 10, "language": 5}
STATUS_POINTS = {"met": 1.0, "partial": 0.5, "missing": 0.0}
CHECK_POINTS = {"pass": 1.0, "warn": 0.5, "fail": 0.0}
ATS_CHECK_IDS = [
    "file_format",
    "text_layer",
    "single_column",
    "no_tables_graphics",
    "standard_headings",
    "contact_in_body",
    "date_format",
    "reverse_chronological",
    "title_alignment",
    "plain_characters",
]
LANGS = {"en", "no"}
OPTION_KEYS = "ABCDEF"


def validate(data):
    errors = []

    def need(obj, key, kind, where):
        if key not in obj:
            errors.append(f"{where}: missing '{key}'")
            return None
        if not isinstance(obj[key], kind):
            errors.append(f"{where}.{key}: expected {kind.__name__}")
            return None
        return obj[key]

    def one_of(obj, key, allowed, where):
        value = obj.get(key)
        if value not in allowed:
            errors.append(f"{where}.{key}: '{value}' is not one of {sorted(allowed)}")

    meta = need(data, "meta", dict, "root")
    if meta is not None:
        one_of(meta, "ui_lang", LANGS, "meta")
        langs = need(meta, "output_langs", list, "meta")
        if langs is not None and (not langs or not set(langs) <= LANGS):
            errors.append("meta.output_langs: must be a non-empty list of 'en' and/or 'no'")
        for key in ("candidate", "role", "company", "date"):
            need(meta, key, str, "meta")
        need(meta, "sources", list, "meta")

    summary = need(data, "summary", str, "root")
    if summary and len(summary) > MAX_SUMMARY:
        errors.append(f"summary: {len(summary)} characters; keep it to one sentence under {MAX_SUMMARY}")
    fixes = need(data, "top_fixes", list, "root")
    if fixes is not None:
        if not 1 <= len(fixes) <= 3:
            errors.append("top_fixes: give one to three items")
        for i, f in enumerate(fixes):
            if not isinstance(f, str) or len(f) > MAX_FIX:
                errors.append(f"top_fixes[{i}]: a string under {MAX_FIX} characters")

    reqs = need(data, "requirements", list, "root")
    if reqs is not None:
        if not reqs:
            errors.append("requirements: at least one item is required")
        for i, r in enumerate(reqs):
            where = f"requirements[{i}]"
            need(r, "text", str, where)
            need(r, "evidence", str, where)
            one_of(r, "category", set(CATEGORY_WEIGHTS), where)
            one_of(r, "status", set(STATUS_POINTS), where)

    kws = need(data, "keywords", list, "root")
    for i, k in enumerate(kws or []):
        where = f"keywords[{i}]"
        need(k, "term", str, where)
        one_of(k, "importance", {"high", "normal"}, where)
        if not isinstance(k.get("found"), bool):
            errors.append(f"{where}.found: expected true or false")

    checks = need(data, "ats_checks", list, "root")
    if checks is not None:
        ids = [c.get("id") for c in checks]
        if ids != ATS_CHECK_IDS:
            errors.append(f"ats_checks: ids must be exactly, in order: {', '.join(ATS_CHECK_IDS)}")
        for i, c in enumerate(checks):
            one_of(c, "status", set(CHECK_POINTS), f"ats_checks[{i}]")

    for i, c in enumerate(need(data, "contradictions", list, "root") or []):
        where = f"contradictions[{i}]"
        need(c, "title", str, where)
        need(c, "detail", str, where)
        one_of(c, "severity", {"high", "low"}, where)

    for section in ("remove", "add", "rewrite"):
        for i, item in enumerate(need(data, section, list, "root") or []):
            need(item, "item", str, f"{section}[{i}]")
            need(item, "reason", str, f"{section}[{i}]")

    for i, item in enumerate(need(data, "research", list, "root") or []):
        need(item, "finding", str, f"research[{i}]")

    questions = need(data, "questions", list, "root")
    if questions is not None and len(questions) > MAX_QUESTIONS:
        errors.append(f"questions: {len(questions)} questions; the form holds {MAX_QUESTIONS} at most (see references/form-questions.md)")
    seen = set()
    for i, q in enumerate(questions or []):
        where = f"questions[{i}]"
        qid = need(q, "id", str, where)
        if qid in seen:
            errors.append(f"{where}.id: '{qid}' is used twice")
        seen.add(qid)
        text = need(q, "question", str, where)
        if text and len(text) > MAX_QUESTION:
            errors.append(f"{where}.question: {len(text)} characters; keep it under {MAX_QUESTION}")
        options = need(q, "options", list, where)
        if options is not None:
            for o in options:
                if len(str(o.get("label", ""))) > MAX_OPTION:
                    errors.append(f"{where}: option {o.get('key')} label is over {MAX_OPTION} characters")
            keys = [o.get("key") for o in options]
            if len(options) > len(OPTION_KEYS) or keys != list(OPTION_KEYS[: len(options)]):
                errors.append(f"{where}.options: keys must be A, B, C... in order, six at most")
            if q.get("recommended") and q["recommended"] not in keys:
                errors.append(f"{where}.recommended: '{q['recommended']}' is not an option key")
    return errors


def band(score):
    return "high" if score >= 75 else "mid" if score >= 50 else "low"


def compute_scores(data):
    breakdown = []
    earned = total = 0.0
    for category, weight in CATEGORY_WEIGHTS.items():
        items = [r for r in data["requirements"] if r["category"] == category]
        if not items:
            continue
        avg = sum(STATUS_POINTS[r["status"]] for r in items) / len(items)
        earned += weight * avg
        total += weight
        breakdown.append(
            {
                "category": category,
                "weight": weight,
                "pct": round(avg * 100),
                "count": len(items),
                "met": sum(r["status"] == "met" for r in items),
                "partial": sum(r["status"] == "partial" for r in items),
                "missing": sum(r["status"] == "missing" for r in items),
            }
        )
    match = round(earned / total * 100)

    def kw_weight(k):
        return 2 if k["importance"] == "high" else 1

    kw_total = sum(kw_weight(k) for k in data["keywords"])
    kw_found = sum(kw_weight(k) for k in data["keywords"] if k["found"])
    coverage = round(kw_found / kw_total * 100) if kw_total else 0

    checks = data["ats_checks"]
    checks_pct = sum(CHECK_POINTS[c["status"]] for c in checks) / len(checks) * 100
    ats = round(0.6 * coverage + 0.4 * checks_pct)
    ats_band = band(ats)
    unreadable = any(c["id"] == "text_layer" and c["status"] == "fail" for c in checks)
    if unreadable:
        ats_band = "low"

    return {
        "match": match,
        "match_band": band(match),
        "breakdown": breakdown,
        "keyword_coverage": coverage,
        "keywords_found": sum(k["found"] for k in data["keywords"]),
        "keywords_total": len(data["keywords"]),
        "ats": ats,
        "ats_band": ats_band,
        "ats_unreadable": unreadable,
        "checks_passed": sum(c["status"] == "pass" for c in checks),
    }


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    data_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) == 3 else data_path.with_name("report.html")
    chat_path = out_path.with_name(out_path.stem + "-chat.html")

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{data_path}: not valid JSON: {e}")

    errors = validate(data)
    if errors:
        print(f"{data_path}: {len(errors)} problem(s). See references/report-data.md.", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    data["scores"] = compute_scores(data)
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    template = TEMPLATE.read_text(encoding="utf-8")
    if MARKER not in template or EMBED_OFF not in template:
        sys.exit(f"{TEMPLATE}: data or embed marker not found")
    # "</" must not appear inside a <script> block
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = template.replace(MARKER, payload)
    out_path.write_text(page, encoding="utf-8")
    chat_path.write_text(page.replace(EMBED_OFF, EMBED_ON), encoding="utf-8")

    s = data["scores"]
    print(f"Wrote {out_path} and {chat_path.name}")
    print(f"Match {s['match']}/100 ({s['match_band']}) · ATS {s['ats']}/100 ({s['ats_band']}) · "
          f"keywords {s['keywords_found']}/{s['keywords_total']} ({s['keyword_coverage']}%)")


if __name__ == "__main__":
    main()
