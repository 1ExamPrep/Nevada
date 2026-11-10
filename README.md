# Pass Your Nevada Contractor Exam

Site: https://passyournevadacontractorexam.com (GitHub Pages, repo `1ExamPrep/Nevada`, branch `main`).
Making another site from this one? Read [NEW-SITE.md](NEW-SITE.md).

## What is here

- 463 active products from the 1 Exam Prep Shopify collection "Nevada Contractor License" (ID 5968560154), on 86
  license pages: `/<license>/` compares the packages, `/<license>/<package>/` is the product page with Buy now
  straight to checkout. Draft products are skipped.
- Licenses are worked out from product titles in `tools/nvclass.py`. Contractor titles carry the NSCB code, such as
  (B-2) or (C-15A), and each code in `CODES` is one license page. Products without a code (electrician cards,
  the Business and Law exam, licensing help, plumbers, national exams) match the rows in `SPECIAL`. New products
  that match nothing are printed by `build.py` as "Unclassified".
- Nevada facts (NSCB, PSI, ICC, Electrical Safety Professionals, City of Reno) live in `tools/nvcopy.py`, checked
  on November 10, 2026.
- Long Shopify descriptions are split into sections at build time (`sectionize()` in `build.py`), so full
  descriptions from the dashboard sync still pass the page checks.
- `python3 tools/check_pages.py . https://passyournevadacontractorexam.com` grades every page against
  "What every page and post needs to pass".

## Design

Design 2, Red Rock Guide: dark hero over red sandstone mesas with the license finder in it, an NSCB facts row,
licensing tables, sticky section tabs and a Quick Facts sidebar on license pages. Nunito Sans, cobalt and red rock.
Set by `"design": 2` in `site-config.json`. The other four layouts stay in `shared/themes` (1 Storefront,
3 NSCB Classification Index, 4 Exam Path, 5 Silver State Editorial); preview any page with `?design=N` or compare
them at `/designs/`.

No logo yet, so the header shows the text wordmark and `build.py` draws the favicon and social card. To add one:
save it as `brand/logo-source.png`, run `python3 tools/make_logo.py`, add `"logoNav": "shared/logo-nav.png"` to
`site-config.json` and rebuild.

## Day to day

- Products change in Shopify: the dashboard sync rebuilds. Or pull locally with `tools/sync_shopify.py`.
- Copy change: edit `tools/nvcopy.py`, `content/faq-general.json` or `build.py`, run `python3 build.py`, push.

## Max, the exam advisor

Off for now (`aiFinderUrl` is empty). To switch it on, give Nevada its own Cloudflare Worker as on the Texas site,
put its address in `aiFinderUrl` and rebuild; `tools/maxkb.py` then writes `shared/kb/`.
