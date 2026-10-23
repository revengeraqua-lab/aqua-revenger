import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request, Response
from content import COMPANY, PHONE, EMAIL, REGIONS, OFFICES, VALUES, PORTFOLIO, LEADERS, PAGES
from urllib.parse import urlencode
from xml.sax.saxutils import escape
from storage import StorageUnavailable, save_enquiry

BASE = Path(__file__).resolve().parent
PRODUCTS = [
    {"id": "250ml", "name": "The little refresh", "size": "250 ml", "pack": "24 bottles / case", "occasion": "Meetings, moments & little adventures", "bottles": 24},
    {"id": "500ml", "name": "Your everyday companion", "size": "500 ml", "pack": "24 bottles / case", "occasion": "On the move. In your element.", "bottles": 24},
    {"id": "1l", "name": "A little more life", "size": "1 litre", "pack": "12 bottles / case", "occasion": "For the long days and longer journeys", "bottles": 12},
    {"id": "2l", "name": "Refresh, together", "size": "2 litres", "pack": "9 bottles / case", "occasion": "Made for the table. Shared with everyone.", "bottles": 9},
]


def create_app(database=None):
    serverless = os.environ.get("VERCEL") == "1"
    app = Flask(__name__, static_folder=None if serverless else "public/static", static_url_path="/static")
    if serverless:
        # URLs remain /static/*; public/static is served by Vercel's CDN.
        app.add_url_rule("/static/<path:filename>", endpoint="static", build_only=True)
    database_url = None if database is not None else (os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL"))
    database_path = str(database) if database is not None else (None if serverless else str(BASE / "instance" / "revenger.sqlite3"))
    app.config.update(DATABASE=database_path, DATABASE_URL=database_url, MAX_CONTENT_LENGTH=32 * 1024)

    # Use an explicit origin so canonical URLs cannot be changed by a Host header.
    origin = os.environ.get("SITE_URL", "https://revenger-397n.vercel.app").rstrip("/")

    def brand_page(key):
        page = PAGES[key]
        canonical = origin + page["path"]
        organization = {
            "@type": "Organization", "@id": origin + "/#organization",
            "name": COMPANY, "url": origin, "email": EMAIL,
            "telephone": "+918169456633", "brand": {"@type": "Brand", "name": "Revenger"},
            "address": [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"], "addressRegion": o["state"], "postalCode": o["pin"], "addressCountry": "IN"} for o in OFFICES],
            "areaServed": [{"@type": "AdministrativeArea", "name": city} for cities in REGIONS.values() for city in cities],
            "employee": [{"@type": "Person", "name": l["name"], "jobTitle": l["role"]} for l in LEADERS],
        }
        # Client-supplied portraits are tracked assets served by the static CDN.
        leaders = LEADERS
        for person, leader in zip(organization["employee"], leaders):
            if leader["portrait"]:
                person["image"] = origin + "/static/" + leader["portrait"]
        graph = [organization, {"@type": "WebSite", "@id": origin + "/#website", "url": origin, "name": "Revenger", "publisher": {"@id": origin + "/#organization"}},
                 {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"], "description": page["description"], "isPartOf": {"@id": origin + "/#website"}}]
        if key != "home":
            graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": origin + "/"}, {"@type": "ListItem", "position": 2, "name": page["label"], "item": canonical}]})
        return render_template("brand.html", key=key, page=page, pages=PAGES, company=COMPANY,
            phone=PHONE, email=EMAIL, regions=REGIONS, offices=OFFICES, values=VALUES,
            portfolio=PORTFOLIO, water_formats=PRODUCTS, leaders=leaders, canonical=canonical,
            share_image=origin + "/static/images/revenger-bottle-real.png",
            schema={"@context": "https://schema.org", "@graph": graph},
            map_url=lambda office: "https://www.google.com/maps/search/?" + urlencode({"api": 1, "query": office["street"] + ", " + office["city"] + ", " + office["pin"]}))

    for key, page in PAGES.items():
        app.add_url_rule(page["path"], endpoint=key, view_func=lambda key=key: brand_page(key))

    @app.get("/robots.txt")
    def robots():
        return Response("User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: " + origin + "/sitemap.xml\n", mimetype="text/plain")

    @app.get("/sitemap.xml")
    def sitemap():
        body = ''.join("<url><loc>" + escape(origin + p["path"]) + "</loc></url>" for p in PAGES.values())
        return Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + '</urlset>', mimetype="application/xml")

    @app.errorhandler(404)
    def missing_page(error):
        return render_template("404.html"), 404

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", enquiries="configured" if app.config["DATABASE_URL"] or app.config["DATABASE"] else "unconfigured")

    @app.get("/api/products")
    def api_products():
        return jsonify(products=PORTFOLIO)

    @app.post("/api/enquiries")
    def enquiry():
        import json
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Please send a valid enquiry."), 400
        fields = {}
        for key in ("name", "phone", "email", "city", "kind", "message"):
            value = data.get(key, "")
            if not isinstance(value, str) or len(value) > (2000 if key == "message" else 180):
                return jsonify(error="Please check your enquiry details."), 400
            fields[key] = value.strip()
        if len(fields["name"]) < 2 or len(fields["city"]) < 2:
            return jsonify(error="Please enter your name and city."), 400
        if not re.fullmatch(r"[+\d\s()-]{10,20}", fields["phone"]) or not 10 <= len(re.sub(r"\D", "", fields["phone"])) <= 15:
            return jsonify(error="Please enter a valid phone number."), 400
        if fields["email"] and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", fields["email"]):
            return jsonify(error="Please enter a valid email address."), 400
        if fields["kind"] not in ("order", "distributor", "general"):
            return jsonify(error="Please select an enquiry type."), 400
        items = data.get("items", [])
        if not isinstance(items, list) or len(items) > len(PRODUCTS):
            return jsonify(error="Please check your selected cases."), 400
        clean_items = []
        for item in items:
            if not isinstance(item, dict) or item.get("id") not in {p["id"] for p in PRODUCTS} or type(item.get("quantity")) is not int or not 1 <= item["quantity"] <= 100:
                return jsonify(error="Please choose between 1 and 100 cases per size."), 400
            clean_items.append({"id": item["id"], "quantity": item["quantity"]})
        if fields["kind"] == "order" and not clean_items:
            return jsonify(error="Add a case to your bag first."), 400
        reference = "RV-" + uuid.uuid4().hex[:10].upper()
        try:
            save_enquiry(app.config, (reference, datetime.now(timezone.utc).isoformat(), fields["name"], fields["phone"], fields["email"], fields["city"], fields["kind"], fields["message"], json.dumps(clean_items)))
        except StorageUnavailable:
            app.logger.error("Enquiry storage unavailable; no enquiry was saved.")
            return jsonify(error="Online enquiries are temporarily unavailable. Please try again later."), 503
        return jsonify(reference=reference, message="Your enquiry has been saved. Keep your reference for follow-up."), 201

    @app.after_request
    def headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

    return app


app = create_app()
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))
