# Round 2 — Advocate A (variant-1-opus-architect), sequential rebuttal (first)

Notation: A/B/C = variants 1/2/3; EVAL = `research/codegraph-evaluation.md`. Primitive paths are relative to `src/superclaude/` and were re-read for this round: `agents/evidence-validator.md:5,62-66`, `skills/sc-pr-submit-protocol/SKILL.md:203-206`, `skills/sc-implement-protocol/SKILL.md:118-119`, `cli/install_skill.py:47-52`.

## Response to criticisms

**B-1.** "A's formula multiplies by a 'Frequency' factor that is also subjective" (round1-B Strength 1).
Partial concession. Frequency is closer to observable than Value, because it records how often the host primitive runs (every PR, every level-3 run). B concedes its own V is judgement too (B Concession 9). But the real flaw is a different one: A's formula has no confidence term. It ranked I-06 and I-08 at 5 and 6, and both rest on `affected`, which EVAL never ran (EVAL §5 has no `affected` run). B's M/P/A weight would have demoted both. The merged ranking should take B's confidence multiplier on top of A's Layer 0.

**B-2.** "A greps 'after the def line' with no end bound (I-02), which can match a different function in the same file" (B Strength 4).
Mostly wrong on the facts. A's I-02 mechanism column says "`codegraph query <s> --json` gives `startLine`/`endLine` (EVAL §5.5) to bound the search" (variant-1 line 61), and C's Round 1 steelman credits A with exactly this bound. Concession: the bound appears only in the mechanism column. It is missing from the idea's procedure and from FR-04, so an implementer could miss it. B's `resolve-callsite.sh` makes the same mechanism executable and testable, so it is the better delivery. See New evidence 6 for a gap that both A and B share.

**B-3 / B-4 / B-5 / B-8 / B-9.** These cover the wildcard `Bash(codegraph *)`, MCP names in read-only agents, evidence-validator in Class D, "try one `sync`", "~300 ms" for `status`, and "zero callers is DELETE evidence". A conceded all six in Round 1 (round1-A Concessions 1-6), and nothing in B's or C's defenses reopens them. A's Layer 0 I-03 therefore shrinks to per-subcommand CLI patterns in Class C only.

**B-6.** "A unions `affected` into VG-1 at once (X-008) on a tool EVAL never ran" (B Weakness 8). C says the same but calls the union "direction-safe" (C Weakness 2).
Full concession, and a stronger one than Round 1. A's Strength 8 claimed the superset is "safe by construction". That holds only against *missed* tests. VG-1 is `uv run pytest <changed-area>`, and "Any non-zero gate blocks the push" (`sc-pr-submit-protocol/SKILL.md:203-206`). So a union that adds a wrong or uncollectable path from an unparsed `affected` output fails VG-1 and blocks a correct push. (Pytest exits non-zero on a path it cannot find; this is general pytest behaviour, not re-checked here.) A union can therefore produce false blocks as well as extra runtime. B's sequence is required before any gate change: advisory delta first, then the 20-change backtest (NFR-08), then the union. A's `selected ⊇ heuristic` rule (FR-07) survives only as the invariant that governs the union stage.

**B-7.** "A's 19 ideas include a tail with its own admitted score of 0.7-1 … A formula the author overrides is not a method" (B Weakness 9).
Partial concession. The I-16 override was disclosed with its reason ("duplicates I-17/I-19"). Now that I-17 is deferred, that reason is weaker and I-16 rises back to its formula rank. Accepted trims: drop I-15 (score 0.7; Glob already gives the structure). Rewrite I-12 to C's asymmetric rule. Fold I-09 into the review merge as stage 1 (context only). Defer I-11 (see C-020). The architecture value of A is the scaffold (C-1..C-4), not the count of ideas.

**C-3.** "A edits the evidence-validator … teaching the independent last gate to treat def-line rows as a special citation class weakens the one validator whose job is disk-truth" (round1-C Weakness 3).
Counter on "weakens": A's FR-04 test asks the validator to *reject* a def-line row cited as a call site (`line-mismatch`), which makes it stricter, not looser. Concession on the edit itself: it is unnecessary. The validator already Reads ±5 lines and compares the quoted snippet, and rejects semantic differences (`evidence-validator.md:62-66`). A call-site snippet cited at `main.py:46` would face `def install(` there (EVAL §5.5) and fail today. So the validator stays byte-identical, and the `resolution` rule lives only in the producer ref (C-1 `refs/citation-resolution.md`).

