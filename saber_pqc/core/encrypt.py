import os
import hashlib

from core.algos_matrix_generation import generate_matrix_A
from core.algos_secret_sampling import sample_secret_vector
from core.params_all import (
    Q, N, L, EP, ET,
    compute_rounding_constant_p,
    compute_compression_shift_p,
    compute_compression_constant_t,
    compute_compression_shift_t
)
from core.algos_polynomial_math import (
    matrix_vector_mul, poly_add, poly_mod, poly_mul
)
from core.algos_compressiong_decompression import (
    poly_add_const_compression, compress_poly, decompress_poly
)
from core.algos_packing_serialization import pack_poly
from core.algos_packing_serialization import unpack_poly


def deserialize_pk(pk_bytes):
    seedA = pk_bytes[:32]
    off = 32
    b = []
    for _ in range(L):
        poly, used = unpack_poly(pk_bytes[off:], EP, N)
        b.append(poly)
        off += used
    return seedA, b


def kem_encapsulate(pk_bytes):
    # ---- random message m ----
    m = os.urandom(32)

    # ---- hash pk ----
    hpk = hashlib.sha3_256(pk_bytes).digest()

    # ---- derive randomness deterministically ----
    buf = hashlib.sha3_512(m + hpk).digest()
    seed_sp = buf[:32]
    kr = buf[32:64]

    # ---- deserialize pk ----
    seedA, b = deserialize_pk(pk_bytes)
    A = generate_matrix_A(seedA, L)

    sp = sample_secret_vector(seed_sp, L)

    # ---------- compute u ----------
    h1 = compute_rounding_constant_p()
    SHIFT_P = compute_compression_shift_p()

    u_full = matrix_vector_mul(A, sp, L)
    u_full = [poly_mod(p, Q) for p in u_full]
    u_full = [poly_add_const_compression(p, h1) for p in u_full]
    u = [compress_poly(p, SHIFT_P) for p in u_full]

    # ---------- compute v ----------
    b_full = [decompress_poly(p, SHIFT_P) for p in b]

    acc = [0] * N
    for i in range(L):
        acc = poly_add(acc, poly_mul(b_full[i], sp[i]))

    acc = poly_mod(acc, Q)

    m_poly = encode_message(m)

    h2 = compute_compression_constant_t(ET)
    SHIFT_T = compute_compression_shift_t(ET)

    acc = poly_add(acc, m_poly)
    acc = poly_add_const_compression(acc, h2)
    v = compress_poly(acc, SHIFT_T)

    # ---------- serialize ciphertext ----------
    ct = bytearray()
    for poly in u:
        ct += pack_poly(poly, EP)
    ct += pack_poly(v, ET)
    ct = bytes(ct)

    # ---------- derive shared secret ----------
    ss = hashlib.sha3_256(kr + ct).digest()

    return ct, ss
