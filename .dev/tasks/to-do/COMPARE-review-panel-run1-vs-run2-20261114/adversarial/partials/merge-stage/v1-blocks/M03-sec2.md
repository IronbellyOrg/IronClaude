<!-- Source: Variant 1, Section 2 (lines 108-129, 131-238, 279-435) — merged per Change #M-03; ids prefixed R1- -->
### 2.10 Run 1 current-state material

Run 2 Sections 2.1-2.9 govern where they differ; corrections applied inside the block are listed in Appendix E. This block carries run 1's Section 2 citation key and its subsections 2.1, 2.2, 2.4 and 2.5 (V1:108-129, 131-238, 279-435); run 1's 2.3 (E3) and 2.6 (overlap matrix) are not carried because run 2's 2.4 and 2.9 supersede them. Run 1's matrix stance was that no component is implemented identically by two efforts (V1:461); run 2's 16-row matrix classifies 11 rows conflicting and 1 identical (Ids) (V2:1102). <!-- Source: new (lead per Change #M-03) -->

**Citation key (used in every Evidence line).**

| Tag | Meaning |
|---|---|
| `R01` to `R13` | `research/NN-*.md` (01 finding-contract, 02 ledger-merge-verdict, 03 clustering, 04 panel-resolution-identity, 05 blocking-calibration, 06 input-contract-briefs, 07 reflect-merge-contract, 08 run-recording-telemetry, 09 consumer-plugpoints, 10 future-consumers, 11 evaluation-evidence, 12 test-pins-regression, 13 gap-fill-reflect-ensemble) |
| `S00` to `S05` | `research/scope/0N-*.md` (00 hand-off copy, 01 other-branch study, 02 review CLI code, 03 reflect side, 04 this-session artifacts, 05 master loop and consumers) |
| `GQ` | `gaps-and-questions.md` (rows `G-nn`, `D-nn`, closed items `C-nn`, owner items `O-n`) |
| `BR` | `BUILD-REQUEST.md` |
| `CR` | E2 `COMBO-REPORT.md` at the E2 commit, under the E2 root `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/`; `CR:<n>` is a line of that file |
| `PR` | E2 `PILOT-REPORT.md` at the E2 commit, same root; `PR:<n>` is a line of that file |
| `AD` | E2 `analysis/audits/audit-D/` at the E2 commit, same root (`AD/summary.md`, `AD/flags.tsv`, `audit2.json`) |
| `HO` | the other session's hand-off `HANDOFF-review-panel-unification.md` at the E2 commit (copy: `research/scope/00-handoff-copy.md`); `HO:<n>` is a line of the hand-off, `HO 3` a section |
| `MR` | the E1 requirements document `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`; `MR:<n>` is a line of that file |
| `§n` after a tag | the numbered section of that research file |
| Code paths in backticks | the code location as read and cited by the research file (path:line) |
| `git show 4a22d742:<path>` | E2 evidence at E2 commit 4a22d74213f93837d00c2c314075dd967b9a98e3 (the only E2 commit used in this file). `<path>` is under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` unless written in full |

**Effort tags.** [E1] = reflect Tier 2 panel kernel, shadow mode and model-combination experiment on `ironbelly/shadow-runs`. [E2] = tasklist review-panel evaluation study at the E2 commit above. [E3] = #346 review loop on master (findings-v1, ledger, review merge/ledger/panel/telemetry CLI, spec-panel Review Loop) plus the installed-only experiment variants. [ext] = a consumer outside all three efforts (pr_submit, Auggie, rf-qa). Where a research file marks code as master baseline but the task scheme tags it [E1], both are shown.

**Verification tags.** [CODE-VERIFIED] = the research file read the code and the claim holds. [CODE-CONTRADICTED] = the code disagrees with a document or earlier claim; the corrected statement is given. [UNVERIFIED] = not confirmed by a code read; it appears only as an open item and never as architecture. Model-behaviour evidence is dated: all runs cited were made between 2026-11-11 and 2026-11-13 on one gateway, and model routing can change (R1-R04 §7, GQ R1-G-33).

Every statement below traces to a code read recorded in a research file. Statements that rest only on a document (requirements documents, hand-off text, SKILL.md prose with no code confirmation) are marked as doc-sourced and are not used in the architecture description.

In this merged copy, these ids carry the prefix `R1-` (Merge Notes, id rule). <!-- Source: new (legend line, rule 3) -->

#### R1 2.1 E1: reflect Tier 2 panel kernel and shadow mode

**What E1 is.** The reflect Tier 2 panel kernel is a set of dormant, telemetry-only review tools plus a ten-step shadow recipe in the reflect skill. The kernel code is already on `origin/master` (commit d2d8a2d16, #519, Stage 0-2 of the Tier 2 review panel); the branch `ironbelly/shadow-runs` is three commits ahead (9874d63fb, c2e3347d3, 792cf8c52) at the time of run 1; HEAD `ad8f57560` is now 5 commits past merge-base `d2d8a2d16`, and the two skill-fix commits touch only four files: `SKILL.md` (inside §4.3a shadow steps 2, 4, 7, 10 and the §9.2 `findings_block_compliance_rate` comment), `refs/reviewer-spec.md` (the shadow instruction line :39) and two tests (R1-S03 baseline note and §1.1 [CODE-VERIFIED via `git diff`]; R1-S02 header). The kernel is therefore master code that E1 authored, not branch-only code. <!-- Variant 1 (modified) — M-25: stale 'three commits ahead' -->

**Key files and functions.**

| Component | File (lines) | What it does | Evidence |
|---|---|---|---|
| findings-v2 contract | `src/superclaude/cli/review/findings_v2.py` (304): `check_finding` :84-187, `parse_block` :215-304 | v1 container plus `citations` (1-8 role-tagged path+line ranges), `lens` (`spec`, `reflect-pre`, `reflect-post`), `channel` (`defect`, `grounding-gap`, `advisory`), `deviation_class`, `reflect_category`, `coverage_rows`, `self_confidence`; `calibrated_confidence` forbidden in a reviewer line (:96-97); block `state` complete/truncated/invalid | R1-R01 §2 [CODE-VERIFIED] |
| Legacy card converter | `cli/review/card_convert.py` (517) | maps four recorded card shapes (`yaml-blocking-minor`, `yaml-other-severity`, `markdown-table`, `unlisted`) to findings-v2; truncates claims to 297 chars plus `...` silently (:199-201, no counter) | R1-R01 §3 [CODE-VERIFIED]; the premise "truncate with a counter as card_convert already does" is [CODE-CONTRADICTED] |
| Clustering | `cli/review/cluster.py` (487): `annotate` :126, `same_defect_v2` :161, `cluster_v2` :381, `clusters_kept` :447; `cluster_cmd.py` (197) | citation-based union-find clustering, `chained` flag, calibrated `support`, `disputed`, `cluster_agreement`; telemetry only, never routes or drops | R1-R03 §2-3, R1-S02 §3 [CODE-VERIFIED] |
| Citation pre-check | `cli/review/verify_cmd.py` (184) | `superclaude review verify-citations`: flags citations to re-read, drops nothing; flags out-of-range lines (`verify_cmd.py:66-67`) | R1-S02 §1; GQ R1-CLS-02 |
| Run manifest | `cli/review/manifest.py` (534), `manifest_cmd.py` (240) | schema `review-panel-manifest/1`, nine ordered stages plus `failed`, hash chain, idempotent replay, resume, publish commit point; attempt payloads stored as hash only | R1-R08 §1 [CODE-VERIFIED] |
| Panel resolver extensions | `cli/review/panel.py` (707): `hard_exclude`, `strict_distinct`, reflect profile `validate_reflect_profile` :80-134; six `review-panel.reflect-*.json` templates; tier file `classes` map | opt-in no-readmission distinctness, class exclusion, at most 3 reviewers, no Fable, no tier0 in a reflect template | R1-R04 §1-2, §4 [CODE-VERIFIED] |
| Contract lint | `cli/reflect/panel_lint.py` (366) | lints a panel run against frozen contract 1.8.0: `STABLE_FIELDS_1_8_0` (110 keys), `TELEMETRY_FIELDS` (27), legal `merge_method` values `adversarial` and `single-reviewer-fallback`, EV-1 on-disk merge gate (:246-299) | R1-R07 §1-3, R1-S03 §1 [CODE-VERIFIED] |
| Replay and exit scripts | `scripts/reflect_cluster_pairs.py`, `reflect_consumer_inventory.py`, `reflect_stage0a_replay.py`, `reflect_verdict_replay.py`, `reflect_shadow_exit.py` (410) | Stage 0-2 measurement: pair labels, consumer census, card conversion share, verdict replay, shadow exit aggregator | R1-S03 §1 [CODE-VERIFIED] |
| Reflect protocol and agents | `skills/sc-reflect-protocol/SKILL.md` (2033), `refs/reviewer-spec.md` (116), `agents/reflect-reviewer.md`, `agents/confidence-calibrator.md`, `agents/evidence-validator.md` | protocol executed by the orchestrating model; read-only reviewer agent (tools Read, Grep, Glob, search; `permissionMode: plan`); calibrator is a troubleshoot agent (6 dimensions) reused by reflect | R1-S03 §1, R1-R05 §4 |
| Wrapper | `cli/reflect/contract.py` (420): `derive_verdict` :138-260, `_degraded_reason` :263-358, `_halted_reason` :361-382 | turns a contract into PASS, HALTED, DEGRADED or BLOCKED | R1-R05 §1, R1-R07 §1 [CODE-VERIFIED] |

**How it works: the authoritative legacy path (default, `--t2-engine legacy`).** The orchestrator composes two or three `reflect-reviewer` agents by model-class rotation and persona (analyzer, qa, refactorer or architect), writes three-section briefs, dispatches, persists cards, runs one blind `confidence-calibrator` per card (one card-level number), then merges by `sc-adversarial-protocol` Mode A (`--depth standard`, convergence score routing PASS at 0.75 or more, PARTIAL at 0.60 or more), runs the `evidence-validator` gate, and writes the 1.8.0 `return-contract.yaml` (R1-S03 §2.2; R1-R07 §1). The skill-path contract has no code writer; the orchestrator writes it (R1-R13 §4 [CODE-VERIFIED by absence], resolving R1-R08 gap 5). The wrapper degrades any Tier 2 run whose convergence score is below 0.80 or null and halts on any regression or drift count above zero (`contract.py:317-326`, `:377-381`; R1-R07 §8, R1-R05 §1).

**How it works: shadow mode (`--t2-engine shadow`, UC-1 pre only; accepted and ignored for UC-2).** Shadow runs next to the legacy steps and changes no verdict, no stable field and no `merge_method`; all panel files go under `<output>/panel/` and all fields under `telemetry:` (R1-S03 §2.3). The ten steps are: resolve and freeze (`review panel resolve --template @reflect-pre ... --strict-distinct`, then `review manifest init`), parity check, briefs plus one findings-v2 instruction line (`reviewer-spec.md:39`), normalise with a bounded re-ask, per-finding calibration line, `review cluster` plus `review verify-citations`, the legacy debate then a written `adversarial/merged-verdict.yaml`, a kept-ids cluster pass after the evidence validator, an identity check, publish (R1-S03 §2.3, SKILL.md :338-349). Shadow is a prose recipe the orchestrator follows; `cli/reflect/` holds no shadow code (R1-R07 §10; R1-S04 §0.8 doc-sourced, spot-checked by R1-R07).

**Current measurements and state (dated).**

| Item | Value | Strength | Evidence |
|---|---|---|---|
| Legacy card conversion share | 479 of 712 units = 67.28% against a 90% target (Stage 0a, 74 `pre-*` dirs, 43 with cards) | census of one repo's history; the owner redefined the gate on 2026-11-12 so recorded cards are a baseline only and the gate applies to cards written under the findings-v2 brief (not yet measured) | R1-S04 §0.3-0.4 (doc-sourced reports) |
| `cluster_v2` pair quality | 50-pair stratified sample (25 merged pairs, 25 apart pairs): precision 21 of 25 (0.84; n=25, so a wide interval); the recall figure 21 of 22 is not a population recall (the apart pairs are a small sample of a far larger apart population, `research/03` section 6.3) | AI-labelled by three same-family labelers; excludes chained and same-reviewer pairs; human labels (issues #525-#530) pending | R1-S04 §0.6; R1-R03 R1-G3; GQ R1-O-5 |
| Legacy per-finding calibration | 0 of 689 findings carry a numeric confidence | census of recorded cards | R1-R05 §5.1 |
| Shadow per-finding calibration | 142 of 142 clustered findings calibrated over 13 runs; blocking findings score higher (mean 0.80, n=16) than non-blocking (mean 0.66, n=126) | no ground truth, so not accuracy evidence | R1-R05 §5.2-5.3 |
| Stage 2 shadow exit | FAIL (exit 1), 13 of 20 runs counted; EV-1 failure rate 8 of 13 = 0.615 versus legacy 3 of 39 = 0.077; parity fails in 6 runs; lint or manifest problems in 9; 0 MALFORMED rows; 0 new degraded reasons; mean findings-block compliance 0.704 over 9 runs (mixed definitions: first-parse and after-re-ask values are averaged together) | measures non-interference, not quality; all failures are contract-writing or placement mistakes, including three contracts made unparseable by unquoted `[1m]` alias names; no run has exercised commit c2e3347d3 | R1-R07 §10 Q7; R1-R11 §8 |
| `cluster_agreement` 1.000 | mostly the no-blocking-cluster branch (`cluster.py:407-408`), not real agreement: 11 of 14 runs have zero blocking clusters, shadow02 and shadow04 are null, shadow09 = 0.9328 is the only real calibrated value | corrected by the gap review | GQ R1-CLS-05 |
| Tier 2 is the typical path | 38 of 39 non-shadow `pre-*` runs selected Tier 2; the parsed-sparse flag was set in 35 of 39 runs (34 of the 38 Tier 2 runs) and was decisive in 0 for certain, at most 1 (R1-C14 recount, `reviews/adversarial/panel-size-cost/adversarial/return-contract.yaml`); counts only, cause not established | measured census of counts; cause not established | R1-R11 §12 [CODE-VERIFIED in data] |
| T2 versus T1 recall (R1-H-A) | not measured | pilot designed, not run | R1-R11 §12; R1-S04 §0.2 |

**Identity and dispatch (dated 2026-11-12 and 2026-11-13).** The panel record pins models; it does not observe them. Spike S-ID (3 probes, 2026-11-12) found self-report matched the pin 0 of 3 times and transcript `message.model` honoured 2 of 3 pins: a `haiku` pin ran `gpt-6.1-sol` because the gateway tier2 alias has no Anthropic model first; the Agent tool result does not expose the served model, only the sidechain transcript on disk does (R1-S04 §0.7). `identity_source: observed` has no implementation (R1-R04 R1-G2 [CODE-CONTRADICTED as an implemented feature]); the `model_observed:` card line is consumed by nothing (R1-R04 R1-G3); the only served-model extraction is the offline `extract.py:42-79` of the combination study (R1-R08 §10). A missing class collapsed a whole panel to Sonnet in the combination runs (R1-R04 summary). The `gateway` environment has `launch: {}`, so every reflect template fails to resolve there, and `anthropic-only` is not anthropic-only at serving time (R1-R04 summary; GQ R1-O-2).

**The 5x3 model-combination experiment (runs 2026-11-13).** Five combinations by three repeats under `.dev/eval-workspaces/shadow-model-combos/` (`PLAN.md`, `FINDINGS.md`, `results.md`, `combos.json`, `analysis/extract.py` 193 lines). It yields leads (orchestrator speed, confidence shift, compliance) at n=3 and no quality answer: blind ground-truth scoring was not approved or run. Combo A's orchestrator was served by GLM 5.3 and Qwen3.8-max, the same models the E2 study banned, which is a likely driver of its leads; `combos.json` `status: "designed, not run"` is stale because all 15 runs exist (R1-R11 §9, §12 gaps). The untracked `runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/` folder is an orchestrator-made base-commit archive, not a reviewer escaping its snapshot, and makes run C3 protocol-different (R1-R11 §10 summary). Per-run cost and served identity exist only in `extract.py`, derived from the outer session log, never in the product record (R1-R08 §10).

**Defects and constraints found.** Contract 1.8.0 is frozen: any new `merge_method` value or new top-level key fails `panel_lint` and needs a version bump, so the shared core can own resolution, cards, clustering, citation checks, calibration coverage and manifests (all telemetry) but not the merge decision or contract writer without a bump (R1-R07 summary). EV-1 is self-attested: the verdict file it reads is written by the same orchestrator (R1-R07 gap, GQ R1-G-13). The calibrator agent implements a 6-dimension troubleshoot rubric with a gated-minimum formula and reflect passes no `rubric_path`, so the claim "re-grades per the 5-dim reflection rubric" is [CODE-CONTRADICTED] (R1-R05 §4.1). Drift halts at any severity (`contract.py:380-381`) while findings-v2 forbids MINOR blocking (`findings_v2.py:107-108`) (R1-R05 §13). `unauthorized_deviation_present` has no producer rule anywhere in the skill (R1-R05 gap, GQ R1-G-03). Pins R1-C1, R1-C6 and R1-C14 compare against `HEAD`, so they guard only uncommitted edits (R1-R07 §10 Q5, R1-R12 §6).

**Evidence:** R1-R01 §2-3; R1-R03 §2-3; R1-R04 §2, §4, §6-7; R1-R05 §1, §4-5, §13; R1-R07 §1-3, §8-10; R1-R08 §1, §9-10; R1-R11 §7-10, §12; R1-S02 §1, §3; R1-S03 §1-2; R1-S04 §0.2-0.8; GQ R1-CLS-02, R1-CLS-05, R1-G-03, R1-G-13; `src/superclaude/cli/review/{findings_v2,card_convert,cluster,cluster_cmd,verify_cmd,manifest,manifest_cmd,panel}.py`, `src/superclaude/cli/reflect/{contract,panel_lint}.py`, `scripts/reflect_shadow_exit.py` (line numbers as given in the table rows above).

#### R1 2.2 E2: tasklist review-panel evaluation study (commit 4a22d742)

**What E2 is.** An evaluation harness and a measured study, not product code. The hand-off states the branch changes no product code (`git diff origin/master...HEAD -- src tests` empty; doc-sourced, R1-S00 §0) and the inventory of the commit lists only study files under `.dev/eval-workspaces/tasklist-review-panel/` (R1-S01 §1; R1-R09 gap 12). The study scored 106 panel runs (rows; 62 distinct reviewer-model sets, including 3 pilot arms and 30 pre-source rows), of which 71 are valid-era rows (213 row-packages, 665 individual reviewer runs; "reviewer run" means one reviewer in one row and is used only for that unit below) against 3 plan packages with 16 known defects taken from real `/sc:implement` failures: `TASK-WF-designSpec-20261107-075614` (10 known, 5 blocking in implement), `TASK-WF-makeTheAliasOnly-20261105-051649` (4 known, 3 blocking) and the control `TASK-WF-design-20261108-041415` (2 known, 0 blocking) (R1-S00 §2.1; R1-R11 §4). It reviews tasklist first reviews only: one round, no reviser, no re-review (R1-S00 §2.7).

**Key files (all at `git show 4a22d742:` under the E2 root).**

| Component | File (lines) | What it does | Evidence |
|---|---|---|---|
| Single-reviewer runner | `tools/run-reviewer.sh` (87) | one fresh `claude -p --model <raw gateway id>` session per reviewer in a sandbox repo; `--permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` (:48); brief = `/sc:spec-panel @<cand> --mode critique` plus the findings-v1 rules (:13-17); per attempt observed model from top-level assistant `message.model` (:51), `MODEL_OK` rule (:55-56), `BLOCK_OK` by fence grep only (:57); two attempts then a hard-coded fallback ladder with `EXCLUDE_MODELS` and never-revisit (:23-43, :69-71); writes `<id>.md`, `meta.json`, `cost.json` | R1-R11 §1 [CODE-VERIFIED] |
| Blind judge | `tools/tmp-scripts/judge-one.sh` (31), `anon-combos.sh` (28) | anonymise reviewer ids to `R1..Rn`, one Opus judge per (row, package) given `ground-truth.json`, `candidate.md` and the merged report, writes `score.json` | R1-R11 §2 [CODE-VERIFIED] |
| Aggregation | `analysis/final-table.py` (83), `three-way.py` (63), `allsets-*.py`, `issue-*.py` | "AS SCORED" and "AUDIT-CLEAN" tables, run-level permutation tests (20,000 shuffles, seed 1, 28 uncorrected p-values), per-issue-by-panel tables | R1-R11 §3 [CODE-VERIFIED] |
| Integrity audits | `analysis/audits/audit-A..F/`; only A (`summary.md` 34 lines, `audit.py` 171) and D (`summary.md` 90 lines, `audit.py` 239, `audit2.py`) have a `summary.md` | A: intended = expected = observed model, fallback, stale attempts, cost consistency, misrouting; D: merge and ledger integrity, dropped-finding counter, report sha against ledger sha, blocking consistency, chain size | R1-R08 §8; R1-S01 §1.5 [CODE-VERIFIED] |
| Ground truth | `<pkg>/ground-truth.json`, `candidate.md`, `resolution-*.json` | per item: `id`, `class`, `plan_quote`, `description`, `evidence[]`, `cost`, `blocking_in_implement`; `verification[]` checks the quote occurs once; resolution files reuse the product resolver output schema `review-panel-resolution/1` | R1-R11 §4 [CODE-VERIFIED] |
| Helper scripts | `tools/tmp-scripts/` (54 scripts plus README, copied from `/tmp`) | job runner with cancel files, anonymisers, batch merges, launchers | R1-S01 §1.4 |
| Reports | `COMBO-REPORT.md` (506; only lines 289 onward current), `PILOT-REPORT.md` (83), `combos/SPEC.md` (152), `manifest.md` | results, decision rule, operations log (outages, contamination, quarantines) | R1-S01 §1.1, R1-S00 §1.2 |

**Reported results (doc-sourced from `COMBO-REPORT.md`; headline numbers were not re-aggregated from raw `score.json`, R1-R11 gap 7; dated 2026-11-11 to 2026-11-13, one gateway, n=4-6 per replicated panel).**

| Result | Reported value | Strength and limit | Evidence |
|---|---|---|---|
| Ceiling | every replicated panel finds about 1.6 to 2.5 of 14 known defects in the two defect-rich packages; no panel significantly better on found, real blocking, wrong blockers or control (permutation p 0.28 to 1.0); only tokens differ (p 0.002 to 0.009) | underpowered; shows model mix is not the lever at this sample size | R1-S00 §2.2 R1; R1-R11 §12 |
| Never found | 4 of 16 issues never found by any run (designSpec GT1, GT2, GT10; alias GT4); the once-found issue is alias GT1 (B6) | [CODE-CONTRADICTED] correction: the hand-off says alias GT3 | R1-S01 summary; R1-R11 stale docs |
| Default panel | ember + 2x luna (64k tokens, about 6 minutes, 1.83 of 14); optional quality tier sonnet + 2x luna (n=6, 2.33 of 14); the "sonnet + 2x luna is the standard" claim from n=1 was rejected by batch 11 | cost and reach trade-off, not a quality difference | R1-S00 §2.2 R3 |
| Surviving statistics | a second luna raises control found by +0.83 (Welch p 0.004, permutation 0.048); 2x luna + 2x ember adds 2.75 to 3.25 wrong blockers (p 0.005 to 0.03); ember + terra is worse by 1.75 found (p 0.029) | the "second run adds nothing" claim was retracted after a flawed attribution | R1-S00 §2.2 R4 |
| Blocking precision | judge-counted "blocking" 65 versus real blocking 38 over 71 rows | read at source in R1-R05 §11 (`COMBO-REPORT.md:291`) | GQ R1-CLS-09 |
| Source-blind runs | 156 of 665 valid-era reviewer runs (individual reviewers inside the 71 valid-era panel rows) never opened `source.md`; the causal link to the brief not naming it is an inference | measured count, inferred cause | R1-R06 summary; GQ R1-CLS-10 |
| Lost at merge | 80 reviewer-level cases, 49 blocking findings lost (24 anchor over 200, 14 anchor2 over 200, 10 claim over 300, 1 refs); 3 merged verdicts would have flipped to PASS | re-derived from committed audit D outputs; the hand-off and `COMBO-REPORT.md:292` say 4 flips, audit D names 3 verdict flips (the third is the merge that lost two blocking findings, F1+F2), so "4" is [CODE-CONTRADICTED] | R1-R02 §4, gap 3 [CODE-VERIFIED] <!-- Variant 1 (modified) — M-25: verdict flips wording (audit D summary) --> |
| Chaining | audit D replay: 195 chained rows among 1398 ledger rows in total, 144 spanning more than 60 lines, 83 mega-rows (8 or more members or 4 or more sections) | script `audit-D/audit2.py:139-155`; the summary wording "rows with 3 or more members" is [CODE-CONTRADICTED], 1398 is all rows | R1-R08 §8.2; R1-R03 summary |

**Model-by-role observations (dated, one gateway).** `claude-sonnet-5-5` never had findings dropped at merge (446 of 446 kept) and read `source.md` in 62 of 63 runs (`gpt-6.1-terra` and `gpt-6.1-sol` also lost none, 103 of 103 and 8 of 8 kept, and opened `source.md` in 44 of 44 and 3 of 3 runs, but their reviews are empty or incomplete; `audit-D/summary.md:18`, `COMBO-REPORT.md:373`); `gpt-6-luna` is fast and thin with the weakest anchor fidelity (91.4% verbatim, 30 findings lost at merge); `muse-ember-1.0` is cheap, with 33 findings lost (the per-model counts include all dropped findings, not only blocking ones, R1-S01 summary correction (d)); `gpt-6.1-terra` and `gpt-6.1-sol` return empty or incomplete reviews; `glm-5.3` was slow in the pilot (805-1435 s per review, `combos/SPEC.md:5`) and the owner removed it from batch 4 onward for delays (`combos/SPEC.md:98`), so no source-era glm data exists (the "adds nothing" and "800-1800 s" wording sits in `COMBO-REPORT.md` lines the file declares superseded and is not carried); `Qwen3.8-max` timed out 3 of 4 runs and was excluded by the owner yet is still listed in the packaged `tier2` (4th of 6), `tier2b` (3rd of 4) and `tier3` (2nd of 2) lists (R1-S00 §2.3; R1-R04 §8; order read from `review-tiers.default.json` at HEAD 792cf8c52; a gateway `live7` resolution can draw it into two slots, R1-D11). <!-- Variant 1 (modified) — M-25: Qwen3.8-max '3 of 3 slots' corrected to '3 of 4 runs' -->

**Strategies that worked and failed (doc-sourced lessons).** Worked: blind scoring with an independent re-judge of 12 rows (12 of 12 agreement); ground truth from real implement failures with a `blocking_in_implement` flag; six read-only integrity audits after the data was in; replicates before any claim; an observed-model check on every run with quarantine instead of deletion; `NOFALLBACK=1` for evaluation runs; counting by agents and by a direct script (R1-S00 §3). Failed: single-run claims, per-reviewer attribution of merged rows, treating judge-blocking as real blocking, many concurrent gateway workers (model-identity bleed), a cyclic fallback ladder that hid wrong-model runs, not shipping `source.md` from the start (R1-S00 §3).

**Defects in the E2 harness itself (code-verified in R1-R11, R1-R08).** `expected_model` is overwritten on fallback (`run-reviewer.sh:58` with `:76`) and `final-table.py:44` groups panels by it; the cost glob also sums stale attempt files (`run-reviewer.sh:87`); `BLOCK_OK` greps the fence only, so invalid lines are invisible to the runner (:57); Bash is not denied under `bypassPermissions` (:48); the judge is blind to reviewer ids but not to panel name (`judge-one.sh:21`); a judge that exits 0 without `score.json` is silently dropped (`final-table.py:48`); the audit filter silently disappears when `/tmp/audit-*/flags.tsv` is missing (`final-table.py:24`); `three-way.py:4` executes a `/tmp` copy of `final-table.py`; audits A and D read attempt transcripts that are not committed (1.48 GB left out by owner order) and hard-code another worktree's paths, so they cannot be re-run from the commit (R1-R11 §1-3; R1-R08 §8, §12). The study bypassed `superclaude review panel resolve` (raw model ids, bash ladder), while its own `resolution-*.json` inputs show Qwen3.8-max and glm-5.3 twice in one `@live7` panel, so the hand-off claim that R1-D11 was "not observed in the eval" is [CODE-CONTRADICTED] in data (R1-R11 §4, R1-R04 summary).

**Product-code defects E2 reported.** R1-D1 to R1-D16 against the shared review package are summarised with their current-code status in section 2.4 (R1-S02 §5, R1-S00 §2.4). All 16 hand-off defects that touch the package were confirmed at current code, with line numbers for R1-D7, R1-D11 and R1-D12 moved (R1-D11 now `panel.py:536-543`, R1-D12 `panel.py:485-494`, R1-D7 `telemetry.py:23` and `findings.py:29`) (R1-S02 §5, R1-R04 §10 stale docs, R1-R03 stale docs).

**Today's data flow of the E2 harness (reviewer output to scored result; it runs stack A of section 2.4 unchanged).**

```
 candidate.md + source.md (copied beside it) -> sandbox repo outside the eval tree
        |
        v
 run-reviewer.sh   fresh `claude -p --model <raw id>`; Edit/Write/NotebookEdit denied, Bash not
        |   brief = /sc:spec-panel @cand --mode critique + findings-v1 rules (no source named)
        |   per attempt: observed model from transcript, MODEL_OK, BLOCK_OK = fence grep only
        |   2 attempts, then bash fallback ladder (EXCLUDE_MODELS, never revisit)
        v
 <id>.md + meta.json + cost.json     (expected_model overwritten on fallback)
        |
        v
 superclaude review merge  [E3 product code, unchanged]  -> ledger.json + merged-1.md
        |      (length-limit drops happen here, D1; round 1 only)
        v
 anonymise (R1..Rn, opaque label) -> blind Opus judge (ground-truth.json + candidate.md)
        |      -> score.json: gt_covered_any, gt_covered_blocking, wrong_blockers
        v
 analysis/final-table.py + three-way.py (permutation tests); audits A..F read the records afterwards
