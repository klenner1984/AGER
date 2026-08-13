# AGER Blast Radius v0.1

AGER Blast Radius is an operational impact heuristic for AI agents. It is not a legal classification, risk certification or substitute for a threat model.

## Dimensions

AGER scores five dimensions from 0 to 100:

- **Financial** — ability to move, commit, approve or influence money.
- **Data** — ability to read, modify, export or delete data.
- **Communication** — ability to contact customers, staff, suppliers or the public.
- **Execution** — ability to change production systems, workflows or business state.
- **Propagation** — ability to invoke additional agents, tools, workflows or delegated identities.

## v0.1 weighting

| Dimension | Weight |
|---|---:|
| Financial | 20% |
| Data | 25% |
| Communication | 20% |
| Execution | 25% |
| Propagation | 10% |

The overall score is the weighted sum, rounded to the nearest integer.

## Input flags

For each dimension the v0.1 scanner recognizes:

- `enabled`: +20
- `external`: +20
- `write`: +25
- `unbounded`: +25
- `sensitive`: +10

Scores are capped at 100.

## Interpretation

- 0–19: low operational reach
- 20–39: limited
- 40–59: material
- 60–79: high
- 80–100: critical operational reach

These bands indicate potential blast radius, not probability of failure.

## Design goal

The score should allow an SME executive to see which agent deserves governance attention first. Future versions may separate inherent and residual blast radius and may support domain-specific calibration.
