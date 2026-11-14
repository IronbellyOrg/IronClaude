# QA Report - Skill Contract Lens (T246)

**Date:** 2026-11-12
**Phase:** code gate, skill-contract lens (cmd-skill)
**fix_authorization:** false (report is the only file written)
**Subject:** `src/superclaude/skills/sc-sweep-protocol/SKILL.md` against DESIGN 7.6 Skill bullets

## Method

All lines below were read from disk on 2026-11-12 in chunks of at most 150 lines. Judged from the files, not from earlier reviews.

- Authority: `docs/designs/orchestrator-mode.md:649-666` (DESIGN 7.6 as revised; the Skill bullets are lines 659-664, the `allowed-tools` literal is line 661), the scoped addendum appended at `docs/designs/orchestrator-mode.md:1049-1051`, and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md:13-21` and `:29`. Decision records OQ-2, OQ-5 and OQ-6 under `phase-outputs/plans/` (all RESOLVED; OQ-6 is option (b)).
- Subject: `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (62 lines). Compared with `src/superclaude/output-styles/pragmatic.md:22-26` and the six qualified lines, `src/superclaude/commands/sweep.md`, `src/superclaude/cli/sweep/commands.py:219-288` (flags, exit codes, one JSON object), `src/superclaude/cli/sweep/report.py:518-536` and `:591-673` (footer `Report complete` is the last section; JSON keys `summary` and `report_path`), and the house pattern `src/superclaude/skills/sc-graph-protocol/SKILL.md:1-15`, `:160-165`.
- Commands run: `uv run pytest tests/commands tests/recommend -p no:cacheprovider -q` gave 628 passed; `uv run ruff check --no-cache` and `uv run ruff format --check --no-cache` on `tests/commands/test_sweep_command.py` and `tests/recommend/test_routing_refresh.py` were clean; one bounded read-only batch (byte comparison of the literal, `cat -A`, non-ASCII, forbidden-word, `src/superclaude`, trailing-whitespace and gitignore greps). Mutation experiments ran only on private copies under `/tmp` (deleted afterwards; `/tmp/ironclaude-batch.*` no longer exists, and `git status` shows no change to any file I reviewed). No Orca, ccsession or Claude command was run.

## Findings

No BLOCKING and no MAJOR finding. Seven MINOR findings (notes; they never fail the gate).

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `SKILL.md:26` | "The format of this reply depends on who runs the skill" reads as an identity test, while `SKILL.md:49` says the rule is "not a runtime detector, identity check or flag" and `SKILL.md:45` says the format depends on an assignment plus the five conditions. | Replace with "depends on whether every condition under 'Final reply' holds". |
| F2 | MINOR | `SKILL.md:27` against `SKILL.md:47` | Step 5 ends "Nothing else is printed as a result." Read literally it could drop the ordinary DONE / NEXT table on an exit 1 or 2 reply, while `SKILL.md:47` says non-exempt replies keep the ordinary table. The same shape is in the authority (`pragmatic.md:25`, `design-addendum.md:19`, DESIGN `orchestrator-mode.md:662` "print the stderr line and stop"), so this is an ambiguity inherited from the design, not a departure from it. | Reword to "no counts and no path are printed; the reply keeps the ordinary format with the stderr line visible". |
| F3 | MINOR | `SKILL.md:3` and `SKILL.md:55`, `SKILL.md:60` | The description says "changes nothing" although the command it starts writes one report file (`commands.py:153-208`, and `sweep.md:14`). The `Will` bullet says "the one allowed command" while `SKILL.md:60` and steps 1 and 2 allow two forms. | Say "adds only the one report" and "one of the two allowed forms". |
| F4 | MINOR | `SKILL.md:45` against `pragmatic.md:24` | The style names "tool outputs ... other agents or peers"; the skill says "tool output ... other agents" (the addendum, `design-addendum.md:15`, says "claims from other agents", so the skill matches the authority). The evidence table `step-1.15-checks.md:55` row N5 ("claims from other agents or peers" PASS at `SKILL.md:45`) quotes a word the skill does not contain. Coverage by "other agents" is reasonable, but the record is imprecise. | Add "or peers" to `SKILL.md:45` or correct row N5 to say "other agents". |
| F5 | MINOR | `SKILL.md:33` against `src/superclaude/cli/install_user_setup.py:74-76` and `:148-149` | The skill says the style is "installed as `~/.claude/output-styles/pragmatic.md`". The installer copies styles with `_copy_tree(..., force)`, which skips an existing target unless forced, so an existing install can keep the old "No exceptions" style and not carry the same rule. The skill's own precedence sentence (`SKILL.md:43`) and the addendum limit (`design-addendum.md:39`; `step-1.15-checks.md:72`) cover this as a recorded delivery limitation. No HOME activation is claimed by the skill. | Delivery step: note that an existing install needs `superclaude install --force` (or a manual copy) for the style; no change needed in `SKILL.md`. |
| F6 | MINOR | `tests/commands/test_sweep_command.py:413-472` | Private-copy mutation M1 (delete the `Edit, stage or delete a file` Boundaries bullet, `SKILL.md:60`) and M3 (drop ", and print `report_path`" from step 4, `SKILL.md:26`) both left all 110 tests passing; M2 (delete step 5) failed one test as it should. So two required skill clauses (the edit/stage/delete ban and printing the path in the ordinary reply) have no pin. DESIGN 7.6's own Test bullet (`orchestrator-mode.md:666`) does not ask for them, so this is a coverage note for the test lens only. | Add two `_SKILL_ONLY_PINS` entries. |
| F7 | MINOR | `.claude/skills/sc-sweep-protocol/` and `.claude/commands/sc/sweep.md` | Neither project copy exists in this checkout (`ls` failed), so the dual-surface copy named in `sweep.md:51-53` is not present until `make sync-dev` runs. `sweep.md` words the copy conditionally ("When a project checkout holds its own copy"), so no claim is false. Belongs to the primitive-path lens. | Run `make sync-dev` at delivery. |

