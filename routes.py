from flask import Blueprint, request, redirect, jsonify, render_template
from models import db, URL
import random
import string

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@main.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "URL required"}), 400

    short_code = generate_short_code()

    new_url = URL(
        long_url=long_url,
        short_code=short_code
    )

    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "short_url": f"http://localhost:5000/{short_code}"
    })


@main.route("/<short_code>")
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if url:
        return redirect(url.long_url)

    return jsonify({"error": "URL not found"}), 404