import sys


def parse_digits(args):
    if not args:
        raise ValueError("Bitte gib die ersten 9 Ziffern der ISBN an, z.B. 3-05-501517 oder 305501517.")
    raw = "".join(args)
    digits = [ch for ch in raw if ch.isdigit()]
    if len(digits) != 9:
        raise ValueError(f"Es wurden {len(digits)} Ziffern gefunden, erwartet werden genau 9.")
    return raw, [int(d) for d in digits]


def compute_check_digit(digits):
    products = []
    total = 0
    for i, d in enumerate(digits, start=1):
        p = i * d
        products.append((i, d, p))
        total += p
    remainder = total % 11
    check = 'X' if remainder == 10 else str(remainder)
    return products, total, remainder, check


def main():
    try:
        raw, digits = parse_digits(sys.argv[1:])
        products, total, remainder, check = compute_check_digit(digits)
    except ValueError as e:
        print(f"Fehler: {e}")
        print("Verwendung: python isbn10_cli.py 3-05-501517")
        sys.exit(1)

    print("ISBN-10 Prüfziffer berechnen")
    print("=" * 30)
    print(f"Eingabe: {raw}")
    print(f"Verwendete 9 Ziffern: {' '.join(map(str, digits))}")
    print()
    print("Zwischenschritte:")
    for i, d, p in products:
        print(f"  Position {i}: {i} * {d} = {p}")
    print()
    print("Summe der gewichteten Ziffern:")
    print("  " + " + ".join(str(p) for _, _, p in products) + f" = {total}")
    print()
    q, r = divmod(total, 11)
    print("Modulo-11-Schritt:")
    print(f"  {total} = 11 * {q} + {r}")
    print(f"  Also ist c10 = {r}")
    if r == 10:
        print("  Da 10 bei ISBN-10 als X geschrieben wird, ist die Prüfziffer: X")
    print()
    print(f"Vollständige ISBN-10: {''.join(map(str, digits))}{check}")
    print(f"Prüfziffer c10: {check}")


if __name__ == '__main__':
    main()