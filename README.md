# Revenger

An animated, responsive brand website for **Revenger**, by **GangaShree Roots Private Limited**. Python Flask renders the website and handles enquiries. SQLite stores submissions. A locally hosted Three.js WebGL scene renders the bottle, detached cap, water stream and droplets in 3D, controlled by native scrolling.

## Run

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. `PORT` can override port 5000. Waitress serves the app with Flask debug mode disabled.

## Features

- Responsive brand story and four product formats
- Five visual chapters: GangaShree Roots → meet Revenger → opening ritual → pour into a glass → everyday bottle formats
- Real bottle/cap geometry, photographic surface detail, 3D water stream and droplets
- Shared camera/depth buffer; the stream follows the transformed bottle mouth
- Native wheel/touch/keyboard scrolling, a collection skip link, and chapter progress
- Static photographic fallback when WebGL is unavailable; reduced motion removes the long pinned section
- Case enquiry bag with quantities, removal and browser persistence
- Validated order, distributor and general enquiries saved to SQLite
- Accessible dialogs, keyboard controls, reduced-motion support and pause control
- Local enquiry management without a publicly exposed admin endpoint

```powershell
python manage.py
python manage.py --export enquiries.csv
python -m unittest discover -s tests -v
```

Database: `instance/revenger.sqlite3` (created automatically). Back up this file. Exports contain customer contact information; keep them private.

## Brand and catalogue setup

The supplied logos informed the green, ivory and gold palette. The current wordmarks are custom typography. Bottle, water splash and forest imagery are generated photorealistic assets; the exact uploaded raster logos are not embedded. The generated bottle is a brand concept; replace it with approved packaging photography when available. Asset prompts and provenance are documented in `ASSETS.md`. Draft sizes and case quantities are in `PRODUCTS` in `app.py`; confirm them before publishing. No unverified source, purification, certification or health claims are used.

REA inspected https://www.bisleri.com as a category reference for product browsing and captured the local site for browser verification. The design and artwork are original.

## Before public launch

Provide real product specifications, service areas, contact details and pricing. The current order flow requests a quotation; it does not take payment or promise fulfilment. Submissions are saved locally, with no email/SMS notifications configured. For public hosting, configure HTTPS, persistent database storage, backups, spam/rate protection and an appropriate privacy/retention policy. Bind the server to your hosting environment as required; the development launch intentionally listens on localhost.

DM Sans and Manrope are self-hosted in `static/fonts` with their SIL Open Font License notices. All fonts, artwork and application scripts are served locally.

## 3D implementation and verification

`static/scroll-story.js` controls the pinned sequence and renderer. `static/story-timeline.js` uses one paused GSAP timeline to choreograph the camera, background, bottle, cap, glass and finale. `static/brand-world.js` handles forest atmosphere and the four-format product reveal. `static/bottle-3d.js` builds the bottle, cap, threads, condensation and material textures; `static/water-3d.js` attaches flowing water to the bottle mouth in world coordinates. The pouring scene uses a 3D glass with a rising water level. The story starts with GangaShree Roots and ends with four bottle formats. Source artwork remains in `static/images`; the product grid retains the approved photographic artwork.

Three.js 0.186.1 is vendored in `static/vendor/three` with its MIT license. No Node build or CDN connection is required to run the Flask site. Browser verification uses the installed Chrome executable:

```powershell
python -m pip install playwright
python tests/browser_check.py
```

The browser check verifies actual WebGL initialization, pinning, scroll-driven cap/flow, reverse scrubbing, responsive layouts, enquiries and reduced motion. Screenshots are saved under `test-results/`.

The animation reference and REA inspection are documented in `REFERENCES.md`. GSAP 3.15.0 is served locally from `static/vendor/gsap`; its source headers and upstream license link are retained.
