"""CSC111 Winter 2023 Course Project
===============================
This Python module contains the implemented encryption and decryption of the project.
Copyright and Usage Information
===============================
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.
This file is Copyright (c) 2023 Nicolas Dias Martins, Sana-E-Zehra Mehdi, Rohan Patra, and Maleeha Rahman.
"""
import csv
import random
import math


def read_csv(primes_list: str) -> list[int]:
    """Return a list of ints based on prime_list.
    Preconditions:
        - primes_list refers to a csv file in the format described on the project report
    """
    primes = []
    with open(primes_list) as csv_file:

        for row in csv.reader(csv_file):
            primes.append(int(row[0]))

    return primes


def select_primes(primes_list: str) -> tuple[int, int]:
    """Return a tuple of ints based on a list created from prime_list.
    Preconditions:
        - primes_list refers to a csv file in the format described on the project report
    """
    primes = read_csv(primes_list)
    first_prime = random.choice(primes)
    primes.remove(first_prime)
    second_prime = random.choice(primes)

    return (first_prime, second_prime)


def generate_keys(primes_list: str) -> tuple[tuple[int, int, int], tuple[int, int]]:
    """Return a generated pair of a public and a private key.
    This function returns a tuple of the format (public key, private key).
    Preconditions:
        - isinstance(primes_list, str)
    """
    primes = select_primes(primes_list)
    p, q = primes

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = random.randint(2, phi - 1)
    while ((d * e) - 1) % phi != 0:
        d = random.randint(2, phi - 1)

    assert verify_key((p, q, d), (n, e))

    return ((p, q, d), (n, e))


def verify_key(private_key: tuple[int, int, int], public_key: tuple[int, int]) -> bool:
    """Helper function for generate_private_key."""
    n, e = public_key
    p, q, d = private_key

    if (p * q) != n:
        return False

    test_message = 'I am the master of my fate, I am the captain of my soul.'
    cyphertext = file_encrypt_str(test_message, public_key)
    decrypted_text = file_decrypt_str(cyphertext, private_key)
    if decrypted_text == test_message:
        return True
    else:
        return False


def file_encrypt_str(plaintext: str, public_key: tuple[int, int]) -> str:
    """Encrypt the given plaintext by using the public key.
    Preconditions:
        - len(plaintext) > 0
    """
    n, e = public_key
    encrypted_text = ''

    for char in plaintext:
        encrypted_text = encrypted_text + chr((ord(char) ** e) % n)

    return encrypted_text


def file_decrypt_str(cyphertext: str, private_key: tuple[int, int, int]) -> str:
    """Decrypt the given cyphertext by using the private key.
    Preconditions:
        - len(cyphertext) > 0
    """
    p, q, d = private_key
    n = p * q
    decrypted_text = ''

    for char in cyphertext:
        decrypted_text = decrypted_text + chr((ord(char) ** d) % n)

    return decrypted_text


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'random', 'math'],
        'disable': ['forbidden-IO-import', 'unused-variable']
    })
