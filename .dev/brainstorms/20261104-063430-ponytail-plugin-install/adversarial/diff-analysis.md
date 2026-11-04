# Diff Analysis: Spec Comparison (Ponytail plugin on every workspace, issue #330)

## Metadata

- Generated: 2026-11-04T06:53:18Z
- Variants compared: 3 (A = `variant-1-opus-architect.md`, B = `variant-2-sonnet-refactorer.md`, C = `variant-3-haiku-qa.md`)
- Source: `seed-brief.md`; extra evidence: `enrichment/env-propagation-evidence.md`
- Code checked: `src/superclaude/cli/install_user_setup.py`, `user_settings_defaults.json`, `main.py`, `doctor.py`, `update.sh`, `docs/getting-started/installation.md`, `tests/cli/test_install_user_setup.py`, `tests/cli/test_update_command.py`, `src/superclaude/output-styles/pragmatic.md`, `src/superclaude/hooks/hooks.json`, `install_hooks.py`, `CHANGELOG.md`, `.dev/codegraph-migration/evidence/P2-layer2.md`
- Total differences found: 80
- Categories: structural (13), content (23), contradictions (17), unique (18), shared assumptions promoted (9)
- Taxonomy column: L1 surface, L2 structural, L3 state/guard/boundary

## Structural Differences

Variant A = `variant-1-opus-architect.md`, B = `variant-2-sonnet-refactorer.md`, C = `variant-3-haiku-qa.md`. Level: L1 surface, L2 structural, L3 state/guard/boundary.

| # | Area | Variant A | Variant B | Variant C | Severity | Level |
|---|------|-----------|-----------|-----------|----------|-------|
| S-001 | Header and provenance | Title, persona line, generation date (A:1-3) | Title, persona bias statement, evidence date and UNVERIFIED convention (B:1-4) | Title states the decision; no persona, date or evidence convention (C:1) | Low | L1 |
| S-002 | Decision Summary form | 9-row table plus four lettered rejected alternatives (a)-(d) (A:9-21) | 9-row table plus a "Why `off`" paragraph (B:9-21); rejected options moved to Design 3.3 | Numbered list of 9 with inline rationale; no rejected-alternatives block (C:5-13) | Low | L1 |
| S-003 | Requirements layout | FR-001..007, NFR-001..005 under subheadings (A:25-41) | FR-001..008, NFR-001..006 under subheadings (B:25-43) | FR-001..007, NFR-001..004 in one flat list (C:17-27) | Low | L1 |
| S-004 | Design section | One JSON block, "Why this works with no code" bullets with line cites, extension rule (A:43-73) | Subsections 3.1 JSON, 3.2 Python with illustrative code, 3.3 Considered and rejected (B:46-98) | Four numbered file edits; the Python change is one sentence, no code (C:29-39) | Medium | L2 |
| S-005 | Interaction section | Four-column table (surface, full/lite, off, IronClaude overlap) with upstream line numbers, then gate V-1 (A:75-91) | Two-column mode table, then interaction bullets each with a position (B:101-118) | Bullets only, no table (C:41-48) | Low | L2 |
| S-006 | Failure Behaviour table | Condition / What happens / Evidence, plus "Budget fit" paragraph (A:93-106) | Case / Behaviour / Result, plus "Clone size" paragraph (B:121-133) | Condition / Behaviour today / Change needed (C:50-59) | Low | L2 |
| S-007 | Where the env-to-hook verification gate lives | Named gate V-1 in Interaction, tied to AC-3 and R-1, with Pass and Fail outcomes (A:91, :151, :159) | AC-M1 in Tests, referenced from an Interaction bullet (B:118, :210) | Unnumbered "Manual acceptance" paragraph; the Risks table calls it "T7", but T7 is a unit test (C:87, :89, :97) | Medium | L2 |
| S-008 | Tests and acceptance layout | T-1..T-4 bullets, AC-1..AC-5 (A:139-153) | T1..T6 table with a "Proves" column mapped to FR/NFR; AC-1..3 plus manual AC-M1..M3 (B:194-212) | T1..T7 bullets, manual paragraph, one "Done when" line; no AC IDs (C:79-91) | Medium | L2 |
| S-009 | Risk table | R-1..R-7 with ID, Probability, Impact, Mitigation (A:157-165) | R1..R9, same columns (B:216-226) | Six rows with no IDs, so nothing can reference them (C:95-102) | Low | L1 |
| S-010 | Docs and CHANGELOG detail | Full replacement sentence, full Ponytail paragraph, CHANGELOG block in the file's `###`/`####` style (A:121-133) | Full docs text block; CHANGELOG with Added and Fixed subsections (B:157-188) | Summary bullets; CHANGELOG as one inline string under `### Added —`, which does not match the file's `### <topic>` / `#### <Kind> (<topic>)` style (`CHANGELOG.md:11-13`) (C:73-75) | Medium | L1 |
| S-011 | Coder Handoff | "Not needed" plus one optional note (A:176-178) | Three-question confirmation for the PR description (B:239-246) | One-line handoff on the template's install source (C:112-114) | Low | L1 |
| S-012 | Out of Scope list | 6 items (A:167-174) | 7 items (B:229-236) | 5 items (C:104-110) | Low | L1 |
| S-013 | Evidence sourcing | Repo `file:line` and upstream files with line numbers via `gh api` | Same, plus a real repo log proving the label defect (`.dev/codegraph-migration/evidence/P2-layer2.md:358`) | Repo lines, but in places cites the enrichment notes (`research-light.md:13`, `codebase-context.md:43`) as the evidence | Low | L1 |

