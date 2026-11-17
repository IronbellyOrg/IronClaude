# Research: Driving-document input contract and reviewer briefs

**Investigation type:** Doc Analyst + Code Tracer
**Scope:** `src/superclaude/rules/prompts/document_review_loop_prompts.md`; `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`; `src/superclaude/agents/reflect-reviewer.md`; E2 `tools/run-reviewer.sh`, per-package `candidate.md`, `tools/tmp-scripts/judge-one.sh` (commit 4a22d74213f93837d00c2c314075dd967b9a98e3); E1 recorded briefs `.dev/reflect/pre-*-shadow*/reviewer-briefs/`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md` Wave 4; `tests/review/test_review_rules_text.py`
**Status:** Complete
**Date:** 2026-11-13

---

Reading order followed: scope `00-handoff-copy.md` sections 2.4, 3 and 6; `01-other-branch-study.md` sections 2 and 6; `03-reflect-side.md` sections 2 and 5; `04-this-session-artifacts.md` sections 0.1, 0.12 and 3; then the source files below. Effort tags: [E1] reflect Tier 2 panel and shadow mode on this branch; [E2] tasklist review-panel study at 4a22d742; [E3] #346 review loop on master (prompts file, review CLI, spec-panel loop).

## 1. `src/superclaude/rules/prompts/document_review_loop_prompts.md` (74 lines) [E3]

What it is: the on-demand prompt file a coordinator reads before briefing a reviewer or reviser in the `/sc:spec-panel --mode critique` review loop (`:3`). It defines three prompts (FIRST-REVIEW, RE-REVIEW, REVISE; `:7-11`), the findings-v1 block (`:56-62`), the fix map (`:64-66`) and the panel CLI wiring (`:68-70`).

### 1.1 Placeholders (the input contract) [E3]

- `## Values to fill` lists exactly five placeholders (`:17-21`): `{{CANDIDATE}}` (the `@file` of the command), `{{BASELINE}}` (`--baseline`), `{{PRIOR}}` (`--re-review`), `{{N}}` (review number) and `{{IDS}}` (blocking ids for the reviser). [CODE-VERIFIED: the prompts file is itself the product artefact; read `:15-21`]
- **There is no source / driving-document placeholder.** No `{{SOURCE}}`, `{{SPEC}}` or equivalent exists anywhere in the file (whole file read, 74 lines). The only role table (`:39-43`) names CANDIDATE, BASELINE and PRIOR. The RE-REVIEW brief even calls `{{BASELINE}}` "the spec as it was before the revision" (`:48`), i.e. the loop treats the candidate document as its own spec: there is no notion of a separate upstream document the candidate must satisfy. [E3]

### 1.2 FIRST-REVIEW brief (`:32`) and grading line (`:31`) [E3]

- The first-review brief says "Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states" (`:32`). The comparison target is the candidate's own stated requirements, not a driving document. This is D8 in the hand-off (HANDOFF section 2.4 row D8) [CODE-VERIFIED at `:32`]. For a spec under review this is correct (a spec has no upstream requirements file in the loop); for a tasklist, a plan, or a PR, which are derived from an upstream document, it means the brief never asks the reviewer to check plan against source.
- "If an input is missing or unreadable, return incomplete" (`:32`) is the only input-validation instruction; since only one input is named, a missing source can never trigger "incomplete".
- The grading check (`:31`) defines blocking as a sentence that holds "with no further assumption" and grades "a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case)" as Medium. This is D9 in the hand-off [CODE-VERIFIED at `:31`]. Interaction with this topic: when a source exists, a requirement that the SOURCE states but the PLAN omits is not "a requirement the document never states" in the spec-review sense; it is a coverage gap against an upstream document, which for a tasklist is often the implementation blocker (the E2 ground-truth class `missing-task`, scope slice 01 section 2.2). The grading line has no wording that separates "missing from the document and from the source" (Medium) from "stated in the source, missing in the plan" (potentially blocking). A unified brief needs that distinction once a source is supplied.

### 1.3 RE-REVIEW and REVISE briefs (`:44-54`) [E3]

- RE-REVIEW inputs are CANDIDATE, BASELINE and PRIOR with a fixed role table (`:39-43`) and a mechanical evidence step (`diff -w BASELINE CANDIDATE`, `:44`) plus a `grep -nF` self-check "when commands can be run" (`:46`). The re-review prompt therefore assumes a reviewer that can run shell commands (`diff`, `grep`). [CODE-VERIFIED `:44`, `:46`]. This conflicts with reflect's read-only reviewer that has no Bash (section 3 below): a reflect-style reviewer could not perform Step 1 itself; the orchestrator would have to inject the diff as a grounding hunk.
- REVISE brief (`:53`) names `{{IDS}}` and `{{CANDIDATE}}` only; a reviser of a tasklist also needs the source to avoid "repairing" a finding into a new source violation. No source is named. [E3]

### 1.4 Review panel CLI wiring (`:68-70`) [E3]

- `:70`: each review runs with the reviewers that `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` prints, "each in a fresh context with the same brief, none seeing another's report or transcript"; reports are merged with `superclaude review merge`; `superclaude review ledger revise --ledger ... --old ... --new ... --fixmap ...` records the reviser's work. "A merge refuses a round in which no reviewer produced a valid findings block". Whether these subcommands are registered is outside this slice (scope slice 02 covers the CLI) and is [UNVERIFIED] here.
- "the same brief" (`:70`) means every panel member gets the identical brief: there is no per-reviewer persona slicing in the E3 loop, in contrast to reflect's persona-filtered briefs (section 2). [CODE-VERIFIED `:70`]
- `## Never` (`:74`): a brief "may narrow the command's scope but may not widen it". Adding a required source read is arguably a widening; a unified brief template should state the source read as part of the core contract, not as a per-caller addition, so it does not collide with this rule.

### 1.5 Findings-block anchor rule and the source [E3]

- `anchor` must be "12 to 200 characters copied exactly from the candidate" (`:60`); `refs` lists "the requirement ids and section numbers the finding rests on" (`:60`). There is no field for a citation INTO the source document. A finding "plan omits source requirement R-7" can only anchor on plan text and put `R-7` in `refs`; the source line is unrecorded and cannot be machine-checked. Reflect's findings-v2 line (section 2.2) adds `citations[]` with `role plan or spec`, which is exactly that missing field.

