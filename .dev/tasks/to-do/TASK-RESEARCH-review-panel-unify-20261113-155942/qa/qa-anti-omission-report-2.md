## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md` (4283 lines)
**Input files checked:** research/05-blocking-calibration.md, research/06-input-contract-briefs.md, research/07-reflect-merge-contract.md, research/08-run-recording-telemetry.md, synthesis/synth-02-target-gaps.md, synthesis/synth-03-external-findings.md, research/scope/01-other-branch-study.md, research/scope/02-review-cli-code.md (all under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/`); total findings enumerated: 823 (62 + 43 + 45 + 30 + 185 + 190 + 108 + 160)
**Date:** 2026-11-14
**Agent:** anti-omission agent 2 of 4 (rf-analyst), fix_authorization: false

Method note: coverage judged by meaning, not by ID. Enumeration is written one input file at a time below. "l.N" means a line of the report; "V-nnn" is a row of the Section 8.1 value inventory (report l.2937-3630); "Cx-nn" is a Section 6 conflict; MS/BL/ENS/DOC/OPEN/D are Section 4 gap rows (l.588-732). "OM-n" points to the numbered entry in "Omissions Found".

Verification methods used (all read-only): full read of each input file; targeted regex search of the report for the distinctive tokens of each item (numbers, identifiers, file:line cites, phrases); a whitespace-normalised `diff` of `synthesis/synth-03-external-findings.md` against report l.782-1151 (369 of 370 lines identical; the one differing line, the web-04 context line, was later corrected to the narrower "21 of 25" precision wording, so it counts as corrected, not omitted); a word-level diff of `synthesis/synth-02-target-gaps.md` against report l.480-780 (all 61 deleted phrases are in-place revisions of rows that remain; none is a dropped finding; report row IDs D1-D16, BL-01..23, MS-01..24, ENS-1..9, OPEN-01..02, DOC-01..70 and the combined D-71..77 row are all present at l.588-732).

## Enumeration

### File 1 of 8: research/05-blocking-calibration.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 05-01 | contract.py maps a contract to 4 verdicts, first match BLOCKED > DEGRADED > HALTED > PASS | 05 §1 | REPRESENTED | l.2787 (verdict map), l.446, V-500 |
| 05-02 | Seven load-bearing booleans; a non-bool (e.g. "true" string) routes BLOCKED | 05 §1.1 | REPRESENTED | l.2874 (`_LOAD_BEARING_BOOL_FIELDS` pinned), V-257 |
| 05-03 | `_degraded_reason` order: single-reviewer-fallback and convergence < 0.80 DEGRADE, so reflect does not trust one reviewer | 05 §1.3 | REPRESENTED | V-501 (l.3439), l.2787, l.1452 |
| 05-04 | `_halted_reason` count fallback: any Drift count halts; Authorized/Necessary never halt | 05 §1.4 | REPRESENTED | V-500 (l.3438), C-16 (l.2193), MS-15 (l.641) |
| 05-05 | `classify_fix`: HUMAN-REQUIRED vs AUTO-FIXABLE split | 05 §1.5 | REPRESENTED | MS-14 (l.640: flag changes `classify_fix` 414 vs 418), SC-18 (l.542) |
| 05-06 | 4-class taxonomy, gate effects per class, precedence Regression > Drift > Necessary > Authorized | 05 §2.1 | REPRESENTED (class effects); the precedence rule is carried only through the any-member rule, see 05-54 | V-500, l.911 |
| 05-07 | Regression is set by evidence, not by assignment: only mapped exit codes set `regression_present`; pytest exit 2/3, timeouts, flaky and unmapped exits are Grounding Gaps | 05 §2.1, §13.1 | OMITTED (MINOR) | OM-1; only the neighbouring static-analysis conflict (G-05) is carried: l.2243, V-503 |
| 05-08 | Reuse-Miss, runtime-surface UNREACHED, contracted-sink findings are modifiers on the 4 classes, never a 5th class; Reuse-Miss blocking bar (S_reuse >= 0.82, confidence >= 0.85) | 05 §2.1 | REPRESENTED | V-289 (l.3227), V-502 (l.3440), l.1495, l.1013 |
| 05-09 | Protocol's "blocking classes (Drift/Regression)" wording matches contract.py:377-381 | 05 §2.1 | REPRESENTED | V-500, l.2787 |
| 05-10 | Grounding Gaps force status partial + needs_human_decision (verdict-changing, not a deviation); Correctness gaps advisory and never gate | 05 §2.2 | REPRESENTED | C-16 (l.2214), V-289, V-297 (l.3235), G-15 (l.641) |
| 05-11 | `unauthorized_deviation_present` has no producer rule anywhere in the skill | 05 §2.3 | REPRESENTED | MS-14 (l.640), SC-18, G-03, V-502 |
| 05-12 | §9.1 flag definitions (regression_present exit-code sourced; user_decision_required = convergence < threshold; per_task_verdicts.deviation_class) | 05 §2.3 | REPRESENTED | V-290 (l.3228), l.2788 |
| 05-13 | Calibrated C routes tiers (0.90/0.85); it is not a per-finding blocking decider | 05 §2.4 | REPRESENTED | V-502, C-06 Cons (l.1590) |
| 05-14 | §7/§11.3 calibrator: class-disjoint from reviewers; empty set -> highest-capability class + `calibrator_diversity: degraded`; inline-fallback marker; three-way partition | 05 §2.5 | REPRESENTED | V-511 (l.3449), l.2774, l.1422, DOC-30 (l.691) |
| 05-15 | "Debate is weighted by calibrated confidence" (SKILL.md:1260) not traced into sc-adversarial | 05 §2.5, Gaps | REPRESENTED | l.476 (matrix row), G-10 (l.3975, "probably contradicted") |
| 05-16 | `calibrator_diversity` never read by contract.py; a degraded calibrator has no verdict effect | 05 §2.6 | REPRESENTED | l.2774 |
| 05-17 | Rubric is card-level: 5-dim mean, no per-finding score, no blocking dimension | 05 §3.1 | REPRESENTED | V-503 (l.3441), l.1593 |
| 05-18 | Rubric dimension 3 vocabulary {Aligned, Refinement, Drift, Regression} is stale | 05 §3.1 | REPRESENTED | DOC-29 (l.690), V-643 |
| 05-19 | Rubric thresholds, Example C (anthropic-only: disjoint set empty -> degraded); no published capability ordering across the six classes (open question) | 05 §3.1 | REPRESENTED (thresholds, Example C); the "no capability ordering" question OMITTED (MINOR) | V-511, l.1590; OM-5 |
| 05-20 | taxonomy ref row (C7, step 5.6a): static unreachability is a Regression vs SKILL §10.10 "static can NEVER set regression_present" | 05 §3.2 | REPRESENTED | l.2243, V-503, Q-12 (l.3956) |
| 05-21 | confidence-calibrator agent: 6 troubleshoot dims, `rubric_path`, gated-min formula, verdict caps, C1-C8 assertions, Read-only sonnet | 05 §4 | REPRESENTED | l.170, l.1562, l.1593, V-504 |
| 05-22 | Agent returns one number per card, no per-finding output; inline fallback; placebo warning (+/-0.05) | 05 §4 | REPRESENTED | l.1596, V-505, l.3270 |
| 05-23 | Reflect passes no `rubric_path`; "re-grades per 5-dim rubric" is CODE-CONTRADICTED | 05 §4.1 | REPRESENTED | DOC-28 (l.689), MS-16 (l.642), contradiction 8 (l.745) |
| 05-24 | 6-vs-5 dimension mapping table | 05 §4.2 | COVERED-BY-DEDUP (into DOC-28 / MS-16, which state the 6-vs-5 mismatch; the per-dimension fit table is the source's own reading) | l.689, l.642 |
| 05-25 | Legacy calibration 0 of 689 (embedded 34/271, sidecar 61/347, none 20/71); numeric in 1 of 74 runs keyed F1 vs R1-F1; layouts 21/10/2/4 | 05 §5.1 | REPRESENTED (totals, id mismatch, layouts) | V-339 (l.3277), V-505, l.160 |
| 05-26 | Consequence adopted: `calibrated_findings n/m` / `calibration_coverage`; multi-layout reader rejected | 05 §5.1 | REPRESENTED | V-339, V-389 (l.3327) |
| 05-27 | Shadow runs: 142/142 clustered findings calibrated in 13 runs (per-run table; shadow12 0/0; shadow01 none) | 05 §5.2 | REPRESENTED (total); per-run table COVERED-BY-DEDUP into the total | l.160, l.1595 |
| 05-28 | 4 of 14 shadow runs (10, 12, 14, 15) write `calibration:` unfenced vs SKILL.md:344 | 05 §5.2 | REPRESENTED | DOC-31 (l.692), l.1576, G-14 |
| 05-29 | Tally: 142 findings (MINOR 100, MAJOR 42); 16 blocking mean 0.801 vs 126 non-blocking mean 0.661; 26 MAJOR non-blocking; association is not accuracy | 05 §5.3 | REPRESENTED | l.160, l.1595, l.2209, l.2244 |
| 05-30 | Shadow run window 2026-11-12 22:22 to 2026-11-13 02:42 UTC; run-directory dates are source-package dates | 05 §5.3 | REPRESENTED | l.1161 |
| 05-31 | finding-grader agent: installed in ~/.claude only, blind per claim, JSON-lines reply, Read tool | 05 §6 | REPRESENTED | V-421 (l.3359), V-506, l.2815, MS-19 |
| 05-32 | Stoprule RUBRIC v1 content: B1 quote, B2 outcome, B3 kinds (a)-(e); CRITICAL under (e); "never a reason" list; Q2 recorded as data | 05 §6 | OMITTED (MINOR); only "rubric B1-B3, agreement never a reason, spec-specific" is carried | OM-3; l.265, l.1454, l.1510, V-506 |
| 05-33 | Grader as decider: separates finding from deciding; rubric is spec-text specific; under B1-B3 a pure Drift is not blocking while reflect halts on Drift; accuracy unmeasured | 05 §6 | REPRESENTED | V-506 (l.3444), l.1510, l.1501, MS-19 |
| 05-34 | findings_v2 enforces: bool blocking, MINOR never blocking, calibrated_confidence rejected, lens/deviation_class/channel rules, label rule only with reflect_category | 05 §7 | REPRESENTED | V-507 (l.3445), l.2240-2245, C-16 |
| 05-35 | findings_v2 does NOT tie deviation_class or channel to blocking; MAJOR may be non-blocking without reflect_category | 05 §7 | REPRESENTED | l.2241, MS-15 (l.641), C-16 Option B |
| 05-36 | card_convert severity-word map: MEDIUM/important -> MINOR non-blocking, unknown word unset; MEDIUM-drift contradicts reflect halting | 05 §8 | REPRESENTED (MEDIUM, important, drift); full word list COVERED-BY-DEDUP | MS-15 (l.641), l.2193, l.1242, V-295 |
| 05-37 | Two-word labels unmatched; a null class is compatible with any class, so such rows can cluster with Drift/Regression rows | 05 §8.2 | REPRESENTED (labels); cluster consequence OMITTED (MINOR) | DOC-08 (l.669), V-295, l.2214; OM-2 |
| 05-38 | cluster.py: reviewer weight, `support`, uncalibrated, `blocking_any` single-member veto, `disputed`, `cluster_agreement`; `calibration_coverage` in cluster_cmd | 05 §9 | REPRESENTED | l.140, l.364, l.591, l.629, V-508 (l.3446) |
| 05-39 | `support` is a ready hook for a calibrator-weighted rule; none implemented | 05 §9 | REPRESENTED | V-508, C-05 Option C (l.1484-1495) |
| 05-40 | Rule A: consequence prose (spec-panel.md:259, prompts :31), each reviewer self-grades; "Medium" encoded as MAJOR + blocking false | 05 §10.1 | REPRESENTED | C-16 (l.2194-2195, l.2240), l.2765, V-509 |
| 05-41 | Rule B: label rule (findings_v2.py:161-162) not lens-scoped; makes Medium unrepresentable | 05 §10.2 | REPRESENTED | l.2240, D9 (l.596), MS-15 |
| 05-42 | Effective master decision = any one reviewer's flag unioned (ledger.py:187,274); `_decision` never reads confidence | 05 §10.3 | REPRESENTED | D4 (l.591), V-068, V-509 |
| 05-43 | Both rules are on master (#519 ancestor check) | 05 §10 | REPRESENTED | MS-22 (l.648), contradiction 13 (l.750) |
| 05-44 | E2: judge-blocking 65 vs 38 real over 71 rows; example "ember + 2x luna 1.00 judge-blocking is 0.17 real" | 05 §11 | REPRESENTED (65 vs 38); the 0.17 example OMITTED (MINOR) | l.1453, l.1527, V-510; OM-4 |
| 05-45 | E2 wrong blockers per panel (1.83, 3.00, 3.20, 4.75; control 0.00-2.00, replicated 0.83-1.75); surviving +2.75-3.25 (p 0.005-0.03); that panel found 1.75/14, real blocking 0.25/8 | 05 §11 | REPRESENTED (surviving effect, 1.8-4.75 range); per-panel table and 1.75/14, 0.25/8 OMITTED (MINOR) | l.197, l.1438, V-033, V-196; OM-4 |
| 05-46 | E2 caveat: ground truth penalises novel-but-real catches, so defect-rich wrong blockers are an upper bound; the control package is the cleaner measure | 05 §11 | REPRESENTED | l.1527, V-027, V-063, V-510 |
| 05-47 | Veto fails the other way: pilot Arm A passed both defect-rich plans; 0/8 recall; merge drops flipped verdicts (3 named + total loss) | 05 §11 | REPRESENTED | V-034 (l.2972), V-510, l.1527, DOC-11 |
| 05-48 | Merge behaves as designed (0 violations over 264 merges), so wrong blockers are policy not a bug | 05 §11 | REPRESENTED | V-177 (l.3115), l.1996 |
| 05-49 | Two independence rules: id-distinct (panel.py:631-635) vs class-disjoint (prose); no class-distinct check and no calibrator role in panel.py; classes map; kimi/deepseek have no models; 2x luna fails the class rule; E2's useful second luna conflicts | 05 §12 | REPRESENTED | l.1439, l.1422, V-511 (l.3449), DOC-30, DOC-24 |
| 05-50 | §13.1 per-finding rule: advisory and grounding-gap never block; reflect-post per class (regression count vs flag, drift, authorized/necessary, none); `unauthorized_deviation_present` options | 05 §13.1 | REPRESENTED (per class and channel, flag options); the regression count-vs-flag distinction OMITTED (MINOR) | C-16 (l.2214, l.2242), SC-18 (l.542), MS-14, V-512 (l.3450); OM-1 |
| 05-51 | reflect-pre: deviation counts are UC-2 specific; UC-1 blocking by the spec consequence rule | 05 §13.1 | REPRESENTED | V-512 (l.3450), l.2789 |
| 05-52 | spec lens: CRITICAL blocks; MAJOR only with a concrete consequence else Medium; MINOR never | 05 §13.1 | REPRESENTED | C-16 (l.2195, l.2240), l.2789 |
| 05-53 | Converted legacy cards: re-derive blocking from deviation_class; normalise two-word labels first | 05 §13.1 | REPRESENTED | C-16 (l.2214), V-295, DOC-08 |
| 05-54 | §13.2 cluster-level class = highest-precedence member class (Regression > Drift > Necessary > Authorized), mirroring the per-file union rule | 05 §13.2 | OMITTED (MINOR) | OM-2; the report states only the any-member veto |
| 05-55 | §14 options table: veto, quorum, calibrator-weighted, blind grader, debate, each with mechanism/evidence/cost | 05 §14 | REPRESENTED | C-05 Options A-E (l.1456-1540), V-513 |
| 05-56 | Debate row caveats: Stage 0 "6.70%" is an overlap figure; 8 null convergence scores; judge identity often unknown | 05 §14 | REPRESENTED | l.1528, C-08 closed (l.4082), V-330 (l.3268), V-331 (l.3269) |
| 05-57 | Combination: finders flag -> blind class-disjoint decider confirms per cluster; any theta/k needs the E2 packages as regression set | 05 §14 | REPRESENTED | C-05 recommended resolution (l.1536), SC-10 (l.534) |
| 05-58 | Gaps: SKILL §10.10 vs taxonomy:123 conflict; MINOR drift vs parser; Rule A vs B | 05 Gaps | REPRESENTED | l.2243, l.641, Q-12 |
| 05-59 | Gap: rf-qa "IMPORTANT is blocking" vs card_convert important -> MINOR (rf-qa file not read) | 05 Gaps | REPRESENTED | l.1242, SC-11 (l.535), l.2805 |
| 05-60 | Gap: findings-v1 parse path of `superclaude review merge` not re-read | 05 Gaps | COVERED-BY-DEDUP (later files read `findings.py`/`ledger.py`; D1 and D4 are CODE-VERIFIED) | D1 (l.588), D4 (l.591) |
| 05-61 | Questions: class-disjointness for finders vs decider; debate decider (no bump) vs script + blind decider (new merge_method) | 05 Gaps | REPRESENTED | C-04 / C-05 / C-11 (l.1422, l.1536, l.1917) |
| 05-62 | Stale docs: rubric dim3, class list (kimi/deepseek), 5-dim claim, fenced calibration, rotation kimi/deepseek | 05 Stale | REPRESENTED | DOC-29, DOC-30, DOC-28, DOC-31, DOC-24 (l.690, 691, 689, 692, 685) |

File 1 total: 62 findings enumerated: 52 REPRESENTED, 2 COVERED-BY-DEDUP (05-24, 05-60), 3 wholly OMITTED at MINOR (05-07, 05-32, 05-54), 5 REPRESENTED with a MINOR residue omitted (05-19, 05-37, 05-44, 05-45, 05-50). Residues are collected in OM-1 to OM-5.

### File 2 of 8: research/06-input-contract-briefs.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 06-01 | Loop prompts file has five placeholders (CANDIDATE, BASELINE, PRIOR, N, IDS) and none for a driving document | 06 §1.1 | REPRESENTED | D8 (l.595), l.1178, l.452, V-514 (l.3452) |
| 06-02 | First-review brief reviews the candidate "against the requirements it states"; the only input check ("incomplete") can never fire for a missing source | 06 §1.2 | REPRESENTED | D8, l.2529, V-514 |
| 06-03 | Grading line (:31): a requirement the document never states is Medium; no wording for "stated in the source, missing in the plan" | 06 §1.2 | REPRESENTED | V-514, D9 (l.596), l.1855 (grading clause), SC-23 (l.547), l.2194 |
| 06-04 | RE-REVIEW brief assumes the reviewer runs `diff -w` and `grep -nF`, which a read-only no-Bash reviewer cannot do | 06 §1.3 | REPRESENTED | V-515 (l.3453), C-18 (l.2319-2385), l.1820 |
| 06-05 | REVISE brief names only IDS and CANDIDATE; a reviser also needs the source | 06 §1.3 | COVERED-BY-DEDUP into D8 / C-10 (`{{SOURCE}}` is a core placeholder for every brief kind) | l.1855, V-522 |
| 06-06 | Panel CLI wiring (:70): same brief to every member, no persona slicing in E3; merge refuses a round with no valid block; fallback when CLI absent | 06 §1.4 | REPRESENTED | MS-07 (l.633), l.2790 (spec module row), V-541 (l.3479) |
| 06-07 | `## Never` rule: a brief may narrow but not widen scope; a required source read is arguably a widening, so state it in the core contract | 06 §1.4 | OMITTED (MINOR) | OM-6 |
| 06-08 | findings-v1 anchor 12-200 and refs list; no field for a citation into the source; v2 `citations[].role` fills that gap | 06 §1.5 | REPRESENTED | l.1855, V-517 (l.3455), BL-04 (l.607) |
| 06-09 | tests/review/test_review_rules_text.py pins: "no_source_path" pins `src/superclaude` not a source document; INS_A adjacency forces the source clause inside the brief line; v1 example-line pin; Values-to-fill presence pins | 06 §1.6 | REPRESENTED | D8 (l.595), DOC-38 (l.699), l.3856 (INS_A/INS_B/INS_C), V-514 |
| 06-10 | Reflect brief: three sections in order; self-contained; pinned only as template text; no code validates a produced brief | 06 §2.1 | REPRESENTED | V-516 (l.3454), DOC-34 (l.695), SC-8 (l.532), l.1799 |
| 06-11 | No driving-document section in the reflect brief; the spec reaches a reviewer only as persona hunks or the reviewer's own Read | 06 §2.1 | REPRESENTED | l.1799, V-516, l.2787 |
| 06-12 | Shadow line placement inside the T1 excerpt; line text; citation roles "plan or spec" vs six parser roles (CODE-CONTRADICTED); rewritten twice on 2026-11-13 | 06 §2.2 | REPRESENTED | DOC-07 (l.668), DOC-32 (l.693), V-517, V-292 (l.3230); the two-commit history is in V-039 / l.3981 |
| 06-13 | D13: spec body injected for the qa persona only (whole file <= 400 lines else sections); other reviewers source-partial by design | 06 §2.3 | REPRESENTED | V-516, l.1799, l.1820 (400-line precedent), D8 |
| 06-14 | Parsed-sparse escalation: Tier 2 is the normal path for workflow plans (MR:142 figures) | 06 §2.3 | REPRESENTED (with correction) | V-518 (l.3456), DOC-59 (l.720), contradiction 16 (l.753) |
| 06-15 | W-3: `spec:N` is resolved against the short `source.md`, so a spec line number can point at the wrong text | 06 §2.3 | REPRESENTED | l.2854, V-517, V-593 (l.3531) |
| 06-16 | Recorded briefs (45): 23 break the shape, 0 carry the verbatim shadow line, shadow01 has no findings-v2 instruction, preambles, qa carries the spec body, one-line `source.md` delegating, shadow09 `gh issue view 357`, no rule follows a delegating source | 06 §2.4 | REPRESENTED | V-516, V-517, DOC-34, DOC-35 (l.696), l.1799, Q-23 (l.3967) |
| 06-17 | Brief mtimes all precede `c2e3347d3`; which installed skill version each run used is unknown | 06 §2.4, Gaps | REPRESENTED | G-42/G-44 (l.3981), l.2633 |
| 06-18 | E2 runner source shipping (:9-11): `|| true` falls through silently, a stale `source.md` could remain; no source field in meta.json | 06 §3.1 | REPRESENTED (no source field: V-519, l.3457); the silent-fallthrough / stale-copy edge OMITTED (MINOR) | OM-6 |
| 06-19 | E2 brief is a filled copy of the E3 first-review prompt; D8 is one defect in one shared prompt | 06 §3.1 | REPRESENTED | V-519, l.1800, l.2529 |
| 06-20 | Runner cwd (`/tmp/evalsb/repo`) differs from candidate/source location; source only reachable relative to the candidate path | 06 §3.1 | OMITTED (MINOR) | OM-6 |
| 06-21 | Permissions: Bash not disallowed under `bypassPermissions`; only Edit/Write/NotebookEdit denied; sandbox and after-the-fact audit are the safeguards | 06 §3.1 | REPRESENTED | l.2326, l.2373, V-183 (l.3121), SC-9 |
| 06-22 | No required-read verification in the runner; raw transcript is saved so a post-run check is possible | 06 §3.1, §4.2 | REPRESENTED | l.2375, V-519, V-521 (l.3459) |
| 06-23 | Per-package candidates name `./source.md` at :3 and :14; sizes 173/200/134 lines, sources 133/378/20 lines; per-model 156/665 split | 06 §3.2 | REPRESENTED (names the source; 156/665 per-model split) / line counts COVERED-BY-DEDUP | V-169 (l.3107), l.1800, l.1846 |
| 06-24 | E2 sources are full specs while several E1 workflow sources are one-line prompts; `input-parse.md:41` defines `source.md` | 06 §3.2 | REPRESENTED | l.2854, l.2787, Q-23 |
| 06-25 | judge-one.sh: judge never receives `source.md`; judge runs under `bypassPermissions` with no deny list | 06 §3.3 | REPRESENTED | l.1847, l.2326, l.2373, MS-17 (l.643) |
| 06-26 | reflect-reviewer.md: allowlist tools, `permissionMode: plan`, `maxTurns: 50`, pinned by `test_reviewer_readonly_tools.py` (`_MUTATORS`) | 06 §4.1 | REPRESENTED | l.2768, V-520 (l.3458), K-7 (l.559) |
| 06-27 | Safety-constraint prose is the backstop to the mechanical allowlist | 06 §4.1 | COVERED-BY-DEDUP into l.2768 / C-18 (allowlist is the mechanism, prose a backstop) | C-18 |
| 06-28 | Agent expects `spec_path` but the brief template has no such field (CODE-CONTRADICTED) | 06 §4.1 | REPRESENTED | DOC-33 (l.694), V-520 |
| 06-29 | Agent description is UC-2 oriented while shadow mode uses it for UC-1 (STALE DOC) | 06 §4.1, Stale | REPRESENTED | DOC-36 (l.697) |
| 06-30 | "Audit the live shared worktree" is a Will Not, yet recorded briefs name the live worktree; use of `--isolate-reviewers` unverified | 06 §4.1 | REPRESENTED | G-44 (l.3981), V-193 (l.3131) |
| 06-31 | Comparison table reflect/E2/E3: mechanism, Bash, verification of reads, isolation, dispatch | 06 §4.2 | REPRESENTED | C-18 positions (l.2326, l.2373), C-09 (l.1732-1794) |
| 06-32 | Conflict: E3 re-review needs a reviewer with diff/grep while reflect forbids live execution; move Step 1 and the self-check to the orchestrator as injected hunks (FR-4 pattern) | 06 §4.2 | REPRESENTED | V-515, l.1820, l.2331 |
| 06-33 | E2 needed Bash only because it drove a slash command inside `claude -p` (inference) | 06 §4.2 | COVERED-BY-DEDUP into l.2331 (allowlist everywhere; `claude -p --allowedTools`) | C-18 |
| 06-34 | Consumer input matrix (6 consumers); only reflect enforces a required source by a STOP | 06 §5 | REPRESENTED | V-521 (l.3459), l.404-407, l.2787-2790 |
| 06-35 | `sc:workflow` passes `source.md` as reflect's `--spec`, conflating source and spec | 06 §5 | REPRESENTED | l.404, l.2854, Q-23, V-517 |
| 06-36 | Two ways to verify a required read: orchestrator injection (deterministic) vs transcript audit | 06 §5 | REPRESENTED | V-521, l.2375 |
| 06-37 | Design input: `{{SOURCE}}`, optional `{{SPEC}}`, `{{GROUNDING}}`; place the clause inside the brief line for the tests | 06 §6.1 | REPRESENTED | C-10 (l.1795-1858), V-522 (l.3460), l.3856 |
| 06-38 | Brief wording: first-review sentence with `{{SOURCE}}`; grading clause for source omissions; citation roles plan/source/spec | 06 §6.2 | REPRESENTED | l.1855, V-517, C-10 recommended resolution |
| 06-39 | One code-rendered template: Task, Inputs, Grounding hunks, Lens, Output contract; conflicts with C7/C6 | 06 §6.3 | REPRESENTED | MS-05 (l.631), l.1819, l.2769 |
| 06-40 | Source exposure policy: inject into every reviewer under a size cap; above cap hunks + path + transcript check; per-reviewer `source_path/sha256/injected/read` | 06 §6.4 | REPRESENTED | l.1820, l.1855, V-519, SC-8 |
| 06-41 | Read-only policy: allowlist for in-session and `claude -p`; `--allowedTools` behaviour unverified; shell steps moved to the orchestrator | 06 §6.5 | REPRESENTED | l.2331, l.2768 (G-45), l.3979 |
| 06-42 | Gaps 1-16: MR:142 second-hand, 156/665 inference, subcommand registration, installed version, isolate-reviewers, allowlist behaviour, source vs spec roles, Wave 0 snapshot of a named spec, all-reviewer injection cost, judge source, brainstorm/design not wired, PR body only | 06 Gaps | REPRESENTED | G-42 to G-47 (l.3967, 3979, 3981), MS-09 (l.635), V-521, Q-23, Q-24 |
| 06-43 | Stale docs: reflect-reviewer UC-2 text, input list, citation roles, HANDOFF D8 line cite, test-name hazard | 06 Stale | REPRESENTED | DOC-36, DOC-33, DOC-07, DOC-37 (l.698), DOC-38 (l.699) |

File 2 total: 43 findings enumerated: 37 REPRESENTED, 3 COVERED-BY-DEDUP (06-05, 06-27, 06-33), 2 wholly OMITTED at MINOR (06-07, 06-20), 1 REPRESENTED with a MINOR residue omitted (06-18). Residues are collected in OM-6.

### File 3 of 8: research/07-reflect-merge-contract.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 07-01 | `--t2-engine legacy\|shadow` (default legacy); `panel` rejected with a literal message until Stage 3; no Python parser, the flag is a protocol rule | 07 §1.1 | REPRESENTED | V-251 (l.3189), V-302 (l.3240), MS-08 (l.634), contradiction 14 (l.751) |
| 07-02 | Legacy keeps contract 1.8.0; shadow is UC-1 only; UC-2 flag accepted and ignored until Stage 5 | 07 §1.2 | REPRESENTED | l.2788, V-302, C-17 (l.2254-2318) |
| 07-03 | Rules D1-D5 and the D3 floor effects (`t2_floor_unmet`, forced `status: partial`) that apply only with the `panel` engine in Stage 3 | 07 §1.2 | OMITTED (MINOR) for the D3 floor effects; D5 `N_eff` has no code is carried | OM-7; l.632, V-281 (l.3219), V-316 |
| 07-04 | Shadow steps 1-10: step 6 `cluster_agreement` never routes; step 7 writes `merged-verdict.yaml` and records `judge_identity`; step 10 puts shadow fields under `telemetry:` | 07 §1.2 | REPRESENTED | V-281 to V-285 (l.3219-3223), V-271, V-272 |
| 07-05 | Merge path: sc-adversarial Mode A call shape; convergence routing >=0.75 PASS / >=0.60 PARTIAL vs wrapper 0.80 floor | 07 §1.3, §3 | REPRESENTED | V-279 (l.3217), l.2876, l.1893 |
| 07-06 | `--unattended` nested output; `artifacts_dir` -> `adversarial_artifacts_dir` rename | 07 §1.3 | REPRESENTED (call shape and rename kept as a constraint) | l.2875 (7.4.1) |
| 07-07 | Step 5.0 probe and fallbacks F1/F2/F3, "loud, never silent" | 07 §1.3 | REPRESENTED | V-279, l.1921 |
| 07-08 | Contract consumers must route on `merge_method` first; null comparisons guarded; promotion-gate condition 9; sprint null routing | 07 §1.4 | REPRESENTED (C16 partly contradicted) | DOC-39 (l.700), V-300-series C16 row l.3244, K-1 (l.553) |
| 07-09 | EV-1 completion rule (a) merged verdict + cards, (b) loud fallback; MALFORMED handling with up to 2 re-runs; testability row encodes only branch (a) | 07 §1.5 | REPRESENTED | DOC-42 (l.703; row :1955 branch (b) missing), DOC-40 (l.701), V-301 (l.3239) |
| 07-10 | §9.1 header history (1.7.x EV-1/EV-2 added with "no stable-field change"; field/value additions have always been bumps) | 07 §1.6, Q2 | OMITTED (MINOR) | OM-7 |
| 07-11 | EV-2: legal `merge_method` values exactly adversarial / single-reviewer-fallback; "Reflect MUST NOT synthesize its own merge"; `user_decision_required` defined on convergence | 07 §1.6 | REPRESENTED | C-11 Evidence (l.1910), V-523 (l.3461), K-1 |
| 07-12 | §9.2: 19 nested telemetry keys; `memory_status` anomaly vs testability row | 07 §1.7 | REPRESENTED | DOC-42, V-534 (l.3472), V-656 (l.3594) |
| 07-13 | panel_lint constants copied by regex from SKILL.md §9.1/§9.2; L0-L7 and bump rule B | 07 §2.1-2.2 | REPRESENTED | V-257 (l.3195), V-264 (l.3202), l.1891 |
| 07-14 | EV-1 in code: card count max(2, resolved), branch (a)/(b); F3 branch stricter than the text (CODE-CONTRADICTED) | 07 §2.3 | REPRESENTED | DOC-40 (l.701), l.1921 |
| 07-15 | Lint/EV-1 do not cover the `--unattended` nested layout (L6 reports `merged-verdict: absent`) | 07 §2.3, Q3 | OMITTED (MINOR) | OM-7 |
| 07-16 | L2 does not inspect `telemetry:` contents, the legal extension point | 07 §2.3 | REPRESENTED | l.1870, l.2874, l.3920 |
| 07-17 | Wrapper version gate: missing/major != 1 BLOCKED; 2.0.0 blocks, 1.9.0 passes the gate | 07 §3 | REPRESENTED | l.1893, l.1907, l.2876 |
| 07-18 | Wrapper never validates `merge_method` values; only single-reviewer-fallback is read | 07 §3 | REPRESENTED | C-11 Evidence (l.1910), V-523 |
| 07-19 | Wrapper 0.80 floor is stricter than SKILL 0.75; a script merge emitting no convergence score would DEGRADE every T2 run | 07 §3 | REPRESENTED | l.2876, C-11 Option B (l.1884), V-523 |
| 07-20 | Anomaly: four wrapper-read keys (`verification_verified`, `reviewers_verified`, `regression_verified`, `adversarial_subrun_status`) outside both lint lists; `ensemble.py` writes them | 07 §3, §8a | REPRESENTED | MS-13 (l.639), ENS-7 (l.657) |
| 07-21 | tests/cli/reflect has 38 test files, not "twelve"; list of the relevant ones | 07 §4 | REPRESENTED | DOC-43 (l.704), contradiction 6 (l.743), V-558 (l.3496) |
| 07-22 | C1/C6/C14 compare with HEAD, skip without git history, guard only uncommitted edits; only the constants-vs-SKILL pin crosses commits | 07 §4.1, Q5 | REPRESENTED | MS-18 (l.644), V-263 (l.3201), K-3 (l.555), l.1914 |
| 07-23 | Lint tests pin `merge_method: panel` (F2) and `1.9.0` (F3) failing; constants sizes 110/27; EV-1 cases F12-F18 | 07 §4.2 | REPRESENTED | V-264 (l.3202), l.1891 |
| 07-24 | test_shadow_exit_script and test_verdict_replay_script details (rewritten live test; exit codes; writes only `--out`) | 07 §4.3-4.4 | REPRESENTED | V-265, V-266 (l.3203-3204), DOC-70 (l.731) |
| 07-25 | Kernel coupling in tests: reflect tests import `findings`, `findings_v2`, `cluster_cmd`, `manifest`, `panel.load_tiers`; a shared core must keep these paths or change tests together | 07 §4 Key | REPRESENTED | V-274 (l.3212, cross-stack coupling), V-268 (l.3206) |
| 07-26 | Live exit output: 13 of 20 counted, shadow02 incomplete, EV-1 8/13 vs 3/39, parity 6, lint/manifest 9, clean runs 10, 11, 12, 14, compliance 0.704, cluster_agreement 1.0 | 07 §5 | REPRESENTED | l.161, V-275 (l.3213), MS-12 (l.638), C-A (l.497) |
| 07-27 | Reading: causes are orchestrator contract-writing/placement lapses, none a merge-quality failure | 07 §5.1 | REPRESENTED | l.161, l.2505 |
| 07-28 | reflect_shadow_exit.py: shadow set selection, `tele()` tolerance, parity recompute, `ev1_fail` counts a missing contract as failure, FAIL/INSUFFICIENT/PASS | 07 §6.1 | REPRESENTED | V-262 (l.3200), OPEN-02 (l.661), MS-13 |
| 07-29 | Aggregator calls the lint with the run's own contract, so L7 parity never fires | 07 §6.1 | OMITTED (MINOR) | OM-7 |
| 07-30 | reflect_verdict_replay: legacy set, paired by dir name; reason-set comparison not paired; a bumped contract is skipped silently | 07 §6.2 | REPRESENTED (reason-set vs paired; both scripts bound to "1.8.0"); the silent-skip residue OMITTED (MINOR) | l.1891, l.1893, l.1536 (paired replay); OM-7 |
| 07-31 | Three "no contract" runs are unparseable YAML (`[1m]` in an unquoted flow list) | 07 §7.1 | REPRESENTED | l.1913, MS-13, V-525 (l.3463) |
| 07-32 | Per-run placement table of `merged-verdict.yaml`, debate artifacts, convergence, cluster_agreement, judge_identity | 07 §7.2 | REPRESENTED (placement and counts) / per-run cells COVERED-BY-DEDUP | V-528 (l.3466), V-343 (l.3281), l.2505 |
| 07-33 | Three merged-verdict files read (shadow09 inline merge with no debate artifacts, shadow12, shadow13 `role: evidence` not a v2 role) | 07 §7.3 | REPRESENTED (shadow09); shadow12/13 details COVERED-BY-DEDUP into the 6-of-14 inline finding | l.1911, V-524 (l.3462) |
| 07-34 | sc-adversarial Mode A return contract has no `merge_method`, no judge identity, writes no `merged-verdict.yaml` | 07 §7.4 | REPRESENTED | MS-24 (l.650), l.1921, DOC-41 (l.702) |
| 07-35 | Agent delegation (debate-orchestrator etc.) vs inline: unverified; 6 of 14 judged inline | 07 §7.4 | REPRESENTED | G-50 (l.3982), V-524 |
| 07-36 | EV-1 is self-attested; shadow09 violates EV-2 in substance, undetectable by the lint; `cluster_agreement` leaks into the merge path (09, 11) | 07 §7.5 | REPRESENTED | MS-12 (l.638), DOC-41, l.1911, V-524 |
| 07-37 | Convergence 1.0 in 9 of 14; cluster_agreement 1.0 in 10 of 11 (later replaced); debate lower in 03, 07, 14 | 07 §7 Key | REPRESENTED (with correction) | l.1524, l.1531 (10-of-11 deliberately not used), l.1912 |
| 07-38 | UC-2 readiness table: templates exist, rules, parser lens, no brief line, reviewer output table, 48 post dirs with 0 findings blocks | 07 §8 | REPRESENTED | V-526 (l.3464), l.2788, C-17 |
| 07-39 | UC-2 gaps 1-5 (no findings-v2 block; category names; HIGH/MEDIUM/LOW vs CRITICAL/MAJOR/MINOR; advisory not forced non-blocking; extra contract fields no kernel output produces) | 07 §8 | REPRESENTED | MS-15 (l.641), DOC-08, l.2281 |
| 07-40 | §8a engine: route, third merge path, `merge_method` label, clean defaults, two contract writers, C1-C16 for this caller, what to keep unchanged | 07 §8a | REPRESENTED | C-17 (l.2254-2318), ENS-1..9 (l.651-659), MS-13, l.2788 |
| 07-41 | C1-C16 re-verification table (12 of 16 code-backed; C13 process; C5 protocol-only; C16 partly contradicted) | 07 §9 | REPRESENTED | K-1..K-3 (l.553-555), V-300 to V-304 (l.3238-3242), DOC-39, DOC-62 (l.723) |
| 07-42 | Answers Q1-Q8: debate vs script merge; legal values and bump rule; EV-1; HEAD pins; UC-2; Stage 2 exit; what a reflect module must keep unchanged (items 1-9) | 07 §10 | REPRESENTED | C-11 (l.1859-1926), 7.4.1 (l.2868-2887), V-529 (l.3467) |
| 07-43 | Open items: sprint/promotion-gate code not read; swarm key list; whether `T2Model0N` pool holds the executor family; C13 enforcement; `--t2-engine panel` message has no code home | 07 Gaps | REPRESENTED | G-52, G-63, G-66 (l.3975-3982), V-409, V-467 |
| 07-44 | Questions: EV-1 rewritten so the merge step writes the verdict; orchestrator writes contracts through a YAML serializer; paired evidence run before any Stage 3 replacement; `channel: advisory` forces `blocking: false` | 07 Gaps | REPRESENTED | C-11 recommended resolution (l.1919-1921), G-57, C-16 (l.2250) |
| 07-45 | Stale docs: testability map `memory_status`, SKILL:714 EV-1 rationale vs installed sc-adversarial artifacts, row :1955 covers only branch (a), "twelve files" | 07 Stale | REPRESENTED | DOC-42, DOC-41, DOC-43 |

File 3 total: 45 findings enumerated: 40 REPRESENTED (07-32 and 07-33 each with a COVERED-BY-DEDUP part), 4 wholly OMITTED at MINOR (07-03, 07-10, 07-15, 07-29), 1 REPRESENTED with a MINOR residue omitted (07-30). Residues are collected in OM-7.

### File 4 of 8: research/08-run-recording-telemetry.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 08-01 | manifest.py data model: schema `review-panel-manifest/1`, frozen fields, input/policy hashes, stages, attempts, reviewer counts, failure_reason | 08 §1.1 | REPRESENTED | MS-04 (l.630), V-531 (l.3469), l.453 |
| 08-02 | Stages `frozen..published` + `failed`; `advance_stage` rules (strict order, 64-hex outputs, hash chain, `resolved` payload rules); `validate` does not re-check the chain or `reviewers_complete` | 08 §1.2 | REPRESENTED | V-531, MS-04, G-72 (l.3984 area), l.1616 |
| 08-03 | Attempts: valid only in an open per-reviewer stage; a new attempt after a `complete` one raises Conflict ("would add a vote"); only a hash of the payload is stored | 08 §1.3 | REPRESENTED (hash-only payload); the open-stage and Conflict rules OMITTED (MINOR) | MS-04, V-531, C-07 (l.1616); OM-9 |
| 08-04 | Resume: same inputs reuse, changed inputs new invocation with history; a `failed` run cannot be retried in place; `reusable_stages` has no in-package caller | 08 §1.4 | REPRESENTED | V-531, V-537 (l.3475), MS-04, l.1616; replay-before-failed-check edge OM-9 |
| 08-05 | Publish: `PUBLISH_FILES`, crash window and re-publish recovery, refused in shadow mode, shadow hashes recorded by `advance published` | 08 §1.5 | REPRESENTED (publish commit point kept); crash-window recovery detail OMITTED (MINOR) | V-531, C-07, l.1870; OM-9 |
| 08-06 | manifest_cmd: init/advance/validate; policy hashes are caller-computed so the policy hash is only as honest as the caller; failed reason defaults "unspecified" | 08 §2 | REPRESENTED | V-532 (l.3470), C-07 (l.1664), l.2770 |
| 08-07 | telemetry.py: two record kinds (`reviewer_run`, `outcome`), six groups incl. three model identities, `KINDS` naming trap, context label regex, truth bases | 08 §3.1 | REPRESENTED | V-004 (l.2942), V-533 (l.3471), D15 (l.602), l.454, C-07 Option C |
| 08-08 | D15: strata fixed to sonnet/haiku; rejects every gateway class; `_ID_TOKEN` is at :23 not :22 | 08 §3.2 | REPRESENTED | D15 (l.602), V-079 (l.3017), DOC-16 (l.677) |
| 08-09 | Storage/loader: month-boundary file reuse, append-only, `INSERT OR IGNORE`, supersession, `cost_per_confirmed_tp` uses `tokens_out` only | 08 §3.3 | REPRESENTED (append-only, idempotent load); `tokens_out`-only cost metric and month-boundary detail OMITTED (MINOR) | V-533; OM-9 |
| 08-10 | Telemetry has no caller in `src` (grep); tests build records by hand | 08 §3.4 | REPRESENTED | D15, V-533, MS-04 |
| 08-11 | telemetry_cmd: default dir/env override; `append` of a list is not atomic; no derivation from transcripts | 08 §4 | REPRESENTED | D15 (l.602), V-533, Q row l.3984 |
| 08-12 | merge_cmd writes no telemetry; ledger keeps the intended model only; dropped finding ids not stored | 08 §5 | REPRESENTED | MS-04 (l.630), V-533, V-536 (l.3474), D1 (l.588) |
| 08-13 | Reflect §9.2 contract and code writers table (ensemble contract, swarm contract, runner.write_reflect_post, write_sidecar, exit sentinel, skill-path agent) | 08 §6 | REPRESENTED | MS-13 (l.639), ENS-7 (l.657), DOC-47 (l.708), V-534 (l.3472), V-527 (l.3465) |
| 08-14 | Stage 2 panel keys under `telemetry:` and what code vs agent produces them; four places hold reflect run data | 08 §6 | REPRESENTED | V-534, l.454, MS-13 |
| 08-15 | E2 committed tree: 1263 `*.meta.json`, 0 `fallback.log`, 0 raw `attemptN.json`, so audit A cannot be re-run from the commit | 08 §7.1 | REPRESENTED (not re-runnable; no fallback.log/attempt files) | DOC-14 (l.675), V-054 (l.2992), G-39 (l.630, l.1657); the count 1263 is a detail |
| 08-16 | Runner derived facts: wall, `OBS`, `TOK`, `MODEL_OK`, `BLOCK_OK`, ladder with `EXCLUDE_MODELS`, never-revisit, 2 attempts | 08 §7.2 | REPRESENTED | l.182, V-020 (l.2958), V-047 (l.2985) |
| 08-17 | Record formats: meta.json fields (sample), cost.json, free-text `fallback.log` | 08 §7.3 | REPRESENTED | l.222, V-535 (l.3473), DOC-46 (l.707) |
| 08-18 | Intended vs served: `expected_model` overwritten on fallback, `attempt=0` reset overwrites files, stale files inflate cost, auxiliary calls counted, intended model kept outside the record | 08 §7.4 | REPRESENTED | l.207, V-173 (l.3111), V-174, V-175, V-535 |
| 08-19 | Cost and time fields: output tokens and wall only; no input/cache tokens, money or start timestamp | 08 §7.5 | REPRESENTED | l.454, V-535, l.2770 |
| 08-20 | Audit A: checks table (1, 1b, 2-6, E1-E11, R1), results (0 mismatches over 828 resolved runs, 2 EXCLUDE, 59 extra-key runs, 5 stale-attempt runs), `audit.py:33` anomaly | 08 §8.1 | REPRESENTED (2 EXCLUDE, 59/57, stale attempts, anomaly) / the 828-run figure, check-4 zero diffs and the per-check table OMITTED (MINOR) | V-054 (l.2992), DOC-14 (l.675), V-173..V-175; OM-8 |
| 08-21 | Audit D: checks table (panel/paths, block ok, conservation, blocking consistency, stale/doc sha, model), results (80 reviewer-level EXCLUDE, 10 EXCLUDE + 78 WARN, 49 blocking dropped, 16 stale, doc sha matched in all 264, drop reasons 56/18/14/3/1, 3 flips, 45 merges without merge-stdout), chain counts 195/1398 (audit2.py) | 08 §8.2 | REPRESENTED (80, 49, 16, drop reasons, 3 flips, 45 merges, 195/1398) / the 10 EXCLUDE + 78 WARN split and the doc-sha-matched fact OMITTED (MINOR) | l.200, l.1304, V-057 (l.2995), V-053, V-178, DOC-18 (l.679); OM-8 |
| 08-22 | Each audit check as a built-in check (A-1/A-4, A-2, A-5, D-3, D-5, D-1, D X1, D-4) with hook and "product lacks it today" evidence | 08 §8.3 | REPRESENTED | V-536 (l.3474), SC-7 (l.531), l.1616 |
| 08-23 | reflect_shadow_exit.py: keys read, run selection, not aggregated (calibration_coverage, identity, cost); parity recompute; only `mf.validate` used; no caller for `reusable_stages`/`read_committed` | 08 §9 | REPRESENTED | V-537 (l.3475), V-262 (l.3200), l.2778 |
| 08-24 | extract.py: per-run record fields, served model per sub-agent call from `parent_tool_use_id`, cost from `total_cost_usd`/`modelUsage`, sample run (haiku slot served by gpt-6.1-sol; USD and minutes), anomalies | 08 §10 | REPRESENTED | V-538 (l.3476), the scope/04 extract.py row at l.3296, l.1370, SC-4 (l.528) |
| 08-25 | Cross-effort comparison table of run records (state, resume, policy/input identity, attempt, intended/served model, fallback, cost, counters, scoring, integrity, writer) | 08 §11.1 | REPRESENTED | overlap matrix l.450-454, V-530 (l.3468) |
| 08-26 | Cost and time per reviewer: E1 none in product, E2 per attempt, E3 schema only | 08 §11.2 | REPRESENTED | l.454, G-73, V-538 |
| 08-27 | Design input: nine points (profile stages, stored attempt payloads, fallback as attempts, kept/rejected counters, built-in checks, telemetry as projection, CLI-copied summary fields, CLI-computed policy hashes, retry in place) | 08 §11.3 | REPRESENTED | C-07 (l.1605-1667, esp. l.1616 and l.1664), V-539 (l.3477), l.2770-2780 |
| 08-28 | Doc-sourced claims table with verification tags (13 rows) | 08 §12 | REPRESENTED | DOC-45/46/47/16/14/18 (l.706-708, 677, 675, 679), V-539, G-76 |
| 08-29 | Gaps 1-17 (validate chain, failed retry, attempt payloads, per-reviewer cost, agent-written telemetry drift, strata owner decision, KINDS, atomic append, no telemetry in merge, E2 files not committed, expected_model overwrite, audit.py:33, which script replays `_check_finding`, panel_cmd telemetry, contract schema duplication, [CODE-CONTRADICTED] carry list, warn vs fail) | 08 Gaps | REPRESENTED | G-72..G-76, G-39 (l.630, l.675, l.1657), Q rows l.3984, MS-04, MS-13 |
| 08-30 | Stale docs: `_ID_TOKEN` line, hand-off "summaries in summary.md", `meta.json` "attempts", `/tmp/audit-*` paths | 08 Stale | REPRESENTED | DOC-16 (l.677), DOC-45 (l.706), DOC-46 (l.707), DOC-14 (l.675) |

File 4 total: 30 finding groups enumerated (several groups hold up to a dozen sub-facts; sub-facts are judged individually in the status cell): 24 REPRESENTED, 0 whole-row COVERED-BY-DEDUP, 0 wholly OMITTED, 6 REPRESENTED with a MINOR residue omitted (08-03, 08-04 edge case, 08-05, 08-09, 08-20, 08-21). Residues are collected in OM-8 and OM-9.

### File 5 of 8: synthesis/synth-02-target-gaps.md (report Sections 3 and 4)

Coverage method for this file: the report's Sections 3 and 4 are the evolved copy of this synthesis. Every ID was located in the report by regex; every text line of the synthesis was compared with the report by a word-level diff (40 synthesis lines differ, all as in-place revisions made by later gates, 61 deleted phrases, none a dropped finding; 58 report lines carry additions). "Where" gives the report line of the row.

Part A: front matter, target state, success criteria, constraints, external context

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S02-01 | Conventions table (effort tags, verification tags, line-number re-read, migration tracks M1-M4, external context rule, log ids) | synth-02 | REPRESENTED | l.482-491 |
| S02-02 | Desired behaviour: one shared core plus thin per-use-case modules; derived from research design inputs | synth-02 | REPRESENTED | l.493 |
| S02-03 | Consumer C-A sc:reflect Tier 2 (UC-1 pre, UC-2 post), M2 | synth-02 | REPRESENTED | l.497 |
| S02-04 | Consumer C-B sc:workflow tasklist review and sc:tasklist gates, M3 | synth-02 | REPRESENTED (extended with Stage 10.5 flags) | l.498 |
| S02-05 | Consumer C-C spec-panel Review Loop, M3 | synth-02 | REPRESENTED | l.499 |
| S02-06 | Consumer C-D spec review for brainstorm and design, M3 | synth-02 | REPRESENTED | l.500 |
| S02-07 | Consumer C-E PR review then rf-qa replacement, M4 | synth-02 | REPRESENTED | l.501 |
| S02-08 | Architecture diagram (consumers over the shared core pipeline) | synth-02 | REPRESENTED | l.503-519 |
| S02-09 | SC-1 one finding contract validates v1, v2 and code-review findings | synth-02 | REPRESENTED | l.525 |
| S02-10 | SC-2 no blocking finding lost at merge (49 lost: 24/14/10/1) | synth-02 | REPRESENTED | l.526 |
| S02-11 | SC-3 minimum valid reviewers; invalid reviewer cannot clear a row | synth-02 | REPRESENTED | l.527 |
| S02-12 | SC-4 observed identity recorded per slot | synth-02 | REPRESENTED | l.528 |
| S02-13 | SC-5 contract 1.8.0 byte-identical; G8 82 and G9 271 tests | synth-02 | REPRESENTED | l.529 |
| S02-14 | SC-6 one clusterer (anchor-only, T01.02, D-P1, cap, chained flag, 195/1398, 83) | synth-02 | REPRESENTED (extended with pass rule) | l.530 |
| S02-15 | SC-7 one run record with built-in checks | synth-02 | REPRESENTED | l.531 |
| S02-16 | SC-8 one code-rendered brief template; 23 of 45 deviate | synth-02 | REPRESENTED | l.532 |
| S02-17 | SC-9 every reviewer read-only on every dispatch path | synth-02 | REPRESENTED | l.533 |
| S02-18 | SC-10 blocking decider separate and measured before it replaces the veto | synth-02 | REPRESENTED (extended) | l.534 |
| S02-19 | SC-11 lossless severity; medium first-class | synth-02 | REPRESENTED | l.535 |
| S02-20 | SC-12 reachability (control C8), subcommand set pinned | synth-02 | REPRESENTED (extended) | l.536 |
| S02-21 | SC-13 post gate keeps CLI/exit codes and can HALT | synth-02 | REPRESENTED | l.537 |
| S02-22 | SC-14 PR and rf-qa plug in by declaring a lens module | synth-02 | REPRESENTED (reworded to X1-X14 and stubs) | l.538 |
| S02-23 | SC-15 Review Loop pins stay green | synth-02 | REPRESENTED | l.539 |
| S02-24 | SC-16 reflect panel mode only after Stage 2 exit; EV-1 reads a file the merge step wrote | synth-02 | REPRESENTED (route made concrete) | l.540 |
| S02-25 | SC-17 distinctness declared per template, replicas optional | synth-02 | REPRESENTED | l.541 |
| S02-26 | K-1 contract 1.8.0 pins (C1-C4, C16) | synth-02 | REPRESENTED | l.553 |
| S02-27 | K-2 C5, C11, C12 bind the skill path; ensemble.py conflicts | synth-02 | REPRESENTED | l.554 |
| S02-28 | K-3 text pins in SKILL.md and briefs (C6, C7, C8, C14) HEAD-relative | synth-02 | REPRESENTED | l.555 |
| S02-29 | K-4 `src/superclaude/` source of truth; `.claude/` never staged | synth-02 | REPRESENTED | l.556 |
| S02-30 | K-5 installed primitives never name `src/superclaude/` paths | synth-02 | REPRESENTED | l.557 |
| S02-31 | K-6 uv only | synth-02 | REPRESENTED | l.558 |
| S02-32 | K-7 reviewers read-only; rf-qa/rf-analyst not reusable as panel reviewers | synth-02 | REPRESENTED | l.559 |
| S02-33 | K-8 PRs only to the fork | synth-02 | REPRESENTED | l.560 |
| S02-34 | K-9 test pins that move with a contract change (goldens, live7 coupling, seven-bullet loop, S1-S3/S5) | synth-02 | REPRESENTED | l.561 |
| S02-35 | K-10 environment facts dated and runtime-dependent | synth-02 | REPRESENTED (extended: tier1a fallback detail) | l.562 |
| S02-36 | K-11 scope: report only, E2 at the commit, second report merged later | synth-02 | REPRESENTED | l.563 |
| S02-37 | External context rows 1-8 (union vs weighted voting; LLM validators; panels vs single judge; debate vs meta-judge; production review systems; severity interchange; finding identity; judge calibration) | synth-02 | REPRESENTED | l.569-576 |
| S02-38 | C8 rule text and how it is applied in this run (rows carrying the C8 note: D14, MS-11, MS-14, ENS-1, ENS-3, ENS-4, ENS-5) | synth-02 | REPRESENTED | l.580-582 |

Part B: gap rows D1-D16 and BL-01 to BL-23

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S02-D1 | D1 over-length / ill-formed fields rejected silently (49 blocking lost) | synth-02 | REPRESENTED | l.588 |
| S02-D2 | D2 a `resolved_check` row clears when a re-reporter's block was invalid | synth-02 | REPRESENTED | l.589 |
| S02-D3 | D3 a round can PASS on one valid reviewer | synth-02 | REPRESENTED | l.590 |
| S02-D4 | D4 one reviewer's `blocking` decides the row and verdict | synth-02 | REPRESENTED | l.591 |
| S02-D5 | D5 missing anchors kept silently and can block | synth-02 | REPRESENTED | l.592 |
| S02-D6 | D6 clustering over/under-merges (transitive union-find) | synth-02 | REPRESENTED | l.593 |
| S02-D7 | D7 ref-id regex misses tasklist ids | synth-02 | REPRESENTED | l.594 |
| S02-D8 | D8 brief never names the driving source | synth-02 | REPRESENTED | l.595 |
| S02-D9 | D9 `missing-requirement` Medium in brief vs blocking in schema; three rules | synth-02 | REPRESENTED | l.596 |
| S02-D10 | D10 `unpassable-ac` rejected | synth-02 | REPRESENTED | l.597 |
| S02-D11 | D11 `distinct_across_slots` silently re-admits duplicates | synth-02 | REPRESENTED | l.598 |
| S02-D12 | D12 env select keys on `$T3Model01`; `T2bModel01` never read | synth-02 | REPRESENTED | l.599 |
| S02-D13 | D13 `lint_cmd` / `estimate_cmd` registered but missing | synth-02 | REPRESENTED (revised, test coverage nuance) | l.600 |
| S02-D14 | D14 #346 merge/ledger/panel CLI has no in-repo caller but one prose paragraph | synth-02 | REPRESENTED | l.601 |
| S02-D15 | D15 telemetry strata only sonnet/haiku; merge and resolve write no telemetry | synth-02 | REPRESENTED | l.602 |
| S02-D16 | D16 round 4 accepted; `--cap` ignored on an existing ledger; verify-only not a code mode | synth-02 | REPRESENTED | l.603 |
| S02-BL01 | BL-01 closed lens tuple | synth-02 | REPRESENTED | l.604 |
| S02-BL02 | BL-02 spec-only categories | synth-02 | REPRESENTED | l.605 |
| S02-BL03 | BL-03 three-level severity, MINOR never blocks | synth-02 | REPRESENTED | l.606 |
| S02-BL04 | BL-04 location types beyond a text anchor | synth-02 | REPRESENTED | l.607 |
| S02-BL05 | BL-05 single-document candidate | synth-02 | REPRESENTED | l.608 |
| S02-BL06 | BL-06 clustering key is document-relative | synth-02 | REPRESENTED | l.609 |
| S02-BL07 | BL-07 requirement-id regex as the ref token | synth-02 | REPRESENTED | l.610 |
| S02-BL08 | BL-08 templates bind models, not roles | synth-02 | REPRESENTED | l.611 |
| S02-BL09 | BL-09 `--kind` accepts only first and re-review | synth-02 | REPRESENTED | l.612 |
| S02-BL10 | BL-10 telemetry strata and document-shaped task fields | synth-02 | REPRESENTED | l.613 |
| S02-BL11 | BL-11 no monotonicity or regression halt in the ledger stop rule | synth-02 | REPRESENTED | l.614 |
| S02-BL12 | BL-12 read-only panel vs in-place fixing | synth-02 | REPRESENTED | l.615 |
| S02-BL13 | BL-13 three verdict contracts, no single owner | synth-02 | REPRESENTED | l.616 |
| S02-BL14 | BL-14 closed PR reviewer set | synth-02 | REPRESENTED | l.617 |
| S02-BL15 | BL-15 PR seam undecided: finder or verifier | synth-02 | REPRESENTED | l.618 |
| S02-BL16 | BL-16 cross-source agreement never changes PR severity | synth-02 | REPRESENTED | l.619 |
| S02-BL17 | BL-17 PR router diverges from its rubric on seven points | synth-02 | REPRESENTED | l.620 |
| S02-BL18 | BL-18 PR finding fields absent from the contract | synth-02 | REPRESENTED | l.621 |
| S02-BL19 | BL-19 "zero issues is suspect" wording in rf-qa agents | synth-02 | REPRESENTED | l.622 |
| S02-BL20 | BL-20 migration surface and text pins of rf-qa | synth-02 | REPRESENTED | l.623 |
| S02-BL21 | BL-21 rf-qa-qualitative needs a lens per document type | synth-02 | REPRESENTED | l.624 |
| S02-BL22 | BL-22 verification stage as a pluggable gate | synth-02 | REPRESENTED | l.625 |
| S02-BL23 | BL-23 five severity vocabularies, three ways of deciding blocking | synth-02 | REPRESENTED | l.626 |

Part C: missing-shared-piece rows MS-01 to MS-23, ENS-1 to ENS-9, OPEN-01 to OPEN-02

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S02-MS01 | MS-01 no single finding contract | synth-02 | REPRESENTED | l.627 |
| S02-MS02 | MS-02 no single clusterer | synth-02 | REPRESENTED | l.628 |
| S02-MS03 | MS-03 no single merge and verdict stage | synth-02 | REPRESENTED | l.629 |
| S02-MS04 | MS-04 no single run record | synth-02 | REPRESENTED | l.630 |
| S02-MS05 | MS-05 no single brief template | synth-02 | REPRESENTED | l.631 |
| S02-MS06 | MS-06 resolver policy not declared | synth-02 | REPRESENTED | l.632 |
| S02-MS07 | MS-07 CLI is helpers, not a review runner | synth-02 | REPRESENTED | l.633 |
| S02-MS08 | MS-08 hook for Wave 4 and Stage 10.5 | synth-02 | REPRESENTED | l.634 |
| S02-MS09 | MS-09 no spec-review hook for brainstorm/design | synth-02 | REPRESENTED | l.635 |
| S02-MS10 | MS-10 Review Loop frozen by tests | synth-02 | REPRESENTED | l.636 |
| S02-MS11 | MS-11 observed identity has no implementation (C8) | synth-02 | REPRESENTED | l.637 |
| S02-MS12 | MS-12 reflect panel mode not enabled; Stage 2 FAIL; EV-1 self-attested | synth-02 | REPRESENTED | l.638 |
| S02-MS13 | MS-13 two reflect contract writers; unparseable YAML | synth-02 | REPRESENTED | l.639 |
| S02-MS14 | MS-14 `unauthorized_deviation_present` no producer (C8) | synth-02 | REPRESENTED | l.640 |
| S02-MS15 | MS-15 reflect blocking-rule conflicts | synth-02 | REPRESENTED | l.641 |
| S02-MS16 | MS-16 calibration rubric and class rules do not fit | synth-02 | REPRESENTED | l.642 |
| S02-MS17 | MS-17 no portable evaluation instrument or ground truth for non-veto deciders | synth-02 | REPRESENTED | l.643 |
| S02-MS18 | MS-18 contract pins are HEAD-relative | synth-02 | REPRESENTED | l.644 |
| S02-MS19 | MS-19 experiment variants not promoted, not in `src` | synth-02 | REPRESENTED | l.645 |
| S02-MS20 | MS-20 target environment unresolved | synth-02 | REPRESENTED | l.646 |
| S02-MS21 | MS-21 no evidence for rounds 2-3 under a multi-reviewer ledger | synth-02 | REPRESENTED | l.647 |
| S02-MS22 | MS-22 ownership of `cli/review/` undecided | synth-02 | REPRESENTED | l.648 |
| S02-MS23 | MS-23 differences against the other session's second report | synth-02 | REPRESENTED | l.649 |
| S02-ENS1 | ENS-1 post gate cannot HALT on a found deviation (C8) | synth-02 | REPRESENTED | l.651 |
| S02-ENS2 | ENS-2 post-gate reviewers see only the tasklist text | synth-02 | REPRESENTED | l.652 |
| S02-ENS3 | ENS-3 `executor_model_class` read but never used on Tier 2 (C8) | synth-02 | REPRESENTED | l.653 |
| S02-ENS4 | ENS-4 `REPORT.md` and verdict matrix never produced (C8) | synth-02 | REPRESENTED | l.654 |
| S02-ENS5 | ENS-5 bounded `--fix` loop cannot trigger (C8) | synth-02 | REPRESENTED | l.655 |
| S02-ENS6 | ENS-6 `merge_method` is a reviewer-count label | synth-02 | REPRESENTED | l.656 |
| S02-ENS7 | ENS-7 two incompatible reflect contracts share one file name and reader | synth-02 | REPRESENTED | l.657 |
| S02-ENS8 | ENS-8 smaller engine defects (exit-code map, rc = 0, shortfall, empty target, nested --remediate) | synth-02 | REPRESENTED | l.658 |
| S02-ENS9 | ENS-9 replace `ensemble.py` or fix in place | synth-02 | REPRESENTED | l.659 |
| S02-OP1 | OPEN-01 re-review protocol undecided | synth-02 | REPRESENTED | l.660 |
| S02-OP2 | OPEN-02 legacy EV-1 baseline may be mis-stated | synth-02 | REPRESENTED | l.661 |

Part D: DOC rows, contradictions, coverage self-check, track table

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S02-DOC01..10 | DOC-01 card_convert counter premise; DOC-02 findings_v2 docstring; DOC-03 severity-rubric vs router; DOC-04 ledger row field names; DOC-05 category-map line cite; DOC-06 loop prompt findings line omits limits; DOC-07 shadow brief omits limits and roles; DOC-08 reflect-reviewer two-word labels; DOC-09 ledger docstring on clearing; DOC-10 confidence "never used" | synth-02 | REPRESENTED (ten rows) | l.662-671 |
| S02-DOC11..20 | DOC-11 "4 verdicts flipped"; DOC-12 D2 coverage wording; DOC-13 `--round` help text; DOC-14 audit scripts' /tmp paths; DOC-15 variants "experiment copies only"; DOC-16 `_ID_TOKEN` line; DOC-17 `anch.py` as chaining evidence; DOC-18 195 of 1398; DOC-19 cluster_agreement null / 1.000; DOC-20 `identity_source: observed` adapter (C8) | synth-02 | REPRESENTED (ten rows) | l.672-681 |
| S02-DOC21..30 | DOC-21 hand-off panel.py lines; DOC-22 gateway note; DOC-23 live7 description; DOC-24 rotation kimi/deepseek; DOC-25 "designed, NOT run" status; DOC-26 find_path unverified; DOC-27 "no skill calls panel resolve"; DOC-28 calibrator 5-dim claim; DOC-29 rubric dimension 3 vocabulary; DOC-30 calibrator class list | synth-02 | REPRESENTED (ten rows) | l.682-691 |
| S02-DOC31..40 | DOC-31 fenced calibration; DOC-32 brief role list; DOC-33 spec_path input; DOC-34 C7 three sections vs recorded briefs; DOC-35 L4 live-execution breach; DOC-36 reflect-reviewer UC-2 text; DOC-37 hand-off D8 line cite; DOC-38 test-name hazard; DOC-39 C16 route on merge_method; DOC-40 EV-1 branch (b) F3 | synth-02 | REPRESENTED (ten rows) | l.692-701 |
| S02-DOC41..50 | DOC-41 EV-1 "reads disk, NOT self-written"; DOC-42 testability rows `memory_status`; DOC-43 "twelve files"; DOC-44 scope-04 EV-1 counts; DOC-45 "six audits have summaries"; DOC-46 meta.json "attempts"; DOC-47 "no Python writer of return-contract.yaml"; DOC-48 `__init__.py` lines; DOC-49 D14 grep claim; DOC-50 "zero is suspect" docstring | synth-02 | REPRESENTED (ten rows) | l.702-711 |
| S02-DOC51..60 | DOC-51 severity-routing.md claims; DOC-52 step 5 single-source; DOC-53 `--candidate` vs `--doc`; DOC-54 census units; DOC-55 judge "blind"; DOC-56 "duplicates not observed"; DOC-57 "sonnet alone most catches per token"; DOC-58 combo A differs only in orchestrator; DOC-59 MR:142 escalation counts; DOC-60 tmp-scripts README / "never pushed" | synth-02 | REPRESENTED (ten rows) | l.712-721 |
| S02-DOC61..70 | DOC-61 superseded E2 claims (alias GT3, DECISION UPDATE, 161); DOC-62 C5 scope; DOC-63 executor-disjoint claim (C8); DOC-64 REPORT.md / matrix claim (C8); DOC-65 bounded `--fix` loop (C8); DOC-66 ensemble docstring `merge_method`; DOC-67 runner.py Tier-1 comment; DOC-68 "111 tests"; DOC-69 D2/D11 "NOT covered"; DOC-70 renamed live-repo test | synth-02 | REPRESENTED (ten rows) | l.722-731 |
| S02-DOC71..77 | Combined QA-note row D-71 to D-77 (panel_lint cite, branch-only after #519, null cluster_agreement, 13 vs 14 clusters.json, "installed only", "a reflect flag change", presentation notes) | synth-02 | REPRESENTED | l.732 |
| S02-41 | 4.1 contradictions 1-16 (D2/D11 coverage; panel resolve callers; 4 vs 3 flips; 195 of 1398; confidence use; twelve files; return-contract writer; calibrator rubric; shadow15; cluster_agreement; variants installed; sonnet per token; branch-only; "reflect flag change"; Critical rows vs log; parsed-sparse recount) | synth-02 | REPRESENTED (all 16; #15 and #16 revised) | l.738-753 |
| S02-42 | 4.2 coverage self-check (row count, Track tag, severity counts, D1-D16 status, BL, MS, DOC coverage, C8 rows, Track none, known-contradicted, items outside this part) | synth-02 | REPRESENTED (counts updated for MS-24) | l.759-769 |
| S02-43 | 4.3 Critical and Important rows by track | synth-02 | REPRESENTED (MS-24 added under M2) | l.775-779 |

File 5 total: 38 front-matter items + 16 D rows + 23 BL rows + 23 MS rows + 9 ENS rows + 2 OPEN rows + 71 DOC rows (listed in seven groups) + 3 section-4 tables = 185 items enumerated: 185 REPRESENTED, 0 COVERED-BY-DEDUP, 0 OMITTED. Report additions not in the synthesis (MS-24, SC-18 to SC-23, route text in SC-16) are outside this gate.

### File 6 of 8: synthesis/synth-03-external-findings.md (report Section 5)

Coverage method for this file: whitespace-normalised `diff` of the synthesis body (370 lines) against report l.782-1151 gives 1 differing line in 370 (the web-04 context line, corrected to "21 of 25 = 0.84, n=25 ... recall is not a population recall"; this is a later correction and counts as represented). Section headings 5.1.1 to 5.5.5 are identical. Each row below groups the findings of one synthesis table, with the individual findings named.

| # | Source finding group (individual findings) | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S03-01 | Reading notes and domain caveat (tags E/A/S/2/V/U, relationship values, D-codes, C-codes) | synth-03 | REPRESENTED | l.786-795 |
| S03-02 | 5.1.1 aggregation rules (5): MultiVer union voting 82.7%/85.0% FPR; calibrated weighted majority vote; Self-Agg SWR-Bench; 14 LLM validators and minority veto; over-rejection / right-for-wrong-reason | synth-03 | REPRESENTED | l.801-809 |
| S03-03 | 5.1.2 production systems (6): Cursor Bugbot; Cloudflare; LinkedIn; Zenodo 294 defects (56.8% singletons); dev.to/Augment ensembles (93.4% second-hand); Mozilla Star Chamber and Ellipsis | synth-03 | REPRESENTED | l.811-820 |
| S03-04 | 5.1.3 dedup across reviewers (2): shared production sequence; NeMo semantic dedup | synth-03 | REPRESENTED | l.822-827 |
| S03-05 | 5.1.4 conflicts and gaps (5): singleton split; reflect DEGRADE vs ledger PASS-on-one; "computed but unused" wording; no clustering error measure; no spec/tasklist panel study | synth-03 | REPRESENTED | l.829-837 |
| S03-06 | 5.1.5 options 1-8 (split candidate/blocking; no hard quorum; abstention counts; tune thresholds; typed dedup; verdict bias; outcome metric; panel size 3 + adjudicator) | synth-03 | REPRESENTED | l.839-850 |
| S03-07 | 5.2.1 interchange standards (6): SARIF level/kind; SARIF rank; GitHub code scanning; GitLab resolution order; DefectDojo/QAC/DEV mappings; property bags and native severity | synth-03 | REPRESENTED | l.856-865 |
| S03-08 | 5.2.2 tool and community scales (8): CodeQL; Semgrep; Google eng-practices; Conventional Comments; SonarQube; CodeRabbit; P0-P3 priorities; OWASP | synth-03 | REPRESENTED | l.867-878 |
| S03-09 | 5.2.3 equivalence table, strategies S1-S7, collapse analysis, six-row loss table (review-loop Medium, deviation classes, rf-qa IMPORTANT, v1 CRITICAL non-blocking, Low vs Nit, Codex P0-P3) | synth-03 | REPRESENTED | l.880-915 |
| S03-10 | 5.2.4 conflicts and gaps (4): medium-tier collapse; extreme collapse; default for unlabelled findings; unverified items | synth-03 | REPRESENTED | l.917-924 |
| S03-11 | 5.2.5 options 1-9 (five-tier core; blocking separate; medium first-class; carry native severity; consequence definitions; non-severity fields; versioned alias table; SARIF rank cut points; P0-P3 hint) | synth-03 | REPRESENTED | l.926-938 |
| S03-12 | 5.3 preface (codebase context from research/05 and 11; web-03 "0 of 689" slip not carried) | synth-03 | REPRESENTED | l.942 |
| S03-13 | 5.3.1 panels vs single judges (7): PoLL; Nine Judges (about 2 effective votes); Apollo; multi-agent debate biases; fuser; practitioner guidance; claim-level self-verification | synth-03 | REPRESENTED | l.944-954 |
| S03-14 | 5.3.2 self-preference, identity, biases (10): self-recognition; 37,448-pair reanalysis; perplexity; GPT-4 0.520 and LinkedIn claim; filename/label effect; blinding guidance; MT-Bench; CALM; rubric option-order bias; code-judge superficial features | synth-03 | REPRESENTED | l.956-969 |
| S03-15 | 5.3.3 rubric anchoring and verbalised confidence (9): 930-response rubric study; rubric-in-prompt; RULERS; evidence gap for blind grader; Xiong; Tian; ownership bias; Ferrer; ACL moderation | synth-03 | REPRESENTED | l.971-983 |
| S03-16 | 5.3.4 calibration methods (3): Platt/isotonic and why no fit is possible now; practice descriptions; evidence gap | synth-03 | REPRESENTED | l.985-991 |
| S03-17 | 5.3.5 conflicts and gaps (6): panel vs best single judge; single adjudicator vs panel; verbalised confidence; rubric as anchor; self-preference size; unverified/excluded | synth-03 | REPRESENTED | l.993-1002 |
| S03-18 | 5.3.6 options 1-8 (optional calibrator; fresh context and different vendor; merge step as fuser; judge-quality measurement; audit sample; re-derive thresholds; offline judge vendor; validate on own data) | synth-03 | REPRESENTED | l.1004-1015 |
| S03-19 | 5.4.1 fingerprint design (11): SARIF identity; GitHub matching; empty-hash order matching; PR in-diff; CodeQL line hash; SARIF locations; DefectDojo import; SonarQube tracking; Semgrep ids; GitLab SAST; Code Climate | synth-03 | REPRESENTED | l.1021-1035 |
| S03-20 | 5.4.2 cross-reviewer dedup and PR locations (6): DefectDojo cross-tool; merging SARIF; DefectDojo location tracking; GitHub review comments (outdated vs re-anchor); LinkedIn/Cloudflare; practitioner dedup rules | synth-03 | REPRESENTED | l.1037-1046 |
| S03-21 | 5.4.3 transitive-chaining safeguards (3): single vs complete linkage; entity-resolution black hole threshold; VL-Dedup size cap | synth-03 | REPRESENTED | l.1048-1054 |
| S03-22 | 5.4.4 conflicts and gaps (hash vs scope; location vs root cause; no category gate in our key; no LLM-reviewer clustering algorithm) | synth-03 | REPRESENTED | l.1056-1063 |
| S03-23 | 5.4.5 options R1-R10 | synth-03 | REPRESENTED | l.1065-1078 |
| S03-24 | 5.5.1 thirteen key takeaways with strength and caveat | synth-03 | REPRESENTED | l.1084-1100 |
| S03-25 | 5.5.2 eight cross-file contradictions and tensions | synth-03 | REPRESENTED | l.1102-1113 |
| S03-26 | 5.5.3 nine findings excluded or down-weighted with rationale | synth-03 | REPRESENTED | l.1115-1127 |
| S03-27 | 5.5.4 six evidence gaps bounding every option | synth-03 | REPRESENTED | l.1129-1138 |
| S03-28 | 5.5.5 seven consolidated external-research options | synth-03 | REPRESENTED | l.1140-1150 |

File 6 total: 28 finding groups enumerated, containing 190 individually named findings, options, strategies and takeaways (26 in 5.1, 42 in 5.2, 43 in 5.3, 34 in 5.4, 43 in 5.5, plus the two preface blocks): all REPRESENTED (one context line corrected to narrower wording), 0 COVERED-BY-DEDUP, 0 OMITTED.

### File 7 of 8: research/scope/01-other-branch-study.md

Coverage method for scope slices: an item is REPRESENTED when it has a row in the Section 8.1 value inventory (report l.2937-3630) with a destination or a DROP reason, or appears elsewhere in substance. The inventory cites this slice as `scope/01:<line>`.

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S01-01 | 1.1 reports/setup: HANDOFF copy (315 lines), `manifest.md`, `PILOT-REPORT.md`, `COMBO-REPORT.md` (only l.289+ current), `combos/SPEC.md`, RAW-TRANSCRIPTS note | scope/01 §1.1 | REPRESENTED | V-008 to V-011, V-017 (l.2946-2955), l.2937 abbreviations |
| S01-02 | 1.2 per-package inputs: 3 packages (candidate, ground-truth, draft, resolution-default/live7), reviews/quarantine dirs; `source.md` is NOT in the eval tree | scope/01 §1.2 | REPRESENTED | V-018, V-019, V-025 (l.2956-2957, l.2963) |
| S01-03 | 1.3 merge and scoring outputs (arms/, combos/, scoring/, label-key) | scope/01 §1.3 | REPRESENTED | V-018 (l.2956) |
| S01-04 | 1.4 `tools/run-reviewer.sh` (87 lines) | scope/01 §1.4 | REPRESENTED | V-020 (l.2958), V-183 |
| S01-05 | 1.4 older runner copies `run-reviewer.sh.bad-launch`, `.unpassable-ac` (34 lines each) | scope/01 §1.4 | OMITTED (MINOR) | OM-10 |
| S01-06 | 1.4 `tools/tmp-scripts/` (54 scripts + README): judge-one, anon-*, arm-merges, merge-b6, gen-judge-list, b4-job-one, startcombo, per-row runners, snap.py, drift-b3.py, brief_c1.py, stats.sh | scope/01 §1.4 | REPRESENTED | V-021 to V-024 (l.2959-2962) |
| S01-07 | 1.4 `analysis/merge-b7..b11.sh`, `b7..b11-launch.sh`, `b11-rerun-one.sh`, judge lists `b*-judge.tsv`, fix lists | scope/01 §1.4 | OMITTED (MINOR) | OM-10 |
| S01-08 | 1.5 analysis scripts: final-table.py, three-way.py, doubles.py, untried.py, attrib.py, b8/b9-table.py, allsets/, issue-table/ | scope/01 §1.5 | REPRESENTED | V-013 to V-016 (l.2951-2954) |
| S01-09 | 1.5 rendered tables and estimates (`final-table.md`, `b8-final.md`, `b9-final.md`, `combo-est-{A,B,self}.md`) | scope/01 §1.5 | OMITTED (MINOR) | OM-10 (derived outputs of V-014) |
| S01-10 | 1.5 audits A-F and the "only A and D have summaries" note | scope/01 §1.5 | REPRESENTED | V-012 (l.2950), V-170 (l.3108), DOC-45 |
| S01-11 | H1-H3, H5-H13, H16, H17, H19, H20, H22-H28, H31-H36 confirmed (CR section starts; 106 runs/62 sets; 71 valid-era rows; ember + 2x luna default; sonnet + 2x luna; haiku + 2x luna; update rejected; three surviving statistics; p-range nuance; pilot arms; pre-registered rule; Qwen timeout; per-model counts; 156/665; source first shipped; audit E; audit A; fresh session; brief lines; judge; ladder fix; concurrency; tmp-scripts count; aliases; sandbox; quarantine; terra/sol; luna 91.4%; 65 vs 38) | scope/01 §2.1 | REPRESENTED | V-165 (l.3103) with V-029 to V-039, V-054 to V-059, V-181, V-184-V-193; l.196-200 |
| S01-12 | H4 correction: the once-found issue is alias GT1 (B6), not GT3 | scope/01 §2.1 | REPRESENTED | V-166 (l.3104), V-031 (l.2969), DOC-61 (l.722) |
| S01-13 | H14 correction: per-model drop counts are all dropped findings (sum 92); 49 is the blocking count | scope/01 §2.1 | REPRESENTED | V-167 (l.3105), V-037 (l.2975), l.1304 |
| S01-14 | H15 correction: audit D names 3 flips (plus 5 total-loss merges), not 4 | scope/01 §2.1 | REPRESENTED | V-168 (l.3106), DOC-11 (l.672), contradiction 3 (l.740) |
| S01-15 | H18 correction: brief never names `source.md` but every candidate does (`candidate.md:3,14`) | scope/01 §2.1 | REPRESENTED | V-169 (l.3107), DOC-37 (l.698), l.1846 |
| S01-16 | H21 correction: only audits A and D have `summary.md` | scope/01 §2.1 | REPRESENTED | V-170 (l.3108), DOC-45, l.185 |
| S01-17 | H29, H30, H37, H38: `checks-gate8` not copied; raw-file counts by scope; `manifest.md` "never pushed" stale; D1-D16 not re-read in slice 01 | scope/01 §2.1 | REPRESENTED (DROP with reason) | V-171 (l.3109), V-024, DOC-60 (l.721) |
| S01-18 | 2.2 fact: identity check accepts `-build`, rejects `<synthetic>` | scope/01 §2.2 | REPRESENTED | V-172 (l.3110) |
| S01-19 | 2.2 fact: fallback overwrites `expected_model` in meta.json | scope/01 §2.2 | REPRESENTED | V-173 (l.3111), l.207 |
| S01-20 | 2.2 fact: 57 auxiliary `claude-gw-tier2[1m]` calls counted in `output_tokens_all` | scope/01 §2.2 | REPRESENTED | V-174 (l.3112), V-054 |
| S01-21 | 2.2 fact: stale attempt files make "highest attemptN" wrong for 5 runs | scope/01 §2.2 | REPRESENTED | V-175 (l.3113) |
| S01-22 | 2.2 fact: anchor resolution failures kept (46 null-span rows, 13 blocking) | scope/01 §2.2 | REPRESENTED | V-176 (l.3114), D5 (l.592) |
| S01-23 | 2.2 fact: blocking/verdict logic consistent (0 violations over 264 merges) | scope/01 §2.2 | REPRESENTED | V-177 (l.3115), l.1996 |
| S01-24 | 2.2 fact: 45 merges lack `merge-stdout.txt` | scope/01 §2.2 | REPRESENTED (DROP with reason) | V-178 (l.3116), l.1657 |
| S01-25 | 2.2 fact: ground-truth format (package, items, dropped, verification; classes; cost values) | scope/01 §2.2 | REPRESENTED | V-179 (l.3117), l.186 |
| S01-26 | 2.2 fact: resolution files reuse `review-panel-resolution/1`; combo rows filter `resolution-live7.json` | scope/01 §2.2 | REPRESENTED | V-180 (l.3118), l.186 |
| S01-27 | 2.2 fact: concurrency limits used | scope/01 §2.2 | REPRESENTED | V-181 (l.3119) |
| S01-28 | 2.2 fact: stop rule "do not silently drop a base reviewer" | scope/01 §2.2 | REPRESENTED | V-181 (l.3119) |
| S01-29 | 2.2 fact: pilot judge cost 1,034,575 output tokens | scope/01 §2.2 | REPRESENTED | V-182 (l.3120), l.2486 |
| S01-30 | §3 reusable pieces (11): runner; identity check; fallback ladder; findings-block gate; blind judge; ground-truth format; six audits; replicates + permutation tests; agents + script cross-check; quarantine/cancel files; sandbox snapshot | scope/01 §3 | REPRESENTED | V-183 to V-193 (l.3121-3131) |
| S01-31 | §4 overlaps (10): finding format; invalid-block handling; blocking rule; calibration; tiers; identity; recording; clustering; driving document; re-review | scope/01 §4 | REPRESENTED | V-194 to V-203 (l.3132-3141), overlap matrix l.441-475 |
| S01-32 | §5 Phase 2 assignments P2-1 to P2-9 | scope/01 §5 | REPRESENTED (DROP with reason: answered by research 01-12) | V-204 (l.3142) |
| S01-33 | §6 gaps and questions 1-13 (audit summaries; wrong once-found issue; 3 vs 4 flips; `source.md` outside tree; `/tmp` paths and unlisted script; expected_model overwrite; reviewer Bash write access; judge without source; D1-D16 not re-read; reflect facts rest on SKILL.md:338-349; review cluster union-find; strict-distinct vs 2x same model; time-bound valid era) | scope/01 §6 | REPRESENTED | V-205 to V-208 (l.3143-3146), V-206 |
| S01-34 | Summary corrections (a) only A and D have summaries, (b) once-found = alias GT1, (c) 3 flips, (d) per-model counts are all dropped, (e) candidates do name `./source.md` | scope/01 Summary | REPRESENTED | V-170, V-166, V-168, V-167, V-169 |

File 7 total: 34 rows enumerating 108 individual items (the section 1 file inventory in 10 groups; H1-H38 individually mapped in S01-11 to S01-17; 12 additional-fact bullets; 11 reusable pieces; 10 overlap topics; 9 assignments; 13 gaps; 5 summary corrections): 105 REPRESENTED, 0 COVERED-BY-DEDUP, 3 OMITTED at MINOR (S01-05, S01-07, S01-09; all derived or superseded harness artifacts, collected in OM-10). The five corrections to the hand-off (S01-12 to S01-16) are all represented.

### File 8 of 8: research/scope/02-review-cli-code.md

Same rule as file 7: a slice item counts as represented when it has an inventory row with a destination or DROP reason, or appears elsewhere in substance. The inventory cites this slice as `scope/02:<line>`. The five-part check of the 651-test breakdown is in S02S-24.

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S02S-01 | Method and origin keys: package on this branch equals d2d8a2d16 (`git log d2d8a2d16..HEAD` empty); #346 vs reflect first-add commits; local master ref stale | scope/02 header | REPRESENTED | l.132, l.241, l.280, MS-22 (l.648), V-360 (l.3298) |
| S02S-02 | Module inventory (16 modules): `__init__`, `findings`, `ledger`, `merge_cmd`, `ledger_cmd`, `panel`, `panel_cmd`, `telemetry`, `telemetry_cmd`, `findings_v2`, `card_convert`, `cluster`, `cluster_cmd`, `verify_cmd`, `manifest`, `manifest_cmd` with line counts, origin, public functions, importers | scope/02 §1 | REPRESENTED | V-001 to V-004 (l.2939-2942), V-209 to V-214 (l.3147-3152), l.250-251, l.280 |
| S02S-03 | Packaged data (9 files): default, live7, six `reflect-*` templates, tier file with `classes` map | scope/02 §1 | REPRESENTED | V-005 (l.2943), V-215, V-216 (l.3153-3154) |
| S02S-04 | Skill callers by grep: reflect SKILL.md:345/:347 are the only in-`src` callers of the package; no skill calls `review merge`/`ledger` | scope/02 §1 | REPRESENTED (with correction: one prose caller exists) | D14 (l.601), contradiction 2 (l.739), DOC-27 (l.688), l.499 |
| S02S-05 | Observations: two parallel stacks on one CLI group; v2 imports private v1 names; no v2 ledger, verdict or merged report | scope/02 §1 | REPRESENTED | l.280, l.290, V-221 (l.3159), V-234 (l.3172) |
| S02S-06 | Contract table aspects (container; multiple blocks; truncated block; result shape; bad line; empty block; prior lines) | scope/02 §2 | REPRESENTED | V-217, V-218, V-219 (l.3155-3157) |
| S02S-07 | Contract table aspects (id; severity; blocking incl. label rule; category and `reflect_category`; claim 300; anchor 12-200; anchor2; refs 8) | scope/02 §2 | REPRESENTED | V-220, V-221 (l.3158-3159), l.346 |
| S02S-08 | Contract table aspects (citations 1-8 and roles; lens; deviation_class; coverage_rows; self_confidence; calibrated_confidence forbidden; channel; roles/lenses; location model) | scope/02 §2 | REPRESENTED | V-222, V-223 (l.3160-3161), V-293 (l.3231) |
| S02S-09 | Answers: v2 imports v1 limits as duplicated literals; docstring compatibility claim not true for prior lines and empty block; card_convert truncates (297 + `...`) instead of rejecting | scope/02 §2 | REPRESENTED | V-221, V-224 (l.3162), DOC-01, DOC-02 (l.662-663), V-211 |
| S02S-10 | Clustering table (12 aspects: input, invalid blocks, location unit, fingerprint, same-defect rule, refs extraction, grouping, chaining, representative, blocking, confidence, output effect) | scope/02 §3 | REPRESENTED | V-225 to V-228 (l.3163-3166), overlap matrix l.346-352 |
| S02S-11 | Four "differences that matter" (over-merge by fingerprint differs in kind; chaining in both; shared id regex; anchor-only findings are singletons in `cluster_v2`) | scope/02 §3 | REPRESENTED | V-227, V-229 (l.3165, l.3167), D6 (l.593), D7 (l.594), MS-02 (l.628) |
| S02S-12 | Templates table (8 templates: slots, reviewer counts, descriptions; personas not in the template; re-review resolves only the fixed slot) | scope/02 §4.1 | REPRESENTED | V-005, V-215 (l.3153), BL-08 (l.611), l.2790 |
| S02S-13 | Tier file: aliases tier1a-tier4, names, classes, environments (gateway empty launch, anthropic-only stand-ins and launch), no `tier0` alias; `find_path` order | scope/02 §4.2 | REPRESENTED | V-216 (l.3154), DOC-26 (l.687), MS-06 (l.632) |
| S02S-14 | Environment selection: `--env`, `$SUPERCLAUDE_REVIEW_ENV`, `$T3Model01`; `T2bModel01` never read | scope/02 §4.3 | REPRESENTED | V-230 (l.3168), D12 (l.599), V-076 |
| S02S-15 | Distinctness and exclusion: seeds and strategies (date-ordinal default), soft re-admission, `hard_exclude`, `strict_distinct`, `skipped_slots`, resolution record fields | scope/02 §4.4 | REPRESENTED | V-231, V-232 (l.3169-3170), V-124 (l.3062), D11 (l.598) |
| S02S-16 | Reflect profile rules (no tier0/Fable, classes required, max 3 reviewers, launch values) and `RESOLUTION_SCHEMA` unverified | scope/02 §4.5 | REPRESENTED | V-233 (l.3171), V-124 |
| S02S-17 | D1 re-checked at current code (+ reflect shares it for native v2 output) | scope/02 §5 | REPRESENTED | D1 (l.588), V-065 (l.3003) |
| S02S-18 | D2 (+ not shared) | scope/02 §5 | REPRESENTED | D2 (l.589), V-066 |
| S02S-19 | D3 | scope/02 §5 | REPRESENTED | D3 (l.590), V-067 |
| S02S-20 | D4 (+ partly shared: `support`/`disputed` unused) | scope/02 §5 | REPRESENTED | D4 (l.591), V-068 |
| S02S-21 | D5, D6, D7, D8 (spot-check), D9 (partly confirmed), D10 | scope/02 §5 | REPRESENTED | D5-D10 (l.592-597), V-069 to V-074 (l.3007-3012) |
| S02S-22 | D11 (lines moved; reflect added opt-in fix), D12 (lines moved), D13 (reflect appended three names), D14 (stronger: no in-repo caller), D15, D16 | scope/02 §5 | REPRESENTED | D11-D16 (l.598-603), V-075 to V-080 (l.3013-3018) |
| S02S-23 | Summary for the reflect side: inherits D1, D6, D7, D11, D12, D13; avoids D2-D4, D16 only because no ledger | scope/02 §5 | REPRESENTED | V-234 (l.3172), l.346 |
| S02S-24 | Tests inventory: 651 collected; per-file counts for 19 files (findings 23, ledger 24, cli 13, panel 41, live7 15, rules_text 5, telemetry 10, findings_v2 92, card_convert 119, cluster 113, cluster_pairs 32, cluster_cmd 15, verify_citations 8, manifest 40, panel_exclusion 32, reflect_profile 17, reflect_templates 21, consumer_inventory 14, stage0a_replay 17); totals #346 = 131 tests / 7 files, reflect = 520 tests / 12 files; fixtures | scope/02 §6 | REPRESENTED | V-007 (l.2945), V-235 to V-243 (l.3173-3181), V-247 (l.3185), V-558 (l.3496), l.254, l.473, DOC-68 (l.729) |
| S02S-25 | Covered-vs-not-covered probes: pinned D3, D5, D11, D8-adjacent test; not covered (`T2bModel01`, `lint_cmd`, `T01.02`, round 4, D2 body, v1 `unpassable-check`, dropped-id recording, v1-to-v2 equivalence, anchor-only `cluster_v2`); limit-equality coupling not pinned | scope/02 §6 | REPRESENTED (with correction: D2 and D11 are pinned) | V-244 to V-246 (l.3182-3184), V-163 (l.3101), DOC-12 (l.673), DOC-69 (l.730) |
| S02S-26 | Phase 2 assignments 1-7 | scope/02 §7 | REPRESENTED (DROP with reason: answered by research 01-12) | V-248 (l.3186) |
| S02S-27 | Gaps: `panel.py:137-400`, `cluster.py:184-487`, `ledger.py` parts, `manifest.py` bodies, spec-panel wiring unread | scope/02 §8 | REPRESENTED (DROP with reason: closed by later reads) | V-249 (l.3187) |
| S02S-28 | Gap items [CODE-CONTRADICTED]: hand-off line numbers for D11/D12/D7; `ledger.py:112` docstring; `findings_v2.py:3` claim | scope/02 §8 | REPRESENTED | DOC-21 (l.682), DOC-16 (l.677), DOC-09 (l.670), DOC-02 (l.663) |
| S02S-29 | Questions: anchor first-class or citations; truncate vs reject; soft vs strict distinctness; `tier0` planned | scope/02 §8 | REPRESENTED | V-250 (l.3188), C-01, C-02, C-04 |
| S02S-30 | Summary (two stacks; 651 tests; 16 defects confirmed; D3, D5, D11 pinned) | scope/02 Summary | REPRESENTED | l.280, l.2203-2250 area, V-244, S02 coverage self-check l.762 |

File 8 total: 30 rows enumerating 160 individual items (16 modules, 9 data files, 3 observations, 24 contract aspects and 3 answers, 12 clustering aspects plus 4 differences, 8 templates, 5 tier-file items, 1 environment rule, 5 distinctness items, 1 reflect profile, 16 defects with their reflect-sharing cells, 19 test files plus 2 totals plus 14 covered/not-covered probes, 7 assignments, 11 gaps and questions); all REPRESENTED, 0 COVERED-BY-DEDUP, 0 OMITTED. The 651-test breakdown is represented per file (S02S-24).

### Omissions Found

Search method for each entry: the distinctive tokens of the finding (numbers, identifiers, phrases) were searched in the whole report (4283 lines) and no sentence with that meaning was found; neighbouring findings that are represented are named so a reader can judge the residue. All entries are sub-facts of findings whose main substance is carried; none changes a decision, a recommendation or a constraint in the report.

| # | Source finding | Source file | Status (OMITTED / COVERED-BY-DEDUP) | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| OM-1 | Regression is evidence-sourced: `regression_present` is set only from the exit-code taxonomy (pytest exit 2/3, timeouts, flaky and unmapped exits are Grounding Gaps); a reviewer's class increments only the count; both halt and both are human-required in code (`contract.py:410-417`) | research/05 §2.1, §13.1 (05-07, 05-50) | OMITTED | n/a (the neighbouring static-analysis conflict G-05 and the `unauthorized_deviation_present` options are carried at l.640, l.2243, V-503) | MINOR |
| OM-2 | Cluster-level deviation class = highest-precedence member class (Regression > Drift > Necessary > Authorized); a null class is compatible with any class, so rows that lose their class to the two-word-label gap can cluster with Drift/Regression rows | research/05 §8.2, §13.2 (05-37, 05-54) | OMITTED | n/a (the any-member veto and the two-word-label gap are carried: V-500, DOC-08) | MINOR |
| OM-3 | Stoprule RUBRIC v1 content: B1 verbatim quote + span, B2 named-reader wrong outcome, B3 kinds (a)-(e), CRITICAL blocking under (e), the "never a reason to block" list, Q2 recorded as data; grader handling of verified vs unverified evidence | research/05 §6 (05-32) | OMITTED | n/a (carried: rubric B1-B3 exists, spec-specific, agreement is never a reason, Drift would not block: l.1454, l.1510, V-506) | MINOR |
| OM-4 | E2 per-panel wrong-blocker figures (ember + 2x luna 1.83, haiku + 2x luna 3.00, ember + haiku + terra 3.20, 2x ember + 2x luna 4.75; control package 0.00-2.00 per run, 0.83-1.75 replicated), the "ember + 2x luna 1.00 judge-blocking is 0.17 real" example, and "that panel found 1.75/14, real blocking 0.25/8" | research/05 §11 (05-44, 05-45) | OMITTED | n/a (carried: 65 vs 38, the 2.75-3.25 surviving effect with p 0.005-0.03, the 1.8-4.75 range at V-196, the upper-bound caveat) | MINOR |
| OM-5 | Open question in the rubric: no capability ordering across the six classes is published (needed to pick "highest capability" for the calibrator) | research/05 §3.1 (05-19) | OMITTED | n/a | MINOR |
| OM-6 | (a) E2 runner: a missing `source.md` falls through `|| true` silently and a stale copy could remain in the sandbox; (b) reviewer cwd differs from the candidate/source directory, so the source is reachable only relative to the candidate path; (c) `## Never` rule (a brief may narrow but not widen the command's scope) means a required source read should be stated in the core contract | research/06 §1.4, §3.1 (06-07, 06-18, 06-20) | OMITTED | n/a (carried: runner records no source field, source shipped beside the candidate but not named: V-519, V-169) | MINOR |
| OM-7 | (a) Written Stage 3 behaviour of the panel engine (D3 floor effects: `t2_floor_unmet`, forced `status: partial`); (b) contract header history: EV-1/EV-2 were added in 1.7.x with "no stable-field change", field and value additions have always been bumps; (c) `panel_lint` EV-1 does not cover the `--unattended` nested layout (L6 reports `merged-verdict: absent`); (d) the aggregator calls the lint with the run's own contract, so L7 parity never fires; (e) a contract bump silently removes bumped runs from verdict replay | research/07 §1.2, §1.6, §2.3, §6.1, §6.2 (07-03, 07-10, 07-15, 07-29, 07-30) | OMITTED | n/a (carried: both scripts bound to "1.8.0", minor bump fails the lint, major bump blocks the wrapper: l.1891-1893, l.2876) | MINOR |
| OM-8 | Audit A: check 1 found 0 mismatches over 828 resolved runs, check 4 found 0 differences, 0 `fallback.log` files; audit D: C3 split into 10 EXCLUDE and 78 WARN, ledger `doc_sha256` matched the candidate in all 264 merges | research/08 §8.1, §8.2 (08-20, 08-21) | OMITTED | n/a (carried: the 2 EXCLUDE runs, 59/57 extra-key runs, 80 reviewer-level EXCLUDE, 49 blocking dropped, 16 stale, drop reasons, 195/1398: V-054, V-057, l.200, l.1304) | MINOR |
| OM-9 | Manifest micro-rules: attempts only valid in an open per-reviewer stage; a new attempt after a `complete` one raises Conflict ("would add a vote"); the identical-replay check precedes the `failed` check; publish crash-window and re-publish recovery; review-telemetry `cost_per_confirmed_tp` uses `tokens_out` only; month-boundary file reuse | research/08 §1.3-1.5, §3.3 (08-03, 08-04, 08-05, 08-09) | OMITTED | n/a (carried: hash-only attempt payloads, resume, no retry after `failed`, publish commit point: V-531, MS-04) | MINOR |
| OM-10 | Scope slice 01 §1.4-1.5 derived artifacts: older runner copies (`run-reviewer.sh.bad-launch`, `.unpassable-ac`), batch merge and launch scripts `merge-b7..b11.sh`, `b*-launch.sh`, judge lists, rendered tables (`final-table.md`, `b8-final.md`, `b9-final.md`, `combo-est-*.md`) | research/scope/01 §1.4, §1.5 (S01-05, S01-07, S01-09) | OMITTED | n/a (the generating scripts and findings are represented: V-014, V-020, V-022, V-023) | MINOR |
| DD-1 | Per-dimension fit table, calibrator 6 vs reflect 5 dimensions | research/05 §4.2 (05-24) | COVERED-BY-DEDUP | DOC-28 (l.689) and MS-16 (l.642) state the mismatch; the per-dimension fit is the source's own reading | not an omission |
| DD-2 | Gap "findings-v1 parse path of `review merge` not re-read" | research/05 Gaps (05-60) | COVERED-BY-DEDUP | D1 (l.588) and D4 (l.591), CODE-VERIFIED by later files | not an omission |
| DD-3 | REVISE brief lacks the source | research/06 §1.3 (06-05) | COVERED-BY-DEDUP | D8 (l.595) and C-10 `{{SOURCE}}` as a core placeholder for every brief kind (l.1855) | not an omission |
| DD-4 | Safety-constraint prose as backstop to the mechanical allowlist | research/06 §4.1 (06-27) | COVERED-BY-DEDUP | C-18 / l.2768 (allowlist is the mechanism) | not an omission |
| DD-5 | E2 needed Bash only because it drove a slash command inside `claude -p` | research/06 §4.2 (06-33) | COVERED-BY-DEDUP | C-18 Option A (l.2331) | not an omission |

Items that later gates deliberately removed or corrected count as represented (executor note 3): the older "driven by the parsed-sparse flag" claim is replaced by the recount (V-518, DOC-59, contradiction 16, l.753); "cluster_agreement 1.0 in 10 of 11" is deliberately not used (l.1531); web-04's "precision 0.84 and recall 0.95" is narrowed to "21 of 25" (l.1019, SC-6 at l.530); hand-off claims marked [CODE-CONTRADICTED] (D2/D11 "not covered", "4 flips", "no skill calls panel resolve", variants "experiment copies only", alias GT3) are stated with the correction in DOC rows and contradictions 1-4, 11.

### Summary

- Files enumerated: 8 of 8 (4 research files, 2 synthesis files, 2 scope slices), 823 findings in total: research/05 62, research/06 43, research/07 45, research/08 30 groups, synth-02 185, synth-03 190 (28 groups), scope/01 108, scope/02 160.
- REPRESENTED (including rows with a MINOR residue): 806. COVERED-BY-DEDUP: 5 (DD-1 to DD-5). OMITTED rows: 12, all MINOR, grouped in OM-1 to OM-10 together with 13 MINOR residues inside rows that are otherwise represented.
- By severity: CRITICAL 0, IMPORTANT 0, MINOR 10 grouped entries (25 instances).
- Hand-off checks required by the gate: the five corrections to the hand-off (H4 alias GT1, H14 per-model drops are all findings, H15 three flips, H18 candidates name `./source.md`, H21 only audits A and D have summaries) are all represented (S01-12 to S01-16, V-166 to V-170); the 651-test breakdown (131 in 7 #346 files + 520 in 12 reflect files, and the per-file counts) is represented (S02S-24, V-007, V-235 to V-243, V-558, l.254, l.473); each of D1-D16 is represented separately (S02-D1 to S02-D16, S02S-17 to S02S-22, V-065 to V-080); E2 facts are cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only.
- Closing note on the method: the synthesis inputs were checked line by line by diff because the report is their direct descendant (Section 5 is identical to synth-03 except one corrected line; Sections 3 and 4 differ from synth-02 only by in-place revisions). The research files and scope slices were checked by meaning against the Section 8.1 inventory (691 rows, V-001 to V-691) and the body sections; the residue found there is small-grained, which is expected given that the inventory walks every takeaway and gap of the four research files.

Verdict: PASS (0 omitted at CRITICAL or IMPORTANT)


