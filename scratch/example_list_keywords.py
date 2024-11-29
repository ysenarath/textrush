from textrush import KeywordProcessor

# Initialize the processor (case-insensitive by default)
kp = KeywordProcessor(case_sensitive=True)

# Add keywords individually
kp.add_keyword("Python", "Python Programming Language")
kp.add_keyword("Rust", "Rust Programming Language")
kp.add_keyword("Machine Learning", "ML")
kp.add_keyword("Artificial Intelligence", "AI")

# Show the keywords
keywords = kp.get_all_keywords()
print(f"Number of keywords: {len(keywords)}, Type: {type(keywords)}")
print(keywords)
print()


# try replace
text = "Python is a programming language. Rust is another programming language."
replaced_text = kp.replace_keywords(text)
print(replaced_text)
print()

keywords = kp.extract_keywords(text, span_info=True)
print(keywords)


text = "python is commonly used in Machine Learning and Artificial Intelligence."
replaced_text = kp.replace_keywords(text)
print(replaced_text)

keywords = kp.extract_keywords(text, span_info=True)
print(keywords)
