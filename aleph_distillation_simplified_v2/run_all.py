\
import subprocess
import sys
import os

SCRIPTS = [
    "scenarios/scenario_base.py",
    "scenarios/scenario_a_equipment_deterioration.py",
    "scenarios/scenario_b_process_optimization.py",
    "scenarios/scenario_c_upset_conditions.py",
]

def main():
    # Add project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root
    
    for s in SCRIPTS:
        print(f"\n=== Running {s} ===")
        subprocess.check_call([sys.executable, s], env=env)

if __name__ == "__main__":
    main()
