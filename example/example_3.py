from textrush import KeywordProcessor

# Initialize processor
keyword_processor = KeywordProcessor(case_sensitive=False)

dictionary = {
    "St.": "Saint",
    "St. John": "Saint John",
    "St. John's": "Saint John's",
    "John's": "Johnny's",
    "New St.": "New Saint",
    "New St. John's": "New Saint John's",
    "-test-": "Test",
    "--test--": "Double Test",
    "test": "Simple Test",
}

# Add complex patterns with special characters and spaces
for k, v in dictionary.items():
    keyword_processor.add_keyword(k, v)

# Test text with special characters, punctuation, and complex overlapping
text = """Visit St. John's Cathedral on New St. John's Road.
There's a -test- and a --test-- and just a test here.
The ST. JOHN'S market near St. John street has great food."""

annotations = keyword_processor.extract_keywords(text, span_info=True)

lower_dict = {k.lower(): v for k, v in dictionary.items()}

for ann in annotations:
    ann_clean, ann_start, ann_end = ann
    surface_form = text[ann_start:ann_end]
    print((*ann, surface_form))
    assert lower_dict[surface_form.lower()] == ann_clean
