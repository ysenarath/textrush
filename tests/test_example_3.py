import unittest
from textrush import KeywordProcessor


class TestSpecialCharacters(unittest.TestCase):
    def setUp(self):
        self.keyword_processor = KeywordProcessor(case_sensitive=False)
        self.dictionary = {
            "St.": "Saint",
            "St. John": "Saint John",
            "St. John's": "Saint John's",
            "John's": "Johnny's",
            "New St.": "New Saint",
            "New St. John's": "New Saint John's",
            "-test-": "Test",
            "--test--": "Double Test",
            "test": "Simple Test",
        }
        for k, v in self.dictionary.items():
            self.keyword_processor.add_keyword(k, v)
        self.lower_dict = {k.lower(): v for k, v in self.dictionary.items()}

    def test_abbreviations(self):
        text = "Visit St. John's Cathedral"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        captured = False
        for clean_text, start, end in results:
            if text[start:end].lower() == "st. john's":
                captured = True
                self.assertEqual(clean_text, "Saint John's")

        self.assertTrue(captured, "Failed to match 'St. John's'")

    def test_nested_abbreviations(self):
        text = "on New St. John's Road"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        captured = False
        for clean_text, start, end in results:
            if text[start:end].lower() == "new st. john's":
                captured = True
                self.assertEqual(clean_text, "New Saint John's")

        self.assertTrue(captured, "Failed to match 'New St. John's'")

    def test_special_characters(self):
        text = "There's a -test- and a --test-- and just a test here"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        expected_matches = {
            "-test-": "Test",
            "--test--": "Double Test",
            "test": "Simple Test",
        }
        found_matches = set()

        for clean_text, start, end in results:
            surface_form = text[start:end]
            found_matches.add((surface_form, clean_text))
            self.assertEqual(
                expected_matches[surface_form],
                clean_text,
                f"Failed to match '{surface_form}'",
            )

        self.assertEqual(
            len(found_matches),
            len(expected_matches),
            "Not all expected matches were found",
        )

    def test_case_insensitive_special(self):
        text = "The ST. JOHN'S market near St. John street"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        for clean_text, start, end in results:
            surface_form = text[start:end]
            self.assertEqual(
                self.lower_dict[surface_form.lower()],
                clean_text,
                f"Failed to match '{surface_form}'",
            )


if __name__ == "__main__":
    unittest.main()