## Content Differences

| # | Topic | Variant A | Variant B | Variant C | Severity | Level |
|---|-------|-----------|-----------|-----------|----------|-------|
| C-001 | Where Ponytail is added | Defaults file only: three entries, zero Python (A:11, NFR-001 A:37) | Defaults file (three entries) plus a failure-label fix in `install_plugins` (B:11, FR-005 B:31) | Defaults file (three entries) plus the same label fix (C:5, FR-006 C:22) | Medium | L2 |
| C-002 | Order in `enabledPlugins` | Last, "so it cannot starve the six existing plugins of the 30 s budget" (A:14, :27, :71) | Last, appended; reordering rejected as a behaviour change to six working plugins (B:27, :69) | First, "budget triage: the issue's target installs before the six"; also first in `extraKnownMarketplaces` (C:17, :33) | High | L3 |
| C-003 | Default mode and how it is set | `env.PONYTAIL_DEFAULT_MODE="off"`, filled only when unset; argues `off` over `lite` because every non-off mode runs the nudge and subagent injection (A:13, :29, :87) | Same value and mechanism; argues against `full` for unattended Orca workers and duplicate ladder (B:13, :21, FR-003 B:29) | Same value and mechanism; "QA position: shipping `full` to everyone is an untestable-here behavioural change" (C:7, FR-003 C:19) | Low | L3 |
| C-004 | Change to `superclaude update` / `update.sh` | None; cites `main.py:403-405`, `update.sh:8`, step 7 at `main.py:231-237` (A:12) | None; cites `main.py:404`, `update.sh:8`, `install_user_setup.py:320-322`; FR-006 forbids editing them (B:12, :32) | None; cites `main.py:403-405`, `update.sh:8`, pinned by `test_update_command.py:88-97` (C:6, FR-007 C:23) | Low | L1 |
| C-005 | Fix the existing failure-label bug (`failed.append(args[3])` reports `--scope` for `plugin install`; `install_user_setup.py:292,303,305`) | Not mentioned; its Failure table presents the warning as already naming `ponytail@ponytail` (A:100) | Fixes it (FR-005); cites the real log showing `--scope (time limit)`; CHANGELOG "Fixed" entry; test T5 (B:14, :73, :187, :200) | Fixes it (FR-006); test T5; CHANGELOG mentions it inline (C:22, :85, :74) | High | L3 |
| C-006 | Shape of the label fix | n/a | Compute `name = args[3] if args[1] == "marketplace" else args[2]` per command; about 4 lines (B:77-92) | Restructure `commands` into `(label, argv)` pairs (C:37) | Low | L2 |
| C-007 | Python-change budget | NFR-001: zero Python lines; a needed change is "a spec deviation to report" (A:37); AC-2 forbids any `src/superclaude/cli/*.py` diff (A:150) | NFR-003 about 4 lines; AC-2 caps `install_user_setup.py` at 5 changed lines (B:40, :208) | No line budget; no diff-scope acceptance criterion | Medium | L2 |
| C-008 | Docs plugin count | "seven plugins, including `playwright`, `frontend-design` and `ponytail`" (A:121) | Drop the count so it cannot drift: "listed in its settings defaults (including ...)" (B:7, :160-161) | "seven plugins", with acceptance `grep -rn "six plugins" docs/` empty (C:73, :75) | Medium | L1 |
| C-009 | Docs paragraph content | Skills and `/ponytail`; mode `off`; `/ponytail default` has no effect while the env var is set; `node`; local ledger; opt out with `false`; deleting the key is not opt-out (A:123) | Mode `off`; env var overrides `/ponytail default`; `node`; opt out with `false`. No ledger and no "deleting the key" note in the docs text (B:165-171) | Mode `off`; ledger is Ponytail's default and not mode-gated, pointer to its README; `node`. No note that `/ponytail default` is ignored (C:73) | Medium | L1 |
| C-010 | CHANGELOG | One Added entry under `### Installer: Ponytail plugin ... (#330)` (A:127-133) | Added entry plus migration sentence for existing Ponytail users with `config.json`, plus a Fixed entry for the label (B:178-188) | One inline Added string, including the label fix (C:74) | Medium | L1 |
| C-011 | Tests | T-1 defaults incl. "last key" order; T-2 install calls; T-3 opt-out; T-4 fill/preserve. No label test, no existing-user test (A:141-145) | T1 defaults plus invariant "every `enabledPlugins` market has `source.repo`"; T2 install calls; T3 preserve; T4 existing-user update with idempotent second run; T5 label and time limit; T6 skip unchanged (B:196-201) | T1 defaults; T2 fill/preserve; T3 install calls and opt-out; T4 already-installed skip; T5 labels; T6 update suite; T7 never-fatal under three conditions (C:81-87) | Medium | L2 |
| C-012 | Verification gate: does settings `env` reach plugin hook processes | V-1 must pass before merge in a throwaway HOME: no ruleset and no `.ponytail-active` flag (A:91, AC-3 A:151) | AC-M1 manual check, same pass signal (`~/.claude/.ponytail-active` absent) (B:118, :210) | Manual throwaway-HOME check; Risks call it a check "before merge" (C:89, :97) | High | L3 |
| C-013 | Fallback if the env route fails | Installer writes `{"defaultMode":"off"}` to `~/.config/ponytail/config.json` only when absent, with an NFR-001 waiver (A:21, :91) | None defined; writing `config.json` is rejected in Design 3.3 (B:97) | Document `config.json` as a user step; installer "must still not write that file" (NFR-002) (C:25, :89) | High | L3 |
| C-014 | Opt-out wording | `false` in `enabledPlugins`; deleting the key is not opt-out; files remain; uninstall command not named (UNVERIFIED) (A:110-113) | `false`; do not delete the key; do not only run `claude plugin uninstall`; mode via env; ledger via `/ponytail band off` (B:139-142) | `false`; "rules only" path via mode; ledger via Ponytail's README (C:63-65) | Low | L1 |
| C-015 | `install --list` / `doctor` | No change; plugins are downloaded, not copied; would be a new feature (A:117) | No change; adds that `update.sh:10` runs `doctor`, so a plugin check would gate updates; backlog suggestion (B:150-153) | No change; a FAIL in doctor would contradict never-fatal (C:69) | Low | L1 |
| C-016 | Coder handoff | Not needed; optional `node` note (A:178) | Confirmation in the PR description: does the template run install/update, are `claude` and `node` on PATH, is there 60 s headroom (B:240-246) | Confirm the template installs `superclaude` from the fork, not a pinned older version (C:114) | Medium | L1 |
| C-017 | Ledger / band caveat | R-4: probability High, local only; `/ponytail band off`; `userConfig.ledger` not automated; cites `register.tsx:154-163` (A:84, :162) | R6: probability Med; gating "UNVERIFIED end to end"; cites `register.tsx:158` (B:109, :223) | "certain when enabled + project detected"; also rebuilds `board.html`; cites `register.tsx:155-167` (C:48, :101) | Low | L3 |
| C-018 | `node` prerequisite | No check; IronClaude's `pragmatic-subagent.js` already needs `node` (A:103, R-7 A:165) | No check, deferred; R3 Low-Med probability, Med impact (B:98, :220) | No check; "the `claude` CLI itself is a Node app, so `claude` present without `node` is unlikely" (C:58) | Low | L3 |
| C-019 | Budget risk analysis | Ponytail "most likely to hit the time limit"; acceptable; budget not raised (A:106) | 13 MB "not an outlier"; Orca may use 25 s first; real run shows budget fully spent (B:128, :133) | Ponytail first "so it wins contention" (C:56, :99) | Medium | L3 |
| C-020 | UserPromptSubmit behaviour in active modes | "per-prompt ruleset injection is Qoder-only" (A:83) | "Re-injects the ruleset each prompt while mode is active" (B:108) | Silent on ordinary prompts; reacts only to `/ponytail ...` (C:45) | Medium | L3 |
| C-021 | Existing Ponytail users (migration) | R-2: `/ponytail default full` silently loses to the env value (A:160) | R1 and R2: the env default also overrides an existing `~/.config/ponytail/config.json` `defaultMode`; CHANGELOG tells them to set the env value (B:183, :218-219) | Not addressed | Medium | L3 |
| C-022 | Supply chain / version pin | R-6: no pin; High impact; pin support UNVERIFIED (A:164) | R5: same; "same trust model as `understand-anything`" (B:222) | Upstream-drift risk Med/Med; CHANGELOG to name the verified version (C:98) | Low | L3 |
| C-023 | Acceptance diff scope | AC-2: only defaults JSON, test file, `installation.md`, `CHANGELOG.md` (A:150) | AC-2: those plus `install_user_setup.py` (at most 5 lines); AC-3 primitive-path grep (B:208-209) | None | Low | L2 |

