#Nothing here yet just doing some general scafolding
#from core.keygen import generate_saber_kem_keypair
from core.pke import generate_pke_keypair
from core.encrypt import encrypy


def main():
    seedA, b, s = generate_pke_keypair()
    pk = {"seedA": seedA, "b": b}

    message = b"Hi"
    ciphertext = encrypy(pk, message)

    print("Generated Ciphertext")
    print(ciphertext)


if __name__ == "__main__":
    main()