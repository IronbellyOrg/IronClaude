# Final Efficacy Report: Debug / Task / Reflect Stack

## 1. Executive verdict

Blunt verdict: the existing debug/task/reflect stack was mostly theatre for this incident chain. It produced artifacts, signoffs, and green-looking reviews, but it did not preempt the production-facing PRD runtime failures that mattered. Its net value was mainly after-the-fact organization: once live runtime exposed a miss, the stack helped frame and land targeted fixes. As a preventive quality system, it failed.

### Theatre scorecard

| Review step | Should have caught | Did catch | Theatre ratio | Verdict |
|---|---:|---:|---:|---|
| `sc:troubleshoot` | 6 | 0 | 1.000 | Full theatre for M1-M6 prevention |
| `task-builder` | 6 | 0 | 1.000 | Full theatre for acceptance-quality prevention |
| `sc:reflect-PRE` | 7 | 0 | 1.000 | Full theatre for pre-implementation gap detection |
| `sc:reflect-POST` | 7 | 0 | 1.000 | Full theatre for signoff validity |
| `adversarial` | 7 | 1 | 0.857 | Mostly theatre; caught only M7 |

Aggregate score: 33 expected catches, 1 actual catch, 32 misses. Preventive catch rate: 3.0%. Theatre ratio: 97.0%.

Net value: low-to-moderate after runtime discovery; near-zero as a pre-runtime preventive gate. The stack did help document and sequence fixes, but the decisive oracle was repeatedly live PRD execution, not the review pipeline.

## 2. The miss timeline and validated root causes

### M1 — Cloud-only `--file` flag used for local PRD spec paths

Validated root cause: the PRD pipeline treated Claude CLI `--file` as a local-path attachment mechanism, even though sibling pipelines already treated it as a cloud-download/session-token path and avoided it. Review analyzed the PRD symptom in isolation instead of checking existing CLI contracts and sibling pipeline behavior.

Surfaced by: live headless PRD runtime halted at scope-discovery with a session-token/file-download failure before downstream artifacts existed.

Fix reference: PR #151 / commit `7601ad25`, `fix(prd): deliver specs/refs inline instead of via cloud-only --file flag`.

### M2 — Parallel-instructions gate applied to the final sequential completion phase

Validated root cause: `_check_parallel_instructions` assumed every phase numbered >=2 was parallelizable work. It scanned all later phase headings and ignored the semantic distinction between work phases and final completion/presentation phases.

Surfaced by: live PRD runtime progressed past M1, then halted at build-task-file with a final phase missing parallel execution instructions.

Fix reference: PR #154 / commit `e97aa4fd`, `fix(prd): exempt sequential completion phase from parallel-instructions gate`.

### M3 — Parallel-instructions regex matched Task-Log placeholder headings as real phases

Validated root cause: the same semantic heuristic treated any Markdown heading containing `Phase N` as an executable task phase. After the final real completion phase was exempted, generated Task-Log placeholders such as `### Phase N - ... Findings` became the next false-positive halt. Review fixed the observed final-phase symptom without analyzing the full regex match domain or unmasked false positives.

Surfaced by: live PRD runtime after #154 halted again at build-task-file, now on a placeholder-like phase failure.

Fix reference: PR #155 / commit `eb9a2633` attempted to fix by making build-task-file `parallel_instructions` advisory in generic gate evaluation.

### M4 — Advisory-gate fix verified an unused evaluator instead of the live PRD executor

Validated root cause: dual gate evaluators existed. PR #155 changed and tested the generic `pipeline.gates.gate_passed` path, while PRD runtime uses `PrdExecutor._evaluate_gate`. Design, implementation, and verification targeted the artifact under design instead of the actually executed runtime path.

Surfaced by: runtime continued to halt after #155 even though tests against `gate_passed` were green.

Fix reference: local / PR #158-equivalent commit `b97c9960`, `fix(prd): honor advisory checks in the executor's _evaluate_gate (live PRD path)`.

### M5 — Verdict parser rejected decorated but well-formed Markdown verdict lines

