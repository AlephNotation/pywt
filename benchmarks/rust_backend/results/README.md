# Published Rust DWT backend results

These are end-to-end timings of normal PyWavelets calls from two isolated
Python environments. `vanilla` is upstream commit `bbdf7eb`; `rust` is branch
commit `170ea7c` using the public `wavelets 0.1.0-alpha.11` crate with its
default direct-FIR kernels. The experimental lattice and annihilator kernels
were not enabled. Lower times and higher speedups are better.

| Host                   | Precision | Forward geometric mean | Inverse geometric mean | Overall geometric mean |       Range |
| ---------------------- | --------: | ---------------------: | ---------------------: | ---------------------: | ----------: |
| AWS c6a.large, AVX2    |   float32 |                  6.02x |                  2.51x |              **3.89x** |  2.20–7.25x |
| AWS c6a.large, AVX2    |   float64 |                  3.46x |                  2.86x |              **3.15x** |  2.33–4.00x |
| AWS c7i.large, AVX-512 |   float32 |                  6.00x |                  2.85x |              **4.14x** | 2.39–10.44x |
| AWS c7i.large, AVX-512 |   float64 |                  3.84x |                  3.14x |              **3.47x** |  2.72–4.70x |

The benchmark covers `dwt`, `idwt`, `dwt2`, `idwt2`, `wavedec2`, `waverec2`,
`dwtn`, and `idwtn`, including first- and last-axis 1D operations. Each cell is
the median of six fresh-process medians; each process visits 64 independently
allocated inputs. Implementation order alternates by round, execution is pinned
to one logical CPU, and numerical-library thread counts are fixed at one.

- [AVX2 tables](aws-c6a-large-avx2-2026-09-02/summary.md), [raw rows](aws-c6a-large-avx2-2026-09-02/raw.csv), and [metadata](aws-c6a-large-avx2-2026-09-02/metadata.json)
- [AVX-512 tables](aws-c7i-large-avx512-2026-09-02/summary.md), [raw rows](aws-c7i-large-avx512-2026-09-02/raw.csv), and [metadata](aws-c7i-large-avx512-2026-09-02/metadata.json)
- [Matched x86-64 wheel sizes](wheel-sizes-x86_64-alpha11.csv)

The Rust-backed wheel is 4,779,388 bytes versus 4,457,489 bytes for vanilla:
a 321,899-byte (7.22%) compressed download increase. The installed `_dwt`
extension is 1,332,896 bytes versus 521,720 bytes. Both wheels were built on
the same host from the commits above.
