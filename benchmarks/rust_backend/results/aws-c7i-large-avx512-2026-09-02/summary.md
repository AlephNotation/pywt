## float32

| Operation        |    vanilla |      rust |   rust call IQR | Speedup |  Speedup IQR |
| ---------------- | ---------: | --------: | --------------: | ------: | -----------: |
| `dwt_axis0`      |   2.758 ms |  0.403 ms |  0.388–0.418 ms |   6.85x |   6.84–6.98x |
| `dwt_last_axis`  |   2.507 ms |  0.510 ms |  0.485–0.526 ms |   4.94x |   4.88–4.98x |
| `idwt_axis0`     |   0.698 ms |  0.269 ms |  0.254–0.281 ms |   2.59x |   2.57–2.67x |
| `idwt_last_axis` |   0.436 ms |  0.179 ms |  0.175–0.193 ms |   2.43x |   2.40–2.56x |
| `dwt2`           |   5.878 ms |  1.106 ms |  1.034–1.148 ms |   5.32x |   5.21–5.47x |
| `idwt2`          |   1.299 ms |  0.490 ms |  0.467–0.534 ms |   2.65x |   2.50–2.66x |
| `wavedec2`       |  12.252 ms |  2.963 ms |  2.833–3.039 ms |   4.14x |   4.12–4.22x |
| `waverec2`       |   4.087 ms |  1.711 ms |  1.632–1.779 ms |   2.39x |   2.31–2.46x |
| `dwtn`           | 106.433 ms | 10.203 ms | 9.968–10.511 ms |  10.44x | 10.36–10.52x |
| `idwtn`          |  28.637 ms |  6.088 ms |  5.904–6.232 ms |   4.74x |   4.67–4.83x |

- Forward geometric mean: 6.00x
- Inverse geometric mean: 2.85x
- Overall geometric mean: 4.14x

## float64

| Operation        |    vanilla |      rust |    rust call IQR | Speedup | Speedup IQR |
| ---------------- | ---------: | --------: | ---------------: | ------: | ----------: |
| `dwt_axis0`      |   3.206 ms |  0.829 ms |   0.785–0.851 ms |   3.87x |  3.84–3.91x |
| `dwt_last_axis`  |   2.898 ms |  0.854 ms |   0.816–0.879 ms |   3.39x |  3.29–3.47x |
| `idwt_axis0`     |   1.425 ms |  0.479 ms |   0.460–0.496 ms |   2.97x |  2.89–3.02x |
| `idwt_last_axis` |   0.942 ms |  0.272 ms |   0.257–0.291 ms |   3.46x |  3.34–3.77x |
| `dwt2`           |   6.727 ms |  1.766 ms |   1.690–1.842 ms |   3.81x |  3.77–3.83x |
| `idwt2`          |   2.472 ms |  0.786 ms |   0.743–0.831 ms |   3.16x |  2.97–3.25x |
| `wavedec2`       |  15.201 ms |  4.315 ms |   4.146–4.437 ms |   3.54x |  3.51–3.56x |
| `waverec2`       |   8.010 ms |  2.960 ms |   2.824–3.131 ms |   2.72x |  2.63–2.78x |
| `dwtn`           | 128.760 ms | 27.455 ms | 26.920–27.894 ms |   4.70x |  4.64–4.72x |
| `idwtn`          |  54.267 ms | 15.762 ms | 15.438–16.098 ms |   3.45x |  3.41–3.51x |

- Forward geometric mean: 3.84x
- Inverse geometric mean: 3.14x
- Overall geometric mean: 3.47x
