---
topic: "Design how /sc:reflect could replace its own Tier 2 review mechanism with the review panel built for /sc:spec-panel under issue #346, generalized into a shared review model (pre-execution first, post-execution later)"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-11T18:33:00Z
checkout_sha: ec259f1b718ccdb9f08bba0237bfa47b2b7601a2
---

# Seed Brief: reflect-tier2-panel-replacement

Socratic dialogue was answered by the worker from the brief text and files (no live human). Each answer that is an assumption is tagged `[ASSUMPTION A-n]` and collected in the last section. Citations are `path:line` for lines read in this session; anything not read is marked UNVERIFIED. Paths are relative to `src/superclaude/` unless they start with `.dev/`.

## Problem Statement

`/sc:reflect` Tier 2 (T2) reviews a plan or finished work with 2-3 reviewer agents of different model classes, blind-calibrates each reviewer card, merges the cards with an `/sc:adversarial` debate, and ends in an evidence-validator gate (skills/sc-reflect-protocol/SKILL.md:587, 592, 600, 633-666). Issue #346 built a separate review panel for `/sc:spec-panel`: a template-driven reviewer pool with model tiers, deterministic parallel resolution, a typed findings format, a deterministic merge with a ledger and rounds (cli/review/panel.py, findings.py, ledger.py). The owner wants one shared review model, with reflect's T2 moved onto it, pre-execution mode first (it runs as an advisory step on every `/sc:workflow` plan, skills/sc-workflow-protocol/SKILL.md:60-64) and post-execution audit later.

The design must say what the panel can take over, what it lacks, what stays in reflect, how reflect's findings fit the panel's format, whether the debate merge survives, which engine runs the reviewers, how the 1.8.0 return contract stays stable, what it costs, and what to measure first.

## Known Context

Reflect T2 today (read):
- Reviewer rotation: 2 reviewers sonnet+haiku, 3 reviewers add qwen/kimi/deepseek else opus, personas analyzer/qa/refactorer; all spawned as the fixed read-only `reflect-reviewer` agent (skills/sc-reflect-protocol/SKILL.md:596-610; refs/reviewer-spec.md:84-110). The agent has `model: sonnet`, `maxTurns: 50`, plan mode, no Bash/Edit/Write/Task (agents/reflect-reviewer.md, read in full).
- Executor-class exclusion, N=2 floor, `executor_exclusion_degraded`, fail-open on unknown executor (SKILL.md:600-602).
- Brief has exactly three sections: T1 card excerpt, Grounding hunks (first line is the codegraph run state), Coverage slice (refs/reviewer-spec.md:33-78).
- Merge: `/sc:adversarial --compare` with a judge class different from the reviewers (SKILL.md:633-657; refs/reviewer-spec.md:112-116). Null `convergence_score` and `merge_method` rules, EV-1 on-disk check, EV-2 legal values (SKILL.md:659-666, 789).
- Return contract 1.8.0, 9.1 stable block, 9.3 consumer map, 9.4 additive-only rule for minor versions (SKILL.md:676-970).
- Promotion gate condition 9: `tier_reached == 2` with null convergence blocks promotion (SKILL.md:1483).
- Headless CLI path: swarm `reflect-review` lens, `default_workers=3`, models from the `T2Model0N` env pool, next command `/sc:adversarial --compare ... --suspect-source ...` (cli/swarm/lenses/reflect_review.py:33-72); `run_tier2_ensemble` dispatches, runs a bounded fallback ladder, reduces, runs the adversarial scorer in a restricted ClaudeProcess, and builds the contract (cli/reflect/ensemble.py:296-511, 722-835).
- The headless contract builder sets `merge_method` to `adversarial` when 2 or more reviewers succeeded, hard-codes `verification_ran: false` with skip reason `no-verification-stage`, `citations_dropped: 0`, and leaves the deviation booleans clean unless the scorer supplies them (cli/reflect/ensemble.py:772-832).
- The wrapper maps contract to verdict in fixed order blocked, degraded, halted, pass; degraded triggers include non-full model diversity, single vendor, `adversarial_unavailable`, `single-reviewer-fallback`, null convergence, convergence below 0.80, and any dropped citation (cli/reflect/contract.py:224-358).
- Diversity helpers: `full` needs 2+ distinct model ids; vendor is single/multi/None (cli/reflect/_diversity.py:8-61).
- Cost profile v1.0.0: T2 35k-70k Claude tokens plus 10k-25k auggie, 480-900 s; hard kill 1.25x (refs/cost-profile.yaml:46-70).

Panel (read):
- Panel schema `review-panel/1` with slots, tiers, count 1..4, strategies fixed/random/round_robin, one fixed anchor, `distinct_across_slots`; deterministic resolution keyed on a run id; template and tier hashes recorded (cli/review/panel.py:25-27, 64, 147, 277-427).
- Packaged templates: `default` (1 fixed tier1b + tier2 + 2 tier3) and `live7` (7 reviewers) (cli/review/data/review-panel.*.json; docs/reference/review-panel-live7.md:5-15).
- Anthropic-only environment replaces non-Sonnet tiers with Haiku stand-ins; gateway environment uses the tier lists (docs/reference/review-panel-live7.md:19, 28-34).
- findings-v1: JSON lines, anchors are quotes from one document, no file:line, no confidence, no deviation class, no coverage rows (cli/review/findings.py:14-196). Matching uses whitespace-flattened quote location, section, fingerprint, span overlap (findings.py:276-413).
- Ledger: rounds, clusters, `confidence` single/overlap, statuses, verdict PASS/FAIL, decision PASS/REVISE/ESCALATE, cap 3, refuses a round with no valid findings block (cli/review/ledger.py:200-298, 301-372, 408-494; merge_cmd.py read in full).
- Review-loop rules: grading by consequence, 3 reviews / 2 fix cycles, reviser contract, the panel section of the prompts file (commands/spec-panel.md:256-264; rules/prompts/document_review_loop_prompts.md:68-74).

