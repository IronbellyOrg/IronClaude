# Revision 2 brief for the stage 1 to 4 plan packages (2026-11-16)

Shared instructions for the four agents that revise the stage 1, 2, 3 and 4 plan packages in place. Read this file first, then `OPEN-QUESTIONS.md` (sections 2 and 3) in the same program folder.

## Why

The pre-execution reviews of stages 1, 3 and 4 said NEEDS-REVISION (stage 2's review did not finish). The owner then answered open questions on 2026-11-16 (recorded in `OPEN-QUESTIONS.md` section 2): `/sc:task` and task-builder are being retired; IronClaude is not installed as a plugin; static QA checks for active workflows stay; the follow-up carrier is `/sc:implement`'s final review step (approved).

No package has been run with `/sc:implement`, so each plan can be edited in place now. The plan file name, slug and frontmatter stay the same.

## Shared design decisions (apply in every stage; do not reopen them)

1. **Retired carriers are not edited.** No task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those. They keep today's text until the owner's retirement removes them. The stage 1 "Merge-rule allow-list" section in `refs/scale-map.md` lists them as `exempt-by-retirement` (by path only, no merge-rule phrase and no old definition sentence written in it), with the sentence that the exemption ends when the retirement removes the file. Tests that exist only to pin those files are not re-pinned by these plans; the retirement owns them. When a test pins both a retired and an active carrier, the plan re-pins the active carrier's part only.
2. **The follow-up carrier is `/sc:implement`'s final review step, record and print only.** Verified facts the plan must respect: `src/superclaude/skills/sc-implement-protocol/refs/qa.md` keeps its own scale and is NOT edited (it is on the not-built list); `qa.md` line 225 says the final summary "is informational and never asks the user anything"; `qa.md` lines 276 to 288 close the list of interrupts ("No other path may stop automation or prompt the user"). So the edit goes into `src/superclaude/skills/sc-implement-protocol/SKILL.md` (final summary instructions) and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (archive gate, run before the package moves in step 6): one read-only call of the sweep command over the follow-up ledgers the package's review loops wrote, and a printed list in the final summary with the plain-English line naming how the owner can file them. It asks nothing and prompts nothing. The once-per-run offer question stays with the top-level session through the output style (the `pragmatic.md` Medium rule, changed from per loop to per run in stage 3) and with the consent-bound filing path (OD15); stage 2 adds no question to `/sc:implement`. Say this in the plan in one sentence so a reviewer sees the choice.
3. **tech-research** (`src/superclaude/skills/tech-research/SKILL.md`) is an active workflow and keeps its ledger-writing edit as already planned (no sweep, no offer there).
4. **Plugin surface.** IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin. Do not create any new plugin surface: no `plugins/superclaude/skills/sc-review-severity/` mirror, no plugin parity test (T15), no `canonical` registry row for a plugin path. Existing hand-kept plugin twins (`plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`) are touched only where an existing test pins them and the active source carrier changes; say so in the plan. The registry keeps exactly 11 `digest` rows, 1 canonical, 2 pointer-only and 5 installed-only unless the review findings below require a different count; if you change a count, change it everywhere and say why. OPEN-QUESTIONS.md section 3.4 records that this reassessment is the plan author's and the owner has not confirmed removing plugin parity.
5. **Ledger decision (owner question 5).** Version 1 keeps `follow-ups.md` as a separate file; no mapping to `review-ledger/1` rows is built in these plans. The stage 1 reuse-audit result decides whether a mapping is ever added. No plan task replaces or edits `src/superclaude/cli/review/ledger.py`.
6. **Do not use `/sc:implement`, commit or push.** Stage with `git add .dev/tasks` only. Never stage under `.claude/`.

## Rules for the plan files (from `~/.claude/skills/sc-workflow-protocol/refs/quality-gates.md`)

- Keep frontmatter keys as they are. Phases: 4 to 8. Task numbers contiguous from 1. `Depends on: Task K` only to a lower K. Every task has `Acceptance criteria:` with at least one bullet. No checkbox lines and no numbered lines (`1.`, `1)`) anywhere. No absolute paths and no `.dev/tasks/to-do/` prefix in operational links (name a package by id and say "found in the to-do or done subfolder of the repository task folder").
- No document written by a task may say `.dev/tasks/` is never staged.
- An acceptance line that a later task of the same package makes false carries its end point ("until Task N").
- Acceptance checks are pinned by content (quote the sentence protected); never by a line number alone.
- Python is `uv run python ...` only.

## What to do (each agent, for its stage)

1. Read the plan, its `source.md`, its stage request in `stage-requests/`, its `artifacts/codegraph-grounding.md`, and the review output named below. Verify each finding against the live files before you change the plan (a finding the live files do not support is recorded as not applied, with the reason).
2. Edit the plan in place with the Edit tool: fix every BLOCKING finding; fix the non-blocking findings that are cheap and clear; apply the shared design decisions above; renumber tasks and fix every `Task N` reference if you add, remove or merge tasks. Keep the phase count within 4 to 8.
3. Append a `## Revision 2 (2026-11-16)` section to the stage request file in `stage-requests/` listing what changed and why (finding id or decision), then copy it byte for byte to the package's `source.md` (`cp`). The plan's `source:` stays `./source.md`.
4. Append a `## Revision 2` section to the package's `artifacts/codegraph-grounding.md`: what you re-checked (file existence with `test -e`, symbols, dependents, with the commands), and a line for each finding applied or not applied.
5. Run the gate check from the task folder: `cd .dev/tasks/to-do && uv run python /tmp/gate_check.py` (it checks all four stage packages; yours must print PASS; the "never stage" wording check must not fire on your plan). Fix and re-run until your package passes.
6. Run `git add .dev/tasks` from the repository root. Do not commit.
7. Final message to the main session (plain text, under 2000 characters, no file bodies): the plan path, the task count before and after, one line per finding id with applied, partly applied or not applied and why, every cross-stage fact another stage's plan must match (file names, command names, artifact names, task counts), and anything you could not do. If a Write or Edit is refused, say which file and return the exact text you intended.

Work only on your stage's files plus the shared files named in step 3. Do not edit another stage's plan; report cross-stage needs in your final message.
