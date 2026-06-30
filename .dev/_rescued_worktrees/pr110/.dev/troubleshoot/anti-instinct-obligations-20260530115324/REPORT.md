---
status: success
tier_reached: 1
confidence: 0.95
escalation_reason: none
hypothesis_count: 1
adversarial_invoked: false
fix_authorized: false
behavior_is_documented: false
test_is_wrong: false
---

# Troubleshoot Report: anti-instinct halt on `no_undischarged_obligations`

## Summary

The roadmap pipeline halted at the `anti-instinct` step with 4 undischarged "stub" obligations in M4. **The 4 findings are false positives produced by a stale pipx-installed scanner.** The scanner fixes that eliminate exactly these cases — Fix 1 (tail-section termination), Fix 3 (descriptor-noun demotion), and Layer 5 (H3 subsection-context) — are committed on the current branch `feat/roadmap-scanner-layer-5-h3-subsection` but were never re-installed into the pipx environment that the `superclaude` CLI actually executes. The pipeline run at 2026-05-30T06:58Z used the pre-fix scanner snapshot.

## Diagnosis

Two simultaneous conditions produced the failure:

1. **Stale pipx install (load-bearing).** The `superclaude` CLI is installed via `pipx install --force ~/workspace/IronClaude` and runs from `/config/.local/share/pipx/venvs/superclaude/.../site-packages/superclaude/cli/roadmap/obligation_scanner.py`. That site-packages copy has **`has_tail: False`, `has_desc: False`** — it predates today's three scanner commits. Editing the source tree does not propagate to the CLI without a re-install.

2. **The fix is real and would catch these 4 cases.** Fix 1's `_find_tail_section_start()` cuts each milestone section at the first template-tail H2 (`Resource Requirements and Dependencies`, `Risk Register`, `Timeline Estimates`, etc., defined in `gates._REQUIRED_H2_SECTIONS`). The 4 reported lines all sit inside those tail sections, downstream of `## M4:` (line 321). With the fix, they would not be attributed to any milestone and never produce an obligation.

| Reported line | Containing tail H2 | Scaffold text | Status with fix |
|---|---|---|---|
| 393 | Resource Requirements and Dependencies (line 380) | "stub transport for tests" | Not scanned (out of milestone) |
| 413 | Risk Register (line 406) | "benchmark with stub fault injection" | Not scanned |
| 420 | Risk Register (line 406) | "N=8 stub workers" | Not scanned |
| 466 | Timeline Estimates (line 462) | "transport Protocol + stub" | Not scanned |

The component tags emitted by the audit (`/`, `fault`, `workers`, `protocol`) confirm these are descriptive prose in mitigation/dependency/timeline cells, not prescriptive scaffolds.

## Evidence

- Failing audit: `.dev/releases/Current/MultiModelSwarm/anti-instinct-audit.md:2` declares `undischarged_obligations: 4`, then enumerates the four M4 lines at lines 21–24.
- Gate definition: `src/superclaude/cli/roadmap/gates.py:317` defines `_no_undischarged_obligations()`; it fails closed unless frontmatter parses to integer 0.
- Tail-section helper (HEAD): `src/superclaude/cli/roadmap/obligation_scanner.py:419` defines `_find_tail_section_start()`; integration at `_split_into_phases()` line 471 cuts `end = min(next_milestone_end, tail_section_start)`.
- Tail H2 set: `src/superclaude/cli/roadmap/gates.py:891` declares `_REQUIRED_H2_SECTIONS` containing `resource requirements and dependencies`, `risk register`, `timeline estimates` — matches all 4 flagged H2 contexts.
- Pipx snapshot lacks fixes: `python -c "import superclaude.cli.roadmap.obligation_scanner as s; print(hasattr(s, '_find_tail_section_start'))"` → `False` (executed against `/config/.local/share/pipx/venvs/superclaude`).
- Roadmap H2 layout: `.dev/releases/Current/MultiModelSwarm/roadmap.md` last milestone `## M4:` at line 321; tail H2s at 380, 406, 427, 446, 462.
- Branch commits (`git log src/superclaude/cli/roadmap/obligation_scanner.py`): `d98ac921` (Layer 5) and `223aeae1` (Fix 1 + Fix 3), both 2026-05-30 05:08 UTC — predate the 06:58 pipeline run but were never `pipx install --force`-ed.

## Proposed Fix

A two-step recovery, no code change required:

```bash
# 1. Re-install the scanner-patched superclaude into pipx (from the worktree with the fixes)
pipx install --force /config/workspace/IronClaude/.claude/worktrees/RoadmapCLI-ObligationFix

# 2. Resume the halted pipeline
superclaude roadmap run \
  /config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md \
  --resume
```

Step 1 is single-line and safe — pipx isolation makes it reversible. Step 2 is the literal resume command the pipeline emitted on halt.

Verification before resume (optional, recommended):

```bash
/config/.local/share/pipx/venvs/superclaude/bin/python -c \
  "import superclaude.cli.roadmap.obligation_scanner as s; \
   print(hasattr(s, '_find_tail_section_start'))"
```

Expected: `True`.

## Alternative Fixes Considered

- **Edit the roadmap to suppress the 4 stub mentions.** Rejected — the mentions are correct, descriptive uses ("stub transport for tests" in a Fallback column is the right text). Rewriting them is content vandalism in service of a scanner bug.
- **Lower the `no_undischarged_obligations` threshold.** Rejected — the gate exists to catch real obligations; loosening it masks future regressions.
- **Re-run pipeline from a different worktree where the source is editable-installed.** Possible but adds operational complexity; pipx is the operator install vector per memory `reference_superclaude_install_vector.md`.

## Risk + Rollback

- Risk: a `pipx install --force` rebuild against the current worktree pulls in any other branch-local source changes too, not just the scanner. The current branch is scanner-only (see `git log --oneline -3`), so risk is low.
- Rollback: `pipx install --force /config/workspace/IronClaude` (main workspace path) reverts to the prior CLI behavior.
- After the resume succeeds: confirm `anti-instinct-audit.md` reports `undischarged_obligations: 0` and the pipeline advances to `test-strategy` → `spec-fidelity` → `deviation-analysis` → `remediate` → `certify`.

## Next Steps

1. Run the two commands above (re-install + resume).
2. If a subsequent step (e.g., `test-strategy`) fails, re-invoke `/sc:troubleshoot` with that step's output — it's a separate diagnosis.
3. Once the pipeline certifies, the branch is ready to PR onto the fork (`gh pr create --repo IronbellyOrg/IronClaude --base master --head feat/roadmap-scanner-layer-5-h3-subsection`).
