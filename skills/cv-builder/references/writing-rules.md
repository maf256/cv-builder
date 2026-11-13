# Writing rules

These rules apply to every word the user reads: the CV, the résumé, the cover letter, the report, and chat messages.

## No buzzwords, no filler

A recruiter reads hundreds of applications that say the candidate is motivated, results-oriented and a team player. Those words carry no information, because anyone can write them and everyone does. They also take the space where a fact would go. The CV earns attention with what the person did, with which tools, for whom, and what came of it.

`references/banned-words.txt` lists words and phrases that must not appear, in English and Norwegian. `scripts/lint_text.py` checks for them. The list is a floor: the rule covers anything of the same kind, including words that are not on it.

What the rule excludes:

- **Self-praise adjectives.** Motivated, passionate, dynamic, hard-working, detail-oriented; engasjert, strukturert, løsningsorientert, selvgående. Show the behaviour in a fact or leave it out.
- **Inflated verbs.** Leveraged, spearheaded, utilized, synergized. Write used, led, built, wrote, sold, taught.
- **Empty claims.** "Proven track record", "excellent communication skills", "gode samarbeidsevner". If it matters, there is an event that shows it: "presented the quarterly results to 40 store managers".
- **Filler.** "Responsible for", "duties included", "in order to", "various", "ansvarlig for", "diverse arbeidsoppgaver". Start with the verb and name the thing.
- **Openers and closers that say nothing.** "I am writing to apply for", "I believe I would be a great fit", "Jeg viser til utlysningen", "Håper på positiv tilbakemelding".
- **Intensifiers and hedges.** Very, highly, extremely, really, quite; veldig, svært, meget.

A term from the posting that names a real tool, method or qualification is a keyword, not a buzzword. "Scrum", "HMS" and "ISO 27001" stay when the user's history supports them. If a banned word is part of an official name (a product, a course title, a job title on a contract), keep the name and pass it to the lint with `--allow`.

When the lint flags a sentence, do not swap in a synonym. Ask what fact the sentence was standing in for. Write that fact, or delete the sentence.

| Instead of | Write |
|---|---|
| Results-driven sales professional with a proven track record | Sold industrial pumps to 60 accounts in Western Norway, 2019–2024 |
| Responsible for managing a team | Led a team of six technicians |
| Excellent communication skills | Wrote the user manual for the booking system; trained 30 new employees |
| Jeg er en strukturert og løsningsorientert person | Innførte ny rutine for varemottak som kuttet feilplukk fra 40 til 12 i måneden |
| Ansvarlig for kundeoppfølging | Fulgte opp 120 bedriftskunder på telefon og e-post |

## Punctuation and AI patterns

Text that reads as machine-written gets discounted, and recruiters spot it fast. The lint catches the mechanical tells; the habits behind them are yours to avoid.

- **No em dashes, no spaced en dashes, no `--`, no spaced hyphens used as dashes.** Use a full stop, a comma or a colon, or split the sentence. The only dash allowed is the unspaced en dash inside a number range (`2021–2025`).
- **No contrast framing.** "It's not X, it's Y", "not just X but Y", "this isn't about X, it's about Y", "more than just X", and in Norwegian "det handler ikke om X, men om Y", "ikke bare X, men også Y". State Y and drop X.
- **No groups of three** adjectives or nouns by reflex. Use the number the facts give you.
- **No tidy closing line** that sums up the letter or restates the fit.
- **No exclamation marks, rhetorical questions, quotations or mottos.**
- **No stock openers** ("In today's…", "I'm excited to…", "I am writing to…") and no stock vocabulary (delve, pivotal, seamless, journey, tapestry).
- **Do not repeat a sentence shape.** If three sentences in a row start the same way or have the same length, rewrite one.

## Truth

- Use only the fact ledger and the form answers. A number appears in a document only if a source or the user gave it. Do not estimate percentages or team sizes.
- Describe what the person did at the level they did it. "Assisted with" stays "assisted with".
- Never upgrade a skill level, a language level, a title or a degree. A course is not a degree; an unfinished programme is listed as unfinished, with the credits earned.
- If a requirement is missing, the documents are silent on it. The cover letter may state what the user is doing about a gap only when the user said so in the form.

