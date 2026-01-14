import hashlib

from typing import List

from core.params_all import (
    Q,
    N
)

def generate_matrix_A(seedA: bytes, L) -> List[List[List[int]]]:
    #Generates the matrix A needed for pke keypair generation. Deterministic from seedA
    shake = hashlib.shake_128(seedA)

    A = [] #matrix to be
    for i in range(L):
        row = []
        for j in range(L):
            poly = generate_uniform_poly(shake)
            row.append(poly)
        A.append(row)
    return A

def generate_uniform_poly(shake) -> List[int]:
    #Generate Polynomial with Coefficients in [0, Q)
    numb_bytes = 2 * N
    raw = shake.digest(numb_bytes)

    poly = []
    index = 0
    for _ in range(N):
        val = raw[index] | (raw[index + 1] << 8)
        index += 2
        poly.append(val % Q)

    return poly