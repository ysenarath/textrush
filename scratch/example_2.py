from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=False)

keywords = {
    "City": ["New"],
    "NYC": ["New York"],
    "The Big Apple": ["New York City"],
    "YCC": ["York City Center"],
    "Downtown": ["City Center"],
    # Overlapping abbreviations
    "Saint": ["St."],
    "Saint John": ["St. John"],
    "Saint John's": ["St. John's"],
    "New Saint John's": ["New St. John's"],
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
