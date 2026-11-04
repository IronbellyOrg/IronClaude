# Round 2: Variant A rebuttal (architect, `variant-1-opus-architect.md`)

Lens: maintainability and extension scaffolding. Re-read 2026-11-04: `install_user_setup.py:29-36,137-172,201-240,251-324`, `main.py:340-405`, `update.sh:1-10`, `tests/cli/test_install_user_setup.py:73-98,175-242`, `.dev/codegraph-migration/evidence/P2-layer2.md:351-358,617-627`, `variant-1-opus-architect.md:91-106`.

## Steelman (after Round 1)

**B.** B's Round 1 is the most disciplined: it conceded its two textual errors (budget wording, no fail path) without moving its design, and its design is the one the code supports. Its 4-line label fix is the smallest change that removes a defect a real offline run has already shown (N1). Its T4 is the only direct proof of the existing-user outcome.

**C.** C's Round 1 is the most self-critical (X-004, X-006, X-015, X-016, S-010 all conceded). Its remaining claim, "first" order, has a real kernel: when budget runs out partway through the installs, position decides who wins, and Ponytail is the issue's subject. Its T7 (never fatal under three conditions) and the `grep -rn "six plugins" docs/` check are cheap, mechanical, and worth keeping.

## Response to Criticisms

| # | Criticism (source) | Response |
|---|---|---|
| R-1 | Failure table shows output the code cannot produce (B W1, C W1, X-003) | **Concede**, with one precision. The time-limit row (A:101) is correct: for a marketplace add `args[1:3]` is `marketplace add` and `args[3]` is the repo (`:278,:292`). The offline row (A:100) is false, and not hypothetically: `P2-layer2.md:624` is that exact condition in a real run and printed six bare `--scope` (N1). |
| R-2 | NFR-001 "zero Python" blocks the right fix (B W1, C W3, X-002) | **Concede.** Replacement rule keeps the architectural intent: "a default plugin is added by data only; no per-plugin code. Code changes are allowed only for defects on the shared plugin path, each pinned by a test and named in the diff-scope AC." That still rejects an `install_ponytail()` step (A:21 (a)) while allowing the label fix. |
| R-3 | T-1 pins "last key" for a false reason (B W2, C W2, U-003) | **Concede** the test and the reason. Keep "append last" only as a diff-hygiene convention (one added line per key, no churn in six working entries), stated without any budget claim. |
| R-4 | "Last protects the six" and "Ponytail most likely to hit the limit" (X-005, X-012) | **Concede both.** Adds precede installs (`:271-284`), so the 13 MB clone is third in the queue on a fresh workspace and can starve all six installs. A:106 must be rewritten; see N4 for why the real fix is outside #330. |
| R-5 | Blocking V-1 plus a code fallback is the costliest item for the least likely event (B W3) | **Concede** the block and the code fallback, given `env-propagation-evidence.md:5-9`. **Counter** on the shape: a check needs a defined fail outcome, and B conceded it had none (B R1 Concessions, X-007). Keep A's pass/fail text; the fail outcome becomes C's documented user step plus a follow-up issue, not installer code. |
| R-6 | Gate lives only in prose AC-3 (C W6) | **Partly counter.** V-1 is named and cross-referenced from AC-3 and R-1 with pass and fail (A:91,151,159). Moot now that it is optional; adopt B's AC-M numbering so it has one ID. |
| R-7 | "Seven plugins" drifts (B W4, C-008) | **Concede** (as in R1); B's count-free sentence plus C's grep. |
| R-8 | No existing-user test, no migration note (U-006, C-021) | **Concede.** N5 shows the test is three assertions on an existing test, so cost is no argument against it. |
| R-9 | Self-correction: my R1 said `P2-layer2.md:357-358,623-624` show budget starvation "both times" | **Wrong.** The second run was offline, not starved (N1). A-007 moves from REJECT to QUALIFY. |

## Updated Assessment

**B** is the right base for every code-facing decision. My R1 objection to its positional label (`args[3] if args[1] == "marketplace" else args[2]`) is withdrawn: C's `(label, argv)` pairs touch six lines (`:278,:281,:289,:292,:303,:305`) and break B's 5-line cap, while B's shape plus a T5 that asserts both labels under a non-zero exit pins the coupling just as well. B still needs: corrected R4 text, a fail outcome for AC-M1, and A's rejected-alternatives record so the next maintainer sees why there is no Ponytail step, no config-file write and no `node` check in one place.

