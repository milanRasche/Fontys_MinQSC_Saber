def pack_poly(coeffs, bits):
    out = bytearray()
    acc = 0
    acc_bits = 0

    for c in coeffs:
        acc |= (c & ((1 << bits) - 1)) << acc_bits
        acc_bits += bits

        while acc_bits >= 8:
            out.append(acc & 0xff)
            acc >>= 8
            acc_bits -= 8

    if acc_bits > 0:
        out.append(acc & 0xff)

    return bytes(out)

def unpack_poly(data, bits, n):
    coeffs = []
    acc = 0
    acc_bits = 0
    idx = 0

    for _ in range(n):
        while acc_bits < bits:
            acc |= data[idx] << acc_bits
            acc_bits += 8
            idx += 1

        coeffs.append(acc & ((1 << bits) - 1))
        acc >>= bits
        acc_bits -= bits

    return coeffs, idx

def serialize_pk(seedA, b, EP):
    out = bytearray(seedA)
    for poly in b:
        out += pack_poly(poly, EP)
    return bytes(out)

def deserialize_pk(pk_bytes, L, N, EP):
    seedA = pk_bytes[:32]
    offset = 32
    b = []

    for _ in range(L):
        poly, used = unpack_poly(pk_bytes[offset:], EP, N)
        b.append(poly)
        offset += used

    return seedA, b

def serialize_ct(u, v, EP, ET):
    out = bytearray()
    for poly in u:
        out += pack_poly(poly, EP)
    out += pack_poly(v, ET)
    return bytes(out)