```
(R1-R11 §1-3; R1-R08 §7-8; R1-S00 §2.1 [CODE-VERIFIED for the scripts; results are doc-sourced].)

**Open E2 decisions.** Seven owner decisions remain open in the hand-off (fix R1-D1, fix R1-D8, default model set, tasklist review inside `/sc:workflow` or a separate command, one reviewer's `blocking` flag versus quorum or calibration, raw transcripts, re-run after R1-D1 and R1-D8) (R1-S00 §4.2).

**Evidence:** `git show 4a22d742:` paths under the E2 root: `tools/run-reviewer.sh:13-17, :23-43, :44-60, :69-71, :75-76, :85, :87`; `tools/tmp-scripts/judge-one.sh:6-23, :21, :25-31`; `analysis/final-table.py:11-13, :24, :34, :44, :48, :80-82`; `analysis/three-way.py:4, :33-44`; `analysis/audits/audit-A/audit.py:2, :33, :42-164`; `analysis/audits/audit-D/audit.py:17-219`; `analysis/audits/audit-D/audit2.py:139-155`; `analysis/audits/audit-D/summary.md:7-29`; `COMBO-REPORT.md:195, :289-373, :421-428`; `tools/tmp-scripts/README.md:7`. Research: R1-R02 §4; R1-R04 §5, §8; R1-R06 §3; R1-R08 §7-8; R1-R11 §1-6; R1-S00 §0-4; R1-S01 §1-2; GQ R1-CLS-09, R1-CLS-10.

#### R1 2.4 The shared review CLI package: two stacks in one package

**Shape.** `src/superclaude/cli/review/` is one click group (`superclaude review`, registered at `cli/main.py:568-570`) that holds two parallel stacks. The #346 v1 stack [E3] (`findings` to `ledger` to `merge_cmd` and `ledger_cmd`, plus `telemetry`; 131 tests) produces verdicts. The reflect v2 stack [E1] (`findings_v2` to `card_convert` and `cluster` to `cluster_cmd` and `verify_cmd`, plus `manifest`; 520 tests) is telemetry and flagging only. `panel.py` is shared by both. The package on this branch equals `origin/master` (d2d8a2d16): `git log d2d8a2d16..HEAD -- src/superclaude/cli/review tests/review` is empty (R1-S02 header). There are seven real subcommands (`panel resolve|validate`, `merge`, `ledger revise|defer|verdict|capture`, `telemetry taskvars|append|load`, `cluster`, `verify-citations`, `manifest init|advance|validate`) plus two ghost loader names, `lint_cmd` and `estimate_cmd`, which belong to unmerged experiment branches PN2 and PN3; the loader swallows the missing module silently; each of the seven real subcommands has its own help-presence test (`test_review_cli.py:44-49` for `panel`, `merge`, `ledger`, `telemetry`; `test_review_cluster_cmd.py:260`; `test_review_verify_citations.py:194`; `test_review_manifest.py:434-439`), but no test pins the exact registered set or the absence of the ghost names (R1-R09 §1 [CODE-VERIFIED]; help tests re-read at HEAD 792cf8c52; R1-D13).

| Module (lines) | Stack | Origin | Role |
|---|---|---|---|
| `findings.py` (457), `ledger.py` (494), `merge_cmd.py` (118), `ledger_cmd.py` (137) | v1 [E3] | #346 | parse findings-v1, cluster, ledger rows, verdict |
| `telemetry.py` (447), `telemetry_cmd.py` (98) | v1 [E3] | #346 | review-telemetry/1; no caller in `src` |
| `findings_v2.py` (304), `card_convert.py` (517), `cluster.py` (487), `cluster_cmd.py` (197), `verify_cmd.py` (184) | v2 [E1] | reflect (#519) | v2 contract, legacy card conversion, citation clustering, citation pre-check |
| `manifest.py` (534), `manifest_cmd.py` (240) | v2 [E1] | reflect (#519) | staged run manifest |
| `panel.py` (707), `panel_cmd.py` (129), 8 `data/review-panel.*.json`, `review-tiers.default.json` | shared | #346 plus reflect additions | template and tier resolution |

(R1-S02 §1 [CODE-VERIFIED].) The v2 stack imports private v1 names (`_check_flat`, `_ID`, `_blocks_after`, `_HEAD_FINDINGS`) and the public `refs_norm` and `flat` from `findings.py`, so a change to the v1 limits or fence rules changes v2 too; the numbers 12, 200, 300 and 8 are repeated as literals in nine places with no shared constant (R1-R01 §14.1). There is no v2 ledger, v2 verdict or v2 merged report (R1-S02 §1 observations).

**Today's data flow, stack A: findings-v1 to verdict [E3] (also the stack E2 drove unchanged).**

```
 reviewer report (fresh context, same brief)  ->  "## Findings block" with ```findings-v1 JSON lines
        |
        v
 findings.parse_block      10 ordered rules per line (findings.py:90-121)
        |   bad line -> skipped, first error kept, block_ok=false; the other lines are KEPT
        v
 findings.annotate         anchor located by flattened exact match in ONE candidate document
        |   missing anchor -> kept, span None, section "none"                       (D5)
        v
 findings.cluster          union-find, transitive: same fp (section+refs) OR (refs intersect or both refs empty)
        |                  and spans within 3 lines; no chain detection              (D6)
        v
 ledger.merge_round        row.blocking = any(member.blocking)                       (D4)
        |   clearing loop: resolved_check rows nobody re-reported -> resolved,
        |   block_ok never read                                                      (D2)
        |   raises only if NO reviewer block is valid                                (D3)
        v
 verdict  = FAIL iff any open|regressed blocking row          (ledger.py:273-274)
 decision = PASS | REVISE (n < cap) | ESCALATE                (label only; round 4 merges)
        |
        v
 merged report + reviser brief -> reviser -> fixmap-v1 -> `review ledger revise` -> next round
```
(R1-R01 §1; R1-R02 §1.2; R1-R03 §1-3; R1-S02 §3 [CODE-VERIFIED]. Not drawn: the installed experiment ledger and stoprule, which are variants of this loop, section 2.3.) [Correction M-25: the `findings.cluster` line of the diagram now names the both-empty-refs branch of `same_defect` (`findings.py:367-379`).] <!-- Variant 1 (modified) — M-25: caption notes the fence-line correction at V1:305 -->

