import numpy as np
import pytest
from numpy.testing import assert_allclose

import pywt
from pywt._extensions import _dwt

DTYPES = (np.float32, np.float64)
WAVELETS = ("haar", "db38", "coif17", "bior4.4")


def _tolerances(dtype):
    if dtype == np.float32:
        return {"rtol": 1e-5, "atol": 2e-5}
    return {"rtol": 1e-12, "atol": 5e-13}


def _c_dwt_axis(data, wavelet, mode, axis):
    """Apply the incumbent C single-signal DWT along one tensor axis."""
    moved = np.moveaxis(data, axis, -1)
    rows = moved.reshape((-1, moved.shape[-1]))
    coefficients = [
        _dwt.dwt_single(np.ascontiguousarray(row), wavelet, mode) for row in rows
    ]
    output_shape = moved.shape[:-1] + (coefficients[0][0].size,)

    def assemble(band):
        values = np.stack([coefficient[band] for coefficient in coefficients])
        return np.moveaxis(values.reshape(output_shape), -1, axis)

    return assemble(0), assemble(1)


def _c_idwt_axis(approx, detail, wavelet, mode, axis):
    """Apply the incumbent C single-signal IDWT along one tensor axis."""
    approx_moved = np.moveaxis(approx, axis, -1)
    detail_moved = np.moveaxis(detail, axis, -1)
    approx_rows = approx_moved.reshape((-1, approx_moved.shape[-1]))
    detail_rows = detail_moved.reshape((-1, detail_moved.shape[-1]))
    rows = [
        _dwt.idwt_single(
            np.ascontiguousarray(approx_row),
            np.ascontiguousarray(detail_row),
            wavelet,
            mode,
        )
        for approx_row, detail_row in zip(approx_rows, detail_rows)
    ]
    output_shape = approx_moved.shape[:-1] + (rows[0].size,)
    return np.moveaxis(np.stack(rows).reshape(output_shape), -1, axis)


def _assert_matches_c(data, wavelet, mode_name, axis):
    mode = pywt.Modes.from_object(mode_name)
    actual_approx, actual_detail = _dwt.dwt_axis(data, wavelet, mode, axis)
    expected_approx, expected_detail = _c_dwt_axis(data, wavelet, mode, axis)
    tolerances = _tolerances(data.dtype.type)
    assert_allclose(actual_approx, expected_approx, **tolerances)
    assert_allclose(actual_detail, expected_detail, **tolerances)

    actual = _dwt.idwt_axis(
        np.ascontiguousarray(actual_approx),
        np.ascontiguousarray(actual_detail),
        wavelet,
        mode,
        axis,
    )
    expected = _c_idwt_axis(actual_approx, actual_detail, wavelet, mode, axis)
    assert_allclose(actual, expected, **tolerances)


@pytest.mark.parametrize("dtype", DTYPES)
@pytest.mark.parametrize("wavelet_name", WAVELETS)
@pytest.mark.parametrize("mode", pywt.Modes.modes)
def test_axis_backend_matches_c_modes(dtype, wavelet_name, mode):
    data = np.random.default_rng(0).standard_normal((3, 17, 4)).astype(dtype)
    _assert_matches_c(data, pywt.Wavelet(wavelet_name), mode, 1)


@pytest.mark.parametrize("dtype", DTYPES)
@pytest.mark.parametrize("length", (2, 3, 8, 64, 65))
def test_axis_backend_matches_c_short_odd_and_even_lengths(dtype, length):
    data = np.random.default_rng(length).standard_normal((3, length, 4))
    _assert_matches_c(data.astype(dtype), pywt.Wavelet("db38"), "symmetric", 1)


@pytest.mark.parametrize("dtype", DTYPES)
@pytest.mark.parametrize("axis", (0, 1, 2))
@pytest.mark.parametrize("layout", ("c", "fortran", "sliced"))
def test_axis_backend_matches_c_axes_and_layouts(dtype, axis, layout):
    data = np.random.default_rng(axis).standard_normal((3, 17, 4)).astype(dtype)
    if layout == "fortran":
        data = np.asfortranarray(data)
    elif layout == "sliced":
        storage = np.empty((6, 34, 8), dtype=dtype)
        storage[::2, ::2, ::2] = data
        data = storage[::2, ::2, ::2]
    _assert_matches_c(data, pywt.Wavelet("db38"), "symmetric", axis)


@pytest.mark.parametrize("dtype", DTYPES)
def test_axis_backend_matches_c_custom_filter_bank(dtype):
    source = pywt.Wavelet("bior4.4")
    wavelet = pywt.Wavelet("custom", source.filter_bank)
    data = np.random.default_rng(1).standard_normal((3, 19, 4)).astype(dtype)
    _assert_matches_c(data, wavelet, "antireflect", 1)


@pytest.mark.parametrize("missing", ("approx", "detail"))
def test_axis_backend_accepts_one_missing_coefficient_band(missing):
    data = np.random.default_rng(2).standard_normal((5, 17))
    approx, detail = pywt.dwt(data, "db4", mode="periodization", axis=1)
    if missing == "approx":
        actual = pywt.idwt(None, detail, "db4", mode="periodization", axis=1)
        approx = np.zeros_like(detail)
    else:
        actual = pywt.idwt(approx, None, "db4", mode="periodization", axis=1)
        detail = np.zeros_like(approx)
    expected = _c_idwt_axis(
        approx,
        detail,
        pywt.Wavelet("db4"),
        pywt.Modes.from_object("periodization"),
        1,
    )
    assert_allclose(actual, expected, rtol=1e-12, atol=5e-13)
