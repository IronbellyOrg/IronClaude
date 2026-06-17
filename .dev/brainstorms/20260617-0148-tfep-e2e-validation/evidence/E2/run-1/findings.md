# TEST E2 — Adapter Contract Round-Trip — run-1

- Worktree: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
- LC_ALL=C for all probes
- T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
- P1 = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- R1 = `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`

---

## Probe 1 — 21-cell field matrix (each of 7 fields x 3 files, every count >=1)

Command:
`for f in <7 fields>; do rg -c "$f" $T1 ; rg -c "$f" $P1 ; rg -c "$f" $R1 ; done`

Verbatim stdout (FIELD T1 P1 R1):
```
FIELD=status                    T1=6  P1=23 R1=8
FIELD=test_is_wrong             T1=3  P1=8  R1=9
FIELD=recommended_escalation    T1=5  P1=6  R1=1
FIELD=tasklist_insertion_path   T1=2  P1=3  R1=1
FIELD=remediation_target        T1=4  P1=3  R1=1
FIELD=root_cause_summary        T1=3  P1=3  R1=1
FIELD=solution_summary          T1=3  P1=3  R1=1
```
EXIT=0 (every per-field rg -c exited 0; no zero counts)

Findings: All 21 cells >=1; minimum cell value is 1. AC2.1 SATISFIED.

Verdict: PASS

---

## Probe 2 — TFEP adapter row count in P1 (EXPECT exactly 5)

Command: `rg -c "TFEP adapter field \(contract v1.1.0" $P1`

Verbatim stdout:
```
5
```
EXIT=0

Findings: Exactly 5 adapter rows. AC2.2 SATISFIED.

Verdict: PASS

---

## Probe 3 — contract_version semver default 1.1.0 in P1 (>=1, exit 0)

Command: `rg -n "Output-contract semver, default .1\.1\.0" $P1`

Verbatim stdout:
```
62:| `contract_version` | semver string | Output-contract semver, default `1.1.0`. Additive version stamp for the Pipeline Hardening Closure fields (FR-13) and the TFEP adapter fields (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`); existing consumers reading only the prior fields are unaffected (NFR-6). Distinct from `target_release`. |
```
EXIT=0

Findings: contract_version documents semver default `1.1.0`. AC2.3 SATISFIED.

Verdict: PASS

---

## Probe 4 — recommended_escalation enum in P1 AND R1

Command (verbatim): `rg -n "none\|retry\|escalate_depth\|halt" $P1 $R1`

Verbatim stdout:
```
src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:163:recommended_escalation: <none|retry|escalate_depth|halt>
```
EXIT=0

PROBE-PATTERN ARTIFACT (load-bearing): the pattern uses an ESCAPED pipe
`none\|retry...` which rg treats as a LITERAL `|`. R1 line 163 has plain pipes
`<none|retry|escalate_depth|halt>` -> matches. P1 line 73 renders the same enum
inside a markdown table with table-escaped pipes (`none\|retry\|...`) -> the
literal-`|` pattern does NOT match (char after `none` is `\`, not `|`). This is
a markdown-escaping artifact, not a real absence.

Semantic confirmation enum present in BOTH:
```
P1:73:| `recommended_escalation` | enum `none\|retry\|escalate_depth\|halt` | TFEP adapter field (contract v1.1.0+). ... `none` = remediation ready; `retry` = re-run at same depth; `escalate_depth` = re-run deeper; `halt` = full stop. |
R1:163:recommended_escalation: <none|retry|escalate_depth|halt>
```

Findings: enum {none, retry, escalate_depth, halt} present in P1 (line 73) and
R1 (line 163). AC2.4 SATISFIED.

Verdict: PASS

---

## Probe 5 — remediation_target enum in P1 AND R1

Command (verbatim): `rg -n "test\|code\|docs\|none" $P1 $R1`

Verbatim stdout:
```
src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:165:remediation_target: <test|code|docs|none>
```
EXIT=0

PROBE-PATTERN ARTIFACT: same escaped-pipe-vs-table-escaped-pipe mechanism as
Probe 4. R1 line 165 (plain pipes) matches; P1 line 75 (table-escaped pipes)
does not match the literal-`|` pattern.

Semantic confirmation enum present in BOTH:
```
P1:75:| `remediation_target` | enum `test\|code\|docs\|none` | TFEP adapter field (contract v1.1.0+). ... `test` when `test_is_wrong` true ...; `docs` when ...; `code` otherwise; `none` when `recommended_escalation: halt`. |
R1:165:remediation_target: <test|code|docs|none>
```

Findings: enum {test, code, docs, none} present in P1 (line 75) and R1 (line
165). AC2.5 SATISFIED.

Verdict: PASS

---

## Probe 6 — Diagnostic backend declaration in T1 (EXPECT exactly 1)

Command: `rg -c "Diagnostic backend.*troubleshoot" $T1`

Verbatim stdout:
```
1
```
EXIT=0

Findings: Exactly one Diagnostic-backend declaration. AC2.6 SATISFIED.

Verdict: PASS

---

## Probe 7 — FALSIFICATION: no producer-internal field leak in R1 "## TFEP Consumer" block (EXPECT 0 hits, exit 1)

Command:
`sed -n '/## TFEP Consumer/,/^### /p' $R1 | rg -n "tier_reached|confidence:|escalation_reason"`

Verbatim stdout:
```
(no output)
```
EXIT=1

Block inspected exposes ONLY the 7 contract fields (status, test_is_wrong,
recommended_escalation, tasklist_insertion_path, remediation_target,
root_cause_summary, solution_summary). No producer-internal fields leak.

Findings: 0 hits, grep exit 1. AC2.7 (falsification) SATISFIED.

Verdict: PASS

---

## Overall

| AC    | Criterion                                           | Result |
|-------|-----------------------------------------------------|--------|
| AC2.1 | all 21 field-matrix cells >=1 (min=1)               | PASS   |
| AC2.2 | adapter rows == 5                                   | PASS   |
| AC2.3 | contract_version 1.1.0 present in P1                | PASS   |
| AC2.4 | recommended_escalation enum in BOTH P1+R1          | PASS   |
| AC2.5 | remediation_target enum in BOTH P1+R1             | PASS   |
| AC2.6 | exactly one Diagnostic-backend declaration in T1   | PASS   |
| AC2.7 | zero producer-internal leak in TFEP Consumer block | PASS   |

normalized_observation_digest: 202f96f6aa6f2ec96f6818ea58e2bcc325b19c9578a8f65664678122bda12bf8

FINAL VERDICT: PASS
