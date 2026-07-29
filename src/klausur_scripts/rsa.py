import argparse
from math import gcd
from typing import List, Tuple


def prime_factorization(n: int) -> List[Tuple[int, int]]:
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            count = 0
            while n % d == 0:
                n //= d
                count += 1
            factors.append((d, count))
        d = 3 if d == 2 else d + 2
    if n > 1:
        factors.append((n, 1))
    return factors


def phi(n: int) -> Tuple[int, List[Tuple[int, int]]]:
    factors = prime_factorization(n)
    result = n
    for p, _ in factors:
        result = result // p * (p - 1)
    return result, factors


def factor_str(factors: List[Tuple[int, int]]) -> str:
    parts = []
    for p, k in factors:
        parts.append(str(p) if k == 1 else f"{p}^{k}")
    return " * ".join(parts) if parts else "1"


def mod_pow_trace(base: int, exp: int, mod: int):
    steps = []
    result = 1
    base = base % mod
    current_exp = exp
    while current_exp > 0:
        before_result = result
        before_base = base
        odd = current_exp % 2 == 1
        if odd:
            result = (result * base) % mod
        squared_base = (base * base) % mod
        steps.append({
            "exp": current_exp,
            "odd": odd,
            "result_before": before_result,
            "base_before": before_base,
            "result_after": result,
            "base_after": squared_base,
        })
        base = squared_base
        current_exp //= 2
    return result, steps


def extended_euclid_steps(a: int, b: int):
    steps = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        steps.append({
            "old_r": old_r,
            "r": r,
            "q": q,
            "remainder": old_r - q * r,
        })
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t, steps


def print_header(title: str) -> None:
    print("=" * 78)
    print(title)
    print("=" * 78)


def print_pow_steps(label: str, base: int, exp: int, mod: int, value: int, steps) -> None:
    print(f"{label}: {base}^{exp} mod {mod}")
    for i, step in enumerate(steps, start=1):
        e = step['exp']
        rb = step['result_before']
        bb = step['base_before']
        ra = step['result_after']
        ba = step['base_after']
        if step['odd']:
            print(f"  Schritt {i}: Exponent {e} ist ungerade")
            print(f"    result = ({rb} * {bb}) mod {mod} = {ra}")
            print(f"    neue Basis = ({bb}^2) mod {mod} = {ba}")
        else:
            print(f"  Schritt {i}: Exponent {e} ist gerade")
            print(f"    result bleibt {rb}")
            print(f"    neue Basis = ({bb}^2) mod {mod} = {ba}")
    print(f"  Ergebnis: {base}^{exp} mod {mod} = {value}")
    print()