**C-4.** "A's I-17 SessionStart hook adds a ~300 ms CLI call to every session start" (C Weakness 4).
Conceded as deferral (Round 1 Concession 8). Note that C's "~300 ms" reuses A's own unverified number (X-017). The cost is unmeasured in both directions.

**C-5.** C-033: "Delete-the-text rollback restores today's behaviour byte-for-byte; no kill switch to maintain" (round1-C per-point).
Partial concession, backed by new evidence (New evidence 1-2). A's FR-16 switch is a source-level switch, not a runtime one. It is still cheaper than a multi-file revert, because flipping one header disables every consumer, which deleting text across about 10 primitives does not. Merge: FR-16 as the release-level switch, plus B's "binary absent equals the native path" as the runtime switch.

**C-6.** C-005: "Guidance-only contract, no args/output, lowest coupling" (C per-point).
Counter. A seam with no output schema pushes every consumer to invent its own degraded keys. C's own §6 shows free-form keys such as `test-scope:codegraph_stale`, which is the drift that C's I-01 says it prevents. Concession: C's PROBE→CALL→VERIFY→DEGRADE block is the clearest procedure text and should be the body of A's C-1 `SKILL.md`.

**C-8.** X-016: "load gains an index owner; A's status line is thinner, my drop orphans B2" (C per-point).
Counter: B itself picks A's dedicated `/sc:graph` over its own `/sc:load --index` (round1-B C-023, X-005), because `init` writes 34 MB at about 1 GB RSS (EVAL §5.4). A one-line status in `/sc:load` that points to `/sc:graph init` gives the visibility without putting a mutation inside a context-loading command.

## Updated assessment of B and C

**B.** B's defenses hold on every gate-safety point, and its concessions are accurate: X-021 (20 of 23 inspected), X-020, telemetry, language scope, and its FR-12 being the riskiest change. B is the superior variant on evidence discipline and on the v1 access model. Its remaining gaps are architectural ones that B partly accepts (round1-B C-005, C-023, C-027 all pick A+B or A): it has no capability map, no lifecycle owner, and no release-level switch. Two of its own claims are in tension and should be reconciled in the merge: "probe once per run" (FR-01) and "re-run `status` before the queries" (§8).

**C.** C's concessions are broad and honest: C-001, X-002, X-008, X-013, X-015, X-018, X-019 and A-006. That leaves three durable contributions: the asymmetric cleanup rule (X-012), the edge-case table with the docs-only-diff rule (U-022), and the mutation-exclusion grep (FR-06). C's remaining positions conflict with its own concessions. C-007 "first probe authoritative" and FR-07 per-run caching both contradict C's A-006 concession, and the tasklist risk note (X-010) still changes tasklist output by index state. C's strongest new point against B is real: MCP calls take 3-15 ms against about 300 ms for the CLI (EVAL §5.5, §5.6). That supports a later MCP stage for loop-heavy orchestrators, and it argues for A's capability map, where switching access path is a one-file change.

## New evidence (not presented in Round 1)

