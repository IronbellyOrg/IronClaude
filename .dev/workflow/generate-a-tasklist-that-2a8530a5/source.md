# Source (inline prompt, persisted verbatim)

Generate a tasklist that covers all of the work mentioned above to refactor auggie-review.  Once done commit and push all planning artifacts to a branch and then open an issue with a description of the outlined work and links to the tasklist to be executed later

# Carried context (from the preceding /sc:analyze session, 2026-10-09)

The prompt refers to work analyzed earlier in the session. It is captured here so the plan is self-contained.

## Request that produced the analysis

Review the /sc:auggie-review command, skills and refs; report all references to /task-builder or /task; propose a refactor that replaces /task-builder with sc:workflow and /task with /sc:implement; validate with a sub-agent that the refactor removes all instances.

## Primitives in scope (all under src/superclaude/)

- commands/auggie-review.md
- agents/auggie-reviewer.md (only a `Task` tool mention; no change)
- skills/sc-auggie-review-protocol/SKILL.md
- skills/sc-auggie-review-protocol/refs/remediation-handoff.md
- skills/sc-auggie-review-protocol/refs/auggie-prompts.md, severity-rubric.md, evals/evals.json (no hits; no change)

## Inventory (case-insensitive "task", 59 hit lines)

- commands/auggie-review.md: 10 (L52, 88, 101, 135, 136, 137, 138, 150, 166, 167); L88 is the `Task` tool
- skills/sc-auggie-review-protocol/SKILL.md: 10 (L4, 183 are the `Task` tool; L327-331, 345, 355, 368 are real refs)
- skills/sc-auggie-review-protocol/refs/remediation-handoff.md: 38 plus 3 BUILD_REQUEST/MDTM-only lines (L78, 91, 94)
- agents/auggie-reviewer.md: 1 (L14, the `Task` tool)

## Chain change

- Phase A: /sc:design (unchanged)
- Phase B: task-builder skill + BUILD_REQUEST becomes `/sc:workflow <output_dir>/remediation-spec.md --handoff none`
- Phase C: `/sc:reflect --type task --analyze` becomes `/sc:reflect --mode pre --spec <spec> --tasklist <plan.md>`
- Phase D: user runs `/task <path>` becomes user runs `/sc:implement <plan.md>`
- Phase E: `/sc:reflect --type task --validate` becomes `/sc:reflect --mode post --diff <output_dir>/remediation.diff --tasklist <plan.md>`

## Design decisions and findings (incl. validator sub-agent results)

- /sc:workflow takes ONE source (file or inline prompt), not a BUILD_REQUEST: append a "Remediation Context" section (goal, why, files) to remediation-spec.md before Phase B.
- plan.md lands in `.dev/workflow/<slug>/` (--output must stay under .dev/workflow/), not next to REVIEW.md; slug is unpredictable, so read the printed plan path and confirm return-contract.yaml.
- Never use `--handoff implement` (it auto-invokes /sc:implement and breaks the no-auto-execute rule).
- Phase E runs before the user commits, so a git ref misses the work: record base_sha, write `git diff <base_sha>` (plus untracked files) to remediation.diff.
- Intentional residuals after refactor: the `Task` subagent tool (4 lines) and the external reflect flag `--tasklist`.
- Stale wording without the word "task" must also change: "reflect-analyze/-validate", remediation-handoff.md L152 (quotes old reflect doc), L191.
- SKILL.md L324 says "four phases"; chain has five.
- Stray text `co` at commands/auggie-review.md L60 (uncommitted typo) is deleted.
- Pinned by tests/pr_submit/test_static_grep.py: `--remediation-offer` table row, `quick` in `--depth` row, `prism-b` in `--auggie-model` row, `--model "${AUGGIE_MODEL:-prism-b}"` in SKILL.md.
- Out of scope: src/superclaude/commands/reflect.md mentions of task-builder//task (L101, 137, 206, 275, 285); missing src/superclaude/hooks/scripts/offer-pr-review.sh expected by tests; .dev/eval-workspaces/sc-auggie-review/** frozen artifacts.
