#!/usr/bin/env python3
"""Validate recipes/*.json and build the static site into _site/.

  _site/index.html    the Rolodex page
  _site/recipes.json  every recipe in one file, sorted by title, each with its slug

Run from the repo root: python3 scripts/build.py
Exits non-zero, naming the file and field, on any recipe that breaks the schema in README.md.
Preview locally with: python3 -m http.server -d _site
"""
import json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"

STR_OR_NULL = (str, type(None))
FIELDS = {
    "title": str,
    "category": str,
    "prepTime": STR_OR_NULL,
    "cookTime": STR_OR_NULL,
    "servings": STR_OR_NULL,
    "dietTags": list,
    "ingredientGroups": list,
    "steps": list,
    "notes": STR_OR_NULL,
    "freezes": str,
    "freezeNote": STR_OR_NULL,
    "sourceUrl": STR_OR_NULL,
    "sourceDomain": STR_OR_NULL,
}
CATEGORIES = {"Main", "Side"}
DIET_TAGS = {"GF", "Vegan", "Vegetarian", "DF"}
FREEZES = {"yes", "partial", "no"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def check(path, r):
    errs = []
    def bad(msg):
        errs.append(f"{path.name}: {msg}")

    if not SLUG.match(path.stem):
        bad("filename must be a lowercase-hyphen slug")
    if not isinstance(r, dict):
        bad("must be a JSON object")
        return errs
    for k in sorted(set(r) - set(FIELDS)):
        bad(f"unknown field {k!r}")
    for k, t in FIELDS.items():
        if k not in r:
            bad(f"missing field {k!r}")
        elif not isinstance(r[k], t):
            bad(f"{k!r} has the wrong type")
    if errs:
        return errs
    if not r["title"].strip():
        bad("'title' is empty")
    if r["category"] not in CATEGORIES:
        bad(f"'category' must be one of {sorted(CATEGORIES)}")
    if r["freezes"] not in FREEZES:
        bad(f"'freezes' must be one of {sorted(FREEZES)}")
    for t in r["dietTags"]:
        if t not in DIET_TAGS:
            bad(f"unknown diet tag {t!r}")
    if not r["ingredientGroups"]:
        bad("'ingredientGroups' is empty")
    for g, group in enumerate(r["ingredientGroups"]):
        if not isinstance(group, dict) or set(group) != {"label", "items"} \
                or not isinstance(group["label"], STR_OR_NULL) or not isinstance(group["items"], list) \
                or not group["items"]:
            bad(f"ingredientGroups[{g}] must be {{label: string|null, items: [...]}} with items")
            continue
        for i, item in enumerate(group["items"]):
            if not isinstance(item, dict) or set(item) != {"name", "amount"} \
                    or not all(isinstance(item[k], str) and item[k].strip() for k in item):
                bad(f"ingredientGroups[{g}].items[{i}] must be {{name, amount}}, both non-empty strings")
    if not r["steps"] or not all(isinstance(s, str) and s.strip() for s in r["steps"]):
        bad("'steps' must be a non-empty list of non-empty strings")
    if (r["sourceUrl"] is None) != (r["sourceDomain"] is None):
        bad("'sourceUrl' and 'sourceDomain' are set together or not at all")
    if r["sourceUrl"] and not r["sourceUrl"].startswith("https://"):
        bad("'sourceUrl' must be an https:// link")
    return errs


def main():
    recipes, errs = [], []
    for path in sorted((ROOT / "recipes").glob("*.json")):
        try:
            r = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            errs.append(f"{path.name}: invalid JSON ({e})")
            continue
        e = check(path, r)
        errs += e
        if not e:
            recipes.append({"slug": path.stem, **r})
    if errs:
        sys.exit("build stopped:\n  " + "\n  ".join(errs))
    recipes.sort(key=lambda r: r["title"].lower())

    shutil.rmtree(SITE, ignore_errors=True)
    SITE.mkdir()
    shutil.copy(ROOT / "index.html", SITE / "index.html")
    (SITE / "recipes.json").write_text(json.dumps(recipes, ensure_ascii=False, separators=(",", ":")))
    print(f"built {len(recipes)} recipes into {SITE.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
