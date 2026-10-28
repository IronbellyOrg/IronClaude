# C — Adversarial Review State (resume analysis)

Status: COMPLETE (read-only analysis, 2026-10-23)
Root: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/` (ROOT below)
Session: `bbddbf85-99f2-4caf-a47f-a402da4f09de`

## 0. Headline

**The merge was finished but never saved.** The dedicated merge-executor (`agent-amerge-causal-analysis-d93f8889e87132e1`, spawned 05:48:10Z, custom type `merge-executor`) returned the complete text of BOTH missing files at 05:54:05Z. It wrote nothing to disk by design ("Parent persists the two complete bodies below"). The parent session then died before persisting them. Most likely cause: the returned body was ~47.8 KB (435 lines), and it landed on top of an already-loaded 76 KB transcript, a 76 KB base-selection file and a 98 KB score manifest. (This is an inference, not verified.)

Resume does not need a new debate and does not need a new merge. It needs: extract → persist → validate on disk → write return contract → update run-evidence.

## 1. Hypotheses (one line each)

| # | Card | One line |
|---|---|---|
| H1 / V1 | `synthesis/hypothesis-01.md` | Checks prove less than the requirement: they confirm format, labels or presence, not behavior, so a later reviewer finds a defect that was already there. |
| H2 / V2 | `synthesis/hypothesis-02.md` | Local repairs miss connected effects: a fix is checked only against the reported symptom and introduces a new fault or leaves a sibling path broken. |
| H3 / V3 | `synthesis/hypothesis-03.md` | Review contracts change during the loop: criteria are softened or restored, hardening is treated as required, or installed policy changes mid-run, which causes reversals and extra reviews. |
| H4 / V4 | `synthesis/hypothesis-04.md` | Brittle evidence and provenance handoffs: proof or change attribution is lost or wrong, so review rejects work whose delivery did not regress. |
| H5 / V5 | `synthesis/hypothesis-05.md` | Late feasibility and repair-authority checks: work is resubmitted with a known blocker it cannot produce evidence for or is not allowed to fix, so review correctly fails again. |

The variant copies `adversarial/variant-N-original.md` are byte-identical to the cards. `cmp` was run and the SHA256 values match `input-manifest.json`.

## 2. Current ranking and scores

**Causal order (provisional, NOT consensus)** (refactor-plan.md:27-35; debate-transcript.md:477-486):
1. V1 Checks prove less → 2. V3 Contracts change → 3. V2 Connected repair effects → 4. V5 Feasibility/authority → 5. V4 Proof/provenance

Round 2 final orders from each advocate (debate-transcript.md:478-484):
| Advocate | Order |
|---|---|
| V1, V2 | V1 > V2 > V3 > V4 > V5 |
| V3 | V1 > V3 > V2 > V4 > V5 |
| V4, V5 | V1 > V3 > V2 > V5 > V4 |

**Writing-base scores. These are not causal likelihood** (base-selection.md:142-150):
| Variant | Quant | Qual (MET/30) | Combined |
|---|---:|---:|---:|
| V4 | 0.920673 | 25/30 | **0.877003** (selected base) |
| V5 | 0.880495 | 26/30 | 0.873581 |
| V2 | 0.907692 | 25/30 | 0.870513 |
| V3 | 0.890385 | 25/30 | 0.861859 |
| V1 | 0.893750 | 24/30 | 0.846875 |

The V4/V5 gap of 0.0034 is below the 0.05 tie threshold. The tiebreak went through wins (1:1), then correctness (5:5), then input order, which selected V4 (base-selection.md:150-155). Forward and reverse qualitative passes agreed on 150 of 150 decisions (base-selection.md:126-135).

## 3. Consensus and dissent

**Consensus:**
- Writing/synthesis convergence was 10 of 10 debate points, alignment 1.0, against a threshold of 0.80. All three taxonomy levels were covered (debate-transcript.md:468-473).
- The point winners were C-002→V3, C-003→V2, C-004→V1, C-005→V5 and C-007→V4. S-001, S-002, C-001, C-006 and A-001 were SHARED (debate-transcript.md:455-466).
- All five advocates place V1 first.
- A-001 comparison rule was accepted: explanatory reach first, direct transition evidence second, with conditional overrides and no probabilities (refactor-plan.md:9).
- Invariant probe: 6 of 6 HIGH assumptions were ADDRESSED and 0 were unaddressed. The gate PASSED for the writing synthesis only (invariant-probe.md:18-20, 68-72).
- The five causes can coexist. There were 0 strict contradictions (diff-analysis.md:40-43).

**Dissent (unresolved; must be preserved):**
- V3 above V2 has 3 of 5 support, and V4 above V5 has 3 of 5. Neither reaches the two-thirds threshold of 4 of 5 (invariant-probe.md:8; debate-transcript.md:486).
- Causal-order consensus was NOT reached (debate-transcript.md:473).

## 4. Adversarial steps: complete vs incomplete

| Step | Status | Evidence |
|---|---|---|
| Prerequisites + input manifest | DONE | input-manifest.json, run-evidence.md:9-10 |
| Step 1 Diff analysis | DONE | diff-analysis.md (10 debate points, 5 unique contributions, A-001 promoted) |
| Step 2 Round 1 (5 parallel) | DONE | debate-transcript.md:14-245 |
| Step 2 Round 2 (sequential rebuttals) | DONE | debate-transcript.md:246-445 |
| Step 2 Round 2.5 invariant probe | DONE | invariant-probe.md |
| Step 2 Round 3 | Intentionally NOT run. Convergence 1.0 ≥ 0.80 and no HIGH unaddressed | debate-transcript.md:449-450 |
| Step 3 Scoring and base selection | DONE (V4) | base-selection.md, score-source-manifest.json |
| Step 4 Refactor plan + independent review | DONE, review PASS, auto-approved | refactor-plan.md:102-109; plan-review-evidence.md |
| Step 5 Merge execution | COMPOSED, NOT PERSISTED | executor final record, see §6 |
| Step 5 Post-merge on-disk validation | NOT DONE | the executor's merge-log Summary itself says "Post-merge on-disk validation: PENDING" |
| Return contract | NOT WRITTEN | — |
| run-evidence.md final update | STALE. It still says debate/merge/contract "Pending" | run-evidence.md:12-20 |

## 5. Missing expected outputs

Expected outputs per protocol FR-005 (SKILL.md:371-385) and Step 5 (SKILL.md:311-328, 2058-2080):

| Expected | Path | State |
|---|---|---|
| Merged artifact | `ROOT/merged-root-cause-analysis.md` | MISSING on disk. Full body exists in the executor transcript |
| Merge log | `ROOT/adversarial/merge-log.md` | MISSING on disk. Full body exists in the executor transcript |
| Return contract | no fixed filename in the protocol; it is MANDATORY even on failure (SKILL.md:425-445) | MISSING |
| Final run evidence | `ROOT/run-evidence.md` | STALE |
| Final ranked report (research-task level) | `RESEARCH-REPORT-review-loops.md` is a 2.6 KB stub; `synthesis/synth-04-options-recommendation.md` is referenced by the task file but does not exist | MISSING / downstream of the merge |

## 6. Inputs needed to finish the merge (no re-debate)

**Source of the composed bodies:**
`/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-amerge-causal-analysis-d93f8889e87132e1.jsonl`. The last line (physical record 71, timestamp 2026-10-23T05:54:05.390Z) is an assistant text block of 435 lines.

Inside that text:
- Lines 7/241 hold the `===== BEGIN/END FILE: .../merged-root-cause-analysis.md =====` markers. The body is wrapped in a ```` ```markdown ```` fence at lines 9 and 239, so the **content is lines 10-238**.
- Lines 243/433 hold the `===== BEGIN/END FILE: .../adversarial/merge-log.md =====` markers. The fence is at lines 245 and 431, so the **content is lines 246-430**.