### 1.6 `tests/review/test_review_rules_text.py` (93 lines) [E3]

- `test_older_pins_still_hold_and_no_source_path` (`:76-92`): despite its name, the "no source path" pin is `assert "src/superclaude" not in TEXT` (`:92`) — it forbids a repository source-code path (the installed-primitive rule in project CLAUDE.md), NOT a source-document placeholder. [CODE-VERIFIED `:92`]. A `{{SOURCE}}` placeholder does not break it. Naming hazard: the task brief calls it "the no-source-path pin"; a reader may take it as forbidding a source-document path. It does not.
- Pins that a `{{SOURCE}}` change must respect:
  - `test_insertions_a_b_c_follow_their_brief_lines` (`:34-42`): the line immediately after `- First-review brief: "` must be the findings-block instruction `INS_A` (`:13`). A new source instruction must therefore go INSIDE the quoted brief sentence (same line) or in `## Values to fill`, not as a new bullet between the brief and the findings-block bullet.
  - `test_each_insertion_is_present_exactly_once` (`:28-31`) and `test_d_text_is_the_contract_text` (`:65-73`) pin the findings-v1 example line verbatim (`:68`); adding a citation field to the example line changes that pin.
  - `test_older_pins...` pins `## Values to fill` (`:81`) and `| ROLE | FILE VALUE | MEANING |` (`:84`) by presence only, so adding a row `SOURCE` to the role table or a bullet to Values to fill is compatible.

Key Takeaways
- [E3] The loop's input contract has five placeholders and none for a driving document (`:17-21`); the first-review brief reviews the candidate "against the requirements it states" (`:32`). D8 is confirmed at source.
- [E3] The grading line (`:31`) makes "a requirement the document never states" Medium, with no wording for "stated in the source, missing in the plan"; adding `{{SOURCE}}` needs a grading clause for source omissions.
- [E3] The re-review prompt assumes the reviewer runs `diff -w` and `grep -nF` (`:44`, `:46`), which a read-only no-Bash reviewer cannot do.
- [E3] The test file's "no source path" pin is about `src/superclaude` (`:92`), not about source documents; a `{{SOURCE}}` placeholder is compatible if inserted inside the brief line or in Values to fill (`:34-42`).
- [E3] findings-v1 has no source-citation field (`:60`); reflect's findings-v2 `citations[].role` (plan|spec) fills that gap.

---

## 2. Reflect brief template: `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` (116 lines) and SKILL.md Step 3B.0 [E1]

### 2.1 The three-section brief (C7) [E1]

- Step 3B.0 writes one brief per reviewer at `<output>/reviewer-briefs/reviewer-<N>.md` (`reviewer-spec.md:21-27`; SKILL.md:303). Each brief is "self-contained, so reviewers run truly in parallel without orchestrator round-trips" (`reviewer-spec.md:29`).
- "A reviewer brief MUST contain exactly these three sections, in this order" (`reviewer-spec.md:33`): `## T1 card excerpt` (`:35-39`), `## Grounding hunks` (`:41-59`), `## Coverage slice` (`:61-74`). Pinned by `test_the_brief_template_has_exactly_three_sections` (`tests/cli/reflect/test_shadow_skill_contract.py:146-165`), which extracts the `#### \`## ...\`` headings between "### Required sections (per brief)" and "### Contract emission" and requires exactly those three (`:153-157`). [CODE-VERIFIED]
- **What the test actually pins:** the TEMPLATE TEXT in reviewer-spec.md, not any produced brief. Briefs are written by the orchestrating model; `grep` over `src/superclaude/cli`, `scripts` and `tests` finds no code that parses or validates a materialized `reviewer-briefs/*.md` (only the template test hits, `test_shadow_skill_contract.py:154-160`). [CODE-VERIFIED by absence, grep run 2026-11-13]. SKILL.md:1934 lists the testability map row `<output>/reviewer-briefs/ min_files=N` (a `dir_count` grader: counts files, not shape).
- **There is no "driving document" section.** The three sections are all orchestrator-derived artefacts (a T1-card slice, hunks, a coverage-matrix slice). The source/spec reaches a reviewer only (a) as grounding hunks the orchestrator chose for that persona, or (b) through the reviewer's own Read of the grounding root. [CODE-VERIFIED `reviewer-spec.md:35-74`]

### 2.2 Shadow line placement [E1]

- In shadow mode one instruction line is appended "inside this section, after the excerpt and not as a fourth section" (`reviewer-spec.md:39`); legacy briefs do not carry it (`:39`). The line asks for an exact `## Findings block` heading, one fenced findings-v2 block, field list, and "citations (1 to 8 objects, each with role plan or spec ...)" plus a `reviewer_model_self_report` line (`:39`). Its example line is parsed by `fv2.parse_block` in `test_the_reviewer_brief_line_carries_the_schema_and_its_example_parses` (`test_shadow_skill_contract.py:199-218`). [CODE-VERIFIED]
- **[CODE-CONTRADICTED] role vocabulary:** the brief line tells reviewers citation `role` is "plan or spec" (`reviewer-spec.md:39`), but the parser accepts six roles `("plan", "spec", "source", "test", "diff", "artifact")` (`src/superclaude/cli/review/findings_v2.py:35`, error text `:63`). The brief narrows the vocabulary; it has no `source` role even though the parser has one, and UC-1 workflow packages call the driving file `source.md` (section 4). A unified brief must decide whether "source" and "spec" are distinct roles (see 2.4 below for why they should be).
- Commit history: the line was rewritten twice on 2026-11-13 (`9874d63fb` 01:54 UTC "require the schema in the reviewer brief"; `c2e3347d3` 02:57 UTC "reviewer brief names the exact findings heading") (`git log -- refs/reviewer-spec.md`, read 2026-11-13). The trigger was the troubleshoot report (scope slice 04 section 0.12): compliance 0.67 because the brief named the format without the schema.

### 2.3 Persona-filtered source injection: only qa gets the spec body (E1 W-3 context) [E1]

