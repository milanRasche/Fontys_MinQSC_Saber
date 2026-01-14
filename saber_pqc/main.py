from core.pke import generate_pke_keypair
from core.encrypt import encrypy
from core.decrypt import decrypt



def main():
    seedA, b, s = generate_pke_keypair()
    pk = {"seedA": seedA, "b": b}

    message = b"Hi"
    ciphertext = encrypy(pk, message)

    print("Generated Ciphertext")
    print(message)
    print(ciphertext)

    decrypted_message = decrypt(s, ciphertext)
    print(decrypted_message)


if __name__ == "__main__":
    main()