Extraction (read-only until the final redirect into the target paths):
```bash
S=/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-amerge-causal-analysis-d93f8889e87132e1.jsonl
tail -1 "$S" | jq -r '[.message.content[]|select(.type=="text")|.text]|join("")' > /tmp/merge-final.txt
grep -n -E '===== (BEGIN|END) FILE|^```' /tmp/merge-final.txt   # expect 7,9,239,241,243,245,431,433
sed -n '10,238p'  /tmp/merge-final.txt > ROOT/merged-root-cause-analysis.md
sed -n '246,430p' /tmp/merge-final.txt > ROOT/adversarial/merge-log.md
```

The composed merged doc has headings: Scope and Comparison Rule, Comparative Ordering, Five Candidate Accounts (5 H3s), Event-to-Mechanism Comparison, What a Later Pass Actually Establishes, How to Distinguish These Causes, Evidence Provenance and Availability, Limits and Remaining Questions, Summary. Its ordering table matches the plan (V1>V3>V2>V5>V4) and it states both dissents. The merge-log reports 8 of 8 changes applied, 0 failed, 0 skipped, and a source guard PASS (29 links resolved).

**Then, still without re-debating:**
1. Run an independent on-disk post-merge validation per SKILL.md:2021-2056: heading hierarchy, internal refs, contradiction re-scan. Add the refactor-plan.md:77 checklist: 5 candidates present, ordered table plus both dissents, no percentages, no cure claims, endpoint labels, provenance tags, and links resolved against the ORIGINAL `synthesis/` directory. Record the result in merge-log.md "Post-Merge Validation", which currently says PENDING.
2. Write the return contract (SKILL.md:431-443). Proposed values:
   - `merged_output_path`: ROOT/merged-root-cause-analysis.md
   - `convergence_score`: 1.0 (writing synthesis only)
   - `artifacts_dir`: ROOT/adversarial
   - `status`: `partial`. The causal order is non-consensus, and SKILL.md:2115 makes the status partial on non-convergence or warnings. Use `success` only if the team decides causal-pair dissent is not a "conflict".
   - `base_variant`: variant-4-original (current-model default; no model:persona)
   - `unresolved_conflicts`: 0 diff points, plus a note listing the 2 disputed causal pairs
   - `fallback_mode`: false (the named-call rejection was retried without an N-1 fallback, debate-transcript.md:11)
   - `failure_stage`: null
   - `invocation_method`: skill-direct
   - `unaddressed_invariants`: []
3. Update run-evidence.md sections "Actual Debate and Scoring", "Merge and Final Validation" and "Final Contract and Paths".
4. Downstream (research task Step 5.11+): build the ranked conclusion and RESEARCH-REPORT from the merged file. Do not re-read the debate corpus.

**Pre-flight guards to recheck (cheap):**
- The SHA256 of the 5 cards still matches input-manifest.json.
- refactor-plan.md is unchanged (canonical SHA `7fa61164...`, plan-review-evidence.md:4).
- The fresh canonical plan review `agent-a815d047710b89c22` PASS, cited in the merge dispatch prompt, satisfies the "additional canonical-disk review" requested at plan-review-evidence.md:74.

## 7. Protocol resume support

- **Single-run Mode A has no step-level resume.** The only resume mechanism is `--pipeline-resume`, which belongs to Meta-Orchestrator pipeline mode. It reads `pipeline-manifest.yaml`, checksums the artifacts and re-runs from the first incomplete phase (SKILL.md:341, 2819-2851). This run was plain Mode A with no pipeline manifest, so `--pipeline-resume` would STOP with "No pipeline manifest found" (SKILL.md:2845).
- **What the protocol does support:** Step 5's inputs are only "Base variant + refactor-plan.md" (SKILL.md:313; dispatch input SKILL.md:1970-1972). On merge failure it says "Preserve all artifacts... Provide refactor-plan.md for manual execution" (SKILL.md:416-418, 1988-1992). Re-running only Step 5 from existing artifacts is therefore in-protocol, and persisting the already-composed output is cheaper still.
- **Do NOT re-invoke `/sc:adversarial` from scratch.** That would regenerate Steps 1-4 and the full debate.
- Return contract write-on-failure is mandatory (SKILL.md:445). It is owed regardless of the outcome.

## 8. Context-pressure files and how to read them

| File | Size | Advice |
|---|---|---|
| Executor final record (in the 1.2 MB jsonl) | 47.8 KB text | Never let it land in the main context. Extract it with `jq`/`sed` in Bash straight to disk (§6). Check only the marker lines. |
| `adversarial/score-source-manifest.json` | 98 KB / 2298 lines, 300 claim/evidence/verdict records | Not needed for the merge. If needed, use `jq` for `.selection`, `.combined`, `.top_two` only. |
| `adversarial/base-selection.md` | 76 KB / 577 lines | Read only lines 1-36 and 110-172 (scores, tiebreak, base, causal comparison). Lines 173-563 are raw forward/reverse passes; skip them. |
| `adversarial/debate-transcript.md` | 76 KB / 489 lines | Read only lines 1-13 and 446-489 (metadata, matrix, convergence, dissent). Lines 14-445 are verbatim advocate text; skip them or delegate to a subagent. |
| Parent session jsonl | 10.9 MB | Do not read. Use grep/jq only. |
| `TASK-RESEARCH-...md` | 181 KB | Read only the Step 5.11+ item ranges (around lines 305-410). |

For on-disk validation, delegate to one fresh subagent (rf-qa or evidence-validator) with only these inputs: the merged file, merge-log, refactor-plan.md and the 5 cards. Keep the parent to paths and verdicts.