- **D13 spec-body hunks (UC-1):** "the SPEC BODY ITSELF is injected into this `## Grounding hunks` block for the **`qa`-persona** reviewer" — whole file when the spec is 400 lines or fewer, else per-section hunks covering 100 percent (`reviewer-spec.md:55`). The qa persona gains one line: "Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding." (`:55`). Stated purpose: "even if Pass 2 under-extracts, one reviewer reads the source document rather than the matrix derived from it" (`:55`). SKILL.md:1717 confirms the token cost note ("adding roughly spec-length tokens to ONE T2 reviewer's brief"). [CODE-VERIFIED: template text; no code materializes it]
- Consequence: by design, the analyzer and refactorer reviewers see only persona-filtered hunks of the spec, never the full source. Two of three reviewers are partially source-blind by construction. Same persona-filtered pattern for FR-4 verification results (`:53`) and FR-RSR.9 runtime-surface ledger (`:57`): all source-of-truth inputs go to qa only.
- **Parsed-sparse escalation:** Step 1B.2b emits `coverage_degraded: parsed-sparse` when `inferred_count > parsed_count` and forbids the Tier-1 stop (SKILL.md:284); the pre-filter is table-wide (SKILL.md:443). Merged requirements record 37 of 38 pre runs escalated to T2, 34 by this pre-filter "because workflow sources carry no labelled requirement ids" (scope slice 04 section 0.1, citing MR:142) [UNVERIFIED in this slice: MR:142 not re-read; the SKILL.md mechanism is CODE-VERIFIED at :284, :443]. So for the workflow consumer, Tier 2 (and its persona-filtered source exposure) is the normal path, not the exception.
- **W-3 (E1):** `cluster-v2-known-weaknesses.md:9` (`.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/`): "A `spec:N` line reference is resolved against the short `source.md` brief, not the spec." Effect: "A spec line number can point at the wrong text, so a path-aware match on it is unreliable." Found by the split-pair judge. [E1, doc-sourced, see 4.2 for the recorded-brief evidence that supports it].

### 2.4 Recorded E1 briefs: what reviewers actually got [E1]

Inspected all 45 briefs in the 15 `.dev/reflect/pre-*-shadow*/reviewer-briefs/` directories with one awk pass (2026-11-13; counts H2 headings outside code fences, findings-v2 mentions, spec-body markers, `source.md` mentions), and read three in full or in part: shadow04 reviewer-2 (`:1-35`), shadow15 reviewer-1 (`:1-36`), shadow01 reviewer-2 (`:1-70`), plus shadow09 reviewer-1 headings. Brief file mtimes span 2026-11-12 20:02 to 2026-11-13 02:35 UTC, all BEFORE `c2e3347d3` (02:57 UTC); the four latest (shadow12-15, 02:11-02:35) are after `9874d63fb` (01:54). Which installed skill version each run used is [UNVERIFIED] (headless runs read the installed `~/.claude` copy; scope slice 04 section 3, "User-level CLI install").

Findings (model-behaviour evidence of the orchestrating model, dated 2026-11-12/13):

1. **The three-section shape is not held in practice.** 23 of 45 briefs carry more or different H2 sections than the template: shadow01 (3 briefs, a 4th H2 such as `## Coverage / acceptance section (qa slice)` inside the T1 excerpt, `shadow01/reviewer-2.md:8`), shadow02 (2), shadow03 (3), shadow06 (3, five H2 incl. `## Codegraph run state`, `## What you are auditing`), shadow09 (3, six H2 `## Mission`, `## Inputs (Read these yourself; ...)`, `## Findings output contract`, `shadow09/reviewer-1.md:6,9,38`), shadow10 (3, the shadow line moved to a 4th section `## Card format (findings-v2 ...)`, which is exactly what `reviewer-spec.md:39` forbids), shadow11 (3), shadow14 (3). Because nothing checks a produced brief (2.1), C7 is a template-text pin only. [E1]
2. **The shadow line is never the verbatim template line.** 0 of 45 briefs contain the phrase "exact heading line" from the current `reviewer-spec.md:39`; 3 briefs (shadow01) have no findings-v2 instruction at all; shadow04 carries a one-line paraphrase "fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec)" (`shadow04/reviewer-2.md:17`) with no schema. Partly explained by timing (briefs predate `c2e3347d3`), but it also shows the orchestrator paraphrases a template line rather than copying it. [E1]
3. **Preamble outside the three sections.** shadow04 (`reviewer-2.md:3-5`), shadow13 (6-8 non-blank lines before the first section) and others put role/read-only/persona text before `## T1 card excerpt`. The persona instruction from D13 (`reviewer-spec.md:55`) lands in this preamble in shadow04 (`reviewer-2.md:5`) and shadow01 (`reviewer-2.md:4`). [E1]
4. **The qa brief does carry the "spec body" in every run** (`specbody>=1` for every reviewer-2 brief; e.g. `shadow15/reviewer-2.md:24` "source.md:1-65 (full spec body — audit the matrix against this)"). D13 is followed. [E1]
5. **The "spec" is often a one-line `source.md` that delegates to another document.** `shadow04/reviewer-2.md:23-27` injects "spec (whole body): .../source.md:1" — a single sentence. `shadow01/reviewer-2.md:58-62` injects `source.md:1-1` ("Detach ... as specified in .dev/troubleshoot/.../remediation-source.md"), and the orchestrator ALSO injected `remediation-source.md:9-26` (`:64-70`); the T1 card records "The 100% union coverage is vacuous. The spec is one line (source.md:1) that delegates every real requirement to `remediation-source.md`" (`shadow01/reviewer-2.md:12`). `shadow09/reviewer-1.md:10` names "SPEC (1 line, incorporates issue #357 by reference)" and tells the reviewer to "run `gh issue view 357`", which (a) violates the L4 live-execution prohibition (SKILL.md:305) and (b) cannot run on `reflect-reviewer` (no Bash, section 3). Coverage rows then cite "spec:1" for every requirement (`shadow09/reviewer-1.md:31-33`). This is the mechanism behind W-3: `spec:N` citations point into a 1-line `source.md`, while the real requirements live in a referenced document. [E1]
6. **The real driving document is resolved by the orchestrator, ad hoc.** When `source.md` delegates, whether the referenced document reaches the brief depends on the orchestrator noticing (shadow01 did, `:64`; shadow09 told the reviewer to fetch it). There is no rule in `reviewer-spec.md` or SKILL.md Step 3B.0 for following a source's "as specified in <path>" reference (whole `reviewer-spec.md` read; SKILL.md:303 read). [E1]

