# RCA #2 — Eval-harness / tooling hypothesis

## Investigation method

1. Inventoried the relocated workspace at `/config/workspace/IronClaude/.dev/eval-workspaces/sc-release-split-protocol/`. Read `fidelity_checker.py`, `trigger-eval-set.json`, `iteration-1/learning-loop-observability/eval_metadata.json`, `iteration-1/learning-loop-observability/with_skill/grading.json`, and `iteration-1/benchmark.json`.
2. Searched the IronClaude repo for any tooling that could produce these specific filenames (`iteration-N/`, `with_skill/`, `without_skill/`, `eval_metadata.json`, `grading.json`, `benchmark.json`, `fidelity_checker.py`, `trigger-eval-set.json`). Searched `Makefile`, `pyproject.toml`, `scripts/`, `tools/`, `tests/`, `src/`, `*.sh`, `*.py`, `*.json`, `*.md`.
3. Reviewed `scripts/eval_runner.py`, `scripts/eval_1.py..eval_3.py`, `scripts/fidelity-check-setup.sh`, `scripts/run-fidelity-batch.sh`, `scripts/run-fidelity-batch-refactored.sh` to verify whether any in-repo runner emits this directory shape.
4. Checked git history for the workspace directory and the skill it sits next to (commit `6c84826`, 2026-03-18).
5. Searched outside the repo (`/config/.claude/`, `/home`) for the canonical filenames and found a hit in `/config/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/`.
6. Read the upstream `skill-creator` plugin: `SKILL.md`, `scripts/run_eval.py`, `scripts/run_loop.py`, `scripts/aggregate_benchmark.py`, `eval-viewer/generate_review.py`, `agents/analyzer.md`.
7. Cross-referenced every artifact filename in the IronClaude workspace against the upstream `skill-creator` SKILL.md — every name matches the upstream convention exactly.

## Findings (with evidence — file paths, line numbers, quotes from artifacts)

### F1. The workspace is the canonical output of Anthropic's `skill-creator` plugin

Upstream plugin path: `/config/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/`

Quote, `SKILL.md` line 167:

> "Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.)."

Line 180:

> "Save outputs to: `<workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/`"

Line 185:

> "Creating a new skill: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`."

Line 188:

> "Write an `eval_metadata.json` for each test case (assertions can be empty for now)."

Lines 225-229:

> "Save results to `grading.json` in each run directory… `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` — This produces `benchmark.json` and `benchmark.md`."

Every directory and filename in `/config/workspace/IronClaude/.dev/eval-workspaces/sc-release-split-protocol/` matches this convention 1-for-1:
- `iteration-1/` (SKILL.md L167)
- `iteration-1/<eval-name>/` named descriptively per L188 (`learning-loop-observability/`, `splittable-auth-system/`, `nosplit-bugfix-hardening/`, `ambiguous-large-plugin-system/`)
- `with_skill/outputs/`, `without_skill/outputs/` (SKILL.md L180, L185)
- `eval_metadata.json` per eval (SKILL.md L188)
- `grading.json` per run (SKILL.md L225)
- `benchmark.json` per iteration (SKILL.md L227-231)

### F2. The eval workspace was hand-rolled by Claude following the harness's instructions, not by an autonomous runner

The harness ships TWO independent automation paths, and neither is what produced this workspace:

- `scripts/run_eval.py` — runs **trigger-evals only** (does Claude pick up the skill from its description?). Output is a single JSON to stdout. It does NOT emit `iteration-N/<name>/with_skill/` directories. (`run_eval.py` L259-306)
- `scripts/run_loop.py` — wraps `run_eval` in a description-improvement loop. Saves to `--results-dir/<timestamp>/results.json` + `report.html`. Same trigger-only signal. (`run_loop.py` L283-323)

Neither writes `with_skill/outputs/<artifacts>` or grades qualitative outputs against assertions. That work — spawning paired `with_skill`/`without_skill` subagents per eval, drafting `eval_metadata.json`, capturing `timing.json`, running `agents/grader.md`, then aggregating with `aggregate_benchmark` — is described in SKILL.md as **a procedure Claude executes manually in-session** (SKILL.md "Step 1: Spawn all runs", L169-219). The harness orchestrates trigger-evals; qualitative evals are an instruction set Claude follows.

This is confirmed by the `metadata.executor_model: "claude-opus-4-6"` field in `iteration-1/benchmark.json` and by the existence of `fidelity_checker.py` — a bespoke domain-specific Python script written for this skill, not part of the plugin. No upstream runner produces a `fidelity_checker.py`; Claude wrote it inline because the release-split skill needed adversarial fidelity verification.

### F3. The harness's path convention is hardcoded in instructions, not in code defaults

The path `<skill-name>-workspace/` is enforced by **prompting Claude**, not by any default in argparse:

- `aggregate_benchmark.py` accepts `--output / -o` (L357-358) and a positional `benchmark_dir` (L342-345). It has no opinion about where the workspace lives. Caller passes the path.
- `generate_review.py` takes positional `workspace-path` (L9). No default.
- `run_loop.py` writes to `--results-dir/<timestamp>/` (L283-289), defaulting to `tempfile.gettempdir()` for the live HTML preview only.

