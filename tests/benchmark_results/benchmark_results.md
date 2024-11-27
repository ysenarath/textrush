# TextRush Benchmark Results

Generated on: 2024-11-26 22:25:28

## 1. Keyword Addition Performance

| Keywords Count | v0.0.2 | vlatest | vflashtext2 | v0.0.3pre1 | vflashtext |
|-|-|-|-|-|-|
| 100 | 84.88µs | 128.03µs | 89.17µs | 148.77µs | 12.07ms |
| 1,000 | 427.01µs | 914.34µs | 672.10µs | 1.36ms | 7.55ms |
| 10,000 | 4.18ms | 9.26ms | 6.38ms | 10.18ms | 9.84ms |
| 100,000 | 41.22ms | 91.77ms | 63.65ms | 104.34ms | 165.39ms |
| 1,000,000 | 407.73ms | 1.26s | 946.59ms | 1.28s | 3.06s |

## 2. ASCII Extraction Performance

| Text Length | Keywords | v0.0.2 | vlatest | vflashtext2 | v0.0.3pre1 | vflashtext |
|-|-|-|-|-|-|-|
| 1,000 | 1,000 | 485.90µs | 61.04µs | 49.83µs | 65.09µs | 106.10µs |
| 1,000 | 10,000 | 4.75ms | 46.97µs | 37.19µs | 38.86µs | 115.39µs |
| 1,000 | 100,000 | 42.31ms | 54.12µs | 42.20µs | 53.88µs | 101.09µs |
| 10,000 | 1,000 | 645.88µs | 258.92µs | 341.89µs | 257.02µs | 818.01µs |
| 10,000 | 10,000 | 4.50ms | 284.19µs | 296.12µs | 255.11µs | 877.14µs |
| 10,000 | 100,000 | 42.65ms | 298.98µs | 336.17µs | 318.05µs | 899.08µs |
| 100,000 | 1,000 | 2.61ms | 2.58ms | 3.01ms | 2.57ms | 8.40ms |
| 100,000 | 10,000 | 6.26ms | 2.62ms | 3.17ms | 2.84ms | 5.74ms |
| 100,000 | 100,000 | 47.60ms | 2.86ms | 3.37ms | 2.84ms | 6.04ms |
| 1,000,000 | 1,000 | 21.49ms | 26.36ms | 30.91ms | 26.80ms | 56.31ms |
| 1,000,000 | 10,000 | 26.82ms | 26.72ms | 30.38ms | 27.26ms | 57.31ms |
| 1,000,000 | 100,000 | 67.38ms | 27.29ms | 30.77ms | 27.35ms | 60.44ms |

## 3. Unicode Text Performance

| Text Length | v0.0.2 | vlatest | vflashtext2 | v0.0.3pre1 | vflashtext |
|-|-|-|-|-|-|
| 1,000 | 5.45ms | 40.77µs | 41.01µs | 41.96µs | 236.99µs |
| 10,000 | 5.26ms | 342.13µs | 442.98µs | 338.79µs | 1.92ms |
| 100,000 | 8.39ms | 3.47ms | 3.70ms | 3.61ms | 19.48ms |

## 4. Case Sensitivity Impact

| Mode | v0.0.2 | vlatest | vflashtext2 | v0.0.3pre1 | vflashtext |
|-|-|-|-|-|-|
| sensitive | 3.56ms | 1.60ms | 1.84ms | 1.55ms | 5.79ms |
| insensitive | 6.09ms | 2.58ms | 2.94ms | 2.79ms | 5.78ms |

## 5. Span Information Overhead

| Mode | v0.0.2 | vlatest | vflashtext2 | v0.0.3pre1 | vflashtext |
|-|-|-|-|-|-|
| without span | 6.16ms | 2.60ms | 3.03ms | 2.68ms | 5.74ms |
| with span | 6.10ms | 2.66ms | 3.42ms | 2.57ms | 5.68ms |