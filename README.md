# Recipe Rolodex

A small, growing collection of home recipes, built for cooking from a phone propped next to the stove.

**Site:** https://slindberg.github.io/recipe-rolodex/

The page is a single column with large type: a gallery of cards, then a full-screen cook view with ingredients, then numbered steps. You can search by title or ingredient, and filter by mains, sides, ≤30 minutes, or freezes. Every recipe has its own link (`#slug`), and the screen stays awake while a recipe is open.

## How it's built

- **Recipes:** `recipes/*.json`, one per recipe. These are the canonical data.
- **Page:** `index.html`, a static page with no dependencies. It fetches `recipes.json`.
- **Build:** `scripts/build.py` validates every recipe against the schema below, then writes `_site/` (the page plus `recipes.json`, all recipes in one file).
- **Deploy:** `.github/workflows/pages.yml` runs the build on every push and pull request, and deploys `_site/` to GitHub Pages from `main`.

Preview locally:

```sh
python3 scripts/build.py && python3 -m http.server -d _site
```

## Recipe schema

```js
{
  title: string,
  category: "Main" | "Side",
  prepTime, cookTime, servings,     // strings or null
  dietTags: string[],               // subset of ["GF", "Vegan", "Vegetarian", "DF"]
  ingredientGroups: [
    { label: string | null, items: [ { name: string, amount: string } ] }
  ],
  steps: string[],
  notes: string | null,             // tips, swaps, protein per serving
  freezes: "yes" | "partial" | "no",
  freezeNote: string | null,        // what freezes and what to hold back
  sourceUrl, sourceDomain           // both strings or both null
}
```

- `amount` is a single string ("1½ cups", "pinch"). Sources are too inconsistent to parse into numbers.
- `ingredientGroups` is always an array. An ungrouped list is one group with `label: null`.
- The slug is the filename, not a field.

Recipes credit their source. Steps are written in our own words, and the original is linked from each recipe.
