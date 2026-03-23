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

def cesar_codage(n, texte):
   
    alphabet = string.ascii_lowercase
    resultat = ""  
    
    for c in texte :
            resultat += decalage(c, n)  

    return resultat
def cesar_decodage(n, texte):
    alphabet = string.ascii_lowercase
    resultat = ""  
    
    for c in texte :
            resultat += decalage(c, -n)  
        
    return resultat


texte = "é La sécurité est une fonction incontournable des réseaux de communication"
texte = texte.lower()
texte = texte.replace("é", "e").replace("è", "e").replace(" ", "")
texte = texte.translate(str.maketrans("", "", string.punctuation))

cle_cesar = 13  
texte_chiffre = cesar_codage(cle_cesar, texte)
texte_dechiffre = cesar_decodage(cle_cesar, texte_chiffre)

print("chiffre :", texte_chiffre)
print("dechiff :", texte_dechiffre)
print(position('z'))