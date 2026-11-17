# Rule copies and pinning tests (read-only research, 2026-11-15)

## 1. Rule copies

All counts are live Grep/`grep -rIE` runs on 2026-11-15 against `src/superclaude` (repo root `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`). "matches" = every match, "lines" = matching lines.

### 1.1 Reconciliation: 21 files / 109 occurrences is NOT reproducible

No pattern I tried gives 21 files and 109 occurrences. Counts of the rule's own sentences:

| Pattern (case-sensitive unless noted) | files | occurrences |
|---|---|---|
| `Grade every review finding as blocking or minor` (S1, definition) | 11 | 11 |
| `Minor findings never fail a review` (S2, never-fail) | 11 | 11 |
| `at most 2 fix cycles \(3 reviews\)` (S3, loop cap) | 12 | 12 |
| `CRITICAL and IMPORTANT findings are blocking` (S5, label mapping) | 7 | 7 |
| `defines its own severity model` (S4, own-model exemption) | 1 | 1 |
| `real defect` | 12 | 12 |
| `regardless of severity` / `no severity level is exempt` / `must still be fixed` | 0 | 0 (the old wording is gone from src) |
| `follow-up candidates` (Medium wording) | 3 (`pragmatic.md`, `commands/spec-panel.md`, `rules/prompts/document_review_loop_prompts.md`) | 7 |
| `blocking or minor` | 12 (the 11 S1 files plus `cli/review/card_convert.py:7`, which is a table row describing a YAML severity word, not the rule) | 12 |

Broader or looser patterns overshoot or undershoot:

| Pattern | files | matches (lines) |
|---|---|---|
| `2 fix cycles` | 22 | 139 (120) |
| `\(3 reviews\)` | 22 | 47 |
| `not rechecked` | 19 | 27 |
| `CRITICAL / IMPORTANT / MINOR` | 10 | 14 |
| `[Ff]ix cycles?` | 25 | 154 (132) |
| `blocking` (lowercase) | 103 | 789 (635) |
| `[Mm]inor` | 68 | 445 (374) |
| `Medium` | 59 | 182 (167) |

Closest by file count: `2 fix cycles` = 22 files / 139 matches (120 lines). Restricted to the owner's 21 listed paths (the 19 paths below plus `commands/spec-panel.md` and `cli/review/card_convert.py`), the same pattern gives 19 files / 132 matches (115 lines), and `blocking finding` gives 20 files / 174 (140). None is 109.

Where the 21 comes from: `.dev/issues/draft-20261115-012634-review-gates-classify-too-many-findings/draft-notes.md:14` says the description's Components table lists 19 shared-rule/propagation paths plus `spec-panel.md` and `card_convert.py` = 21 paths (all exist), and `draft-notes.md:15,24` records the literal definition count as 11 in 11 files and the 109 as unreproduced. I could not find the method behind 109. (Unrelated: `.dev/review-severity-rule/site-sweep.md:38` has "search 2: 109 lines", but that is a 2026-11-02 fix-loop scan count at HEAD f90877be, not this rule's copy count. UNVERIFIED that it is the origin.)

Fact: of the 19 listed paths, 8 do NOT carry the S1 sentence: `agents/rf-task-builder.md` and the 7 skill entrypoints (`task`, `tech-research`, `task-builder`, `tech-reference`, `operational-guide`, `roadmap`, `readme`). The 7 skills carry fix-cycle wording (`2 fix cycles`, see 1.2). `rf-task-builder.md` has no `2 fix cycles` hit at all; it matches `fix cycle|Open Questions|blocking` on 6 lines (not itemised).

### 1.2 Files carrying the rule sentences (src/superclaude), with line numbers

Pattern used per column: S1 `Grade every review finding as blocking or minor`; S2 `Minor findings never fail a review`; S3 `at most 2 fix cycles \(3 reviews\)`; S5 `CRITICAL and IMPORTANT findings are blocking`.