Therefore there is **no env var, no flag, and no config file** in the upstream harness that controls where the workspace goes. The placement is purely the result of the SKILL.md instruction at L167 ("sibling to the skill directory") combined with the actual location of `sc-release-split-protocol` (`.claude/skills/sc-release-split-protocol/`). Sibling of that path is `.claude/skills/sc-release-split-protocol-workspace/`. Mechanically inevitable, given the instruction.

### F4. No in-repo runner ever produced this workspace

`scripts/eval_runner.py`, `scripts/eval_{1,2,3}.py`: orchestrate the **roadmap CLI pipeline**, not skills. They write to `.dev/releases/.../eval-results/` (eval_runner.py L37). Unrelated.

`scripts/fidelity-check-setup.sh`, `scripts/run-fidelity-batch.sh`: wrap `superclaude roadmap run` for past releases under `.dev/releases/complete/`. They produce `spec-fidelity.md`, not `fidelity_checker.py`-style results. Unrelated.

The IronClaude repo has its own `FidelityChecker` class (`src/superclaude/cli/roadmap/fidelity_checker.py`, used by `tests/v3.3/test_fidelity_checker.py`). It is a different artifact — a Python class for the roadmap pipeline. The 387-line `fidelity_checker.py` script in the workspace is bespoke ad-hoc tooling Claude wrote for this skill (it shells out to `claude -p ... --model haiku` for LLM grading; see L137-142). It was never part of the repo's installable code.

### F5. The skill itself doesn't acknowledge a workspace

`src/superclaude/skills/sc-release-split-protocol/` contains only `SKILL.md`, `__init__.py`, `refs/`. No `tests/`, no `evals/`, no workspace stub. The skill spec (SKILL.md L1-300) says nothing about an evaluation harness or a workspace directory. The workspace was generated externally and dropped into `.claude/skills/` as a sibling to the installed skill.

Git evidence: commit `6c84826` (2026-03-18 "Prepro to Framework Wide refactor") added `.claude/skills/sc-release-split-protocol-workspace/{fidelity_checker.py, trigger-eval-set.json, iteration-1/benchmark.json, eval-review.html}` together with `.claude/skills/sc-release-split-protocol/SKILL.md` in a single commit. There is no `src/superclaude/skills/sc-release-split-protocol-workspace/` counterpart — it was committed `.claude/`-only because it is not distributable. (Confirmed in `.dev/tasks/done/TASK-RF-20260325-001/phase-outputs/test-results/phase1-sync-result.md` line 9: "MISSING in src/superclaude/skills/: sc-release-split-protocol-workspace, task-builder, task, tech-research".)

## Root cause (one-paragraph hypothesis)

The eval workspace was created by Claude executing Anthropic's `skill-creator` plugin instructions in a development session. Skill-creator's `SKILL.md` (L167) hardcodes the convention "Put results in `<skill-name>-workspace/` as a sibling to the skill directory" — and because `sc-release-split-protocol` lives at `.claude/skills/sc-release-split-protocol/`, the mechanically-required sibling is `.claude/skills/sc-release-split-protocol-workspace/`. The harness has no flag, env var, or default path that can redirect this; the convention is enforced by prompting (Claude follows the SKILL.md instruction) not by tooling defaults. The IronClaude project's CLAUDE.md output-paths rule says writes should go to `.dev/` or the `--output` directory, but Claude prioritized the active skill's instructions over the project's rules — and there was no in-repo guardrail (CLAUDE.md addendum naming this skill, .gitignore pattern, or pre-write hook) to override the upstream convention. Result: workspace landed exactly where skill-creator told it to land. No in-repo eval runner exists for this skill; everything in the workspace is one-shot Claude-authored output (the bespoke `fidelity_checker.py`, the per-eval grading runs) executed under skill-creator's procedural template.

## Confidence in this hypothesis (0.0 - 1.0, with reasoning)

**0.92.**

Reasoning for high confidence:
- Every artifact filename matches upstream skill-creator SKILL.md verbatim (F1).
- The mechanical sibling-path inevitability is provable from one quoted instruction line (F3, SKILL.md L167).
- Upstream harness has been audited for path-handling — there is provably no flag or env var that could have redirected output (F3, argparse signatures inspected).
- No in-repo runner produces these filenames or this directory shape (F2, F4).
- Workspace was committed alongside the skill, not produced by a CI/Make target (F5, git evidence).

What keeps me from 0.99:
- I did not find a transcript of the actual session that produced the workspace, only the artifacts and the harness's instructions. It is logically possible (though unlikely) that some other harness with the same conventions exists — e.g., a forked or earlier version of skill-creator. The match is so exact (`with_skill`/`without_skill`/`grading.json` field names like `text`/`passed`/`evidence`, all matching SKILL.md L225) that another tool reproducing it independently is implausible but not impossible. 8 percentage points reserved for that.

## Refactor proposal

