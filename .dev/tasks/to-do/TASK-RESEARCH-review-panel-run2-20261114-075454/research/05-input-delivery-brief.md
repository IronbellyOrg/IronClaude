# Research: Input delivery and reviewer brief (what a shared Review Panel core must expose per module)
**Investigation type:** Code Tracer
**Scope:** scope slices 03, 05, 06, 01, 09, 10; `src/superclaude/rules/prompts/document_review_loop_prompts.md`; `src/superclaude/commands/spec-panel.md`; reviewer-spec brief; `src/superclaude/cli/tasklist/`; `src/superclaude/cli/review/panel.py` and `findings.py`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md`; `src/superclaude/cli/reflect/`; E2 branch tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` (git show only)
**Status:** Complete
**Date:** 2026-11-14
---

Citation form: `HEAD:<path>:<line>` = this worktree (branch `ironbelly/shadow-runs`, commit `50d4d2b9d`); `E2@6c09843:<path>:<line>` = `git show 6c0984326cbb8fb06c4a36065de58b171d3f8175:<path>`. "Slice NN" = `${TASK_DIR}research/scope/NN-*.md`. Tags: [CODE-VERIFIED] confirmed at a cited line in code or in the shipped prompt text; [CODE-CONTRADICTED]; [UNVERIFIED]; [SLICE-ONLY] = taken from a slice and not re-derived (treated as [UNVERIFIED]).

## Unit 1. The shipped review-loop brief `document_review_loop_prompts.md` (HEAD, 74 lines)

File: `HEAD:src/superclaude/rules/prompts/document_review_loop_prompts.md` (74 lines, read in full).

- `:3` scope sentence: prompts for a coordinator that briefs a reviewer/reviser in a document review loop (`/sc:spec-panel --mode critique`); hard gate: spec-panel makes reading it mandatory. [CODE-VERIFIED]
- `:15-21` "Values to fill": exactly five placeholders: `{{CANDIDATE}}` (`:17`), `{{BASELINE}}` (`:18`), `{{PRIOR}}` (`:19`), `{{N}}` (`:20`), `{{IDS}}` (`:21`). There is NO `{{SOURCE}}`, `{{DRIVING_DOC}}`, `{{PLAN}}` or any placeholder for an input document other than the candidate. [CODE-VERIFIED by reading `:15-21`. Negative evidence: a case-insensitive Grep of the file for `source|driving|plan|spec\b` matches only `:3` (the command name) and `:48` (the baseline "spec as it was before the revision"); the words "source" and "driving" occur nowhere]
- `:31` Grading check (rubric): sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y."; blocking needs "two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass"; "Grade it Medium when ... the finding is a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case)"; "A Medium finding goes under follow-up candidates even when its label is MAJOR." [CODE-VERIFIED `:31`]
- `:32` First-review brief (single sentence, quoted): "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. ... If an input is missing or unreadable, return incomplete. ..." The phrase "against the requirements it states" scopes the review to the candidate itself; "an input" is not defined. [CODE-VERIFIED `:32`]
- `:48` Re-review brief: names candidate, baseline, prior report; same "If an input is missing or unreadable, return incomplete" sentence. [CODE-VERIFIED `:48`]
- `:53` Revise brief names `{{IDS}}` and `{{CANDIDATE}}` only. [CODE-VERIFIED]
- `:56-60` Findings block: fence info string `findings-v1`, JSON lines; category list at `:60` = `contradiction, unpassable-check, data-loss, safety, missing-requirement, other`; `anchor` "12 to 200 characters copied exactly"; `refs` "lists the requirement ids and section numbers" (no cap stated); `claim` "one sentence" (no 300 cap stated); no mention of the `id` pattern or "MINOR cannot be blocking". [CODE-VERIFIED `:60`, compared with `findings.py:90-121` in Unit 3]
- `:62` "The verdict line stays the reviewer's verdict." (reviewers are not told that one blocking row from any reviewer fails the merged round, B-7). [CODE-VERIFIED `:62`]
- `:68-70` Review panel paragraph: `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>`; reviewers get "the same brief, none seeing another's report or transcript"; `superclaude review merge`; `superclaude review ledger revise ...`. Input delivery here = the coordinator writes the same brief text per reviewer; the file path is the `@file` named in the brief. [CODE-VERIFIED `:70`]
- `:74` Never-clause: a brief "may narrow the command's scope but may not widen it". [CODE-VERIFIED]

Key Takeaways (Unit 1):
- The shipped brief is a prose template with five coordinator-filled placeholders; all five name documents of the candidate's own revision chain (candidate, baseline, prior report) or finding ids. No role exists for a second, driving document (plan -> source, tasklist -> spec).
- The grading rule is welded into the brief at `:31` (the Medium rule and the "requirement the document never states" demotion). A core that serves tasklist reviews inherits that demotion unless the grading paragraph becomes a per-module block.
- The category list, the 12-200 anchor limit and the verdict sentence are duplicated here and in `findings.py`; only the anchor limit is stated with its number in the prompt (B-2).

