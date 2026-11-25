# Brainstorm notes: unattended mode for /sc:implement

Deliverable: SPEC.md (same folder). Date: 2026-11-23. Depth: `standard` with 3 proposals, strategy `systematic`, codebase enrichment by direct reading, no web research. Why standard: the design touches one command and its protocol but has many gates (about 18 decision points); `deep` (up to 7 proposals, 3 dialogue batches) would add proposals that differ in framing, not in the decisions that matter, and the sibling commands already fix the pattern. Why not `quick`: it caps at 2 proposals, too few to expose the safety versus minimal tension.

## Revision 2026-11-23 (owner decision O3 answered)

The coordinator relayed the owner's answer to O3: no human approval of the workflow plan; the plan must pass review-panel scrutiny with no blockers before implement starts; house rule at most 3 reviews, then escalate to the owner with the open blocking findings. SPEC.md was revised: the hash pin `--plan-sha256`, `E-PLAN-NOT-APPROVED`, `plan_approval` and the inline-prompt source are gone; `--plan-review <report>`, `E-PLAN-NOT-REVIEWED`, `implement.plan_review` and a `gate` helper subcommand replace them. The proposals and `adversarial/` files below are the pre-revision history and still mention the hash pin; they were not rewritten.

Which panel fits (read in `~/.claude/commands/sc/spec-panel*.md`, `~/.claude/skills/sc-spec-panel-stoprule-protocol/SKILL.md` and `scripts/stoprule.py`):
- `/sc:spec-panel-stoprule` fits. Its last report line `verdict: PASS|FAIL` is written only by `stoprule.py finalize` from a sealed claim ledger, `check` detects an edited ledger (exit 6), the report carries a sentinel `<!-- stoprule v1 review=N/3 spec=<12 hex> ... confirmed=<n> ... -->`, and `begin` exits 4 at a prior review 3 (the house rule). PASS means no confirmed blocking finding, no open or regressed prior blocking finding, every changed hunk covered, every claim graded.
- Plain `/sc:spec-panel` has an `## Unattended mode` (a worker can run it) and the same `review: N of 3` cap, but its `verdict:` line is typed by the reviewer and the report has no plan hash and no tamper check, so a gate cannot trust it. Rejected as the gate.
- `/sc:spec-panel-ledger` has no unattended mode (it stops on `--unattended`); `-ponytail`, `-armb`, `-diffgate` not read, UNVERIFIED.
- Problem found: `/sc:spec-panel-stoprule` "deliberately has no `## Unattended mode` section and does not accept `--unattended`" (command file line 18), so it cannot be a worker `Command:` line. Hence open decision OD-1 (who runs the loop).
- `check --spec` does NOT bind a report to a plan (it skips form checks when the spec hash differs, `cmd_check`), so the gate also compares the sentinel's `spec=` with the SHA-256 of the plan read as UTF-8 text (how `stoprule.py` hashes, `read_text`).
- Waiver flag: not provided (SPEC UI-26). Reason: the verdict replaces the person, a brief-carried flag would make the gate optional by the brief writer's choice; a run without the gate is a person-run attended run. Alternative if the owner wants simple stories to skip: a flag that quotes the owner's words, like the commit grant of WC-9.
- Workflow already has its own gate (`review_verdict: FAIL` and `open_blockers` in the package contract, `E-MANAGED-REVIEW-FAIL`, from its reflect-based remediation with 2 fix cycles); it stays and stacks with the panel gate.

## Options considered

| Option | What it is | Verdict |
|---|---|---|
| A. Minimal delta | one `## Unattended mode` section, text clauses in the skill, no new code, no new STOP code | base of the merge |
| B. Safety first | adds report-directory placement rules, ledger-derived status, hash pin, forced sequential, extras cap, ranked risks | merged in |
| C. Pipeline first | adds `--plan-only`, `E-PLAN-NOT-APPROVED`, `implement:` mapping, coordinator next-step table, contract edits, launch-level text | merged in, except `--plan-only` |
| D (session addition) | a stdlib helper script for argument parsing, directory check and contract writing | adopted; none of A to C proposed it |
| E (rejected) | no helper, status written by the model from its own notes | rejected: the status would be decided from session memory, and the grammar and contract could not be unit tested |
| F (rejected) | provisional contract at start, replaced at the end | rejected: a contract that exists during the run triggers liveness state S9 (finished but unreported) |

## Why the chosen design won

It follows the four sibling sections word for word in structure (lowest review cost, the existing section test applies), maps every STOP code to a status in one closed table (the freeze rule of WORKER-CONTRACT D2 then works unchanged), never writes a Ruling or starts an operator review, and makes the parts that can be executable executable (the helper), so the acceptance criteria are observable. The only new stop code is `E-PLAN-NOT-APPROVED`; the only new flags are `--report-dir` (as in 20 sibling commands) and `--plan-sha256`.

## Decisions where the proposals split, and the ruling

See `adversarial/diff-analysis.md` (18 points) and `adversarial/debate-transcript.md`. The three that matter most: E-ARCHIVE-BLOCKED is `blocked` or `failed`, not `partial` (D2 freeze text); parallel batches run sequentially under the mode (a batch task gets no ladder and halts `batch`); a task completed under an earlier Ruling gives `partial` so the known gap reaches the coordinator.

## Not converged