| File | S1 definition | S2 never-fail | S3 loop cap | S5 label map | Other variants in the same file |
|---|---|---|---|---|---|
| `output-styles/pragmatic.md` | 225 | 226 | 227 | 229 | S4 own-model exemption 228; Medium/`follow-up candidates` 230; spec-panel scale 231 |
| `agents/rf-qa.md` | 108 | 109 | 110 | 111 | |
| `agents/rf-qa-qualitative.md` | 108 | 109 | 110 | 111 | 9 hits of "never fail a review/the review" (8 verdict blocks + S2) |
| `templates/documents/agent_template_qa.md` | 161 | 162 | 163 | 140 (and a 2nd hit) | |
| `templates/documents/skill_template.md` | 828 | 829 | 830 | 831 | |
| `templates/workflow/01_mdtm_template_generic_task.md` | 644 | 645 | 646 | 647 | |
| `templates/workflow/02_mdtm_template_complex_task.md` | 655 | 656 | 657 | 658 | |
| `rules/prompts/automated_qa_workflow_qa_prompt.md` | 11 | 12 | 13 | none | no CRITICAL/IMPORTANT/MINOR scale, so no S5 |
| `rules/prompts/doc_code_analyst_qa_prompt.md` | 27 | 28 | 29 | none | |
| `rules/prompts/documentation_expert_qa_prompt.md` | 28 | 29 | 30 | none | |
| `rules/prompts/recruiting_expert_qa_prompt.md` | 27 | 28 | 29 | none | |
| `commands/spec-panel.md` | none | `never fail a review` at 259 | 261 | none | own scale: grading rule at 259, verdict/`follow-up candidates` at 260, FR-8 at 332 |
| `rules/prompts/document_review_loop_prompts.md` | none | 2 hits of "never fail the review" | none | none | Medium/`follow-up candidates` at 31, 32, 48 (first-review brief at 32 quotes "Minor findings are notes and never fail the review") |
| `cli/review/card_convert.py` | none | none | none | none | own severity word mapping: docstring line 7 (`yaml-blocking-minor`), line 37 (`minor, medium, low, should-fix, important, nit, info, p2, p3 to MINOR and not blocking`), set at line 82, shape check at line 374 |

Totals for the four exact sentences: S1 11 + S2 11 + S3 12 + S5 7 = 41 occurrences (S4 adds 1 = 42). 11 files carry S1-S3; 13 files if `spec-panel.md` and `document_review_loop_prompts.md` are counted as variants; 14 with `card_convert.py`. Every one of these files except `card_convert.py` and the 11 S1 files is a variant, not a verbatim copy.

The fix-cycle cap family (`2 fix cycles`, 22 files / 120 lines) additionally appears in: `skills/roadmap/SKILL.md` (14), `skills/readme/SKILL.md` (19), `skills/tech-research/SKILL.md` (17), `skills/tech-reference/SKILL.md` (16), `skills/operational-guide/SKILL.md` (15), `skills/task/SKILL.md` (7), `skills/task-builder/SKILL.md` (3), `skills/prd/refs/build-request-template.md` (2), `skills/tdd/refs/build-request-template.md` (2), `core/HOW-WE-WORK.md` (1), plus the 12 files above that carry S3 (counts per file for the 11 S1-S3 files range 1 to 4). These carry the cap, not necessarily the blocking/minor definition.

`CRITICAL / IMPORTANT / MINOR` (10 files, 14 matches): skill_template 1, agent_template_qa 2, task-builder 1, 01 1, 02 1, task 1, pragmatic 1, roadmap 2, rf-qa-qualitative 2, rf-qa 2.

### 1.3 Mirrors and installed copies (identity checked with `cmp -s`, 2026-11-15)

