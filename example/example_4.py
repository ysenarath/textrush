from textrush import KeywordProcessor

# Initialize processor
keyword_processor = KeywordProcessor(case_sensitive=False)

dictionary = {
    "": "empty",
    " ": "space",
    "  ": "double space",
    "a": "letter",
    "café": "coffee",
    "CAFÉ": "COFFEE",
    "$100": "hundred dollars",
    "100%": "hundred percent",
    "@user@": "username",
    "@user": "at-user",
    "user@": "user-at",
    "....": "ellipsis",
    "..": "dots",
}

# Add complex patterns with special characters and spaces
for k, v in dictionary.items():
    keyword_processor.add_keyword(k, v)

# Test text with special characters, punctuation, and complex overlapping
text = """Visit the café or CAFÉ for $100 coffee....
Some users (@user@ and @user and user@) paid 100% 
Here are some dots .. and more....
  Multiple spaces  test  """

annotations = keyword_processor.extract_keywords(text, span_info=True)

lower_dict = {k.lower(): v for k, v in dictionary.items()}

for ann in annotations:
    ann_clean, ann_start, ann_end = ann
    surface_form = text[ann_start:ann_end]
    print((*ann, surface_form))
    assert lower_dict[surface_form.lower()] == ann_clean
