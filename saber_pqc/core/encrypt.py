import os
from .pke import (
    generate_matrix_A,
    sample_secret_vector,
    matrix_vector_mul,
    poly_add,
    poly_mod,
    poly_mul,
    encode_message,
    SEED_BYTES,
    Q
)

def encrypy(pk, message: bytes):
    seedA = pk["seedA"]
    b = pk["b"]

    A = generate_matrix_A(seedA)

    seed_sp = os.urandom(SEED_BYTES) #Not True Random but close enough for testing purposes
    sp = sample_secret_vector(seed_sp)

    bp = matrix_vector_mul(A, sp)

    print("DEBUG bp length:", len(bp))
    print("DEBUG bp[0] length:", len(bp[0]))

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