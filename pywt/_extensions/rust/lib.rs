#![deny(unsafe_op_in_unsafe_fn)]

use std::panic::{AssertUnwindSafe, catch_unwind};
use std::slice;

use wavelets::{Boundary, DwtPlanner, Wavelet, WaveletNum};

const INVALID_ARGUMENT: i32 = 1;
const INVALID_FILTER_BANK: i32 = 2;
const PLAN_FAILED: i32 = 3;
const PANICKED: i32 = 4;

fn boundary(mode: i32) -> Option<Boundary> {
    match mode {
        0 => Some(Boundary::Zero),
        1 => Some(Boundary::Symmetric),
        2 => Some(Boundary::Constant),
        3 => Some(Boundary::Smooth),
        4 => Some(Boundary::Periodic),
        5 => Some(Boundary::Periodization),
        6 => Some(Boundary::Reflect),
        7 => Some(Boundary::Antisymmetric),
        8 => Some(Boundary::Antireflect),
        _ => None,
    }
}

fn buffer_len(outer: usize, axis: usize, inner: usize) -> Option<usize> {
    outer.checked_mul(axis)?.checked_mul(inner)
}

#[allow(clippy::too_many_arguments)]
unsafe fn filters(
    dec_lo: *const f64,
    dec_hi: *const f64,
    rec_lo: *const f64,
    rec_hi: *const f64,
    filter_len: usize,
) -> Result<Wavelet, i32> {
    if [dec_lo, dec_hi, rec_lo, rec_hi]
        .into_iter()
        .any(|filter| filter.is_null())
    {
        return Err(INVALID_ARGUMENT);
    }
    let dec_lo = unsafe { slice::from_raw_parts(dec_lo, filter_len) };
    let dec_hi = unsafe { slice::from_raw_parts(dec_hi, filter_len) };
    let rec_lo = unsafe { slice::from_raw_parts(rec_lo, filter_len) };
    let rec_hi = unsafe { slice::from_raw_parts(rec_hi, filter_len) };
    Wavelet::from_filters(dec_lo, dec_hi, rec_lo, rec_hi).map_err(|_| INVALID_FILTER_BANK)
}

#[allow(clippy::too_many_arguments)]
unsafe fn forward<T: WaveletNum>(
    input: *const T,
    approx: *mut T,
    detail: *mut T,
    signal_len: usize,
    coeff_len: usize,
    outer: usize,
    inner: usize,
    dec_lo: *const f64,
    dec_hi: *const f64,
    rec_lo: *const f64,
    rec_hi: *const f64,
    filter_len: usize,
    mode: i32,
) -> Result<(), i32> {
    if input.is_null() || approx.is_null() || detail.is_null() {
        return Err(INVALID_ARGUMENT);
    }
    let input_len = buffer_len(outer, signal_len, inner).ok_or(INVALID_ARGUMENT)?;
    let output_len = buffer_len(outer, coeff_len, inner).ok_or(INVALID_ARGUMENT)?;
    let wavelet = unsafe { filters(dec_lo, dec_hi, rec_lo, rec_hi, filter_len) }?;
    let mut planner = DwtPlanner::<T>::new();
    let plan = planner
        .plan_dwt(
            signal_len,
            &wavelet,
            boundary(mode).ok_or(INVALID_ARGUMENT)?,
        )
        .map_err(|_| PLAN_FAILED)?;
    if plan.coeff_len() != coeff_len {
        return Err(INVALID_ARGUMENT);
    }

    let input = unsafe { slice::from_raw_parts(input, input_len) };
    let approx = unsafe { slice::from_raw_parts_mut(approx, output_len) };
    let detail = unsafe { slice::from_raw_parts_mut(detail, output_len) };
    let mut scratch = vec![T::zero(); plan.axis_scratch_len(outer, inner)];
    plan.forward_axis_into(input, outer, inner, approx, detail, &mut scratch);
    Ok(())
}