## Contradictions

Type: CROSS (between variants), INTRA (inside one variant), CODE (variant claim contradicted by the repository).

| # | Type | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact | Level |
|---|------|-------------------|--------------------|--------------------|--------------------|--------|-------|
| X-001 | CROSS | Plugin order | "Ponytail is placed last so it cannot starve the six existing plugins of the 30 s budget" (A:14) | "Order: appended last. Reordering for time-budget priority is rejected" (B:69) | "`\"ponytail@ponytail\": true` in `enabledPlugins`, first in map order (budget triage ...)" (C:17) | High | L3 |
| X-002 | CROSS | Any Python change at all | "**NFR-001** Zero lines of Python change in `src/superclaude/cli/`" (A:37) | "FR-005 The install-failure label ... names the plugin ... This is the only Python change." (B:31) | "**FR-006** Fix the pre-existing failure-label defect" (C:22) | High | L2 |
| X-003 | CODE | What the failure warning prints today | Offline row: "line `⚠️  Plugins: not installed: DietrichGebert/ponytail, ponytail@ponytail`", under "All rows are existing behaviour of `install_plugins`; the spec adds no handling" (A:95, :100). **False:** an install argv is `["plugin","install",p,"--scope","user","-y"]` (`install_user_setup.py:281`) and failures append `args[3]` (`:303`, `:305`), so today's line reads `DietrichGebert/ponytail, --scope`. The real log at `.dev/codegraph-migration/evidence/P2-layer2.md:358` shows `install frontend-design@claude-plugins-official --scope (time limit)`. | Correct: "`args[3]` is `\"--scope\"`" (B:73) | Correct in FR-006 (C:22) | High | L3 |
| X-004 | CODE + INTRA | C's "today" failure row | — | — | Failure table header "Behaviour today (verified)", row "Offline / non-zero exit: plugin id listed in `⚠️  Plugins: not installed: ...`" (C:52, :55). **False** per `install_user_setup.py:303,305`, and contradicts C's own FR-006 (C:22). Decision Summary item 4 also says "unchanged contract — never fatal, reported by name" (C:8), which only becomes true after FR-006. | Medium | L3 |
| X-005 | CODE | Effect of placing Ponytail last on the budget | "placing Ponytail last means its commands run after the six existing plugins' commands" (A:71); "cannot starve the six" (A:14). **False:** `install_plugins` queues every missing marketplace add before any install (`install_user_setup.py:271-284`). On a fresh workspace the 13 MB `DietrichGebert/ponytail` clone is the third command, ahead of all six installs. `P2-layer2.md:357-358` shows exactly this failure shape: Orca used 25 s, the marketplace adds ran, and every install hit the time limit. | R4 "30 s budget starves the last-listed plugin (Ponytail ...)" (B:221): partly false for the same reason; the clone can starve the six installs, not only Ponytail's install | C-019 claim that "first" wins contention is closer, see X-006 | High | L3 |
| X-006 | CODE | Effect of placing Ponytail first | — | — | "ponytail first in order (FR-001) so it wins contention" (C:56); `extraKnownMarketplaces` gains Ponytail "(first)" (C:33). Partly false: marketplace commands follow `wanted` order (`install_user_setup.py:272-279`), so key order in `extraKnownMarketplaces` has no effect, and Ponytail's install still runs after every other missing marketplace add. Its marketplace add and its install are first within their groups, which is all "first" buys. | Medium | L3 |
| X-007 | CROSS | Fallback when settings `env` does not reach the hook | Installer writes `{"defaultMode": "off"}` to `~/.config/ponytail/config.json` when absent, needing an NFR-001 waiver (A:91) | No fallback; config-file write rejected: "needs Ponytail's private path resolution ..., new Python, and a new write outside `~/.claude`" (B:97) | "fall back to documenting `~/.config/ponytail/config.json {\"defaultMode\":\"off\"}` ... (the installer must still not write that file, NFR-002)" (C:89) | High (reduced: `enrichment/env-propagation-evidence.md` documents and live-observes settings `env` reaching spawned subprocesses, so the fallback is unlikely to trigger) | L3 |
| X-008 | CROSS | UserPromptSubmit in active modes | "per-prompt ruleset injection is Qoder-only" (A:83) | "Re-injects the ruleset each prompt while mode is active" (B:108) | Silent on that point; only `/ponytail ...` reactions described (C:45) | Medium (sets the cost of a user opting in to `full`; upstream `ponytail-mode-tracker.js` not re-read here: UNVERIFIED) | L3 |
| X-009 | CROSS | Gate status of the env check | "**V-1 (must be checked before merge ...)**" (A:91) | AC-M1 manual, "resolving the UNVERIFIED" (B:210) | "UNVERIFIED platform assumption to check here" (C:89) | Medium. All three treat it as open; the new evidence file says "a throwaway-HOME session check remains optional confirmation, not a merge gate" (`env-propagation-evidence.md:9`) | L3 |
| X-010 | CROSS | Docs plugin count | "seven plugins" (A:121) | "Replace the count so it cannot drift again" (B:157) | "\"six plugins\" → \"seven plugins\"" (C:73) | Low | L1 |
| X-011 | CROSS | Is a Coder handoff needed | "Not needed for this PR." (A:178) | "A handoff is needed only as a confirmation" (B:240) | "Handoff needed, one line to the template owner" (C:114) | Low | L1 |
| X-012 | CROSS | Clone-size risk | Ponytail "is the plugin most likely to hit the time limit" (A:106) | "it is not an outlier next to the two existing marketplaces" (B:133); no sizes given for the other two, so UNVERIFIED | Risk med/low (C:99) | Low | L3 |
| X-013 | CROSS | Ledger certainty | Probability "High" (A:162) | Probability "Med", "gating UNVERIFIED end to end" (B:223) | "certain when enabled + project detected" (C:101) | Low | L3 |
| X-014 | CROSS | Naming an uninstall command | "exact uninstall command UNVERIFIED, so docs do not name one" (A:110) | "do not only run `claude plugin uninstall`" (B:139) | Not named | Low | L1 |
| X-015 | INTRA | C's test IDs | — | — | Risks: "T7 manual throwaway-HOME check before merge" (C:97); T7 is "no fatal path", a unit test (C:87). The manual check has no ID. | Low | L1 |
| X-016 | INTRA | C's CHANGELOG and version | — | — | Risks: "CHANGELOG names the verified version" (C:98); C's CHANGELOG text names no version (C:74) | Low | L1 |
| X-017 | CODE (unverifiable) | `node` absence likelihood | IronClaude already needs `node` for `pragmatic-subagent.js` (A:103): **verified**, `install_hooks.py:66-68`, `hooks.json:124` | — | "The `claude` CLI itself is a Node app, so `claude` present without `node` is unlikely" (C:58): no repo evidence; UNVERIFIED (Claude Code also ships a standalone native install) | Low | L3 |

