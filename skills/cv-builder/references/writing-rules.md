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
- Write dates one way throughout a document: `03.2021–06.2023` or `Mar 2021 – Jun 2023`, never both.

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

| Choice | Meaning |
|---|---|
| Brief and factual | Shortest wording that stays complete. No summary section unless it adds a fact. Cover letter under 200 words |
| Neutral professional | Plain and businesslike. Cover letter 200 to 300 words |
| Warm in the letter | CV as above. The cover letter may say in the user's own terms why the work matters to them, using their answer to the motivation question |
| Formal | Full forms, no contractions, conventional salutation and close |

Tone changes sentence shape and length. It never licenses buzzwords.

## Norwegian

- Bokmål unless the user chose nynorsk. Do not mix the two.
- Norwegian business writing is direct and informal by international standards: "Hei" plus the contact's name is a normal salutation, "Med vennlig hilsen" a normal close. Use the contact name from the posting.
- No English loanwords where a Norwegian word is in common use, except the names of tools and methods.
- Compound words are written together (prosjektleder, kundeservice). Job titles are lower-case inside a sentence.
- Dates: `03.2021–06.2023` or `mars 2021 – juni 2023`.
