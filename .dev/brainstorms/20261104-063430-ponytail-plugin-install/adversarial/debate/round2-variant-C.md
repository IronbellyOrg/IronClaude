# Round 2: Variant C rebuttal (QA, `variant-3-haiku-qa.md`)

Lens: test surface, edge cases, regression risk, acceptance criteria. Re-read 2026-11-04: `install_user_setup.py:185-324`, `tests/cli/test_install_user_setup.py:73-98,175-242`, `install_hooks.py:60-80`, `.dev/codegraph-migration/evidence/P2-layer2.md:355-358,619-627`, `enrichment/assumption-evidence.md`, `enrichment/env-propagation-evidence.md`, both opponents' Round 2.

## Steelman (after Round 2)

**A.** A's Round 2 replacement rule ("a default plugin is added by data only; code changes only for defects on the shared plugin path, each pinned by a test", A R-2) is the correct resolution of X-002 and keeps everything C wanted from A's architecture. A's N2 is the best precision in the debate: the time-limit label already contains the plugin id (`:292` joins `args[1:3]`, so `install <id> --scope (time limit)`, confirmed at `P2-layer2.md:358`); only `:303,:305` drop it. A's N4 (Orca probe `timeout=10` at `:190` ignores the deadline; install capped at 25 s at `:226` against the 30 s budget) gives A-007 a mechanism, and A's N7 (project settings override a user `false`, `assumption-evidence.md:20`) fixes opt-out wording C got wrong by omission.

**B.** B's Round 2 is the discipline win. Its M1a/M1b split answers C's R1 weakness 6 exactly, its specified fail outcome for M1b (hold merge, document `config.json`, backlog issue, no installer write) is C's own R1 fallback adopted wholesale, and its N4 (`/ponytail default` prints success while the env key wins) upgrades a docs caveat into a required sentence. B's N3 gives T5 a concrete fixture with zero new setup.

## Response to Criticisms

