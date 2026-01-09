#Nothing here yet just doing some general scafolding
#from core.keygen import generate_saber_kem_keypair
from core.pke import generate_pke_keypair


def main():
    print("Generating Keypair")
    seedA, b, s = generate_pke_keypair()
    print(len(b), len(b[0]))
    print(seedA)


if __name__ == "__main__":
    main()