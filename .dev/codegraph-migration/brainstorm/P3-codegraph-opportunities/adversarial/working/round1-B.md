---
round: 1
advocate_for: variant-2-sonnet-analyzer (Variant B)
persona: analyzer
sources: variant-1-opus-architect.md (A), variant-2-sonnet-analyzer.md (B), variant-3-haiku-backend.md (C), diff-analysis.md, seed-brief.md, EVAL (codegraph-evaluation.md)
---

# Round 1 advocate: Variant B (analyzer)

Notation: A/B/C = variants 1/2/3. EVAL = codegraph-evaluation.md. Primitive line citations were re-read for this round (troubleshoot `:218`, `:256`, `:281`, `:286`; reflect `:347`; auggie-review `:218`; cleanup-audit `:75`, `:86`, `:8`; pr-submit `:4`, `:206`; `hooks.json:52,59`; evidence-validator `:5`, `:97`; runtime-surface `:25`, `:61`; implement `qa.md:9`; tasklist `:1326`, `:1658`, `:1670`). All matched what the variants say.

## Position summary

B is the variant whose recommendations follow from what EVAL actually measured: it separates measured mechanism (M) from unmeasured benefit (P) and gates every behaviour-changing step (`affected` in VG-1, the out-of-hunk exemption, the allowlist breadth) on that line. A is the strongest on breadth and on two operational facts B missed (telemetry on the CLI path, Markdown repos get no signal), and C drifts into 1:1 Serena swaps and contains four checkable errors, so the best merge is B's evidence discipline and safety rules with A's lifecycle and telemetry findings.

## Steelman

### Variant A (opus architect)

Strongest version: codegraph is a single-maintainer dependency (EVAL §1: 30 releases, 8 in about 3 months, top contributor 1,535 commits vs 11-18 for the next three), so the right design is one seam that owns the capability map, probe, citation resolution and degraded vocabulary, so a backend swap touches one ref plus allowlist lines (A §1, INV-4, C-1). A also identifies two real facts B omits. First, telemetry: EVAL §7 puts `CODEGRAPH_TELEMETRY=0` only in the MCP entry and the Coder image, so Bash CLI calls on another host send telemetry (A B5, U-002). Second, value depends on the target repo's language; EVAL §5.4 indexed python/yaml/liquid, so Markdown primitives get nothing (A §1, U-003). A also names `/sc:graph` as a user-typed owner for the unowned per-worktree `init` (EVAL §4, §7), refuses it in a nested worktree without `--worktree-local` (matches EVAL §5.8 text), and adds a kill switch (FR-16, NFR-08) and a pre-edit impact check in implement Q1 (I-05) that is truly "before edits". Its tasklist drop cites the exact booster row (`sc-tasklist-protocol/SKILL.md:1326`, ">2 files affected"), which I verified. A is the most complete spec: 19 ideas, 16 FR, 8 NFR, closed `graph:*` vocabulary that can be grep-tested.

