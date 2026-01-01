\
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
    Return (y_bz_eq, T_bubble) for a given liquid benzene mole fraction x_bz at pressure P.
    Bubble point is solved by Newton with a safe clamp.
    """
    x = min(max(x_bz, 1e-9), 1 - 1e-9)

    # simple guess using normal boiling points (rough)
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
            # fallback: small step
            step = -0.5 if val > 0 else 0.5
        else:
            step = -val / dfdT

        # damping / clamp
        step = max(min(step, 10.0), -10.0)
        T_new = T + step
        T_new = min(max(T_new, 40.0), 160.0)

        # if not improving, reduce step
        if abs(f(T_new)) > abs(val):
            T_new = T + 0.5 * step
            T_new = min(max(T_new, 40.0), 160.0)

        T = T_new

    y_eq = x * psat_mmHg("benzene", T) / P_mmHg
    y_eq = min(max(y_eq, 1e-9), 1 - 1e-9)
    return y_eq, T
