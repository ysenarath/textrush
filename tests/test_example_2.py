import unittest
from textrush import KeywordProcessor


class TestNestedPhrases(unittest.TestCase):
    def setUp(self):
        self.keyword_processor = KeywordProcessor(case_sensitive=False)
        self.dictionary = {
            "New": "City",
            "New York": "NYC",
            "New York City": "The Big Apple",
            "York City Center": "YCC",
            "City Center": "Downtown",
            "Center": "Middle",
        }
        for k, v in self.dictionary.items():
            self.keyword_processor.add_keyword(k, v)
        self.lower_dict = {k.lower(): v for k, v in self.dictionary.items()}

    def test_multiline_text(self):
        text = """Welcome to New York City Center! 
        The New York skyline is amazing."""
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        for clean_text, start, end in results:
            surface_form = text[start:end]
            self.assertEqual(
                self.lower_dict[surface_form.lower()],
                clean_text,
                f"Failed to match '{surface_form}'",
            )

    def test_overlapping_city_names(self):
        text = "You can find another City Center downtown"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        captured = False
        for clean_text, start, end in results:
            if not captured:
                captured = text[start:end] == "City Center"

        self.assertTrue(captured, "Failed to match 'City Center'")

    def test_case_variations(self):
        text = "the New YORK CITY is the most famous one"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        captured = False
        for clean_text, start, end in results:
            captured = text[start:end] == "New YORK CITY"

        self.assertTrue(captured, "Failed to match 'New YORK CITY'")


if __name__ == "__main__":
    unittest.main()
