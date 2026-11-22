# The Magnetic Wife: page code for GoHighLevel

The sales page, thank-you page and policy pages live here and are served by
GitHub Pages at https://happyspousehappyhouse.love (see `docs/CNAME`).
Payment and file delivery run on Whop; customer details are kept in GoHighLevel.
A change pushed here goes live within about 10 minutes.

## How it fits together

- `src/` holds the page sources: the letter (`index.src.html`), styles, the
  checkout script (`site.js`) and the settings (`config.js`).
- `make_pages.py` builds them into `docs/`, one script per page.
- `docs/` is published by GitHub Pages on the custom domain: the full site
  (`index.html`, `thank-you/`, `privacy/`, `terms/`, `refunds/`) plus one-script
  versions of each page (`sales.js` etc.) for embedding in a GHL page if needed.

## Settings (`src/config.js`)

| Setting | What it does |
|---|---|
| `planId` | Whop `plan_` ID. When set, the Whop checkout appears inside the page. |
| `checkoutUrl` | Whop link used while `planId` is empty. |
| `returnUrl` | Where Whop sends buyers after paying (the GHL thank-you page). |
| `offerLabel` | Small label above the price. |
| `pixelId` | Meta Pixel ID. |

## Optional: embedding in a GHL page

A GHL funnel step can show a page with one Code (Custom JS/HTML) element containing:

```html
<div id="tmw-root"></div>
<script src="https://happyspousehappyhouse.love/sales.js"></script>
```

Swap `sales.js` for `thank-you.js`, `privacy.js`, `terms.js` or `refunds.js` on
the other steps.

## Updating

```bash
python3 make_pages.py
git add -A && git commit -m "Update page" && git push
```

## Copyright

All rights reserved. See `LICENSE`: nothing here may be copied or reused without written permission.
