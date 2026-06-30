# Research Notes: Execute the PR #197 reduce-then-merge plan (feat/rf-harness-sync)

**Date:** 2026-06-28
**Scenario:** A (Explicit — user supplied the full 6-phase spine + exact per-phase validation commands)
**Depth Tier:** Standard
**Track Count:** 1 (the 6 phases are strictly sequential and contribute to one cohesive merge — NOT independent streams)
**Status:** Complete
**Driving spec:** `.dev/brainstorms/pr197-final-merge-strategy/merged-requirements.md` (§7 = step spine; Appendix = per-file matrix)

---

## EXISTING_FILES

**Worktree / branch state (verified `git` 2026-06-28):**
- cwd / worktree root: `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation`
- Branch: `feat/rf-harness-sync`; **5 commits ahead, 0 behind `origin/master`** (origin = `IronbellyOrg/IronClaude.git`, the fork). `origin/HEAD → origin/master`.
- `git merge-base HEAD origin/master = cda6e2d4526c73a3d2739a3bf6efb500c4402f60` (= origin/master tip; branch is strictly ahead). This is `start_commit` for frontmatter.
- Working tree: only untracked `.dev/brainstorms/...` + `.dev/reflect/...` (the reduction has NOT been applied yet).
- `git diff --stat origin/master...HEAD` = **18 files, +7920/-664** — matches the Appendix matrix exactly.

**The 18 files and their VERIFIED disposition (Appendix matrix):**

ACCEPT (additive, already on branch, NO edit) — 11 files:
- `src/superclaude/skills/operational-guide/SKILL.md` (NEW, +1656)
- `src/superclaude/skills/readme/SKILL.md` (NEW, +2161)
- `src/superclaude/skills/roadmap/SKILL.md` (NEW, +2678)
- `src/superclaude/skills/tech-reference/SKILL.md` (rewrite ±437)
- `src/superclaude/skills/tech-research/SKILL.md` (rewrite ±827)
- `src/superclaude/skills/task/SKILL.md` (/task lens QA ±343)
- `src/superclaude/agents/{rf-assembler,rf-task-builder,rf-task-executor,rf-task-researcher,rf-team-lead}.md` (small corrective tavily/RF-sync tweaks)

DROP / restore-master (Decision B) — 3 files:
- `src/superclaude/cli/reflect/runner.py` → `git checkout origin/master --` (target EXISTS on master ✓)
- `tests/cli/reflect/test_no_nesting_guard.py` → `git checkout origin/master --` (target EXISTS on master ✓)
- `tests/cli/reflect/test_inline_directive.py` (NEW +50) → `git rm` (absent on master ✓ — confirmed; new in 197)

REJECT / restore-master (Decision A refs) — 2 files (pure rewrite, full restore):
- `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` → `git checkout origin/master --` (EXISTS on master ✓)
- `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` → `git checkout origin/master --` (EXISTS on master ✓)

HUNK-SURGERY (mixed accept/reject within one file) — 2 files:
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (±40): restore master §7.1/§11.3/§9.3-telemetry; RETAIN EV-1 §8 + EV-2 §9 + §12 detector; reword changelog.
- `src/superclaude/skills/task-builder/SKILL.md` (±143): RETAIN EV-3/EV-4 + reflect_post_mode/--cli/CLI_MODE (already on branch); FLIP CLI clause-1 polarity to exclusion model.

## PATTERNS_AND_CONVENTIONS

