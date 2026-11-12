#!/usr/bin/env python3
"""Check documents for banned words and phrases.

Usage: lint_text.py <file-or-directory>... [--lang en|no] [--allow "phrase"]...

Checks .md files against references/banned-words.txt. A file's language is taken
from --lang, else from an en/ or no/ folder in its path; other files are checked
against both lists. The report data is not checked: it may quote the user's CV.
--allow exempts an exact phrase, for official names that contain a banned word.
Exits 1 if anything is found. Standard library only.
"""
import re
import sys
from pathlib import Path

WORDS_FILE = Path(__file__).resolve().parent.parent / "references" / "banned-words.txt"


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


def compile_patterns(phrases):
    patterns = []
    for phrase in phrases:
        stem = phrase.rstrip("*")
        body = r"\s+".join(re.escape(part) for part in stem.split())
        tail = r"\w*" if phrase.endswith("*") else ""
        patterns.append((phrase, re.compile(rf"(?<![\w-]){body}{tail}(?![\w-])", re.IGNORECASE)))
    return patterns


def file_lang(path, forced):
    if forced:
        return forced
    for part in path.parts:
        if part in ("en", "no"):
            return part
    return None


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

    lists = load_words()
    compiled = {lang: compile_patterns(words) for lang, words in lists.items()}
    hits = 0
    for path in files:
        lang = file_lang(path, forced)
        patterns = compiled.get(lang) or [p for group in compiled.values() for p in group]
        for number, line in lines_of(path):
            masked = line
            for phrase in allowed:
                masked = re.sub(re.escape(phrase), lambda m: "\0" * len(m.group()), masked, flags=re.IGNORECASE)
            for phrase, pattern in patterns:
                for match in pattern.finditer(masked):
                    hits += 1
                    print(f"{path}:{number}: '{match.group()}' (rule: {phrase})\n    {line.strip()[:160]}")

    if hits:
        print(f"\n{hits} banned word(s) or phrase(s) in {len(files)} file(s). "
              "Replace each with the concrete fact, or delete the sentence.")
        sys.exit(1)
    print(f"Clean: {len(files)} file(s) checked.")


if __name__ == "__main__":
    main()
