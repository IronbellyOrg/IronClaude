# Round 2 — Advocate B (variant-2-sonnet-analyzer), sequential rebuttal (second)

Notation: A/B/C = variants 1/2/3; EVAL = `research/codegraph-evaluation.md`. Primitive paths are relative to `src/superclaude/`. Re-read for this round: `skills/sc-auggie-review-protocol/SKILL.md:124-141,214-219`, `skills/sc-pr-submit-protocol/SKILL.md:200-209`, `skills/sc-implement-protocol/SKILL.md:116-123`, `cli/install_skill.py:44-55`, `skills/sc-cleanup-audit-protocol/SKILL.md:72-87`, EVAL lines 96, 195, 209-214, and A's variant line 61.

## Response to criticisms

**1.** (round1-A) "B has no capability abstraction (B §6 N-1 interface is readiness-only). Adding MCP later, which B's own Q1 contemplates, means editing every consumer." Repeated in round2-A: "it has no capability map, no lifecycle owner, and no release-level switch."
Partly wrong on the facts, partly right. Consumers do not hold CLI knowledge in B: N-1 owns probe, provenance and `resolve-callsite.sh`, and N-2 owns `callers`/`impact`/`affected` invocation, parsing and the prod/test split (B §6). What each consumer holds is a Step-0 line plus allowlist lines, and those are edits A's capability map would not remove either. The criticism holds in one respect: nothing in B says "capability X is served by CLI form Y today and MCP tool Z once listed", and B's own Q1 leaves that door open. Concession: add a small `refs/capability-map.md` inside N-1 (capability, CLI form, MCP tool name `codegraph_*`, fallback, tested version). It is cheap and also lists the golden-fixture commands. I do not accept it as a "kill switch" (see item 8).

**2.** (round1-A, round1-C, round2-A) "B's FR-17 lets `/sc:load --index` run `init --yes` ... in a session-context command. That breaks separation of concerns." (A); "B's `/sc:load --index` runs `init` inside an onboarding command" (C).
Conceded, as in Round 1 (X-005 = A). EVAL §5.4 puts `init` at about 1 GB peak RSS and 34 MB written. A user-typed `/sc:graph init` with the nested-worktree refusal (EVAL §5.8) is the cleaner owner. I withdraw FR-17 and I-09's `--index` flag. It follows that X-016 should be A's read-only status line and nothing else (changed below).

**3.** (round1-A, round2-A) "B's FR-01 runs 'N-1 once per run' while its §8 says 're-run status immediately before the queries'. That is an internal inconsistency (A-006)." / "Two of its own claims are in tension."
Conceded. I re-read B: FR-01 says "once per run before any other codegraph call"; §8 says "not once per session". Those are not literally contradictory (run vs session), but FR-01 as written does not require a freshness re-check. Resolution for the merge: availability and provenance (`version`, `index_root == realpath`) are latched once per run; `status` freshness is re-run before every query batch that follows an in-run write. Put that split in FR-01 and in N-1's output (`checked_at`).

**4.** (round1-A, round1-C) "B's D-05 claims 'Grep sees every static reference the graph sees'. EVAL does not support this." / "asserted, not measured."
Conceded again (X-020). I also concede the follow-on: B's D-05 rests partly on that sentence, and what remains does not carry the whole drop. The READ-ONLY charter does not forbid a query step (a `callers` query writes nothing), and `:86` ("MCP tools are unavailable to background subagents ... execute in the orchestrator only") only moves the call to the orchestrator. What survives: `:75` keeps grep as the DELETE gate, and the graph's marginal value is unmeasured. I now move C-019 to C's asymmetric rule (nonzero graph callers upgrade DELETE to REVIEW; zero proves nothing), orchestrator-only, low rank, gated on a one-hour spike showing the upgrade ever fires where grep did not. A's "zero = extra DELETE evidence" remains wrong (violates my own FR-07).