### Code-check log (claims checked and found true)

| Claim | Variant | Checked at | Result |
|---|---|---|---|
| `update` calls `install_user_setup(force=True)` | A, B, C | `main.py:403-405` | True |
| `update.sh:8` runs `superclaude install --force`; `:10` runs `superclaude doctor` | A, B, C | `update.sh:8,10` | True |
| Install step 7 runs user setup | A | `main.py:231-237` | True |
| Nested fill entry by entry; user value kept | A, B, C | `install_user_setup.py:36, 153-161` | True |
| `wanted` filter is `is True` | A, B, C | `install_user_setup.py:266` | True |
| Order: rules, styles, defaults, Orca, plugins | B | `install_user_setup.py:317-323` | True |
| `ok=True` on every plugin path | A, B, C | `install_user_setup.py:258, 286, 307-311` | True (C omits `:286`) |
| Non-dict `enabledPlugins` coerced to `{}` → "already installed" | C | `install_user_setup.py:264-266, 285-286` | True |
| Malformed settings → `ok=False`, file untouched | B | `install_user_setup.py:146-148` | True |
| `_ORCA_TIMEOUT=25`, `_NETWORK_BUDGET=30` | B, C | `install_user_setup.py:34-35` | True |
| Existing assertions are prefix and `"time limit"` only | B, C | `tests/cli/test_install_user_setup.py:240, 242` | True; B's new format keeps them green |
| `playwright` `False` survives defaults | C | `tests/cli/test_install_user_setup.py:92` | True |
| Update test pins installer order; `install_plugins` stubbed | A, C | `tests/cli/test_update_command.py:44-46, 88-97, 129-133` | True |
| `install --list` and `doctor` have no plugin check; doctor "plugin" = pytest plugin | A, B, C | `main.py:86-172`; `doctor.py:27-49` (`_check_pytest_plugin` at `:30`) | True |
| Docs say "six plugins" | all | `docs/getting-started/installation.md:354` (only hit in `docs/`) | True |
| Settings-defaults table row lists no plugins | B | `installation.md:345` | True |
| `post-release-manifest.json:28` names "default plugins" without a count | B | that line | True |
| `c-e2e-transcript.txt:308` is a historical install transcript | A | that line | True |
| `[Unreleased]` empty at `CHANGELOG.md:5` | A, B | `CHANGELOG.md:5-7` | True |
| Pragmatic ladder at `pragmatic.md:136-152` | all | `pragmatic.md:136-152` | True |
| IronClaude SubagentStart injects freshness + pragmatic blocks | A | `hooks/hooks.json:110-128` | True |
| `/sc:implement` never invokes `ponytail-review` | A, B, C | `tests/skills/test_implement_severity_static.py:149`; `source.md:208-224` | True |
| Only `src/superclaude` hits for "ponytail" are two `sc-pr-submit-protocol` scripts and `sc-implement-protocol/refs/qa.md` | B | grep of `src/superclaude` | True (3 files) |
| No `statusLine` in `src/superclaude` | B, C | grep of `src/superclaude` | True |

