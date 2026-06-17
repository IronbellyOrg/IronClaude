# TEST E3 — Protocol-Chain Resolution — run-2

Independent read-only re-execution. LC_ALL=C. Files:
- T1 = src/superclaude/skills/sc-task-protocol/SKILL.md
- P1 = src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
- C1 = src/superclaude/commands/troubleshoot.md

## H1 — context.yaml write (AC3.1)
Command: rg -n "Write context to .\{output_dir\}/context\.yaml" $T1
EXIT=0
    205:4. Write context to `{output_dir}/context.yaml` — this file is the `{context_path}` passed to the diagnostic backend in Step 3.

## H2 — exact invocation shape (AC3.2)
Command: rg -nF "/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}" $T1
EXIT=0
    215:6. Invoke: `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` ... Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY; remediation insertion and resume stay with task-protocol.

## H3 — NO --fix prohibition
Command: rg -n "Pass NO .--fix" $T1
EXIT=0
    215:6. Invoke: ... Pass NO `--fix` — TFEP invokes troubleshoot for DIAGNOSIS ONLY ...

## H4 — return-contract gated on caller (AC3.3)
Command: rg -n "return-contract" $P1
EXIT=0
    148:6. ... When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5).
    471:4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write `<output-dir>/return-contract.yaml` mapping the Output Contract fields to the TFEP-consumed schema: status, test_is_wrong, recommended_escalation, tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary. ...
    479:   - (if `caller=task-unified`) the emitted `return-contract.yaml` path.
    481:**Exit criteria**: ... When `caller=task-unified`, `return-contract.yaml` is written and its path returned.
Verbatim gating sentence present at P1:148.

## H5 — emit + path returned (AC3.3)
Command: rg -n "Emit TFEP return-contract|return-contract\.yaml.*written and its path returned" $P1
EXIT=0
    471:4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write ...
    481:**Exit criteria**: ... When `caller=task-unified`, `return-contract.yaml` is written and its path returned.

## H6 — six branch keys + precedence note (AC3.4)
Command: rg -n "first match wins|test_is_wrong == true|remediation_target == .docs.|status == .success.|recommended_escalation == .none.|recommended_escalation == .retry.|recommended_escalation == .escalate_depth.|recommended_escalation == .halt." $T1
EXIT=0
    222:Evaluate the branches top-to-bottom, first match wins; the asymmetric-cost gates (test_is_wrong, remediation_target == "docs") are checked first.
    224:- If test_is_wrong == true: Present to user for review. Do NOT auto-fix tests.
    225:- If remediation_target == "docs": present to user for spec/stakeholder review. ...
    226:- If status == "success": proceed to Step 5 ...
    227:- If recommended_escalation == "none": remediation ready ...
    228:- If recommended_escalation == "retry": re-run /sc:troubleshoot once at the SAME --depth ...
    229:- If recommended_escalation == "escalate_depth": re-invoke /sc:troubleshoot at --depth deep ...
    230:- If recommended_escalation == "halt" (or status == "failed"): **FULL STOP** ...
All six branch keys present, plus the first-match-wins precedence note.

## H7 — escalation_count increment + FULL STOP (AC3.5)
Command: rg -n "increment .escalation_count.|FULL STOP" $T1
EXIT=0
    213:- 3rd TFEP trigger → **FULL STOP** (report to user, no further fixes)
    228:- ... (re-enter Step 3; increment escalation_count).
    229:- ... (re-enter Step 3; increment escalation_count). If already at --depth deep ... treat as FULL STOP.
    230:- ... **FULL STOP** ... (immediate FULL STOP regardless of escalation_count).
    270:3rd TFEP trigger  → FULL STOP. Report to user. Do not attempt further fixes.

