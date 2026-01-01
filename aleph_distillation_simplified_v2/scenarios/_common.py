from distill.column import ColumnSpec, DistillationColumn
from distill.io_utils import save_case_outputs
import matplotlib.pyplot as plt
import numpy as np


def run_case(out_dir, case_name, spec: ColumnSpec):
    col = DistillationColumn(spec)
    df, summary = col.simulate()
    paths = save_case_outputs(out_dir, case_name, df, summary)
    return df, summary, paths


if __name__ == "__main__":
    # Example: Run a base case and print the results
    spec = ColumnSpec(
        n_stages=15,
        feed_stage=8,
        pressure_mmHg=760.0,
        F=100.0,
        zF=0.5,
        q=1.0,
        D=50.0,
        reflux_ratio=2.5,
        eff_profile=[0.70]*15,
    )
    df, summary, paths = run_case("outputs", "base_from_common", spec)
    print("\n=== DataFrame ===")
    print(df)
    print("\n=== Summary ===")
    print(summary)
    print("\n=== Saved Paths ===")
    print(paths)
    
    # Plot T-xy diagram (Temperature vs Composition)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extract data
    x_vals = df['x_bz'].values
    y_vals = df['y_bz'].values
    T_vals = df['T_C'].values
    stages = df['stage'].values
    
    # Plot liquid composition vs temperature
    ax.plot(x_vals, T_vals, 'b-o', linewidth=2, markersize=8, label='Liquid Composition (x_bz)')
    
    # Plot vapor composition vs temperature
    ax.plot(y_vals, T_vals, 'r-s', linewidth=2, markersize=8, label='Vapor Composition (y_bz)')
    
    # Annotate stages
    for i, (x, y, T, stage) in enumerate(zip(x_vals, y_vals, T_vals, stages)):
        ax.text(x, T - 0.8, f'{int(stage)}', ha='center', fontsize=9, color='blue', fontweight='bold')
        ax.text(y, T + 0.8, f'{int(stage)}', ha='center', fontsize=9, color='red', fontweight='bold')
    
    # Highlight feed stage
    feed_stage_idx = spec.f - 1
    if 0 <= feed_stage_idx < len(x_vals):
        x_feed = x_vals[feed_stage_idx]
        y_feed = y_vals[feed_stage_idx]
        T_feed = T_vals[feed_stage_idx]
        ax.plot(x_feed, T_feed, 'b*', markersize=20, label=f'Feed Stage {spec.f} (liquid)')
        ax.plot(y_feed, T_feed, 'r*', markersize=20, label=f'Feed Stage {spec.f} (vapor)')
    
    # Formatting
    ax.set_xlabel('Composition (Benzene Mole Fraction)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_title('Distillation Column T-xy Diagram', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, loc='best')
    ax.set_xlim(-0.05, 1.05)
    
    plt.tight_layout()
    plt.savefig('outputs/txy_diagram.png', dpi=150, bbox_inches='tight')
    print("\n=== T-xy Diagram saved as: outputs/txy_diagram.png ===")
    plt.close()
