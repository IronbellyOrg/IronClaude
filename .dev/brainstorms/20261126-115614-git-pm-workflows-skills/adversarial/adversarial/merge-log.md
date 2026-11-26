# Merge Execution Log

## Metadata

- Base: Variant A
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (39 planned changes, 10 changes not made, revision notes for fix cycles 1 and 2)
- Final review applied: `refactor-plan-review-3.md` (PASS, 0 BLOCKING, 10 MINOR)
- Changes applied: 39 of 39 planned
- Status: success
- Timestamp: 2026-11-26T15:54:27Z (merge start; recorded in the merged document's header block)
- Output: `merged-output.md` (804 lines, 90 `<!-- Source: ... -->` comments, header block of three provenance comments before the H1)

Method: the base was copied with `cp`, then each change was applied in plan order with Edit (one change at a time). Edited regions were re-read at checkpoints (after Changes 5, 12, 31 and 36) and the whole outline was re-checked after the last change. The Round 3 debate files were not needed: every change that cites debate text has its full wording in the plan.

Conventions used in the merged text:

- Plan change numbers appear only inside provenance comments.
- Debate finding ids (INV-...), diff ids (C-011), unique-contribution ids (U-0xx), Round 2 entry ids (E6) and Variant B risk ids (R2, R10) appear only inside provenance comments. This applies review note M3-10 and extends it to the same class of id.
- Debate-only text is tagged `Debate Round 3, <ref> - merged per Change #<n>` or `Debate Round 2 ... - merged per Change #<n>`.
- Provenance text names variants only by the letters A, B and C.

## Orchestrator adjustments after post-merge validation

The executor's contradiction re-scan found 2 new contradictions and left them for a decision. The orchestrator resolved both from the text of the merged document itself (no new requirement, no new decision), then re-read the edited lines:

1. FR-035 (every `git commit` uses `--only` with a pathspec file) vs FR-038 and FR-117 (a pathless `/sc:git commit` commits the index exactly as staged). Resolved: FR-035 now names the pathless `/sc:git commit` as the one exception (`git commit -F <message file>`, no `--only`, no pathspec file). Medium severity.
2. FR-100 (legacy `commits.md` is never staged) vs its own last sentence (the terminal line "stays staged"). Resolved: the sentence now splits managed runs (staged with `.dev/tasks`) from legacy runs (never staged, stays in the untracked file). Low severity.

After these edits: new contradictions found by the executor 2, resolved 2, open 0. Post-merge validation status: passed. The open minor review notes (M3-2, M3-3, M3-7, M3-9 and the remaining parts of M3-4 and M3-6) stay listed below for the design step.

## Changes Applied

### Change 1: Complete placeholder table; separate source package from task package
- **Status**: Applied
- **Source**: Variant B, Path notation; Variant C, Path notation paragraph
- **Target**: Base §1.1; FR-060, FR-061 step 1, FR-062, FR-064, T-01
- **Before**: Two-column table of seven placeholders, including the false "only tracked file" claim for `<dev>`. `<pkg>` and `<run dir>` were overloaded for the task package.
- **After**: Three-column table (Placeholder | Meaning | How to resolve) of 11 rows, adding `<skill-dir>`, `<pkg-dir>`, `<run-dir>` and `<root-instructions>`. An "Aliases used by the source variants" paragraph follows, ending with the no-model-or-vendor-name sentence. The task-package uses now read `<pkg-dir>` and `<run-dir>`.
- **Provenance tag**: `<!-- Source: Base (original, modified) - table given a "How to resolve" column and ... rows from Variant B, Path notation; aliases of Variants B and C mapped; merged per Change #1 -->`
- **Validation**: Structural integrity pass | References pass | Contradictions pass

### Change 2: Glossary of terms used before their definition
- **Status**: Applied
- **Source**: Repository vocabulary listed in the plan
- **Target**: New §1.7 Terms
- **Before**: Section did not exist.
- **After**: A 12-row table: Q0..Q8, Q8a/R0/L0, Q0 pin and `q0-head`, Ruling, K3, WC-4, WC-9, WC-11, P4, TAMPER, LL-COMMIT/LL-PROTECTED, Boundary.
- **Provenance tag**: `<!-- Source: Base (original, modified) - glossary added for terms the base used before defining them ... merged per Change #2; ... M3-4(c) -->`
- **Validation**: pass | pass | pass

### Change 3: Root-cause section
- **Status**: Applied
- **Source**: Variant B, Section 2 (RC-1..RC-7); Variant C, Distribution (the RC-6 plugin-parity point)
- **Target**: New §1.6 Root causes
- **Before**: Section did not exist.
- **After**: RC-1..RC-7 at two to four bullets each, with aliases mapped. RC-5's front-matter sentence is dropped. RC-6 keeps the point that `make verify-sync` is not proof of plugin parity. RC-7 names no tools ("an existing marketplace commit plugin", "a tool that commits after every edit", and "its gone-branch cleanup" for the plugin's cleanup command). RC-5 says "configures", not "runs", so it agrees with the corrected §1.5 fact.
- **Provenance tag**: `<!-- Source: Variant B, Section 2 (RC-1..RC-7), shortened ... - merged per Change #3 -->`
- **Validation**: pass | pass | pass

### Change 4: Correct two baseline facts
- **Status**: Applied
- **Source**: Variant B, Section 10 R11; debate Round 2 evidence
- **Target**: §1.5 (one row replaced, one row added), FR-016, FR-031, Risk 2
- **Before**: The §1.5 row said messages "are checked by" `conventional-pre-commit`. FR-016 said `settings.json` was the only stageable path, with no mention of other tracked files.
- **After**: The §1.5 row says the hooks are configured, not installed, and the helper validates the message itself. A new row lists the tracked `<dev>/` files. FR-016 says tracking is not authority to stage. FR-031 adds the `dev-copy-path` refusal with no staging hint. The Risk 2 residual adds the "hooks not installed" sentence.
- **Provenance tag**: `<!-- Source: Base (original, modified) - the conventional-pre-commit row replaced ... merged per Change #4 -->` (§1.5); the FR-031 tag names Change #4
- **Validation**: pass | pass | pass

