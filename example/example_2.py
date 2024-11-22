from textrush import KeywordProcessor

# Initialize with case sensitivity off
keyword_processor = KeywordProcessor(case_sensitive=False)

# Add various overlapping and nested keywords
keyword_processor.add_keyword("New", "City")
keyword_processor.add_keyword("New York", "NYC")
keyword_processor.add_keyword("New York City", "The Big Apple")
keyword_processor.add_keyword("York City Center", "YCC")
keyword_processor.add_keyword("City Center", "Downtown")
keyword_processor.add_keyword("Center", "Middle")

# Test text with multiple overlapping matches and repeated patterns
text = """Welcome to New York City Center! 
The New York skyline is amazing. 
You can find another City Center downtown, 
but the New YORK CITY is the most famous one."""

print("Found keywords:")
print(list(keyword_processor.extract_keywords(text)))

# Expected matches:
# [
#   'New', 'New York', 'New York City', 'York City Center', 'City Center', 'Center',  # from first line
#   'New', 'New York',  # from second line
#   'City Center', 'Center',  # from third line
#   'New', 'New York', 'New York City'  # from fourth line
# ]
