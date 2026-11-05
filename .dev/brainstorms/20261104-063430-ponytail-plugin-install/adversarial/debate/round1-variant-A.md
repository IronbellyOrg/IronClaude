# Round 1: Variant A advocate (architect, `variant-1-opus-architect.md`)

Lens: maintainability and extension scaffolding. Code claims re-checked 2026-11-04 against `src/superclaude/cli/install_user_setup.py:251-324`, `user_settings_defaults.json:28-50`, `main.py:340-362,400-406`, `update.sh:1-10`, `.dev/codegraph-migration/evidence/P2-layer2.md:357-358,623-624`.

## Position Summary

A's architecture is the right base: Ponytail is data in one defaults file, the plugin step stays generic, and the spec records its decisions (rejected alternatives, extension rule, gate with pass/fail). A is wrong on two code facts (X-003, X-005) and its "zero Python" rule must give way to the label fix. Recommended result: **merge A (structure, decision record, interaction analysis) + B (label fix evidence, existing-user test, docs without a count, migration note) + C (label-pair shape, template-pin handoff item)**.

## Steelman

**B (refactorer).** B is the most correct spec on the code. It found a real, user-visible defect on the exact path Ponytail travels (`install_user_setup.py:303,305` append `args[3]`, which is `--scope` for an install) and proved it with a real log (B:73). Its T4 (B:199) is the only test that proves the issue's "existing user via update" criterion. Removing the plugin count from the docs (B:157-161) removes a drift point for good. Its R1/CHANGELOG migration sentence (B:183,218) protects the one group most likely to notice a silent mode change: existing Ponytail users.

**C (QA).** C is the only variant that tried to give Ponytail, the subject of the issue, priority under a budget that real runs exhaust (C:17, C:56). Its `(label, argv)` pairs (C:37) make the failure label explicit instead of positional. It is the only variant whose Coder note touches the package-upgrade precondition (C:114, U-016), and the only one with a mechanical docs check (`grep -rn "six plugins" docs/`, C:75). It refuses any installer write outside `~/.claude` (NFR-002, C:25).

## Strengths Claimed (A)

1. **Data-only extension model, stated as a rule.** A:7 and A:73 make "the next default plugin is added by data" an explicit design rule; no per-plugin step, registry or hook. Rejected alternative (a) (A:21) names why a dedicated step breaks the single list of default plugins. Verified: `install_plugins` derives market, repo and command from the defaults file alone (`install_user_setup.py:266-284`).
2. **Decision record.** Four lettered rejected alternatives with reasons (A:21), including (b) Ponytail's own `full` and (c) installed-but-disabled. B splits this across sections (B:21, 94-98); C has none (S-002). A future maintainer reads why, not only what.
3. **Per-subagent load quantified (U-002).** A:82 counts IronClaude's existing two SubagentStart blocks (`hooks.json:110-128`) and shows `full` adds a third to every Orca worker and `/sc:*` subagent. This is the strongest architectural reason for `off`, and only A states it.
4. **Statusline nudge tied to installer behaviour.** A:81 links the nudge to the fact that the installer never sets `statusLine`, so it would fire on every new workspace.
5. **User-facing traps documented (U-004).** A:123 is the only docs text saying both that `/ponytail default` has no effect while the env value is set and that deleting the key is not an opt-out (re-added by `:159-161`).
6. **Diff-scope acceptance criterion.** AC-2 (A:150) pins which files may change; B copies the pattern (B:208); C has none (C-023). It stops scope creep on a "small" change.
7. **Gate with explicit pass and fail outcomes (U-001).** A:91 defines what passes (no ruleset, no `.ponytail-active`) and what happens on failure. B's AC-M1 has the pass signal but no failure path; C's check has neither an ID nor a defined outcome (X-015).
8. **`node` dependency grounded in repo fact.** A:103 cites `install_hooks.py:66-68`: IronClaude already needs `node`, so no new prerequisite. C's equivalent claim is unverified (X-017).

## Weaknesses Identified in Others

1. **B, budget reasoning (X-005).** B:221 says the budget "starves the last-listed plugin (Ponytail)". False for the same reason A is: all marketplace adds run before any install (`:271-284`), so the 13 MB Ponytail clone runs before all six installs on a fresh workspace.
2. **B, no failure path for the env check.** AC-M1 (B:210) states a pass signal but not what the spec does if it fails, and B rejects every config-file route (B:97). Now low-impact given `env-propagation-evidence.md`, but the spec has no defined fallback.
3. **B, positional label.** `name = args[3] if args[1] == "marketplace" else args[2]` (B:79) keeps the label coupled to argv positions, the same coupling that caused the bug. One more flag before the plugin id breaks it again.
4. **C, "first" buys little (X-006).** Key order in `extraKnownMarketplaces` has no effect (`:272-279` iterates `wanted`); Ponytail's install still runs after every other missing marketplace add. Reordering also changes the order of six working plugins for a partial gain.
5. **C, "Behaviour today (verified)" is false (X-004).** C:55 says the failure line lists the plugin id today; it contradicts C's own FR-006.
6. **C, unreferenceable artefacts.** Risks have no IDs (S-009); "T7" in Risks is a unit test, not the manual check (X-015); CHANGELOG promises a version it does not name (X-016); CHANGELOG style does not match the file (S-010).
7. **C, unverified `node` claim (X-017).** "`claude` is a Node app" has no repo evidence; Claude Code has a native install.
8. **All three, incl. A: "reruns converge" (A-007).** `P2-layer2.md:357-358,623-624` show two runs where Orca took 25 s and every install was starved both times.

