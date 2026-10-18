import os
import re
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE = Path(__file__).resolve().parent
PRODUCTS = [
    {"id": "250ml", "name": "The little refresh", "size": "250 ml", "pack": "24 bottles / case", "occasion": "Meetings, moments & little adventures", "bottles": 24},
    {"id": "500ml", "name": "Your everyday companion", "size": "500 ml", "pack": "24 bottles / case", "occasion": "On the move. In your element.", "bottles": 24},
    {"id": "1l", "name": "A little more life", "size": "1 litre", "pack": "12 bottles / case", "occasion": "For the long days and longer journeys", "bottles": 12},
    {"id": "2l", "name": "Refresh, together", "size": "2 litres", "pack": "9 bottles / case", "occasion": "Made for the table. Shared with everyone.", "bottles": 9},
]


def create_app(database=None):
    app = Flask(__name__)
    app.config.update(DATABASE=str(database or BASE / "instance" / "revenger.sqlite3"), MAX_CONTENT_LENGTH=32 * 1024)
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(app.config["DATABASE"])) as db:
        db.execute("CREATE TABLE IF NOT EXISTS enquiries (reference TEXT PRIMARY KEY, created_at TEXT NOT NULL, name TEXT NOT NULL, phone TEXT NOT NULL, email TEXT, city TEXT NOT NULL, kind TEXT NOT NULL, message TEXT, items TEXT)")
        db.commit()

    @app.get("/")
    def home():
        return render_template("index.html", products=PRODUCTS)

    @app.get("/api/products")
    def products():
        return jsonify(products=PRODUCTS)

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
        with closing(sqlite3.connect(app.config["DATABASE"])) as db:
            db.execute("INSERT INTO enquiries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (reference, datetime.now(timezone.utc).isoformat(), fields["name"], fields["phone"], fields["email"], fields["city"], fields["kind"], fields["message"], json.dumps(clean_items)))
            db.commit()
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
