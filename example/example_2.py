from textrush import KeywordProcessor

keyword_processor = KeywordProcessor(case_sensitive=False)

dict = {
    "New": "City",
    "New York": "NYC",
    "New York City": "The Big Apple",
    "York City Center": "YCC",
    "City Center": "Downtown",
    "Center": "Middle",
}

# Add various overlapping and nested keywords
for k, v in dict.items():
    keyword_processor.add_keyword(k, v)

# Test text with multiple overlapping matches and repeated patterns
text = """Welcome to New York City Center! 
The New York skyline is amazing. 
You can find another City Center downtown, 
but the New YORK CITY is the most famous one."""

annotations = keyword_processor.extract_keywords(text, span_info=True)

lower_dict = {k.lower(): v for k, v in dict.items()}

for ann in annotations:
    ann_clean, ann_start, ann_end = ann
    surface_form = text[ann_start:ann_end]
    print((*ann, surface_form))
    assert lower_dict[surface_form.lower()] == ann_clean
