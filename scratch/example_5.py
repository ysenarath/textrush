from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=True)

keywords = {
    # European Languages
    "café": "coffee shop",  # French
    "München": "Munich",  # German
    # Asian Scripts
    "東京": "Tokyo",  # Japanese
    "서울": "Seoul",  # Korean
    "北京": "Beijing",  # Chinese
    # Right-to-Left Scripts
    "مرحبا": "hello",  # Arabic
    "قهوة": "coffee",
    # Cyrillic and Greek
    "Москва": "Moscow",  # Russian
    "Αθήνα": "Athens",  # Greek
    # Complex Scripts (Sinhala)
    "ක්‍රීඩා": "sports",  # With combined letters
    "කර්තෘ": "author",  # With special characters
    "ශ්‍රී ලංකා": "Sri Lanka",  # Mixed phrase
}
kp.add_keywords_from_dict(keywords)

# Mixed language text processing
text = """Welcome to ශ්‍රී ලංකා! 
Would you like some café in Москва?
Visit 東京 for the ක්‍රීඩා competition."""

matches = kp.extract_keywords(text)
print(matches)  # ['Sri Lanka', 'coffee shop', 'Moscow', 'Tokyo', 'sports']
