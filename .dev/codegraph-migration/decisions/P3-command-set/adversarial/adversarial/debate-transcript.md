# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% (23 of 23 diff points have a 2/3 majority; 13 unanimous)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (Mode A; one advocate per input file, default model, no persona)
- Taxonomy coverage gate: L1 covered (S-001), L2 covered (14 points), L3 covered (8 points). No forced round.
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Shared-assumption omissions: none (every advocate answered A-001..A-006)

Orchestrator verification notes (checked against the files during the run):
- `specs/phase-3-codegraph-adoption-spec.md` was edited by another session while this run was in progress. At diff time, §4 sat at lines 131-162; when the advocates read it, §4 sat at lines 186-217. The advocates' line numbers (188, 197, 210) match the newer file. The orchestrator re-checked by grep: line 197 holds "would tie generic guidance to one command", line 210 names the init owner as "`/sc:codegraph`", line 154 (§2.2 rank 13) says "advisory", and line 146 (§2.2 rank 5) says "Guide rule 1 plus the confirmation procedure in section 3".
- SPEC §2.3 (lines 157-167) defers reflect UC-2 test mapping (I-14), the workflow informational note (I-13) and the implement post-edit check (I-07 post). SPEC §2.4 drops index-repo graph stats (D-21). These bear on the caller lists in all three variants.

## Round 1: Advocate Statements

### Variant A Advocate (default model; `option-a.md`)

**Position**: Variant A ships three commands, each with one job: `/sc:impact`, `/sc:test-scope` and `/sc:graph [status|init]`. The shared rules go in the core guide, which the spec already decided on (SPEC §4, P3-D2). Test selection has a different input (changed files), a different codegraph verb (`affected`), a different `--depth` and a different status (advisory) from finding dependents, so it should not be a flag on `/sc:impact`.

**Steelman of Variant B**: B is the only variant that closes the call-site gap the evaluation measured mechanically. Caller rows give `main.py:46`, not the call at `:255` (EVAL §5.5). It also keeps BRS FR-02's closed `graph:*` vocabulary and Invariant 4 ("single seam", BRS §8.1), so consumers cannot drift apart. It is the only variant that states its per-run cost honestly (BRS OQ-6).

**Steelman of Variant C**: C covers dependents, tests and index ownership with the smallest surface: two commands, which fits CTX rule 7. Its defaults (`--depth` 2, `--limit` 20) match BRS K-2. Its fail-open result (`status: partial` plus Grep results) uses the `return-contract.yaml` status values that already exist (CTX facts). Its call-site check is FR-06's method written as a procedure, with no fragile parser.

**Key strengths claimed**:
1. **The seam matches the spec.** The rules live in `~/.claude/CODEGRAPH.md` (SPEC §4, P3-D2). The spec rejects putting them in a skill's refs: it "would tie generic guidance to one command" (SPEC §4, line 197).
2. **Test selection fits a command of its own.** BRS K-3 defines `/sc:test-scope` with its own interface and fields (`selection_source`, `delta[]`, `filtered[]`; BRS lines 241-250). FR-13 stage 0 and SPEC §2.2 rank 13 call it "advisory". Variant A's "advisory superset" label and per-test source carry that through (U-007). C drops the label.
3. **It avoids the diff-to-symbol problem.** codegraph has "no diff-to-symbol mapping" (EVAL §6.1), but `affected` takes plain file lists (`git diff --name-only | codegraph affected --stdin`, EVAL §4). So `/sc:test-scope --diff` needs no hunk mapping, while `/sc:impact --tests` inherits it.
4. **`--depth` keeps one meaning.** The `impact --depth` and `affected --depth` verbs are separate (EVAL §3). Variant A keeps separate flags, which avoids the gap C-009 found in B and C.
5. **`--file` input is kept**, matching BRS K-2 line 234. C drops it.

**Weaknesses identified in Variant B**:
1. It contradicts P3-D2. The core guide was decided, and B concedes "the guide plus Read already enforces read-before-cite" (X-001).
2. Its resolver depends on CLI output that changes often: 8 releases in about 3 months (BRS §8.2, "Output format drift"). Golden fixtures are extra maintenance (NFR-04, NFR-12).
3. The per-run skill cost is unmeasured (BRS OQ-6; UNVERIFIED).
4. `--tests` hides an advisory, unbacktested list inside a dependents contract. The backtest gate G-BACKTEST has not run (NFR-08).

