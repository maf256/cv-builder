# The question form

The form closes Phase 1. Its answers, the sources and the posting are everything Phase 2 may use.

## Limits

- **At most 8 questions.** Each question under 90 characters, each option label under 60. `build_report.py` rejects anything longer.
- Lettered options A to D (six at most), plus a one-line field for the user's own answer.
- Write in the conversation language. Fill options from the analysis: name the actual item, date or skill, never a placeholder.
- Ask only what the documents cannot answer. If you can read the answer from a source, do not ask.

## Questions, in priority order

Fill the form from the top until you reach 8. Whatever does not fit is handled by the defaults below, or asked in chat at the gate.

| # | id | Asked when | Question | Options |
|---|---|---|---|---|
| 1 | `level_en`, `level_no` | Always; one per output language | "English level?" / "Norwegian level?" | A: B1, simple sentences. B: B2, clear and direct. C: C1, fluent. D: C2, native-level. Recommend the level the sources document |
| 2 | `tone` | Always | "Tone?" | A: Brief and factual. B: Neutral. C: Warm cover letter, factual CV. D: Formal |
| 3 | `remove` | Always | "Remove these?" | Multi-select, one option per proposed removal. Group minor ones into one option |
| 4 | `missing` | Always | "Anything missing from your documents?" | A: No. Own answer: skills, jobs, projects or courses, with dates |
| 5 | `motivation` | Always | "Why this employer?" | Two or three options from the research, plus own answer. The letter needs the user's real reason |
| 6 | `conflict_<n>` | Each `high` contradiction | Name the fact: "End date at Nordlys?" | One option per version, with its source |
| 7 | `gap_<n>` | Each `must` requirement rated `missing` or `partial` | Name the requirement: "Azure Data Factory?" | A: Yes, details below. B: Some exposure, details below. C: No. D: Learning it now, details below |
| 8 | `title` | The user's titles differ from the posting's for the same work | "Headline?" | The truthful candidates. Never a title the user has not held |

Drop these only after the fixed five and the conflicts are in. If more than one gap or conflict competes for the last slots, keep the ones the posting weighs most.

## Defaults (not asked)

State them in the plan at the gate; the user can change them there.

| Setting | Default |
|---|---|
| Length | Résumé one page. CV one page for under five years of experience, otherwise two |
| Personal details | Name, e-mail, phone, city, LinkedIn or portfolio if the sources have it. No photo, date of birth or full address unless the posting asks |
| References | "Available on request" ("Oppgis ved forespørsel") |
| Written standard | Bokmål, unless the user's own documents are in nynorsk |
| Low-severity gaps in the timeline | Left unexplained; mentioned in the plan so the user can object |
| Unconfirmed additions (a skill with no role behind it) | Left out until the user gives detail |

Ask these in chat at the gate only when the posting or the sources make the default wrong: a work permit or licence the posting requires and no source shows, a mix of bokmål and nynorsk in the sources, a photo requested.

## Reading the answers

The **Copy answers** button produces lines such as:

```
level_en: B (B2, clear and direct)
remove: A (Skill-level bars), C (Hobbies section)
missing: [own answer] Terraform, used at Acme 2022–2023
```

Accept the same in looser form typed in chat. An option letter plus text means the option applies with the detail given. If a question is unanswered, apply the recommended option when there is one; otherwise ask it in chat before the gate.