## Concessions

1. **X-003 (A's failure table is false).** A:100 shows a line the code cannot produce. Re-checked: the command-failure path appends bare `--scope` (`:303,305`; live output `P2-layer2.md:624` "--scope, --scope, ..."), and the time-limit path prints `install <id> --scope (time limit)` (`:292`; `P2-layer2.md:358`). A's NFR-001 "zero Python" and AC-2 "no `cli/*.py`" must be dropped. With seven plugins an unnamed failure is a real maintainability defect.
2. **X-005 (A's budget rationale is false).** A:14 and A:71 claim "last" protects the six. It does not: Ponytail's marketplace add is the third command, ahead of every install. A's T-1 order assertion (A:141, U-003) pins a rationale that is wrong and should be removed.
3. **C-008.** "Seven plugins" (A:121) will drift on the next plugin; B's count-free sentence is better and fits A's own extension rule.
4. **U-006 / C-021.** A has no existing-user test and no migration note; B's T4 and R1 sentence should be adopted.
5. **C-013.** With the env evidence, A's installer write to `~/.config/ponytail/config.json` is no longer worth a code path outside `~/.claude`.

## Positions on diff points

| ID | Preferred | One-line reason |
|---|---|---|
| C-002 / X-001 order | B | Append last as a stable data convention; drop every budget claim about order, and drop A's T-1 order assertion. |
| X-005 budget ordering | none (concede A and B) | Key order cannot protect anyone, because adds precede installs; the real fix (group add+install per plugin, or split the Orca budget) is a separate backlog issue, not #330. |
| C-005 / X-002 / X-003 label fix | merge C shape + B evidence | Fix it; build `(label, argv)` pairs (C:37) so the label is explicit, not positional; keep B's T5, R8, CHANGELOG "Fixed" entry and add `P2-layer2.md:624` as evidence. |
| C-012 / X-009 env gate | merge A + B | Downgrade to recommended pre-merge confirmation (`env-propagation-evidence.md:9`); keep A's pass/fail wording inside B's AC-M1. |
| C-013 / X-007 fallback | C | If confirmation fails, document `config.json` as a user step and open a follow-up; no installer write outside `~/.claude`. |
| U-006 existing-user test | B | Only direct proof of the existing-user criterion; also catches idempotence. |
| C-008 docs count | B (+ C grep) | Count-free wording; keep C's `grep -rn "six plugins" docs/` as the acceptance check. |
| C-016 Coder handoff | merge B + C | B's three questions plus C's "template installs from the fork, not a pinned older version" (needed by A-001). |
| C-021 migration note | B | Existing Ponytail users with `config.json` `defaultMode` silently lose it to the env value; one CHANGELOG sentence fixes the surprise. |
| U-007 (supporting) | B | "Every `enabledPlugins` market has a `source.repo`" is the extension scaffolding A's rule needs; adopt it. |

## Shared Assumptions

| ID | Response | Reasoning |
|---|---|---|
| A-001 | REJECT | False as stated: `update` re-runs installers for the current package (`main.py:344-345,360`) and `update.sh:7` runs `pipx install --force ./` without `git pull`; docs and CHANGELOG must say "upgrade the package, then `superclaude update`". |
| A-002 | QUALIFY | The six existing plugins already reach this state (`P2-layer2.md:358`) and Claude Code installs enabled plugins in the background (`assumption-evidence.md:19`); low risk, record as UNVERIFIED, no spec change. |
| A-003 | QUALIFY | Weakly supported (`marketplaces/ponytail/` path in `source.md:213`) and the two existing marketplaces rely on the same rule; the manual check must assert a second install reports `already installed` with no re-add. |
| A-004 | QUALIFY | No `userConfig` field is required (`assumption-evidence.md:14`) and `-y` is passed; whether closed stdin prompts is UNVERIFIED, so the manual check covers it and a hang is bounded by the budget. |
| A-005 | ACCEPT | Skills do not read the mode; only hook scripts do (`assumption-evidence.md:7-9`). |
| A-006 | QUALIFY | No output on ordinary prompts is stated upstream; activation phrases ("stop ponytail"/"normal mode" only turn it off, A:83) and per-prompt `node` cost are unmeasured; note in docs, no gate. |
| A-007 | REJECT | Contradicted twice (`P2-layer2.md:357-358,623-624`): when Orca takes 25 s, every run starves the installs; specs must drop "reruns converge" and file a backlog issue on the shared budget. |
| A-008 | QUALIFY | A shell-exported value may win over settings `env` (order UNVERIFIED); a user who exports it chose it, so document, do not code. |
| A-009 | QUALIFY | A missing `node` gives a non-zero exit, which should not block; a hang up to the 15 s hook timeout per prompt is possible but unobserved; keep as a documented risk. |
