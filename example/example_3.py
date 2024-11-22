from textrush import KeywordProcessor

# Initialize processor
keyword_processor = KeywordProcessor(case_sensitive=False)

# Add complex patterns with special characters and spaces
keyword_processor.add_keyword("St.", "Saint")
keyword_processor.add_keyword("St. John", "Saint John")
keyword_processor.add_keyword("St. John's", "Saint John's")
keyword_processor.add_keyword("John's", "Johnny's")
keyword_processor.add_keyword("New St.", "New Saint")
keyword_processor.add_keyword("New St. John's", "New Saint John's")
keyword_processor.add_keyword("-test-", "Test")
keyword_processor.add_keyword("--test--", "Double Test")
keyword_processor.add_keyword("test", "Simple Test")

# Test text with special characters, punctuation, and complex overlapping
text = """Visit St. John's Cathedral on New St. John's Road.
There's a -test- and a --test-- and just a test here.
The ST. JOHN'S market near St. John street has great food."""

print("Found keywords:")
print(list(keyword_processor.extract_keywords(text)))

# Expected matches:
# [
#   'St.', 'St. John', "St. John's",  "John's",
#   'New St.', "New St. John's", "John's",
#   '-test-', '--test--', 'test',
#   "ST. JOHN'S", 'ST.', 'St. John', "John's"
# ]