## Sentences

- One fact per bullet. Start with a past-tense verb for past roles, present tense for the current one. No pronoun in CV bullets.
- Name the tool, the quantity and the counterpart when the source gives them: what, with what, how much, for whom.
- Bullets do not end with a full stop. Paragraphs do.
- Cut any word whose removal does not change the meaning.
- No exclamation marks. No rhetorical questions. No quotations or mottos.
- Write dates one way throughout a document: `03.2021–06.2023` (unspaced en dash between numbers) or `Mar 2021 to Jun 2023`, never both.

## Language level

The user chooses a CEFR level for each output language. It is the level of the written text, and it should match how the user will speak in the interview. Write at the chosen level, not above it.

| Level | On the page |
|---|---|
| B1 | Short main clauses. Common words. One idea per sentence. No idioms, no passive constructions, no subordinate chains. The cover letter is three short paragraphs |
| B2 | Clear, direct sentences, some subordinate clauses. Standard professional vocabulary. Occasional linking words (because, so, although) |
| C1 | Fluent professional prose. Precise vocabulary for the field, varied sentence length. Still plain; fluency is not ornament |
| C2 | As a native professional would write: idiomatic and exact, with full control of register |

Technical terms the role requires are used at every level; a B1 text still says "PLC programming". Lower levels mean simpler sentences around the terms, not fewer facts.

For Norwegian, the same scale applies. At B1 and B2 avoid long compounds where two words would be clear, and prefer the common verb to the formal one (bruke, not anvende; få, not motta).

## Tone

The tone choice applies to the cover letter. The CV and the résumé stay factual in every case: plain bullets, no voice.

| Choice | Meaning |
|---|---|
| Friendly and conversational (default) | Reads like a capable person writing to someone they would like to work with. See "Cover letter voice" below. 200 to 300 words |
| Neutral | Plain and businesslike, no chat. 200 to 300 words |
| Brief and factual | Shortest wording that stays complete. Under 150 words |
| Formal | Full forms, no contractions, conventional salutation and close. 250 to 300 words |

Tone changes sentence shape and length. It never licenses buzzwords, dashes or the patterns above.

## Cover letter voice (friendly and conversational)

The goal is a letter a real person could have written in twenty minutes, not a template with the blanks filled in.

- **Speak to a person.** Address the contact by first name when the posting names one ("Hi Kari," / "Hei Kari,"). Use "I" and "you" or "dere". Write the way you would explain it across a table.
- **Start with the reason, not the formalities.** First sentence: the role and why it caught the writer's attention, taken from the user's motivation answer. Never "I am writing to apply".
- **Use short, common words.** Contractions are fine in English ("I've", "I'm", "didn't"). In Norwegian use "jeg vil gjerne", "jeg har jobbet med", not "undertegnede" or "med dette søker jeg".
- **Vary the rhythm.** Mix longer sentences with a short one. One sentence can be five words.
- **Be specific once or twice.** One concrete detail beats a list of strengths: the report that went to 40,000 customers, the dashboard the sales managers opened every Monday. Use only details from the sources or the form answers.
- **Admit a gap in one plain sentence** when the user said how they are closing it ("I haven't used Azure Data Factory yet. I'm taking the DP-203 course and finish in March."). Do not apologise and do not dress it up.
- **Keep one personal note** the user gave: why this employer, why this field, a reason for the move. Never invent a motivation.
- **End where the content ends.** Practical matter (start date), then a plain sign-off ("Best," / "Hilsen"). No summary, no "I look forward to".

Read the finished letter aloud in your head. If a sentence sounds like a brochure, rewrite it the way the person would say it.

## Norwegian

- Bokmål unless the user chose nynorsk. Do not mix the two.
- Norwegian business writing is direct and informal by international standards: "Hei" plus the contact's name is a normal salutation, "Med vennlig hilsen" a normal close. Use the contact name from the posting.
- No English loanwords where a Norwegian word is in common use, except the names of tools and methods.
- Compound words are written together (prosjektleder, kundeservice). Job titles are lower-case inside a sentence.
- Dates: `03.2021–06.2023` or `mars 2021 til juni 2023`.
