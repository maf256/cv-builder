---
name: reload
description: Side phase of /cv-builder. After the résumé and cover letter are written, re-runs the analysis on those documents and shows a fresh one-sentence summary with new scores next to the phase one scores. Changes nothing. Use when the user runs /reload, or asks to re-check, re-score or re-analyse their finished CV after /cv-builder.
---

# Reload

A read-only re-check. `/cv-builder` analysed the user's old CV in phase one and wrote new documents in phase two. `/reload` analyses the new documents the same way and shows what changed. It asks no questions, shows no form, and edits no document.

Run the scripts with `python3`. On Windows the command is `python` or `py -3`; use whichever runs Python 3.

The scripts, template and rubric belong to the sibling skill `cv-builder` (the folder next to this one). Paths below are relative to it.

## Rules

- Same writing rules as `/cv-builder`: no buzzwords, no filler, no em dashes, no "it's not X, it's Y". Read `cv-builder/references/writing-rules.md` before writing the summary.
- Judge, do not flatter. A score that went up because the documents improved is good news; a number that did not move is reported as it is.
- Never edit the documents here. If something is still wrong, say what and offer to fix it afterwards.

## Steps

1. **Find the run.** Look in `cv-output/` in the working directory for folders that contain `report-data.json` and at least one `resume.md` under `en/` or `no/`.
   - One match: use it. Several: list them, newest first, and ask which.
   - A folder with `report-data.json` but no documents: phase two has not run. Say so and stop; the user needs to finish `/cv-builder`.
   - No folder: tell the user to run `/cv-builder` first.
2. **Language.** Use `meta.ui_lang` from `report-data.json`. Do not ask again.
3. **Read** everything the analysis rests on:
   - `report-data.json` (phase one: requirements, keywords, contradictions, scores) and `answers.md`
   - the current `resume.md` and `cover-letter.md` in each language folder. If the user says they edited the Word or PDF file instead, read that file and use it as the text
   - the source files listed in `meta.sources`, when they are still available, to check the new documents against the facts
   - the posting at `meta.posting_url`; if it cannot be fetched, rely on the requirements saved in `report-data.json`
4. **Re-run the analysis** as defined in `cv-builder/references/analysis-rubric.md`, with these rules:
   - Keep the phase one requirements, with the same text and categories, so the scores compare. Add a requirement only if the posting has changed.
   - Rate each as `met` only when the new CV shows it and a source or a form answer supports it. A claim the sources do not support is a new `high` contradiction.
   - Re-check the keywords against the résumé in the language the posting is written in.
   - Rate the ten ATS checks on the new résumé: headings, dates, single column, title alignment, and the rest. For the Word and HTML files the renderer produces, check the file rather than assuming.
5. **Check the documents against the run.** Each failure becomes a contradiction, a still-open fix, or a `remove`, `add` or `rewrite` item:
   - every approved removal is gone, and every approved addition is present
   - every answer in `answers.md` shows up where it should
   - dates, titles and employers match across the résumé, the cover letter and both languages
   - nothing appears in the documents that no source supports
   - the résumé fits one page, or two if the plan said so: run `python3 scripts/render_docs.py <folder>` and read the page counts, or keep it under about 450 words when no PDF can be made
   - the lint passes, including the list layout of Languages, Education and Courses: `python3 scripts/lint_text.py <folder>`. List any hits as an open fix
   - the cover letter reads like a person wrote it: no contrast framing, no tidy closing line, varied sentence length, a concrete detail or two
6. **Write `reload-data.json`** in the same folder, following `cv-builder/references/report-data.md` with these differences:
   - `meta.mode` is `"reload"`
   - `summary`: one sentence under 160 characters that states the result, for example "Match up 24 points; the Nordlys end date still differs between the résumé and the letter."
   - `top_fixes`: what is still open, from zero to three items, most important first. Leave it empty when nothing is
   - `contradictions`: the ones that remain or are new, not the resolved ones
   - `remove`, `add`, `rewrite`: only what is still worth changing; usually empty
   - `research`: an empty list
   - `questions`: an empty list
7. **Build and show it.**

   ```bash
   python3 scripts/build_report.py cv-output/<name>/reload-data.json
   ```

   Check the numbers in your summary against the script's "Since phase one" line. If the summary quotes a change that is not what the script printed, fix the summary and build again.

   The script reads the phase one scores from `report-data.json` in the same folder, computes the new ones, and writes `reload.html` and `reload-chat.html` with a "since phase one" change on each number. Show `reload-chat.html` in the chat the same way `/cv-builder` shows its report (`html_preview` for the height, then `html_render`); without inline rendering, open `reload.html`.
8. **Close.** One line in chat. If items are still open, ask whether to fix them. On a yes, edit the Markdown documents, run `render_docs.py` and `lint_text.py`, and run `/reload` again. Without a yes, change nothing.

Each run overwrites `reload-data.json`, `reload.html` and `reload-chat.html`. The comparison is always against phase one, so repeated reloads show the total change.
