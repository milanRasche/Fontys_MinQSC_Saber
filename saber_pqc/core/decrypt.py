from core.params_all import (
    Q,
    N
)

from core.algos_polynomial_math import (
    poly_mul,
    poly_add,
    poly_mod
)

def decrypt(sk, ciphertext):
    s = sk
    bp = ciphertext["bp"]
    vp = ciphertext["vp"]

    acc = [0] * N
    for i in range(len(s)):
        prod = poly_mul(s[i], bp[i])
        acc = poly_add(acc, prod)

    acc = poly_mod(acc, Q)

    m_poly = [(v - a) % Q for v, a in zip(vp, acc)]

    message = decode_message(m_poly)
    return message

def decode_message(m_poly):
    bits = []
    threshold = Q // 4

    for coeff in m_poly:
        if coeff > threshold:
            bits.append(1)
        else:
            bits.append(0)

    # Convert bits → bytes
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte |= bits[i + j] << j
        out.append(byte)

    return bytes(out)