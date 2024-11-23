import unittest
from textrush import KeywordProcessor


class TestOverlappingKeywords(unittest.TestCase):
    def setUp(self):
        self.keyword_processor = KeywordProcessor(case_sensitive=False)
        self.dictionary = {
            "Big Ben": "Clock Tower",
            "Big Ben Apple": "New York",
            "Apple": "Just Apple",
        }
        for k, v in self.dictionary.items():
            self.keyword_processor.add_keyword(k, v)
        # Convert dictionary to lowercase for case-insensitive comparison
        self.lower_dict = {k.lower(): v for k, v in self.dictionary.items()}

    def test_basic_overlapping(self):
        text = "I love Big Ben Apple and the big apple."
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matches = {}
        counts = {}
        for clean_text, start, end in results:
            surface_form = text[start:end]
            matches[surface_form.lower()] = clean_text
            counts[clean_text] = counts.get(clean_text, 0) + 1
        # Big Ben Apple is matched once
        self.assertEqual(
            matches["big ben apple"], "New York", "Failed to match 'Big Ben Apple'"
        )
        # "Just Apple" is matched twice. Once for "Big Ben Apple" and once for "big apple"
        # one of which is overlapping with "Big Ben Apple" above
        self.assertEqual(counts["Just Apple"], 2, "Failed to match 'Just Apple'")

    def test_case_insensitive(self):
        text = "BIG BEN APPLE is different from Big Ben"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matches = {}
        counts = {}
        for clean_text, start, end in results:
            surface_form = text[start:end]
            matches[surface_form.lower()] = clean_text
            counts[clean_text] = counts.get(clean_text, 0) + 1
        # Big Ben Apple is matched once
        self.assertEqual(
            matches["big ben apple"], "New York", "Failed to match 'Big Ben Apple'"
        )
        self.assertEqual(counts["New York"], 1, "Failed to match 'New York'")
        # Big Ben is matched twice (case-insensitive)
        self.assertEqual(matches["big ben"], "Clock Tower", "Failed to match 'Big Ben'")
        self.assertEqual(counts["Clock Tower"], 2, "Failed to match 'Clock Tower'")
        # Apple is matched once
        self.assertEqual(matches["apple"], "Just Apple", "Failed to match 'Apple'")
        self.assertEqual(counts["Just Apple"], 1, "Failed to match 'Just Apple'")


if __name__ == "__main__":
    unittest.main()
