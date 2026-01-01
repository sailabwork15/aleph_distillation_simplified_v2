import sys
from pathlib import Path

# Allow running this file directly: add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Set matplotlib to use non-interactive backend before any plotting
import matplotlib
matplotlib.use('Agg')

import itertools
import pandas as pd

from distill.column import ColumnSpec
from scenarios._common import run_case
from scenarios.plot_profiles import plot_composition_profile


def main():
    out_dir = "outputs/scenario_C"
    rows = []

    # Feed composition variation ±10% change in benzene concentration
    for zF in [0.45, 0.50, 0.55]:
        spec = ColumnSpec(zF=zF, eff_profile=[0.70]*15)
        df, summary, _ = run_case(out_dir, f"C_zF_{zF:.2f}", spec)
        plot_composition_profile(df, title=f"C: Feed Composition zF = {zF:.2f}", 
                                output_path=f"{out_dir}/C_zF_{zF:.2f}_profile.png")
        rows.append({"study": "zF", "zF": zF, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"]})

    # Feed rate changes: 80%, 100%, 120%
    for mult in [0.8, 1.0, 1.2]:
        F = 100.0 * mult
        # Keep D scaled with F for fairness (simple assumption)
        D = 50.0 * mult
        spec = ColumnSpec(F=F, D=D, eff_profile=[0.70]*15)
        df, summary, _ = run_case(out_dir, f"C_F_{int(mult*100)}pct", spec)
        plot_composition_profile(df, title=f"C: Feed Rate F = {F:.1f} kmol/h ({int(mult*100)}%)", 
                                output_path=f"{out_dir}/C_F_{int(mult*100)}pct_profile.png")
        rows.append({"study": "F", "F": F, "D": D, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"]})

    # Combined upsets: composition and rate together
    for zF, mult in itertools.product([0.45, 0.55], [0.8, 1.2]):
        F = 100.0 * mult
        D = 50.0 * mult
        spec = ColumnSpec(F=F, D=D, zF=zF, eff_profile=[0.70]*15)
        df, summary, _ = run_case(out_dir, f"C_comb_zF_{zF:.2f}_F_{int(mult*100)}", spec)
        plot_composition_profile(df, title=f"C: Combined (zF={zF:.2f}, F={int(mult*100)}%)", 
                                output_path=f"{out_dir}/C_comb_zF_{zF:.2f}_F_{int(mult*100)}_profile.png")
        rows.append({"study": "combined", "zF": zF, "F": F, "D": D, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"]})

    df = pd.DataFrame(rows)
    df.to_csv(f"{out_dir}/C_summary_table.csv", index=False)
    print("Scenario C complete. Summary table saved to outputs/scenario_C/C_summary_table.csv")
    print("Composition profiles saved for all cases")


if __name__ == "__main__":
    main()