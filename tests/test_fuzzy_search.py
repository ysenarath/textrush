import unittest
from textrush import KeywordProcessor


class TestFuzzySearch(unittest.TestCase):
    def setUp(self):
        self.processor = KeywordProcessor()
        # Add some sample keywords
        self.processor.add_keyword("python")
        self.processor.add_keyword("programming")
        self.processor.add_keyword("development")
        self.processor.add_keyword("software")
        self.processor.add_keyword("code")

    def test_exact_match(self):
        # Test exact matches still work with high threshold
        matches = self.processor.fuzzy_search(query="python", threshold=0.9)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "python")
        self.assertAlmostEqual(matches[0][1], 1.0)

    def test_close_match(self):
        # Test close matches with minor typos
        matches = self.processor.fuzzy_search(query="pythn", threshold=0.8)
        self.assertTrue(len(matches) > 0)
        self.assertEqual(matches[0][0], "python")
        self.assertGreater(matches[0][1], 0.8)

    def test_multiple_matches(self):
        # Test multiple matches with varying similarities
        matches = self.processor.fuzzy_search(query="programing", threshold=0.8)
        self.assertTrue(len(matches) > 0)
        # Should match "programming" with high similarity
        self.assertEqual(matches[0][0], "programming")
        self.assertGreater(matches[0][1], 0.8)

    def test_no_matches(self):
        # Test when no matches meet the threshold
        matches = self.processor.fuzzy_search(query="xyz", threshold=0.8)
        self.assertEqual(len(matches), 0)

    def test_threshold_filtering(self):
        # Test different thresholds
        high_threshold = self.processor.fuzzy_search(query="progamming", threshold=0.9)
        low_threshold = self.processor.fuzzy_search(query="progamming", threshold=0.7)
        self.assertTrue(len(low_threshold) >= len(high_threshold))

    def test_case_sensitivity(self):
        # Test case insensitive matching
        matches = self.processor.fuzzy_search(query="PYTHON", threshold=0.8)
        self.assertTrue(len(matches) > 0)
        self.assertEqual(matches[0][0], "python")
        self.assertGreater(matches[0][1], 0.8)


if __name__ == "__main__":
    unittest.main()
