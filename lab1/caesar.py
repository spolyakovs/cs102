def encrypt_caesar(plaintext: str) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    key=3
    for i in range (len(plaintext)):
        if plaintext[i].isupper():
            basetext = ord("A")
            simbol = chr((ord(plaintext[i]) - basetext + key) % 26 + basetext)
        elif plaintext[i].islower(): 
            basetext = ord("a")
            simbol = chr((ord(plaintext[i]) - basetext + key) % 26 + basetext)
        else: simbol = plaintext[i]
        ciphertext = ciphertext + simbol
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    key=3
    for i in range (len(ciphertext)):
        if ciphertext[i].isupper():
            numba = ord("A")
            simbol = chr((ord(ciphertext[i]) - numba - key) % 26 + numba)
        elif ciphertext[i].islower(): 
            numba = ord("a")
            simbol = chr((ord(ciphertext[i]) - numba - key) % 26 + numba)
        else: simbol = ciphertext[i]
        plaintext = plaintext + simbol
    return plaintext