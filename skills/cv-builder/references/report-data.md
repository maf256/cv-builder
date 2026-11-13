# report-data.json

`scripts/build_report.py` reads this file, validates it, adds a `scores` object, and writes `report.html` (standalone) and `report-chat.html` (themed for inline display in chat). Use exactly these keys and enumerated values. All free text is written in the conversation language (`meta.ui_lang`).

Describe changes in the report; do not include rewritten CV text.

```json
{
  "meta": {
    "ui_lang": "en",
    "output_langs": ["en", "no"],
    "candidate": "Full name as on the CV",
    "role": "Job title from the posting",
    "company": "Employer",
    "posting_url": "https://...",
    "date": "2026-01-31",
    "sources": ["cv-2025.pdf", "bachelor-diploma.pdf"]
  },
  "summary": "One sentence, under 160 characters: the verdict and the main gap.",
  "top_fixes": [
    "Add Power BI: the reference letter proves it",
    "Switch to one column and drop the skill bars"
  ],
  "requirements": [
    {
      "text": "Three years' experience with Python",
      "category": "must",
      "status": "met",
      "evidence": "Developer at Acme 2019–2023, Python named in two roles"
    }
  ],
  "keywords": [
    { "term": "Python", "importance": "high", "found": true }
  ],
  "ats_checks": [
    { "id": "file_format", "status": "pass", "note": "Text-based PDF" }
  ],
  "contradictions": [
    {
      "title": "End date at Acme differs",
      "detail": "The CV says June 2023, the reference letter says March 2023.",
      "sources": ["cv-2025.pdf", "reference-acme.pdf"],
      "severity": "high"
    }
  ],
  "remove": [
    { "item": "Summer job at a kiosk, 2008", "reason": "Unrelated to the role and 18 years old" }
  ],
  "add": [
    {
      "item": "AWS Solutions Architect certificate (2024)",
      "reason": "Attached but not on the CV; the posting lists AWS as required",
      "needs_confirmation": false
    }
  ],
  "rewrite": [
    { "item": "Acme role description", "reason": "Lists duties only; the source shows the SQL work the posting asks for" }
  ],
  "research": [
    {
      "finding": "The team builds the billing platform used by the municipal clients",
      "use": "Cover letter, second paragraph",
      "source_url": "https://..."
    }
  ],
  "questions": [
    {
      "id": "level_en",
      "question": "English level?",
      "options": [
        { "key": "A", "label": "B1: short, simple sentences" },
        { "key": "B", "label": "B2: clear and direct" },
        { "key": "C", "label": "C1: fluent professional" },
        { "key": "D", "label": "C2: native-level" }
      ],
      "multi": false,
      "allow_custom": true,
      "recommended": "B"
    }
  ]
}
```

## Field rules

| Field | Rule |
|---|---|
| `meta.ui_lang` | `en` or `no`; the report's own labels follow it |
| `meta.output_langs` | Non-empty list of `en` and/or `no` |
| `meta.date` | ISO date of the analysis |
| `requirements[].category` | `must`, `experience`, `nice`, `education`, `language` |
| `requirements[].status` | `met`, `partial`, `missing` |
| `requirements` | At least one item |
| `keywords[].importance` | `high` or `normal` |
| `keywords[].found` | `true` or `false` |
| `ats_checks` | Exactly the ten ids in `analysis-rubric.md`, each once, in that order |
| `ats_checks[].status` | `pass`, `warn`, `fail` |
| `contradictions[].severity` | `high` or `low` |
| `summary` | One sentence, at most 160 characters. Plain words, no hedging |
| `top_fixes` | One to three strings, at most 90 characters each, ordered by impact |
| `questions` | At most 8; see `form-questions.md` |
| `questions[].question` | At most 90 characters |
| `questions[].options[].label` | At most 60 characters |
| `questions[].id` | Unique; use the ids in `form-questions.md` |
| `questions[].options` | Zero to six items, keys `A` to `F` in order. Zero options makes an open question |
| `questions[].multi` | `true` lets the user tick several options |
| `questions[].allow_custom` | Keep `true`; the user must always be able to write their own answer |
| `questions[].recommended` | Optional; one option key |

`contradictions`, `remove`, `add`, `rewrite` and `research` may be empty lists but must be present. Do not add a `scores` key; the script writes it.
