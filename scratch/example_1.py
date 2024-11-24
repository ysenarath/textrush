from textrush import KeywordProcessor

# Initialize the processor (case-insensitive by default)
kp = KeywordProcessor(case_sensitive=False)

# Add keywords individually
kp.add_keyword("python", "Python Programming Language")

# Add multiple keywords from a dictionary
keywords = {
    "rust": "Rust Programming Language",
    "machine learning": "ML",
    "artificial intelligence": "AI",
}
kp.add_keywords_from_dict(keywords)

# Extract keywords
text = "I love Python and Rust for Machine Learning and Artificial Intelligence"
keywords = kp.extract_keywords(text)
print(
    keywords
)  # ['Python Programming Language', 'Rust Programming Language', 'ML', 'AI']

# Extract with span information
spans = kp.extract_keywords(text, span_info=True)
print(spans)
