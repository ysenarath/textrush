from textrush import KeywordProcessor

keyword_processor = KeywordProcessor(case_sensitive=False)

dictionary = {
    "Big Ben": "Clock Tower",
    "Big Ben Apple": "New York",
    "Apple": "Just Apple",
}

# Add various overlapping and nested keywords
for k, v in dictionary.items():
    keyword_processor.add_keyword(k, v)

# Test text with multiple overlapping matches and repeated patterns
text = "I love Big Ben Apple and the big apple."

annotations = keyword_processor.extract_keywords(text, span_info=True)

lower_dict = {k.lower(): v for k, v in dictionary.items()}

for ann in annotations:
    ann_clean, ann_start, ann_end = ann
    surface_form = text[ann_start:ann_end]
    print((*ann, surface_form))
    assert lower_dict[surface_form.lower()] == ann_clean