| Location | Carries rule files? | Identical to src? |
|---|---|---|
| `plugins/superclaude/` (125 tracked files per `git ls-files plugins`) | Only `commands/spec-panel.md` and `rules/prompts/document_review_loop_prompts.md` hold any of the four sentences or `follow-up candidates`; the 11 S1-S3 files are ABSENT from the plugin (no `agents/rf-qa*.md`, no `output-styles/`, no `templates/documents|workflow`, no 4 `*_qa_prompt.md`) | `document_review_loop_prompts.md` IDENTICAL; `spec-panel.md` DIFFERS (plugin copy is an older variant: no `--unattended` section, "Sequential" vs "Native reasoning", plugin-only fallback path) |
| Project `.claude/` | `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_*`, `02_*`, `commands/sc/spec-panel.md` | all 7 IDENTICAL to src. No `output-styles/` and no `rules/` dir in project `.claude/` (ls shows agent-memory, agents, cache, commands, hooks, settings.json, skills, templates). |
| `~/.claude/` (installed) | `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, 4 `templates/...`, 4 `rules/prompts/*_qa_prompt.md`, `rules/prompts/document_review_loop_prompts.md`, `commands/sc/spec-panel.md` | all IDENTICAL to src (cmp) |

Extra installed-only items (not in this branch's src, UNVERIFIED origin, probably other branches' installs): `~/.claude/commands/sc/spec-panel-{armb,diffgate,ledger,ponytail,stoprule}.md` and `spec-panel.md.bak.20261111T164114Z` carry the cap sentence; `~/.claude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py` and `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` carry it too; `~/.claude/output-styles/pragmatic.md.bak.20261111T164114Z` carries S1-S5 and DIFFERS from src (stale backup). `~/.claude/file-history/` and `paste-cache/` also hold the sentences (transient session copies, not install targets).

Whole-tree sanity (src vs `~/.claude`): `templates/`, `rules/`, `output-styles/` have 0 src-side differences; `agents/` 2 src-side entries (src README.md and `__init__.py`, never installed); `skills/` 2 src-side differences (`__init__.py`, `sc-reflect-protocol/refs/reviewer-spec.md` differs); `commands/` vs `commands/sc/` 2 src-side differences (not itemised, UNVERIFIED which). Project `.claude/` vs src: `templates` 0 diffs, `agents` 2, `commands` 2, `skills` 14, `hooks` 23.

## 2. Prior art (.dev/review-severity-rule/inventory.md)

Read in full (215 lines). Header: dated 2026-10-31, branch `fix/review-severity-rule`, base `f90877be`; restart note 2026-11-01. The file itself does not name a PR; `git log` on `pragmatic.md` shows `80f934de5 fix(qa): minor findings never fail a review; cap review loops at 2 rounds (#343)`, then `f90aca51a ... (refs #346) (#477)` and `77e0a7029 fix(review): grade findings by consequence and add a Medium warning tier (refs #346) (#478)` (the Medium tier and spec-panel scale came after the inventory).

- Purpose: a before-edit inventory of every site of the OLD rule ("any issue of ANY severity must FAIL", "regardless of severity", "no severity level is exempt", "Zero tolerance ... must be perfect to pass") and of review-loop caps above 2. User decision (line 4): minors never fail and are not rechecked, remove any severity rule, cap review loops at 2.
- Categories (lines 8-12): (a) fails a review on a minor/cosmetic finding; (b) rechecks minors or sends them to a fix pass; (c) allows more than 2 review rounds, no cap, or passes open blocking findings at the cap.
- S1-S5 (lines 20-26) = the canonical text, all put into `pragmatic.md`: S1 blocking/minor definition; S2 minors never fail, are notes, are not rechecked; S3 loop cap "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"; S4 a protocol with its own severity model (`/sc:implement`) keeps it; S5 on a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT are blocking, grade by definition not label. Other edited files carry S1-S3 word for word, and S5 where they have such a scale (line 18).
- Section 2 (a/b sites with file:line, current text, replacement): 2.1 output style (`pragmatic.md:225`); 2.2 QA agents (`rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, plus DNSP clauses in `skills/task-builder/SKILL.md:895` and `templates/modularization-template-review/synthetic-dnsp-finding.contract:52`); 2.3 templates (`agent_template_qa.md`, MDTM 01/02, modularization templates, `skill_template.md`); 2.4 skills (shared RF prompt blocks in prd, tdd, tech-reference, tech-research, operational-guide, readme, plus gate prose in task, task-builder, roadmap-family); 2.5 four `rules/prompts/*_qa_prompt.md`.
- Section 3 (c): 3.1 at-cap "become Open Questions" rows to HALT-and-escalate (MDTM 01/02, `rf-task-builder.md`, task-builder); 3.2 cap numbers 3 to 2 (superseded 2026-11-02 by `.dev/review-severity-rule/cap-sites.md`: 138 IN sites in 38 files, including CLI defaults under `src/superclaude/cli/`); kept as-is: sc-roadmap-protocol REVISE loop, `pr-submit --max-rounds` default 2.
- Section 4 decisions: round = one fix cycle (2 cycles = 3 reviews); `/sc:implement` option A (drop the second A2 repair; edits to `refs/retry.md`, `refs/qa.md`, `refs/ledger.md` and plugin twins); `update.sh` unchanged; cli-portify convergence default to 1; `/sc:workflow` unchanged.
- Section 5: wording kept as not-a-minor-fails rule ("Zero tolerance - if you can't verify it, it fails", fabrication rules, "EXACT means EXACT", `/sc:pr-submit` Low/Nit report-only).
- Section 6 (lines 203-213): tests that pinned the old wording (`test_implement_severity_static.py`, `test_nfr_conv_9_zero_trust.py`, `test_dnsp_all_agents_fail_bypass.py`, `test_task_builder_merge.py`, `test_implement_severity_replay.py`, `test_task_workspace_lifecycle.py`); and a new test `tests/skills/test_review_severity_rule.py` (line 215) asserting S1-S5 in `pragmatic.md`, S1-S3 in each edited QA agent/template/prompt, S5 where a CRITICAL/IMPORTANT/MINOR scale exists, src/plugin twin equality.
- Application: it is a plan (replacement-text table). The older package `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261031-235404` is "superseded ... unexecuted" (line 5); `.dev/tasks/done/TASK-WF-removeTheAnyIssu-20261102-053741` is the one now in `done/` (that this package applied it is inferred from the directory name and site-sweep.md:4, UNVERIFIED by reading the package). The live src now shows the result: the old wording has 0 hits (`regardless of severity`, `no severity level is exempt`, `must still be fixed`), and S1-S3 sit in exactly the 11 files the inventory named for them (2.1, 2.2 rf-qa pair, 2.3 templates, 2.5 four prompts).

How it differs from my Grep list (section 1):
- It lists OLD wording sites to rewrite (hundreds of lines in about 38+ files); my list is the NEW sentences now present (11 files for S1-S3, 7 for S5). Overlap: the 11 S1-S3 files match its section-1 plan exactly.
- It does not list `commands/spec-panel.md` (its own CRITICAL/MAJOR/MINOR scale, `follow-up candidates`, review cap at line 261), `rules/prompts/document_review_loop_prompts.md`, or the Medium wording at `pragmatic.md:230-231`; those came later (the file ends before them). It treats `cli/review/card_convert.py` as out of scope; it was not in its list.
- It scheduled edits in 7 skill entrypoints (task, task-builder, roadmap, readme, tech-reference, tech-research, operational-guide) but gave them local replacement wording, not S1-S3; my Grep confirms they do not carry S1 (they carry `2 fix cycles` and `blocking finding` wording only).
- Its cap table (cap-sites.md, 138 sites) is wider than the 12-file S3 list: the cap family is 22 files on `2 fix cycles`.

## 3. Tests that pin rule text

Grep of `tests/` (skipping `__pycache__`) for the rule sentences found 5 files; widening to the verdict bullets, mirrors and hashes gives 8 test modules plus 2 YAML fixtures that pin rule text. All paths under `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/`.

### 3.1 The three "known candidates" named in the request

- `tests/pr_submit/test_finding_verify.py` does NOT pin rule text. Docstring lines 1-10: verify-before-remediate FSM tests (verified finding goes on, false positive recorded `REPORT_ONLY`, no round consumed); it imports `superclaude.pr_submit.fsm` and `models` (lines 14-15). The only severity-like word is the test body `"real defect"` (line 22). Breaks only if the Python FSM changes, not if rule prose changes.
- `tests/pr_submit/test_marker_malformed.py` does NOT pin rule text. Docstring lines 1-16: Augment review status-marker parsing, rule "written once in `refs/detection-contract.md`" (line 10). Not tied to the blocking/minor rule.
- `tests/skills/test_review_severity_mapping.py` DOES pin it (3.2 item 2).
- Related pr_submit test: `tests/pr_submit/test_severity_router.py` pins the Python severity router (Critical/High/Medium/Low, "T-310 Medium routes `--fix` ONLY", "T-312 Low is report-only", lines 1-8, 46-67) and cites `severity-rubric.md:104-152`. That is `/sc:pr-submit`'s own scale (code in `superclaude.pr_submit`), unaffected by prose changes to the review rule.

### 3.2 Tests that DO pin rule text

1. `tests/skills/test_review_severity_rule.py` (520 lines, STATIC, scans `git ls-files` of `src plugins commands agents skills`, line 28).
   - Pins S1-S5 as the five bullets that follow the binary-verdict bullet of `pragmatic.md`: `BINARY_VERDICT_BULLET` line 66-68 `"- Every review agent MUST produce a binary verdict: PASS or FAIL."`; openings `S_OPENINGS` lines 69-75 (`"- Grade every review finding as blocking or minor."`, `"- Minor findings never fail a review:"`, `"- A review loop (review, fix, re-review) runs at most 2 fix cycles"`, `"- A protocol that defines its own severity model,"`, `"- On a CRITICAL / IMPORTANT / MINOR scale,"`); `canonical_rule_bullets()` lines 78-96 takes exactly `lines[start+1:start+6]` and asserts each opening.
   - `S1_S3_FILES` lines 181-192 (10 files: rf-qa, rf-qa-qualitative, agent_template_qa, skill_template, MDTM 01, 02, 4 `rules/prompts/*_qa_prompt.md`) must contain the S1, S2, S3 bodies verbatim after whitespace flattening (`test_c_s1_s3_copied_verbatim`, 196-203); `S5_FILES = S1_S3_FILES[:6]` (line 193) must contain S5. `pragmatic.md` itself is not in the list (it is the source). No `(S1)`-style labels or "contains the canonical cap text" allowed (206-210).
   - `CANONICAL_CAP_TEXT` line 215 `"at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"` must be in `pragmatic.md` and in S3 (228-230); `AT_CAP_CLAUSES` 216-219.
   - `BANNED_SEVERITY_PHRASES` lines 112-125 (e.g. `any issue of any severity`, `regardless of severity`, `no severity level is exempt`, `must still be fixed`, `ALL findings must be resolved`, `CRITICAL, IMPORTANT, and MINOR issues`) must not appear in `src`, `plugins`, `commands`, `agents` (172-176).
   - Edit-table pins: `test_e_every_cap_edits_row_holds` asserts 161 rows (line 263) and `test_j_every_sweep_edits_row_holds` 139 rows (line 270) from `fixtures/review_severity_cap_edits.yaml` (1398 lines) and `fixtures/review_severity_sweep_edits.yaml`; for each row `old` must be absent and `new` present in `row["file"]` (252-258). Byte-copy check against `.dev/review-severity-rule/{cap,sweep}-edits.yaml` is skipped if absent (275-283).
   - Also: no cap of 3 to 9 fix cycles in `src`/`plugins` outside sc-implement-protocol (`CAP_REGRESSION` 288-293, allowlist 295-304); shared suffixes kept (`"Only PASS or FAIL — no conditional pass."` line 344, readme `"List each with specific remediation."`); sc-implement-protocol plugin twins byte-equal (371-385); sweep phrases and fix-loop patterns F1-F6 (390-406, 448-464); `zero[- ]tolerance` only with a qualifier (469-521).
   - Would break if the rule text changed: reword or move any of S1-S5 in `pragmatic.md` (breaks all `test_c_*`, `test_d_*`, and every importer of `canonical_rule_bullets`); change S1-S3 or S5 in any of the 10 files without updating them identically; reword any of the 161 + 139 edit-table `new` strings (tracked in the two fixtures); reintroduce a banned phrase; add a fix-cycle cap of 3 or more. Replacing S1-S5 in `pragmatic.md` with a pointer to a new core doc breaks `canonical_rule_bullets()` immediately (assert at lines 89-95).
2. `tests/skills/test_review_severity_mapping.py` (145 lines, STATIC). Parametrized over `commands/spec-panel.md` in `src` and `plugins` (`SPEC_PANELS` lines 24-27).
   - Review Loop bullet 2 literals (lines 53-62): `"grade by consequence, not by label"`, `"CRITICAL is blocking"`, `"a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome"`, `"security, data-loss or safety-boundary risk"`, `"otherwise it is Medium (a warning listed under `follow-up candidates`)"`, `"MINOR is a note"`, `"never appear in the Reviser brief"`.
   - Bullet 3 (69-76): `"minor notes and Medium warnings allowed"`, `"`follow-up candidates`"`, `"asks the user once per loop"`, `"creates none without the user's answer"`, `"an `--unattended` run only records the list"`; bullet 6 `"listing only blocking finding ids"` (81); boundary table `"one row per input class that applies to the guard"`, `"the six classes below are the menu, not a quota"` (89-92); FR-8 `"It is blocking when it names a concrete wrong outcome"` / `"otherwise it is Medium"` (99-103); FR-10 `"This is a hard gate, not advisory."` (110).
   - `pragmatic.md` (117-145): the line right after S5 must start `"- Among minor findings, one that describes a real but non-blocking weakness"` and contain `"is Medium"`, `"never fails a review"`, `"never appears in a reviser brief"`, `"asks the user once per loop whether to open an issue"`, `"no issue is created without the user's answer"`, `"only records the list"`; the line after must start `"- On `/sc:spec-panel`'s CRITICAL / MAJOR / MINOR scale"` and contain `"MAJOR is blocking only when it names a concrete wrong outcome"` and `"a reviewer never suppresses such a finding because its label says Medium or minor"`; and the whole style text must contain `"a finding of any label whose consequence is a security, data-loss or safety-boundary risk is blocking"` (140-145).
   - Would break if: the Medium/spec-panel bullets move away from directly after S5, any of those literals are reworded (in src OR the plugin copy of spec-panel), or S5 is moved (uses `canonical_rule_bullets()[4]` and `lines.index(s5)`, lines 119-120).
3. `tests/skills/test_implement_severity_static.py` (628 lines): only `test_p1_output_style_exempts_implement_severity_model` (lines 485-498) pins `pragmatic.md`: S2 must equal the exact string `"- Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL."` and S4 the exact `/sc:implement` exemption bullet (494-498). It imports `canonical_rule_bullets` (line 12). Any rewording of S2 or S4 breaks it. The rest of the file pins `/sc:implement`'s own severity model (refs/qa.md, refs/retry.md), which stays separate.
4. `tests/skills/test_review_loop_extension.py` line 76: `assert "at most 2 fix cycles (3 reviews)" in cap` for spec-panel Review Loop bullet 4, parametrized over src and plugin spec-panel (lines 18-22). Also bullet pins at 40-85 (hash header, fail-closed verdict, no edits between fix 2 and review 3). Breaks if the cap bullet wording changes.
5. `tests/skills/test_review_prompt_overrides.py` (283 lines): brief lint (35-58) and `test_shipped_briefs_pass_the_lint_and_carry_the_roles` (110-131) over `rules/prompts/document_review_loop_prompts.md` quoted briefs: `"review 1 of 3"`, `"never fail the review"` (124), `"not a minimum number of findings"` (125), `"do not start another review"`, `"Prefer deleting or narrowing"`, etc.; `pragmatic.md` literals (238-253: `"A zero-finding result is valid."`, `"MUST state what it checked"`, `"Never invent a finding to avoid a zero"`, `"never to meet a quota"`); rf-qa, rf-qa-qualitative, agent_template_qa must carry `"**Independent stance**"`, `"there is no minimum count"`, `"do not invent findings to avoid a zero"` (256-268); 5 skill/template files need `"no minimum count"` (271-283). Removing these sentences (e.g., when consolidating into a core doc) breaks it. It does not pin S1-S5 wording itself.
6. `tests/audit/test_nfr_conv_9_zero_trust.py`: `PASS_BULLET` (lines 80-83) `"- **PASS** — No CRITICAL or IMPORTANT gaps; any MINOR gaps are listed as notes. Green light for synthesis."` and `FAIL_BULLET` (84-88) `"- **FAIL** — Any CRITICAL or IMPORTANT gap exists. List each with a specific remediation action. All blocking gaps must be resolved before proceeding; MINOR gaps never fail the gate."` must be byte-present in `src/superclaude/agents/rf-qa.md` AND the mirror `.claude/agents/rf-qa.md` (lines 60-61); also a scorer where CRITICAL/IMPORTANT fail and MINOR passes (92-120). Fixtures: `tests/audit/fixtures/nfr_conv_9/*.md` (not read; UNVERIFIED). Breaks if those two rf-qa bullets are reworded.
7. `tests/audit/test_severity_floor_unweakened.py`: SHA-256 `BASELINE_BLOCK_SHA` (line 54, `be18e2cf...46b1b`) of rf-qa-qualitative's `## Critical Rules` block through Rule 11, for `src` and the `.claude/agents` mirror (39-40); its comment 49-53 says Rule 10 now reads "Maximum 2 fix cycles ... with the open blocking findings. All blocking findings must be resolved; minor findings are recorded as notes." Rule 6 text must stay verbatim (57-61) and have no softening tokens such as "may be minor" (195-221). Any edit to any line of that Critical Rules block changes the hash and breaks it (it needs re-pinning); Rule 6 must never be softened.
8. `tests/audit/test_dnsp_all_agents_fail_bypass.py` (only if those lines change): sha256 pin of `rf-team-lead.md` Fix Cycles rule line (`max 2 cycles per phase`, `max-2-cycles` token) at every site that cites it (lines 14, 32-34, 79-81, 330-336), with fixture `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` (UNVERIFIED: which src files hold the token now; grep limited to 12 lines).
9. `tests/review/test_review_rules_text.py` (93 lines): pins `src/superclaude/rules/prompts/document_review_loop_prompts.md` structure: each insertion exactly once (lines 28-31), order `### Findings block` < `### Fix map` < `### Review panel` < `## Never` (45-62), the findings-v1 contract tokens (65-73), older pins and `assert "src/superclaude" not in TEXT` (76-92). This is the existing shared review-loop doc and its precedent for a shared review document; a new doc must not be folded into it without keeping those pins.
10. Not rule-text pins but related: `tests/review/test_review_card_convert.py` (card_convert word mapping, `yaml-blocking-minor` shape, line 143; `{f["blocking"]...}` line 157); `tests/skills/test_spec_panel_review_loop.py:113-114` ("may not grade a minor finding as blocking"); `tests/skills/test_review_brief_placement.py:58`; `tests/skills/test_worker_contract.py:777,1726,1861` (unresolved High or Medium HALT, open blocking findings). Install tests `tests/unit/test_cli_install.py:163-165`, `tests/cli/test_install_user_setup.py:852`, `tests/cli/test_install_keep.py:23-27` check that `output-styles/pragmatic.md` is an installed resource (see section 4).

Number of test modules that pin rule or Medium/severity text: 8 (items 1-8), plus 2 YAML fixtures (`tests/skills/fixtures/review_severity_cap_edits.yaml`, `review_severity_sweep_edits.yaml`) and `tests/skills/fixtures/review_brief_t07_original.txt`/`t09_original.txt` (kept as flagged negatives). The two pr_submit tests named in the request are not among them.

## 4. Sync and install mechanics

Item 9 in section 3 pins the structure of the shared review-loop prompt file rather than the rule wording, so the count of rule-text-pinning modules stays 8.

### 4.1 `make sync-dev` / `make verify-sync` (`Makefile`)

- `sync-dev` (lines 108-163) copies from `src/superclaude/` into the project `.claude/`: skills (dirs with `SKILL.md`, lines 112-125), agents `*.md` except README (126-130), commands `*.md` to `.claude/commands/sc/` (131-136), hooks `scripts/*.sh|*.js` plus `scripts/session-init.sh` (137-147), and `templates/` recursively (148-157). It does NOT copy `core/`, `rules/` or `output-styles/` (consistent with the `ls` of project `.claude/`: no `rules`, no `output-styles`, no core docs).
- `verify-sync` (lines 165-onward) diffs the same five classes (skills 170-200, agents 202-226, commands 228-252, hooks 254-278, templates 280-305), then an "Installer Registration" check of hook scripts against `_FRESHNESS_SCRIPTS` (307-317). Nothing is verified for core, rules or output-styles.
- Consequence for a new shared doc: if it lives under `src/superclaude/core/`, `rules/` or `output-styles/` no `.claude/` mirror exists and none is checked; if it lives under `templates/`, `skills/<name>/refs/`, `agents/` or `commands/` it is mirrored by `make sync-dev` and must pass `make verify-sync`. Mirrors under `.claude/` are gitignored and never staged (project CLAUDE.md rule).

### 4.2 `make build-plugin` / `sync-plugin-repo` (`Makefile` 65-87, `scripts/build_superclaude_plugin.py`)

- `plugins/superclaude/` is a hand-maintained tracked tree (125 files by `git ls-files`: `agents` 22, `commands` 28, `core` 7, `hooks` 16, `rules` 1, `skills` 22, `templates` 6, `modes` 8, `mcp` 9, ...). The build does not regenerate it from `src/`: `build_superclaude_plugin.py:16` sets `PLUGIN_SRC = plugins/superclaude`, and lines 74-77 copy only `agents`, `commands`, `hooks`, `rules`, `scripts`, `skills` to `dist/plugins/superclaude`, plus manifests. `core/`, `templates/`, `output-styles/` are not in the dist build. `sync-plugin-repo` rsyncs agents, commands, hooks, scripts, skills and `.claude-plugin` (lines 81-86), not `rules` (it syncs fewer folders than the build copies).
- The plugin copy is kept in step by hand and by parity tests. Examples: `HOW-WE-WORK.md` is copied byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (project CLAUDE.md; test `tests/commands/test_routing_plugin_parity.py:38`); `rules/prompts/document_review_loop_prompts.md` exists in both trees and is IDENTICAL (section 1.3), with the spec-panel plugin copy naming a fallback `${CLAUDE_PLUGIN_ROOT}/rules/prompts/document_review_loop_prompts.md` (plugins/superclaude/commands/spec-panel.md:266), and `scripts/build_superclaude_plugin.py:74-75` comments that `rules/` was added to the build for exactly that case.
- The 11 S1-S3 files are NOT in the plugin today (section 1.3), so a plugin-only install does not get the rule through them; only `spec-panel.md` (variant) and the review-loop prompts reach plugin users.

### 4.3 `superclaude install` (`src/superclaude/cli/main.py:178-236`, update path 365-404)

`install` calls, in order: `install_core_files` (178), `install_commands` (188), `install_agents` (196), `install_hooks` (217), `install_templates` (227), `install_user_setup` (236); `install_all_skills` is imported at line 78; the update path repeats them with `force=True` (365-404).

| Source dir | Destination | Mechanism | Citation |
|---|---|---|---|
| `src/superclaude/core/*.md` | `~/.claude/<FILE>.md` | `core_source.glob("*.md")`; copy unless the file exists and not `--force` | `install_core.py:58-76` |
| `src/superclaude/commands/*.md` | `~/.claude/commands/sc/` | `install_commands` (`_EXCLUDE_FILES` skips README) | `tests/unit/test_cli_install.py:972-979` (not re-read in the installer) |
| `src/superclaude/agents/*.md` | `~/.claude/agents/` | `install_agents` | `main.py:196` |
| `src/superclaude/skills/*/` | `~/.claude/skills/` | `install_all_skills` | `main.py:78` |
| `src/superclaude/templates/**` | `~/.claude/templates/` | `rglob("*")`, files only, skips `__pycache__` and protected subdirs | `install_templates.py:44-67` |
| `src/superclaude/rules/**` | `~/.claude/rules/<group>/...` | `_copy_tree` with `rglob("*")`; then adds `claudeMdExcludes` for the three groups so Claude Code never auto-loads them | `install_user_setup.py:68-109, 153-183` |
| `src/superclaude/output-styles/**` | `~/.claude/output-styles/` | same `_copy_tree` | `install_user_setup.py:186-201` |

Behaviour that matters for a change to the rule text: an existing destination file is KEPT without `--force` and reported as stale (`install_core.py:70-72, 96-105`; `install_user_setup.py:88-92`); with `--force` or `superclaude update` a differing file is saved aside as `<name>.bak.<time>` first (`install_user_setup.py:94-97, 118-119`). That explains the stale `pragmatic.md.bak.20261111T164114Z` seen under `~/.claude/output-styles/`.

### 4.4 What a NEW shared core document needs

- `src/superclaude/core/REVIEW-SEVERITY.md` (or any `core/*.md`) is installed to `~/.claude/REVIEW-SEVERITY.md` with NO code change, because `install_core_files` globs `core/*.md` (`install_core.py:58`), on a fresh install and on `update`. On an existing install without `--force`, a NEW name does not exist at the destination, so it is copied (line 70 only skips existing files); edits to an existing core file need `--force`/`update` to reach `~/.claude`.
- Optional (not required for install): add the name to `KNOWN_CORE_FILES` (`install_core.py:14-29`); it only filters `list_installed_core_files` (line 177). Today `ISSUE-BACKLOG.md`/`ISSUE-HANDOFF.md`/`WORKER-CONTRACT.md` are in it; the test `tests/cli/test_bash_inspection_policy.py:38-44` shows the pattern (install, then `list_installed_core_files()` contains the file).
- The baseline-resource test `tests/unit/test_cli_install.py:123-128` lists 10 core names and checks presence only (`_assert_present`, lines 502-506: every listed name must exist; extra files are fine), so an extra core file does not break it (it is already out of date: it lacks ISSUE-BACKLOG, ISSUE-HANDOFF and WORKER-CONTRACT).
- Packaging: hatch `include = ["src/**", "plugins/**"]` with `force-include` of both trees (`pyproject.toml:78-87`), so new files under `src/superclaude/core/` ship in the wheel automatically (the installer's wheel lookup prefers `core/` in the package, `install_core.py:139-147`).
- Not mirrored automatically: `.claude/` (sync-dev ignores `core/`) and `plugins/superclaude/` (hand-maintained; its `core/` has 7 tracked files and lacks 6 of src's 12 core `.md` files: BASH_INSPECTION_POLICY, CLAUDE, HOW-WE-WORK, ISSUE-BACKLOG, ISSUE-HANDOFF, WORKER-CONTRACT). A new core doc is therefore invisible to plugin-only installs unless it is also placed in `plugins/superclaude/` (for reading by commands, the working precedent is `rules/prompts/`, which `build_superclaude_plugin.py:76` ships and a test pins) and given a parity test. Consumers must name both surfaces (`~/.claude/<FILE>.md` and `${CLAUDE_PLUGIN_ROOT}/...`), as spec-panel.md does; never `src/superclaude/...`.
- A new file under `rules/` inside an existing group (`core`, `contextual`, `prompts`) is installed with no code change; a new top-level group would also need `_RULE_GROUPS` (`install_user_setup.py:34`) so it is added to `claudeMdExcludes`.
- Existing tests that list or inspect installed names would still pass, but a new test is advisable to pin the doc's text, mirroring `test_review_severity_rule.py`.
- Conclusion: yes, a new shared core document can be installed to `~/.claude/<FILE>.md` without any installer code change. Reaching plugin users, `.claude/` dev mirrors and pinning tests takes extra manual files, not code changes to the installer.

### 4.5 Tests enforcing "no `src/superclaude/` path in installed primitives"

There is no single global scan test. Enforcement is the manual grep named in the project CLAUDE.md plus per-site tests:
- `tests/skills/test_primitive_dual_surface_lookup.py` (63 lines): pins that the adversarial prerequisite checks in 4 files (`_ADV_SITES` lines 16-21) name BOTH `~/.claude/skills/sc-adversarial-protocol/SKILL.md` and the project `.claude/...` copy (lines 28-35); the brainstorm persona check names both agent surfaces (38-47); and `task-builder/SKILL.md`'s `1. **Locate \`rf-qa.md\`.**` line names the project copy before `~/.claude/agents/rf-qa.md` (50-62). It does not scan for `src/superclaude` strings itself (its docstring only recounts PR #278).
- Per-file absence asserts (`"src/superclaude" not in ...`): `tests/review/test_review_rules_text.py:92` (the review-loop prompts file), `tests/skills/test_review_brief_placement.py:68,103`, `tests/skills/test_spec_panel_review_loop.py:159` (spec-panel section), `tests/skills/test_worker_contract.py:925`, `tests/skills/test_task_workspace_lifecycle.py:317`, `tests/core/test_codegraph_guide.py:116` ("installed guide must not name a src/ path"), `tests/pr_submit/test_merge_guard_protocol.py:89,534,753`, `tests/pr_submit/test_conflict_sync_protocol.py:714`.
- So a new core/rules doc added to the install set is covered by such a check only if its own test adds one; the new doc should include `assert "src/superclaude" not in text` in its pin test.

UNVERIFIED: `install_commands.py` / `install_agents.py` / `install_skills.py` internals were not read (destinations taken from `main.py` call order and `tests/unit/test_cli_install.py`); `scripts/` plugin-parity tests other than `test_routing_plugin_parity.py` were not enumerated.
