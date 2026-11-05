# Debate Round 1: Variant B (refactorer, Sonnet)

Evidence checked this round against `src/superclaude/cli/install_user_setup.py:251-311`, `update.sh:1-12`, `main.py:340-405`, `user_settings_defaults.json:28-47`, `installation.md:353-360`.

## Position Summary

Merge, with B as the base: the defaults-file change plus the 4-line label fix, B's existing-user test (T4) and migration note, and A's pass/fail wording for the env check, kept as a non-blocking confirmation. B's two real errors (budget wording, no fallback) are fixable in text without changing the design. A's "zero Python" rule is the one position the code refutes outright.

## Steelman

**A (architect).** A has the cleanest structural argument: the plugin step is data-driven, so adding a default plugin should be data only, and "a code change is a spec deviation to report" (A:37) is a strong guard against scope creep. A has the best interaction table (A:79-85): it counts the per-subagent load (two IronClaude blocks already, `hooks.json:110-128`), names the `/ponytail default` shadowing trap (A:113), and gives a concrete pass/fail for the env check (A:91). Its docs paragraph (A:123) is the most complete user-facing text.

**C (QA).** C is the only variant that sees the label defect (FR-006, C:22) and the package-upgrade precondition (C:114) together, and it explains why the tests never caught the defect (they assert only the prefix). T7 (never fatal under three conditions, C:87) and T4 (skip when installed, C:84) are cheap regression nets. "Confirm the template installs superclaude from the fork, not a pinned older version" is the only handoff question that matches A-001. The `grep -rn "six plugins" docs/` acceptance (C:75) is mechanical and checkable.

## Strengths Claimed

1. **Found and proved the label defect with a real log.** B cites the argv shape and `P2-layer2.md:358` (B:73). Verified: `install_user_setup.py:281` builds `[..., p, "--scope", "user", "-y"]`; `:292`, `:303`, `:305` read `args[3]`, which is `--scope` for installs. With seven plugins an unnamed failure is unactionable.
2. **Smallest correct fix.** B's shape (B:77-92) is one added line and three changed lines, keeps `ok` always True, and keeps existing assertions green (`tests/cli/test_install_user_setup.py:240,242`). C's `(label, argv)` restructure (C:37) rebuilds the whole `commands` list for the same result.
3. **Diff-scope acceptance criterion.** AC-2 (B:208) caps the Python change at 5 lines and forbids `update.sh`, `main.py`, `doctor.py`. A's scope AC is unsatisfiable (Weakness 1); C has none (C-023).
4. **Existing-user proof (U-006).** T4 (B:199) starts from settings with the old six plugins, shows the three new keys arrive, and a second run is a no-op. It is the only test that proves the issue's "every existing workspace" outcome at the settings level.
5. **Drift-proof docs.** Dropping the count (B:157-161) removes the hazard at `installation.md:354` ("six plugins", verified). A's and C's "seven" recreate it at the next add.
6. **Future-add guard.** T1's invariant (every `enabledPlugins` marketplace has a `source.repo`, B:196) holds today: `claude-plugins-official` and `understand-anything` cover all six (`user_settings_defaults.json:28-47`). It protects the data-only path A and C both rely on.
7. **Migration note (U-008).** B alone says the env default overrides an existing `~/.config/ponytail/config.json` `defaultMode` and gives the CHANGELOG sentence (B:183, R1 B:218).
8. **Rejected-options discipline.** Design 3.3 (B:94-98) states why no `install_ponytail()`, no config-file write, no `node` pre-check.

## Weaknesses Identified in Others

1. **A: NFR-001 "zero Python" is refuted by the code (X-002, X-003).** A's Failure table shows offline printing `not installed: DietrichGebert/ponytail, ponytail@ponytail` as existing behaviour (A:100). Verified `:303,:305`: it prints `DietrichGebert/ponytail, --scope`. AC-2 (A:150) then forbids the fix.
2. **A: T-1 pins "last key" (A:141, U-003).** It pins an order whose purpose ("cannot starve the six", A:14, A:71) is false: `:271-284` queues every marketplace add before any install (X-005). A test encoding a false rationale is future debt.
3. **A: blocking V-1 plus a code fallback (A:91).** The fallback needs an NFR-001 waiver, a new write outside `~/.claude`, and Ponytail's private path rules, to cover a case `env-propagation-evidence.md:5-9` documents as unlikely. It is the highest-complexity item in any variant for the lowest-probability event.
4. **A: "seven plugins" (A:121)** keeps the drift-prone count (C-008).
5. **C: "first" ordering (C:17, C:33; X-001, X-006).** It reorders six working plugins. Key order in `extraKnownMarketplaces` does nothing (`:272-279` follows `wanted`), and Ponytail's install still follows every missing add, so "wins contention" (C:56) is mostly void.
6. **C: false "verified" row (X-004).** "Behaviour today (verified)" says the plugin id is reported (C:52, C:55); that contradicts C's own FR-006 and `:303`.
7. **C: hygiene gaps.** No line budget or diff-scope AC (C-007, C-023); CHANGELOG as an inline string that does not match the file's `###`/`####` style (S-010); Risks have no IDs and "T7" names a unit test while meaning the manual check (X-015); no migration note (C-021); no existing-user test; "claude is a Node app so node is present" is unverified (X-017).

