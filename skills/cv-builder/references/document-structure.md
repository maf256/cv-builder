# Document structure

Write each document as Markdown using only the elements below. `scripts/render_docs.py` converts them to Word, HTML and PDF with one fixed style, so every run looks the same and the result stays readable by an ATS: one column, real text, no tables, no images, no icons.

## Markdown subset

| Element | Use |
|---|---|
| `# Name` | Once, first line: the person's name |
| A plain line directly under `#` | Contact line; separate items with ` · ` |
| `## Section` | Section headings |
| `### Entry` | A role, degree or course: `### Title, Employer` |
| `*text*` alone on the line under `###` | Dates and place: `*03.2021–06.2023 · Bergen*` |
| `- text` | Bullets |
| Plain paragraphs | Summary, cover-letter body |
| `**bold**`, `[text](url)` | Sparingly; links for e-mail, LinkedIn, portfolio |
| Two trailing spaces | Line break inside a paragraph (address block, sign-off) |

No tables, images, HTML, nested lists or horizontal rules.

## Section headings

Use these names. ATS parsers look for them.

| English | Norwegian |
|---|---|
| Summary | Profil |
| Experience | Arbeidserfaring |
| Education | Utdanning |
| Courses and certifications | Kurs og sertifiseringer |
| Skills | Kompetanse |
| Languages | Språk |
| Volunteering | Verv og frivillig arbeid |
| References | Referanser |

## resume.md: the résumé (CV)

The résumé is the one CV document. In Norwegian it is the "CV". There is no separate long version.

Order: name and contact line, summary, experience, education, courses and certifications, skills, languages, then volunteering and references if used. Put education before experience when the user is a recent graduate or the posting weighs the degree more than the work history.

- **Length**: one A4 page by default, about 450 words. Two pages only when the history needs it and the user agreed in the plan at the gate, about 900 words.
- **Summary**: one or two sentences of fact: current role or field, years in it, the qualifications the posting asks for that the user has. Leave it out when the tone is brief and it would only repeat the first entry.
- **Experience**: newest first. Each entry has title, employer, dates, place, and two to four bullets. Give recent and relevant roles more bullets. Older or unrelated roles that are kept become one line under an "Earlier roles" / "Tidligere stillinger" entry, or are dropped.
- **Education**: degree, institution, dates. Add the thesis or main subjects only when they answer a requirement.
- **Skills**: grouped by kind in plain lines, for example `- Programming: Python, SQL, TypeScript`. List only skills the ledger supports, preferring the posting's keywords. No self-ratings, bars or stars.
- **Languages**: language and level. Use CEFR levels or the standard terms (morsmål, flytende; native, fluent) and the test name when there is one (Norskprøve B2, IELTS 7.5).
- No references section unless the user asked for one.

### List layout (checked by the lint)

Education, Courses and certifications, and Languages follow one rule, by the number of entries in the section. Exactly three counts as three or fewer.

| Entries | Layout |
|---|---|
| Three or fewer | One entry per line: a bullet, or a `###` entry for a degree or course |
| More than three | Everything on one line, entries separated by semicolons. Languages may use commas when each level is in brackets |

```
## Languages
- English (native)
- Norwegian (B2)

## Languages
English (native), Norwegian (B2), Spanish (A2), German (A1)

## Courses and certifications
Norskprøve B2, 2024; AWS Solutions Architect, 2024; Scrum Master, 2022; First aid, 2023
```

## cover-letter.md

Structure:

```
# Name
Contact line

Place, date

Employer
Attn. contact person (if the posting names one)

## Application for <role> (Søknad på stillingen som <rolle>)

Salutation

Paragraph 1: the role applied for and the strongest reason the user fits it, stated as a fact.
Paragraph 2: one or two pieces of evidence from the user's history that answer the posting's main requirements.
Paragraph 3: why this employer, from the user's own answer and the research.
Paragraph 4 (optional): practical matters: start date, relocation, a gap or career change explained in one sentence.

Sign-off
Name
```

- One page; word count and voice by the chosen tone (`writing-rules.md`). The default is friendly and conversational.
- Do not repeat the CV. Pick the two facts that matter most and say what they mean for this employer.
- Use the posting's reference number in the heading when it has one.
- Salutation and sign-off by tone. Friendly (default): "Hi Kari," / "Best,"; "Hei Kari," / "Hilsen". Neutral or brief: "Dear Kari Hansen," / "Kind regards,"; "Hei Kari," / "Med vennlig hilsen". Formal: "Dear Ms Hansen," / "Yours sincerely,"; "Hei Kari Hansen," / "Med vennlig hilsen". If no contact is named, address the team or department named in the posting.
- End on the last piece of content. No sentence about hoping to hear back and no summing-up line.

## Norwegian conventions

- A Norwegian CV is one to two pages; here it is one unless the user chose two. Reference letters (attester) and diplomas (vitnemål) are sent as separate attachments when the posting asks for them; the CV does not reproduce them.
- Date of birth and a photo are optional and uncommon in the public sector. Follow the user's answer to `personal`.
- References: "Oppgis ved forespørsel" is accepted. If listed, give name, title, employer, phone.
- Foreign degrees: keep the original name and add the Norwegian equivalent in brackets only when the user has a recognition decision (HK-dir, formerly NOKUT) or states the equivalence.
- Norwegian language level matters to many employers. State it with its evidence (Norskprøve, Bergenstest, completed course level).
