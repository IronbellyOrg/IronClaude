# Reusable Prompt: Adversarial Comparison of EXECUTED Pipeline Outputs (Code Audit + E2E Test Suite)

**Version:** 1.0
**Purpose:** Standardized scoring + adversarial debate of the **executed code** produced by two competing pipelines (e.g., task-builder vs Sprint CLI) for the same design specification, using a 3-tier test methodology (mocks → synthetic → real-world data) to drive the e2e dimension.
**Companion to:** `pipeline-comparison-prompt.md` (which compares the TASKLISTS that produced these code outputs). This prompt compares the **CODE** the tasklists actually produced.
**Reusable for:** Any future post-execution audit comparison; not hard-coded to `cliEval`.
**Cost envelope:** ~800K-1.4M tokens per full run (heavier than the tasklist-comparison prompt because real execution + e2e tests add substantial token + wall-clock cost).

---

## How to use this prompt

1. **Run the two pipelines to completion FIRST.** See `execution-guide.md`. Both worktrees must be in a "execution complete" state with their respective `cli/eval/` source code + `tests/cli/test_eval/` test code produced.
2. Substitute the five `{{TEMPLATE_VARIABLES}}` at the top of Section A.
3. Paste Sections A through F into a fresh Claude Code chat OPENED IN THE CANONICAL REPO (not in either worktree).
4. The receiving agent self-discovers worktree paths and executes the 7 phases.
5. Final delta verdict lands at `{{OUTPUT_DIR}}/audit-summary.md` + `audit-summary.json`.

---

# Section A — Template Variables

```
{{RELEASE_ID}}                  e.g., "cliEval"
{{WORKTREE_A_PATH}}             e.g., "../IronClaude-cliEval-A"
{{WORKTREE_B_PATH}}             e.g., "../IronClaude-cliEval-B"
{{TARGET_PACKAGE}}              e.g., "src/superclaude/cli/eval"   (what each pipeline produced)
{{TARGET_TEST_DIR}}             e.g., "tests/cli/test_eval"
{{OUTPUT_DIR}}                  e.g., ".dev/releases/current/cliEval/comparison/audit-<ISO>/"
```

If any variable is missing, `AskUserQuestion` — do not invent defaults.

---

# Section B — Objective

Compare the **executed code outputs** of Pipeline A and Pipeline B for the same design spec. The output is a delta verdict assessing not just whether each pipeline produced code, but whether that code:

- Matches the design spec (fidelity)
- Passes its own tests
- Survives 3 tiers of e2e tests (mock + synthetic + real-world data)
- Has acceptable code quality (complexity, coupling, maintainability)
- Has acceptable runtime characteristics (where measurable)
- Would pass a security audit
- Would survive a hostile reviewer

## What this audit does NOT do

- Does not re-execute either pipeline. Both pipelines must already have run.
- Does not modify either worktree's source code.
- Does not assume the tasklist quality (see `pipeline-comparison-prompt.md` for that).
- Does not adjudicate WHY a pipeline produced what it did (causal attribution is out of scope).
- Does not score the design spec (constant input to both).

## What this audit MUST produce

- Static-analysis report per pipeline (Section D rubric, 14 dimensions)
- E2E test report per pipeline (3-tier methodology, Section D §D.test)
- A `/sc:adversarial`-driven debate over the two combined audit reports
- A final delta verdict with confidence percentage

---

# Section C — Dimensions to Score (14, expanded from the tasklist rubric)

The same 12 dimensions as the tasklist-comparison prompt apply, **PLUS 2 new dimensions** specific to executed code:

| Group | Dimension | Weight | What it measures |
|---|---|---|---|
| Structural | D1. Coverage / Completeness | 1.5× | % of design-spec ACs that map to producing code |
| Structural | D2. Granularity / Module separation | 1.0× | Sub-package layout, file size, class cohesion |
| Structural | D3. Dependency clarity | 1.0× | Import graph cleanliness; circular deps; YAGNI deps |
| Structural | D4. Quality gates | 1.5× | Test coverage %, lint clean, type-check passes |
| Operational | D5. Executability | 1.5× | Can `superclaude eval doctor` actually run? Does `eval run` work? |
| Operational | D6. Fidelity to source spec | 1.5× | Every claimed feature in design-spec maps to ≥1 line of code; no phantom features |
| Operational | D7. Adaptability / Resilience | 1.0× | Error handling, retry, fail-open, graceful degradation |
| Operational | D8. Reviewability | 1.0× | Docstring/comment quality, naming, public API discoverability |
| Meta | D9. Reproducibility | 0.75× | Determinism in tests, no flakiness, no clock-dependent assertions |
| Meta | D10. Token / LOC efficiency | 0.75× | Bytes per AC; less code per dimension = better, all else equal |
| Meta | D11. Risk surface | 0.75× | Destructive ops without guards, missing rollback, weak validation |
| Meta | D12. Auditability | 1.0× | Logging, telemetry, traceability of code-→-AC provenance |
| **NEW: Runtime** | D13. E2E test pass-rate (3-tier) | 2.0× | Mock-tier % + synthetic-tier % + real-world-tier % — see §D.test below |
| **NEW: Hostile review** | D14. Security + hostile-input survival | 1.5× | Behavior under malformed input, malicious paths, race conditions, resource exhaustion |