**Weaknesses identified in Variant C**:
1. `degraded: [codegraph]` is a token outside FR-02's closed vocabulary (X-003).
2. Test lists carry no advisory label, against FR-13 stage 0 and SPEC §2.2 rank 13.
3. Its "No per-run skill invocation" claim conflicts with callers probing through `/sc:graph status` (X-002).
4. A caller that only wants tests must call `/sc:impact` and supply a symbol or diff. Whether the dependents work then costs extra tokens is UNVERIFIED.
5. It drops `--file`, which BRS K-2 includes.

**Concessions**:
- Three command files, three test files and three install-list entries are the largest maintenance surface (CTX criterion 5).
- Keeping both `/sc:impact --tests` and `/sc:test-scope` duplicates work (X-004). The fix is to drop `--tests` from impact.
- No step finds the call-site line (EVAL §5.5 gap). A should adopt FR-06 as a written procedure in the guide, as C does.
- A gives no per-command fail-open result shape and no degraded tokens. It should adopt C's `status: partial` and B's `graph:*` vocabulary.
- The value of `affected` is unmeasured: EVAL never ran it.

**Shared assumptions**:
- **A-001 QUALIFY**: a nested worktree is answered from the parent index with a warning and needs `init -i` (EVAL §5.8). `/sc:graph init` must adopt K-4's refusal unless `--worktree-local` is passed (BRS line 256).
- **A-002 QUALIFY**: hunk-to-symbol mapping is done on the IronClaude side through `query --json` spans (BRS K-2). `/sc:test-scope` needs none, because `affected` takes files (EVAL §4).
- **A-003 REJECT**: no watcher runs without an MCP client (EVAL §4), and INV-001 (HIGH) is unresolved. Every output must carry `index_state` and `checked_at` (FR-05).
- **A-004 QUALIFY**: `return-contract.yaml` is the existing convention (CTX facts), and BRS §8.2 says no contract field is added. Whether reflect's parser and pr-submit's state machine ignore the extra file is UNVERIFIED.
- **A-005 QUALIFY**: a CLI query takes about 290 ms (EVAL §5.5), but the token overhead of a nested command against the 2K-token budget (NFR-06) is unmeasured (UNVERIFIED).
- **A-006 ACCEPT**: FR-09 already names reflect's runtime-surface table as the single partition. All variants should cite it.

**Recommended final set**: (1) `/sc:impact <symbol>... | --file | --diff`, with no `--tests` flag; adopt C's defaults and `status: partial`, B's `graph:*` tokens, and the FR-06 call-site procedure written in the guide. (2) `/sc:test-scope --files | --diff`: advisory (FR-13 stage 0), recording `selection_source` per test, with fallback `heuristic_only`. (3) `/sc:graph [status|init] [--worktree-local] [--output-dir]`: the only command allowed to run `init`, and it refuses in a nested worktree unless `--worktree-local` is passed.

### Variant B Advocate (default model; `option-b.md`)

**Position**: Phase 3 should ship `/sc:impact` with `--tests` and `/sc:graph [status|init]`. The third unit should be `sc-graph-grounding`, cut down to the mechanics that a prose guide cannot carry: the probe output fields and the call-site resolver. The rules themselves belong in `~/.claude/CODEGRAPH.md`, which spec §4 (P3-D2, line 188) already decides.

**Steelman of Variant A**: Each command has one job, so each has a contract that is easy to test. It is the only variant that labels test selection an "advisory superset" and records the source of each test (variant-1 line 8). That matches BRS FR-13 stage 0 and spec §2.2 rank 13 ("advisory").

**Steelman of Variant C**: It adds the fewest new files (CTX "smallest correct change"). It puts the rules in the core guide that spec §4 lines 188-197 already chose, and that section explicitly rejects putting them in a skill ref (line 197). It is the only variant that gives concrete defaults and a fail-open result shape (variant-3 line 7).

