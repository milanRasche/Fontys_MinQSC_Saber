import os

from core.algos_matrix_generation import generate_matrix_A

from core.algos_polynomial_math import (matrix_vector_transpose)

from core.algos_secret_sampling import sample_secret_vector

from core.params_all import (
    compute_rounding_constant_p,
    compute_compression_shift_p,
    SEED_BYTES
)

from core.algos_compressiong_decompression import (compress_poly, poly_add_const_compression)


def generate_pke_keypair(L):
    #Generate Uniform Seed
    seedA = os.urandom(SEED_BYTES)

    #Expand from seed A using Shake128 (128 Hashing ALgorithm in SHA-3)
    A = generate_matrix_A(seedA, L)

    #Sample secret vectore from binomial distribution
    seed_s = os.urandom(SEED_BYTES) #Not True Random but close enough for testing purposes
    s = sample_secret_vector(seed_s, L)

    #Compute b= A^T * s + h (mod q)
    h1 = compute_rounding_constant_p()
    b_full = matrix_vector_transpose(A, s, L)

    b_full = [poly_add_const_compression(p, h1) for p in b_full]

    shift_p = compute_compression_shift_p()
    b = [compress_poly(p, shift_p) for p in b_full]

    return seedA, b, s