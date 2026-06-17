# TEST E3 — Protocol-Chain Resolution (rerun v2, run-3 of 3)

Independent read-only re-execution. Worktree: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`. `LC_ALL=C`.

Files: T1=`src/superclaude/skills/sc-task-protocol/SKILL.md`, P1=`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, C1=`src/superclaude/commands/troubleshoot.md`.

## Probes

### H1 (AC3.1) — caller writes context.yaml — EXIT 0
`rg -n "Write context to .\{output_dir\}/context\.yaml" $T1`
```
205:4. Write context to `{output_dir}/context.yaml` — this file is the `{context_path}` passed to the diagnostic backend in Step 3.
```

### H2 (AC3.2) — exact diagnosis-only invocation shape — EXIT 0
`rg -nF "/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}" $T1`
```
215:6. Invoke: `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` ... Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY ...
```

### H3 — "Pass NO --fix" present — EXIT 0
`rg -n "Pass NO .--fix" $T1` → matches T1:215 (same line).

### H4 (AC3.3) — backend gates emit on caller=task-unified — EXIT 0
`rg -nF "When \`caller=task-unified\`, mark Wave 5 to emit \`return-contract.yaml\`" $P1` → P1:148.
`rg -n "return-contract" $P1` → P1:148, 471 (Wave 4.5 emit), 479, 481.

### H5 (AC3.3) — return-contract path returned — EXIT 0
`rg -n "Emit TFEP return-contract|return-contract\.yaml.*written and its path returned" $P1`
```
471:4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** ...
481:**Exit criteria**: ... When `caller=task-unified`, `return-contract.yaml` is written and its path returned.
```

### H6 (AC3.4) — six-branch consumer ladder + first-match-wins — EXIT 0
`rg -n "first match wins|test_is_wrong == true|remediation_target == .docs.|status == .success.|recommended_escalation == .none.|recommended_escalation == .retry.|recommended_escalation == .escalate_depth.|recommended_escalation == .halt." $T1`
```
222:Evaluate the branches top-to-bottom, first match wins; the asymmetric-cost gates (`test_is_wrong`, `remediation_target == "docs"`) are checked first.
224:- If `test_is_wrong == true`: ...
225:- If `remediation_target == "docs"`: ...
226:- If `status == "success"`: ...
227:- If `recommended_escalation == "none"`: ...
228:- If `recommended_escalation == "retry"`: ...
229:- If `recommended_escalation == "escalate_depth"`: ...
230:- If `recommended_escalation == "halt"` (or `status == "failed"`): **FULL STOP** ...
```
All six canonical branch keys present AND the "first match wins" precedence note present → `branch_keys_all_present: true`.

### H7 (AC3.5) — escalation_count increment + FULL STOP — EXIT 0
`rg -n "increment .escalation_count.|FULL STOP" $T1` → T1:213, 228, 229, 230, 270.

### H8 (AC3.6) — depth ladder by trigger ordinal — EXIT 0
`rg -n "1st TFEP trigger|2nd TFEP trigger|systemic failure OR ≥3 new failing tests|3rd TFEP trigger|--depth standard|--depth deep" $T1` → T1:210-215, 229, 268-270.

### H9 (AC3.7) FALSIFICATION — every --fix is a prohibition — EQUAL
`TOTAL=$(rg -c -- "--fix" $T1); PROHIB=$(rg -c "NO .--fix|Pass NO .--fix|with NO --fix" $T1); echo "FIX_TOTAL=$TOTAL FIX_PROHIBITION=$PROHIB"`
```
FIX_TOTAL=2 FIX_PROHIBITION=2
```
The two lines containing `--fix` (T1:215 "Pass NO `--fix`", T1:239 "with NO --fix") each also carry an explicit prohibition phrase → counts EQUAL. No positive `--fix` pass-through exists in task-protocol.

### H10 (AC3.8) FALSIFICATION — zero residual --tier/--intent — EXIT 1 (no matches = 0)
`rg -c -- "--tier|--intent" $T1 $C1 $P1 src/superclaude/commands/task.md src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` → no output, exit 1 → `tier_intent_count: 0` across all five surfaces.

## Findings

Every deterministic gate passed on independent re-execution. The TFEP wire is fully connected and one-directional for remediation ownership: task-protocol (the caller) materializes the caller brief at `{output_dir}/context.yaml` (H1), then invokes the diagnostic backend with the exact `--caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` shape and an explicit `Pass NO --fix` (H2/H3). The backend conditionally arms the contract emission strictly on `caller=task-unified` (H4, P1:148→471) and guarantees the contract is written and its path returned at its exit criteria (H5, P1:481). The caller then routes the returned 7-field contract through a top-to-bottom, first-match-wins six-branch ladder with the asymmetric-cost gates checked first (H6), incrementing `escalation_count` on retry/escalate and hard-stopping on halt/failed/3rd-trigger (H7), with depth selected by trigger ordinal (H8). Both falsification gates hold: diagnosis-only is airtight (no positive `--fix` in task-protocol, H9 equal counts) and the legacy `--tier`/`--intent` flag surface is fully removed (H10 zero).

## Anchored conclusion (AC3.9, JUDGMENT)

The protocol chain resolves end-to-end with no break in the wire. The invocation contract (H2, T1:215) names exactly the parameters the backend gates on (H4, P1:148/471) and the backend's exit criteria guarantee the return value the caller's ladder consumes (H5, P1:481 → H6, T1:222-230). Caller-emit-consumer is therefore continuous and self-consistent — the command emitted upstream is the command honored downstream, and the contract emitted downstream is the contract routed upstream.

## Verdict: PASS

normalized_observation_digest: 18f526d247a6361e990aef5d7eff2b77a80d048146cdc06d7f550f46d5cd978d
