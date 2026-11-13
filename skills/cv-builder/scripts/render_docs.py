#!/usr/bin/env python3
"""Render the Phase 2 documents.

Usage: render_docs.py <output-directory> [--no-pdf]

Converts every resume.md and cover-letter.md under the directory to a
single-column HTML file and a Word file (.docx) with one fixed style, and to
PDF when Chrome, Chromium or Edge is installed. Supports the Markdown subset
described in references/document-structure.md. Standard library only.
"""
import html
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

DOC_NAMES = ("resume.md", "cover-letter.md")

CSS = """
@page { size: A4; margin: 16mm 18mm; }
* { box-sizing: border-box; }
html { font-size: 10.5pt; }
body {
  font-family: Arial, Helvetica, "Liberation Sans", sans-serif;
  color: #111; background: #fff; line-height: 1.42;
  max-width: 174mm; margin: 0 auto; padding: 16mm 0;
}
h1 { font-size: 20pt; margin: 0 0 2pt; line-height: 1.15; }
h1 + p { margin: 0 0 12pt; color: #333; }
h2 {
  font-size: 11pt; text-transform: uppercase; letter-spacing: .06em;
  margin: 14pt 0 6pt; padding-bottom: 2pt; border-bottom: 1px solid #111;
  break-after: avoid;
}
h3 { font-size: 10.5pt; margin: 9pt 0 0; break-after: avoid; }
h3 + p.meta { margin: 0 0 3pt; color: #444; font-style: normal; break-after: avoid; }
p { margin: 0 0 7pt; }
ul { margin: 2pt 0 7pt; padding-left: 14pt; }
li { margin: 0 0 2pt; }
a { color: inherit; text-decoration: none; }
.letter h2 { text-transform: none; letter-spacing: 0; border: 0; font-size: 12pt; margin: 16pt 0 10pt; }
.letter p { margin: 0 0 10pt; }
@media screen { body { padding: 16mm 18mm; max-width: 210mm; box-shadow: 0 0 0 1px #ddd; } }
@media print { body { padding: 0; max-width: none; } }
"""

BROWSERS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "microsoft-edge",
    "chrome",
    "msedge",
)


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def parse(markdown):
    """Return blocks: (kind, value). kind is h1, h2, h3, meta, li or p; a p value is a list of lines."""
    blocks, paragraph = [], []

    def flush():
        if not paragraph:
            return
        whole = " ".join(part.strip() for part in paragraph)
        after_h3 = blocks and blocks[-1][0] == "h3"
        if after_h3 and len(paragraph) == 1 and re.fullmatch(r"\*[^*]+\*", whole):
            blocks.append(("meta", whole[1:-1]))
        else:
            lines, current = [], []
            for part in paragraph:
                current.append(part.strip())
                if part.endswith("  "):
                    lines.append(" ".join(current))
                    current = []
            if current:
                lines.append(" ".join(current))
            blocks.append(("p", lines))
        paragraph.clear()

    for line in markdown.splitlines():
        stripped = line.strip()
        heading = re.match(r"(#{1,3})\s+(.*)", stripped)
        if not stripped:
            flush()
        elif heading:
            flush()
            blocks.append((f"h{len(heading.group(1))}", heading.group(2)))
        elif re.match(r"[-*]\s+", stripped):
            flush()
            blocks.append(("li", re.sub(r"^[-*]\s+", "", stripped)))
        else:
            paragraph.append(line)
    flush()
    return blocks


def to_html(blocks):
    out, in_list = [], False
    for kind, value in blocks:
        if in_list and kind != "li":
            out.append("</ul>")
            in_list = False
        if kind == "li":
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(value)}</li>")
        elif kind == "meta":
            out.append(f'<p class="meta">{inline(value)}</p>')
        elif kind == "p":
            out.append("<p>" + "<br>".join(inline(l) for l in value) + "</p>")
        else:
            out.append(f"<{kind}>{inline(value)}</{kind}>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


# --- Word output -------------------------------------------------------------

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
INLINE_TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*]+\*|\[[^\]]+\]\([^)\s]+\))")


def runs(text, bold=False, size=None, color=None):
    """Word runs for one line of inline Markdown."""
    out = []
    for token in INLINE_TOKEN.split(text):
        if not token:
            continue
        b, i = bold, False
        link = re.fullmatch(r"\[([^\]]+)\]\(([^)\s]+)\)", token)
        if link:
            label, url = link.group(1), link.group(2)
            shown = re.sub(r"^(mailto:|https?://)", "", url).rstrip("/")
            token = label if shown == label.rstrip("/") else f"{label} ({url})"
        elif token.startswith("**") and token.endswith("**") and len(token) > 4:
            token, b = token[2:-2], True
        elif token.startswith("*") and token.endswith("*") and len(token) > 2:
            token, i = token[1:-1], True
        props = ("<w:b/>" if b else "") + ("<w:i/>" if i else "")
        if size:
            props += f'<w:sz w:val="{size}"/>'
        if color:
            props += f'<w:color w:val="{color}"/>'
        out.append(f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(token)}</w:t></w:r>')
    return "".join(out)


