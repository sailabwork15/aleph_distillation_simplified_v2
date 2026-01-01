import sys
from pathlib import Path

# Allow running this file directly: add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from distill.column import ColumnSpec
from scenarios._common import run_case


def main():
    spec = ColumnSpec(
        n_stages=15,
        feed_stage=8,
        pressure_mmHg=760.0,
        F=100.0,
        zF=0.5,
        q=1,
        D=50.0,
        reflux_ratio=2.5,
        eff_profile=[0.70]*15,
    )
    df, summary, paths = run_case("outputs", "base", spec)
    print("Base summary:", summary)
    print("Saved:", paths)


if __name__ == "__main__":
    main()