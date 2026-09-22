# Contributing to OSINT-CSE

Thanks for helping keep this list useful and up to date. There are two easy ways to contribute: **suggest a new CSE** or **report a broken one**.

## Reporting a broken CSE

Don't remove or edit an existing entry yourself. Instead, [open a "Broken CSE" issue](../../issues/new?template=broken_cse.yml) so we keep a record of what changed and can decide whether to fix, replace, or remove the entry.

Before opening the issue, please:

1. Try the link in a new incognito/private browser window (some CSEs fail silently if you're logged into certain Google accounts).
2. Try at least 2 different sample queries — a CSE can be broken for one query type but fine for others.
3. Check that there isn't already an open issue about the same link.

## Suggesting a new CSE

Open a ["Suggest a new CSE" issue](../../issues/new?template=suggest_cse.yml), or go straight to a pull request if you're comfortable editing Markdown tables. Either way, please:

1. **Test it manually** — confirm it returns relevant results for at least 2–3 sample queries before submitting.
2. **Check for duplicates** — search the README (Ctrl/Cmd+F) to make sure it isn't already listed, including under a slightly different name.
3. **Pick the right section** — Global Search, Country/Language-specific, Job Search, Most Wanted & Sanctioned, Documents & Statistics, Wikileaks, Fact-Checking, Files & Clouds, Webcams, or Pastebin. Propose a new section if none fit.

## Pull request format

Each entry is one row in a Markdown table:

```
| [CSE Name](https://link-to-cse) | Short description of what it searches, plus language/region notes | 🇷🇺 (optional region flags) |
```

Guidelines:

- Keep the description factual and short (what it searches, any quirks, interface language if not English).
- Add region/language flag emoji in the last column only for tables that already have that column.
- Attribute the creator when known, e.g. "by Pogoda", "by cipher387".
- Don't reorder unrelated rows in the same PR — keep diffs focused on your addition.

## Code of conduct

Be respectful. This is a shared resource for the OSINT and fact-checking community — assume good faith, and remember that some contributors work in sensitive or high-risk contexts.
