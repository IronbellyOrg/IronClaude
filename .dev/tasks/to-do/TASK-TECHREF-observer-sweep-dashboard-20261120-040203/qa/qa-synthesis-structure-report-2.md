# QA Report - Synthesis Gate (Structure and Content-Quality Lens), Partition B

**Topic:** Observer, sweep and dashboard family technical reference
**Date:** 2026-11-20
**Phase:** synthesis-gate
**Fix cycle:** N/A (first review; fix_authorization false)
**Partition:** 2 (B) - synth-05, synth-06, synth-07
**Status:** Complete

[PARTITION NOTE: Cross-file checks limited to assigned subset.]

---

## Working Notes (verification log, appended incrementally)

Read in full: template (708 L), synth-05 (224 L), synth-06 (255 L), synth-07 (369 L). Snapshot reads (origin/master 61ac2c2e6 export) so far, all matching the synth text unless listed under Findings:
- Line counts: AWR scripts sum 5,777 (SKILL.md 194, 5,971 total), run.py 887, common.py 507, test file 4,005 L and 142 `def test_`; observer 13 top-level .py = 6,011 L; schema 158 L; adapter 512, collector 361, commands 524, probes 1,477, parse 835; tests/observe 36 entries, 26 test files; 19 observer JSON fixtures (10 variants, 8 golden, question-cap-100).
- Signatures and cites confirmed: `classify.py` unpack 42-51, `_classification` 130-143, `RULES` 345-355, `classify` 369, `classify_all` 880; `report.py` 26-27, 54-68, 608, 613; `probes.py` 49-60 (10 templates), 1322 `collect`; `export.py` 25-47; `Collector.__init__` collector.py:135; `read_pages` adapter.py:395; `build_view` view.py:968; `render` render.py:1449; `main.py` 581-583 and 590-592; config.json 14 keys; cycle.py `_TOP_KEYS` 58 / 216; forbidden prefixes = 13; `_ORCA_CLIS` install_user_setup.py:36; gate constants commands.py:67, 70.
- AWR gate: `passed` / `page_ok` / `summary_ok` / `deliverable` / `gate` / `close_run` (run.py:219-383) match the synth text, including CC-04 (close enforces `passed()` only; `dm` enforces `deliverable`, clickup.py:619).
- Orca verb inventory re-derived by grep of probes.py, adapter.py and all AWR scripts: no verb is missing from synth-06 8.1.
- PRs via read-only `gh --repo IronbellyOrg/IronClaude`: #684 merged 2026-11-20T02:01:07Z d7d645ddd; #686 and #690 open; #503 merged 2026-11-11T19:54:57Z 9e2608b03; #673, #539, #681-#683 merged.
- Design package (checkout): 406 tracked files, render.py 130 / fixtures.py 122 / canvas.py 122, 19 tests, fixture sha256 prefix 1f17a907 equals manifest, 8 palette colours equal theme.py:59-69, `.dev/research/orca-dashboard-20261105/` has 0 tracked files, commit 495eb96d1 not an ancestor of origin/master; the 12 cited `.dev/issues/409/...` files exist on origin/master.

---

## Overall Verdict: FAIL

Three blocking findings (B-1, B-2, B-3) are open; 13 minor findings are notes. Everything else sampled held: the synth files are accurate and well cited, so the fixes are small (two false statements to reword, one budget and duplication cut).

## Items Reviewed (per file; Synthesis Gate checklist, 12 items)

Legend: PASS = verified, no blocking defect (minor notes may exist); FAIL = blocking finding open; N/A = item does not apply to the file; UNVERIFIABLE = cannot be checked inside this partition.

