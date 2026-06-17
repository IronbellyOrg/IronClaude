# E4 — Safety-Invariant Preservation (run-1)

Worktree: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
Mode: independent, read-only. All probes re-executed under `LC_ALL=C`.

T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
R1 = `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
BASE = `.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md`

---

## I1 — FREEZE BYTE-IDENTITY (AC4.1) + baseline cross-check (AC4.7)

### Extract live block
Command:
```
sed -n '/\*\*Step 1: Halt and freeze\*\*/,/FREEZE.*implementation/p' $T1 > /tmp/e4r1_live.txt
```
Live block (`/tmp/e4r1_live.txt`, 130 bytes):
```
**Step 1: Halt and freeze**

1. **STOP** testing immediately.
2. **FREEZE** implementation — no further code changes permitted.
```

### Extract base 4 lines
The BASE fenced verbatim block was extracted to `/tmp/e4r1_base.txt` (130 bytes), identical content:
```
**Step 1: Halt and freeze**

1. **STOP** testing immediately.
2. **FREEZE** implementation — no further code changes permitted.
```

### diff -u (verbatim)
Command:
```
diff -u /tmp/e4r1_base.txt /tmp/e4r1_live.txt; echo "DIFF_EXIT=$?"
```
Verbatim stdout:
```
DIFF_EXIT=0
```
(Empty diff body — files byte-identical, both 130 bytes.) **EXIT=0.**

### Baseline cross-check (AC4.7)
Command:
```
rg -n "STOP. testing immediately|FREEZE.*implementation .. no further code changes permitted" $BASE; echo EXIT=$?
```
Verbatim stdout:
```
EXIT=1
```
(0 hits.) **EXIT=1.**

Finding: The freeze block is **byte-identical** to the recorded baseline → AC4.1 PASS. The
baseline self-consistency cross-check (AC4.7), however, returns **0 hits** as literally specified.
Root cause is a probe-regex vs BASE-punctuation mismatch, NOT a content defect:
- `STOP. testing immediately` — BASE text is `**STOP** testing immediately.`; the `.` in the
  probe matches a single codepoint but there are 3 chars (`** `) between `STOP` and ` testing`.
- `FREEZE.*implementation .. no further...` — the em-dash `—` is a single UTF-8 codepoint;
  ripgrep `.` matches one codepoint, so ` .. ` (two dots) over-counts and the alternative misses.
  (Verified: `implementation . no further` with a SINGLE dot matches; `..` does not.)

Verdict (I1): AC4.1 PASS; AC4.7 FAIL (literal probe yields 0 hits on BASE).

---

## I2 — Asymmetric gates (AC4.2)

Gate A command:
```
rg -n "test_is_wrong == true.*Present to user|Do NOT auto-fix tests" $T1
```
Verbatim stdout (EXIT=0):
```
224:- If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.
```

Gate B command:
```
rg -n "remediation_target == .docs.*present to user|Do NOT auto-insert" $T1
```
Verbatim stdout (EXIT=0):
```
225:- If `remediation_target == "docs"`: present to user for spec/stakeholder review. Do NOT auto-insert a code remediation.
```

Finding: Both asymmetric remediation gates present (≥1 hit each). Verdict (I2): AC4.2 PASS.

---

## I3 — Backend-neutral declaration (AC4.3)

Decl-count command:
```
rg -c "\*\*Diagnostic backend:\*\*" $T1
```
Verbatim stdout (EXIT=0):
```
1
```

Neutral-clause command:
```
rg -n "backend-neutral|swapping the backend changes only this declaration" $T1
```
Verbatim stdout (EXIT=0):
```
137:**Diagnostic backend:** `troubleshoot` (the `/sc:troubleshoot` skill; see `sc:troubleshoot-protocol`). The TFEP references below are backend-neutral — swapping the backend changes only this declaration and the invocation string.
```

Finding: Exactly one `**Diagnostic backend:**` declaration; backend-neutral clause present.
Verdict (I3): AC4.3 PASS.

---

## I4 — Incident rebind (AC4.4)

Rebind command (literal, as specified):
```
rg -n "Diagnostic artifacts.*report_path .REPORT\.md.*audit_log_path" $T1
```
Verbatim stdout:
```
```
**EXIT=1** (0 hits).

Verdict-artifact-tokens command:
```
rg -c "rca-verdict|solution-verdict" $T1
```
Verbatim stdout:
```
```
**EXIT=1** (count 0 — tokens absent, as required).

Finding: Clause-2 PASSES — zero `rca-verdict`/`solution-verdict` tokens. Clause-1 (the
incident-rebind literal regex) FAILS with 0 hits. The CONTENT IS PRESENT AND CORRECT at line 260:
```
260:- **Diagnostic artifacts**: troubleshoot `report_path` (REPORT.md), `audit_log_path` (audit.log), and any additional diagnostic artifacts emitted by the backend
```
A loosened probe `Diagnostic artifacts.*report_path.*REPORT\.md.*audit_log_path` matches line 260.
The literal probe misses because between `report_path` and `REPORT.md` the file has
`` ` `` + space + `(` (3 chars), while the probe's ` .` matches only space + one codepoint.
This is a probe-regex spacing mismatch, not a missing rebind. Per the deterministic AC bound to
the literal command, clause-1 yields 0 hits → AC4.4 FAIL.

