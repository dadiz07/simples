from bitarray import bitarray

def P10(texte):
    return bitarray([texte[2], texte[4], texte[1], texte[6], texte[3], texte[9], texte[0], texte[8], texte[7], texte[5]])

def P8(texte):
    return bitarray([texte[5], texte[2], texte[6], texte[3], texte[7], texte[4], texte[9], texte[8]])

def IP(texte):
    return bitarray([texte[1], texte[5], texte[2], texte[0], texte[3], texte[7], texte[4], texte[6]])

def IP_1(texte):
    return bitarray([texte[3], texte[0], texte[2], texte[4], texte[6], texte[1], texte[7], texte[5]])

def EP(texte):
    return bitarray([texte[3], texte[0], texte[1], texte[2], texte[1], texte[2], texte[3], texte[0]])

def P4(texte):
    return bitarray([texte[1], texte[3], texte[2], texte[0]])

def S0_BOX(number) :
    if number == bitarray('0000') :
        return bitarray ('01')
    if number ==bitarray ('0001') :
        return bitarray('00')
    if number == bitarray('0010') :
        return bitarray('11')    
    if number == bitarray('0011') :
        return bitarray('10')    
    if number == bitarray('0100') :
        return bitarray('11')    
    if number == bitarray('0101') :
        return bitarray('10') 
    if number == bitarray('0110') :
        return bitarray('01')       
    if number == bitarray('0111') :
        return bitarray('00')    
    if number == bitarray('1000') :
        return bitarray('00')    
    if number == bitarray('1001') :
        return bitarray('10')    
    if number == bitarray('1010') :
        return bitarray('01') 
    if number == bitarray('1011') :
        return bitarray('11')
    if number == bitarray('1100') :
        return bitarray('11')
    if number == bitarray('1101') :
        return bitarray('01')
    if number == bitarray('1110') :
        return bitarray('11')
    if number == bitarray('1111') :
        return bitarray('10')   

def S1_BOX(number) :
    if number == bitarray('0000') :
        return bitarray ('00')
    if number ==bitarray ('0001') :
        return bitarray('01')
    if number == bitarray('0010') :
        return bitarray('10')    
    if number == bitarray('0011') :
        return bitarray('11')    
    if number == bitarray('0100') :
        return bitarray('10')    
    if number == bitarray('0101') :
        return bitarray('00') 
    if number == bitarray('0110') :
        return bitarray('01')       
    if number == bitarray('0111') :
        return bitarray('11')    
    if number == bitarray('1000') :
        return bitarray('11')    
    if number == bitarray('1001') :
        return bitarray('00')    
    if number == bitarray('1010') :
        return bitarray('01') 
    if number == bitarray('1011') :
        return bitarray('00')
    if number == bitarray('1100') :
        return bitarray('10')
    if number == bitarray('1101') :
        return bitarray('01')
    if number == bitarray('1110') :
        return bitarray('00')
    if number == bitarray('1111') :
        return bitarray('11')   
    

def generate_keys(key):
  
    k = P10(key)  
    L = k[:5]  
    R = k[5:]  

   
    L = L[1:] + L[:1]
    R = R[1:] + R[:1]
    
    key1 = P8(L + R)  

    L = L[2:] + L[:2]
    R = R[2:] + R[:2]

    key2 = P8(L + R)  
    
    return key1, key2


def chiffrement_DES(plaintext,key):
    
    key1,key2  = generate_keys(key)
    print (key1,key2)

    enc  = IP(plaintext)  
    L0   = enc[4:]
    R0   = enc[:4]

    enc  = EP(R0)
    enc  = enc ^ key1 

    S0   = enc[4:]
    S1   = enc[:4]

   
    new_var0 = bitarray([S0[0], S0[3], S0[1], S0[2]])  
    new_var0 = S0_BOX(new_var0)

    new_var1 = bitarray([S1[0], S1[3], S1[1], S1[2]])  
    new_var1 = S1_BOX(new_var1)

    enc = new_var0 + new_var1  
    enc = P4(enc)

    R1 = L0 ^ enc  

    ciphertext0 = R0 + R1

    L1 = ciphertext0[4:]
    R1 = ciphertext0[:4]

    enc = EP(R1)
    enc = enc ^ key2

    S0   = enc[4:]
    S1   = enc[:4]

    new_var0 = bitarray([S0[0], S0[3], S0[1], S0[2]])  
    new_var0 = S0_BOX(new_var0)

    new_var1 = bitarray([S1[0], S1[3], S1[1], S1[2]])  
    new_var1 = S1_BOX(new_var1)
  
    enc = new_var0 + new_var1  
    enc = P4(enc)

    R2 = L1 ^ enc

    ciphertext1 = R1 + R2

    ciphertext = IP_1(ciphertext1)
    
    return ciphertext

    
def decode_DES(plaintext,key):
    
    key1,key2  = generate_keys(key)
 

    enc  = IP(plaintext)  
    L0   = enc[4:]
    R0   = enc[:4]

    enc  = EP(R0)
    enc  = enc ^ key2 

    S0   = enc[4:]
    S1   = enc[:4]

   
    new_var0 = bitarray([S0[0], S0[3], S0[1], S0[2]])  
    new_var0 = S0_BOX(new_var0)

    new_var1 = bitarray([S1[0], S1[3], S1[1], S1[2]])  
    new_var1 = S1_BOX(new_var1)

    enc = new_var0 + new_var1  
    enc = P4(enc)

    R1 = L0 ^ enc  

    ciphertext0 = R0 + R1

    L1 = ciphertext0[4:]
    R1 = ciphertext0[:4]

    enc = EP(R1)
    enc = enc ^ key1

    S0   = enc[4:]
    S1   = enc[:4]

    new_var0 = bitarray([S0[0], S0[3], S0[1], S0[2]])  
    new_var0 = S0_BOX(new_var0)

    new_var1 = bitarray([S1[0], S1[3], S1[1], S1[2]])  
    new_var1 = S1_BOX(new_var1)
  
    enc = new_var0 + new_var1  
    enc = P4(enc)

    R2 = L1 ^ enc

    ciphertext1 = R1 + R2

    ciphertext = IP_1(ciphertext1)
    
    return ciphertext

    
plaintext = bitarray('01111110') 
key = bitarray ('1010000010') 
ciphertext = chiffrement_DES(plaintext,key)
print('your ciphertext :' , ciphertext)
print('your plaintext' , decode_DES(ciphertext,key))
