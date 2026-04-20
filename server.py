from flask import Flask, request, jsonify, send_from_directory
import requests, os
from dotenv import load_dotenv

# ✅ Load .env file
load_dotenv()

API_KEY = os.getenv("GCSE_KEY")
CX_ID = os.getenv("CX_ID")

print("API_KEY Loaded:", API_KEY)
print("CX_ID Loaded:", CX_ID)

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    search_url = (
        f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX_ID}&q={query}"
    )
    print("Search URL:", search_url)

    try:
        res = requests.get(search_url, timeout=5).json()
        items = [
            {
                "title": i["title"],
                "link": i["link"],
                "snippet": i.get("snippet", "")
            }
            for i in res.get("items", [])
        ]
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
