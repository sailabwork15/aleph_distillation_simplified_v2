import sys
from pathlib import Path

# Allow running this file directly: add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

\
import numpy as np
from distill.column import ColumnSpec
from scenarios._common import run_case


def main():
    out_dir = "outputs/scenario_A"

    # A0 Baseline 70%
    spec0 = ColumnSpec(eff_profile=[0.70]*15)
    run_case(out_dir, "A0_baseline_70pct", spec0)

    # A1 Uniform reduction to 60%
    spec1 = ColumnSpec(eff_profile=[0.60]*15)
    run_case(out_dir, "A1_uniform_60pct", spec1)

    # A2 Localized damage: trays 5-8 at 50%, others 70% (stage numbering from top)
    eff2 = [0.70]*15
    for s in range(5, 9):  # 5,6,7,8
        eff2[s-1] = 0.50
    spec2 = ColumnSpec(eff_profile=eff2)
    run_case(out_dir, "A2_local_5to8_50pct", spec2)

    # A3 Progressive: 70% (top) to 55% (bottom)
    eff3 = np.linspace(0.70, 0.55, 15).tolist()
    spec3 = ColumnSpec(eff_profile=eff3)
    run_case(out_dir, "A3_progressive_70to55", spec3)

    print("Scenario A complete. See outputs/scenario_A/")


if __name__ == "__main__":
    main()