**New weighting:** D13 carries the highest weight (2.0×) because executed code's e2e survival is the single most important signal. D14 mirrors D4's weight (1.5×) because production safety is critical.

### Per-dimension scoring rules (same as tasklist-comparison)

- 0-2 FAIL, 3-4 WEAK, 5-6 MARGINAL, 7-8 PASS, 9-10 EXCELLENT
- Each score requires ≥2 file:line evidence quotes
- Counter-evidence is mandatory (look for weaknesses even at high scores)
- Concrete recommendation to push toward 10

### Weighted aggregation (revised for 14 dimensions)

```
max_possible = Σ(10 × weight) = 14×10 max if all weights were 1.0, but with the actual weights:
             = 10×(1.5+1.0+1.0+1.5 + 1.5+1.5+1.0+1.0 + 0.75+0.75+0.75+1.0 + 2.0+1.5)
             = 10 × 15.75 = 157.5
percent_score = raw_score / 157.5 × 100
critical_score = Σ_{D1,D4,D5,D6,D13,D14} dimension_score  # 6 critical dimensions now
critical_percent = critical_score / 60 × 100
```

Grade table same as tasklist-comparison-prompt but with the broader critical set.

### Delta verdict labels (same)

A-WINS / B-WINS / HYBRID-BEATS-BOTH / TIE / BOTH-FAIL

---

# Section D — The 7-Phase Execution Plan

## Phase 0 — Worktree validation & gate

1. Verify `{{WORKTREE_A_PATH}}` and `{{WORKTREE_B_PATH}}` exist and are valid git worktrees: `git -C {{WORKTREE_X}} worktree list` for each.
2. Verify both worktrees contain the expected target package: `{{WORKTREE_X}}/{{TARGET_PACKAGE}}/` must have ≥1 Python file.
3. Verify both worktrees pass `uv run python -c "import {{python_import_path_of_target}}; print(ok)"` from inside each worktree.
4. If any of the above fail: HALT with `**Verdict:** BLOCKED — <reason>`. Do not proceed.
5. Create `{{OUTPUT_DIR}}` with these subdirectories: `static-A/`, `static-B/`, `e2e-A/`, `e2e-B/`, `adversarial-output/`, `qa/`, `final/`.

## Phase 1 — Static analysis per pipeline (2 parallel `/sc:analyze` invocations)

Hand off to `/sc:analyze` for each worktree's `{{TARGET_PACKAGE}}`. Invoke the real command (Rule 3).

**Pipeline A invocation (run inside `{{WORKTREE_A_PATH}}`):**
```
/sc:analyze {{TARGET_PACKAGE}} --focus quality,security,architecture --depth deep --format report
```
Capture to `{{OUTPUT_DIR}}/static-A/sc-analyze-report.md`.

**Pipeline B invocation (run inside `{{WORKTREE_B_PATH}}`):**
```
/sc:analyze {{TARGET_PACKAGE}} --focus quality,security,architecture --depth deep --format report
```
Capture to `{{OUTPUT_DIR}}/static-B/sc-analyze-report.md`.

Also run these external tools per pipeline (in parallel via Bash):

```bash
# Inside each worktree:
uv run ruff check {{TARGET_PACKAGE}} {{TARGET_TEST_DIR}} 2>&1 | tee {{OUTPUT_DIR}}/static-X/ruff.txt
uv run mypy {{TARGET_PACKAGE}} 2>&1 | tee {{OUTPUT_DIR}}/static-X/mypy.txt
uv run radon cc {{TARGET_PACKAGE}} -a 2>&1 | tee {{OUTPUT_DIR}}/static-X/radon-cc.txt
uv run radon mi {{TARGET_PACKAGE}} -s 2>&1 | tee {{OUTPUT_DIR}}/static-X/radon-mi.txt
git -C {{WORKTREE_X}} log --oneline ^origin/master | wc -l   # commit count for the pipeline's branch
wc -l {{TARGET_PACKAGE}}/**/*.py {{TARGET_TEST_DIR}}/**/*.py  # LOC totals
```

