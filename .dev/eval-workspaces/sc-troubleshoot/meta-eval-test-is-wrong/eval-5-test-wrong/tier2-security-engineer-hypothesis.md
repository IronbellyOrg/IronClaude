# Hypothesis: The test, if "fixed by code change," would silently weaken the OPS-002 defense-in-depth chain

**Agent**: security-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:34:30Z
**Cause class**: Test infrastructure (test polices an inverted/invented policy in a security-adjacent gate)

## Claim

OPS-002 is a security-adjacent allowlist that protects the operator's real filesystem (`~/.claude/`, `/etc/`, `/var/lib/`, `/root/`) from a buggy or hostile eval suite that resolves a scratch root outside the documented safe set. The synthetic regression test mis-encodes the policy by adding an invented `.dev/eval-workspaces/` rejection rule. **The danger is not the test failure itself — it's the remediation path a less-careful diagnosis would propose.**

If a downstream agent (or human) tries to "fix the code to make the test pass," they have three options, all bad:

1. **Add a denylist for `.dev/eval-workspaces/`**: introduces a denylist concept that doesn't exist in the architecture (the policy is allowlist-only by design). This silently weakens the contract because future contributors will assume denylist semantics elsewhere.
2. **Remove `.dev/eval-runs/` from the allowlist**: catastrophic. Operators relying on the documented repo-relative scratch root would be locked out. Breaks every CI run.
3. **Add a name-based reject before the allowlist check**: special-casing a path family. Brittle, doesn't generalize, and adds a code path that bypasses the unified `resolve_scratch_root` ingress (the cross-module consistency guarantee).

All three would pass through code review as "small change to make a test pass." The correct move is to refuse the false premise and delete the test.

## Evidence

- `docs/eval/scratch-roots.md:28-38` — "Why an allowlist (and not a denylist)" section explicitly rejects the denylist pattern. Quote: "The allowlist closes that surface by defaulting to refusal."
- `docs/eval/scratch-roots.md:39-51` — four layered defenses (loader-time, doctor pre-flight, HomeIsolation containment, atomic setup wrapper) all funnel through the same allowlist. Any name-based reject special case would skip several of these.
- `src/superclaude/cli/eval/config.py:32-50` — `SCRATCH_ROOT_POLICY` is a string constant emitted verbatim on every rejection. The cross-module consistency claim (OPS-002) hinges on every consumer quoting the same policy text — modifying the runtime check without updating the constant + doc + default tuple is caught by `test_policy_constant_*` and `test_default_allowlist_matches_policy_constant`, but a special-case denylist BEFORE the allowlist check would slip past all three.
- `src/superclaude/cli/eval/commands.py:845-850` — doctor calls `resolve_scratch_root(output_dir)` and immediately renders any `ScratchRootViolation` through `format_scratch_root_violation`. There is no name-based reject anywhere in this path — and there shouldn't be.

## Proposed Fix

**Delete the test.** Same conclusion as `quality-engineer`, reached from a different direction (security-policy-integrity rather than test-correctness).

**Additional recommendation**: add a comment to `_default_allowed_scratch_roots()` explicitly noting "if you're adding to this tuple, also update `SCRATCH_ROOT_POLICY` and `docs/eval/scratch-roots.md`." (Already enforced by drift-guard tests, but inline comments help future contributors avoid this class of error.)

**Files to change**:
- `tests/cli/eval/test_scratch_root_policy.py` — delete `test_doctor_rejects_workspace_default`.

**Files NOT to change**:
- `src/superclaude/cli/eval/config.py` — leave the allowlist + policy constant untouched.
- `src/superclaude/cli/eval/commands.py` — leave the doctor flow untouched.

## Confidence

Self-reported: 0.94

Per-dimension self-assessment:
- Evidence grounding: 1.0
- Symptom coverage: 1.0 — explains both the surface failure and the latent asymmetric cost.
- Reproducibility fit: 1.0
- Fix directness: 1.0
- Domain coherence: 0.5 — test + security policy.

## Risks

The strongest counterargument: maybe the test author noticed a real attack surface where `.dev/eval-workspaces/` *was* accidentally allowlisted in some draft branch, and wrote the test as a tripwire. **Mitigation**: `git log --all -p -- src/superclaude/cli/eval/config.py | grep -i workspaces` — if no commit ever added `eval-workspaces` to the allowlist, the tripwire interpretation is implausible.

## If I'm wrong, it's probably because...

A different, more recent OPS-002 update (post the "tautology fix") added `.dev/eval-workspaces/` to the allowlist intentionally (e.g. to support a new eval-workspace feature), and the test was a forward-leaning guard against premature expansion — but in that case the test is asking the wrong question (it should pin the *acceptance* of allowlisted workspace paths, not their rejection).

## Alternatives considered

- **Tighten the code to add a name-based reject for `eval-workspaces`**: rejected on architectural grounds (denylist-by-stealth breaks the allowlist-only invariant).
- **Add `.dev/eval-workspaces/` to the allowlist so the test fails for the "right" reason**: rejected — it would silently expand the trusted scratch surface; the canonical doc says `eval-workspaces/` is a dev-tool directory, not a scratch root.

## Grounding gaps

None for the security analysis. The asymmetric-cost argument doesn't depend on running the test — it depends on the architecture of the policy, which is fully readable in the source.