#[allow(clippy::too_many_arguments)]
unsafe fn inverse<T: WaveletNum>(
    approx: *const T,
    detail: *const T,
    output: *mut T,
    signal_len: usize,
    coeff_len: usize,
    outer: usize,
    inner: usize,
    dec_lo: *const f64,
    dec_hi: *const f64,
    rec_lo: *const f64,
    rec_hi: *const f64,
    filter_len: usize,
    mode: i32,
) -> Result<(), i32> {
    if approx.is_null() || detail.is_null() || output.is_null() {
        return Err(INVALID_ARGUMENT);
    }
    let coefficient_count = buffer_len(outer, coeff_len, inner).ok_or(INVALID_ARGUMENT)?;
    let output_len = buffer_len(outer, signal_len, inner).ok_or(INVALID_ARGUMENT)?;
    let wavelet = unsafe { filters(dec_lo, dec_hi, rec_lo, rec_hi, filter_len) }?;
    let mut planner = DwtPlanner::<T>::new();
    let plan = planner
        .plan_dwt(
            signal_len,
            &wavelet,
            boundary(mode).ok_or(INVALID_ARGUMENT)?,
        )
        .map_err(|_| PLAN_FAILED)?;
    if plan.coeff_len() != coeff_len {
        return Err(INVALID_ARGUMENT);
    }

    let approx = unsafe { slice::from_raw_parts(approx, coefficient_count) };
    let detail = unsafe { slice::from_raw_parts(detail, coefficient_count) };
    let output = unsafe { slice::from_raw_parts_mut(output, output_len) };
    let mut scratch = vec![T::zero(); plan.scratch_len()];
    plan.inverse_axis_into(approx, detail, outer, inner, output, &mut scratch);
    Ok(())
}

macro_rules! axis_ffi {
    ($forward:ident, $inverse:ident, $sample:ty) => {
        /// Applies a batched forward transform to C-contiguous tensor buffers.
        ///
        /// # Safety
        ///
        /// Every pointer must reference a valid, suitably aligned buffer of
        /// the length implied by the shape arguments. Input and output buffers
        /// must not overlap.
        #[unsafe(no_mangle)]
        pub unsafe extern "C" fn $forward(
            input: *const $sample,
            approx: *mut $sample,
            detail: *mut $sample,
            signal_len: usize,
            coeff_len: usize,
            outer: usize,
            inner: usize,
            dec_lo: *const f64,
            dec_hi: *const f64,
            rec_lo: *const f64,
            rec_hi: *const f64,
            filter_len: usize,
            mode: i32,
        ) -> i32 {
            catch_unwind(AssertUnwindSafe(|| unsafe {
                forward(
                    input, approx, detail, signal_len, coeff_len, outer, inner, dec_lo, dec_hi,
                    rec_lo, rec_hi, filter_len, mode,
                )
            }))
            .map_or(PANICKED, |result| result.map_or_else(|error| error, |()| 0))
        }

        /// Applies a batched inverse transform to C-contiguous tensor buffers.
        ///
        /// # Safety
        ///
        /// Every pointer must reference a valid, suitably aligned buffer of
        /// the length implied by the shape arguments. Input and output buffers
        /// must not overlap.
        #[unsafe(no_mangle)]
        pub unsafe extern "C" fn $inverse(
            approx: *const $sample,
            detail: *const $sample,
            output: *mut $sample,
            signal_len: usize,
            coeff_len: usize,
            outer: usize,
            inner: usize,
            dec_lo: *const f64,
            dec_hi: *const f64,
            rec_lo: *const f64,
            rec_hi: *const f64,
            filter_len: usize,
            mode: i32,
        ) -> i32 {
            catch_unwind(AssertUnwindSafe(|| unsafe {
                inverse(
                    approx, detail, output, signal_len, coeff_len, outer, inner, dec_lo, dec_hi,
                    rec_lo, rec_hi, filter_len, mode,
                )
            }))
            .map_or(PANICKED, |result| result.map_or_else(|error| error, |()| 0))
        }
    };
}

axis_ffi!(pywt_rs_dwt_axis_f32, pywt_rs_idwt_axis_f32, f32);
axis_ffi!(pywt_rs_dwt_axis_f64, pywt_rs_idwt_axis_f64, f64);