- **Source-of-truth discipline (CLAUDE.md, hard):** edit `src/superclaude/` ONLY, then `make sync-dev` copies → `.claude/`. `make verify-sync` must pass. NEVER edit `.claude/` directly; NEVER `git add` any `.claude/` path except `settings.json`; if `git add` needs `-f` on `.claude/`, STOP.
- **PR target (CLAUDE.md, hard):** fork `IronbellyOrg/IronClaude` ONLY. Every `gh pr` invocation MUST carry `--repo IronbellyOrg/IronClaude`. Never bare `gh pr`, never upstream `SuperClaude-Org`.
- **Single-line commands only** (memory `feedback_no_multiline_paste`): no heredocs, no `\` continuations, no multi-line quoted strings.
- **make lint ≠ CI ruff format** (memory): `make lint` = `ruff check` only; CI separately runs `ruff format --check src/ tests/`. Step 5 runs BOTH.
- **ruff version-mismatch footgun** (memory `reference_ruff_version_mismatch_worktree`): `uri run ruff format src/ tests/` (write mode) can reformat ~106 unrelated files; step 5 uses `--check` (read-only) which is safe. If a format gap is found, scope the fix to changed files only.
- **Augment re-review trigger** (memory `reference_augment_review_triggers`): pushes do NOT re-trigger Augment; you MUST comment `auggie review` on the PR after pushing for the re-review to fire.
- **`git checkout origin/master -- <path>`** restores master's blob into the working tree + index regardless of branch commit history — correct mechanism for DROP/REJECT full-file restores.

## GAPS_AND_QUESTIONS

1. **Reflect SKILL.md hunk surgery (step 3) is the highest-risk item.** Branch SKILL.md currently has only 3 telemetry-token hits — ALL inside the changelog prose at line 699 describing their REMOVAL (`1.5.1: ... removed ... executor_class_source / executor_class_resolved / executor_exclusion_degraded`). `origin/master` SKILL.md has **8** hits (the real §9.3 telemetry blocks + §7.1/§11.3 rule text). Step 3 must restore master's actual telemetry/§7.1/§11.3 blocks while NOT clobbering EV-1/EV-2 (which are net-new — 10 hits on branch, 0 on master). This is genuine hunk-level surgery: a naive full `git checkout origin/master` of SKILL.md would DESTROY EV-1/EV-2. → Needs a researcher to map exact line ranges of each master block to restore and each EV block to retain.
2. **task-builder clause-flip blast radius (step 4).** Clause 1 (line 2245) is the named flip target, but the same "instance-level independence / does NOT class-exclude" framing also appears at lines 2170 (frontmatter comment), 2246 (clause 2), 2250 (clause 6), 2276 (frontmatter population note). Flipping ONLY clause 1 leaves the note internally contradictory. Decision needed: flip clause 1 + harmonize the dependent assertions (2/4/6 + provenance lines) so the note is consistent under the exclusion model. The user's directive says "FLIP the CLI-mode clause-1 polarity"; faithful execution = clause 1 primary + harmonize dependents to avoid contradiction.
3. **contract changelog reword (step 3).** Line 699 changelog carries `1.5.1: instance-level anti-self-confirmation (§7.1) replaces executor-class exclusion (removed ... telemetry ...)`. §3.1 requires rewording to DROP the instance-level/"replaces exclusion" claim, keep only the EV-1/EV-2 runtime-hardening note, `contract_version` stays `"1.7.0"`.

## RECOMMENDED_OUTPUTS

Generated MDTM tasklist with 7 phases (Phase 0 baseline → Phases 1-6 mapping the spec's Steps 1-6 → final completion), Template 02. Each phase = ordered B2-self-contained items with the user's EXACT single-line validation commands embedded. Hard constraints baked into a Prerequisites/Constraints block AND restated per-item where load-bearing.

## SUGGESTED_PHASES (researcher assignments — 4 parallel general-purpose)

- **R1 — File-inventory / git-disposition (verify+extend).** Confirm all 18 file dispositions; produce the exact single-line `git checkout origin/master -- <paths>` and `git rm <path>` commands for steps 2/3; confirm master-restore targets + new-file rm target. Output: `research/01-git-disposition.md`.
- **R2 — Reflect SKILL.md hunk-surgery surface (HIGHEST RISK).** Diff branch vs `origin/master` for `sc-reflect-protocol/SKILL.md`; enumerate (a) master blocks to restore (§7.1, §11.3, §9.3 telemetry, input-resolution `--executor-model` line, metrics.json block) with line ranges, (b) EV blocks to RETAIN (EV-1 §8 ORCHESTRATOR-VERIFIES-ON-DISK, EV-2 §9 merge_method legal-values, §12 file_present+card_count detector) with line ranges, (c) the exact changelog line to reword. Output: `research/02-reflect-skill-hunk-surface.md`.
- **R3 — task-builder SKILL.md clause-flip surface.** Locate clause 1 + dependent clauses (2/4/6) + provenance lines (2170/2276) asserting instance-level; quote each verbatim; propose the exclusion-model rewording for each so the note is internally consistent; confirm EV-3/EV-4 + reflect_post_mode/--cli/CLI_MODE hunks are present and RETAINED (not restored). Output: `research/03-taskbuilder-clause-flip.md`.
- **R4 — Template, examples, tests, validation commands.** MDTM template 02 rules (A3/A4/B2/M3); 1-2 existing tasklist examples in this worktree's `.dev/tasks/to-do/`; verify validation commands resolve (`make sync-dev`/`make verify-sync`/`make lint` targets in Makefile; markdownlint invocation via `.markdownlint.json`; `uv run pytest tests/cli/reflect`, `tests/swarm`; `ruff format --check`); confirm `gh pr` fork-target shape + PR #197 URL. Output: `research/04-template-tests-validation.md`.

## TEMPLATE_NOTES

- **Template 02** (complex): multi-phase, sequential dependencies, conditional hunk surgery, embedded validation gates. NOT template 01.
- **QA_GATE_REQUIREMENTS: NONE** for the generated tasklist. Rationale: this is a deterministic git-reduction + targeted-edit task whose verification is the user's exact per-phase validation commands (pytest/grep/make/markdownlint) embedded as explicit `- [ ]` items, plus the external `auggie review` gate (step 6). It does NOT produce documents or transform source material, so MDTM M3/M4 multi-agent QA gates do not apply. (A.10.5's "minimum 6 agents per gate" rule only applies to QA gates the tasklist actually contains; a task with no agent-QA gates is not penalized.)
- **POST_REFLECT_GATE: DISABLED.** The user's explicit 6-phase plan ends at external `auggie review` as the review gate; no reflect POST step is in scope. Running `superclaude reflect run` as a POST self-audit would invoke the just-edited `sc-reflect-protocol` skill (self-referential + fragile) and is out of the stated scope. Documented as a reversible decision note in the tasklist.
- **TESTING_REQUIREMENTS:** the tasklist RUNS existing tests (`tests/cli/reflect`, `tests/swarm`) as validation; it authors NO new tests (step 2 in fact REMOVES `test_inline_directive.py` and restores master's `test_no_nesting_guard.py`). So no new-test authoring items.
- **VALIDATION_REQUIREMENTS:** the user's per-phase single-line commands are authoritative and must appear verbatim as verification clauses.

## AMBIGUITIES_FOR_USER

- **task-builder clause-flip blast radius** (GAPS #2): flipping clause 1 alone leaves clauses 2/4/6 + provenance lines contradictory. Faithful resolution = flip clause 1 + harmonize dependents to the exclusion model. The tasklist encodes this as an explicit decision within the step-4 item and surfaces it in Open Questions so the user can constrain the flip to clause-1-only if they prefer. NOT a blocker — proceeding with the harmonize-dependents interpretation as most-reasonable.
- All other intent is unambiguous: the user supplied the phases AND the exact validation commands.