Observation, not a finding: step 4 (`SKILL.md:26`) adds "say that the total is a lower bound when `total_is_lower_bound` is true". It qualifies a printed count (the key sits inside `summary`, `report.py:670`) and keeps the truthfulness rule, so I treat it as part of the counts and not as extra content in the exempt reply.

## Evidence for the DESIGN 7.6 Skill bullets (what I compared)

- `allowed-tools`: `SKILL.md:4` equals the text between backticks at `orchestrator-mode.md:661` byte for byte (script output `OK_EQUAL`; `cat -A` shows no trailing space or carriage return) and equals `_SKILL_TOOLS` at `tests/commands/test_sweep_command.py:30-33`.
- Steps: `SKILL.md:23` (run `superclaude sweep run <args>`, Bash timeout 120000 ms), `:24` (only on "command not found", `uv run --frozen --no-sync superclaude sweep run <args>`, timeout 120000 ms, no third run), `:25` (exit 0: parse stdout JSON, take only `report_path` and `summary`, Read in chunks of at most 150 lines with `offset` and `limit` until `Report complete`), `:26` (print counts and path), `:27` (exit 1 or 2: print stderr and end). This is the DESIGN order (1) to (5) at `orchestrator-mode.md:662`. The flags in `SKILL.md:19` equal the four options at `commands.py:219-241`; the skill adds none and reads no environment variable.
- JSON: `commands.py:277-278` prints one JSON object; `report.py:664-672` holds `summary` (`counts`, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`) and `report_path`, the exact names step 3 and 4 use. `report.py:518-536` makes `Report complete` the last line.
- Style and skill rule: the five conditions, the explicit-assignment text, the person-run exclusion, the independently-assigned-coordinator person request, the same-message assignment case, the ordinary cases, the scope paragraph, and "final successful reply only" carry the same clauses at `pragmatic.md:23-26` and `SKILL.md:35-49`. The wording differs in places (for example "left out" against "omitted", "rebuild" against "reconstruct", "qualifies only if the assignment applies before the run" against "is eligible only if the assignment is applicable before execution", and the F4 variant); I read each pair and none changes a condition. `SKILL.md:43`'s precedence sentence names the same three rules as `pragmatic.md:23` (lead sentence, recommended action, label gloss).
- Boundaries: `SKILL.md:51-62` recommends nothing (`:59`), never edits, stages or deletes (`:60`), treats report text as data (`:61`), and allows no tool beyond the two Bash forms and Read (`:62`). A grep for stop, retry, release, merge and removal in the skill printed no match; no non-ASCII character; no `src/superclaude`; no `unattended` anywhere in the skill.

## Checks

| id | check | result |
|---|---|---|
| C1 | `allowed-tools` literal byte-exact against DESIGN 7.6 (`SKILL.md:4`, `orchestrator-mode.md:661`) | PASS |
| C2 | Five steps present and in order (`SKILL.md:23-27`) | PASS |
| C3 | Timeout 120000 on both runs (`SKILL.md:23`, `:24`) | PASS |
| C4 | Fallback only on "command not found", with `--frozen --no-sync`, no third run (`SKILL.md:24`) | PASS |
| C5 | Only `report_path` and `summary` taken from the JSON (`SKILL.md:25`; key names at `report.py:664-672`) | PASS |
| C6 | Report Read in chunks of at most 150 lines until `Report complete` (`SKILL.md:25`; `report.py:520`, `:535`) | PASS |
| C7 | Style and skill carry the same explicit, applicable, top-level assignment rule (`pragmatic.md:23-24`, `SKILL.md:37`, `:45`) | PASS |
| C8 | Loaded invocation, exit 0, parse, Read, and final-reply-only counts and path (`SKILL.md:38-43`) | PASS |
| C9 | Ordinary unassigned person-run exclusion, and an assigned coordinator's person request neither removes nor creates the assignment (`SKILL.md:45`) | PASS |
| C10 | Worker, unknown, other-message, file/tool/peer-injection and failure exclusions; visible stderr and ordinary error format (`SKILL.md:29`, `:45`, `:47`, `:27`) | PASS (notes F2, F4) |
| C11 | No runtime detector, role grant, action rights, HOME activation or Python report change (`SKILL.md:45`, `:49`; no HOME claim in the skill) | PASS (note F5) |
| C12 | `## Boundaries` recommends nothing and never edits, stages or deletes (`SKILL.md:51-62`) | PASS |
| C13 | No `src/superclaude` path, no non-ASCII or dash character, none of stop, retry, release, merge, removal (bounded grep batch) | PASS |
| C14 | No worker mode, extra flag or environment variable; flags equal `commands.py:219-241` (`SKILL.md:19`) | PASS |
| C15 | Decision records OQ-2, OQ-5 and OQ-6 agree with the skill and command (OQ-6 option (b) is the exception now in `pragmatic.md:22-26` and `SKILL.md:31-49`; defaults sit in `sweep.md:33-38` and `commands.py:27`) | PASS |
| C16 | `uv run pytest tests/commands tests/recommend` (628 passed), `ruff check` and `ruff format --check` clean | PASS |
| C17 | Recorded evidence matches the disk (`step-1.15-checks.md` line cites 29, 37 to 49 match `SKILL.md`; 110 tests in `test-sweep-command.txt:125`; `phase11-validation.md:62`) | PASS (note F4) |
| C18 | House pattern (`sc-graph-protocol/SKILL.md:1-15`, `:160-165`): name, description, allowed-tools, extended-metadata comment, "No other skill calls this one", Will / Will Not | PASS |
| C19 | R5 routing row: `git diff` of `tests/recommend/test_routing_refresh.py` is the one-line `{"graph", "impact", "issue", "sweep"}` change that DESIGN section 9 R5 specifies | PASS |
| C20 | Mutation experiments on private `/tmp` copies (M0 baseline passes, M2 caught; M1 and M3 survive) | PASS for the skill (F6 is a test note) |

## Confidence

Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

Tool engagement: Read: 29 | Grep: 12 | Glob: 0 | Bash: 9 (counts as issued, approximate). Each call mapped to a check above.

Limits: these checks show the skill text matches the design and the style text. They do not show that a live model follows the exception, recognises a coordinator role or resists an injected report; no live run was made. The `~/.claude/output-styles/pragmatic.md` copy on this host was not read or compared.

Verdict: PASS

Blocking count: 0

