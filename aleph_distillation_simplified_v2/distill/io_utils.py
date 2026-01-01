\
import json
from pathlib import Path

import matplotlib.pyplot as plt


def ensure_dir(path: str | Path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_case_outputs(out_dir, case_name, df, summary):
    out_dir = ensure_dir(out_dir)
    csv_path = out_dir / f"{case_name}.csv"
    json_path = out_dir / f"{case_name}.json"
    png_path = out_dir / f"{case_name}_T_profile.png"

    df.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(summary, indent=2))

    # Temperature profile plot (stage 1 at top)
    plt.figure()
    plt.plot(df["stage"], df["T_C"])
    plt.gca().invert_xaxis()  # optional: show top on left, bottom on right
    plt.xlabel("Stage (1=top)")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature Profile: {case_name}")
    plt.tight_layout()
    plt.savefig(png_path, dpi=160)
    plt.close()

    return {"csv": str(csv_path), "json": str(json_path), "png": str(png_path)}
