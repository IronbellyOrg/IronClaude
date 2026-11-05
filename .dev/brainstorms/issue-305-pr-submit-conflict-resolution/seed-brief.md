---
topic: "Add merge-conflict resolution to sc:pr-submit (issue #305): decide whether new tool calls, new refs, new templates and/or new agents, or which combination, is the most effective approach, and how to structure it efficiently so process complexity is layered on only as merge-conflict complexity increases (for example: trivial and lockfile/generated-file conflicts first, then text conflicts, then semantic conflicts that need a human). Must keep sc:pr-submit's push rules (one fix commit per cycle, never force-push, pre-push head guard, push_parent_ok) or change them only explicitly, and must say how a resolution is published without force-pushing (e.g. a merge commit of the base into the PR branch)."
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-04T13:10:00Z
---

# Seed Brief: pr-submit-conflict-resolution

Socratic dialogue: standard depth, `code` domain, Clarify + Validate batches (10 questions), auto-answered from the issue text, the orchestrator brief and the code (not interactive).

## Dialogue (auto-answered)

1. Entry point: `/sc:pr-submit` (command `src/superclaude/commands/pr-submit.md`, skill `src/superclaude/skills/sc-pr-submit-protocol/`, core `src/superclaude/pr_submit/`). New capability, not a bug fix.
2. Scope: a new subsystem inside one existing tool: skill wave(s) + ref(s) + small pure-Python core helpers + tests; possibly an agent and a template.
3. Behaviour to add: when the PR branch conflicts with its base (GitHub `mergeable: CONFLICTING` / `mergeStateStatus: DIRTY`, or a local `git merge origin/<base>` stops), resolve the conflicts safely and publish the resolution without force-pushing; today the skill only reports "behind base" on the `--pr` path and halts on the create path.
4. Non-negotiable constraints: the push rules (one fix commit per cycle, never force-push, pre-push head guard `pr_head_ok`, `push_parent_ok`), `--monitor` ordinal ceilings (L1 propose only, L2 local only, L3 push), `--repo` pinned to origin, never stage `.claude/` except settings.json, never stash (worktrees share one stash stack), the write-ahead run log and `--resume`.
5. Done: a released design implemented with tests in `tests/pr_submit/`, lint/format/verify-sync green, docs (SKILL.md, refs, command) updated.
6. Existing implementations: Wave 0 behind-base check (`needs_rebase`), Wave 6 fix commit + pre-push head guard + push triad, VAL gates, `refs/troubleshoot-dispatch.md`, `evidence-validator` agent. `push_parent_ok` today rejects any commit with two parents, so a merge commit cannot be pushed without an explicit, tested change.
7. Consumers: the operator running the attended session; GitHub reviewers (Augment, Codex) who re-review the new head.
8. Test surface: unit tests of pure core helpers (classification, tier routing, merge-parent check, run-log events) plus static-grep tests of the skill text; no live git network tests.
9. Forcing function: issue #305 (featRel, next release of sc:pr-submit).
10. Rollback: a merge commit is reversible with a normal revert commit; nothing is rewritten; a halt leaves the merge in progress or aborted locally with nothing pushed.

## Problem Statement

sc:pr-submit cannot get a PR out of a merge-conflict state. Reviews and CI can be clean while GitHub refuses the merge, and the only output is a report. Conflicts range from mechanical (lockfiles, generated files, adjacent edits) to semantic (both sides changed the same behaviour) and the process must not pay the semantic-conflict cost for a lockfile conflict.

## Known Context

- Research: 424 behaviours from three community skills, ROI-scored by /ponytail-review; 74 scored above 5 (`.dev/research/issue-305-conflict-resolution/03-roi-scored-list.md`). High scorers: never leave markers; forbid blanket `--ours/--theirs .` and `reset --hard`; read index stages 1/2/3; resolve by intent and halt when intent is not statable in one sentence; never invent a third behaviour; say what was dropped; migrations, submodules and binaries halt; generated files regenerate from resolved sources; `uv lock` for uv.lock; tree conflicts (DU/UD/AA) via `git status`; never stash; current worktree only; never `--no-verify`; stage exact paths.
- Ranking and top-3 rationale: `.dev/research/issue-305-conflict-resolution/01-recommend-plugin-results.md`.
- Merge (not rebase) is the only way to integrate the base into a published PR head without a force-push; the resulting merge commit has parents `[pr_head, base_tip]`.

## Constraints

- Keep every push rule; any change (for example a merge-commit variant of `push_parent_ok`) must be explicit, narrow and tested.
- Layer complexity: cheap deterministic tiers first; model judgment only for text conflicts; human halt for semantic or high-risk conflicts.
- Deterministic decisions in the importable core; git/gh I/O in the skill/scripts; refs lazy-loaded per wave.
- No new external dependency (no mergiraf requirement); no global git config changes.
- Installed primitives must not hardcode `src/superclaude/` paths.

## Success Criteria

- A conflicted PR at L3 with only mechanical conflicts ends with one merge commit pushed fast-forward and the PR mergeable.
- Text conflicts are resolved with stated intent per side, recorded per file, validated by VAL; unclear intent halts.
- Semantic/high-risk conflicts halt with a clear message and nothing pushed.
- L1 proposes only; L2 leaves the resolved merge uncommitted or committed locally with nothing pushed.
- All existing tests still pass; new tests pin the tiering, the merge-parent check and the halts.

## Open Questions

- New agent, or reuse troubleshoot/evidence-validator plus a ref?
- When does conflict resolution run: Wave 0 (before reviews), after reviews are clean, or both?
- Does a conflict resolution consume a review round, and does it re-trigger reviewers?
- Where does the merge commit fit with "one fix commit per cycle": a separate cycle type, or the cycle's single commit?
- L2 semantics: leave the merge in progress, or commit locally without pushing?
- Template for the per-file resolution record and the HALT message: new template file or inline in the ref?
- The SKILL text contradicts itself on the create path: Wave 0 says rebase when behind base (SKILL.md:267) while the STOP block and Error Handling row say HALT (SKILL.md:220-223, :315). Which wins?

## Enrichment Context

Sources: codebase `fallback_1` (auggie codebase-retrieval not available in this session; codegraph index healthy, then Grep/Read); research `skipped` (external research already done in steps 1-3 of issue #305, see Known Context). Full artifact: `enrichment/codebase-context.md`.

- `push_parent_ok` rejects any commit with two parents (`src/superclaude/pr_submit/fsm.py:593`), pinned by a test; publishing a merge commit needs a new, explicit check (parents exactly `[pre_push_sha, base_sha]`).
- The Wave 6 fix commit uses `git commit --only -- <paths>`, which git refuses during an in-progress merge: a merge commit needs its own commit step (plain `git commit` after exact-path staging, `GIT_EDITOR=true` or `--no-edit`).
- Recovery (`recovery.py`) and push records have no field distinguishing a merge push from a fix push; the push idempotency key is `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`.
- Nothing reads GitHub `mergeable` / `mergeStateStatus` today (zero grep hits in src/ and tests/).
- Test pins that a design must respect: SKILL.md has exactly one python code block executed by two tests (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`); the run-log event count is pinned at 41 (`tests/pr_submit/test_run_log.py:168`, `tests/pr_submit/test_codex_reviews.py:441`); T-N50 bans the words "git" and "gh" in `fsm.py` and `refs/state-machine.md`; `tests/pr_submit/test_static_grep.py:627-755` pins the push-guard wording and order.
- No existing template for a resolution record or HALT message; `merge-executor` agent merges debate documents, not git branches; `evidence-validator` is read-only and reusable for checking a stated intent against evidence.