**Key strengths claimed**:
1. The resolver closes a gap that was measured. Caller rows give the definition line, `main.py:46`, not the call at `:255` (EVAL §5.5). Spec §2.2 rank 5 rates call-site confirmation "High" value.
2. A script can encode BRS FR-06 exactly, which prose does not do reliably. FR-06 requires a `query --json` match on file plus `startLine`, a call-expression Grep, rejection of strings, comments and assignments, a multi-match rule, and a budget of 5 per symbol and 20 per run. INV-024 (MEDIUM) flags the prose method as at risk.
3. Its degraded tokens come from the closed `graph:*` set that BRS FR-02 requires ("Consumers invent no tokens").
4. Its probe records worktree provenance, version and telemetry (BRS K-1 output fields, FR-03, FR-22, NFR-09). That is how a nested worktree's foreign index gets caught (EVAL §5.8).
5. It is the only variant that states its own per-run cost honestly (variant-2 line 24, BRS OQ-6).

**Weaknesses identified in Variant A**:
1. It needs three command files, three test files and three install-list entries (variant-1 line 27).
2. `--tests` duplicates `/sc:test-scope`, and the variant leaves that unresolved (X-004).
3. It has no step that finds the call-site line, only "re-Read", despite EVAL §5.5.
4. It builds a standalone command whose value is unmeasured: `affected` was never run in EVAL, and BRS NFR-08 gates the union on a backtest.
5. It does not specify a degraded marker.

**Weaknesses identified in Variant C**:
1. `degraded: [codegraph]` is outside the BRS FR-02 closed set.
2. Its claim of "no per-run invocation" conflicts with probing through `/sc:graph status` (X-002).
3. Its written Grep-then-Read procedure must be followed correctly by every agent, every run (INV-024).
4. It has no pin check or nested-worktree check (EVAL §5.8, BRS NFR-09).
5. It drops `--file`.
6. Its tests carry no advisory label, although BRS FR-13 stage 0 keeps the list advisory.

**Concessions**:
- Spec §4 P3-D2 already rejects putting the rules in a skill, so B's "one seam owns semantics" is overruled for the rules. Only the mechanics remain.
- A shell resolver that parses CLI output is brittle (BRS §8.2 "Output format drift"). It needs golden fixtures (NFR-04). Exact-path allowlists for scripts are unproven (INV-019, MEDIUM). The resolver's reliability is UNVERIFIED.
- The latency and token cost of invoking the skill on every run is UNVERIFIED (OQ-6).
- C's interface is better specified than B's.

**Shared assumptions**:
- **A-001 QUALIFY**: `init` is safe only in sibling worktrees. A nested worktree is answered from the parent index and needs `init -i` (EVAL §5.8), so `/sc:graph` needs BRS K-4's `--worktree-local` refusal.
- **A-002 REJECT**: codegraph has "no diff-to-symbol mapping" (EVAL §6.1). Mapping must happen on the IronClaude side through `query --json` spans (BRS K-2); how accurate that is remains UNVERIFIED.
- **A-003 REJECT**: no watcher runs without an MCP client (EVAL §4), and INV-001 (HIGH) is open. Results need the BRS FR-05 re-check and a `stale` label.
- **A-004 QUALIFY**: `return-contract.yaml` is the existing convention (CTX), and BRS §8.2 says "No contract field is added". Whether reflect and pr-submit actually consume it is UNVERIFIED.
- **A-005 QUALIFY**: CLI queries were measured at about 290-297 ms (EVAL §5.5), but the cost of a nested invocation is UNVERIFIED for every variant (OQ-6). BRS NFR-06 (artifacts on disk, at most 2K tokens inline) is the only mechanism that would make it cheaper.
- **A-006 ACCEPT**: BRS FR-09 makes reflect's runtime-surface table the single prod/test definition. Every variant should cite it.

**Recommended final set**: (1) `/sc:impact <symbol>... | --diff [<base>]`, using C's defaults and fail-open result, B's `graph:*` tokens, and an `--tests` list labelled advisory with a per-test source. (2) `/sc:graph [status|init] [--worktree-local]`, the only owner of `init`, refusing nested worktrees unless `--worktree-local` is given. (3) `sc-graph-grounding`, delegate-only and limited to the probe plus `resolve-callsite.sh`, with no rules of its own. If the E-3 or E-4 checks fail, fold the resolver into `/sc:impact` and ship the two commands alone.