## Unique Contributions

| # | Variant | Contribution | Value Assessment | Level |
|---|---------|--------------|------------------|-------|
| U-001 | A | Named gate V-1 with explicit Pass and Fail outcomes and a defined code fallback (write `config.json` only when absent) (A:91) | Medium (was High; the env-propagation evidence now makes the fallback unlikely to be needed) | L3 |
| U-002 | A | Counts the per-subagent context load: IronClaude already injects two blocks per subagent (`hooks.json:110-128`); `full` would add a third to every Orca worker and `/sc:*` subagent (A:82) | Medium | L3 |
| U-003 | A | Test T-1 pins Ponytail as the last `enabledPlugins` key (A:141) | Low (pins an order whose budget rationale is false, X-005) | L2 |
| U-004 | A | Docs paragraph warns that `/ponytail default` has no effect while the env value is set, and that deleting the key is not an opt-out (A:123) | Medium | L1 |
| U-005 | B | Real repo log proving the label defect (`P2-layer2.md:358`) and a mitigation risk for consumers that parse `--scope` (R8) (B:73, :225) | Medium | L3 |
| U-006 | B | Test T4: an existing user with only the old six plugins gets the three new keys, and a second run is idempotent (B:199) | High (directly proves the "existing user via update" success criterion) | L3 |
| U-007 | B | T1 invariant: every `enabledPlugins` marketplace has a `source.repo` in the defaults, guarding every future plugin add (B:196) | Medium | L2 |
| U-008 | B | Migration risk R1: the env default silently overrides an existing Ponytail user's `~/.config/ponytail/config.json` `defaultMode`; CHANGELOG sentence tells them what to set (B:183, :218) | Medium | L3 |
| U-009 | B | `update.sh:10` runs `doctor`, so a plugin check in `doctor` would gate updates on network state (B:151) | Low | L2 |
| U-010 | B | Coder confirmation checklist, including a template that pre-writes `settings.json` (nested fill still adds missing keys; a pinned `false` wins) (B:242-244) | Medium | L1 |
| U-011 | B | R9: an unknown mode value falls through to `full` upstream, which T1 would not catch (B:226) | Low | L3 |
| U-012 | B | Manual AC-M2 and AC-M3 (opt-out rerun; no `claude` on PATH; blocked network) (B:211-212) | Low | L2 |
| U-013 | C | Hooks register through the plugin's own hook file, not `settings.json`, so `apply_settings_defaults` (which never touches `hooks`) cannot collide with them (C:44) | Low | L3 |
| U-014 | C | `known[market] = source` at `install_user_setup.py:279` is same-run dedup only; persistence is `claude`'s own `known_marketplaces.json`, so a rerun retries just the install (C:57) | Low | L3 |
| U-015 | C | Pre-existing quirk: non-dict `enabledPlugins` reports "already installed" (C:59), verified at `:264-286` | Low | L3 |
| U-016 | C | Coder handoff: confirm the template installs `superclaude` from the fork and not a pinned older version (C:114). This is the only variant touching the package-upgrade precondition (see A-001) | Medium | L1 |
| U-017 | C | Tests T4 (already-installed skip for Ponytail) and T7 (never fatal under three conditions) (C:84, :87) | Low | L2 |
| U-018 | C | Docs acceptance: `grep -rn "six plugins" docs/` returns nothing (C:75) | Low | L1 |

