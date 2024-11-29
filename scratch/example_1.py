from textrush import KeywordProcessor

# Initialize the processor (case-insensitive by default)
kp = KeywordProcessor(case_sensitive=False)

# Add keywords individually
kp.add_keyword("python", "Python Programming Language")

# Add multiple keywords from a dictionary
keywords = {
    "Rust Programming Language": ["rust"],
    "ML": ["machine learning"],
    "AI": ["artificial intelligence"],
    "Machine": ["system", "device", "machine"],
}
kp.add_keywords_from_dict(keywords)

# Extract keywords
text = "I love Python and Rust for Machine Learning and Artificial Intelligence"
keywords = kp.extract_keywords(text)
print(keywords)
# ['Python Programming Language', 'Rust Programming Language', 'Machine', 'ML', 'AI']

# Extract with span information
spans = kp.extract_keywords(text, span_info=True)
print(spans)
# [('Python Programming Language', 7, 13), ('Rust Programming Language', 18, 22), ('Machine', 27, 34), ('ML', 27, 43), ('AI', 48, 71)]

# return only the longest keywords
keywords = kp.extract_keywords(text, span_info=False, strategy="longest")
print(keywords)
# ['Python Programming Language', 'Rust Programming Language', 'ML', 'AI']
