# TEST E3 — Protocol-Chain Resolution (RE-RUN v2, run-1)

Read-only validation of the TFEP (Test-Failure Escalation Protocol) chain between
`sc-task-protocol` (T1), `sc-troubleshoot-protocol` (P1), and `troubleshoot.md` (C1).

- T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
- P1 = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- C1 = `src/superclaude/commands/troubleshoot.md`
- Env: `LC_ALL=C`

---

## H1 — context.yaml write (AC3.1)
Command: `rg -n "Write context to .\{output_dir\}/context\.yaml" $T1`
Stdout:
`205:4. Write context to `{output_dir}/context.yaml` — this file is the `{context_path}` passed to the diagnostic backend in Step 3.`
EXIT=0

## H2 — exact /sc:troubleshoot invocation shape (AC3.2)
Command: `rg -nF "/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}" $T1`
Stdout: matched at line 215 (full Invoke bullet incl. "Pass NO `--fix`").
EXIT=0

## H3 — NO --fix prohibition present (supports AC3.7)
Command: `rg -n "Pass NO .--fix" $T1`
Stdout: matched at line 215.
EXIT=0

## H4 — return-contract gating on caller=task-unified (AC3.3)
Command: `rg -n "return-contract" $P1`
Stdout lines: 148 (Wave 0: mark Wave 5 to emit return-contract.yaml when caller=task-unified),
471 (Wave 5 step 4.5 Emit TFEP return-contract conditional), 479 (footer path), 481 (Exit criteria).
H4a exact-fixed probe matched line 148. EXIT=0

## H5 — return-contract emit + return statement (AC3.3)
Command: `rg -n "Emit TFEP return-contract|return-contract\.yaml.*written and its path returned" $P1`
Stdout lines: 471, 481. EXIT=0

## H6 — consumer branch ladder, all six keys + first-match-wins (AC3.4)
Command: rg over the 8-alternation pattern on $T1.
Stdout lines 222-230: 222 "first match wins" precedence note; 224 test_is_wrong==true;
225 remediation_target=="docs"; 226 status=="success"; 227 escalation=="none";
228 escalation=="retry"; 229 escalation=="escalate_depth"; 230 escalation=="halt".
All six canonical branch keys + first-match-wins note present. branch_keys_all_present=true. EXIT=0

## H7 — escalation_count / FULL STOP machinery (AC3.5)
Command: `rg -n "increment .escalation_count.|FULL STOP" $T1`
Stdout lines: 213, 228, 229, 230, 270. EXIT=0

## H8 — trigger->depth mapping (AC3.6)
Command: rg over trigger/depth alternation on $T1.
Stdout lines: 210 (1st→standard), 211 (2nd→deep), 212 (systemic/≥3→deep),
213 (3rd→FULL STOP), 215, 229, 268-270. EXIT=0

## H9 — FALSIFICATION: --fix usage all prohibited (AC3.7)
Command: TOTAL=rg -c -- "--fix" $T1 ; PROHIB=rg -c "NO .--fix|Pass NO .--fix|with NO --fix" $T1
Stdout: `FIX_TOTAL=2 FIX_PROHIBITION=2` — both --fix occurrences (lines 215, 239) are
prohibition contexts. FIX_TOTAL == FIX_PROHIBITION. EXIT=0

## H10 — FALSIFICATION: zero --tier/--intent tokens (AC3.8)
Command: `rg -c -- "--tier|--intent" $T1 $C1 $P1 src/superclaude/commands/task.md src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
Stdout: (empty). EXIT=1. Per-file recheck: all 0. tier_intent_count=0.

---

## Findings

The TFEP protocol chain resolves end-to-end with no breaks. Producer side (T1):
Step 4 writes diagnostic context to {output_dir}/context.yaml (H1, line 205); Step 6
invokes the troubleshoot backend with the precise parameterized shape
`--caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}`
and explicitly passes NO --fix (H2/H3, line 215). Backend side (P1): caller=task-unified
is captured in Wave 0 (H4, line 148) and gates Wave 5 step 4.5 to emit
<output-dir>/return-contract.yaml, with exit criteria (line 481) confirming the contract
is written and its path returned only under that caller (H4/H5). Back on the producer
side, the consumer branch ladder (H6, lines 222-230) evaluates all six canonical branch
keys top-to-bottom under an explicit "first match wins" rule, asymmetric-cost gates first.
The escalation machinery (H7) and trigger->depth mapping (H8) are complete and consistent.

Both falsification probes hold: H9 shows every --fix token in T1 is inside a prohibition
clause (FIX_TOTAL == FIX_PROHIBITION == 2); H10 confirms --tier/--intent are fully absent
across all five chain files (count 0 everywhere).

## AC3.9 — Chain-continuous conclusion [JUDGMENT, anchored]

Citing only H2, H4, H5, H6: the chain is continuous. The producer's invocation edge (H2)
hands --caller task-unified plus --context/--output-dir/--depth to the backend; that same
caller token is the gate (H4) arming the backend to emit return-contract.yaml; the backend
exit contract (H5) guarantees the file is written and its path returned; the producer then
consumes that contract through a deterministic first-match-wins branch ladder over all six
return-contract keys (H6). Every link — invocation in, contract gated, contract
emitted/returned, contract consumed — is anchored to a concrete line match with no missing
hop. The chain is resolved and unbroken.

## Verdict

PASS — All acceptance criteria AC3.1–AC3.9 satisfied.
normalized_observation_digest = 18f526d247a6361e990aef5d7eff2b77a80d048146cdc06d7f550f46d5cd978d
