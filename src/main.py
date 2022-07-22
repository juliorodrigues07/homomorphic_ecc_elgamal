from cryptographic_functions import homomorphic_tally
from cryptographic_functions import keys_generator
from cryptographic_functions import encryption
from cryptographic_functions import g_point
from cryptographic_functions import random
from cryptographic_functions import n
import time


def main():

    # DECRIPTAÇÃO HOMOMÓRFICA (El Gamal exponencial aditivo)
    begin_1 = time.time()
    votes, first_pairs, seconds_pairs = list(), list(), list()
    private_key, public_key, ephemeral_key = keys_generator()

    for i in range(n):

        # Gera os votos para um candidato de forma aleatória (1: recebeu o voto | 0: não recebeu o voto)
        votes.append(random.randint(0, 1))

        # Realiza a encriptação de cada voto
        a, b = encryption(votes[i], public_key, ephemeral_key)

        # Acumula os pares de textos cifrados de cada voto
        first_pairs.append(a)
        seconds_pairs.append(b)

    begin_2 = time.time()
    tally = homomorphic_tally(private_key, first_pairs, seconds_pairs)
    end_1 = time.time()

    print('\nTOTAL DE VOTOS: ' + str(n) + '\n')

    # Contagem dos votos: incrementar G até que este seja igual à private_key * g_point (tally)
    i = 0
    s = g_point * 0
    while tally != s and i < n + 1:
        s += g_point
        i += 1

    print('Totalização homomórfica:          ' + str(i) + ' votos')
    end_2 = time.time()

    print('\nTempo total:                      ' + str(round(end_2 - begin_1, 3)) + 's')
    print('Tempo para encriptação dos votos: ' + str(round(begin_2 - begin_1, 3)) + 's')
    print('Tempo para decriptação dos votos: ' + str(round(end_1 - begin_2, 3)) + 's')
    print('Tempo para totalização dos votos: ' + str(round(end_2 - end_1, 3)) + 's' + '\n')


if __name__ == '__main__':
    main()
