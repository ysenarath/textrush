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

        for clean_text, start, end in results:
            surface_form = text[start:end]
            self.assertEqual(
                self.lower_dict[surface_form.lower()],
                clean_text,
                f"Failed to match '{surface_form}'",
            )

    def test_case_insensitive(self):
        text = "BIG BEN APPLE is different from Big Ben"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        # # Verify the first match is "New York" (for "BIG BEN APPLE")
        # self.assertEqual(results[0][0], "New York")

        # # Verify the second match is "Clock Tower" (for "Big Ben")
        # self.assertEqual(results[1][0], "Clock Tower")

        for clean_text, start, end in results:
            surface_form = text[start:end]
            self.assertEqual(
                self.lower_dict[surface_form.lower()],
                clean_text,
                f"Failed to match '{surface_form}'",
            )


if __name__ == "__main__":
    unittest.main()
