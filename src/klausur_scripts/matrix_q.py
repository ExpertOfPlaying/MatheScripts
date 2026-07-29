import argparse
from typing import List


def q_matrix(q: int) -> List[List[int]]:
    return [[q, 1], [1, 0]]


def mat_mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]


def mat_vec_mul(a: List[List[int]], v: List[int]) -> List[int]:
    return [a[0][0] * v[0] + a[0][1] * v[1], a[1][0] * v[0] + a[1][1] * v[1]]


def mat_det(a: List[List[int]]) -> int:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def mat_inv_2x2(a: List[List[int]]) -> List[List[int]]:
    det = mat_det(a)
    if det not in (1, -1):
        raise ValueError(f"Inverse is not integral because det(Q) = {det}.")
    return [
        [a[1][1] * det, -a[0][1] * det],
        [-a[1][0] * det, a[0][0] * det],
    ]


def format_matrix(m: List[List[int]]) -> str:
    return f"[[{m[0][0]:>6}, {m[0][1]:>6}],\n [{m[1][0]:>6}, {m[1][1]:>6}]]"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Berechnet die Matrix-Q-Methode für den erweiterten euklidischen Algorithmus. "
            "Gib die Quotienten/Reste-Schritte als q-Werte ein."
        )
    )
    parser.add_argument(
        "quotients",
        metavar="q",
        type=int,
        nargs="+",
        help="Quotienten q1 q2 ... qk aus dem euklidischen Algorithmus",
    )
    parser.add_argument(
        "--gcd",
        type=int,
        default=1,
        help="ggT d; standardmäßig 1. Für das Beispiel 2406 und 654 ist d=6.",
    )
    parser.add_argument(
        "--target",
        type=int,
        default=None,
        help="Optionales Ziel c für ax + by = c. Falls c ein Vielfaches von d ist, wird skaliert.",
    )
    parser.add_argument(
        "--ab",
        metavar=("a", "b"),
        type=int,
        nargs=2,
        default=None,
        help="Optional: Originalzahlen a b zum direkten Prüfen der Bézout-Koeffizienten.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    qs = args.quotients
    d = args.gcd

    print("=" * 72)
    print("Matrix-Q-Methode für Bézout-Koeffizienten")
    print("=" * 72)
    print(f"Eingegebene Quotienten: {qs}")
    print(f"Verwendeter ggT d = {d}")
    print()

    q_mats = [q_matrix(q) for q in qs]
    Q = [[1, 0], [0, 1]]

    print("1) Einzelne Q-Matrizen")
    for i, (q, m) in enumerate(zip(qs, q_mats), start=1):
        print(f"Q_{i} für q_{i} = {q}:")
        print(format_matrix(m))
        print()

    print("2) Sukzessives Ausmultiplizieren")
    for i, m in enumerate(q_mats, start=1):
        old = Q
        Q = mat_mul(Q, m)
        print(f"Schritt {i}: Q_bis_{i} = Q_bis_{i-1} * Q_{i}")
        print("Vorher:")
        print(format_matrix(old))
        print("Mal:")
        print(format_matrix(m))
        print("Ergibt:")
        print(format_matrix(Q))
        print()

    print("3) Gesamte Matrix Q")
    print(format_matrix(Q))
    print(f"det(Q) = {mat_det(Q)}")
    print()

    Q_inv = mat_inv_2x2(Q)
    print("4) Inverse Matrix Q^{-1}")
    print(format_matrix(Q_inv))
    print()

    vec_d0 = [d, 0]
    ab_from_q = mat_vec_mul(Q, vec_d0)
    print("5) Aus Q * (d, 0)^T erhält man (a, b)^T")
    print(f"Q * ({d}, 0)^T = ({ab_from_q[0]}, {ab_from_q[1]})^T")
    print("Also sind:")
    print(f"a = {ab_from_q[0]}")
    print(f"b = {ab_from_q[1]}")
    print()

    a, b = ab_from_q
    x0, y0 = Q_inv[0]
    print("6) Bézout-Koeffizienten aus der ersten Zeile von Q^{-1}")
    print(f"x0 = {x0}, y0 = {y0}")
    print(f"Prüfung: {a}*({x0}) + {b}*({y0}) = {a * x0 + b * y0}")
    print()

    print("7) Allgemeine Lösung für ax + by = d")
    print(f"x = {x0} + k*({b // d})")
    print(f"y = {y0} - k*({a // d})")
    print("für k ∈ Z")
    print()

    if args.target is not None:
        c = args.target
        print("8) Skalierung auf ax + by = c")
        if c % d != 0:
            print(f"Keine Lösung, weil {c} kein Vielfaches von d = {d} ist.")
        else:
            factor = c // d
            xs = x0 * factor
            ys = y0 * factor
            print(f"Faktor = c / d = {c} / {d} = {factor}")
            print(f"Spezielle Lösung: x = {xs}, y = {ys}")
            print(f"Prüfung: {a}*({xs}) + {b}*({ys}) = {a * xs + b * ys}")
        print()

    if args.ab is not None:
        ain, bin_ = args.ab
        print("9) Vergleich mit explizit eingegebenem (a, b)")
        print(f"Eingabe: a = {ain}, b = {bin_}")
        if (ain, bin_) == (a, b):
            print("Die aus Q rekonstruierte Zahl stimmt mit der Eingabe überein.")
            print(f"Direkte Prüfung: {x0}*{ain} + ({y0})*{bin_} = {x0 * ain + y0 * bin_}")
        else:
            print("Achtung: Die aus den Quotienten rekonstruierte Zahl ist anders als die Eingabe.")
            print(f"Aus Q folgt nämlich (a, b) = ({a}, {b}).")
        print()


if __name__ == "__main__":
    main()