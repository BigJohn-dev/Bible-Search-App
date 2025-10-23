import os
import unittest
from bible_loader import BibleLoader
from bible_searcher import BibleSearcher


class TestBibleSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        xml_path = os.path.join(base_dir, "SF_2009-01-23_ENG_KJV_(KING JAMES VERSION)(2).xml")

        cls.loader = BibleLoader(xml_path)
        cls.loader.load()
        cls.bible_data = cls.loader.get_verses()
        cls.searcher = BibleSearcher(cls.bible_data)


    def test_get_all_verses(self):
        self.assertGreater(len(self.bible_data), 30000)

    def test_search_with_text(self):
        results = self.searcher.search("love")
        self.assertGreater(len(results), 0)
        self.assertTrue(any("love" in r["text"].lower() for r in results))

    def test_search_for_specific_verse(self):
        results = self.searcher.search("John 3:16")
        self.assertEqual(len(results), 1)
        verse = results[0]
        self.assertTrue(verse["reference"].startswith("John 3:16"))
        self.assertIn("For God so loved the world", verse["text"])

    def test_search_for_chapter(self):
        results = self.searcher.search("Genesis 1")
        self.assertGreater(len(results), 20)
        self.assertTrue(all(r["reference"].startswith("Genesis 1:") for r in results))

    def test_search_with_reference(self):
        results = self.searcher.search("for God loved world")
        self.assertTrue(any("John 3:16" in r["reference"] for r in results))


if __name__ == "__main__":
    unittest.main()
