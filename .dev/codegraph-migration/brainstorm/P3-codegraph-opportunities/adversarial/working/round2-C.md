# Round 2 — Advocate C (variant-3-haiku-backend), sequential rebuttal (last)

Notation: A/B/C = variants 1/2/3; EVAL = `research/codegraph-evaluation.md`. Re-read for this round: `sc-pr-submit-protocol/SKILL.md:4,201-210`, `sc-implement-protocol/SKILL.md:118-119`, `cli/install_skill.py:46-53`, `sc-auggie-review-protocol/SKILL.md:128-140,214-219`, EVAL lines 96, 188-195. New measurements of my own are marked [measured].

## Response to criticisms

**1.** (round1-A W5, round1-B W1-2) "C drifts into 1:1 Serena swaps... four checkable errors."
Already conceded in Round 1; nothing new reopens it. What survives the concession, and what I defend: I-04's diff-hunk→symbol derivation and I-05's severity-semantics change are genuinely "beyond"; I-02 shrinks to composing with the Phase-3 plan and its MCP-only outline path is dropped (X-019). B's R2 New evidence 1 downgrades X-019 from "C wrong" to "both directions UNVERIFIED" (EVAL line 96 is an abbreviated usage line; line 195 proves `callers` takes an undocumented `--limit`). That does not rehabilitate my claim — EVAL still does not document CLI file mode — but the diff-analysis fact-check verdict should read "unsupported", not "refuted".

**2.** (round1-A W7, round1-B W3) "C's FR-05 can narrow VG-1"; "the `git diff | codegraph affected` pipeline is unproven under scoped Bash."
Conceded then; my New evidence 1 makes the concession stronger, not weaker: my design's failure mode was worse than "narrow" — see below, a replaced list can false-block the push outright. On the pipeline: pr-submit `:4` enumerates `Bash(git *), Bash(uv *), Bash(make *), Bash(jq *)` (re-read), so compound-command matching is exactly the unverified surface A's Q-2 named. Positional args (A) it is: C-014 moves to A.

**3.** (round1-A W8, round1-B W4, both R2 files) "C-007 'first probe authoritative' and FR-07 per-run caching contradict C's own A-006 concession"; "the tasklist risk note still changes tasklist output by index state."
Full concession on both — these are the two places my artifact conflicts with my own concessions, and A and B were right to press them after I half-fixed them in Round 1.
Fix for the first: the latch must split. Availability and provenance (`version`, `index_root == realpath(worktree)`) latch once per run; freshness is re-checked (`status`) before any query batch that follows an in-run write; cached rows are invalidated by that re-check, not held for the run (EVAL §4: no watcher without an MCP client). This is B's R2 item-3 resolution and it is correct; my C-007 moves to B and A-006 moves to REJECT.
Fix for the second: the tasklist file is a committed artifact; an `affects_n_callers` field sourced from local index state makes its bytes machine-state-dependent even when tiering never reads it. The graph number moves to the run ledger and the reviewer package; the task file keeps at most a static flag derivable from the task text alone. X-010 and C-016 move to A+B.

**4.** (round1-A W9, R2-A C-6) "A seam with no output schema pushes every consumer to invent its own degraded keys. C's own §6 shows free-form keys such as `test-scope:codegraph_stale`, which is the drift that C's I-01 says it prevents."
Conceded. A is right and the hit lands on the exact property I marketed. Free-form keys make degradation observable but not parseable, and per-consumer key invention is six divergent copies of the thing I-01 exists to prevent. I accept A's merge as stated in R2-A: C's PROBE→CALL→VERIFY→DEGRADE block becomes the body of the seam skill; A's closed `graph:*` vocabulary becomes its output schema; B's resolver script becomes its executable part. C-005 → A+B+C. My residual point survives inside the merge: the sequence text is the only artifact an implementing engineer can follow step-by-step, which is why A asked for it as the skill body rather than as a ref table.

**5.** (R2-A C-4 note) "C's '~300 ms' reuses A's own unverified number (X-017)."
Conceded — a citation error of mine. My Round 1 weakness 4 argued against A's SessionStart hook using A's unverified figure. EVAL §5.5 timed `query` (290 ms) and `callers` (297 ms); `status` was never timed. The hook deferral stands on the unmeasured-cost and extra-failure-surface grounds, not on a number.

**6.** (round1-B W10, R2-B item 9) "B's CLI-only stance ignores the measured 3-15 ms vs 290-300 ms gap"; B's rebuttal: artifacts are computed once per run per symbol, not per hunk, ~9 s for 30 symbols inside NFR-01's 15 s.
Concession from me: my Round 1 W6 framed the cost as "per-hunk loops (reflect Step 1B.3 over ≥3 tasks × hunks)", which misdescribes B's design — B computes artifacts once per run and pastes them. The arithmetic is B's and it holds for its call counts. What survives is the trigger, which B has now adopted: log the actual query count per run, and when serial CLI queries pass roughly 100 (about 30 s), switch the orchestrator's capability to the listed MCP tool via the capability map. C-002 becomes that combination.

