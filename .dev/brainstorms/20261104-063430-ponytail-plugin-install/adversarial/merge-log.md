# Merge Execution Log

## Metadata
- Base: Variant B (sonnet:refactorer), `adversarial/variant-2-sonnet-refactorer.md`
- Incorporated: Variant A (opus:architect), Variant C (haiku:qa), orchestrator decisions on `adversarial/invariant-probe.md`
- Plan: `adversarial/refactor-plan.md` (22 changes, auto-approved 2026-11-04T07:43:14Z)
- Output: `adversarial/merged-output.md` (base copied, then every change applied with Edit in plan order)
- Executor: merge-executor agent
- Changes applied: 22 of 22 planned
- Status: success (Change 8 kept as an explicit OPEN DECISION, both outcomes written, none picked)
- Timestamp: 2026-11-04T07:51:51Z

Line citations `B:n` refer to the base variant. Code claims kept in the merged spec were re-read in this worktree: `src/superclaude/cli/install_user_setup.py` (lines 31-36, 137-172, 175-240, 251-324), `user_settings_defaults.json` (1-50), `install_hooks.py:66-68`, `hooks/hooks.json:110-128`, `main.py:233,342,404`, `update.sh:7-10`, `tests/cli/test_install_user_setup.py:73-98,175-242`, `tests/cli/test_update_command.py` (install_user_setup at 24-48, 253-289), `tests/unit/test_cli_install.py` (exists), `CHANGELOG.md:5,11-13`, `docs/getting-started/installation.md:345,353-360`, `.dev/codegraph-migration/evidence/P2-layer2.md:357,358,623`, `enrichment/assumption-evidence.md:19-20`, `enrichment/env-propagation-evidence.md:9`. Upstream Ponytail line numbers were not re-read (no network use); they are carried from `invariant-probe.md`.

## Changes Applied

### Change 1: Order is a diff-hygiene convention, not a budget lever
- **Status**: Applied
- **Source**: Round 2 consensus (A R2 R-3, B R2 Final C-002, C R2 #1)
- **Target**: Base, Design 3.1 "Order" bullet (B:69)
- **Before**: "appended last. Reordering for time-budget priority is rejected ... retried by rerunning (`:309`)"
- **After**: appended last as a diff-hygiene convention; order is not a budget lever because every missing marketplace add runs before any install (`:271-284`, verified); no test pins the order; T1 must not assert key order
- **Provenance tag**: `<!-- Source: Base (original, modified) — "Order" bullet per Change #1 ... -->` on 3.1
- **Validation**: Structural integrity ✅ | References ✅ (T1 resolves) | Contradictions ✅

### Change 2: Correct the budget wording
- **Status**: Applied
- **Source**: B R2 #1; A R2 N1, N4; C R2 N3
- **Target**: Base, Failure row "30 s shared budget spent" (B:128), "Clone size" paragraph (B:133), Risk R4 (B:221)
- **Before**: "rerun resumes where it stopped"; "so it is not an outlier next to the two existing marketplaces"; R4 "starves the last-listed plugin (Ponytail, Orca runs first)"
- **After**: "a rerun resumes where it stopped while some run leaves budget"; outlier clause deleted, measured size kept; R4 = plan text verbatim, pointing to Known Limitations and Follow-ups. R4 Impact cell aligned to "a rerun resumes while some run leaves budget" (consistency with the new wording)
- **Provenance tag**: Failure Behaviour and Risks section tags cite Change #2
- **Validation**: Structural ✅ | References ✅ | Contradictions ✅ ("last-listed" and "not an outlier": 0 hits)

### Change 3: NFR-003 states A's replacement rule
- **Status**: Applied
- **Source**: Variant A, Round 2 R-2 (adopted by B and C in R2)
- **Target**: Base, NFR-003 (B:40)
- **Before**: "Net diff target: 3 JSON entries, about 4 changed Python lines, tests, 2 doc files. ..."
- **After**: plan text verbatim (data-only plugins; code only for shared-path defects pinned by a test and named in AC-2; FR-005 the only one, at most 5 Python lines; no new module/constant/flag/option)
- **Provenance tag**: `<!-- Source: Base (original, modified) — NFR-003: Variant A (opus:architect), Round 2 R-2 ... Change #3 ... -->`
- **Validation**: Structural ✅ | References ✅ (AC-2, FR-005) | Contradictions ✅ (agrees with FR-005, AC-2 "at most 5 changed lines")

### Change 4: Rejected-alternatives record
- **Status**: Applied
- **Source**: Variant A Decision Summary (A:21); B R2 #7
- **Target**: Base, Design 3.3 (B:94-98)
- **Before**: three unlettered bullets (dedicated step, config.json, node pre-check)
- **After**: lettered list (a)-(g): dedicated step; Ponytail's `full`; installed but disabled; installer writes `config.json` (XDG path per Change 10, user step if M1b fails); `node` pre-check (A's repo fact `install_hooks.py:66-68` replaces the UNVERIFIED playwright claim); reordering for budget; merge-blocking env gate. Section refs use spec sections (3.1 "Order", AC-M1), not plan change numbers
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Decision Summary rejected alternatives (A:21) + Base 3.3 (B:96-98) — merged per Change #4 ... -->`
- **Validation**: Structural ✅ | References ✅ (R2, M1b, AC-M1, 3.1) | Contradictions ✅