Validated root cause: `_check_verdict_field` accepted only a few bare verdict shapes and did not model normal agent Markdown output: headings, bullets, bold punctuation, emoji, or bold-wrapped PASS/FAIL values. Reviews fixed individual gate symptoms but did not generalize to the brittle-parser class across verdict-gated QA steps.

Surfaced by: live PRD runtime reached QA gates such as research-qa and halted when a decorated verdict line like `## Verdict: PASS` or `- **Verdict:** ✅ **PASS**` was rejected.

Fix reference: local commit `07cb149f`, `fix(prd): tolerate decorated verdict lines in _check_verdict_field`.

### M6 — Resume step-ID mismatch between execution log and `prd resume` validation

Validated root cause: executable/internal PRD step IDs drifted from artifact/report names. Runtime emits and uses `research-qa`, while resume validation accepts `qa-research-gate`, apparently leaking report artifact naming into the resume-step registry. Producer and consumer do not share one canonical enum/map.

Surfaced by: live resume attempt failed with an unrecognized resume step ID when using the runtime step ID `research-qa`.

Fix reference: no committed fix found in supplied evidence. Git grep still showed executor using `research-qa` while config resume validation included `qa-research-gate`.

### M7 — Completion-signal substring matching could exempt real work phases accidentally

Validated root cause: the #154 completion-phase exemption initially used bare substring matching, so completion signal tokens such as `complete` and `present` matched unrelated words such as `incomplete` and `representation`. That could silently turn real work phases into exempt completion phases.

Surfaced by: PR review / adversarial review activity during #154, not a later live whack-a-mole halt.

Fix reference: included inside PR #154 / commit `e97aa4fd` by changing completion-signal matching to word-boundary matching.

## 3. Systemic causes

### SC1 — No runtime-contract oracle at producer/consumer and entrypoint boundaries

The stack accepted plausible artifacts, unit-level evidence, named abstractions, and generated reports as proof of runtime behavior without forcing the exact runtime contract to cross the actual producer-consumer seam. This covered M1, M2, M4, M5, and M6.

Core failure: reviewers could choose a plausible oracle instead of the decisive one. Reaching research-notes, changing a generic evaluator, seeing a report filename, or testing a local parser was treated as enough even when the real PRD path had not accepted and acted on the runtime value.

### SC2 — Semantic-classifier reviews lacked domain partition and negative-boundary obligations

The stack validated representation-shaped evidence as semantic truth: `Phase N` meant executable phase, final/max phase meant completion, neat `verdict: PASS` represented agent output, and substring matches represented intent. This covered M2, M3, M5, and M7.

Core failure: parsers, regexes, and semantic gates were reviewed as matchers rather than classifiers with positive, negative, near-miss, and provenance/context domains.

### SC3 — Scope-freezing converted first diagnoses into inherited theatre

Once troubleshoot framed the first visible symptom, later stages inherited that frame. Task-builder converted it into acceptance criteria; reflect-PRE and reflect-POST checked those criteria; adversarial challenged inside the same box. This covered M1-M6.

Core failure: no mandatory stage reopened the causal boundary, asked what downstream step would become exposed after the fix, or forced a falsifier outside the original symptom path.

### SC4 — Human-readable taxonomy substituted for executable API identity

Reviewers treated semantically plausible names as binding machine contracts: local `--file` looked like local file attachment, `gate_passed` looked like the PRD gate oracle, report names looked like resume step IDs, and prose headings looked like executable phases. This covered M1, M3, M4, M6, and M7.

Core failure: no canonical-source discipline forced owner/producer/consumer/grammar proof for behavior-controlling tokens.

## 4. Merged generalized remediation strategy

### 4.1 Runtime Boundary Contract Oracle

Principle: no behavioral signoff from plausible artifacts. A fix is accepted only when the actual runtime output, invocation, state, message, file, event, or decision produced at the relevant boundary is accepted and acted on by the intended live consumer through the same public entrypoint and execution path a real caller would use.

Mechanism:

