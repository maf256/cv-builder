---
name: cv-builder
description: Interactive CV builder that tailors a résumé (CV) and cover letter to one job posting, in English, Norwegian or both. It first analyses the user's attached CVs, certificates and course records against the posting (match score, ATS check, contradictions, what to remove and add), shows the analysis as an HTML report with a question form, and writes the documents only after the user answers and confirms. Use when the user runs /cv-builder or asks to tailor, review or build a CV, résumé, cover letter, søknad or søknadsbrev for a job application.
---

# CV Builder

This skill turns a person's existing career documents and one job posting into a tailored résumé (the CV) and cover letter. It runs in two phases with a gate between them:

- **Phase 1, analyse.** Read everything, compare it with the posting, and report. Nothing is rewritten in this phase.
- **Phase 2, write.** Runs only after the user has answered the question form and confirmed. It produces the documents in an output directory.

File paths below are relative to this skill's directory. Run the scripts with `python3`. On Windows the command is `python` or `py -3`; use whichever runs Python 3.

## Rules that hold in every step

1. **No buzzwords, no filler and no machine-written tells, anywhere.** This covers the CV, the résumé, the cover letter, the report and your own chat messages. That includes em dashes and contrast framing such as "it's not X, it's Y". Read `references/writing-rules.md` before writing any text for the user, and run `scripts/lint_text.py` on every document you produce. A document that fails the lint is not finished.
2. **Never invent.** Every fact in an output document must trace to an attached source or to an answer the user gave in the form. If a claim has no source, ask; do not round up job titles, dates, skill levels, grades or numbers. Where the posting asks for something the user lacks, the documents leave it out. They do not imply it.
3. **No edits before the gate.** Phase 1 proposes changes; it does not write CV text. Do not show rewritten bullets or draft paragraphs until Phase 2.
4. **One language choice drives everything.** The answer to step 0 sets the conversation language, the report language and the output documents.
5. **Personal data stays local.** Fetch the job posting and research the employer, but never put the user's name, contact details or document contents into a search query or any external service.

## Step 0: language

The first thing you do after the command, before reading anything, is ask one question:

> Norsk, English, or both? / Norsk, engelsk eller begge?

Use the question tool if the session has one; otherwise ask in plain text and wait.