**Today's data flow, stack B: findings-v2 to telemetry, beside the authoritative legacy verdict [E1].**

```
 reviewer card (reflect-reviewer, persona) = legacy card + "## Findings block" (findings-v2)
        |                                    + calibration.per_finding (blind calibrator line)
        |
        +--> findings_v2.parse_block     23 ordered rules per line (findings_v2.py:84-187)
        |        ANY bad line -> block state "invalid"
        |        -> cluster_v2 skips EVERY finding of a non-complete block (cluster.py:221, :256-257)
        |    cluster_v2          citation-based union-find; `chained` flag; calibrated `support`;
        |                        `disputed`; cluster_agreement; anchor-only findings stay singletons
        |    verify-citations    flags citations to re-read, drops nothing
        |        ==> panel/clusters.json + telemetry: block   TELEMETRY ONLY, never routes or drops
        |
        +--> legacy path (authoritative; protocol steps executed by the orchestrator)
                 sc-adversarial Mode A over the card files -> adversarial/merged-verdict.yaml
                 -> evidence-validator -> return-contract.yaml (1.8.0, orchestrator-written)
                 -> contract.derive_verdict: HALTED on regression or drift count > 0,
                    DEGRADED on convergence < 0.80 or null, else PASS
```
(R1-R01 §2; R1-R03 §2; R1-R05 §1, §7, §9; R1-R07 §1; R1-S02 §3 [CODE-VERIFIED for the CLI and wrapper steps; the debate, evidence-validator and contract writing are protocol-executed and checked on disk by `panel_lint` EV-1, R1-R07 §2.3, rather than by a Python orchestrator].)

