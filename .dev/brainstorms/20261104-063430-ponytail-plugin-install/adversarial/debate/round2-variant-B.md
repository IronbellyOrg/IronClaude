# Round 2: Variant B rebuttal (refactorer, `variant-2-sonnet-refactorer.md`)

Lens: smallest correct diff, no new mechanism. Re-read 2026-11-04: `install_user_setup.py:26-36,185-324`, `tests/cli/test_install_user_setup.py:175-242`, `main.py:340-361`, `update.sh:1-10`, `hooks/hooks.json:110-128`, `.dev/codegraph-migration/evidence/P2-layer2.md:355-358,619-624`, upstream `hooks/ponytail-mode-tracker.js` and `ponytail-config.js` via `gh api` (read-only).

## Steelman (after Round 1 and A's Round 2)

**A.** A's Round 2 is the strongest self-correction in the debate. It conceded the false failure row, the false budget rationale and the order test, then replaced "zero Python" with a better rule: "a default plugin is added by data only; code changes only for defects on the shared plugin path, each pinned by a test" (A R-2). That is the correct statement of what B's NFR-003 was reaching for. A also showed U-006 costs three assertions (N5) and caught the project-over-user precedence gap in the opt-out wording (N7). A's per-subagent count (two IronClaude SubagentStart hooks, `hooks.json:110-128`) is a real argument for `off` that B never quantified.

**C.** C conceded its false "verified" row, its "first" mechanism and its ID hygiene. Its remaining kernel is sound: the never-fatal contract has an untested leg. No test in `test_install_user_setup.py` reaches the `claude CLI not found` branch (`install_user_setup.py:256-258`); B's NFR-001 lists "claude missing" as a guarantee and proves it only manually (AC-M3).

## Response to Criticisms

| # | Criticism (source) | Response |
|---|---|---|
| 1 | Budget wording: "starves the last-listed plugin" (A W1, C W2, X-005) | **Concede** (as R1). Adds precede installs (`:271-284`), so the clone is third in the queue. R4 becomes: "the 30 s budget can starve any install on a fresh workspace; Ponytail's 13 MB clone runs ahead of all six installs; a rerun resumes". No design change. |
| 2 | No fail outcome for AC-M1 (A W2, C W4, X-007) | **Concede, now specified.** If AC-M1b fails: hold the merge, document `~/.config/ponytail/config.json {"defaultMode":"off"}` as a user step, open a backlog issue. No installer write outside `~/.claude`. A's pass/fail wording is adopted. |
| 3 | AC-M1 conflates install mechanics with env propagation (C W6) | **Concede.** Split: AC-M1a (install mechanics: `installed_plugins.json` lists it; `known_marketplaces.json` key is `ponytail` for A-003; a second run prints `already installed` with no re-add; no prompt or hang for A-004) and AC-M1b (env: no `.ponytail-active`, no ruleset). Both stay non-blocking per `env-propagation-evidence.md:9`, recorded in the PR. |
| 4 | Positional label `args[3] if args[1]=="marketplace" else args[2]` repeats the coupling that caused the bug (A R1 W3) | **Withdrawn by A (R2).** I add: both argv lists are built within ten lines of the loop (`:278,:281`), and T5 asserts both labels, so a new flag breaks a test, not a report. |
| 5 | X-008: B:108 says the tracker re-injects the ruleset each prompt (A, C) | **Concede, with evidence.** Upstream `ponytail-mode-tracker.js:173-191` re-injects only inside `if (isQoder && !deactivated)`. On Claude Code it emits for `/ponytail` commands and deactivation phrases (`:125-165`). Fix the table cell; `off` is unaffected. |
| 6 | Docs drop the ledger and "do not delete the key" (C W5; C-009) | **Partly counter, partly concede.** C is wrong that B omits the `/ponytail default` override: B:169-170 says the variable "overrides `/ponytail default <mode>`". Concede the rest: add "do not delete the key" (in B:139 but not in the docs block), one ledger sentence (R6), and "in your user settings" (A N7: project settings win, `assumption-evidence.md:20`). |
| 7 | Rejected alternatives are scattered (A R2) | **Partly counter.** B:94-98 already holds "no `install_ponytail()`", "no `config.json` write", "no `node` pre-check" in one block. Concede two missing entries: Ponytail's own `full` (only in B:21) and installed-but-disabled; add both to 3.3. |
| 8 | Per-subagent load not counted (U-002) | **Concede.** Add to "Why `off`": IronClaude already runs two SubagentStart hooks (`hooks.json:110-128`); `full` would add a third to every Orca worker. |
| 9 | C's T7 (never fatal, three conditions) and T4 (skip) missing | **Qualify.** The code has no Ponytail branch, so a Ponytail-keyed leg adds no path coverage: `test_plugins_install_missing_enabled_defaults` (`:182-209`) already iterates every default and `test_plugins_skip_already_installed` (`:212-226`) covers the generic skip. **Accept one thing:** a `claude`-absent leg in T5 (monkeypatch `which` to `None`, assert the skip line and `ok is True`). It is test-only and backs B's own NFR-001. |

