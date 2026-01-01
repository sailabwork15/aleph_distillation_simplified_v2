import sys
from pathlib import Path

# Allow running this file directly: add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Set matplotlib to use non-interactive backend before any plotting
import matplotlib
matplotlib.use('Agg')

import numpy as np
from distill.column import ColumnSpec
from scenarios._common import run_case
from scenarios.plot_profiles import plot_composition_profile


def main():
    out_dir = "outputs/scenario_A"

    # A0 Baseline 70%
    spec0 = ColumnSpec(eff_profile=[0.70]*15)
    df0, summary0, _ = run_case(out_dir, "A0_baseline_70pct", spec0)
    plot_composition_profile(df0, title="A0: Baseline (70% Efficiency)", 
                            output_path=f"{out_dir}/A0_baseline_70pct_profile.png")

    # A1 Uniform reduction to 60%
    spec1 = ColumnSpec(eff_profile=[0.60]*15)
    df1, summary1, _ = run_case(out_dir, "A1_uniform_60pct", spec1)
    plot_composition_profile(df1, title="A1: Uniform Reduction (60% Efficiency)", 
                            output_path=f"{out_dir}/A1_uniform_60pct_profile.png")

    # A2 Localized damage: trays 5-8 at 50%, others 70% (stage numbering from top)
    eff2 = [0.70]*15
    for s in range(5, 9):  # 5,6,7,8
        eff2[s-1] = 0.50
    spec2 = ColumnSpec(eff_profile=eff2)
    df2, summary2, _ = run_case(out_dir, "A2_local_5to8_50pct", spec2)
    plot_composition_profile(df2, title="A2: Localized Damage (Stages 5-8, 50% Efficiency)", 
                            output_path=f"{out_dir}/A2_local_5to8_50pct_profile.png")

    # A3 Progressive: 70% (top) to 55% (bottom)
    eff3 = np.linspace(0.70, 0.55, 15).tolist()
    spec3 = ColumnSpec(eff_profile=eff3)
    df3, summary3, _ = run_case(out_dir, "A3_progressive_70to55", spec3)
    plot_composition_profile(df3, title="A3: Progressive Degradation (70% top to 55% bottom)", 
                            output_path=f"{out_dir}/A3_progressive_70to55_profile.png")

    print("Scenario A complete. See outputs/scenario_A/")
    print("Plots saved for all cases (A0-A3)")


if __name__ == "__main__":
    main()