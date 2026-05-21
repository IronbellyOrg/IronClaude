# Troubleshoot Report — Scratch-root allowlist tautology (eval_run vs doctor)

**Command**: `/sc:troubleshoot --type security --scope src/superclaude/cli/eval/` (NEW protocol skill)
**Tier reached**: 2 (escalated under `security_caution` rule) | **Confidence**: 0.90 | **Status**: success
**Source**: subagent inline output (final REPORT.md write was blocked; sibling artifacts written: hypothesis cards, candidate-fixes.md, fix-proposals/, adversarial/merged-output.md, audit.log)

## Summary

`eval run --output-dir /etc/foo` silently succeeds because `eval_run` passes the operator-supplied output dir as **both** the candidate path and the allowlist-extending `output_dir=` keyword argument. `resolve_scratch_root` appends the kwarg to the allowlist before checking the candidate, so the check becomes a tautology. `doctor` does not pass the kwarg, so its allowlist stays canonical and `/etc/foo` is correctly rejected.

## Diagnosis

**Root cause** (cited from snapshot fixture):

- `commands.py:1473-1477` — `eval_run` calls:

  ```
  resolve_scratch_root(requested_output, config=base_config, output_dir=output_dir)
  ```

  passing the operator's `--output-dir` value as **both** the candidate AND the `output_dir=` allowlist-extending kwarg.
- `config.py:217-220` — `resolve_scratch_root` appends the `output_dir` kwarg to the runtime allowlist.
- `config.py:225-231` — the subsequent loop matches the candidate against the (now-self-extended) allowlist; it trivially matches.
- `commands.py:815-823` — `doctor` calls `resolve_scratch_root(output_dir)` **without** the kwarg → allowlist stays canonical → `/etc/foo` correctly rejected.
- The post-fix live code at `config.py:203-213` explicitly anti-documents the snapshot's pattern (independent confirmation of the diagnosis).

## Evidence

1. `fixtures/real-bug-scratch-root/commands.py:1476` — `output_dir=output_dir` self-reference.
2. `fixtures/real-bug-scratch-root/commands.py:817` (doctor) — no `output_dir=` kwarg, correct behavior.
3. `fixtures/real-bug-scratch-root/config.py:217-231` — allowlist extension + check logic.
4. `fixtures/real-bug-scratch-root/scratch-roots.md` — OPS-002 policy with verbatim `/etc/foo` rejection example.

## Proposed Fix (merged from adversarial debate, Fix-1 + Fix-3)

1. **Drop `output_dir=output_dir`** from the `eval_run` first-gate call. The function signature retains `output_dir=` for the legitimate defense-in-depth callers (e.g. `HomeIsolation.containment_guard`), but `eval_run` must not pass the operator-supplied candidate as both arguments.
2. **Add a CLI-boundary regression test** at `tests/cli/eval/test_eval_run_scratch_root.py` asserting:
   - `superclaude eval run --output-dir /etc/foo` exits with code 2
   - stderr contains the OPS-002 policy reference
   - Parity test: same input passed to `doctor` also rejects (cross-module invariant)
3. **Follow-up** (separate task `T-OPS002-helper-guard`): tighten `resolve_scratch_root` itself to reject the self-allowlisting misuse pattern at the helper level (Fix-2 from the debate — split out to avoid bundling).

## Alternative Fixes Considered

- **Fix-1 alone** (drop kwarg only): rejected as insufficient — leaves the helper open to the same misuse if a future caller repeats the mistake.
- **Fix-2 alone** (helper guard only): rejected as wrong-layer — would silently break the legitimate defense-in-depth callers.
- **Fix-3 alone** (test only, no code change): rejected — does not fix the bug.

The merged Fix-1 + Fix-3 is the chosen approach. Fix-2 becomes a follow-up.

## Risk + Rollback

- **Likelihood of regression**: Low. The kwarg drop is a one-line removal in a single call site; existing tests pin the doctor behavior.
- **Test coverage**: Currently partial; the new regression test closes the gap.
- **Rollback**: `git revert` of the kwarg-drop commit reverts to the bug (silent acceptance). The regression test will then fail loudly, surfacing the revert.

## Tier 2 Process

- Tier 1 confidence: 0.78 (multi-domain symptom — CLI surface + helper logic + policy) → escalated under `security_caution` rule (security type + confidence < 0.95).
- Tier 2 agents spawned (in agent voice, inline simulation): root-cause-analyst, security-engineer, quality-engineer.
- All 3 converged on the same diagnosis but proposed 3 distinct fixes → triggered Wave 4 adversarial debate.
- Adversarial merged-output: Fix-1 + Fix-3 chosen, Fix-2 deferred. Self-review PASS (no regressions, edge cases covered, test plan present).

## Audit

- Hypothesis cards: `tier1-hypothesis.md`, `tier2-root-cause-analyst-hypothesis.md`, `tier2-security-engineer-hypothesis.md`, `tier2-quality-engineer-hypothesis.md`
- Candidate fixes index: `candidate-fixes.md`
- Fix proposals: `fix-proposals/fix-{1,2,3}.md`
- Adversarial artifacts: `adversarial/merged-output.md` (+ supporting debate-transcript, base-selection)
- Audit log: `audit.log`
