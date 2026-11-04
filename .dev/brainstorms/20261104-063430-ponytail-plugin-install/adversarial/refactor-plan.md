# Refactoring Plan: Merge into Base (Variant B)

## Overview

- Base: Variant B, `variant-2-sonnet-refactorer.md` (sonnet:refactorer), selected in `base-selection.md` (final 0.9395; Level 1 tiebreaker over A at 0.9392).
- Incorporating strengths from: Variant A (`variant-1-opus-architect.md`, opus:architect) and Variant C (`variant-3-haiku-qa.md`, haiku:qa), plus orchestrator decisions on the HIGH items in `invariant-probe.md`.
- Planned changes: 22
- Risk level: Medium overall. Most changes are text inside the base; four rewrite a whole base section (Changes 11, 18, 19, 21).
- Citations: `B:n` / `A:n` / `C:n` are variant lines; `A R2 N5` means `debate/round2-variant-A.md`, item N5; `INV-nnn` is `invariant-probe.md`.
- Scope of the merged spec stays #330: defaults file (three entries), the 4-line label fix, tests in `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md`, `CHANGELOG.md`. No other code file.

### Kept unchanged from the base (carried by the Round 2 consensus)

These base items are already in the consensus form and the merge executor must keep them as written:

- FR-001..FR-004 and the JSON block (`B:27-30,49-63`): `"ponytail@ponytail": true` appended after `understand-anything@understand-anything`, `extraKnownMarketplaces.ponytail` from `DietrichGebert/ponytail`, `env.PONYTAIL_DEFAULT_MODE = "off"` filled only when absent.
- FR-005 and Design 3.2 (`B:31,71-92`): the 4-line label fix `name = args[3] if args[1] == "marketplace" else args[2]`, `ok` stays `True`.
- T1 (`B:196`): defaults carry the three entries and every `enabledPlugins` marketplace has a `source.repo`.
- T2 (`B:197`): `["plugin","marketplace","add","DietrichGebert/ponytail"]` in calls and `ponytail@ponytail` in installs.
- AC-2 (`B:208`: allowed files, at most 5 changed Python lines), AC-3 (`B:209`), AC-M2 and AC-M3 (`B:211-212`).
- Visibility section (`B:147-153`): no change to `install --list` or `doctor`.

## Planned Changes

### Change 1: Order is a diff-hygiene convention, not a budget lever (consensus)

- **Source**: Round 2 consensus of all three advocates; A R2 R-3, B R2 Final C-002, C R2 #1.
- **Target**: Base, Design 3.1 "Order" bullet (`B:69`) (replace).
- **Rationale**: X-001/X-005: marketplace adds run before every install (`install_user_setup.py:271-284`), so key order protects nothing. All three advocates settled on "append last as a diff-hygiene convention; no budget rationale; no order test".
- **Integration point**: Replace `B:69` with: "Order: appended last as a diff-hygiene convention (one added line per key, no churn in the six existing entries). Order is not a budget lever, because every missing marketplace add runs before any install. No test pins the order." T1 must not assert key order.
- **Risk**: Low. Text only.

### Change 2: Correct the budget wording (X-005, X-012, A-007)