### Change 5: Section order (shared commit rules before their users)
- **Status**: Applied
- **Source**: Base
- **Target**: Whole document
- **Before**: §4 implement, §5 submodule, §6 shared rules, §7..§13.
- **After**:
  - New order: §4 shared rules (moved from §6), §5 submodule, §6 implement (from §4; subsections renumbered 6.1..6.7), a new empty §7 (commit state, recovery and owner resolution), then §8..§14.
  - Reference fixes: §1.4 "§4 explains why"; FR-008 "§10"; FR-072 "§6.3-§6.6 and §7"; FR-094 "(§6.3)"; the §3 table row's Extra guard "§6". D4's "(§5)" and FR-013's "§2.2" were checked and are unchanged.
- **Provenance tag**: per-section tags such as `<!-- Source: Base (original, modified) - section moved ahead of the sections that use it (was §6) per Change #5 -->`
- **Validation**: pass | pass (every § reference re-checked after the move) | pass

### Change 6: Helper moves to a mirrored skill script with versioned results
- **Status**: Applied
- **Source**: Variant B, Section 3.1 and FR-019; Variant C, FR-021 and NFR-006; base §2.3
- **Target**: §2.3 heading and paragraph, FR-008, FR-010, FR-013, new FR-019, AC-03, T-13, NFR-003, NFR-009, FR-060, FR-081, §1.3, the §2 intro, Risk 9
- **Before**: `<cli> vcs` group under `<pkg>/cli/vcs/` registered in `main.py`; four verbs; `rules.py`.
- **After**:
  - `vcs.py`, `vcs_rules.py`, `vcs_plan.py` and `vcs_submodules.py` under `sc-git-protocol/scripts/`, run with `uv run --no-project python "<skill-dir>/scripts/vcs.py"` and mirrored to `<plugin>`.
  - Seven verbs, with `stage-plan --candidate`, and one JSON object per verb carrying `vcs_contract: "1"`.
  - FR-019 resolves the helper and sets the `helper-missing` stops.
  - Every package-CLI name in the list above is replaced.
- **Executor harmonization (logged, not in the plan text)**: FR-010's `check-message` line now reads "reports `ok`, or `refused` with the violated rule in `reason`". The base text "prints `ok` or `refused: <rule>`" would contradict the plan's new sentence "Every verb prints one JSON object".
- **Provenance tag**: `<!-- Source: Base (original, modified) - module split ... location moved to a mirrored skill script ... (Variant B, Section 3.1 and FR-019) and versioned results added (Variant C, FR-021 and NFR-006); merged per Change #6 ... -->`; FR-019 is tagged `Variant B, Section 5.1 ... and Variant C, Section NFR-006 ... - merged per Change #6`
- **Validation**: pass | pass (B10 scan: no `<cli> vcs` and no bare `rules.py` left) | pass