### Variant C Advocate (default model; `option-c.md`)

**Position**: Ship two commands, `/sc:impact` (with `--tests` folded in) and `/sc:graph [status|init]`. The shared rules go in the core guide `~/.claude/CODEGRAPH.md`, not in a skill. This is the smallest set that covers impact, test selection and index ownership, and it is the only variant that matches the spec's placement decision P3-D2 (spec §4 line 188).

**Steelman of Variant A**: A gives each command one job and one contract. It labels test selection an "advisory superset" and records where each test came from, which matches BRS FR-13 stage 0 and K-3's `selection_source` (lines 246, 280). It is also the only variant that admits `affected` was never run in EVAL.

**Steelman of Variant B**: B goes straight at the measured gap: caller rows give the definition line, not the call site (`main.py:46` vs `:255`, EVAL §5.5). It does this with a mechanical resolver that follows FR-06 (line 273). Its closed `graph:*` vocabulary (FR-02) and its provenance probe (FR-03, `foreign_index`) are the only answers any variant gives to nested-worktree poisoning and degraded-marker drift.

**Key strengths claimed**:
1. Variant C matches P3-D2. The spec rejects putting guidance "inside the new skill" because that "would tie generic guidance to one command" (spec §4 line 197). Its readiness check is one line of the guide (line 210).
2. It is the smallest correct change (CTX line 13, rule 7): two command files and two test-list entries, against three units for A and B.
3. It states the failure behaviour explicitly: `status: partial` plus Grep results, so the caller never stops. `partial` already exists in the return-contract enum (CTX line 11), which meets criterion 4 and NFR-07 (line 301).
4. Its defaults (depth 2, limit 20) and multi-symbol input match BRS K-2 (line 234) and NFR-01's 30-symbol batch (line 295).
5. One home for tests avoids A's duplication problem (X-004). Building a standalone command around `affected` is speculative while its benefit is unmeasured, because NFR-08 backtesting gates it (line 302).
6. Call-site confirmation is FR-06's own method (Grep inside the span, then Read) with no script. That avoids INV-019: exact-path script allowlists are still unproven until E-3 (line 370), and FR-04 limits scripts to orchestrators with unrestricted Bash until then.

**Weaknesses identified in Variant A**:
1. It needs three command files, protocols, tests and doc entries, and it admits this (variant-1 line 27).
2. The standalone value of `test-scope` is UNVERIFIED: `affected` was never run (variant-1 line 29; NFR-08).
3. `--tests` duplicates `test-scope` and A leaves that unresolved (X-004).
4. Every caller probes through a command invocation, and A never states the cost (X-002).
5. `--file` pinning waits on E-2 (BRS line 234).

**Weaknesses identified in Variant B**:
1. A skill invoked by every consumer on every run contradicts P3-D2 (spec §4 lines 188, 197). B admits that "the guide plus Read already enforces read-before-cite" (variant-2 line 26).
2. The per-run cost is UNVERIFIED (OQ-6), and NFR-06 caps graph text at 2K tokens per run (line 300).
3. The script brings an allowlist problem (INV-019/E-3) and golden-fixture upkeep with every pin bump (NFR-04, NFR-12).
4. Its caller list adds explain, load and cleanup-audit, which widens overlap with `/sc:explain` (criterion 6).

**Concessions**:
- `degraded: [codegraph]` breaks FR-02's closed set. C should emit `graph:*` tokens.
- C should adopt A's advisory label and per-test `source` field.
- C has no nested-worktree guard. `init` needs a `--worktree-local` refusal (BRS K-4 line 256).
- Offering `/sc:graph status` as a probe partly undercuts the claim of "no per-run invocation" (X-002).
- A written procedure is less deterministic than B's resolver.
- All variants say `/sc:graph`, but spec §4 line 210 says `/sc:codegraph`. The name has to be reconciled.

