from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=False)

keywords = {
    # Nested city names
    "New": "City",
    "New York": "NYC",
    "New York City": "The Big Apple",
    "York City Center": "YCC",
    "City Center": "Downtown",
    # Overlapping abbreviations
    "St.": "Saint",
    "St. John": "Saint John",
    "St. John's": "Saint John's",
    "New St. John's": "New Saint John's",
}
kp.add_keywords_from_dict(keywords)

# Process nested phrases
text = "Welcome to New York City Center!"
matches = kp.extract_keywords(text)
print(matches)  # ['City', 'NYC', 'The Big Apple', 'YCC', 'Downtown']

# Process abbreviations
text = "Visit New St. John's Cathedral"
matches = kp.extract_keywords(text)
print(matches)  # ['City', "New Saint John's", 'Saint', "Saint John's"]