### synth-05-subsystem-work-report-dashboard.md (Sections 5.5, 5.6; 224 lines)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match template | PASS | `### 5.5`, `### 5.6` carry Purpose, Key Files, How It Works, Public Interface, Dependencies, Consumers, Conventions (template 5.1 order). Minor M-9: 5.6 puts Dependencies and Consumers in one bold paragraph and Public Interface after "Overlaps". |
| 2 | Table columns per template | PASS | Key Files (File / Purpose), Dependencies (Depends On / Type / Description), Consumers (Used By / How) match template 5.1. |
| 3 | No fabrication (sampled) | PASS | About 30 claims traced to code or files: script line totals 5,777 / 5,971 (wc), run.py 887, common.py 507, test file 4,005 L and 142 `def test_`, gate chain `passed`/`page_ok`/`summary_ok`/`deliverable` (run.py:219-368), `run.py close` checks only `passed()` for non-hourly runs (run.py:371-383), `move_to_closed` sets `closed_at` (run.py:483), `prefs.check_url` accepts only GitHub and ClickUp (prefs.py:18-33), design package 406 files / 130-122-122 line counts / 19 tests / fixture hash 1f17a907 equal to manifest, 8 palette colours equal canvas.py:7 vs theme.py:59-69, QA.md:9 and :36, PRs #684, #686, #690, #503, #673, #539 states and dates via `gh`. |
| 4 | Evidence citations use real paths | PASS | Every sampled path exists (snapshot Glob/ls; `.dev/issues/409/...` files via `git ls-tree origin/master`). Minor M-2, M-1. |
| 5 | Subsystem depth in budget | PASS | 5.5 is 129 lines (complex 120-200); 5.6 is 91 lines (standard 80-120). |
| 6 | Extension Guide actionability | N/A | Section 13 is in synth-07. |
| 7 | Cross-section consistency | PASS | 5.5 and 5.6 facts (entry-file contract, `orchestrator_repo`, WC-16 absence, design package to observer none) agree with synth-06 8.2 rows. Only within this partition. |
| 8 | No doc-only claims in architecture/API | PASS | Designed items are labelled "designed", "[UNVERIFIED]" or "absent" in the built-versus-designed table. |
| 9 | Stale docs surfaced | PASS | SKILL.md:14, 172, 183 and design DQ13 marked [CODE-CONTRADICTED]; C1-C6 body contradictions tabled; `rendering-rules.md:3` marked [STALE DOC]. |
| 10 | Content rules | PASS (minor notes) | No code reproduction; signatures only. Minor M-10 (statistics embedded in tables), M-11 (two long prose paragraphs: "Lock, gate, carry-forward", "Wording rule"). |
| 11 | All expected sections have content | PASS | No placeholders (Grep TBD/TODO/FIXME: only the check name "placeholders" matched). |
| 12 | No hallucinated paths | PASS | Parent dirs and files exist: `scripts/*.py` (16), `templates/` (7 files), `tests/skills/test_agent_work_report.py`, package root, `.dev/issues/409/*` on origin/master. `.dev/research/orca-dashboard-20261105/` exists locally, 0 tracked files, as the file states. |

