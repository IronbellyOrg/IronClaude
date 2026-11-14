# QA Report - Primitive-path lens (T251)

**Phase:** cmd-skill gate, rf-qa primitive-path domain lens
**Date:** 2026-11-12
**fix_authorization:** false (report is the only file written)

Files judged from disk, not from earlier reviews: `src/superclaude/commands/sweep.md` (68 lines), `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (62 lines), `src/superclaude/output-styles/pragmatic.md` (git diff and lines 18-29). House patterns: `src/superclaude/commands/graph.md`, `issue.md`, `src/superclaude/skills/sc-graph-protocol/SKILL.md`.

## Path inventory (every path-like token, read now)

| Where | Token | Kind | Judgement |
|---|---|---|---|
| `sweep.md:16` | `~/.claude/WORKER-CONTRACT.md` | installed core doc | installed form; the file exists as `src/superclaude/core/WORKER-CONTRACT.md` and installs to `~/.claude/` (a core doc has no project copy); see F-1 for the claim made about it |
| `sweep.md:49` | `~/.claude/skills/sc-sweep-protocol/SKILL.md` | installed skill | correct, listed first |
| `sweep.md:51-53` | `.claude/skills/sc-sweep-protocol/SKILL.md` | project dual-surface copy | labelled ("When a project checkout holds its own copy ... the dual surface is"), listed after |
| `sweep.md:55` | `~/.claude/skills/` first | lookup order | matches the project rule (skills read `~/.claude/skills/` first, then `.claude/skills/`) |
| `sweep.md:14,38` | `<root>/.dev/sweeps/` | runtime output folder | not a primitive path; matches `src/superclaude/cli/sweep/commands.py:99-123` |
| `SKILL.md:15` | `~/.claude/commands/sc/sweep.md`, or project `.claude/commands/sc/sweep.md` | installed command + project copy | both surfaces, installed first; same wording as `sc-graph-protocol/SKILL.md:15` and `sc-impact-protocol/SKILL.md:15` |
| `SKILL.md:33` | `~/.claude/output-styles/pragmatic.md` | installed output style | informational ("installed as"), not a read instruction; no project copy exists (see C6) |
| `SKILL.md:23-24` | `superclaude sweep run`, `uv run --frozen --no-sync superclaude sweep run` | CLI forms | package behaviour reached through the CLI, not a package path; see F-2 |
| both files | any `src/superclaude/`, `.py`, `cli/`, `pm_agent/`, `contracts/`, `examples/` | package code | none found (C1, C2) |

`pragmatic.md` (the style file) names the skill only as `sc-sweep-protocol` (lines 23-26), with no path; its git diff adds no path token (B2 below).

## Findings

No BLOCKING and no MAJOR finding. Three MINOR findings (notes; they never fail the gate).

### F-1 (MINOR, carry to the contract gate) `sweep.md:16` states a fact about a file that has not been edited yet

- Evidence: `src/superclaude/commands/sweep.md:16` says "It is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`". The list is `src/superclaude/core/WORKER-CONTRACT.md:23`: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit`. `/sc:sweep` is not on it. `git status` shows `WORKER-CONTRACT.md` unmodified.
- Why only MINOR: the path form is right (installed `~/.claude/` core-doc path). The addition is a scheduled deliverable of the same package: task item 12.2 (unchecked) and DESIGN section 7.6 line 657 and section 8 (steps 1.18 and 1.19 land in one commit). As the files stand today the sentence is ahead of the file it cites.
- Smallest fix: none now. The contract gate (item 12.21) must re-read `WORKER-CONTRACT.md:23` and confirm `/sc:sweep` is on the list before this sentence ships. If item 12.2 is dropped, reword `sweep.md:16`.

### F-2 (MINOR) `SKILL.md:24` step 2 fallback is a dev-checkout-only form and is not labelled

- Evidence: `src/superclaude/skills/sc-sweep-protocol/SKILL.md:24` runs `uv run --frozen --no-sync superclaude sweep run <args>` when step 1 says "command not found". `grep -rln 'uv run --frozen --no-sync' src/superclaude/skills src/superclaude/commands` lists only this skill (no house pattern). Outside a checkout that environment has no `superclaude`, so the form cannot succeed; line 29 then reports the failure accurately, so nothing is hidden and no package path is named.
- Smallest fix: add "(works only in a dev checkout that has the project environment)" to step 2. Optional.

### F-3 (MINOR) the tests do not pin several path rules the primitives follow

- Evidence: experiments on private copies under `/tmp` (deleted afterwards; no repository file changed). Each copy ran `tests/commands/test_sweep_command.py`:
  - m0 unmodified: 110 passed.
  - m1 `SKILL.md:15` drops "or the project `.claude/commands/sc/sweep.md`" (single surface): 110 passed, NOT caught.
  - m4 the two Activation bullets in `sweep.md:49-53` swapped (project copy first): 110 passed, NOT caught.
  - m2 `SKILL.md:15` command path replaced by a `src/superclaude/` path: caught (`test_sweep_no_src_superclaude_path[SKILL.md]`).
  - m3 `sweep.md:16` core-doc path replaced by a `src/superclaude/` path: caught (same test, `[sweep.md]`).
  - m5 `SKILL.md:33` installed output-style path removed: caught (`test_skill_states_clause[...installed-path]`).
