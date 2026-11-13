#!/usr/bin/env python3
"""Check documents for banned words, dash punctuation and AI sentence patterns.

Usage: lint_text.py <file-or-directory>... [--lang en|no] [--allow "phrase"]...

Checks .md files against:
  - references/banned-words.txt (buzzwords, filler, AI vocabulary)
  - dash punctuation: em dashes, spaced en dashes, double hyphens, spaced hyphens
    used as dashes (an unspaced en dash inside a number range such as 2021–2025
    is allowed)
  - AI sentence patterns: "it's not X, it's Y", "not just X but Y", and the
    Norwegian equivalents
  - list layout in the Languages, Education and Courses sections: three entries
    or fewer go one per line; more than three go on one line, separated by
    semicolons (commas also work for languages)

A file's language is taken from --lang, else from an en/ or no/ folder in its
path; other files are checked against both languages. The report data is not
checked: it may quote the user's CV. --allow exempts an exact phrase, for
official names that contain a banned word. Exits 1 if anything is found.
Standard library only.
"""
import re
import sys
from pathlib import Path

WORDS_FILE = Path(__file__).resolve().parent.parent / "references" / "banned-words.txt"

APOS = "['’]"

# (label, regex, language or None for both)
PATTERNS = [
    ("em dash", r"—", None),
    ("spaced dash", r"\s–\s", None),
    ("double hyphen", r"(?<!-)--(?!-)", None),
    ("hyphen used as a dash", r"(?<=\S) - (?=\S)", None),
    ("'it's not X, it's Y'", rf"\b(?:it|this|that)(?:{APOS}s| is) not\b[^.!?]{{1,80}}?[,;]\s*(?:it|this|that)(?:{APOS}s| is)\b", "en"),
    ("'not just X but Y'", r"\bnot (?:just|only|merely|simply)\b[^.!?]{1,80}?\bbut\b", "en"),
    ("'isn't about X, it's about Y'", rf"\b(?:isn{APOS}t|is not|wasn{APOS}t|was not) (?:just |only |merely )?about\b[^.!?]{{1,80}}?[,;]\s*(?:it{APOS}s|it is|but)\b", "en"),
    ("'more than just'", r"\bmore than (?:just|only)\b", "en"),
    ("'det handler ikke om'", r"\bdet handler ikke om\b", "no"),
    ("'ikke bare X, men også Y'", r"\bikke bare\b[^.!?]{1,80}?\bmen (?:også|like)\b", "no"),
    ("'det er ikke X, det er Y'", r"\b(?:det|dette) er ikke\b[^.!?]{1,80}?[,;]\s*(?:det|dette) er\b", "no"),
    ("'mer enn bare'", r"\bmer enn bare\b", "no"),
]


def load_words():
    lists, current = {}, None
    for line in WORDS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = lists.setdefault(line[1:-1], [])
        elif current is not None:
            current.append(line)
    return lists


def compile_words(phrases):
    patterns = []
    for phrase in phrases:
        stem = phrase.rstrip("*")
        body = r"\s+".join(re.escape(part) for part in stem.split())
        tail = r"\w*" if phrase.endswith("*") else ""
        patterns.append((f"banned: {phrase}", re.compile(rf"(?<![\w-]){body}{tail}(?![\w-])", re.IGNORECASE)))
    return patterns


def compile_patterns(lang):
    return [(label, re.compile(rx, re.IGNORECASE)) for label, rx, only in PATTERNS if only in (None, lang)]


def file_lang(path, forced):
    if forced:
        return forced
    for part in path.parts:
        if part in ("en", "no"):
            return part
    return None


LIST_SECTIONS = {
    "languages": True, "språk": True,
    "education": False, "utdanning": False,
    "courses and certifications": False, "kurs og sertifiseringer": False,
    "courses and certificates": False, "kurs og sertifikater": False,
    "courses": False, "kurs": False,
}


def split_top_level(text, separators):
    """Split on separators that are not inside brackets."""
    parts, depth, current = [], 0, ""
    for ch in text:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch in separators and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += ch
    parts.append(current)
    return [p.strip() for p in parts if p.strip()]


def check_list_layout(path):
    """Yield (line number, heading, message) for sections that break the layout rule."""
    sections, current = [], None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if line.startswith("## "):
            name = line[3:].strip()
            current = (number, name, []) if name.lower() in LIST_SECTIONS else None
            if current:
                sections.append(current)
        elif line.startswith("# "):
            current = None
        elif current and line:
            current[2].append(line)

    for number, name, body in sections:
        languages = LIST_SECTIONS[name.lower()]
        body = [l for l in body if not re.fullmatch(r"\*[^*]+\*", l)]  # date and place lines
        entries = [l for l in body if l.startswith("### ")]
        bullets = [l for l in body if re.match(r"[-*]\s+", l)]
        if entries:
            count, one_line = len(entries), False
        elif bullets:
            count, one_line = len(bullets), False
        elif len(body) >= 2:
            count, one_line = len(body), False
        elif body:
            count = len(split_top_level(body[0], ",;" if languages else ";"))
            one_line = True
        else:
            continue
        if not one_line and count > 3:
            yield number, name, (f"{count} entries on separate lines. With more than three, write them "
                                 "on one line separated by semicolons")
        elif one_line and 2 <= count <= 3:
            yield number, name, (f"{count} entries on one line. With three or fewer, put each on its own line")


def lines_of(path):
    return list(enumerate(path.read_text(encoding="utf-8").splitlines(), 1))


def main():
    args = sys.argv[1:]
    forced, allowed, targets = None, [], []
    while args:
        arg = args.pop(0)
        if arg == "--lang" and args:
            forced = args.pop(0)
        elif arg == "--allow" and args:
            allowed.append(args.pop(0).lower())
        else:
            targets.append(Path(arg))
    if not targets:
        sys.exit(__doc__)

    files = []
    for target in targets:
        if target.is_dir():
            files += sorted(target.rglob("*.md"))
        else:
            files.append(target)
    files = [f for f in files if f.name != "answers.md"]  # the user's own words

    words = load_words()
    word_rules = {lang: compile_words(group) for lang, group in words.items()}
    hits = 0
    for path in files:
        lang = file_lang(path, forced)
        langs = [lang] if lang in ("en", "no") else ["en", "no"]
        rules = []
        for item in langs:
            rules += word_rules.get(item, []) + compile_patterns(item)
        seen = set()
        rules = [r for r in rules if not (r[0] in seen or seen.add(r[0]))]
        for number, name, message in check_list_layout(path):
            hits += 1
            print(f"{path}:{number}: '{name}' (list layout)\n    {message}")
        for number, line in lines_of(path):
            masked = line
            for phrase in allowed:
                masked = re.sub(re.escape(phrase), lambda m: "\0" * len(m.group()), masked, flags=re.IGNORECASE)
            for label, pattern in rules:
                for match in pattern.finditer(masked):
                    hits += 1
                    print(f"{path}:{number}: '{match.group().strip()}' ({label})\n    {line.strip()[:160]}")

    if hits:
        print(f"\n{hits} problem(s) in {len(files)} file(s). Replace each with the concrete fact, "
              "split the sentence, or delete it.")
        sys.exit(1)
    print(f"Clean: {len(files)} file(s) checked.")


if __name__ == "__main__":
    main()
