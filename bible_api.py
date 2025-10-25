from flask import Flask, request, jsonify
from bible_loader import BibleLoader
from bible_searcher import BibleSearcher

class BibleAPI:

    def __init__(self, bible_file):
        self.app = Flask(__name__)

        self.bible_loader = BibleLoader(bible_file)
        self.bible_loader.load()

        self.searcher = BibleSearcher(self.bible_loader.get_verses())

        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def home():
            return jsonify({
                "message": "Welcome to the Bible Search (KJV)",
            })

        @self.app.route("/search", methods=["GET"])
        def search_verses():
            query = request.args.get("q", "").strip()
            fuzzy = request.args.get("fuzzy", "false").lower() == "true"

            if not query:
                return jsonify({"error": "Please provide a search query"}), 400

            results = self.searcher.search(query, use_fuzzy=fuzzy)

            return jsonify({
                "query": query,
                "count": len(results),
                "results": results
            })

    def run(self):
        self.app.run(debug=False)
