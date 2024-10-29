from textrush import KeywordProcessor

keyword_processor = KeywordProcessor(case_sensitive=True)
keyword_processor.add_keyword("Big Apple", "New York")

text = "I love Big Apple and the big apple."

print(keyword_processor.extract_keywords(text))
# ['Big Apple', 'big apple']
