# Sirjna (Frappe v15) — Esbuild-Safe MVP

This app is a minimal, validated skeleton that **builds cleanly on Frappe Cloud**.

- Includes: `hooks.py`, `modules.txt`, `patches.txt`, `build.json`, `public/css/sirjna.css`, `www/index.html`
- No `app_include_js`, and `build.json` paths point only to existing files.
- Safe for `bench build --app sirjna` with Frappe v15's esbuild.

## Install (Frappe Cloud)
1. Upload to a private GitHub repo.
2. FC → Site → Apps → Get App → GitHub (your repo).
3. Install on the site.
4. Open `/` to see the confirmation page.