### synth-06-integration-config-perf.md (Sections 6-11; 255 lines)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match template | PASS | 6, 7 (N/A with rationale), 8.1-8.3, 9.1-9.3, 10.1-10.3, 11.1-11.3 all present with template numbering. |
| 2 | Table columns per template | PASS (minor) | 8.2, 8.3, 9.1-9.3, 10.1-10.3, 11.2, 11.3 match. 8.1 uses Tool/Binary/Verb/Purpose/Status/Source instead of Endpoint/Method/...; this is the brief's required Orca verb inventory (research-notes.md:98), so accepted. Minor M-7 (file-format table sits in 8.2). |
| 3 | No fabrication (sampled) | PASS | About 35 claims traced: 13 forbidden prefixes and 3 templates (adapter.py:29-50), `_ORCA_CLIS` (install_user_setup.py:36), sweep `ALLOWED_ORCA` 10 templates and call sites (probes.py:49-60, 399, 1150, 1166, 1178, 1282, 1335), AWR Orca verbs (grep of all scripts), collector constants (collector.py:28-34), `STALE_SECONDS` 45 (view.py:33), exit codes 129/143 computed as `128 + signal` (keys.py:121, 125), config.json 14 keys, env vars (grep), `.gitignore:255-256`, probes.py:85-89 byte limits, commands.py:29 `MAX_SUFFIX = 99`, clickup.py:40-44, sessions.py:48-49, collect.py:267, activity.py:225, waker.py:39-42, test_probes_allowlist.py:609-619 (1+2+5+1 = 9 argv). |
| 4 | Evidence citations | PASS (minor) | All sampled cites resolve. Minor M-4, M-5. |
| 5 | Subsystem depth | N/A | No subsystems. |
| 6 | Extension Guide | N/A | Section 13 is in synth-07. |
| 7 | Cross-section consistency | PASS | 8.2 rows match 5.5/5.6 and the synth-07 touch points; 8.1 verb families agree with GF-3 (4 designed argv match a sweep template, none match the observer). Cross-partition links (Section 5.1-5.4) not checked. |
| 8 | No doc-only claims in API/Integration | PASS | Orchestrator design verbs tagged [DESIGN-ONLY] with DESIGN line numbers; WC-16 row marked "prose duty, no code [CODE-VERIFIED absence]". |
| 9 | Stale docs surfaced | PASS | Source-conflict paragraph and DC/KNOWN LIMIT labels in 10.2; full list in synth-07 14.4. |
| 10 | Content rules | PASS (minor notes) | Tables used throughout; no code reproduction. Minor M-10. |
| 11 | All expected sections have content | PASS | Sections 6 and 7 are N/A with rationale (CLI and file based tools, static renderer); 8.1 inventory covers observer, sweep, AWR and design package (no Orca call); file formats and schemas written are in 8.2. No placeholders. |
| 12 | No hallucinated paths | PASS | All sampled files exist in the snapshot. |

### synth-07-conventions-extension-debt.md (Sections 12-16, Appendix; 369 lines)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match template | PASS | 12.1-12.3, 13.1-13.2, 14.1-14.3 (+14.4-14.6 extra), 15.1-15.2, 16, Appendix present. |
| 2 | Table columns per template | PASS (minor) | 12.2, 12.3, 13.1, 13.2, 14.1, 14.3, 15.1 match. Minor M-8: 12.1 uses "Evidence" for "Example"; 14.2 uses Research label / Evidence instead of Severity / Effort to Fix (disclosed). |
| 3 | No fabrication (sampled) | FAIL | About 40 claims traced and held (rule table, unpack, signatures, gate constants, test names `test_allowed_orca_is_exactly_the_ten_templates` at test_probes_allowlist.py:370, `test_no_module_other_than_the_adapter_imports_subprocess...` test_commands.py:585, `FORBIDDEN_PREFIXES >=` floor test_adapter.py:178-192, CHANGELOG.md:170 and commands.md:619-621 wording, WC:23, 110, 287-289, `commands/sweep.md:22, 47`, register counts 40/5/35/2/52 = 134). Two false statements found: B-1, B-2. |
| 4 | Evidence citations | PASS | All sampled cites resolve; skeleton signatures match code (`_classification` classify.py:130-136, `collect` probes.py:1322, `Collector.__init__` collector.py:135-145, `read_pages` adapter.py:395-401, `render` report.py:608, `to_json` report.py:613, `build_view` view.py:968, `render` render.py:1449). |
| 5 | Subsystem depth | N/A | No Section 5 content. |
| 6 | Extension Guide actionability (Section 13) | PASS (minor) | Five scenarios A-E each have ordered steps, file:line registration points, tests and pitfalls, and a skeleton; the cited signatures and registration points match code (CLASSES unpack classify.py:42-51, RULES 345-355, `NEXT_INSPECTION` report.py:54-68, `_TEXT_FIELDS` export.py:25-45, `ALLOWED_ORCA` probes.py:49-60, run.py dispatch 868-887, REQUIRED_CHECKS 204-212). Skeletons for C and E are one line each (minor M-12). B-1 sits in scenario A pitfalls. |
| 7 | Cross-section consistency | UNVERIFIABLE | Gap-to-step mapping needs Sections 4 and 5.1-5.4 (partition A). Within the partition, 13.1 touch points agree with 8.2. |
| 8 | No doc-only claims in architecture/API | PASS | Orchestrator items labelled designed/unbuilt; WC-16 binding left UNVERIFIED. |
| 9 | Stale docs surfaced in Section 14 | PASS | 14.4 A lists SD/CC rows by subject, B lists 40 UNVERIFIED, C the open gaps; register totals verified (U 40, SD 35, CC 5, DC 2, G 52 = 134). Minor M-13. |
| 10 | Content rules compliance | FAIL | B-3: 369 lines against the brief's 160 (synth-07 line 4 admits it); partition B plus the rest total 1,644 lines against the Standard ceiling of 1,200 (phase5-synthesis-inventory.md:15 hands this to Gate 2); the same facts are restated in several sections (`orchestrator_repo` on 14 lines across the three files, WC-16 on 13, C8 "Remediation task not created" sentence on 8). |
| 11 | All expected sections have content | PASS | No placeholders; 15.2 spot-check protocol and 16 glossary populated. |
| 12 | No hallucinated paths | PASS | Sampled: `sc-closeout-protocol/scripts/settle.sh`, `refs/settle.md`, `commands/closeout.md`, `hooks/scripts/launch-level-guard.sh`, `templates/qa-report-template.md`, `docs/user-guide/cli-groups.md`, `docs/testing/v6.0.0/post-release-report.md`, all `tests/sweep/*`, `tests/observe/*`, `tests/skills/test_worker_contract.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/commands/test_sweep_command.py` exist. |