Where it is genuinely right against B: pre-edit timing (B's I-07 runs after the diff exists), the lifecycle command, the telemetry blocker, and the grep-testable vocabulary.

### Variant C (haiku backend)

Strongest version: treat codegraph like a backend dependency with a contract, `PROBE -> CALL -> VERIFY -> DEGRADE`, with a run-scoped latch (no retry), caching per run, and "never silence" on empty `affected` for a source diff (C §2 contract block, FR-02, FR-05, FR-07). Its `affected` handling is the most careful on one point: an empty result with a non-empty source diff forces the heuristic, while a docs-only diff may honestly yield no tests (C §8 table, U-022). Its rule "a row that fails re-Read is dropped, never repaired by guessing an offset" (FR-03) is the cleanest statement of the citation contract, and the stale-index rule (HIGH becomes MEDIUM when stale, U-021) is a pragmatic guard on reflect severity. The mutation-exclusion grep (`codegraph (init|index|sync|...)` returns 0, FR-06) is mechanically testable. The edge-case table maps observed EVAL behaviour to a contract response, which is exactly what an implementer needs.

Where it is genuinely right against B: the drop-never-repair rule, the explicit docs-only-diff case, and the test-by-grep mutation exclusion.

## Strengths claimed

1. **Evidence classes make the ranking auditable.** B defines M/P/A before §1 and carries them into the score `V x C / E` with C = 1.0/0.6/0.3 (B §4). Every rank can be recomputed and its confidence challenged. A's formula multiplies by a "Frequency" factor that is also subjective, and C's ranking is qualitative with no formula (diff-analysis C-024). I-08 (`affected`) lands at 0.9 instead of top-3 solely because EVAL never ran `affected` (A-008 says "STATED (B only)").
2. **B is the only variant that gates `affected` on a measurement.** EVAL §3 lists the subcommand but §5 never runs it. B ships an advisory delta first and unions into VG-1 only after a 20-change backtest (FR-13, NFR-08: recall at least that of `<changed-area>`, median 25 files or fewer). A unions immediately (FR-07) and C replaces the heuristic (FR-05: `tests` "is exactly the parsed `affected --json` list", which can narrow the set; X-008). Narrowing a push gate on an unrun tool is the highest-cost error in the field.
3. **B finds the parity hazard the 1:1 swap creates.** EVAL §5.5 shows 20 of 23 callers: 2 production (`install_mcp_server`, `install`) and 18 tests. Reflect's rule is "HIGH if >5 referencing call sites" (`skills/sc-reflect-protocol/SKILL.md:347`), so a naive callers swap trips HIGH on tests alone. B partitions with reflect's own runtime-surface table (`refs/runtime-surface.md:25`, FR-09). A and C do not partition; C's I-05 even keeps tests in the count (X-013).
4. **B's citation resolver is the most precise.** `codegraph query <caller> --json` returns `startLine`/`endLine` (EVAL §5.5), so B Greps the callee only inside that span, then Reads (I-02, N-1 `resolve-callsite.sh`). A greps "after the def line" with no end bound (I-02), which can match a different function in the same file. The measured gap is `main.py:46` vs `:255`; the span closes exactly that.
5. **B's access model matches the constraints that exist.** CLI-first with orchestrator-computed artifacts follows the repo's own precedent: troubleshoot pastes the producers table into briefs (`SKILL.md:281`) and reflect reviewers get pre-computed material (`:355`). This avoids the `CODEGRAPH_MCP_TOOLS` blocker (EVAL §3: only `codegraph_explore` listed) and keeps read-only agents' `tools:` lines untouched (FR-11), so no test pin on `troubleshoot-analyst.md:5` moves.
6. **B has the narrowest safe allowlist.** One pattern per subcommand, never `Bash(codegraph *)` (FR-04). EVAL §3 lists `install`, `uninstall`, `upgrade`, `unlock`, `telemetry` as CLI subcommands, and EVAL §2/§5.9 shows `install` edits `~/.claude.json`, `settings.json` (adds `codegraph prompt-hook`) and `CLAUDE.md`. A wildcard pre-approves that. Existing allowlists are already enumerated (`sc-cleanup-audit-protocol/SKILL.md:8`, `sc-pr-submit-protocol/SKILL.md:4`), so per-subcommand patterns fit the house style.
7. **B alone handles freshness without touching the index.** Probe never syncs; re-run `status` right before queries (B §8); `index_root == realpath(worktree root)` or discard (FR-03). EVAL §5.7 shows `codegraph sync` failing on the writer lock while the daemon runs, which makes A's "try one `sync`" (FR-10) a step that fails whenever an MCP session is open. B also notes the CLI-only case: no watcher without an MCP client (EVAL §4).
8. **B states its unknowns.** Output-format drift (EVAL §3 gives `--json` only for `query` and `affected`) leads to golden fixtures and a `parse_failed` degrade (NFR-04). `status` timing is "UNVERIFIED, measure" (NFR-01), where A asserts "~300 ms" for `status` (X-017) although EVAL §5.5 timed only `query` and `callers`.
9. **B's drop list is reasoned from primitive text.** D-05 (cleanup-audit) cites the read-only charter, `init` writing `.codegraph/`, and MCP unavailability to background subagents (`:86`). D-02 cites the 1 s pre-edit timeout (`hooks.json:52`, verified as the `freshness-pre-edit.sh` entry). D-10 cites `hooks.json:59` (matcher `Read` only), which also kills `node` file mode as a Read replacement; A and C reach the same drop.
10. **B closes the explore question with a budget, not a slogan.** 24,913 characters is about 6K tokens at 4 chars/token (B says it is an estimate) against `~3k` Wave 1 (`SKILL.md:218`, verified). Explore is banned in waves under 8K and in every subagent, but stays usable interactively with `maxFiles <= 5` (FR-10), which the CLI parameter range (1-20, EVAL §3) supports.

## Weaknesses identified in other variants

1. **C breaks the scope (C-001).** Its I-02 ("replace Serena overview/find_symbol rows"), I-04 (replaces `find_declaration`), I-05 (replaces `find_referencing_symbols`) and I-06 (replaces the Serena fallback tier) are exactly the 1:1 swaps INV §4 assigns to Phase 3 and the seed brief says to go beyond (Problem Statement: "where, beyond 1:1 Serena replacement"). Four of C's 13 ideas, three of C's top six, are out of scope.
2. **C contains four checkable errors.** (a) MCP names `mcp__codegraph__search/__callers` (X-018) do not match EVAL §3's `codegraph_search`, so the server-prefixed form is `mcp__codegraph__codegraph_*`; its allowlists would not match. (b) `codegraph_node {file, symbolsOnly:true}` is claimed to work through the CLI "today" (X-019); EVAL §3 lists CLI `node [name]` only. (c) It cites "Wave 1.5 :256" as the Tier-1 budget of 2k (X-015); `:218` is Wave 1 at about 3k and `:256` is Wave 1.5 (verified). (d) It says both "no allowlist change" (§1) and "adding `Bash(codegraph *)` patterns" (§2) while FR-10 forbids the wildcard (X-002).
3. **C's `affected` pipeline is unproven under scoped Bash.** `git diff --name-only | codegraph affected --stdin` (I-09) runs under pr-submit's `Bash(git *)`-style allowlist (`:4`). Whether a pipeline is accepted is UNVERIFIED (A's own Q-2). B passes files as arguments or `--stdin` from a file (C-014).
4. **C and A both treat non-empty caller lists as complete (A-007).** C's I-05 uses `callers --limit 100` as the shared-vs-collision test; A's severity counts "resolved call sites". EVAL verified one symbol (§5.5). B partly shares the problem (see Concessions) but ties the threshold to distinct production symbols and records `shown/total` (FR-08, FR-09).
5. **A's `Bash(codegraph *)` for Class C (X-002).** With EVAL §2 and §3 above, one wildcard line in pr-submit or auggie-review allows `codegraph install`, `upgrade`, `uninit` and `unlock`. A's own FR-09 forbids using them but a grep test on body text does not constrain what a pre-approved allowlist permits.
6. **A grants MCP names to read-only agents in v1 (X-001, X-003).** A's B1 depends on the Phase 2 registration setting `CODEGRAPH_MCP_TOOLS` for a subset, and an explicit allowlist then blocks `explore`/`files` for everyone (A Q-1; EVAL §3 line 94). Seven extra always-loaded schemas have unmeasured cost (U-014). A also lists `evidence-validator` in Class D, which erodes the independent last gate (X-004).
7. **A's "try one `sync`" contradicts EVAL §5.7** (see Strength 7). It also puts an index mutation into read-only flows, which A's D-08 and FR-09 forbid elsewhere (X-006).
8. **A unions `affected` into VG-1 at once (X-008)** on a tool EVAL never ran; at depth 2 an unmeasured union can inflate the set, and A's Q-8 admits the right depth is unknown.
9. **A's 19 ideas include a tail with its own admitted score of 0.7-1** (I-09, I-12, I-15 at ranks 17-19; I-16 "demoted by judgment" from a formula score of 3 to rank 16). A formula the author overrides is not a method.
10. **C's `impact == 0` DELETE logic and "grep misses are not graph misses" (X-012, X-020)** rest on a claim EVAL does not state. C's FR-05 also lets graph results replace the heuristic, so a stale index (A-006) silently narrows tests.

## Concessions

1. **X-021 / EVAL fact-check against B.** B writes that the sample had "23 callers reported" and "the rest were test functions" (B §1, I-05). EVAL §5.5 shows 20 rows: 2 production and 18 tests; the other 3 were never inspected. The inference is still valid (tests inflate the count), but "23 callers, 2 production" overstates it. The correct claim is "20 of 23 inspected: 2 production". Also the whole hazard rests on one symbol (A-007).
2. **X-020 / D-05 reasoning.** B says "Grep sees every static reference the graph sees." EVAL states neither direction. The drop conclusion (graph cannot tighten DELETE, grep is the gate at `:75`) stands on the read-only charter and on FR-07's asymmetry, not on that sentence.
3. **Telemetry (U-002) is a real miss.** B's default is the CLI via Bash, which makes the omission larger for B than for the others. EVAL §7 puts `CODEGRAPH_TELEMETRY=0` only in the MCP entry and the Coder image, and `codegraph telemetry status/off` exists (EVAL §1, §2). The probe should record `telemetry` and flag it, as A does.
4. **Language dependence (U-003).** B never says that Markdown-only repos return nothing. EVAL §5.4 lists python 440, yaml 49, liquid 11.
5. **B's hook rejection is a value judgement.** `hooks.json` already runs SessionStart hooks with 5-10 s timeouts, so A's one-line status hook is feasible. B's D-03 argument that it "adds nothing the probe doesn't give" is arguable, not a proof. The 1 s cited in D-02 applies only to the pre-edit hook.
6. **Pre-edit timing.** B's I-07 runs after the diff exists. A's I-05 (Q1, before edits) matches "impact before edits" better. B has no answer for the Q1 gap (B ranks I-07 last).
7. **FR-12 changes a rule.** `dependent-impact` exempt from the out-of-hunk downgrade (`auggie-review SKILL.md:218`) is a semantic change to a validated rule. It is bounded (only when the call-site line is Read-verified) but it is B's riskiest proposal and A/C's context-only default is the safer first release.
8. **One probe per run (A-006).** B requires "once per run" (FR-01) while also saying to re-run `status` before the queries (§8). Those two statements are in tension for implement/pr-submit, which edit mid-run.
9. **B's scores use subjective V (1-5).** The formula is auditable, the inputs are judgement.
10. **Breadth.** B drops workflow and cleanup-audit and has 10 ideas; A covers more primitives (explain, index-repo, load, reuse-auditor liveness). Some of that breadth is low value, but the reuse-auditor liveness idea (A I-11) is not clearly wrong.

## Shared assumptions

| A-ID | Verdict | Reason |
|---|---|---|
| A-001 | ACCEPT | Seed constraint; B has the same rule (FR-02) and tests it by `codegraph` off PATH (FR-01). |
| A-002 | ACCEPT | Seed citation contract plus EVAL §5.5 gap; B enforces it (FR-06) and keeps `evidence-validator` Read-only. |
| A-003 | QUALIFY | The seed says auggie is unavailable in the run session, but primitives run elsewhere where auggie works; the fallback when auggie is down is Grep/Read. B's D-01 reasoning ("auggie offloads cost, explore adds it") is valid only when auggie is up. |
| A-004 | QUALIFY | The 24,913-character sample is one call with a two-word query; `maxFiles` (1-20, EVAL §3) was not varied. B's ban is on budgeted waves, not on explore generally, which is the right scope. |
| A-005 | ACCEPT as risk | Size of `callers`/`impact` output was never measured. B caps artifacts at 40 rows and 6 KB (FR-10) and 2K tokens per run (NFR-06) instead of claiming "a few hundred tokens". |
| A-006 | REJECT | Implement and pr-submit edit files mid-run; without an MCP client no watcher runs (EVAL §4). B should re-probe before queries (§8) and should reconcile with FR-01, see Concessions 8. |
| A-007 | REJECT | One symbol was verified. B treats non-empty lists as a lead and records `shown/total`; partial: still assumes call edges are complete for Python. |
| A-008 | QUALIFY | Only B marks `affected` unrun. Use it advisory first with the NFR-08 backtest. A and C should not make it a gate. |
| A-009 | ACCEPT | `init` costs about 34 MB and about 1 GB RSS (EVAL §5.4) and writes `.codegraph/`; read-only flows never init. |
| A-010 | ACCEPT | Discard foreign-index answers (B FR-03). The warning text is pinned to v1.6.2; B covers drift with golden fixtures (NFR-04). |
| A-011 | ACCEPT | Per-worktree init has no owner (EVAL §4, §7); B degrades to `uninitialized` and names `/sc:load --index` as a fallback owner, though A's dedicated command is cleaner. |
| A-012 | QUALIFY | Agents can Read refs by path, but the Skill call cost is unmeasured (B Q6). B's mitigation: a shared ref copied into consumers' `refs/` is an alternative to a skill. |

## Per-point positions

| ID | Superior | Reason |
|---|---|---|
| S-001 | none | cosmetic; B's `source_brief` field gives traceability only |
| S-002 | none | identical section order |
| S-003 | B+C | C puts the vector table up front; B adds explicit drops per vector |
| S-004 | A+B | A's seven classes distinguish scoped vs unrestricted Bash; B adds a stance column per blocker |
| S-005 | B | M/P/A classes feed the ranking score |
| S-006 | B | ten ideas cover all nine vectors; A's ranks 16-19 score about 1 |
| S-007 | A+B | A's layer 0 prerequisites with B's recomputable score table |
| S-008 | A+B | table with IDs, as both do; C's unnumbered bullets cannot be cross-referenced |
| S-009 | A+B | one subsection per candidate with fields; C's table loses interface detail |
| S-010 | A+C | invariants (A) and the observed-behaviour to contract-response table (C) |
| S-011 | none | counts do not indicate quality |
| C-001 | A+B | both stay beyond 1:1; C drifts into SYM/REF swaps |
| C-002 | B | artifacts in briefs avoid the listing blocker and keep agents read-only |
| C-003 | B | do not set `CODEGRAPH_MCP_TOOLS` until schema overhead is measured |
| C-004 | B | per-subcommand patterns because EVAL §2/§3 shows `install` edits Claude config |
| C-005 | A+B | A's capability map and kill switch with B's executable resolver script |
| C-006 | A+B | A's closed grep-testable vocabulary with B's `parse_failed` state; C's binary latch hides `stale` |
| C-007 | B | never sync; re-probe before queries (EVAL §5.7 lock failure) |
| C-008 | B | budget-based ban (below 8K, subagents) allows bounded interactive explore |
| C-009 | B | `startLine`/`endLine` span bounds the call-site Grep; C's drop-never-repair rule added |
| C-010 | B+C | evidence-validator stays Read-only; independence is the gate |
| C-011 | A | pre-edit impact at Q1 is truly before edits; B's I-07 is post-edit |
| C-012 | B | names the real blind spot (directory chunking plus out-of-hunk rule), see Concessions 7 |
| C-013 | B | advisory first, union only after backtest; `affected` was never run |
| C-014 | A+B | positional args or `--stdin` from a file; no pipeline under scoped Bash |
| C-015 | A+B | A's callers (limit 10) feeds B's pasted artifact precedent (`SKILL.md:281`); C's I-02 is a 1:1 swap |
| C-016 | A+B | both keep tasklist deterministic (`:1326`, `:1658`); workflow is optional and after a spike |
| C-017 | B | distinct production caller symbols via the runtime-surface table |
| C-018 | B | no new reflect field in v1, only `degraded_components` entries |
| C-019 | B | drop it; the DELETE gate stays grep (`:75`) and the audit is read-only, though B's D-05 sentence is unproven |
| C-020 | B | spike before adopting; A and C depend on an unlisted tool in a read-only agent |
| C-021 | none | all onboarding claims are unmeasured; the 58K to 3K figure is the primitive's own |
| C-022 | B | no new hooks; value judgement (see Concessions 5) |
| C-023 | A | a dedicated user-typed command with a nested-worktree refusal beats folding `init` into `/sc:load` |
| C-024 | A+B | A's frequency factor with B's evidence confidence weight |
| C-025 | A+B | enablers first; add A's troubleshoot callers and B's token guard |
| C-026 | A+B | A's tasklist and graph-scout drops with B's hook and producer-enumeration drops |
| C-027 | A+B | B's probe plus blast-radius candidates with A's `/sc:graph` lifecycle command |
| C-028 | B | blast-radius output has prod/test split, shown/total and call-site status |
| C-029 | A+B | B's wider caller list, trimmed to where the probe pays (not `explain`) |
| C-030 | B | re-query once when total is 100 or less; notes CLI `callers` lacks a documented file argument |
| C-031 | B+C | golden fixtures, byte-identical output (B) and per-run caching (C) |
| C-032 | A+B | A's telemetry and language-dependence risks with B's allowlist blast radius |
| C-033 | A+B | A's kill switch and B's absence equals native path |
| X-001 | B | v1 agents get artifacts; no MCP names until listed and measured |
| X-002 | B | no wildcard; EVAL §2/§3 |
| X-003 | B | do not set the env in v1; measure schema overhead first |
| X-004 | B+C | validator remains `Read, Grep, Glob` (`evidence-validator.md:5`) |
| X-005 | A | only a user-typed command may init; B's `/sc:load --index` mixes mutation into a context command |
| X-006 | B+C | primitives never call `sync` |
| X-007 | B | no SessionStart hook; value judgement, see Concessions 5 |
| X-008 | B | no gate change until the backtest passes |
| X-009 | A+B | keep today's downgrade by default; allow a Read-verified `dependent-impact` exemption |
| X-010 | A+B | both drop tasklist for determinism; C's I-11 conflicts with it |
| X-011 | B | workflow preview is class A (spec text to symbol is judgement) |
| X-012 | B+C | zero callers proves nothing; A's "extra DELETE evidence" violates FR-07 |
| X-013 | B | count distinct production caller symbols |
| X-014 | B | bounded interactive explore only |
| X-015 | A+B | `:218` Wave 1 is about 3k; C cites the Wave 1.5 line (`:256`) |
| X-016 | A+B | A's status line, B's explicit `--index`; C's drop is fine for a rewrite only |
| X-017 | B | `status` latency is UNVERIFIED; EVAL §5.5 timed `query` and `callers` only |
| X-018 | A | correct `mcp__codegraph__codegraph_*` names; B avoids MCP names, C's would not match |
| X-019 | B | CLI outline route uses `query --json` and `startLine`/`endLine`, not `node symbolsOnly` |
| X-020 | none | neither claim is in EVAL; both unverified |
| X-021 | none | B overstates "23 callers, 2 production"; EVAL shows 20 of 23 inspected |
