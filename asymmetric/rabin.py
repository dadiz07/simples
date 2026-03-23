from sympy import isprime, gcdex

def verify_rabin_keys(p, q):
    
    if (not (isprime(p) and isprime(q))) or (p % 4 != 3 or q % 4 != 3):
        return False
    else:
         return True     


def extended_gcd(p, q):
    
    a, b, _ = gcdex(p, q)
    return a, b



def encrypt_rabin(plaintext,p,q):
    n= p*q
    c = pow(plaintext, 2, n)  
    return c



def decrypt_rabin(ciphertext, p, q):
    n  = p * q  
    m  = pow(ciphertext,0.5) % n
    print(m)
    mp = pow(ciphertext,(p+1)//4,p) % n
    mq = pow(ciphertext,(q+1)//4,q) % n
    Yp , Yq = extended_gcd(p,q)
    R = (p * mq * Yp + q * mp * Yp ) % n 
    S = (p * mq * Yp - q * mp * Yp ) % n
    return R,S,n-R,n-S

p = 59
q = 47  
plaintext = 42
print(verify_rabin_keys(p, q))
ciphertext = (encrypt_rabin(plaintext,p,q))
print(ciphertext)
print(decrypt_rabin(ciphertext,p,q))