### Change 7: Helper boundary (object writes disclosed, every repository write visible)
- **Status**: Applied
- **Source**: Variant B, Section 4.1 FR-019; Round 2 concessions of Variants B and C
- **Target**: FR-011, NFR-002
- **Before**: A 12-verb read-only allow-list, with "The helper performs no write".
- **After**: The plan's extended allow-list, including the private-index `read-tree`/`add`/`write-tree`, the submodule-read rule, the loose-object disclosure and the literal-Bash-call sentence. NFR-002 adds the printed path list and the separate verification call.
- **Provenance tag**: `<!-- Source: Base (original, modified) - allow-list extended with private-index verbs (Variant B, Section 4.1 FR-019) ... merged per Change #7 -->`
- **Validation**: pass | pass | pass (NFR-002's stale sentence was later fixed by M3-8)

### Change 8: Operation registry with lazy ref loading
- **Status**: Applied
- **Source**: Variant B, FR-004 and NFR-011; base FR-006..FR-008
- **Target**: New FR-018 in §2.2
- **Before**: No per-invocation ref limit.
- **After**: FR-018: at most two refs per invocation, reads never load `refs/safety.md`, plus the size-budget sentence (NFR-012).
- **Provenance tag**: `<!-- Source: Variant B, Section 3.2 (FR-004) and Section 12 (NFR-011, NFR-002 size limits) - merged per Change #8 -->`
- **Validation**: pass | pass | pass

### Change 9: Bare `/sc:git` runs status
- **Status**: Applied
- **Source**: Variant C, FR-007
- **Target**: FR-002, FR-004, T-12
- **Before**: `/sc:git status`; "no operation" was a STOP case.
- **After**: `/sc:git [status]`; "With no operation, `/sc:git` runs `status`."; T-12 adds "bare `/sc:git` runs status".
- **Provenance tag**: `<!-- Source: Base (original, modified) - bare invocation runs status (Variant C, Section FR-007) per Change #9; ... -->`
- **Validation**: pass | pass | pass

### Change 10: Unauthorized writes refused, no replayable commands
- **Status**: Applied
- **Source**: Variant B, FR-012; Variant C, FR-010
- **Target**: FR-020 (second half), new FR-023
- **Before**: A dry run that printed the exact commands.
- **After**: A refusal with the `authorization: ...` token and no command lines. FR-023 limits the grant scope to the repository and the named paths, branch or submodule target.
- **Provenance tag**: `<!-- Source: Base (original, modified) - FR-020 refuses ... (Variant B, Section 4 FR-012) per Change #10 -->`; `<!-- Source: Variant C, Section FR-010 ... - merged per Change #10 -->`
- **Validation**: pass | pass | pass

### Change 11: Protected-branch floor, additive local default, honest notice
- **Status**: Applied
- **Source**: Debate Round 2 C-017 resolutions; Variant B, FR-015/FR-037
- **Target**: FR-013 bullet 1, FR-032, Risk 6
- **Before**: The fixed set plus the `origin/HEAD` target; no notice; no detached-HEAD scope.
- **After**:
  - FR-013: an additive default plus names from the repository's own instructions, and submodules read their own refs.
  - FR-032: the `default branch unknown` notice and the local fix, and the detached-HEAD refusal in the receiving repository.
  - Risk 6: residual appended.
- **Provenance tag**: `<!-- Source: Base (original, modified) - ... protected-branch floor ... per Change #11 ... -->`
- **Validation**: pass | pass | pass

### Change 12: The write report states what changed; undo advice authorizes nothing
- **Status**: Applied
- **Source**: Variant B, FR-018; Variant C, NFR-001 and NFR-004
- **Target**: FR-022 (last two sentences)
- **Before**: Prints the new HEAD, its parent, and `git reset --soft <parent>`.
- **After**: Prints the checked preconditions, the argv, the result, HEAD before and after, and the index and worktree change. The undo advice is never run and authorizes nothing. No contents, credentials or credential-bearing URLs are printed.
- **Provenance tag**: `<!-- Source: Base (original, modified) - write report from Variant B, Section 4 FR-018 and Variant C, Section NFR-001 and NFR-004, merged per Change #12 -->`
- **Validation**: pass | pass | pass

### Change 13: Literal paths, deletions, gitlink prefixes, pathspec transport
- **Status**: Applied
- **Source**: Variant C, FR-018 and NFR-005; Round 3 rulings INV-007, INV-008, INV-012
- **Target**: New FR-035; FR-062 (a)-(e); FR-031; FR-063; T-02
- **Before**: Argv was `git add -- <paths>` / `git commit --only ... -- <paths>`.
- **After**: FR-035's NUL pathspec-file transport with `--literal-pathspecs`. FR-062 gets rules (a)-(e). FR-031 applies (c)-(e) to `/sc:git`. FR-063 and T-02 use the FR-035 shape. INV ids are kept out of the body.
- **Provenance tag**: `<!-- Source: Variant C, Section FR-018 and NFR-005 (literal path handling), with the debate Round 3 ruling INV-012 (pathspec transport) - merged per Change #13 -->`
- **Validation**: pass | pass | see new contradiction NC-1 (FR-035 versus the pathless `/sc:git commit` of FR-038)

### Change 14: Message format
- **Status**: Applied
- **Source**: Base FR-066; Variant B, FR-028 and FR-016 step 1; Variant C, FR-019; Round 3 ruling INV-015
- **Target**: FR-061 message step, FR-066, new FR-039
- **Before**: 72 characters; the in-package message file; no plan or boundary trailers.
- **After**:
  - FR-066: 72 code points without normalization, plus the `Implement-Plan:`, per-member `Implement-Task:`, `Implement-Boundary:` and `Implement-Ledger:` trailers, with attribution trailers after them.
  - FR-039: `/sc:git` messages are written to a temporary file outside the work tree.
  - FR-061 step 1 was edited for the interim state; its final wording comes from Change 25 step (2), as the plan directs.
- **Provenance tag**: `<!-- Source: Base (original, modified) - code-point length (debate Round 3 ruling INV-015); Implement-Plan trailer from Variant B ...; boundary-key trailer from Variant C ...; merged per Change #14 -->`
- **Validation**: pass | pass | pass

### Change 15: Hook outcomes (frozen-candidate classes, never an automatic retry)
- **Status**: Applied
- **Source**: Variant B, FR-021 and its Round 2 entry; Variant C, FR-020; Round 3 rulings INV-020, INV-029
- **Target**: New FR-036; FR-064 and FR-065 replaced; Risk 2
- **Before**: Two tokens (`blocked-by-host`, `commit-failed`); R0 re-planned automatically, including hook rewrites.
- **After**:
  - FR-036 defines seven classes.
  - FR-064 writes the sidecar refused line, saves the log, pins `rewritten/`, and bans retry and bypass.
  - FR-065 allows a later attempt only as FR-107 permits, after disclosure; `hook-rewrite-committed` goes to the owner choices.
  - Risk 2 gets the accepted unscanned-evidence residual and the owner follow-up.
- **Provenance tag**: `<!-- Source: Variant B, Section 4.1 FR-021 ... with the debate Round 3 rulings INV-020 and INV-029 - merged per Change #15 -->`; the §6.5 tag names Change #15
- **Validation**: pass | pass | pass

### Change 16: Commit positions, settle before advance, FINAL input rule
- **Status**: Applied
- **Source**: Base FR-057; Variant C, FR-013 and FR-022; debate Round 3 (INV-022)
- **Target**: FR-057 (appended), new FR-077 and FR-079 (placed in §6.3 after FR-059)
- **Before**: The positions, without the join or ordering detail.
- **After**: The appended Q8a/R0/L0 ordering paragraph; FR-077 settle before advance; FR-079 FINAL judges current files.
- **Provenance tag**: `<!-- Source: Debate Round 3 (settle before advance, ruling INV-022) with Variant C, Section FR-013 and FR-022 ... - merged per Change #16 -->`
- **Validation**: pass | pass | pass

### Change 17: Wave 0 preflight before the ledger; original branch captured
- **Status**: Applied
- **Source**: Base FR-054; Variant B, FR-022/FR-023; Variant C (Round 2); Round 3 ruling INV-002
- **Target**: FR-054 (replaced), FR-010 `preflight` fields
- **Before**: Eight bullet reasons, including `dirty`.
- **After**: The plan's paragraph with nine reasons (`not-person`, ..., `git-too-old`) and the inline-intake note, plus the flag-only `q0-branch` rule with `branch-changed` and `branch-unproven`. `symbolic_ref` is added to the preflight fields; `dirty` was removed from them in Change 6.
- **Provenance tag**: `<!-- Source: Base (original, modified) - placement after step 5 kept; ... dirty reason removed; branch capture from the debate Round 3 ruling INV-002; merged per Change #17 -->`
- **Validation**: pass | pass | pass

### Change 18: STOP table, transient stops and the archive gate
- **Status**: Applied
- **Source**: Base FR-070; debate Round 3 (INV-023)
- **Target**: FR-070 (replaced)
- **Before**: Two codes with a `COMMIT: refused` ledger effect.
- **After**:
  - Two rows with single-valued columns, and the open reason class with its listed reasons, including `helper-missing`.
  - Two transient `E-RESUME-NEEDED` reasons, with the rule for which code a lock gets.
  - The archive-gate refusal `E-ARCHIVE-BLOCKED reason=unsettled-boundary`; its "**INV-023.**" label is dropped from the body.
  - The revised `SKILL.md:51` sentence.
- **Provenance tag**: `<!-- Source: Base (original, modified) - two STOP codes kept; open reason class, transient E-RESUME-NEEDED reasons and the archive-gate refusal from the debate Round 3 text (ruling INV-023); merged per Change #18 -->`
- **Validation**: pass | pass | pass

### Change 19: The person's edits (accepted-tree pin, `changed-after-review`, `foreign-change`)
- **Status**: Applied
- **Source**: Variant B, FR-027 items 2-3; Variant C, FR-017; Round 3 rulings INV-003, INV-025
- **Target**: New FR-073, FR-074, FR-075 in §6.4; Risk 4
- **Before**: The Wave 0 `dirty` refusal was the only protection.
- **After**: The three requirements. Risk 4 is rewritten with its new mitigation and the single-writer residual.
- **Provenance tag**: `<!-- Source: Variant B, Section 5.3 FR-027 items 2-3 ... and Variant C, Section FR-017 ..., with the debate Round 3 rulings INV-003 and INV-025 - merged per Change #19 -->`
- **Validation**: pass | pass | pass

### Change 20: Commit scope (own package as literal files; `/sc:git commit` never widens)
- **Status**: Applied
- **Source**: Base FR-062 and D8; Round 3 rulings INV-018, INV-024
- **Target**: New FR-076 (§6.4), new FR-038 (§4), FR-033, FR-062 bullets 1-2 and the new S definition
- **Before**: `commit_paths` came from "pending tasks' latest `complete` lines", and the package directory was included as a directory.
- **After**:
  - FR-062 builds `commit_paths` from the anchor `complete` lines and holds the single definition of S. The managed sentence uses the FR-076 literal-file expansion and staging by FR-061 step (5).
  - FR-076 adds the package expansion and its accepted risk.
  - FR-038 sets the `/sc:git commit` staging order, and FR-033 points the pathless case at FR-038.
- **Provenance tag**: the FR-062 tag names Change #20; `<!-- Source: Base (original, modified) - base FR-062 and D8 package rule refined to literal files by the debate Round 3 ruling INV-018 ... merged per Change #20 -->`; FR-038 is tagged `Variant B (its version of the debate Round 3 ruling INV-024 ...) - merged per Change #20`
- **Validation**: pass | pass | see NC-1

### Change 21: Distinct implement-side ref name and two-part load rule
- **Status**: Applied
- **Source**: Variant B, FR-032
- **Target**: FR-072, T-09
- **Before**: `refs/commit.md`, loaded only with the flag.
- **After**: `refs/commit-step.md`, loaded when the flag is present or `commits.md` exists. It has "Reconcile and settle" and "Commit procedure" parts, the `/sc:git` side lives in `refs/safety.md`, and the `SKILL.md` budget is 15 lines. T-09's clause is updated. The analogy clause "the same way `refs/retry.md` is loaded only when needed" is kept from the base.
- **Provenance tag**: `<!-- Source: Base (original, modified) - section references renumbered per Change #5; ref renamed refs/commit-step.md (Variant B, Section 5.5 FR-032) ... per Change #21; ... M3-6 ... -->`
- **Validation**: pass | pass | pass (load rule consistent with FR-019, FR-051, NFR-018, T-09, T-16 and AC-08)

### Change 22: Commit state in a sidecar, not the task ledger
- **Status**: Applied
- **Source**: Variant B, FR-029; Variant C, FR-022/FR-023; debate Round 2
- **Target**: FR-068 and FR-069 deleted; FR-060 record forms; FR-071; Risk 3; new FR-100 (§7.1)
- **Before**: Four `COMMIT:` ledger records and the `_COMMIT` archive parser change.
- **After**:
  - FR-068 and FR-069 are removed; a deletion note sits in the §6.7 provenance comment.
  - FR-060 `nothing` writes `commit skipped ... reason=empty`, and `refused` records in the FR-064 form.
  - FR-071 reads the `commits.md` `sha=`/`recovered` lines.
  - Risk 3 now covers a sidecar format change.
  - FR-100 holds the sidecar location and six line forms. "FR-054's INV-002 rule" becomes "FR-054 or its branch check", and "(U-017)" moved to provenance.
- **Provenance tag**: `<!-- Source: Variant B, Section 5.5 FR-029 (sidecar commits.md) and Variant C, Section FR-022 and FR-023 ... - merged per Change #22 -->`
- **Validation**: pass | pass (no `COMMIT:` token left in the body; nothing references FR-068 or FR-069) | see NC-2 (FR-100 staging sentence for legacy runs)

### Change 23: Run-scoped grant, ledger segments, first-complete eligibility
- **Status**: Applied
- **Source**: Debate Round 3 text for INV-001 (items 1-9); Round 2 A-003 resolutions; rulings INV-014, INV-011
- **Target**: FR-050 (appended), FR-051 (replaced), FR-055 (deleted), FR-056, FR-058, FR-094, new FR-101..FR-109 (§7.2)
- **Before**: The `COMMIT: on` marker, the old "pending" definition, and a resume rule that wrote no `COMMIT:` line.
- **After**:
  - FR-050: the grant paragraph and the accepted stale-copy residual, labelled "Accepted residual:" in place of the INV-011 id.
  - FR-051: the `off` run line.
  - FR-055 removed, with a deletion note in provenance.
  - FR-056: the terms pointer and the new trigger.
  - FR-058: the batch rule; the "**INV-014:**" label is dropped.
  - FR-094: the trigger and settle-before-advance phrase.
  - FR-101..FR-109, with the FR-107 state table indented under its item.
- **Provenance tag**: `<!-- Source: Debate Round 3, INV-001 items 1-9 ... and the ruling INV-014 - merged per Change #23 -->`; the FR-050/FR-051, §6.3 and FR-094 tags name Change #23
- **Validation**: pass | pass | pass (each of "eligible", "due", "pending", "settled" and "unsettled" has a single definition; see the open notes for inherited edges)

### Change 24: `--commit-tasks` scope (person provenance first, contradiction removed)
- **Status**: Applied
- **Source**: Base FR-052 and T-15; Variant B, FR-022
- **Target**: FR-052, T-15
- **Before**: The allowed files omitted `WORKER-CONTRACT.md`, which contradicted FR-091.
- **After**: The runtime check is the guard; a static list of seven files including `WORKER-CONTRACT.md` and the plugin copies; primitives defined. T-15 lists exactly those paths.
- **Provenance tag**: `<!-- Source: Base (original, modified) - runtime person check first ... per Change #24 -->`
- **Validation**: pass | pass | pass

### Change 25: Boundary procedure, verification and pin lifetime
- **Status**: Applied
- **Source**: Debate Round 2 C-010 resolutions; Round 3 ruling INV-004; Variant B, FR-029; Variant C, FR-022
- **Target**: FR-061 (step list replaced), FR-060 `ok` branch, new FR-130..FR-133 (§7.5)
- **Before**: Six steps; a crash between the commit and its record was recorded as `no-changes`.
- **After**: The nine-step ordered procedure (message step from Change 14); FR-130 `verify`, FR-131 pin lifetime, FR-132 retry inputs, FR-133 no lock. "(C-011)" and "INV-004" moved to provenance.
- **Executor harmonization (logged)**: the plan's step (1) is the `stage-plan` call, which FR-060 already makes. To avoid running `stage-plan` twice, FR-061's lead-in says step (1) is the FR-060 call and steps (2)-(9) run only on `ok`, and FR-060's `ok` branch reads "continue with FR-061 step (2)". The plan lists "FR-060 (`ok` branch)" as a target without giving text.
- **Provenance tag**: the §6.4 tag names Change #25; `<!-- Source: Debate Round 2 C-010 resolutions ... the debate Round 3 ruling INV-004, and Variant C, Section FR-022 - merged per Change #25 -->`
- **Validation**: pass | pass | pass

### Change 26: Worktree recovery snapshot and outside-S comparison
- **Status**: Applied
- **Source**: Debate Round 3 text for INV-021 (items 1-9)
- **Target**: New §7.3 with FR-110..FR-118
- **Before**: Only the Wave 0 `dirty` pre-check, removed in Change 17.
- **After**: The nine requirements as written in the plan.
- **Provenance tag**: `<!-- Source: Debate Round 3, INV-021 items 1-9 ...; replaces the base Wave 0 dirty pre-check - merged per Change #26 -->`
- **Validation**: pass | pass | pass

### Change 27: Owner resolution of an unsettled boundary
- **Status**: Applied
- **Source**: Debate Round 3 text for INV-027 (items 1-7)
- **Target**: New §7.4 with FR-120..FR-126; the FR-010 `resolve-check` verb (already listed by Change 6)
- **Before**: `uncertain` was a dead end.
- **After**: The two record forms and their regexes (inside code spans), the information-before-choice, who-may-answer, `resolve-check`, meaning, idempotence and test requirements.
- **Provenance tag**: `<!-- Source: Debate Round 3, INV-027 items 1-7 ... - merged per Change #27 -->`
- **Validation**: pass | pass | pass

### Change 28: Migration inventory
- **Status**: Applied
- **Source**: Base FR-017 and T-14; Variant B, FR-009, FR-010 and §9.2; debate Round 2
- **Target**: FR-017 (appended), new FR-078 (placed in §6.6 after FR-067, beside the other Ruling rule), T-14 (replaced)
- **Before**: T-14 had four items.
- **After**: FR-017 keeps `/sc:pr-submit` out of the route steps. FR-078 sets the Ruling text when commits are on. T-14 holds the full consumer inventory; "the archive gate (Change 18)" is written "(FR-070)".
- **Provenance tag**: `<!-- Source: Debate Round 2 (Variant A's note on refs/retry.md:504 and Variant B's note on the Ruling cost-if-wrong) - merged per Change #28 -->`; the §2.5 and §10 tags name Change #28
- **Validation**: pass | pass | pass

### Change 29: Submodule status (independent facts plus one derived state)
- **Status**: Applied
- **Source**: Variant C, FR-024/FR-025; base FR-040; Variant B, FR-033; debate Round 2
- **Target**: FR-040 (replaced)
- **Before**: A closed list of eight states.
- **After**: Nullable fact fields, one derived state with fixed precedence (10 states), unset versus false, sorted rows, an empty list when there are no submodules.
- **Provenance tag**: `<!-- Source: Base (original, modified) - closed state list kept as one derived state with fixed precedence over independent nullable facts (Variant C, Section FR-024 and FR-025; ...), merged per Change #29 -->`
- **Validation**: pass | pass | pass

### Change 30: Submodule update (no orphaned commits, approved URL, partial results)
- **Status**: Applied
- **Source**: Variant B, FR-034 and FR-037b; Variant C, FR-026 and FR-028; Round 3 rulings INV-009, INV-010
- **Target**: FR-002 submodule form, FR-041, new FR-044..FR-046, NFR-001, T-07, §1.4 bullet, FR-005, T-12
- **Before**: An update for `pointer-moved` with no ancestry check; NFR-001 claimed no remote access, which contradicted the clone that `update --init` performs.
- **After**:
  - FR-002 gains the `--url` form. FR-041 is the ancestry-checked update with the 128-exit rule and revalidation.
  - FR-044 sets the URL-repeat rule and `remote-mismatch`, FR-045 the partial results, FR-046 the guard denial.
  - NFR-001 states its single exception. §1.4 and FR-005 say "fetch on its own" with the exception. T-07 and T-12 are extended.
- **Provenance tag**: `<!-- Source: Variant C, Section FR-026 and FR-028 ... with the debate Round 3 ruling INV-010; Variant B, Section 6 FR-037b ... - merged per Change #30 -->`; the FR-041, NFR-001, §1.4 and §2.1 tags name Change #30
- **Validation**: pass | pass | pass (the fetch exception is consistent across §1.4, §3, FR-004, FR-005, FR-041, FR-042, FR-044, NFR-001, D4 and T-12)

### Change 31: Pointer commit
- **Status**: Applied
- **Source**: Variant B, FR-035; Variant C, FR-027/FR-028; debate Round 2; Round 3 ruling INV-030
- **Target**: FR-042 (replaced). D4 is replaced in Change 38.
- **Before**: Warned and committed; required a submodule HEAD on a branch.
- **After**: Six numbered conditions, containment only through the `.gitmodules` remote, the honest last-fetch wording, a one-path commit using the FR-035 argv, a post-commit gitlink check, and residuals.
- **Provenance tag**: `<!-- Source: Base (original, modified) - clean module, submodule-unpublished refusal ... (debate Round 3 ruling INV-030); merged per Change #31 -->`
- **Validation**: pass | pass | pass

### Change 32: Branch cleanup routing names every `/sc:worktrees` verb
- **Status**: Applied
- **Source**: Variant C, FR-029; Variant B, FR-039
- **Target**: FR-080 (replaced); the `branch list` description in FR-007 (`refs/status.md` bullet)
- **Before**: Printed only `list` and `prune`.
- **After**: Prints `list`, `archive` (which writes even without `--apply`), and `retire`/`prune` (which remove only with `--apply`). The `[gone]` note is added to `branch list`.
- **Provenance tag**: `<!-- Source: Variant C, Section FR-029 (route names every /sc:worktrees verb, unique contribution U-020) - merged per Change #32 -->`; the §2.2 tag names Change #32
- **Validation**: pass | pass | pass

### Change 33: Delivered K3 rule
- **Status**: Applied
- **Source**: Base FR-091/FR-092; Variant B, FR-040; Variant C, FR-032
- **Target**: FR-091 (replaced), FR-092 (unchanged; WC-4 is now in §1.7), T-18
- **Before**: The K3 rewrite without positions, the WC-9 quote or the refs line.
- **After**: The plan's FR-091 text. T-18 names `tests/skills/test_worker_contract.py`.
- **Provenance tag**: `<!-- Source: Base (original, modified) - delivered K3 rule ... (Variant B, Section 8 FR-040; Variant C, Section FR-032), merged per Change #33 -->`
- **Validation**: pass | pass | pass

### Change 34: Non-functional requirements
- **Status**: Applied
- **Source**: Variant C, NFR-001/003/007; Variant B, NFR-002/003/005/007/010
- **Target**: NFR-006, NFR-007, NFR-010, NFR-011 (edited); NFR-012..NFR-018 (appended); FR-013 `MIN_GIT` bullet
- **Before**: NFR-001..NFR-011, with `MIN_GIT = (2, 23)`.
- **After**: The edits, seven new NFRs, and a `MIN_GIT` bullet that matches NFR-011. Per-requirement provenance tags were added across §11.
- **Provenance tag**: `<!-- Source: Variant B, Section 12 ... and Variant C, Section NFR-001, NFR-003 and NFR-007 - merged per Change #34 -->`
- **Validation**: pass | pass | pass

### Change 35: Test obligations
- **Status**: Applied
- **Source**: Base §9 table; Variant B, §9.2; Variant C, FR-034; Round 3 test lists
- **Target**: T-01, T-04, T-06, T-07, T-08, T-10, T-11, T-16, T-18 (edited); T-19..T-27 (appended)
- **Before**: 18 rows with `COMMIT:` ledger assumptions.
- **After**: 27 rows. T-01's boundary cases moved to T-19 in the merged terms, and T-01 says so in one sentence. T-04 covers the FR-036 classes. T-10 is the sidecar parity test. T-11 is the archive gate. T-16 covers the `off` run line. T-07's text names the requirements, not change numbers.
- **Provenance tag**: the §10 section tag lists every row change with its change number
- **Validation**: pass | pass (every T id resolves) | pass

### Change 36: Acceptance criteria with runnable observations
- **Status**: Applied
- **Source**: Variant B, §13; base §13
- **Target**: §14: Observation column; AC-05, AC-07, AC-08, AC-12 edited; AC-16..AC-21 appended
- **Before**: 15 criteria with three columns.
- **After**: 21 criteria with four columns and the sentence "A behavioural test outranks a text count." Observation cells were then reassigned under M3-1.
- **Mechanical reference fixes (logged)**:
  - AC-05's Check gains T-19, because Change 35 moved the boundary cases from T-01 to T-19.
  - AC-06's "T-01 (batch case)" becomes "T-19 (batch case)".
  - AC-12's Check is T-11, the test the plan's AC-12 text names.
- **Provenance tag**: `<!-- Source: Base (original, modified) - AC-to-test mapping kept; Observation column ... from Variant B, Section 13; ... per Change #36; ... M3-1 ... -->`
- **Validation**: pass | pass | pass

### Change 37: Risk table with root causes and ratings
- **Status**: Applied
- **Source**: Variant B, §10; Round 3 residuals
- **Target**: §12
- **Before**: 14 rows with four columns.
- **After**: Seven columns (# | Risk | Root cause | Likelihood | Impact | Mitigation | Residual) and 23 rows. The plan's ratings are used; row 1 gains the deny-rule follow-up and row 13 is reworded. INV ids and Variant B risk ids are in provenance only.
- **Executor note (logged)**: the plan gives no root-cause text for the base rows or mitigation/residual text for rows 15-23. Root causes were taken from the matching Variant B §10 row (rows 1, 2, 4, 5, 9, 10, 12, 16, 22, 23) or from the row's own cited evidence and the plan rationale (rows 3, 6, 7, 8, 11, 13, 14, 15, 17-21). New-row mitigations and residuals restate the cited requirements; no new requirement was added.
- **Provenance tag**: `<!-- Source: Base (original, modified) - root-cause, likelihood and impact columns from Variant B, Section 10 ...; rows 15-23 added ...; merged per Change #37; ... M3-8 -->`
- **Validation**: pass | pass | pass

### Change 38: Decisions under the merged design
- **Status**: Applied
- **Source**: Base §12 D1..D8; Variant B, §11 Q6 and D-7
- **Target**: §13: mapping line; D1-D4 and D8 replaced; D6 and D7 appended; D9-D11 added
- **Before**: D1-D4 and D8 described the `<cli> vcs` helper, `refs/commit.md`, the plain flag and the package directory.
- **After**: The plan's texts. The D6 additions keep Variant B's citations (`WORKER-CONTRACT.md:302`, `:244`).
- **Provenance tag**: `<!-- Source: Base (original, modified) - D1-D4 and D8 restated ... merged per Change #38 -->`
- **Validation**: pass | pass | pass

### Change 39: Seed constraints kept (checklist)
- **Status**: Applied
- **Source**: Seed brief constraints; base §1.4
- **Target**: New §1.8
- **Before**: Section did not exist.
- **After**: An 11-row table (Constraint | Kept by); every cited id resolves.
- **Provenance tag**: `<!-- Source: Base (original, modified) - checklist of the seed brief's constraints ... merged per Change #39 -->`
- **Validation**: pass | pass | pass

## Post-Merge Validation

### Structural Integrity

- Heading hierarchy: pass. The first heading is the H1. Only the three provenance header comments come before it, and the first non-comment line is the H1 (line 5). Levels run H1 → H2 → H3 with no gaps, and there are no H4 headings.
- Section ordering: pass. §1 (1.1-1.8), §2 (2.1-2.5), §3, §4, §5, §6 (6.1-6.7), §7 (7.1-7.5), §8-§14, in the order Change 5 sets. Requirement blocks keep base ids; new ids are exactly as the plan assigns.
- Orphaned subsections: none. Every H3 sits under its H2.
- Document flow: pass. Every heading is followed by a `<!-- Source: ... -->` comment (checked mechanically). There are 90 source comments, all single-line.
- §7 subsection headings: the plan names only "7.x Protecting work outside the commit set". The executor created 7.1-7.5 and ordered them by id (FR-100; FR-101..FR-109; FR-110..FR-118; FR-120..FR-126; FR-130..FR-133).

### Internal References

Counts cover the body text only. Provenance comments are excluded, because they cite source-variant ids such as "Variant B, FR-016".

- Total references: 592 tokens (each id's own defining mention included):
  - 449 FR/NFR tokens to 122 distinct ids;
  - 93 T/AC tokens to 48 distinct ids;
  - 22 D tokens to 11 distinct ids;
  - 28 internal § tokens to 12 distinct sections.
- Out of scope: 6 further § tokens point into external documents (developer guide §3.1 and §5.6; `research-deep.md` §1 and §3).
- Resolved: 592.
- Broken: 0. The deleted ids FR-055, FR-068 and FR-069 have no remaining reference.
- Mechanical fixes made during the merge:
  - the Change 5 § renumbering (6 sites);
  - AC-05 and AC-06 Check cells pointed at T-19 after the T-01 split;
  - T-14's change-number citation replaced by FR-070;
  - FR-100's "FR-054's INV-002 rule" replaced by "FR-054 or its branch check".

### Contradiction Re-Scan

New contradictions introduced: 2. Neither is fixed, because each needs a decision the plan does not make.

- **NC-1 (Medium): pathless `/sc:git commit`, FR-035 versus FR-038 and FR-117.**
  - FR-035 says every `git commit` in the spec runs as `git --literal-pathspecs commit --only ... --pathspec-from-file=<file>`.
  - FR-038 says a pathless `/sc:git commit` freezes the index change set as S and "commits the index as the person staged it". FR-117 repeats that S.
  - `git commit --only <paths>` commits the working-tree content of those paths, so passing the frozen index change set through the FR-035 form would commit unstaged edits of partially staged files. That widens the commit FR-038 says never widens.
  - Possible resolutions for the owner: exempt the pathless form from `--only` and pathspecs (a plain `git commit -F <file>`), or say how S is transported for it.
- **NC-2 (Low): FR-100, terminal-line staging in legacy runs.**
  - FR-100 says legacy `<run-dir>/commits.md` is never staged.
  - The same requirement then says, without limiting it to managed runs, that a terminal line "stays staged and enters the next boundary commit; after the last boundary it stays staged".
  - For a legacy run that sentence cannot hold. The intended reading is evidently managed runs only.

Checked with no new contradiction:

- The commit-boundary terms (due, eligible, pending, prepared, settled, unsettled, uncertain) each have the single meaning FR-103, FR-105, FR-107 and FR-108 give them. Every "pending" in the body uses the FR-107 meaning. The known edges are inherited from Round 3 (M3-2, M3-4) and listed below.
- The load rule of `refs/commit-step.md`: FR-072, FR-019, FR-051, FR-101, NFR-018, T-09, T-16 and AC-08 agree (flagged run, or any run where `commits.md` exists, with only the "Reconcile and settle" part when unflagged). Nothing else says "loaded only with the flag".
- The fetch exception for `submodule update`: consistent across §1.4, the §3 forbidden row, FR-004, FR-005, FR-041, FR-042, FR-044, NFR-001, D4 and T-12.
- The seed constraints:
  - no push, merge or PR in `/sc:git`: FR-002, FR-004, FR-005, D7, NFR-001;
  - no relay: FR-019, FR-072, D2;
  - PRs stay with `/sc:pr-submit`: §1.4, FR-004;
  - local branch cleanup by reuse only: FR-080, FR-081, FR-082;
  - no remote branch deletion: FR-081, AC-11.
  
  The only `update-ref -d` calls touch `refs/<package>/...` pins, and NFR-017 forbids `refs/heads/*`.

Watch items. These are wording tensions or factual risks, not contradictions:

- (a) FR-022 says no write asks for a second confirmation, while FR-044's URL repeat works like one for a clone. §1.8 already frames FR-044 as the confirmation for that case.
- (b) "eligible" also appears in FR-042 for submodule targets, a different domain from FR-103.
- (c) NFR-001 cites only FR-044 for its exception, while §1.4 and FR-005 cite FR-041 and FR-044. The fetch for `target-not-local` is authorized under FR-041.
- (d) AC-21 repeats AC-14.
- (e) §2.3's claim that the launch-level guard's word classifier does not match `.../sc-git-protocol/scripts/vcs.py` comes from the plan and is not verified here. The path contains "git" between hyphens, and Variant B's evidence says the guard matches a git word in the command text.

### Banned-name check

`grep -inE 'claude|opus|sonnet|haiku|gpt|gemini|anthropic|openai'` over the merged document, comments included, prints nothing (0 hits). The placeholder-alias table of Variant A is kept and completed per Change 1.

## Summary

- Total changes planned: 39
- Successfully applied: 39
- Failed: 0
- Skipped: 0
- Changes not made, per the plan's table (base kept): 10 diff points (S-001, S-004, S-012, C-001, C-002, X-002, X-003, X-009, X-011, X-012). No edits were needed for them.
- Executor harmonizations, all mechanical and logged under their changes:
  - FR-010 `check-message` wording;
  - FR-060/FR-061 step-(1) handoff;
  - AC-05/AC-06 checks pointed at T-19;
  - risk-table root-cause and new-row cells;
  - "Accepted residual:" labels in place of INV ids;
  - §7 subsection headings;
  - FR-078 placed in §6.6;
  - RC-5 "configures".
- Post-merge validation: PASS for structure and references (0 broken). The contradiction re-scan found 2 new contradictions (NC-1, NC-2), listed above and not fixed.

## Open minor notes (refactor-plan-review-3.md)

| Note | Result | Reason |
|---|---|---|
| M3-1 | Applied | AC-03's observation is now `vcs.py --help` lists the seven verbs. The parity `cmp`/`diff -r`, `make verify-sync` and the `commands/` count are under AC-04. AC-05's observation is adapted from Variant B's AC-09: two flagged tasks give two commits and two `commit sha=` lines. The fix keeps every observation the plan lists and only moves it to the criterion it tests. |
| M3-2 | Open | The fix would change FR-108's Round 3 text, which the plan says to keep as written. An attempt that has a prepared line but no pins, with HEAD at the parent, is still "pending" in FR-107 and "uncertain" in FR-108. Both readings fail safe. |
| M3-3 | Open | Adding the "prepared, no terminal line, HEAD ≠ parent" row and moving the `recovered` clause would rewrite the FR-107 table, which the plan says to keep as written. FR-108, FR-109, T-22 and AC-16 still pin the behaviour. |
| M3-4 | Partly applied | (c) is applied: the Boundary row in §1.7 now says an anchor is eligible when it lies in an `on` segment. (a) and (b) are open: both would change Round 3 FR-105 text or add a new attempt-numbering rule. |
| M3-5 | Applied | FR-050 now says that after a revocation line the run counts as "any other run" for FR-056 and FR-107, and that a boundary already due stops `unsettled`. This narrows the grant and agrees with "plain words can narrow the grant, never widen it". |
| M3-6 | Partly applied | The placement part is applied: FR-072 puts FR-019's implement clause and FR-071 in "Reconcile and settle" and FR-078 in "Commit procedure". Open: whether `verify` (or `reconcile`) runs the FR-113 comparison in unflagged runs, where the review's own wording leaves the choice open, and the "recompute damage from its pin on every run" rule, which would be a new behaviour. |
| M3-7 | Open | The fix would replace the helper resolution order that FR-019 and the `<skill-dir>` row state explicitly. It fails safe (`helper-missing`), and the plugin system is not yet available. |
| M3-8 | Applied | All four parts: NFR-002 reads "writes no ref, no user index, no work-tree file and no config (FR-011)"; the Risk 2 mitigation reads "FR-036 classes; STOP; a later flagged run retries only as FR-065 and FR-107 allow"; FR-033 follows FR-036 and FR-064's no-retry rules with rewritten pins under `refs/<package>/git/`; FR-061 step (3) names the agent as the writer of `commit-paths-<key>-a<n>.txt`. |
| M3-9 | Open | The suggested fixes offer alternatives (the evidence for quiescence, a renewed review versus restore-or-abandon, which position writes the mixed-batch line), so none is unambiguous. The gaps are inherited from Round 3 and fail safe through `abandon`. |
| M3-10 | Applied | INV ids appear only in provenance comments. The same treatment covers diff ids (C-011), unique-contribution ids (U-009, U-017, U-021), the Round 2 entry id (E6) and Variant B risk ids (R2, R10); a body scan finds none of them. |