## Unit 2. The parser side of the contract: `findings.py` (v1) and `findings_v2.py` (HEAD)

File: `HEAD:src/superclaude/cli/review/findings.py` (457 lines per Read; slice 09 says 457 [CODE-VERIFIED: last numbered line 457]).

- `findings.py:14-24` constants: `SEVERITIES = (CRITICAL, MAJOR, MINOR)`; `CATEGORIES = (contradiction, unpassable-check, data-loss, safety, missing-requirement, other)` (`:15-22`); `PRIOR_STATUSES`, `ACTIONS`. [CODE-VERIFIED]
- `:26` `_ID = ^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` (id <= 16 chars). `:29` `_REF_TOKEN = \b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b`; `:30` `_SECTION_REF = ^\d+(?:\.\d+)*$`; `:31` `_HEAD_FINDINGS = ^#{1,6}\s+Findings block\s*$` (case-insensitive, any heading level, exact words "Findings block"); `:32` `_HEAD_FIXMAP`. [CODE-VERIFIED]
- `:90-121` `_check_finding`: id pattern and uniqueness (`:92-95`), severity (`:96`), blocking bool (`:98`), MINOR cannot be blocking (`:100-101`), category membership (`:102`), anchor 12-200 after whitespace flattening (`:104`, via `_check_flat` `:79-87`), optional anchor2 12-200 (`:107-110`), refs list of <= 8 strings (`:111-117`), claim <= 300 (`:118`). Unknown keys are NOT rejected. [CODE-VERIFIED]
- `:124-196` `parse_block`: heading missing -> `ok=False` (`:128-133`); no fenced `findings-v1` block (`:134-142`); more than one block -> `ok=False`, last used (`:143-150`); unclosed fence -> truncated (`:151-158`); each bad line is an error and is skipped (`:160-195`). So an over-length anchor/claim line is dropped from `findings` with an error, which is the D1 silent-drop at the parser level; the merge consequence is a separate unit (slice 09, not re-derived here). [CODE-VERIFIED for the parser; the "merge drops silently" consequence is [SLICE-ONLY]]
- `:321-337` `refs_norm`: collects `_REF_TOKEN` matches from anchor, anchor2, claim and refs, plus bare numeric section refs; drops `SHA-` tokens. [CODE-VERIFIED]
- [RUN] probe (`uv run --no-sync python -c` calling `refs_norm({'anchor':'x','claim':'x','refs':[t]})`, no file written): `FR-8`, `AC-0.4`, `NFR-004`, `REQ-014`, `D-0012`, `R-001`, `R-1.2`, `P1`, `3.2` are recognised; `T03.02`, `T03.02.1`, `I7`, `B3`, `GT10`, `P12`, `S2.3`, `Task 12`, `FR-RSR.9`, `SHA-256` are NOT. So spec-style hyphenated ids work and tasklist task ids (`T03.02`) and letter-segment ids (`FR-RSR.9`, used in the reflect brief text) yield an empty `refs_norm`. [RUN, 2026-11-14, HEAD]

File: `HEAD:src/superclaude/cli/review/findings_v2.py` (304 lines per slice 09 [SLICE-ONLY]; read `:1-200`).
- `:15-22` imports `CATEGORIES`, `_ID`, `_HEAD_FINDINGS`, `_blocks_after`, `_check_flat` from `findings.py`: v2 shares the v1 category vocabulary and limits by import, not by copy. [CODE-VERIFIED]
- `:35` `ROLES = (plan, spec, source, test, diff, artifact)`: the schema already has an input-role vocabulary including `source`. `:36` `LENSES = (spec, reflect-pre, reflect-post)`. `:37` `CHANNELS`. `:41-48` `REFLECT_CATEGORIES` maps a third reflect vocabulary (`ordering, acceptance, coverage, contradiction, risk, deviation`) onto the six-value `CATEGORIES` (`:159-160` enforces the pairing). [CODE-VERIFIED]
- `:59-81` `_check_citation`: role in `ROLES`, repo-relative path, `line_start`/`line_end` integers, optional quote 12-200. `:84-187` `check_finding`: needs an `anchor` or `citations` (`:122-134`); `reflect-post` requires `deviation_class` (`:147-149`); `coverage_rows` must be inside the assigned Coverage slice (`:166-176`). [CODE-VERIFIED]
- `HEAD:src/superclaude/cli/review/cluster.py:67-71` `PRIMARY_ROLES = {reflect-pre: (plan,), reflect-post: (source, diff), spec: (spec,)}`: a per-lens table that already says which citation role is primary. [CODE-VERIFIED]

Key Takeaways (Unit 2):
- The one place where the brief and the parser share numbers is `findings.py`; v2 imports it. A shared core can keep ONE category/limit module and let both brief and parser read it (the brief at `prompts:60` is a hand-typed copy; a test pinning prompt vs parser is what B-2 asks for).
- `_REF_TOKEN` (`findings.py:29`) is spec-id-shaped. It is also duplicated as `_ID_TOKEN` at `HEAD:src/superclaude/cli/review/telemetry.py:23` (two copies of one regex [CODE-VERIFIED]). Task ids of a tasklist (`T03.02`) are invisible to it. It must become a per-module pattern list (hook), not a literal.
- Roles (`plan/spec/source/test/diff/artifact`) exist in v2 `citations`, but nothing in the v1 prompt or in any shipped brief tells a reviewer which file has which role (see Units 3-5).

