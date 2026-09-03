# Published Rust DWT backend results

These are end-to-end timings of normal PyWavelets calls from two isolated
Python environments. `vanilla` is upstream commit `bbdf7eb`; `rust` is branch
commit `2aa0340` using wavelets commit `5a192fb`. The exact wavelets revision
was selected with a benchmark-only Cargo patch; the branch's public dependency
remains crates.io `wavelets 0.1.0-alpha.11`. The experimental lattice and
annihilator kernels were not enabled. Lower times and higher speedups are
better.

| Host                   | Precision | Forward geometric mean | Inverse geometric mean | Overall geometric mean |       Range |
| ---------------------- | --------: | ---------------------: | ---------------------: | ---------------------: | ----------: |
| AWS c6a.large, AVX2    |   float32 |                  6.12x |                  2.38x |              **3.82x** |  2.07–7.48x |
| AWS c6a.large, AVX2    |   float64 |                  3.61x |                  2.74x |              **3.15x** |  2.22–4.07x |
| AWS c7i.large, AVX-512 |   float32 |                  5.76x |                  2.71x |              **3.95x** | 2.19–10.29x |
| AWS c7i.large, AVX-512 |   float64 |                  3.78x |                  2.93x |              **3.33x** |  2.61–4.60x |

The benchmark covers `dwt`, `idwt`, `dwt2`, `idwt2`, `wavedec2`, `waverec2`,
`dwtn`, and `idwtn`, including first- and last-axis 1D operations. Each cell is
the median of six fresh-process medians; each process visits 64 independently
allocated inputs. Implementation order alternates by round, execution is pinned
to one logical CPU, and numerical-library thread counts are fixed at one.

- [AVX2 tables](aws-c6a-large-avx2-2026-09-03/summary.md), [raw rows](aws-c6a-large-avx2-2026-09-03/raw.csv), and [metadata](aws-c6a-large-avx2-2026-09-03/metadata.json)
- [AVX-512 tables](aws-c7i-large-avx512-2026-09-03/summary.md), [raw rows](aws-c7i-large-avx512-2026-09-03/raw.csv), and [metadata](aws-c7i-large-avx512-2026-09-03/metadata.json)
- [Matched x86-64 wheel sizes](wheel-sizes-x86_64-alpha11.csv)

The retained alpha.11 size measurement used matched wheels: the Rust-backed
wheel is 4,779,388 bytes versus 4,457,489 bytes for vanilla,
a 321,899-byte (7.22%) compressed download increase. The installed `_dwt`
extension is 1,332,896 bytes versus 521,720 bytes. Both wheels were built on
the same host; the current performance rerun did not repeat the unchanged
distribution-size measurement.