**7.** (round1-B W10, R2-B item 4) "'grep misses are not graph misses' is asserted, not measured."
Split answer. Epistemically: conceded, EVAL states neither direction (X-020 = none as a factual claim). Operationally: I keep the corroboration-only rule, and note that B has now adopted it as the substance of its own C-019 reversal — its R2 moves cleanup-audit to my asymmetric rule precisely because neither coverage direction is proven. A rule both opponents implement is not a slogan anymore.

**8.** (R2-B New evidence 3) Per-subcommand allowlists vs bundled scripts: "the effective control is then the script body."
Accepted, and it is the sharpest operational point in Round 2. Control must attach to the code that actually executes; a pre-approved script path whose body runs any codegraph subcommand is an allowlist laundering surface (and `BASH_INSPECTION_POLICY.md` already forbids broad wrapper allowlists). Adopted: exact-path script patterns for closed-Bash consumers, and the subcommand grep extended to script bodies. My FR-06 mutation-exclusion grep already covers them — see New evidence 4.

**9.** (R2-A New evidence 6) The span lookup must bind `(file, startLine == def_line)` else `unresolved`.
Accepted and folded into FR-03: this is a precise trigger for my `dropped: ambiguous` reason, which I had left prose. The two-unrelated-`install`-functions sample (EVAL §5.6) is exactly the case my drop-never-repair rule exists for; the binding rule makes the drop mechanical.

## Updated assessment of A and B

**A.** Round 2 was a genuine correction pass: six withdrawals plus two findings against its own design (reinstall erasure of its kill switch; its NFR-08 de-registration claim wrong for CLI-default consumers). Its unique survivors are real — the user-typed `/sc:graph` owner, telemetry on the CLI path (U-002), language-scope honesty (U-003), the pre-edit step. Its C-6 counter against my free-form keys is the single most useful hit A landed on me. Remaining weaknesses: Class A/D MCP defaults still wait on B1/Q-4, so A's richest access tier is undeliverable in v1; and the capability map is a convention until a second access path actually exists (B's point, which B's own R2 concession partially answers by adopting the map).

**B.** Still the most disciplined variant, and its Round 2 concessions are all real: FR-17 withdrawn, FR-01 reconciled with §8, the D-05 sentence dropped, my C-019 adopted with a sensible spike gate, and C-002 given a measurement trigger. B's bundled-scripts question is the best new operational finding of the round. Remaining gaps: no lifecycle owner until it accepted A's (now settled), and its probe/resolver content still needs a body of procedure text to live in — which is what my sequence block becomes in the merged seam.

## New evidence (not presented in Round 1)

