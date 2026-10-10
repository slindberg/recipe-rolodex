# Recipe Rolodex

A public, static recipe collection. GitHub Pages serves it at https://slindberg.github.io/recipe-rolodex/. Every push to `main` validates the recipes and redeploys the site.

**This repository is public. Everything committed here, including history, is readable by anyone.**

## Adding or editing a recipe

- One file per recipe: `recipes/<slug>.json`, where the slug is the title in lowercase words joined by hyphens. The schema is in `README.md`.
- **Write the steps in your own words.** Keep every quantity, time, and temperature, and link the original in `sourceUrl` / `sourceDomain`. Ingredient lists can be kept as given.
- **Name ingredients unambiguously:** "GF tortillas", not "tortillas"; "firm tofu", not "tofu".
- **Nothing about the people who cook or eat these recipes.** No names, no health or diet reasons, no personal tastes, and no notes about a particular kitchen or its equipment. A swap goes in `notes` as a plain option ("walnuts work in place of the pistachios"), never with a reason why.
- Run `python3 scripts/build.py` before committing. It stops on any file that breaks the schema.