def to_docx_body(blocks, letter):
    def para(content, before=0, after=120, extra=""):
        return (f'<w:p><w:pPr><w:spacing w:before="{before}" w:after="{after}"/>{extra}</w:pPr>{content}</w:p>')

    out = []
    for index, (kind, value) in enumerate(blocks):
        if kind == "h1":
            out.append(para(runs(value, bold=True, size=40), after=40))
        elif kind == "h2" and letter:
            out.append(para(runs(value, bold=True, size=24), before=280, after=200))
        elif kind == "h2":
            border = '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="111111"/></w:pBdr><w:keepNext/>'
            out.append(para(runs(value.upper(), bold=True, size=22), before=260, after=110, extra=border))
        elif kind == "h3":
            out.append(para(runs(value, bold=True), before=160, after=0, extra="<w:keepNext/>"))
        elif kind == "meta":
            out.append(para(runs(value, color="444444"), after=50, extra="<w:keepNext/>"))
        elif kind == "li":
            indent = '<w:ind w:left="280" w:hanging="200"/>'
            out.append(para(runs("•  " + value), after=30, extra=indent))
        else:
            content = '<w:r><w:br/></w:r>'.join(runs(line) for line in value)
            contact = index > 0 and blocks[index - 1][0] == "h1"
            out.append(para(content, after=200 if letter or contact else 130))
    return "".join(out)


def write_docx(path, blocks, lang, letter):
    document = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="{W_NS}"><w:body>'
        f"{to_docx_body(blocks, letter)}"
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="907" w:right="1020" w:bottom="907" w:left="1020" w:header="0" w:footer="0" w:gutter="0"/>'
        "</w:sectPr></w:body></w:document>"
    )
    styles = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="{W_NS}"><w:docDefaults>'
        '<w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:color w:val="111111"/>'
        f'<w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="{"nb-NO" if lang == "no" else "en-GB"}"/></w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
        '</w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style></w:styles>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        "</Relationships>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/_rels/document.xml.rels", doc_rels)


def page(markdown, lang, kind):
    title = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    name = title.group(1).strip() if title else ""
    labels = {
        "en": {"resume": "Résumé", "cover-letter": "Cover letter"},
        "no": {"resume": "CV", "cover-letter": "Søknad"},
    }
    label = labels[lang][kind]
    body_class = "letter" if kind == "cover-letter" else "doc"
    return (
        f'<!doctype html>\n<html lang="{"nb" if lang == "no" else "en"}">\n<head>\n<meta charset="utf-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(name)}, {label}</title>\n<style>{CSS}</style>\n</head>\n"
        f'<body class="{body_class}">\n{to_html(parse(markdown))}\n</body>\n</html>\n'
    )


def find_browser():
    for candidate in BROWSERS:
        if Path(candidate).is_file():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    return None


def pdf_pages(path):
    try:
        return len(re.findall(rb"/Type\s*/Page(?![s\w])", path.read_bytes()))
    except OSError:
        return 0


def main():
    args = [a for a in sys.argv[1:] if a != "--no-pdf"]
    if len(args) != 1:
        sys.exit(__doc__)
    root = Path(args[0])
    sources = sorted(p for p in root.rglob("*.md") if p.name in DOC_NAMES)
    if not sources:
        sys.exit(f"No {', '.join(DOC_NAMES)} found under {root}")

    browser = None if "--no-pdf" in sys.argv else find_browser()
    for src in sources:
        lang = "no" if "no" in src.parts else "en"
        html_path = src.with_suffix(".html")
        markdown = src.read_text(encoding="utf-8")
        html_path.write_text(page(markdown, lang, src.stem), encoding="utf-8")
        write_docx(src.with_suffix(".docx"), parse(markdown), lang, src.stem == "cover-letter")
        line = f"{html_path}  +  {src.stem}.docx"
        if browser:
            pdf_path = src.with_suffix(".pdf")
            result = subprocess.run(
                [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                 f"--print-to-pdf={pdf_path.resolve()}", html_path.resolve().as_uri()],
                capture_output=True, timeout=120,
            )
            if result.returncode == 0 and pdf_path.exists():
                pages = pdf_pages(pdf_path)
                line += f"  +  {pdf_path.name} ({pages} page{'s' if pages != 1 else ''})"
                if src.name == "cover-letter.md" and pages > 1:
                    line += "  <-- must fit one page: shorten it"
                elif src.name == "resume.md" and pages > 1:
                    line += "  <-- over one page: shorten it, or keep two only if the user agreed"
            else:
                line += "  (PDF failed)"
        print(line)
    if not browser and "--no-pdf" not in sys.argv:
        print("No Chrome, Chromium or Edge found: PDFs were not made. "
              "The .docx files are ready to send; for PDF, print the HTML files from a browser.")


if __name__ == "__main__":
    main()
