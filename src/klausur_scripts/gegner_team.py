import argparse


def residue_to_team(residue: int, modulus: int) -> int:
    return modulus if residue % modulus == 0 else residue % modulus


def opponent_of_special_team(num_teams: int, round_number: int):
    if num_teams < 2 or num_teams % 2 != 0:
        raise ValueError("Die Anzahl 2m muss gerade und mindestens 2 sein.")

    modulus = num_teams - 1
    m = num_teams // 2

    if round_number < 1 or round_number > modulus:
        raise ValueError(f"Die Runde r muss zwischen 1 und {modulus} liegen.")

    raw_product = round_number * m
    residue = raw_product % modulus
    x = residue_to_team(residue, modulus)
    return modulus, m, raw_product, residue, x


def print_solution(num_teams: int, round_number: int):
    modulus, m, raw_product, residue, x = opponent_of_special_team(num_teams, round_number)

    print("=== Gegner von Mannschaft 2m ===")
    print(f"Eingabe: 2m = {num_teams}, also m = {m}, Runde r = {round_number}")
    print(f"Modul: 2m - 1 = {modulus}\n")

    print("Gesucht: Gegen wen spielt Mannschaft 2m an Tag r?\n")

    print("Herleitung:")
    print("1) Mannschaft 2m spielt genau dann gegen x, wenn x + x ≡ r (mod 2m - 1).")
    print(f"   Also: 2·x ≡ {round_number} (mod {modulus})")
    print()

    print("2) Wir brauchen das Inverse von 2 modulo (2m - 1).")
    print(f"   Da 2m = {num_teams} ≡ 1 (mod {modulus}), gilt:")
    print(f"   2·{m} = {2*m} ≡ 1 (mod {modulus})")
    print(f"   Also ist 2^(-1) ≡ {m} (mod {modulus})")
    print()

    print("3) Beide Seiten mit m multiplizieren:")
    print("   x ≡ r·m (mod 2m - 1)")
    print(f"   x ≡ {round_number}·{m} = {raw_product} (mod {modulus})")
    print(f"   {raw_product} mod {modulus} = {residue}")
    if residue == 0:
        print(f"   Die Restklasse 0 wird durch Mannschaft {modulus} dargestellt.")
    print(f"   Also ist x = {x}")
    print()

    print("Ergebnis:")
    print(f"   Mannschaft {num_teams} spielt in Runde {round_number} gegen Mannschaft {x}.")


def print_table(num_teams: int):
    modulus = num_teams - 1
    m = num_teams // 2

    print("=== Tabelle: Gegner von Mannschaft 2m in allen Runden ===")
    print(f"2m = {num_teams}, m = {m}, Modul = {modulus}\n")

    for r in range(1, modulus + 1):
        _, _, raw_product, residue, x = opponent_of_special_team(num_teams, r)
        residue_text = str(x) if residue == 0 else str(residue)
        print(f"r = {r}: x = {r}·{m} = {raw_product} ≡ {residue_text} (mod {modulus})  ->  Gegner: {x}")


def interactive_mode():
    print("Gegner-von-2m-Rechner\n")
    try:
        num_teams = int(input("Gib 2m ein (gerade Anzahl Mannschaften): ").strip())
        mode = input("Nur eine Runde oder alle? (eine/alle): ").strip().lower()
        print()
        if mode == "alle":
            print_table(num_teams)
        else:
            round_number = int(input("Gib die Runde r ein: ").strip())
            print()
            print_solution(num_teams, round_number)
    except ValueError as e:
        print(f"Fehler: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Berechnet, gegen wen Mannschaft 2m in Runde r spielt."
    )
    parser.add_argument("teams", nargs="?", type=int, help="2m, also die gerade Anzahl Mannschaften")
    parser.add_argument("round", nargs="?", type=int, help="Runde r")
    parser.add_argument("--all", action="store_true", help="Tabelle für alle Runden ausgeben")
    args = parser.parse_args()

    if args.teams is None:
        interactive_mode()
        return

    try:
        if args.all:
            print_table(args.teams)
        else:
            if args.round is None:
                raise ValueError("Bitte eine Runde r angeben oder --all verwenden.")
            print_solution(args.teams, args.round)
    except ValueError as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()