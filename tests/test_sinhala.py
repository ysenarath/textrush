import unittest
from textrush import KeywordProcessor


class TestSinhalaSupport(unittest.TestCase):
    def setUp(self):
        self.keyword_processor = KeywordProcessor(case_sensitive=True)
        
        # Dictionary with Sinhala keywords
        self.dictionary = {
            # Basic Sinhala words
            "අම්මා": "mother",
            "තාත්තා": "father",
            "මල්ලි": "younger brother",
            "අක්කා": "elder sister",
            
            # Words with combined letters (යුක්තාක්ෂර)
            "ක්‍රීඩා": "sports",
            "ශ්‍රී": "sri",
            "ද්විත්ව": "double",
            
            # Words with special characters
            "කර්තෘ": "author",
            "කාර්යාලය": "office",
            "පුස්තකාලය": "library",
            
            # Common phrases
            "ආයුබෝවන්": "welcome",
            "සුභ උදෑසනක්": "good morning",
            "ස්තූතියි": "thank you",
            
            # Place names
            "කොළඹ": "Colombo",
            "මහනුවර": "Kandy",
            "ගාල්ල": "Galle",
            
            # Mixed Sinhala phrases
            "ශ්‍රී ලංකා": "Sri Lanka",
            "මහා පරිමාණ": "large scale",
            "සිංහල භාෂාව": "Sinhala language"
        }
        
        for k, v in self.dictionary.items():
            self.keyword_processor.add_keyword(k, v)

    def test_basic_sinhala_words(self):
        text = "අම්මා සහ තාත්තා, මල්ලි සහ අක්කා"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        expected = ["mother", "father", "younger brother", "elder sister"]
        for exp in expected:
            self.assertIn(exp, matched_values)

    def test_combined_letters(self):
        text = "ක්‍රීඩා පිටියේ ශ්‍රී ලාංකික ද්විත්ව තරඟය"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        self.assertIn("sports", matched_values)
        self.assertIn("sri", matched_values)
        self.assertIn("double", matched_values)

    def test_special_characters(self):
        text = "කර්තෘ කාර්යාලය පුස්තකාලය අසල පිහිටා ඇත"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        self.assertIn("author", matched_values)
        self.assertIn("office", matched_values)
        self.assertIn("library", matched_values)

    def test_common_phrases(self):
        text = "ආයුබෝවන්! සුභ උදෑසනක්. ස්තූතියි."
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        self.assertIn("welcome", matched_values)
        self.assertIn("good morning", matched_values)
        self.assertIn("thank you", matched_values)

    def test_place_names(self):
        text = "කොළඹ සිට මහනුවර හරහා ගාල්ල දක්වා ගමන"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        self.assertIn("Colombo", matched_values)
        self.assertIn("Kandy", matched_values)
        self.assertIn("Galle", matched_values)

    def test_mixed_phrases(self):
        text = """ශ්‍රී ලංකාවේ සිංහල භාෂාව 
        මහා පරිමාණ පර්යේෂණයක් සිදු කෙරේ"""
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        self.assertIn("Sri Lanka", matched_values)
        self.assertIn("Sinhala language", matched_values)
        self.assertIn("large scale", matched_values)

    def test_mixed_with_english(self):
        text = """Welcome to ශ්‍රී ලංකා!
        Visit our කාර්යාලය in කොළඹ."""
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        expected = ["Sri Lanka", "office", "Colombo"]
        for exp in expected:
            self.assertIn(exp, matched_values)


if __name__ == '__main__':
    unittest.main()
