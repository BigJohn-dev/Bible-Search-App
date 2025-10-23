from bible_api import BibleAPI

if __name__ == "__main__":
    bible_file = "SF_2009-01-23_ENG_KJV_(KING JAMES VERSION)(2).xml"
    api = BibleAPI(bible_file)
    api.app.run(debug=False)
