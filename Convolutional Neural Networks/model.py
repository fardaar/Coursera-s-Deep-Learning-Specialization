import numpy as np
import h5py
import matplotlib.pyplot as plt


def zero_pad(X, pad):
    X_pad = np.pad(X, ((0, 0), (pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=0)
    return X_pad


def conv_single_step(a_slice_prev, W, b):
    s = a_slice_prev * W
    Z = np.sum(s)
    Z = Z + float(b)
    return Z


def conv_forward(A_prev, W, b, hyper_parameters):
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
    (f, f, n_C_prev, n_C) = W.shape
    stride = hyper_parameters['stride']
    pad = hyper_parameters['pad']

    n_H = int(np.floor(((n_H_prev - f) + 2 * pad) / stride)) + 1
    n_W = int(np.floor(((n_W_prev - f) + 2 * pad) / stride)) + 1

    Z = np.zeros((n_H, n_W))

    A_prev_pad = zero_pad(A_prev, pad)

    for i in range(m):
        a_prev_pad = A_prev_pad[i]
        for h in range(n_H):
            vert_start = h
            vert_end = h + n_H

            for w in range(n_W):
                horiz_start = w
                horiz_end = w + n_W

                for c in range(n_C):
                    a_slice_prev = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]
                    weights = W[vert_start:vert_end, horiz_start:horiz_end, c, :]
                    biases = b[vert_start:vert_end, horiz_start:horiz_end, c, :]
                    Z[i, h, w, c] = a_slice_prev * weights + biases

    cache = (A_prev, W, b, hyper_parameters)
    return Z, cache
