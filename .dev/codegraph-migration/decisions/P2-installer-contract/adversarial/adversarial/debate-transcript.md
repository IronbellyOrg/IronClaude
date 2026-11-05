# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential), plus forced L1 taxonomy round, Round 2.5 invariant probe, and one resolution round for the HIGH invariant blocker
- Convergence after Round 2: 17/18 = 94% (BLOCKED_BY_TAXONOMY: L1 had zero coverage)
- Convergence after forced L1 round: 18/18 = 100% (BLOCKED_BY_INVARIANTS: INV-001 HIGH)
- Convergence after resolution round: 18/18 = 100%, CONVERGED
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (Mode A, one per input file; current model; personas: V1 architect, V2 analyzer, V3 qa)
- Denominator: S-001, S-002, C-001..C-009, X-001..X-004, A-001, A-002, A-004 = 18 points (U-NNN tracked, not counted)

Below: Round 1 statements and Round 2 rebuttals, as condensed by the orchestrator from each advocate's full reply (citations kept; orchestrator corrections marked).

Orchestrator citation notes: the env/headers guard is at `install_mcp.py:867` (the A and B advocates are right; diff-analysis's 858-864 and C's 862-864 are off by a few lines). `install-update-flow.md:223` confirms "codegraph is not baked anywhere today"; `:232` (Coder `ironclaude/install.sh:44-66,112-125`) confirms the Coder slug saves and restores `~/.claude/CLAUDE.md` around install. Upstream layout links `~/.local/bin/codegraph` to `versions/<tag>/bin/codegraph` (`codegraph-evaluation.md`, section 2).

## Variant 1 (A) advocate, architect

**Position.** A is the only option where a green install AND a green doctor both mean "pinned, registered codegraph". It provides one receipt-gated removal command. C's additions (daemon-aware cleanup, ownership view, dangling check) can be folded into A without weakening doctor or dropping uninstall.

**Strengths.** (1) The goal is literal and provable: install exits 1 through `main.py:264-275`. (2) Standalone doctor and `make verify` (`Makefile:42`) must not print "healthy" without codegraph or with the upstream prompt hook present. (3) Coder never runs doctor (only `superclaude install`), so strict doctor adds no failure in Coder. (4) C already writes receipt-gated deletion for old dirs, so exposing `--uninstall --servers codegraph` is cheap. (5) The receipt can also prove ownership of the registration entry (A-001).

**Critiques.** B makes the goal optional and leaves Coder CI's exit-0 proof empty; its fixed-path `rm -rf` can hit an upstream `install.sh` copy, and it leaves a stale entry silently when the env guard refuses. C's advisory doctor relies on install having just run, which is not true for standalone doctor or for later drift; C writes a receipt that no user removal command consumes.

**Concessions.** Largest code (about 370 lines and 35 tests); it re-adds a surface Phase 1 deletes; strict doctor fails on drift the next install fixes; A says nothing about old version dirs or the daemon (should adopt U-003); offline macOS is red; "red twice" in option-a.md:20 is wrong, because `set -e` stops `update.sh` before doctor.

**Verdicts.** C-001 1/3, C-002 1, C-003 1, C-004 1, C-005 3, C-006 1, C-007 2, C-008 1, C-009 1/3, X-001 1, X-002 1, X-003 1, X-004 1, S-002 1, U-001 1 (subsumed), U-002 3, U-003 3, U-004 2.
**Assumptions.** A-001 ACCEPT (the guard must recognise IronClaude-owned entries); A-002 ACCEPT; A-004 QUALIFY (install defaults touch only unset settings keys, so the prompt-hook check still matters).

## Variant 2 (B) advocate, analyzer

**Position.** B is the smallest correct contract. Install always attempts codegraph, and failure never turns `./update.sh` or the Coder slug red. Coder has not baked codegraph today, so a required phase is a live outage risk.

