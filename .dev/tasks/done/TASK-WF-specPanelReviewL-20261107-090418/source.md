# Design: Review Loop contract for `/sc:spec-panel` (issue 346)

**Status:** Design only (nothing implemented). Next: `/sc:workflow` on this file, then `/sc:implement` on the plan it prints.
**Issue:** IronbellyOrg/IronClaude #346 ("Document review loops do not converge: revisers add mechanisms, re-reviews re-attack the whole spec, no growth or scope limits").
**Branch:** `ironbelly/issue-346-review-loop-convergence`
**Source of truth:** `src/superclaude/` -> `make sync-dev` -> `.claude/` (never stage `.claude/`). The `plugins/superclaude/` mirror files named below are edited by hand (tests pin them).
**Produced by:** `/sc:design` on the finalized spec, 2026-11-07. The spec came from a deep `/sc:troubleshoot` run, one `/sc:spec-panel` review round (verdict FAIL, five blocking findings) and one refactor that applied them. Working files (not committed): `.dev/issues/346/fix-spec-final.md`, `.dev/issues/346/spec-panel-review.md`, and the troubleshoot report `.dev/troubleshoot/bug-document-review-loops-do-not-converge-20261107080542/REPORT.md`.

---

## 1. Purpose and scope

The issue reports a document review loop (write, run `/sc:spec-panel`, revise, re-review) that did not converge: findings went 24, 13, 14 over three rounds and the specification grew from 57,763 to 92,194 bytes. A fourth round with a constrained brief found 7 and the spec shrank to 89,089 bytes, but still failed because the brief graded any finding as a failure. The framework has no review-loop contract for `/sc:spec-panel`: the command cannot take prior findings, nothing limits what a reviser may add, its severities (CRITICAL, MAJOR, MINOR) have no mapping to blocking or minor, and the routing guide tells users to loop "until no critical findings remain".

This design adds that contract as one short `## Review Loop` section in the `/sc:spec-panel` command, two flags on its Usage line, a corrected sentence in the routing guide (and the two release guides that repeat it), and one new text-presence test.

**What this design does not claim.** The troubleshoot run could not establish how much of the observed trend these missing rules caused (calibrated confidence 0.30; the run host and its artifacts were unreachable, and the briefs the coordinator wrote are not available). This is a conditional fill of a documented rule gap, not a confirmed root-cause fix. The change makes the loop stop, narrow and be checkable; it does not prove the loop would have converged.

Out of scope: the installer (see section 11), `pragmatic.md` S1-S5, `/sc:implement`'s own model, a monotonic halt, a size limit on revisions, and the generic `--iterations` flag documentation.

## 2. Binding decisions and constraints

| # | Constraint | Source |
|---|---|---|
| C1 | Minor findings never fail a review; only blocking findings give FAIL. A review loop runs at most 2 fix cycles (3 reviews), then escalates with the open blocking findings; a protocol may define its own severity model (S4). | `src/superclaude/output-styles/pragmatic.md:224-229` |
| C2 | S1-S5 are copied verbatim into ten files and pinned. Do not edit or insert between them. spec-panel declares its own model under S4 instead. | `tests/skills/test_review_severity_rule.py:66-107` |
| C3 | The cap text must read exactly `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`; no cap number above 2 outside `sc-implement-protocol`; any-severity phrases are banned in `src/`, `plugins/`, `commands/`, `agents/`. | `test_review_severity_rule.py:215-219,288-339`, `:112-176` |
| C4 | An edit to `HOW-WE-WORK.md` is copied byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; the level table stays equal in `src/superclaude/core/CLAUDE.md`; no routing row id is renamed or removed; the file stays ASCII. | `CLAUDE.md` (project), `tests/commands/test_routing_plugin_parity.py:38`, `tests/core/test_how_we_work_routing_table.py`, `tests/core/test_claude_md_routing_block.py:29` |
| C5 | Installed primitives never name `src/superclaude/` paths; they use installed paths. Where one file is read, agents look in the project `.claude/agents/` first, then `~/.claude/agents/`. | project `CLAUDE.md` ("Never Hardcode `src/superclaude/` Paths"), `tests/skills/test_primitive_dual_surface_lookup.py:6-7,50-60` |
| C6 | `/sc:spec-panel` never modifies a specification without consent. | `src/superclaude/commands/spec-panel.md:451` |
| C7 | Never stage `.claude/`; always stage `.dev/tasks`. | project and global `CLAUDE.md` |
| C8 | `plugins/superclaude/commands/spec-panel.md` already differs from `src/` by one word at line 219 ("Sequential" vs "Native reasoning"). Edit it in place; do not byte-copy `src/` over it. | spec, verified in the self-review |

