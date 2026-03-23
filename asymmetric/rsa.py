
from sympy import factorint, mod_inverse

def encrypt_message(plaintext, n, e):
    return pow(plaintext, e, n)

def decrypt_message(ciphertext, n, e):
    factors = factorint(n)  
    p, q = list(factors.keys())  

    phi = (p - 1) * (q - 1)

    d = mod_inverse(e, phi)  

    plaintext = pow(ciphertext, d, n)
    return plaintext


n = 18446744400127067027 
e = 65537   
plaintext = 12345678  


ciphertext = encrypt_message(plaintext, n, e)
print('Encrypted text:', ciphertext)

plaintext = decrypt_message(ciphertext, n, e)
print('Decrypted text:', plaintext)
