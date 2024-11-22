from textrush import KeywordProcessor

keyword_processor = KeywordProcessor(case_sensitive=False)

keyword_processor.add_keyword("Big Ben", "Clock Tower")
keyword_processor.add_keyword("Big Ben Apple", "New York")
keyword_processor.add_keyword("Apple", "Just Apple")

text = "I love Big Ben Apple and the big apple."

print(keyword_processor.extract_keywords(text, span_info=True))
# [('Clock Tower', 7, 14), ('New York', 7, 20), ('Just Apple', 15, 20), ('Just Apple', 33, 38)]
