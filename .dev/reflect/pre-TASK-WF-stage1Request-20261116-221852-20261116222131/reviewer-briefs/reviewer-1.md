# Reviewer 1 brief (persona: analyzer, model class: sonnet)

Task: UC-1 pre-execution audit. Audit the plan .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md against its source .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/source.md (absolute: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/...). Report deviations and gaps with file:line citations you have Read. You are read-only; do not run commands.

## T1 card excerpt

## Analyzer slice (root cause and deviation candidates)

- A1 Source is layered: lines 3 to 22 (the original request) say stage 1 "creates new files only ... edits no review-loop carrier" and "No edit of any carrier (pragmatic.md, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT)"; Revision 2 (line 36) says "sc-implement-protocol joins the not-edited list"; Revision 4 (lines 61 to 67, "authoritative where it differs") edits SKILL.md and refs/managed-workspace.md of sc-implement-protocol, their two plugin twins, and src/superclaude/cli/review/__init__.py. The plan resolves this in its Constraints (first two bullets). Candidate deviation: Authorized expansion by Revision 4, if the plan states the precedence unambiguously.
- A2 Source line 66 requires the stored-tag name `protected-risk-dispute` to be absent ("no stored tag `protected-risk-dispute`"); the plan says "no stored tag for a safety hit exists" and never names the string. Candidate: minor omission.
- A3 Source line 22 lists "the 35 percent target" among things not to change; plan Constraints "Also not built" names the cap of 2 fix cycles, qa.md, own-scale primitives but not the 35 percent target. Candidate: minor omission.
- A4 Source line 18 asks for a final owner-summary task (./artifacts/stage1-summary-for-owner.md); Revision 4 cut row C10 removes it (line 63); the plan has no such task and its Not-built bullet lists "the owner summary file". Candidate: Authorized (cut).
- A5 Coverage parse: Pass 1 found 9 ids (R-001 to R-008, REQ-09) that are review-recommendation and requirement-number mentions inside Revision 2 and 3 prose, not requirements; coverage_pct (parsed) = 0.0 is therefore an artifact. Pass 2 produced 15 inferred rows; 5 match a task by containment, 10 do not, but 7 of those 10 have 0.53 or more of their content words in the plan's Constraints section (a section, not a task item, which the protocol does not count).


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T22:19:30Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/source.md:59-67

```markdown
Applied to the plan in place (plan file name, slug and source path unchanged; the package now has 2 tasks in 2 phases and frontmatter `depth: quick`, down from 16 tasks in 4 phases). Source: `cuts-debate/final-cuts.md` (authoritative where it differs from the revisions above). The Goal, the title, every `Task N` and every `Depends on` line were rewritten.

- **Kept, as Task 1 (was Task 13, rebuilt standalone).** `src/superclaude/cli/review/safety_route.py` (GR1 vocabulary in one list, GR12 raise-only rule), `src/superclaude/cli/review/safety_cmd.py`, the subcommand `superclaude review safety-scan <file>` registered in the tuple of `src/superclaude/cli/review/__init__.py`, and the tests `tests/review/test_review_safety_route.py` and `tests/review/test_review_safety_cmd.py`. It takes plain row text, imports no codec and no classifier, reports unreadable or missing input as such (exit 2, never a hit count), and stores no tag.
- **Kept, as Task 2 (was stage 2 Task 3, shrunk to print-only).** Paragraph "Follow-up print (record and print only)." in `SKILL.md` ("Done") and `refs/managed-workspace.md` (after the closing fence of the `FINAL:` block, before step 6); prints every non-superseded minor line of every task's notes file, runs `superclaude review safety-scan` over each notes file, prints "no notes file for T<id>" for a missing file, asks nothing, changes no verdict or archive outcome; both files copied byte for byte to the plugin twin (pinned by `test_h_implement_protocol_plugin_twins_byte_equal`); `refs/qa.md` unedited (SHA-256 recorded at the task start); active-flow smoke check recorded in `./artifacts/print-smoke.txt`.
- **Cut: Tasks 1 to 12, 14, 15 and 16.** C1 (classifier, its inputs supplier and its command: Tasks 5, 9, 10, 11 and 12), C2 (follow-up ledger codec, filing logic and the ledger reference: Tasks 4, 7 and 8), C4 (skill folder, rule, scale map, registry, install check and registry drift tests: Tasks 1, 2, 3, 6, 14 and 15), C10 (the owner summary: Task 16). C3 shrank the stage 2 carrier to the print. C7 cut the shadow stage and the five-run gate, keeping only the print and its smoke check. One Constraints bullet states that these are not built.
- **Stage 2 is withdrawn into this package.** Its seven other tasks are cut (rows C2 and C7); its ledger row and request file are marked withdrawn by the main session.
- **Depth.** Two tasks fit `depth: quick` (2 to 4 phases, one task per phase). The program gate checker `/tmp/gate_check.py` requires `depth: standard` and 4 to 8 phases; it fails this package for that reason only.
- **Names stages 3 and 4 must match:** command `superclaude review safety-scan <file>` (option `--unattended`); files `src/superclaude/cli/review/safety_route.py`, `src/superclaude/cli/review/safety_cmd.py`, `tests/review/test_review_safety_route.py`, `tests/review/test_review_safety_cmd.py`; paragraph title "Follow-up print (record and print only)."; artifacts `./artifacts/qa-md-sha256-before.txt` and `./artifacts/print-smoke.txt`; no stored tag `protected-risk-dispute`.
- **Added after the reviewer pass (2026-11-16).** The Constraints now name `src/superclaude/cli/review/__init__.py` as the third existing file the package edits (Task 1 registers `safety_cmd`).
```

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md:17-30

