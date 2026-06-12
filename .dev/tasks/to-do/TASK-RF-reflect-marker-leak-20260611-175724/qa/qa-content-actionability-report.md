# QA Report — Content Actionability Lens (rf-qa-qualitative)

**Topic:** TASK-RF-reflect-marker-leak-20260611-175724 — reflect wrapper marker-leak fix
**Date:** 2026-06-11
**Phase:** doc-qualitative (actionability lens, REPORT-ONLY, fix_authorization:false)
**Fix cycle:** N/A

---

## Overall Verdict: PASS

The fix is actionable on all four dimensions of the embedded lens prompt. A future
executing reflect agent can construct the verification command without interpretation;
the regression test has a verified fail-before / pass-after property; the contract
deferral carries an exact ready-to-apply patch; and the validation evidence names
precisely what passed. The adversarial mandate ("assume ≥5 actionability errors") was
applied with full rigor — I actively hunted for the five errors and verified each
candidate against source. None survived verification. Reporting a fabricated finding to
satisfy the ≥5 mandate would itself be a false-evidence violation, so I report the honest
result with the verification trail below.

## NO DIRECT EDITS CONFIRMED

I made NO edits to any file. fix_authorization was false. All tool calls were Read,
Grep, Bash (read-only git/sed/grep + one read-only `uv run pytest`), and one Write to
THIS report file only.

## Items Reviewed
| # | Check (actionability dimension) | Result | Evidence |
|---|---------------------------------|--------|----------|
| 1 | Skill text gives unambiguous command-construction order | PASS | SKILL.md §6.1.1 control (i) L501 + control (d) L496 — see Finding analysis below |
| 2 | Regression test fails-before / passes-after the skill fix | PASS | Pre-fix envelope had 0 marker + 0 `env -u` (git show HEAD); test asserts both present; `uv run pytest ...::test_verification_envelope_strips_reflect_wrapper_marker` → 1 passed |
| 3 | Contract action OR deferral is actionable | PASS | `phase-outputs/plans/contract-carveout-deferral.md` L24-29 carries exact patch text + exact insertion point |
| 4 | Validation evidence tells a maintainer exactly what passed | PASS | `final-output-summary.md` L29-35 per-step command/exit/verdict table; honest scoping of repo-wide ruff exit-1 |

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0 / Important: 0 / Minor: 0
- Issues fixed in-place: 0 (report-only)

## Detailed actionability analysis

### Dimension 1 — Command construction order (the hardest actionability claim)

The adversarial worry here is wrapper-nesting ambiguity: control (d) (L496) says "Wrap
every command as `timeout <N> <cmd>`" while control (i) (L501) says the invocation MUST be
`timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <validated base command>`. Read in
isolation, an executor could ask "does the (d) timeout wrap the (i) env-strip, or does the
(i) wrapper replace (d)?"

This ambiguity is RESOLVED by control (i)'s own closing sentence (L501):
> "The strip preserves controls (d)–(h): the `timeout <N>` wrap from (d) remains the
> outer wrapper..."

So the canonical, unambiguous nesting is `timeout <N> env -u <MARKER> <validated base
command>` — outer-to-inner: timeout, then env-strip, then base verb. The ordering
gate is also explicit ("After the base verification command passes controls (a)–(c) and
the no-mutation gate"). `<N>` resolves to control (d)'s concrete "default 120s, max 600s"
(verified present at L496). An executor has a fully determined construction recipe. PASS.

### Dimension 2 — Regression test fail-before / pass-after

Empirically verified, not assumed:
- `git show HEAD:.../SKILL.md` §6.1.1 envelope → 0 occurrences of `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, 0 of `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.
- Current envelope → 2 + 2 occurrences.
- Test (`test_marker_suppression.py` L112-134) extracts the envelope via stable anchors
  (`### 6.1.1 \`execute_shell_command\` safety envelope` → `### 6.2`, both verified to exist
  exactly once) and asserts BOTH `_MARKER in envelope` AND `f"env -u {_MARKER}" in envelope`.
- Both assertions are FALSE against the pre-fix text and TRUE against the post-fix text →
  genuine fail-before/pass-after. Live run: `1 passed in 0.13s`.

The test is a source-contract test (reads `src/`, not the `.claude/` mirror — L19-22) and
carries a docstring (L121-128) directing that if the fix moves into Python a direct
marker-present→marker-stripped unit test must supersede it. That forward-instruction is
itself actionable for a future maintainer. PASS.

### Dimension 3 — Contract deferral actionability

`contract-carveout-deferral.md` is the DEFAULT path (no operator authorization for the
cross-worktree edit). It is actionable because it gives a maintainer everything needed to
apply the carve-out later without re-deriving anything:
- Exact target file + section (L26-27: "immediately after the generator `MUST NOT clear,
  unset, or overwrite ...` bullet in §3").
- Exact patch text (L29, a verbatim exception clause).
- The reason deferral was chosen (concurrent-worktree-ownership risk, L13). PASS.

### Dimension 4 — Validation evidence

`final-output-summary.md` gives a per-step table (L29-35) with command, exit code, and
verdict for each of steps 3.1–3.5, and the marker/`env -u` semantic change in prose
(L23-25). Crucially it does NOT overclaim: the repo-wide ruff exit-1 (L33-34) is honestly
scoped to pre-existing unrelated debt with the task's own files shown CI-clean, and the
contract status is honestly "DEFERRED (default path)" (L37-39). The test-count claim "6
marker-suppression incl. new test" matches the file (6 `def test_` functions). A maintainer
reading this knows exactly what passed, what was deferred, and what is pre-existing
out-of-scope debt. PASS.

## Issues Found
None. No CRITICAL, IMPORTANT, or MINOR actionability defects survived verification.

## Actions Taken
None (report-only, fix_authorization:false). No files modified.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- This spawn carried NO `## Inherited Structural Verdict` block, so I relied on no
  upstream rf-qa PASS items. I performed standalone verification of every claim per the
  missing-verdict fallback.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Command-construction-order ambiguity (d)-vs-(i): verified by Reading SKILL.md L496 + L501
  and confirming (i)'s closing sentence pins (d) as the outer wrapper — tool: Read offset
  489 limit 17.
- Fail-before property: verified by `git show HEAD:.../SKILL.md` envelope grep returning 0/0
  marker occurrences pre-fix — tool: Bash git show + grep -c.
- Pass-after property: verified by live `uv run pytest ...::test_verification_envelope_strips_reflect_wrapper_marker` → 1 passed — tool: Bash uv run pytest.
- Test anchor existence: verified `### 6.1.1 ... safety envelope` and `### 6.2` each resolve
  exactly once so the test's `.index()` extraction cannot raise — tool: Bash grep -n.
- Test-count claim accuracy: verified summary's "6" against `grep -c "^def test_"` = 6 — tool: Bash grep -c.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 5 | Grep/Bash: 5 | Glob: 0
(Tool calls ≥ checklist items: 4 dimensions, 10 verifying tool invocations. Not suspect.)

**On the ≥5-errors adversarial mandate:** I treated it as an instruction to search
exhaustively, not as a quota to fill. The one genuine ambiguity candidate (wrapper nesting
order) was found and then verified to be explicitly resolved in the source text. I will not
manufacture four more findings to hit a number — that would violate the false-evidence
prohibition. The honest verdict is PASS.

## Recommendations
- None blocking. (Non-actionability note, out of this lens's scope: the pre-existing
  repo-wide ruff debt and the deferred sibling-contract carve-out are already logged as
  Follow-Up Items in the task file — both correctly out of scope for this fix.)

## QA Complete
