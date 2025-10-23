class BibleSearcher:
    def __init__(self, verses):
        self.verses = verses

    def search(self, query, use_fuzzy=False, threshold=80, limit=50):
        query = query.lower()
        results = []
        count = 0

        for verse in self.verses:
            text = verse['text'].lower()

            # Fast path: simple substring match
            if not use_fuzzy and query in text:
                ref = f"{verse['book']} {verse['chapter']}:{verse['verse']}"
                results.append({"reference": ref, "text": verse['text']})
                count += 1
                if count >= limit:
                    break

            # Fuzzy path: slower but flexible
            elif use_fuzzy:
                from rapidfuzz import fuzz
                score = fuzz.partial_ratio(query, text)
                if score >= threshold:
                    ref = f"{verse['book']} {verse['chapter']}:{verse['verse']}"
                    results.append({
                        "reference": ref,
                        "text": verse['text'],
                        "match_score": score
                    })
                    count += 1
                    if count >= limit:
                        break

        return results
