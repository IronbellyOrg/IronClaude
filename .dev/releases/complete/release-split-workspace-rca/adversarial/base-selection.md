# Base Selection — Custom 65/35 Scoring (Root Cause / Solution)

## Scoring Method

Per user specification, default 50/50 quant/qual replaced with:
- **65% weight on Root Cause component** (likelihood, evidence quality, explanatory power)
- **35% weight on Solution component** (effectiveness, cost, alignment with proposed cause)

Each axis scored 0.0–1.0; sub-axes averaged within their component before weighting.

## Per-RCA Sub-Scores

### RCA #1 — Skill-spec / output-path

| Component | Sub-axis | Score | Reasoning |
|---|---|---|---|
| Root Cause | Likelihood | 0.10 | Author self-declared 0.95 confidence skill is NOT the cause |
| Root Cause | Evidence quality | 0.90 | Exhaustive grep + sibling-skill comparison; verifiable |
| Root Cause | Explanatory power | 0.10 | Cannot explain placement; admits skill is downstream |
| Solution | Effectiveness | 0.30 | Guard fires only on SuperClaude-skill entry path; bug used skill-creator entry path instead |
| Solution | Cost | 0.85 | Cheap (~3 small edits) |
| Solution | Alignment | 0.20 | Solution targets a non-cause; structurally weak |

- RC avg: (0.10 + 0.90 + 0.10) / 3 = **0.367**
- Sol avg: (0.30 + 0.85 + 0.20) / 3 = **0.450**
- Weighted: (0.367 × 0.65) + (0.450 × 0.35) = 0.238 + 0.158 = **0.396**

### RCA #2 — Eval harness / plugin convention

| Component | Sub-axis | Score | Reasoning |
|---|---|---|---|
| Root Cause | Likelihood | 0.95 | Smoking gun: SKILL.md L167; mechanically inevitable given skill location |
| Root Cause | Evidence quality | 0.95 | Verbatim quotes (L167/180/185/188/225-229), filename match, argparse audit |
| Root Cause | Explanatory power | 0.90 | Explains placement; honestly notes can't explain *why* skill-creator was used |
| Solution | Effectiveness | 0.80 | PreToolUse hook is only enforcement not dependent on Claude obedience |
| Solution | Cost | 0.55 | Hook needs precise pattern matching to avoid breaking legit `.claude/skills/<skill>/` writes |
| Solution | Alignment | 0.90 | Directly addresses the upstream plugin's hardcoded convention |

- RC avg: (0.95 + 0.95 + 0.90) / 3 = **0.933**
- Sol avg: (0.80 + 0.55 + 0.90) / 3 = **0.750**
- Weighted: (0.933 × 0.65) + (0.750 × 0.35) = 0.607 + 0.263 = **0.870**

### RCA #3 — Governance / naming convention

| Component | Sub-axis | Score | Reasoning |
|---|---|---|---|
| Root Cause | Likelihood | 0.55 | Real gap, but author self-flags 0.7 — explains *survival*, not *occurrence* |
| Root Cause | Evidence quality | 0.95 | Verified missing files, exact Makefile lines, exhaustive `*-workspace` inventory, broken pointers |
| Root Cause | Explanatory power | 0.65 | Explains why nothing caught it; doesn't explain initial occurrence |
| Solution | Effectiveness | 0.85 | 5-pronged (R1–R5) covers CI gap, error misdirection, gitignore gap, doc corrosion |
| Solution | Cost | 0.65 | Five separate changes; medium effort |
| Solution | Alignment | 0.95 | Tight F-finding → R-action mapping |

- RC avg: (0.55 + 0.95 + 0.65) / 3 = **0.717**
- Sol avg: (0.85 + 0.65 + 0.95) / 3 = **0.817**
- Weighted: (0.717 × 0.65) + (0.817 × 0.35) = 0.466 + 0.286 = **0.752**

## Final Ranking

| Rank | RCA | Total | Margin to Next |
|---|---|---|---|
| 1 | RCA #2 | **0.870** | +0.118 |
| 2 | RCA #3 | **0.752** | +0.356 |
| 3 | RCA #1 | **0.396** | — |

## Tiebreaker Check

Top two (RCA #2, RCA #3) margin: 0.118 = 11.8% — well above 5% threshold. **No tiebreaker needed.**

## Edge-Case-Coverage Floor

All three RCAs have explicit Limitations sections naming gaps in their analysis. All clear the 1/5 floor. **No variant disqualified.**

## Position-Bias Mitigation

Forward pass (RCA-1 → RCA-2 → RCA-3) and reverse pass (RCA-3 → RCA-2 → RCA-1) produced identical rankings: RCA #2 first, RCA #3 second, RCA #1 third. **No disagreements; no re-evaluation needed.**

## Selected Base: RCA #2

**Rationale:** RCA #2's smoking gun (skill-creator SKILL.md L167) is the highest-evidence cause attribution and mechanically explains the observed placement. Its proposed PreToolUse hook is the only enforcement layer that doesn't depend on Claude obedience to written rules. Combined RC×Sol score 0.870 leads by 11.8 percentage points.

**Strengths to preserve from base (RCA #2):**
- Smoking-gun cause attribution: skill-creator plugin SKILL.md L167
- Option D PreToolUse hook (the enforcement layer)
- Option C CLAUDE.md addendum (the documentation layer)
- Option B `make eval-skill` convenience target

**Strengths to incorporate from non-base:**

From RCA #3 (entire R1–R5 governance fix):
- R1 .dev/README.md (closes the documentation gap)
- R2 verify-sync error message correction (closes the misdirection)
- R3 CI wiring of verify-sync + lint-architecture (closes the dormant-detection gap) ← **highest priority per INV-002**
- R4 *-workspace blocklist message (suffix-attractor mitigation)
- R5 Repair broken CLAUDE.md pointers (governance corrosion)

From RCA #1 (defensive subset):
- Output-path safety gate at SKILL.md Prerequisites step 2a
- `release-split.md` Options table policy note

**Rejected from non-base:**
- RCA #1's framing of skill spec as "the cause" (author self-rejected)
- RCA #3's framing of governance as "the dominant cause" (superseded by RCA #2's smoking gun; demoted to systemic-cause role)