Key Takeaways
- [E1] Reflect's brief has three fixed sections, none of them named "source"; the full spec body reaches only the qa persona (`reviewer-spec.md:55`). Two of three reviewers are source-partial by design.
- [E1] C7 ("exactly three sections", shadow line inside T1 excerpt) pins template text only (`test_shadow_skill_contract.py:146-165`); 23 of 45 recorded briefs break the shape and 0 of 45 carry the verbatim current shadow line. A unified brief should be rendered by code from a template, not written by the orchestrator.
- [E1] The brief's citation role list ("plan or spec", `reviewer-spec.md:39`) is narrower than the parser (`findings_v2.py:35` has `source`); the workflow `source.md` is often a one-line pointer, so "spec" and "source" are different things in practice (W-3).
- [E1] Parsed-sparse escalation (SKILL.md:284, :443) makes Tier 2 the normal path for workflow plans, so the source-exposure rules of the Tier 2 brief matter for nearly every run.
- [E1] No rule follows a delegating `source.md` to its referenced spec; recorded runs show the orchestrator doing it ad hoc or pushing it onto a reviewer that cannot run the command.

---

## 3. The E2 study inputs: runner, candidates and judge (read with `git show 4a22d742:<path>`) [E2]

Paths below are relative to `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` at commit `4a22d74213f93837d00c2c314075dd967b9a98e3`.

### 3.1 `tools/run-reviewer.sh` (87 lines) [E2]

- **Source shipping (`:9-11`).** The runner copies the candidate to `/tmp/evalsb/cand/$PKG/candidate.md` (`:7-8`) and, if `.../eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md` exists in the OTHER worktree (absolute path hard-coded, `:10`), copies it to `/tmp/evalsb/cand/$PKG/source.md` (`:11`). Edge case: when the source does not exist, `:11` falls through to `|| true` silently, and a stale `source.md` from an earlier copy would stay in the sandbox; no record of whether a source was shipped is written to `meta.json` (`:58` has no source field). [CODE-VERIFIED]
- **Brief (`:13-17`).** Line 13 invokes `/sc:spec-panel @$CAND_SB --mode critique`; line 15 is the FIRST-REVIEW brief text of `document_review_loop_prompts.md:32` with `$CAND_SB` and `$SHA` filled ("against the requirements it states"); line 17 restates the grading check (`:31`) and the findings-v1 schema and says "from ~/.claude/rules/prompts/document_review_loop_prompts.md, read it first". **The brief names only `$CAND_SB`; `source.md` is never mentioned.** [CODE-VERIFIED `:13-17`]. D8 holds for the E2 brief exactly as for the E3 prompt file: the E2 brief is a filled copy of the E3 first-review prompt, so it inherits the gap. [E2][E3]
- **Working directory vs source location.** The reviewer runs with `cd /tmp/evalsb/repo` (`:48`), while candidate and source sit in `/tmp/evalsb/cand/$PKG/` (`:7`, `:11`), a different tree. The reviewer can only find `source.md` by resolving `./source.md` relative to the candidate path, not relative to its cwd. [CODE-VERIFIED]
- **Permissions (`:48`).** `timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit`. Bash is NOT disallowed, and `bypassPermissions` approves every remaining tool call, so a reviewer could write files through Bash (redirects, `sed -i`, `git`). The only safeguards are (a) the sandbox is a `/tmp` git-archive copy (scope slice 01, H32/`manifest.md:10`), and (b) an after-the-fact audit (audit C, "no candidate was written", COMBO-REPORT:373 per scope slice 01 H23). [CODE-VERIFIED `:48`; audit claim from scope slice, not re-read]
- **Required-read verification: none in the runner.** `meta.json` records model identity, block presence, wall time, tokens and exit (`:58`) but nothing about which files the reviewer opened. The 156/665 "never referenced source.md" figure was produced afterwards from raw transcripts (scope slice 01 H17, COMBO-REPORT:373). The raw transcript IS saved (`$RID.attempt$attempt.json`, `:48`), so a post-run check is possible from the runner's own output. [CODE-VERIFIED for what `meta.json` holds]

### 3.2 Per-package `candidate.md` (3 packages) [E2]

Packages at 4a22d742: `TASK-WF-design-20261108-041415`, `TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649` (each holding `candidate.md`, `ground-truth.json`, `ground-truth-draft.json`, `resolution-default.json`, `resolution-live7.json`, `reviews/`, `reviews-failed-launch-1/`; `git ls-tree`). No `source.md` is committed in any eval package.

| Package | candidate lines | `source.md` mentions in candidate | candidate:3 | candidate:14 | `.dev/tasks/done/<pkg>/source.md` in this worktree (tracked) |
|---|---|---|---|---|---|
| design | 173 | 2 | `source: ./source.md` | `Source: ./source.md` | 133 lines, 14,466 bytes |
| designSpec | 200 | 13 | `source: ./source.md` | `Source: ./source.md` | 378 lines, 43,932 bytes |
| makeTheAliasOnly | 134 | 2 | `source: ./source.md` | `Source: ./source.md` | 20 lines, 6,432 bytes |

[CODE-VERIFIED by `git show` and `wc` 2026-11-13; `git ls-files` confirms the three `source.md` files are tracked on this branch]. So every candidate carries a pointer to its source in frontmatter and body (`workflow-plan/1.2` frontmatter, the same `source: ./source.md` key that `sc-workflow-protocol/SKILL.md:71` mandates), yet the brief does not tell the reviewer to open it. The pointer inside the document was not enough for 156 of 665 valid-era runs (ember 81/209, luna 49/222, sonnet 1/63, terra 0/44; scope slice 01 H17) — model-dependent behaviour recorded 2026-11-12. [E2]

The E2 sources are full specs (133-378 lines), unlike several E1 workflow sources that are one-line prompts (section 2.4 item 5). The source length distribution is input-dependent: `sc-workflow-protocol/refs/input-parse.md:41` defines `source.md` as "byte-exact copy of a file source, or the inline prompt text". [CODE-VERIFIED `input-parse.md:41`] [E1][E2]

### 3.3 `tools/tmp-scripts/judge-one.sh` (31 lines) [E2]