1. **[measured] The `affected` union can false-block through two distinct pytest exit codes, only one of which B's R2 covered.** B's New evidence 2 handles the stale-index-missing-path case. I ran the other case: `pytest <existing-file-with-no-tests>` exits **5** (no tests collected); `pytest <missing-path>` exits **4**; both non-zero, and `sc-pr-submit-protocol/SKILL.md:203-204` says "Any non-zero gate blocks the push". So an `affected` entry that resolves to a *real* file collecting zero tests also blocks a correct push — `git ls-files` filtering does not catch it, because the file exists. Union-stage guard: pre-pass `pytest --collect-only -q`, drop paths collecting zero tests, fall back to `<changed-area>` on any collection error; the NFR-08 backtest must record both the collection-error and zero-collect rates.
2. **[measured] Rollback-by-deletion is operational fiction after install.** `install_skill.py:47-52` does `shutil.rmtree` + `copytree` under `force`, and `./update.sh` runs `superclaude install --force` (EVAL §2). Any local deletion of codegraph text — my NFR-05 mechanism — is erased on the next update. Rollback must be a source-level revert plus release; the runtime switch is the binary being off PATH (B's NFR-07 test). Partial concession on C-033: my claim holds only inside the dev loop, not as an operational rollback.
3. **Self-correction: my own §8 ambiguity row and I-04 say "pin with `file`", but `file` is documented only on the MCP tools** (EVAL §3: `codegraph_callers`/`codegraph_node` parameter tables); the CLI usage line (EVAL line 96) shows no `file` for either. With B's finding that the usage line is abbreviated, the correct state is: MCP-documented, CLI-UNVERIFIED. Closure is one command per subcommand: capture `codegraph callers --help` and `codegraph node --help` before Phase 3.
4. **[measured] My FR-06 grep already covers skill-bundled scripts.** Eight scripts live under `skills/*/scripts/` (cleanup-audit, crash-recovery ×2, implement, pr-submit ×4), all inside the grep path `src/superclaude/{skills,...}`. Adopting B's extend-the-grep-to-script-bodies costs nothing in my test; it is a wording change.
5. **[measured] Containment baseline is exactly zero.** `grep -i codegraph` over `src/superclaude/` returns 0 hits today. Every codegraph mention after adoption is attributable to the migration PRs by construction, so A's NFR-03 count needs no baseline archaeology and the drift check starts from a clean state.

## Shared assumptions — changes only

| A-ID | New position | Reason |
|---|---|---|
| A-006 | REJECT (was QUALIFY) | As stated ("one probe per run is enough") it is wrong for implement/pr-submit, which edit mid-run, and for CLI-only sessions where no watcher runs (EVAL §4). The split survives: availability latches once, freshness re-checks after in-run writes |

## Updated per-point positions

| ID | Superior | Changed? |
|---|---|---|
| S-001 | A | no |
| S-002 | none | no |
| S-003 | C | no |
| S-004 | A | no |
| S-005 | B | no |
| S-006 | B | no |
| S-007 | A+B (A's Layer 0 + B's confidence weight) | yes |
| S-008 | A+B | no |
| S-009 | A | no |
| S-010 | A+C (A's invariants + C's edge-case table) | yes |
| S-011 | B | no |
| C-001 | A+B | no |
| C-002 | combination: B for v1; A's MCP classes after measurement; logged query count (~100 serial calls) is the switch trigger | yes |
| C-003 | B | no |
| C-004 | B | no |
| C-005 | A+B+C (A's map and closed vocab, B's probe/resolver, C's sequence text as the skill body) | yes |
| C-006 | A+B | no |
| C-007 | B (never sync; availability latched, freshness re-checked after in-run writes) | yes |
| C-008 | A+B (A's no-primitive-step-names-explore grep, B's routing block against unprompted calls to the one always-listed tool) | yes |
| C-009 | A+B+C (typed resolution, B's resolver with the (file,startLine) binding, C's drop-never-repair) | yes |
| C-010 | B+C | no |
| C-011 | A+B (pre-edit as warning/Q3 input, post-edit on the actual diff) | yes |
| C-012 | B (context-only stage 1, shadow-mode counting stage 2) | no |
| C-013 | B | no |
| C-014 | A (positional args; FR-13 escalation makes `--stdin` surplus) | yes |
| C-015 | A | no |
| C-016 | A+B (graph numbers to ledger/reviewer package, not the committed task file) | yes |
| C-017 | B | no |
| C-018 | B | no |
| C-019 | C (asymmetric rule; B's orchestrator-only + spike gate accepted) | no |
| C-020 | B (defer; no MCP in v1 agents, candidates not precomputable) | yes |
| C-021 | A (light edits; N-3 deferred by B itself) | yes |
| C-022 | B | yes |
| C-023 | A | no |
| C-024 | B | no |
| C-025 | A+B | yes |
| C-026 | A+B+C (adds C's `sync` drop) | yes |
| C-027 | A+B (seam, /sc:impact, /sc:test-scope, /sc:graph; `/sc:ground` folds into the seam ref — a command wrapper added nothing once the skill owns the resolver and vocabulary) | yes |
| C-028 | A+B (A's modes and caps, B's prod/test split; `--diff` and `file`-pin need the CLI doc capture) | yes |
| C-029 | B | no |
| C-030 | B | no |
| C-031 | A+B+C (B's fixtures/backtest, A's containment count, C's mutation-exclusion grep over primitives and script bodies) | yes |
| C-032 | A+B | yes |
| C-033 | A+B (source-level revert/release + binary-absent runtime switch; delete-the-text holds only in the dev loop) | yes |
| X-001 | B | no |
| X-002 | B | no |
| X-003 | B | no |
| X-004 | B+C | no |
| X-005 | A | no |
| X-006 | B+C | no |
| X-007 | B | yes |
| X-008 | B (backtest extended with zero-collect and collection-error rates before any union) | no |
| X-009 | B (shadow mode, then enable on counts) | no |
| X-010 | A+B (tasklist artifact stays deterministic; risk data to the ledger) | yes |
| X-011 | A+B (gated on existing symbols, informational, FR-07 applies) | yes |
| X-012 | C | no |
| X-013 | B | no |
| X-014 | A+B | yes |
| X-015 | A | no |
| X-016 | A (status line only; B withdrew FR-17) | yes |
| X-017 | B | no |
| X-018 | A | no |
| X-019 | B (both CLI claims unverified; closure = `--help` capture before Phase 3) | no |
| X-020 | C as an operational rule (corroboration-only, now implemented by all three); none as a factual claim | no |
| X-021 | B | no |
