# Aleph Distillation Column Model (Simplified)

A small **first‑principles** benzene–toluene column model with:
- Ideal VLE (Antoine + Raoult)
- Bubble point calculation per tray
- Murphree vapor efficiency per tray
- Constant molar overflow (no enthalpy balance)
- **Newton–Raphson** nonlinear solver (finite‑difference Jacobian + damping)

Stage numbering follows the assessment: **Stage 1 is the top tray (counting from the condenser)**.
The model uses a total condenser and an equilibrium reboiler as boundary units (not counted in the 15 stages).

## Setup
```bash
pip install -r requirements.txt
```

## Run scenarios
```bash
python scenarios/scenario_base.py
python scenarios/scenario_a_equipment_deterioration.py
python scenarios/scenario_b_process_optimization.py
python scenarios/scenario_c_upset_conditions.py
```

Outputs are written to `outputs/` (CSV + JSON summary + PNG plot).

## Notes / Limitations
- Energy is reported using **boilup (V)** and **reflux (L)** as *proxies* (with constant molar overflow).
- For rigorous energy numbers, you would add enthalpy balance + latent heats (not required here).
