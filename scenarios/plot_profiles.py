"""
Plotting module for distillation column composition profiles.
Plots stage number (x-axis) vs component mole fractions (y-axis).
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_composition_profile(df: pd.DataFrame, title: str = "", output_path: str = None):
    """
    Plot benzene and toluene compositions across stages.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns: stage, x_bz, y_bz, T_C, eff
    title : str
        Plot title
    output_path : str
        Path to save the plot. If None, displays but doesn't save.
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object
    ax : matplotlib.axes.Axes
        The axes object
    """
    # Calculate toluene compositions
    df_plot = df.copy()
    df_plot['x_tol'] = 1.0 - df_plot['x_bz']
    df_plot['y_tol'] = 1.0 - df_plot['y_bz']
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot compositions
    ax.plot(df_plot['stage'], df_plot['x_bz'], 'o-', label='x_bz (liquid benzene)', linewidth=2, markersize=5)
    ax.plot(df_plot['stage'], df_plot['y_bz'], 's-', label='y_bz (vapor benzene)', linewidth=2, markersize=5)
    ax.plot(df_plot['stage'], df_plot['x_tol'], '^--', label='x_tol (liquid toluene)', linewidth=2, markersize=5)
    ax.plot(df_plot['stage'], df_plot['y_tol'], 'v--', label='y_tol (vapor toluene)', linewidth=2, markersize=5)
    
    # Formatting
    ax.set_xlabel('Stage Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mole Fraction', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1])
    
    # Set x-axis to show all stages
    ax.set_xticks(df_plot['stage'].values)
    
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved: {output_path}")
    
    plt.close(fig)  # Close the figure to prevent memory buildup and GUI window display
    return fig, ax


def plot_all_profiles(case_results: list, output_dir: str = "outputs"):
    """
    Plot multiple cases for comparison.
    
    Parameters
    ----------
    case_results : list
        List of tuples: (df, summary, case_name)
    output_dir : str
        Directory to save plots
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for df, summary, case_name in case_results:
        title = f"{case_name}\nBenzene-Toluene Distillation Column"
        plot_path = output_dir / f"{case_name}_profile.png"
        plot_composition_profile(df, title=title, output_path=str(plot_path))


if __name__ == "__main__":
    # Example usage
    print("This module is meant to be imported and used in scenario files.")