| Answer | Conversation and report | Documents written in Phase 2 |
|---|---|---|
| Norwegian | Norwegian (bokmål, unless the user's own documents are in nynorsk) | Norwegian only |
| English | English | English only |
| Both | The language the user has been writing in; English if unclear | One full set in each language |

From here on, every question, message and report label is in the conversation language.

## Step 1: gather the inputs

Look at what arrived with the command:

- **Attachments.** CVs and résumés, diplomas, school certificates, transcripts, course certificates, reference letters (attester), and anything with personal details. These are the main source of truth about the user. Read every one in full, including scanned PDFs and images.
- **The job posting.** Usually one link. Fetch it and read the whole posting, including the employer section and the application instructions (deadline, required attachments, application language, contact person).

If something is missing, ask for it and wait:

- No attachments: ask the user to attach their current CV and any certificates. If they have no CV at all, collect their history by interview, one topic at a time (work, education, courses, languages, skills), and treat their answers as the source.
- No job posting: ask for the link or the pasted text. This skill tailors to one posting; do not proceed without it.
- The link cannot be fetched (login wall, expired posting): say so and ask the user to paste the text.

If there are several postings, ask which one to target. Run the skill once per posting.

## Step 2: analyse (Phase 1)

Read `references/analysis-rubric.md` and follow it. It defines the fact ledger, how requirements are extracted and rated, the fixed ATS checks, and how contradictions are found. In short, you produce:

1. A **fact ledger**: every dated role, degree, course, certificate, skill and language level, each with the file it came from.
2. The posting's **requirements**, each rated met, partial or missing, with the evidence.
3. **Contradictions** between the sources: dates that disagree, titles that differ between documents, overlapping periods, unexplained gaps, skills claimed with no supporting role, language levels that differ.
4. An **ATS assessment** of the current CV against the fixed checklist, and keyword coverage against the posting.
5. **What to remove**: content that does not serve this posting, with the reason for each item.
6. **What to add or rewrite**: content that exists in the sources but is missing or buried in the CV, and gaps the user may be able to fill.
7. **Research** for the writing phase: what the employer does, the terms it uses for this role, anything in the posting or on the employer's site that should shape the cover letter. Keep each finding with its source URL.

Do not compute the scores yourself. The report script computes them from your ratings so that the numbers mean the same thing on every run.

## Step 3: build the report

The report is always the same HTML page. Only the data changes. It is short on purpose: a one-sentence verdict, three fixes, four numbers, then the form.

1. Get the folder name from the script, never by hand:

   ```bash
   python3 scripts/slug.py "<full name>" "<job title>" "<company>"
   ```

   It prints `fullname-jobtitle-company`, lower-case ASCII, for example `sam-example-data-analyst-acme-energi-as`. Create `cv-output/<that name>/` in the user's working directory.
2. Write `report-data.json` there, following `references/report-data.md` exactly. Include the questions from step 4.
3. Run:

   ```bash
   python3 scripts/build_report.py cv-output/<name>/report-data.json
   ```

   This validates the data, computes the scores, and writes two files next to the JSON: `report.html` (standalone, for a browser) and `report-chat.html` (the same page, themed for inline display). Fix any validation error it prints and run it again.
4. **Show the report in the chat. Do not ask the user to open a file.**
   - If your host can render HTML inline, use it with `report-chat.html`. In T3 Code, load `html_preview` and `html_render` with ToolSearch, call `html_preview` with the file path to get `contentHeight`, then call `html_render` with the same path and `height` set to `contentHeight` (at most 2000).
   - If the host has no inline rendering, open `report.html` (`open` on macOS, `xdg-open` on Linux, `start` on Windows) and give its path.

Never hand-write the report HTML and never edit `assets/report-template.html` during a run. If Python is unavailable, compute the scores by the formulas in `references/analysis-rubric.md`, add them to the JSON under `scores`, and substitute the JSON for the `/*__CV_DATA__*/` marker in a copy of the template.

After the report, write one line in chat: that the form at the bottom needs answers. Do not repeat the report's contents.

## Step 4: the question form

The form is the last section of the report. It must be quick to fill in: **at most 8 questions**, each question under 90 characters, each option under 60. Build the list from `references/form-questions.md`, which sets the fixed questions, the order of priority when there are too many, and the defaults that are not asked.

Every question has lettered choices (A to D) and a one-line field for the user's own answer. Mark the choice you would pick as recommended when you have a basis for it.

The user answers in the report and presses **Copy answers**, then pastes the result into the chat. Also accept answers typed directly, for example `1B, 2A, 4: remove only the 2009 internship`. If the copy button does not work in the host, the user can type the letters.

## Step 5: the gate

When the answers arrive:

1. Save them as `answers.md` in the output directory.
2. If an answer is ambiguous, conflicts with a source, or adds a skill or role with no detail (employer, dates, what they did), ask a follow-up. New experience needs enough detail to write a truthful entry.
3. State the plan in a few lines: which documents, which languages, language level and tone for each, what will be removed, what will be added.
4. Ask the user to confirm. Do not start Phase 2 until they say yes.

## Step 6: write (Phase 2)

Read `references/writing-rules.md` and `references/document-structure.md` first.

For each output language, write two documents as Markdown. There is no separate long CV:

| File | What it is |
|---|---|
| `resume.md` | The résumé, which is the CV: only what matters for this posting, one page by default |
| `cover-letter.md` | The cover letter (søknadsbrev), addressed to this employer and this role |

Layout of the output directory:

```
cv-output/<name>/
  report.html
  report-data.json
  answers.md
  en/  resume.md  cover-letter.md  (+ .docx, .html and .pdf for each)
  no/  resume.md  cover-letter.md  (+ .docx, .html and .pdf for each)
```

Create only the language folders the user chose.

When both languages are chosen, write each set in its own language from the facts. Do not translate one into the other sentence by sentence; names of employers, degrees and certificates stay in their original form, with a short explanation in brackets where the reader would not know them.

Write to the language level the user chose for each language (`references/writing-rules.md` describes what each CEFR level means on the page) and in the tone they chose. The tone applies to the cover letter, which defaults to friendly and conversational and must read like a person wrote it (`Cover letter voice` in `writing-rules.md`). The résumé stays factual whatever the tone.

Then render and check:

```bash
python3 scripts/render_docs.py cv-output/<name>
python3 scripts/lint_text.py cv-output/<name>
```

`render_docs.py` turns each Markdown file into a Word file (`.docx`) and a single-column HTML file, both readable by an ATS, and into a PDF when Chrome, Chromium or Edge is installed. `lint_text.py` reports every banned word, dash, machine-written pattern and list-layout error (Languages, Education, Courses) with its file and line. Rewrite each flagged sentence, then run both again until the lint passes. Do not silence a hit by swapping in a synonym with the same emptiness; say the concrete thing or delete the sentence.

## Step 7: verify and hand over

Before you tell the user it is done, check each document against this list:

- Every fact is in the ledger or in `answers.md`.
- Every removal the user approved is gone, and nothing they wanted kept was dropped.
- The contradictions are resolved the way the user said.
- Dates, titles and employer names are identical across the résumé and the cover letter, and across both languages.
- The résumé fits one page, or two if the user agreed to that at the gate. `render_docs.py` prints the PDF page counts; without PDFs, keep it under about 450 words (900 for two pages).
- The posting's keywords appear where the user's history supports them, and nowhere else.
- The lint passes.

Tell the user they can run `/reload` once they have read the documents (or edited them) to get a fresh analysis with new scores next to the phase one numbers.

Then report in chat: the output path, the list of files, what changed against the original CV in a few lines, and anything the user still has to do themselves (for example attach diplomas the posting asks for, or fill in a referee's phone number). Tell them which file to upload: the `.docx` is the safest for an ATS, the PDF for e-mail. If PDFs could not be made, say so and tell them to print the HTML files to PDF from a browser.
