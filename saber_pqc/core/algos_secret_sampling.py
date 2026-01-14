import hashlib

from typing import List

from params_all import (
    MU,
    N,
    
)

def sample_secret_vector(seed:bytes, L) -> List[List[int]]:
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