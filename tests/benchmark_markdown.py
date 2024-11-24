import json
from pathlib import Path
from collections import defaultdict
import re
from datetime import datetime

def find_latest_results():
    """Find the latest benchmark result for each version."""
    results_dir = Path('tests/benchmark_results')
    version_results = defaultdict(list)
    
    # Group results by version
    for result_file in results_dir.glob('benchmark_result_*.json'):
        match = re.match(r'benchmark_result_(.+?)_(\d{8}_\d{6})\.json', result_file.name)
        if match:
            version, timestamp = match.groups()
            version_results[version].append((timestamp, result_file))
    
    # Get latest result for each version
    latest_results = {}
    for version, results in version_results.items():
        # Sort by timestamp and get the latest
        latest = sorted(results, key=lambda x: x[0])[-1]
        latest_results[version] = latest[1]
    
    return latest_results

def format_time(seconds):
    """Format time in a human-readable way."""
    if seconds < 0.000001:  # < 1µs
        return f"{seconds*1000000000:.2f}ns"
    elif seconds < 0.001:  # < 1ms
        return f"{seconds*1000000:.2f}µs"
    elif seconds < 1:  # < 1s
        return f"{seconds*1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"

def format_number(n):
    """Format large numbers with commas for better readability."""
    return f"{int(n):,}"

def create_markdown(results_files):
    """Create markdown from benchmark results."""
    markdown = ["# TextRush Benchmark Results\n"]
    markdown.append("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
    # Load all results
    versions_data = {}
    for version, filepath in results_files.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            versions_data[version] = json.load(f)
    
    # Keyword Addition Performance
    markdown.append("## 1. Keyword Addition Performance\n")
    markdown.append("| Keywords Count | " + " | ".join(f"v{v}" for v in versions_data.keys()) + " |")
    markdown.append("|" + "-|"*(len(versions_data)+1))
    
    for count in ['100', '1000', '10000', '100000', '1000000']:
        row = [format_number(count)]
        for version in versions_data.keys():
            if count in versions_data[version]['results']['keyword_addition']:
                time = versions_data[version]['results']['keyword_addition'][count]
                row.append(format_time(time))
            else:
                row.append("N/A")
        markdown.append("| " + " | ".join(row) + " |")
    
    # ASCII Extraction Performance
    markdown.append("\n## 2. ASCII Extraction Performance\n")
    markdown.append("| Text Length | Keywords | " + " | ".join(f"v{v}" for v in versions_data.keys()) + " |")
    markdown.append("|" + "-|"*(len(versions_data)+2))
    
    for length in ['1000', '10000', '100000', '1000000']:
        for count in ['1000', '10000', '100000']:
            row = [format_number(length), format_number(count)]
            for version in versions_data.keys():
                if (length in versions_data[version]['results']['ascii_extraction'] and 
                    count in versions_data[version]['results']['ascii_extraction'][length]):
                    time = versions_data[version]['results']['ascii_extraction'][length][count]
                    row.append(format_time(time))
                else:
                    row.append("N/A")
            markdown.append("| " + " | ".join(row) + " |")
    
    # Unicode Performance
    markdown.append("\n## 3. Unicode Text Performance\n")
    markdown.append("| Text Length | " + " | ".join(f"v{v}" for v in versions_data.keys()) + " |")
    markdown.append("|" + "-|"*(len(versions_data)+1))
    
    for length in ['1000', '10000', '100000']:
        row = [format_number(length)]
        for version in versions_data.keys():
            if length in versions_data[version]['results']['unicode_extraction']:
                time = versions_data[version]['results']['unicode_extraction'][length]
                row.append(format_time(time))
            else:
                row.append("N/A")
        markdown.append("| " + " | ".join(row) + " |")
    
    # Case Sensitivity
    markdown.append("\n## 4. Case Sensitivity Impact\n")
    markdown.append("| Mode | " + " | ".join(f"v{v}" for v in versions_data.keys()) + " |")
    markdown.append("|" + "-|"*(len(versions_data)+1))
    
    for mode in ['sensitive', 'insensitive']:
        row = [mode]
        for version in versions_data.keys():
            time = versions_data[version]['results']['case_sensitivity'][mode]
            row.append(format_time(time))
        markdown.append("| " + " | ".join(row) + " |")
    
    # Span Information
    markdown.append("\n## 5. Span Information Overhead\n")
    markdown.append("| Mode | " + " | ".join(f"v{v}" for v in versions_data.keys()) + " |")
    markdown.append("|" + "-|"*(len(versions_data)+1))
    
    for mode in ['without_span', 'with_span']:
        row = [mode.replace('_', ' ')]
        for version in versions_data.keys():
            time = versions_data[version]['results']['span_info'][mode]
            row.append(format_time(time))
        markdown.append("| " + " | ".join(row) + " |")
    
    return "\n".join(markdown)

def main():
    # Find latest results for each version
    latest_results = find_latest_results()
    
    if not latest_results:
        print("No benchmark results found!")
        return
    
    # Create markdown
    markdown = create_markdown(latest_results)
    
    # Save markdown
    output_path = Path('tests/benchmark_results/benchmark_results.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"Markdown report generated: {output_path}")

if __name__ == "__main__":
    main()
