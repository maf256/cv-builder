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

## cv.md: the full CV

Order: name and contact line, summary, experience, education, courses and certifications, skills, languages, then volunteering and references if used. Put education before experience when the user is a recent graduate or the posting weighs the degree more than the work history.

- **Summary**: two or three sentences of fact: current role or field, years in it, the two or three qualifications the posting asks for that the user has. Leave it out when the tone is brief and it would only repeat the first entry.
- **Experience**: newest first. Each entry has title, employer, dates, place, and two to five bullets. Give recent and relevant roles more bullets. Older or unrelated roles that are kept get one line or none.
- **Education**: degree, institution, dates. Add the thesis or main subjects only when they answer a requirement.
- **Skills**: grouped by kind in plain lines, for example `- Programming: Python, SQL, TypeScript`. List only skills the ledger supports. No self-ratings, bars or stars.
- **Languages**: language and level. Use CEFR levels or the standard terms (morsmål, flytende; native, fluent) and the test name when there is one (Norskprøve B2, IELTS 7.5).
- Length follows the user's answer to `length`.

## resume.md: one page

The same facts, cut to what this posting needs. It must fit one A4 page when rendered.

- Summary of at most two sentences, or none.
- The three or four most relevant roles, two or three bullets each. Earlier roles become one line under an "Earlier roles" / "Tidligere stillinger" entry, or are dropped.
- Highest degree and the certifications the posting names.
- One skills block with the posting's keywords the user holds.
- Languages on one line.
- No references section.

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

- One page; word count by the chosen tone (`writing-rules.md`).
- Do not repeat the CV. Pick the two facts that matter most and say what they mean for this employer.
- Use the posting's reference number in the heading when it has one.
- Salutation and sign-off: English "Dear <name>," / "Kind regards,"; Norwegian "Hei <fornavn>," / "Med vennlig hilsen". If no contact is named, address the team or department named in the posting.
- End on the last piece of content. No sentence about hoping to hear back.

## Norwegian conventions

- A Norwegian CV is one to two pages. Reference letters (attester) and diplomas (vitnemål) are sent as separate attachments when the posting asks for them; the CV does not reproduce them.
- Date of birth and a photo are optional and uncommon in the public sector. Follow the user's answer to `personal`.
- References: "Oppgis ved forespørsel" is accepted. If listed, give name, title, employer, phone.
- Foreign degrees: keep the original name and add the Norwegian equivalent in brackets only when the user has a recognition decision (HK-dir, formerly NOKUT) or states the equivalence.
- Norwegian language level matters to many employers. State it with its evidence (Norskprøve, Bergenstest, completed course level).