- For every behavioral claim, declare a boundary contract: public entrypoint, producer, emitted runtime value, transport/serialization form, consumer, expected action, observable acceptance signal, and failure signal.
- Require a minimal probe that invokes the real entrypoint or real producer, captures the actual runtime output, passes that output unmodified across the real seam, and records a machine-checkable consumer acceptance signal.
- If multiple seams are implicated, require one focused probe per seam plus one full-path public-entrypoint probe.
- Static inspection, generated artifacts, report files, helper calls, renamed abstractions, mocked consumers, and unit-only tests are supporting evidence only, not signoff evidence.
- If a boundary cannot be exercised, status is downgraded through an explicit impossibility waiver; it is not marked fixed.

### 4.2 Boundary-Contract Oracle for Semantic Classifiers

Principle: any component mapping surface representation to operational meaning must be reviewed as a boundary classifier, not a matcher.

Mechanism:

- Name the decision being made.
- Enumerate input dimensions: syntax, metadata, provenance, generation source, lifecycle state, ordering, decoration, and context.
- Partition the domain into true positives, true negatives, near-miss negatives, and provenance/context negatives.
- Provide executable fixtures or documented oracle checks for every required bucket.
- Identify the semantic invariant admitting positives and excluding negatives.
- Reject evidence that proves only representation shape.

### 4.3 Boundary Reopening Contract with independent re-expansion gates

Principle: the first plausible diagnosis remains provisional until independent boundary validation proves the remedy addresses the broader failure class, adjacent contracts, downstream/upstream effects, and ways the chosen oracle could be wrong.

Mechanism:

- Trigger for systemic, cross-stage, production-facing, ambiguous-root-cause, repeated-miss, or non-trivial fixes.
- Insert an early independent gate before task construction.
- Require a boundary ledger with class generalization, exposure map, independent contract match, and counter-oracles.
- Require task acceptance criteria to include at least one check from each ledger category.
- Before final approval, verify at least one widened-boundary check, one falsification check, and one independent contract match.
- Forbid generic statements like “downstream considered” without named consumers, contracts, terminal states, or falsifiers.

### 4.4 Executable Contract Identity Ledger

Principle: machine behavior must be justified by executable contract identity, not by plausible human-readable taxonomy.

Mechanism:

For each behavior-controlling token, flag, status field, parser trigger, phase marker, or control-flow signal, require a ledger entry containing:

- owner/source of truth;
- producer/emitter;
- consumer/acceptor;
- exact accepted grammar or allowed values;
- serialization boundary;
- executable evidence source such as schema, parser, CLI help, enum, generated type, API spec, or runtime metadata;
- round-trip proof showing producer output accepted by consumer without prose translation;
- at least one reasonable-looking negative example that is rejected or non-binding.

Display text, report titles, documentation headings, comments, nearby variable names, substring matches, and similar terms cannot be accepted as executable contract evidence.

## 5. `sc:troubleshoot` refactor and would-have-caught matrix

### Refactor summary

The updated `sc:troubleshoot` refactor keeps the Boundary Reopening, Contract Identity, Semantic Classifier, and Runtime Boundary Oracle gates, but widens them into production-facing pipeline-health signoff mode.

New generalized mechanisms:

1. Reachable STRICT Gate Continuation Inventory.
2. Downstream Classifier Blast-Radius Matrix.
3. Live Call-Path and Duplicate-Evaluator Ledger.
4. Shared Parser/Gate Registry Audit.
5. Operator Recovery Round-Trip Oracle.
6. Standing Semantic Near-Miss Suites for phase/heading/classifier gates.

These trigger from topology and risk class, not PRD-specific names. For production-facing pipeline bugs, `sc:troubleshoot` may not claim success unless downstream strict gates, shared parsers, duplicate evaluators, and operator recovery paths are audited or explicitly waived as partial.

### Key protocol changes