**C** should give up "first". N3 shows order is decided only by the defaults file, and the one real run that hit the budget (`P2-layer2.md:358`) ran out before any install started, so position bought nothing there. "First" helps only in a narrow window (budget ends partway through installs), at the cost of reordering six working plugins for a plugin that ships dormant (`off`). C's T7, T4 skip test, grep check and fork-not-pinned handoff question should all survive into the merge.

**Merge recommendation (unchanged in shape):** A's structure (decision record, extension rule restated per R-2, interaction table, pass/fail wording) + B's code facts, label fix, T1 invariant, T4, migration note, count-free docs + C's T7, grep check and handoff question.

## New Evidence

- **N1. The second logged run was offline, not starved.** `P2-layer2.md:624` lists eight failures with no `(time limit)` suffix, so each command started with at least 2 s left (`install_user_setup.py:291-292`) and failed fast; `:627` shows a `URLError` on the next download. It is A's own "Offline" row happening for real, printing `--scope` six times. Only `:358` shows budget starvation.
- **N2. The defect is confined to the exit and exception paths.** The time-limit label `" ".join(args[1:3]) + f" {args[3]}"` (`:292`) already contains the plugin id for installs (`P2-layer2.md:358`). Only `:303` and `:305` drop it. The existing test checks the prefix after a non-zero exit (`test_install_user_setup.py:239-240`) and `"time limit"` (`:241-242`), so T5 must assert the plugin id on the non-zero-exit path; a `deadline=0` test alone would pass today.
- **N3. Order is a defaults-file-only lever.** `wanted` iterates `defaults["enabledPlugins"]` (`:266`), filtered by the user's value. The user's dict order does not matter, even though nested fill appends new keys at its end (`:158-160`). New and existing users get the same queue.
- **N4. Orca can use more than the whole shared budget.** `_find_orca` probes up to two CLIs (`_ORCA_CLIS`, `:30`) with a fixed `timeout=10` (`:190`) that ignores the deadline, then installs with up to 25 s (`:204,:226`) against a 30 s budget (`:35`). While any Orca skill is missing it retries every run (`:213-215`). That is the mechanism behind A-007 and belongs in a backlog issue (bound the probe by the deadline, or give plugins their own budget), not in #330.
- **N5. U-006 is cheap.** `test_settings_defaults_fill_only_missing_values` (`test_install_user_setup.py:73-98`) already starts from existing settings with a user `False` and a user `env` value and asserts idempotence (`:97-98`). B's T4 = assert the three Ponytail keys arrive, plus a user-set `PONYTAIL_DEFAULT_MODE` is kept. `test_plugins_install_missing_enabled_defaults` (`:182-209`) already iterates every default, so after the change it runs `marketplace add DietrichGebert/ponytail` unasserted; add one line beside `:205`.
- **N6. A-001 re-confirmed.** `update.sh:7` is `pipx install --force ./` from the local checkout with no pull; `update` re-installs "to match the current package version" (`main.py:344-345,360`) and only then runs user setup (`:403-405`).
- **N7. Opt-out wording gap.** Project settings `enabledPlugins` take precedence over user settings (`assumption-evidence.md:20`), so a user `false` loses to a project that enables Ponytail. The docs opt-out sentence should say "in your user settings".

## Final Positions

| ID | Preferred | Changed since R1? |
|---|---|---|
| C-002 / X-001 order | B: append last as a convention; no budget rationale; no order test | no |
| C-005 / X-002 / X-003 label fix | merge: B's 4-line shape + T5 asserting both labels on the non-zero-exit path (N2) + C's T7 | yes (shape moved from C's pairs to B's) |
| X-005 budget ordering | none: correct the text in all three; backlog issue per N4 | no |
| C-012 / X-009 env gate | merge: A's pass/fail wording inside B's AC-M1, non-blocking | no |
| C-013 / X-007 fallback | C: documented `config.json` user step plus follow-up issue; no installer write | no |
| C-008 docs count | B, plus C's grep check | no |
| C-016 Coder handoff | merge B + C | no |
| C-021 migration note | B | no |
| U-006 existing-user test | B, as an extension of the existing test (N5) | no |
| A-001 | REJECT (assumption false; docs and CHANGELOG state "upgrade the package, then `superclaude update`") | no |
| A-002 | QUALIFY | no |
| A-003 | QUALIFY | no |
| A-004 | QUALIFY | no |
| A-005 | ACCEPT | no |
| A-006 | QUALIFY | no |
| A-007 | QUALIFY: converges only while some run leaves budget; one starved run observed (`P2-layer2.md:358`), mechanism in N4 | yes (was REJECT; N1) |
| A-008 | QUALIFY | no |
| A-009 | QUALIFY | no |
