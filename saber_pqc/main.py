import time

from core.pke import generate_pke_keypair
from core.encrypt import encrypy
from core.decrypt import decrypt

L = 3
RUNS = 100


def main():
    hex_key = "f71ca5a5e867119e1fc0d9e802596da2e07f3e83d66b4f2123451a8a0d231afc"
    message = bytes.fromhex(hex_key)

    total_keygen = 0.0
    total_encrypt_only = 0.0
    total_encrypt_with_keygen = 0.0
    total_decrypt = 0.0

    for i in range(RUNS):
        # ---- ENCRYPT (including keygen) ----
        enc_start = time.perf_counter()

        keygen_start = time.perf_counter()
        seedA, b, s = generate_pke_keypair(L)
        keygen_end = time.perf_counter()

        pk = {"seedA": seedA, "b": b}

        encrypt_start = time.perf_counter()
        ciphertext = encrypy(pk, message, L)
        encrypt_end = time.perf_counter()

        enc_end = time.perf_counter()

        # ---- DECRYPT ----
        dec_start = time.perf_counter()
        decrypted_message = decrypt(s, ciphertext)
        dec_end = time.perf_counter()

        # ---- VERIFY ----
        if decrypted_message != message:
            raise ValueError(f"Decryption failed at run {i}")

        # ---- ACCUMULATE TIMES ----
        total_keygen += (keygen_end - keygen_start)
        total_encrypt_only += (encrypt_end - encrypt_start)
        total_encrypt_with_keygen += (enc_end - enc_start)
        total_decrypt += (dec_end - dec_start)

    # ---- AVERAGES ----
    avg_keygen = total_keygen / RUNS
    avg_encrypt_only = total_encrypt_only / RUNS
    avg_encrypt_with_keygen = total_encrypt_with_keygen / RUNS
    avg_decrypt = total_decrypt / RUNS

    print(f"Runs: {RUNS}")
    print("\n--- Average Timing (seconds) ---")
    print(f"Avg key generation: {avg_keygen:.6f}")
    print(f"Avg encryption (only): {avg_encrypt_only:.6f}")
    print(f"Avg encrypt (keygen + encrypt): {avg_encrypt_with_keygen:.6f}")
    print(f"Avg decryption: {avg_decrypt:.6f}")

    print("\n--- Average Timing (milliseconds) ---")
    print(f"Avg key generation: {avg_keygen * 1000:.3f} ms")
    print(f"Avg encryption (only): {avg_encrypt_only * 1000:.3f} ms")
    print(f"Avg encrypt (keygen + encrypt): {avg_encrypt_with_keygen * 1000:.3f} ms")
    print(f"Avg decryption: {avg_decrypt * 1000:.3f} ms")


if __name__ == "__main__":
    main()