## 3. Corrections to the spec text

Only items where this design deliberately differs from the finalized spec, or fixes a reference:

- The spec's Docs group named `docs/user-guide/flags.md:248` and `commands/sc-help.md:91`. Both document the generic global `--iterations` flag (1-10), not spec-panel. They are not edited.
- The old routing sentence ("until no critical findings remain") appears in four files, not two: `src/superclaude/core/HOW-WE-WORK.md:65`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:65`, `docs/guides/prd-skill-release-guide.md:493`, `docs/guides/tdd-skill-release-guide.md:501` (verified by search on 2026-11-07).
- The spec says the new test imports `AT_CAP_CLAUSES[1]`; that is the string `HALT and escalate to the user with the open blocking findings` (`test_review_severity_rule.py:216-219`).

## 4. Interface: Usage line

In `src/superclaude/commands/spec-panel.md` line 22 and `plugins/superclaude/commands/spec-panel.md` line 22, append after `[--format standard|structured|detailed]`:

```text
 [--re-review <prior-findings-file> --baseline <saved-copy>]
```

`<prior-findings-file>` is the report of the prior review. `<saved-copy>` is a saved copy of the text that prior review saw (a copy, not a git ref: a ref fails on untracked or `.dev/` files).

## 5. The `## Review Loop` section (literal text)

Insert before `## Output Formats` (line 254 in both copies) in both spec-panel files, byte for byte. Each numbered item is ONE line, so the repo's line-based matchers see each bullet whole.

```markdown
## Review Loop

1. **Mode**: `--re-review` applies to `--mode critique` only; without both `--re-review` and `--baseline` the run is a first review of the full document, with `baseline: missing` noted if only one was given; if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review.
2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open).
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the prior report's N plus 1 (1 for a first review); a prior-findings file at `review: 3` (a higher value counts as 3) with `verdict: FAIL` means do not review (this check runs before the first-review default of bullet 1), HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--re-review` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review.
5. **Re-review output**: first a table of prior blocking findings `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again); then findings on lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`; an `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only; an empty diff leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line, listing only blocking finding ids and restating this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking.
```

Design notes on the text:

- Bullet 2 is spec-panel's own severity model under S4 (`pragmatic.md:228`). FR-8/FR-9 (`spec-panel.md:316-317`) stay blocking because a blank behaviour cell has no state trace yet FR-9 forces MAJOR.
- Bullet 4 reuses the canonical cap text and the at-cap clause verbatim so the existing pin tests (C3) accept it. There is no second stop (no monotonic halt) beside the 3-review cap.
- Bullet 5's pointer names only steps 1-5 of the rf-qa Fix Cycle Process (`src/superclaude/agents/rf-qa.md:386-396`), not its Retry Monotonicity Protocol. The inline rules stand alone, because rf-qa grades CRITICAL/IMPORTANT/MINOR while spec-panel grades CRITICAL/MAJOR/MINOR. The pointer carries no `src/superclaude` path (C5).
- Bullet 6 is a rule for the reviser, delivered through the report because the reviser reads the report, not the command. The "report byte size before and after" is a report, not a limit: a limit conflicts with FR-8/FR-9 gap-filling, and nothing could check it from text.

## 6. Routing guide and release guides

In `src/superclaude/core/HOW-WE-WORK.md` line 65, replace the text from "ask Claude to apply them to the PRD" to the end of the line with:

```text
save a copy of the PRD, ask Claude to apply them to the PRD, then run it again with `--re-review <this report> --baseline <the saved copy>`; stop after 2 fix cycles (3 reviews) and decide with the open blocking findings.
```

The line then reads "... Decide which findings to accept, save a copy of the PRD, ask Claude to apply them to the PRD, then run it again with `--re-review <this report> --baseline <the saved copy>`; stop after 2 fix cycles (3 reviews) and decide with the open blocking findings." Then byte-copy the file to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Without the saved copy and the report, the second run is a full first review, which is the failure being removed.

Apply the same replacement to `docs/guides/prd-skill-release-guide.md:493` and `docs/guides/tdd-skill-release-guide.md:501`. Both lines read exactly `It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain.`; keep the "It only reports." prefix.

## 7. Component architecture