## H8 — depth-mapping ladder (AC3.6)
Command: rg -n "1st TFEP trigger|2nd TFEP trigger|systemic failure OR ≥3 new failing tests|3rd TFEP trigger|--depth standard|--depth deep" $T1
EXIT=0
    210:- 1st TFEP trigger → --depth standard
    211:- 2nd TFEP trigger (escalation) → --depth deep
    212:- systemic failure OR ≥3 new failing tests → --depth deep
    213:- 3rd TFEP trigger → **FULL STOP** ...
    215:6. Invoke: ... --depth standard for the 1st/simple TFEP trigger, and --depth deep for a systemic failure, ≥3 new failing tests, or a 2nd (escalation) trigger. ...
    268:1st TFEP trigger  → /sc:troubleshoot --caller task-unified --depth standard
    269:2nd TFEP trigger (escalation, systemic, or ≥3 new failing tests)  → /sc:troubleshoot --caller task-unified --depth deep
    270:3rd TFEP trigger  → FULL STOP. ...

## H9 — FALSIFICATION: --fix accounting (AC3.7)
Command: TOTAL=$(rg -c -- "--fix" $T1); PROHIB=$(rg -c "NO .--fix|Pass NO .--fix|with NO --fix" $T1); echo "FIX_TOTAL=$TOTAL FIX_PROHIBITION=$PROHIB"
EXIT=0
    FIX_TOTAL=2 FIX_PROHIBITION=2
Per-line: both --fix occurrences (T1:215 "Pass NO --fix", T1:239 "with NO --fix") sit inside prohibition clauses. Counts EQUAL ⇒ no un-prohibited --fix leaks into the TFEP invocation path.

## H10 — FALSIFICATION: legacy --tier/--intent eradication (AC3.8)
Command: rg -c -- "--tier|--intent" $T1 $C1 $P1 src/superclaude/commands/task.md src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md
EXIT=1 (no matches)
Per-file confirmation:
    src/superclaude/skills/sc-task-protocol/SKILL.md : 0
    src/superclaude/commands/troubleshoot.md : 0
    src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md : 0
    src/superclaude/commands/task.md : 0
    src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md : 0
All five files exist; zero legacy --tier/--intent tokens.

## Findings

Every deterministic probe lands exactly where the acceptance criteria require, and both
falsification probes hold rather than fail. The diagnosis-only contract is internally
consistent: task-protocol passes --caller task-unified with NO --fix (H2/H3), and the
--fix accounting (H9) proves no remediation flag leaks into the troubleshoot invocation —
both --fix tokens in T1 are prohibition language, not invocation. The legacy tier/intent
surface is fully eradicated across the protocol chain and its consumer command/template (H10).
On the producer side, troubleshoot-protocol conditions return-contract.yaml emission strictly
on caller=task-unified (H4 at P1:148/471) and guarantees the path is returned at exit (H5 at
P1:481). On the consumer side, task-protocol's branch table evaluates the six wire keys
top-to-bottom under an explicit first-match-wins precedence with asymmetric-cost gates first
(H6), and the escalation ladder (H7/H8) terminates deterministically at FULL STOP.

## Anchored conclusion (AC3.9)

The protocol chain is CHAIN-CONTINUOUS with no missing hop. task-protocol emits the context
file and invokes troubleshoot with the exact --caller task-unified --context {context_path}
--output-dir {output_dir} --depth {depth} shape (anchor H2, T1:215). troubleshoot-protocol
maps its Output Contract into the TFEP wire schema — status, test_is_wrong,
recommended_escalation, remediation_target — gated on caller=task-unified (anchor H4, P1:471)
and returns the contract path at exit (anchor H5, P1:481). task-protocol then consumes exactly
those wire keys in its branch table — test_is_wrong == true, remediation_target == "docs",
status == "success", recommended_escalation == none/retry/escalate_depth/halt — under a
documented first-match-wins precedence (anchor H6, T1:222-230). Producer-emitted fields and
consumer-evaluated predicates reference the same set; the resolution is unbroken end to end.

## Verdict

PASS — all acceptance criteria AC3.1 through AC3.9 satisfied.
normalized_observation_digest: 1409a638d2732284d04b19c0571305d5f59593a40eadfbcbaa06630ee490078c