## Shared Assumptions

### Agreement points and their preconditions

All three variants agree on the points below. Each precondition is classified STATED (a variant says it), UNSTATED (relied on but not said), or CONTRADICTED (the repository or evidence says otherwise).

| Agreement point | Precondition | A | B | C | Classification | Notes |
|---|---|---|---|---|---|---|
| P1 Ship mode `off` via settings `env.PONYTAIL_DEFAULT_MODE` | Settings `env` is exported to plugin hook subprocesses | STATED, UNVERIFIED, gate V-1 (A:91) | STATED, UNVERIFIED, AC-M1 (B:118) | STATED, UNVERIFIED (C:89) | STATED; now **evidenced**: docs say `env` applies "to subprocesses Claude Code spawns", hooks "run ... with Claude Code's environment", and a live Bash subprocess saw the settings values (`enrichment/env-propagation-evidence.md:5-7`). A plugin-hook-specific run was not done (`:9`). | All three gates can drop from merge blocker to optional confirmation (X-009) |
| P1 | No shell-exported `PONYTAIL_DEFAULT_MODE` overrides or conflicts with the settings value | — | — | — | UNSTATED → A-008 | |
| P2 Defaults file is the only entry point; update paths unchanged | Existing users get the new keys through nested fill | STATED (A:31) | STATED (B:67) | STATED (C:5) | STATED, verified `install_user_setup.py:153-161` | Needs a dict-shaped `enabledPlugins`/`env` (`:156-157`) and parseable settings (`:147-148`); B covers malformed settings only |
| P2 | Existing users actually run the new package version | — | — | Partly, for Coder only (C:114) | UNSTATED → A-001 | |
| P2 | `apply_settings_defaults` runs before `install_plugins` in the same run | STATED (A:69) | STATED (B:12) | implied | STATED, verified `install_user_setup.py:320-322` | |
| P3 Plugin enabled in settings even when the install fails or `claude` is missing | Claude Code tolerates an `enabledPlugins` entry for a plugin that is not installed | STATED as UNVERIFIED (A:104) | — | — | UNSTATED for B and C → A-002 | |
| P4 `ponytail@ponytail` resolves with no special case | `claude plugin marketplace add DietrichGebert/ponytail` registers under the key `ponytail` in `known_marketplaces.json` | STATED as UNVERIFIED (A:70) | Asserts the upstream manifest `name` only (B:28, :68) | — | UNSTATED as a key claim → A-003 | |
| P4 | `claude plugin install ponytail@ponytail --scope user -y` with stdin closed (`install_user_setup.py:281, 300`) completes without prompting for Ponytail's `userConfig` (ledger, webhook) | — | — | — | UNSTATED → A-004 | |
| P5 Skills satisfy "valuable skill missing" even in `off` | Skills of an enabled plugin are listed regardless of the plugin's own mode | Asserted, no source (A:85) | Asserted (B:13) | Asserted (C:7) | UNSTATED → A-005 | |
| P6 `off` is dormant | SessionStart and SubagentStart exit early in `off` | STATED with upstream lines (A:81-82) | STATED (B:106-107) | STATED (C:45) | STATED (upstream, not re-read here) | |
| P6 | Mode `off` also disables UserPromptSubmit mode-tracker effects on ordinary prompts | STATED (A:83) | STATED (B:108) | STATED (C:45) | STATED for `/ponytail` commands; UNSTATED whether any natural-language phrase can switch the mode on, and that the hook still starts a `node` process per prompt (B:117 says per event) → A-006 | |
| P7 Never fatal; reruns converge | Each rerun has enough budget left to make progress | STATED as "reruns converge" (A:102) | STATED (B:128) | STATED (C:57) | UNSTATED precondition: the Orca step does not use the budget every run → A-007. Partly CONTRADICTED by `P2-layer2.md:357-358` | |
| P7 | A hook that fails (no `node`, exit 127, or 15 s timeout) does not block the session or the prompt | "never block tools" (A:89) | display UNVERIFIED (B:129) | display UNVERIFIED (C:58) | UNSTATED for blocking and latency → A-009 | |
| P8 Opt-out by `false` | `false` survives fill and is filtered out | STATED | STATED | STATED | STATED, verified `install_user_setup.py:159, 266`; `tests/cli/test_install_user_setup.py:92` | |
| P9 No `install --list` / `doctor` change | Install output line is enough visibility | STATED | STATED | STATED | STATED | |
| P10 No version pin; source only `DietrichGebert/ponytail` | Marketplace head is acceptable | STATED (A:164) | STATED (B:222) | STATED (C:98) | STATED | |

