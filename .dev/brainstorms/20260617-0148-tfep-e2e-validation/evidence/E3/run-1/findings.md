# E3 — Protocol-Chain Resolution — run-1 Findings

Worktree: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend
Files: T1=src/superclaude/skills/sc-task-protocol/SKILL.md ; P1=src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md ; C1=src/superclaude/commands/troubleshoot.md
Probe harness: LC_ALL=C; ripgrep (rg); stdout captured verbatim.

## H1

```
$ rg -n "Write context to .\{output_dir\}/context\.yaml" $T1
205:4. Write context to `{output_dir}/context.yaml` — this file is the `{context_path}` passed to the diagnostic backend in Step 3.
EXIT=0
```

## H2

```
$ rg -nF "/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}" $T1
215:6. Invoke: `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` where `{depth}` is determined by the depth mapping above (this step's bullets): `--depth standard` for the 1st/simple TFEP trigger, and `--depth deep` for a systemic failure, ≥3 new failing tests, or a 2nd (escalation) trigger. Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY; remediation insertion and resume stay with task-protocol.
EXIT=0
```

## H3

```
$ rg -n "Pass NO .--fix" $T1
215:6. Invoke: `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` where `{depth}` is determined by the depth mapping above (this step's bullets): `--depth standard` for the 1st/simple TFEP trigger, and `--depth deep` for a systemic failure, ≥3 new failing tests, or a 2nd (escalation) trigger. Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY; remediation insertion and resume stay with task-protocol.
EXIT=0
```

## H4a

