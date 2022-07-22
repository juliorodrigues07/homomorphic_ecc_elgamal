from Cryptodome.PublicKey import ECC
from Cryptodome.Random import random

# Total de eleitores
n = 5000

# Curva elíptica selecionda
e_curve = 'P-256'

# Ponto G (gerador)
g_point = ECC.EccPoint(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                       0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)


def keys_generator():

    # Gera a chave privada e a chave pública a partir do ponto G
    key = ECC.generate(curve=e_curve)

    # Geração da chave efêmera (256 bits para a curva P-256)
    ephemeral_key = random.getrandbits(256)

    private_key = key.d
    public_key = key.pointQ

    return private_key, public_key, ephemeral_key


def encryption(vote, public_key, ephemeral_key):

    # k * G
    first_pair = g_point * ephemeral_key

    # v * G + k * P
    second_pair = (g_point * vote) + (public_key * ephemeral_key)

    return first_pair, second_pair


def decryption(private_key, first_pair, second_pair):

    # inverso(A * x) + B
    message = (-(first_pair * private_key)) + second_pair

    return message


def homomorphic_tally(private_key, first_pair, second_pair):

    i = 1
    a = first_pair[0]
    b = second_pair[0]

    while i < n:

        # Acumula o total dos pares de textos cifrados de votos encriptados
        a += first_pair[i]
        b += second_pair[i]
        i += 1

    # Decripta o total (soma homomórfica)
    message = decryption(private_key, a, b)
    return message