**Key divergences between the two stacks (all [CODE-VERIFIED]).**

| Aspect | v1 stack [E3] | v2 stack [E1] | Evidence |
|---|---|---|---|
| Invalid block | line skipped, other lines kept and clustered (`findings.py:188-192`, `ledger.py:135-138`) | whole block `invalid`; the reviewer's findings are not clustered (`findings_v2.py:299-303`, `cluster.py:256-257`); per-line errors are persisted in `cards[].errors` (`cluster_cmd.py:161`, GQ R1-CLS-01) | R1-R01 §2.3; R1-R03 |
| Empty block | valid | invalid unless every assigned coverage row is observed (`findings_v2.py:291-298`) | R1-R01 §2.4 |
| Prior lines (re-review) | accepted (`findings.py:175-187`) | rejected (`findings_v2.py:279-283`): v2 has no re-review protocol | R1-R01 §2.4 |
| Location | `anchor` exact quote in one document | `citations` (role, path, line range, optional quote); anchor optional | R1-R01 §2; R1-S02 §2 |
| Fingerprint | sha256 of `v1\|section\|refs` | sha256 of `v2\|role\|path\|section\|refs\|class`, with section always empty (so equal refs on one file merge at any distance) | R1-S02 §3; R1-R03 |
| Chaining | not detected | detected, flagged, excluded from `cluster_agreement`, not split | R1-R03 §2 |
| Representative claim | first member (`ledger.py:191`, `:199`) | highest calibrated confidence | R1-R03 |
| Line convention | 0-based half-open (`findings.py:302`), tolerance 3 | 1-based inclusive (`findings_v2.py:77`), tolerance 3 | R1-R03 R1-G10 |
| Ref-id regex | `_REF_TOKEN` (`findings.py:29`) | the same `refs_norm`, imported (`cluster.py:64`) | R1-S02 §3 |
| Docstring claim | none | `findings_v2.py:3-5` is a line-level claim, true for `check_finding` without a lens, and states the prior-line difference itself (`:5`); it omits that a pure-v1 line fails under lens `reflect-post` (`deviation_class` required, `:147-149`), the empty-block rule (`:291-298`) and the whole-block `invalid` state (`:299-303`), so v2 is not a block-level drop-in for v1 [CODE-VERIFIED] | R1-R01 §2.4 |

