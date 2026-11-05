# Round 1 — Variant C (QA)

Variant: C (`variant-3-haiku-qa.md`), persona QA: test surface, edge cases, regression risk, acceptance criteria. Opponents: A (`variant-1-opus-architect.md`), B (`variant-2-sonnet-refactorer.md`). Diff: `diff-analysis.md`; enrichments re-verified in repo this session.

## Position Summary

C ships the same data-only core as A and B but is the only variant whose acceptance surface can actually detect the two defects the diff analysis confirmed in code: the `--scope` failure-label bug (X-003) and the misleading budget-order reasoning (X-005/X-006). The superior artifact is a merge: B's test suite (T4 existing-user, T1 invariant) plus C's never-fatal T7 and manual gates, with A's fallback discipline kept as a documented contingency rather than installer code.

## Steelman (A)

A is the strongest on architecture discipline: "data, not code" (`variant-1-opus-architect.md:7`), NFR-001 zero Python lines with an explicit deviation-reporting rule (`:37`), and AC-2 that mechanically enforces the scope with `git diff --stat` (`:150`). Its named gate V-1 with defined Pass/Fail outcomes and a pre-committed fallback (`:91`) is the cleanest verification treatment of the three, and U-002 (counting a third per-subagent injection block on every Orca worker, `hooks.json:110-128`) is systems thinking neither opponent matched.

## Steelman (B)

B is the strongest on correctness of the current code and on regression coverage. It found the `--scope` label defect A missed, cited a real log proving it fires in production (`.dev/codegraph-migration/evidence/P2-layer2.md:358`, verified this session), and scoped the fix to ~4 lines with an argv-shape that keeps the existing weak assertions green (`variant-2-sonnet-refactorer.md:77-92`). Its T4 existing-user idempotent test (U-006, `:199`) is the single highest-value test any variant proposes: it directly proves the "existing user via update" success criterion. B's FR/NFR-to-test "Proves" mapping (`:196-201`) is the best acceptance-criteria engineering in the set.

## Strengths Claimed (C)

