import os
import hashlib
from typing import List

#Params Saber
N = 256
L = 3
Q = 8192
MU = 10
SEED_BYTES = 32

def generate_pke_keypair():
    #Generate Uniform Seed
    seedA = os.urandom(SEED_BYTES)

    #Expand from seed A using Shake128 (128 Hashing ALgorithm in SHA-3)
    A = generate_matrix_A(seedA)

    #Sample secret vectore from binomial distribution
    seed_s = os.urandom(SEED_BYTES)
    s = sample_secret_vector(seed_s)




def generate_matrix_A(seedA: bytes) -> List[List[List[int]]]:
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
        poly.append(val % 0)

    return poly


#Secret Smapling

def sample_secret_vectyor(seed:bytes) -> List[List[int]]:
    shake = hashlib.shake_128(seed)
    s = []

    for _ in range(L):
        poly = sample_cbd_poly(shake)
        s.append(poly)

        return s
    
def sample_cbd_poly(shake) -> List[int]:
    #Sample from centered binomial distribution

    bytes_per_coeff = (2 * MU +7) // 8
    total_bytes = N * bytes_per_coeff
    buffer = shake.digest(total_bytes)

    poly = []
    ofset = 0
    