import argparse


def residue_to_team(residue: int, modulus: int) -> int:
    return modulus if residue % modulus == 0 else residue % modulus


def compute_round(num_teams: int, round_number: int):
    modulus = num_teams - 1
    pairings = []
    seen = set()
    special_team = num_teams

    for x in range(1, modulus + 1):
        raw_subtraction = round_number - x
        raw_residue = raw_subtraction % modulus
        y = residue_to_team(raw_residue, modulus)

        info = {
            "x": x,
            "raw_subtraction": raw_subtraction,
            "raw_residue": raw_residue,
            "y": y,
            "special": False,
            "skip": False,
            "reason": ""
        }

        if x == y:
            pair = tuple(sorted((x, special_team)))
            if pair not in seen:
                seen.add(pair)
                info["special"] = True
                info["reason"] = f"x = y = {x}, also spielt {x} gegen {special_team}."
                pairings.append((x, special_team, info))
            else:
                info["skip"] = True
                info["reason"] = f"Paar {pair[0]}-{pair[1]} wurde bereits gefunden."
                pairings.append((x, special_team, info))
            continue

        pair = tuple(sorted((x, y)))
        if pair in seen:
            info["skip"] = True
            info["reason"] = f"Paar {pair[0]}-{pair[1]} wurde bereits gefunden."
            pairings.append((x, y, info))
            continue

        seen.add(pair)
        info["reason"] = f"{x} + {y} = {x + y} ≡ {round_number} (mod {modulus})"
        pairings.append((x, y, info))

    return pairings


def final_blocks(pairings):
    blocks = []
    seen = set()
    for x, y, info in pairings:
        if info["skip"]:
            continue
        pair = tuple(sorted((x, y)))
        if pair not in seen:
            seen.add(pair)
            blocks.append(pair)
    return blocks


def print_round(num_teams: int, round_number: int, detailed: bool = True):
    modulus = num_teams - 1
    pairings = compute_round(num_teams, round_number)

    print(f"=== Runde {round_number} ===")
    print(f"Regel: x + y ≡ {round_number} (mod {modulus})")
    print(f"Restklasse 0 wird durch Mannschaft {modulus} dargestellt.\n")

    if detailed:
        print("--- Berechnung pro x ---")
        for x, y, info in pairings:
            print(f"x = {info['x']}")
            print(f"  x + y ≡ {round_number} (mod {modulus})")
            print(f"  y ≡ {round_number} - {info['x']} = {info['raw_subtraction']} (mod {modulus})")
            print(f"  {info['raw_subtraction']} mod {modulus} = {info['raw_residue']}")
            if info['raw_residue'] == 0:
                print(f"  Die Restklasse 0 wird durch Mannschaft {modulus} repräsentiert, also y = {info['y']}")
            else:
                print(f"  Also y = {info['y']}")

            if info["special"]:
                print(f"  Spezialfall: {info['reason']}")
                print(f"  Block: ({info['x']}, {y})")
            elif info["skip"]:
                print(f"  Überspringen: {info['reason']}")
            else:
                print(f"  Prüfung: {info['reason']}")
                print(f"  Block: ({info['x']}, {info['y']})")
            print()

    print("--- Endgültige Blöcke der Runde ---")
    for i, block in enumerate(final_blocks(pairings), start=1):
        print(f"Block {i}: {block[0]} gegen {block[1]}")
    print()


def print_full_schedule(num_teams: int, detailed: bool = True):
    if num_teams < 2 or num_teams % 2 != 0:
        raise ValueError("Die Anzahl 2m muss gerade und mindestens 2 sein.")

    modulus = num_teams - 1
    print("=== Vollständiger Rundenturnier-Plan ===")
    print(f"Eingabe: 2m = {num_teams}")
    print(f"Es gibt {modulus} Runden, da 2m - 1 = {modulus}.\n")

    for round_number in range(1, modulus + 1):
        print_round(num_teams, round_number, detailed=detailed)


def interactive_mode():
    print("Rundenturnier-Vollplan\n")
    try:
        num_teams = int(input("Gib 2m ein (gerade Anzahl Mannschaften): ").strip())
        mode = input("Alles detailliert ausgeben? (j/n): ").strip().lower()
        print()
        print_full_schedule(num_teams, detailed=(mode != 'n'))
    except ValueError as e:
        print(f"Fehler: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Berechnet den vollständigen Rundenturnierplan für 2m Mannschaften."
    )
    parser.add_argument("teams", nargs="?", type=int, help="2m, also die gerade Anzahl Mannschaften")
    parser.add_argument("--summary", action="store_true", help="Nur die finalen Blöcke jeder Runde ausgeben")
    args = parser.parse_args()

    if args.teams is None:
        interactive_mode()
        return

    try:
        print_full_schedule(args.teams, detailed=not args.summary)
    except ValueError as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    main()