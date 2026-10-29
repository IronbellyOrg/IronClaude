# P2 installer contract: final recommendation
<!-- Produced by /sc:adversarial (Step 5 merge of refactor-plan.md, 12 of 12 changes applied) -->
<!-- Base: Variant 3 (option-c, original); additions from Variant 2 (option-b) and Variant 1 (option-a) -->
<!-- Date: 2026-10-29 -->

Verdict: codegraph is a required phase (`superclaude install` exits 1 when it fails), doctor fails only on a dangling registered command, and removal is receipt-gated and documented (no CLI flag).

The shared baseline (pin, reuse, download, register) is in `context.md` in this folder and is not repeated here.

## Phase <!-- Source: V3 base; banner from L1 forced round; failure output from V2 U-004; changes 1, 3, 4, 5, 7, 9, 10 -->
- Banner: "Installing codegraph (required user-level phase)...". On failure, stderr names the failed stage and the exact recovery command. The result feeds `main.py:264-275`, so install exits 1 after every other phase has run, and Coder CI's existing exit-0 check proves "installed by default".
- Candidates: exactly the `context.md` order. Extract a download to a temp dir, then rename. Never overwrite a link or dir that is not in the receipt; report it instead (registration uses the absolute version-dir path).
- Owned entry: type stdio or absent, no `url`, no `headers`, `args == ["serve","--mcp"]`, and env keys a subset of {CODEGRAPH_TELEMETRY, CODEGRAPH_NO_UPDATE_CHECK, CODEGRAPH_MCP_TOOLS}. Owned entries may be replaced, including when a pin bump changes the realpath. This replaces the env/headers refusal in the guard at `install_mcp.py:867-873`.
- User-managed entry (not owned): if its command resolves to an executable, the phase passes with "user-managed codegraph entry kept" plus `claude mcp remove codegraph --scope user`; otherwise the phase fails with that same command.
- The matcher compares the whole entry (type, command, args, env, alwaysLoad), so drift gets repaired.
- Platforms: the downloader's 4-entry platform map. An unsupported platform fails the phase with a named message, as `install_mcp.py:486-496` does today.

## Doctor <!-- Source: V3 base; C-002 majority (V2 + V3); change 2 -->
- New check "codegraph MCP registration". It sets passed=False only when the user entry `codegraph` exists and its `command`, resolved with `shutil.which` when it is a bare name, is not an executable file. Reason: codegraph tools would be silently missing from every session.
- Reported in details with passed=True: missing entry, version drift, the `codegraph prompt-hook` hook and the `CODEGRAPH_START` block. An unreadable `~/.claude.json` reports "unknown" with passed=True.
- No presence or drift failure: under `update.sh:2,8,10` doctor runs only after install exits 0, and `make verify` never exits non-zero (`Makefile:42`).

## Removal <!-- Source: V3 base; C-003 (all three advocates); change 9 -->
- No new CLI flag. Documented removal: `claude mcp remove codegraph --scope user`, then delete the receipt-listed paths.
- `superclaude install --list` prints, from the receipt, owned vs external paths and each link's resolved path ("owned: ~/.codegraph/versions/v1.6.2" or "external: /usr/local/bin/codegraph, not owned"). Baked or external binaries and `.codegraph/` project indexes are never listed as removable.

## Receipt <!-- Source: V3 base amended by A-002 (V1), INV-004, INV-010, INV-011; changes 6, 7 -->
- `~/.codegraph/.superclaude-receipt.json` holds the tag, tarball sha256, link targets and the owned version dirs in install order. It is written only after a verified download, never for a baked or external binary.
- A corrupt receipt means delete nothing, never fail, and rewrite it. A link counts as owned only while it points where the receipt says.

## Old version dirs <!-- Source: V3 C-005 simplified; INV-001 resolution round; change 8 (replaces the daemons/ lookup) -->
- On a pin bump, install the new dir, flip links, and keep the previous owned dir for one run.
- Delete an older receipt-listed dir only when all three hold: this run's registration was verified; the receipt and `~/.claude.json` both read OK; and none of the registered command realpath, `~/.local/bin/codegraph` or `~/.codegraph/current` (owned or not) resolves inside it.

## Size <!-- Source: change 12 (raises V3's 170-line estimate) -->
About 300 lines: `install_codegraph.py` about 180, `install_mcp.py` +60, `doctor.py` +30, `main.py` +30. About 33 tests.

## Coder prerequisites <!-- Source: INV-015, INV-009; change 11 -->
- Bake codegraph at the exact pin on PATH; test-57 accepts the codegraph registration; no pin bump before the bake; Phase 1 and Phase 2 land as one master unit.
- A Coder `timeout 60` kill between registration remove and add is repaired on the next run.

## Debate result <!-- Source: base-selection.md; debate-transcript.md Metadata and Convergence Assessment -->
- Base scores: C 0.896, B 0.859, A 0.839. The C-B margin is 0.037 (under 0.05), so tiebreaker level 1 applied: C won debate points 18/18.
- Convergence 18/18 = 100% (threshold 80%), standard depth: 2 rounds, plus a forced L1 round, an invariant probe and a resolution round.
- 1 HIGH invariant, INV-001, was resolved by the Old version dirs rule. Minority dissent: A wanted doctor to fail on a missing entry.

## Incorporated from the losing options <!-- Source: base-selection.md "Strengths to incorporate" -->
- From B: the U-004 recovery command in the failure output; a missing entry is reported, not failed; minimal-code pushback (no keep-aside copy, no timing machinery, no separate platform table).
- From A: prompt-hook leftover reporting (the hook survives the additive hook merge); receipt-proven ownership, applied to links and version dirs (the owned-entry test uses env keys instead, because a baked binary has no receipt).

## Rejected <!-- Source: refactor-plan.md "Changes NOT Being Made" -->
A's `superclaude mcp --uninstall --servers codegraph`; A's strict doctor (presence, drift, leftovers, missing entry); B's non-fatal phase; B's no-receipt fixed-path `rm -rf`; C's `~/.codegraph/daemons/` lookup; INV-002 version-split, INV-009 time-budget, INV-011 keep-aside and INV-012 separate-table machinery.