The harness cannot be modified — it's a vendored Anthropic plugin under `/config/.claude/plugins/marketplaces/claude-plugins-official/`. So the fix is project-local. Four options analyzed, recommended option called out:

**Option A — Project-local override file in `.claude/`.** Add `.claude/skill-overrides/skill-creator.md` with project-specific path conventions; rely on Claude reading both the plugin SKILL.md and the override. *Pros:* discoverable, lives next to other project Claude config. *Cons:* skill-creator doesn't have a documented override mechanism, so this is a soft norm Claude has to honor — not enforced. Same failure mode as today.

**Option B — Makefile/CLI wrapper that pre-creates a symlink.** `make eval-skill SKILL=sc-release-split-protocol` creates `.claude/skills/sc-release-split-protocol-workspace -> ../../.dev/eval-workspaces/sc-release-split-protocol`, then prints the resolved path for the agent to use. *Pros:* enforces redirect at the filesystem layer; harness writes happen but land in `.dev/`. *Cons:* requires the user/agent to invoke the wrapper before starting an eval session; if Claude is started via `/skill-creator` directly (no make), the symlink isn't there.

**Option C — CLAUDE.md addendum that explicitly overrides the plugin's instruction.** Add to `/config/workspace/IronClaude/CLAUDE.md`: "When using the skill-creator plugin, ignore its 'sibling to the skill directory' convention. ALWAYS place `<skill-name>-workspace/` under `.dev/eval-workspaces/<skill-name>/`. This override applies to all `iteration-N/`, `with_skill/`, `without_skill/`, `eval_metadata.json`, `grading.json`, and `benchmark.json` artifacts." *Pros:* zero infra; project CLAUDE.md is loaded with high priority; overrides plugin instructions per the system-reminder rule "These instructions OVERRIDE any default behavior". *Cons:* relies on Claude obedience to written rules — same failure mode as today, just with a more specific rule.

**Option D — Pre-write guardrail hook in `.claude/settings.json`.** Configure a `PreToolUse` hook on `Write` and `Edit` that rejects paths matching `.claude/skills/*-workspace/**` and rewrites them to `.dev/eval-workspaces/<skill-name>/**`. *Pros:* enforced by the harness, not by Claude obedience; survives any future skill that follows the same convention; produces a clear error message that teaches the right path. *Cons:* hook must be careful not to break legitimate writes inside non-workspace paths under `.claude/skills/` (the actual skill files); requires testing.

**Recommended: Option D + Option C in combination.** Option D is the only enforcement that doesn't rely on Claude reading and obeying instructions. Option C documents the rule for human readers and gives Claude a chance to do the right thing without triggering the guardrail. Together: the rule is written down (C), and the rule is enforced (D). Option B is a useful additional convenience for anyone running eval sessions outside Claude.

## Acceptance criteria

1. A new eval session for any skill in `.claude/skills/X/` writes its workspace to `.dev/eval-workspaces/X/`, never to `.claude/skills/X-workspace/`.
2. If Claude attempts to `Write` to `.claude/skills/*-workspace/**`, the operation is blocked by a pre-tool-use hook with a message pointing to the correct path. (verifies Option D)
3. `CLAUDE.md` contains an explicit override for the skill-creator plugin's sibling-workspace convention. (verifies Option C)
4. `make eval-skill SKILL=<name>` creates the `.dev/eval-workspaces/<name>/` directory and prints the absolute path for use as the workspace root. (verifies Option B convenience)
5. `make verify-sync` continues to pass; `.claude/skills/` contains only the actual skill directories (`sc-release-split-protocol/` etc.), no `*-workspace/` siblings.
6. Existing relocated workspace at `.dev/eval-workspaces/sc-release-split-protocol/` continues to work with `aggregate_benchmark.py` and `generate_review.py` (since both accept positional paths).

## Limitations / what this hypothesis can't explain

- I cannot prove from artifacts alone *which session* placed the workspace there or whether it was a single Claude invocation or several. The git history shows everything landed in one commit, but that commit could batch multiple sessions.
- This hypothesis explains why the workspace is at the wrong path. It does NOT explain why the workspace was committed at all (Anthropic eval workspaces are typically `.gitignore`'d). That overlaps with the **governance/naming** angle (RCA #3): no `.gitignore` rule for `*-workspace/` and no review gate caught the addition. RCA #3 should investigate why the commit was accepted.
- It also doesn't explain why the team chose `skill-creator` for this skill specifically (vs a custom in-repo eval). That's a process question for RCA #1 (the skill's own behavioral spec) — does `sc-release-split-protocol` itself instruct or imply use of a particular eval workflow?
- If RCA #3 finds the `.gitignore`/governance angle is the only fix the team wants, this RCA's Option D guardrail is still recommended — instructing-the-LLM rules historically fail under context pressure, and the hook is the only enforcement that doesn't.

If this angle dead-ends in implementation (e.g., the team decides not to add a hook), the most informative remaining angle is **RCA #3 governance** — specifically a `.gitignore` rule for `**/*-workspace/` plus a `make verify-sync` check that flags any `.claude/skills/*-workspace/` directory as an error before commit.
