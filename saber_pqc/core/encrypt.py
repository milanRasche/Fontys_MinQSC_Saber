import os

from core.algos_matrix_generation import generate_matrix_A

from core.algos_secret_sampling import sample_secret_vector

from core.params_all import (
    Q,
    N,
    SEED_BYTES
)

from core.algos_polynomial_math import (
    matrix_vector_mul,
    poly_add,
    poly_mod,
    poly_mul
)

def encrypy(pk, message: bytes, L):
    seedA = pk["seedA"]
    b = pk["b"]

    A = generate_matrix_A(seedA, L)

    seed_sp = os.urandom(SEED_BYTES) #Not True Random but close enough for testing purposes
    sp = sample_secret_vector(seed_sp, L)

    bp = matrix_vector_mul(A, sp, L)

    acc = [0] * len(bp[0])
    for i in range(len(sp)):
        prod = poly_mul(b[i], sp[i])
        acc = poly_add(acc, prod)

    m_poly = encode_message(message)
    vp = poly_add(acc, m_poly)
    vp = poly_mod(vp, Q)

    return {
        "bp": bp,
        "vp": vp
    }

def encode_message(m: bytes):
    bits = []
    for byte in m:
        for i in range(8):
            bits.append((byte >> i) & 1)

    poly = [bit * (Q // 2) for bit in bits[:N]]
    return poly