**Hand-off defects R1-D1 to R1-D16 against current code.** All 16 were checked in R1-S02 §5 against the code on this branch (= master); the table gives the confirmed status and whether the reflect v2 stack shares the defect.

| ID | Defect | Status now | Reflect v2 shares it? |
|---|---|---|---|
| R1-D1 | over-length anchor, anchor2, claim (also anchor under 12, more than 8 refs, MINOR plus blocking) are rejected; ledger keeps only `block_ok` and one first-error warning, not ids | confirmed (`findings.py:104,108,118`; `ledger.py:130-134,141-149`) | yes for native v2 output, and harsher (one bad line invalidates the block); no for converted legacy cards, which truncate silently |
| R1-D2 | an unreported `resolved_check` row clears even when the reviewer block was invalid | confirmed (`ledger.py:254-258`); docstring :112 contradicted | no ledger |
| R1-D3 | a round passes with one valid reviewer | confirmed (`ledger.py:150-157,273-274`) | no verdict |
| R1-D4 | one reviewer's `blocking` decides the row and verdict; `confidence` display only | confirmed (`ledger.py:187,213-218`); "never used" only partly true | partly: `blocking_any`, with `support` and `disputed` computed but unused |
| R1-D5 | missing anchors kept silently | confirmed (`findings.py:349-358`) | partly: unresolved citations kept, flagged by `verify-citations` |
| R1-D6 | transitive clustering over- and under-merges; row keeps first member's claim | confirmed (`findings.py:367-407`) | yes, partly mitigated by the `chained` flag; v2 adds an over-merge path (empty section) |
| R1-D7 | ref regex misses `T01.02` (and `P10`; pulls `P1` out of `D-P1`) | confirmed (`findings.py:29`; `telemetry.py:23`) | yes (shared import) |
| R1-D8 | brief never names the source document | confirmed in the E3 brief (`document_review_loop_prompts.md:17-21,32`); reflect injects the spec body for the qa persona only | partly |
| R1-D9 | brief grades an unstated requirement Medium while the schema lets `missing-requirement` block | confirmed; v2 with `reflect_category: coverage` forces MAJOR to block (`findings_v2.py:161-162`): opposite rule | different rule |
| R1-D10 | `unpassable-ac` rejected, only `unpassable-check` valid | confirmed; an E2 harness brief error, fixed in the eval only; `card_convert` coerces unknown words to `other` | same rejection in v2 |
| R1-D11 | duplicates silently re-admitted when a pool is exhausted | confirmed at `panel.py:536-543`; `--strict-distinct` is the opt-in fix | default still re-admits |
| R1-D12 | environment keyed on `$T3Model01` only; `T2bModel01` never read | confirmed at `panel.py:485-494` | same selector |
| R1-D13 | `lint_cmd` and `estimate_cmd` registered but absent; error swallowed | confirmed (`__init__.py:19-36`) | the loader also carries the three reflect modules |
| R1-D14 | no tasklist review step in `sc-tasklist` or `sc-workflow`; loop only in spec-panel plus prompts | confirmed for direct CLI calls; both skills reach reflect (section 2.5); [CODE-CONTRADICTED] that no skill calls `panel resolve` (reflect shadow step 1 and prompts :70 do) | n/a |
| R1-D15 | telemetry strata only sonnet and haiku; `merge` and `panel resolve` write no telemetry | confirmed (`telemetry.py:112-115,267-268`; `merge_cmd.py:71-118`) | reflect does not use `review telemetry` |
| R1-D16 | round 4 accepted; `--cap` ignored on an existing ledger; verify-only not a code mode | confirmed (`ledger.py:114-118`; `merge_cmd.py:101-104`) | no rounds |

