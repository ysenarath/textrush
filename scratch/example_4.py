from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=True)
keywords = {
    # Basic Emojis
    "😊": "smile",
    "❤️": "heart",
    "🌟": "star",
    # Complex Emoji Sequences
    "👨‍💻": "technologist",
    "👨‍👩‍👧‍👦": "family",
    "🏳️‍🌈": "rainbow flag",
    # Emoji-Text Combinations
    "I❤️NY": "i love new york",
    "🎉Party": "celebration party",
    # Special Symbols
    "©": "copyright",
    "®": "registered",
    "™": "trademark",
    "°C": "celsius",
    # Mathematical Symbols
    "π": "pi",
    "∑": "sum",
    "√": "square root",
    "≠": "not equal",
    # Currency Symbols
    "€": "euro",
    "£": "pound",
    "₿": "bitcoin",
}
kp.add_keywords_from_dict(keywords)

# Process text with mixed symbols
text = """Product™ (©2023)
Temperature: 20°C
Developer: 👨‍💻
Rating: ⭐⭐⭐
Price: 99€ or 1₿
Satisfaction: 😊"""

matches = kp.extract_keywords(text)
print(
    matches
)  # ['trademark', 'copyright', 'celsius', 'technologist', 'euro', 'bitcoin', 'smile']
