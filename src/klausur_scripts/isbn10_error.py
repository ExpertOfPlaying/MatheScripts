import sys


def normalize_isbn(s: str):
    raw = s.strip().replace('-', '').replace(' ', '').upper()
    if len(raw) != 10:
        raise ValueError(f"ISBN-10 muss 10 Zeichen haben, erhalten: {len(raw)}")
    vals = []
    for i, ch in enumerate(raw):
        if ch == 'X':
            if i != 9:
                raise ValueError("'X' ist nur an der 10. Stelle erlaubt.")
            vals.append(10)
        elif ch.isdigit():
            vals.append(int(ch))
        else:
            raise ValueError(f"Ungültiges Zeichen: {ch}")
    return raw, vals


def fmt_vals(vals):
    out = []
    for v in vals:
        out.append('X' if v == 10 else str(v))
    return out


def checksum_details(vals):
    weights = list(range(1, 11))
    products = [w * v for w, v in zip(weights, vals)]
    total = sum(products)
    remainder = total % 11
    return weights, products, total, remainder


def print_checksum(vals, label="ISBN"):
    weights, products, total, remainder = checksum_details(vals)
    digits = fmt_vals(vals)
    print(f"\n=== Prüfsummenprüfung für {label} ===")
    print("Ziffern:", digits)
    print("Gewichte:", weights)
    parts = [f"{w}*{d}" for w, d in zip(weights, digits)]
    print("Gewichtete Summe:", " + ".join(parts))
    print("Produkte:", products)
    print("Summe =", total)
    print(f"Summe mod 11 = {remainder}")
    if remainder == 0:
        print("Ergebnis: Prüfsumme stimmt, kein Fehler erkennbar.")
    else:
        print("Ergebnis: Prüfsumme stimmt NICHT, Fehler erkannt.")


def error_vector_method(c, r):
    e = [ri - ci for ri, ci in zip(r, c)]
    weights = list(range(1, 11))
    weighted = [w * ei for w, ei in zip(weights, e)]
    total = sum(weighted)
    return e, weighted, total, total % 11


def transposition_method(c, r):
    diffs = [i for i, (ci, ri) in enumerate(zip(c, r), start=1) if ci != ri]
    if len(diffs) != 2:
        return None
    x, y = diffs
    cx, cy = c[x - 1], c[y - 1]
    rx, ry = r[x - 1], r[y - 1]
    if not (rx == cy and ry == cx):
        return None
    value = (x - y) * (cy - cx)
    return {
        'x': x,
        'y': y,
        'cx': cx,
        'cy': cy,
        'value': value,
        'mod': value % 11,
    }


def main():
    print("ISBN-10 Prüfsummen- und Fehleranalyse-Tool")
    print("Eingaben dürfen Ziffern, Bindestriche und an letzter Stelle X enthalten.")
    print()
    mode = input("Modus wählen: [1] Prüfsumme prüfen, [2] Zwei ISBNs vergleichen: ").strip()

    try:
        if mode == '1':
            s = input("ISBN-10 eingeben: ")
            raw, vals = normalize_isbn(s)
            print_checksum(vals, raw)
        elif mode == '2':
            s1 = input("Original c eingeben: ")
            s2 = input("Empfangenes/falsches r eingeben: ")
            raw_c, c = normalize_isbn(s1)
            raw_r, r = normalize_isbn(s2)

            print_checksum(c, f"c = {raw_c}")
            print_checksum(r, f"r = {raw_r}")

            print("\n=== Methode 1: Fehlervektor e = r - c ===")
            e, weighted, total, mod = error_vector_method(c, r)
            print("c =", fmt_vals(c))
            print("r =", fmt_vals(r))
            print("e = r - c =", e)
            print("Gewichte h =", list(range(1, 11)))
            print("h * e^T Beiträge =", weighted)
            print("h * e^T Summe =", total)
            print("h * e^T mod 11 =", mod)
            if mod == 0:
                print("Ergebnis: Keine Prüfsummenänderung modulo 11.")
            else:
                print("Ergebnis: Prüfsumme ändert sich modulo 11, Fehler wird erkannt.")

            print("\n=== Methode 2: Zahlendreher-Formel ===")
            trans = transposition_method(c, r)
            if trans is None:
                print("Die beiden ISBNs unterscheiden sich nicht in genau einem Zahlendreher an zwei Stellen.")
            else:
                x = trans['x']
                y = trans['y']
                cx = trans['cx']
                cy = trans['cy']
                val = trans['value']
                modv = trans['mod']
                print(f"Fehlerstellen: x = {x}, y = {y}")
                print(f"Im Original: c_x = {cx}, c_y = {cy}")
                print(f"Im Fehlerwort: r_x = {cy}, r_y = {cx}")
                print(f"Formel: (x - y) * (c_y - c_x) = ({x} - {y}) * ({cy} - {cx}) = {val}")
                print(f"Modulo 11: {val} mod 11 = {modv}")
                if modv == 0:
                    print("Ergebnis: Kein erkennbarer Fehler modulo 11.")
                else:
                    print("Ergebnis: Fehler wird erkannt.")

                print("\nVergleich beider Methoden:")
                print(f"Methode 1 ergab h*e^T mod 11 = {mod}")
                print(f"Methode 2 ergab (x-y)(c_y-c_x) mod 11 = {modv}")
        else:
            print("Ungültiger Modus. Bitte 1 oder 2 wählen.")
            sys.exit(1)
    except ValueError as e:
        print("Fehler bei der Eingabe:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()