1. **Only variant to test the never-fatal contract under Ponytail load**: T7 asserts `ok=True` under claude-absent, non-zero-exit, AND `deadline=0` with ponytail in the wanted set (`variant-3-haiku-qa.md:87`). A has AC-4 resting on the existing generic test (`:152`); B's T5 covers two conditions (`:200`). The third plugin raises contention; the contract needs its own regression pin.
2. **Only variant to test already-installed skip for the new plugin**: T4 (`:84`) extends the skip path to ponytail. A and B rely on the existing generic test — yet NFR idempotency (B's NFR-004) is precisely what a new defaults key can break.
3. **Edge-case rows nobody else has**: no-`claude` partial state, partially-spent budget with `known[market]` same-run dedup explained (U-014), non-dict `enabledPlugins` coercion quirk surfaced (U-015, verified `install_user_setup.py:264-266`), and the band-ledger "certain when enabled" honesty (`:48,101`).
4. **Testability as the mode argument**: "shipping `full` to everyone is an untestable-here behavioural change to every session and subagent" (`:7`) — the QA framing for `off` that A reaches architecturally (`:87`).
5. **U-016**: the only variant touching the package-upgrade precondition (template installs from fork, not a pinned older version, `:114`) — which the diff analysis promoted to the High-impact assumption A-001.
6. **U-013**: hook registration cannot collide with `apply_settings_defaults` because it never touches `hooks` (`:44`) — eliminates a whole class of merge-conflict edge case.

## Weaknesses Identified in others

1. **A's failure table is falsified by code (X-003)**: it presents `not installed: DietrichGebert/ponytail, ponytail@ponytail` as "existing behaviour" (`variant-1-opus-architect.md:95,100`), but `install_user_setup.py:292,303,305` appends `args[3]` = `"--scope"` (verified this session). A spec whose Failure Behaviour section describes output the code cannot produce fails its own acceptance bar.
2. **A and B's budget reasoning is wrong in the same way (X-005)**: both argue "last" protects the six existing plugins (`A:14,71`; `B:221`), but `install_user_setup.py:271-284` queues ALL marketplace adds before ALL installs, so a 13 MB clone as the third command can starve all six installs — exactly the shape in `P2-layer2.md:357-358`. A even writes a test (T-1, `A:141`) pinning an order whose stated rationale is false.
3. **A's zero-Python NFR is process over truth**: refusing the label fix means shipping a seventh plugin whose failure warning cannot say which plugin failed (`install_user_setup.py:303`) — directly worsening the retry advice the never-fatal contract depends on. NFR-001 makes the right fix a "deviation to report" (`A:37`).
4. **B has no fallback for the env route (X-007)**: it rejects the config-file write (`B:97`) but defines nothing if `env` fails to propagate; the new evidence makes that unlikely, not impossible. A and C both define one.
5. **B's docs drop two user-facing caveats** A and C carry: `/ponytail default` being silently overridden by the env key, and (in the docs text) the ledger location (`B:165-171` vs `A:123`, `C:73`).
6. **A and B under-specify the gate as a merge criterion**: A says "must be checked before merge" but only in prose AC-3; B's AC-M1 conflates proving install mechanics with proving env propagation in one manual step (`B:210`). C separates the mechanical manual check from the unit suite (T6/T7) — though C's own ID hygiene is worse (see Concessions).

## Concessions

- **X-004 stands against C**: my failure table row "plugin id listed" under "Behaviour today (verified)" (`variant-3-haiku-qa.md:52,55`) is false for the same `args[3]` reason and contradicts my own FR-006 (`:22`); Decision item 4's "reported by name" (`:8`) is post-fix, not today. The table header should have said "after FR-006".
- **X-006 partly stands**: "ponytail first ... wins contention" (`:56`) overstates — key order in `extraKnownMarketplaces` has zero effect (`install_user_setup.py:272-279` iterates `wanted`); only `enabledPlugins` order positions ponytail's add and install first within their groups. The direction is right; the mechanism as written is half wrong.
- **X-015**: my Risks table calls the manual check "T7" (`:97`) but T7 is a unit test (`:87`) — the manual check has no ID.
- **X-016**: "CHANGELOG names the verified version" (`:98`) is not executed by my CHANGELOG text (`:74`).
- **S-010**: my CHANGELOG block uses `### Added —` inline, not the file's `### <topic> (#NNN)` / `#### <Kind> (<topic>)` style (`CHANGELOG.md:11-13`); A's and B's blocks match it.
- **C misses B's T4 existing-user test and T1 `source.repo` invariant**, and misses A's named Pass/Fail gate structure — real acceptance-surface gaps.
- **C cites the enrichment notes rather than upstream source** where A read upstream directly (S-013); as evidence provenance, mine is one step weaker.

## Positions on diff points

| ID | Preferred variant | One-line reason |
|---|---|---|
| C-002/X-001 | C (qualified) | Marketplace adds all precede installs (verified `:271-284`), so "last protects the six" is false in both A and B; within-install order is all any position controls, and the issue's target plugin first is defensible triage — but C's X-006 mechanism claim must be corrected, and B's minimal-churn argument means the merge should not reorder if evidence stays ambiguous. |
| C-005/X-002/X-003 | B+C (identical fix) | The label defect is real and proven by a production log; B's ~4-line argv-shape fix plus C's T5/T7 tests is the complete package; A's zero-Python stance ships a known reporting bug to seven plugins. |
| C-012/X-009 | merge: A's gate form, none as merge blocker | New evidence (`env-propagation-evidence.md:5-9`) documents and live-observes settings `env` reaching spawned subprocesses; keep A's named Pass/Fail structure as an optional confirmation, not a blocker. |
| C-013/X-007 | C's fallback, A's waiver discipline | Documenting `~/.config/ponytail/config.json {"defaultMode":"off"}` as a user step keeps the installer inside `~/.claude/` (NFR-002) and needs no code; A's pre-committed trigger condition is worth adopting verbatim. |
| X-005 | C (corrected) | Adds-before-installs is verified; both "last" rationales and C's over-broad "wins contention" must be rewritten against `install_user_setup.py:271-284`; the merged spec should cite `P2-layer2.md:357-358` as the observed failure shape. |
| U-006 | B, verbatim | T4 existing-user-with-old-six → three new keys → idempotent second run is the direct proof of the update-path success criterion; C and A must adopt it. |
| C-008 | B | Dropping the count kills the drift class; C's grep acceptance survives either way. |
| C-016 | B (plus C's U-016) | B's three-question confirmation is actionable; add C's fork-vs-pinned-version question, the only item addressing A-001's Coder half. |
| C-021 | B | Migration note for existing Ponytail users (`config.json` silently overridden) belongs in CHANGELOG; C omitted it entirely, A covered only `/ponytail default`. |

## Shared Assumptions

| # | Response | Reasoning |
|---|---|---|
| A-001 | ACCEPT | Verified: `update` re-runs installers but never upgrades the package; existing users need a package upgrade first — C's U-016 covers only the Coder template half, so docs/CHANGELOG must state the upgrade step. |
| A-002 | ACCEPT | Enabled-but-not-installed is the exact post-failure state all three ship; the six existing plugins already reach it (`P2-layer2.md:355,358`) with no recorded bad session-side outcome, so it needs the observation, not new code. |
| A-003 | QUALIFY | The `known_marketplaces.json` keying claim is plausible (weak path evidence) and a mismatch only degrades to a re-queued add per run inside the never-fatal budget — worth one manual check in the throwaway-HOME run, not a code change. |
| A-004 | ACCEPT | No `userConfig` field is required (`assumption-evidence.md`), so a closed-stdin `-y` install cannot fail validation; residual prompt risk stays covered by the never-fatal T7 path. |
| A-005 | ACCEPT | Enrichment verified the skills never read the mode (`assumption-evidence.md:5-9`); this was the High-impact assumption underpinning `off` closing #330, and it now holds with evidence. |
| A-006 | QUALIFY | No-output-on-ordinary-prompts is stated by all three, but natural-language activation phrases and per-prompt `node` latency remain unaddressed; cheap to observe in the same throwaway-HOME session, no design change. |
| A-007 | QUALIFY | "Reruns converge" is partly contradicted by `P2-layer2.md:357-358` (Orca can eat 25 s every run while its skills are missing); convergence holds only if some run leaves budget — the merged spec should say this in the budget row. |
| A-008 | ACCEPT | Process env vs settings `env` precedence is untested but low-impact; the throwaway-HOME check with a clean shell settles it in the same run. |
| A-009 | QUALIFY | Non-blocking is likely (hooks emit context only) but a hung UserPromptSubmit hook can cost up to 15 s per prompt; observe in the manual session, document if it fires. |