Evidence (read):
- PN1 panel on specs fixes 15.7 of 44 ledger defects against 2.8 for baseline (p 0.003) at about 408k loop tokens, 7.6x the baseline; 71% of those tokens are the Haiku stand-in lane, 26% the primary lane, 3% a Fable adjudicator, now forbidden (.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:19, 55-68; p18/debate/BRIEF.md:55-64). 1S+6H gained about 3 fixed defects over 1S+3H on one spec (docs/reference/review-panel-live7.md:19-26).
- The panel gain is measured on specs, one spec, Haiku stand-ins. Reflect T2's benefit is not measured (brief).
- Six recorded reflect pre-execution runs under the phase5 bundle: five reached T2, all with merge_method adversarial and convergence 1.0 or 0.97; artifact sizes 221k-372k bytes; model diversity degraded in two and vendor diversity single in all five; citations dropped 0-3 (counted from the six return-contract.yaml files; sizes from `du`). One run stopped at T1.

## Constraints

- Design only. No edits under src/, tests/, docs/, plugins/. Only the brainstorm folder is written.
- Reflect return contract 1.8.0 stays stable: map new outputs onto `merge_method`, `convergence_score`, null-score rules and gate condition 9, or plan a versioned change with every consumer (SKILL.md:945-970).
- Reflect keeps code grounding, coverage mapping, deviation classification, tier rubric, remediation, promotion.
- Blind calibration and the evidence-validator gate stay unless a replacement grounds at least as strongly.
- Installed primitives never hardcode `src/superclaude` paths in the proposed design.
- Model ceiling: Fable and Tier 0 forbidden; Opus only sparingly (p18/debate/BRIEF.md:63-64).

## Success Criteria

- At least 3 candidate architectures including "leave reflect as is".
- A chosen architecture with reasons, answers to Q1-Q7, adapter sketches for pre and post, a staged migration with pre-execution behind a flag first, a 1.8.0 contract mapping, a cost model, main risks, a first measurement.
- Every claim tagged with a path:line read in this session or marked UNVERIFIED.

## Open Questions

- Does the debate add anything beyond what deterministic matching gives, given recorded convergence of 1.0 in 4 of 5 T2 runs? (Evidence is thin: 6 runs.)
- Does reflect T2 have measurable benefit at all (not measured)?
- How do reviewer cards cite code across files when the panel matcher assumes one document?
- Which of Q1-Q7 need the owner? Only one candidate: migrate at all versus measure first (see assumption A-1).

## Assumptions (Socratic answers made by the worker)

- [ASSUMPTION A-1] The owner wants a design, not a decision to ship; "measure first" is acceptable as the first stage.
- [ASSUMPTION A-2] "Shared review model" means one finding schema, one dispatch layer and one merge/ledger layer used by both spec-panel and reflect, with command-specific briefs, graders and gates on top.
- [ASSUMPTION A-3] Pre-execution reflect reviews a plan (tasklist) against its source spec; its findings cite plan lines and spec lines, which are two documents, not source code. Post-execution findings cite source files and diff hunks.
- [ASSUMPTION A-4] Calibrated confidence per card is reflect's own number and must remain a per-finding field, not replaced by the panel's single/overlap label.
- [ASSUMPTION A-5] Token cost is measured in output tokens, as in the 346 experiments; input and auggie tokens are not counted there.
- [ASSUMPTION A-6] No live owner decision is needed to proceed; no `orca orchestration ask` was sent.

## Enrichment Context

Source: `mcp__litellm__augment_code-augment_code_search` on branch `master` (quality_tier: primary). Full notes: `enrichment/codebase-context.md`.

- Reflect T2 has two engines: an agent-session path (skill, `reflect-reviewer` agents, `/sc:adversarial`, evidence-validator) and a headless swarm path (`cli/reflect/ensemble.py`) whose contract builder emits only a subset of 1.8.0 and hard-codes `verification_ran: false` and `citations_dropped: 0` (ensemble.py:808-817, Read).
- Consumers that must not change: `sc:workflow` Wave 4 reads only `reflect_status` and `reflect_report_path`; sprint/wrapper verdict map reads `merge_method`, `adversarial_convergence_score`, diversity fields and `citations_dropped`; promotion gate condition 9 reads null convergence at T2.
- Field-name drift to preserve: contract field is `adversarial_convergence_score` (SKILL.md:787; contract.py:299), prose and gate say `convergence_score` (SKILL.md:659-663, 1483).
- Six recorded pre-execution runs: convergence 1.0 in 4 of 5 T2 runs, 0.97 in one; vendor diversity single in all 5; citations dropped in 3 of 5; artifacts 221k-372k bytes. Small sample, not a quality measure.
- Panel gaps against reflect: no executor-class input, single-document anchors, no confidence/class/coverage fields, no evidence gate, no calibration.
- Cost anchors: PN1 408k loop output tokens (71% parallel Haiku stand-in lane); reflect T2 design 35k-70k Claude tokens, observed artifacts 55k-93k tokens per the brief.
