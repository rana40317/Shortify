from flask import Flask, render_template, request, jsonify, redirect
from shortener import shortenurl

app = Flask(__name__)
shortener = shortenurl()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("long_url")
    if not long_url:
        return jsonify({"error": "No URL provided"}), 400
    short_key = shortener.encode(long_url)
    short_url = request.host_url + short_key
    return jsonify({"short_url": short_url})

@app.route("/<key>")
def redirect_url(key):
    long_url = shortener.decode(key)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)