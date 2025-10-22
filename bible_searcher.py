from rapidfuzz import fuzz

class BibleSearcher:

    def __init__(self, verses):
        self.verses = verses

    def search(self, query, threshold=80):
        query = query.lower()
        results = []

        for verse in self.verses:
            text = verse['text'].lower()
            score = fuzz.partial_ratio(query, text)

            if score >= threshold:
                ref = f"{verse['book']} {verse['chapter']}:{verse['verse']}"
                results.append({
                    "reference": ref,
                    "text": verse['text'],
                    "match_score": score
                })

        results = sorted(results, key=lambda x: x['match_score'], reverse=True)
        return results