### Brief-specific checks

| Check | Result | Evidence |
|---|---|---|
| Section 8 Orca verb inventory across all tools | PASS | Re-derived from probes.py, adapter.py and a grep of every AWR script (terminal list/read/wait/send/create, worktree list/set, tab list/close/switch/create, eval, automations list/runs); no verb missing from synth-06 8.1. |
| File formats and schemas each tool writes | PASS (minor M-7) | synth-06 8.2 "File formats and schemas written" table covers observer snapshot v1, sweep Markdown and JSON v1, AWR run folder, design package. |
| No unification recommendation | PASS | Grep over the three files: only the labels "Unification touch points (facts only; no recommendation)" and "No unification between the tools is recommended or implied". Section 14.5 "Question for the owner" is worded as a fact. |
| Sections 6 and 7 N/A with rationale | PASS | synth-06 lines 9 and 32. |
| No placeholders / empty sections | PASS | Grep TBD, TODO, FIXME, lorem, template brackets: no placeholder hit. |

---

## Issues Found

### Blocking (3)

| ID | Severity | File and location | Evidence | Required fix |
|----|----------|-------------------|----------|--------------|
| B-1 | IMPORTANT | synth-07 line 71, Section 13.1 row A, Pitfalls: "A rule-name literal is tested in two places of `classify_all` (:958-961)" | `classify.py:958` tests one rule-name tuple, `cls.rule in ("idle", "person_active")`; `:960` tests `if forced:` (join and source flags), not a rule name. A grep of `"idle"` and `"person_active"` in classify.py finds only the rule definitions (310, 326, 352, 353) and line 958. The sentence was copied from GF-4 line 38, which is wrong. | Replace with the verified fact: "`classify_all` tests the rule names `idle` and `person_active` once, at `classify.py:958` (adds the `last_activity from <source>` suffix); a new rule whose evidence needs that suffix must be added to that tuple." |
| B-2 | IMPORTANT | synth-07 line 111 (13.1 touch-point row "Living-report entry-file contract": "already called by `check.py:77`, `common.py:136`, `settle.sh:1037-1042`") and line 280 (14.5: "Callers of the missing `report-entry` verb (`check.py:77`, `common.py:136`, `settle.sh:1037-1042`)") | `check.py:77` is a docstring ("its `report-entry` verb checks with it"); `common.py:136` is a comment ("`superclaude orchestrator report-entry` writes them"). Only `settle.sh:1037-1042` runs the verb (`--help` probe at :1037, call at :1042). Research 05 line 304 says "mentions"; the synth turned it into "called". This is a caller-liveness statement used to justify not raising a C8 candidate. | Reword both places: the verb is named in `check.py:77` (docstring) and `common.py:136` (comment) and is called only by `settle.sh:1037-1042`, which probes it and ends `ENTRY escalated why=surface_absent`. Keep the D10 coverage sentence for that one caller. |
| B-3 | IMPORTANT | Partition B as a whole, mainly synth-07 (369 lines, brief asked about 160, admitted at its line 4) | The tier is Standard, 800-1,200 lines (phase1-tier-selection.md). Synthesis total is 1,644 lines (`wc -l`, seven files) and `reviews/phase5-synthesis-inventory.md:15` says "Gate 2 must bring the assembled document within budget". Template rule: a document over its ceiling needs editing, and each concept is described in exactly one section. Duplication measured with Grep (matching lines, three files): `orchestrator_repo` 14, WC-16 13, D-1 / DC-02 / C8-9 17, "Remediation task not created" 8. Lines are also very long (several over 1,500 characters), so line count understates size. | Cut, do not move: (1) 14.5 table rows C8-1..C8-9 repeat 14.1 and 10.2; keep rule R-C8 plus one short row per ID (ID, label, declaring line, code evidence) and point to 14.1 for impact; (2) 13.1 "Unification touch points" table (about 18 rows) repeats 8.2 and 16; keep only rows not in 8.2; (3) drop the "Replacement wording (GF-2, verbatim)" paragraph in 14.4 (it proposes a repo doc edit; the SD-07 to SD-09 rows already carry the facts); (4) synth-05 "Wording rule" paragraph repeats 14.5; keep one sentence and a pointer; (5) synth-06 closing "Source conflicts and corrections" paragraph repeats 14.4. Aim at about 230 fewer lines across partition B (to about 620). Protect: the 8.1 verb inventory, the 14.4 contradictions list, the five 13.1 scenarios. |