**Strengths.** (1) Ordering risk: no bake exists today (`install-update-flow.md:223`); the monitor rewrites the pin automatically; under A or C a bump before the bake fails every slug. (2) The 60 s budget, of which user setup reserves 30 s for network; B degrades instead of failing. (3) Smallest code (about 250 lines and 22 tests). (4) No daemon race: B never deletes a version dir. (5) No second red gate. (6) Its stderr recovery message names the command (today's message only says "retry", `main.py:258-261`).

**Critiques.** A re-adds uninstall and receipt machinery, and its CLAUDE.md block check is dead weight inside `update.sh`. A and C: the env guard (`install_mcp.py:867`) makes every pin bump exit 1 unless it is fixed. C: "a dangling command breaks every session" is unverified; C's receipt must hold a list (A-002), which C's size estimate omits.

**Concessions.** "By default" can silently fail; the exit code gives Coder CI no proof (concedes C-009); `rm -rf` can hit an upstream copy (concedes X-004); the stale entry is silent if A-001 is unfixed; U-001 could be grafted onto B.

**Verdicts.** C-001 2, C-002 2, C-003 2, C-004 2, C-005 2, C-006 2, C-007 2, C-008 2, C-009 3, X-001 2, X-002 2, X-003 2, X-004 3, S-002 2, U-001 3, U-002 2, U-003 2, U-004 2.
**Assumptions.** A-001 ACCEPT; A-002 QUALIFY (not applicable to B); A-004 QUALIFY (the Coder slug restores CLAUDE.md, so report the block, do not fail on it).

## Variant 3 (C) advocate, qa

**Position.** Required phase; doctor fails only on a dangling registered command; receipt plus documented removal, no new flag. One hard gate, on the exit code that both callers already check.

**Strengths.** (1) `update.sh:2,8` and Coder's exit-0 check already gate on install; matches the current Codebase Memory pattern (`main.py:254-275`). (2) Under `set -e` doctor runs only after install exits 0, so a presence check there only adds false reds. (3) A dangling command is caught, and doctor exit 1 (`main.py:508-512`) turns `make verify` red. (4) The receipt applies the "never delete an external binary" rule to exact paths.

**Critiques.** A double-fails on one cause, re-adds uninstall (about 80 lines and 7 tests), and its CLAUDE.md check is redundant. B can silently not install, and Coder must then add its own assertion (code moves to another repo, it is not removed); B's `rm -rf` can delete an unowned copy.

**Concessions.** The `~/.codegraph/daemons/` version lookup is unverified (the registry exists; per-version mapping is not shown; sockets are per project). The simpler baseline rule "keep the previous dir until the next run" (`codegraph-evaluation.md` section 7, step 4) is preferred. The A-001 guard blocks pin bumps under A and C unless fixed. Standalone doctor passes when no entry is registered. The bake must come first.

**Verdicts.** C-001 3, C-002 3, C-003 3, C-004 3, C-005 3 (simplified), C-006 2, C-007 2, C-008 3, C-009 3, X-001 3, X-002 3, X-003 3, X-004 3, S-002 3, U-001 3, U-002 3, U-003 3 (simplified), U-004 2.
**Assumptions.** A-001 ACCEPT; A-002 ACCEPT; A-004 QUALIFY.

# Round 2 rebuttals (working)

## Variant 1 (A) rebuttal
Orchestrator verified: `Makefile:42` ends `|| echo "❌ Some checks failed"`, so `make verify` never exits non-zero (doctor's only hard consumer is `update.sh:10`); `install_hooks.py:14` "Additive merge for the hooks key: existing user hooks preserved".

- (a) Uninstall CLI: CONCEDED. The goal never names removal; receipt + documented removal + C's `--list` ownership view is enough. C-003 to V3.
- (b) Strict doctor: partly conceded. Inside `update.sh` presence/shape checks add nothing; the CODEGRAPH_START check is redundant (dropped). Rebutted: the upstream `codegraph prompt-hook` survives every install (additive hook merge), so it must at least be reported. Rebutted: standalone doctor passing with NO codegraph entry is a false "healthy"; doctor already checks an installed component (`_check_ccsession`, `doctor.py:42`), so "fail on missing entry" follows practice.
- (c) Most code: CONCEDED; after (a) and (b) A shrinks to C's size.
- Ordering: a required phase adds no NEW ordering step. Phase 1 removal already forces Coder to make test-57 pin-agnostic before a bump (install-update-flow 5.3 step 2), and that test must accept "codegraph registered", which under `--network=none` needs the bake (order D) for B too. B's only gain is a transient online download failure, where its exit 0 is the conceded silent gap.
- New evidence: `make verify` cannot go red (C's claim is wrong); A-001 fix: recognise owned entries by receipt or by known env keys `CODEGRAPH_TELEMETRY`, `CODEGRAPH_NO_UPDATE_CHECK` (+ Phase 3's `CODEGRAPH_MCP_TOOLS`).
- Changed positions: C-002 -> 3 amended (fail on dangling command AND missing entry; drift, prompt hook, block in details); C-003 -> 3; C-004 1/3 (receipt holds list of version dirs); C-007 -> 3; C-008 -> 3; X-002 -> 3; X-003 -> 3; S-002 -> 3. C-001 stays required (1/3).

## Variant 2 (B) rebuttal
- (a) CONCEDED: test-57 must accept "codegraph registered" (install-update-flow 5.3 step 2); B's exit 0 moves the assertion into Coder, it does not remove it.
- (b) CONCEDED: delete only receipt-listed paths (C); the receipt holds a list of version dirs (A-002).
- (c) Ordering advantage WITHDRAWN: pin bump before bake under `--network=none` still fails test-57's registration assertion under B, on a different line. After the bake, reuse needs no network in all variants. B's only remaining gain (transient failure on a real boot) is the conceded silent gap.
- "Never deletes a version dir" is a disk leak once a pin bump re-registers a new realpath; C's simplified rule (keep the previous receipt-listed dir, delete older ones next run) bounds it without a `daemons/` lookup.
- Against Variant 1's amendment: failing doctor on a MISSING entry conflicts with the documented removal (`claude mcp remove codegraph` leaves standalone doctor red forever) and adds nothing inside `update.sh`. Report it, do not fail.
- New evidence: guard and message at `install_mcp.py:867-873` are hard-coded to codebase-memory-mcp, so the codegraph phase needs its own owned-entry test in every variant (A-001 is not a discriminator). Phase 1+2 land as one master unit (row E, `install-update-flow.md:325`) in every variant.
- Final: C-001 3 (+U-004 graft), C-002 3 (missing entry reported, not failed), C-003 3, C-004 3, C-005 3 simplified, C-006 1/3 tie, C-007 3 (smallest correct), C-009 3, X-001 3, X-004 3, U-001 3.

## Variant 3 (C) rebuttal
- (a) `make verify` claim CONCEDED; doctor's only exit-code consumer is `update.sh:10`, reached only after install exits 0.
- (b) "breaks every session" DOWNGRADED: a missing stdio command fails that one server (shown failed in `/mcp`, `claude mcp list`); the session continues (public sources, not reproduced). Corrected rationale: codegraph tools silently missing from every session. U-001 keeps `passed: False`.
- (c) Receipt list CONCEDED: tag, sha256, link targets, list of owned version dirs (+~10 lines, +2 tests).
- (d) `daemons/` lookup WITHDRAWN: keep the previous receipt-listed dir one run, delete older ones (`codegraph-evaluation.md` section 7 step 4).
- Open split: sides with Variant 2: a missing entry is REPORTED, not failed (documented removal is a valid state; presence is enforced by install's exit code).
- A-001 test: env-key subset, not receipt (a baked binary has no receipt): owned = no `headers` and `set(env) <= {CODEGRAPH_TELEMETRY, CODEGRAPH_NO_UPDATE_CHECK, CODEGRAPH_MCP_TOOLS}`; owned entries may be replaced after a pin bump, anything else is refused as today.
- Final: every point 3 (C-006 tie 1/3; U-004 from 2 adopted).

Orchestrator note: today's `_native_selection_error` (`install_mcp.py:486-496`) makes the required Codebase Memory phase fail on any non-Linux or non-amd64/arm64 host, so `superclaude install` already exits 1 on macOS today.

## Forced round: Taxonomy level L1 (surface)
- S-001: V1 and V2 want four sections (Phase / Doctor / Removal / Receipt); V3 wants the receipt under its own heading because A-002 enlarges it, plus "Old version dirs". VERDICT: five sections, Phase / Doctor / Removal / Receipt / Old version dirs (majority, V3 base).
- Phase banner: "Installing codegraph (required user-level phase)..." (unanimous once C-001 is settled; "default" is accurate only under B's non-fatal contract). Failure line: "Required codegraph phase incomplete...", modelled on `main.py:258-261`. `--list` header: "codegraph MCP (user scope):".
- Doctor check name: "codegraph MCP registration" (majority; V1 preferred "codegraph installed"). The summary gives the state, path and version; on failure: "registered command not executable: <path>".

## Round 2.5: Invariant probe
See `invariant-probe.md`: 15 findings, 1 HIGH (INV-001). Convergence BLOCKED on INV-001.

## Resolution round (all three advocates, parallel, on INV-001..INV-015)
- INV-001: ACCEPT, unanimous. Combined rule: delete a receipt-listed version dir only when (a) this run's registration was verified, (b) both the receipt and `~/.claude.json` were read successfully (any read failure means delete nothing; added by V2), and (c) no path among the registered `command` realpath, `~/.local/bin/codegraph` and `~/.codegraph/current` resolves inside it, checking the links whether or not IronClaude owns them (added by V3). The previous owned dir is still kept one run (V1, V3), because a daemon can run the old binary with no link pointing at it (`codegraph-evaluation.md` 5.7). About 10 lines and 3 tests. Blocker resolved.
- INV-002: QUALIFY, unanimous. One fixed candidate order; drop "(or the PATH winner)". `--list` prints each link's resolved path (V2/V3); no extra version-split machinery.
- INV-003: ACCEPT, unanimous: extract to a temp dir, then rename. A link not in the receipt is left alone and reported, not overwritten. It does not fail the phase, because registration uses the absolute version-dir path (V3 qualifier).
- INV-004: ACCEPT, unanimous. A link is owned only while it points where the receipt says. One helper, reused by INV-001 and `--list`.
- INV-005: ACCEPT (V2, V3; V1 QUALIFY via INV-014). The owned-entry test also requires `type` stdio or absent, no `url`, no `headers`, and `args == ["serve","--mcp"]`.
- INV-006: ACCEPT (V1, V3; V2 QUALIFY). For a refused user entry whose command resolves to an executable, the phase passes with "user-managed codegraph entry kept; to use IronClaude's pinned entry run `claude mcp remove codegraph --scope user` and re-run install". If its command does not resolve, the phase fails with the same command.
- INV-007: ACCEPT, unanimous: resolve a bare command with `shutil.which`.
- INV-008: ACCEPT (V2 QUALIFY on wording): doctor reports "unknown" with passed=True; the install failure names `~/.claude.json`.
- INV-009: ACCEPT as a documentation note only: a Coder `timeout 60` kill between remove and add is repaired on the next run. No time-budget code.
- INV-010: ACCEPT (V1, V3; V2 REJECT as moot): the receipt list is kept in install order.
- INV-011: QUALIFY, unanimous: a corrupt receipt means delete nothing, never fail, and rewrite it. No keep-aside copy.
- INV-012: QUALIFY, unanimous: the platform map the downloader needs, with an unsupported platform failing the phase with a named message (same pattern as `install_mcp.py:486-496`). No separate table.
- INV-013: ACCEPT. Nothing to do.
- INV-014: ACCEPT, unanimous: the matcher compares the whole expected entry (type, command, args, env, alwaysLoad).
- INV-015: ACCEPT, unanimous: Coder handoff prerequisites (bake at the exact pin, test-57 accepts the codegraph registration, no pin bump before the bake, Phase 1+2 as one master unit). No IronClaude code.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | V3 | 75% | Five-section layout; V1/V2 accepted in the forced round |
| S-002 | L2 | V3 | 90% | V1 conceded the uninstall CLI; V2 conceded receipt-gated deletion |
| C-001 | L3 | V3 (= V1) | 95% | V2 withdrew non-fatal after the test-57 argument; exit code is the gate `update.sh:2,8` and Coder use |
| C-002 | L3 | V3 | 85% | V1 conceded presence/drift checks; missing entry reported (V2+V3 majority, V1 dissent) |
| C-003 | L2 | V3 | 95% | All: documented removal + receipt + `--list`, no flag (Phase 1 deletes it) |
| C-004 | L2 | V3 (amended) | 95% | Receipt with an owned-dir list (A-002); no receipt for baked/external binaries |
| C-005 | L3 | V3 (simplified) | 90% | `daemons/` lookup withdrawn; keep previous one run + INV-001 reference rule |
| C-006 | L2 | V3 (tie with V1) | 85% | Bake-before-bump is forced by the goal + test-57 in every variant; V2 withdrew |
| C-007 | L2 | V3 | 85% | V2 at ~250 lines is not correct; V3 is the smallest correct |
| C-008 | L3 | V3 | 90% | `install --force` and the Coder slug handle CLAUDE.md; the prompt hook survives the additive merge (`install_hooks.py:14`), so report it |
| C-009 | L2 | V3 (= V1) | 95% | V2 conceded |
| X-001 | L3 | V3 | 95% | Unanimous after Round 2 |
| X-002 | L3 | V3 | 90% | `set -e` means doctor runs only after a successful install |
| X-003 | L2 | V3 | 90% | V1 conceded |
| X-004 | L2 | V3 | 95% | V2 conceded |
| A-001 | L3 | V3 | 95% | ACCEPT x3. Owned-entry test: env keys subset of {CODEGRAPH_TELEMETRY, CODEGRAPH_NO_UPDATE_CHECK, CODEGRAPH_MCP_TOOLS}, no headers or url, stdio, the expected args (INV-005). The guard is hard-coded at `install_mcp.py:867-873` |
| A-002 | L3 | V3 | 90% | ACCEPT x2, QUALIFY (V2, later conceded) |
| A-004 | L3 | V3 | 90% | QUALIFY x3: report the block, do not fail |

Unique contributions adopted: U-001 (V3, with rationale downgraded to "codegraph tools silently missing from every session", since a missing stdio command fails only that server; public sources, not reproduced), U-002 (V3), U-003 (V3, simplified), U-004 (V2, grafted into V3).

## Convergence Assessment
- Points resolved: 18 of 18
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 1 point (forced round), L2 8, L3 9
- Invariant gate: 0 HIGH UNADDRESSED after the resolution round; 8 MEDIUM had fixes agreed in that round; LOW items logged
- Status: CONVERGED
- Unresolved points: none. Minority dissent on record: V1 wanted standalone doctor to fail on a missing entry (C-002).
