\
import subprocess
import sys

SCRIPTS = [
    "scenarios/scenario_base.py",
    "scenarios/scenario_a_equipment_deterioration.py",
    "scenarios/scenario_b_process_optimization.py",
    "scenarios/scenario_c_upset_conditions.py",
]

def main():
    for s in SCRIPTS:
        print(f"\n=== Running {s} ===")
        subprocess.check_call([sys.executable, s])

if __name__ == "__main__":
    main()
