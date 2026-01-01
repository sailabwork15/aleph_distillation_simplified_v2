\
import numpy as np


class NewtonSolver:
    """
    Small Newton–Raphson solver:
    - finite-difference Jacobian
    - damping / backtracking
    """

    def __init__(self, tol=1e-9, max_iter=40, fd_eps=1e-6):
        self.tol = tol
        self.max_iter = max_iter
        self.fd_eps = fd_eps

    def solve(self, fun, x0):
        x = np.array(x0, dtype=float)
        r = fun(x)
        rnorm = float(np.linalg.norm(r, ord=2))

        for it in range(self.max_iter):
            if rnorm < self.tol:
                return x, {"converged": True, "iters": it, "res_norm": rnorm}

            J = self._jacobian(fun, x, r)

            # Solve J dx = -r (least squares if singular)
            try:
                dx = np.linalg.solve(J, -r)
            except np.linalg.LinAlgError:
                dx = np.linalg.lstsq(J, -r, rcond=None)[0]

            # Backtracking line search
            alpha = 1.0
            x_new = x + alpha * dx
            r_new = fun(x_new)
            rnorm_new = float(np.linalg.norm(r_new, ord=2))

            while rnorm_new > rnorm and alpha > 1e-3:
                alpha *= 0.5
                x_new = x + alpha * dx
                r_new = fun(x_new)
                rnorm_new = float(np.linalg.norm(r_new, ord=2))

            x, r, rnorm = x_new, r_new, rnorm_new

        return x, {"converged": False, "iters": self.max_iter, "res_norm": rnorm}

    def _jacobian(self, fun, x, r_at_x):
        n = x.size
        J = np.zeros((n, n), dtype=float)
        eps = self.fd_eps

        for j in range(n):
            xj = x[j]
            h = eps * (abs(xj) + 1.0)

            x_f = x.copy()
            x_b = x.copy()
            x_f[j] = xj + h
            x_b[j] = xj - h

            rf = fun(x_f)
            rb = fun(x_b)
            J[:, j] = (rf - rb) / (2 * h)

        return J
