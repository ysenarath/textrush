from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=False)
keywords = {
    # Abbreviations
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "St.": "Saint",
    # Special characters
    "-test-": "Test",
    "--test--": "Double Test",
    "test": "Simple Test",
    # Mixed cases with punctuation
    "St. Mary's": "Saint Mary's",
    "O'Connor": "OConnor",
    "Smith-Jones": "SmithJones",
}
kp.add_keywords_from_dict(keywords)

text = """Dr. Smith-Jones visited St. Mary's.
There's a -test- and a --test-- here."""

matches = kp.extract_keywords(text)
print(matches)  # ['Doctor', 'SmithJones', 'Saint', "Saint Mary's", ...]
