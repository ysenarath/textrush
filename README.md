# TextRush

A high-performance text processing library implemented in Rust with Python bindings, designed for efficient keyword extraction and replacement operations. TextRush excels at handling overlapping keywords, case sensitivity options, and multilingual text processing.

[![PyPI](https://img.shields.io/pypi/v/textrush)](https://pypi.org/project/textrush/)
[![Downloads](https://pepy.tech/badge/textrush)](https://pepy.tech/project/textrush)
[![License](https://img.shields.io/github/license/ysenarath/textrush)](
    https://github.com/ysenarath/textrush/blob/main/LICENSE
)
[![GitHub stars](https://img.shields.io/github/stars/ysenarath/textrush)](https://github.com/ysenarath/textrush/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ysenarath/textrush)](https://github.com/ysenarath/textrush/forks)


## Installation

```bash
pip install textrush
```

## Features

- **High Performance**: Core implementation in Rust for optimal efficiency
- **Case Sensitivity**: Optional case-sensitive or case-insensitive matching
- **Overlapping Keywords**: Compared to FlashText(2), TextRush generates overlapping matches
- **Unicode Support**: Full multilingual text processing capabilities, including complex scripts
- **Special Character Support**: Comprehensive handling of emojis, symbols, abbreviations, and Unicode characters
- **Span Information**: Optional position tracking for matched keywords

## Quick Start

```python
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
```

## Advanced Usage

### Nested Phrases and Overlapping Keywords

TextRush handles overlapping keywords:

```python
from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=False)

keywords = {
    "City": ["New"],
    "NYC": ["New York"],
    "The Big Apple": ["New York City"],
    "YCC": ["York City Center"],
    "Downtown": ["City Center"],
    # Overlapping abbreviations
    "Saint": ["St."],
    "Saint John": ["St. John"],
    "Saint John's": ["St. John's"],
    "New Saint John's": ["New St. John's"],
}
kp.add_keywords_from_dict(keywords)

# Process nested phrases
text = "Welcome to New York City Center!"
matches = kp.extract_keywords(text)
print(matches)  # ['City', 'NYC', 'The Big Apple', 'YCC', 'Downtown']

# Process abbreviations
text = "Visit New St. John's Cathedral"
matches = kp.extract_keywords(text)
print(matches)  # ['City', "New Saint John's", 'Saint', "Saint John's"]
```

### Special Characters and Abbreviations

TextRush handles special characters, punctuation, and abbreviations with ease:

```python
from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=False)

keywords = {
    # Abbreviations
    "Doctor": ["Dr."],
    "Mister": ["Mr."],
    "Saint": ["St.", "St. Mary's"],
    # Special characters
    "Test": ["-test-", "--test--"],
    "Simple Test": ["test"],
    "Double Test": ["--test--"],
    # Mixed cases with punctuation
    "Saint Mary's": ["St. Mary's"],
    "OConnor": ["O'Connor"],
    "SmithJones": ["Smith-Jones"],
}

kp.add_keywords_from_dict(keywords)

text = """Dr. Smith-Jones visited St. Mary's.
There's a -test- and a --test-- here."""

matches = kp.extract_keywords(text)
print(matches)  # ['Doctor', 'SmithJones', 'Saint', "Saint Mary's", ...]
```

### Unicode Symbols and Emojis

TextRush provides comprehensive support for Unicode symbols, emojis, and special characters:

```python
from typing import Dict, List
from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=True)

keywords: Dict[str, List[str]] = {}
for word, clean_name in {
    # Basic Emojis
    "😊": "smile",
    "❤️": "heart",
    "🌟": "star",
    # Complex Emoji Sequences
    "👨‍💻": "technologist",
    "👨‍👩‍👧‍👦": "family",
    "🏳️‍🌈": "rainbow flag",
    # Emoji-Text Combinations
    "I❤️NY": "i love new york",
    "🎉Party": "celebration party",
    # Special Symbols
    "©": "copyright",
    "®": "registered",
    "™": "trademark",
    "°C": "celsius",
    # Mathematical Symbols
    "π": "pi",
    "∑": "sum",
    "√": "square root",
    "≠": "not equal",
    # Currency Symbols
    "€": "euro",
    "£": "pound",
    "₿": "bitcoin",
}.items():
    keywords.setdefault(clean_name, []).append(word)

kp.add_keywords_from_dict(keywords)

print(kp.get_all_keywords())
# ['©', '≠', '€', 'I❤️NY', '£', '∑', '🌟', 'π', '₿', ...]

# Process text with mixed symbols
text = """Product™ (©2023)
Temperature: 20°C
Developer: 👨‍💻
Rating: ⭐⭐⭐
Price: 99€ or 1₿
Satisfaction: 😊"""

matches = kp.extract_keywords(text)
print(matches)
# ['trademark', 'copyright', 'celsius', 'technologist', ...]
```

### Multilingual Support

TextRush provides robust support for multiple languages and scripts, including:

- European Languages (French, German, Spanish)
- Asian Scripts (Japanese, Korean, Chinese)
- Right-to-Left Scripts (Arabic)
- Cyrillic and Greek
- Complex Scripts (Sinhala with යුක්තාක්ෂර support)

```python
from textrush import KeywordProcessor

kp = KeywordProcessor(case_sensitive=True)

# clean_name -> [keywords]
keywords = {
    # European Languages
    "coffee shop": ["café"],
    "Munich": ["München"],
    # Asian Scripts
    "Tokyo": ["東京"],
    "Seoul": ["서울"],
    "Beijing": ["北京"],
    # Right-to-Left Scripts
    "hello": ["مرحبا"],  # Arabic
    "coffee": ["قهوة"],  # Arabic
    # Cyrillic and Greek
    "Moscow": ["Москва"],
    "Athens": ["Αθήνα"],
    # Complex Scripts (Sinhala)
    "sports": ["ක්‍රීඩා"],
    "author": ["කර්තෘ"],
    "Sri Lanka": ["ශ්‍රී ලංකා"],
}
kp.add_keywords_from_dict(keywords)

# Mixed language text processing
text = """Welcome to ශ්‍රී ලංකා! 
Would you like some café in Москва?
Visit 東京 for the ක්‍රීඩා competition."""

matches = kp.extract_keywords(text)
print(matches)
# ['Sri Lanka', 'coffee shop', 'Moscow', 'Tokyo', 'sports']
```

## API Reference

### KeywordProcessor

#### Constructor

```python
KeywordProcessor(case_sensitive: bool = False)
```
- `case_sensitive`: Whether to perform case-sensitive matching (default: False)

#### Methods

##### add_keyword
```python
add_keyword(keyword: str, clean_name: str = None)
```
- `keyword`: The keyword to match in text
- `clean_name`: The replacement text (defaults to keyword if None)

##### add_keywords_from_dict
```python
add_keywords_from_dict(
    self,
    mapping: Mapping[str, Iterable[str] | str],
    errors: str = "raise",
)
```
- `dictionary`: Dictionary mapping keywords to their clean names
- `errors`: How to handle invalid keywords ("ignore" or "raise")

##### extract_keywords
```python
extract_keywords(text: str, span_info: bool = False, strategy: str = "all") -> List[str]
```
- `text`: The input text to process
- `span_info`: Whether to include position information
- `strategy`: How to handle overlapping keywords ("all", "longest")
- Returns: List of matches or list of (match, start, end) tuples if span_info=True

##### replace_keywords
```python
replace_keywords(text: str) -> str
```
- `text`: The input text to process
- Returns: Text with all keywords replaced by their clean names

## Performance

TextRush is intended for high-performance text processing tasks, with a focus on speed. The benchamrk results are provided in [this page](https://github.com/ysenarath/textrush/blob/main/tests/benchmark_results/benchmark_results.md).

## Credits

TextRush is inspired by and builds upon the work of:
- [FlashText](https://github.com/vi3k6i5/flashtext) - The original Python implementation
- [FlashText2-rs](https://github.com/shner-elmo/flashtext2-rs) - A Rust implementation of FlashText

## License

MIT License - see LICENSE file for details
