## float32

| Operation        |    vanilla |      rust |    rust call IQR | Speedup |  Speedup IQR |
| ---------------- | ---------: | --------: | ---------------: | ------: | -----------: |
| `dwt_axis0`      |   2.825 ms |  0.455 ms |   0.443–0.470 ms |   6.38x |   6.29–6.53x |
| `dwt_last_axis`  |   2.588 ms |  0.528 ms |   0.507–0.548 ms |   4.83x |   4.70–5.00x |
| `idwt_axis0`     |   0.725 ms |  0.297 ms |   0.287–0.308 ms |   2.46x |   2.39–2.56x |
| `idwt_last_axis` |   0.469 ms |  0.193 ms |   0.180–0.203 ms |   2.46x |   2.38–2.88x |
| `dwt2`           |   5.858 ms |  1.180 ms |   1.122–1.231 ms |   4.94x |   4.86–4.99x |
| `idwt2`          |   1.304 ms |  0.602 ms |   0.577–0.622 ms |   2.19x |   2.14–2.34x |
| `wavedec2`       |  12.130 ms |  3.013 ms |   2.907–3.117 ms |   4.05x |   4.04–4.09x |
| `waverec2`       |   4.140 ms |  1.736 ms |   1.638–1.817 ms |   2.38x |   2.32–2.45x |
| `dwtn`           | 111.541 ms | 10.576 ms | 10.335–10.951 ms |  10.29x | 10.22–10.58x |
| `idwtn`          |  29.115 ms |  6.543 ms |   6.242–6.694 ms |   4.61x |   4.48–4.70x |

- Forward geometric mean: 5.76x
- Inverse geometric mean: 2.71x
- Overall geometric mean: 3.95x

## float64

| Operation        |    vanilla |      rust |    rust call IQR | Speedup | Speedup IQR |
| ---------------- | ---------: | --------: | ---------------: | ------: | ----------: |
| `dwt_axis0`      |   3.330 ms |  0.885 ms |   0.866–0.903 ms |   3.76x |  3.75–3.92x |
| `dwt_last_axis`  |   2.975 ms |  0.901 ms |   0.867–0.929 ms |   3.33x |  3.16–3.41x |
| `idwt_axis0`     |   1.473 ms |  0.518 ms |   0.501–0.533 ms |   2.84x |  2.83–2.95x |
| `idwt_last_axis` |   0.994 ms |  0.296 ms |   0.284–0.317 ms |   3.36x |  3.30–3.52x |
| `dwt2`           |   6.880 ms |  1.866 ms |   1.825–1.919 ms |   3.66x |  3.62–3.73x |
| `idwt2`          |   2.514 ms |  0.898 ms |   0.864–0.927 ms |   2.79x |  2.74–2.82x |
| `wavedec2`       |  15.515 ms |  4.229 ms |   4.111–4.381 ms |   3.67x |  3.62–3.68x |
| `waverec2`       |   8.101 ms |  3.100 ms |   2.983–3.271 ms |   2.61x |  2.57–2.67x |
| `dwtn`           | 133.128 ms | 29.068 ms | 28.565–29.628 ms |   4.60x |  4.45–4.63x |
| `idwtn`          |  56.889 ms | 18.374 ms | 17.551–19.316 ms |   3.11x |  2.94–3.22x |

- Forward geometric mean: 3.78x
- Inverse geometric mean: 2.93x
- Overall geometric mean: 3.33x
