# Reflect report: pre-execution audit of the minfix implementation plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.79
citations_total: 154
citations_revalidated: 94
citations_dropped: 1
citations_inferred: 6
citation_budget_policy: sampled
citations_dropped_extrapolated: 2
coverage_degraded: parsed-sparse
```

- Spec: `.dev/tasks/to-do/TASK-WF-spec-20261108-181543/source.md` (byte copy of `.dev/brainstorms/346-minfix/SPEC.md`)
- Plan: `.dev/tasks/to-do/TASK-WF-spec-20261108-181543/TASK-WF-spec-20261108-181543.md` (8 tasks, 4 phases)
- Verdict: FAIL — 4 blocking findings (M-F1..M-F4) and 11 minor findings. Advisory only: this report never edits the plan.
- Coverage: 0 labeled requirement IDs (coverage_pct null); 142 inferred requirements, 104 matched by the deterministic containment rule (coverage_pct_union 0.7324). Of the 38 unmatched (calibrator-corrected split, reflection-card.yaml): 21 are outside the plan's declared scope (plan line 19), 16 are covered in other words, 1 is a real gap (INF-032 = M-F3). Separately, INF-028 counts as matched (to Task 8, ratio 0.7) but that match is false; it is M-F2.
- Tier 2: three read-only reviewers (sonnet/analyzer, haiku/qa, opus/refactorer), blind calibration (0.81, 0.70, 0.80), adversarial merge (agreement 19/19, convergence BLOCKED_BY_INVARIANTS: INV-001, INV-003 carried into the merge).
- Degraded: executor class not resolved (anti-self-confirmation weakened); single vendor; calibrator_diversity degraded (opus also reviewed).

## Findings (merged card)

Full card with provenance: `nested/adversarial-1/merged-verdict.md`.

| id | grade | class | claim | fix |
|---|---|---|---|---|
| M-F1 | blocking | gap | The plan's regression run omits tests/recommend/test_routing_refresh.py, which should fail once src/superclaude/commands/spec-panel-minfix.md exists. Task 5 either ships a command that breaks an existing test or stops blocked on a test it never runs, and plan:119 gives no permission to edit that test, so adding the command to the allowed set alone cannot pass: an executor following plan:119 must stop instead of editing the test. | In Task 5 add "spec-panel-minfix" to _POST_REFRESH_ADDITIONS in tests/recommend/test_routing_refresh.py (with a comment naming issue #346); add that file to the plan:124 regression run and to the files Task 5 touches; rewrite plan:119 so this one listed test edit is allowed instead of "stops this task as blocked"; flag the edit to the owner as one source.md does not list. |
| M-F2 | blocking | gap | No task delivers the required correction and retry when the re-reviewer's own checker call exits 2. source.md:46 requires it, but the literal block the plan ships (source.md:120) handles only exits 3/4/5/70; the exit-2 retry exists only for the reviser at source.md:127, and plan:117 copies the block unchanged apart from one owner-decision sentence. The auditor's own coverage matrix credits this requirement to Task 8; that is an audit artifact error, not a plan claim. | In Task 5 Region 4, append one owner-decision sentence inside the existing source.md:120 paragraph (the same channel plan:117 already uses) saying an exit 2 from the reviewer's own check call is corrected once and re-run; add a pin for that sentence in tests/skills/test_spec_panel_minfix.py. Task 7 inherits it through its byte-identity AC (plan:147). |
| M-F3 | blocking | gap | The source.md:46 step-3 requirement that the run at `review: 3` also lists each budget escalation with its need and each `GRADE-CONFLICT` has no plan task; Review Loop bullet 4 escalates only with the open blocking findings and the shipped block never mentions GRADE-CONFLICT. | Append one owner-decision sentence inside the same source.md:120 paragraph as M-F2 (Task 5 Region 4) stating the `review: 3` escalation also lists each budget escalation with its need and each `GRADE-CONFLICT`, and add a pin in tests/skills/test_spec_panel_minfix.py. |
| M-F4 | blocking | unverifiable-AC | importlib loading of fixcheck.py (plan:50) writes scripts/__pycache__/*.pyc carrying the absolute src/superclaude path, and Task 4's recursive grep (plan:104) then matches it, so the Task 4 AC cannot pass. Nothing in the repo suppresses bytecode, and a later `sys.dont_write_bytecode` leaves the .pyc written in Task 1. | Use `grep -rnI --exclude-dir=__pycache__` in the Task 4 AC (works regardless of when the .pyc was written); optionally set `sys.dont_write_bytecode` in the test; note that the install copy (`cp -rn`, install_skill.py copytree) carries the harmless .pyc, or exclude `__pycache__` from it. |
| M-F5 | minor | unverifiable-AC | The repo variant lands at exactly 500 lines, the lint-architecture hard limit, and no AC checks it; the M-F2 and M-F3 sentences cannot add lines without breaking it. | Add AC wc -l <= 500 plus make lint-architecture and make lint to Task 5. Append the M-F2 and M-F3 sentences inside existing paragraphs, never as new lines, since the variant already lands at exactly 500 lines. |
| M-F6 | minor | gap | No task bullet says check verifies the baseline hash; only a Task 3 test exercises it. | Add a Task 2 bullet: check exits 4 when sha256(--baseline) differs from reviewed_sha256; move the test to Task 2. |
| M-F7 | minor | unverifiable-AC | gross, net and add-only are never defined and the delete exemption's cap is unstated. | Define the three counts in Task 2 and add a test for the delete exemption. |
| M-F8 | minor | unverifiable-AC | The exact post-edit text of Review Loop bullet 6 is not given; pins check only substrings and the owner sentence only via `carried-open:`. | Write the full resulting bullet 6 in Task 5 and pin the exact owner sentence; test bullet 6 has no `;;`. |
| M-F9 | minor | gap | The 40-character unique-substring quote match is dropped without being listed as a deviation; plan:63 has no minimum length or uniqueness rule, so a short quote attaches to any hunk. | State the quote-match rule in Task 2 or list it as not implemented. |
| M-F10 | minor | unverifiable-AC | The Task 1 subprocess test does not prove no superclaude import is needed when superclaude is installed in the active environment; a lazy function-level import passes both checks. | Run the subprocess with -I or a scrubbed environment and assert sys.modules has no superclaude entry. |
| M-F11 | minor | gap | "Corrected once and re-run" does not say what a second exit 2 does, on either the reviser or the reviewer path; the M-F2 sentence would copy the gap. | In the M-F2 sentence, state that a second exit 2 is handled like exit 3 (stop and escalate). |
| M-F12 | minor | structural | The compatibility checks the source requires in the first implementation task run in Task 5 instead. The move is necessary, because before Task 5 the new command does not exist and there is nothing to trip, but the plan does not declare it as a deviation. | State the move to Task 5 as a deviation in Constraints. |
| M-F13 | minor | unverifiable-AC | The pin "the `~/.claude/` path precedes the `.claude/` path" is ambiguous: read over the whole file it fails, because bullet 5 names the project .claude/ path first and must stay byte-identical. | Scope the check to the `## Fix Budget` section and use a lookbehind `(?<!~/)\.claude/skills/sc-fixcheck/`; apply the same scoping to Task 4 (plan:103). |
| M-F14 | minor | gap | INSTALL.md's pre-run probe needs one valid and one invalid fixture on disk, but no task creates them. | Task 8 adds .dev/brainstorms/346-minfix/probe/{valid,invalid}/ fixtures with exit-0/exit-1 ACs, or INSTALL.md states the coordinator writes them. |
| M-F15 | minor | gap | test_worker_contract.py's write-verb audit scans every file under src/superclaude/{skills,commands,agents}; the plan does not warn that new text must avoid git add/commit/push/merge/stash, gh pr and gh api tokens, and Task 4 does not run that test, so a SKILL.md hit is found one task late. | Add that rule to Constraints. |

