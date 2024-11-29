import unittest
from textrush import KeywordProcessor


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.keyword_processor = KeywordProcessor(case_sensitive=True)
        self.vocab = {
            "": "empty",
            " ": "space",
            "  ": "double space",
            "a": "letter",
            "café": "coffee",
            "CAFÉ": "COFFEE",
            "$100": "hundred dollars",
            "100%": "hundred percent",
            "@user@": "username",
            "@user": "at-user",
            "user@": "user-at",
            "....": "ellipsis",
            "..": "dots",
        }
        # clean_names = {}
        for clean_name, keyword in self.vocab.items():
            self.keyword_processor.add_keyword(keyword, clean_name)
            # clean_names.setdefault(clean_name, []).append(keyword)
        # self.keyword_processor.add_keywords_from_dict(clean_names)
        print(self.keyword_processor.get_all_keywords())

    def test_unicode_characters(self):
        text = "Visit the café or CAFÉ"
        results = self.keyword_processor.extract_keywords(text, span_info=True)

        # Both café and CAFÉ should match to their respective values
        self.assertEqual(len(results), 2)

        mappings = {}
        for clean_text, start, end in results:
            surface_form = text[start:end]
            mappings[surface_form] = clean_text
        self.assertEqual(mappings["café"], "coffee")
        self.assertEqual(mappings["CAFÉ"], "COFFEE")

    def test_special_symbols(self):
        text = "Price is $100 with 100% satisfaction"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        # Check currency and percentage symbols
        matched_values = [result[0] for result in results]
        print(matched_values)
        self.assertIn("hundred dollars", matched_values)
        self.assertIn("hundred percent", matched_values)

    def test_user_mentions(self):
        text = "Contact @user@ or @user or user@"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        actual_matches = [result[0] for result in results]
        # Check all user mention patterns
        self.assertIn("username", actual_matches)
        self.assertIn("at-user", actual_matches)
        self.assertIn("user-at", actual_matches)

    def test_dots_and_spaces(self):
        text = "Some dots .. and more.... with  spaces"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        # self.assertEqual(len(results), 0)
        print(results)


if __name__ == "__main__":
    unittest.main()
