from core.params_all import Q

def poly_add_const_compression(poly, c):
    return [(x + c) % Q for x in poly]


def compress_poly(poly, shift):
    return [(x >> shift) for x in poly]


def decompress_poly(poly, shift):
    return [(x << shift) for x in poly]
