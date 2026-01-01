\
import numpy as np
import pandas as pd

from .thermo import y_benzene_equilibrium, ATM_MMHG
from .solver import NewtonSolver


class ColumnSpec:
    def __init__(
        self,
        n_stages=15,
        feed_stage=8,          # counting from condenser: stage 1 is top
        pressure_mmHg=ATM_MMHG,
        F=100.0,
        zF=0.5,
        q=1.0,                 # 1=sat liquid, 0=sat vapor
        D=50.0,
        reflux_ratio=2.5,
        eff_profile=None,      # list of length n_stages (Murphree vapor efficiency)
    ):
        self.n = int(n_stages)
        self.f = int(feed_stage)
        self.P = float(pressure_mmHg)
        self.F = float(F)
        self.zF = float(zF)
        self.q = float(q)
        self.D = float(D)
        self.R = float(reflux_ratio)

        if eff_profile is None:
            self.eff = np.ones(self.n) * 0.70
        else:
            self.eff = np.array(eff_profile, dtype=float)
            if self.eff.size != self.n:
                raise ValueError("eff_profile must have length n_stages")

    def flows(self):
        """
        Constant molar overflow flows for total condenser.
        Above feed: L, V
        Below feed: Ls, Vs
        """
        L = self.R * self.D
        V = (self.R + 1.0) * self.D

        Ls = L + self.q * self.F
        Vs = V + (1.0 - self.q) * self.F

        B = self.F - self.D

        return {"L": L, "V": V, "Ls": Ls, "Vs": Vs, "B": B}


class DistillationColumn:
    def __init__(self, spec: ColumnSpec):
        self.spec = spec
        self.solver = NewtonSolver(tol=1e-9, max_iter=60, fd_eps=1e-6)

    def simulate(self, x_init=None):
        n = self.spec.n
        if x_init is None:
            # simple initial guess: decreasing benzene from top to bottom
            x_guess = np.linspace(0.95, 0.05, n).clip(1e-6, 1 - 1e-6)
            xB_guess = 0.05
            x0 = np.concatenate([x_guess, [xB_guess]])
        else:
            x0 = np.array(x_init, dtype=float)

        def residual(u):
            # unknowns: x1..xN, xB
            x = u[:n].copy()
            xB = float(u[n])

            # clamp to keep stable
            x = np.clip(x, 1e-8, 1 - 1e-8)
            xB = float(np.clip(xB, 1e-8, 1 - 1e-8))

            # compute y and T from bottom to top using Murphree
            y = np.zeros(n + 2)  # y[1..n] trays, y[n+1] reboiler vapor
            T = np.zeros(n + 2)

            y[n + 1], T[n + 1] = y_benzene_equilibrium(xB, self.spec.P)

            for i in range(n, 0, -1):
                y_eq, Ti = y_benzene_equilibrium(x[i - 1], self.spec.P)
                T[i] = Ti
                Ei = float(np.clip(self.spec.eff[i - 1], 0.0, 1.0))
                y[i] = y[i + 1] + Ei * (y_eq - y[i + 1])

            xD = float(np.clip(y[1], 1e-8, 1 - 1e-8))  # total condenser: xD = y1

            fl = self.spec.flows()
            L, V, Ls, Vs, B = fl["L"], fl["V"], fl["Ls"], fl["Vs"], fl["B"]
            f = self.spec.f

            r = np.zeros(n + 1)

            # stage-by-stage benzene component balances
            for i in range(1, n + 1):
                feed = self.spec.F * self.spec.zF if i == f else 0.0

                # liquid entering from above
                if i == 1:
                    Lin = L
                    xin = xD
                else:
                    Lin = L if (i - 1) < f else Ls
                    xin = x[i - 2]

                # vapor entering from below
                if i == n:
                    Vin = Vs
                    yin = y[n + 1]
                else:
                    Vin = V if (i + 1) <= f else Vs
                    yin = y[i + 1]

                # outflows from stage i
                Lout = L if i < f else Ls
                Vout = V if i <= f else Vs

                r[i - 1] = Lin * xin + Vin * yin + feed - (Lout * x[i - 1] + Vout * y[i])

            # reboiler benzene balance
            r[n] = Ls * x[n - 1] - (B * xB + Vs * y[n + 1])

            return r

        sol, info = self.solver.solve(residual, x0)

        # build profile dataframe from converged solution
        x = np.clip(sol[:n], 1e-8, 1 - 1e-8)
        xB = float(np.clip(sol[n], 1e-8, 1 - 1e-8))

        y = np.zeros(n + 2)
        T = np.zeros(n + 2)
        y[n + 1], T[n + 1] = y_benzene_equilibrium(xB, self.spec.P)
        for i in range(n, 0, -1):
            y_eq, Ti = y_benzene_equilibrium(x[i - 1], self.spec.P)
            T[i] = Ti
            Ei = float(np.clip(self.spec.eff[i - 1], 0.0, 1.0))
            y[i] = y[i + 1] + Ei * (y_eq - y[i + 1])

        xD = float(np.clip(y[1], 1e-8, 1 - 1e-8))
        fl = self.spec.flows()

        df = pd.DataFrame({
            "stage": list(range(1, n + 1)),
            "x_bz": x,
            "y_bz": y[1:n + 1],
            "T_C": T[1:n + 1],
            "eff": self.spec.eff,
        })

        summary = {
            "converged": bool(info["converged"]),
            "iters": int(info["iters"]),
            "res_norm": float(info["res_norm"]),
            "xD_bz": float(xD),
            "xB_bz": float(xB),
            "xB_tol": float(1 - xB),
            "flows": fl,
            "spec": {
                "n_stages": self.spec.n,
                "feed_stage": self.spec.f,
                "P_mmHg": self.spec.P,
                "F": self.spec.F,
                "zF_bz": self.spec.zF,
                "q": self.spec.q,
                "D": self.spec.D,
                "R": self.spec.R,
            },
        }

        return df, summary
