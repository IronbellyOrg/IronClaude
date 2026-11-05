# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential A -> B -> C), Round 2.5 invariant probe, plus one invariant-resolution round (gate-forced, parallel) to clear HIGH INV-001
- Round 3: skipped (depth=standard)
- Convergence achieved: 100% (23 of 23 diff points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3
  - Variant 1 (option-a.md): advocate-a, persona architect (+ analyzer)
  - Variant 2 (option-b.md): advocate-b, persona devops/backend (+ analyzer)
  - Variant 3 (option-c.md): advocate-c, persona security (+ analyzer)
- Full verbatim statements (the authoritative record; this transcript condenses them): `round1-advocate-{a,b,c}.md`, `round2-advocate-{a,b,c}.md`, `resolution-advocate-{a,b,c}.md`; probe: `fault-finder-raw.md`, `invariant-probe.md`.
- Delivery note: Round 1 statements were first returned to the parent session instead of the orchestrator; each advocate re-wrote its statement verbatim to its file, which was read from disk. No content was lost.
- Omission check: every advocate answered A-001..A-007 in Round 1 (0 omissions).

## Round 1: Advocate Statements

### Variant 1 Advocate (architect)
**Position**: Option A, amended. It is the only option that meets the goal through `./update.sh` alone, and it adds no new kind of destructive behaviour. Its matchers must become exact argv/path allowlists.

**Steelman of Variant 2**: The only option that leaves kind-B workspaces clean with no human step, reusing tested receipt + sha256 proof.
**Steelman of Variant 3**: A literal reading of "Coder-owned leftovers are handed off"; dry-run preview; no change to `update.sh` or the time budget.

**Key strengths claimed**: install has no early return after `--list`, so a step is reached on every path (`main.py:189-275`); install already removes exact user entries with no prompt (`install_mcp.py:874-895`); reuses `read_user_mcp_entry` and a parameterised cleanup helper that Phase 2 needs; fits the 60 s bound; keeps different-shape same-name entries (U-002).
**Weaknesses identified in Variant 2**: uninstalls Coder's uv tool without proof; prompt-free account-wide upstream uninstall is exactly what `install_mcp.py:981-986` forbids; timeouts exceed the bound; keeps the module Phase 1 deletes.
**Weaknesses identified in Variant 3**: fails the goal on `./update.sh` (X-003); its consent premise is wrong (`install_mcp.py:874-895`); "shape-matched" undefined; migration-only flag.
**Concessions**: serena substring matcher misses the older IronClaude shape (A-001); basename looser than `install_mcp.py:757-763`; on Coder it removes a Coder-written entry (X-004); C's preview worth adopting.
**Shared assumptions**: A-001 ACCEPT (real contradiction), A-002 QUALIFY, A-003 QUALIFY, A-004 QUALIFY, A-005 QUALIFY, A-006 REJECT (receipt/marker are IronClaude files), A-007 ACCEPT.

### Variant 2 Advocate (devops/backend)
**Position**: B is the only variant that takes responsibility for files IronClaude provably installed; its uv-tool step and updater deletion are wrong. Narrowed B merged into A.

**Steelman of Variant 1**: Meets the goal on both paths at almost no cost; reuses helpers install already uses without prompting; U-002 is the best safety detail.
**Steelman of Variant 3**: Never changes user MCP state without a visible preview; fully respects the hand-off clause.

**Key strengths claimed**: receipt and `.pending` are IronClaude-written (`install_codebase_memory.py:81-86`) and would be orphaned by A and C; reuses proven ownership proof; zero cost when no receipt.
**Weaknesses identified in Variant 1**: misses the older serena shape; basename looser than existing matcher; leaves receipt/marker; prints upstream uninstall after removing the registration although existing code orders native uninstall first (`install_mcp.py:993-995`).
**Weaknesses identified in Variant 3**: fails X-003; wrong consent premise; undefined matcher; migration-only flag.
**Concessions**: drop `uv tool uninstall serena-agent` (Coder-owned); drop updater deletion (`install_codebase_memory.py:74-78,371`); prompt-free account-wide uninstall breaks consent; B's "60 s" is really `INSTALL_TIMEOUT = 300` (`install_codebase_memory.py:28`); network-free upstream uninstall UNVERIFIED.
**Shared assumptions**: A-001 REJECT (both historic shapes), A-002 QUALIFY, A-003 QUALIFY, A-004 QUALIFY, A-005 QUALIFY (upstream first), A-006 REJECT (remove under existing lstat/uid/nlink checks), A-007 QUALIFY.

### Variant 3 Advocate (security)
**Position**: Concede automatic removal for `codebase-memory-mcp` (written by IronClaude's required phase, `main.py:254-262`); keep consent for `serena` (opt-in, `install_mcp.py:60`; argv identical to Coder's bundle).

**Steelman of Variant 1**: Only option meeting the `./update.sh` goal; reuses verified helpers; non-fatal (matters under `set -euo pipefail`); U-002.
**Steelman of Variant 2**: Leaves most workspaces clean; tested receipt proof.

**Key strengths claimed**: serena is opt-in; serena ownership unprovable (X-004); Coder re-adds serena each start, so automatic removal is churn; dry-run preview; no time added.
**Weaknesses identified in Variant 1**: substring matcher misses the older form and matches hand-made entries; basename looser than exact path; ignores receipt/marker.
**Weaknesses identified in Variant 2**: uninstalls Coder's uv tool; prompt-free account-wide uninstall; exceeds 60 s.
**Concessions**: fails X-003; "no prompt-free mutation" overstated (`install_mcp.py:874-883`); "shape-matched" undefined; flag costs more than A's sunset table.
**Shared assumptions**: A-001 REJECT, A-002 QUALIFY, A-003 QUALIFY, A-004 QUALIFY, A-005 QUALIFY, A-006 REJECT (delete only after binary is gone), A-007 QUALIFY.

## Round 2: Rebuttals

### Variant 1 Rebuttal
- Serena opt-in (C): **conceded.** cbm removed automatically; the current-pin serena entry is kept with a printed `claude mcp remove serena --scope user`. Rejects C's flag: no consented serena path exists today (`install_mcp.py:1320-1324`), so a printed command gives the same consent at no code cost.
- Ordering (B): **conceded order, rejected keeping the module.** With a receipt present, keep the cbm registration and print the upstream uninstall (preserves `install_mcp.py:993-999` order) without retaining the 759-line module.
- Receipt/marker timing (C): **conceded** — delete only when the binary is absent, regular, single-link, user-owned.
- Exceptions/60 s kill: proposed placing the step first with its own try/except (later superseded by INV-007).

### Variant 2 Rebuttal
- Keeping receipt-gated removal: **conceded**; B's binary automation withdrawn; amended A's receipt/marker rule accepted in full.
- Serena: current pin **conceded** to keep-and-print (indistinguishable from Coder; still works after Phase 1). **New split held:** the pre-0e7bc31f registry argv (with `--enable-*` flags) was written only by IronClaude's code — the docs of the time told users a shorter command — so remove that exact argv automatically.
- Confirmed A's finding that no consented serena removal path exists.

### Variant 3 Rebuttal
- `--retire-legacy` and `--dry-run`: **conceded in full.** A cheaper preview survives inside the `install --list` block that Phase 1 must rewrite anyway (`main.py:161-186`).
- Older serena form: consent alone does not decide; provable ownership does — **accepts B's removal** (also a security gain: the old form ran unpinned GitHub HEAD code).
- Goal tension: **concedes** keep-and-print misses the goal for the current pin on non-Coder dev workspaces; today's docs command passes no `--scope` (`mcp-server-guide.md:394`, `serena-installation.md:34`), so a user-scope current-pin entry on a dev workspace is most likely IronClaude-written. Supplies the residual-risk statement; rejects an unverified `serena-agent` uv-tool Coder signal.

## Round 2.5: Invariant Probe (summary)

14 findings against the Round 2 consensus; 12 UNADDRESSED (HIGH 1: INV-001; MEDIUM 8; LOW 3). Gate status after Round 2.5: **BLOCKED_BY_INVARIANTS** (INV-001). Details: `invariant-probe.md`.

## Invariant-Resolution Round (gate-forced)

The orchestrator drafted resolutions (`invariant-resolutions-proposed.md`) and re-verified INV-001 evidence read-only (pre-fork `subprocess.run(list, shell=(sys.platform == "win32"))` in 5bee1571/43112779, so `$(pwd)` was stored literally). Each advocate answered all 14:
- advocate-a: 13 ACCEPT, INV-001 QUALIFY (confirm the no-shell call style before pinning `$(pwd)` rows — confirmed by orchestrator and by advocates b and c). Accepts moving the step off "first".
- advocate-b: 13 ACCEPT, INV-003 QUALIFY (print the absolute upstream uninstall whenever `$HOME/.local/bin/codebase-memory-mcp` exists, even if the matched entry points elsewhere) — adopted.
- advocate-c: 13 ACCEPT, INV-007 QUALIFY (the missing-CLI skip note must print the manual remove command, because direct exec drops alias-only `claude`) — adopted. Withdraws the exact-path request (INV-002).
Gate status after this round: all 14 ADDRESSED; gate cleared.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | Variant 1 | 90% | All three prefer A's section set (stale-primitive note, sunset). |
| S-002 | L1 | Variant 1 | 90% | B depends on A's text; C's matcher undefined; B and C conceded. |
| C-001 | L2 | Variant 1 (merged) | 92% | Automatic step in install; C conceded X-003 and withdrew the flag (R2). |
| C-002 | L2 | Variant 1 (merged with B's receipt/marker idea) | 90% | Registrations only + IronClaude files; B withdrew binary/uv-tool removal. |
| C-003 | L3 | Merge (all) | 88% | Provenance-tiered exact allowlist (B R2 split, INV-001/002 resolutions). |
| C-004 | L3 | Variant 1 | 95% | Non-fatal; all cite `set -euo pipefail` in `update.sh`. |
| C-005 | L2 | Tie (all) | 95% | All keep data and print delete commands. |
| C-006 | L2 | Merge (A for cbm, C for serena/Coder) | 88% | Bundle re-adds serena; handoff closes it. |
| C-007 | L3 | Variant 1 (modified) | 90% | B exceeds budget (300 s); hard cap via INV-007. |
| C-008 | L2 | Variant 1 (amended) | 88% | Binary-gated keep + absolute printed uninstall (INV-003/005). |
| C-009 | L3 | Variant 1 | 92% | Only A states missing-CLI behaviour; C's qualify adds the printed command. |
| C-010 | L2 | Variant 1 | 90% | Sunset table cheaper than a flag; C withdrew the flag. |
| X-001 | L3 | Variant 1 | 95% | `install_mcp.py:874-895` already removes exact entries without prompt; C conceded. |
| X-002 | L2 | Variant 1 / Variant 3 | 95% | uv tool is Coder's; B conceded. |
| X-003 | L2 | Variant 1 | 85% | `./update.sh` alone must suffice; residual for current serena pin recorded. |
| X-004 | L2 | Variant 3 (current pin) + Variant 1 (code-only rows) | 85% | Ambiguous rows handed off; provable rows removed. |
| A-001 | L3 | Merge | 90% | Allowlist built from repo history incl. pre-fork rows. |
| A-002 | L3 | Merge (provenance tiers) | 88% | Shape proves ownership only when one writer is possible. |
| A-003 | L3 | Variant 1 (modified) | 85% | Reached on every path (`main.py:189-275`), not `--force`-gated, own exception guard, freed slot. |
| A-004 | L3 | Variant 1 | 75% | Verify re-read + cause-specific warnings; CLI-side resolution UNVERIFIED (residual). |
| A-005 | L3 | Variant 2's order via Variant 1's skip-and-print | 88% | Keep registration while the binary exists; upstream uninstall first. |
| A-006 | L3 | Variant 2 direction + Variant 3 condition | 88% | Delete IronClaude files only once the binary is absent, existing predicates. |
| A-007 | L3 | Variant 1 | 85% | Restart note + doctor warning. |

Debate points credited (winner or co-winner): Variant 1: 21; Variant 2: 3 (A-005, A-006, C-002 partial); Variant 3: 4 (X-002, X-004, C-006, A-006 condition).

## Convergence Assessment
- Points resolved: 23 of 23
- Alignment: 100% (unanimous on every point after the resolution round; after Round 2 alone, 23/23 had at least a 2/3 majority)
- Threshold: 80%
- Taxonomy coverage: L1 = 2, L2 = 9, L3 = 12 (all levels covered; no forced taxonomy round needed)
- Invariant gate: BLOCKED after Round 2.5 (INV-001 HIGH) -> cleared by the invariant-resolution round
- Status: CONVERGED
- Unresolved points: none