- The convergence figure (about 0.83) is the session's own count of agreement across 18 points, not the adversarial skill's formula. The debate was one model playing three lenses plus three independently written proposals; only the proposals were independent.
- Whether the helper script is worth its new executable surface (about 150 to 250 lines, stdlib only). The text-only alternative (E) is cheaper but not testable; recorded in the spec as a decision already taken, not an owner question.
- Extras cap (20 minutes) and the 240 second wait are starting values, not measured.
- One owner question remains: OD-1 (who runs the stoprule loop, since it has no unattended mode; also UNVERIFIED whether the contract lets the coordinator session run a multi-agent review). It does not block the build. O3, O5 authorization and `--plan-only` are decided (see CHANGES).
- The status of a legacy FINAL `issues` as `partial` and of a Ruling-accepted task as `partial` are judgment calls; both are listed as defaults the owner can overturn.

## UNVERIFIED (not read in a file or command output)

- Added by the O3 revision: whether `/sc:spec-panel-stoprule` has ever been run on a `/sc:workflow` plan (it reviews specifications; plan quality of its findings is untested); `stoprule.py` read in parts only (header, `cmd_check`, sentinel line, `read_text`, `cmd_verdict`), not the whole 2050 lines; the other spec-panel variants (`-ponytail`, `-armb`, `-diffgate`) not read; the O3 answer itself is from the coordinator's message, not yet recorded in `shared/CONSENSUS.md`.

- `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` (whether its ledger parser can be imported).
- `tests/skills/test_implement_*.py` contents (STOP-table or grammar pins that a new row could break).
- `superclaude issue-pipeline plan-hash` digest definition; `brief.py` and `worker-brief.txt` beyond the design document's description; `launch.py` beyond the constant.
- Whether a session started by Orca's `worker-start` has a launch-level guard record and is therefore governed by LL-IMPL.
- How `plugins/superclaude/` is refreshed (the Makefile `build-plugin` target writes to `dist/`).
- `docs/user-guide/` pages other than `orchestrator-mode.md`; `HOW-WE-WORK.md` exact insertion point (only grep lines read).
- Whether the installed `WORKER-CONTRACT.md` (which differs from origin/master in the never-as-worker list, the WC-3 Ruling sentence and the push sentence) is newer or older than master; the spec cites sentences that are identical in both.
- The worker contract test count: the file I read asserts 23 entries; a design document says 31. The spec says "read the current value".
- Whether the phase 2 live check of WORKER-CONTRACT passed.
- Local checkout state: branch ironbelly/orch-ledger-20261122 is 150 commits behind origin/master and 4 ahead; the spec's facts come from `git show origin/master:...` and the installed copies, not from the checkout. No fetch was run.

## CHANGES (SPEC.md, since the first version of 2026-11-23)

Requirement ids UI-01 to UI-35 kept their numbers; nothing was renumbered. UI-36 and UI-37 are new. Count: 37.

| Change | Where | Reason |
|---|---|---|
| O3 answered: no human plan approval, panel verdict gates the build | header, Summary, section E | owner, 2026-11-23 |
| UI-24 was "hash pin `--plan-sha256`"; now the panel-verdict gate (`--plan-review`, `gate` helper subcommand, hash binding through the report's `spec=` value) | UI-24 | O3 |
| UI-25 was "never infers approval"; now gate failures: `failed` or `blocked` with `E-PLAN-NOT-REVIEWED reason=<r>`, review cap 3, escalation at review 3, no freeze | UI-25 | O3, house rule |
| UI-26 was "both answers work"; now "no waiver flag for a build", why, and that a person-run hand use needs no verdict | UI-26 | O3 |
| `E-PLAN-NOT-APPROVED` renamed `E-PLAN-NOT-REVIEWED` (still exempt from the freeze) | UI-08, UI-25, UI-32, tests | O3 |
| `--plan-sha256`, `plan_approval`, `hash` subcommand removed; `plan_review` mapping added to the `implement:` contract block | UI-02, UI-07, UI-29 | O3 |
| Inline-prompt sources refused under `--unattended` (no file to review); `mode: legacy-prompt` removed | UI-05, UI-07 | O3 |
| O5 decided: the owner's approval authorizes `--unattended` on implement briefs, no live check gates it; live check kept as evidence | UI-32, Test plan | owner, 2026-11-23 |
| `--plan-only` decided for v1: UI-36 (flag, checks run, `--plan-review` optional) and UI-37 (writes only the contract, status, `preflight` values); acceptance criterion, helper tests, live-check step, UNATTENDED_EXPECT flag, brief row | new UI-36, UI-37; UI-02, UI-29, UI-32, AC, Test plan, Fix approach | owner, 2026-11-23 |
| Open decisions: O3, O5-authorization and `--plan-only` removed as questions (listed as decided); OD-1 (who runs the stoprule loop) added and still open; the old OD-2 and OD-3 deleted | Open decisions | owner answers |
| Trims to stay under 45000 characters (44960 by `wc -m`): shorter wording in Problem Statement, Related, Components, Fix approach, Test plan and several requirements; no requirement dropped | various | size limit |

Not changed: UI-01, UI-03, UI-04 (apart from wording), UI-06, UI-08 (apart from the `E-PLAN-NOT-REVIEWED` rows), UI-09 to UI-23, UI-27 to UI-35.

Left as pre-revision history and now out of date: `proposals/`, `adversarial/`, `seed-brief.md` (they mention the hash pin and `--plan-only` as rejected).

One thing the owner has not decided and the first message did not say: OD-1. I kept it open instead of deciding it, because it needs the owner's view on whether the coordinator session runs the review loop.