def solve_verbose(m: int, e: int, a: int | None = None) -> None:
    print_header("RSA: privaten Schlüssel d berechnen")
    print(f"Gegeben: m = {m}, e = {e}")
    if a is not None:
        print(f"Zusätzlicher Klartext a = {a}")
    print()

    phi_m, factors_m = phi(m)
    print("1) Primfaktorzerlegung von m und Berechnung von φ(m)")
    print(f"m = {m} = {factor_str(factors_m)}")
    print("Formel: φ(m) = m * Π (1 - 1/p) über alle verschiedenen Primfaktoren p von m")
    print(f"Daher: φ({m}) = {phi_m}")
    print()

    g = gcd(e, phi_m)
    print("2) Bedingung für die Existenz von d")
    print(f"ggT(e, φ(m)) = ggT({e}, {phi_m}) = {g}")
    if g != 1:
        print("Da der ggT nicht 1 ist, besitzt e kein Inverses modulo φ(m).")
        print("Also existiert kein gültiger privater Schlüssel d.")
        return
    print("Da der ggT = 1 ist, besitzt e ein Inverses modulo φ(m).")
    print(f"Gesucht ist also d mit: {e} * d ≡ 1 (mod {phi_m})")
    print()

    print("3) Lösungsweg 1: Satz von Euler + schnelles Potenzieren")
    phi_phi_m, factors_phi = phi(phi_m)
    print(f"Zuerst berechnen wir φ(φ(m)) = φ({phi_m}).")
    print(f"{phi_m} = {factor_str(factors_phi)}")
    print(f"Also: φ({phi_m}) = {phi_phi_m}")
    print("Nach dem Satz von Euler gilt:")
    print("e^φ(φ(m)) ≡ 1 (mod φ(m))")
    print("Also ist e^(φ(φ(m)) - 1) ein Inverses von e modulo φ(m).")
    print(f"Damit: d ≡ {e}^{phi_phi_m - 1} (mod {phi_m})")
    print()
    d_euler, pow_steps = mod_pow_trace(e, phi_phi_m - 1, phi_m)
    print_pow_steps("Square-and-Multiply für d", e, phi_phi_m - 1, phi_m, d_euler, pow_steps)

    print("4) Lösungsweg 2: Bézout / Erweiterter Euklidischer Algorithmus")
    gcd_val, x, y, ee_steps = extended_euclid_steps(e, phi_m)
    for i, step in enumerate(ee_steps, start=1):
        print(f"  Schritt {i}: {step['old_r']} = {step['q']} * {step['r']} + {step['remainder']}")
    print()
    print("Bézout-Koeffizienten liefern:")
    print(f"{x} * {e} + ({y}) * {phi_m} = {gcd_val}")
    d_ea = x % phi_m
    print(f"Also: d ≡ {x} ≡ {d_ea} (mod {phi_m})")
    print(f"Ergebnis von Lösungsweg 2: d = {d_ea}")
    print()

    print("5) Vergleich und Prüfung von d")
    print(f"Lösungsweg 1 liefert d = {d_euler}")
    print(f"Lösungsweg 2 liefert d = {d_ea}")
    print(f"Prüfung: {e} * {d_ea} = {e * d_ea}")
    print(f"{e * d_ea} mod {phi_m} = {(e * d_ea) % phi_m}")
    print(f"Privater Schlüssel d = {d_ea}")
    print()

    if a is not None:
        print("6) Verschlüsselung des Klartexts a")
        if not (0 <= a < m):
            print(f"Warnung: Für RSA wählt man normalerweise 0 <= a < m. Hier ist a = {a}.")
            print(f"Wir reduzieren daher zuerst modulo m: a ≡ {a % m} (mod {m})")
            a = a % m
            print()
        c, enc_steps = mod_pow_trace(a, e, m)
        print_pow_steps("Verschlüsselung c = a^e mod m", a, e, m, c, enc_steps)
        print(f"Codewort c = {c}")
        print()

        print("7) Entschlüsselung des Codeworts c")
        adec, dec_steps = mod_pow_trace(c, d_ea, m)
        print_pow_steps("Entschlüsselung a = c^d mod m", c, d_ea, m, adec, dec_steps)
        print(f"Wiedergewonnener Klartext = {adec}")
        print()

        print("8) Gesamtprüfung")
        print(f"Startwert a = {a}")
        print(f"Verschlüsselt c = {c}")
        print(f"Entschlüsselt a' = {adec}")
        if adec == a:
            print("Die Entschlüsselung liefert wieder den ursprünglichen Klartext.")
        else:
            print("Die Entschlüsselung weicht vom ursprünglichen Klartext ab.")
        print()


def parse_args():
    parser = argparse.ArgumentParser(
        description="RSA-Rechner mit vollständigem Rechenweg: Bestimmt d und kann zusätzlich verschlüsseln und entschlüsseln."
    )
    parser.add_argument("m", type=int, help="RSA-Modulus m")
    parser.add_argument("e", type=int, help="öffentlicher Exponent e")
    parser.add_argument("--a", type=int, default=None, help="Optionaler Klartext a zur Verschlüsselung und Entschlüsselung")
    return parser.parse_args()


def main():
    args = parse_args()
    solve_verbose(args.m, args.e, args.a)


if __name__ == "__main__":
    main()