### Promoted shared assumptions

| # | Assumption [SHARED-ASSUMPTION] | Source Agreement | Impact | Status | Level |
|---|---|---|---|---|---|
| A-001 | Existing users pick up the new defaults just by running `superclaude update` or `update.sh`. In fact `update` re-runs the installers "to match the current package version" (`main.py:344-345, 360`) and never calls pipx or pip (coordinator confirmed). `update.sh:7` runs `pipx install --force ./` from the local checkout with no `git pull`. The Ponytail entries arrive only after the package itself is upgraded. | All three claim "no change to update paths" and that existing users get Ponytail on their "next install or update" (A:31, B:12, C:6). Only C hints at it, and only for Coder templates (C:114) | High. The success criterion for existing users depends on it; docs, CHANGELOG and tests should state the upgrade step | UNSTATED (A, B); partly STATED (C) | L3 |
| A-002 | Claude Code accepts `enabledPlugins["ponytail@ponytail"]: true` for a plugin not yet installed (no `claude`, offline, time limit) without an error or a blocking prompt | All ship this state. A marks it UNVERIFIED (A:104); B and C are silent. The six existing plugins already reach this state (`P2-layer2.md:355, 358`), but the session-side outcome is not recorded | Medium | UNSTATED (B, C) | L3 |
| A-003 | The marketplace added from `DietrichGebert/ponytail` is keyed `ponytail` in `~/.claude/plugins/known_marketplaces.json`, matching the market name taken from the plugin id (`install_user_setup.py:273, 277`) | A: UNVERIFIED (A:70). B asserts only the upstream manifest name. C silent. Weak support: a workspace path `/config/.claude/plugins/marketplaces/ponytail/` appears in `.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md:213` | Medium. If the key differs, `market not in known` is true every run, so the add is re-queued each time, uses budget, and may fail permanently | UNSTATED (B, C) | L3 |
| A-004 | `claude plugin install ponytail@ponytail --scope user -y` with `stdin=DEVNULL` completes without prompting for Ponytail's `userConfig` (ledger default true, webhook empty) | None of the three discusses install-time `userConfig` prompts | Medium. A prompt with stdin closed would fail or hang until the time limit on every run | UNSTATED | L3 |
| A-005 | Skills and `/ponytail` of an enabled plugin are available whatever Ponytail's mode is (mode gates only hooks) | All three base the "valuable skill missing" claim on it (A:85, B:13, C:7); none cites evidence | High. If a skill itself checks the mode, `off` does not close #330 | UNSTATED | L3 |
| A-006 | In `off`, the UserPromptSubmit tracker has no effect on ordinary prompts: no natural-language trigger switches the mode on, and its per-prompt `node` start (15 s timeout) adds no noticeable latency | All three say ordinary prompts produce no output; none addresses activation phrases or per-prompt cost (B:117 notes cost UNVERIFIED for all hooks) | Low | UNSTATED (sub-precondition of a STATED point) | L3 |
| A-007 | Reruns converge: every `superclaude install` run leaves enough of the shared 30 s budget for the plugin step. Orca runs first with up to 25 s (`install_user_setup.py:34, 226, 321`) and retries on every run while its skills are missing (`:213-217`) | All three rely on "rerun to retry" (A:102, B:128, C:57) | Medium. `P2-layer2.md:357-358` shows Orca timing out at 25 s and every install starved; on such a workspace Ponytail (a third clone) never installs | UNSTATED; partly CONTRADICTED by the log | L3 |
| A-008 | No shell-exported `PONYTAIL_DEFAULT_MODE` conflicts with the settings value, so the settings `env` value decides the mode | All three treat the settings value as authoritative; none discusses the order of process env vs settings `env` | Low | UNSTATED | L3 |
| A-009 | A failing Ponytail hook (no `node`: exit 127; or a hang up to the 15 s timeout) does not block a prompt or session start; the cost is noise only | A: "never block tools" (A:89); B and C mark only the display UNVERIFIED | Low-Medium. A UserPromptSubmit hang adds up to 15 s per prompt | UNSTATED | L3 |

