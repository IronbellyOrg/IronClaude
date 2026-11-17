# Debate Points and Clusters (Step 2 input)

Generated from `diff-analysis.md`. Skill formula: total diff points = S + C + X + promoted A. Clusters group related points so two advocates can debate 234 points in a bounded number of rounds; every point belongs to exactly one cluster. Unique contributions (U) are not diff points under the skill; they are handled in the U-register at the end.

- Debate points: 234 (S 56, C 97, X 63, promoted A 18)
- Clusters: 26
- Taxonomy level is tagged per cluster (L1 surface/format/rating; L2 structural/architecture/organisation; L3 state mechanics: guards, quorum, ledger state, invariants, verified code facts). Per skill, each point has exactly one level; a point inherits its cluster level.
- Points per level: L1 50, L2 126, L3 58

## Cluster table

| Cluster | Level | Topic | #pts | Member points (id: short title [severity]) |
|---|---|---|---|---|
| CL-01 | L2 | Core shape and engine boundary (one superset core vs thin shared contract plus per-module engines) | 10 | S-040: Whole-design options [Medium]; C-005: Shape of the shared core [High]; C-050: Core location and shape [High]; C-061: Clustering [High]; C-076: Shape of the recommended core (Sec 7) [High]; C-090: Clustering [High]; X-002: One finding contract / one clusterer / one merge vs two gram [High]; X-038: Shape of the shared core [High]; X-042: Which clusterer the core uses [High]; X-051: Which engine shape the unified Review Panel should have [High] |
| CL-02 | L2 | Finding contract, location types (anchor vs citations), PR fields, brief/input contract | 6 | C-051: Finding contract / grammar [High]; C-053: Invalid-block unit of loss [Medium]; C-066: Brief / input contract [Low]; C-088: PR code review integration [High]; X-007: PR-review fields in the finding contract [High]; X-059: Whether PR-specific fields enter the finding contract [Medium] |
| CL-03 | L3 | Over-length lines, truncation, claim cut and itemised drop record | 4 | C-052: Over-limit lines (200/300 limits) [High]; C-077: Length limits and over-length lines [Medium]; X-040: Does the claim field get truncated [Medium]; X-056: Whether to truncate the `claim` field [Medium] |
| CL-04 | L3 | Who decides blocking; quorum; blind grader; calibration; exit codes | 13 | C-011: Ledger and verdict defects [High]; C-054: Who decides blocking [High]; C-056: Calibration role [Medium]; C-065: Blocking predicate / severity vocabulary [Medium]; C-078: Blocking decider [High]; C-080: Quorum and degraded outcome [Medium]; C-087: "Medium" severity [Medium]; X-003: Who decides blocking [High]; X-004: Reviewer quorum value [Medium]; X-006: `medium` severity as a core token [Medium]; X-039: Who decides "blocking" in the core [High]; X-055: Who decides a blocking finding in the core [High]; X-058: Meaning of the new exit code 12 [Medium] |
| CL-05 | L3 | Ledger rounds, clearing by silence, verdict derivation, verdict contract | 7 | C-055: Ledger rounds, clearing, quorum [Medium]; C-063: Reflect merge path / contract [Medium]; C-064: Verdict contract and exit codes [Medium]; C-079: Round / ledger model [High]; C-085: Reflect contract writer / merge step [Medium]; X-044: One verdict contract vs per-engine verdicts [Medium]; X-046: Ledger rounds: open gate vs closed design [Medium] |
| CL-06 | L2 | Dispatch, identity, tier data, environments, read-only enforcement | 9 | C-012: Dispatch, identity and resolver [Medium]; C-037: Tier and class configuration [Medium]; C-038: Identity spike and collapse figures [Medium]; C-058: Dispatch mechanism [Medium]; C-059: Model tier source and environment [Medium]; C-067: Reviewer read-only enforcement [Low]; C-082: Dispatch and identity [Medium]; X-009: Core launches reviewers / gateway launch adapters [High]; X-045: End-state dispatch design [Medium] |
| CL-07 | L3 | Panel resolver distinctness default (soft vs declared per slot) | 4 | C-060: Distinctness default [High]; C-081: Panel resolution and distinctness [Medium]; X-041: Default distinctness of panel models [High]; X-057: Default distinctness behaviour of the resolver [Medium] |
| CL-08 | L2 | Run record, manifest, telemetry (manifest vs events.jsonl; telemetry producer) | 4 | C-034: Run record / telemetry [Medium]; C-057: Run record, manifest, telemetry [Medium]; C-083: Run record and telemetry [Medium]; X-010: Run record shape and where audit checks live [Medium] |
| CL-09 | L3 | Reflect Tier 2 engines (fix ensemble.py now vs freeze), shadow exit, contract writer | 13 | C-010: Post-gate engine (`ensemble.py`) [Medium]; C-017: Reflect Tier 2 convergence threshold [Medium]; C-018: Merge decision source for reflect (`merge_method`, `merged-v [Medium]; C-020: E1 kernel merge facts [Medium]; C-021: Where the swarm ensemble belongs [Medium]; C-022: Engine A vs engine B depth [High]; C-023: Stage 2 shadow exit [High]; C-024: 5x3 combination experiment [Medium]; C-025: Reflect memory writes [Medium]; C-062: Reflect Tier-2 engines [High]; C-084: Reflect Tier 2 engine and post gate [High]; X-043: Fate of the code-driven Tier 2 engine [High]; X-054: Reflect Tier 2 engine: touch `ensemble.py` now or not [High] |
| CL-10 | L2 | Consumers and entry points (tasklist/workflow, PR review, rf-qa, future exposures) | 12 | S-021: Consumers + future-use blockers [Medium]; C-006: Consumers in the target [Medium]; C-014: Future consumers (PR code review, rf-qa) [Medium]; C-040: Consumers: depth [Medium]; C-041: Entry-point decision for tasklist review [Medium]; C-068: Consumer entry for tasklist/workflow [Medium]; C-069: Future consumers (PR review, rf-qa) [High]; C-086: Tasklist / workflow entry [Medium]; C-089: rf-qa / rf-qa-qualitative replacement [High]; X-005: Entry point for workflow/tasklist review (DO4) [High]; X-047: How tasklist and workflow reach the panel [Medium]; X-060: Status of "is workflow/tasklist review reflect pre or a dire [Medium] |
| CL-11 | L2 | E2 collaboration designs and process-redesign brainstorms | 5 | S-018: E2 split [High]; C-002: Scope of the underlying research [High]; C-028: E2 collaboration and process-redesign work [High]; C-072: Collaboration and process redesign [High]; C-091: Collaboration designs and process redesign (E2 brainstorms) [High] |
| CL-12 | L2 | Installed-only E3 variants and experiment evidence | 7 | S-023: E3 split in matrix [Medium]; C-030: E3 installed variants [High]; C-031: Phase-5 experiment numbers [Medium]; C-071: Installed-only E3 variants [High]; C-094: Experiment variants (E3-installed) [Medium]; X-034: Verification status of diffgate, ponytail/fix-audit, armb [Medium]; A-019: The installed `~/.claude/` variants on this machine represen [Medium] |
| CL-13 | L2 | Evaluation, acceptance, ground truth, E1/E2 evidence independence | 11 | S-020: Eval harness, governance, repo constraints [High]; C-013: Evaluation and ground truth [High]; C-026: E2 headline numbers [High]; C-027: E2 model-by-role observations [Medium]; C-029: E1 and E2 provenance entanglement [High]; C-043: Judge blinding facts [Medium]; C-070: Evaluation and rollout [Medium]; C-092: Evaluation / acceptance [High]; X-021: What 1,398 counts in the E2 chain replay [Low]; X-025: How many Qwen3.8-max runs timed out [Medium]; X-026: Verdict flips and what else audit D lists [Medium] |
| CL-14 | L2 | Decisions only one report treats as an axis (panel size and cost, calibration, clustering, identity check) | 3 | S-045: Decisions that are stand-alone in only one report [High]; C-073: Panel size and Tier 2 escalation cost [Medium]; C-093: Panel size versus cost [Medium] |
| CL-15 | L1 | Severity ratings of agreed facts and application of rule C8 (Critical vs Important) | 12 | C-003: Gap-table size and Critical definition [High]; C-009: Rule C8 and which gaps it touches [High]; X-011: Severity: over-length fields drop whole findings (49 blockin [High]; X-012: Severity: ledger clears a row by silence [High]; X-013: Severity: `lint_cmd` / `estimate_cmd` registered but absent [Medium]; X-014: Severity and verification status: telemetry store with no pr [Medium]; X-015: Severity and C8 status: reflect panel kernel not reachable ( [High]; X-016: Severity: Stage 2 exit FAIL and orchestrator-written steps [Medium]; X-017: Severity: #346 `merge`/`ledger`/`panel` CLI has no productio [Medium]; X-018: Severity: no dispatch contract / resolver policy [Medium]; X-019: Severity: evaluation and driving-document input [Medium]; A-008: Unwired-but-named capability is Critical even when the skill [High] |
| CL-16 | L2 | Evidence baseline: E2 pin, HEAD, scope slices, line-number freshness | 12 | S-015: E2 baseline pin [High]; S-016: Evidence-source basis [High]; S-041: Evidence baseline pinned [Medium]; C-001: E2 evidence baseline (which commit) [High]; X-001: Which E2 commit is the evidence base [Medium]; X-062: E2 study pin commit [Medium]; X-063: Baseline HEAD of the code read [Low]; A-002: Code facts and line numbers cited at HEAD 792cf8c52 (V1:489, [Medium]; A-024: Research-file counts taken from hand-offs or scope slices ca [Medium]; A-036: Code line citations from older HEADs (V1 `792cf8c52`, V2 `50 [Medium]; A-037: The E2 pinned commit is the right baseline (V1 `4a22d74` 202 [Medium]; A-055: E2 harness files are not tracked at HEAD and are read throug [Medium] |
| CL-17 | L2 | Section 6 method: conflict classification, debates run, status taxonomy, tiebreaker winners | 16 | S-032: Organising unit of Section 6 [High]; S-033: Option labels reused with different meaning [Medium]; S-034: Where the recommendation sits [Medium]; S-035: Option scoring layout [Low]; S-036: Status taxonomy and classification result [High]; S-037: Number and depth of adversarial debates [High]; S-038: Conflict log form [High]; S-039: Defect register inside Section 6 [Medium]; S-043: Corrected-claims, open-question and coverage tables inside S [Medium]; S-044: Post-debate re-rating of options [Low]; S-055: Meaning of "C-nn" ids [Medium]; C-074: Evidence-number reconciliation [Low]; C-075: Open invariants after debates [Medium]; C-097: Status wording for debated conflicts [Low]; X-052: Whether the core-shape question can be decided by evidence [High]; A-052: All debates ended `partial` with unaddressed HIGH invariants [High] |
| CL-18 | L3 | Fact disputes settled by code or data (KeyError path, 1,398, census counts, key counts, timeouts, calibrator) | 17 | X-020: Does `ledger.merge_round` raise `KeyError` on a v2 citation- [Medium]; X-022: Count of rf-* agent spawn sites [Low]; X-023: Key count of the engine-A reflect contract [Low]; X-024: Keys of the swarm ensemble contract outside the frozen 1.8.0 [Low]; X-027: Definition behind `findings_block_compliance_rate` 0.704 [Medium]; X-028: `cluster_agreement` in the shadow runs [Low]; X-029: rf-qa family call-site census [Medium]; X-030: Calibrator rubric dimension mismatch [Medium]; X-031: What `findings.same_defect` links [Low]; X-032: Whether `ensemble.py` is E1 work [Medium]; X-033: Count of severity label sets in the repo [Low]; X-048: Is the 5-versus-6-dimension calibrator mismatch a verified f [Low]; X-049: Is a v2 citation-only finding a crash of the v1 ledger path [Medium]; X-050: Identity source of shadow and combo runs [Low]; X-053: What a v2 citation-only finding does on the shipped merge pa [Medium]; X-061: rf-qa spawn-site census [Low]; A-057: A v2 citation-only finding reaches the shipped merge path an [Medium] |
| CL-19 | L2 | Section 7 shape and the adjudication-override layer between Sections 3/4 and 7 | 6 | S-007: Adjudication-override layer [High]; S-013: Where precedence between Section 4 and the recommendation is [High]; S-046: Section 7 shape and size [High]; S-054: Debate-invariant presentation [Medium]; C-004: Status of the Section 3 target [High]; C-095: Constraints and invariants carried [High] |
| CL-20 | L2 | Section 8 form (migration plan vs inputs for a later plan) and the value inventory | 7 | S-047: Section 8 purpose and contents [High]; S-048: Where the value inventory lives [High]; S-049: Inventory row schema and destination vocabulary [High]; S-056: No-regression gate list form [High]; C-096: Branching / PR sequencing content [Medium]; A-056: The inventory destinations agree with the architecture recom [High]; A-059: The counts of "rows", "gates", "constraints" and "open quest [Medium] |
| CL-21 | L1 | Sections 1, 3 and 4: structure, target-state layout, gap-table design (residual) | 17 | S-001: Header metadata and scope note [Medium]; S-002: Table of Contents shape [Medium]; S-003: Preamble before Section 1 [Medium]; S-004: Section 3 internal organization [High]; S-005: External research inside Section 3 [Medium]; S-006: Architecture diagram in Section 3 [Low]; S-008: Section 1 length and format [Low]; S-009: Section 10 ToC items [Low]; S-010: Section 4 subsections [Medium]; S-011: Gap table row-id scheme and grouping [High]; S-012: Migration-track tagging inside Section 4 [High]; S-014: Contradiction table column order and population [Low]; C-007: Success criteria [High]; C-008: Constraints list [Medium]; C-015: Stale-documentation treatment [Medium]; C-019: Section 1 evidence emphasis [Medium]; X-008: Per-slot `role`/`lens`/`agent` in panel templates [Medium] |
| CL-22 | L1 | Section 2 organisation and evidence depth (residual) | 13 | S-017: Sec 2 size and subsection plan [High]; S-019: Dispatch/tier/identity [Medium]; S-022: Overlap matrix design [High]; S-024: Where contradictions are recorded [Medium]; S-025: Unverified items [Medium]; S-026: Diagrams [Low]; C-032: Defect enumeration against current code [High]; C-033: Test surface [Low]; C-035: Brief and input delivery [Medium]; C-036: Severity vocabularies [Medium]; C-039: Tier-2 prevalence [Low]; C-042: Overlap-matrix interpretive stance [Medium]; A-018: Tier lists in `review-tiers.default.json` describe what the  [High] |
| CL-23 | L2 | Section 5 external research (source sets, severity, calibration, fingerprinting, runtime and git topics) | 15 | S-027: Sec 5 source set [High]; S-028: Sec 5 entry format [Low]; S-029: Sec 5 options lists [Medium]; S-030: Sec 5 summary [Medium]; S-031: Within-subsection conflicts [Low]; C-044: Sec 5 aggregation evidence [High]; C-045: Sec 5 severity [High]; C-046: Sec 5 judge and calibration [High]; C-047: Sec 5 fingerprinting and clustering [High]; C-048: Sec 5 runtime and git topics [High]; C-049: Sec 5 handling of codebase context [Low]; X-035: SARIF `kind` values [Low]; X-036: Use of arXiv 2606.19544 verbosity finding [Low]; X-037: Evidence status of Codex P0-P3 behaviour [Low]; A-027: The skill panel (engine B) will be the Tier-2 path the share [Medium] |
| CL-24 | L1 | Sections 9 and 10, open questions, id namespaces, appendices | 8 | S-050: Section 9 organisation [Medium]; S-051: Section 9 column set [Low]; S-052: Section 10 evidence trail [Medium]; S-053: Appendices [Low]; C-016: Open decisions and unverified claims carried from Section 4 [High]; A-006: Gap ids G-nn, D-nn and C-nn are different namespaces in each [High]; A-012: The two gap logs (V1 "94 open rows, none Critical, 30 Import [Medium]; A-058: Cross-report ids (C-nn, Q-nn, A-n, G-nn) can be compared one [High] |
| CL-25 | L2 | Section 6 residual points not in a topical cluster | 3 | S-042: Citation keys [Low]; A-038: `tests/review` size claim "651 tests" counts collected tests [Low]; A-041: Section 6 numbers about E1 shadow runs (13 of 20, EV-1 8 of  [Low] |
| CL-26 | L2 | Sections 7 to 10 residual points not in a topical cluster | 0 |  |

## Promoted shared assumptions (answer ACCEPT / REJECT / QUALIFY)

- A-002: Code facts and line numbers cited at HEAD 792cf8c52 (V1:489, V1:99) or 50d4d2b9d (V2:108)  (cluster CL-16)
- A-006: Gap ids G-nn, D-nn and C-nn are different namespaces in each report (V1 "G-20" is a log ro (cluster CL-24)
- A-008: Unwired-but-named capability is Critical even when the skill text stages it for a later re (cluster CL-15)
- A-012: The two gap logs (V1 "94 open rows, none Critical, 30 Important", V2 "555 rows") are inter (cluster CL-24)
- A-018: Tier lists in `review-tiers.default.json` describe what the gateway can serve (cluster CL-22)
- A-019: The installed `~/.claude/` variants on this machine represent what consumers see (cluster CL-12)
- A-024: Research-file counts taken from hand-offs or scope slices carry over unchanged (cluster CL-16)
- A-027: The skill panel (engine B) will be the Tier-2 path the shared core serves, or at least tha (cluster CL-23)
- A-036: Code line citations from older HEADs (V1 `792cf8c52`, V2 `50d4d2b9d`) hold at the current  (cluster CL-16)
- A-037: The E2 pinned commit is the right baseline (V1 `4a22d74` 2026-11-13; V2 `6c09843` 2026-11- (cluster CL-16)
- A-038: `tests/review` size claim "651 tests" counts collected tests (cluster CL-25)
- A-041: Section 6 numbers about E1 shadow runs (13 of 20, EV-1 8 of 13, 6 of 9 collapse) are valid (cluster CL-25)
- A-052: All debates ended `partial` with unaddressed HIGH invariants, yet their winners are adopte (cluster CL-17)
- A-055: E2 harness files are not tracked at HEAD and are read through `git show` at a commit, not  (cluster CL-16)
- A-056: The inventory destinations agree with the architecture recommended in Section 7 (cluster CL-20)
- A-057: A v2 citation-only finding reaches the shipped merge path and crashes with `KeyError 'anch (cluster CL-18)
- A-058: Cross-report ids (C-nn, Q-nn, A-n, G-nn) can be compared one to one when the reports are m (cluster CL-24)
- A-059: The counts of "rows", "gates", "constraints" and "open questions" in each report measure t (cluster CL-20)

## U-register (unique contributions; for retention in the merge)

| id | Variant | Value | Contribution (short) |
|---|---|---|---|
| U-001 | (see diff-analysis) | High | V1 |
| U-002 | (see diff-analysis) | High | V1 |
| U-003 | (see diff-analysis) | High | V1 |
| U-004 | (see diff-analysis) | Medium | V1 |
| U-005 | (see diff-analysis) | High | V1 |
| U-006 | (see diff-analysis) | Medium | V1 |
| U-007 | (see diff-analysis) | Low | V1 |
| U-008 | (see diff-analysis) | Medium | V1 |
| U-009 | (see diff-analysis) | Medium | V1 |
| U-010 | (see diff-analysis) | High | V1 |
| U-011 | (see diff-analysis) | Medium | V1 |
| U-012 | (see diff-analysis) | Medium | V1 |
| U-013 | (see diff-analysis) | Low | V1 |
| U-014 | (see diff-analysis) | Medium | V1 |
| U-015 | (see diff-analysis) | Medium | V1 |
| U-016 | (see diff-analysis) | Medium | V1 |
| U-017 | (see diff-analysis) | Low | V1 |
| U-018 | (see diff-analysis) | High | V2 |
| U-019 | (see diff-analysis) | Medium | V2 |
| U-020 | (see diff-analysis) | High | V2 |
| U-021 | (see diff-analysis) | High | V2 |
| U-022 | (see diff-analysis) | High | V2 |
| U-023 | (see diff-analysis) | High | V2 |
| U-024 | (see diff-analysis) | High | V2 |
| U-025 | (see diff-analysis) | High | V2 |
| U-026 | (see diff-analysis) | High | V2 |
| U-027 | (see diff-analysis) | High | V2 |
| U-028 | (see diff-analysis) | Medium | V2 |
| U-029 | (see diff-analysis) | High | V2 |
| U-030 | (see diff-analysis) | Medium | V2 |
| U-031 | (see diff-analysis) | High | V2 |
| U-032 | (see diff-analysis) | High | V2 |
| U-033 | (see diff-analysis) | Medium | V2 |
| U-034 | (see diff-analysis) | Medium | V2 |
| U-035 | (see diff-analysis) | High | V2 |
| U-036 | (see diff-analysis) | High | V2 |
| U-037 | (see diff-analysis) | High | V2 |
| U-038 | (see diff-analysis) | Low | V2 |
| U-039 | (see diff-analysis) | Medium | V2 |
| U-040 | (see diff-analysis) | High | V2 |
| U-041 | (see diff-analysis) | Medium | V2 |
| U-042 | (see diff-analysis) | High | V2 |
| U-043 | (see diff-analysis) | Medium | V2 |
| U-044 | (see diff-analysis) | High | V2 |
| U-045 | (see diff-analysis) | High | V2 |
| U-046 | (see diff-analysis) | High | V2 |
| U-047 | (see diff-analysis) | High | V2 |
| U-048 | (see diff-analysis) | High | V2 |
| U-049 | (see diff-analysis) | High | V2 |
| U-050 | (see diff-analysis) | Medium | V2 |
| U-051 | (see diff-analysis) | High | V2 |
| U-052 | (see diff-analysis) | Medium | V2 |
| U-053 | (see diff-analysis) | Medium | V2 |
| U-054 | (see diff-analysis) | High | V2 |
| U-055 | (see diff-analysis) | Medium | V2 |
| U-056 | (see diff-analysis) | High | V2 |
| U-057 | (see diff-analysis) | Medium | V2 |
| U-058 | (see diff-analysis) | High | V1 |
| U-059 | (see diff-analysis) | Medium | V1 |
| U-060 | (see diff-analysis) | Medium | V1 |
| U-061 | (see diff-analysis) | Medium | V1 |
| U-062 | (see diff-analysis) | Medium | V1 |
| U-063 | (see diff-analysis) | Medium | V1 |
| U-064 | (see diff-analysis) | High | V1 |
| U-065 | (see diff-analysis) | High | V1 |
| U-066 | (see diff-analysis) | High | V1 |
| U-067 | (see diff-analysis) | Medium | V1 |
| U-068 | (see diff-analysis) | High | V1 |
| U-069 | (see diff-analysis) | Low | V1 |
| U-070 | (see diff-analysis) | Low | V1 |
| U-071 | (see diff-analysis) | High | V2 |
| U-072 | (see diff-analysis) | High | V2 |
| U-073 | (see diff-analysis) | High | V2 |
| U-074 | (see diff-analysis) | High | V2 |
| U-075 | (see diff-analysis) | High | V2 |
| U-076 | (see diff-analysis) | High | V2 |
| U-077 | (see diff-analysis) | High | V2 |
| U-078 | (see diff-analysis) | Medium | V2 |
| U-079 | (see diff-analysis) | Medium | V2 |
| U-080 | (see diff-analysis) | Medium | V2 |
| U-081 | (see diff-analysis) | Medium | V2 |
| U-082 | (see diff-analysis) | Medium | V2 |
| U-083 | (see diff-analysis) | Medium | V2 |
| U-084 | (see diff-analysis) | Medium | V2 |
| U-085 | (see diff-analysis) | Medium | V2 |
| U-086 | (see diff-analysis) | High | V1 |
| U-087 | (see diff-analysis) | High | V1 |
| U-088 | (see diff-analysis) | High | V1 |
| U-089 | (see diff-analysis) | Medium | V1 |
| U-090 | (see diff-analysis) | Medium | V1 |
| U-091 | (see diff-analysis) | Medium | V1 |
| U-092 | (see diff-analysis) | Medium | V1 |
| U-093 | (see diff-analysis) | Medium | V1 |
| U-094 | (see diff-analysis) | Low | V1 |
| U-095 | (see diff-analysis) | Low | V1 |
| U-096 | (see diff-analysis) | High | V1 |
| U-097 | (see diff-analysis) | High | V1 |
| U-098 | (see diff-analysis) | High | V1 |
| U-099 | (see diff-analysis) | High | V1 |
| U-100 | (see diff-analysis) | High | V1 |
| U-101 | (see diff-analysis) | High | V1 |
| U-102 | (see diff-analysis) | High | V1 |
| U-103 | (see diff-analysis) | Medium | V1 |
| U-104 | (see diff-analysis) | Medium | V1 |
| U-105 | (see diff-analysis) | Medium | V1 |
| U-106 | (see diff-analysis) | Medium | V1 |
| U-107 | (see diff-analysis) | Medium | V1 |
| U-108 | (see diff-analysis) | Low | V1 |
| U-109 | (see diff-analysis) | Medium | V1 |
| U-110 | (see diff-analysis) | High | V2 |
| U-111 | (see diff-analysis) | High | V2 |
| U-112 | (see diff-analysis) | High | V2 |
| U-113 | (see diff-analysis) | High | V2 |
| U-114 | (see diff-analysis) | High | V2 |
| U-115 | (see diff-analysis) | High | V2 |
| U-116 | (see diff-analysis) | High | V2 |
| U-117 | (see diff-analysis) | High | V2 |
| U-118 | (see diff-analysis) | High | V2 |
| U-119 | (see diff-analysis) | Medium | V2 |
| U-120 | (see diff-analysis) | Medium | V2 |
| U-121 | (see diff-analysis) | Medium | V2 |
| U-122 | (see diff-analysis) | Low | V2 |
| U-123 | (see diff-analysis) | Medium | V2 |
| U-124 | (see diff-analysis) | Low | V2 |
