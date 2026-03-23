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
    mix_matrix_inverse = np.array([
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
def reverse_s_box(number):
    if number == bitarray('1110'):
        return bitarray('0000')
    if number == bitarray('0100'):
        return bitarray('0001')
    if number == bitarray('1101'):
        return bitarray('0010')
    if number == bitarray('0001'):
        return bitarray('0011')
    if number == bitarray('0010'):
        return bitarray('0100')
    if number == bitarray('1111'):
        return bitarray('0101')
    if number == bitarray('1011'):
        return bitarray('0110')
    if number == bitarray('1000'):
        return bitarray('0111')
    if number == bitarray('0011'):
        return bitarray('1000')
    if number == bitarray('1010'):
        return bitarray('1001')
    if number == bitarray('0110'):
        return bitarray('1010')
    if number == bitarray('1100'):
        return bitarray('1011')
    if number == bitarray('0101'):
        return bitarray('1100')
    if number == bitarray('1001'):
        return bitarray('1101')
    if number == bitarray('0000'):
        return bitarray('1110')
    if number == bitarray('0111'):
        return bitarray('1111')

def shiftrow(texte):
    m=texte[4:8]
    texte[4:8] = texte[12:16]
    texte[12:16] = m
    return texte


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
    text1 = reverse_s_box(text[0:4])
    text2 = reverse_s_box(text[4:8])
    text3 = reverse_s_box(text[8:12])
    text4 = reverse_s_box(text[12:16])
    texte = text1 + text2 + text3 + text4
    return texte


key = "1100001111110000"
ciphertext="1111001111100110"


key0 = generate_keys(key, 0)
key1 = generate_keys(key, 1)
key2 = generate_keys(key, 2)


shift_row = bitarray(ciphertext) ^ key2
print("xor with key2 :" ,shift_row )
kk =bitarray('1111000110100111')
nib = shiftrow(shift_row)

print("shiftrow :" ,nib)

gg =Nibble_Sub(nib)
print("nib_sub :", gg)

print("xor with key1 :", gg ^ key1)

kk =bitarray('1111000110100111')

print("result of mix col :" ,kk)

nib1 = shiftrow(kk)

print ("result of nibsub" , nib1)

rr =Nibble_Sub(nib1)

plaintexte = rr ^ key0 

print(plaintexte)