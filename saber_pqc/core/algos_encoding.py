from core.params_all import (
    Q,
    N
)

def encode_message(m: bytes):
    bits = []
    for byte in m:
        for i in range(8):
            bits.append((byte >> i) & 1)

    poly = [bit * (Q // 2) for bit in bits[:N]]
    return poly