(R1-S02 §5, R1-R02 §1.4, R1-R04 §10, R1-R09 §7; line numbers for R1-D7, R1-D11 and R1-D12 are the current ones, the hand-off's older lines are stale with behaviour unchanged.)

**Test surface.** `tests/review` collects 651 tests in 19 files (131 in the seven #346 files, 520 in 12 reflect files); `tests/cli/reflect` has 38 files and 353 tests (not 12); six skill-text tests hold 178; the whole surface is 1182 (R1-R12 summary). The hand-off count of 111 tests predates #519 (R1-S00 §8 [CODE-CONTRADICTED] by R1-R12). Four tests pin defects as intended behaviour: `test_review_ledger.py:376-385` pins R1-D3 and R1-D2, `:408` pins R1-D5, the exclusion tests plus both golden fixtures pin R1-D11, and `test_review_ledger.py:129` and `test_review_telemetry.py:327` encode R1-D4 and R1-D15 (R1-R12 §3, summary). <!-- Variant 1 (modified) — M-25: 37 corrected to 38 reflect test files (V1:381 only; checked by fault-finder row 6) -->

**Evidence:** R1-S02 §1-6; R1-R01 §1-3, §14; R1-R02 §1, §5; R1-R03 §1-3; R1-R04 §1-4; R1-R08 §3-5; R1-R09 §1, §7; R1-R12 §1, §3 and summary; `src/superclaude/cli/review/` files at the line numbers shown above.

#### R1 2.5 Consumers and future consumers today

**How each consumer reaches a review today.**

```
 /sc:spec-panel --mode critique ---> prompts file :70 ---> superclaude review panel resolve | merge | ledger   [E3 stack A]
 sc:workflow Wave 4   (advisory) ---> /sc:reflect --mode pre, default flags ---> legacy Tier 2 rotation       [E1 legacy]
 sc:tasklist Stage 10.5 (advisory) -> /sc:reflect --mode pre --remediate ...  ---> legacy Tier 2 rotation     [E1 legacy]
 sc:tasklist per-phase post gate (BLOCKING) -> superclaude reflect run --depth deep --fix
                                  ---> runner.py:538-545 ---> ensemble.py (swarm, score-only debate, contract "1.0")
 /sc:reflect --t2-engine shadow ---> panel kernel steps 1-10 (stack B)        nobody passes this flag
 sc:brainstorm, sc:design ---> no review step
 pr_submit FSM ---> Augment + Codex (closed tuple) ---> severity_router ---> S2b verify seam ---> /sc:troubleshoot
 rf-* skills (11 skill files) ---> rf-qa | rf-qa-qualitative | rf-analyst agents (write tools, in-place fix)
```
(R1-R09 §2-7; R1-R13 §2.1, §6; R1-R10 §1, §3 [CODE-VERIFIED for the code paths; SKILL.md prose for the advisory or blocking status is checked against `refs/return-contract.md:16` and the post-gate text at `sc-tasklist-protocol/SKILL.md:1141-1184`].)

| Consumer | Review mechanism today | Advisory or blocking | Who owns the verdict | Evidence |
|---|---|---|---|---|
| `/sc:spec-panel --mode critique` [E3] | prose Review Loop plus the CLI named only in the rules prompts file; one-reviewer fallback when `superclaude` is missing | blocking through the ledger verdict, exit 0/10/11 | `ledger.py` | R1-R09 §2; R1-S05 §2 |
| `sc:workflow` Wave 4 [E1 via reflect] | `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, defaults for every other flag, no `--remediate` (`sc-workflow-protocol/SKILL.md:85-91`); `source.md` is passed as reflect's `--spec`, so a prompt-only source yields a one-line "spec" (W-3) | advisory (`refs/return-contract.md:16`) | reflect contract | R1-R09 §3; R1-R06 §5 |
| `sc:tasklist` Stage 10.5 [E1 via reflect] | N parallel `/sc:reflect --mode pre --remediate` per phase, depth and tier computed into `validation/reflect-pre/depth-map.yaml` (`SKILL.md:1619-1646`) | advisory sign-off | reflect contract | R1-R09 §4.1 |
| `sc:tasklist` per-phase post gate | generated phase files carry `superclaude reflect run <phase-tasklist> --depth deep --fix --no-promote --base <sha> --output ...` (`SKILL.md:1155-1179`, template `phase-template.md:182`) | blocking | the code-driven engine below | R1-R09 §4.2; R1-R13 §6 |
| `sc:brainstorm`, `sc:design` | none. Brainstorm Wave 3 delegates to `sc-adversarial-protocol` for proposal debate (routing at convergence 0.65 and 0.50), not for reviewing its output; `design.md` step 4 is self-validation with codegraph; neither carries FR/AC ids by rule | n/a | n/a | R1-R09 §6; R1-S05 §1B |
| PR review (`pr_submit`, `sc-auggie-review-protocol`) [ext] | findings from a closed set of two GitHub bots (`REVIEWERS = ("augment","codex")`, `reviewers.py:41`), normalised to `Finding`, graded by `remap_severity`, deduplicated by exact `(path, line)`, verified at the S2b seam (`fsm.py:941`), routed Critical/High to `--depth deep --fix`, Medium to `--fix`, Low/Nit report-only; `/sc:auggie-review` is already an internal once-per-PR fallback finder (`fsm.py:956-1022`) | blocking via route and merge guard | `severity_router.py` | R1-R10 §1 [CODE-VERIFIED] |
| rf-qa, rf-qa-qualitative, rf-analyst [ext] | zero-trust QA agents spawned at 43 call sites in 11 skill files [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E] (R1-R10 §3 census; 32 of the 41 review call sites among the 43 depend on an in-place fix step); `rf-qa.md` has write tools and `permissionMode: bypassPermissions`; issues table with columns #, Severity, Location, Issue and Required Fix, severities CRITICAL/IMPORTANT/MINOR and `Location = [file:section]`; fix cycle, two cycles then escalate, with monotonicity and regression halts (`rf-qa.md:381-418`) | PASS/FAIL | the agent | R1-R10 §3; R1-S05 §1C <!-- Variant 1 (modified) — M-25 (M-24 item 7): unit note on run 1's 43 call sites --> |

(The R1-S05 grep census counts 19 skill files and 521 matching lines for the same agents; the units differ, matching lines in 19 files against spawning call sites in 11 skill files, so both are kept, R1-S05 §1C, R1-R10 summary.)

**The third merge path: the code-driven Tier 2 engine behind the blocking post gate [E1-adjacent: master baseline].** `superclaude reflect run` accepts only `--depth standard|deep` (`commands.py:255`), and `runner.py:538-545` always calls `run_tier2_ensemble` for those depths and then sets `rc = 0` unconditionally, so the `/sc:reflect` skill, its 1.8.0 contract, `panel_lint` and the shadow kernel are never involved in the gate (R1-R13 §2.1, §2.4 [CODE-VERIFIED]). Provenance contradiction: the task scheme tags `cli/reflect/` code [E1], but `git diff --stat origin/master` over `ensemble.py`, `runner.py`, `contract.py`, `commands.py`, `config.py` is empty and `git log` shows PRs #213, #214, #220 and #329, so the engine predates the E1 shadow work and is master baseline; the stronger evidence is the diff, so this file calls it E1-adjacent (R1-R13 §1.7).

| Property | What the code does | Evidence |
|---|---|---|
| Reviewers | in-process transport calls to external OpenAI-compatible models from the `T2Model0N` env pool (swarm package), no tools; they see only a header with the base ref plus the tasklist body, no diff and no code under audit; an `OSError` yields an empty body | `ensemble.py:339`, `:601-630`; R1-R13 §1.5 |
| Merge | mechanical concatenation, then a score-only `/sc:adversarial` child that returns `convergence_score` only | `ensemble.py:514-561`, `:633-654`; R1-R13 §1.5 |
| Contract | writes its own version-`"1.0"` `return-contract.yaml` with 11 keys outside the 1.8.0 lists (`REFLECT_CONTRACT_VERSION` :74; `yaml.safe_dump` :886-895); `merge_method` is `adversarial` whenever two or more reviewers succeed, even if the adversarial step failed (:773); `status` is the literal `"success"` (:789) | R1-R13 §1.6, §3-4 |
| Verdict | deviation fields default clean (:103-113, :442-471), so no production contract can HALT on a found deviation; the gate is a reviewer-agreement and diversity check, not a deviation audit | R1-R13 §10 R1-D1 (graded Critical) |
| Missing steps | no calibration, no evidence validation (`citations_dropped` is the constant 0, :817), no clustering, no reviewer cards | R1-R13 §1.5 |
| Executor exclusion | `executor_model_class` is read from phase-file frontmatter (`config.py:53`, `:351-354`) but the Tier 2 route never uses it; the gate's "executor-disjoint reviewers" claim (`sc-tasklist-protocol/SKILL.md:1165`, `:1177`) is [CODE-CONTRADICTED] | R1-R13 §2.4, §6 |
| Fix loop | `--fix` is inert on this route: the ensemble contract carries no remediation keys | `runner.py:762-775`; R1-R13 §2.2 |
| Failure surface | an exception in the engine re-raises and exits 1, outside the documented 0/10/11/2 map (`commands.py:442-469`); `REPORT.md` and the per-task verdict matrix the gate text promises are never produced | R1-R13 §2.4, §6, §10 |
| Tests | `tests/cli/reflect/test_ensemble_*` (2036 lines); tests patching `runner.ClaudeProcess` never exercise the engine through the runner | R1-R13 §2.1, §7 |

Two reflect contract schemas therefore share one file name and one reader (`contract.py`): the skill's 1.8.0 contract written by the orchestrator and this engine's code-written "1.0" (R1-R13 gap 15, R1-R08 §12).

**Callers of the review CLI today.** Grep over skills, commands and core (2026-11-14): `review merge` and `review ledger revise` are named only in `document_review_loop_prompts.md:70`; `ledger defer|verdict|capture` have no prose caller; `review panel resolve` is called by reflect shadow step 1 (`SKILL.md:340`) and prompts :70; `cluster`, `verify-citations` and `manifest` only by reflect shadow steps and offline scripts; `telemetry *` and `panel validate` by tests only (R1-R09 §7 [CODE-VERIFIED]). The earlier statement that no skill calls `panel resolve` is [CODE-CONTRADICTED] (GQ R1-CLS-12).

**Known gaps in the PR and rf-qa consumers (current state, not design).** The PR router differs from its rubric on at least seven points (rubric `in_diff` exception versus an unconditional tier drop at `severity_router.py:178-189`; no `error-handling` row in the router or the rubric; `security-latent` exists only in the router; `tests` floor Medium versus the rubric's calibration example Low; step 5 drops every finding when `deep=True` and no caller passes it; low-confidence Critical drop unconditional; fixed ceilings), most of them dormant for live Augment and Codex roots because those carry only a severity hint, not `category`, `confidence` or `in_diff` (R1-R10 §2, §1.3; the classifier's added fields are [UNVERIFIED]). `rf-qa.md:41` still says a QA pass that finds zero issues is suspect, which conflicts with the #346 no-quota rule, and the test docstring that claims the wording was removed is [CODE-CONTRADICTED] (the test bans only "surfaces zero issues as suspect", `test_review_prompt_overrides.py:146`) (R1-R10 §4). Replacing rf-qa also touches three test files that pin rf-qa text (R1-S05 §1C; R1-R12 §7).

**Evidence:** R1-R09 §2-7 and summary; R1-R10 §1-4 and summary; R1-R13 §1-2, §4-6, §10 and summary; R1-R06 §5; R1-S05 §1B-1D, §3; `sc-workflow-protocol/SKILL.md:85-91`; `sc-tasklist-protocol/SKILL.md:1141-1184, :1619-1646`; `src/superclaude/cli/reflect/{ensemble,runner,commands,config,contract}.py` (lines as cited in the table); `src/superclaude/pr_submit/{reviewers,fsm,severity_router,models}.py`.
