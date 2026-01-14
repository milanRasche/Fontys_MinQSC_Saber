import os

from algos_matrix_generation import generate_matrix_A

from algos_secret_sampling import sample_secret_vector

from params_all import (
    Q,
    SEED_BYTES
)

from algos_polynomial_math import (
    matrix_vector_mul,
    poly_add,
    poly_mod,
    poly_mul
)

from algos_encoding import (
    encode_message
)

def encrypy(pk, message: bytes):
    seedA = pk["seedA"]
    b = pk["b"]

    A = generate_matrix_A(seedA)

    seed_sp = os.urandom(SEED_BYTES) #Not True Random but close enough for testing purposes
    sp = sample_secret_vector(seed_sp)

    bp = matrix_vector_mul(A, sp)

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