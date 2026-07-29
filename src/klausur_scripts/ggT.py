import sys

def gcd_steps(a: int, b: int):
    a, b = abs(a), abs(b)
    if a == 0 and b == 0:
        return [], 0
    if b > a:
        a, b = b, a
    steps = []
    while b != 0:
        q, r = divmod(a, b)
        steps.append((a, b, q, r))
        a, b = b, r
    return steps, a


def main():
    if len(sys.argv) != 3:
        print("Verwendung: python ggt_cli.py <zahl1> <zahl2>")
        sys.exit(1)

    try:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    except ValueError:
        print("Fehler: Beide Eingaben müssen ganze Zahlen sein.")
        sys.exit(1)

    steps, ggt = gcd_steps(x, y)

    print(f"Eingabe: a = {x}, b = {y}")
    print("Euklidischer Algorithmus:")

    if x == 0 and y == 0:
        print("ggT(0, 0) ist hier als 0 behandelt.")
        print("Ergebnis: 0")
        return

    if not steps:
        print("Keine Division mit Rest nötig.")
        print(f"Ergebnis: ggT({x}, {y}) = {ggt}")
        return

    for i, (a, b, q, r) in enumerate(steps, start=1):
        print(f"Schritt {i}: {a} = {q} * {b} + {r}")

    print(f"Ergebnis: ggT({x}, {y}) = {ggt}")


if __name__ == "__main__":
    main()