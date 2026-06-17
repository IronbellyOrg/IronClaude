# TEST E2 — Adapter Contract Round-Trip — run-2 findings

INDEPENDENT READ-ONLY validation. Environment: `LC_ALL=C`. Worktree:
`/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`

Targets:
- T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
- P1 = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- R1 = `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`

---

## Probe 1 — 7-field x 3-file presence matrix (21 cells, every count >= 1)

Command (per field f; per file in {T1,P1,R1}): `rg -c "$f" "$file"`

Verbatim stdout:
```
field=status file=T1 count=6 exit=0
field=status file=P1 count=23 exit=0
field=status file=R1 count=8 exit=0
field=test_is_wrong file=T1 count=3 exit=0
field=test_is_wrong file=P1 count=8 exit=0
field=test_is_wrong file=R1 count=9 exit=0
field=recommended_escalation file=T1 count=5 exit=0
field=recommended_escalation file=P1 count=6 exit=0
field=recommended_escalation file=R1 count=1 exit=0
field=tasklist_insertion_path file=T1 count=2 exit=0
field=tasklist_insertion_path file=P1 count=3 exit=0
field=tasklist_insertion_path file=R1 count=1 exit=0
field=remediation_target file=T1 count=4 exit=0
field=remediation_target file=P1 count=3 exit=0
field=remediation_target file=R1 count=1 exit=0
field=root_cause_summary file=T1 count=3 exit=0
field=root_cause_summary file=P1 count=3 exit=0
field=root_cause_summary file=R1 count=1 exit=0
field=solution_summary file=T1 count=3 exit=0
field=solution_summary file=P1 count=3 exit=0
field=solution_summary file=R1 count=1 exit=0
```
EXIT=0

Findings: All 21 cells return count >= 1; minimum cell = 1. AC2.1 satisfied.
Verdict: PASS

---

## Probe 2 — adapter-row count in P1 (EXPECT exactly 5)

Command: `rg -c "TFEP adapter field \(contract v1.1.0" $P1`

Verbatim stdout:
```
5
```
EXIT=0

Findings: Exactly 5 adapter rows. AC2.2 satisfied.
Verdict: PASS

---

## Probe 3 — contract_version default 1.1.0 in P1 (EXPECT >=1, exit 0)

Command: `rg -n "Output-contract semver, default .1\.1\.0" $P1`

Verbatim stdout:
```
62:| `contract_version` | semver string | Output-contract semver, default `1.1.0`. Additive version stamp for the Pipeline Hardening Closure fields (FR-13) and the TFEP adapter fields (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`); existing consumers reading only the prior fields are unaffected (NFR-6). Distinct from `target_release`. |
```
EXIT=0

Findings: contract_version default `1.1.0` present at P1:62. AC2.3 satisfied.
Verdict: PASS

---

## Probe 4 — recommended_escalation enum in BOTH P1 + R1

Command (spec, literal): `rg -n "none\|retry\|escalate_depth\|halt" $P1` and same on `$R1`

Verbatim stdout (P1):
```
```
EXIT=1  (no output)

Verbatim stdout (R1):
```
163:recommended_escalation: <none|retry|escalate_depth|halt>
```
EXIT=0

PROBE-INSTRUMENT ANALYSIS: P1 exit-1 is a ripgrep artifact, NOT a content gap. In rg's
default Rust regex engine `\|` is a LITERAL pipe, so the spec pattern searches for the
plain string `none|retry|escalate_depth|halt`. P1's markdown table cell escapes the pipes
(`none\|retry\|escalate_depth\|halt`, backslashes present) so the pattern misses. R1 uses
unescaped pipes and matches.

Corroborating backslash-tolerant re-probe:
`rg -n "recommended_escalation.*none.*retry.*escalate_depth.*halt" $P1`
```
73:| `recommended_escalation` | enum `none\|retry\|escalate_depth\|halt` | TFEP adapter field (contract v1.1.0+). ...
```
EXIT=0

Findings: Enum GENUINELY present in BOTH P1 (line 73) and R1 (line 163). AC2.4 (content
criterion "enum in BOTH") satisfied.
Verdict: PASS

---

## Probe 5 — remediation_target enum in BOTH P1 + R1

Command (spec, literal): `rg -n "test\|code\|docs\|none" $P1` and same on `$R1`

Verbatim stdout (P1):
```
```
EXIT=1  (no output)

Verbatim stdout (R1):
```
165:remediation_target: <test|code|docs|none>
```
EXIT=0

PROBE-INSTRUMENT ANALYSIS: Same `\|`=literal-pipe artifact as probe 4. P1 escapes the
enum pipes (`test\|code\|docs\|none`); R1 uses unescaped pipes.

Corroborating backslash-tolerant re-probe:
`rg -n "remediation_target.*test.*code.*docs.*none" $P1`
```
75:| `remediation_target` | enum `test\|code\|docs\|none` | TFEP adapter field (contract v1.1.0+). ...
```
EXIT=0

Findings: Enum GENUINELY present in BOTH P1 (line 75) and R1 (line 165). AC2.5 satisfied.
Verdict: PASS

---

## Probe 6 — Diagnostic-backend declaration in T1 (EXPECT exactly 1)

Command: `rg -c "Diagnostic backend.*troubleshoot" $T1`

Verbatim stdout:
```
1
```
EXIT=0

Findings: Exactly one declaration. AC2.6 satisfied.
Verdict: PASS

---

## Probe 7 — FALSIFICATION: no producer-internal field leak in `## TFEP Consumer` block of R1 (EXPECT 0 hits, exit 1)

Command: `sed -n '/## TFEP Consumer/,/^### /p' $R1 | rg -n "tier_reached|confidence:|escalation_reason"`

Verbatim stdout:
```
```
EXIT=1  (zero hits)

Findings: No producer-internal fields leak into the TFEP Consumer block. AC2.7 satisfied.
Verdict: PASS

---

## Overall Verdict

AC2.1 PASS, AC2.2 PASS, AC2.3 PASS, AC2.4 PASS, AC2.5 PASS, AC2.6 PASS, AC2.7 PASS.

**E2 run-2 VERDICT: PASS**

normalized_observation_digest = 202f96f6aa6f2ec96f6818ea58e2bcc325b19c9578a8f65664678122bda12bf8

Adjudicator note: spec probe-4/probe-5 P1 commands carry a ripgrep `\|`=literal-pipe
artifact that yields exit-1 on P1's backslash-escaped markdown enum cells. Underlying
content (both enums in both files) is present and confirmed via backslash-tolerant
re-probes. Verdict decided on the content criteria AC2.4/AC2.5 ("enum in BOTH"). If the
harness instead scores the LITERAL spec-command P1 exit codes as the criterion, probes 4
and 5 on P1 register FAIL — flagged here for transparent adjudication.
