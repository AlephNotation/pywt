## float32

| Operation | vanilla | rust | rust call IQR | Speedup | Speedup IQR |
|---|---:|---:|---:|---:|---:|
| `dwt_axis0` | 4.149 ms | 0.614 ms | 0.606–0.622 ms | 6.76x | 6.71–6.78x |
| `dwt_last_axis` | 3.863 ms | 0.680 ms | 0.672–0.688 ms | 5.69x | 5.68–5.71x |
| `idwt_axis0` | 0.751 ms | 0.363 ms | 0.355–0.373 ms | 2.07x | 2.07–2.08x |
| `idwt_last_axis` | 0.530 ms | 0.217 ms | 0.215–0.228 ms | 2.41x | 2.40–2.45x |
| `dwt2` | 9.037 ms | 1.466 ms | 1.456–1.479 ms | 6.16x | 6.15–6.19x |
| `idwt2` | 1.448 ms | 0.698 ms | 0.690–0.702 ms | 2.07x | 2.07–2.08x |
| `wavedec2` | 17.234 ms | 3.553 ms | 3.528–3.587 ms | 4.85x | 4.78–4.87x |
| `waverec2` | 4.495 ms | 1.942 ms | 1.935–1.956 ms | 2.31x | 2.31–2.32x |
| `dwtn` | 167.682 ms | 22.408 ms | 21.090–23.342 ms | 7.48x | 7.30–7.55x |
| `idwtn` | 40.501 ms | 12.717 ms | 12.572–12.969 ms | 3.17x | 3.16–3.21x |

- Forward geometric mean: 6.12x
- Inverse geometric mean: 2.38x
- Overall geometric mean: 3.82x

## float64

| Operation | vanilla | rust | rust call IQR | Speedup | Speedup IQR |
|---|---:|---:|---:|---:|---:|
| `dwt_axis0` | 4.618 ms | 1.135 ms | 1.124–1.182 ms | 4.07x | 4.03–4.08x |
| `dwt_last_axis` | 4.186 ms | 1.180 ms | 1.171–1.193 ms | 3.54x | 3.54–3.56x |
| `idwt_axis0` | 1.423 ms | 0.640 ms | 0.631–0.649 ms | 2.22x | 2.20–2.23x |
| `idwt_last_axis` | 1.062 ms | 0.344 ms | 0.341–0.355 ms | 3.10x | 3.07–3.10x |
| `dwt2` | 9.786 ms | 2.630 ms | 2.606–2.653 ms | 3.72x | 3.71–3.73x |
| `idwt2` | 2.807 ms | 1.140 ms | 1.134–1.150 ms | 2.46x | 2.44–2.49x |
| `wavedec2` | 22.026 ms | 6.345 ms | 6.126–6.418 ms | 3.47x | 3.45–3.49x |
| `waverec2` | 8.777 ms | 3.514 ms | 3.499–3.531 ms | 2.50x | 2.49–2.51x |
| `dwtn` | 238.297 ms | 72.739 ms | 71.678–73.883 ms | 3.28x | 3.23–3.42x |
| `idwtn` | 99.571 ms | 26.887 ms | 26.562–27.311 ms | 3.67x | 3.48–3.79x |

- Forward geometric mean: 3.61x
- Inverse geometric mean: 2.74x
- Overall geometric mean: 3.15x
