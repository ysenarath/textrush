from textrush import KeywordProcessor

keyword_processor = KeywordProcessor(case_sensitive=False)
keyword_processor.add_keyword("Big Ben", "Clock Tower")
keyword_processor.add_keyword("Big Ben Apple", "New York")
keyword_processor.add_keyword("Apple", "Just Apple")

text = "I love Big Ben Apple and the big apple."

print(keyword_processor.extract_keywords(text, span_info=True))
# ['Big Apple', 'big apple']