| # | Criticism (source) | Response |
|---|---|---|
| 1 | "First" buys little; reorders six working plugins (A W4, B W5, X-006; A R2 "C should give up 'first'") | **Concede the position.** Steelman first: order is a real lever for everyone (`wanted` iterates the defaults file, `:266`; user dict order irrelevant, A N3), and in the partial-budget window the issue's target installs first. But the one observed starvation run (`P2-layer2.md:358`) skipped every install — position bought nothing — and the window that remains favors the wrong plugin: with `off` as the shipped default, Ponytail is dormant while the six it would jump are in active use. Guaranteeing a dormant install by starving an in-use one is backwards triage. C moves to B: append last as a diff-hygiene convention, no budget rationale, no order test. |
| 2 | C's "Behaviour today (verified)" row is false (X-004) | **Conceded in R1, stands.** Worse than I said: B R2 N1 shows the exit-code path failing in a real run (`P2-layer2.md:624`, six bare `--scope`). And A R2 R-1's precision is right — my R1 attack on A's table applied to the offline row only; A's time-limit row was directionally correct. |
| 3 | Hygiene: risk/check IDs, "T7" naming a unit test, CHANGELOG version and style, no line budget, no diff-scope AC (A W6, B W7; X-015, X-016, S-010, C-007, C-023) | **Concede.** C's artifacts are the worst of the three on referenceability; the merge must take B's AC-2 (5-line cap, allowed-files list), give the manual check one ID (B's M1a/M1b), ID every risk, and use the file's `###`/`####` CHANGELOG style with the verified upstream version named. |
| 4 | "`claude` is a Node app" is unverified (X-017) | **Concede.** Replace with A's repo-grounded fact: IronClaude's own SubagentStart hook needs `node` (`src/superclaude/cli/install_hooks.py:66-68`, "(needs node)" comment on `pragmatic-subagent.js`). Same docs conclusion, real evidence. |
| 5 | T7/T4 Ponytail-keyed legs add no branch coverage (B R2 #9) | **Mostly concede.** The code has no Ponytail branch, so keying the legs to Ponytail adds nothing today; the generic iteration (`test_install_user_setup.py:182-209`) picks Ponytail up automatically once the defaults change. Accept B's one addition — a `claude`-absent leg — and see New Evidence N1: it is the only untested branch in `install_plugins`, and B's own steelman of C conceded the kernel ("the never-fatal contract has an untested leg"). T7's three conditions survive keyed to whatever fixture already exists; the Ponytail fixture requirement drops. |
| 6 | `(label, argv)` pairs restructure is 6 lines against B's 4-line cap (A R2, B R2 #4) | **Concede the shape.** My R1 table already preferred B's argv-shape with C's tests; A's Round 2 converged on the same. The pairs' residual value (label built where argv is built, cannot desynchronize) is fully replaced by T5 asserting both labels on both paths. |
| 7 | B R2 #6: C's R1 claim that B omits the `/ponytail default` override is half wrong | **Concede.** B's docs block does carry it (B:169-170). My R1 weakness 5 overstated; the ledger-location and do-not-delete halves stand and B conceded those. |
| 8 | A R2 N2: a `deadline=0`-only label test passes today | **Correct, adopt.** Pre-fix, `:292` already emits the id. The load-bearing assertion is the non-zero-exit path (id present, `--scope` absent); the merged T5 must also assert `--scope` absent on the time-limit path, or it pins nothing after B's fix drops the verb. |

## Updated Assessment

**A** resolved its two code errors the right way: it kept the extension rule's intent and dropped only the false absolute. Its R-9 self-correction (`P2-layer2.md:624` is offline fast-failure, not starvation) was also right, and it improved the merged spec more than its R1 did. A's remaining unique load is structure: decision record, gate pass/fail wording, N7, and the per-subagent count.

**B** is the base for everything executable: the 4-line fix, T4 as an extension of the existing fill test (A N5's construction is right — `:73-98` already asserts idempotence at `:97-98`), M1a/M1b, count-free docs, migration note. B's R2 has no remaining unforced errors that I can find; its N3 fixture guidance should be adopted verbatim.

**C** ends the debate smaller than it entered, and correctly so: "first" is gone, the pairs are gone, the Ponytail-keyed test legs are gone. What survives from C is the acceptance discipline: the never-fatal contract gets its first real branch test (claude-absent), both failure paths get label assertions that fail pre-fix, the docs grep stays, the fork-not-pinned Coder question stays, and the throwaway-HOME check keeps A's pass/fail wording inside B's M1a/M1b.

**Merge:** B's code, tests and docs base + A's structure, gate wording, N4/N7 + C's claude-absent leg, both-path `--scope` assertions, grep check, Coder question.

## New Evidence

- **N1. The `claude`-absent branch of `install_plugins` has no test.** All three plugin tests monkeypatch `which` to `/bin/claude` (`test_install_user_setup.py:195,222,233`); only the Orca tests use `None` (`:112`). The branch at `install_user_setup.py:256-258` returns an exact tuple, so the new leg can assert it exactly the way `:226` pins the skip message: `(True, "⏭️  Plugins: claude CLI not found; skipped")`. B reached the same conclusion in its steelman; this is the verification and the assertion shape.
- **N2. Pick the T5 fixture deliberately.** `test_plugin_failures_and_time_limit_never_fail_install` enables only `playwright` (`:232`), so under B's N3 shape its post-fix labels are `anthropics/claude-plugins-official` / `playwright@claude-plugins-official` — no Ponytail fixture needed, since the label logic is plugin-agnostic. A Ponytail-named failure assertion requires adding Ponytail to that fixture dict; either is correct, the merged spec should just say which.
- **N3. Both logged runs show Orca consuming 25 s.** `P2-layer2.md:357` and `:623` each show the Orca timeout — the A-007 mechanism is observed twice, not once. In run 2 the two marketplace adds then failed fast offline (`:624`) and every install was skipped, so that single run is simultaneously evidence for the exit-path label defect and for the starvation shape. A-007's QUALIFY rests on two runs, not one.
- **N4. An A-003 key mismatch is masked by the success line.** If `known_marketplaces.json` is not keyed `ponytail`, the add re-queues every run (`:277-279`), succeeds, `failed` stays empty, and the function returns `✅ Plugins: installed ...` (`:307-311`) — a 13 MB re-clone per run reported as success, no warning ever. The M1a second-run check must therefore assert the exact `already installed` message (or zero `claude` invocations), not merely the absence of a warning. A's and B's checks already do assert the message; this is the mechanism that makes the detail load-bearing.

## Final Positions

| ID | Preferred approach | Changed since R1? |
|---|---|---|
| C-002 / X-001 | B: append last as a diff-hygiene convention; no budget rationale; no order test | yes |
| C-005 / X-002 / X-003 | B's 4-line shape + T5 asserting id present and `--scope` absent on BOTH paths + claude-absent leg; A's R-2 rule as the NFR wording | no |
| X-005 | none: correct the text in all three; backlog issue per A N4 (bound the `:190` probe by the deadline, or split the budget) | yes |
| C-012 / X-009 | merge: B's M1a/M1b split with A's pass/fail wording, non-blocking (`env-propagation-evidence.md:9`) | yes |
| C-013 / X-007 | C: documented `config.json` user step + backlog issue; no installer write (A and B converged here in R2) | no |
| C-016 | merge B + C: B's three questions + fork-not-pinned-version question | no |
| C-021 | B, plus B N4's warning that `/ponytail default` reports success while ignored | no |
| U-006 | B's T4, built as an extension of the existing fill test (A N5) | no |
| C-008 | B count-free wording + C's `grep -rn "six plugins" docs/` | no |
| A-001 | REJECT as stated (assumption false; docs/CHANGELOG say "upgrade the package, then `superclaude update`"; keep the Coder question) | yes (label only; substance unchanged) |
| A-002 | QUALIFY | no |
| A-003 | QUALIFY, sharpened by N4 (assert the exact message, not absence of warning) | no |
| A-004 | QUALIFY: no required fields means validation cannot fail, but closed-stdin prompting is UNVERIFIED (`assumption-evidence.md:15`); checked in M1a | yes (was ACCEPT; overstated) |
| A-005 | ACCEPT | no |
| A-006 | QUALIFY, narrowed by B N5 to per-prompt `node` cost (no phrase switches the mode on) | no |
| A-007 | QUALIFY: converges only while some run leaves budget; mechanism observed twice (N3) | no |
| A-008 | ACCEPT | no |
| A-009 | QUALIFY | no |