```
$ rg -nF "When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml`" $P1
148:6. If `--caller` is set, record it in the audit header `caller:` field (see the TARGET header below). If `--context <path>` is set, read it (the caller brief) and resolve it to an absolute path; STOP if the path is unreadable. When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5).
EXIT=0
```

## H4b

```
$ rg -n "return-contract" $P1
148:6. If `--caller` is set, record it in the audit header `caller:` field (see the TARGET header below). If `--context <path>` is set, read it (the caller brief) and resolve it to an absolute path; STOP if the path is unreadable. When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5).
471:4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write `<output-dir>/return-contract.yaml` mapping the Output Contract fields to the TFEP-consumed schema: `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`. Source the asymmetric-cost gates from `test_is_wrong`/`test_file_path`/`behavior_is_documented`; source `root_cause_summary` from the REPORT.md Diagnosis (step 2) and `solution_summary` from the REPORT.md Proposed Fix / Next Steps; derive `recommended_escalation` from `status`+`tier_reached`+`confidence`. Derivation clarifications: copy `status` from the Output Contract `status` computed in step 3 (values `success|partial|failed`). Default `tasklist_insertion_path` to `null` in this diagnosis-only TFEP mode — under the remediation-ownership decision the task-protocol composes the `## Failure Remediation Plan (Adjudicated)` block from `remediation_target`/`root_cause_summary`/`solution_summary`, so this field is non-null ONLY if troubleshoot itself wrote a standalone adjudicated remediation-plan file under `<output-dir>/` (do not invent a new mandatory artifact; the default is `null`). `test_file_path` is intentionally NOT duplicated into this 7-field wire set: when `remediation_target=test` the test path remains available via the broader Output Contract / REPORT.md, and the consumer's asymmetric-cost branch presents to the user (it does not auto-fix), so the path need not be in the wire contract. Path-valued fields in the emitted `return-contract.yaml` are ABSOLUTE paths. For `recommended_escalation` use this deterministic tie-break hint: `status=failed` or a hard-stop → `halt`; `status=partial` with low confidence → `escalate_depth`; `status=partial` at tier < 2 → `retry`; `status=success` → `none` (the consumer-side action mapping lives in the task-protocol consumer, Phase 5). Record `return_contract_path` in the audit footer (SUMMARY block). NOTE: TFEP invokes troubleshoot for DIAGNOSIS ONLY and does NOT pass `--fix` (per the task-protocol remediation-ownership decision) — this step emits the contract but does NOT apply any remediation. The same fields are ALSO rendered as the `## TFEP Consumer` section of REPORT.md (per `refs/report-template.md`) when `caller=task-unified`.
479:   - (if `caller=task-unified`) the emitted `return-contract.yaml` path.
481:**Exit criteria**: `REPORT.md` written, audit log finalized, user notified. If `--fix` is not set, return the output contract and STOP. When `caller=task-unified`, `return-contract.yaml` is written and its path returned.
EXIT=0
```

## H5

```
$ rg -n "Emit TFEP return-contract|return-contract\.yaml.*written and its path returned" $P1
471:4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write `<output-dir>/return-contract.yaml` mapping the Output Contract fields to the TFEP-consumed schema: `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`. Source the asymmetric-cost gates from `test_is_wrong`/`test_file_path`/`behavior_is_documented`; source `root_cause_summary` from the REPORT.md Diagnosis (step 2) and `solution_summary` from the REPORT.md Proposed Fix / Next Steps; derive `recommended_escalation` from `status`+`tier_reached`+`confidence`. Derivation clarifications: copy `status` from the Output Contract `status` computed in step 3 (values `success|partial|failed`). Default `tasklist_insertion_path` to `null` in this diagnosis-only TFEP mode — under the remediation-ownership decision the task-protocol composes the `## Failure Remediation Plan (Adjudicated)` block from `remediation_target`/`root_cause_summary`/`solution_summary`, so this field is non-null ONLY if troubleshoot itself wrote a standalone adjudicated remediation-plan file under `<output-dir>/` (do not invent a new mandatory artifact; the default is `null`). `test_file_path` is intentionally NOT duplicated into this 7-field wire set: when `remediation_target=test` the test path remains available via the broader Output Contract / REPORT.md, and the consumer's asymmetric-cost branch presents to the user (it does not auto-fix), so the path need not be in the wire contract. Path-valued fields in the emitted `return-contract.yaml` are ABSOLUTE paths. For `recommended_escalation` use this deterministic tie-break hint: `status=failed` or a hard-stop → `halt`; `status=partial` with low confidence → `escalate_depth`; `status=partial` at tier < 2 → `retry`; `status=success` → `none` (the consumer-side action mapping lives in the task-protocol consumer, Phase 5). Record `return_contract_path` in the audit footer (SUMMARY block). NOTE: TFEP invokes troubleshoot for DIAGNOSIS ONLY and does NOT pass `--fix` (per the task-protocol remediation-ownership decision) — this step emits the contract but does NOT apply any remediation. The same fields are ALSO rendered as the `## TFEP Consumer` section of REPORT.md (per `refs/report-template.md`) when `caller=task-unified`.
481:**Exit criteria**: `REPORT.md` written, audit log finalized, user notified. If `--fix` is not set, return the output contract and STOP. When `caller=task-unified`, `return-contract.yaml` is written and its path returned.
EXIT=0
```

## H6

```
$ rg -n "first match wins|test_is_wrong == true|remediation_target == .docs.|status == .success.|recommended_escalation == .none.|recommended_escalation == .retry.|recommended_escalation == .escalate_depth.|recommended_escalation == .halt." $T1
222:Evaluate the branches top-to-bottom, first match wins; the asymmetric-cost gates (`test_is_wrong`, `remediation_target == "docs"`) are checked first.
224:- If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.
225:- If `remediation_target == "docs"`: present to user for spec/stakeholder review. Do NOT auto-insert a code remediation.
226:- If `status == "success"`: proceed to Step 5 (insert remediation plan + resume).
227:- If `recommended_escalation == "none"`: remediation ready — insert the adjudicated plan and resume (Step 5). (A `status == "partial"` diagnosis is routed by `recommended_escalation` — normally `retry`/`escalate_depth` per the backend derivation — not auto-resumed here.)
228:- If `recommended_escalation == "retry"`: re-run `/sc:troubleshoot` once at the SAME `--depth` (re-enter Step 3; increment `escalation_count`).
229:- If `recommended_escalation == "escalate_depth"`: re-invoke `/sc:troubleshoot` at `--depth deep` (re-enter Step 3; increment `escalation_count`). If the run was already at `--depth deep`, there is no deeper level — treat as FULL STOP.
230:- If `recommended_escalation == "halt"` (or `status == "failed"`): **FULL STOP** — report to user, no further fixes (immediate FULL STOP regardless of `escalation_count`).
EXIT=0
```

## H7

```
$ rg -n "increment .escalation_count.|FULL STOP" $T1
213:- 3rd TFEP trigger → **FULL STOP** (report to user, no further fixes)
228:- If `recommended_escalation == "retry"`: re-run `/sc:troubleshoot` once at the SAME `--depth` (re-enter Step 3; increment `escalation_count`).
229:- If `recommended_escalation == "escalate_depth"`: re-invoke `/sc:troubleshoot` at `--depth deep` (re-enter Step 3; increment `escalation_count`). If the run was already at `--depth deep`, there is no deeper level — treat as FULL STOP.
230:- If `recommended_escalation == "halt"` (or `status == "failed"`): **FULL STOP** — report to user, no further fixes (immediate FULL STOP regardless of `escalation_count`).
270:3rd TFEP trigger  → FULL STOP. Report to user. Do not attempt further fixes.
EXIT=0
```

## H8

```
$ rg -n "1st TFEP trigger|2nd TFEP trigger|systemic failure OR ≥3 new failing tests|3rd TFEP trigger|--depth standard|--depth deep" $T1
210:- 1st TFEP trigger → `--depth standard`
211:- 2nd TFEP trigger (escalation) → `--depth deep`
212:- systemic failure OR ≥3 new failing tests → `--depth deep`
213:- 3rd TFEP trigger → **FULL STOP** (report to user, no further fixes)
215:6. Invoke: `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` where `{depth}` is determined by the depth mapping above (this step's bullets): `--depth standard` for the 1st/simple TFEP trigger, and `--depth deep` for a systemic failure, ≥3 new failing tests, or a 2nd (escalation) trigger. Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY; remediation insertion and resume stay with task-protocol.
229:- If `recommended_escalation == "escalate_depth"`: re-invoke `/sc:troubleshoot` at `--depth deep` (re-enter Step 3; increment `escalation_count`). If the run was already at `--depth deep`, there is no deeper level — treat as FULL STOP.
268:1st TFEP trigger  → /sc:troubleshoot --caller task-unified --depth standard
269:2nd TFEP trigger (escalation, systemic, or ≥3 new failing tests)  → /sc:troubleshoot --caller task-unified --depth deep
270:3rd TFEP trigger  → FULL STOP. Report to user. Do not attempt further fixes.
EXIT=0
```

## H9

```
$ TOTAL=$(rg -c -- "--fix" $T1); PROHIB=$(rg -c "NO .--fix|Pass NO .--fix|with NO --fix" $T1); echo "FIX_TOTAL=$TOTAL FIX_PROHIBITION=$PROHIB"
FIX_TOTAL=2 FIX_PROHIBITION=2
EXIT=0
```

## H10

```
$ rg -c -- "--tier|--intent" $T1 $C1 $P1 src/superclaude/commands/task.md src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md
EXIT=1
```

## Findings

All ten probes resolved as specified. AC3.1 (H1, line 205): the task-protocol binds the diagnostic context to `{output_dir}/context.yaml` and identifies it as the `{context_path}` passed to the backend. AC3.2 (H2, line 215): the dispatch carries the exact fixed-string shape with all four required flags — `--caller task-unified`, `--context {context_path}`, `--output-dir {output_dir}`, `--depth {depth}`. AC3.3: the troubleshoot backend ingests the caller at Wave 0 (H4, line 148 — `When caller=task-unified, mark Wave 5 to emit return-contract.yaml`) and the producing emit is gated on the same caller at Wave 5 step 4.5 (H5, line 471) with the exit-criteria reaffirmation at line 481 — both ingest and emit are conditioned on `caller=task-unified`. AC3.4 (H6): all six branch keys are present plus the precedence note `first match wins` (line 222) — the asymmetric-cost gates `test_is_wrong == true` (224) and `remediation_target == "docs"` (225), `status == "success"` (226), and the four `recommended_escalation` arms none/retry/escalate_depth/halt (227-230). AC3.5 (H7): loop discipline shows `increment escalation_count` (lines 228, 229) and `FULL STOP` at multiple terminal points (213, 229, 230, 270). AC3.6 (H8): the depth map carries all three ordinals — 1st->`--depth standard` (210), 2nd->`--depth deep` (211), 3rd->FULL STOP (213) — and both depth tokens appear. AC3.7 (H9): the falsification holds — every literal `--fix` occurrence in T1 (FIX_TOTAL=2) is a prohibition (FIX_PROHIBITION=2); there is no live/permissive `--fix` in the TFEP dispatch path. AC3.8 (H10): the legacy `--tier`/`--intent` flags are fully removed — zero matches (exit 1) across all five files.

## AC3.9 — Anchored Chain-Continuity Conclusion

The protocol chain is continuous: every output a step requires has a later producer or ingester anchor. (1) The task-protocol DISPATCHES with the four-flag shape at T1:215 (H2), declaring the `--context`/`--output-dir`/`--depth` it will hand off. (2) The troubleshoot backend INGESTS that handoff at P1:148 (H4) — reading `--context`, resolving the path, and marking Wave 5 to emit the return-contract precisely when `caller=task-unified`. (3) The backend PRODUCES the contract at P1:471 and reaffirms it at P1:481 (H5) — `return-contract.yaml` written and its path returned. (4) The task-protocol CONSUMES that contract's fields through the first-match-wins branch ladder at T1:222-230 (H6), routing on `test_is_wrong`/`remediation_target`/`status`/`recommended_escalation`. No required output is orphaned: the dispatch's flags are read by the ingest gate, and the contract the emit produces is read by the consumer ladder. The chain is closed.

## Verdict

PASS — all deterministic criteria AC3.1-AC3.8 satisfied; anchored judgment AC3.9 confirms a continuous, closed chain. normalized_observation_digest = cf4ead44b9029fbf70b1976594630ff7edb7605281a76a87710b39dabef21108