## Concessions

- **R4 and the Failure row are partly wrong (X-005).** B:221 says the last-listed plugin is the one starved. Verified `:271-284`: the 13 MB Ponytail clone is queued ahead of all six installs on a fresh workspace, so it can starve the six existing installs. This is a real cost of the feature, not only a risk to Ponytail. Fix the wording; the mitigation (non-fatal, named, rerun) is unchanged. The rerun story is also weaker than B claimed because Orca may spend 25 s every run (A-007, `P2-layer2.md:357-358`).
- **No fallback if env does not reach the hook (X-007).** B says only UNVERIFIED and rejects config-file writes (B:97). B must say what happens if AC-M1 fails.
- **X-008.** B:108 says the tracker re-injects each prompt in active modes; A:83 says that is Qoder-only. B did not re-read the upstream file. It does not affect the `off` default; soften the cell to UNVERIFIED.
- **"Reordering rejected" (B:69)** is the right minimal-risk call but was argued as if order mattered for budget. It does not.
- B's `(time limit)` string drops the "install"/"marketplace add" verb (B:82). Cosmetic; tests keep `"time limit" in message`.

## Positions on diff points

| ID | Preferred | One-line reason |
|---|---|---|
| C-002 / X-001 plugin order | B (append last), rationale corrected | Order is not a budget lever (adds precede installs, `:271-284`); do not reorder six working plugins; do not pin order in a test (drop A's U-003). |
| C-005 / X-002 / X-003 label fix | B, plus C's test T5 | Defect is real at `:292,303,305`; 4-line fix; correct A's NFR-001 and Failure row. |
| C-012 / X-009 env gate | B's AC-M1, non-blocking | Docs and a live subprocess observation exist (`env-propagation-evidence.md:5-9`); record a throwaway-HOME check in the PR. Use A's V-1 pass/fail text. |
| C-013 / X-007 fallback | Merge C + A's trigger | No installer write. Document `config.json {"defaultMode":"off"}` as the user-level fallback; if the check fails, hold the merge and open a follow-up. Reject A's code fallback. |
| X-005 budget ordering | Neither A nor B as written | Correct text: the clone is third in the queue, ahead of the installs; mitigation is non-fatal plus rerun. No code change. |
| U-006 existing-user test | B (T4) | Directly proves the success criterion. |
| C-008 docs count | B | No count to drift; C's `grep "six plugins" docs/` acceptance still passes. |
| C-016 Coder handoff | Merge B + C | B's three questions plus C's "installs from the fork / current version" question; PR description only, not blocking. |
| C-021 migration note | B | Only B covers an existing Ponytail user whose `config.json` default is overridden; one CHANGELOG sentence. |

## Shared Assumptions

| ID | Response | Reasoning |
|---|---|---|
| A-001 | ACCEPT as a real gap | Verified `update.sh:7` is `pipx install --force ./` from the local checkout with no pull, and `main.py:340-345` says "to match the current package version"; add one docs/CHANGELOG sentence, no code. |
| A-002 | QUALIFY | The six existing plugins already reach enabled-but-uninstalled and Claude Code installs plugins in the background (`assumption-evidence.md:17-20`); inherited behaviour, mark UNVERIFIED in Failure Behaviour. |
| A-003 | QUALIFY | Upstream manifest name is `ponytail` and the other marketplaces rely on the same key logic (`:273,277`); worst case is a re-queued add each run, so confirm the `known_marketplaces.json` key in the throwaway-HOME run. |
| A-004 | QUALIFY | No `userConfig` field is required (`assumption-evidence.md:14`), so a missing value cannot fail validation; whether `-y` with closed stdin prompts is unverified, so check it in the same manual run. |
| A-005 | ACCEPT | `ponytail-review` and `ponytail-audit` do not read the mode; only the hook scripts do (`assumption-evidence.md:7-9`). |
| A-006 | QUALIFY | `/ponytail` commands are the only documented triggers; per-prompt `node` start cost is unmeasured and low impact; soften B:108 per X-008. |
| A-007 | QUALIFY | Reruns converge only when Orca does not consume the budget every run; `P2-layer2.md:357-358` shows it can. Say "usually converges" and keep Coder question 3. |
| A-008 | ACCEPT | A shell-exported value winning over the settings value is an ordinary user choice; one docs clause, no code. |
| A-009 | QUALIFY | Missing `node` (exit 127) is likely noise only, but a UserPromptSubmit hang could cost up to 15 s per prompt; record it as a risk next to the Coder `node` question, no new check. |