## Recommendations

### Recommendation R-001: Allow and run the routing-refresh test edit in Task 5
- **File:** `.dev/tasks/to-do/TASK-WF-spec-20261108-181543/TASK-WF-spec-20261108-181543.md` (Task 5, plan line 119 and line 124)
- **Change:** add `"spec-panel-minfix"` to `_POST_REFRESH_ADDITIONS` in `tests/recommend/test_routing_refresh.py` (line 33), add that file to the line-124 run, and rewrite line 119 so this one edit is allowed.
- **Verifier:** `uv run pytest tests/recommend/test_routing_refresh.py -v` passes after Task 5.
- **Linked finding(s):** M-F1
- **Priority:** P0

### Recommendation R-002: Ship the reviewer-side exit-2 retry and the review-3 escalation listing
- **File:** plan Task 5 Region 4 (plan line 117); `tests/skills/test_spec_panel_minfix.py`
- **Change:** append two owner-decision sentences inside the existing source.md:120 paragraph: an exit 2 from the reviewer's own call is corrected once and re-run (a second exit 2 is handled like exit 3), and the `review: 3` escalation also lists each budget escalation with its need and each `GRADE-CONFLICT`; pin both.
- **Verifier:** the Task 5 pin test passes; `wc -l src/superclaude/commands/spec-panel-minfix.md` stays at or below 500.
- **Linked finding(s):** M-F2, M-F3, M-F5, M-F11
- **Priority:** P0 (owner sign-off: the sentences amend the block source.md calls literal, using the plan line 117 channel)

### Recommendation R-003: Make the Task 4 grep immune to bytecode
- **File:** plan Task 4 acceptance criteria (plan line 104)
- **Change:** use `grep -rnI --exclude-dir=__pycache__ 'src/superclaude' src/superclaude/skills/sc-fixcheck`.
- **Verifier:** the grep prints nothing after Tasks 1-3 tests have run.
- **Linked finding(s):** M-F4
- **Priority:** P0