- The tests at `tests/commands/test_sweep_command.py:114-128` pin only the command's Activation surfaces (and not their order); nothing pins `SKILL.md:15`'s dual surface or installed-first order.
- Smallest fix: add one assertion that `SKILL.md:15` holds both `~/.claude/commands/sc/sweep.md` and `.claude/commands/sc/sweep.md` and that the installed one comes first, and one that the Activation installed bullet precedes the project bullet.

### Observation (not a finding)

`.claude/commands/sc/sweep.md` and `.claude/skills/sc-sweep-protocol/` do not exist in this checkout (`make sync-dev` has not run). Both primitives name the project copy conditionally ("When a project checkout holds its own copy"), and `.claude/` content is gitignored sync output, so this is expected.

## Batch inspection log (one read-only script, run once)

B1 no `src/superclaude` hit in the three primitives (NO_MATCH). B2 the only path token in the `pragmatic.md` diff is the diff header. B3 `Makefile:109-135` `sync-dev` copies skills, agents and commands; no `output-styles` target, and `.claude/output-styles` is absent. B4 `uv run --frozen --no-sync` appears only in the sweep skill. B5 `commands.py:64-123` matches `sweep.md:37-38` (root must hold `.git`; output is `<root>/.dev/sweeps/` or below and apart from the inputs). B6 `plugins/superclaude/` holds no `sc-graph-protocol` either, so no mirror is expected. B7 the test pins listed under F-3. B8 the installed-then-project wording of `SKILL.md:15` equals the `graph` and `impact` skills.

Also run: `uv run --no-sync pytest tests/commands/test_sweep_command.py tests/recommend/test_routing_refresh.py -q` gave 358 passed; `ruff check` on `src` and the test file is clean; `ruff format --check` on the test file is clean. `git diff -U0 -- tests/recommend/test_routing_refresh.py` is one line, `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "sweep"}` (line 33); it has no path content.

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | No `src/superclaude/` path in `sweep.md` or `SKILL.md` | PASS |
| C2 | No reference to package code (`.py`, `cli/`, `pm_agent/`, `contracts/`, `examples/`); package behaviour only through the `superclaude sweep run` CLI | PASS |
| C3 | Every skill lookup in `sweep.md` names the installed path first and the project `.claude/` copy after, labelled (`sweep.md:49-53`) | PASS |
| C4 | The stated lookup order matches the project rule: skills read `~/.claude/skills/` first (`sweep.md:55`) | PASS |
| C5 | The command lookups in `SKILL.md:15` name both surfaces, installed first, same wording as the `graph` and `impact` skills | PASS |
| C6 | `SKILL.md:33` output-style path: informational, not a lookup; no project copy of output styles exists (`Makefile` `sync-dev`, `.claude/output-styles` absent, installer copies to `~/.claude/output-styles/`) | PASS |
| C7 | `pragmatic.md` diff adds no path token; the style names the skill without a path (lines 23-26) | PASS |
| C8 | The invocation `> Skill sc:sweep-protocol` equals the skill's frontmatter `name: sc:sweep-protocol` (`SKILL.md:2`) and follows `graph.md` | PASS |
| C9 | Runtime path statements (`--root` holds `.git`; `--output` under `<root>/.dev/sweeps/`, apart from inputs) match `commands.py:64-123` | PASS |
| C10 | Statement about the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` is true on disk today (`sweep.md:16`) | FAIL (MINOR, F-1: backed by item 12.2, not yet done) |
| C11 | Command forms in the skill work outside a checkout or are labelled dev-only (`SKILL.md:24`) | FAIL (MINOR, F-2) |
| C12 | The tests pin the path rules (both surfaces in both files, order, no `src/superclaude/`) | FAIL (MINOR, F-3: mutations m1 and m4 survive) |
| C13 | `tests/commands` and `tests/recommend` pass; `ruff check` and `ruff format --check` clean | PASS (358 passed) |
| C14 | Pre-7.10 anchor: `pragmatic.md:22` now holds the scoped sweep exception, not the unqualified table mandate | PASS |
| C15 | The review wrote no repository file other than this report; `/tmp` copies deleted | PASS |

## Summary

- Checks passed: 12 / 15. Failed: 3, all MINOR (notes).
- BLOCKING: 0. MAJOR: 0. MINOR: 3 (F-1, F-2, F-3).
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 9 | Grep: 8 | Glob: 0 | Bash: 7 (one batched read-only script, one mutation run on `/tmp` copies, one pytest and ruff run, plus short single inspections). No live Orca, ccsession or Claude command was run.
- Not reviewed here (other lenses own them): the DESIGN 7.6 and R5 wording, the OQ records, the `step-7.10` and `test-sweep-command-summary` evidence, and the read-only and reader-clarity claims.

Verdict: PASS
Blocking count: 0

## QA Complete
