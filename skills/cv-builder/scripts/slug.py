#!/usr/bin/env python3
"""Print the output folder name: fullname-jobtitle-company.

Usage: slug.py "<full name>" "<job title>" "<company>"

Lower-case ASCII, words joined with hyphens. Norwegian letters become ae, o, a.
Standard library only.
"""
import re
import sys
import unicodedata

NORDIC = str.maketrans({"æ": "ae", "Æ": "ae", "ø": "o", "Ø": "o", "å": "a", "Å": "a"})


def slug(text):
    text = text.translate(NORDIC)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    parts = [slug(arg) for arg in sys.argv[1:]]
    if not all(parts):
        sys.exit("Each of name, job title and company must contain letters or digits.")
    print("-".join(parts))


if __name__ == "__main__":
    main()
