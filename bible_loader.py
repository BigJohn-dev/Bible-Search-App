import xml.etree.ElementTree as ET

class BibleLoader:

    def __init__(self, filename):
        self.filename = filename
        self.verses = []

    def load(self):
        print("Loading Bible... please wait.")

        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()

            for book in root.findall(".//BIBLEBOOK"):
                book_name = book.attrib.get("bname", "Unknown")

                for chapter in book.findall(".//CHAPTER"):
                    chapter_num = chapter.attrib.get("cnumber")

                    for verse in chapter.findall(".//VERS"):
                        verse_num = verse.attrib.get("vnumber")
                        text = (verse.text or "").strip()

                        self.verses.append({
                            "book": book_name,
                            "chapter": chapter_num,
                            "verse": verse_num,
                            "text": text,
                            "text_lower": text.lower()
                        })

            print(f"Loaded {len(self.verses)} verses from {self.filename}")

        except FileNotFoundError:
            print(f"File not found: {self.filename}")
        except ET.ParseError as e:
            print(f"XML parsing error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def get_verses(self):
        return self.verses