### Minor (notes only; not rechecked, no fix pass required)

| ID | File and location | Note |
|----|-------------------|------|
| M-1 | synth-05 Key Files, `.dev/issues/409/` row "(origin/master; checkout copy)" | The owner records, `bmad/spec-orca-observer/*` and `visual-parity/REDESIGN-SPEC.md` exist on origin/master only; the checkout copy of `.dev/issues/409/` does not hold them (ls). Say "origin/master only". |
| M-2 | synth-05 rules table, S1 "`unavailable (no source)`, `view.py:134`" | The literal is `UNAVAILABLE` at `view.py:113`; line 134 is `UNAVAILABLE_FACTS`. |
| M-3 | synth-05 5.6 name parity "observer-only: 8 `golden-*`, `question-cap-100` (19 files)" | 19 is the observer's total fixture count (10 + 8 + 1), not the observer-only count (9). |
| M-4 | synth-06 Section 6, `Session` field list | Omits `selected_row` and `mark_wall_time` (view.py:157, 163). |
| M-5 | synth-06 9.1 | `daily_run_local` and `missed_run_dm_local` are "07:00" and "09:00" in config.json, not "07" and "09". |
| M-6 | synth-06 9.1 and synth-07 14.4 C (G-48) | "A fuller grep is needed" is answerable now: in the skill folder `clickup_email` and `clickup_user_id` appear only in config.json (both null); `clickup_user_id` is also a settings.json key (clickup.py:559-562); no config read. State the result. |
| M-7 | synth-06 | The "File formats and schemas written" table is in 8.2; the brief says 8.1. Section 8 carries it. |
| M-8 | synth-07 12.1, 14.2 | Column "Evidence" replaces "Example" (12.1); 14.2 uses Research label / Evidence instead of Severity / Effort to Fix (disclosed; if the final template-conformance gate checks column names, add the two columns with "not rated"). |
| M-9 | synth-05 5.6 | Dependencies and Consumers are one inline bold paragraph, Public Interface follows "Overlaps"; template order and tables not followed. |
| M-10 | synth-05, synth-06 | Counts and line totals repeated through tables; template says state key numbers once in Section 1. |
| M-11 | synth-05 5.5 | "Lock, gate, carry-forward" and "Wording rule" are prose paragraphs of over 1,000 characters where tables would do. |
| M-12 | synth-07 13.1 skeletons C and E | One-line skeletons (tuple, `def main(run)`); they omit the schema JSON edit (C) and the SKILL.md step row (E), which the steps do list. |
| M-13 | synth-07 14.4 A | ID column tags SD-06, SD-07, SD-21 to SD-24 as CODE-CONTRADICTED while the register and 15.1 count them as STALE DOC; the heading sentence explains it, the table does not. |

