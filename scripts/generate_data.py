#!/usr/bin/env python3
"""
Regenerate docs/data.json from README.md so the GitHub Pages site
(docs/) always reflects the tables in README.md as the single source
of truth.

Usage: python scripts/generate_data.py README.md docs/data.json
"""
import re
import sys
import json

SKIP_SECTIONS = {"table of contents", "contributing"}
HEADER_CELL_NAMES = {"name", "resource", "engine", "description", "region", "cheatsheet"}


def strip_emoji(text: str) -> str:
    return re.sub(r"^[^\w]+", "", text).strip()


def is_separator_row(cells):
    return all(re.match(r"^:?-+:?$", c.strip()) for c in cells if c.strip() != "")


def extract_links(cell):
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", cell)


def parse_readme(text: str):
    lines = text.splitlines()
    h2, h3 = None, None
    section = None
    entries = []
    skip_section = False

    for raw_line in lines:
        stripped = raw_line.strip()

        m2 = re.match(r"^##\s+(.*)", stripped)
        m3 = re.match(r"^###\s+(.*)", stripped)

        if m2 and not stripped.startswith("###"):
            h2 = strip_emoji(m2.group(1))
            h3 = None
            skip_section = h2.lower() in SKIP_SECTIONS
            section = h2
            continue
        if m3:
            h3 = strip_emoji(m3.group(1))
            section = f"{h2} — {h3}" if h2 else h3
            continue

        if skip_section:
            continue

        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if is_separator_row(cells):
                continue
            if cells[0].lower() in HEADER_CELL_NAMES:
                continue

            links = extract_links(cells[0])
            if not links:
                if len(cells) >= 2:
                    links2 = extract_links(cells[1])
                    if links2:
                        link_text, link_url = links2[0]
                        entries.append({
                            "section": section,
                            "name": f"{cells[0]}: {link_text}",
                            "link": link_url,
                            "desc": "",
                            "region": cells[2] if len(cells) > 2 else "",
                        })
                continue

            name, link = links[0]
            desc = cells[1] if len(cells) > 1 else ""
            region = cells[2] if len(cells) > 2 else ""
            if len(links) > 1:
                extra = "; ".join(f"{t}: {u}" for t, u in links[1:])
                desc = f"{desc} (also: {extra})".strip()
            entries.append({
                "section": section,
                "name": name,
                "link": link,
                "desc": desc,
                "region": region,
            })
            continue

        bm = re.match(r"^-\s+(.*)", stripped)
        if bm:
            content = bm.group(1)
            links = extract_links(content)
            if links:
                name, link = links[0]
                desc = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", "", content, count=1)
                desc = re.sub(r"\s{2,}", " ", desc).strip(" .—-")
                entries.append({
                    "section": section,
                    "name": name,
                    "link": link,
                    "desc": desc,
                    "region": "",
                })
            continue

    return entries


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_data.py <README.md> <docs/data.json>", file=sys.stderr)
        sys.exit(1)

    readme_path, output_path = sys.argv[1], sys.argv[2]

    with open(readme_path, encoding="utf-8") as f:
        text = f.read()

    entries = parse_readme(text)

    if not entries:
        print("No entries parsed from README.md — aborting to avoid wiping data.json.", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(entries)} entries to {output_path}")


if __name__ == "__main__":
    main()
