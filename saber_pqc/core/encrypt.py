import os
import hashlib

from core.algos_matrix_generation import generate_matrix_A
from core.algos_secret_sampling import sample_secret_vector
from core.params_all import (
    Q,
    N,
    SEED_BYTES,
    compute_rounding_constant_p,
    compute_compression_shift_p,
    compute_compression_constant_t,
    compute_compression_shift_t
)
from core.algos_polynomial_math import (
    matrix_vector_mul,
    poly_add,
    poly_mod,
    poly_mul
)
from core.algos_compressiong_decompression import (
    poly_add_const_compression, compress_poly, decompress_poly
)

def encrypt(pk, message: bytes, L, ET):
    """
    Encrypt AES key using SABER PKE + shared secret derived from v
    """
    seedA = pk["seedA"]
    b = pk["b"]  # compressed

    A = generate_matrix_A(seedA, L)
    seed_sp = os.urandom(SEED_BYTES)
    sp = sample_secret_vector(seed_sp, L)

    # ---------- compute u = (A * sp + h1) >> (EQ - EP) ----------
    h1 = compute_rounding_constant_p()
    SHIFT_P = compute_compression_shift_p()

    u_full = matrix_vector_mul(A, sp, L)
    u_full = [poly_mod(p, Q) for p in u_full]
    u_full = [poly_add_const_compression(p, h1) for p in u_full]
    u = [compress_poly(p, SHIFT_P) for p in u_full]

    # ---------- compute v = (b * sp + h2) >> (EQ - ET) ----------
    b_full = [decompress_poly(p, SHIFT_P) for p in b]

    acc = [0] * N
    for i in range(L):
        prod = poly_mul(b_full[i], sp[i])
        acc = poly_add(acc, prod)
    acc = poly_mod(acc, Q)

    h2 = compute_compression_constant_t(ET)
    SHIFT_T = compute_compression_shift_t(ET)
    acc = poly_add_const_compression(acc, h2)
    v = compress_poly(acc, SHIFT_T)

    # ---------- derive shared secret from v for AES key ----------
    v_bytes = b"".join(int.to_bytes(c, 2, "little") for c in v)
    shared_secret = hashlib.shake_128(v_bytes).digest(len(message))
    encrypted_key = bytes([a ^ b for a, b in zip(message, shared_secret)])

    return {
        "u": u,
        "v": v,
        "encrypted_key": encrypted_key
    }
