#pragma once

#include <stddef.h>

/* The filter bank is outside the Rust backend's supported domain, including
 * coefficients that become non-finite in the execution dtype. No output has
 * been written; the caller may use the incumbent C backend. Other nonzero
 * statuses are errors, not fallback requests.
 */
enum { PYWT_RS_UNSUPPORTED_FILTER_BANK = 2 };

int pywt_rs_dwt_axis_f32(
    const float *input,
    float *approx,
    float *detail,
    size_t signal_len,
    size_t coeff_len,
    size_t outer,
    size_t inner,
    const double *dec_lo,
    const double *dec_hi,
    const double *rec_lo,
    const double *rec_hi,
    size_t filter_len,
    int mode
);

int pywt_rs_dwt_axis_f64(
    const double *input,
    double *approx,
    double *detail,
    size_t signal_len,
    size_t coeff_len,
    size_t outer,
    size_t inner,
    const double *dec_lo,
    const double *dec_hi,
    const double *rec_lo,
    const double *rec_hi,
    size_t filter_len,
    int mode
);

int pywt_rs_idwt_axis_f32(
    const float *approx,
    const float *detail,
    float *output,
    size_t signal_len,
    size_t coeff_len,
    size_t outer,
    size_t inner,
    const double *dec_lo,
    const double *dec_hi,
    const double *rec_lo,
    const double *rec_hi,
    size_t filter_len,
    int mode
);

int pywt_rs_idwt_axis_f64(
    const double *approx,
    const double *detail,
    double *output,
    size_t signal_len,
    size_t coeff_len,
    size_t outer,
    size_t inner,
    const double *dec_lo,
    const double *dec_hi,
    const double *rec_lo,
    const double *rec_hi,
    size_t filter_len,
    int mode
);