- Add `--pipeline-health focused|continuation|full`, defaulting to `continuation` for production-facing, pipeline-like, CLI-orchestrated, multi-step, or observed-halt issues.
- Add machine-checkable output statuses: `strict_gate_inventory_status`, `downstream_classifier_blast_radius_status`, `live_call_path_ledger_status`, `shared_parser_registry_status`, and `operator_recovery_round_trip_status`.
- Add Will / Will Not rules forbidding pipeline-health success after reaching only the next artifact or local seam.
- Require topology inventories via code search and pass-oracle evidence via public CLI/runtime observation.
- Add troubleshoot-scoped agents: `strict-gate-inventory-auditor`, `downstream-classifier-blast-radius-auditor`, `live-call-path-ledger-auditor`, `shared-parser-registry-auditor`, and `operator-recovery-round-trip-validator`.
- Expand Wave 1.8 into Contract Identity + Semantic Classifier Discovery + Pipeline Continuation Inventory.
- Add Wave 1.9 for Downstream Blast-Radius and Live-Path Ledgers.
- Expand Wave 5.5 into a pipeline signoff oracle requiring continuation probes, live evaluator proof, classifier fixtures, shared parser fixtures, and recovery-token round trips.

### Would-have-caught matrix

| Miss | Would refactored troubleshoot catch it? | Mechanism |
|---|---|---|
| M1 | Yes | Boundary Reopening + Contract Identity + Runtime Boundary Oracle would require executable `--file` semantics and public PRD local-spec delivery proof. |
| M2 | Yes | Reachable STRICT Gate Continuation Inventory would identify build-task-file after M1; continuation smoke would expose final sequential phase false positive. |
| M3 | Yes | Downstream Classifier Blast-Radius Matrix would require regex-domain, provenance/context, placeholder-heading, and unmasking negatives. |
| M4 | Yes | Live Call-Path and Duplicate-Evaluator Ledger would prove PRD uses `PrdExecutor._evaluate_gate`, not generic `gate_passed`. |
| M5 | Yes | Shared Parser Registry Audit would inventory `_check_verdict_field` across QA gates and require decorated Markdown verdict fixtures. |
| M6 | Yes | Operator Recovery Round-Trip Oracle would feed emitted runtime step IDs through public resume validation and catch `research-qa` vs `qa-research-gate`. |
| M7 | Yes | Standing Semantic Near-Miss Suite would require substring/word-boundary negatives such as `incomplete` and `representation`. |

## 6. Rollback-replay result

Rollback replay result after refactor round 2: 7 of 7 misses caught.

Final coverage: 100%.

Misses still slipping after <=3 rounds: none.

Residual-gap analysis:

- No M1-M7 miss still slips under the refactored `sc:troubleshoot` protocol when applied at rollback commit `ac80f176` with production-facing pipeline-health mode enabled.
- The decisive improvement is not more generic review text; it is topology-aware signoff. The refactor requires downstream strict-gate inventory, live evaluator identity, duplicate-evaluator detection, shared parser registry coverage, semantic near-miss fixtures, and recovery round-trip validation before success.
- The remaining risk is cost and execution feasibility. Some public-entrypoint probes may be slow or depend on external services. The refactor handles this by requiring explicit impossibility waivers and downgrading status to partial, not by silently accepting artifact evidence.
- Another residual risk is waiver abuse. If teams routinely waive runtime probes, theatre returns. The anti-theatre control is that waived evidence cannot support `status: success` for production-facing pipeline bugs.

## 7. Blunt bottom line

Yes: based on the rollback replay, the refactored troubleshoot pipeline would have caught all of M1-M7 in one shot at `ac80f176`, provided it was run in production-facing pipeline-health mode and its blocking gates were enforced rather than waived.

The important caveat: static troubleshooting alone cannot prove all runtime behavior. The irreducibly un-catchable part by static analysis is whether the public entrypoint actually exercises the expected runtime path under real execution conditions: external CLI semantics, cloud/session behavior, generated agent output shape, halt/resume behavior, and downstream gate continuation. Those require a runtime/exercise mechanism.

So the final answer is not “make static review smarter.” The final answer is: static review must build the topology and contract map, then a runtime oracle must exercise the live seams. Without that runtime/exercise mechanism, the stack will keep producing convincing theatre whenever plausible artifacts diverge from actual execution.

Relevant paths:

- `/config/workspace/IronClaude/.dev/troubleshoot/meta-efficacy-pipeline/EFFICACY-REPORT.md`
- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py`
- `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py`
- `/config/workspace/IronClaude/src/superclaude/cli/prd/process.py`
- `/config/workspace/IronClaude/src/superclaude/cli/prd/config.py`