**5.** (round1-A) "Its `sc-structure-brief` (N-3) is a new skill for value that B itself rates P-class at 0.6 (rank 9)."
Conceded. B's own score table ranks I-10 at 0.6 with "token claim unmeasured", and the "58K to 3K" figure belongs to the primitive, not to a measurement. Defer N-3. A's lighter in-place edits (explain one-hop, load status line; A's own R2 drops I-15) are cheaper. This leaves B with two candidates, so the merged candidate set has to take A's `/sc:graph` to meet the brief's 3-5 range.

**6.** (round1-A) "B also overstates the sample: 'the rest were test functions'. EVAL §5.5 shows only 20 of 23 rows."
Already conceded (X-021). EVAL line 195 shows "20 of 23"; the 3 hidden rows were not inspected. The hazard stays valid as direction (tests inflate counts) and rests on one symbol.

**7.** (round1-C) "B's `dependent-impact` exemption from the out-of-hunk downgrade (X-009) is the boldest gate change in the debate, built on Class P ... and a Python-regex hunk-to-symbol extractor."
Conceded in Round 1 (Concession 7), and I tighten it. FR-12 has no gate of its own; only `affected` has NFR-08. Merge rule: stage 1 ships the blast-radius artifact as context only (A's I-09 and my I-04 agree on this). Stage 2 ships `dependent-impact` in shadow: it is reported as ordinary "context", and the audit log counts how many Read-verified rows the `:218` downgrade would have dropped over a fixed number of reviews. The exemption is enabled only if that count is nonzero and the false-positive rate is acceptable.
Correction to my own Round 1 wording: I wrote that a broken caller "can never surface today". `:218` says an out-of-hunk finding is "downgraded to 'context' or dropped, depending on severity", so it can surface as context. Also, `:136-137` shows directory chunking happens only for 16-30 files or 1500-5000 diff lines; up to 15 files go to a single Auggie call. My I-04 blind-spot claim applies fully only to that middle band, plus the out-of-hunk rule at every size. I lower I-04's V from 4 to 3: 3 x 0.6 / 2 = 0.9, a tie with I-06 and I-08. On B's own tie-break (lower risk), I-06 (risk L) outranks I-04 (risk M), so I-06 moves to rank 5.

**8.** (round1-A strengths 2 and 3; round2-A "no release-level switch") "B relies on uninstalling the binary, and C relies on deleting text."
Half right. B's runtime switch is real (NFR-07: `codegraph` absent equals the native path, tested per primitive). A's round2-A New evidence 1 shows the other half is weaker than claimed: `install_skill.py:46-48` does `shutil.rmtree` then `copytree` under `force`, so a `status: disabled` edit in an installed ref is erased by `./update.sh`. A's switch is a source edit plus release, which is still cheaper than touching about 10 primitives. Fair combination: A's header as the release-level switch, B's absence-equals-native as the runtime switch. A's NFR-08 text on MCP de-registration is also wrong for CLI-default consumers (A's own point 2), which supports B's FR-01 test.

**9.** (round1-C) "B's CLI-only-everywhere stance ignores the measured 3-15 ms MCP vs 290-300 ms CLI gap (EVAL §5.6) for per-hunk loops — reflect Step 1B.3 over >=3 tasks x hunks at 300 ms per call compounds."
The numbers are right (EVAL lines 188 and 209-214: callers 297 ms by CLI; 3 and 15 ms by MCP). The conclusion does not follow for B's design. B's artifacts are computed once per run per changed symbol, not per hunk per task, and capped (FR-10: 40 rows, 6 KB). Arithmetic from EVAL numbers (an estimate, not a measurement): 30 symbols x 300 ms is about 9 s, inside NFR-01's 15 s. The argument becomes valid when serial CLI queries pass roughly 100 in a run (about 30 s), and then MCP, listed per the capability map, is the better path. Concession: B's "irrelevant at 30-60 calls" (§2.1) is arithmetic, not a measurement, and NFR-01 should log the actual query count so the MCP switch is data-driven. I move C-002 to "B for v1, A's MCP classes after measurement".

**10.** (round2-A New evidence 6) "The span lookup is itself ambiguous ... a resolver ... must select the match whose file and `startLine` equal the caller row's file and def line, and it must mark the row `unresolved` otherwise. Neither A's I-02 nor B's `resolve-callsite.sh` states this."
Accepted, with one detail. B's §8 says "require a unique kind/file match, else `ambiguous[]`", and the script has `--file`, but neither binds the match to the caller row's def line. EVAL line 195-ish and §5.6 show the name-search hazard (two unrelated `install` functions). The binding rule is stricter and correct: match `(file, startLine == def_line)`, else `unresolved`. I also accept A's typed row field as the row-level form of B's `call_site_status`.
Correction to my Round 1: I wrote that A greps "after the def line" with no end bound. A's I-02 mechanism column says "`codegraph query <s> --json` gives `startLine`/`endLine` ... to bound the search" (variant-1 line 61). That claim of mine was wrong on the facts. A's gap is only that FR-04 does not repeat it.

**11.** (round1-A strength 7; round2-A New evidence 5) "Its pre-edit impact runs earlier than B's post-edit context."
Partly conceded. A's own R2 point stands: `sc-implement-protocol/SKILL.md:118` says "Implement only that task", and `:119` makes a drive-by file a minor unless a breach applies, so pre-edit impact cannot widen Q1's edits. Its remaining value is a warning to the implementer and input to Q3. My post-edit check covers the symbols that actually changed. They are complementary, so C-011 becomes A+B, not A alone.

**12.** (round1-A per-point) "C-008: A — simplest grep-enforceable ban." and "C-014: A — positional args avoid unverified pipeline matching."
C-008: conceded in part. My interactive `maxFiles <= 5` allowance (FR-10, §2.1) has no consumer in B's own ideas: I-10 and N-3 use `status`, `files`, `callers`, `callees`. A permission with no user is surplus. Adopt A's "no primitive step names explore" test. Keep my routing block (I-03), because `codegraph_explore` is the one always-loaded tool (EVAL §3) and the model may call it unprompted; a grep over primitives cannot constrain that. C-014: conceded. FR-13 already escalates above 200 files, so positional args always fit and `--stdin` from a file is surplus, with its own unverified redirect matching.

## Updated assessment of A and C

**A.** A's Round 2 is a large honest correction: wildcard, MCP names in agents, validator edit, `sync`, `status` latency, zero-callers-DELETE, union-at-once (now with the VG-1 false-block evidence) are all withdrawn, and it found the reinstall-erases-switch fact against its own FR-16. What remains uniquely A's: the user-typed `/sc:graph` lifecycle owner, the telemetry blocker (U-002), the language-scope honesty (U-003), and the pre-edit step. Weaknesses that remain: A's Class A/D MCP default still waits on B1; A's `--diff` and "always pass `file`" rest on a CLI limitation that is not established (see New evidence 1); and its capability map is only a convention until a second access path exists. I take A for the scaffold's lifecycle command, telemetry, language scope and class table.

**C.** C conceded the right things (C-001, X-002, X-008, X-013, X-015, X-018, X-019). C's surviving contributions are real: the asymmetric cleanup rule (now adopted in my C-019 position), the edge-case table (S-010), the docs-only-diff rule (U-022), and the mutation-exclusion grep (FR-06), which is a good test form for my FR-04. C's W6 latency argument is the strongest point against me and is adopted above as an MCP-stage trigger. C's remaining positions that conflict with its own concessions: C-007 "first probe authoritative" and FR-07 per-run caching against its A-006 concession, and the tasklist risk note, which still changes tasklist output by index state.

## New evidence (not presented in Round 1)

1. **The EVAL CLI list is an abbreviated usage line, so absence from it is not proof.** EVAL line 96 lists `callers <symbol>` with no `--limit`, yet EVAL line 195 prints "Showing 20 of 23; pass --limit to widen." The list shows flags for `query` and `affected` and omits them for `callers`. So "CLI `node` has no file or `symbolsOnly` mode" (X-019; A's R2 point 3; my Round 1) and "CLI `callers` has no `file` argument" are inferences from absence, UNVERIFIED in both directions. C's "CLI works today" claim is equally unverified. B's design survives either way because it depends on neither; A's `--diff` "not v1-ready on the CLI" is also not established. Cheap closure: record `codegraph callers --help` and `codegraph node --help` output before Phase 3. This corrects the diff-analysis premise behind X-019.
2. **The VG-1 false-block applies to B's union stage too.** `sc-pr-submit-protocol/SKILL.md:203-204`: "Any non-zero gate blocks the push", and VG-1 is `uv run pytest <changed-area>` (`:206`). My FR-13 says the union "never removes tests", but NFR-08 measures recall and set size, not collection errors. A stale index (EVAL §4: no watcher without an MCP client) can return a test path that a rename or deletion removed. Add to the union stage: filter to paths present in `git ls-files`; a collection error caused only by an `affected`-only path is logged as advisory and the run falls back to `<changed-area>`; the backtest records the collection-error rate.
3. **B has an unresolved control question between per-subcommand allowlists and bundled scripts.** FR-04 pre-approves per-subcommand patterns, while N-1 and N-2 run codegraph from bundled scripts. If the model invokes a script, the approved pattern is the script path and the inner `codegraph` calls are not separately matched (Claude Code permission matching: UNVERIFIED here). The effective control is then the script body. `BASH_INSPECTION_POLICY.md` also forbids broad wrapper allowlists. Resolution: use exact-path script patterns for closed-Bash consumers (pr-submit, auggie-review, cleanup-audit), and make FR-04's grep test (subcommands outside the read-only set return 0 hits) run over the script bodies as well as the primitives.
4. **I-04's evidence base is narrower than stated** (see item 7): chunking applies only to 16-30 files or 1500-5000 lines (`:136-137`), and out-of-hunk findings become "context" rather than always vanishing (`:218`). This lowers I-04 and raises I-06 in B's own ranking.
5. **Cleanup-audit's drop reasons were partly wrong** (see item 4): a query-only step does not violate READ-ONLY, and the MCP constraint only forces the call into the orchestrator.

## Shared assumptions — changes only

| A-ID | New position | Reason |
|---|---|---|
| A-008 | REJECT (as a v1 gate input; was QUALIFY) | EVAL never ran `affected`, and a union can false-block VG-1 (`sc-pr-submit-protocol/SKILL.md:203-204`), including through B's own FR-13 (New evidence 2). Advisory-only until the NFR-08 backtest, extended with collection-error rate, passes |

All other positions are unchanged from Round 1 (A-001/002/009/010/011 ACCEPT; A-003/004/012 QUALIFY; A-005 ACCEPT as risk; A-006/007 REJECT). New evidence 1 adds a caveat to A-010 (version-pinned text), not a change.

## Updated per-point positions

| ID | Superior | Changed from Round 1? |
|---|---|---|
| S-001 | none | no |
| S-002 | none | no |
| S-003 | B+C | no |
| S-004 | A+B | no |
| S-005 | B | no |
| S-006 | A+B (A's coverage filtered by B's evidence classes; A trimmed its tail) | yes |
| S-007 | A+B | no |
| S-008 | A+B | no |
| S-009 | A+B | no |
| S-010 | A+C | no |
| S-011 | none | no |
| C-001 | A+B | no |
| C-002 | combination: B for v1, A's MCP classes after measurement | yes |
| C-003 | B | no |
| C-004 | B | no |
| C-005 | A+B | no |
| C-006 | A+B | no |
| C-007 | B | no |
| C-008 | A+B (A's no-primitive-names-explore test, B's routing block) | yes |
| C-009 | combination: B resolver, A's typed row and (file, startLine) match, C's drop-never-repair | yes |
| C-010 | B+C | no |
| C-011 | A+B | yes |
| C-012 | A+B (context first, shadow-mode exemption second) | yes |
| C-013 | B | no |
| C-014 | A | yes |
| C-015 | A+B | no |
| C-016 | A+B | no |
| C-017 | B | no |
| C-018 | B | no |
| C-019 | C (asymmetric rule, orchestrator-only, spike-gated) | yes |
| C-020 | B | no |
| C-021 | A (light edits; N-3 deferred) | yes |
| C-022 | B | no |
| C-023 | A | no |
| C-024 | A+B | no |
| C-025 | A+B (B's top five swaps I-04 for I-06) | no |
| C-026 | A+B+C | yes |
| C-027 | A+B | no |
| C-028 | B | no |
| C-029 | A+B | no |
| C-030 | B | no |
| C-031 | B+C | no |
| C-032 | A+B | no |
| C-033 | A+B | no |
| X-001 | B | no |
| X-002 | B | no |
| X-003 | B | no |
| X-004 | B+C | no |
| X-005 | A | no |
| X-006 | B+C | no |
| X-007 | B | no |
| X-008 | B | no |
| X-009 | A+B | no |
| X-010 | A+B | no |
| X-011 | A+B (gated on existing symbols; informational; FR-07 applies) | yes |
| X-012 | B+C | no |
| X-013 | B | no |
| X-014 | A+B | yes |
| X-015 | A+B | no |
| X-016 | A | yes |
| X-017 | B | no |
| X-018 | A | no |
| X-019 | B (both CLI claims unverified; B's design needs neither) | no |
| X-020 | none | no |
| X-021 | none | no |