## Summary

- Total structural differences: 13
- Total content differences: 23
- Total contradictions: 17 (10 cross-variant; 5 checked against code: X-003, X-004 (also intra), X-005, X-006, X-017 (unverifiable half); 2 intra-variant: X-015, X-016)
- Total unique contributions: 18 (A 4, B 8, C 6)
- Total promoted shared assumptions: 9 (A-001..A-009)
- Highest-severity items: C-002, C-005, C-012, C-013, X-001, X-002, X-003, X-005, X-007, U-006, A-001, A-005
- Main findings for the debate:
  1. All three variants agree on the core design: defaults file only, `env.PONYTAIL_DEFAULT_MODE="off"`, opt-out by `false`, no change to update paths, `install --list` or `doctor`.
  2. The real splits: whether to fix the `--scope` failure label (B and C yes, A no), plugin order (A and B last, C first), and the fallback if the env route fails (A writes `config.json`, B none, C docs only).
  3. Code contradicts two claims. Variant A's failure table shows output the current code cannot produce (X-003). Both A's and B's budget reasoning ignore that every marketplace clone runs before every install (X-005).
  4. New evidence (`enrichment/env-propagation-evidence.md`) supports the env-propagation assumption all three left UNVERIFIED. That weakens the case for a merge-blocking gate (X-009) and for any fallback (X-007).
  5. Unstated precondition A-001: `superclaude update` does not upgrade the package, so existing users get Ponytail only after a package upgrade. None of the variants states this for ordinary users.
