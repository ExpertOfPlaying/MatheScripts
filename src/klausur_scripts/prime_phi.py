import argparse
from collections import Counter


def prime_factorization_steps(n: int):
    steps = []
    factors = []
    current = n
    divisor = 2

    while divisor * divisor <= current:
        while current % divisor == 0:
            new_value = current // divisor
            steps.append((current, divisor, new_value))
            factors.append(divisor)
            current = new_value
        divisor = 3 if divisor == 2 else divisor + 2

    if current > 1:
        steps.append((current, current, 1))
        factors.append(current)

    return factors, steps


def format_factorization(counter: Counter) -> str:
    parts = []
    for p in sorted(counter):
        exp = counter[p]
        parts.append(f"{p}^{exp}" if exp > 1 else str(p))
    return " * ".join(parts)


def phi_from_factorization(counter: Counter):
    result = 1
    detail_rows = []
    for p in sorted(counter):
        k = counter[p]
        term_value = (p ** (k - 1)) * (p - 1)
        result *= term_value
        detail_rows.append((p, k, f"{p}^({k}-1) * ({p}-1)", term_value))
    return result, detail_rows


def parse_args():
    parser = argparse.ArgumentParser(
        description="Liest eine Zahl z ein, zerlegt sie in Primfaktoren und berechnet phi(z) mit Erklärschritten."
    )
    parser.add_argument("z", type=int, help="Die Zahl z, für die phi(z) berechnet werden soll")
    return parser.parse_args()


def main():
    args = parse_args()
    z = args.z

    if z <= 0:
        print("Bitte gib eine positive ganze Zahl z > 0 ein.")
        return

    print("=" * 72)
    print("Primfaktorzerlegung und Eulersche Phi-Funktion")
    print("=" * 72)
    print(f"Eingabe: z = {z}")
    print()

    if z == 1:
        print("1) Spezialfall")
        print("Die Zahl 1 hat keine Primfaktorzerlegung im üblichen Sinn.")
        print("Per Definition gilt: phi(1) = 1")
        return

    factors, steps = prime_factorization_steps(z)
    counter = Counter(factors)

    print("1) Primfaktorzerlegung Schritt für Schritt")
    for old, divisor, new in steps:
        print(f"{old} / {divisor} = {new}   -> Primfaktor {divisor}")
    print()

    print("2) Zusammenfassung der Primfaktorzerlegung")
    print(f"{z} = {' * '.join(map(str, factors))}")
    print(f"{z} = {format_factorization(counter)}")
    print()

    print("3) Formel für die Eulersche Phi-Funktion")
    print("Wenn z = p1^k1 * p2^k2 * ... * pr^kr, dann gilt:")
    print("phi(z) = Produkt über alle Primfaktoren p von p^(k-1) * (p-1)")
    print("Also: phi(z) = z * Produkt über alle verschiedenen Primfaktoren p von (1 - 1/p)")
    print()

    phi_value, detail_rows = phi_from_factorization(counter)

    print("4) Einsetzen der Primfaktoren")
    symbolic_parts = []
    numeric_parts = []
    for p, k, symbolic, value in detail_rows:
        symbolic_parts.append(symbolic)
        numeric_parts.append(str(value))
        print(f"Für p = {p} mit Exponent k = {k}:")
        print(f"phi({p}^{k}) = {p}^({k}-1) * ({p}-1) = {value}")
        print()

    print(f"phi({z}) = {' * '.join(symbolic_parts)}")
    print(f"phi({z}) = {' * '.join(numeric_parts)}")
    print(f"phi({z}) = {phi_value}")
    print()

    print("5) Alternative Kontrolle mit der Kurzformel")
    print(f"phi({z}) = {z}", end="")
    running_num = z
    for p in sorted(counter):
        print(f" * (1 - 1/{p})", end="")
    print()

    for p in sorted(counter):
        before = running_num
        running_num = running_num * (p - 1) // p
        print(f"Nach Primfaktor {p}: {before} * ({p}-1)/{p} = {running_num}")
    print()

    print(f"Ergebnis: phi({z}) = {phi_value}")


if __name__ == "__main__":
    main()