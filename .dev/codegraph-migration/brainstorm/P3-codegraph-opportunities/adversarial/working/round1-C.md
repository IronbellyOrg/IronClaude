# Round 1 — Variant C (backend/haiku) positions

## Position summary

Codegraph is a dependency with a contract, not a tool list: one shared PROBE→CALL→VERIFY→DEGRADE sequence (my §2) makes idempotency, fail-open and rollback free by construction, because primitives only ever hold the read-only five verbs and never touch index state (FR-06, FR-07). My distinctive, defensible core is the asymmetric evidence rule (graph positives act, graph emptiness never does), the mutation-exclusion grep test, and the docs-only-diff escalation key. I concede upfront: C-001 scope drift, the X-002 allowlist self-contradiction, the X-008 "replace can narrow" gate design, X-013 tests-in-severity, and the X-015/X-018/X-019 fact-check losses.

## Steelman

### Variant A (architect)

The strongest version of A: it is the only variant that enumerated the full operational blocker surface — B5 telemetry on the CLI path (Bash calls do not inherit the MCP entry's `CODEGRAPH_TELEMETRY=0`; EVAL §1 says telemetry is default-on), B7 (node file mode is invisible to the `Read` freshness matcher, `hooks.json:59`), U-003 (Markdown-heavy repos get no graph signal, EVAL §5.4: python/yaml/liquid only). Its `resolution: def-line|call-site-verified|unresolved` field is the most engineered citation mechanism, it found `query --json` `endLine` (EVAL §5.5) to bound call-site Grep, and its capability-map seam (consumers name capabilities, not tools) is the right abstraction against a single-maintainer upstream shipping 8 releases/quarter (EVAL §1). A genuinely gets right: the blocker table with owners, `/sc:graph` as a dedicated, user-typed init owner, and pre-fix impact in remediation chains (U-006).

### Variant B (analyzer)

The strongest version of B: its M/P/A evidence classes refuse to rank unmeasured benefit as equal to measured, and that discipline produced the two best catches in the debate — U-009 (the 20-of-23 callers sample held 2 production callers and 18 test functions, EVAL §5.5, so a naive 1:1 swap trips reflect's ">5 referencing call sites" HIGH rule on tests alone) and U-010 (the NFR-08 backtest gate before any VG-1 change, since EVAL never ran `affected`). Its artifact-in-brief access model removes the `CODEGRAPH_MCP_TOOLS` blocker with zero env dependency by following repo precedent (`sc-troubleshoot-protocol/SKILL.md:281` producers table; reflect reviewers audit pre-computed hunks), and its golden fixtures (U-012) are the correct defense against text-output drift. B genuinely gets right: B7 (no documented `--json` for `callers`/`impact`/`status`, EVAL §3), the provenance check (`index_root` == worktree realpath), and the honest "status timing UNVERIFIED".

## Strengths claimed

1. **The contract sequence is the idempotency and rollback story in one artifact.** §2's fenced PROBE→CALL→VERIFY→DEGRADE block with a run-scoped latch (FR-02: one probe, never retried) and FR-07 (cache per run, one affected computation per validation cycle) is the only proposal where re-running a wave is provably side-effect free. EVAL §5.7 ("scripts must not rely on `codegraph sync` succeeding while an agent session is open") makes A's try-one-sync a latent flake; my FR-06 mutation-exclusion grep (`codegraph (init|index|sync|uninit|unlock|upgrade|install)` → 0 hits) is machine-checkable.
2. **Asymmetric evidence is fail-safe where A is fail-risky.** My I-07: `impact > 0` upgrades a DELETE to REVIEW; `impact = 0` proves nothing. A's I-12 uses "zero graph callers is extra evidence for DELETE" — the graph has no text search and misses string/config references (EVAL §6.1), so A's direction can manufacture false DELETEs; mine can only add conservatism. The cleanup-audit grep gate (`sc-cleanup-audit-protocol/SKILL.md:75`, verified) stays untouched either way.
3. **The edge-case table maps every observed EVAL behavior to a contract response** (§8: uninitialized sibling, nested-worktree-with-warning, writer lock, `install` ambiguity, "Showing 20 of 23" truncation, docs-only diff, CLI-vs-MCP latency, connect-time catch-up). Neither A nor B gives a row-per-behavior mapping; U-018/U-021/U-022 (stale→HIGH-as-MEDIUM; docs-only diffs may honestly yield no tests) came out of it.
4. **Nine-vector coverage is declared up front with net positions** (§1 table), so a reader can audit vector coverage before reading ideas. A has no explicit map; B buries it in §4.
5. **`source: graph|heuristic|none` provenance in `/sc:test-scope` (C-3/FR-05)** makes test-selection provenance observable in the run-log next to the VAL gates, and FR-05's escalation keys on source-file diffs so a docs-only diff may honestly yield no tests (U-022) while a src diff with empty graph output can never silently skip tests.
6. **CLI-first for Bash-capable orchestrators is available today.** A's Class A default (MCP for troubleshoot/reflect) is gated on B1, an unowned installer env change (EVAL §7 step 5 sets only telemetry vars). My position needs no blocker resolution for the highest-frequency consumers.
7. **`/sc:ground` (C-4) centralizes FR-03 enforcement**: graph locates, Read verifies, dropped rows carry reasons (`no_match|unverified|ambiguous`). This keeps re-Read-before-cite enforceable in one place rather than re-implemented per consumer.
8. **Dropped ideas include the two hygiene drops others missed**: any primitive running `sync` (writer lock, EVAL §5.7) and splitting `/sc:impact`//`sc:test-scope` into per-skill private scripts, which would recreate the six-divergent-copies drift I-01 exists to remove.

## Weaknesses identified in other variants

1. **A's "try one `sync`" (X-006)** is a mutation from a read path that EVAL §5.7 explicitly warns against; even the success case (CLI-only session, no daemon) makes a "read-only grounding" step write index state, breaking A's own NFR-07 ("no new side effects").
2. **A binds VG-1 to an unmeasured command.** Immediate union (FR-07) is direction-safe (never narrows) but EVAL never ran `affected` (A-008, conceded by B alone); B's advisory→backtest→union sequencing is the operationally correct order. A also claims `status` ≈ 300 ms "EVAL §5.5" (X-017) — §5.5 timed `query`/`callers` (290/297 ms); status timing was not captured.
3. **A edits the evidence-validator and lists it in Class D for MCP names** (X-004). Even as text-only, teaching the independent last gate to treat def-line rows as a special citation class weakens the one validator whose job is disk-truth; B and I keep it `Read, Grep, Glob`.
4. **A's I-17 SessionStart hook** adds a ~300 ms CLI call to every session start, including repos with no `.codegraph/`; B's D-03 (the probe already answers on demand; `freshness-pre-edit.sh` timeout is 1 s) is decisive.
5. **B's `dependent-impact` exemption from the out-of-hunk downgrade (X-009)** is the boldest gate change in the debate, built on Class P (self-admitted UNVERIFIED benefit) and a Python-regex hunk-to-symbol extractor (B's own OQ-7 doubts non-Python). The Read-verified guard is well designed, but it should land behind B's own backtest discipline, not before it.
6. **B's CLI-only-everywhere stance ignores the measured 3-15 ms MCP vs 290-300 ms CLI gap** (EVAL §5.6) for per-hunk loops — reflect Step 1B.3 over ≥3 tasks × hunks at 300 ms per call compounds; my edge-case table names this and prefers MCP where listed.
7. **B's `/sc:load --index` runs `init` inside an onboarding command** (X-005/X-016): a 34 MB, ~1 GB-RSS write path (EVAL §5.4) inside `/sc:load`, however flag-gated, mixes mutation into context-loading; A's dedicated `/sc:graph` that refuses nested worktrees without `--worktree-local` is the cleaner ownership.
8. **B's "Grep sees every static reference the graph sees" (D-05, X-020) is asserted, not measured** — EVAL states neither direction; it reports "Linking dynamic dispatch" at index time (§5.4) and interface→impl dispatch via explore (§6.2). Both B's slogan and mine ("grep misses ≠ graph misses") are UNVERIFIED; the safe operational rule is corroboration-only in either direction, which is what I-07 actually implements.

## Concessions

1. **C-001 scope drift is real.** I-02's "replace Serena overview/find_symbol rows", I-04's `find_declaration` anchoring and I-05's `find_referencing_symbols` replacement overlap the INV §4 1:1 work the seed scoped out; only I-04's diff-hunk→symbol derivation and I-05's severity-semantics change are genuinely "beyond". I-02's framing should be rewritten as a Tier-1 restructure that composes with the 1:1 plan.
2. **X-002 self-contradiction.** My §2 says "no allowlist change beyond adding `Bash(codegraph *)` patterns" and I-07 uses a `;`-joined pattern, while my FR-10 forbids bare `Bash(codegraph *)`. FR-10 is the correct half; B's per-subcommand rule is the resolution I adopt.
3. **X-008/C-013: my test-selection design can narrow the gate.** FR-05's "tests is exactly the parsed affected list" replaces `<changed-area>` and can shrink today's set on an unmeasured command (A-008). B's advisory→backtest→union order is superior; my surviving contribution is the `source:` provenance field and the docs-only-diff rule, which fold into B's union stage.
4. **X-013/C-017: "re-word to caller count (tests included)" is measurably wrong.** EVAL §5.5's sample: 2 production callers among 23. B's prod-only distinct-caller count (FR-09, runtime-surface table) is required; my stale→HIGH-as-MEDIUM demotion (U-021) remains a good addition on top.
5. **X-015: I cited the wrong wave's budget.** Verified: `sc-troubleshoot-protocol/SKILL.md:218` sets Wave 1 (Tier 1) at ~3k tokens; `:256` is Wave 1.5's 2k. My I-02 and NFR-02 both misattribute 2k to Tier 1.
6. **X-018: my MCP tool names would not match.** EVAL §3 names the tools `codegraph_search`, `codegraph_callers`, …, so the server-prefixed names are `mcp__codegraph__codegraph_*` (A's form). My `mcp__codegraph__search`-style entries in read-only-agent `tools:` lines would silently fail.
7. **X-019: CLI `node [name]` does not document file/symbolsOnly mode** (EVAL §3 CLI table); my I-02 claim "skill has Bash → CLI works today" is unsupported for the file-outline path — file-mode node is MCP-only, which is B1-blocked. I-02's CLI path must fall back to `query --json`/Grep outlines.
8. **A-006 bites my design too:** my FR-07 caches graph results for the whole run while implement/pr-submit edit files mid-run, so post-edit queries can read a pre-edit index. FR-03's re-Read drops stale rows, but B's re-probe-before-queries after in-run edits is the stronger freshness floor.

## Shared assumptions

| A-ID | Position | Reason |
|---|---|---|
| A-001 | ACCEPT | Seed constraint; my NFR-01/FR-01 encode it with a degraded key per step |
| A-002 | ACCEPT | EVAL §5.5 definition-line gap; my FR-03 makes re-Read the only citation-grade bridge |
| A-003 | QUALIFY | The policy (explore never a default step) stands on its own measured cost (24,913 chars, EVAL §5.6); the auggie-is-free rationale does not — auggie itself is fallible (troubleshoot already accepts a Glob/Grep floor), so fallbacks must chain to Grep/Read, not to auggie |
| A-004 | QUALIFY | Sample of one; the ban costs nothing so keep it, but a bounded `maxFiles≤5` single-symbol measurement would close the question |
| A-005 | QUALIFY | EVAL §5.5-§5.6 measured latency only, never output size; my ~1k caps are estimates — enforce caps, don't assume cheapness |
| A-006 | QUALIFY | Latch is right for availability, wrong for freshness: no watcher runs in CLI-only sessions (EVAL §4) and orchestrators edit mid-run; re-probe `status` before graph calls that follow in-run writes |
| A-007 | QUALIFY | Verified on one symbol (§5.5); my I-03 already calls the callers list "a floor, not exhaustive" — treat non-empty as partial, never complete |
| A-008 | REJECT (for gates) | EVAL never ran `affected`; usable advisory-only until B's NFR-08 backtest passes — my I-09 as written violates this and must adopt the backtest |
| A-009 | ACCEPT | init writes ~34 MB at ~1 GB peak RSS (EVAL §5.4); read-only flows must never init |
| A-010 | ACCEPT | EVAL §5.8 warning text is pinned behavior; foreign-index rows are citations of another tree |
| A-011 | QUALIFY | No owner exists (EVAL §4, §7); consumers must ship anyway (fail-open), and degraded-key frequency in audit logs is the signal for when to fund an init owner |
| A-012 | QUALIFY | Orchestrators invoke a peer skill; agents Read refs by installed path (EVAL §3: subagents never see server instructions, so ref-by-path is the only channel); B's Skill-call-cost question (Q-6) is real — my C-1 is guidance-only with no args/output to minimize it |

## Per-point positions

| ID | Superior | Reason |
|---|---|---|
| S-001 | A | Traceable front matter incl. ground_truth and date |
| S-002 | none | Identical section order across variants |
| S-003 | C | Nine-vector table with net positions in §1 is auditable before reading ideas |
| S-004 | A | 7 lettered classes + B1-B7 owner table is the most complete access model |
| S-005 | B | M/P/A evidence classes beat raw V/E/R scales and my nothing |
| S-006 | B | 10 ideas, each evidence-classed, no filler |
| S-007 | B | Score table with stated method, sequencing and coverage notes |
| S-008 | A+B | IDed drops cross-reference cleanly; my bullets do not |
| S-009 | A | Per-candidate subsections carry full interface detail |
| S-010 | C | Observed-behavior→contract-response table maps every EVAL edge to a FR |
| S-011 | B | Most specific requirements, incl. golden fixtures and backtest |
| C-001 | A+B | Both exclude the 1:1 swaps; I drifted (conceded) |
| C-002 | B+C | CLI-first orchestrators (C, no blocker) composes with artifact-in-brief agents (B) |
| C-003 | B | Do not set the env in v1; measure schema overhead first |
| C-004 | B | Per-subcommand patterns; my own FR-10 agrees, my §2 text erred |
| C-005 | C | Guidance-only contract, no args/output, lowest coupling; A's capability map is the better backend-swap abstraction and should merge in |
| C-006 | A+B | A's closed vocabulary + B's `parse_failed`; my binary available/unavailable under-discriminates |
| C-007 | C | Never sync; first probe authoritative + stale flag; A's try-one-sync is the flake |
| C-008 | A | Ban explore from primitives entirely; my maxFiles door adds surface for no consumer need |
| C-009 | B | Resolver script with measured `query --json` span + in-span Grep + Read is the most concrete |
| C-010 | B+C | Validator stays Read/Grep/Glob (B and C agree); A's edit risks the independent gate |
| C-011 | A | Pre-edit Q1 impact plus pre-fix impact in remediation chains is the fullest coverage |
| C-012 | B | Blast-radius artifact + Read-verified `dependent-impact` is the only fix for the chunking blind spot |
| C-013 | B | Advisory→backtest→union; my replace-form can narrow the gate (conceded) |
| C-014 | B | Positional args / `--stdin` from file; pipeline matching under scoped Bash is UNVERIFIED |
| C-015 | A | search+node+callers in Wave 1 and 1.6 as one edit; my split is thinner and I-02's CLI claim failed X-019 |
| C-016 | C | Informational risk note in both workflow and tasklist; determinism intact because it never feeds tiering |
| C-017 | B | Prod-only distinct callers; the 2-of-23 sample makes test-inclusive counts wrong |
| C-018 | B | No new reflect field in v1; `degraded_components` only, zero parser risk |
| C-019 | C | Asymmetric: positive upgrades to REVIEW, empty proves nothing; A's zero-callers-DELETE-confidence is fail-risky |
| C-020 | A | Caller-liveness check closes a real false-recommendation class |
| C-021 | B | structure-brief + load --index is the most substantive onboarding move |
| C-022 | B+C | No new hooks; the probe answers on demand (B's D-03 latency argument) |
| C-023 | A | Dedicated `/sc:graph`, user-typed, refuses nested worktrees; I left B2 unowned |
| C-024 | B | Confidence-weighted ranking is the most defensible method |
| C-025 | A | Layer-0 allowlists→contract→citation is the true dependency order; my #2 (affected) was premature |
| C-026 | B | Best-evidenced drops (hook latency vs 1 s timeout, producer enumeration is text search) |
| C-027 | C | Four candidates incl. `/sc:ground`, the shared verify layer that centralizes FR-03 |
| C-028 | B | Prod/test partition, truncated, ambiguous, unmapped_files — richest and best semantics |
| C-029 | B | Widest caller set incl. load, index-repo, explain |
| C-030 | B | Shown/total + one re-query ≤100 + notes CLI callers lacks a file arg |
| C-031 | B | Golden fixtures + backtest are the strongest guards against measured drift risk |
| C-032 | A | Telemetry-on-CLI-path and Markdown-repo honesty are the two highest-value risk finds |
| C-033 | C | Delete-the-text rollback restores today's behavior byte-for-byte; no kill switch to maintain |
| X-001 | B | No MCP names in v1; artifacts by path remove the blocker entirely |
| X-002 | B | Never wildcard; my FR-10 was right, my §2 wording was not |
| X-003 | B | Defer the env decision with a measurement gate |
| X-004 | B+C | Validator keeps Read/Grep/Glob |
| X-005 | A | User-typed dedicated command owns init; B buries it in /sc:load, C forbids all |
| X-006 | B+C | Never sync from primitives (EVAL §5.7) |
| X-007 | B+C | No SessionStart hook |
| X-008 | B | Backtest before any gate change |
| X-009 | B | Read-verified exemption only, landed after the backtest |
| X-010 | C | Risk field is informational; determinism concern applies to tiering, which I do not touch — label it `graph_derived` so reflect never reads it as fact |
| X-011 | A | Adoption plus caller files named in acceptance criteria is more actionable than my count-only field |
| X-012 | C | Asymmetric evidence; empty is never proof |
| X-013 | B | Prod-only distinct caller symbols |
| X-014 | A | Total primitive ban; no step needs explore |
| X-015 | A | Correctly cites :218 ~3k; I cited Wave 1.5's 2k (conceded) |
| X-016 | B | load gains an index owner; A's status line is thinner, my drop orphans B2 |
| X-017 | B | "status timing UNVERIFIED, measure" is the accurate read of EVAL |
| X-018 | A | `mcp__codegraph__codegraph_*` is the correct form; mine would not match |
| X-019 | B | File-mode node is MCP-only; mechanisms resting on `query --json` are measured |
| X-020 | C | Operationally: corroboration-only in both directions; epistemically both slogans are UNVERIFIED |
| X-021 | B | Reads only the 20 shown rows; the 3 hidden stay unknown |