### Change 5: Per-subagent count
- **Status**: Applied
- **Source**: Variant A Interaction table (A:82); B R2 #8
- **Target**: Base, "Why `off`" paragraph (B:21) and Interaction bullet "Orca workers / subagents" (B:117)
- **Before**: no count of existing subagent injections
- **After**: sentence inserted after the first sentence of "Why `off`" and at the start of the Orca workers bullet: two existing SubagentStart blocks (`freshness-subagent-start.sh`, `pragmatic-subagent.js`, `src/superclaude/hooks/hooks.json:110-128`, verified); a non-`off` mode adds a third
- **Provenance tag**: Decision Summary tag ("Why off" paragraph per Change #5) and Interaction tag (Orca workers bullet per Change #5)
- **Validation**: Structural ✅ | References ✅ | Contradictions ✅

### Change 6: Correct the UserPromptSubmit cell
- **Status**: Applied
- **Source**: Variant A (A:83); B R2 #5
- **Target**: Base, Interaction table, UserPromptSubmit active-mode cell (B:108)
- **Before**: "Re-injects the ruleset each prompt while mode is active"
- **After**: plan text (emits only for `/ponytail ...` and deactivation phrases on Claude Code; per-prompt re-injection is Qoder-only; no phrase switches the mode on). The debate citation "(B R2 N5)" was left in the provenance tag, not the spec body. `off` cell unchanged
- **Provenance tag**: Interaction tag ("UserPromptSubmit row: Variant A, Interaction table (A:83) per Change #6")
- **Validation**: Structural ✅ (table column count unchanged) | References ✅ | Contradictions ✅

### Change 7: Real `off` footprint replaces every "dormant / nothing is added" claim (INV-001)
- **Status**: Applied (nine places, each listed)
- **Source**: `invariant-probe.md` INV-001 (upstream `band/register.tsx`); A R-4 (A:162); C (C:48)
- **Target / Before / After** per occurrence:
  1. Decision Summary row 3 (B:13): "no rules, map, nudge or per-subagent injection" -> no ruleset, codebase map, statusline offer or subagent context; band module still runs (band, `git grep`, Edit/Write watch, ledger row), pointer to "`off` footprint".
  2. "Why `off`" (B:21): added "`off` is not silent: Ponytail's band module keeps running in every session".
  3. NFR-006 (B:43): "no injected context (mode `off`)" -> "no injected ruleset in mode `off`, and the band module's footprint".
  4. Interaction Band row (B:109): "UNVERIFIED end to end" dropped; INV-001's upstream lines cited (`:95-103`, `:86-91`, `:201-222`, `:254-290`, `:154-163`, `:292-349`). New paragraph "**`off` footprint.**" after the table carries the full plan wording and the two controls (`/ponytail band off`, `ledger` userConfig `false`).
  5. Opt-out item 3 (B:141): UNVERIFIED wording replaced by the two controls and a pointer to 3.1a; "to stop the band module entirely, use opt-out 1".
  6. Docs block (B:165-171): "nothing is added to your sessions" replaced (later restructured by Change 11).
  7. CHANGELOG Added (B:183): "adds no rules, codebase map or statusline prompt" replaced (later restructured by Change 12).
  8. R6 (B:223): probability Med -> High; full footprint; both controls; opt-out 1 stops all of it.
  9. R7 (B:224): risk text kept; mitigation now names what `off` still does.
- **Provenance tag**: Decision Summary, Requirements, Interaction, Opt-out, Docs and CHANGELOG, Risks tags each cite Change #7
- **Validation**: Structural ✅ | References ✅ (3.1a, opt-out 1, "`off` footprint" x6 resolve) | Contradictions ✅ ("dormant" 0 hits, "nothing is added" 0 hits, "no injected context" 0 hits)

### Change 8: Ledger default, OPEN DECISION pending coordinator (INV-001)
- **Status**: Applied as an explicit Open Decision; no outcome picked
- **Source**: Orchestrator instruction on INV-001
- **Target**: Base, new subsection after Design 3.1
- **Before**: [Section did not exist]
- **After**: `### 3.1a Open Decision: ledger default` with "Status: PENDING coordinator decision. The implementer must not pick."; Outcome 1 (defaults gain `pluginConfigs["ponytail@ponytail"].options.ledger = false`, top-level fill only when absent, T1 asserts it, docs/CHANGELOG say off and how to re-enable, M1c records a ledger row, UNVERIFIED until then); Outcome 2 (no defaults entry, docs/CHANGELOG say on and how to turn off); footprint wording holds for both. Consistency additions so neither outcome contradicts the body: (a) the fill-only-when-absent claim is backed by verified code (`pluginConfigs` is not in `_NESTED_KEYS`, `install_user_setup.py:36,162-164`); (b) a note that under Outcome 1 only, the defaults change is four entries (FR-001..FR-003, NFR-006); (c) Out of Scope's "setting plugin `userConfig`" line gains "except the ledger default if 3.1a picks outcome 1"; (d) the docs and CHANGELOG blocks carry a `<LEDGER SENTENCE ...>` placeholder holding both outcome texts
- **Provenance tag**: `<!-- Source: Orchestrator instruction on invariant-probe.md INV-001 — merged per Change #8 (new subsection; OPEN DECISION, both outcomes kept, none picked) -->`
- **Validation**: Structural ✅ (H3 under Design, between 3.1 and 3.2) | References ✅ ("3.1a" x10 resolve) | Contradictions ✅ (Out of Scope and entry counts reconciled)

### Change 9: `/ponytail` mode is shared per repo (INV-002)
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-002
- **Target**: Base, Interaction "Pragmatic ladder" (B:113), Opt-out item 2 (B:140), docs block (B:168)
- **Before**: "opt in per session (`/ponytail` ...)", "For one session, type `/ponytail`", "Type `/ponytail` for one session"
- **After**: plan wording in all three (every session in that repo; a new `off` session switches it back off; every subagent of every session gets the ruleset while on; bare `/ponytail` -> `full`), with upstream line cites in the Interaction bullet
- **Provenance tag**: Interaction and Opt-out tags cite Change #9
- **Validation**: Structural ✅ | References ✅ | Contradictions ✅ ("one session"/"per session" remaining hits are R11 and the doctrine-duplication sentence, both correct)

### Change 10: `$XDG_CONFIG_HOME` path for Ponytail's files (INV-006)
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-006
- **Target**: B:97 (via Change 4 item (d)), B:142 (Opt-out item 4), CHANGELOG migration (B:183), R1 (B:218), R6 (B:223, via Change 7), M1b fallback (via Change 18), Out of Scope (B:233)
- **Before**: `~/.config/ponytail/...` only
- **After**: `$XDG_CONFIG_HOME/ponytail/...` (or `~/.config/ponytail/...` when `XDG_CONFIG_HOME` is unset) at first mention in each section
- **Provenance tag**: 3.3, Opt-out, Risks, Out of Scope tags cite Change #10
- **Validation**: Structural ✅ | References ✅ | Contradictions ✅ (every `~/.config/ponytail` mention is now paired with the XDG form)

### Change 11: Docs block rewrite
- **Status**: Applied
- **Source**: Base docs block (B:159-172) + Variant A (A:123) + A R2 N7 + B R2 #6 + Variant C (C:73,75) + A-001 + INV-026
- **Target**: Base, `installation.md` block (B:157-174)
- **Before**: one count-free paragraph + one Ponytail paragraph ("nothing is added", "for one session", opt-out without user-settings precedence or "do not delete the key")
- **After**: items in plan order: (1) count-free plugin sentence unchanged; (2) what Ponytail adds, `off` default, real footprint, `/ponytail band off`, ledger placeholder with both outcome texts; per-repo mode; (3) env overrides `/ponytail default <mode>`, which prints "PONYTAIL DEFAULT SET"; (4) opt-out in user settings, project settings win, do not delete the key; (5) upgrade step (`git pull` before `./update.sh`, then `superclaude update`/`install`); (6) `node`, already needed by IronClaude's SubagentStart hook; (7) Known Limitation verbatim. One line after the block says the ledger sentence is the only open text. AC-1 gains `grep -rn "six plugins" docs/` returns nothing (verified: today the only hit is `installation.md:354`)
- **Provenance tag**: `<!-- Source: Base (original, modified) — installation.md block: Base B:159-172 + Variant A docs paragraph (A:123) + Variant C (C:73,75) — merged per Change #11 ... -->`
- **Validation**: Structural ✅ | References ✅ (3.1a) | Contradictions ✅ (agrees with Changes 7-10 and 20; limitation text identical to Known Limitations)

### Change 12: CHANGELOG block (Added + Fixed + migration)
- **Status**: Applied
- **Source**: Base CHANGELOG (B:178-188) + B R2 N4 + C R2 #3 + A-001 + Changes 7, 8, 10
- **Target**: Base, CHANGELOG block (B:176-188)
- **Before**: Added entry with "adds no rules ..." and "set to the same value" migration
- **After**: structure kept (`### Ponytail plugin installed by default (#330)` / `#### Added (default plugins)` / `#### Fixed (plugin install report)`, matches `CHANGELOG.md:11-13`, verified). Added entry: install/update/`update.sh`, verified v5.3.3, `off` when unset, footprint, ledger placeholder with both outcomes, opt out in user settings and do not delete the key, upgrade-then-update, `node`. Migration bullet: plan text verbatim with the XDG path. Fixed entry unchanged
- **Provenance tag**: Docs and CHANGELOG tag ("CHANGELOG block per Change #12")
- **Validation**: Structural ✅ (fenced; inner headings are inside the code fence) | References ✅ | Contradictions ✅

### Change 13: Failure Behaviour additions
- **Status**: Applied
- **Source**: Variant A (A:103-104); C R2 N4; INV-024, INV-025
- **Target**: Base, Failure Behaviour table (B:124-131)
- **Before**: six rows; `node` row said display UNVERIFIED
- **After**: `node` row now carries A's repo fact (`install_hooks.py:66-68`, verified) and INV-025 (upstream force-exit within 1 s; `"verbose": true` at `user_settings_defaults.json:6`, verified). Two rows inserted at the end: "Enabled in settings but not installed" (background install, `assumption-evidence.md:19`, UNVERIFIED) and "Marketplace keyed other than `ponytail`" (re-queued add, `:277-279`; success line at `:306-311`; caught only by M1a). Citation note: the plan said `:19`/`:17` for the background-install evidence; the line holding it is `:19`, used in both places. The plan's `:307-311` was widened to `:306-311` (the `if failed` branch starts at 306; the success line is 311)
- **Provenance tag**: Failure Behaviour tag ("`node` row and two new rows: Variant A, Failure Behaviour (A:103-104) per Change #13")
- **Validation**: Structural ✅ (3 columns per row) | References ✅ (M1a) | Contradictions ✅ (see R3 alignment below)

### Change 14: T5 asserts the plugin id present and `--scope` absent on both paths
- **Status**: Applied
- **Source**: Base T5 (B:200) + B R2 N3 + A R2 N2 + C R2 #8, N2
- **Target**: Base, Tests row T5 (B:200)
- **Before**: Ponytail-enabled fixture; asserted the name and not `--scope`
- **After**: extend the existing `playwright`-only fixture; both legs assert `ok is True`, `anthropics/claude-plugins-official`, `playwright@claude-plugins-official`, `"--scope" not in message`; time-limit leg also `(time limit)`. Added one verified sentence: before the fix both legs fail on `--scope` (`:292,303,305`) and today's assertions (`:240,242`) pass either way. Checked against the code: the non-zero leg today prints `anthropics/claude-plugins-official, --scope`; the time-limit leg prints `marketplace add anthropics/claude-plugins-official (time limit), install playwright@claude-plugins-official --scope (time limit)`
- **Provenance tag**: Tests tag ("T5 per Change #14")
- **Validation**: Structural ✅ | References ✅ (FR-005, NFR-001) | Contradictions ✅

### Change 15: `claude`-absent test leg
- **Status**: Applied
- **Source**: C R2 N1; B R2 #9
- **Target**: Base, Tests table (new row T5c after T5) and Failure row "No `claude` CLI" (B:126)
- **Before**: [Row did not exist]; failure row had no test pointer
- **After**: T5c row (monkeypatch `setup.shutil.which` -> `None`; assert the exact tuple with two spaces after the emoji, verified at `install_user_setup.py:258`; branch untested today, `which` patched at `test:195,222,233`, verified). Failure row appended "Pinned by T5c." AC-1 updated to "T1..T5 and T5c" so the acceptance list covers the new row
- **Provenance tag**: Tests tag ("T5c: Variant C (C R2 N1) per Change #15"); Failure Behaviour tag cites Change #15
- **Validation**: Structural ✅ | References ✅ (T5c x5) | Contradictions ✅

### Change 16: Existing-user test as an extension of the fill test (INV-017)
- **Status**: Applied
- **Source**: Base T3, T4 (B:198-199); A R2 N5; B R2 Final U-006; C R2; INV-017
- **Target**: Base, Tests rows T3 and T4 (B:198-199)
- **Before**: T3 = extend fill test with user values; T4 = new `test_existing_user_gets_ponytail_on_update`
- **After**: one row "T3/T4": extend `test_settings_defaults_fill_only_missing_values` (`:73-98`, verified; base said 73-99) with Leg 1 (existing user, keys arrive, second run `already present`) and Leg 2 (user `False` and `full` kept). Dependent references updated: Opt-out paragraph test range `:73-99` -> `:73-98` and "FR tests below" -> "T3/T4 below"; update-path paragraph "T4 covers" -> "T3/T4 leg 1 covers"
- **Provenance tag**: Tests tag ("T3/T4 per Change #16 (INV-017)"); Opt-out tag ("test range per Change #16")
- **Validation**: Structural ✅ | References ✅ | Contradictions ✅

### Change 17: Install test assertions
- **Status**: Applied
- **Source**: Base T2 (B:197); A R2 N5
- **Target**: Base, Tests row T2
- **Before**: two assertions, no location
- **After**: appended "Both assertions go next to the existing assertions at `test_install_user_setup.py:205`; the test already iterates every default, so no fixture change" (verified: `:186` iterates every default, `:205` is the Understand-Anything add assertion)
- **Provenance tag**: Tests tag ("T2 per Change #17")
- **Validation**: Structural ✅ | References ✅ | Contradictions ✅

### Change 18: Manual checks M1a / M1b / M1c, non-blocking
- **Status**: Applied
- **Source**: Base AC-M1 (B:210) + B R2 #2, #3 + A V-1 (A:91) + C R2 N4 + INV-009, INV-010, INV-029
- **Target**: Base, AC-M1 (B:210) and Interaction "Environment" bullet (B:118)
- **Before**: one AC-M1 item mixing install mechanics and env propagation, described as proving env before merge; Environment bullet UNVERIFIED
- **After**: AC-M1 (manual, non-blocking) with M1a (install mechanics, fail outcome), M1b (env reaches the hook, counts only if M1c passed, fail outcome = documented XDG `config.json` user step + follow-up issue, installer never writes outside `~/.claude`), M1c (positive control; UNVERIFIED if no session can start; ledger row recorded if 3.1a picks outcome 1). Each item says "non-blocking". Environment bullet points to `enrichment/env-propagation-evidence.md` and M1b. Item names kept as "M1a/M1b/M1c" under AC-M1, matching every other reference. The base's "`settings.json` has the three keys" check was not carried into M1a because the plan's M1a list omits it; T1 and T3/T4 cover it offline
- **Provenance tag**: Tests tag ("AC-M1 M1a/M1b/M1c per Change #18 ..."); Interaction tag ("Environment bullet per Change #18")
- **Validation**: Structural ✅ (nested list under AC-M1) | References ✅ (M1a x5, M1b x7, M1c x6) | Contradictions ✅ (no remaining "proves before merge" wording)

### Change 19: Coder Handoff, merged B + C
- **Status**: Applied
- **Source**: Base Coder Handoff (B:239-246) + Variant C (C:114) + C R2 Final C-016 + INV-027
- **Target**: Base, Coder Handoff (B:239-246)
- **Before**: title "Coder Handoff"; three questions; "Put this in the PR description"; "If answers 1 or 2 ..."
- **After**: title "Coder Handoff (confirmation only; no Coder repo edits, no Orca link flags)"; base intro kept; PR description carries a one-paragraph summary; questions 1-3 kept (3 now names the Orca limitation section); question 4 from C (fork at current version, not a pinned older one); closing "No answer blocks this PR. The PR keeps `Closes #330`. If answer 1, 2 or 4 is 'no', file a handoff issue from `~/.claude/ISSUE-HANDOFF.md`."
- **Provenance tag**: `<!-- Source: Base Coder Handoff (B:239-246) + Variant C (haiku:qa), Coder Handoff (C:114) — merged per Change #19 ... -->`
- **Validation**: Structural ✅ | References ✅ (R3, R4, Known Limitations) | Contradictions ✅ (Decision row 9 matches)

### Change 20: Known limitations and follow-ups
- **Status**: Applied
- **Source**: A R2 N4; B R2 Final X-005; C R2 N3; INV-028, INV-024
- **Target**: Base, new H2 after Risks and before Out of Scope; Risks R10
- **Before**: [Section did not exist]
- **After**: Limitation (verbatim, same text as the docs block); Mechanism (spec only; `install_user_setup.py:190,226,34,35,213-215` and `P2-layer2.md:357,623`, all verified); Follow-ups 1-5. R10 row added after R9
- **Provenance tag**: `<!-- Source: Round 2 consensus ... + invariant-probe.md INV-028 orchestrator decision — merged per Change #20 (new section) -->`
- **Validation**: Structural ✅ (H2 between Risks and Out of Scope) | References ✅ | Contradictions ✅

### Change 21: Decision Summary rows follow the changes
- **Status**: Applied
- **Source**: Changes 1-20
- **Target**: Base, Decision Summary rows 2, 3, 4, 7, 8, 9
- **Before / After**: row 2 + package-upgrade sentence; row 3 already carried the Change 7 wording (applied under Change 7, re-checked here); row 4 now names the current output on both paths (`:303,305` and `:292`, verified; base cited `:292,305`) and the fix; row 7 + user-settings opt-out, do not delete the key, grep empty; row 8 = "T1-T5 plus T5c ...; T3/T4 merged into the extended fill test; no new test file"; row 9 = Coder Handoff section (four questions), PR keeps `Closes #330`
- **Provenance tag**: Decision Summary tag ("rows 2, 4, 7, 8, 9 per Change #21; row 3 per Change #7")
- **Validation**: Structural ✅ | References ✅ | Contradictions ✅ (each row re-checked against its section)

### Change 22: Risk table refresh for the probe items
- **Status**: Applied
- **Source**: INV-002, INV-006, INV-009, INV-024; Changes 7-10, 18, 20
- **Target**: Base, Risks R1, R2, R6; R10 (Change 20); new R11
- **Before**: R1/R2 without XDG path or the success message
- **After**: R1 gains XDG path (Change 10) and "`/ponytail default <mode>` prints success but has no effect"; R2 names the XDG write and "PONYTAIL DEFAULT SET"; R6 per Change 7; R10 per Change 20; R11 (INV-002) inserted after R10. INV-009 handled by M1b's dependency on M1c, not a risk row
- **Provenance tag**: Risks tag ("R1, R2 per Change #22; ... R11 per Change #22 (INV-002)")
- **Validation**: Structural ✅ (5 columns per row) | References ✅ | Contradictions ✅

### Post-merge validation edits (not plan changes)
Made only to clear findings of the contradiction re-scan; each is a wording fix with no new decision:
1. Decision Summary row 6: "showing seven plugins is its own feature" -> "showing all default plugins is its own feature" (count-free rule, C-008/X-010).
2. Visibility: "adding all seven is a feature" -> "adding all of them is a feature" (same rule).
3. Failure row "Offline": "both names are reported by FR-005" -> "After the FR-005 fix both are reported by name (repo and plugin id); today the failed install is reported as `--scope` (`:303`)", so no row implies the current code prints the plugin id.
4. R3 Impact: "Med (noise; display UNVERIFIED)" -> "Med (noise: an error per hook run, see the Failure Behaviour `node` row)", to match the Change 13 row.
5. R4 Mitigation: "Coder handoff check 3" -> "Coder Handoff question 3", so the reference names the target as written.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ One H1; H2 sections; H3 only under Design (3.1, 3.1a, 3.2, 3.3). No level gaps, no orphaned subsections. The `###`/`####` lines in the CHANGELOG block are inside a `text` code fence, not document headings.
- Section ordering: ✅ Decision Summary, Requirements, Design (3.1, 3.1a, 3.2, 3.3), Interaction, Failure Behaviour, Opt-out, Visibility, Docs and CHANGELOG, Tests and AC, Risks, Known Limitations and Follow-ups, Out of Scope, Coder Handoff. 3.1a follows the JSON it modifies; Known Limitations sits after Risks and before Out of Scope as planned.
- Document flow: ✅ Provenance header before the H1; one `<!-- Source: ... -->` tag directly under the H1 and under every H2/H3 that holds content (17 tags; the `## Design` H2 holds only its 3.x subsections, each tagged).

### Internal References
- Total references: 145 occurrences of requirement, test, criterion, check and risk IDs plus named section references (47 distinct targets: FR-001..FR-008, NFR-001..NFR-006, T1, T2, T3/T4, T5, T5c, T6, AC-1..AC-3, AC-M1..AC-M3, M1a..M1c, R1..R11, 3.1a, "`off` footprint", Known Limitations and Follow-ups, Opt-out item 2, opt-out 1, Coder Handoff question 3)
- Resolved: 145
- Broken: 0
- Code citations kept in the spec were re-read in this worktree (list in Metadata); two corrected during the merge: fill test range `:73-99` -> `:73-98`; Decision row 4 `:292,305` -> `:303,305` plus `:292`.

### Contradiction Re-Scan
- New contradictions introduced: 0 (after the five validation edits above)
- Phrase scan of the merged file: "dormant" 0, "nothing is added" 0, "zero Python" 0, "Ponytail first" 0, "seven plugins" 0, "all seven" 0, "last-listed" 0, "not an outlier" 0, "for one session" 0, "display UNVERIFIED" 0, "gating UNVERIFIED" 0.
- Failure rows: every row shows only output the current code can print, or says explicitly that the text is after the FR-005 fix (Offline row; 3.2 "Message becomes"); the time-limit row names no plugin; the marketplace-key row's `✅ Plugins: installed ...` is reachable today (`install_user_setup.py:311`).
- Contradictions found by the scan and fixed: R3 "display UNVERIFIED" vs the Change 13 `node` row; plugin count in Decision row 6 and Visibility; Offline row wording; Out of Scope "no `userConfig`" vs Open Decision outcome 1 (fixed inside Change 8); "three entries" vs outcome 1 (noted inside Change 8).
- Open item (not a contradiction): 3.1a is PENDING the coordinator; the docs and CHANGELOG blocks carry both outcome sentences in a `<LEDGER SENTENCE ...>` placeholder.

## Summary
- Total changes planned: 22
- Successfully applied: 22 (Change 8 applied as an explicit Open Decision with both outcomes; no outcome chosen)
- Failed: 0
- Skipped: 0
- Validation-only wording edits outside the plan: 5 (listed above)
- Post-merge validation: PASS