- **Source**: B R2 #1; A R2 N1 and N4; C R2 N3.
- **Target**: Base, Failure Behaviour row "30 s shared budget spent" (`B:128`), "Clone size" paragraph (`B:133`), Risk R4 (`B:221`) (replace).
- **Rationale**: B conceded that the 13 MB Ponytail clone is queued third, ahead of all six installs, on a fresh workspace (B R2 #1). "Not an outlier" (`B:133`) gives no sizes for the other two repos (X-012). "Rerun resumes" holds only while some run leaves budget; Orca used 25 s in both logged runs (`P2-layer2.md:357,623`).
- **Integration point**: R4 becomes: "The 30 s shared budget can starve any install on a fresh workspace: Ponytail's 13 MB clone runs ahead of all six installs. A rerun usually resumes, but not while Orca uses the budget on every run (see Known limitations)." In `B:133` delete "so it is not an outlier next to the two existing marketplaces" and keep the measured size. In `B:128` change "rerun resumes where it stopped" to "a rerun resumes where it stopped while some run leaves budget".
- **Risk**: Low. Text only.

### Change 3: NFR-003 states A's replacement rule (consensus)

- **Source**: Variant A, Round 2 R-2; adopted in B R2 Final C-005 and C R2 Final.
- **Target**: Base, NFR-003 (`B:40`) (replace).
- **Rationale**: X-002 resolved: A dropped "zero Python" and all three accepted A's restated rule as the NFR wording.
- **Integration point**: NFR-003: "A default plugin is added by data only; there is no per-plugin code. Code changes are allowed only for defects on the shared plugin path, each pinned by a test and named in AC-2. This PR's only such change is FR-005 (at most 5 changed Python lines). No new module, constant, flag or CLI option."
- **Risk**: Low.

### Change 4: Rejected-alternatives record (from A)

- **Source**: Variant A, Decision Summary (`A:21`); A R2 Updated Assessment; B R2 #7.
- **Target**: Base, Design 3.3 "Considered and rejected" (`B:94-98`) (restructure).
- **Rationale**: B conceded two missing entries (Ponytail's own `full`; installed-but-disabled) and agreed the record belongs in one place (B R2 #7).
- **Integration point**: Rewrite 3.3 as a lettered list: (a) a dedicated `install_ponytail()` step; (b) Ponytail's own default `full`; (c) installed but disabled (hides the skills, so #330 stays open); (d) the installer writes `config.json` (see Change 10 for the path); (e) a `node` pre-check; (f) reordering plugins for budget priority (Change 1); (g) a merge-blocking env gate (Change 18). One-line reason each, taken from `A:21`, `B:96-98` and the debate points cited.
- **Risk**: Low. Additive.

### Change 5: Per-subagent count (from A)

- **Source**: Variant A, Interaction table (`A:82`, U-002); B R2 #8.
- **Target**: Base, "Why `off`" paragraph (`B:21`) and Interaction bullet "Orca workers / subagents" (`B:117`) (insert).
- **Rationale**: B conceded it never quantified this (B R2 #8); A's count is the strongest architectural reason for `off`.
- **Integration point**: Insert after the first sentence of `B:21`: "IronClaude already injects two blocks into every subagent (`freshness-subagent-start.sh` and `pragmatic-subagent.js`, `src/superclaude/hooks/hooks.json:110-128`); a non-`off` mode would add a third to every Orca worker and `/sc:*` subagent." Add the same fact to `B:117`.
- **Risk**: Low. Additive.

### Change 6: Correct the UserPromptSubmit cell (X-008)

- **Source**: Variant A (`A:83`); B R2 #5 (upstream `ponytail-mode-tracker.js:125-165,173-191`).
- **Target**: Base, Interaction mode table, UserPromptSubmit row (`B:108`) (replace).
- **Rationale**: B conceded the cell was wrong: per-prompt re-injection runs only under Qoder.
- **Integration point**: Active-mode cell: "On Claude Code, emits only for `/ponytail ...` commands and deactivation phrases ('stop ponytail', 'normal mode'); per-prompt ruleset re-injection is Qoder-only. No phrase switches the mode on (B R2 N5)." `off` cell unchanged.
- **Risk**: Low.

### Change 7: Real `off` footprint replaces every "dormant / nothing is added" claim (INV-001, orchestrator decision)

- **Source**: `invariant-probe.md` INV-001 (upstream `band/register.tsx:86-91,154-163,201-222,254-349`); A R-4 (`A:162`); C (`C:48`).
- **Target**: Base, Decision Summary row 3 (`B:13`), "Why `off`" (`B:21`), NFR-006 (`B:43`), Interaction table Band row (`B:109`), Opt-out item 3 (`B:141`), docs block (`B:165-171`), CHANGELOG Added (`B:183`), Risks R6 and R7 (`B:223-224`) (replace).
- **Rationale**: INV-001 (HIGH): the band module never checks the level. "Nothing is added to your sessions" (`B:168`) and "no injected context" (`B:43`) are false as written.
- **Integration point**: Everywhere the base says or implies `off` is dormant, state instead: "In `off`, Ponytail injects no ruleset, codebase map, statusline offer or subagent context. Its band module still runs in every session, Orca workers included: it draws a band above the prompt, runs `git grep` over the repo at session start, watches every Edit and Write, and after every turn writes a ledger row (`$XDG_CONFIG_HOME/ponytail/band/<project>.csv` when that variable is set, else `~/.config/ponytail/band/<project>.csv`; local only, webhook empty by default)." Document two controls: `/ponytail band off` hides the band (it writes `~/.claude/.ponytail-band`; the `git grep`, the Edit/Write watch and the ledger keep running), and Ponytail's `ledger` userConfig option (`false` stops the CSV row). Interaction Band row (`B:109`): drop "UNVERIFIED end to end" and cite INV-001's upstream lines. R6: probability High, the full footprint, both controls. R7: "Users read `off` as broken" stays, and the docs sentence names what `off` still does. NFR-006: "limited to: one more plugin, one more env key, no injected ruleset in mode `off`, and the band module's footprint above".
- **Risk**: Medium. Rewrites claims in nine places. A missed occurrence leaves a false claim, so the merge log must list each one.

### Change 8: Ledger default, open decision PENDING coordinator (INV-001)

- **Source**: Orchestrator instruction on INV-001.
- **Target**: Base, Design 3.1 (`B:47-69`) and Opt-out (`B:136-144`) (insert a new subsection "Open decision: ledger default", after 3.1).
- **Rationale**: The coordinator has not yet decided whether IronClaude turns the ledger off by default. The plan writes both outcomes and picks neither.
- **Integration point**: Insert:
  - "**Status: PENDING coordinator decision. The implementer must not pick.**"
  - "Outcome 1, ledger off by default: the defaults file gains `pluginConfigs["ponytail@ponytail"].options.ledger = false`. The top-level `pluginConfigs` key is filled only when the user's settings lack it, so a user value is never changed. T1 asserts the entry. Docs and CHANGELOG say the ledger ships off and how to turn it back on. M1c records whether a ledger row appears (UNVERIFIED until then)."
  - "Outcome 2, Ponytail's default (ledger on): no defaults entry. Docs and CHANGELOG say the ledger is on and that the `ledger` userConfig option turns it off."
  - Change 7's wording holds for both outcomes; only the default sentence differs.
- **Risk**: Medium. An unresolved decision blocks finishing the docs. Mitigation: both texts are pre-written.

### Change 9: `/ponytail` mode is shared per repo, not per session (INV-002)

- **Source**: `invariant-probe.md` INV-002 (`ponytail-runtime.js:46-66`, `ponytail-activate.js:31-35`, `ponytail-mode-tracker.js:110-118`).
- **Target**: Base, Interaction "Pragmatic ladder" bullet (`B:113`), Opt-out item 2 (`B:140`), docs block ("Type `/ponytail` for one session", `B:168`) (replace).
- **Rationale**: INV-002 (MEDIUM): "per session" is false. The mode is stored per project directory plus a global flag.
- **Integration point**: Replace "for one session" with: "`/ponytail <level>` switches the mode for every session in that repo, not only the current one. Any new session that starts in `off` in that repo (an Orca worker, a resume, `/clear`) switches it back off. While a level is on, every subagent of every session in the repo gets the ruleset. Bare `/ponytail` switches to `full`."
- **Risk**: Low.

### Change 10: `$XDG_CONFIG_HOME` path for Ponytail's files (INV-006)

- **Source**: `invariant-probe.md` INV-006 (`ponytail-config.js:54-65`, `register.tsx:148-149`).
- **Target**: Base, every `~/.config/ponytail/...` mention: `B:97`, `B:142`, CHANGELOG migration sentence (`B:183`), R1 (`B:218`), R6 (`B:223`), and the fallback user step from Change 18 (replace).
- **Rationale**: Ponytail prefers `$XDG_CONFIG_HOME/ponytail` when that variable is set.
- **Integration point**: Write "`$XDG_CONFIG_HOME/ponytail/` (or `~/.config/ponytail/` when `XDG_CONFIG_HOME` is unset)" at first mention in each section; later mentions in the same section may use the short form.
- **Risk**: Low.

### Change 11: Docs block rewrite (count-free, opt-out, upgrade, footprint)

- **Source**: Base docs block (`B:159-172`) + Variant A docs paragraph (`A:123`) + A R2 N7 + B R2 #6 + C (`C:73,75`) + A-001 (all three Round 2) + INV-026.
- **Target**: Base, Docs and CHANGELOG, `installation.md` block (`B:157-174`) (restructure).
- **Rationale**: Consensus: docs stay count-free; opt-out says `false` in USER settings, because project settings win (`assumption-evidence.md:20`); "do not delete the key" (B conceded it was missing from the docs text, B R2 #6); "upgrade the package, then `superclaude update`/`install`" (A-001 rejected as stated by all three in Round 2).
- **Integration point**: The docs block must contain, in this order:
  1. The count-free plugin sentence (`B:160-163` unchanged).
  2. What Ponytail adds (skills, `/ponytail`), the `off` default and its real footprint (Change 7), the per-repo mode (Change 9), the ledger default (Change 8 outcome text).
  3. `PONYTAIL_DEFAULT_MODE` overrides `/ponytail default <mode>`, which prints "PONYTAIL DEFAULT SET" but has no effect while the variable is set (B R2 N4).
  4. Opt-out: "Set `"ponytail@ponytail": false` in `enabledPlugins` in your user settings (`~/.claude/settings.json`). A project `.claude/settings.json` that enables it wins over your user value. Do not delete the key: the next install adds it back as `true`."
  5. Upgrade step: "Existing workspaces get Ponytail only after the IronClaude package itself is upgraded: upgrade the package the way you installed it (for a checkout, `git pull` before `./update.sh`, because `update.sh` reinstalls from the local checkout), then run `superclaude update` or `superclaude install`."
  6. `node` needed for its hooks; IronClaude's own SubagentStart hook already needs it (`install_hooks.py:66-68`).
  7. Known limitation from Change 20 (one sentence).
  - Add to AC-1: "`grep -rn "six plugins" docs/` returns nothing" (from `C:75`).
- **Risk**: Medium. Largest user-facing text; it must agree with Changes 7-10 and 20.

### Change 12: CHANGELOG block (Added + Fixed + migration)

- **Source**: Base CHANGELOG (`B:178-188`) + B R2 N4 + C R2 #3 + A-001 + Changes 7, 8 and 10.
- **Target**: Base, Docs and CHANGELOG, CHANGELOG block (`B:176-188`) (replace).
- **Rationale**: Consensus: CHANGELOG has Added + Fixed + a migration sentence saying `/ponytail default` reports success but the env value wins; the upgrade step goes in the CHANGELOG too (A-001).
- **Integration point**: Keep the `### Ponytail plugin installed by default (#330)` / `#### Added (default plugins)` / `#### Fixed (plugin install report)` structure (`B:179-187`, matches `CHANGELOG.md:11-13`). Added entry: install/update/`update.sh` install `ponytail@ponytail` from `DietrichGebert/ponytail` (verified against upstream v5.3.3); `PONYTAIL_DEFAULT_MODE=off` when unset; the `off` footprint (Change 7) and ledger default (Change 8); opt out with `false` in user settings, do not delete the key; "upgrade the IronClaude package, then run `superclaude update` or `superclaude install`"; `node` needed. Migration sentence: "If you already use Ponytail with a default in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json`), the new `PONYTAIL_DEFAULT_MODE=off` wins over it, and `/ponytail default <mode>` reports success but has no effect while that variable is set. Set `env.PONYTAIL_DEFAULT_MODE` to your preferred mode instead." Fixed entry unchanged (`B:187`).
- **Risk**: Low.

### Change 13: Failure Behaviour additions (A-002, A-003, `node`)

- **Source**: Variant A (`A:103-104`); C R2 N4; `invariant-probe.md` INV-024, INV-025.
- **Target**: Base, Failure Behaviour table (`B:124-131`) (insert two rows, replace the `node` row).
- **Rationale**: A-002 (enabled but not installed) is a state every failure path ships, and only A recorded it. C R2 N4 showed that a marketplace key mismatch hides behind a success line.
- **Integration point**: Insert row "Enabled in settings but not installed (any failure above)": same state the six existing plugins can reach; Claude Code may install it in the background (`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`, `assumption-evidence.md:19`); UNVERIFIED. Insert row "Marketplace keyed other than `ponytail` in `known_marketplaces.json`": the add re-queues every run and the step still prints `✅ Plugins: installed ...` (`install_user_setup.py:277-279,307-311`); caught only by M1a. Replace the `node` row (`B:129`) evidence with A's repo fact (`install_hooks.py:66-68`) and INV-025 (upstream hooks force-exit within 1 s; with the defaults' `"verbose": true` each failure shows an error).
- **Risk**: Low. Additive.

### Change 14: T5 asserts the plugin id present and `--scope` absent on both failure paths (consensus)

- **Source**: Base T5 (`B:200`) + B R2 N3 + A R2 N2 + C R2 #8 and N2.
- **Target**: Base, Tests table row T5 (`B:200`) (replace).
- **Rationale**: Today's assertions (`test_install_user_setup.py:240,242`) pass with or without the defect. Before the fix, the time-limit path already prints the id (`:292`), so the non-zero-exit leg is the one that fails before the fix (A R2 N2). Consensus requires both paths to assert the id present and `--scope` absent.
- **Integration point**: T5 = extend `test_plugin_failures_and_time_limit_never_fail_install` (`:229-242`) using its existing `playwright`-only fixture (C R2 N2: the label logic is plugin-agnostic, so no Ponytail fixture). Non-zero-exit leg: `ok is True`; message contains `anthropics/claude-plugins-official` and `playwright@claude-plugins-official`; `"--scope" not in message`. `deadline=0` leg: `ok is True`; message contains `(time limit)` and the same two names; `"--scope" not in message`.
- **Risk**: Low. Test only.

### Change 15: `claude`-absent test leg (consensus)

- **Source**: C R2 N1; B R2 #9.
- **Target**: Base, Tests table (`B:194-201`) (insert new row T5c after T5) and Failure row "No `claude` CLI" (`B:126`) (append "pinned by T5c").
- **Rationale**: The branch at `install_user_setup.py:256-258` has no test; every plugin test patches `which` to `/bin/claude` (`test:195,222,233`). B's NFR-001 guarantee was proven only manually.
- **Integration point**: T5c: monkeypatch `shutil.which` to return `None`; assert `install_plugins(...) == (True, "⏭️  Plugins: claude CLI not found; skipped")` (two spaces after the emoji, as in the source). Proves NFR-001.
- **Risk**: Low. Test only.

### Change 16: Existing-user test as an extension of the existing fill test (consensus, INV-017)

- **Source**: Base T3 and T4 (`B:198-199`); A R2 N5; B R2 Final U-006; C R2 Updated Assessment; `invariant-probe.md` INV-017.
- **Target**: Base, Tests table rows T3 and T4 (`B:198-199`) (restructure into one row, "T3/T4").
- **Rationale**: Consensus: build the existing-user proof as an extension of `test_settings_defaults_fill_only_missing_values` (`test:73-98`), not a new test. INV-017: one fixture cannot both add a key and keep a user value for that same key, so the extension needs two legs.
- **Integration point**: Extend `test_settings_defaults_fill_only_missing_values` with two legs. Leg 1 (existing user): settings hold the old six plugins and two marketplaces; after `apply_settings_defaults`, `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]` is present and `env["PONYTAIL_DEFAULT_MODE"] == "off"` (the three keys arrive), the rest is unchanged, and a second run returns `(True, "✅ Settings defaults: already present")`. Leg 2 (user choice kept): `enabledPlugins["ponytail@ponytail"] = False` and `env.PONYTAIL_DEFAULT_MODE = "full"` are unchanged after apply. Proves FR-003, NFR-002, NFR-004 and the existing-user success criterion.
- **Risk**: Low. Test only.

### Change 17: Install test assertions (consensus)

- **Source**: Base T2 (`B:197`); A R2 N5 ("add one line beside `:205`").
- **Target**: Base, Tests table row T2 (`B:197`) (insert one clarifying sentence).
- **Rationale**: Consensus requires the install test to assert `marketplace add DietrichGebert/ponytail` and `install ponytail@ponytail`. T2 already does; A R2 N5 shows the existing test runs the add unasserted until these lines exist.
- **Integration point**: Append to T2: "Both assertions go next to the existing assertions at `test_install_user_setup.py:205`; the test already iterates every default, so no fixture change."
- **Risk**: Low.

### Change 18: Manual checks M1a / M1b / M1c, non-blocking (consensus, INV-009, INV-010, INV-029)

- **Source**: Base AC-M1 (`B:210`) + B R2 #2 and #3 + A V-1 pass/fail wording (`A:91`) + C R2 N4 + `invariant-probe.md` INV-009, INV-010, INV-029 (orchestrator decision).
- **Target**: Base, Tests and Acceptance Criteria, AC-M1 (`B:210`) (restructure into three items); Interaction "Environment" bullet (`B:118`) (replace its UNVERIFIED with a pointer to `enrichment/env-propagation-evidence.md` and M1b).
- **Rationale**: Consensus: M1a covers install mechanics, M1b covers env propagation; both non-blocking, recorded in the PR. INV-029 (HIGH): nothing proves Ponytail is present in a session. INV-009: M1b's absence signal needs a positive control.
- **Integration point**: All three run in one throwaway `HOME` under `/tmp`, never this workspace's `~/.claude`, with network and the real `claude` CLI. Evidence is recorded in the PR. No check blocks the merge (`env-propagation-evidence.md:9`).
  - **M1a (install mechanics)**: `~/.claude/plugins/installed_plugins.json` lists `ponytail@ponytail`; `~/.claude/plugins/known_marketplaces.json` has the key `ponytail` (A-003); a second `superclaude install` prints exactly `✅ Plugins: already installed` (C R2 N4: a key mismatch otherwise hides behind `✅ Plugins: installed ...`); the install finishes with no prompt and no hang under closed stdin (A-004). Fail outcome (INV-010): record the evidence in the PR and open a follow-up issue.
  - **M1b (env reaches the hook)**: with settings `env.PONYTAIL_DEFAULT_MODE = "off"`, a new session shows no Ponytail ruleset and `~/.claude/.ponytail-active` is absent (A's V-1 pass wording, `A:91`). M1b counts as evidence only if M1c passed in the same HOME (INV-009). Fail outcome: document `{"defaultMode": "off"}` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json`) as a user step in the docs, and open a follow-up issue. The installer never writes outside `~/.claude`.
  - **M1c (positive control, INV-029)**: the plugin's skill files exist under the installed plugin directory in `~/.claude/plugins/`. If a Claude session can be started in that HOME: the `ponytail-*` skills are listed, `/ponytail lite` returns "PONYTAIL MODE CHANGED — level: lite" and `~/.claude/.ponytail-active` appears, then `/ponytail off` clears it. If a session cannot be started there, record M1c as UNVERIFIED in the PR (and M1b therefore as unconfirmed). If Change 8 outcome 1 is chosen, also record whether a ledger row is written.
- **Risk**: Medium. Restructures acceptance; a reader could mistake the M checks for merge gates. The text says "non-blocking" in each item.

### Change 19: Coder Handoff section, merged B + C, no Coder repo edits (consensus, INV-027)

- **Source**: Base Coder Handoff (`B:239-246`) + Variant C (`C:114`) + C R2 Final C-016 + `invariant-probe.md` INV-027 (orchestrator decision).
- **Target**: Base, Coder Handoff (`B:239-246`) (restructure).
- **Rationale**: Consensus merges B's three questions with C's fork-not-pinned-version question. INV-027 decision: keep "Closes #330", because the issue asks that the installer and update scripts install Ponytail and this change does. The Coder confirmation is written as a handoff section in the merged spec, with no Coder repo edits.
- **Integration point**: Section title "Coder Handoff (confirmation only; no Coder repo edits, no Orca link flags)". Questions: (1) does the template run `superclaude install` or `update` on create and refresh, and does a pre-written `settings.json` pin `PONYTAIL_DEFAULT_MODE` or `false` (`B:242`); (2) are `claude` and `node` on PATH before that step (`B:243`); (3) is there headroom for a third marketplace clone, given Change 20's limitation (`B:244`); (4) does the template install `superclaude` from the fork at its current version rather than a pinned older one, since existing workspaces get Ponytail only after a package upgrade (`C:114`, A-001). Close with: "No answer blocks this PR. The PR keeps `Closes #330`. If answer 1, 2 or 4 is 'no', file a handoff issue from `~/.claude/ISSUE-HANDOFF.md`." The PR description carries a one-paragraph summary of this section.
- **Risk**: Low.

### Change 20: Known limitations and follow-ups (consensus, INV-028, INV-024)

- **Source**: A R2 N4; B R2 Final X-005; C R2 N3; `invariant-probe.md` INV-028 (orchestrator decision: out of scope), INV-024.
- **Target**: Base, new H2 "Known Limitations and Follow-ups" inserted after Risks (`B:226`) and before Out of Scope (`B:229`) (insert). Also add Risks R10 (insert after `B:226`).
- **Rationale**: Consensus makes the budget/Orca starvation a follow-up. INV-028 decision: out of scope for this PR, stated as a known limitation in the PR description and the docs.
- **Integration point**:
  - Limitation (verbatim in the docs, Change 11 item 7, and in the PR description): "On a workspace where Orca's skill install uses the shared 30 s network budget on every run, the installer may not reach the Ponytail install. Such a workspace gets Ponytail on a later run that leaves budget, or through Claude Code's own background install of enabled plugins (UNVERIFIED)."
  - Mechanism (spec only): `_find_orca` probes with a fixed `timeout=10` that ignores the deadline (`install_user_setup.py:190`), then installs with up to 25 s (`:226`) of a 30 s budget (`:35`), and retries every run while an Orca skill is missing (`:213-215`); observed at `P2-layer2.md:357,623`.
  - R10 (INV-024): Claude Code installs enabled plugins in the background, so a session started during workspace boot may clone the same marketplace while the installer does (a race), or may rescue a starved install. Both effects are UNVERIFIED. Probability Low, impact Low, mitigation: never fatal; M1a observes the installer path only.
  - Follow-ups (each a backlog issue from `~/.claude/ISSUE-BACKLOG.md`): (1) bound the Orca probe by the deadline or give plugins their own budget; (2) if M1b fails, the `config.json` user-step follow-up from Change 18; (3) if M1a fails, its follow-up; (4) report default-plugin state in `doctor`, informational only (`B:153`); (5) the ledger default, if the coordinator defers the Change 8 decision.
- **Risk**: Low. Additive.

### Change 21: Decision Summary rows follow the changes above

- **Source**: Changes 1-20.
- **Target**: Base, Decision Summary table (`B:9-19`) (replace rows 2, 3, 4, 7, 8, 9).
- **Rationale**: The summary must not contradict the body after the merge.
- **Integration point**: Row 2: add "existing workspaces get the entries after the package is upgraded (A-001)". Row 3: replace "no rules, map, nudge or per-subagent injection" with the Change 7 wording. Row 4: name the fixed label on both paths. Row 7: add "opt out in user settings; do not delete the key; `grep "six plugins"` empty". Row 8: "T1-T5 plus T5c; T3/T4 merged into the extended fill test". Row 9: "Coder Handoff section (confirmation only); PR keeps `Closes #330`".
- **Risk**: Medium. Touches every row a reader sees first; a stale row contradicts the body. The merge executor re-checks each row against its section.

### Change 22: Risk table refresh for the probe items

- **Source**: `invariant-probe.md` INV-002, INV-006, INV-009, INV-024; Changes 7-10, 18, 20.
- **Target**: Base, Risks table (`B:216-226`) (replace R1, R2, R6; insert R10 per Change 20; insert R11).
- **Rationale**: The orchestrator asked for the MEDIUM probe items to be folded into wording or risks.
- **Integration point**: R1 and R2 gain the XDG path (INV-006) and "`/ponytail default` prints success" (B R2 N4). R6 per Change 7. R11 (INV-002): "A user switches Ponytail on in one session; another session or Orca worker starting in that repo switches it back off, or the ruleset reaches every subagent in that repo while on." Probability Medium among opt-in users, impact Low, mitigation the Change 9 docs sentence. INV-009 is handled by M1b's dependency on M1c (Change 18), not a risk row.
- **Risk**: Low.

## Base Weaknesses to Fix

| Issue in base | Better variant / source | Fix approach |
|---------------|-------------------------|--------------|
| R4 and the budget rows say the last-listed plugin is starved; adds actually precede installs (X-005) | A R2 N4, C R2 N3 (none of the three was right as written) | Change 2 |
| "Not an outlier" clone size has no comparison data (X-012) | A (`A:106` gives the measured size only) | Change 2 |
| UserPromptSubmit cell says per-prompt re-injection (X-008) | A (`A:83`) | Change 6 |
| No fail outcome for the env check (X-007) | C (`C:89`) with A's trigger (`A:91`) | Change 18 (M1b fail outcome) |
| AC-M1 mixes install mechanics and env propagation (C R1 W6) | B's own R2 split | Change 18 |
| Docs omit "do not delete the key", the ledger and user-settings precedence (C-009) | A (`A:111,123`), A R2 N7, C (`C:73`) | Changes 7, 11 |
| Missing rejected alternatives `full` and disabled | A (`A:21`) | Change 4 |
| Per-subagent load not counted (U-002) | A (`A:82`) | Change 5 |
| No `claude`-absent test (C R2 N1) | C | Change 15 |
| T5 assertions pass before the fix | A R2 N2, C R2 #8 | Change 14 |
| "Existing users get it on update" ignores the package upgrade (A-001) | C (`C:114`) partly; all three in R2 | Changes 11, 12, 19, 21 |
| "Nothing is added to your sessions" in `off` (INV-001) | invariant probe; A R-4, C (`C:48`) | Changes 7, 8 |
| "/ponytail for one session" (INV-002) | invariant probe | Change 9 |
| No session-side proof of presence (INV-029) | invariant probe | Change 18 (M1c) |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-002 / X-001 | C: Ponytail first in `enabledPlugins` and `extraKnownMarketplaces` (`C:17,33`) | C conceded (C R2 #1): `extraKnownMarketplaces` order has no effect (X-006), the one starved run skipped every install (`P2-layer2.md:358`), and moving a dormant plugin ahead of six in active use is backwards triage. |
| U-003 | A: T-1 asserts Ponytail is the last key (`A:141`) | Pins an order whose stated reason is false (X-005); A conceded (A R2 R-3). |
| X-002 / C-007 | A: NFR-001 zero Python lines; AC-2 forbids any `cli/*.py` diff (`A:37,150`) | Would ship the `--scope` defect on a seventh plugin (X-003; `P2-layer2.md:624`); A withdrew it (A R2 R-2). |
| C-006 | C: `(label, argv)` pairs (`C:37`) | Touches six lines against the 5-line cap for the same behaviour; T5 on both paths pins the coupling (A R2 Updated, B R2 #4, C R2 #6). |
| C-013 / X-007 | A: installer writes `config.json` when absent (`A:21,91`) | New write outside `~/.claude`, Ponytail's private path rules, an NFR waiver, for an event `env-propagation-evidence.md` makes unlikely (B R1 W3; A R2 R-5). The documented user step is kept instead (Change 18). |
| X-009 / C-012 | A: V-1 must pass before merge (`A:91`) | All three settled on a non-blocking check (`env-propagation-evidence.md:9`); A's pass/fail wording is kept (Change 18). |
| C-008 / X-010 | A and C: "seven plugins" (`A:121`, `C:73`) | Recreates the drift at the next add; A conceded (A R1 Concession 3). C's grep is kept (Change 11). |
| C-011 (C T4, T7 Ponytail-keyed legs) | C: Ponytail-keyed skip test and never-fatal legs (`C:84,87`) | No Ponytail branch in the code, so the legs add no coverage (B R2 #9); C conceded (C R2 #5). Only the `claude`-absent leg is kept (Change 15). |
| X-017 | C: "`claude` is a Node app, so `node` is present" (`C:58`) | Unverified; replaced by A's repo fact (`install_hooks.py:66-68`), C R2 #4. |
| INV-027 | Probe: open the PR as "Refs #330" and close only after Coder confirmation | Orchestrator decision: keep `Closes #330`; the issue asks that the installer and update scripts install Ponytail, which this does. The confirmation lives in the Coder Handoff section (Change 19). |
| INV-028 | Probe: bound the `_find_orca` probe (`install_user_setup.py:190`) in this PR | Orchestrator decision: out of scope; stated as a known limitation and listed as a follow-up (Change 20). |
| INV-026 (second half) | Edit `superclaude update --help` ("Update SuperClaude to latest version", `main.py:342`) | `main.py` stays untouched (FR-006, AC-2). Docs carry the upgrade step instead (Change 11). |
| C-015 | Any `install --list` or `doctor` plugin report | All three agree it is beyond #330; `doctor` runs in `update.sh:10`, so a check there would gate updates (`B:151`). Follow-up (4) in Change 20. |
| INV-007, INV-014, INV-015, INV-018, INV-019, INV-020, INV-021, INV-023 | Probe LOW/MEDIUM items: fork-repo guard, false "already installed" on malformed settings, success line lists skipped plugins, one key per repo, `@` in every key, partial clone after a timeout, `CLAUDE_CONFIG_DIR`, shell-exported mode | Each predates #330 or is LOW with no current instance; none is in the Round 2 consensus or the orchestrator's decision list. Not added, to hold the diff to #330. INV-023 stays an accepted assumption (A-008). |
| C-022 | Version pin for Ponytail | Pin syntax for `claude plugin install` is UNVERIFIED; all three accept marketplace head (R5). The CHANGELOG names the verified version instead (Change 12). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Stale order rationale remains | Restore `B:69` |
| 2 | Low | Budget text stays wrong (X-005) | Restore `B:128,133,221` |
| 3 | Low | NFR conflicts with FR-005 | Restore `B:40` |
| 4 | Low | Rejected options scattered | Restore Design 3.3 |
| 5 | Low | Weaker `off` rationale | Remove inserted sentence |
| 6 | Low | Wrong active-mode cost | Restore `B:108` |
| 7 | Medium | A missed "dormant" claim leaves the spec false (INV-001) | Revert the nine edits; the merge log lists each |
| 8 | Medium | Implementer picks a ledger default without the coordinator | Remove the subsection; keep Change 7 text |
| 9 | Low | Users expect per-session scope | Restore `B:113,140,168` |
| 10 | Low | Wrong path for XDG users | Restore `~/.config` mentions |
| 11 | Medium | Docs disagree with Changes 7-10 and 20 | Restore `B:157-174` and reapply one by one |
| 12 | Low | CHANGELOG style or content drift | Restore `B:176-188` |
| 13 | Low | Missing failure rows | Remove inserted rows |
| 14 | Low | T5 stays green before the fix | Restore `B:200` |
| 15 | Low | `claude`-absent branch untested | Remove T5c |
| 16 | Low | Existing-user proof missing or conflated (INV-017) | Restore `B:198-199` |
| 17 | Low | Assertion location unclear | Remove the sentence |
| 18 | Medium | M checks read as merge gates, or M1b counted without M1c | Restore `B:210,118` |
| 19 | Low | Coder questions incomplete | Restore `B:239-246` |
| 20 | Low | Limitation unstated in PR and docs | Remove the new section and R10 |
| 21 | Medium | Summary contradicts body | Restore `B:9-19` |
| 22 | Low | Probe items missing from risks | Restore `B:216-226` |

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-04T07:43:14Z
- Open item carried into the merge: Change 8 (ledger default) is PENDING a coordinator decision; the merge writes both outcomes and picks neither.
