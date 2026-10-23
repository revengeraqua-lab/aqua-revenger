# Revenger — GangaShree Roots Private Limited

A six-page Flask brand portfolio: Home, Company & Leadership, Products, Values, Service Areas and Contact.

## Run locally

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. Python 3.11+ is supported. No Node build is needed. Source assets are tracked in `public/static` and served locally under `/static`.

## Content

`content.py` contains approved company facts, leadership biographies, the water/soda/jeera/lemon portfolio, two office addresses, ten service areas, and page titles/descriptions. `templates/brand.html` renders all six pages. `public/static/brand.css` and `brand.js` provide the responsive design and lightweight interactions. The homepage includes the cinematic Three.js / GSAP scroll story: full-screen water introduction with gentle refraction, bottle reveal, opening cap, water pouring into a glass and brand finale. The homepage header starts transparent over the water and becomes a compact white fixed navigation on scroll. Other pages load only the portfolio styles and interactions.

Leadership includes the client-supplied portraits of Subir Banerjee (Managing Director) and Rakesh Salve (Chief Executive Officer), with their existing biographies. The catalogue adds generated Revenger product concept artwork for water, soda, jeera soda and lemon soda; see `ASSETS.md`. Do not infer certifications or final packaging specifications from these visuals.

Water enquiry cards restore the four existing formats (250 ml, 500 ml, 1 litre and 2 litres). Visitors choose a bottle quantity, then continue to Contact with their product, size and quantity prefilled. Beverage cards offer quantity enquiries without inventing unconfirmed capacities. The client requested no prices; no prices, case counts or checkout are displayed. Final formats and availability are confirmed by the company.

The shared footer includes the leaf wordmark, navigation, service areas, direct telephone/email and office map links, plus the linked "Designed and developed by dipanshudev.com" credit. The strip above navigation is removed from every page. Cards use one-time scroll entrances and subtle hover feedback, respecting reduced motion; the cinematic homepage is retained. `REFERENCES.md` documents the REA Bisleri layout inspection.

## Deployment

Import with the Flask preset and repository root `./`. Entry point: `app.py`. `public/static` is served by Vercel's CDN. The app never creates a SQLite file at startup.

Set `SITE_URL` to the final brand domain, including https but no trailing slash. Default: https://revenger-397n.vercel.app. This controls canonical URLs, structured data and the sitemap. See `SEO-NOTES.md` for research and search-launch steps.

Contact actions use the confirmed telephone and email. The composer opens an email draft and does not submit or store visitor data. Email is only sent when the visitor sends it using their mail app.

## Legacy API storage

The existing `/api/enquiries` API and local management tool remain for compatibility; they are not used by the portfolio contact page. SQLite is available locally; on Vercel configure a persistent PostgreSQL `DATABASE_URL` or `POSTGRES_URL` to use that API. Without it the API returns a safe 503. Never use temporary storage for customer enquiries.

## Verification

```powershell
python -m unittest discover -s tests -v
python tests/browser_check.py
python tests/catalogue_check.py
python tests/browser_check.py https://revenger-397n.vercel.app
python tests/catalogue_check.py https://revenger-397n.vercel.app
```

Browser verification uses the installed Chrome executable through Playwright in an isolated profile. It checks 3D rendering, scroll chapters, cap opening, pouring, reverse scroll, pause/resume, reduced motion, all pages, metadata, responsive widths, navigation and contact prefills. The catalogue check also verifies all seven product images, the footer credit, quantity bounds and size/quantity enquiry prefills. No email is sent.


## Interactive bottle

When the bottle is visible, hold the right or left mouse button on the scene and drag horizontally for a full 360-degree turn. On touch devices, swipe horizontally; vertical swipes still scroll the story. Focus the canvas and use Left/Right arrows to rotate, Home or the Reset view button to restore the view. The closed cap follows the bottle orientation; the detached cap is framed below the actual header height with a safety margin, including short desktop screens.


The cap opening is choreographed in `public/static/cap-motion.js`: continuous screw rotation with a matching axial rise, a separate vertical clearance lift, then a smooth arc to the parked position. Its orientation blend excludes the screw rotation so multiple turns remain continuous in either scroll direction. The cap has a modeled hollow underside, and the neck has continuous spiral thread geometry.

The cinematic HUD (chapter numbers, progress labels, swipe instructions and visible pause/reset buttons) is visually removed. Pause and reset remain keyboard-focus controls; the canvas also supports Home to reset.


The header and footer pair the wordmark with `public/static/images/leaf-mark.svg`, a vector interpretation of the packaging leaf emblem. Front and rear half-wrap label meshes repeat the same packaging artwork around the bottle, including the rear PET texture. No unconfirmed back-label specifications are invented. Chapter headings fade sequentially (out, then in) rather than crossfading on top of each other. `bottle-framing.js` projects the bottle bounds, reserves neck-release space, and fits them below navigation across viewport sizes and inspection angles.

## Interactive service globe

The homepage's "Local connections" section includes a real Three.js globe with all ten service-city points. Select a city or a globe point to focus it and update the city-specific enquiry link. Drag with a mouse or swipe horizontally on touch; arrow keys rotate and Home/India view reset the globe. Vertical touch gestures retain native page scrolling. The pause control and reduced-motion preference stop automatic motion.

`service-globe.js` and the 162 KB local land geometry load only when approaching the section. Rendering stops offscreen or in a hidden tab. A static SVG and city selection remain available if WebGL is unavailable; there are no external runtime map requests or API keys. Only approximate city centres are shown, not factory, office or service-radius coordinates. Map/coordinate sources and attribution are in `REFERENCES.md`.

Run `python tests/globe_check.py` (or append the live site URL) to verify lazy loading, ten-city selection, actual point picking, enquiry prefills, mouse/keyboard/touch rotation, responsive layout, reduced motion, offscreen suspension and WebGL fallback. Rebuild the coastlines, land dots and SVG from a downloaded Natural Earth `ne_110m_land.geojson` with `python tools/build_globe_data.py path/to/ne_110m_land.geojson`.
