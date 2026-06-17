# TEST E2 — Adapter Contract Round-Trip — run-3

Independent, read-only re-execution. LC_ALL=C for all probes.

- T1 = src/superclaude/skills/sc-task-protocol/SKILL.md
- P1 = src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
- R1 = src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md

All three files confirmed present.

---

## probe-1 — field matrix (21 cells, each >=1)

Command:
  for f in status test_is_wrong recommended_escalation tasklist_insertion_path remediation_target root_cause_summary solution_summary; do rg -c "$f" $T1; rg -c "$f" $P1; rg -c "$f" $R1; done

Verbatim stdout (FIELD T1/P1/R1):
  status                  T1=6  P1=23 R1=8
  test_is_wrong           T1=3  P1=8  R1=9
  recommended_escalation  T1=5  P1=6  R1=1
  tasklist_insertion_path T1=2  P1=3  R1=1
  remediation_target      T1=4  P1=3  R1=1
  root_cause_summary      T1=3  P1=3  R1=1
  solution_summary        T1=3  P1=3  R1=1
EXIT=0

Findings: Every one of the 21 cells is >=1; minimum cell value is 1. AC2.1 satisfied.
Verdict: PASS

---

## probe-2 — TFEP adapter rows in P1 (expect 5)

Command: rg -c "TFEP adapter field \(contract v1.1.0" $P1
Verbatim stdout:
  5
EXIT=0

Findings: Exactly 5 adapter-row matches in P1 (the 5 adapter fields). AC2.2 satisfied.
Verdict: PASS

---

## probe-3 — contract semver default 1.1.0 in P1

Command: rg -n "Output-contract semver, default .1\.1\.0" $P1
Verbatim stdout:
  62:| `contract_version` | semver string | Output-contract semver, default `1.1.0`. Additive version stamp for the Pipeline Hardening Closure fields (FR-13) and the TFEP adapter fields (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`); existing consumers reading only the prior fields are unaffected (NFR-6). Distinct from `target_release`. |
EXIT=0

Findings: 1 hit at P1 line 62, exit 0. contract_version declares the 1.1.0 default. AC2.3 satisfied.
Verdict: PASS

---

## probe-4 — recommended_escalation enum in BOTH P1+R1

Command: rg -n "none\|retry\|escalate_depth\|halt" $P1 $R1
Verbatim stdout:
  src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:163:recommended_escalation: <none|retry|escalate_depth|halt>
EXIT=0

Findings: The literal-pipe probe (\| = literal | in rg's Rust regex) matched only the
unescaped R1 form (line 163). P1 renders the same enum inside a markdown table cell with
backslash-escaped pipes (none\|retry\|escalate_depth\|halt, P1 line 73), so the literal-pipe
pattern does not match it. Cross-check confirms presence in P1:
rg -c 'none\\|retry\\|escalate_depth\\|halt' $P1 => 1.
AC2.4 (enum in BOTH P1+R1) satisfied — semantically present in both, differing only by
markdown-table pipe-escaping.
Verdict: PASS

---

## probe-5 — remediation_target enum in BOTH P1+R1

Command: rg -n "test\|code\|docs\|none" $P1 $R1
Verbatim stdout:
  src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:165:remediation_target: <test|code|docs|none>
EXIT=0

Findings: Same escaping dynamic as probe-4. Literal-pipe probe matched only the unescaped R1
form (line 165). P1 carries the table-escaped form test\|code\|docs\|none at line 75;
cross-check rg -c 'test\\|code\\|docs\\|none' $P1 => 1 confirms presence. AC2.5 satisfied.
Verdict: PASS

---

## probe-6 — Diagnostic backend declaration in T1 (expect 1)

Command: rg -c "Diagnostic backend.*troubleshoot" $T1
Verbatim stdout:
  1
EXIT=0

Findings: Exactly one Diagnostic-backend declaration in T1. AC2.6 satisfied.
Verdict: PASS

---

## probe-7 — FALSIFICATION: no producer-internal field leak in ## TFEP Consumer block

Command: sed -n '/## TFEP Consumer/,/^### /p' $R1 | rg -n "tier_reached|confidence:|escalation_reason"
Verbatim stdout:
  (no output)
EXIT=1

Findings: Zero matches (rg exit 1 = no matches). The ## TFEP Consumer block of R1 does not
leak producer-internal fields (tier_reached / confidence: / escalation_reason).
Falsification held — AC2.7 satisfied.
Verdict: PASS

---

## Overall

| AC | Description | Result |
|----|-------------|--------|
| AC2.1 | all 21 cells >=1 | PASS |
| AC2.2 | adapter rows == 5 | PASS |
| AC2.3 | contract_version 1.1.0 present | PASS |
| AC2.4 | recommended_escalation enum in BOTH P1+R1 | PASS |
| AC2.5 | remediation_target enum in BOTH P1+R1 | PASS |
| AC2.6 | exactly one Diagnostic-backend decl | PASS |
| AC2.7 | zero TFEP-consumer leak (falsification) | PASS |

normalized_observation_digest: 202f96f6aa6f2ec96f6818ea58e2bcc325b19c9578a8f65664678122bda12bf8

Verdict: PASS