- The blind judge brief lists exactly three files: ground truth, candidate, anonymized merged report (`:12-16`) and says "Do not read anything outside the files named here" (`:12`). **The judge never gets `source.md`.** [CODE-VERIFIED `:13-16`]. Matching is "against candidate.md" anchors and quotes (`:19`). For tasklist review this is acceptable because ground truth items carry a `plan_quote`; for a judge of source-coverage findings ("plan omits source requirement R-7") the judge cannot confirm the source side.
- The judge runs `--permission-mode bypassPermissions` with no `--disallowedTools` at all (`:25-27`); it must write `score.json` (`:21`). Read-only for the judge is prompt-only. [CODE-VERIFIED `:25-27`]

Key Takeaways
- [E2][E3] The E2 brief is a filled copy of the E3 first-review prompt (`run-reviewer.sh:15` vs `document_review_loop_prompts.md:32`); both name only the candidate. D8 is one defect in one shared prompt, not two.
- [E2] Every candidate names `./source.md` at `:3` and `:14`, and the runner ships the file beside it (`:9-11`), yet 156/665 runs never referenced it: a pointer inside the document plus a file on disk is not a reliable input contract; the brief must name it and the run must check it.
- [E2] The runner records no "source shipped" or "source read" field (`:58`); the read check was a separate offline audit over raw transcripts.
- [E2] Read-only is enforced only for Edit/Write/NotebookEdit; Bash stays available under `bypassPermissions` (`:48`); the judge has no deny list (`:25-27`).
- [E2] The judge has no source input (`:13-16`), so it cannot score source-coverage findings.

---

## 4. Reviewer read-only enforcement: reflect allowlist vs E2 deny list [E1][E2]

### 4.1 `src/superclaude/agents/reflect-reviewer.md` (151 lines) [E1]

- Frontmatter `tools: Read, Grep, Glob, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact` (`:5`), `permissionMode: plan` (`:8`), `maxTurns: 50` (`:7`), `model: sonnet` (`:6`). An ALLOWLIST: no Bash, Edit, Write, Task. [CODE-VERIFIED `:5-8`]. Pinned by `tests/cli/reflect/test_reviewer_readonly_tools.py`: `_MUTATORS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})` (`:30`) and `test_reflect_reviewer_tools_excludes_all_mutators` (`:78`). [CODE-VERIFIED]
- Safety Constraint (`:36-40`): "DO NOT modify, edit, delete, move, or rename ANY file. You have no write/Bash/Task tool ..." and states that the prose is the backstop to the mechanical allowlist (`:40`). [CODE-VERIFIED]
- Inputs (`:48-59`): the agent expects `spec_path`, `tasklist_path`, `diff_scope`, `reviewer_grounding_root`, `persona_lens`, `output_path`. **[CODE-CONTRADICTED] vs reviewer-spec.md:** the agent says the orchestrator passes `spec_path` (an absolute path to the driving spec, `:52`), but the brief template defines only three sections (T1 excerpt, hunks, coverage slice, `reviewer-spec.md:33-74`) with no `spec_path` field. In the recorded E1 briefs the spec path appears only as hunk H3 titles (e.g. `shadow15/reviewer-2.md:24`) or, in shadow09, an ad hoc `## Inputs (Read these yourself ...)` section (`shadow09/reviewer-1.md:9-13`). So the agent's own input contract (named spec path) and the template (no spec field) disagree; the agent file wins in practice only when the orchestrator improvises.
- The agent description and Triggers are UC-2 oriented ("Audits completed work against its driving spec/tasklist", `:3`; "for a UC-2 post-execution deviation audit", `:15`), while shadow mode is UC-1 only (scope slice 03 section 2.3). The 4-category taxonomy (`:21-26`) is post-execution vocabulary; UC-1 reviewers use it only loosely. [E1, CODE-VERIFIED text]
- "Audit the live shared worktree instead of the supplied snapshot" is a Will Not (`:131`); recorded briefs show `worktree_root` = the live worktree, not a snapshot (`shadow04/reviewer-2.md:3`, `:21`). Whether `--isolate-reviewers` was used in those runs is [UNVERIFIED].
- `maxTurns: 50` and read tools mean a reviewer CAN open the spec itself when a path is in its brief. Read-verification is possible from the subagent transcript (scope slice 04 section 3, "Observed identity" reads sidechain transcripts), but no step does it today. [E1]

### 4.2 Comparison [E1][E2]

| Aspect | Reflect (E1) | E2 runner | E3 loop prompt |
|---|---|---|---|
| Mechanism | Agent-type allowlist (`reflect-reviewer.md:5`), `permissionMode: plan` (`:8`) | CLI deny list `--disallowedTools Edit Write NotebookEdit` + `bypassPermissions` (`run-reviewer.sh:48`) | None in the prompt; spec-panel reviewers are whatever `review panel resolve` prints (`document_review_loop_prompts.md:70`); "Do not edit the candidate" is prose (`:32`) |
| Bash | Not available | Available, auto-approved | Required for Step 1 `diff -w` and self-check `grep -nF` (`:44`, `:46`) |
| Verification of reads | none | none in runner; offline audit over transcripts | none |
| Isolation | L2 snapshot (`reflect-reviewer.md:146`), optional | `/tmp/evalsb/repo` git archive minus `.dev/tasks/done`, eval workspaces, `.dev/research` (scope slice 01 H32) | "fresh context ... none seeing another's report or transcript" (`:70`) |
| Dispatch | in-session Agent tool subagent | `claude -p` subprocess, JSON transcript saved | unspecified (fresh context) |

- **Conflict:** the E3 re-review contract needs a reviewer that runs `diff` and `grep` (`:44`, `:46`), while reflect forbids any live execution in a brief (SKILL.md:305) and gives the reviewer no Bash. A unified panel must move Step 1 (the diff evidence block) and the self-check into the orchestrator and inject them as grounding hunks — the same FR-4 pattern reflect already uses for verification results (`reviewer-spec.md:53`). [E1][E3]
- E2 needed Bash only because it drove `/sc:spec-panel` as a slash command inside `claude -p`; the review itself needs Read/Grep/Glob. [E2, inference from the brief at `:13-17`; no Bash step is named in the first-review brief]

