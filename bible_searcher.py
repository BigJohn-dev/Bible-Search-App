import re
from functools import lru_cache
from rapidfuzz import fuzz


class BibleSearcher:

    def __init__(self, verses):
        self.verses = verses

    @lru_cache(maxsize=200)
    def search(self, query, use_fuzzy=False, threshold=80, limit=50):
        query = query.strip().lower()

        ref_match = self._parse_reference(query)
        if ref_match:
            return self._search_by_reference(*ref_match)

        return self._search_by_text(query, use_fuzzy, threshold, limit)

    def _search_by_text(self, query, use_fuzzy, threshold, limit):
        results = []
        count = 0

        for verse in self.verses:
            text_lower = verse["text_lower"]

            if not use_fuzzy and query in text_lower:
                ref = f"{verse['book']} {verse['chapter']}:{verse['verse']}"
                results.append({"reference": ref, "text": verse["text"]})
                count += 1
                if count >= limit:
                    break

            elif use_fuzzy:
                score = fuzz.partial_ratio(query, text_lower)
                if score >= threshold:
                    ref = f"{verse['book']} {verse['chapter']}:{verse['verse']}"
                    results.append({
                        "reference": ref,
                        "text": verse["text"],
                        "match_score": score
                    })
                    count += 1
                    if count >= limit:
                        break

        return sorted(results, key=lambda x: x.get("match_score", 100), reverse=True)

    def _parse_reference(self, query):
        match = re.match(r"^(?:(?P<book>[1-3]?\s?[A-Za-z]+)\s*)?(?P<chapter>\d+)(?::(?P<verse>\d+))?$", query)
        if not match:
            return None

        book = match.group("book")
        chapter = match.group("chapter")
        verse = match.group("verse")
        return (book, chapter, verse)

    def _search_by_reference(self, book, chapter, verse):
        results = []

        for v in self.verses:
            if (
                    (not book or v["book"].lower().startswith(book.lower())) and
                    v["chapter"] == chapter and
                    (not verse or v["verse"] == verse)
            ):
                ref = f"{v['book']} {v['chapter']}:{v['verse']}"
                results.append({"reference": ref, "text": v["text"]})

        return results
