# QA Report — Research Depth (research-depth lens)

**Topic:** sc:submit-pr MDTM task-file research depth audit
**Date:** 2026-06-11
**Phase:** research-depth
**Stance:** ADVERSARIAL — research assumed superficial until proven otherwise
**Fix authorization:** false
**Assigned files:** research/01..07 (all read end-to-end)

---

## Overall Verdict: PASS (with 3 MINOR depth caveats the builder should heed)

The research is materially DEEPER than "list filenames + use Python." It demonstrates behavioral
understanding at every pivotal seam: it captures the actual severity-remap *algorithm* (not just the
rubric's name), the *exact* gh/GraphQL surfaces (verified against live gh 2.45.0 + GitHub docs), the
*architecture decision* for the deterministic core with a live-verified hyphen-import proof, and it
honestly flags the Monitor-tool session-bound limitation rather than hand-waving it. Three spec
defects (--cov, marker registration, troubleshoot-won't-auto-apply seam) were independently surfaced
as builder warnings. This clears the depth bar for a high-quality, complex multi-subsystem task file.
The caveats below are real but do not block — none would force a builder to re-research from scratch.

---

## Items Reviewed (depth checklist, 6 items)

| # | Depth check | Result | Evidence |
|---|-------------|--------|----------|
| 1 | Deterministic-core architecture (HOW, not "use Python") — R4 pivotal | PASS | R4:13-63 gives full 7-module layout (fsm/severity/loop_guard/classifier/detection/models/run_log) with per-module ownership, the `src/superclaude/submit_pr/` (underscored) vs hyphenated-skill-dir split rationale, and the swarm-skill↔cli.swarm-package precedent (R4:131-146). Live-verified the hyphen import failure (R4:39-48). Dispositive evidence cited = spec Python test bodies; I independently confirmed at spec:905-944. |
| 2 | R3 reuse defers to rubric w/o re-implementing — actual remap algo captured | PASS | R3:40-54 captures the full 5-step pipeline (hint→category floor/ceiling table→confidence→diff-locality→cross-source bonus). I re-read severity-rubric.md:63-101 directly: R3's description is faithful, not a paraphrase — the 5 steps + the floor/ceiling semantics match the source exactly. R3:60-73 explicitly draws the grade-vs-route boundary (route map is NEW C3 logic, NOT in rubric). |
| 3 | DET probe (R6) concretely characterized — exact gh cmds + YAML fields | PASS | R6:30-71 lists 5 concrete capture steps with copy-pasteable `--repo`-pinned `gh`/`gh api` commands, each mapped to the exact contract field it fills (`augment_bot_login`, `emission_shape`, `findings_locus`, `severity_field_path`, `review_completeness_signal`, `probe_evidence`). R6:90-117 encodes it as a `needs_human_decision` HALT item with a programmatic acceptance check (`grep -q '^locked: true'`) + T-210 mechanical gate. |
| 4 | Monitor wiring (R5) honestly assessed (feasibility + session-bound) | PASS | R5:16-26, 56-96 explicitly: harness Monitor tool IS available, this would be the FIRST skill to arm it (no prior art — grep-confirmed), AND the honesty flag that session-close=monitor-lost, durability comes from --resume+JSONL not the Monitor tool. R5 also surfaces the biggest real seam (troubleshoot won't auto-apply edits) at R5:144-154 / §6.2. |
| 5 | Builder can write per-file items for 12 skill files + 21 tests + Python core w/o re-reading source | PASS (with caveat C1) | R1:33-198 gives one row per spec path with status/purpose; R4:151-184 maps all 21 test files → modules + pattern; R1:137-153 enumerates all 22 modules + 18 fixtures by name. Caveat: SKILL.md *internal section content* is conventions-only (R2), not per-ref outline — see MINOR C1. |
| 6 | Cross-cutting risks surfaced as actionable builder warnings | PASS | Flag conflict `--depth quick`+`--fix` STOP (R3:148-158, 221-223); marker registration (R4:215-245); --cov defect (R4:55-63); hook-sync open Q (R1:124-128, R2:495-502) — though R5:168-174 RESOLVES it via Makefile read. All four are explicit, severity-flagged builder warnings. |

---

## Summary

- Checks passed: 6 / 6
- Checks failed: 0
- Depth caveats (MINOR, non-blocking): 3
- Files independently spot-verified against source: 3 (spec:905-944, spec:1025, severity-rubric.md:63-101)

---

## Per-file depth verdict

| File | Depth | One-line basis |
|------|-------|----------------|
| 01-component-inventory | DEEP | Per-path EXISTS/NEW/EDIT/REUSE with line counts + the C5 hook edit anchors (lines 49-58, 60-72) + correct never-stage-.claude flag. |
| 02-skill-command-hook | DEEP | Two frontmatter flavors w/ file:line, canonical section order, lazy-ref-load convention, full hook skeleton (exit-code contract, prefilter, fail-open), Activation pattern — all evidence-cited. |
| 03-reuse-surfaces | DEEP | Actual 5-step remap algo captured by reference (verified faithful), evidence-validator reuse instead of new agent, the `--depth quick`+`--fix` STOP finding. Genuine behavioral understanding. |
| 04-test-infra-core | DEEP (pivotal, nailed) | The architecture decision with live import-failure proof + 3 test idioms + marker/--cov/banned-import defects. This is the file the whole task hinges on; it is the strongest. |
| 05-integration-points | DEEP | Monitor feasibility + honest session-bound caveat + the troubleshoot-won't-auto-apply seam (single biggest wiring risk) + registration/sync mechanics from real Makefile lines. |
| 06-detection-probe-gh | DEEP | 5 exact probe captures, REST reply endpoint verified vs GitHub docs, GraphQL resolve (no native gh verb, gh 2.45.0 confirmed) with the two-call thread-id→resolve sequence + permissions HALT. |
| 07-mdtm-template | DEEP | All Template-02 PART1 rule IDs (A/B/L/M/I) with line cites + 2 prior-art exemplars + a concrete L5-gated DAG phase recommendation. |

---

## Issues Found (all MINOR — depth caveats, not blockers)

| # | Severity | Location | Issue | Recommended builder action |
|---|----------|----------|-------|----------------------------|
| C1 | MINOR | R1 + R2 (SKILL.md interior) | The research deeply covers WHICH files exist and the skill/ref *conventions*, but does NOT produce a per-ref content outline for the 9 NEW refs (state-machine.md, augment-poll.md, finding-verify.md, troubleshoot-dispatch.md, thread-reply.md, etc.). A builder can write the *file-creation checklist items* without re-reading source, but the *substantive content* of each ref (e.g. the FSM state table in state-machine.md, the §11 run-log schema in loop-guard.md) lives only in the spec, not pre-digested in research. | Builder must pull ref *bodies* from merged-spec §5/§7/§11/§12 directly (the research correctly defers there). Not a research gap per se — the spec is the SoT for those — but the builder should not expect research to have pre-outlined each ref's interior. Flag in task items: "read merged-spec §N for the contract body." |
| C2 | MINOR | R5 §6.2 / §2.3 (the troubleshoot seam) | R5 correctly identifies that troubleshoot won't auto-apply edits and that sc:submit-pr must own edit application at L2/L3 — but leaves the RESOLUTION as "flag to spec author" rather than characterizing HOW the FSM applies edits (which module, what the S3_FIXING transition concretely does). The deterministic-core architecture (R4) also does not assign an owner module for edit-application. | Builder should treat edit-application as a named FSM responsibility (likely fsm.py S3_FIXING driving agent-side Edit, NOT a core-pure module since it's I/O). Confirm against spec §FSM (spec:266-280) during item authoring; do not let this seam fall between R4 (core) and R5 (wiring) ownership. |
| C3 | MINOR | R2 §7.2 vs R5 §3.2 (hook-sync open question) | R2 left "does make sync-dev copy hooks/?" as an UNRESOLVED open question (R2:495-502, "this R2 pass did not read the Makefile"). R5 §3.2 (R5:168-174) actually answers it from Makefile:108-135 — but only for skills/agents/commands; R5's enumeration does NOT list `hooks/` either, so whether the C5 hook edit auto-syncs to `.claude/hooks/` remains genuinely unconfirmed across BOTH files. R1:124-128 independently notes `.claude/hooks/scripts/offer-pr-review.sh` is ABSENT. | Builder should add an explicit task item to grep the Makefile `sync-dev` target for a `hooks` copy rule BEFORE relying on hook sync, and keep the C5 edit `src/`-only with a verify-sync check. The research surfaced the risk but did not close it — acceptable (it's flagged), but the builder must not assume hooks sync. |

---

## Adversarial probes I ran (to defeat the "shallow" null hypothesis)

1. **Is R3 just naming the rubric, or did it capture the algorithm?** Re-read severity-rubric.md:63-101
   directly. R3's 5-step description is faithful to the source (category floor/ceiling table,
   confidence drop, diff-locality drop, cross-source bonus). NOT shallow. The T-301/T-302 mappings
   (R3:50, 66-67) tie spec tests to specific rubric rows — behavioral, not nominal.
