# Rust DWT backend comparison

This harness compares the public PyWavelets API from isolated vanilla and
Rust-backed installations. It does not compare Rust calls with Python loops.
Every timed operation is a normal `pywt.dwt`, `pywt.idwt`, `pywt.dwt2`,
`pywt.idwt2`, `pywt.wavedec2`, `pywt.waverec2`, `pywt.dwtn`, or `pywt.idwtn`
call.

## Method

The matrix covers ten forward and inverse operations in both `float32` and
`float64`:

- `dwt` and `idwt`, axis 0 and the last axis: db38, 256 × 256
- `dwt2` and `idwt2`: db38, 256 × 256
- `wavedec2` and `waverec2`: db20, level 2, 512 × 512
- `dwtn` and `idwtn`: db38, axes 0 and 1, 256 × 256 × 16

Each fresh process allocates 64 deterministic random inputs and retains every
output. This samples allocator and page layouts instead of repeatedly timing a
single favorable address. One untimed operation warms the code path. The
runner rotates implementation order between six process rounds, pins execution
to one logical CPU when requested, and fixes common numerical-library thread
counts at one.

The summary reports:

- the median of the six process medians for each implementation;
- the median per-process call IQR for the Rust backend;
- the median and IQR of the six paired vanilla/Rust speedup ratios;
- geometric means split by direction and dtype.

## Reproduce

Create two environments with the same Python and NumPy versions. Install the
chosen upstream commit in one and this branch in the other. For example:

```bash
python -m venv /tmp/pywt-vanilla
python -m venv /tmp/pywt-rust
/tmp/pywt-vanilla/bin/pip install /path/to/upstream-pywt
/tmp/pywt-rust/bin/pip install /path/to/this-branch \
  -Csetup-args=-Duse-rust=true
```

Run the balanced comparison on Linux:

```bash
python benchmarks/rust_backend/run.py \
  --python vanilla=/tmp/pywt-vanilla/bin/python \
  --python rust=/tmp/pywt-rust/bin/python \
  --cpu 2 \
  --output raw.csv

python benchmarks/rust_backend/summarize.py raw.csv \
  --csv summary.csv \
  --markdown summary.md
```

Run AVX2 measurements on an AVX2-only host so runtime dispatch selects the
same production code path that users of that machine receive.

To record distribution-size impact, build matched wheels and run:

```bash
python benchmarks/rust_backend/wheel_size.py \
  vanilla=/path/to/vanilla.whl rust=/path/to/rust.whl \
  --output wheel-sizes.csv
```

`wheel_bytes` is the compressed artifact users download.
`dwt_uncompressed_bytes` is the installed extension size. Both are reported so
that one cannot be mistaken for the other.

Published runs live under [`results`](results). Each result directory contains
the raw process rows, the machine-readable summary, the rendered table, machine
metadata, and matched wheel sizes.
