# cv-builder

A Claude skill that tailors a résumé (CV) and cover letter to one job posting, in English, Norwegian or both.

It works in two rounds. First it reads your documents and the posting and reports what it found. It rewrites nothing until you have answered its questions and confirmed.

## What it does

Run `/cv-builder` with your CV, any certificates or transcripts, and a link to the job posting.

**Round 1: analysis**

1. Asks whether to continue in Norwegian, English or both. The answer sets the conversation language and the language of the documents.
2. Reads every attachment and the posting.
3. Shows a short report **in the chat**, in hosts that render HTML inline (T3 Code does). Elsewhere it opens the file in your browser. The layout is the same every time:
   - a one-sentence verdict and the three fixes that matter most
   - four numbers: match score, ATS estimate, keyword coverage, contradictions
   - folded details: requirements with evidence, keywords, ATS checks, contradictions, what to remove, add and rewrite, employer research
4. Ends with a form of at most eight quick questions: language level (B1 to C2), cover letter tone, what to remove, anything missing, why this employer, and the contradictions and gaps the analysis found. Each has lettered choices and a one-line field for your own answer. Press **Copy answers** and paste the result into the chat.

Length, personal details and references are not asked; the skill picks sensible defaults and states them before it writes.

**Round 2: writing**

After you confirm, it writes into `cv-output/fullname-jobtitle-company/`, for example `cv-output/sam-example-data-analyst-acme-energi-as/`:

```
report.html
answers.md
en/  resume  cover-letter     (.md, .docx, .html, .pdf)
no/  resume  cover-letter     (.md, .docx, .html, .pdf)
```

Only the languages you chose are written. PDFs are made when Chrome, Chromium or Edge is installed; the Word and HTML files are always made.

## /reload

After phase two, run `/reload` for a fresh check of the finished documents. It analyses the new résumé and cover letter the same way phase one analysed the old CV, then shows a one-sentence summary and new scores with the change since phase one on each number. It asks nothing, shows no form and edits nothing. If something is still open it offers to fix it, and you can run `/reload` again afterwards. Output: `reload.html` in the same folder.

## Rules the skill follows

- **No buzzwords, filler or machine-written tells.** A lint script checks every document against a list of banned words in both languages (`references/banned-words.txt`), against em dashes and other dash substitutes, against patterns such as "it's not X, it's Y", and for list layout: Languages, Education and Courses go one per line up to three entries, and on one line beyond that. The run is not finished until it passes.
- **A cover letter that sounds like a person.** The default tone is friendly and conversational: first-name salutation, short common words, varied sentence length, one or two concrete details, no tidy closing line. The résumé stays factual.
- **Nothing invented.** Every fact comes from your documents or your form answers.
- **No edits before you confirm.**
- **Your data stays local.** The skill fetches the posting and researches the employer; it does not send your details anywhere.

## Install

### As a plugin (Claude Code)

```
/plugin marketplace add maf256/cv-builder
/plugin install cv-builder@cv-builder
```

Then run `/cv-builder:cv-builder`, and `/cv-builder:reload` after phase two.

### As a personal skill

```bash
git clone https://github.com/maf256/cv-builder.git
mkdir -p ~/.claude/skills
cp -r cv-builder/skills/cv-builder cv-builder/skills/reload ~/.claude/skills/
```

Then run `/cv-builder` in any project. To install it for one project only, copy the folder to `.claude/skills/` in that project.

### Claude.ai and Claude Desktop

Zip the `skills/cv-builder` and `skills/reload` folders (one zip each) and upload them under Settings → Capabilities → Skills.

## Requirements

- Python 3.8 or later (standard library only) for the report, the document renderer and the lint.
- Optional: Chrome, Chromium or Edge for PDF output.

## Layout

```
skills/cv-builder/
  SKILL.md                      the workflow
  references/
    analysis-rubric.md          how requirements, ATS checks and scores are defined
    report-data.md              the data format behind the report
    form-questions.md           the fixed and conditional form questions
    writing-rules.md            buzzword rule, language levels, tone
    document-structure.md       résumé and cover letter structure, list layout; Norwegian conventions
    banned-words.txt            the lint list, English and Norwegian
  assets/report-template.html   the report page (standalone and chat versions)
skills/reload/SKILL.md          /reload: re-analyses the finished documents
  scripts/
    build_report.py             validates data, computes scores, fills the template
    slug.py                     folder name: fullname-jobtitle-company
    render_docs.py              Markdown to Word, HTML and PDF
    lint_text.py                banned words, dashes, AI patterns, list layout
examples/sam-example-data-analyst-acme-energi-as/     a fictional run: report data, a résumé, a cover letter
```

## Try the report without Claude

```bash
python3 skills/cv-builder/scripts/build_report.py examples/sam-example-data-analyst-acme-energi-as/report-data.json
open examples/sam-example-data-analyst-acme-energi-as/report.html
```

## How the scores work

- **Match score**: each requirement counts 1 if met, 0.5 if partly met, 0 if missing. Categories are weighted: required skills 50, experience 20, preferred 15, education 10, languages 5.
- **ATS estimate**: 60% keyword coverage, 40% the ten format checks. ATS products differ, so this is an estimate.

The script computes both from the ratings, so a number means the same thing on every run.

## Customising

- Add or remove banned words in `references/banned-words.txt`.
- Change the document look in the `CSS` block and `write_docx` in `scripts/render_docs.py`.
- Change weights in `scripts/build_report.py` and `references/analysis-rubric.md` together.

## License

MIT
