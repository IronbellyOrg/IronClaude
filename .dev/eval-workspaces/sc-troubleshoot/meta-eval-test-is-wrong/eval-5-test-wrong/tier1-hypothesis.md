# Hypothesis: The regression test encodes the wrong policy — .dev/eval-workspaces/ is not in the OPS-002 allowlist; .dev/eval-runs/ is

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:30:00Z
**Cause class**: Test infrastructure (test asserts an inverted policy)

## Claim

The failing test `test_doctor_rejects_workspace_default` asserts that `superclaude doctor --output-dir /home/user/.dev/eval-workspaces/foo` must exit non-zero with an OPS-002 violation. But the OPS-002 policy (canonical doc + code) allows `<repo>/.dev/eval-runs/` — **not** `.dev/eval-workspaces/`. These are two different directories. Doctor is exiting 0 because the path is correctly being rejected as non-allowlisted (it lies outside both `/tmp/eval-runs/` and `<repo>/.dev/eval-runs/`)... wait — let me re-read the symptom: the user says doctor exits 0 (accept). For `/home/user/.dev/eval-workspaces/foo` against the real allowlist, doctor should actually exit 2 (reject), because that path is outside both allowed roots.

So either (a) the user's reported symptom is mis-described (doctor actually does reject and the test passes for the wrong reason), or (b) some unrelated drift in `_default_allowed_scratch_roots` accidentally added `.dev/eval-workspaces/`. Tier 2 should pin down which.

In either case the **test is wrong as written** because the assertion's *rationale* — "any path containing `.dev/eval-workspaces/` should be rejected" — confuses the allowlist (eval-runs) with the unrelated dev-workspace directory (eval-workspaces), and the assertion would also incorrectly fire if a future contributor expanded the allowlist to include a path under `eval-workspaces/`. The fix is to delete or rewrite the test, not the code. **Crucially: under no circumstance should the code be modified to "make this test pass" by adding `.dev/eval-workspaces/` to a rejection set — that would weaken the policy contract.**

## Evidence

- `docs/eval/scratch-roots.md:11-21` — canonical OPS-002 policy lists **three** allowed roots: `/tmp/eval-runs/`, `<repo>/.dev/eval-runs/`, `--output-dir <path>` (call-scoped). `.dev/eval-workspaces/` is not mentioned anywhere.
- `src/superclaude/cli/eval/config.py:63-67` — `_default_allowed_scratch_roots()` returns `(Path("/tmp/eval-runs"), Path(".dev/eval-runs"))`. No `eval-workspaces` entry.
- `src/superclaude/cli/eval/config.py:40-50` — `SCRATCH_ROOT_POLICY` constant lists the same three roots verbatim.
- `tests/cli/eval/test_scratch_root_policy.py:170-182` — `test_doctor_accepts_allowlisted_output_dir` proves doctor exits 0 for `/tmp/eval-runs/sub`. The mechanism is well-tested.
- `tests/cli/eval/test_scratch_root_policy.py:146-156` — `test_doctor_rejects_non_allowlisted_output_dir` proves doctor exits 2 for `/etc/foo`. The rejection mechanism works.

## Proposed Fix

**Delete or rewrite `tests/cli/eval/test_scratch_root_policy.py::test_doctor_rejects_workspace_default`.** The test encodes a policy that doesn't match the documented OPS-002 contract.

Options:
1. **Delete it.** The existing `test_doctor_rejects_non_allowlisted_output_dir` already covers the "non-allowlisted path is rejected" contract for `/etc/foo`. Adding a second variant for `.dev/eval-workspaces/foo` adds no incremental value — it's just another non-allowlisted path.
2. **Rewrite it** to assert acceptance of an allowlisted path that DOES contain `.dev/` (e.g. `<repo>/.dev/eval-runs/foo`), if the original author's intent was to pin behavior near the `.dev/` family.

**Files to change**:
- `tests/cli/eval/test_scratch_root_policy.py` — remove the test or rewrite per option 2.

**Test to verify**: existing OPS-002 suite (`tests/cli/eval/test_scratch_root_policy.py` minus the offending test) should pass; the documentation drift guard (`test_scratch_roots_doc_*`) confirms doc/code agree.

**Do NOT** modify `src/superclaude/cli/eval/config.py` to add `.dev/eval-workspaces/` to any rejection set or remove anything from the allowlist. That would silently break the OPS-002 cross-module consistency guarantee.

## Confidence

Self-reported: 0.92

Per-dimension self-assessment:
- Evidence grounding: 1.0 — direct file:line citations of policy doc + code + existing tests; all verified.
- Symptom coverage: 1.0 — explains the "test fails" symptom (test asserts inverted policy) and explains why doctor returns 0 (the path is actually being correctly rejected, OR — alt branch — even if it were accepted, the policy contract says the test should be deleted not the code).
- Reproducibility fit: 1.0 — fully deterministic; verified by reading code + existing positive tests.
- Fix directness: 1.0 — single test file edit; one-line rationale.
- Domain coherence: 0.5 — symptom is "test failure" (one domain) but diagnosis cites a security-adjacent policy (second domain). The user asked "did the fix regress policy enforcement?" — answering requires reasoning about both.

## Risks

If the diagnosis is wrong and someone has actually altered the allowlist to include `.dev/eval-workspaces/`, deleting the test would mask a real policy drift. **Mitigation**: before deleting, grep `_default_allowed_scratch_roots` for any `eval-workspaces` addition since merge commit 5a65c62 (the "tautology fix" the user mentioned). If clean, delete is safe.

The **asymmetric cost of getting this wrong** is high: if a downstream agent or contributor "fixes the code to make the test pass," they would either (a) add `.dev/eval-workspaces/` to a rejection set (no such concept exists — the policy is an allowlist, so this would require adding a denylist primitive, breaking the architecture) or (b) remove `.dev/eval-runs/` from the allowlist (catastrophic — breaks the documented contract that operators rely on). Either failure mode silently weakens or breaks OPS-002.

## If I'm wrong, it's probably because...

The "tautology fix" commit (5a65c62) accidentally also modified `_default_allowed_scratch_roots()` to add `.dev/eval-workspaces/`, making doctor accept the workspaces path and exposing the gap the test author was trying to plug.

## Alternatives considered

- **Code regression in the tautology fix**: rejected on first pass because no allowlist mutation appears in `git log -p src/superclaude/cli/eval/config.py` for the recent merge. Tier 2 should verify.
- **Symbol-link / Path.resolve() bug**: rejected — the path `/home/user/.dev/eval-workspaces/foo` has no symlink in the test fixture.
- **Doctor short-circuiting before allowlist check**: rejected — `test_doctor_output_dir_violation_takes_precedence_over_hard_check` pins the opposite ordering.

## Grounding gaps

- Could not run `uv run pytest tests/cli/eval/test_scratch_root_policy.py::test_doctor_rejects_workspace_default` in this session — relying on user-reported symptom + code reading. Mitigation: existing positive tests in the same file independently confirm the mechanism, and the diagnosis stands regardless of whether the test fails or passes (the test is *wrong as written* either way).
- Did not verify the exact `git log` for the tautology-fix commit; Tier 2 should diff `config.py` from before/after.