```text
coordinator (Orca worker, human or script)         reviser (separate agent)
  keeps: review count, prior-findings file,          reads: the report (Reviser brief)
         saved copy of the text each review saw      edits: only text a blocking finding names
        |                                            reports: byte size before and after
        | 1. save copy; run /sc:spec-panel --mode critique   (first review: review: 1 of 3)
        v
/sc:spec-panel (reviewer, simulated panel)
  writes report: findings + Reviser brief + last line "verdict: PASS|FAIL"
        |
        | PASS            -> done
        | FAIL, review<3  -> coordinator passes the report's Reviser brief to the reviser,
        |                    saves a copy, then runs /sc:spec-panel --re-review <report> --baseline <copy>
        | FAIL, review 3  -> HALT, escalate to the user with the open blocking findings
        v
re-review (--re-review): one review per run, ignores --iterations, no revised spec;
  output = prior-blocking table, then findings on changed lines (origin=changed|unchanged)
```

Data the reviewer needs (all produced by the coordinator): the report (header `review: N of 3`), and the saved copy. The command itself keeps no state.

## 8. Files to create or change

| Group | File | Change |
|---|---|---|
| Core | `src/superclaude/commands/spec-panel.md` | Usage tail (line 22) and the `## Review Loop` section before `## Output Formats` (line 254) |
| Core | `plugins/superclaude/commands/spec-panel.md` | The same two blocks, in place (C8) |
| Core | `src/superclaude/core/HOW-WE-WORK.md` | Line 65 sentence (section 6) |
| Core | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Byte copy of the edited file |
| Test | `tests/skills/test_spec_panel_review_loop.py` | New (section 9) |
| Docs | `docs/guides/prd-skill-release-guide.md` (line 493), `docs/guides/tdd-skill-release-guide.md` (line 501) | Sentence from section 6; droppable, no test pins them beyond the new test's guide check |
| Design | `docs/designs/spec-panel-review-loop.md` | This file |

After editing: `make sync-dev` (copies the command into the untracked `.claude/`), `make verify-sync`. Stage `src/`, `plugins/`, `tests/`, `docs/`, and `.dev/tasks`; never `.claude/`.

## 9. Test design

New `tests/skills/test_spec_panel_review_loop.py`. Imports `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES` from `tests.skills.test_review_severity_rule` (the package import pattern already used in `tests/skills/test_implement_severity_static.py:12`), defines its own whitespace flatten (`" ".join(text.split())`), and reads files from the repo root (`Path(__file__).resolve().parents[2]`). Parametrize over `SPEC_PANELS = ("src/superclaude/commands/spec-panel.md", "plugins/superclaude/commands/spec-panel.md")`.