### Recommendation R-004: Fold the eleven minor findings into the task text
- **File:** plan Tasks 1, 2, 4, 5, 8 and Constraints
- **Change:** apply the fixes listed for M-F5..M-F15 in the table above.
- **Verifier:** re-run `/sc:reflect --mode pre` on the revised plan; the minor rows no longer appear.
- **Linked finding(s):** M-F5..M-F15
- **Priority:** P2

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | They are escalated as open: both concern how `fixcheck.py` scores entries after `--enforce`, and the replay harness (open question 1) is the first place they would be tested. | source.md:5 | none (ratio 0.4737) |
| INF-002 | The design therefore caps size AND gates the four shapes. | source.md:11 | none (ratio 0.2857) |
| INF-003 | This spec adds the script that checks it. | source.md:12 | none (ratio 0.5) |
| INF-004 | 427's 3-review cap, grading rule, `verdict:` line and re-review flags stay as they are. The coordinator gets no new duty. | source.md:15 | Task 8 (ratio 0.6111) |
| INF-005 | If that fails it stops with `E-FIXCHECK-MISSING`, naming both install paths (`~/.claude/skills/sc-fixcheck/`, then project `.claude/skills/sc-fixcheck/`). It never falls back silently to plain 427 behaviour. | source.md:19 | none (ratio 0.5909) |
| INF-006 | It runs `hash` on the spec it reviews, at EVERY review (first review and re-review), and writes the result as `reviewed_sha256` in the report. | source.md:21 | Task 2 (ratio 0.6667) |
| INF-007 | It writes a fenced `fixbudget` block: one line per finding of this review, plus one line per prior blocking id still open or regressed (so a finding escalated in cycle 1 gets a budget again in cycle 2). | source.md:21 | Task 2 (ratio 0.7391) |
| INF-008 | `refs` names the citation prefix the report uses for spec lines (`SPEC`, `SPEC2`, ...): | source.md:21 | none (ratio 0.5556) |
| INF-009 | `budget` is `std`, `override` (at most one per report, blocking only, never on an `origin=changed` finding, needs an `override-reason` line), `gap:<n>` (a blocking FR-8/FR-9 gap fill naming n guard-table rows), or `-` (minor). | source.md:36 | Task 1 (ratio 0.6296) |
| INF-010 | A `CRITICAL`, `MAJOR/FR-8` or `MAJOR/FR-9` line graded minor prints `GRADE-CONFLICT <id>` and keeps budget 0; it is not an input error. | source.md:36 | Task 1 (ratio 0.9444) |
| INF-011 | If the verdict is FAIL below `review: 3`, the report carries the Reviser brief (literal text in section 3.2, item 5). | source.md:36 | Task 8 (ratio 0.8125) |
| INF-012 | The script, not the model, writes `<report dir>/.fixcheck/base-<N>.md` and refuses (exit 4, `STALE-BASE`) if the spec's sha256 differs from this report's `reviewed_sha256`. | source.md:39 | Task 1 (ratio 0.85) |
| INF-013 | `snapshot` is therefore the normal path in both cycles. | source.md:39 | none (ratio 0.3333) |
| INF-014 | Per blocking id: delete the wrong sentence or clause; else narrow it (no more words); else replace it (within the gross cap); else add, only after writing a `considered:` line (why delete or narrow fails). | source.md:40 | Task 2 (ratio 0.6667) |
| INF-015 | A finding that cannot be answered within budget goes under `## deferred` as `<id>: escalated: <what it needs>`. It is never expanded. | source.md:40 | Task 5 (ratio 0.8462) |
| INF-016 | Non-blocking findings: no edit (budget 0). Their disposition row reads `deferred (minor, fixcheck budget 0)`. | source.md:41 | Task 1 (ratio 0.7143) |
| INF-017 | Ledger: a fenced `fixledger` block at the end of the reviser's own disposition file (a file the brief already requires, so no new authored file). Its first line is `report: <file name of the review report it answers>`. | source.md:42 | Task 1 (ratio 0.7273) |
| INF-018 | Entries are numbered `## L1`, `## L2`, ...; one entry per change: `finding` (one id), `op` (delete/narrow/replace/add), `old` (the exact baseline sentence; for an add, `anchor`, the sentence it follows), `new` (first 10 new words), `considered` (for add), optional `depends: L<n>`. | source.md:42 | Task 2 (ratio 0.6667) |
| INF-019 | Run `check --baseline <b> --revised <spec> --report <report> --ledger <disposition>`. It prints to stdout and writes nothing. | source.md:43 | Task 1 (ratio 0.8462) |
| INF-020 | Exit 1: cut the named entries down once and run `check` again; if it still exits 1, run `check --enforce`. | source.md:43 | Task 3 (ratio 0.6429) |
| INF-021 | That reverts each failing finding whole (plus findings whose entries `depends:` on it, plus unattributed hunks) to baseline text, lists each reverted finding as `escalated`, and re-checks. | source.md:43 | Task 3 (ratio 0.8421) |
| INF-022 | Exit 2: correct the call once and re-run. Exit 3, 4, 5 or 70, or a non-zero exit from `--enforce`: edit nothing more, paste the output. | source.md:43 | Task 1 (ratio 0.6316) |
| INF-023 | Report the byte size before and after (427 bullet 6) and paste the final `FIXCHECK`, `result:` and `escalated:` lines. | source.md:44 | Task 5 (ratio 0.7857) |
| INF-024 | After 427's own input and cap checks (bullets 1 and 4) and before the prior-blocking table, the reviewer runs `check` itself on (the saved copy passed as `--baseline`, which is exactly the text the prior review saw, the spec, the prior report) with no `--ledger` argument | source.md:46 | none (ratio 0.5938) |
| INF-025 | the script then finds the one file in the prior report's directory whose `fixledger` block starts `report: <prior report's file name>` (none or more than one is exit 3). | source.md:46 | Task 1 (ratio 0.8947) |
| INF-026 | The reviewer puts `fixcheck: <exit> ...` in the header. This run is authoritative whether or not the reviser ran the script. | source.md:46 | none (ratio 0.5) |
| INF-027 | A missing or malformed input, an exit 3, 4, 5 or 70, or a disposition whose last `FIXCHECK` line shows exit 3, 4, 5 or 70, stops the review with the named error and escalates to the user with the open blocking findings. It never falls back to a first review. | source.md:46 | none (ratio 0.5926) |
| INF-028 | An exit 2 from the reviewer's own call is corrected once and re-run. | source.md:46 | Task 8 (ratio 0.7) |
| INF-029 | In the prior-blocking table an over-budget id shows `open (over budget)`, an escalated or reverted id `open (escalated: budget)` with its stated need, and an unanswered id `open (unanswered)`. | source.md:46 | Task 2 (ratio 0.75) |
| INF-030 | Every `origin=changed` finding carries `attacks: L<n>/<finding id>`, taken from the run's per-hunk line whose revised line range contains the line the finding quotes, so fix-to-child chains become a computed column. | source.md:46 | Task 2 (ratio 0.6154) |
| INF-031 | The reviewer copies only ids and numbers from the run, never the reviser's prose reasons. | source.md:46 | Task 5 (ratio 0.7273) |
| INF-032 | At `review: 3` the run escalates as 427 says, now also listing each budget escalation with its need and each `GRADE-CONFLICT`: that is the justified escalation. | source.md:46 | none (ratio 0.5) |
| INF-033 | What the checker computes (stdlib `argparse difflib hashlib json re os tempfile pathlib`) | source.md:48 | none (ratio 0.1667) |
| INF-034 | Normalise (line endings, whitespace, table padding, emphasis). Split into units per line, sentence and table cell. | source.md:50 | Task 2 (ratio 1.0) |
| INF-035 | `difflib.SequenceMatcher(autojunk=False)` on units gives hunks; a word-level matcher inside each hunk counts added and deleted words. | source.md:50 | Task 2 (ratio 0.8824) |
| INF-036 | `path:line` citations, pipes and heading marks are not words (bytes count raw text). Identical moved units count zero. | source.md:50 | Task 2 (ratio 1.0) |
| INF-037 | Attribution: a hunk belongs to the entry whose `old` quote it contains (or whose `anchor` precedes it) and whose `new` words start it. The script derives the real op and refuses a mislabelled one. | source.md:50 | Task 2 (ratio 0.85) |
| INF-038 | A hunk that matches no entry is unattributed (policy failure), including one whose entry quotes text not in the baseline; the report prints the reason (`quote not in baseline`) on that hunk's line. | source.md:50 | Task 2 (ratio 0.9) |
| INF-039 | Before attribution, a diff hunk that spans units claimed by more than one ledger entry is split per entry (each entry's `old`/`anchor` unit range), so two edits to neighbouring sentences are credited to both entries. | source.md:50 | Task 2 (ratio 1.0) |
| INF-040 | An entry to which no hunk is attributed is `reverted` (status escalated, not a failure), whatever its text, and a reverted entry counts toward no per-finding total (entries, words, elements), so a plain `check` after `--enforce` scores cleanly. | source.md:50 | Task 2 (ratio 0.6923) |
| INF-041 | A blocking id with neither an entry nor a `## deferred` line is `unanswered`: it stays open and is reported, but is not an exit-1 reason (it adds no text). | source.md:50 | Task 2 (ratio 0.9412) |
| INF-042 | The report prints one line per hunk: `h<k> L<n>/unattributed <finding id> revised:<first line>-<last line> +<added words>/-<deleted words>`. A finding id written into the spec, such as `(F3)`, is a new id. | source.md:50 | Task 2 (ratio 0.875) |
| INF-043 | Per finding it totals gross, net, add-only words, entries, new headings, ids, table rows, normative words (MUST SHALL must never always shall), universal words (only every exactly none total closed), condition words (if unless when whenever where except otherwise: each a new guard) and new check recipes | source.md:50 | Task 2 (ratio 0.9429) |
| INF-044 | Output is deterministic (no clock, no randomness). | source.md:50 | none (ratio 0.4) |
| INF-045 | / CRITICAL (blocking) / 120 / 80 / 80 / 6 / 0 / 0 / 1 / 2 / 1 / 2 / 1 / | source.md:56 | Task 2 (ratio 0.75) |
| INF-046 | / blocking MAJOR (incl. FR-8/FR-9) / 80 / 50 / 50 / 4 / 0 / 0 / 1 / 1 / 1 / 1 (gap:n gives n) / 1 / | source.md:57 | Task 1 (ratio 0.7143) |
| INF-047 | / minor (any non-blocking) / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / | source.md:58 | Task 1 (ratio 0.8) |
| INF-048 | Cycle cap, overrides included: 600 gross added words and 6,144 gross added bytes, plus a raw file-size check (revised size minus baseline size at most 6,144 bytes, so whitespace or padding the normaliser ignores is still capped). | source.md:60 | Task 2 (ratio 0.7308) |
| INF-049 | Over the cap, `--enforce` reverts whole findings (blocking MAJOR before CRITICAL, largest first, then by id) and lists each as escalated. | source.md:60 | Task 3 (ratio 0.9375) |
| INF-050 | `delete` entries are free of the gross cap. `override` doubles gross, net, add-only and entries for one finding and never lifts the heading or id limit. | source.md:60 | Task 2 (ratio 0.9412) |
| INF-051 | Exit codes (one list for every actor, pinned to the script constants): 0 accept; 1 policy failure, every reason tied to a hunk (over budget, forbidden element, cycle cap, unattributed hunk including a quote not in the baseline, mislabelled op on an attributed hunk, edit on a minor id); 2 usage; 3 bad input (missing or empty file, no `fixbudget` block, malformed or second override, ledger missing, not found or ambiguous); 4 hash conflict; 5 cannot write a file safely (the spec for `--enforce`, the copy for `snapshot`); 70 internal error. | source.md:62 | Task 1 (ratio 0.6562) |
| INF-052 | `--enforce` without `--ledger` uses the same lookup as `check`. `--enforce` exits 0 when its re-check is 0. | source.md:62 | Task 3 (ratio 0.9091) |
| INF-053 | if the raw size check still fails after the reverts (changes the normaliser ignores), `--enforce` restores the whole baseline file and lists every blocking id as escalated. | source.md:62 | Task 3 (ratio 0.8571) |
| INF-054 | Only `check --enforce` writes the spec, atomically. `spec-panel-minfix` itself never edits the spec (427 design C6). | source.md:62 | none (ratio 0.5) |
| INF-055 | REMOVED mechanically: minor budget 0, any hunk charged to a minor id fails and `--enforce` reverts it, whatever the task brief says | source.md:69 | none (ratio 0.5625) |
| INF-056 | at most 1,200 gross words (14.7% of 8,148) and 12,288 bytes (21.3%) over two cycles | source.md:74 | none (ratio 0.5) |
| INF-057 | The authoritative record is the re-review's own `check` run, so a reviser who skips the script is caught; a reviewer who skips its own run is not. | source.md:77 | none (ratio 0.5333) |
| INF-058 | copy of the current `src/superclaude/commands/spec-panel.md` with only the regions of 3.2 changed | source.md:84 | Task 5 (ratio 1.0) |
| INF-059 | one page: purpose, subcommands, formats, exit codes; described as run by commands, not by users | source.md:85 | Task 4 (ratio 0.8333) |
| INF-060 | / new / `src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py` / about 350 lines, stdlib only, no `superclaude` import; | source.md:86 | Task 1 (ratio 0.8) |
| INF-061 | / new / `tests/skills/test_sc_fixcheck.py` / behaviour tests of the script (3.4) / | source.md:87 | Task 1 (ratio 0.8889) |
| INF-062 | / new / `tests/skills/test_spec_panel_minfix.py` / text pins of the variant command (3.4) / | source.md:88 | Task 5 (ratio 1.0) |
| INF-063 | the original stays the control; `test_spec_panel_review_loop.py`, `test_review_severity_rule.py`, `test_worker_contract.py` run unchanged | source.md:89 | Task 5 (ratio 0.8889) |
| INF-064 | the first implementation task runs them and adds a plugin mirror only if a parity test demands it | source.md:90 | none (ratio 0.5385) |
| INF-065 | Never stage `.claude/` (`make sync-dev` creates the dev copy). Neither new installed primitive names a `src/superclaude/` path. | source.md:92 | Task 8 (ratio 0.6875) |
| INF-066 | Both look in `~/.claude/skills/sc-fixcheck/` first, then the project `.claude/skills/sc-fixcheck/` (dual-surface rule for skills). | source.md:92 | none (ratio 0.5) |
| INF-067 | Frontmatter `name: spec-panel-minfix`, description marked experimental; the command name in the title and Usage lines. | source.md:96 | Task 5 (ratio 1.0) |
| INF-068 | Repository file only: Usage line 2 drops `[--unattended] [--report-dir <dir>]`, and the `## Unattended mode` section is removed. | source.md:97 | Task 5 (ratio 0.9231) |
| INF-069 | `## Review Loop` keeps seven bullets; bullets 1-5 and 7 are byte-identical. | source.md:98 | Task 5 (ratio 1.0) |
| INF-070 | Bullet 6 is 427's text minus the clause "each added paragraph or table cites its finding id" | source.md:98 | Task 5 (ratio 0.8571) |
| INF-071 | with this appended before its final period: `; the Reviser brief carries the ## Fix Budget steps, and a blocking finding the reviser cannot fix within budget is listed escalated with what it needs, never expanded`. The pins `Reviser brief` and `byte size before and after` stay. | source.md:98 | Task 5 (ratio 0.96) |
| INF-072 | A new `## Fix Budget` section between `## Review Loop` and `## Output Formats`, literal text below. | source.md:99 | Task 5 (ratio 0.9167) |
| INF-073 | Not changed: the existing Tool Coordination line that names `src/superclaude/examples/release-spec-template.md` (line 220) stays byte-identical. | source.md:101 | Task 5 (ratio 0.7778) |
| INF-074 | The project rule says not to add such references to a primitive, so the owner must accept this known inherited hit, or fix line 220 in both commands as a separate change. | source.md:101 | none (ratio 0.35) |
| INF-075 | If `hash --file <spec>` cannot run, stop with `E-FIXCHECK-MISSING`, name both paths, and do not review. | source.md:106 | Task 5 (ratio 0.7333) |
| INF-076 | Words are counted without `path:line` citations; bytes are counted on the raw added text. | source.md:108 | Task 2 (ratio 0.9) |
| INF-077 | / CRITICAL / CRITICAL blocking / 120 / 80 / 80 / 6 / 0 / 0 / 1 / 2 / 1 / 2 / 1 / | source.md:112 | Task 2 (ratio 0.75) |
| INF-078 | / blocking MAJOR / MAJOR blocking, FR-8, FR-9 / 80 / 50 / 50 / 4 / 0 / 0 / 1 / 1 / 1 / 1 / 1 / | source.md:113 | Task 1 (ratio 0.8) |
| INF-079 | / minor / every non-blocking finding / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / | source.md:114 | Task 2 (ratio 0.8333) |
| INF-080 | Whole cycle, overrides included: at most 600 gross added words and 6,144 gross added bytes, and the revised file at most 6,144 bytes larger than the baseline. | source.md:116 | Task 2 (ratio 0.7647) |
| INF-081 | `gap:<n>` (a blocking `MAJOR/FR-8` or `MAJOR/FR-9` gap fill, n = the guard-table rows it names) sets the condition-word limit to n. `override` and `gap:<n>` are exclusive. | source.md:116 | Task 1 (ratio 0.6667) |
| INF-082 | Exit codes of `hash`, `snapshot` and `check`: 0 accept; 1 policy failure, every reason tied to a hunk | source.md:118 | Task 1 (ratio 0.7143) |
| INF-083 | In every critique-mode review, run `hash --file <spec>` and add to the report a `fixbudget` block | source.md:120 | Task 1 (ratio 0.75) |
| INF-084 | On a `--re-review`, after the checks of Review Loop bullets 1 and 4 and before the prior-blocking table, run `check` without `--enforce` and without `--ledger` | source.md:120 | Task 2 (ratio 0.6471) |
| INF-085 | stop with the named input error, never fall back to a first review, and escalate with the open blocking findings | source.md:120 | none (ratio 0.4615) |
| INF-086 | Copy only numbers and ids from that run, never the reviser's reasons. | source.md:120 | Task 5 (ratio 1.0) |
| INF-087 | Reviser brief (place above the final `verdict:` line; fill `<...>`): | source.md:122 | none (ratio 0.5) |
| INF-088 | Every other finding is a minor note: change nothing for it and write `deferred (minor, fixcheck budget 0)` in its disposition row; a task brief that says to apply every finding is narrowed to this list (Review Loop bullet 7). | source.md:123 | Task 1 (ratio 0.625) |
| INF-089 | The script writes only `<report dir>/.fixcheck/base-<N>.md` and exits 4 if the spec changed since this review. Do not use a `--baseline` copy named in a review brief: that is the text the previous review saw. | source.md:124 | Task 8 (ratio 0.68) |
| INF-090 | Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for. | source.md:125 | Task 2 (ratio 0.6667) |
| INF-091 | A finding you cannot fix inside its budget goes under `## deferred` as `<id>: escalated: <what it needs>`. Do not expand it to fit. | source.md:126 | Task 5 (ratio 0.6) |
| INF-092 | Exit 0 is required. | source.md:127 | Task 1 (ratio 1.0) |
| INF-093 | In your report give the byte size before and after and paste the `result:`, `escalated:` and `FIXCHECK` lines of the first run when it was not exit 0, then those of the final run last, above the `fixledger` block. | source.md:128 | Task 2 (ratio 0.7083) |
| INF-094 | Constants `BUDGETS` (keys C, M, m = the table), `CYCLE_GROSS_WORDS=600`, `CYCLE_GROSS_BYTES=6144`, `MAX_OVERRIDES=1`, `EXIT={OK:0, POLICY:1, USAGE:2, INPUT:3, HASH:4, WRITE:5, INTERNAL:70}`. | source.md:133 | Task 1 (ratio 0.9615) |
| INF-095 | `parse_fixbudget` (block, overrides, `reviewed_sha256`, `refs`, GRADE-CONFLICT, Reviser-brief ids must be blocking ids, else exit 3) | source.md:133 | Task 1 (ratio 0.7857) |
| INF-096 | `--enforce` (whole-finding revert, `depends:` coupling, cycle-cap order, whole-file restore if the raw size check still fails, atomic temp-file-and-rename write, re-check; exit 3 without a ledger file or with an empty ledger) | source.md:133 | Task 3 (ratio 0.9259) |
| INF-097 | `snapshot` (writes only `.fixcheck/base-<N>.md`, exit 4 on hash mismatch) | source.md:133 | Task 1 (ratio 0.9091) |
| INF-098 | clean in-budget fix exits 0; 81 added words on a MAJOR fix exits 1 (`gross`); net 51 at gross 60 exits 1; a one-word minor edit exits 1 | source.md:153 | Task 2 (ratio 1.0) |
| INF-099 | a new heading, id, second table row, second MUST or second condition word each exit 1 with its own reason; an unattributed hunk, a quote not in the baseline and a mislabelled op each exit 1 | source.md:153 | Task 2 (ratio 1.0) |
| INF-100 | a blocking id neither fixed nor deferred is reported `unanswered` and does not change the exit code; a raw size growth above 6,144 bytes from whitespace only exits 1; a second or reason-less override exits 3 | source.md:153 | Task 2 (ratio 0.9259) |
| INF-101 | without `--ledger`, the lookup finds the one disposition file whose block names the report, and none or two such files exit 3; the per-hunk lines exist, carry the right `L<n>` and line range, and are identical across two runs | source.md:153 | Task 2 (ratio 0.8) |
| INF-102 | edits to two neighbouring sentences by two entries are credited to both entries; a finding reverted for exceeding its entries limit scores 0 entries afterwards; moved text counts zero; a `path:line` token adds zero words and a `(F3)` tag fails with `id` | source.md:153 | Task 2 (ratio 0.8889) |
| INF-103 | `--enforce` restores the over-budget and unattributed text, keeps in-budget fixes, reverts `depends:` partners whole, and a second `--enforce` changes nothing; `--enforce` without a ledger exits 3 and leaves the spec unchanged | source.md:153 | Task 3 (ratio 1.0) |
| INF-104 | `snapshot` on a changed spec and `check` on a mismatched baseline exit 4; the cycle cap reverts in the stated order | source.md:153 | Task 3 (ratio 0.7692) |
| INF-105 | after `--enforce`, a plain `check` on the same four inputs exits 0 and scores the reverted entries `reverted`; a property test (random edits, random ledgers) always satisfies that rule. | source.md:153 | Task 3 (ratio 0.85) |
| INF-106 | name and Usage lines; faithful copy (outside the listed regions the file equals `spec-panel.md` line for line, so an unmirrored edit of the original fails) | source.md:154 | Task 5 (ratio 0.8333) |
| INF-107 | seven bullets, 1-5 and 7 equal to the original's, bullet 6 contains `Reviser brief`, `byte size before and after` and `## Fix Budget`; `## Fix Budget` between `## Review Loop` and `## Output Formats`; the budget table, cycle limits and exit line equal the script constants | source.md:154 | Task 5 (ratio 0.9355) |
| INF-108 | the `~/.claude/` path precedes the `.claude/` path; `E-FIXCHECK-MISSING` present; no `src/superclaude` in the `## Fix Budget` section, the amended bullet 6 or the skill | source.md:154 | Task 5 (ratio 1.0) |
| INF-109 | Each adopter needs its own S1-style measurement first. | source.md:158 | none (ratio 0.375) |
| INF-110 | Command `spec-panel-minfix`, invoked as `/sc:spec-panel-minfix` (Skill target `sc:spec-panel-minfix`). Checker skill folder `sc-fixcheck`. | source.md:161 | Task 8 (ratio 0.7273) |
| INF-111 | Nothing about `spec-panel` changes. | source.md:161 | Task 3 (ratio 0.6) |
| INF-112 | To change one thing at a time, the experiment's `spec-panel-minfix.md` is the 3.2 change applied to that 472-line text (regions 1, 3 and 4; region 2 does not apply because that text has no unattended lines). | source.md:163 | Task 5 (ratio 0.7308) |
| INF-113 | The implementer builds it from `git show 95f2c6e4:src/superclaude/commands/spec-panel.md` into the experiment folder under `.dev/` (for example `.dev/experiments/346-minfix/build/spec-panel-minfix.md`), never under `src/`. The repository file applies the same hunks to the current 486-line `src/` file. | source.md:163 | none (ratio 0.5714) |
| INF-114 | Install for the experiment (owner or coordinator, never a worker; additive, no `--force`, no package reinstall): | source.md:165 | Task 8 (ratio 1.0) |
| INF-115 | `cp -n` never overwrites, and `~/.claude/commands/sc/spec-panel.md` is only hashed, never written. | source.md:178 | Task 8 (ratio 0.9231) |
| INF-116 | The existing D10 install watcher logs only the spec-panel sha256 and the `WORKER-CONTRACT.md` state; it must be extended to the three new files, and a change of any of them during an arm voids V6 as before. | source.md:178 | Task 8 (ratio 0.64) |
| INF-117 | After merge, `superclaude install` copies the new command and skill beside the originals in the same way (it skips existing command files unless `--force`). | source.md:178 | Task 8 (ratio 0.6471) |
| INF-118 | A missing home copy stops the run with `E-FIXCHECK-MISSING`, never a silent plain-427 review. | source.md:180 | Task 5 (ratio 0.6667) |
| INF-119 | Before measured runs, a fresh worker loads `/sc:spec-panel-minfix` through the Skill tool and runs the installed checker on one valid and one invalid fixture (exit 0, exit 1). | source.md:180 | Task 8 (ratio 0.9091) |
| INF-120 | The same probe checks that the worker's permission mode runs `uv run --no-project python ~/.claude/skills/...` without a prompt (UNVERIFIED today). | source.md:180 | Task 8 (ratio 0.6316) |
| INF-121 | with this one substitution applied to the review briefs T05, T07 and T09: | source.md:182 | Task 8 (ratio 1.0) |
| INF-122 | The reviser briefs T06 and T08 stay verbatim (the reviser learns the budget from the report). No brief mentions the checker, ledger or budget. | source.md:188 | Task 8 (ratio 0.7143) |
| INF-123 | Record the substitution in the coordinator log. | source.md:188 | Task 8 (ratio 0.75) |
| INF-124 | Scenario S1 (Orca worker-contract spec, 57,763 bytes, 8,148 words), base commit 2cb683f5, same overlay, same verbatim briefs plus the substitution of section 4, model claude-opus-5-5, `WORKER-CONTRACT.md` moved aside, 3 reviews and 2 fix cycles, two fresh worktrees (for example `exp346-ab-min-r1`, `-r2`). | source.md:191 | none (ratio 0.5227) |
| INF-125 | First, one pilot replicate runs BOTH fix cycles and checks that the reviser runs `snapshot` and `check` under the S1 ownership clauses | source.md:191 | none (ratio 0.4) |
| INF-126 | A failed pilot changes the Reviser brief wording, not the design. | source.md:191 | none (ratio 0.5) |
| INF-127 | If wording cannot fix it, the fallback is to name the cycle's own saved copy as the baseline in T06 (`spec-v1-draft.md`) and T08 (`spec-v2-after-round1.md`), declared as a second brief change. The pilot is not one of the two measured replicates. | source.md:191 | Task 8 (ratio 0.7419) |
| INF-128 | Comparators: ctl-r1 and ctl-r2 (reused, as in D11), then arm A and Arm B as secondary. | source.md:191 | Task 8 (ratio 0.6) |
| INF-129 | (a) review-3 critical+major proxy mean at most 3 and every replicate better than every control replicate (with controls 8 and 4, each replicate at most 3), or a clean pass sooner; | source.md:193 | none (ratio 0.5263) |
| INF-130 | (b) growth after two fix cycles at most 44.4%, every replicate below both controls; (c) effect larger than the larger within-arm spread. | source.md:193 | none (ratio 0.4286) |
| INF-131 | Validity V1-V6 as before, plus V7: each cycle's disposition ends with `FIXCHECK exit=0` (or lists what `--enforce` reverted) and the next review's own `check` does not exit 3, 4, 5 or 70. A replicate failing V7 is "mechanism not honoured" and is not treatment. | source.md:193 | none (ratio 0.5312) |
| INF-132 | and review 3 reported as proxy and blocking count, with blocking split into carried (open from review 2: unfixed, escalated, reverted) and new (on cycle-2 hunks), before the bar is applied. | source.md:195 | Task 2 (ratio 0.7368) |
| INF-133 | Minimality is not enough: the script ends exit 0 in both cycles of both replicates and review 3 is above 3 in either. Then drop minfix as a standalone fix and test it only combined with a verdict-side change. | source.md:202 | none (ratio 0.4) |
| INF-134 | The budget converts fix-induced findings into unfixed ones: carried open blocking findings at review 3 are 3 or more in either replicate. | source.md:203 | none (ratio 0.5333) |
| INF-135 | Surface is not the driver: 14 or fewer cycle-2 hunks, yet 3 or more new critical+major findings on them at review 3 in either replicate. | source.md:204 | none (ratio 0.5) |
| INF-136 | Only growth improves: growth is met but the review-3 proxy is not better than Arm B's mean 3.5. 427 already meets the growth bar, so the extra cost buys nothing; reject it. | source.md:205 | none (ratio 0.375) |
| INF-137 | Not a test of the idea (re-run instead): any V1-V7 failure, any check exit 3, 4, 5 or 70, or byte growth above 21.3% (raw `wc -c`, which the raw size check bounds) while the script reports exit 0 in both cycles (a checker bug). | source.md:206 | none (ratio 0.5) |
| INF-138 | Renumbering must be escalated in v1; the replay harness measures the false-positive rate first | source.md:224 | none (ratio 0.4) |
| INF-139 | 427 bullet 7 should prevail, and the arm reports both the proxy and the blocking count | source.md:227 | none (ratio 0.5) |
| INF-140 | First implementation task: a replay harness runs the finished script over the six recorded loops (baseline = previous history copy, ledger synthesised from each disposition). It checks the per-finding counts within 10% of section 2.3's calibration and measures the false-positive rate of `when`/`where` and the over-cap count per loop. | source.md:238 | none (ratio 0.5128) |
| INF-141 | Proposed v1 rule: print a deletion hunk with the revised line it sits before; merged opcodes are split per entry (section 2.2). Confirm both in the replay harness. | source.md:247 | Task 2 (ratio 0.7619) |
| INF-142 | If Arm C passes, merging bullet 6 and `## Fix Budget` into `spec-panel.md` is a separate change that must update the 427 pin test and the plugin mirror; the other adopters (section 3.5) each need their own measurement. | source.md:248 | none (ratio 0.5) |

