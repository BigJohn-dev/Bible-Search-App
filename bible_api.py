from flask import Flask, request, jsonify
from bible_loader import BibleLoader
from bible_searcher import BibleSearcher

class BibleAPI:
    """Flask-based REST API for KJV Bible searching."""

    def __init__(self, bible_file):
        self.app = Flask(__name__)

        # Load Bible once
        self.bible_loader = BibleLoader(bible_file)
        self.bible_loader.load()

        # Initialize searcher
        self.searcher = BibleSearcher(self.bible_loader.get_verses())

        # Register routes
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def home():
            return jsonify({
                "message": "📖 Welcome to the Bible Search API (KJV)",
                "usage": {
                    "text_search": "/search?q=for+God+so+loved+the+world",
                    "reference_search": "/search?q=John+3:16",
                    "optional": "Add &fuzzy=true for flexible search"
                }
            })

        @self.app.route("/search", methods=["GET"])
        def search_verses():
            query = request.args.get("q", "").strip()
            fuzzy = request.args.get("fuzzy", "false").lower() == "true"

            if not query:
                return jsonify({"error": "Please provide a search query, e.g. /search?q=love"}), 400

            results = self.searcher.search(query, use_fuzzy=fuzzy)

            return jsonify({
                "query": query,
                "fuzzy_search": fuzzy,
                "count": len(results),
                "results": results
            })

        @self.app.route("/favicon.ico")
        def favicon():
            return "", 204

    def run(self):
        self.app.run(debug=False)
