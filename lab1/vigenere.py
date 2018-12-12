def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    for i in range (len(plaintext)):
        keynumb = i % len(keyword)
        if plaintext[i].isupper():
            basekey = ord("A")
        elif plaintext[i].islower():
            basekey = ord("a")
        key = ord(keyword[keynumb]) - basekey
        if plaintext[i].isupper():
            basetext = ord("A")
            simbol = chr((ord(plaintext[i]) - basetext + key) % 26 + basetext)
        elif plaintext[i].islower():
            basetext = ord("a")
            simbol = chr((ord(plaintext[i]) - basetext + key) % 26 + basetext)
        else: simbol = plaintext[i]
        ciphertext = ciphertext + simbol
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    for i in range (len(ciphertext)):
        keynumb = i % len(keyword)
        if ciphertext[i].isupper():
            basekey = ord("A")
        elif ciphertext[i].islower():
            basekey = ord("a")
        key = ord(keyword[keynumb]) - basekey
        if ciphertext[i].isupper():
            basetext = ord("A")
            simbol = chr((ord(ciphertext[i]) - basetext - key) % 26 + basetext)
        elif ciphertext[i].islower():
            basetext = ord("a")
            simbol = chr((ord(ciphertext[i]) - basetext - key) % 26 + basetext)
        else: simbol = ciphertext[i]
        plaintext = plaintext + simbol
    return plaintext
