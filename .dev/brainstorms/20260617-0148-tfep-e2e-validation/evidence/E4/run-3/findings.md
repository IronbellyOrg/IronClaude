# E4 — Safety-Invariant Preservation — run-3

Independent, read-only re-execution. Worktree:
`/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
Probes run under `LC_ALL=C`. Files:
- T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
- R1 = `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- BASE = `.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md`

---

## I1 — FREEZE byte-identity (AC4.1)

Live extract: `sed -n '/\*\*Step 1: Halt and freeze\*\*/,/FREEZE.*implementation/p' $T1 > /tmp/e4r3_live.txt`
Baseline extract: 4 verbatim freeze lines from the code fence in BASE (`awk '/^```$/{c++;next} c==1{print}' BASE > /tmp/e4r3_base.txt`).

Command: `diff -u /tmp/e4r3_base.txt /tmp/e4r3_live.txt`

```
(no output — files identical)
```
DIFF_EXIT=0

Both files contain exactly:
```
**Step 1: Halt and freeze**

1. **STOP** testing immediately.
2. **FREEZE** implementation — no further code changes permitted.
```
(the dash is a UTF-8 em-dash, byte-identical in both). **AC4.1 PASS.**

---

## I1b — baseline non-empty cross-check (feeds AC4.7)

Command: `rg -n "STOP. testing immediately|FREEZE.*implementation .. no further code changes permitted" $BASE`

```
(no match)
```
EXIT=1  (spec EXPECT: >=1)

Finding: probe-regex strictness defect. The pattern `STOP. testing` uses a single
`.` wildcard, but the markdown source is `**STOP** testing` — the two `*` bold
markers occupy two characters where the probe allows one, so the regex misses.
The FREEZE branch `implementation .. no further` likewise mis-aligns on the
em-dash byte sequence. The content is verifiably present: plain
`grep -n "STOP" $BASE` returns line 11 `1. **STOP** testing immediately.` and the
relaxed pattern `STOP\*\* testing immediately` matches. The baseline is genuinely
non-empty and self-consistent (it is the same verbatim block that diff-matched in
I1). The literal probe exit (1) is recorded faithfully → contributes to AC4.7 FAIL
on the mechanical gate, but the invariant content is intact.

---

## I2 — non-auto-fix gates (AC4.2)

I2a command: `rg -n "test_is_wrong == true.*Present to user|Do NOT auto-fix tests" $T1`
```
224:- If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.
```
EXIT=0

I2b command: `rg -n "remediation_target == .docs.*present to user|Do NOT auto-insert" $T1`
```
225:- If `remediation_target == "docs"`: present to user for spec/stakeholder review. Do NOT auto-insert a code remediation.
```
EXIT=0

Both safety gates present. **AC4.2 PASS.**

---

## I3 — single backend declaration + backend-neutral clause (AC4.3)

I3a command: `rg -c "\*\*Diagnostic backend:\*\*" $T1`
```
1
```
EXIT=0  (exactly one declaration)

I3b command: `rg -n "backend-neutral|swapping the backend changes only this declaration" $T1`
```
137:**Diagnostic backend:** `troubleshoot` (the `/sc:troubleshoot` skill; see `sc:troubleshoot-protocol`). The TFEP references below are backend-neutral — swapping the backend changes only this declaration and the invocation string.
```
EXIT=0

One declaration + neutrality clause. **AC4.3 PASS.**

---

## I4 — incident rebind from report_path/audit_log_path + zero verdict artifacts (AC4.4)

I4a command: `rg -n "Diagnostic artifacts.*report_path .REPORT\.md.*audit_log_path" $T1`
```
(no match)
```
EXIT=1  (spec EXPECT: >=1)

Finding: probe-regex strictness defect. The real line 260 is:
`- **Diagnostic artifacts**: troubleshoot `report_path` (REPORT.md), `audit_log_path` (audit.log), and any additional diagnostic artifacts emitted by the backend`.
The probe segment `report_path .REPORT\.md` expects `report_path` + one space +
one wildcard char + `REPORT`, but the actual text after `report_path` is a
backtick then ` (` then `REPORT.md` — the literal single-space in the pattern
cannot match the backtick. The relaxed intent pattern
`report_path.*REPORT\.md.*audit_log_path` matches line 260. The incident rebind to
`report_path`/`audit_log_path`/REPORT.md IS present; the literal probe exit (1)
is recorded faithfully.

I4b command: `rg -c "rca-verdict|solution-verdict" $T1`
```
0
```
EXIT=1 (rg -c with zero matches exits 1) — **zero verdict artifacts, as required.**

AC4.4 has two halves: the verdict-artifact-absence half PASSES (zero
rca-verdict/solution-verdict). The report_path/audit_log_path rebind content is
present but the literal I4a probe returned 0 matches → **AC4.4 FAIL on the
mechanical gate (probe-regex defect, content intact).**

---

## I5 — report-template MUST-NOT-change rules (AC4.5)

Command: `rg -n "Files that MUST NOT change|behavior_is_documented" $R1`
```
92:**Files that MUST NOT change** (REQUIRED when `Test is wrong: true` OR `Behavior is documented: true` in the header; OMIT this subsection otherwise):
276:- An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix ... trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)
285:Set `Behavior is documented: true` (and `behavior_is_documented=true` in the output contract) when ALL three conditions hold:
291:Mutually exclusive with `Test is wrong: true` **by construction** ... Only one can be true.
297:- A `## Files that MUST NOT change` subsection MUST appear ... trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)
```
EXIT=0

Report-template MUST-NOT-change rules present. **AC4.5 PASS.**

---

## I6 — FALSIFICATION: freeze block free of backend terminology (AC4.6)

Command: `rg -n "forensic|troubleshoot" /tmp/e4r3_live.txt`
```
(no match)
```
NEG_EXIT=1  (zero hits, as required)

The freeze block contains no `forensic`/`troubleshoot` backend tokens.
`freeze_backend_token_count=0`. **AC4.6 PASS.**

---

## Verdict

**FAIL** (mechanical gate).

The load-bearing safety invariant is PRESERVED: AC4.1 freeze byte-identity holds
(DIFF_EXIT=0, live block byte-identical to verbatim baseline), AC4.2/4.3/4.5/4.6
all PASS, and the freeze block carries zero backend terminology.

Two probes returned 0 against their stated EXPECT(>=1) — I1b (AC4.7) and I4a
(AC4.4). Both are **probe-regex strictness defects, not artifact regressions**:
I1b's single-`.` wildcard cannot span the `**STOP**` bold markers; I4a's
literal-space cannot span the `report_path`-backtick boundary. In both cases the
target content is verifiably present (plain grep / relaxed patterns confirm). Per
the deterministic "PASS iff ALL criteria" gate, run-3 records FAIL on the literal
exit codes rather than silently rewriting the probes to manufacture a PASS. A
re-spec with corrected I1b/I4a regexes (e.g. `STOP\*\* testing`,
`report_path.*REPORT\.md.*audit_log_path`) would yield PASS.

normalized_observation_digest: 4c755bc4d688266ed76f0368f3a89c9beb91c34d989844b9294d9514d2746f25