These produce the raw inputs for D4 (Quality gates) and D14 (Security).

## Phase 2 — 3-Tier E2E Test Execution per pipeline (parallel)

This is the **most important phase** — it produces the D13 signal (weight 2.0×). Three tiers per pipeline, all required:

### §D.test — 3-Tier methodology

**Tier 1: Mock data tests** — `uv run pytest {{TARGET_TEST_DIR}} -v --tb=short`

These are the pipeline's own pytest tests. They use mocks/fixtures, do NOT spawn real subprocesses, and validate harness internals. Capture output, pass-rate, and any failed test names.

```bash
cd {{WORKTREE_X}}
uv run pytest {{TARGET_TEST_DIR}} -v --tb=short 2>&1 | tee {{OUTPUT_DIR}}/e2e-X/tier1-mock.txt
echo "EXIT=$?" >> {{OUTPUT_DIR}}/e2e-X/tier1-mock.txt
```

**Tier 2: Synthetic-data tests** — exercise the harness against a STUB eval suite (e.g., `cli/eval/suites/stub.yaml` if the design-spec called for it). Synthetic = real subprocess + real PTY but fake eval bodies that do not require live MCP servers or 30-minute clock waits.

```bash
cd {{WORKTREE_X}}
# Discover the stub suite the pipeline produced; expect path: {{TARGET_PACKAGE}}/suites/stub.yaml
uv run superclaude eval run --suite stub --output {{OUTPUT_DIR}}/e2e-X/tier2-synthetic-run/ 2>&1 | \
  tee {{OUTPUT_DIR}}/e2e-X/tier2-synthetic.txt
echo "EXIT=$?" >> {{OUTPUT_DIR}}/e2e-X/tier2-synthetic.txt
```

If the pipeline did not produce a stub suite, the receiving agent must construct a minimal 1-eval stub on the fly (see Appendix A below for the canonical stub template) and run it.

**Tier 3: Real-world data tests** — exercise the harness against a SUBSET of the real eval suite. For `cliEval`, that means running 3 selected real evals from the 15 (e.g., E1 sticky lifecycle, E3 freshness gate, E7 clean install) — the ones whose execution does NOT require >5 min wall-clock and DOES not require live MCP servers (gate via `--no-mcp` flag if appropriate).

```bash
cd {{WORKTREE_X}}
uv run superclaude eval run --suite real --eval E1,E3,E7 --no-mcp \
  --output {{OUTPUT_DIR}}/e2e-X/tier3-real-run/ 2>&1 | \
  tee {{OUTPUT_DIR}}/e2e-X/tier3-real.txt
echo "EXIT=$?" >> {{OUTPUT_DIR}}/e2e-X/tier3-real.txt
```

If the pipeline did not implement enough of the 15 evals to run any of {E1, E3, E7}, record this as a critical gap and assign Tier-3 score = 0 for that pipeline.

### Tier scoring formula

```
tier1_pct = passed / total × 100 from pytest output
tier2_pct = (1 if exit=0 else 0) × 100   # stub eval is binary
tier3_pct = passed_evals / 3 × 100        # out of the 3 selected real evals

D13_score = round((tier1_pct × 0.4 + tier2_pct × 0.2 + tier3_pct × 0.4) / 10)
           # tier 1 + tier 3 dominate (40% each); tier 2 is connective tissue (20%)
```

Tier 1's weight is high because it represents the pipeline's own QA discipline; Tier 3's weight matches it because real execution survival is the ultimate signal.

### Parallelism

Pipeline A's 3 tiers run sequentially WITHIN A — but Pipeline A and Pipeline B run in PARALLEL (two `Agent` calls). Inside each pipeline, the 3 tiers cannot run in parallel because Tier 2 and Tier 3 share state (per-eval HOMEs go through the same machinery).

## Phase 3 — Parallel rubric scoring (6 agents × 14 dimensions = same fan-out as tasklist comparison, but expanded)

Six `general-purpose` agents in one message. Per pipeline, 3 agents covering different dimension groups, now including D13/D14:

| Agent ID | Pipeline | Dimensions | Output |
|---|---|---|---|
| A-1 | A | D1, D2, D3, D4 | `{{OUTPUT_DIR}}/scores/A-structural.yaml` |
| A-2 | A | D5, D6, D7, D8 | `{{OUTPUT_DIR}}/scores/A-operational.yaml` |
| A-3 | A | D9, D10, D11, D12, **D13, D14** | `{{OUTPUT_DIR}}/scores/A-meta-runtime.yaml` |
| B-1 | B | D1, D2, D3, D4 | `{{OUTPUT_DIR}}/scores/B-structural.yaml` |
| B-2 | B | D5, D6, D7, D8 | `{{OUTPUT_DIR}}/scores/B-operational.yaml` |
| B-3 | B | D9, D10, D11, D12, **D13, D14** | `{{OUTPUT_DIR}}/scores/B-meta-runtime.yaml` |

