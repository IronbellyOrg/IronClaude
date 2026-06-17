# E3 — Protocol-Chain Resolution (rerun v2, run-2)

INDEPENDENT, READ-ONLY validation. No edits/stages/commits. All probes re-executed under `LC_ALL=C`.

- T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
- P1 = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- C1 = `src/superclaude/commands/troubleshoot.md`

## Probes

### H1 — context.yaml emission (EXIT 0)
`rg -n "Write context to .\{output_dir\}/context\.yaml" $T1`
```
205:4. Write context to `{output_dir}/context.yaml` — this file is the `{context_path}` passed to the diagnostic backend in Step 3.
```

### H2 — exact troubleshoot invocation shape (EXIT 0)
`rg -nF "/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}" $T1`
```
215:6. Invoke: `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` ... Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY; remediation insertion and resume stay with task-protocol.
```

### H3 — NO --fix prohibition (EXIT 0)
`rg -n "Pass NO .--fix" $T1`
```
215:... Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY ...
```

### H4 — return-contract gated on caller (EXIT 0, both sub-probes)
`rg -nF "When \`caller=task-unified\`, mark Wave 5 to emit \`return-contract.yaml\`" $P1`
```
148:6. ... When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5).
```
`rg -n "return-contract" $P1` → matches at lines 148, 471, 479, 481 (gate, emit step, exit-criteria back-reference).

### H5 — contract written + path returned (EXIT 0)
`rg -n "Emit TFEP return-contract|return-contract\.yaml.*written and its path returned" $P1`
```
471:4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write `<output-dir>/return-contract.yaml` ...
481:**Exit criteria**: ... When `caller=task-unified`, `return-contract.yaml` is written and its path returned.
```

### H6 — branch ladder: all six keys + first-match-wins (EXIT 0)
`rg -n "first match wins|test_is_wrong == true|remediation_target == .docs.|status == .success.|recommended_escalation == .none.|recommended_escalation == .retry.|recommended_escalation == .escalate_depth.|recommended_escalation == .halt." $T1`
```
222:Evaluate the branches top-to-bottom, first match wins; the asymmetric-cost gates (test_is_wrong, remediation_target == "docs") are checked first.
224:- If test_is_wrong == true: Present to user for review. Do NOT auto-fix tests.
225:- If remediation_target == "docs": present to user ...
226:- If status == "success": proceed to Step 5 ...
227:- If recommended_escalation == "none": remediation ready ...
228:- If recommended_escalation == "retry": re-run /sc:troubleshoot once at SAME --depth ...
229:- If recommended_escalation == "escalate_depth": re-invoke at --depth deep ...
230:- If recommended_escalation == "halt" (or status == "failed"): FULL STOP ...
```
Per-key presence (independent count): first_match_wins=1, test_is_wrong==true=1, remediation_target==docs=2, status==success=1, escalation none/retry/escalate_depth/halt = 1 each. branch_keys_all_present = true.

### H7 — escalation_count increment + FULL STOP (EXIT 0)
`rg -n "increment .escalation_count.|FULL STOP" $T1` → lines 213, 228, 229, 230, 270.

### H8 — trigger/depth ladder (EXIT 0)
`rg -n "1st TFEP trigger|2nd TFEP trigger|systemic failure OR ≥3 new failing tests|3rd TFEP trigger|--depth standard|--depth deep" $T1` → lines 210, 211, 212, 213, 215, 229, 268, 269, 270.

### H9 — FALSIFICATION: --fix count equality
`TOTAL=$(rg -c -- "--fix" $T1); PROHIB=$(rg -c "NO .--fix|Pass NO .--fix|with NO --fix" $T1); echo ...`
```
FIX_TOTAL=2 FIX_PROHIBITION=2
```
EQUAL. Every `--fix` occurrence in T1 is a prohibition; no path passes `--fix` to the backend.

### H10 — FALSIFICATION: zero --tier/--intent (EXIT 1, no matches)
`rg -c -- "--tier|--intent" $T1 $C1 $P1 src/superclaude/commands/task.md src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
Per-file counts: T1=0, troubleshoot.md=0, P1=0, task.md=0, report-template.md=0. No legacy `--tier`/`--intent` flag leakage anywhere on the chain.

## Findings

The full TFEP producer→backend→consumer chain resolves end-to-end with no broken hop. The producer (task-protocol) writes the diagnostic context file (H1) and invokes the backend with the byte-exact wire shape (H2), explicitly withholding `--fix` (H3), and the falsification probe H9 confirms there is no hidden `--fix` path (FIX_TOTAL==FIX_PROHIBITION==2). The backend (troubleshoot) conditionally emits `return-contract.yaml` keyed on `caller=task-unified` (H4) and guarantees the path is returned (H5). The consumer ladder back in task-protocol carries all six canonical branch keys plus the documented first-match-wins precedence note (H6), wires escalation accounting and terminal FULL STOPs (H7), and maps the 1st/2nd/3rd-trigger depth ladder (H8). Legacy `--tier`/`--intent` surface area is fully retired across all five files (H10, exit 1).

## Anchored Conclusion

[JUDGMENT,anchored] The protocol chain is continuous. task-protocol emits the exact invocation `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` (H2). The troubleshoot backend gates `return-contract.yaml` emission on precisely that `caller=task-unified` value and returns its path (H4, H5). The contract's `status`/`test_is_wrong`/`remediation_target`/`recommended_escalation` fields are then consumed by the six-branch ladder with first-match-wins precedence (H6). Producer wire shape, backend gate, and consumer branch set form one closed loop with no unresolved field or dangling hop — conclusion drawn solely from H2/H4/H5/H6 anchors.

## Verdict

**PASS** — AC3.1 through AC3.9 all satisfied. normalized_observation_digest = `18f526d247a6361e990aef5d7eff2b77a80d048146cdc06d7f550f46d5cd978d`.
