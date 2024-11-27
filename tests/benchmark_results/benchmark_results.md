# TextRush Benchmark Results

Generated on: 2024-11-26 22:11:18

## 1. Keyword Addition Performance

| Keywords Count | v0.0.2 | vlatest | v0.0.3pre1 |
|-|-|-|-|
| 100 | 84.88µs | 128.03µs | 148.77µs |
| 1,000 | 427.01µs | 914.34µs | 1.36ms |
| 10,000 | 4.18ms | 9.26ms | 10.18ms |
| 100,000 | 41.22ms | 91.77ms | 104.34ms |
| 1,000,000 | 407.73ms | 1.26s | 1.28s |

## 2. ASCII Extraction Performance

| Text Length | Keywords | v0.0.2 | vlatest | v0.0.3pre1 |
|-|-|-|-|-|
| 1,000 | 1,000 | 485.90µs | 61.04µs | 65.09µs |
| 1,000 | 10,000 | 4.75ms | 46.97µs | 38.86µs |
| 1,000 | 100,000 | 42.31ms | 54.12µs | 53.88µs |
| 10,000 | 1,000 | 645.88µs | 258.92µs | 257.02µs |
| 10,000 | 10,000 | 4.50ms | 284.19µs | 255.11µs |
| 10,000 | 100,000 | 42.65ms | 298.98µs | 318.05µs |
| 100,000 | 1,000 | 2.61ms | 2.58ms | 2.57ms |
| 100,000 | 10,000 | 6.26ms | 2.62ms | 2.84ms |
| 100,000 | 100,000 | 47.60ms | 2.86ms | 2.84ms |
| 1,000,000 | 1,000 | 21.49ms | 26.36ms | 26.80ms |
| 1,000,000 | 10,000 | 26.82ms | 26.72ms | 27.26ms |
| 1,000,000 | 100,000 | 67.38ms | 27.29ms | 27.35ms |

## 3. Unicode Text Performance

| Text Length | v0.0.2 | vlatest | v0.0.3pre1 |
|-|-|-|-|
| 1,000 | 5.45ms | 40.77µs | 41.96µs |
| 10,000 | 5.26ms | 342.13µs | 338.79µs |
| 100,000 | 8.39ms | 3.47ms | 3.61ms |

## 4. Case Sensitivity Impact

| Mode | v0.0.2 | vlatest | v0.0.3pre1 |
|-|-|-|-|
| sensitive | 3.56ms | 1.60ms | 1.55ms |
| insensitive | 6.09ms | 2.58ms | 2.79ms |

## 5. Span Information Overhead

| Mode | v0.0.2 | vlatest | v0.0.3pre1 |
|-|-|-|-|
| without span | 6.16ms | 2.60ms | 2.68ms |
| with span | 6.10ms | 2.66ms | 2.57ms |