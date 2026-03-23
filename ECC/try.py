
def is_on_curve(x, y):
    return (y ** 2) % p == (x ** 3 + a * x + b) % p


def generate_points():
    points = []
    for x in range(p):
        for y in range(p):
            if (y * y) % p == (x ** 3 + a * x + b) % p:
                points.append((x, y))
    return points


def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        l = (3 * P[0] ** 2 + a) * pow(2 * P[1], -1, p) % p
    else:                         #
        if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
            return None  # Point à l'infini
        l = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p
                            #
    x_r = (l ** 2 - P[0] - Q[0]) % p
    y_r = (l * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)


def scalar_mult(k, P):
    R = None
    while k > 0:
        if k & 1:
            R = P if R is None else point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R


def ecdh_key_exchange(private_key, public_key):
    return scalar_mult(private_key, public_key)


# Signature ECDSA

def ecdsa_sign(d, m, G, t):
    while True:
        k = 3  # Choix fixe pour la démo, mais devrait être aléatoire !
        Q = scalar_mult(k, G)
        r = Q[0] % t
        if r == 0:
            continue
        k_inv = pow(k, -1, t)
                
        s = (k_inv * (d * r + m)) % t
        if s == 0:
            continue
        return (r, s)


def ecdsa_verify(P, m, r, s, G, t):
    if not (1 <= r < t and 1 <= s < t):
        return False
    s_inv = pow(s, -1, t)
            
    u1 = (m * s_inv) % t
    u2 = (r * s_inv) % t
    Q = point_add(scalar_mult(u1, G), scalar_mult(u2, P))
    if Q is None:
        return False
    return Q[0] % t == r


def main():
    print("Génération des points de la courbe : y² = x³ + 2x + 2 mod 17")
    points = generate_points()
    for pt in points:
        print(f"Point: {pt}")
    print(f"Total: {len(points)} points")

    # Choisir un point générateur
    G = (5, 16)
    assert G in points
    print(f"\n==> Point générateur choisi : {G}")

    # Ordre supposé du point
    t = 19

    # Clés privées
    d_A = 7
    d_B = 3

    # Clés publiques
    P_A = scalar_mult(d_A, G)
    P_B = scalar_mult(d_B, G)

    print(f"\n==> Clé publique Alice : {P_A}")
    print(f"==> Clé publique Bob : {P_B}")

    # ECDH - échange de clé
    S_A = ecdh_key_exchange(d_A, P_B)
    S_B = ecdh_key_exchange(d_B, P_A)

    print(f"\nClé partagée (Alice) : {S_A}")
    print(f"Clé partagée (Bob) : {S_B}")

    # ECDSA - signature
    message = 13
    r, s = ecdsa_sign(d_A, message, G, t)

    print(f"\nSignature de Alice sur le message {message} :")
    print(f"r = {r}, s = {s}")

    # Vérification
    valid = ecdsa_verify(P_A, message, r, s, G, t)
    print(f"\nVérification de la signature : {'valide' if valid else 'invalide'}")

p = 17
a = 2
b = 2

if __name__ == "__main__":
    main()