2. **Is R4's architecture claim a guess or grounded?** R4's dispositive evidence is the spec's Python
   test bodies. I independently read spec:905-944 and spec:1025: the tests DO call
   `poll_augment_review(pr_num=42)` returning a state object with `.findings`/`.terminated`, and
   `remap_severity(finding).remapped_severity` — in-process Python contracts a markdown ref cannot
   satisfy. R4's conclusion (must be importable Python pkg) follows necessarily. The --cov hyphen
   defect at spec:1025 is real (confirmed verbatim).
3. **Is R6's DET probe vague?** No — it is 5 copy-pasteable `gh api` commands each bound to a named
   contract field, plus the GraphQL resolve sequence (two calls: reviewThreads query → thread node id
   → resolveReviewThread mutation) with the REST-id≠GraphQL-id gotcha and the permissions HALT. This
   is encode-able as a real gating item today.
4. **Did R5 hand-wave Monitor?** No — it explicitly says this is the first skill to arm the harness
   Monitor tool (grep-confirmed zero prior art), and flags the session-bound limitation as a true V1
   constraint mitigated only by --resume+JSONL. It also distinguishes the unrelated cli-portify Python
   OutputMonitor (a red herring). Honest, not hand-waved.

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source?** 3 dispositive ones — the spec
   Python test bodies (spec:905-944), the broken --cov target (spec:1025), and the severity-remap
   algorithm (severity-rubric.md:63-101). These are the load-bearing claims on which the depth verdict
   turns; verifying them defeats the "researchers fabricate plausible cites" failure mode.