## Updated Assessment

**A** is the right source for structure: the extension rule as restated in A's R-2, the pass/fail gate wording, the rejected-alternatives list, the per-subagent count, and the correct reading of upstream (A was right on X-008; B was wrong). A's R-9 self-correction is accurate: `P2-layer2.md:624` is a fast-failure run, not starvation (`:627` shows a `URLError` in the next step). I adopt A's N5 (T4 as an extension of the existing fill test) and N7.

**C** should drop "first" (conceded) and its `(label, argv)` restructure, which touches six lines (`:278,:281,:289,:292,:303,:305`) against a 5-line cap for no behavioural gain. C keeps: the `claude`-absent leg, the `grep -rn "six plugins" docs/` check, the fork-not-pinned-version Coder question, and the point that label tests must assert the plugin id, not only the prefix.

**Merge:** B's code and test base, A's structure and gate wording, C's grep, Coder question and `claude`-absent leg.

## New Evidence

- **N1. Both failure paths now have real logs.** `P2-layer2.md:358` shows the time-limit path (`install <id> --scope (time limit)`, from `:292`). `P2-layer2.md:624` shows the exit-code path from `:303,:305`: `anthropics/claude-plugins-official, Lum1104/Understand-Anything, --scope, --scope, --scope, --scope, --scope, --scope`. R1 inferred the second path from code; it is now observed. Six of eight entries are unnamed, so with seven plugins the line cannot say which one failed.
- **N2. No code consumer parses the label.** A search for `Plugins: not installed` and `(time limit)` outside `.md` files finds only `install_user_setup.py:292,308`. R8 ("Very low") drops to "none found".
- **N3. T5 needs no Ponytail fixture.** `_plugin_home` with `playwright` enabled (`test_install_user_setup.py:232`) already queues one marketplace add and one install. After the fix the message must contain `anthropics/claude-plugins-official` and `playwright@claude-plugins-official` and not `--scope`; `deadline=0` must contain `(time limit)` and the same names. Today's assertions (`:240,:242`) pass with or without the defect, which is why it survived.
- **N4. `/ponytail default` reports success while the env key is `off`.** Upstream `ponytail-mode-tracker.js:67-72` writes the config and prints "PONYTAIL DEFAULT SET - new sessions start in <mode>", but `getDefaultMode` reads the env first (`ponytail-config.js:85`). The user is told it worked and it did not. R2 becomes a required docs sentence, and the CHANGELOG migration sentence (R1) should say so.
- **N5. Natural-language phrases cannot switch Ponytail on.** `isDeactivationCommand(prompt)` only turns the mode off (`ponytail-mode-tracker.js:160-165`); bare `/ponytail` turns on `full` when the default is `off` (`:117`). A-006 narrows to per-prompt `node` start cost.
- **N6. An unknown env value degrades to `full`.** `normalizeMode` returns `null` for unknown values (`ponytail-config.js:23`), then config, then `full`. R9 stands; T1 asserts the literal `"off"`.
- **N7. The package-upgrade gap is a docs fix.** `update.sh:7` is `pipx install --force ./` with no `git pull`; `main.py:344-345` says "to match the current package version". Docs and CHANGELOG say "upgrade the package, then run `superclaude update`". No code.

## Final Positions

| ID | Preferred approach | Changed since R1? |
|---|---|---|
| C-002 / X-001 | B: append last as a diff-hygiene convention; no budget rationale; no order test | no |
| C-005 / X-002 / X-003 | B's 4-line shape + T5 asserting both labels on both paths (N3) + `claude`-absent leg; A's replacement rule as NFR-003 wording | no |
| X-005 | none: correct the text in all three; budget fix is a separate backlog issue (bound the Orca probe at `:190`, or give plugins their own budget) | no |
| C-012 / X-009 | merge: B's AC-M1 split into M1a/M1b, A's pass/fail wording, non-blocking | yes (split) |
| C-013 / X-007 | merge C + A's trigger: documented `config.json` user step, hold merge, backlog issue; no installer write | no |
| C-008 | B (count-free) + C's `grep -rn "six plugins" docs/` | no |
| C-016 | merge B + C: B's three questions + "template installs the fork's current version" | no |
| C-021 | B: CHANGELOG migration sentence, now also warning that `/ponytail default` reports success but is ignored (N4) | no |
| U-006 | B's T4, built as an extension of the existing fill test (A N5) | no |
| A-001 | REJECT as stated (assumption is false; gap fixed in docs, N7) | yes (label only; R1 said "ACCEPT as a real gap") |
| A-002 | QUALIFY | no |
| A-003 | QUALIFY (checked in AC-M1a) | no |
| A-004 | QUALIFY (checked in AC-M1a) | no |
| A-005 | ACCEPT | no |
| A-006 | QUALIFY, narrowed to per-prompt `node` cost (N5) | yes (narrowed) |
| A-007 | QUALIFY: converges only while some run leaves budget; Orca can consume it (`:34,:190,:226`) | no |
| A-008 | ACCEPT | no |
| A-009 | QUALIFY | no |