| # | Test | Assertion (literal text on flattened content) |
|---|---|---|
| T1 | Usage line | the first line starting `/sc:spec-panel ` contains `[--re-review <prior-findings-file> --baseline <saved-copy>]` |
| T2 | Section position | `## Review Loop` exists once and comes before `## Output Formats` |
| T3 | Seven single-line bullets | between the heading and the next `## ` heading there are exactly seven lines matching `^[1-7]\. \*\*` in order: Mode, Grading, Verdict, Cap, Re-review output, Reviser contract, Precedence |
| T4 | Cap | the section contains `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` |
| T5 | Vocabulary | the section contains `resolved|open|regressed`, `origin=changed|unchanged`, `verdict: PASS`, `verdict: FAIL`, `review: N of 3`, `Reviser brief`, `byte size before and after` |
| T6 | Lookup order | the section contains the literal ``the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md` `` (without the trailing space), so the project path precedes the `~/` path |
| T7 | Spec review fixes | the section contains ``ignores `--iterations` ``, ```regressed` = a finding the prior report marked resolved that fails again``, `never fall back to a first review` |
| T8 | Precedence | the section contains `a brief may narrow this scope; it may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking` |
| T9 | No source path | the section contains no `src/superclaude` (scoped to the section; the whole file has one at line 218 and must not be asserted) |
| T10 | Guide sentence | in both HOW-WE-WORK copies, the line containing `It only reports.` also contains `--re-review`, `--baseline` and `save a copy of the PRD`, and "until no critical findings remain" appears in none of the two HOW-WE-WORK copies and the two release guides |

Keep green (run, do not edit): `tests/skills/test_review_severity_rule.py` (its matchers scan the new text in both spec-panel copies), `tests/commands/test_routing_plugin_parity.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/core/test_claude_md_routing_block.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/docs/test_onboarding_deck.py`, `tests/skills/test_worker_contract.py`. The matchers were hand-checked only; the first implementation task is to run the severity test against the new text and, if a bullet is flagged, change the minimum wording while keeping the literals T3-T8.

Limit stated plainly: every rule here is prose read by a model. The tests prove the text is present and in the right order, not that a reviewer obeys it.

## 10. Sync, routing registration and documentation

- No new command, skill or agent, so no routing row, `/sc:help` entry or install registration changes.
- `HOW-WE-WORK.md` has no routing-table row for line 65 (it is a numbered step in prose), so row ids and the level table stay untouched.
- The new text reaches an existing host only after `superclaude install --force` or `update` (`src/superclaude/cli/install_commands.py:74-76` keeps existing command files unless forced). Note this in the PR body.

## 11. Out of scope and follow-ups

- **Installer fix** (changed command text reaching existing hosts without `--force`): a different subsystem; `_copy_tree` is shared with `install_rules` (`install_user_setup.py:110,141`), so a change widens the blast radius.
- **No monotonic halt**: the 3-review cap already stops the issue's rounds at review 3; a second stop would overlap it.
- **`WORKER-CONTRACT.md` pointer for brief authors**: optional, Orca-only reach, the file is pinned by `tests/skills/test_worker_contract.py`.
- **Other copies of the spec-panel Usage line**: `docs/user-guide/commands.md:1316` and the legacy `commands/sc-spec-panel.md`.
- **No change to `pragmatic.md` or to the generic `--iterations` rows** (`docs/user-guide/flags.md:248`, `commands/sc-help.md:91`).
- **A captured per-round record** from one real loop (the troubleshoot tasklist's two enabling tasks) is the way to learn how much of the trend these rules explain; not part of this change.

## 12. Risks

- Prose only: a coordinator that drops the flags or the saved copy starts a fresh first review, and nothing enforces the count (bullet 4 names who keeps it).
- FR-8/FR-9 stay blocking, so they can still drive new guards on changed lines.
- MAJOR grading can vary between reviewers (accepted; the concrete-wrong-outcome test narrows it).
- The plugin spec-panel copy has one-word drift (line 219); this change does not fix it.
- Whether the plugin install provides `~/.claude/agents/rf-qa.md` is unverified; bullet 5 stands alone if it is absent.
- Because the causal link is unproven (0.30), the change may not stop the next non-converging loop by itself.

## 13. Defaults chosen by this design

| # | Default | Reason |
|---|---|---|
| D1 | Flag names `--re-review` and `--baseline` | Fixed by the spec; the guide wording matches them |
| D2 | Baseline is a saved copy, not a git ref | Untracked and `.dev/` files have no ref |
| D3 | Round header `review: N of 3`, last line `verdict: PASS|FAIL` | Smallest literals a coordinator can read and a test can assert |
| D4 | `--re-review` is critique-only and never revises | Keeps revision in a separate reviser and honours C6 |
| D5 | Plugin spec-panel edited in place | Avoids hiding the existing drift |
| D6 | Docs group last and droppable | No test depends on it |
| D7 | New test imports two constants, not private helpers | Avoids coupling to `_flat` and `_read` |

## 14. Facts cited, verified 2026-11-07

`spec-panel.md:22` (Usage line, both copies), `:254` (`## Output Formats`, both copies), `:234-252` (`--iterations`), `:316-318` (FR-8 to FR-10), `:451` (no unconsented edits); `HOW-WE-WORK.md:65` (both copies) and `docs/guides/prd-skill-release-guide.md:493`, `docs/guides/tdd-skill-release-guide.md:501` (the old sentence); `pragmatic.md:224-229` (S1-S5); `rf-qa.md:386-401` (Fix Cycle Process and cap); `test_review_severity_rule.py:31-32` (`_flat`), `:215-219` (cap constants), `:288-339` (old-cap matcher); `test_implement_severity_static.py:12` (import pattern); `install_commands.py:74-76`. No flag is cited that is not shown in a command file read in this session.

## 15. Acceptance criteria for the implementation

1. Both spec-panel files carry the Usage tail and the seven-bullet `## Review Loop` section, byte-identical to section 5, before `## Output Formats`; the plugin copy still differs from `src/` only by the pre-existing line-219 word.
2. `src/superclaude/core/HOW-WE-WORK.md:65` carries the section 6 sentence and `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` is byte-equal to it; the two release guides carry the same sentence.
3. `uv run pytest tests/skills/test_spec_panel_review_loop.py` passes (T1-T10) and fails if any literal in T3-T10 is removed.
4. `uv run pytest tests/skills/test_review_severity_rule.py tests/commands/test_routing_plugin_parity.py tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/skills/test_primitive_dual_surface_lookup.py tests/skills/test_worker_contract.py` passes.
5. `make lint` and the pinned ruff format check pass; `make sync-dev` then `make verify-sync` pass; `git status` shows no staged `.claude/` path.
6. No `pragmatic.md`, `sc-implement-protocol` or `WORKER-CONTRACT.md` file is changed.
7. The PR body uses `Refs` (not `Closes`): the causal link is unproven, so the issue is not fully delivered by a rule gap fill alone.