**Note:** A-3 / B-3 each cover 6 dimensions (heavier load) because D13 + D14 are runtime-oriented and require reading Phase 2 test outputs. The 6th-dimension load is justified.

Each agent receives the Phase 1 static-analysis report + Phase 2 e2e-test outputs for ITS pipeline only. Pipeline isolation rule: A-agents cannot read Pipeline B's outputs (same anti-cheating rule as tasklist comparison).

## Phase 4 — Aggregation (per pipeline)

Two aggregators (parallel). Identical to tasklist-comparison Phase 3 logic, but adapted for 14 dimensions and the revised max_possible (157.5) + critical_score (60). Output: `score-A.md`, `score-B.md`, `score-A.json`, `score-B.json`.

## Phase 5 — Adversarial debate (hand-off to `/sc:adversarial`)

Same hand-off pattern as tasklist-comparison. Verified invocation (every flag traces to `src/superclaude/commands/adversarial.md`):

```
/sc:adversarial --compare {{OUTPUT_DIR}}/scores/score-A.md,{{OUTPUT_DIR}}/scores/score-B.md \
                --depth deep \
                --focus completeness,executability,fidelity,e2e-survival,security \
                --output {{OUTPUT_DIR}}/adversarial-output/ \
                --convergence 0.85 \
                --auto-stop-plateau
```

The `--focus` list includes `e2e-survival` and `security` — both are verified-acceptable values (the adversarial protocol accepts arbitrary focus area names; only the FLAGS themselves are verified against the table).

**Rule 3 compliance:** Do not reimplement the 5-step debate protocol. The 6 protocol artifacts (diff-analysis.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, merged output) are produced by `/sc:adversarial` itself.

## Phase 6 — `rf-qa-qualitative` verification of adversarial output

Identical to tasklist-comparison Phase 5. Spawn `rf-qa-qualitative` to verify the adversarial output's claims trace to evidence in `score-A.md` / `score-B.md`. Output: `{{OUTPUT_DIR}}/qa/adversarial-qa-report.md`.

## Phase 7 — Final synthesis & delta verdict

Same as tasklist-comparison Phase 6, but:
- 14 dimensions in the per-dimension delta table (instead of 12)
- Critical-percent denominator is 60 (instead of 40)
- The "Top 5 dimensions driving the delta" section MUST include D13 if D13 was a deciding factor (it usually will be)
- A new section: **"Real-world execution survival"** — summarizes the 3-tier test results per pipeline, calls out tier-3 failures by eval ID
- A new section: **"Production-readiness verdict"** — explicit GO / GO-WITH-FIXES / NO-GO recommendation for shipping the pipeline's output to master

Output files:
- `{{OUTPUT_DIR}}/final/audit-summary.md`
- `{{OUTPUT_DIR}}/final/audit-summary.json`
- `{{OUTPUT_DIR}}/final/production-readiness.md` (explicit ship/no-ship recommendation)

---

# Section E — Pass/Fail criteria for the audit itself

The audit PASSES (verdict is trustworthy) when ALL hold:

