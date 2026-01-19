import time
import os
import psutil

from core.pke import generate_pke_keypair
from core.encrypt import encrypt
from core.decrypt import decrypt

RUNS = 100

VARIANTS = [
    ("LightSaber", 2, 3),
    ("Saber",      3, 4),
    ("FireSaber",  4, 6),
]

process = psutil.Process()  # Track current process

def main():
    print("==== SABER AES-256 Encryption/Decryption Benchmark ====\n")
    print(f"Runs per variant: {RUNS}\n")

    for name, L, ET in VARIANTS:
        print(f"--- {name} (L={L}, ET={ET}) ---")

        # ---- KEY GENERATION (once) ----
        start_keygen = time.perf_counter()
        seedA, b, s = generate_pke_keypair(L)
        end_keygen = time.perf_counter()
        pk = {"seedA": seedA, "b": b}
        keygen_time_ms = (end_keygen - start_keygen) * 1000
        keygen_ram_mb = process.memory_info().rss / (1024 * 1024)  # in MB

        total_enc = 0.0
        total_dec = 0.0
        peak_ram_mb = 0.0

        for _ in range(RUNS):
            aes_key = os.urandom(32)

            # ---- ENCRYPT ----
            t0 = time.perf_counter()
            ciphertext = encrypt(pk, aes_key, L, ET)
            t1 = time.perf_counter()

            # ---- DECRYPT ----
            t2 = time.perf_counter()
            decrypted_key = decrypt(s, ciphertext, L, ET)
            t3 = time.perf_counter()

            # RAM after this run
            ram_after = process.memory_info().rss / (1024 * 1024)
            peak_ram_mb = max(peak_ram_mb, ram_after)

            total_enc += (t1 - t0)
            total_dec += (t3 - t2)

            if decrypted_key != aes_key:
                print("ERROR: AES key mismatch!")
                print("orig:", aes_key.hex())
                print("dec :", decrypted_key.hex())
                raise ValueError("Decryption failed")

        avg_enc_ms = (total_enc / RUNS) * 1000
        avg_dec_ms = (total_dec / RUNS) * 1000

        print(f"Keygen time:        {keygen_time_ms:.3f} ms")
        print(f"Avg encryption:     {avg_enc_ms:.3f} ms")
        print(f"Avg decryption:     {avg_dec_ms:.3f} ms")
        print(f"Peak RAM usage:     {peak_ram_mb:.2f} MB")
        print(f"Avg enc+dec total:  {avg_enc_ms + avg_dec_ms:.3f} ms\n")


if __name__ == "__main__":
    main()
