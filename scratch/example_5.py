from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=True)

# clean_name -> [keywords]
keywords = {
    # European Languages
    "coffee shop": ["café"],
    "Munich": ["München"],
    # Asian Scripts
    "Tokyo": ["東京"],
    "Seoul": ["서울"],
    "Beijing": ["北京"],
    # Right-to-Left Scripts
    "hello": ["مرحبا"],  # Arabic
    "coffee": ["قهوة"],  # Arabic
    # Cyrillic and Greek
    "Moscow": ["Москва"],
    "Athens": ["Αθήνα"],
    # Complex Scripts (Sinhala)
    "sports": ["ක්‍රීඩා"],
    "author": ["කර්තෘ"],
    "Sri Lanka": ["ශ්‍රී ලංකා"],
}
kp.add_keywords_from_dict(keywords)

# Mixed language text processing
text = """Welcome to ශ්‍රී ලංකා! 
Would you like some café in Москва?
Visit 東京 for the ක්‍රීඩා competition."""

matches = kp.extract_keywords(text)
print(matches)
# ['Sri Lanka', 'coffee shop', 'Moscow', 'Tokyo', 'sports']
