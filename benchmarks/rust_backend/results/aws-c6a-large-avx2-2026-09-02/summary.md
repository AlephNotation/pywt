## float32

| Operation        |    vanilla |      rust |    rust call IQR | Speedup | Speedup IQR |
| ---------------- | ---------: | --------: | ---------------: | ------: | ----------: |
| `dwt_axis0`      |   4.172 ms |  0.627 ms |   0.611–0.638 ms |   6.66x |  6.64–6.68x |
| `dwt_last_axis`  |   3.901 ms |  0.698 ms |   0.674–0.711 ms |   5.60x |  5.56–5.61x |
| `idwt_axis0`     |   0.766 ms |  0.347 ms |   0.340–0.355 ms |   2.20x |  2.19–2.21x |
| `idwt_last_axis` |   0.526 ms |  0.206 ms |   0.204–0.215 ms |   2.55x |  2.54–2.57x |
| `dwt2`           |   9.085 ms |  1.465 ms |   1.448–1.480 ms |   6.19x |  6.16–6.22x |
| `idwt2`          |   1.450 ms |  0.656 ms |   0.650–0.661 ms |   2.21x |  2.21–2.21x |
| `wavedec2`       |  17.427 ms |  3.684 ms |   3.664–3.719 ms |   4.73x |  4.71–4.74x |
| `waverec2`       |   4.510 ms |  1.962 ms |   1.951–1.978 ms |   2.30x |  2.30–2.30x |
| `dwtn`           | 167.967 ms | 23.116 ms | 21.602–23.654 ms |   7.25x |  7.00–7.40x |
| `idwtn`          |  42.771 ms | 12.171 ms | 12.016–12.409 ms |   3.51x |  3.35–3.53x |

- Forward geometric mean: 6.02x
- Inverse geometric mean: 2.51x
- Overall geometric mean: 3.89x

## float64

| Operation        |    vanilla |      rust |    rust call IQR | Speedup | Speedup IQR |
| ---------------- | ---------: | --------: | ---------------: | ------: | ----------: |
| `dwt_axis0`      |   4.694 ms |  1.262 ms |   1.247–1.274 ms |   3.72x |  3.71–3.74x |
| `dwt_last_axis`  |   4.263 ms |  1.259 ms |   1.245–1.274 ms |   3.40x |  3.39–3.42x |
| `idwt_axis0`     |   1.424 ms |  0.612 ms |   0.605–0.621 ms |   2.33x |  2.32–2.33x |
| `idwt_last_axis` |   1.078 ms |  0.335 ms |   0.331–0.344 ms |   3.21x |  3.19–3.22x |
| `dwt2`           |   9.911 ms |  2.684 ms |   2.660–2.704 ms |   3.69x |  3.69–3.71x |
| `idwt2`          |   2.809 ms |  1.071 ms |   1.064–1.083 ms |   2.63x |  2.62–2.63x |
| `wavedec2`       |  22.117 ms |  6.644 ms |   6.382–6.747 ms |   3.33x |  3.32–3.35x |
| `waverec2`       |   8.737 ms |  3.556 ms |   3.538–3.578 ms |   2.46x |  2.45–2.47x |
| `dwtn`           | 237.360 ms | 74.375 ms | 73.229–75.765 ms |   3.18x |  2.99–3.29x |
| `idwtn`          | 100.574 ms | 25.069 ms | 24.666–25.622 ms |   4.00x |  3.92–4.05x |

- Forward geometric mean: 3.46x
- Inverse geometric mean: 2.86x
- Overall geometric mean: 3.15x
