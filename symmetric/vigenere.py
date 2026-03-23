import string


def position(x):
    alphabet = string.ascii_lowercase
    if x in alphabet :
     return alphabet.index(x)
    else :
      return -1

def decalage(x, n):
    alphabet = string.ascii_lowercase
    return alphabet[(position(x) + n) % 26]

def vigenere_coder(texte, cle):
    texte = texte.replace("é", "e").replace("è", "e").replace(" ", "")
    texte = texte.translate(str.maketrans("", "", string.punctuation))
    texte_code = ""
    
    for i, c in enumerate(texte):
        
        decal = position(cle[i % len(cle)])
        texte_code += decalage(c, decal)

    return texte_code

def vigenere_decoder(texte_code, cle):
   
    alphabet = string.ascii_lowercase
    texte = ""
    cle = cle.lower()

    for i, c in enumerate(texte_code):
        if c in alphabet:
            decal = position(cle[i % len(cle)])
            texte += decalage(c, -decal)
        else:
            texte += c

    return texte

texte = "le chiffrement est utile. mais n'est pas youjour efficase"
cle ="azerty"    


result=vigenere_coder(texte, cle)
print ("chiffre :",result)
result2 = vigenere_decoder(result, cle)
print("dechiff :",result2)