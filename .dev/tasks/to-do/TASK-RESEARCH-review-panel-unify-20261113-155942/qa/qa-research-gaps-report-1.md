# QA Report — Research Gate (Gap-Detection Lens, Partition 1 of 2)

**Topic:** Unified Review Panel (E1 reflect Tier 2 panel kernel / E2 tasklist review-panel study at 4a22d742 / E3 #346 review loop)
**Date:** 2026-11-13
**Phase:** research-gate
**Lens:** gap-detection (checklist items 5-10: contradiction resolution, gap severity, depth appropriateness, integration points, pattern documentation, incremental writing)
**Fix cycle:** N/A (first review)
**fix_authorization:** false (report only)
**Assigned files:** research/01-finding-contract.md, 02-ledger-merge-verdict.md, 03-clustering.md, 04-panel-resolution-identity.md, 05-blocking-calibration.md, 06-input-contract-briefs.md
**Depth tier:** Deep

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

**Analyst reports at start of review:** `qa/analyst-completeness-report-1.md` and `qa/analyst-cross-validation-report-1.md` existed but were header-only stubs (cross-validation verdict "PENDING (written last)"); no gap lists or severity ratings were present to verify, so full independent verification was performed.

---

## Per-file findings (appended as each file is reviewed)

### 01-finding-contract.md (474 lines, Status: Complete, Summary present)

Read in full (lines 1-475). Spot-checked against code (Bash `sed -n`):
- `cluster.py:221` `valid = block.get("state") == "complete"` and `cluster.py:256-257` skip of non-valid reviewers: confirmed.
- `findings_v2.py:161-162` blocking label rule: confirmed.
- `card_convert.py:303-311` `counts` has no truncation counter: confirmed, so the [CODE-CONTRADICTED] tag on the research-prompt premise is correct.

- Item 5 (contradictions): none inside the file. Cross-file checks are below.
- Item 6 (gap severity): the Gaps section (:445-461) has 4 [UNVERIFIED], 3 [CODE-CONTRADICTED], 4 plain gaps and 3 questions. None of them carries a severity rating in the file. My ratings:
  - G01-1, "do `cluster_cmd`/`verify_cmd` persist per-line `errors`" (:447). This touches D1 surfacing, which feeds the finding-schema and merge decisions. The code answers it: `cluster_cmd.py:161` writes `"errors": block["errors"]`. 03 §3 (:157) answers it inside the partition, but 01 still says [UNVERIFIED]. MINOR, because synthesis can use 03.
  - G01-2, "does `verify_cmd` check `line_end`" (:448). The code answers it: `verify_cmd.py:66-67` returns `out-of-range`. 03 §4 (:170) answers it inside the partition. MINOR, for the same reason.
  - G01-3 DNSP code (:449), G01-4 `remap_severity` caller (:450) and the `security-latent` emitter (:455) are PR-review and rf-qa details that do not block a conflict decision. MINOR.
  - Questions (:459-461) on blocking ownership, the re-review protocol and `_REF_TOKEN` are framed openly as owner or conflict-log inputs and are not hidden. OK.
- Item 7 (depth): PASS. Data flow is traced end to end for both stacks: reviewer line -> `parse_block` -> `ledger.merge_round` (v1), and reviewer line -> `cluster.py` valid gate (v2). The card path is traced too: card -> card_convert -> check_finding.
- Item 8 (integration points): PASS. Attach points are given with file:line: the container at findings.py:31 and :38-76, `LENSES` at :36, `PRIMARY_ROLES` at cluster.py:67-70 and `PROFILES` at review_ledger.py:53-59.
- Item 9 (patterns): PASS. Captured patterns: v2 imports private v1 names (:62, :116), the limits are duplicated as literals in 9 places (§14.1), and the Medium grade exists only in prose (§5).

### 02-ledger-merge-verdict.md (329 lines, Status: Complete, Summary present)

Read in full (lines 1-330).
- Item 5 (contradictions):
  - 02 and 01 agree on the 49 lost blocking findings. 02 §4.2 (48 length + 1 refs) is consistent with 01 :285 and :386.
  - 02 corrects the hand-off's "4 verdict flips" to 3 and explains the 4 (:128, Gap 3). 01 :377 says only "verdicts flipped" with no count, so the files do not conflict.
  - 02 §5.4 (:181) and 01 §2.3 (:100) agree that v2 drops the whole reviewer, and 03 Q5 confirms it.
  - Resolved: none open.
- Item 6 (gap severity): the Gaps section (:303-317) has 13 entries and none is rated. My ratings:
  - G02-8 [UNVERIFIED] "does verify-citations check that the cited line range exists" (:312). This is a design input to the merge and anchor-handling conflict, because 02 §5.3 step 2 (:174) builds on it. It is answered in code (`verify_cmd.py:66-67`) and in 03 §4 (:170). MINOR, because the answer is in the partition.
  - G02-7 [UNVERIFIED] E2 "65 blocking vs 38 real over 71 rows" (:311) is cited through the hand-off only. This number is the main E2 evidence for the blocking-rule conflict (single-reviewer veto vs quorum or grader). It must be source-verified in at least one file before synthesis. See the 05 entry below for whether 05 does that.
  - G02-9 re-ask compliance (:313) and G02-10 no round 2-3 evidence (:314): these are evidence absences, stated openly, with no data in any effort. Synthesis must carry them as open questions. They do not hide a decision. MINOR.
  - G02-12 blocking-decider choice (:316) and G02-13 anchor-to-citation step (:317): these are conflict-log inputs, framed openly. OK.
  - G02-5 haiku/grok count gap (:309) and G02-11 grader_model read by grep only (:315): MINOR.
- Item 7 (depth): PASS. `merge_round` is traced step by step (§1.2, 12 steps). The D1 loss path is traced from reviewer line to verdict (§4.3), and the v2-capable merge requirements are derived from code (§5.3).
- Item 8 (integration points): PASS. Covered with file:line: the CLI seam (`merge_cmd.py:22-70`, `ledger_cmd.py:13` exit codes), the `--resolution` coupling between panel and merge (:89), `PROFILES` as the extension point (:225), and grader reuse after clustering (:260).
- Item 9 (patterns): PASS. Covered: verdict by stored label, not recompute (:41), the cap enforced by label vs by refusal (§6.2 table), and tests that pin defects (§3).
- Minor note: the header date is 2026-11-14 (:6), and §1.4 and §4.2 say "re-read 2026-11-14", but the file's mtime is 2026-11-13 17:44 UTC. This is probably a timezone or context-date artefact. MINOR.

### 03-clustering.md (396 lines, Status: Complete, Summary present)

Read in full (lines 1-397). Spot-checks:
- `cluster.py:405-408` returns `agreement = 1.0` when there is no blocking cluster: confirmed.
- `cluster_cmd.py:161` persists `errors`: confirmed.
- `verify_cmd.py:66-67` `out-of-range`: confirmed.
- `stage0a-report.md:243` totals and `:251` showing `1.0000`: confirmed. So 03's [CODE-CONTRADICTED] correction of scope slice 04 §0.3 is right.

- Item 5 (contradictions): 03 finds and resolves three contradictions with scope slices or E2 docs: `anch.py` is not chaining evidence (:281), the "195 of 1398" denominator (:288), and `cluster_agreement` null vs 1.0000 (:228). Each one is resolved against code or data. Within the partition, 03 also resolves the [UNVERIFIED] items G01-1, G01-2 and G02-8 (above). Nothing unresolved.
- Item 6 (gap severity): the Gaps section (:368-382) has 13 entries and none is rated. My ratings:
  - G03-1 W-3 [UNVERIFIED] (:370), "`spec:N` resolved against short `source.md`". This affects the location model and the brief/input conflict. 01 §3.3 (:135) already reads `card_convert.py:124-125` (the `source.md` or `spec` token maps to role `spec` on the spec path). See the 06 entry for whether W-3 is closed.
  - G03-4 [UNVERIFIED] "is the shadow-run `cluster_agreement` 1.000 from the no-blocking branch" (:373). This bears on calibration and agreement evidence for the who-judges / calibration conflict. See 05.
  - G03-2 D7 effect on real tasklists (:371), G03-3 population precision/recall (:372) and G03-5 the v2 loss on E2 data (:374) are inferences or measurements not done, and they are labelled as such. MINOR, but synthesis must not state them as measured.
  - G03-10 line-number convention (:379), G03-11 no symbol/section for v2 (:380) and G03-13 ordering dependence (:382) are design notes. MINOR.
  - G03-12 invalid-block policy (:381) is an open conflict input. OK.
- Item 7 (depth): PASS. Both algorithms are traced from CLI entry to output (Q1 table, :309-323). There is an execution probe of `refs_norm` (§5.2), and the E2 replay code is read side by side with `findings.py`.
- Item 8 (integration points): PASS. Covered with file:line: the `review cluster` CLI (`cluster_cmd.py:96-133`), `clusters_kept` (:447), the ledger entry (`ledger.py:165`), and the reuse points for one clusterer in Q9 (`findings.locate`, `_citation`, `section_of`, `opcodes`/`map_span`, `verify_cmd._check`).
- Item 9 (patterns): PASS. Covered: the regex copied, not imported (`telemetry.py:23`), refs harvested from prose, representative-by-input-order, and tests pinning behaviour (§6.5).
- G03-4 can be answered from the run files. I ran `jq` over the 14 `.dev/reflect/pre-*shadow*/panel/clusters.json` files:
  - 11 runs have 0 blocking clusters, so `cluster_agreement` is 1.0 by the default branch (`cluster.py:407-408`).
  - shadow02 and shadow04 each have 1 blocking cluster, and it is chained, so the value is null.
  - Only shadow09 has a real calibrated value: 0.9328 over 3 unchained blocking clusters.
  - So scope 04 F-18 ("1.000 everywhere") carries no calibration signal, and the only real agreement figure in E1 comes from one run. MINOR, because 03 already warns that the value may be the default branch. Synthesis should cite this answer and not leave the item [UNVERIFIED].

### 04-panel-resolution-identity.md (318 lines, Status: Complete, Summary present)

Read in full (lines 1-319).
- Item 5 (contradictions):
  - 04 corrects scope 02 D14: `document_review_loop_prompts.md:70` calls `panel resolve` in prompt text (:256, Gap 14). This is consistent with 01 §5 (:191), which cites the same line for the merge refusal.
  - 04 §10.1 (E2 reused the `review-panel-resolution/1` shape) and §5 (E2 bypassed the resolver) agree with 02 §2.2 (:89): the shape was reused and the resolver was not.
  - Stale hand-off line numbers are reconciled (:306-308).
  - No open contradictions.
- Item 6 (gap severity): the Gaps section (:287-302) has 14 entries and none is rated. My ratings:
  - G04-6 [UNVERIFIED] "is `--forward-subagent-text` required for sub-agent `message.model`" (:294). The file says it "decides whether observed identity is available for skill-driven dispatch at all". It bears on the identity conflict (observed vs pinned), but it does not block the decision, because §7.1 shows observation works with the flag (combo runs 2026-11-13). Synthesis must carry it as an open feasibility question. MINOR.
  - G04-2 (identity adapter not implemented, [CODE-CONTRADICTED]), G04-3 (`model_observed` unused) and G04-5 (rule D5 has no code) are verified absences, stated as such. OK.
  - G04-10 (Sonnet-alone 2/16) and G04-11 (E2 `manifest.md:11`) are [UNVERIFIED] side evidence and not decision-bearing. MINOR.
  - G04-12 (is distinctness a correctness requirement or a cost knob) and G04-13 (`verify-only` kind) are owner questions, framed openly. OK.
  - G04-1 (qwen/kimi/deepseek branch), G04-4 (tier0), G04-7 (gateway routing is runtime), G04-8 and G04-9 (E2 runner cost and APIERR) are documented and MINOR.
- Item 7 (depth): PASS. Covered end to end: template -> `validate_panel` -> `resolve_slot`/`resolve` -> resolution JSON -> (not) dispatch -> served model. Actual `panel resolve` runs were made (live7 duplicate, reflect gateway error, strict collapse), and the env-alias routing to served model is traced (§4.1, §7.2).
- Item 8 (integration points): PASS. Covered with file:line: slot keys (`panel.py:46`), `_KINDS` (:36), the reflect profile (:71-157), `select_env` (:485-494), CLI options (`panel_cmd.py:18-63`), telemetry `REVIEWER_GROUPS` (`telemetry.py:30-81`), and the reflect §4.3a step lines.
- Item 9 (patterns): PASS. "Panel data, not code, selects models", the "prose loops drive the CLI" corollary (resolution recorded but not dispatched), and record fields rewritten to agree (E1 card `model:` := pin, E2 `expected_model` := fallback, :218) are all captured.

### 05-blocking-calibration.md (420 lines, Status: Complete, Summary present)

Read in full (lines 1-421).
- Item 5 (contradictions):
  - 05 verifies the E2 "65 vs 38" figure at source (`COMBO-REPORT.md:291`, §11). That closes 02 G02-7 inside the partition.
  - 05 §8.1 and 01 §3.2 agree on MEDIUM -> MINOR non-blocking. 05 §12 and 04 agree that `panel.py` has no calibrator.
  - Three of 05's own [UNVERIFIED] items are verified in sibling files:
    - rf-qa IMPORTANT is blocking: 05 :396, verified in 01 §9 (:246, rf-qa.md:106-111).
    - The `review merge` v1 parse path: 05 :397, verified in 02 §1.2 and §5.1.
    - The 6.70% figure: 05 :395, verified in 03 §6.1 (:229, stage0a-report.md:295-297).
  - Cross-file this is not a contradiction, but 05 still shows them as open. MINOR.
  - Source-document conflicts are surfaced and not resolved, which is correct for a research file:
    - SKILL.md:1196 vs `deviation-taxonomy.md:123` (static Regression).
    - Drift halts at any severity vs MINOR-never-blocks.
    - Rule A vs Rule B.
  - All of them are listed in Gaps (:398-400) for the conflict log.
- Item 6 (gap severity): the Gaps section (:389-407) has 18 entries and none is rated. My ratings:
  - G05-3 [UNVERIFIED] SKILL.md:1260 "debate is weighted by calibrated confidence" (:393). This bears on the who-judges / calibration conflict, because it decides whether calibrator-weighted debate is existing value to keep. My grep of `src/superclaude/skills/sc-adversarial-protocol/` for `calibrat` returns only `SKILL.md:1513` and `:1523` (the debate's own winner-confidence output). Nothing reads a calibrated confidence from input cards, so the claim is probably [CODE-CONTRADICTED]. The partition 2 files (07-12) do not mention it (grep). MINOR as a gate item, because it is visibly tagged [UNVERIFIED] and 05 §14 does not lean on it. Synthesis must not list "calibration-weighted debate" as existing value without this check.
  - G05-1 producer of `unauthorized_deviation_present` (:391). This is a verified absence (grep at §2.3), and 05 §13.1 gives it as an owner decision with options (a)/(b). Open and visible. OK.
  - G05-2 [CODE-CONTRADICTED] 5-dim vs 6-dim calibrator (:392). Resolved against code. OK.
  - G05-4 producer side of grounding gaps (:394). Prose-only producer. MINOR.
  - Conflicts (:398-400) and questions (:406-407) are conflict-log inputs. OK.
  - The grader accuracy gap (:405) and the no-ground-truth gap (:404) are evidence absences, stated openly. MINOR.
- Item 7 (depth): PASS. Covered end to end:
  - contract -> verdict (`derive_verdict` first-match chain, §1)
  - finding -> reflect flags -> panel blocking (§13)
  - a read-only tally of calibration vs blocking over 142 shadow findings (§5.3)
  - E2 ground-truth evidence traced to COMBO-REPORT and PILOT-REPORT lines (§11)
- Item 8 (integration points): PASS. Covered with file:line:
  - `support` as the calibrated-quorum hook (`cluster.py:39-49`, :336-351)
  - `PROFILES`-style per-lens predicates (§13)
  - the calibrator slot needed in the template (§12)
  - `merge_method` contract-bump rule (SKILL.md:837)
- Item 9 (patterns): PASS. Covered: prose rules executed by the orchestrating model vs code rules (Reuse-Miss threshold, :69), agents reused across skills without a rubric override (§4), and telemetry-not-routing for new signals (§9).

### 06-input-contract-briefs.md (282 lines, Status: Complete, Summary present)

Read in full (lines 1-283). Spot-check: E2 `COMBO-REPORT.md:373` (via `git show 4a22d742`) holds "156 valid-era runs of 665 never referenced source.md (ember 81 of 209, luna 49 of 222, ... sonnet 1 of 63, terra 0 of 44)". The figures in 06 §3.2 (:125) are correct, and `:291` holds the 65 vs 38 figure cited by 05.

- Item 5 (contradictions):
  - 06 §2.4 item 5 (:91) gives the recorded-brief mechanism for W-3: one-line `source.md` injected as "spec", with `spec:1` citations.
  - That is consistent with 01 §3.3 (:135, card_convert maps a `source.md`/`spec` token to role `spec` on the spec path). It closes 03 G03-1 inside the partition.
  - 06 §1.4 (:34) and 04 §9 (:256) agree that `document_review_loop_prompts.md:70` names `panel resolve`, `review merge` and `ledger revise`.
  - Internal E1 contradictions (agent `spec_path` vs template; C7 template vs 23 of 45 recorded briefs; L4 vs `gh issue view` in shadow09) are tagged [CODE-CONTRADICTED] and resolved against evidence.
  - No open contradictions.
- Item 6 (gap severity): the Gaps section (:253-270) has 16 entries and none is rated. My ratings:
  - G06-2 [UNVERIFIED] 156/665 and per-model split (:256). This is the main D8 evidence for the brief/input conflict, and 06 itself did not re-read the source. It is verified by my `git show` of CR:373 above, and 04 §8 read CR:373. Answered inside the partition, so MINOR. The causal link (brief does not name source -> not read) is marked as an inference by E2 itself ("UNVERIFIED" in CR:373), and 06 keeps it as an inference. Correct.
  - G06-3 (are `panel resolve`/`merge`/`ledger revise` registered) (:257). Answered in 02 §2 (merge_cmd, ledger_cmd) and 04 §3 and §4 (resolve was run). MINOR.
  - G06-1 MR:142 (:255), G06-4 skill version per shadow run (:258), G06-5 `--isolate-reviewers` (:259) and G06-6 `claude -p --allowedTools` behaviour (:260) are side evidence or design-feasibility notes, tagged. MINOR. G06-6 must stay an open item if synthesis recommends an allowlist for `claude -p` dispatch.
  - Questions 11-14 (source vs spec roles, Wave 0 snapshot of a referenced spec, injection cost, judge without source) and gaps 15-16 (brainstorm/design not wired, PR review without linked issue) are conflict-log or future-consumer inputs, framed openly. OK.
- Item 7 (depth): PASS. Covered end to end:
  - candidate/source -> brief -> reviewer reads -> findings citation -> judge
  - all 45 recorded E1 briefs inspected (awk pass plus 3 read in full)
  - the E2 runner traced line by line (shipping, cwd, permissions, meta fields)
  - consumer input matrix for 6 consumers (§5)
- Item 8 (integration points): PASS. Covered with file:line:
  - `## Values to fill` (`document_review_loop_prompts.md:15-21`)
  - the brief line and test pins (`test_review_rules_text.py:34-42`, :92)
  - reflect template sections (`reviewer-spec.md:33-74`)
  - `sc-workflow-protocol/SKILL.md:89` (Wave 4 call)
  - `input-parse.md:41`
  - the reviewer allowlist (`reflect-reviewer.md:5`)
- Item 9 (patterns): PASS. Covered:
  - prose-driven briefs drift from the template (23/45)
  - tests pin template text, not produced artefacts (C7)
  - the E2 brief is a filled copy of the E3 prompt
  - read-only by allowlist vs deny list

---

## Cross-file checks

### Item 10 — incremental writing compliance (all 6 files)

- File timestamps cannot settle this. Every file has birth == modify, but my own report also shows birth == modify after a Write and two Edits (`stat`, 20:37:02), because the Edit pathway rewrites atomically. So mtime/birth equality is not evidence of a one-shot write.
- Evidence used instead: tool calls in the session transcripts under `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-brainstorm-reflect-panel/` (grep for Write/Edit tool_use on each path). The Write and Edit counts include duplicated transcript records.

| File | Write calls | Edit calls |
|---|---|---|
| 01 | 2 | 8 |
| 02 | 2 | 18 |
| 03 | 2 | 10 |
| 04 | 2 | 10 |
| 05 | 2 | 18 |
| 06 | 2 | 9 |

- Every file was created once and then grown by repeated Edits. The content shows the same pattern: numbered sections, each closed by "Key Takeaways", then Gaps, Stale Docs and Summary.
- PASS.

### Item 5 — contradictions across 01-06

- No unresolved contradiction between research files was found. Agreements checked:
  - 49 lost blocking findings (01 / 02)
  - 3 vs 4 verdict flips (02 corrects, 04 Stale Docs agrees, 05 :314 agrees)
  - v2 whole-reviewer drop (01 / 02 / 03)
  - MEDIUM -> MINOR (01 / 05)
  - no calibrator in `panel.py` (04 / 05)
  - `document_review_loop_prompts.md:70` resolver call (01 / 04 / 06)
  - W-3 mechanism (01 / 03 / 06)
- Contradictions between source documents (Rule A vs Rule B; Drift halts vs MINOR never blocks; SKILL.md:1196 vs taxonomy:123; 5-dim vs 6-dim calibrator; reflect "unauthorized" flag with no producer) are surfaced in the files' Gaps sections for the conflict log. That is the correct handling at the research stage.

### Item 6 — the "no decision-blocking gap rated Minor" check

None of the six files rates its own gaps (CRITICAL/IMPORTANT/MINOR), so I rated every gap above. The gaps that bear on a conflict decision are either answered in the partition (with an exact file:line) or openly framed as an owner or design question:

| Decision area | Gaps that bear on it | Answer or framing |
|---|---|---|
| Finding schema / D1 | G01-1 | `cluster_cmd.py:161`, 03 §3 |
| Merge / anchor handling | G01-2, G02-8 | `verify_cmd.py:66-67`, 03 §4 |
| Blocking rule | G02-7 | CR:291, 05 §11 |
| Blocking rule | G05-1 | owner options, 05 §13.1 |
| Clustering | G03-12 | owner question |
| Identity | G04-6 | feasibility shown with the flag |
| Brief / input | G06-2 | CR:373 |
| Brief / input | G03-1 | 06 §2.4 |

The only decision-bearing gap still unanswered inside the partition is G05-3 (debate weighted by calibrated confidence). It is visibly [UNVERIFIED], 05 §14 does not depend on it, and my grep suggests it is false. I rate it MINOR, with a required carry-forward note (below).

---

## Overall Verdict: PASS (with notes)

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | Bash `grep -n "^\*\*Status"`: all 6 files are `Status: Complete`. Each has a `## Summary` (read in full). |
| 5 | Contradiction resolution | PASS | Cross-file agreements listed above. All source-document conflicts are surfaced in Gaps. No research-file pair disagrees. |
| 6 | Gap severity | PASS (with notes) | 84 gap entries across 6 files, all rated by QA above. Decision-bearing gaps are answered in the partition (file:line given) or framed as owner questions. No CRITICAL or IMPORTANT gap is open. |
| 7 | Depth appropriateness (Deep) | PASS | Each file traces a full data flow (per-file entries). There are execution probes in 03 §5.2 and 04 §4, and read-only tallies in 05 §5.3 and 06 §2.4. |
| 8 | Integration point coverage | PASS | Attach points with file:line in every file (per-file entries). |
| 9 | Pattern documentation | PASS | v2 importing private v1 names, panel data selecting models, prose loops driving the CLI, tests pinning text: all captured (01 :62, 04 §1/§6, 05 §4, 06 §1.6/§2.1). |
| 10 | Incremental writing | PASS | Transcript tool-call counts: 1 Write plus 4-9 Edits per file (counts doubled in the table above by duplicated records). |

## Summary
- Checks passed: 7 / 7 (lens items 5-10 plus item 1)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | File | Finding | Fix |
|---|----------|------|----------|-----|
| 1 | MINOR | 01-06 (all) | No research file rates its own Gaps entries by severity. Ratings exist only in this QA report. | When the gaps log (`gaps-and-questions.md`) is compiled, carry the QA ratings over from this report and the partition-2 report. |
| 2 | MINOR | 01 :447-448, 02 :312, 05 :395-397, 06 :256-257 | Items tagged [UNVERIFIED] in one file are verified in a sibling file of this partition: `cluster_cmd.py:161` errors persisted; `verify_cmd.py:66-67` out-of-range; rf-qa IMPORTANT blocking (01 §9); v1 merge parse path (02 §1.2); 6.70% (03 §6.1); 156/665 (CR:373); CLI subcommands exist (02 §2, 04 §3). | Synthesis must cite the verifying file and line, not the [UNVERIFIED] tag. |
| 3 | MINOR | 03 :373 (G03-4) | It is left [UNVERIFIED] whether shadow `cluster_agreement` 1.000 is the default branch. `jq` over 14 shadow `clusters.json` files: 11 runs have 0 blocking clusters (1.0 by default, `cluster.py:407-408`), shadow02 and shadow04 are null (only blocking cluster is chained), and shadow09 is 0.9328 (3 blocking clusters). | Synthesis: state that E1 has exactly one real calibrated agreement value (shadow09), and that F-18 "1.000 everywhere" carries no signal. |
| 4 | MINOR | 05 :393 (G05-3) | SKILL.md:1260 "debate is weighted by calibrated confidence" is left [UNVERIFIED]. Grep of `src/superclaude/skills/sc-adversarial-protocol/` for `calibrat` finds only `SKILL.md:1513` and `:1523` (the debate's own winner-confidence output). No input-card calibrated weighting was found, and partition-2 files do not cover it. | Synthesis must not list "calibration-weighted debate" as existing value. Tag it as probably [CODE-CONTRADICTED] in the conflict log unless file 07 shows otherwise. |
| 5 | MINOR | 04 :294 (G04-6), 06 :260 (G06-6) | Two dispatch-feasibility unknowns: `--forward-subagent-text` for observed identity, and `claude -p --allowedTools` under bypass. | Carry both as Open Questions next to the identity and read-only recommendations. |
| 6 | MINOR | 02 :6 | The header date and the "re-read 2026-11-14" notes do not match the file mtime (2026-11-13 17:44 UTC). | Cosmetic. Use the date of the run. |

## Actions Taken
None. fix_authorization was false. No research file was modified.

## Recommendations
- Green light for synthesis on partition 1 from the gap-detection lens.
- When compiling `gaps-and-questions.md`, use the ratings in this report and apply Issues 2-5 so that resolved [UNVERIFIED] items are not carried as open, and G05-3 is not carried as value.
- The gate verdict still needs the merge with partition 2 and the analyst reports. The analyst reports were header-only stubs when this review ran.

## Confidence Gate
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 0 | Glob: 0 | Bash: 11 (code and data spot-checks: sed on cluster/findings_v2/card_convert/verify_cmd/cluster_cmd, jq over shadow clusters.json, git show of COMBO-REPORT:291/:373, grep of sc-adversarial-protocol, stat and transcript grep for item 10). No web research was performed.
- Unchecked items: none. Items 2-4 are outside the lens. No defect was met under them during the reads, beyond the cross-file notes above.

## QA Complete
