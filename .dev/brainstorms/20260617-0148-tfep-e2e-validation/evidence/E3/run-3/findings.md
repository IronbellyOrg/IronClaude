# E3 Protocol-Chain Resolution — run-3 findings

Independent read-only re-execution. Files:
- T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
- P1 = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- C1 = `src/superclaude/commands/troubleshoot.md`

All probes run with `LC_ALL=C`.

## H1 — context.yaml write (AC3.1)
Command: `rg -n "Write context to .\{output_dir\}/context\.yaml" $T1`  EXIT: 0
```
205:4. Write context to `{output_dir}/context.yaml` — this file is the `{context_path}` passed to the diagnostic backend in Step 3.
```

## H2 — exact /sc:troubleshoot invocation shape (AC3.2)
Command: `rg -nF "/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}" $T1`  EXIT: 0
```
215:6. Invoke: `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` where ... Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY ...
```
The exact fixed-string invocation shape is present verbatim.

## H3 — Pass NO `--fix`
Command: `rg -n "Pass NO .--fix" $T1`  EXIT: 0 (T1:215, same line as H2).

## H4 — return-contract gated on caller=task-unified (AC3.3 part)
Command: `rg -nF "When \`caller=task-unified\`, mark Wave 5 to emit \`return-contract.yaml\`" $P1` then `rg -n "return-contract" $P1`  EXIT: 0
```
148:6. ... When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5).
471:4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write `<output-dir>/return-contract.yaml` ...
479:   - (if `caller=task-unified`) the emitted `return-contract.yaml` path.
481:**Exit criteria**: ... When `caller=task-unified`, `return-contract.yaml` is written and its path returned.
```

## H5 — return-contract emit/return (AC3.3 part)
Command: `rg -n "Emit TFEP return-contract|return-contract\.yaml.*written and its path returned" $P1`  EXIT: 0 (P1:471, P1:481).

## H6 — six branch keys + precedence note (AC3.4)
Command: `rg -n "first match wins|test_is_wrong == true|remediation_target == .docs.|status == .success.|recommended_escalation == .none.|recommended_escalation == .retry.|recommended_escalation == .escalate_depth.|recommended_escalation == .halt." $T1`  EXIT: 0 — 8 matching lines.
```
222:Evaluate the branches top-to-bottom, first match wins; the asymmetric-cost gates (`test_is_wrong`, `remediation_target == "docs"`) are checked first.
224:- If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.
225:- If `remediation_target == "docs"`: present to user ...
226:- If `status == "success"`: proceed to Step 5 ...
227:- If `recommended_escalation == "none"`: remediation ready ...
228:- If `recommended_escalation == "retry"`: ... increment `escalation_count`.
229:- If `recommended_escalation == "escalate_depth"`: ... treat as FULL STOP.
230:- If `recommended_escalation == "halt"` (or `status == "failed"`): **FULL STOP** ...
```
All six required branch keys present plus the "first match wins" precedence note.

## H7 — escalation_count increment / FULL STOP (AC3.5)
Command: `rg -n "increment .escalation_count.|FULL STOP" $T1`  EXIT: 0 (T1:213,228,229,230,270).

## H8 — depth mapping (AC3.6)
Command: `rg -n "1st TFEP trigger|2nd TFEP trigger|systemic failure OR ≥3 new failing tests|3rd TFEP trigger|--depth standard|--depth deep" $T1`  EXIT: 0 (T1:210,211,212,213,215,229,268,269,270).
```
210:- 1st TFEP trigger → `--depth standard`
211:- 2nd TFEP trigger (escalation) → `--depth deep`
212:- systemic failure OR ≥3 new failing tests → `--depth deep`
213:- 3rd TFEP trigger → **FULL STOP** ...
```

## H9 — FALSIFICATION: --fix count parity (AC3.7)
Command: `TOTAL=$(rg -c -- "--fix" $T1); PROHIB=$(rg -c "NO .--fix|Pass NO .--fix|with NO --fix" $T1); echo "FIX_TOTAL=$TOTAL FIX_PROHIBITION=$PROHIB"`  EXIT: 0
```
FIX_TOTAL=2 FIX_PROHIBITION=2
```
Line-level confirmation — both `--fix` mentions are prohibition contexts:
- T1:215 "Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY"
- T1:239 "troubleshoot diagnoses and emits the contract ... with NO --fix"
COUNTS EQUAL. No un-prohibited `--fix` leak in the TFEP path.

## H10 — FALSIFICATION: zero --tier/--intent (AC3.8)
Command: `rg -c -- "--tier|--intent" $T1 $C1 $P1 src/superclaude/commands/task.md src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`  EXIT: 1 (no matches across all five surfaces → tier_intent_count = 0).

## Findings paragraph
Every deterministic gate (AC3.1–AC3.8) holds against the live files in this worktree. The producer (sc-task-protocol) emits the exact, fixed-string `/sc:troubleshoot --caller task-unified ...` invocation with `--fix` explicitly withheld; the consumer-side branch table carries all six contract keys under a "first match wins" precedence rule with asymmetric-cost gates evaluated first. The diagnostic backend (sc-troubleshoot-protocol) conditionally emits `return-contract.yaml` strictly when `caller=task-unified`, mapping its Output Contract to the seven-field TFEP wire schema, and returns the artifact path. Both falsification probes clear: the `--fix` token appears only in prohibition phrasing (count parity 2==2), and no `--tier`/`--intent` token survives anywhere across the five inspected surfaces.

## Anchored conclusion (AC3.9)
The protocol chain is continuous and unbroken. The task protocol PRODUCES the diagnostic call with the canonical wire shape (H2, T1:215). The troubleshoot protocol PRODUCES the `return-contract.yaml` artifact conditionally on that same caller token (H4 at P1:148/471/481; H5 at P1:471/481). The task protocol then CONSUMES that artifact via its `recommended_escalation`/`status`/`remediation_target` branch keys (H6, T1:222–230). Producer → artifact → consumer all resolve against the same `caller=task-unified` contract with no seam. Conclusion cites only H2/H4/H5/H6 anchors as required.

## Verdict
PASS — all of AC3.1 through AC3.9 satisfied.
normalized_observation_digest: cf4ead44b9029fbf70b1976594630ff7edb7605281a76a87710b39dabef21108
