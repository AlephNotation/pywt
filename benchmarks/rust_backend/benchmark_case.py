"""Measure one public PyWavelets operation in a fresh process."""

from __future__ import annotations

import argparse
import gc
import math
import statistics
import time

import numpy as np

import pywt

CASES = (
    "dwt_axis0",
    "dwt_last_axis",
    "idwt_axis0",
    "idwt_last_axis",
    "dwt2",
    "idwt2",
    "wavedec2",
    "waverec2",
    "dwtn",
    "idwtn",
)


def random_arrays(shape, dtype, count, seed):
    rng = np.random.default_rng(seed)
    return [rng.standard_normal(shape).astype(dtype) for _ in range(count)]


def prepare_case(case, dtype, count):
    if case in {"dwt_axis0", "dwt_last_axis"}:
        axis = 0 if case == "dwt_axis0" else -1
        inputs = random_arrays((256, 256), dtype, count, 101)
        return inputs, lambda data: pywt.dwt(data, "db38", mode="symmetric", axis=axis)

    if case in {"idwt_axis0", "idwt_last_axis"}:
        axis = 0 if case == "idwt_axis0" else -1
        inputs = [
            pywt.dwt(data, "db38", mode="symmetric", axis=axis)
            for data in random_arrays((256, 256), dtype, count, 102)
        ]
        return inputs, lambda coefficients: pywt.idwt(
            *coefficients, "db38", mode="symmetric", axis=axis
        )

    if case == "dwt2":
        inputs = random_arrays((256, 256), dtype, count, 201)
        return inputs, lambda data: pywt.dwt2(data, "db38", mode="symmetric")

    if case == "idwt2":
        inputs = [
            pywt.dwt2(data, "db38", mode="symmetric")
            for data in random_arrays((256, 256), dtype, count, 202)
        ]
        return inputs, lambda coefficients: pywt.idwt2(
            coefficients, "db38", mode="symmetric"
        )

    if case == "wavedec2":
        inputs = random_arrays((512, 512), dtype, count, 301)
        return inputs, lambda data: pywt.wavedec2(
            data, "db20", mode="symmetric", level=2
        )

    if case == "waverec2":
        inputs = [
            pywt.wavedec2(data, "db20", mode="symmetric", level=2)
            for data in random_arrays((512, 512), dtype, count, 302)
        ]
        return inputs, lambda coefficients: pywt.waverec2(
            coefficients, "db20", mode="symmetric"
        )

    if case == "dwtn":
        inputs = random_arrays((256, 256, 16), dtype, count, 401)
        return inputs, lambda data: pywt.dwtn(
            data, "db38", mode="symmetric", axes=(0, 1)
        )

    if case == "idwtn":
        inputs = [
            pywt.dwtn(data, "db38", mode="symmetric", axes=(0, 1))
            for data in random_arrays((256, 256, 16), dtype, count, 402)
        ]
        return inputs, lambda coefficients: pywt.idwtn(
            coefficients, "db38", mode="symmetric", axes=(0, 1)
        )

    raise ValueError(f"unknown case: {case}")


def assert_finite(value):
    if isinstance(value, np.ndarray):
        assert np.isfinite(value).all()
    elif isinstance(value, dict):
        for child in value.values():
            assert_finite(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            assert_finite(child)
    else:
        raise TypeError(type(value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("implementation")
    parser.add_argument("round", type=int)
    parser.add_argument("case", choices=CASES)
    parser.add_argument("dtype", choices=("float32", "float64"))
    parser.add_argument("--layouts", type=int, default=64)
    args = parser.parse_args()

    if args.layouts < 4:
        parser.error("--layouts must be at least 4")
    dtype = getattr(np, args.dtype)
    inputs, function = prepare_case(args.case, dtype, args.layouts)
    assert_finite(function(inputs[0]))
    gc.collect()

    outputs = []
    samples = []
    gc.disable()
    try:
        for value in inputs:
            started = time.perf_counter_ns()
            outputs.append(function(value))
            samples.append((time.perf_counter_ns() - started) / 1e6)
    finally:
        gc.enable()

    assert len(outputs) == args.layouts
    assert_finite(outputs[0])
    assert_finite(outputs[-1])
    samples.sort()
    q1 = samples[math.floor((args.layouts - 1) * 0.25)]
    median = statistics.median(samples)
    q3 = samples[math.ceil((args.layouts - 1) * 0.75)]
    print(
        args.implementation,
        args.round,
        args.case,
        args.dtype,
        args.layouts,
        q1,
        median,
        q3,
        sep=",",
    )


if __name__ == "__main__":
    main()