- [ ] Phase 0 gate cleared (both worktrees valid, target package present, importable)
- [ ] All 3 tiers ran for both pipelines (tier-2 / tier-3 may have failed; that's a finding, not a gate)
- [ ] All 6 Phase-3 agents produced valid score fragments with file:line evidence
- [ ] `/sc:adversarial` produced all 6 expected artifacts
- [ ] `rf-qa-qualitative` PASS (or disclosed FAIL in confidence)
- [ ] Final confidence ≥ 65% (higher bar than tasklist-comparison's 60% because real code is on the line)

The audit FAILS (verdict NOT trustworthy) when ANY hold:

- Either pipeline could not be imported (the code is broken on day 0 — a finding but trumps comparison)
- A Phase-3 agent fabricated test results (cited a pytest line that doesn't exist)
- D13 or D14 was scored without exercising Phase 2 outputs (audit-of-audit fail)
- `/sc:adversarial` did not converge after 3 rounds AND no plateau-stop engaged
- `rf-qa-qualitative` FAIL persisted after 1 retry

On audit-fails: `**Verdict:** UNRELIABLE — see <reason>`.

---

# Section F — Special cases

## Case 1: One pipeline produced NOTHING

If Pipeline B's execution failed catastrophically (e.g., `superclaude sprint` aborted on Phase 1 and never produced `cli/eval/`), the audit MUST still produce a verdict. Mark Pipeline B's scores as `0` for D1-D6 (incomplete output) and `N/A` for D7-D14 (cannot evaluate). Verdict: **A-WINS by forfeit**, with a separate section titled "Pipeline B execution failure" describing the root cause.

## Case 2: Both pipelines produced functionally identical code (high overlap)

If `diff --recursive` between the two `{{TARGET_PACKAGE}}/` trees shows >90% line overlap, mark `TIE` early and switch the audit focus to: which pipeline's PROCESS produced this result more efficiently (LOC of artifacts, wall-clock, token spend). This becomes a process-comparison rather than artifact-comparison.

## Case 3: One pipeline produced a HYBRID that includes the other's signatures

If Pipeline A's code obviously copy-pasted Pipeline B's structure (or vice versa, e.g., the executing agent peeked at the sibling worktree), this is a process violation. Flag it explicitly in `audit-summary.md` under "Process integrity findings." The verdict still stands on artifact quality, but the recommendation section must note that the pipelines' independence was compromised.

## Case 4: Real-world data tier (Tier 3) requires live MCP servers and they are unavailable

Run Tier 3 with `--no-mcp` and select 3 evals from the 15 that do NOT require MCP (likely E11, E13, E15 for cliEval). Document in `tier3-real.txt` the skip reason. The Tier-3 score reflects what was actually run; the audit summary's "Open Questions" section notes that MCP-dependent evals were not tested.

---

# Appendix A — Canonical 1-eval stub (when pipeline produced none)

If the pipeline's harness has no `suites/stub.yaml`, the receiving agent constructs one at `{{WORKTREE_X}}/{{TARGET_PACKAGE}}/suites/stub-audit.yaml` for Tier-2 testing:

```yaml
name: stub-audit
version: "1.0"
description: "Audit-time stub eval — proves the harness can spawn-and-observe a real Claude Code subprocess"

defaults:
  per_eval_timeout_sec: 60
  capture_tty: true

required_binaries:
  - { name: claude, failure_mode: hard }
  - { name: make,   failure_mode: hard }
  - { name: jq,     failure_mode: hard }

evals:
  - id: STUB_AUDIT_E1
    title: "Spawn claude, send /help, expect command list"
    category: smoke
    timeout_sec: 60
    isolation:
      home_strategy: ephemeral
    inputs:
      - prompt: "/help"
    expects:
      - { type: exit_code, value: 0 }
      - { type: stdout_contains, pattern: "Available Commands" }
```

If the harness's manifest schema doesn't accept these exact field names, the receiving agent must adapt — the spirit is "smallest possible eval that proves the spawn-and-observe loop works."

---

# Appendix B — Confidence calculation (refined for executed-code audit)

```
base = 1.00
- 0.10 if Phase 6 QA verdict was FAIL after 1 retry
- 0.05 per dimension where score divergence > 4 points (no inter-agent agreement)
- 0.10 if /sc:adversarial convergence_score < 0.70
- 0.05 if total_acs_in_spec < 5 (small sample)
- 0.10 if Tier 3 was skipped entirely (real-world signal absent)
- 0.05 if 1+ Phase-3 agent's evidence quote failed integrity check (citation mismatch)
- 0.10 if both pipelines scored < 50% (no useful signal between two failures)
- 0.05 if production-readiness for either pipeline = NO-GO (the comparison is moot)

confidence = max(50, round(base × 100))
```

Floor at 50%; the audit must produce SOMETHING actionable even in degraded states. Anything below 60% → the verdict label MUST include "(LOW CONFIDENCE)".

---

# Appendix C — Authoring provenance

- **Companion to:** `pipeline-comparison-prompt.md` (this is the executed-code variant)
- **Verified commands:** `/sc:adversarial` (same 15 flags), `/sc:analyze` (same 3 flags), plus external `uv run pytest`/`ruff`/`mypy`/`radon` (built-ins, no verification required)
- **Rule compliance:**
  - Rule 1: every `/sc:adversarial` and `/sc:analyze` flag traces to verified flag tables
  - Rule 2: no ghost commands (rejected: there is no `/sc:audit-code` — used `/sc:analyze` instead)
  - Rule 3: `/sc:adversarial` invoked, not reimplemented; the 3-tier methodology is OURS, not a target's protocol
- **Date authored:** 2026-05-18
- **Reusability:** Any future post-execution pipeline comparison via template-variable substitution.
