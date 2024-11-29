import time
import json
from pathlib import Path
from datetime import datetime
from textrush import versions

version = "0.0.4-dev"

if version == "latest" or version.endswith("-dev"):
    from textrush import KeywordProcessor
else:
    KeywordProcessor = versions[version]


def load_benchmark_data():
    data_path = Path("tests/benchmark_data/benchmark_dataset.json")
    if not data_path.exists():
        # Generate data if it doesn't exist
        print("Benchmark dataset not found. Generating...")
        import benchmark_data

        benchmark_data.save_benchmark_data()

    print("Loading benchmark dataset...")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def benchmark_keyword_addition(keywords, case_sensitive=False):
    kp = KeywordProcessor(case_sensitive=case_sensitive)

    print(f"Adding {len(keywords)} keywords...")
    start_time = time.time()
    for i, keyword in enumerate(keywords):
        kp.add_keyword(keyword)
        if (i + 1) % 100000 == 0:  # Progress indicator for large sets
            print(f"Added {i + 1} keywords...")
    end_time = time.time()

    return end_time - start_time


def benchmark_keyword_extraction(text, keywords, case_sensitive=False, with_span=False):
    print(f"Preparing processor with {len(keywords)} keywords...")
    kp = KeywordProcessor(case_sensitive=case_sensitive)
    for i, keyword in enumerate(keywords):
        kp.add_keyword(keyword)
        if (i + 1) % 100000 == 0:  # Progress indicator
            print(f"Added {i + 1} keywords...")

    print(f"Extracting keywords from text of length {len(text)}...")
    start_time = time.time()
    kp.extract_keywords(text, span_info=with_span)
    end_time = time.time()

    return end_time - start_time


def run_benchmarks():
    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "version": version,
        },
        "results": {},
    }

    print(f"Running TextRush Benchmarks (v{version})...")
    data = load_benchmark_data()

    # 1. Keyword Addition Performance
    print("\n1. Keyword Addition Performance")
    print("-" * 30)
    results["results"]["keyword_addition"] = {}

    for count in ["100", "1000", "10000", "100000", "1000000"]:
        print(f"\nTesting keyword addition with {count} keywords...")
        keywords = data["ascii"]["keywords"][count]
        time_taken = benchmark_keyword_addition(keywords)
        results["results"]["keyword_addition"][count] = time_taken
        print(f"Time taken: {time_taken:.4f} seconds")

    # 2. Keyword Extraction Performance (ASCII)
    print("\n2. Keyword Extraction Performance (ASCII)")
    print("-" * 30)
    results["results"]["ascii_extraction"] = {}

    for length in ["1000", "10000", "100000", "1000000"]:
        text = data["ascii"]["texts"][length]
        results["results"]["ascii_extraction"][length] = {}
        print(f"\nTesting text length: {length}")

        for count in ["1000", "10000", "100000"]:
            print(f"Testing with {count} keywords...")
            keywords = data["ascii"]["keywords"][count]
            time_taken = benchmark_keyword_extraction(text, keywords)
            results["results"]["ascii_extraction"][length][count] = time_taken
            print(f"Time taken: {time_taken:.4f} seconds")

    # 3. Unicode Text Performance
    print("\n3. Unicode Text Performance")
    print("-" * 30)
    results["results"]["unicode_extraction"] = {}

    for length in ["1000", "10000", "100000"]:
        print(f"\nTesting Unicode text length: {length}")
        text = data["unicode"]["texts"][length]
        keywords = data["unicode"]["keywords"]["10000"]
        time_taken = benchmark_keyword_extraction(text, keywords)
        results["results"]["unicode_extraction"][length] = time_taken
        print(f"Time taken: {time_taken:.4f} seconds")

    # 4. Case Sensitivity Impact
    print("\n4. Case Sensitivity Impact")
    print("-" * 30)
    results["results"]["case_sensitivity"] = {}

    text = data["ascii"]["texts"]["100000"]
    keywords = data["ascii"]["keywords"]["10000"]

    print("\nTesting case sensitive matching...")
    time_sensitive = benchmark_keyword_extraction(text, keywords, case_sensitive=True)
    print("\nTesting case insensitive matching...")
    time_insensitive = benchmark_keyword_extraction(
        text, keywords, case_sensitive=False
    )

    results["results"]["case_sensitivity"] = {
        "sensitive": time_sensitive,
        "insensitive": time_insensitive,
    }

    print(f"Case sensitive: {time_sensitive:.4f} seconds")
    print(f"Case insensitive: {time_insensitive:.4f} seconds")

    # 5. Span Information Overhead
    print("\n5. Span Information Overhead")
    print("-" * 30)
    results["results"]["span_info"] = {}

    print("\nTesting without span information...")
    time_without_span = benchmark_keyword_extraction(text, keywords, with_span=False)
    print("\nTesting with span information...")
    time_with_span = benchmark_keyword_extraction(text, keywords, with_span=True)

    results["results"]["span_info"] = {
        "without_span": time_without_span,
        "with_span": time_with_span,
    }

    print(f"Without span info: {time_without_span:.4f} seconds")
    print(f"With span info: {time_with_span:.4f} seconds")

    # Save results
    results_dir = Path("tests/benchmark_results")
    results_dir.mkdir(exist_ok=True)

    result_file = (
        results_dir
        / f"benchmark_result_{version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nBenchmark results saved to: {result_file}")


if __name__ == "__main__":
    run_benchmarks()