```markdown
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` and the cuts list `cuts-debate/final-cuts.md` both sit inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF. The cuts list is authoritative where it differs from the earlier stage requests (revision 4 of the source says so); the rows C1 to C4, C7 and C10 of its section (a) decide what this package builds. Section numbers, requirement ids (REQ-nn) and guardrails (GR1, GR12) refer to the spec.
- One package, two tasks. This is stage 1 of four packages (stages 0, 1, 3 and 4); stage 2 is withdrawn into this package and has no package of its own. The package adds new files only (the scan module, its command module and their tests) and edits exactly three existing files: `src/superclaude/cli/review/__init__.py` (one name added to the tuple of subcommand modules, Task 1) and `SKILL.md` and `refs/managed-workspace.md` of the `sc-implement-protocol` skill (Task 2), plus the two plugin twins of those skill files. It edits no other review-loop carrier. It runs only after the owner has said go for stage 1 in chat and the go is recorded in the stage ledger `stage-requests/README.md` in PF (Task 1 checks that). Stage 3 starts only after this package is done, as its own entry check reads.
- Depth. The source's revision 4 says this package has two tasks in two phases and `depth: quick`; the program gate checker that requires `depth: standard` and 4 to 8 phases fails it for that reason only. The owner chose `quick` in chat on 2026-11-16.
- Not built (cuts rows C1, C2, C3, C4 and C10): the follow-up ledger and its codec, the classifier and its inputs supplier, the carrier registry and scale map, the new skill folder and its references, the install check for digest versions, the registry drift tests, the owner summary file, the sweep and the shadow stage. Nothing here reads, writes or names any of them, and no stored tag for a safety hit exists: the scan only prints.
- Also not built: any Jev or other external judge call, key or account (owner decision OD3 stays open; no finding text leaves the machine); any edit of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` or its plugin twin (it keeps its own scale, and its final summary "never asks the user anything"); any edit of `src/superclaude/cli/review/ledger.py`, `WORKER-CONTRACT.md` or the own-scale primitives; code-assigned severity in `src/superclaude/cli/**/*.py`; any change to the cap of 2 fix cycles.
- Retired carriers stay unedited. `/sc:task` and task-builder are being retired (owner, 2026-11-16): no task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`.
- Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface. The one existing hand-kept twin it touches is `plugins/superclaude/skills/sc-implement-protocol/`, and only its two files `SKILL.md` and `refs/managed-workspace.md`, because `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins them byte for byte to their sources. The owner has not confirmed removing plugin parity (the program's open-questions file, section 3.4); this plan does not decide it.
- Carrier choice. The owner approved the final review step of `/sc:implement` as the follow-up carrier, "record and print only". The once-per-run offer question stays with the top-level session through the output style, so the added paragraph asks the user nothing, makes no offer and adds no stop code.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. New text added to installed primitives avoids the words the static scans pin (the halt, stop and ruling words of `tests/skills/test_implement_severity_static.py`, the old cap wording and the sweep-phrase patterns of `tests/skills/test_review_severity_rule.py`) and cites no `SKILL.md:<number>` style pointer.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; keep everything under the project `.claude/` folder out of `git add` (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...` and `uv run python ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes tells a reader to keep `.dev/tasks/` out of `git add`. Staging is not committing.
```

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md:34-36

```markdown
## Task 1: Build the safety scan module and the `safety-scan` command

Before creating any file, run the entry check: the stage ledger `stage-requests/README.md` in PF must hold an owner go for stage 1 with a date; when it does not, create nothing and report to the owner. Then create three things.
```

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md:56-60

```markdown
## Task 2: Add the print-only follow-up paragraph to the final review step

Depends on: Task 1

Before editing, record the SHA-256 of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` and of its plugin twin `plugins/superclaude/skills/sc-implement-protocol/refs/qa.md` in `./artifacts/qa-md-sha256-before.txt` (two lines; equal today). Then read `src/superclaude/skills/sc-implement-protocol/SKILL.md` (the "Done" section and the "Whole-list review" section), `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (the archive gate, steps 1 to 6) and `refs/qa.md` (the notes-file definition: line 1 holds the `start` sha, lines 2 to m are the live lines, lines after m begin with `superseded `; and the closed list of interrupts), and edit only the first two files.
```

### Makefile:48-51

```make
lint: lint-architecture
	@echo "Running linter..."
	uv run ruff check .

```

### tests/skills/test_implement_severity_static.py:290-298

```python
# --- SPEC AC-11 (V1 F-11, V2 F-15): every halt/STOP/Ruling site classified ---
#
# blocking   reachable only while a blocking finding with a confirmed anchor is open
# stop-row   non-finding STOP row of the SKILL.md STOP table, or FR-019 items 5 and 6
# definition grammar, examples, the reason table, or a rule that writes nothing

_SITE = re.compile(r"\bhalt(s|ed|ing)?\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b")

_ALLOW = [
```

## Coverage slice

| Requirement | Source | Match | Task | Where |
|---|---|---|---|---|
| INF-006 | inferred | none |  | line 63 |
| INF-007 | inferred | none |  | line 63 |
| INF-008 | inferred | none |  | line 64 |
| INF-009 | inferred | none |  | line 65 |
| INF-010 | inferred | none |  | line 66 |
| INF-011 | inferred | none |  | line 67 |
| INF-012 | inferred | none |  | line 22 |
| INF-013 | inferred | none |  | line 22 |
| INF-014 | inferred | none |  | line 7 |
| INF-015 | inferred | none |  | line 18 |
