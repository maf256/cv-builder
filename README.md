# cv-builder

A Claude skill that tailors a CV, résumé and cover letter to one job posting, in English, Norwegian or both.

It works in two rounds. First it reads your documents and the posting and reports what it found. It rewrites nothing until you have answered its questions and confirmed.

## What it does

Run `/cv-builder` with your CV, any certificates or transcripts, and a link to the job posting.

**Round 1: analysis**

1. Asks whether to continue in Norwegian, English or both. The answer sets the conversation language and the language of the documents.
2. Reads every attachment and the posting.
3. Builds an HTML report, the same layout every time:
   - match score against the posting's requirements, with the evidence for each
   - ATS estimate: keyword coverage and ten format checks
   - contradictions between your documents (dates, titles, gaps)
   - what to remove, what to add, what to rewrite
   - research on the employer for the cover letter
4. Ends the report with a form. Each question has lettered choices and a field for your own answer: language level (B1 to C2), tone, length, removals, new skills, new experience, and questions raised by the analysis. Press **Copy answers** and paste the result into the chat.

**Round 2: writing**

After you confirm, it writes into `cv-output/<company>-<role>/`:

```
report.html
answers.md
en/  cv  resume  cover-letter     (.md, .docx, .html, .pdf)
no/  cv  resume  cover-letter     (.md, .docx, .html, .pdf)
```

Only the languages you chose are written. PDFs are made when Chrome, Chromium or Edge is installed; the Word and HTML files are always made.

## Rules the skill follows

- **No buzzwords or filler.** A lint script checks every document against a list of banned words in both languages (`references/banned-words.txt`), and the run is not finished until it passes.
- **Nothing invented.** Every fact comes from your documents or your form answers.
- **No edits before you confirm.**
- **Your data stays local.** The skill fetches the posting and researches the employer; it does not send your details anywhere.

## Install

### As a plugin (Claude Code)

```
/plugin marketplace add maf256/cv-builder
/plugin install cv-builder@cv-builder
```

Then run `/cv-builder:cv-builder`.

### As a personal skill

```bash
git clone https://github.com/maf256/cv-builder.git
mkdir -p ~/.claude/skills
cp -r cv-builder/skills/cv-builder ~/.claude/skills/
```

Then run `/cv-builder` in any project. To install it for one project only, copy the folder to `.claude/skills/` in that project.

### Claude.ai and Claude Desktop

Zip the `skills/cv-builder` folder and upload it under Settings → Capabilities → Skills.

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
    document-structure.md       CV, résumé and cover letter structure; Norwegian conventions
    banned-words.txt            the lint list, English and Norwegian
  assets/report-template.html   the report page
  scripts/
    build_report.py             validates data, computes scores, fills the template
    render_docs.py              Markdown to Word, HTML and PDF
    lint_text.py                banned-word check
examples/acme-data-analyst/     a fictional run: report data, a résumé, a cover letter
```

## Try the report without Claude

```bash
python3 skills/cv-builder/scripts/build_report.py examples/acme-data-analyst/report-data.json
open examples/acme-data-analyst/report.html
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
