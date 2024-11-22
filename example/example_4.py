from textrush import KeywordProcessor

# Initialize processor
keyword_processor = KeywordProcessor(case_sensitive=False)

# Edge cases with unicode, whitespace, and special patterns
keyword_processor.add_keyword("", "empty")  # empty string
keyword_processor.add_keyword(" ", "space")  # single space
keyword_processor.add_keyword("  ", "double space")  # double space
keyword_processor.add_keyword("a", "letter")  # single letter
keyword_processor.add_keyword("café", "coffee")  # unicode
keyword_processor.add_keyword("CAFÉ", "COFFEE")  # unicode uppercase
keyword_processor.add_keyword("$100", "hundred dollars")  # starts with special char
keyword_processor.add_keyword("100%", "hundred percent")  # ends with special char
keyword_processor.add_keyword("@user@", "username")  # special chars on both ends
keyword_processor.add_keyword("@user", "at-user")  # special char prefix
keyword_processor.add_keyword("user@", "user-at")  # special char suffix
keyword_processor.add_keyword("....", "ellipsis")  # repeated special chars
keyword_processor.add_keyword("..", "dots")  # subset of another pattern

# Test text with various edge cases
text = """Visit the café or CAFÉ for $100 coffee....
Some users (@user@ and @user and user@) paid 100% 
Here are some dots .. and more....
  Multiple spaces  test  """

print("Found keywords:")
print(list(keyword_processor.extract_keywords(text)))

# Expected matches:
# [
#   'café', '$100', '....', '...',
#   '@user@', '@user', 'user@', '100%',
#   '..', '....',
#   ' ', '  ', ' '
# ]