**Shared assumptions**:
- **A-001 QUALIFY**: a nested worktree is answered from the parent index with a warning (EVAL §5.8), so `init` must refuse there unless `--worktree-local` (`init -i`) is passed (BRS line 256).
- **A-002 QUALIFY**: codegraph has "no diff-to-symbol mapping" (EVAL §6.1), so the mapping is IronClaude-side through `query --json` spans (BRS line 234). For non-Python code it is UNVERIFIED, so the fallback is a files-only scope.
- **A-003 REJECT**: freshness without a daemon is unmeasured (INV-001 HIGH, line 353; EVAL §4). Rows must carry `index_state` and `checked_at` and stay advisory under G-FRESH.
- **A-004 QUALIFY**: `return-contract.yaml` is already the callable-skill convention (CTX line 11). Reflect and pr-submit read it as an input artifact only, with no new field (BRS §8.2 line 333).
- **A-005 QUALIFY**: the cost of a nested call compared with doing the work inline is UNVERIFIED. The only figures are CLI query times of about 290 ms (EVAL §5.5) and the NFR-06 2K-token budget.
- **A-006 ACCEPT**: FR-09 makes reflect's runtime-surface table the single prod/test definition (line 276), and C should cite it.

**Recommended final set**: (1) `/sc:impact <symbol>... | --diff [<base>] [--depth 2] [--limit 20] [--tests]`: production and test dependents, call sites confirmed by Grep then Read per FR-06, and an advisory `affected` plus path-heuristic test list with a `source` per test; `graph:*` degraded tokens and `status: partial` with Grep or files-only results when codegraph is absent. (2) `/sc:graph [status|init] [--worktree-local] [--output-dir]`: readiness, version, counts and next action, and the only user-typed owner of `init`, which refuses in a nested worktree unless the flag is given. The shared rules (readiness, read-before-cite, fail-open, call-site procedure) go in `~/.claude/CODEGRAPH.md` per P3-D2.

## Round 2: Rebuttals

Skipped: depth=quick.

## Round 2.5: Invariant Probe

Skipped: --depth quick. No `invariant-probe.md` was produced, and the invariant gate was not applied.

## Round 3: Final Arguments

Skipped: depth=quick.

## Per-point positions (Round 1)

A tie vote ("A=B=C") counts as "no superior variant". A point is agreed when at least 2 of 3 advocates name the same winner (or the same tie).

| Point | Level | Adv A | Adv B | Adv C | Agreed | Winner |
|---|---|---|---|---|---|---|
| S-001 | L1 | A=B=C | A=B=C | A | yes (2/3) | tie |
| S-002 | L2 | C | C | C | yes (3/3) | C |
| S-003 | L2 | C | C | C | yes (3/3) | C |
| S-004 | L2 | C | C | C | yes (3/3) | C |
| C-001 | L2 | A=C | C | C | yes (2/3; all include C) | C |
| C-002 | L2 | A | A | A | yes (3/3) | A |
| C-003 | L3 | B | B | B | yes (3/3) | B |
| C-004 | L2 | A=B | C | C | yes (2/3) | C |
| C-005 | L3 | C | C | C | yes (3/3) | C |
| C-006 | L2 | C | B | B | yes (2/3) | B |
| C-007 | L2 | A=C | A=C | A | yes (2/3; all include A) | A=C |
| C-008 | L2 | B | B | B | yes (3/3) | B |
| C-009 | L3 | A | A | A | yes (3/3) | A |
| X-001 | L2 | A=C | C | C | yes (2/3; all include C) | C |
| X-002 | L2 | B | B | B | yes (3/3) | B |
| X-003 | L3 | B | B | B | yes (3/3) | B |
| X-004 | L2 | B=C | B=C | B=C | yes (3/3) | B=C |
| A-001 | L3 | A=B=C | B | B | yes (2/3) | B |
| A-002 | L3 | A | A=B=C | A=B=C | yes (2/3) | tie |
| A-003 | L3 | A=B=C | A=B=C | B | yes (2/3) | tie |
| A-004 | L2 | A=B=C | A=B=C | A=B=C | yes (3/3) | tie |
| A-005 | L2 | B | C | B | yes (2/3) | B |
| A-006 | L3 | A=B=C | A=B=C | A=B=C | yes (3/3) | tie |

