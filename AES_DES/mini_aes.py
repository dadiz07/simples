from bitarray import bitarray
import numpy as np
def gf2_multiply(a, b):
    """
    Multiply two numbers in GF(2^4) and reduce modulo x^4 + x + 1 (0b10011)
    """
    result = 0
    modulus = 0b10011  # x^4 + x + 1
    
    for i in range(4):  # Iterate over each bit of b
        if (b >> i) & 1:  # If the i-th bit of b is 1, XOR shifted a into result
            result ^= (a << i)
    
    # Perform modular reduction if result is greater than 4 bits
    for i in range(7, 3, -1):  # Highest possible bit index (7 down to 4)
        if (result >> i) & 1:  # If the i-th bit is 1, reduce
            result ^= (modulus << (i - 4))
    
    return result & 0b1111  # Ensure the result is within 4 bits

def s_box(number):
    if number == bitarray('0000') :
        return bitarray ('1110')
    if number ==bitarray ('0001') :
        return bitarray('0100')
    if number == bitarray('0010') :
        return bitarray('1101')    
    if number == bitarray('0011') :
        return bitarray('0001')    
    if number == bitarray('0100') :
        return bitarray('0010')    
    if number == bitarray('0101') :
        return bitarray('1111') 
    if number == bitarray('0110') :
        return bitarray('1011')       
    if number == bitarray('0111') :
        return bitarray('1000')    
    if number == bitarray('1000') :
        return bitarray('0011')    
    if number == bitarray('1001') :
        return bitarray('1010')    
    if number == bitarray('1010') :
        return bitarray('0110') 
    if number == bitarray('1011') :
        return bitarray('1100')
    if number == bitarray('1100') :
        return bitarray('0101')
    if number == bitarray('1101') :
        return bitarray('1001')
    if number == bitarray('1110') :
        return bitarray('0000')
    if number == bitarray('1111') :
        return bitarray('0111')               
    
def generate_keys(key,round):
    
    w0 = bitarray(key[0:4])  
    w1 = bitarray(key[4:8])
    w2 = bitarray(key[8:12])
    w3 = bitarray(key[12:16])

    w4 = w0 ^ s_box(w3) ^ bitarray('0001')
    w5 = w1 ^ w4
    w6 = w2 ^ w5
    w7 = w3 ^ w6

    w8 = w4 ^ s_box(w7) ^ bitarray('0010')
    w9 = w5 ^ w8
    w10 = w6 ^ w9
    w11 = w7 ^ w10

    if round ==0 :
        w = w0 + w1 + w2 + w3
    elif  round ==1 :
        w = w4 + w5 + w6 + w7
    elif round ==2 :
        w = w8 + w9 + w10 + w11
    return w
    
def Nibble_Sub(text):
    text = bitarray(text)
    text1 = s_box(text[0:4])
    text2 = s_box(text[4:8])
    text3 = s_box(text[8:12])
    text4 = s_box(text[12:16])
    texte = text1 + text2 + text3 + text4
    return texte

def shiftrow(texte):
    m=texte[4:8]
    texte[4:8] = texte[12:16]
    texte[12:16] = m
    return texte

def mix_columns(texte):

    """
    Perform MixColumns transformation in GF(2^4)
    """
    texte_string = texte.to01()  # Convert bitarray to string
    
    # Construct the 2x2 state matrix in binary
    state = np.array([
        [int(texte_string[0:4], 2), int(texte_string[8:12], 2)],
        [int(texte_string[4:8], 2), int(texte_string[12:16], 2)]
    ])
    
    # MixColumns matrix in GF(2^4)
    mix_matrix = np.array([
        [2, 3],
        [3, 2]
    ])
    
    # Perform matrix multiplication in GF(2^4)
    result_matrix = np.zeros((2, 2), dtype=int)
    for i in range(2):
        for j in range(2):
            result_matrix[i][j] = gf2_multiply(mix_matrix[i][0], state[0][j]) ^ gf2_multiply(mix_matrix[i][1], state[1][j])
    
    # Convert result matrix back to bitarray
    result_bits = bitarray(f"{result_matrix[0][0]:04b}{result_matrix[1][0]:04b}{result_matrix[0][1]:04b}{result_matrix[1][1]:04b}")
    
    return result_bits

def mini_AES(plaintexte,key) :
    
    key0 = generate_keys(key, 0)
    key1 = generate_keys(key, 1)
    key2 = generate_keys(key, 2)

    bit_plain = bitarray(plaintexte)^ key0
    print("first xor :",bit_plain)

    p_new = Nibble_Sub(bit_plain)
    print("Nibble_Sub:", p_new)


    shift_new = shiftrow(p_new)
    print("ShiftRow:", shift_new)


    result = mix_columns(shift_new)


    w0, w1, w2, w3 = result[0:4], result[4:8], result[8:12], result[12:16]
    result_new = w0 + w2 + w1 + w3  # Reordering
    print("MixColumns:", result_new)


    phase2 = result_new ^ key1
    print("XOR with Key1:", phase2)   


    phase2_new = Nibble_Sub(phase2)
    print("Nibble_Sub:", phase2_new)


    last = shiftrow(phase2_new)
    print("ShiftRow:", last)


    ciphertext = last ^ key2
    print("Ciphertext:", ciphertext)

    return ciphertext 

plaintexte = "1001110001100011"
key = "1100001111110000"
       
mini_AES(plaintexte,key)

