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
                "message": "📖 Welcome to the Bible Search API (KJV)",
                "usage_example": "/search?q=for%20God%20so%20loved%20the%20world"
            })

        @self.app.route("/search", methods=["GET"])
        def search_verses():
            query = request.args.get("q", "").strip()
            if not query:
                return jsonify({"error": "Please enter text to search (e.g. /search?q=love)"}), 400

            results = self.searcher.search(query)
            return jsonify({
                "query": query,
                "count": len(results),
                "results": results
            })

    def run(self):
        self.app.run(debug=True)