Shared-assumption responses: A-001 QUALIFY ×3; A-002 QUALIFY (A, C), REJECT (B); A-003 REJECT ×3; A-004 QUALIFY ×3; A-005 QUALIFY ×3; A-006 ACCEPT ×3. A-003 is rejected unanimously: every merged command must carry `index_state` and `checked_at` and treat its results as advisory until E-1 (BRS FR-05, INV-001).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | tie | 60% | Heading names only; one advocate preferred A's cleaner headings |
| S-002 | C | 90% | Smallest unit count fits CTX rule 7; all three advocates agree |
| S-003 | C | 90% | Caller list with step IDs; B points to another document |
| S-004 | C | 92% | Defaults and fallback written into the command entry (variant-3 line 7) |
| C-001 | C | 88% | Matches SPEC §4 P3-D2 (core guide); A equal on placement, C adds the call-site rule; B advocate conceded |
| C-002 | A | 90% | Advisory label and per-test source match BRS FR-13 stage 0 and SPEC §2.2 rank 13; C advocate conceded |
| C-003 | B | 80% | Only mechanical answer to EVAL §5.5; reliability UNVERIFIED; SPEC §2.2 rank 5 plans a written procedure instead |
| C-004 | C | 65% | Multi-symbol input; BRS K-2 says `--file` waits on E-2; A advocate preferred keeping `--file` |
| C-005 | C | 85% | Explicit `status: partial` result; its token must be corrected (X-003) |
| C-006 | B | 70% | Provenance and pin check catch a foreign index (FR-03, EVAL §5.8) |
| C-007 | A=C | 75% | Both state machine output for `/sc:graph` |
| C-008 | B | 70% | Widest caller coverage; C advocate warned it widens overlap with `/sc:explain`, and SPEC §2.3 defers some callers |
| C-009 | A | 90% | Separate verbs, separate `--depth` (EVAL §3) |
| X-001 | C | 88% | SPEC §4 (P3-D2) supersedes BRS FR-01; B advocate conceded |
| X-002 | B | 85% | Only B states its invocation cost (OQ-6) |
| X-003 | B | 95% | BRS FR-02 closed `graph:*` set; C advocate conceded |
| X-004 | B=C | 92% | One home for test selection; A advocate conceded the duplication |
| A-001 | B | 70% | B's provenance probe detects `foreign_index`; all three agree `init` needs a `--worktree-local` refusal |
| A-002 | tie | 60% | No variant states diff-to-symbol mapping (EVAL §6.1) |
| A-003 | tie | 70% | Unanimous REJECT; no variant re-checks freshness (FR-05, INV-001) |
| A-004 | tie | 75% | Same contract assumption in all three |
| A-005 | B | 65% | Only B names the nested-invocation cost |
| A-006 | tie | 85% | None names FR-09; all accept it |

Diff points won (exclusive; shared wins count 0.5): A 2.5 (C-002, C-009, half of C-007), B 7.5 (C-003, C-006, C-008, X-002, X-003, A-001, A-005, half of X-004), C 8.0 (S-002, S-003, S-004, C-001, C-004, C-005, X-001, half of X-004, half of C-007). Ties: S-001, A-002, A-003, A-004, A-006.

## Convergence Assessment
- Points resolved: 23 of 23 (unanimous: 13)
- Alignment: 100%
- Threshold: 80%
- Status: CONVERGED (diff-point and taxonomy gates only; the invariant gate was not applied at depth quick, and debate-protocol.md says quick runs "No convergence check", so this figure is a Round 1 majority count, not a multi-round convergence)
- Unresolved points: none at the diff-point level
- Open decision outside the diff points: the third unit. Advocate A wants `/sc:test-scope` (and no `--tests` on impact); Advocate B wants a trimmed `sc-graph-grounding` (probe plus resolver only, with a fold-back rule); Advocate C wants no third unit. All three agree on `/sc:impact` and `/sc:graph`.
- Name conflict raised by Advocate C: the variants say `/sc:graph`; SPEC §4 line 210 says `/sc:codegraph`.