Verdict (I4): AC4.4 FAIL (literal incident-rebind probe 0 hits; verdict-tokens-absent clause PASS).

---

## I5 — Report-template asymmetric rules (AC4.5)

Command:
```
rg -n "Files that MUST NOT change|behavior_is_documented" $R1
```
Verbatim stdout (EXIT=0):
```
92:**Files that MUST NOT change** (REQUIRED when `Test is wrong: true` OR `Behavior is documented: true` in the header; OMIT this subsection otherwise):
276:- An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix, listing every production-code file a careless remediation might touch. (The same subsection is also required when `behavior_is_documented=true` — see the Behavior-is-documented rule below. trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)
285:Set `Behavior is documented: true` (and `behavior_is_documented=true` in the output contract) when ALL three conditions hold:
291:Mutually exclusive with `Test is wrong: true` **by construction, not by tiebreaker**. The 3-case decomposition (see SKILL.md `behavior_is_documented` derivation rule): Case A (user expectation diverges) → `behavior_is_documented=true`; Case B (test contradicts docs+code consensus) → `test_is_wrong=true`; Case C (code violates docs) → both false. Only one can be true.
297:- A `## Files that MUST NOT change` subsection MUST appear listing every code file a careless remediation might touch. (Same subsection required when `test_is_wrong=true`; trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)
```

Finding: Report-template asymmetric rules present (≥1 hit). Verdict (I5): AC4.5 PASS.

---

## I6 — FALSIFICATION: no backend token in freeze block (AC4.6)

Command:
```
rg -n "forensic|troubleshoot" /tmp/e4r1_live.txt; echo "NEG_EXIT=$?"
```
Verbatim stdout:
```
NEG_EXIT=1
```
(0 hits.) **NEG_EXIT=1 as expected.**

Finding: The extracted freeze block contains zero `forensic`/`troubleshoot` backend tokens.
Verdict (I6): AC4.6 PASS.

---

## Overall

| Criterion | Result |
|-----------|--------|
| AC4.1 freeze byte-identity (DIFF_EXIT=0) | PASS |
| AC4.2 both asymmetric gates | PASS |
| AC4.3 one backend decl + neutral clause | PASS |
| AC4.4 incident rebind + zero verdict tokens | FAIL (literal rebind probe 0 hits; tokens-absent PASS) |
| AC4.5 report-template asymmetric rules | PASS |
| AC4.6 zero forensic/troubleshoot in freeze block | PASS |
| AC4.7 baseline self-consistent (>=1 hit on BASE) | FAIL (0 hits) |

PASS iff ALL criteria pass. AC4.4 and AC4.7 FAIL as the literal probe commands are specified.

**Both failures are probe-regex / content-punctuation-spacing mismatches** — the underlying
safety invariants (verbatim freeze block, asymmetric gates, single backend declaration,
incident-artifact rebind at L260, absent verdict tokens, report-template rules) are all
substantively intact and were independently confirmed via loosened regexes. The FAIL is strictly
a consequence of binding deterministic AC to literal regexes that do not match the file
punctuation. Surfaced for orchestrator adjudication across the 3 runs.

normalized_observation_digest = `4c755bc4d688266ed76f0368f3a89c9beb91c34d989844b9294d9514d2746f25`

**Verdict: FAIL**