---

## Actions Taken

None. fix_authorization was false; no synthesis file was modified. Only this report was written. No source, design, GitHub or Orca write was made; `gh` calls were read-only with `--repo IronbellyOrg/IronClaude`; one `python3` call was blocked by the UV hook and not retried (replaced by `jq`).

## Recommendations

1. Send B-1, B-2 and B-3 to the serialized fix agent. B-1 and B-2 are one-sentence rewrites (verify against classify.py:958 and settle.sh:1037-1042). B-3 is a cut of duplicated text; keep the protected parts named above.
2. After B-3, the fix agent should re-count lines (`wc -l`) and keep every blocking-defect row already labelled DEFECT-CANDIDATE (C8-8, C8-9) visible in Section 14.
3. Cross-partition checks left for the merge: gap-to-step mapping (item 7 of synth-07), `5.1-5.4` consistency with 8.2 rows, and the assembled-document line total.

## Summary

- Checks (applicable, 3 files x 12 items = 36, less 4 N/A): 32 | PASS 29 (8 with minor notes) | FAIL 2 (synth-07 items 3 and 10) | UNVERIFIABLE 1 (synth-07 item 7) | N/A 4 (synth-05 item 6; synth-06 items 5 and 6; synth-07 item 5)
- Findings: blocking 3 (CRITICAL 0, IMPORTANT 3), minor 13
- Issues fixed in place: 0 (not authorized)

## Confidence Gate

- **Confidence:** Verified: 31/32 applicable checks carried out with tool evidence (29 PASS + 2 FAIL) | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% (31 / (32 - 1)); this is completeness of checking, not a pass rate.
- **Limit stated:** item 3 (no fabrication) was verified by sampling, about 105 claims across the three files (about 30 in synth-05, 35 in synth-06, 40 in synth-07), not every claim; the approximate count is from this session's call log. The other 12-item checks were applied to every table and section.
- **Tool engagement:** Read: 53 | Grep: 28 | Glob: 4 | Bash: 11 (1 blocked by the UV hook) | gh read-only calls inside Bash: 9 PRs. Read + Grep + Glob = 85, above the 31 applicable checks.
- **UNVERIFIABLE:** synth-07 item 7 (cross-section consistency with Sections 4 and 5.1-5.4, held by partition A).
- **UNCHECKED:** none.
- Not run by design (read-only brief): tests, renderer, Orca. Test results stay UNVERIFIED as the synth files say.
- Self-audit: the verdict is FAIL on three specific, reproducible statements and one budget finding; PASS items cite named reads. If I reported zero issues here, the false "called by" and "two places" statements would have gone into the final reference.

## QA Complete
