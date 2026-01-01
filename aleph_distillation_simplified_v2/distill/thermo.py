import math

# Antoine coefficients (P in mmHg, T in °C): log10(P) = A - B/(C+T)
ANTOINE = {
    "benzene": (6.90565, 1211.033, 220.79),
    "toluene": (6.95334, 1343.943, 219.377),
}

ATM_MMHG = 760.0


def psat_mmHg(component: str, T_C: float) -> float:
    A, B, C = ANTOINE[component]
    return 10 ** (A - B / (C + T_C))


def y_benzene_equilibrium(x_bz: float, P_mmHg: float) -> tuple[float, float]:
    """
    Bubble-point calculation (given liquid x_bz):
    Solves: x*Psat_bz(T) + (1-x)*Psat_tol(T) = P
    Returns (y_bz_eq, T_bubble).
    """
    x = min(max(x_bz, 1e-9), 1 - 1e-9)

    # rough temperature guess using normal boiling points
    T = x * 80.1 + (1 - x) * 110.6

    def f(Tc: float) -> float:
        return x * psat_mmHg("benzene", Tc) + (1 - x) * psat_mmHg("toluene", Tc) - P_mmHg

    # Newton with finite-difference derivative + damping
    for _ in range(60):
        val = f(T)
        if abs(val) < 1e-8:
            break

        h = 1e-3 * (abs(T) + 1.0)
        dfdT = (f(T + h) - f(T - h)) / (2 * h)

        if abs(dfdT) < 1e-10:
            step = -0.5 if val > 0 else 0.5
        else:
            step = -val / dfdT

        step = max(min(step, 10.0), -10.0)
        T_new = min(max(T + step, 40.0), 160.0)

        if abs(f(T_new)) > abs(val):
            T_new = min(max(T + 0.5 * step, 40.0), 160.0)

        T = T_new

    y_eq = x * psat_mmHg("benzene", T) / P_mmHg
    y_eq = min(max(y_eq, 1e-9), 1 - 1e-9)
    return y_eq, T


def x_benzene_from_y_dewpoint(y_bz: float, P_mmHg: float) -> tuple[float, float]:
    """
    Dew-point calculation (given vapor y_bz):
    Solves: y_bz * P/Psat_bz(T) + (1-y_bz) * P/Psat_tol(T) = 1
    Returns (x_bz_eq, T_dew).
    """
    y = min(max(y_bz, 1e-9), 1 - 1e-9)

    # rough guess between component normal boiling points
    T = y * 80.1 + (1 - y) * 110.6

    def g(Tc: float) -> float:
        Pb = psat_mmHg("benzene", Tc)
        Pt = psat_mmHg("toluene", Tc)
        return y * (P_mmHg / Pb) + (1 - y) * (P_mmHg / Pt) - 1.0

    for _ in range(60):
        val = g(T)
        if abs(val) < 1e-8:
            break

        h = 1e-3 * (abs(T) + 1.0)
        dgdT = (g(T + h) - g(T - h)) / (2 * h)

        if abs(dgdT) < 1e-10:
            step = -0.5 if val > 0 else 0.5
        else:
            step = -val / dgdT

        step = max(min(step, 10.0), -10.0)
        T_new = min(max(T + step, 40.0), 160.0)

        if abs(g(T_new)) > abs(val):
            T_new = min(max(T + 0.5 * step, 40.0), 160.0)

        T = T_new

    # Once T_dew is found, compute x from x_i = y_i * P / Psat_i(T), then normalize
    Pb = psat_mmHg("benzene", T)
    Pt = psat_mmHg("toluene", T)

    x_b = y * (P_mmHg / Pb)
    x_t = (1 - y) * (P_mmHg / Pt)
    s = x_b + x_t

    if s <= 0:
        x_eq = 0.5
    else:
        x_eq = x_b / s

    x_eq = min(max(x_eq, 1e-9), 1 - 1e-9)
    return x_eq, T