1. **The kill switch is erased by reinstall.** `cli/install_skill.py:47-52` runs `shutil.rmtree` and then `copytree` under `force`, and `./update.sh` runs `superclaude install --force` (EVAL §2). A user who flips `status: disabled` in `~/.claude/skills/sc-graph-grounding/refs/capability-map.md` loses the change on the next update. FR-16 therefore needs a source edit and a release.
2. **A's NFR-08 is partly wrong.** It says "removing the codegraph registration … makes every consumer degrade". Class B/C consumers default to the CLI (A §2.1), and CLI subcommands do not depend on the MCP registration (EVAL §3, §5.5 ran the CLI without MCP). The runtime off switch is the binary being off PATH (B's FR-01 test), not de-registration.
3. **Pinning by file is MCP-only.** CLI `callers <symbol>` takes no file argument, and `node [name]` has no file or `symbolsOnly` mode (EVAL §3 CLI list; B noted the first under C-030). So A's ambiguity rule "always pass `file`" (§8), I-09, and C-2 `--diff` hunk-to-symbol mapping work only on the MCP path, which is B1-blocked. On the CLI path they need `query --json` matches filtered by file, or an IronClaude-side extractor (B's approach). C-2 `--diff` is not v1-ready on the CLI.
4. **A false block is a real failure mode of the union.** See B-6: `sc-pr-submit-protocol/SKILL.md:203-206`.
5. **Pre-edit impact cannot license edits outside the task.** `sc-implement-protocol/SKILL.md:118-119` reads "Implement only that task", and a drive-by file is a minor unless a breach applies. A's I-05 output should therefore feed the Q3 review package and the ledger, not widen Q1 edits. B's post-edit check covers what actually changed. The two are complementary (C-011 becomes A+B).
6. **The span lookup is itself ambiguous.** `query` is a name search. The explore sample matched two unrelated `install` functions (`eval/signal_handler.py:195`, `cleanup_audit/process.py:57`; EVAL §5.6). A resolver that runs `query <caller> --json` must select the match whose file and `startLine` equal the caller row's file and def line, and it must mark the row `unresolved` otherwise. Neither A's I-02 nor B's `resolve-callsite.sh` states this.

## Shared assumptions — changes only

| A-ID | New position | Reason |
|---|---|---|
| A-008 | REJECT (as a v1 gate input; was QUALIFY) | EVAL never ran `affected`, and a union can false-block VG-1 (`sc-pr-submit-protocol/SKILL.md:203-206`), not only inflate it. `affected` is advisory until B's NFR-08 backtest passes |

## Updated per-point positions

| ID | Superior | Changed? |
|---|---|---|
| S-001 | A | no |
| S-002 | none | no |
| S-003 | C | no |
| S-004 | A+B | no |
| S-005 | B | no |
| S-006 | A+B | no |
| S-007 | A+B (Layer 0 + B's confidence-weighted table) | yes |
| S-008 | A+B | no |
| S-009 | A+B | no |
| S-010 | A+C | no |
| S-011 | none | no |
| C-001 | A+B | no |
| C-002 | B+A (B artifacts for v1 agents; A's Class A MCP once listed) | no |
| C-003 | B | no |
| C-004 | B | no |
| C-005 | A+B+C (A's map/schema, B's probe/resolver, C's sequence text) | yes |
| C-006 | A+B | no |
| C-007 | B | no |
| C-008 | A | no |
| C-009 | A+B+C (typed resolution, B's resolver + file/startLine match, C's drop-never-repair) | yes |
| C-010 | B+C (validator unchanged) | yes |
| C-011 | A+B (pre-edit for named symbols, post-edit on the actual diff) | yes |
| C-012 | A+B | no |
| C-013 | A+B (B's sequence, A's invariant at the union stage) | no |
| C-014 | A | no |
| C-015 | A+B | no |
| C-016 | A | no |
| C-017 | B | no |
| C-018 | B | no |
| C-019 | C | no |
| C-020 | B (defer; agents have no MCP in v1, and candidates cannot be precomputed) | yes |
| C-021 | A (minus I-15) | no |
| C-022 | B | no |
| C-023 | A | no |
| C-024 | A+B | no |
| C-025 | A+B | no |
| C-026 | A+B+C (adds C's `sync` drop) | yes |
| C-027 | A+B (A's four slots, B's probe/blast-radius content) | yes |
| C-028 | A+B (A's modes and caps, B's prod/test split; `--diff` MCP-gated) | yes |
| C-029 | A | no |
| C-030 | B | no |
| C-031 | A+B | no |
| C-032 | A+B | no |
| C-033 | A+B (source switch + binary-absent runtime switch) | yes |
| X-001 | B | no |
| X-002 | B | no |
| X-003 | B | no |
| X-004 | B+C | yes |
| X-005 | A | no |
| X-006 | B+C | no |
| X-007 | B | no |
| X-008 | A+B | no |
| X-009 | A+B | no |
| X-010 | A+B | no |
| X-011 | A | no |
| X-012 | C | no |
| X-013 | B | no |
| X-014 | A | no |
| X-015 | A+B | no |
| X-016 | A | no |
| X-017 | B | no |
| X-018 | A | no |
| X-019 | B (A's I-09 and C-2 `--diff` also rely on MCP-only `node symbolsOnly`) | yes |
| X-020 | none | no |
| X-021 | A | no |
