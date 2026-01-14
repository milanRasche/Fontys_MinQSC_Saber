from core.pke import generate_pke_keypair
from core.encrypt import encrypy
from core.decrypt import decrypt

L = 3

def main():
    seedA, b, s = generate_pke_keypair(L)
    pk = {"seedA": seedA, "b": b}

    message = b"Hi"
    ciphertext = encrypy(pk, message, L)

    print("Generated Ciphertext")
    print(message)
    print(ciphertext)

    decrypted_message = decrypt(s, ciphertext)
    print(decrypted_message)


if __name__ == "__main__":
    main()