Key Takeaways
- [E1] Reflect enforces read-only mechanically with a tool allowlist (`reflect-reviewer.md:5`); E2 used a deny list that leaves Bash auto-approved (`run-reviewer.sh:48`) and relied on an after-the-fact audit; E3 has no mechanism in the prompt.
- [E1] The `reflect-reviewer` agent expects a `spec_path` input (`:52`) that the three-section brief template never provides; this is a contract mismatch inside E1.
- [E3][E1] The E3 re-review evidence step requires shell commands; a read-only unified reviewer needs the orchestrator to compute `diff -w` and the quote self-check and inject them as hunks.
- [E1][E2] Neither path verifies that a reviewer read a required file; both save a transcript (E2 JSON at `run-reviewer.sh:48`, E1 sidechain transcripts) from which it could be checked.

---

## 5. Consumer input matrix: plan, spec, source, required reads, verification [E1][E2][E3]

Terms used: **candidate** = the document or change under review (findings anchor here); **source** = the driving document the candidate was derived from (the snapshot the producer recorded); **spec** = the full requirements text, which equals the source when the source is a file, and is a referenced document when the source is a prompt that delegates ("as specified in <path>"); **baseline/prior** = re-review inputs.

| Consumer | Candidate | Source | Spec (if different) | Other inputs | Required reads today | How a required read could be verified |
|---|---|---|---|---|---|---|
| reflect pre (UC-1) [E1] | `--tasklist` plan (`commands/reflect.md:27`, `:93`) | `--spec` (required, `commands/reflect.md:27`, `:92`) | Any document the spec references; no rule follows it (section 2.4 item 6) | T1 card, coverage matrix, codegraph state, verification hunks (`reviewer-spec.md:35-74`) | Only qa persona gets the spec body (`reviewer-spec.md:55`); others get persona-filtered hunks | Spec hunks are injected by the orchestrator, so "read" = present in brief (checkable from the brief file); for reviewer-side reads, the subagent transcript |
| reflect post (UC-2) [E1] | the diff (`--diff`) or task log (`--task-log`) (`commands/reflect.md:28`) | `--tasklist` (recommended) and `--spec` (recommended) (`commands/reflect.md:92-93`) | as above | verification results (FR-4, `reviewer-spec.md:53`), runtime-surface ledger (FR-RSR.9, `:57`) | none stated; coverage slice is "tasklist-task-to-diff-hunk mapping" (`reviewer-spec.md:63`) | same as pre; shadow mode is UC-1 only (scope slice 03, section 2.3) |
| workflow tasklist review [E1][E2] | `<pkg>/<id>.md` | `<pkg>/source.md` (`sc-workflow-protocol/SKILL.md:47`, `:89`; byte-exact file copy or inline prompt, `refs/input-parse.md:41`) | When `source.md` is a prompt naming a file, that file (not snapshotted) | `artifacts/codegraph-grounding.md` pre-check (`SKILL.md:87`) | Wave 4 calls `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` (`SKILL.md:89`), so the reflect-pre rules apply; no panel step of its own (HANDOFF D14) | as reflect pre; plus E2's transcript method (did any tool call open `source.md`) |
| spec review for brainstorm / design [E3] | the spec document (`/sc:spec-panel @file`, `commands/spec-panel.md:22`) | none named; the loop reviews "against the requirements it states" (`document_review_loop_prompts.md:32`) | upstream brief/issue if any (not modelled) | baseline + prior on re-review (`:17-19`) | none | n/a today. **Gap:** neither `sc-brainstorm-protocol/SKILL.md` nor `commands/design.md` calls `/sc:spec-panel` or the review loop (grep for `spec-panel` and `review` in both, 2026-11-13: only adversarial delegation at `sc-brainstorm-protocol/SKILL.md:39`). The consumer does not exist yet. |
| PR code review [E3-adjacent] | the PR diff (`sc-auggie-review-protocol/SKILL.md:30-31`, `:97`) | PR title and body from `gh pr view ... title,body,files` (`:30`, `:97`) | the linked issue / spec — not fetched | file list (`:130`) | none; the PR body is used only to drop findings that restate its caveats (`:229`) | n/a today |
| rf-qa replacement [E3-adjacent] | research/synthesis/report files (`agents/rf-qa.md:47-49`) | "Research directory path and topic context" (`:48`); the research question lives in the task file | the task file's embedded research prompt | "Verification criteria (the checklist to apply)" (`:50`) | the files listed by the orchestrator | n/a today |

Observations:
- Only reflect has a required source input enforced by a STOP (`commands/reflect.md:32`: "`--mode pre` with no `--spec`"). The E3 loop, PR review and rf-qa have no source role at all. [E1][E3]
- The workflow chain passes `source.md` as reflect's `--spec` (`sc-workflow-protocol/SKILL.md:89`), which conflates "source" and "spec": for an inline-prompt source the "spec" is the prompt (W-3; section 2.4 item 5). [E1]
- A required read can be verified in two ways, both already used somewhere: (a) **orchestrator injection** — the source text is a grounding hunk in the brief, so its presence is checked by reading the brief (reflect qa persona, `reviewer-spec.md:55`); (b) **transcript audit** — scan the reviewer's tool calls for a Read of the source path (E2 audit C, 156/665). (a) is deterministic and works for read-only subagents; (b) is the only option when the source is too large to inject and needs a transcript-capable adapter (`claude -p --output-format json`, `run-reviewer.sh:48`, or sidechain transcripts, scope slice 04 section 3).

Key Takeaways
- [E1][E2][E3] Six consumers, three distinct candidate kinds (document, plan, diff); only reflect requires a source input, and it routes the whole source only to one persona.
- [E1] `sc:workflow` passes `source.md` as reflect's `--spec` (`SKILL.md:89`), so a prompt-only source yields a one-line "spec" (W-3).
- [E3] Spec review for brainstorm/design is not wired today; PR review reads the PR body but not a linked issue; rf-qa receives a checklist, not a driving document.
- [E1][E2] Two verification methods exist: injection (deterministic, used by reflect qa) and transcript audit (used offline by E2).

---

## 6. Design input: `{{SOURCE}}` placeholder, shared grounding hunks, one brief template [E1][E2][E3]

Everything in this section is design input derived from the verified facts above; it is not implemented anywhere.

### 6.1 Placeholder set

