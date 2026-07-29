import argparse
from math import gcd


def extended_euclid_verbose(a: int, b: int):
    divisions = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        divisions.append((old_r, q, r, old_r - q * r))
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    return old_r, old_s, old_t, divisions


def solve_crt(a: int, m1: int, b: int, m2: int) -> None:
    print("=" * 78)
    print("Simultane Kongruenzen mit erweitertem Euklidischen Algorithmus")
    print("=" * 78)
    print("Gegeben:")
    print(f"  z ≡ {a} (mod {m1})")
    print(f"  z ≡ {b} (mod {m2})")
    print()

    print("1) Prüfe die Moduln")
    g_simple = gcd(m1, m2)
    print(f"ggT({m1}, {m2}) = {g_simple}")
    if g_simple != 1:
        print("Die Moduln sind nicht teilerfremd. Dieses Skript behandelt den Fall ggT(m1,m2)=1.")
        return
    print("Die Moduln sind teilerfremd, also gibt es genau eine Lösung modulo m1*m2.")
    print()

    print("2) Euklidischer Algorithmus")
    g, s_m2, t_m1, divisions = extended_euclid_verbose(m2, m1)
    for left, q, right, rest in divisions:
        print(f"{left} = {q} * {right} + {rest}")
    print()

    print("3) Bézout-Darstellung")
    print("Aus dem erweiterten Euklidischen Algorithmus folgt:")
    print(f"1 = ({s_m2})*{m2} + ({t_m1})*{m1}")
    print()

    diff = b - a
    print("4) Differenz der Reste")
    print(f"b - a = {b} - {a} = {diff}")
    print()

    print("5) Multipliziere die Bézout-Gleichung mit (b-a)")
    coef_m2 = s_m2 * diff
    coef_m1 = t_m1 * diff
    print(f"{diff} = ({coef_m2})*{m2} + ({coef_m1})*{m1}")
    print()

    print("6) Konstruktion einer Lösung")
    print("Wir setzen z = a + m1*t0 und wollen z ≡ b (mod m2).")
    print(f"Dann muss m1*t0 ≡ b-a ≡ {diff} (mod {m2}) gelten.")
    print(f"Aus der Gleichung oben lesen wir ab: ({coef_m1})*{m1} ≡ {diff} (mod {m2}).")
    print(f"Also wählen wir t0 = {coef_m1}.")
    z0 = a + m1 * coef_m1
    print(f"Dann ist z = {a} + {m1}*({coef_m1}) = {z0}")
    print()

    modulus = m1 * m2
    smallest = z0 % modulus
    print("7) Gesamtlösung")
    print(f"z ≡ {z0} (mod {modulus})")
    print(f"Also alle Lösungen: z = {z0} + {modulus}*k,  k ∈ Z")
    print(f"Kleinste positive Lösung: {smallest}")
    print()

    print("8) Probe")
    print(f"{smallest} mod {m1} = {smallest % m1}")
    print(f"{smallest} mod {m2} = {smallest % m2}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Löst zwei simultane Kongruenzen z ≡ a (mod m1), z ≡ b (mod m2) mit dem Rechenweg über den erweiterten Euklidischen Algorithmus."
    )
    parser.add_argument("a", type=int, help="Rest a der ersten Kongruenz")
    parser.add_argument("m1", type=int, help="Modul m1 der ersten Kongruenz")
    parser.add_argument("b", type=int, help="Rest b der zweiten Kongruenz")
    parser.add_argument("m2", type=int, help="Modul m2 der zweiten Kongruenz")
    return parser.parse_args()


def main():
    args = parse_args()
    solve_crt(args.a, args.m1, args.b, args.m2)


if __name__ == "__main__":
    main()