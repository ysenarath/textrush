import random
import string
import json
from pathlib import Path

# Fixed seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def generate_random_text(length, unicode=False):
    if not unicode:
        return "".join(random.choices(string.ascii_letters + " ", k=length))
    chars = string.ascii_letters + " " + "αβγδεζηθικλμνξοπρστυφχψω"
    return "".join(random.choices(chars, k=length))


def generate_keywords(count, min_len=3, max_len=10, unicode=False):
    keywords = []
    for _ in range(count):
        length = random.randint(min_len, max_len)
        if unicode:
            chars = string.ascii_letters + "αβγδεζηθικλμνξοπρστυφχψω"
        else:
            chars = string.ascii_letters
        keyword = "".join(random.choices(chars, k=length))
        keywords.append(keyword)
    return keywords


def generate_benchmark_data():
    data = {
        "ascii": {"texts": {}, "keywords": {}},
        "unicode": {"texts": {}, "keywords": {}},
    }

    # Generate ASCII data
    # Larger text sizes
    for length in [1000, 10000, 100000, 1000000]:
        data["ascii"]["texts"][str(length)] = generate_random_text(length)

    # Keyword counts up to millions
    for count in [100, 1000, 10000, 100000, 1000000]:
        print(f"Generating {count} keywords...")
        data["ascii"]["keywords"][str(count)] = generate_keywords(count)

    # Generate Unicode data
    for length in [1000, 10000, 100000]:
        data["unicode"]["texts"][str(length)] = generate_random_text(
            length, unicode=True
        )

    # More Unicode keywords
    print("Generating Unicode keywords...")
    data["unicode"]["keywords"]["10000"] = generate_keywords(10000, unicode=True)

    return data


def save_benchmark_data():
    # Create benchmark_data directory if it doesn't exist
    data_dir = Path("tests/benchmark_data")
    data_dir.mkdir(exist_ok=True)

    # Generate and save data
    print("Generating benchmark data...")
    data = generate_benchmark_data()

    print("Saving benchmark data...")
    with open(data_dir / "benchmark_dataset.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Benchmark data saved successfully!")


if __name__ == "__main__":
    save_benchmark_data()
