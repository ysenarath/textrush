import unittest
from textrush import KeywordProcessor


class TestUnicodeSymbols(unittest.TestCase):
    def setUp(self):
        self.keyword_processor = KeywordProcessor(case_sensitive=True)
        
        # Dictionary with emojis and special Unicode symbols
        self.dictionary = {
            # Emojis
            "😊": "smile",
            "❤️": "heart",
            "🌟": "star",
            "🎉": "celebration",
            "👍": "thumbs up",
            
            # Emoji sequences
            "👨‍💻": "technologist",
            "👨‍👩‍👧‍👦": "family",
            "🏳️‍🌈": "rainbow flag",
            
            # Emoji with text
            "I❤️NY": "i love new york",
            "🎉Party": "celebration party",
            
            # Special Unicode symbols
            "★": "black star",
            "☆": "white star",
            "©": "copyright",
            "®": "registered",
            "™": "trademark",
            "°C": "celsius",
            "∞": "infinity",
            
            # Mathematical symbols
            "π": "pi",
            "∑": "sum",
            "√": "square root",
            "≠": "not equal",
            "≤": "less than or equal",
            
            # Currency symbols
            "€": "euro",
            "£": "pound",
            "¥": "yen",
            "₿": "bitcoin"
        }
        
        for k, v in self.dictionary.items():
            self.keyword_processor.add_keyword(k, v)

    def test_basic_emojis(self):
        text = "Hello 😊 World ❤️"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("smile", matched_values)
        self.assertIn("heart", matched_values)

    def test_emoji_sequences(self):
        text = "Developer 👨‍💻 with family 👨‍👩‍👧‍👦"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("technologist", matched_values)
        self.assertIn("family", matched_values)

    def test_emoji_with_text(self):
        text = "Welcome to I❤️NY! 🎉Party time!"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("i love new york", matched_values)
        self.assertIn("celebration party", matched_values)

    def test_special_unicode_symbols(self):
        text = "Temperature: 20°C, Rating: ★★★☆☆"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("celsius", matched_values)
        self.assertIn("black star", matched_values)
        self.assertIn("white star", matched_values)

    def test_mathematical_symbols(self):
        text = "Formula: π × r² ≠ ∞, where ∑x ≤ 10"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("pi", matched_values)
        self.assertIn("infinity", matched_values)
        self.assertIn("sum", matched_values)
        self.assertIn("not equal", matched_values)
        self.assertIn("less than or equal", matched_values)

    def test_currency_symbols(self):
        text = "Prices: 100€, 50£, 1000¥, 2₿"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("euro", matched_values)
        self.assertIn("pound", matched_values)
        self.assertIn("yen", matched_values)
        self.assertIn("bitcoin", matched_values)

    def test_mixed_symbols(self):
        text = """Product™ (©2023)
        Price: 99€ or 1₿
        Rating: ★★★★☆
        Satisfaction: 😊 100%"""
        
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        
        expected_matches = [
            "trademark", "copyright", "euro", "bitcoin",
            "black star", "white star", "smile"
        ]
        for expected in expected_matches:
            self.assertIn(expected, matched_values)


if __name__ == '__main__':
    unittest.main()
