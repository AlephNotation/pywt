#pragma once

#include <stddef.h>

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
