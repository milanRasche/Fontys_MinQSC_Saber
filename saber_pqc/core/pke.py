import os
import hashlib
from typing import List

from 

#Params Constant across all 3 Saber Versions
N = 256
Q = 8192 #2^13
EQ = 13

#Params Saber
L = 3
MU = 10
SEED_BYTES = 32
EP = 10
ET = 3

def generate_pke_keypair():
    #Generate Uniform Seed
    seedA = os.urandom(SEED_BYTES)

    #Expand from seed A using Shake128 (128 Hashing ALgorithm in SHA-3)
    A = generate_matrix_A(seedA)

    #Sample secret vectore from binomial distribution
    seed_s = os.urandom(SEED_BYTES) #Not True Random but close enough for testing purposes
    s = sample_secret_vector(seed_s)

    #Compute b= A^T * s + h (mod q)
    h = computer_rounding_constant()
    b = matrix_vector_transpose(A, s, h)

    return seedA, b, s



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
        poly.append(val % Q)

    return poly

#TODO: Stuff down here needs to go into a different file as its used in other palces.
#Secret Smapling

def sample_secret_vector(seed:bytes) -> List[List[int]]:
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
    offset = 0

    for _ in range(N):
        chunk = buffer[offset:offset + bytes_per_coeff]
        offset += bytes_per_coeff
        poly.append(centered_binomial(chunk))
    
    return poly

def centered_binomial(data: bytes) -> int:

    bits = bin(int.from_bytes(data, byteorder="big")).removeprefix('0b')

    a = sum(int(b) for b in bits[:MU])
    b = sum(int(b) for b in bits[MU:2 * MU])

    return a - b