Extend `## Values to fill` (`document_review_loop_prompts.md:15-21`) with:
- `{{SOURCE}}`: the driving document snapshot (reflect `--spec`, workflow `<pkg>/source.md`, PR linked issue/body, rf-qa task research prompt), with its sha256, mirroring how `{{CANDIDATE}}` carries a sha in `:32`.
- `{{SPEC}}` (optional): the referenced requirements document when `{{SOURCE}}` delegates to a file. Resolved by the orchestrator, not the reviewer (section 2.4 item 6 shows reviewers cannot resolve it without Bash). If not resolvable, the brief says so and findings that would need it are reported as grounding gaps (findings-v2 already has a `grounding-gap` channel, `findings_v2.py:37`).
- `{{GROUNDING}}`: orchestrator-rendered hunks (the reflect `## Grounding hunks` shape, `reviewer-spec.md:45-47`: H3 `path:line-range` + fenced verbatim excerpt) — this is where diff evidence (E3 Step 1), verification results (FR-4) and source excerpts go, so no reviewer needs Bash.
- Keep `{{CANDIDATE}}`, `{{BASELINE}}`, `{{PRIOR}}`, `{{N}}`, `{{IDS}}` as they are.

Test compatibility (section 1.6): add the placeholders to `## Values to fill` and put the source clause INSIDE the brief sentence (`- First-review brief: "...`) so `test_insertions_a_b_c_follow_their_brief_lines` (`test_review_rules_text.py:34-42`) still holds; `"src/superclaude" not in TEXT` (`:92`) is unaffected.

### 6.2 Brief wording

- First-review: "Review the candidate {{CANDIDATE}} (sha256) against {{SOURCE}} (sha256), the document it was built from, and against the requirements it states." Plus "If {{SOURCE}} is missing or unreadable, return incomplete" — this reuses the existing missing-input rule (`:32`) so a source-blind run fails loud instead of silently reviewing the candidate alone.
- Grading clause (D9 interaction, section 1.2): "A requirement {{SOURCE}} states that the candidate drops or contradicts is graded with the same blocking test as a stated text" — otherwise a source omission falls under "a requirement the document never states" and is capped at Medium (`:31`).
- Citation: findings must cite the source line for a source-based claim: findings-v2 `citations[]` with `role: source` (already legal, `findings_v2.py:35`) or `role: spec`. Update the brief role list (`reviewer-spec.md:39` says "plan or spec") to "plan, source or spec" so W-3 cannot recur silently: a `source` citation into a one-line prompt is then visibly different from a `spec` citation into the referenced document.

### 6.3 One template, per-consumer slots

A single template with fixed sections, rendered by code (section 2.4 shows orchestrator-written briefs drift from the template in 23 of 45 cases):

1. `## Task` — the consumer's brief sentence (first review / re-review / reflect pre / reflect post / PR / rf-qa) with `{{CANDIDATE}}`, `{{SOURCE}}`, `{{SPEC}}`.
2. `## Inputs` — a machine-readable list: role, repo-relative path, sha256, line count, "injected below" or "read it yourself". This is what `reflect-reviewer.md:52` (`spec_path`) already expects and what shadow09 improvised (`shadow09/reviewer-1.md:9-13`).
3. `## Grounding hunks` — reflect's shape (`reviewer-spec.md:41-59`), including the codegraph run-state line, diff evidence for re-reviews, verification results, and source hunks.
4. `## Lens` — persona slice (reflect T1 card excerpt + coverage slice) or empty for E3's "same brief" panels (`document_review_loop_prompts.md:70`).
5. `## Output contract` — the findings block line, rendered verbatim from one constant (today two strings: `document_review_loop_prompts.md:60` findings-v1 and `reviewer-spec.md:39` findings-v2).

Conflict with C7: reflect's "exactly three sections" (`test_shadow_skill_contract.py:146-165`) and the C6 rule that SKILL.md edits stay inside allowed sections (scope slice 03, C6) must be changed or retired together with this template; the reflect three sections map onto slots 3 and 4, and the shadow line onto slot 5.

### 6.4 Source exposure policy

- Inject the full source into EVERY reviewer's grounding hunks when it fits a size cap (reflect already uses 400 lines as the whole-file threshold for qa, `reviewer-spec.md:55`; E2 sources were 20-378 lines, section 3.2), instead of qa only. Rationale: E2 measured that a source pointer was ignored in 23% of runs (156/665, scope slice 01 H17); injection removes the dependency on reviewer behaviour. Cost note: reflect already accepts "roughly spec-length tokens to ONE T2 reviewer" (SKILL.md:1717); all-reviewer injection multiplies that by N (2-3 reflect reviewers; 3 in E2 panels). This trade-off is an open decision.
- Above the cap: per-section hunks for the persona, plus the path in `## Inputs` marked "read it yourself", plus a transcript check (section 5) recorded as `source_read: true|false|unknown` per reviewer in telemetry.
- Record per reviewer in the run record: `source_path`, `source_sha256`, `source_injected: whole|sections|none`, `source_read` — the field E2's `meta.json` lacked (`run-reviewer.sh:58`).

### 6.5 Read-only policy for the shared reviewer

- Use an allowlist agent (the `reflect-reviewer` pattern, `reflect-reviewer.md:5`) for in-session dispatch, and for `claude -p` dispatch use `--allowedTools Read Grep Glob` (or an equivalent allowlist) rather than a deny list under `bypassPermissions` (`run-reviewer.sh:48`). [design input; the exact `claude -p` allowlist flag behaviour is UNVERIFIED in this slice]
- Move every shell step out of briefs (E3 Step 1 `diff -w` and the `grep -nF` self-check, `document_review_loop_prompts.md:44`, `:46`) into the orchestrator, delivered as grounding hunks (the FR-4 pattern, `reviewer-spec.md:53`).

Key Takeaways
- [E3] Add `{{SOURCE}}` (+ optional `{{SPEC}}`, `{{GROUNDING}}`) to the existing Values-to-fill list; the existing tests allow it if the source clause stays inside the brief line.
- [E1][E2] Inject the source into every reviewer under a size cap; record `source_injected` and `source_read` per reviewer; the reflect qa-only injection and E2's pointer-only approach both leave reviewers source-blind.
- [E1][E3] Add `source` to the brief's citation roles (the parser already accepts it) and a grading clause for source omissions.
- [E1] Render briefs by code from one template; the recorded briefs show that orchestrator-written briefs do not keep the template shape.
- [E1][E2][E3] Use an allowlist for every dispatch path and move shell evidence into orchestrator-made hunks.

