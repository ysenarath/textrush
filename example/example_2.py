from textrush import KeywordProcessor


def main():
    # Initialize the keyword processor
    processor = KeywordProcessor(case_sensitive=False)

    # Add some keywords
    processor.add_keyword("rust")
    processor.add_keyword("python")
    processor.add_keyword("programming")

    # Example texts to process
    texts = [
        "I love rust programming",
        "Python is great for development",
        "Using rust with python for efficient programming",
        "This text has no keywords",
    ]

    print("\nExample 1: Extract keywords from multiple texts")
    print("-" * 50)
    keywords = processor.extract_keywords(texts)
    for text, found_keywords in zip(texts, keywords):
        print(f"Text: {text}")
        print(f"Keywords found: {found_keywords}\n")

    print("\nExample 2: Extract keywords with positions from multiple texts")
    print("-" * 50)
    keywords_with_spans = processor.extract_keywords_with_span_from_list(texts)
    for text, spans in zip(texts, keywords_with_spans):
        print(f"Text: {text}")
        print("Keywords with positions:")
        for keyword, start, end in spans:
            print(f"  - '{keyword}' found at position {start}-{end}")
        print()


if __name__ == "__main__":
    main()