## Unit 3. E2 harness brief and input delivery at the tip (`run-reviewer.sh`)

File: `E2@6c09843:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh` (path found with `git ls-tree -r --name-only`; a second copy exists at `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh`, not read).

- `:7-8` candidate copied to the sandbox path `/tmp/evalsb/cand/$PKG/candidate.md`. `:9-11` "ship source.md next to the candidate when the eval carries it": `SRC_EVAL` is the hard-coded absolute path `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md`; copy to `/tmp/evalsb/cand/$PKG/source.md`; every failure path ends in `|| true`, so a missing source is silent. [CODE-VERIFIED via `git show | cat -n`]
- `:12` `SHA=$(sha256sum "$CAND_SB")`. `:13-17` `BRIEF` = `/sc:spec-panel @$CAND_SB --mode critique` + the first-review brief (`:15`, same words as `HEAD:prompts:32`, with the candidate path and sha filled in) + a "First-review rules" paragraph (`:17`) that restates the grading check, the Medium rule, the six categories and the `## Findings block` format. [CODE-VERIFIED]
- Negative evidence for open item (b): a case-insensitive grep of the whole script for `source|unpassable` returns only `:9`, `:10`, `:11` (the copy, a shell comment and variables) and `:17` (the string `document_review_loop_prompts.md` and the category `unpassable-check`). The string `source.md` is never inside `BRIEF` (`:13-17`). [CODE-VERIFIED] So at the E2 tip the file is put on disk but the brief never names it.
- `:17` category list reads `contradiction|unpassable-check|data-loss|safety|missing-requirement|other` (matches `findings.py:15-22`); `unpassable-ac` appears nowhere in the tip script. [CODE-VERIFIED]

Key Takeaways (Unit 3):
- E2 input delivery = copy two files into one sandbox directory and name ONE of them in the brief. The reviewer finds `source.md` only by listing the directory or by the candidate's own text (candidates reference `./source.md`, slice 03 section 5 [SLICE-ONLY]).
- Both the path (`/tmp/evalsb/cand/<pkg>/`) and the origin of the source (`.dev/tasks/done/<pkg>/source.md`) are harness constants; a core must take "input documents by role, with a path and a hash each" as data.

## Unit 4. Status of the brief/harness defect lists at HEAD and tip

Item (c). `B-1..B-7` and harness `H1-H12` are from the run-2 hand-off (slice 01 lines 208-214 and 345-353); `CB-1..CB-5` and the collab `H1-H4` (name source.md; truncate; pre-implementation checkout; remove leak) are from the E2 process-redesign brainstorm (slice 06 section 3, lines 175-221, and slice 05 S3.25). "H1-H4" in the assignment is ambiguous, so both sets are given.

| ID | Claim | Re-check | Status |
|---|---|---|---|
| B-1 / CB-1 / collab-H1 | brief names no source/driving doc | `HEAD:prompts:15-21` five placeholders, no source; `:32` "against the requirements it states"; E2 tip `run-reviewer.sh:13-17` does not name `source.md`; the reflect brief carries the spec body inline for the qa persona (`reviewer-spec.md:55`, Unit 6) | OPEN for the review-loop and E2 panel briefs at HEAD [CODE-VERIFIED] |
| B-2 / CB-4 | claim<=300, refs<=8, id<=16, MINOR-not-blocking not in the prompt | `prompts:60` states only the anchor 12-200; `findings.py:26,100-101,111-118` | OPEN [CODE-VERIFIED] |
| B-3 | blocking semantics conflict (`spec-panel.md:259` "CRITICAL is blocking"; `prompts:31` grading sentence; `findings.py:100-101` rejects only MINOR+blocking) | `spec-panel.md:259` read; `findings.py:100-101` read | OPEN [CODE-VERIFIED] |
| B-4 | report ends with `verdict:` (`spec-panel.md:260,263`) vs `## Findings block` last (`prompts:58`) | all three lines read; `_HEAD_FINDINGS` accepts any heading level (`findings.py:31`) | OPEN, low [CODE-VERIFIED] |
| B-5 | no anchor guidance for `missing-requirement` | `prompts:60` says only "the text that is wrong" | OPEN [CODE-VERIFIED] |
| B-6 | `unpassable-ac` in harness brief | tip `run-reviewer.sh:17` carries `unpassable-check`; HEAD Grep (excluding `.dev/tasks`) for `unpassable-ac` found no file | FIXED in harness; was never in a shipped file [CODE-VERIFIED] |
| B-7 | reviewers not told one blocking row fails the round | `prompts:62` "The verdict line stays the reviewer's verdict" | OPEN [CODE-VERIFIED] (the `ledger.py:273-274` side is [SLICE-ONLY]) |
| CB-2, CB-3, CB-5 | list every confirmed defect; blocker sentence; keep half the time for free review | CB-3 sentence already is the grading check at `prompts:31`; CB-2 and CB-5 text exists in no shipped file (Grep of `src/` for "at least half of your time" and "every confirmed defect" found nothing under the paths read) | CB-3 PRESENT; CB-2, CB-5 OPEN (study-only proposals). Search: Grep of the worktree excluding `.dev/**` for `at least half of your time|every confirmed defect|SWEEP SHEET|RECIPES AND LEDGER|ledger-v1|panel-msg` found no file, so none of the redesign brief wording or `ledger-v1`/`panel-msg` schemas exists in shipped code [CODE-VERIFIED negative] |
| collab-H2 truncate before merge | | no truncating code in `findings.py` (`:79-87` rejects over-length) | OPEN [CODE-VERIFIED] |
| collab-H3, H4 | pre-implementation sandbox; remove leak dirs | harness-only (E2 `run-reviewer.sh` sandbox `git archive`, slice 03 manifest) | OPEN, not a core item [SLICE-ONLY] |

