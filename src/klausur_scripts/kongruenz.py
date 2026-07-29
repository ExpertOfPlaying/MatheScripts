import argparse


def mod_repr(n: int, m: int) -> int:
    return n % m


def check_congruence(a: int, b: int, m: int, verbose: bool = True) -> bool:
    if m == 0:
        raise ValueError("Modulo m darf nicht 0 sein.")
    modulus = abs(m)
    diff = a - b
    rem_a = mod_repr(a, modulus)
    rem_b = mod_repr(b, modulus)

    is_congruent = diff % modulus == 0

    if verbose:
        print("=== Kongruenzprüfung ===")
        print(f"Gegeben: a = {a}, b = {b}, m = {m}")
        print(f"Wir rechnen mit |m| = {modulus}, da der Modulus positiv betrachtet wird.\n")

        print("1) Definition prüfen:")
        print("   a ≡ b (mod m) genau dann, wenn m die Differenz (a - b) teilt.")
        print(f"   Also berechnen wir zuerst: a - b = {a} - {b} = {diff}\n")

        print("2) Teilbarkeitsprüfung:")
        if is_congruent:
            quotient = diff // modulus
            print(f"   {diff} = {modulus} · {quotient}")
            print(f"   Die Differenz ist also ein Vielfaches von {modulus}.")
        else:
            q, r = divmod(diff, modulus)
            print(f"   {diff} = {modulus} · {q} + {r}")
            print(f"   Die Differenz ist also KEIN Vielfaches von {modulus}.")
        print()

        print("3) Kontrolle über die Reste:")
        print(f"   a mod {modulus} = {a} mod {modulus} = {rem_a}")
        print(f"   b mod {modulus} = {b} mod {modulus} = {rem_b}")
        if rem_a == rem_b:
            print("   Beide Zahlen haben denselben Rest.")
        else:
            print("   Die Zahlen haben unterschiedliche Reste.")
        print()

        print("4) Ergebnis:")
        if is_congruent:
            print(f"   JA: {a} ≡ {b} (mod {modulus})")
        else:
            print(f"   NEIN: {a} ≢ {b} (mod {modulus})")

    return is_congruent


def interactive_mode() -> None:
    print("Kongruenz-App\n")
    try:
        a = int(input("Gib a ein: ").strip())
        b = int(input("Gib b ein: ").strip())
        m = int(input("Gib m ein (m ≠ 0): ").strip())
        print()
        check_congruence(a, b, m, verbose=True)
    except ValueError as e:
        print(f"Fehler: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prüft, ob zwei Zahlen a und b modulo m kongruent sind, und zeigt die Rechenschritte."
    )
    parser.add_argument("a", nargs="?", type=int, help="Erste Zahl")
    parser.add_argument("b", nargs="?", type=int, help="Zweite Zahl")
    parser.add_argument("m", nargs="?", type=int, help="Modulus")
    parser.add_argument("--quiet", action="store_true", help="Nur Ergebnis ohne Erklärungen ausgeben")
    args = parser.parse_args()

    if args.a is None or args.b is None or args.m is None:
        interactive_mode()
        return

    try:
        result = check_congruence(args.a, args.b, args.m, verbose=not args.quiet)
        if args.quiet:
            modulus = abs(args.m)
            print("JA" if result else "NEIN")
            print(f"{args.a} {'≡' if result else '≢'} {args.b} (mod {modulus})")
    except ValueError as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()