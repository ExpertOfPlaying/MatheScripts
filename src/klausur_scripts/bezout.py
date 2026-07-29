import sys


def euclid_steps(a: int, b: int):
    x, y = abs(a), abs(b)
    steps = []
    while y != 0:
        q, r = divmod(x, y)
        steps.append((x, y, q, r))
        x, y = y, r
    return steps, x


def extended_gcd(a: int, b: int):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t

    return old_r, old_s, old_t


def print_forward(steps):
    print("Euklidischer Algorithmus:")
    if not steps:
        print("Keine Division mit Rest nötig.")
        return
    for i, (a, b, q, r) in enumerate(steps, start=1):
        print(f"Schritt {i}: {a} = {q} * {b} + {r}")


def print_back_substitution_target(a: int, b: int, c: int, steps):
    nonzero = [s for s in steps if s[3] != 0]
    if not nonzero:
        return None

    start_index = None
    for i, (x, y, q, r) in enumerate(nonzero):
        if r == abs(c):
            start_index = i
            break

    if start_index is None:
        return None

    x, y, q, r = nonzero[start_index]

    print("\nRückwärtsrechnen mit c:")
    print(f"{r} = {x} - {q} * {y}")

    expr = {x: 1, y: -q}

    substitutions = {rem: (sx, sq, sy) for (sx, sy, sq, rem) in nonzero}
    target_value = r

    def fmt(coeffs):
        terms = []
        for val in (a, b):
            coef_val = coeffs.get(val, 0)
            if coef_val != 0:
                terms.append((coef_val, val))

        for val in sorted(k for k in coeffs if k not in (a, b) and coeffs[k] != 0):
            terms.append((coeffs[val], val))

        if not terms:
            return "0"

        out = []
        for i, (coef_term, val) in enumerate(terms):
            sign = "-" if coef_term < 0 else "+"
            mag = abs(coef_term)

            if mag == 1:
                term = f"{val}"
            else:
                term = f"{mag} * {val}"

            if i == 0:
                out.append(term if coef_term > 0 else f"- {term}")
            else:
                out.append(f" {sign} {term}")
        return "".join(out)

    changed = True
    while changed:
        changed = False
        for key in list(expr.keys()):
            if key not in (a, b) and key in substitutions and expr[key] != 0:
                coef = expr.pop(key)
                sx, sq, sy = substitutions[key]
                expr[sx] = expr.get(sx, 0) + coef
                expr[sy] = expr.get(sy, 0) - coef * sq
                print(f"{target_value} = {fmt(expr)}")
                changed = True
                break

    return expr


def solve_diophantine(a: int, b: int, c: int):
    if a == 0 and b == 0:
        if c == 0:
            return "unendlich", None
        return "keine", None

    g, x0, y0 = extended_gcd(a, b)

    if c % g != 0:
        return "keine", (g, x0, y0)

    factor = c // g
    x = x0 * factor
    y = y0 * factor
    return "eine", (g, x0, y0, x, y, factor)


def main():
    if len(sys.argv) != 4:
        print("Verwendung: python bezout_cli.py <a> <b> <c>")
        sys.exit(1)

    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        c = int(sys.argv[3])
    except ValueError:
        print("Fehler: Alle Eingaben müssen ganze Zahlen sein.")
        sys.exit(1)

    print(f"Eingabe: a = {a}, b = {b}, c = {c}")

    steps, g_forward = euclid_steps(a, b)
    print_forward(steps)
    print(f"\nErgebnis: ggT({a}, {b}) = {g_forward}")

    status, data = solve_diophantine(a, b, c)

    if status == "unendlich":
        print("\n0*x + 0*y = 0 ist für beliebige ganze x, y lösbar.")
        return

    if status == "keine":
        print(f"\nDa ggT({a}, {b}) = {data[0]} die Zahl {c} nicht teilt, gibt es keine ganzzahlige Lösung.")
        return

    g, x0, y0, x, y, factor = data

    coeffs_c = print_back_substitution_target(abs(a), abs(b), c, steps)

    if coeffs_c is not None:
        ax = coeffs_c.get(abs(a), 0)
        by = coeffs_c.get(abs(b), 0)

        if a < 0:
            ax = -ax
        if b < 0:
            by = -by

        sol_x = ax
        sol_y = by

        print("\nDarstellung von c als Linearkombination:")
        print(f"{c} = ({sol_x}) * {a} + ({sol_y}) * {b}")

        print("\nEine Lösung ist daher:")
        print(f"x = {sol_x}, y = {sol_y}")
    else:
        print("\nBézout-Darstellung des ggT:")
        print(f"{g} = ({x0}) * {a} + ({y0}) * {b}")

        print(f"\nDa {c} = {factor} * {g}, multiplizieren wir mit {factor}:")
        sol_x = x
        sol_y = y
        print(f"x = {sol_x}, y = {sol_y}")

    print(f"Probe: {a} * ({sol_x}) + {b} * ({sol_y}) = {a * sol_x + b * sol_y}")


if __name__ == "__main__":
    main()