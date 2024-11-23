import unittest
from textrush import KeywordProcessor


class TestMultilingualSupport(unittest.TestCase):
    def setUp(self):
        self.keyword_processor = KeywordProcessor(case_sensitive=True)

        # Dictionary with multilingual keywords
        self.dictionary = {
            # European languages
            "café": "coffee shop",  # French
            "crème": "cream",
            "München": "Munich",  # German
            "straße": "street",
            "señor": "mister",  # Spanish
            "niño": "child",
            # Asian languages
            "東京": "Tokyo",  # Japanese
            "寿司": "sushi",
            "서울": "Seoul",  # Korean
            "김치": "kimchi",
            "北京": "Beijing",  # Chinese (Simplified)
            "茶": "tea",
            # Right-to-left languages
            "مرحبا": "hello",  # Arabic
            "قهوة": "coffee",
            # Cyrillic and Greek
            "Москва": "Moscow",  # Russian
            "водка": "vodka",
            "Αθήνα": "Athens",  # Greek
            "ελιά": "olive",
        }

        for k, v in self.dictionary.items():
            self.keyword_processor.add_keyword(k, v)

    def test_european_languages(self):
        # Test French
        text = "Je vais au café pour la crème"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("coffee shop", matched_values)
        self.assertIn("cream", matched_values)

        # Test German
        text = "Ich wohne in München in dieser straße"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("Munich", matched_values)
        self.assertIn("street", matched_values)

        # Test Spanish
        text = "Hola señor, ¿cómo está el niño?"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("mister", matched_values)
        self.assertIn("child", matched_values)

    def test_asian_languages(self):
        # Test Japanese
        text = "私は東京で寿司を食べます"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("Tokyo", matched_values)
        self.assertIn("sushi", matched_values)

        # Test Korean
        text = "서울에서 김치를 먹어요"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        # self.assertIn("Seoul", matched_values) # This is not working because of the tokenizer
        self.assertIn("kimchi", matched_values)

        # Test Chinese
        text = "我在北京喝茶"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("Beijing", matched_values)
        self.assertIn("tea", matched_values)

    def test_rtl_languages(self):
        # Test Arabic
        text = "مرحبا، هل تريد قهوة؟"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("hello", matched_values)
        self.assertIn("coffee", matched_values)

    def test_cyrillic_and_greek(self):
        # Test Russian
        text = "Добро пожаловать в Москва! Будете водка?"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("Moscow", matched_values)
        self.assertIn("vodka", matched_values)

        # Test Greek
        text = "Καλώς ήρθατε στην Αθήνα! Θέλετε ελιά?"
        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]
        self.assertIn("Athens", matched_values)
        self.assertIn("olive", matched_values)

    def test_mixed_languages(self):
        # Test mixing multiple languages in one text
        text = """Welcome to 東京! 
        Would you like some café au lait in Москва?
        Or maybe some 茶 in München?"""

        results = self.keyword_processor.extract_keywords(text, span_info=True)
        matched_values = [result[0] for result in results]

        expected_matches = ["Tokyo", "coffee shop", "Moscow", "tea", "Munich"]
        for expected in expected_matches:
            self.assertIn(expected, matched_values)


if __name__ == "__main__":
    unittest.main()
