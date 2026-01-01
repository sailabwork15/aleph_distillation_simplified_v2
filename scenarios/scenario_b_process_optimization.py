import sys
from pathlib import Path

# Allow running this file directly: add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

\
import numpy as np
import pandas as pd

from distill.column import ColumnSpec
from scenarios._common import run_case


def main():
    out_dir = "outputs/scenario_B"
    rows = []

    # Reflux ratio sensitivity: 1.5 to 4.0
    for R in np.linspace(1.5, 4.0, 6):
        spec = ColumnSpec(reflux_ratio=float(R), eff_profile=[0.70]*15)
        _, summary, _ = run_case(out_dir, f"B_R_{R:.2f}", spec)
        rows.append({"study": "reflux_ratio", "R": R, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"],
                     "V_proxy": summary["flows"]["V"], "L_proxy": summary["flows"]["L"]})

    # Feed stage optimization: stages 5 to 11
    for f in range(5, 12):
        spec = ColumnSpec(feed_stage=f, eff_profile=[0.70]*15)
        _, summary, _ = run_case(out_dir, f"B_feedstage_{f}", spec)
        rows.append({"study": "feed_stage", "feed_stage": f, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"],
                     "V_proxy": summary["flows"]["V"], "L_proxy": summary["flows"]["L"]})

    # Feed condition analysis: q = 1.0, 0.5, 0.0
    for q in [1.0, 0.5, 0.0]:
        spec = ColumnSpec(q=q, eff_profile=[0.70]*15)
        _, summary, _ = run_case(out_dir, f"B_q_{q:.1f}", spec)
        rows.append({"study": "feed_q", "q": q, "xD_bz": summary["xD_bz"], "xB_tol": summary["xB_tol"],
                     "V_proxy": summary["flows"]["V"], "L_proxy": summary["flows"]["L"],
                     "Vs_proxy": summary["flows"]["Vs"], "Ls_proxy": summary["flows"]["Ls"]})

    df = pd.DataFrame(rows)
    df.to_csv(f"{out_dir}/B_summary_table.csv", index=False)
    print("Scenario B complete. Summary table saved to outputs/scenario_B/B_summary_table.csv")


if __name__ == "__main__":
    main()