---

## Gaps and Questions

1. [UNVERIFIED] MR:142 ("37 of 38 pre runs escalated to T2, 34 by the parsed-sparse pre-filter") is taken from scope slice 04 section 0.1, not re-read here. The SKILL.md mechanism (`:284`, `:443`) is CODE-VERIFIED.
2. [UNVERIFIED] The 156/665 source-blind figure and its per-model split (COMBO-REPORT:373) and audit C's "no candidate was written" come from scope slice 01 (H17, H23); COMBO-REPORT itself was not re-read in this slice. The causal link "the brief does not name the source, so the reviewer did not open it" stays an inference (COMBO-REPORT:373 per HANDOFF D8).
3. [UNVERIFIED] Whether `superclaude review panel resolve`, `review merge` and `review ledger revise` (named at `document_review_loop_prompts.md:70`) are registered on this branch and on master; covered by the CLI slice.
4. [UNVERIFIED] Which installed skill version each of the 15 shadow runs used. All brief mtimes predate `c2e3347d3`; shadow12-15 postdate `9874d63fb`. File mtime is weak evidence (a copy could reset it).
5. [UNVERIFIED] Whether shadow runs used `--isolate-reviewers`; recorded briefs name the live worktree as `worktree_root` (`shadow04/reviewer-2.md:3`, `:21`), against `reflect-reviewer.md:131` ("Will Not: audit the live shared worktree").
6. [UNVERIFIED] `claude -p` allowlist behaviour (`--allowedTools` vs `--disallowedTools` under `bypassPermissions`) for a generic runner; not tested here.
7. [CODE-CONTRADICTED] Brief role list "plan or spec" (`reviewer-spec.md:39`) vs parser roles including `source`, `test`, `diff`, `artifact` (`findings_v2.py:35`).
8. [CODE-CONTRADICTED] `reflect-reviewer.md:52` says the orchestrator passes `spec_path`; the three-section template (`reviewer-spec.md:33-74`) has no such field and recorded briefs only carry it ad hoc (shadow09).
9. [CODE-CONTRADICTED] C7 "exactly three sections, shadow line inside T1 card excerpt" holds for the template text (`test_shadow_skill_contract.py:146-165`) but not for 23 of 45 recorded briefs; shadow10 put the shadow line in a fourth section. Nothing in code checks a produced brief.
10. [CODE-CONTRADICTED] SKILL.md:305 (L4) forbids live-execution instructions in briefs; `shadow09/reviewer-1.md:11` tells the reviewer to run `gh issue view 357`.
11. Question: should "source" (the producer's snapshot, `input-parse.md:41`) and "spec" (the referenced requirements document) be separate roles in the input contract? W-3 and shadow01/shadow09 say yes; today `sc-workflow-protocol/SKILL.md:89` passes `source.md` as `--spec`.
12. Question: should `sc:workflow` Wave 0 snapshot a file that an inline prompt names as its spec ("as specified in <path>")? Today only the prompt text is snapshotted (`input-parse.md:41`), so the referenced spec can change after planning and is not hashed.
13. Question: source-to-every-reviewer injection cost vs qa-only; no measurement exists. E2 measured only the cost of a source-blind pointer approach, not an injected one.
14. Question: the E2 judge has no source (`judge-one.sh:13-16`); a regression suite that scores source-coverage findings needs a judge brief with `{{SOURCE}}`.
15. Gap: spec review for `sc:brainstorm` / `sc:design` is not wired today (no `spec-panel` or review-loop call in `sc-brainstorm-protocol/SKILL.md` or `commands/design.md`); its source (the brainstorm brief or issue) is undefined.
16. Gap: PR review reads the PR body only to drop restated caveats (`sc-auggie-review-protocol/SKILL.md:229`) and never fetches a linked issue as a driving document.

## Stale Documentation Found

- **[STALE DOC]** `src/superclaude/agents/reflect-reviewer.md:3`, `:15` describe the agent as a UC-2 post-execution deviation auditor, while shadow mode and the parsed-sparse escalation use it for UC-1 pre-execution plan review (SKILL.md:311 per scope slice 03; recorded UC-1 briefs `shadow01/reviewer-2.md:3`).
- **[STALE DOC]** `src/superclaude/agents/reflect-reviewer.md:48-59` input list (`spec_path`, `tasklist_path`, `diff_scope`, `output_path`) does not match the brief template in `reviewer-spec.md:33-74`.
- **[STALE DOC]** `reviewer-spec.md:39` citation roles "plan or spec" lag the parser's six roles (`findings_v2.py:35`).
- **[STALE DOC]** HANDOFF D8 cites "the eval copy `tools/run-reviewer.sh:15`" as lacking the source; the brief spans `:13-17` and the source copy is at `:9-11` (scope slice 01 H18 already noted the nuance that `candidate.md:3` names `./source.md`).
- Naming hazard (not stale, but misleading): `test_older_pins_still_hold_and_no_source_path` (`test_review_rules_text.py:76-92`) pins "no `src/superclaude` path", not "no source document".

## Summary

No review brief in any of the three efforts names a driving document as a required input: the E3 first-review prompt reviews the candidate "against the requirements it states" with no `{{SOURCE}}` placeholder (`document_review_loop_prompts.md:17-21`, `:32`), and the E2 runner sends a filled copy of it (`run-reviewer.sh:13-17`) while only shipping `source.md` beside the candidate, which 156 of 665 runs never opened. Reflect (E1) injects the spec body for the qa persona only (`reviewer-spec.md:55`), and its three-section shape is pinned only as template text, broken in 23 of 45 recorded briefs. For workflow plans the "spec" is often a one-line `source.md` that delegates to another file, which is the mechanism behind W-3 (`input-parse.md:41`, `sc-workflow-protocol/SKILL.md:89`). Read-only enforcement differs: reflect uses a tool allowlist, E2 a deny list that leaves Bash auto-approved, and the E3 re-review step itself requires shell commands. Design input: one code-rendered brief template with `{{SOURCE}}`/`{{SPEC}}`/`{{GROUNDING}}` slots, source injected for every reviewer under a size cap, `source` citations plus a source-omission grading clause, `source_injected`/`source_read` per reviewer, and an allowlist reviewer with all shell evidence computed by the orchestrator.
