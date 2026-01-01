import sys
from pathlib import Path

# Allow running this file directly: add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

\
import itertools
import pandas as pd

from distill.column import ColumnSpec
from scenarios._common import run_case


def main():
    out_dir = "outputs/scenario_C"
    rows = []

    # Feed composition variation ±10% change in benzene concentration
    for zF in [0.45, 0.50, 0.55]:
        spec = ColumnSpec(zF=zF, eff_profile=[0.70]*15)
        _, summary, _ = run_case(out_dir, f"C_zF_{zF:.2f}", spec)
        rows.append({"study": "zF", "zF": zF, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"]})

    # Feed rate changes: 80%, 100%, 120%
    for mult in [0.8, 1.0, 1.2]:
        F = 100.0 * mult
        # Keep D scaled with F for fairness (simple assumption)
        D = 50.0 * mult
        spec = ColumnSpec(F=F, D=D, eff_profile=[0.70]*15)
        _, summary, _ = run_case(out_dir, f"C_F_{int(mult*100)}pct", spec)
        rows.append({"study": "F", "F": F, "D": D, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"]})

    # Combined upsets: composition and rate together
    for zF, mult in itertools.product([0.45, 0.55], [0.8, 1.2]):
        F = 100.0 * mult
        D = 50.0 * mult
        spec = ColumnSpec(F=F, D=D, zF=zF, eff_profile=[0.70]*15)
        _, summary, _ = run_case(out_dir, f"C_comb_zF_{zF:.2f}_F_{int(mult*100)}", spec)
        rows.append({"study": "combined", "zF": zF, "F": F, "D": D, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"]})

    df = pd.DataFrame(rows)
    df.to_csv(f"{out_dir}/C_summary_table.csv", index=False)
    print("Scenario C complete. Summary table saved to outputs/scenario_C/C_summary_table.csv")


if __name__ == "__main__":
    main()