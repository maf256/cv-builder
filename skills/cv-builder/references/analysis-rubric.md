# Analysis rubric (Phase 1)

The analysis must give the same result for the same inputs. Follow the steps in order and use only the categories, statuses and check ids defined here.

## 1. Fact ledger

Before comparing anything, list every fact in the sources. Keep the ledger in your working notes; it is the reference for every later step and for Phase 2.

For each entry record: what it is, the dates exactly as written, and the source file.

- Roles: employer, title, start and end (month and year where given), location, tasks, results, tools.
- Education: institution, degree or programme, dates, grade if stated.
- Courses and certificates: name, issuer, date, expiry if any.
- Skills: each tool, method or language, and where it is evidenced (a role, a course, or only a skills list).
- Languages: level as stated, and the evidence (test, certificate, self-assessment).
- Personal details: name spelling, contact details, work permit or residence status if stated.

When two sources disagree, record both versions. Do not pick one.

## 2. Requirements

Extract every requirement from the posting as one short line each. Split compound requirements ("bachelor's degree and three years' experience" is two). Assign each to exactly one category:

| Category | What goes here |
|---|---|
| `must` | Skills, tools and qualifications the posting states as required, or lists without qualification under requirements |
| `experience` | Years of experience, seniority, industry or domain background, type of role held before |
| `nice` | Anything marked as an advantage, preferred, a plus ("en fordel", "ønskelig") |
| `education` | Degrees, certifications, licences, authorisations |
| `language` | Spoken and written language requirements |

Rate each requirement against the ledger:

| Status | Rule |
|---|---|
| `met` | A source shows it directly: a role where it was used, a certificate, a degree |
| `partial` | Related but not the same (adjacent tool, shorter duration, lower level), or claimed in a skills list with no role or course behind it |
| `missing` | No source supports it |

Write the evidence for each rating: for `met` and `partial`, where it appears; for `missing`, what is absent. Rate what the sources show, not what the user probably has. Gaps the user may be able to fill become form questions.

## 3. Keywords

List the terms an ATS or recruiter would search for: tools, technologies, methods, certifications, job titles, domain terms. Take them from the posting's wording. Aim for 15 to 30. Exclude soft-skill adjectives; they are not searchable evidence.

Mark each `high` (in the title, the requirements, or repeated) or `normal`, and whether the current CV contains it. Count a keyword as found only if the term or its standard abbreviation appears in the CV text.

## 4. ATS checks

Rate the user's current CV on exactly these ten checks, in this order, each `pass`, `warn` or `fail`, with a one-line note. If the user attached several CVs, rate the most recent and say which.

| id | Pass when |
|---|---|
| `file_format` | The file is a text-based PDF or DOCX |
| `text_layer` | All text can be selected and extracted; nothing is an image or scan |
| `single_column` | One column; extracted text reads in the right order |
| `no_tables_graphics` | No content in tables, text boxes, icons, charts or skill bars |
| `standard_headings` | Sections use conventional names (Experience, Education, Skills / Erfaring, Utdanning, Kompetanse) |
| `contact_in_body` | Name, e-mail and phone are in the body, not in a header, footer or image |
| `date_format` | Every role and degree has dates in one consistent format |
| `reverse_chronological` | Newest first within each section |
| `title_alignment` | The CV's headline or most recent title uses terms close to the posting's title, where that is truthful |
| `plain_characters` | Standard fonts and bullets; no symbols or ligatures that extract as garbage |

Use `warn` when a check is partly satisfied or cannot be determined from the file.

## 5. Contradictions

Compare the ledger against itself and against the posting. Report each finding with the sources involved and a severity.

Check for:

- Dates that differ between documents for the same role or degree.
- A title or employer name written differently in different documents.
- Roles that overlap in time without explanation.
- Gaps longer than six months with nothing recorded.
- A degree's dates that do not fit the certificate or transcript.
- Skills listed that no role, course or project supports.
- Language levels that differ between documents, or that the user's own writing contradicts.
- Stated years of experience that do not add up from the dated roles.
- Details that differ between a CV and a profile or older CV the user attached.

Severity is `high` when a recruiter or background check would notice it (dates, titles, degrees) and `low` otherwise.

## 6. Remove, add, rewrite

- **Remove**: content with no bearing on this posting or that weakens the application. Typical cases: roles older than 15 years unrelated to the role, school-level education when a degree exists, outdated tools, hobby lists, objective statements, self-rated skill bars, duplicate entries, personal details the market does not expect. Give the reason for each item.
- **Add**: content that exists in the sources but not in the current CV (a certificate attached but not listed, a course that answers a requirement), and items that need the user's confirmation before they can be used (set `needs_confirmation` to true).
- **Rewrite**: entries that are relevant but written so that the relevance is hidden, for example a bullet that lists duties without the tool the posting asks for when the source shows the tool was used.

Describe the change; do not write the new text in Phase 1.

## 7. Research

Read the employer's own site and the full posting. Record only findings that will change what gets written: what the team or product does, terms the employer uses for the role, the application language, required attachments, the named contact. Each finding carries its source URL and a note on where it will be used. Search with the employer and role only, never with the user's details.

## 8. Scores

`scripts/build_report.py` computes these. The formulas are here so the user can be told what a number means and so the scores can be computed by hand if Python is unavailable.

**Match score (0 to 100).** Each requirement scores 1 for `met`, 0.5 for `partial`, 0 for `missing`. Each category's result is the average of its requirements. Categories are weighted:

| Category | Weight |
|---|---|
| `must` | 50 |
| `experience` | 20 |
| `nice` | 15 |
| `education` | 10 |
| `language` | 5 |

Match = sum of (weight × category average) ÷ sum of the weights of the categories that have at least one requirement, × 100, rounded.

Bands: 75 and above is a strong match, 50 to 74 a partial match, below 50 a weak match.

**Keyword coverage (0 to 100).** `high` keywords count double. Coverage = weight of found keywords ÷ weight of all keywords × 100, rounded.

**ATS score (0 to 100).** Checks score 1 for `pass`, 0.5 for `warn`, 0 for `fail`. ATS = 0.6 × keyword coverage + 0.4 × (average of the ten checks × 100), rounded.

Verdict: 75 and above is likely to pass, 50 to 74 is at risk, below 50 is likely to be filtered out. If `text_layer` fails, the verdict is likely to be filtered out whatever the score, because the file cannot be read.

Tell the user this is an estimate. ATS products differ, and most rank applications for a recruiter instead of rejecting them outright.