2. **Which files did I read?** All 7 research files end-to-end; merged-spec.md ranges 905-945 and
   1010-1038; severity-rubric.md:63-101 (via grep/sed). Tool engagement: Read 9 (7 research + 2 spec
   ranges), Bash 2 (dir listing + rubric sed), Write 2 (report header + body). Total verification tool
   calls (9 Read + 2 Bash = 11) ≥ 6 checklist items — engagement floor satisfied.
3. **If I found 0 blocking issues, why trust it?** I did NOT find 0 issues — I found 3 MINOR depth
   caveats (per-ref interior not pre-digested; the edit-application seam owner unassigned across R4/R5;
   hook-sync question unresolved across R2+R5). I actively tried to falsify the depth claim by
   re-reading the source the research cites and looking for paraphrase-drift or fabricated cites; the
   cites held. The caveats are honest residue, not rubber-stamping.
4. **Web research?** None performed — all verification was local-file-bound (research files + spec +
   rubric). R6's external claims (GitHub REST reply endpoint, GraphQL resolve, gh 2.45.0, cli/cli#12419)
   were NOT independently re-fetched this pass; they are flagged here as research-asserted-but-not-
   QA-reverified (low risk — R6 cited specific docs/issue numbers, and these are the builder's to honor,
   not the depth gate's to adjudicate). Tool-engagement: Tavily not invoked (no external lookup needed
   for a depth audit of local research).

## Confidence

- **Verified:** 6/6 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100%
- **Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 2
- Note: confidence is on the DEPTH question (is the research deep enough?), computed over the 6
  checklist items, each verified with cited evidence + at least one cross-read into source for the
  3 pivotal claims (items 1, 2, 3).

## Recommendations for the task-builder

1. **Proceed** — research depth is sufficient to build a high-quality complex task file. R4 is the
   anchor; honor its `src/superclaude/submit_pr/` (underscored) core decision and the corrected
   `--cov=superclaude.submit_pr`.
2. **Encode the 3 spec defects as task items** (they are not optional fixes): (a) correct the --cov
   path; (b) register markers `loop_guard/autonomy/recovery/p0/loop` in pyproject.toml
   `[tool.pytest.ini_options]` or `--strict-markers` fails collection; (c) the DET probe HALT gate.
3. **Heed C1/C2/C3:** pull ref bodies from spec §5/§7/§11/§12 (not from research); assign the
   edit-application seam to a named FSM responsibility; add a Makefile-grep item before relying on
   hook sync.
4. **Honor R3's reuse-by-reference rule** — severity-routing.md must DEFER to severity-rubric.md by
   citation, never copy the table (drift is the failure these refs prevent).

## QA Complete