Postscript: no inferred row was dropped (all 142 quotes matched their cited line by script; see the evidence-validator result below).

## Evidence-validator result

- Agent: evidence-validator (independent, read-only). Policy: sampled (citations > 20): 100% of the blocking findings' evidence (28 citations in merged-verdict.md) and of R-001..R-003 (6), all minor-finding evidence (42), every 3rd inferred-requirement row (47) plus about 35 more spot checks, 8 self-audit lines and 5 header numbers; 171 re-reads in total across REPORT.md and the merged card.
- Report citations re-read: about 94 of 154 (all 12 non-table citations, about 82 of the 142 inferred rows; all 142 inferred quotes were also matched to their cited line by the deterministic script).
- Dropped: 1. Original claim text (REPORT.md line 20, before correction): "Of the 38 unmatched: 22 are outside the plan's declared scope (plan line 19), 14 are covered in other words, 2 are real gaps (INF-028 = M-F2, INF-032 = M-F3)." Reason: reflection-card.yaml and t1-card.md support 21 / 16 / 1, and INF-028 is a matched row, not one of the 38. The line now carries the supported split.
- Overstatement noted (not dropped): [INFERRED] M-F4's "Nothing in the repo suppresses bytecode" holds for config files, but src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:35 tells /sc:implement executors to run task checks with `PYTHONDONTWRITEBYTECODE=1` and remove caches they created, so under /sc:implement the .pyc may never exist; the grep-exclusion fix stays cheap insurance and the merged grade is kept as debated.
- Status consequence: >= 1 dropped citation forces `status: partial`.

## Inferred-claim audit

- `citations_inferred: 6`
- Inferred-fraction: `6 / 154` = 0.04