Key Takeaways (Unit 4):
- Nothing in B-1..B-5, B-7 or CB-1/2/4/5 has been fixed in a shipped file at HEAD. The only fixed item (B-6) was fixed in a study script, and no shipped file ever carried the typo.
- All open brief items are brief-text or brief-template items, which supports putting the brief builder into the shared core with per-module blocks.

## Unit 5. Open item (e): the two E2 claims marked [CODE-CONTRADICTED]

### (e1) `unpassable-ac` in the E2 harness brief
- The harness copy `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh.unpassable-ac` (listed by slice 03 section 1/6.2) is a superseded file kept as evidence [SLICE-ONLY, not opened here].
- `HEAD:src/superclaude/rules/prompts/document_review_loop_prompts.md:60` lists `unpassable-check`; `HEAD:src/superclaude/cli/review/findings.py:17` has `"unpassable-check"`; E2 tip `run-reviewer.sh:17` has `unpassable-check`. [CODE-VERIFIED] The claim "the rules file and CATEGORIES say unpassable-check, so `unpassable-ac` is a harness-brief typo" holds.
- Searches tried: Grep for `unpassable-ac` over the whole worktree with `!.dev/tasks/**` returned "No files found" (so no file under `src/`, `docs/`, `tests/`, `.dev/` outside tasks, and not under `.dev/eval-workspaces` at HEAD); Grep of the tip script for `unpassable` (Unit 3). Negative evidence: no shipped brief or rule at HEAD carries `unpassable-ac`. The `.claude/` mirror was not searched by this agent's Grep (gitignored); [UNVERIFIED] for the mirror, but `make verify-sync` makes it a copy of `src/`.
- Residual: `unpassable-ac` survives as a ground-truth CLASS name in E2 `ground-truth.json` (slice 03 section 7 [SLICE-ONLY]), a different vocabulary from the findings category. That is a mapping problem (core category set vs a module's ground-truth classes), not a brief defect.

### (e2) `theory.py` HARD set as applied
File: `E2@6c09843:.dev/brainstorms/20261113-163248-panel-collaboration/enrichment/pc-patterns/theory.py` (5,717 bytes; found with `git ls-tree`).
- `theory.py:8`: `HARD = {"I5", "I7", "B7", "B8", "I6", "B1", "B2", "B3", "I4"}  # cross-doc/missing-task + satisfiability`. Members re-derived: I5, I7, B7, B8, I6, B1, B2, B3, I4 (nine). It includes B3 and B7; it excludes B5, I1 and B6. [CODE-VERIFIED]
- `theory.py:13` `hard(r) = len(HARD & set(r["gt"]))`; `:24` prints `low-think: hard/run` and `high-think: hard/run` split at each model's own median thinking tokens (`:21-22`). `r["gt"]` is the keyword PROXY output of `gtproxy.py`, not the blind judge (`gtproxy.py:1-2` "regex proxy, not a judge"). [CODE-VERIFIED]
- `gtproxy.py:91-93` defines the same grouping: "cross-doc / missing-task (I5, I7, B7, B8, I6)", "satisfiability (B1, B2, B3, I4)", "in-plan contradiction (B4, B5, I1, I2, I3, B6)". So HARD = first group + second group; the excluded B5, I1, B6 (and B4, I2, I3) are the third group, and I8 is in no group. The set is a deliberate by-kind definition, not a typo, but it differs from the "ten missed issues" list (B1, B2, B5, B6, B8, I1, I4, I5, I6, I7; slice 05 S2.3 line 22 [SLICE-ONLY]): extra in HARD = {B3, B7}; missing from HARD = {B5, B6, I1}. [CODE-VERIFIED for the set arithmetic]
- Proxy has a signature for every label (`gtproxy.py:19-36`: B1-B8, I1-I8 appear), so B5, I1, B6 were not left out for lack of a proxy. [CODE-VERIFIED] The B3 signature is `T(f,"9") and re.search("condition|word.?list|fails? (when|on)|itself")` (`:22`), a loose pattern.
- Output at the tip, `theory.md:5-11` (hard/run, low-think to high-think): ember 0.25 to 0.22; luna 0.09 to 0.09; haiku 0.29 to 0.70; sonnet 0.46 to 0.74; grok 0.08 to 0.50 (n=12 each half); terra 0.14 to 0.19; wonder 0.67 to 0.67 (n=12 each half). Spearman 0.64 across seven models (`theory.md:13`). [CODE-VERIFIED by reading `theory.md`]
- Effect on the thinking-budget conclusion: (1) the merged-spec line "not a thinking-budget ceiling" rests on ember and luna being flat, both models with the smallest thinking medians (7,094 and 3,560 tokens, `theory.md:5-6`); in the same table haiku, sonnet and grok rise within model. (2) The metric counts B3, the issue the seed brief says 68 of 76 runs found (slice 05 S2.4 [SLICE-ONLY]), so it is not a measure of "hard" issues for the cheap panels; it also drops B5, I1, B6. Whether the correction would make ember/luna rise cannot be computed from the commit: `theory.py:3` reads `/tmp/pc-patterns/records_gt.json`, written by `gtproxy.py:105`, and that file is not among the 12 files committed under `pc-patterns/` (`git ls-tree`: analyze.py, collect.py, gt.md, gtproxy.py, how.py, out.md, rev.md, rev.py, sample.py, surf.md, theory.md, theory.py). [CODE-VERIFIED: file list] So the conclusion is "unproven in either direction for ember/luna; contradicted as a general claim by haiku, sonnet, grok in the same table", not "refuted".
- Also: `gtproxy.py:4` hard-codes the E2 worktree path; the derived proxy is calibrated only against judged rows (`:51-76`), its precision/recall printout is not committed in what was read [UNVERIFIED].

Key Takeaways (Unit 5):
- (e1) is closed: harness typo, never shipped. A shared core should still validate any brief against `CATEGORIES` in a test (B-2 lesson), because the typo cost 15 dropped findings in one combo run (slice 03 [SLICE-ONLY]).
- (e2) means: the thinking-budget finding must not be carried into a core design as a fact; the core only needs to record thinking tokens per reviewer run, and any lever decision waits for a re-computation with the judge and a defined hard set.

## Unit 6. How input reaches the reviewers: the five brief families at HEAD (open item b)

| # | Family | Where the brief is built | How the document(s) reach the reviewer | Is a second (driving) document delivered? |
|---|---|---|---|---|
| 1 | Review loop (`/sc:spec-panel --mode critique`) | coordinator writes the text of `prompts:32` / `:48` / `:53` (`HEAD:prompts:15-21` fills 5 placeholders) | candidate by `@file` plus its sha256 in the brief (`prompts:32`; `spec-panel.md:258` "the report header also records the SHA-256 of the candidate and, when a baseline was given, of the baseline"); baseline and prior report by path (`prompts:48`); panel members from `review panel resolve` (`prompts:70`) | No. Baseline and prior report only. [CODE-VERIFIED] |
| 2 | E2 harness (`run-reviewer.sh`, tip) | `BRIEF` at `:13-17` | candidate path in `/tmp/evalsb/cand/<pkg>/`; `source.md` copied beside it (`:9-11`) but not named | File present, role not stated. [CODE-VERIFIED] |
| 3 | Reflect Tier 2 legacy/shadow (SKILL.md Wave 3A) | `<output>/reviewer-briefs/reviewer-<N>.md`, 3 sections, self-contained (`HEAD:refs/reviewer-spec.md:21-33`) | inline: T1 card excerpt (`:35-39`), grounding hunks as `file:line` H3 blocks (`:41-59`), coverage slice (`:61-74`); input frozen in `<output>/artifacts/input-snapshot.yaml` (`SKILL.md:340` `manifest init --snapshot`) | Yes, inline for the qa persona only: UC-1 spec body as hunk(s), whole file if <= 400 lines else per-section (`reviewer-spec.md:55`). [CODE-VERIFIED] |
| 4 | Reflect code-driven engine (`reflect run`, tasklist post gate) | `HEAD:src/superclaude/cli/reflect/ensemble.py:601-616` `build_worker_prompt`; lens `HEAD:src/superclaude/cli/swarm/lenses/reflect_review.py:47-51` | tasklist body pasted inline between `<<<TARGET>>>` and `<<<END TARGET>>>` with a "Base ref / Tasklist" header (`ensemble.py:619-630`) | No. `config.spec_path` is forwarded only to the `/sc:reflect --spec` command line (`HEAD:src/superclaude/cli/reflect/runner.py:471-472`); `ensemble.py` never references `spec_path` (Grep of `src/superclaude/cli` for `spec_path` lists `runner.py:471`, `models.py:69`, `config.py:*` and roadmap files, no `ensemble.py` line). [CODE-VERIFIED, negative] |
| 5 | Tasklist fidelity validation (`cli/tasklist/prompts.py`) | `HEAD:src/superclaude/cli/tasklist/prompts.py:18-135` `build_tasklist_fidelity_prompt(roadmap_file, tasklist_dir, tdd_file, prd_file)`; the only other builder is `build_tasklist_generate_prompt` (`:158`) | "Read the provided roadmap file and the generated tasklist files" (`:41`): paths, not content | Roadmap yes; spec NO by design: "VALIDATION LAYERING GUARD ... Do NOT compare the tasklist against the original specification" (`:43-48`). Own vocabulary: HIGH/MEDIUM/LOW (`:49-69`), `DEV-NNN` ids, YAML frontmatter (`:90-99`), no `findings-v1`. [CODE-VERIFIED] |

Answer to (b): the scope-slice-02 Q-F reading is correct for families 1 and 2 (the brief never names `source.md`, Units 1 and 3) and the "inference, UNVERIFIED" status of the cause stands (E2 `COMBO-REPORT.md:373` per slice 03 [SLICE-ONLY]; no run tested the naming at HEAD). It is NOT true of all briefs: family 3 delivers the spec body inline and by role. Input reaches reviewers four different ways (path in prose, sandbox copy, inline hunks, inline paste), so there is no single "input" object a core could validate today.

Related code that resolves roles by FILE NAME instead of by a declared role: `HEAD:src/superclaude/cli/review/card_convert.py:15-18` and `:466-470` take the plan as the `<id>.md` entry (or `TASK-` prefix at the snapshot root) and the spec as the single snapshot entry whose name is exactly `source.md`; `:111-125` maps the tokens `plan`, `source.md`, `spec` to roles. If zero or several entries match, refs are "unresolved" (`:128-129`, `:468-471`). [CODE-VERIFIED] In family 3 the word "spec" in `--spec` and the file name `source.md` of a managed plan package are bridged only here.

Reflect brief heading (known anchors `SKILL.md:87`, `:338-349`): `:87` is the `--t2-engine` flag definition (default `legacy`, `panel` rejected); `:342` says shadow briefs are "the legacy briefs plus the one findings-block instruction line of `refs/reviewer-spec.md`"; the line itself is `reviewer-spec.md:39`: `End your card with the exact heading line "## Findings block" (not "## Findings"), then one fenced findings-v2 block ...`, with the same six categories (alphabetical order), `lens "reflect-pre"`, claim <= 300, and citations "1 to 8 objects, each with role plan or spec". Heading text agrees with `findings.py:31` (`Findings block`). The brief narrows the citation roles to `plan|spec` while `findings_v2.py:35` allows six. [CODE-VERIFIED]

Key Takeaways (Unit 6):
- Two of five families (3, 4) already put the driving document or the target inline; the two that use the shared `findings-v1` loop (1, 2) pass it by path and never name it. The tasklist fidelity prompt (5) is a different product (deviation report, HIGH/MEDIUM/LOW) that a unified core must either adopt as a module vocabulary or leave outside.
- The code-driven engine (4) reviews a tasklist without the spec it was written from, while its own UC-1 route (3) gives the qa reviewer the spec. A core "input manifest by role" would make that difference visible and testable.
- `panel.py` has no brief and no brief placeholder: the only "placeholder" there is a tier with an empty model list (`HEAD:src/superclaude/cli/review/panel.py:284-292`), unrelated to the brief. `panel.py` resolves slots/tiers/models only. [CODE-VERIFIED by Grep of `panel.py` for `brief|placeholder`]

## Unit 7. Spec-shape hard-codings found (open item d) and what to make pluggable

| # | Hard-coding | Location (HEAD unless stated) | Shape it assumes | Core action |
|---|---|---|---|---|
| 1 | Reference-id regex `[A-Z]{1,4}-[0-9]+(.[0-9]+)*|P[0-9]` | `findings.py:29`; duplicate `telemetry.py:23` (`_ID_TOKEN`) | spec/PRD requirement ids (FR-8, AC-0.4); [RUN] shows `T03.02`, `FR-RSR.9`, `P12`, `I7` not matched | one pattern list owned by the module; both files import it |
| 2 | Section-ref rule `^\d+(\.\d+)*$` | `findings.py:30`, `:334-336` | numbered headings | per-module hook (tasklist uses Task ids and phase files) |
| 3 | Category set (6) | `findings.py:15-22`; copied in `prompts:60`, `reviewer-spec.md:39`, E2 `run-reviewer.sh:17`; reflect vocabulary `findings_v2.py:41-48`; E2 ground-truth classes (`unpassable-ac`, `missing-task`, `ambiguity`, `contradiction`, slice 03 [SLICE-ONLY]) | spec-defect classes; no "missing-task" class | keep ONE tuple in the core, generate every brief copy from it, give modules a mapping table (as `REFLECT_CATEGORIES` does) |
| 4 | Brief placeholders | `prompts:15-21`: CANDIDATE, BASELINE, PRIOR, N, IDS | revision-chain of one document | core exposes a list of (role, path, sha256, required?) plus N and IDS; roles `plan/spec/source/test/diff/artifact` already exist in `findings_v2.py:35` |
| 5 | Grading paragraph incl. "requirement the document never states" = Medium | `prompts:31`, `spec-panel.md:259`, E2 harness `:17` | spec review where unstated requirements are follow-ups | per-module block (tasklists: missing-task is the defect class that E2 found hardest, slice 06 [SLICE-ONLY]) |
| 6 | Telemetry strata `("sonnet","haiku")` | `telemetry.py:112-115` ("owner decision D3"), validated at `:267-268` | the E3 loop's two reviewer tiers | strata as a registered list per module/experiment; today a stratum other than these two is a validation error |
| 7 | Review kinds | `telemetry.py:19` `("first","re-review","audit")` vs `panel.py:36` `_KINDS = ("first","re-review")` | loop rounds | one kind list; `audit` exists only in telemetry |
| 8 | Document-shape metrics in the telemetry `task` group | `telemetry.py:50-65`: `ids_defined`, `cross_refs`, `rfc2119` (`:26`), `doc_format`, `specialization` | RFC-2119 spec text | metrics must be computed by a module-supplied function; a tasklist has no MUST/SHALL |
| 9 | Primary citation role per lens | `cluster.py:67-71` `PRIMARY_ROLES` | lenses `spec`, `reflect-pre`, `reflect-post` only (`findings_v2.py:36`) | already table-driven: good pattern to copy for a new lens |
| 10 | Reflect reviewer cap | `panel.py:71-73` `_REFLECT_PREFIX`, `_REFLECT_LAUNCH`, `_REFLECT_MAX_REVIEWERS = 3`; `validate_reflect_profile` `:80-134` | one module's profile hard-wired inside the shared validator | profile registry keyed by template prefix |
| 11 | Role-by-filename resolution | `card_convert.py:15-18`, `:466-470` | package layout `<id>/<id>.md` + `source.md` | roles declared in the input manifest, not inferred |
| 12 | E2 harness paths | `run-reviewer.sh:10` (`.../eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md`), `:7` (`/tmp/evalsb`); `gtproxy.py:4`; collab launch scripts (slice 05 S1.17 [SLICE-ONLY]) | one worktree | parameters |

All rows 1-4, 6-11 [CODE-VERIFIED] at the cited lines (rows 5 and 12 partly [SLICE-ONLY] as marked).

Key Takeaways (Unit 7):
- Four of the twelve are "one fact, two copies" (rows 1, 3, 7 and the placeholders list in prompt vs brief): the failure mode a shared core removes by generation, not by review.
- Rows 6 and 8 are measurement hard-codings that would silently mislabel tasklist or PR-review runs; they need to be extension points before the shadow-run store (E1) and the E2 data are merged into one telemetry table.

## Unit 8. What a shared core must expose per module (open item a)

Derived from Units 1-7; every row cites its code basis. "Module" = a thin consumer (spec review loop, tasklist review, reflect Tier 2, later PR code review and rf-qa replacement).

| Core exposes | Per-module value (examples found in code) | Basis |
|---|---|---|
| Input manifest: ordered roles, each `{role, path, sha256, required, inline|by-path}` | spec loop: candidate, baseline, prior; tasklist: plan + `source.md` as `spec`; reflect: card, hunks, coverage slice; PR review: `diff`, `test`; rf-qa: `artifact` | `prompts:15-21`; `findings_v2.py:35`; `reviewer-spec.md:33-61`; `run-reviewer.sh:9-11` |
| Missing-input rule per role | `required` -> return incomplete (`prompts:32`); optional-absent -> recorded `no_source`-style flag, not silent (`run-reviewer.sh:11` `|| true` is the anti-pattern) | `prompts:32`; E2 harness `:11` |
| Brief assembler with named blocks | role list, grading rule, category list (generated), limits (generated from `findings.py:26,100,104,111-118`), ending format and heading (`findings.py:31`), verdict consequence (B-7), tool/read-only rule, "state what you covered" | `prompts:31-32,56-62`; `reviewer-spec.md:39`; B-2, B-7 |
| Category set + module mapping | six values; `REFLECT_CATEGORIES`-style map; ground-truth class map for studies | `findings.py:15-22`; `findings_v2.py:41-48` |
| Reference syntax | pluggable list of id patterns + a path:line citation form; `refs_norm` takes the list | `findings.py:29-30,321-337`; `card_convert.py:88-95` |
| Lens + primary role table | `spec`, `reflect-pre`, `reflect-post`; new lenses (`tasklist`, `pr-diff`) add a `PRIMARY_ROLES` row | `findings_v2.py:36`; `cluster.py:67-71` |
| Panel template and caps | template id/prefix, reviewer cap, kinds | `panel.py:36,71-73`; `telemetry.py:19` |
| Hash-frozen input snapshot | reflect has `artifacts/input-snapshot.yaml`; loop has sha256 in the brief; E2 has none | `SKILL.md:340`; `prompts:32`; Unit 3 |
| Findings schema choice | `findings-v1` (anchor) or `findings-v2` (citations with role) per module | `findings.py:124`; `findings_v2.py:84-187` |
| Telemetry strata and doc metrics hooks | list of strata, module metric function | `telemetry.py:50-65,112-115` |
| Reviewer-side effort record | observed model, thinking tokens, whether each role was opened (E2 audit C had to infer it, 161 of 665 runs, slice 03 [SLICE-ONLY]) | no code at HEAD records "role opened" [UNVERIFIED negative: not searched beyond `telemetry.py` groups `:30-81`, which have no such field] |

Future consumers (unblocked only if the table above is core): PR code review needs roles `diff` and `test` (already in `ROLES`) and a `reflect-post`-like lens (`PRIMARY_ROLES` row `source, diff`, `cluster.py:70`); rf-qa replacement needs the `artifact` role and a module grading block (no `rf-qa` code was read in this item).

## Gaps and Questions

1. [UNVERIFIED] Whether `source.md` naming in the brief changes how often it is read. The E2 report calls the cause an inference (`COMBO-REPORT.md:373`, slice 03 [SLICE-ONLY]); no code or run at HEAD tests it. Searches: Grep of `src/` and `docs/` for any record of "source opened" per run found none in `telemetry.py` groups.
2. [UNVERIFIED] Merge-side consequences of over-length lines (D1, 49 blocking findings lost) were read only as the parser rule (`findings.py:104,118,160-195`); `merge_cmd.py`/`ledger.py` were not read in this item (slice 09 owns them).
3. [UNVERIFIED] `ledger.py:273-274` for B-7 (blocking row from any reviewer fails the round) was not re-read; only the prompt side (`prompts:62`) is verified here.
4. [UNVERIFIED] The `.claude/` mirror copies were not searched for `unpassable-ac`; the worktree Grep skips ignored paths. Low risk (mirror of `src/`).
5. [UNVERIFIED] The thinking-budget recomputation: `/tmp/pc-patterns/records_gt.json` is not committed (Unit 5); the proxy's precision/recall printout (`gtproxy.py:73`) was not found in the committed `out.md` by this item (file not opened).
6. [UNVERIFIED] Counts quoted from slices (156 of 665 runs, 49 blocking findings, 68 of 76 runs finding B3) were not re-derived; they come from E2 reports and the slices.
7. Question: should the E2 tasklist fidelity prompt (family 5, own HIGH/MEDIUM/LOW vocabulary) be a core module or stay a separate gate? Not decidable from code; it is a design choice for the report.
8. Question: assignment item (c) lists "H1-H4" without saying which set. Both were covered in Unit 4 (run-2 hand-off H1-H12 lines are in slice 01 `:352-353` and are [SLICE-ONLY] except H1 `run-reviewer.sh:66-83`, not re-read here; collab H1-H4 from slice 05 S3.25).
9. Not read by this item: `src/superclaude/cli/review/ledger.py`, `merge_cmd.py`, `manifest.py` bodies, `reflect/config.py`, `agents/reflect-reviewer.md`, `rf-qa.md` (outside the assigned list).

## Stale Documentation Found

- **[STALE DOC]** E2 `manifest.md:3-6` says the E2 branch is "local, never pushed"; slice 03 section 2 reports the branch exists on origin at tip 6c09843. [UNVERIFIED] by this item (not re-checked with `git branch -r`; the tip object was readable with `git show`, which only shows the commit exists locally).
- Anomaly (not a stale doc): the shell comment at E2 `run-reviewer.sh:9` ("ship source.md next to the candidate when the eval carries it (per-model source input)") describes delivery of the file, while the brief at `:13-17` never names it (Unit 3). Comment and brief are both current; they only differ in what they promise.
- E2 slice-03 claim "`unpassable-ac` is a harness-brief typo" is [CODE-VERIFIED] (Unit 5), not stale.
- No content or citation from the forbidden run-1 folder or the RUN2-QUEUED note was read or used; the Grep for `unpassable-ac` used `!.dev/tasks/**`, and the Grep for brief wording used `!.dev/**`.

## Summary

Four different briefs deliver input to reviewers at HEAD, and only the reflect brief (spec body inline, role by section) states what each document is; the shared review-loop brief and the E2 harness pass the candidate by path and never name `source.md`, and the code-driven reflect engine never gives its reviewers the spec at all. B-1..B-5, B-7 and CB-1/2/4/5 are still open at HEAD, B-6 (`unpassable-ac`) was a harness-only typo that no shipped file ever carried, and the E2 `theory.py` HARD set (B3 and B7 in, B5/I1/B6 out, by-kind definition) means the "not a thinking-budget ceiling" claim cannot be used as a fact because haiku, sonnet and grok rise within model and the data file is not committed. A shared core must therefore expose an input manifest (role, path, sha, required), generated brief blocks (categories and limits from `findings.py`), pluggable reference patterns, per-module grading blocks, lens/role tables and strata, and replace twelve spec-shaped hard-codings (the id regex duplicated in `findings.py:29` and `telemetry.py:23`, the `("sonnet","haiku")` strata, filename-based role resolution in `card_convert.py`). The tasklist fidelity prompt is a separate vocabulary that needs an explicit decision.
