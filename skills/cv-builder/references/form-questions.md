# The question form

The form closes Phase 1. Its answers, together with the sources and the posting, are everything Phase 2 may use.

Write each question in the conversation language. Each has lettered options and a free-text field. Keep option labels short and concrete, and fill them from the analysis: an option should name the actual item, date or skill, not a placeholder. Keep the whole form to 16 questions or fewer; if the analysis triggers more, merge related ones.

Put the questions in the order below.

## Fixed questions (every run)

| id | Topic | Question | Options |
|---|---|---|---|
| `level_en` / `level_no` | Language level | Which level should the documents in this language be written at? One question per output language | A: B1, short simple sentences. B: B2, clear and direct. C: C1, fluent professional. D: C2, native-level. Recommend the level the sources document for the user; a CV written above the level the user speaks at interview works against them |
| `tone` | Tone | How should the documents read? | A: Brief and factual, shortest possible. B: Neutral professional. C: Warm and personal in the cover letter, factual in the CV. D: Formal |
| `length` | Length | How long should the full CV be? (The résumé is always one page.) | A: One page. B: Two pages. C: As long as the relevant history needs |
| `remove` | Remove | Which of the proposed removals do you approve? | Multi-select. One option per proposed removal, naming the item. If there are more than six, group the minor ones into one option |
| `new_skills` | New skills | Do you have skills, tools or certificates that are in none of the documents you sent? | A: No, the documents are complete. Free text: list them, with where each was used or learned |
| `new_experience` | New experience | Is there work, projects, volunteering or study missing from the documents? | A: No. Free text: employer or context, dates, what you did |
| `motivation` | Cover letter | Why this employer and this role? | Two to four options drawn from the research (a product, a field of work, a stated need in the posting), plus free text. The cover letter needs the user's actual reason; do not guess it |
| `personal` | Personal details | Which details should the CV show besides name, e-mail and phone? | Multi-select. A: City. B: Full address. C: Date of birth. D: Photo. E: LinkedIn or portfolio link. For Norwegian applications recommend A and E unless the posting asks for more |
| `references` | References | How should references be handled? | A: "Available on request" ("Oppgis ved forespørsel"). B: List them; write names, titles and contact details in the text field. C: Leave the section out |

## Conditional questions

Add these when the analysis triggers them.

| id | When | Question | Options |
|---|---|---|---|
| `gap_<n>` | A `must` or `experience` requirement is rated `missing` or `partial` | Names the requirement and asks what the user can truthfully claim | A: Yes, I have this; I will describe where and when in the text field. B: Some exposure; describe it. C: No. D: No, but I am learning it now; describe the course or project |
| `conflict_<n>` | Each contradiction of severity `high`, and `low` ones where the right version is not obvious | States both versions and their sources | One option per version, plus free text for "neither, the correct one is..." |
| `timeline_<n>` | A gap longer than six months | Asks what the user did in that period and whether to show it | A: Show it; describe it in the text field. B: Leave it unexplained. C: Explain it in the cover letter only |
| `add_<n>` | An item under `add` has `needs_confirmation` true | Asks whether the item is correct and may be used | A: Yes, use it. B: Yes, with a correction; write it. C: No |
| `title` | The user's titles differ from the posting's title for the same kind of work | Asks which headline to use | Options listing the truthful candidates. Never offer a title the user has not held as a past job title; a headline may name the target field |
| `nb_nn` | Norwegian output, and the sources mix bokmål and nynorsk | Which written standard? | A: Bokmål. B: Nynorsk |
| `permit` | The posting requires a work permit, licence, authorisation or security clearance and no source shows it | Asks for the status | A: I have it; state the type and expiry. B: Applied for. C: No |

## Reading the answers

The **Copy answers** button produces lines such as:

```
level_en: B
remove: A, C
new_skills: [own answer] Terraform, used at Acme 2022–2023
```

Accept the same in looser form typed in chat. An option letter and free text together mean the option applies with the detail given. If a required question is unanswered, ask it in chat before the gate.
