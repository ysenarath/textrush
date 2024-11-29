from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=False)

# Dictionary of keywords (clean_name -> [keywords])
keywords = {
    # Abbreviations
    "Doctor": ["Dr."],
    "Mister": ["Mr."],
    "Saint": ["St.", "St. Mary's"],
    # Special characters
    "Test": ["-test-", "--test--"],
    "Simple Test": ["test"],
    "Double Test": ["--test--"],
    # Mixed cases with punctuation
    "Saint Mary's": ["St. Mary's"],
    "OConnor": ["O'Connor"],
    "SmithJones": ["Smith-Jones"],
}

kp.add_keywords_from_dict(keywords)

text = """Dr. Smith-Jones visited St. Mary's.
There's a -test- and a --test-- here."""

matches = kp.extract_keywords(text)
print(matches)  # ['Doctor', 'SmithJones', 'Saint', "Saint Mary's", ...]
