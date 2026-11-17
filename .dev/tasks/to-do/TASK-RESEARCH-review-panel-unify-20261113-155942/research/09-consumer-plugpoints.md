# Research: Consumer plug points and the review CLI surface

**Investigation type:** Integration Mapper
**Scope:** `src/superclaude/skills/sc-workflow-protocol/SKILL.md`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/commands/design.md`, `src/superclaude/commands/spec-panel.md`, `src/superclaude/rules/prompts/document_review_loop_prompts.md`, `src/superclaude/cli/review/__init__.py` (this branch and `origin/master`), `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (escalation rule), Grep of `superclaude review|review_ledger|review panel resolve` over `src/superclaude/{skills,commands,core}`, installed-only `~/.claude/commands/sc/spec-panel-{armb,diffgate,ledger,ponytail,stoprule}.md` (names and descriptions)
**Status:** Complete
**Date:** 2026-11-14

---

## 1. The `superclaude review` CLI surface: this branch versus `origin/master` (Q7, Q4)

Refs used: HEAD = `792cf8c52` (ironbelly/shadow-runs); `origin/master` = `d2d8a2d16` (#519). `git merge-base --is-ancestor origin/master HEAD` succeeded, so master is an ancestor of this branch. The local `master` ref was not used.

### 1.1 Registration chain

- `src/superclaude/cli/main.py:568` imports `review_group` from `superclaude.cli.review`; `:570` registers it as `main.add_command(review_group, name="review")` [CODE-VERIFIED]. [E3, E1]
- `src/superclaude/cli/review/__init__.py:14-16` defines the click group `review`. `:19-29` lists nine module names (`panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `lint_cmd`, `estimate_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`); `:30-35` imports each and, on `ModuleNotFoundError` whose `.name` is exactly that module, silently `continue`s; `:36` registers `_module.command`. The docstring `:3-4` states the intent: "Subcommand modules are optional, so branches that add different subcommands merge without touching this file." [CODE-VERIFIED] [E3 for the loader and first six names, E1 for the last three]
- `git diff --stat origin/master HEAD -- src/superclaude/cli/review` is empty: the review package is **byte-identical** between this branch and `origin/master`. The shadow-runs commits after #519 did not touch it. [E1, E3]

### 1.2 History of the loader list

- Pre-#519 (`git show d2d8a2d16^:src/superclaude/cli/review/__init__.py`): the tuple held six names, ending at `estimate_cmd`; the package had `findings.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `panel.py`, `panel_cmd.py`, `telemetry.py`, `telemetry_cmd.py`, `data/` only. [E3]
- #519 (`d2d8a2d16`, E1's Stage 0-2 reflect panel work) appended `cluster_cmd`, `verify_cmd`, `manifest_cmd` and added `card_convert.py`, `cluster.py`, `cluster_cmd.py`, `findings_v2.py`, `manifest.py`, `manifest_cmd.py`, `verify_cmd.py`. [E1]
- `git log -S '"lint_cmd"' origin/master -- .../__init__.py` points at `9163bd1c7` (the #498 merge of 346Claude-integration). [E3]

### 1.3 Full subcommand surface (identical on both refs)

Verified by reading the decorators and by `uv run superclaude review --help` (read-only, run 2026-11-14):

| Subcommand | Defined at | Origin | In-repo caller in `src/superclaude/{skills,commands,core}` |
|---|---|---|---|
| `review panel resolve` | `panel_cmd.py:13` group, `:18` | E3 (reflect options added by E1) | `sc-reflect-protocol/SKILL.md:340` (shadow step 1) [E1]; prompts file `document_review_loop_prompts.md:70` is outside the grepped dirs (section 6) |
| `review panel validate` | `panel_cmd.py:111` | E3 | none |
| `review merge` | `merge_cmd.py:21`, body `:71` | E3 | none |
| `review ledger revise / defer / verdict / capture` | `ledger_cmd.py:31` group, `:36`, `:74`, `:94`, `:112` | E3 | none |
| `review telemetry taskvars / append / load` | `telemetry_cmd.py:15` group, `:20`, `:41`, `:73` | E3 | none |
| `review cluster` | `cluster_cmd.py:96`, body `:133` | E1 | `sc-reflect-protocol/SKILL.md:345`, `:347` |
| `review verify-citations` | `verify_cmd.py:76`, body `:113` | E1 | `sc-reflect-protocol/SKILL.md:345` |
| `review manifest init / advance / validate` | `manifest_cmd.py:48` group, `:53`, `:137`, `:218` | E1 | `init` and `advance`: `sc-reflect-protocol/SKILL.md:338`, `:340`, `:342`, `:349`; `validate`: no hit for `manifest validate` in the SKILL (Grep) |
| `review lint` | not present | E3 (experiment) | n/a |
| `review estimate` | not present | E3 (experiment) | n/a |

The `--help` listing shows exactly seven commands: `cluster`, `ledger`, `manifest`, `merge`, `panel`, `telemetry`, `verify-citations`. No `lint`, no `estimate`. [CODE-VERIFIED]

### 1.4 D13: `lint_cmd` / `estimate_cmd` and the silent-skip risk (Q4)

- No `lint_cmd.py` or `estimate_cmd.py` exists in the package on either ref (directory listing and `git ls-files`). [CODE-VERIFIED] [E3]
- They exist only on experiment branches: `lint_cmd.py` in `448048aec` "experiment(review): mechanical requirements lint as reviewer evidence (PN2, refs #346)" (2026-11-10, branch `origin/346Claude-pn2-mechanical-lint`) and `estimate_cmd.py` in `c503587d9` "experiment(review): capture-recapture estimator for remaining review defects (PN3, refs #346)" (2026-11-10, branch `origin/346Claude-pn3-capture-recapture`). So the names are deliberate hooks for unmerged experiment branches, which matches the loader docstring `__init__.py:3-4`. This is a new finding not in the hand-off. [E3]
- The swallow is narrow (`__init__.py:33` re-raises any `ModuleNotFoundError` for a different module, e.g. a missing dependency inside an existing module), so a broken import inside `cluster_cmd.py` would still fail loudly. What is silent is a module file that is **absent** (deleted, renamed, or not merged). [CODE-VERIFIED] [E3, E1]
- Same risk for E1's appended names: `cluster_cmd`, `verify_cmd`, `manifest_cmd` are loaded by the same loop (`:26-28`). Reflect's shadow steps call `review manifest advance` after every stage, `review cluster` and `review verify-citations` (`sc-reflect-protocol/SKILL.md:338`, `:345`, `:347`). If one of those files disappeared, `superclaude review cluster` would become an unknown command at run time, not an import error; reflect's step rule "A step that cannot run records `panel_fallback_reason` (D4) and the run continues as legacy" (`SKILL.md:338`) would absorb it silently into the fallback path. [E1]
- No test pins the registered set: `grep -rn "lint_cmd\|estimate_cmd\|review_group" tests` returned nothing. A one-line test asserting `set(review_group.commands)` equals the expected seven would close the gap. [E1, E3]

Key Takeaways:
- The review CLI is the same on this branch and `origin/master`; E1's reflect work is already on master (`#519`).
- Seven real subcommands; two ghost names (`lint`, `estimate`) belong to unmerged #346 experiment branches PN2 and PN3.
- The optional-module loader turns "file missing" into "command missing" with no error; nothing tests the registered command set, and reflect's fallback rule would hide such a loss.

---

## 2. spec-panel: how the prose loop drives the CLI, and the fallback (Q3, Q1 for spec-panel)

### 2.1 The command file holds no CLI call

- `src/superclaude/commands/spec-panel.md` frontmatter `:1-8` (name `spec-panel`, persona list, no skill named). Usage `:22` shows `--mode discussion|critique|socratic` and `--re-review <prior-findings-file> --baseline <saved-copy>`. [CODE-VERIFIED] [E3]
- `## Review Loop` `:256-264` is seven prose bullets: Mode (`:258`), Grading (`:259`), Verdict (`:260`), Cap (`:261`), Re-review output (`:262`), Reviser contract (`:263`), Precedence (`:264`). None names `superclaude review`; the Grep of section 6 finds no hit in `src/superclaude/commands`. [CODE-VERIFIED] [E3]
- Hard gate `:266-268`: before any re-review and before writing or accepting a review or revise brief, read `~/.claude/rules/prompts/document_review_loop_prompts.md` in full; if it cannot be read, return `incomplete` and review nothing. [CODE-VERIFIED] [E3]
- Blocking rule (prose): CRITICAL blocks; MAJOR or FR-8/FR-9 blocks only with a concrete wrong outcome or a security, data-loss or safety-boundary risk; otherwise Medium; MINOR is a note (`:259`). Verdict line `verdict: PASS|FAIL` (`:260`). Cap: 2 fix cycles = 3 reviews, `review: N of 3` (`:261`). So spec-panel's own result is **blocking** within its loop (FAIL triggers a revision, review 3 FAIL escalates to the user). [CODE-VERIFIED] [E3]
- `:262` delegates the re-check procedure to `rf-qa.md`'s Fix Cycle steps 1-5 (project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`). This is a coupling a future rf-qa replacement must keep or move. [CODE-VERIFIED] [E3]

### 2.2 The prompts file is the only CLI wiring

`src/superclaude/rules/prompts/document_review_loop_prompts.md` (74 lines, `wc -l`, matching the hand-off) is installed by `install_rules` (`src/superclaude/cli/install_user_setup.py:153-179`, "never auto-loaded" at `:179`). The installed copy `~/.claude/rules/prompts/document_review_loop_prompts.md` is byte-identical to the source (`diff -q`, 2026-11-14). [CODE-VERIFIED] [E3]

- `:3` scopes it to `/sc:spec-panel --mode critique`. [E3]
- Placeholders `:17-21`: `{{CANDIDATE}}`, `{{BASELINE}}`, `{{PRIOR}}`, `{{N}}`, `{{IDS}}`. There is no source/spec placeholder (D8 holds). [CODE-VERIFIED] [E3]
- FIRST-REVIEW brief `:29-33`, RE-REVIEW `:35-49` (fixed role table `:39-43`, `diff -w` evidence `:44`, `grep -nF` self-check `:46`), REVISE `:51-54`. `missing-requirement` style findings are graded Medium by the grading check (`:31`), while `:60` lets any finding carry `blocking: true` (D9 holds). [CODE-VERIFIED] [E3]
- Findings block `:56-62` (`findings-v1`, fields id, severity, blocking, category, anchor 12-200 chars, anchor2, refs, claim; prior lines on re-review). Fix map `:64-66` (`fixmap-v1`). [CODE-VERIFIED] [E3]
- `### Review panel` `:68-70`, the single paragraph that drives the CLI. Sequence for the coordinator (the session running the loop, not the reviewer):
  1. `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>`: a panel for a first review, one reviewer for a re-review by default; each reviewer in a fresh context with the same brief, none seeing another's report. Options exist in code at `panel_cmd.py:18` onward. [CODE-VERIFIED for the command; the "one reviewer for re-review" default is inside `panel.py`, not re-read here: UNVERIFIED in this slice]
  2. `superclaude review merge`, "also for a single reviewer"; its merged report and ledger give the verdict and the Reviser brief ids (`merge_cmd.py:21`, `:71` docstring "print the verdict, decision and Reviser brief ids as JSON"). [CODE-VERIFIED]
  3. After revising: `superclaude review ledger revise --ledger --old --new --fixmap` moves applied rows to `resolved_check` (`ledger_cmd.py:36`). [CODE-VERIFIED for registration]
  4. "A merge refuses a round in which no reviewer produced a valid findings block" and "Only these scripts change a finding's status." [doc claim; scope slice 02 confirms the refusal at `ledger.py:150-157` and that it passes with one valid reviewer (D3): CODE-VERIFIED by that slice, not re-read here]
- Not called by the prompts file: `review ledger verdict`, `ledger defer`, `ledger capture`, `panel validate`, the whole `telemetry` group, and every E1 command (`cluster`, `verify-citations`, `manifest`). The stop decision is therefore made in prose (spec-panel `:261`), not from `ledger verdict`'s exit code (0/10/11 per scope slice 05). [CODE-VERIFIED by reading `:70`] [E3]

### 2.3 Prose-only fallback

- `:70` last sentence: "If the `superclaude` command is not installed, run one reviewer and say so in the loop summary." That is the whole fallback. [CODE-VERIFIED] [E3]
- Consequences: (a) no ledger, so `resolved_check`/`regressed` state lives only in the prose rules (spec-panel `:262` prior-findings table); (b) no merge refusal, so a single reviewer's invalid findings block is not caught by a script; (c) no panel, so a fallback run is a one-reviewer run with no diversity. The spec-panel bullets `:256-264` are written to stand alone (they restate verdict, cap and reviser rules), which is what makes this fallback viable. [E3]
- How the fallback is detected is not specified (no `command -v superclaude` instruction). On this machine `superclaude` resolves to `~/.local/bin/superclaude` (2026-11-14). Whether that pipx/uv install carries the same `review` subcommands as this checkout was not checked: UNVERIFIED. [E3]
- The `incomplete` hard gate (`spec-panel.md:268`) and the fallback differ: a missing prompts file stops the review; a missing CLI only degrades it.

### 2.4 Installed-only variant commands (names and descriptions only)

All five exist under `~/.claude/commands/sc/` and nowhere under `src/` (Glob in scope slice 05; not re-run here). Line counts and `description:` read 2026-11-14:

| Variant | Lines | Description (frontmatter) |
|---|---|---|
| `spec-panel-armb.md` | 472 | "Multi-expert specification review and improvement using renowned specification and software engineering experts" (same as base) |
| `spec-panel-diffgate.md` | 481 | "... with a computed re-review surface (diffgate variant)" |
| `spec-panel-ledger.md` | 475 | "... with a script-kept finding ledger (find once, then verify)" |
| `spec-panel-ponytail.md` | 483 | "... (variant: adds the --fix-audit step, issue 346)" |
| `spec-panel-stoprule.md` | 481 | "... (experimental variant: computed review-loop verdict)" |

All tagged [E3] (experiment variants; phase-5 bundle per scope slice 05 §1A). Each variant is a full fork of the 490-line base, so a unified panel that changes `spec-panel.md` will not reach them.

Key Takeaways:
- spec-panel's review loop is blocking (FAIL to revise, review 3 FAIL escalates) and is the only consumer that uses `review merge` and `review ledger revise`, and it does so only through prose in the rules prompts file, not in the command.
- The CLI is optional: without `superclaude` the loop becomes one reviewer with no ledger and no script check, and the detection of "not installed" is unspecified.
- Five installed-only spec-panel forks sit outside the repo and outside any unification change.

---

## 3. sc:workflow tasklist review (Q1)

`src/superclaude/skills/sc-workflow-protocol/SKILL.md`:

- Wave 3 Gate `:79-83`: schema gate from `refs/quality-gates.md`; quick = schema-min, standard/deep = full; fail = STOP `E-GATE`. Not a review panel. [CODE-VERIFIED] [E2 baseline]
- Wave 4 Reflect `:85-93`:
  - `:87` advisory codegraph pre-check written to `<pkg>/artifacts/codegraph-grounding.md` under `## Pre-check`; never edits `<id>.md`. [CODE-VERIFIED]
  - `:89` the call: `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` via Skill `sc:reflect-protocol`, "defaults for every other flag, no `--remediate`". Records `reflect_status` and `reflect_report_path` from reflect's `return-contract.yaml`. [CODE-VERIFIED] [E1 engine, E2 target]
  - `:91` unattended form adds `--unattended --output <report-dir>/nested/reflect-<n>/`. [CODE-VERIFIED]
  - `:93` "Advisory and read-only: never edit, delete, or regenerate `<id>.md` from findings, and never change the workflow `status`." Reflect unavailable or failed gives `reflect_status: skipped|failed`, still proceeds. [CODE-VERIFIED]
- `refs/return-contract.md:16` `reflect_status: success | partial | failed | skipped # ... advisory only`; `:21` "`reflect_*` are additive and advisory: they never change `status`." [CODE-VERIFIED]
- Inputs and ids: the spec is `<pkg>/source.md` (always present, `SKILL.md:77`), the candidate is `<pkg>/<id>.md` whose tasks are headed `## Task N:` numbered 1..N across the plan (`:73`) with `Acceptance criteria:` blocks; dependencies as `Depends on: Task K`. Task ids are therefore `Task N`, not `T01.02`; neither form matches the findings-v1 ref token (D7: letters-hyphen-digits or `P<digit>`), so findings-v1 clustering of workflow-plan findings would fall back to span proximity. INFERENCE from the regex quoted in scope slice 02 §5 D7; not tested. [E2, E3]
- Result: **advisory**. Nothing in the workflow blocks on reflect findings. [E1, E2]

The E2 study's "tasklist review panel" (scope slice 00 §6 item 10) has no plug point here today: the only review is reflect pre, and the E2 study drove `/sc:spec-panel --mode critique` against plans manually (hand-off D14). [E2] [UNVERIFIED: the hand-off statement on how E2 drove the panel was not re-read in E2 files in this slice]

Key Takeaways:
- sc:workflow's only review step is Wave 4 `/sc:reflect --mode pre` with default flags; advisory; it records status and a report path only.
- A thin "workflow tasklist review" module has one natural plug point: Wave 4 (`SKILL.md:89`), either replacing or adding to the reflect call; the contract fields `reflect_status`/`reflect_report_path` are the existing output slot.
- Workflow plan ids (`Task N`) do not match the findings-v1 ref regex.

---

## 4. sc:tasklist stage and phase gates (Q1)

`src/superclaude/skills/sc-tasklist-protocol/SKILL.md`:

### 4.1 Stage 10.5 Pre-Reflect Sign-off (`:1619-1646`)

- Runs after the Stage 7-10 patch chain and any P2 loop have terminated (`:1621`); disjoint from the P2 QA loop by stage, finding source and ownership (`:1623`). [CODE-VERIFIED] [E1 engine]
- Fan-out of N agents, one per phase file, in one parallel wave via the Stage 7 `Task` primitive (`:1625`). [CODE-VERIFIED]
- Depth/tier computed deterministically per phase from Tier Distribution, Critical Path Override, Risk, task count and Traceability Matrix into `validation/reflect-pre/depth-map.yaml` (`:1627`, `:1650-1660`). Spec resolution order: explicit `--spec`, then auto-wired TDD/PRD from `.roadmap-state.json`, then the roadmap itself (`:1627`). [CODE-VERIFIED]
- Call `:1630-1635`: `/sc:reflect --mode pre --remediate --tasklist TASKLIST_ROOT/phase-<P>-tasklist.md --spec <RESOLVED_SPEC_PATH> --depth <det.> --tier <det.> --output TASKLIST_ROOT/validation/reflect-pre/phase-<P>/`. No `--executor-model` at PRE (`:1627`), no `--t2-engine`. [CODE-VERIFIED]
- Verdict handling `:1640`: PASS recorded in the index "Pre-Reflect Sign-off" column; PARTIAL/FAIL recorded with a link, "the bundle **still ships** (audit-first)"; `--remediate` only *offers* remediation and never auto-mutates the phase file; a `needs_human_decision` item HALTs. Stage gate `:1646`: "The bundle ships regardless of verdict (advisory-blocking)." [CODE-VERIFIED]
- So Stage 10.5 is **advisory** on the verdict but **blocking** on `needs_human_decision` in the remediation offer (`:1640`, unattended `:1642` turns it into `blocked`). [E1]
- Skipped under `--no-reflect` or `--dry-run` (`:1644`).

### 4.2 Per-phase post gate (`:1155-1179`)

- Gate command `:1157-1163`: recursion guard on `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, then `superclaude reflect run TASKLIST_ROOT/phase-<PP>-tasklist.md --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`. This is the Python reflect wrapper, not the review CLI. [CODE-VERIFIED] [E1]
- `:1165` depth fixed `deep` (forced Tier 2), no `--tier`, reviewer exclusion class read by the wrapper from the phase file frontmatter `executor_model_class`. Traced in the Phase 3 fix cycle 1: the wrapper does read it (`src/superclaude/cli/reflect/config.py:53` key name, `:350-355` env `EXECUTOR_MODEL_CLASS` first, then frontmatter) [CODE-VERIFIED], but it is **unused on the route this gate takes**: `--depth deep` always runs the code engine `run_tier2_ensemble` (`runner.py:538-545`), and `ensemble.py` never reads `executor_model` (0 Grep matches); the value reaches only the Tier 1 prompt (`runner.py:480-481`), which the CLI cannot reach because it accepts only `standard|deep` (`commands.py:253-258`). So the gate's "executor-disjoint reviewers" claim (`:1165`, AC `:1177`) is [CODE-CONTRADICTED]; reviewers are the external `T2Model0N` pool (`research/13-gap-fill-reflect-ensemble.md` §2.4). [E1]
- `:1170-1171`, `:1176-1179`: **blocking**. Only wrapper exit 0 completes; 10/11/2 fail; and the gate also fails at exit 0 when the derived `reflect_post.verdict` is not `pass`, `adversarial_subrun_status` is partial/failed, `tier_reached == 2` with `adversarial_convergence_score < 0.80`, or drift/regression counts > 0. [CODE-VERIFIED] [E1]
- Ids: phase tasklists use the generator's task ids (hand-off D7 cites `T01.02` form) and `R-###` roadmap ids (`:1660`). `R-001` matches the findings-v1 ref regex; `T01.02` does not. [E2, E3]

Key Takeaways:
- sc:tasklist reaches review only through reflect: pre (advisory, per phase, deterministic depth/tier) and post (blocking, forced deep, via the `superclaude reflect run` wrapper).
- Neither call passes `--t2-engine`; no tasklist code calls `superclaude review` directly.
- The post gate's blocking rules read reflect contract fields (`tier_reached`, `adversarial_convergence_score`, deviation counts); a unified panel that replaces reflect Tier 2 must keep those fields or the gate silently changes meaning.
- [E1] The engine behind the post gate is `ensemble.py`, not the `/sc:reflect` skill (`runner.py:538-545`); it writes the deviation counts as zeros and never sets the halting flags (`ensemble.py:442-471`, :779-785), so the gate's drift/regression check (`:1171`) can never fire on this engine (research/13 §6). A panel that plugs in here replaces `ensemble.py`, not the skill-path Tier 2.

---

## 5. Does reflect `--mode pre` with default flags reach the Tier 2 panel? (Q6)

From `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and `src/superclaude/commands/reflect.md`:

- Default depth is `standard` (`commands/reflect.md:98`: "`--depth` | `standard` | quick (Tier 1 only) / standard (Tier 1, escalate by §5 rubric) / deep (force Tier 2)"); `--tier auto` default (`SKILL.md:85`); `--reviewers` default 3 (`SKILL.md:86`). [CODE-VERIFIED (prose spec is the code for a skill)] [E1]
- `--t2-engine legacy | shadow`, default `legacy` (`SKILL.md:87`); "With `legacy` the panel code is never called." `panel` is rejected until Stage 3. [CODE-VERIFIED] [E1]
- Rubric §5.3 (`SKILL.md:427-439`), first match wins: row 1 and row 2 STOP at T1 when confidence `C >= 0.90`/`0.85` with narrow scope and low unmapped density; row 4 `S_domains >= 3`, row 5 `S_dev_density > 0.20`, row 6 `C < 0.85` ESCALATE; rows 3/3a are UC-2 only; row 8 default STOP at T1. Pre-filters `coverage_undefined`, `coverage_degraded`, `surface_unreached` force T2 (`:443`). [CODE-VERIFIED] [E1]
- Decision table `SKILL.md:323-330`: `--depth standard`, rubric escalates: "T1 work, then T2", panel called "Only with `--t2-engine shadow`"; "with `legacy`, never". [CODE-VERIFIED] [E1]

Answer: with default flags, `/sc:reflect --mode pre` **can** reach Tier 2 (rubric-driven, e.g. `C < 0.85`, a multi-domain tasklist, or a coverage pre-filter), but at Tier 2 it runs the **legacy** reviewer rotation (§7.1) plus the `sc-adversarial-protocol` merge, not the `superclaude review` panel. The panel kernel (`review panel resolve`, `cluster`, `verify-citations`, `manifest`) runs only with an explicit `--t2-engine shadow` on the skill path, which no consumer passes (the post gate's `superclaude reflect run` route has no such flag, see the first Corollary) (Grep for `t2.engine|t2_engine` in `src/superclaude` hits only reflect's own SKILL.md, `refs/reviewer-spec.md`, `cli/review/manifest.py` and `manifest_cmd.py`). In shadow it is measurement only: "change no verdict" (`SKILL.md:338`). [E1]

Corollaries:
- sc:workflow (`--depth` default) and sc:tasklist Stage 10.5 (deterministic `--depth/--tier`) reach Tier 2 sometimes; the tasklist post gate (`--depth deep`) always reaches Tier 2, but not through the skill: `superclaude reflect run --depth deep` sets `expected_tier = 2` (`src/superclaude/cli/reflect/runner.py:538`) and in production calls the code engine `run_tier2_ensemble` (`runner.py:540-545`, i.e. `ensemble.py`), never `/sc:reflect`, so neither the skill's legacy rotation nor its `--t2-engine` switch (`SKILL.md:311`) applies on this route, and the reflect CLI has no `--t2-engine` option (0 Grep matches for `t2.engine` in `src/superclaude/cli/reflect/`) (see §4.2 above and `research/13-gap-fill-reflect-ensemble.md` §2.1, §5). [CODE-VERIFIED] [E1]
- Today **no consumer** exercises E1's panel kernel in production; it is reachable only from manual shadow runs. [E1]
- Loop to note: reflect's `--remediate` plan route calls `sc:workflow-protocol`, whose Wave 4 runs reflect pre again (`refs/remediation-handoff.md:14`: "its built-in advisory `--mode pre` review is surfaced"). A unified panel inherits this nesting. [E1]

Key Takeaways:
- Default reflect pre reaches Tier 2 only by rubric, and then uses the legacy rotation, never the review CLI panel.
- E1's panel kernel has zero production callers. For the consumers that reach Tier 2 through the `/sc:reflect` skill (sc:workflow Wave 4, sc:tasklist Stage 10.5), turning it on is a reflect flag change (`--t2-engine`), not a consumer change. It is not so for the blocking per-phase post gate: that gate runs `superclaude reflect run` -> `run_tier2_ensemble` (`ensemble.py`) with no `--t2-engine` switch (0 Grep matches in `src/superclaude/cli/reflect/`; `--depth` accepts only `standard|deep`, `commands.py:253-258`), so enabling the panel there needs a code change at `runner.py:538-545` / `ensemble.py` (`research/13-gap-fill-reflect-ensemble.md` §2.1, §5.1). [CODE-VERIFIED] [E1]

---

## 6. Brainstorm and design: artifact, ids and the spec-review hook (Q1, Q2)

### 6.1 sc:brainstorm

`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`:
- Output artifacts `:53-59`: `seed-brief.md`, `merged-requirements.md` ("Adversarial-merged unified spec", `:56`), `enrichment/*`, `adversarial/` (6 standard artifacts). Pipeline position `:42`. [CODE-VERIFIED] [future consumer]
- Wave 3 `:264-320` calls `sc-adversarial-protocol` with `--source <output>/seed-brief.md --generate spec` (`:272-283`), routes on `convergence_score`: `>= 0.65` PASS copies `merged_output_path` to `merged-requirements.md`; `>= 0.50` PARTIAL adds frontmatter `adversarial_status: partial`; `< 0.50` FAIL skips Wave 4 (`:310-313`). This convergence check is the only quality gate; there is no spec review. [CODE-VERIFIED] [E1-adjacent: same adversarial merge E1's legacy Tier 2 uses]
- Wave 4 `:322-339`: `none` (default) prints "Next: /sc:design @<output>/merged-requirements.md ..." (`:332`); `design` only prints a recommendation and never invokes (`:334`); `tasklist` validates `>= 3` enumerated requirements by regex for "bullets, numbered items, or headings" (`:337`) then invokes `sc-tasklist-protocol --source <output>/merged-requirements.md` (`:338`). [CODE-VERIFIED]
- Return contract `report_path: <output>/merged-requirements.md | null` (`:388`). [CODE-VERIFIED]
- **Id convention:** Grep for `FR-|AC-|NFR-|requirement id` in the skill folder returns no id rule. The only structure demanded is ">= 3 enumerated requirements" with the regex looking for bullets in sections like "Functional Requirements", "Acceptance Criteria" or numbered items (`refs/handoff-routing.md:185`). `sc-adversarial-protocol` has no requirement-id rule for `--generate spec` either; its provenance-comment examples show `FR-007 → Target FR-012` and `AC-NFR-3` (`sc-adversarial-protocol/refs/debate-protocol.md:349-352`), i.e. ids are carried when the variants used them, not created. So **`merged-requirements.md` is not guaranteed to carry FR/AC ids.** [CODE-VERIFIED] [future consumer]

### 6.2 sc:design

`src/superclaude/commands/design.md` (149 lines):
- No skill named; frontmatter `:1-8` (`mcp-servers: [codegraph]`, `personas: []`). Behavioral Flow `:28-34`: step 4 Validate is self-validation of names, signatures and consumers against code via codegraph (`:33`, `:65`). No reviewer, panel, reflect or spec-panel reference anywhere in the file (read in full). [CODE-VERIFIED]
- Output: design document via `--output <file>` (`:23`, `:26`); under `--unattended`, `report_path` is the `--output` file or `<report-dir>/design-report.md`, success = document written; "There is no gate" (`:123-124`). Each document carries one `Grounding:` line (`:74`). [CODE-VERIFIED]
- No id convention for design elements. Next step `/sc:implement` (`:149`). [CODE-VERIFIED]

### 6.3 What a spec-review hook needs (Q2)

- Artifact: brainstorm `<output>/merged-requirements.md` (after Wave 3 PASS/PARTIAL, before Wave 4), design `--output` file or `<report-dir>/design-report.md` (after step 5 Document).
- Ids: findings-v1 `refs` (prompts `:60`) and clustering rely on letters-hyphen-digits ids (`FR-1`, `AC-0.4`). Neither artifact guarantees such ids, so either the hook (a) accepts id-less documents and clusters by anchor/span only, or (b) the producing skill is told to number requirements `FR-n`/`AC-n` (brainstorm already counts enumerated requirements at `:337`). The hand-off D8 also applies: the review brief has no source placeholder, so the brainstorm hook cannot hand `seed-brief.md` to reviewers as the driving document, and the design hook cannot hand `merged-requirements.md`. [E3]
- Hook form, evidence for each option:
  - `/sc:spec-panel --mode critique @<file>`: exists, already speaks findings-v1, has grading, cap and verdict prose (`spec-panel.md:256-264`) and the CLI wiring plus fallback (prompts `:68-70`). But it is a full multi-expert command (490 lines) with an Improve step, and its loop is interactive (asks the user about follow-up issues, `:260`); spec-panel's prose is the only place the merge/ledger CLI is used. Brainstorm already uses the "Skill invocation, not command" pattern (`:302`); spec-panel has no protocol skill to invoke. [E3]
  - Direct `superclaude review` calls: the CLI has no "review this document" command; it only resolves a panel, merges reports and keeps a ledger. Reviewer dispatch and briefs must still come from a prompt (today only `document_review_loop_prompts.md`). So a "direct call" still needs the prompts file and an orchestrator. [E3, E1]
  - Conclusion: as the code stands, the hook would be `/sc:spec-panel --mode critique` (first review only, advisory) or a new thin protocol that reads `document_review_loop_prompts.md` and calls `review panel resolve` + `review merge`. Which one is a design decision; nothing in code picks it.
- Advisory or blocking: brainstorm's design hand-off is print-only (`:334`) and design has "no gate" (`:124`), so the existing style argues for advisory; brainstorm's `tasklist` handoff (`:338`) would be the place to make it blocking (a FAIL could stop the handoff).

Key Takeaways:
- Brainstorm and design have no review step; their artifacts are `merged-requirements.md` and the design `--output` file.
- `merged-requirements.md` carries FR/AC ids only if the debate variants wrote them; no rule creates them.
- A direct `superclaude review` call is not enough on its own: the CLI merges and tracks, it does not brief or dispatch reviewers.

---

## 7. D14: who calls `review merge`, `review ledger` and `review panel resolve` (Q5)

Grep `superclaude review|review_ledger|review panel resolve` over `src/superclaude/skills`, `src/superclaude/commands`, `src/superclaude/core` (2026-11-14): hits only in `src/superclaude/skills/sc-reflect-protocol/SKILL.md` at `:338`, `:340`, `:345`, `:347`, `:349`. No hit in any command or core file; no hit for `review_ledger` anywhere in those directories. [CODE-VERIFIED]

Per subcommand:

| Subcommand | Prose callers in `src/` | Python callers | Verdict on "no in-repo caller" |
|---|---|---|---|
| `review merge` | `src/superclaude/rules/prompts/document_review_loop_prompts.md:70` only (outside the three grepped dirs) | `tests/review/test_review_ledger.py:11` imports the `ledger` module (not the command) | Holds for skills/commands/core; the only caller is the rules prompts file read by spec-panel's hard gate (`spec-panel.md:268`). [E3] |
| `review ledger revise/defer/verdict/capture` | prompts `:70` names only `ledger revise`; `defer`, `verdict`, `capture` have no prose caller at all | tests import `ledger` | Holds; three of four ledger subcommands are unused by any instruction. [E3] |
| `review panel resolve` | reflect shadow step 1 `sc-reflect-protocol/SKILL.md:340` (`--template @reflect-pre ... --strict-distinct`); prompts `:70` | `scripts/reflect_shadow_exit.py:52` imports `panel` | **[CODE-CONTRADICTED]** as a blanket claim: reflect calls it, but only on the `--t2-engine shadow` path that no consumer enables (section 5). [E1, E3] |
| `review cluster`, `verify-citations`, `manifest` | reflect shadow steps only (`:338-349`) | `scripts/reflect_cluster_pairs.py:75-76`, `scripts/reflect_stage0a_replay.py:65-66`, `scripts/reflect_shadow_exit.py:51` | E1-only, shadow-only. [E1] |
| `review telemetry *`, `panel validate` | none | tests only | No caller. [E3] |

Hand-off D14 checks:
- "No tasklist review step exists in `sc-tasklist-protocol` or `sc-workflow-protocol`" (grep for `superclaude review`, `review panel`, `review_ledger`, `review loop`): [CODE-VERIFIED] for direct review-CLI calls; both skills do have reflect-based review steps (sections 3 and 4), which the hand-off's grep does not count. [E2]
- "The review loop lives only in `commands/spec-panel.md:256-268` plus the prompts file": [CODE-VERIFIED] (section 2). [E3]
- "The review ledger skill, `spec-panel-ledger/-stoprule` commands and `finding-grader` agent exist only as experiment copies under `.dev/experiments/346-validation/phase5/final-bundle/builds/`": [CODE-CONTRADICTED, partially] for this machine: the five spec-panel variant commands exist under `~/.claude/commands/sc/` (section 2.4, `ls`/`wc` 2026-11-14). The skill and agent installs were reported by scope slice 05 §1A and not re-listed here. [E3]

Key Takeaways:
- The #346 merge/ledger CLI has exactly one in-repo caller: one paragraph of the rules prompts file, read only by `/sc:spec-panel --mode critique`.
- `panel resolve`, `cluster`, `verify-citations` and `manifest` are called only by reflect's shadow steps, which no consumer turns on.
- So in production today neither E1's kernel nor E3's ledger is reached by sc:workflow, sc:tasklist, sc:brainstorm or sc:design.

---

## 8. Design input: one CLI surface all thin modules call (Q8)

What the evidence above implies for a single surface. These are design inputs, not verified behaviour.

1. **The CLI is helpers, not a review runner.** Today nothing in `superclaude review` briefs or dispatches reviewers; dispatch lives in prose (prompts `:70`; reflect `SKILL.md:342` "Dispatch is the legacy dispatch"). Every thin module therefore needs the same three prose pieces: a brief template, a dispatch rule, and the CLI calls. A shared "panel protocol" reference (one file, like `document_review_loop_prompts.md` but target-agnostic, with a `{{SOURCE}}` placeholder for D8) would let each module stay thin. [E1, E3]
2. **Two parallel pipelines over one package.** E3: `panel resolve` → reviewers write findings-v1 → `merge` (clusters + ledger + verdict) → `ledger revise` → `merge` (next round). E1: `panel resolve` → `manifest init/advance` → cards with findings-v2 + calibration → `cluster` → `verify-citations` → legacy debate → `cluster --kept`. They share only `panel resolve` and `findings.refs_norm`. One surface needs one sequence; the natural union is `resolve → (manifest) → collect → merge/cluster → verify-citations → verdict/ledger`. [E1, E3]
3. **Verdict ownership differs per consumer.** spec-panel is blocking via `ledger.py` verdict (through `merge`); the tasklist post gate is blocking via reflect contract fields (`tier_reached`, `adversarial_convergence_score`, deviation counts; `sc-tasklist-protocol/SKILL.md:1171`); workflow and Stage 10.5 are advisory. A unified CLI should return one machine verdict (`ledger verdict` already has exit codes 0/10/11 per scope slice 05) and let each module decide advisory versus blocking, rather than encoding it in the CLI. [E1, E2, E3]
4. **Per-consumer inputs the surface must accept:** candidate path; source/spec path (workflow `source.md`, tasklist `RESOLVED_SPEC_PATH`, brainstorm `seed-brief.md`, design `merged-requirements.md`); run id; kind first/re-review; lens or profile (`@reflect-pre`, spec, tasklist); executor class to exclude (tasklist post reads `executor_model_class`, but the post gate's route never uses it: `--depth deep` runs `ensemble.py`, which never reads it, §4.2, `research/13` §2.1 [CODE-VERIFIED]); output dir (each consumer already has a nested `--output` convention, e.g. `<report-dir>/nested/reflect-<n>/`). [E1, E2, E3]
5. **Ids.** Workflow `Task N`, tasklist `T01.02`/`R-###`, brainstorm free-form or `FR-n`, spec-panel `FR-8`/`AC-0.4`. The shared ref regex accepts only the letters-hyphen-digits forms (D7). A per-profile id pattern in the panel template would let each module declare its ids. [E2, E3]
6. **Registration.** Replace the optional loader (`__init__.py:19-35`) for core subcommands with explicit imports, or keep the loader only for experiment names and add a test pinning the core set; remove `lint_cmd`/`estimate_cmd` from the tuple until PN2/PN3 merge (section 1.4). [E1, E3]
7. **Fallback.** Define one fallback for "CLI not installed" for all modules (today: spec-panel runs one reviewer, prompts `:70`; reflect falls back to legacy with `panel_fallback_reason`, `SKILL.md:338`; others have none) and one detection rule. [E1, E3]
8. **Turn-on switch.** For the consumers that reach Tier 2 through the `/sc:reflect` skill (workflow Wave 4, tasklist Stage 10.5), the only switch today is reflect's `--t2-engine`; those consumers pass none. Putting the engine choice in the panel template or a project default, rather than in each caller's flags, would avoid editing those skills to turn the panel on. It does not reach the blocking per-phase post gate: that gate runs `superclaude reflect run` -> `run_tier2_ensemble` (`ensemble.py`) with no `--t2-engine` switch, so no template or project default turns the panel on there; that needs a code change at `runner.py:538-545` / `ensemble.py` (`research/13-gap-fill-reflect-ensemble.md` §2.1, §5.1). [CODE-VERIFIED] [E1]

Key Takeaways:
- A single surface needs a shared brief/dispatch reference as well as CLI subcommands; the CLI alone cannot run a review.
- Keep verdict computation in the core and advisory/blocking policy in each thin module.
- Fix the loader and add a source placeholder before more consumers depend on the CLI.

---

## Gaps and Questions

- [UNVERIFIED] The "one reviewer for a re-review by default" rule of prompts `:70` lives in `panel.py`/the packaged templates; not re-read in this slice.
- [UNVERIFIED] Whether the globally installed `superclaude` (`~/.local/bin/superclaude`) carries the same seven `review` subcommands as this checkout; `--help` was run through `uv run` in the checkout only.
- Resolved in the Phase 3 fix cycle 1: the wrapper reads `executor_model_class` (`config.py:53`, :350-355) but the Tier 2 route the gate takes (`ensemble.py`) never uses it; the gate's executor-disjoint claim (`sc-tasklist-protocol/SKILL.md:1165`, :1177) is [CODE-CONTRADICTED] (section 4.2; research/13 §2.4, §6).
- [UNVERIFIED] How E2 drove `/sc:spec-panel --mode critique` against plans (hand-off D14 text); not checked in E2 files with `git show 4a22d742...` in this slice.
- [UNVERIFIED] Installed `sc-review-ledger`, `sc-spec-panel-stoprule-protocol` skills and `finding-grader` agent (taken from scope slice 05; only the five variant commands were listed here).
- [CODE-CONTRADICTED] "No in-repo caller of `review panel resolve`": reflect's shadow step 1 calls it (`sc-reflect-protocol/SKILL.md:340`), shadow path only.
- [CODE-CONTRADICTED, partially] Hand-off: variant commands "exist only" in the phase-5 bundle; they are installed under `~/.claude/commands/sc/`.
- Open: what fallback rule spec-panel uses to detect "`superclaude` not installed" (prompts `:70` gives none).
- Open: should the brainstorm/design hook be advisory (matching `design.md:124` "no gate") or blocking at brainstorm's `tasklist` handoff (`SKILL.md:338`)? User decision.
- Open: should brainstorm require `FR-n`/`AC-n` ids in `merged-requirements.md` so findings refs and clustering work?
- Open: is the "workflow tasklist review" the reflect pre Tier 2 panel or a separate direct panel call in Wave 4? (Same question as scope slice 05 §1B.)
- Open: the reflect `--remediate` plan route nests sc:workflow, which runs reflect pre again; does the unified panel need a recursion or depth guard like `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`?
- Gap: no test pins the registered `review` subcommand set (section 1.4).
- Gap: three of four `ledger` subcommands (`defer`, `verdict`, `capture`), all of `telemetry`, and `panel validate` have no instruction that calls them.

## Stale Documentation Found

- **[STALE DOC]** Hand-off D13 cites `__init__.py:19-32`; the loop now spans `:19-36` and the swallow is `:30-35` (lines grew when #519 appended three names). Behaviour unchanged.
- **[STALE DOC]** Hand-off D13 does not say where `lint_cmd`/`estimate_cmd` come from; they are the PN2 and PN3 experiment branches (`448048aec`, `c503587d9`), so the names are planned modules, not typos.
- **[STALE DOC]** Hand-off D14 phrase "only as experiment copies under `.dev/experiments/...`" is stale for this machine (installed copies exist in `~/.claude/`).
- **[STALE DOC]** Hand-off D14 grep result "returned nothing" is stale against this tree: the same grep now hits `sc-reflect-protocol/SKILL.md` (E1's shadow steps, added by #519 and later commits).
- No staleness found in `spec-panel.md:256-268` or prompts `:68-70` against the scope slice 05 description.

## Summary

The `superclaude review` CLI is identical on this branch and `origin/master`: seven real subcommands, plus two ghost loader names (`lint_cmd`, `estimate_cmd`) that belong to the unmerged #346 experiment branches PN2 and PN3. The optional-module loader turns a missing file into a missing command with no error, and no test pins the set. No consumer skill calls the CLI directly. sc:workflow (advisory Wave 4) and sc:tasklist (advisory Stage 10.5) reach review through `/sc:reflect`, and reflect uses E1's panel kernel only with `--t2-engine shadow`, which nobody passes, so default reflect pre reaches Tier 2 through the legacy rotation at most. sc:tasklist's blocking per-phase post gate does not use the skill: it runs `superclaude reflect run --depth deep`, which in production always calls `run_tier2_ensemble` in `ensemble.py` (`runner.py:538-545`), so its Tier 2 is that code engine, not the skill's legacy rotation or panel (§4.2, §5; `research/13-gap-fill-reflect-ensemble.md` §2.1, §5). The #346 merge/ledger CLI is driven only by one paragraph of `document_review_loop_prompts.md`, read by `/sc:spec-panel --mode critique`, with a one-reviewer fallback when the CLI is missing. Brainstorm and design have no review step, and `merged-requirements.md` carries FR/AC ids only by accident, so a spec-review hook must either tolerate id-less documents or require ids, and needs a shared brief/dispatch reference because the CLI alone cannot run reviewers.
