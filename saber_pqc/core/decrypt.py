import hashlib

from core.params_all import (
    Q,
    N,
    compute_compression_shift_p,
    compute_compression_shift_t
)
from core.algos_polynomial_math import (
    poly_mul,
    poly_add,
    poly_mod
)
from core.algos_compressiong_decompression import decompress_poly

def decrypt(sk, ciphertext, L, ET):
    """
    Decrypt AES key using SABER PKE + shared secret
    """
    u = ciphertext["u"]
    v = ciphertext["v"]
    encrypted_key = ciphertext["encrypted_key"]

    SHIFT_P = compute_compression_shift_p()
    SHIFT_T = compute_compression_shift_t(ET)

    # ---- decompress u and v ----
    u_full = [decompress_poly(p, SHIFT_P) for p in u]
    v_full = decompress_poly(v, SHIFT_T)

    # ---- compute s^T * u (optional, needed if message were embedded) ----
    acc = [0] * N
    for i in range(L):
        prod = poly_mul(sk[i], u_full[i])
        acc = poly_add(acc, prod)
    acc = poly_mod(acc, Q)

    # ---- derive shared secret from v ----
    v_bytes = b"".join(int.to_bytes(c, 2, "little") for c in v)
    shared_secret = hashlib.shake_128(v_bytes).digest(len(encrypted_key))

    # ---- recover AES key ----
    aes_key = bytes([a ^ b for a, b in zip(encrypted_key, shared_secret)])
    return aes_key
