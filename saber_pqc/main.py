import time

from core.pke import generate_pke_keypair
from core.encrypt import encrypt
from core.decrypt import decrypt

L = 4
ET = 3

def main():
    # AES-256 key to encrypt
    hex_key = "f71ca5a5e867119e1fc0d9e802596da2e07f3e83d66b4f2123451a8a0d231afc"
    aes_key = bytes.fromhex(hex_key)
    print(f"Original AES key ({len(aes_key)} bytes): {aes_key.hex()}")

    # ---- KEY GENERATION ----
    print("\n--- Generating Keypair ---")
    start_keygen = time.perf_counter()
    seedA, b, s = generate_pke_keypair(L)
    end_keygen = time.perf_counter()
    print(f"SeedA: {seedA.hex()}")
    print(f"b[0] (first poly): {b[0][:8]} ...")
    print(f"s[0] (first secret poly): {s[0][:8]} ...")
    print(f"Key generation time: {(end_keygen - start_keygen)*1000:.3f} ms")

    pk = {"seedA": seedA, "b": b}

    # ---- ENCRYPT ----
    print("\n--- Encrypting AES key ---")
    start_encrypt = time.perf_counter()
    ciphertext = encrypt(pk, aes_key, L, ET)
    end_encrypt = time.perf_counter()
    print(f"Ciphertext u[0] (first poly): {ciphertext['u'][0][:8]} ...")
    print(f"Ciphertext v (first 16 coeffs): {ciphertext['v'][:16]} ...")
    print(f"Encrypted AES key (first 8 bytes): {ciphertext['encrypted_key'][:8].hex()} ...")
    print(f"Encryption time: {(end_encrypt - start_encrypt)*1000:.3f} ms")

    # ---- DECRYPT ----
    print("\n--- Decrypting AES key ---")
    start_decrypt = time.perf_counter()
    decrypted_key = decrypt(s, ciphertext, L, ET)
    end_decrypt = time.perf_counter()
    print(f"Decrypted AES key: {decrypted_key.hex()}")
    print(f"Decryption time: {(end_decrypt - start_decrypt)*1000:.3f} ms")

    # ---- VERIFY ----
    if decrypted_key != aes_key:
        raise ValueError("Decryption failed: AES key mismatch!")
    else:
        print("\nAES key successfully encrypted and decrypted via SABER PKE + shared secret.")

if __name__ == "__main__":
    main()
