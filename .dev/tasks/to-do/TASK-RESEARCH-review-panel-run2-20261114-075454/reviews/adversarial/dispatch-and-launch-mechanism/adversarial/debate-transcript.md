# Adversarial Debate Transcript

Slot C-07 (dispatch-and-launch-mechanism). Variant 1 = Proposal A (`variant-1-original.md`: per-environment launch adapters, raw-id `claude -p --model` with a transcript identity check, class-word Agent call kept for `reflect-reviewer`, reflect ceiling widened). Variant 2 = Proposal B (`variant-2-original.md`: class-word dispatch only, no raw-id launcher in the core).

The full advocate texts are kept verbatim in the round files next to this transcript: `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`, and the Round 2.5 raw output `round2.5-fault-finder-raw.md`. This transcript condenses them and holds the scoring matrix and the convergence assessment.

## Metadata
- Depth: standard
- Rounds completed: 2 (plus Round 2.5 invariant probe)
- Convergence achieved: 80.77% of diff points agreed (21 of 26); status BLOCKED_BY_INVARIANTS (see Convergence Assessment)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2
- Diff points debated: 26 = S-001..S-003 (3), C-001..C-009 (9), X-001..X-009 (9), promoted shared assumptions A-002..A-006 (5). A-001 is STATED and was not promoted (both advocates answered it anyway: A QUALIFY, B ACCEPT).
- Taxonomy coverage (AD-5): L1 surface (S-001, X-007), L2 structural (S-002, S-003, C-001, C-002, C-007, C-008, C-009, X-006, A-001) and L3 state-mechanics (the 16 other points) all have debated points. No forced round was needed.
- Omissions: none. Both advocates answered A-001..A-006 in Round 1 and A-002..A-006 again in Round 2.

## Round 1: Advocate Statements

### Variant 1 Advocate (Proposal A; default model, default persona)
**Position**: A class-word-only core cannot be the whole answer for gateway panels (a class word does not name a model, the binding is set per session, nothing mechanical forces the orchestrator to pass it); B is right about what reflect should ship first (ceiling stays, read-only from the agent file until a process-level probe passes). Calibrated end state offered in Round 1: a staged hybrid, B's dispatch contract now, A's id-based adapters as data and a launcher not admitted past the reflect ceiling until the read-only probe M-2 passes.

**Steelman of Variant 2**: Read-only by construction is the property the research calls HARD (INV-G); exactly one path has it today, the agent file with a `tools:` allowlist without Bash/Edit/Write/Task (`reflect-reviewer.md:5-8`), pinned statically by `test_reviewer_readonly_tools.py`; the E2 raw-id launcher ran `bypassPermissions` with only `Edit Write NotebookEdit` disallowed (Bash open); reach cost is smaller than it looks (3-reviewer cap equals 3 launch words; class words reached `gpt-6-luna` and `claude-haiku-5-5` in recorded runs); the `--env gateway` refusal is an empty data map, not the ceiling; raw ids also fail over in the shim and E2's ladder reassigns `MODEL`, so identity is a transcript read on both paths.

**Key strengths claimed**:
1. A model id is a stable address, a class word a per-session alias: `haiku` was served `gpt-6.1-sol`, `claude-haiku-5-5` and `gpt-6-luna` across combos; `select_env` returns `gateway` for any session with `T3Model01` set (`panel.py:485-494`).
2. Reach is bounded by the enum (`docs/reference/model-aliases.md:48`): 12 non-Fable models share 3 usable words.
3. A launched `--model` argument cannot be dropped by the orchestrator (run A-r3 dropped it six times); B's dispatch-error rule has no code enforcing it.
4. The additive `adapters` form moves no frozen test (`test_review_panel.py:303-308`).
5. The reflect ceiling is a template-class rule, not a limit of `resolve` (`test_review_panel.py:243-257`).
6. A names a falsifiable probe for INV-G (M-2) and says what A becomes if it fails; B proposes no dynamic read-only test.
7. Identity is judged per attempt against the id requested for that attempt.

**Weaknesses identified in Variant 2**:
1. The map B fills is a static claim about a dynamic binding; the resolver would pin the wrong intended model.
2. Nothing checks that the map is one-to-one (`distinct_across_slots` excludes a repeated model, not a repeated word, `panel.py:631-635`).
3. The dispatch-error rule has no enforcer; the replay runs after the votes.
4. B's identity capture is unbuilt (`hooks.json:179` registers `SubagentStop` only for a freshness counter).
5. `live7` (7 reviewers) and larger PR panels are out of reach.
6. B's "checkable by one rule" holds for agent files only (`process.py:150-154` passes no allowlist).
7. B misstated A on X-002 and X-007.

**Concessions**: X-009 is a real defect (ceiling widened without reading `read_only`); X-008 (E2 identity evidence ran under `bypassPermissions`, which `--restricted` refuses); X-005 overstated ("silent swap", the fallback is logged); "no check at all today" for the class-word path is too strong (`SKILL.md:341`); the `agent-class` adapter is not a launcher (the Agent call is made by the orchestrator); X-003 (D4 lists "gateway" separately from "null `launch`"); C-007 (build on `ClaudeProcess`, do not rewrite E2's shell); until M-2 passes A and B ship the same thing.

**Shared assumptions**: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 ACCEPT; A-006 REJECT.

### Variant 2 Advocate (Proposal B; default model, default persona)
**Position**: Variant 2 is the better core for the consumers that matter first (reflect, rf-qa replacement) because the only repo-owned, test-pinned read-only property is the agent-file path, and it fixes the `--env gateway` refusal with one data edit. Concedes Variant 1 is better on reach, on concreteness about served-model recording, and on test format, and concedes X-002 and X-007. Calibrated end state: Variant 2 now, with Variant 1's M-1/M-2 probes kept as the entry gate for any later raw-id adapter.

**Steelman of Variant 1**: The product can resolve a gateway panel but cannot launch one; a class word is an environment-dependent alias; the Agent `model` argument is an enum of four words so tier-2b/3/4 and non-first-slot models cannot be named; a raw-id launcher names the model and reads `message.model` per attempt against the id requested for that attempt (`run-reviewer.sh:51,56`); A names the read-only cost honestly (`read_only: unproven`, `agent-class` default for untrusted diffs, M-2); only A designs for panels beyond three or four distinct gateway models and for the shim failover on named ids.

**Key strengths claimed**:
1. Read-only by construction is repo-owned and test-pinned on the path B keeps (`reflect-reviewer.md:5-8`, `test_reviewer_readonly_tools.py:30,59-66,100-103`; the dynamic test is deferred, `:12`).
2. The gateway refusal is a data gap, not a ceiling (`panel.py:72-73,153-156`; `review-tiers.default.json:29`).
3. Class words have reached gateway models in practice (D1-D3, E1-E3).
4. The identity check is not a property of the raw-id path; both read the same transcript field; no product code reads it on either path.
5. The raw-id path does not buy identity assurance as built (shim failover; `MODEL_OK` is relative to the ladder step).
6. A's own evidence does not transfer to A's own read-only adapter (X-008).
7. The core stays launch-free and deterministic (`test_review_panel.py:294-300`).
8. Raw-id substrate already exists where an engine needs it (`ClaudeProcess` `--model`, `reviewer_profile`).
9. A re-review is one Agent call with the original slot's class word.

**Weaknesses identified in Variant 1**:
1. The `agent-class` adapter has no executor in a Python module.
2. The ceiling is widened before the read-only condition is checked (X-009).
3. Identity evidence does not carry to the read-only adapter (X-008).
4. Two parallel maps (`launch`, `adapters`) with no stated precedence.
5. A rebuilds a launcher when `ClaudeProcess` exists.
6. A's reach advantage is deferred for its main (INV-G) consumers.
7. A's D4 argument for the additive key is partly wrong (X-003).
8. A's cost and tool-surface claims for the restricted child are unmeasured (MCP tools under `--restricted`).

**Concessions**: X-002 and X-007 (B misdescribed A and missed an existing static test); X-006 scope (the `ClaudeProcess` callers launch one model per run); U-008 (served-model capture is unbuilt on B's path); reach (B cannot name tier-2b/3/4 or non-first-slot models, and panel composition depends on the launching session); the dispatch-error rule is a prompt rule; `permissionMode: plan` as a second layer is unverified; if M-2 passes, B's read-only edge narrows.

**Shared assumptions**: A-001 ACCEPT; A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 ACCEPT; A-006 REJECT.

## Round 2: Rebuttals

### Variant 1 Rebuttal (advocate A, sequential first)
Conceded B's weaknesses 1, 2, 3, 4, 5, 6 and 7 against Variant 1 as written and restated the design as V1' (later called H-gated): one `launch` vocabulary in the existing field (a class word, or `claude-p`), no `adapters` key, no `read_only: unproven` marker, the class-word half is "a dispatch rule plus a transcript reader" and only `claude-p` is a launcher, the launcher a thin caller of `ClaudeProcess(reviewer_profile=True, model=..., extra_args=[restricted flags])`, `_REFLECT_LAUNCH` untouched until M-1 and M-2 pass under the restricted flag set.

New evidence brought: N1 `validate_tiers` rejects any environment key outside `available, stand_ins, launch, note` (`panel.py:371-373`) and `load_tiers` raises (`:477-481`), so `adapters` would also fail on an older installed CLI; N2 the `launch` value has almost no Python consumers; N3 the packaged `reflect-pre` reaches five models for three class words, chosen per run id (`panel.py:545,606-610`; `review-panel.reflect-pre.json:9-11`), `reflect-lite` nine; N4 a per-workspace tier file already exists (`find_path`, `panel.py:397-419`); N5 `--restricted`, `--tools`, `--strict-mcp-config` exist on 2.1.325 and `--restricted` ignores the settings files that decide a `reviewer_profile` child's surface; N6 `ClaudeProcess` already carries `--model`, `reviewer_profile` and `extra_args`; N7 the launcher must walk `fallbacks` once with an exclusion list (E2's cyclic ladder ran a review on Qwen3.8-max); N8 the full commit id in Variant 1 line 7 is not a valid object (the short form `6c09843` resolves).

Resolution proposed ("H-gated"): ship now S1 dispatch rule (B's), S2 no data/validator/resolver/ceiling change, S3 one transcript reader, S4 dynamic read-only test on the Agent path, S5 class-word maps live in the workspace tier file (`find_path`); gated G1 identity and reach under restricted flags, G2 read-only plus tool surface, G3 no regression, G4 cost (informational); if G1-G3 pass, launcher, `gateway.launch` fill with `claude-p` for the ids that passed, and a one-value ceiling widening ship together.

Residuals held: R1 packaged `gateway.launch` stays `{}`; R2 launcher lives in the shared review layer (about 55%); R3 raw-id reach should be measured now; R4 only a Python-built `--model` removes the A-r3 omission; R5 recorder differentiator for `claude-p` is narrow.

Final shared assumptions: A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 ACCEPT; A-006 REJECT.

### Variant 2 Rebuttal (advocate B, sequential second; saw A's Round 2)
Conceded the packaged `gateway.launch` fill is wrong and withdrew it (v2:18), on three checks: in-memory runs over 400 run ids show `reflect-pre` slots `t1b` and `t1a` constant and `t4` varying across three models, `reflect-lite` 17 distinct per-run panels over nine models; the documented default binding (`haiku` = tier 2) disagrees with every tier 4 model (`model-aliases.md:26-28,33-35`; `results.jsonl` A-r1, A-r2); any packaged tier edit changes `tiers_sha256` and orphans recorded shadow runs (`reflect_shadow_exit.py:128-132,205-207`); `gateway` is the default environment when `$T3Model01` is set (`panel.py:485-494`). Confirmed N1 and said it does not touch B (B adds no key). Conceded weaknesses 1, 2, 4, 5 (capability gap), 6, 7 and A's concessions 5, 8, 1, 2, 7, 4. Contested that the class-word path has no mechanical fix for A-r3: a PreToolUse hook on `Agent` calls has repo precedent (`hooks.json:116`, `launch-level-guard.sh:182-205`); whether the payload carries `model` is unverified.

Resolution proposed ("V2-bound"): ship now S1-S5 as in H-gated plus S6 shape tests and S7 (PreToolUse guard, named, not built); S5 realized as `panel resolve --tiers <file> --env <new env name>` with `available`, `stand_ins`, one-word-per-model `launch`, `note` (an in-memory run resolved `reflect-pre` and `reflect-lite` to one panel over 400 run ids, `_check_reflect_resolution` passing); gated G2 before any raw-id reviewer in an INV-G module, G1 as a measurement and an admission gate but not a ship gate; a launcher is built only when a named consumer needs a model no class word can serve (a panel with more than three distinct served models) and G1 and G2 passed, as a `ClaudeProcess` caller in the consuming engine; the packaged `gateway` environment is never filled (a new environment name instead).

Residuals held: RB1 passing G1/G2 does not commit anyone to build; RB2 launcher location (consuming engine, about 55%); RB3 what to count for the reach trigger (per run three words, the five and nine are unions over seeds); RB4 whether the omitted-argument failure is fixable only in Python is not established (one spike answers it); RB5 recorder differentiator disappears if the `SubagentStop` spike passes; RB6 never fill the packaged `gateway` environment.

Final shared assumptions: A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 ACCEPT; A-006 REJECT.

## Round 2.5: Invariant Probe

Independent fault-finder (see `invariant-probe.md` and `round2.5-fault-finder-raw.md`): 19 findings, 3 ADDRESSED, 16 UNADDRESSED (1 HIGH: INV-017; 12 MEDIUM; 3 LOW). INV-017 (sufficiency challenge): the ship-now set S1-S6 does not by itself close the A-r3 collapse failure, because in shadow the dispatch is the legacy dispatch, calibrator Agent calls carry a null word in six of 15 runs and no S item covers them, an omitted `model` falls back to `model: sonnet`, and the only mechanical guard (S7) is unbuilt with an unverified payload. Standard depth has no Round 3, so nothing was resolved in a later round.

## Scoring Matrix

Winner and confidence per point are taken from the two Round 2 position tables. Where both advocates name the same winner the confidence is the mean of their two stated confidences (rounded); where the labels differ the point is unresolved at 50%. "Hybrid" names the combination both advocates described.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Variant 2 | 55% | B's tagged evidence table and "what the evidence does not show" list are easier to audit than A's inline-tagged prose; layout only. |
| S-002 | Hybrid | 58% | A's rated Preserved/Endangered split plus B's one-row-per-invariant coverage, plus the shadow-hash row B missed (`reflect_shadow_exit.py:128`). |
| S-003 | Hybrid | 68% | A's right-if/wrong-if rule and fallback on every measurement applied to B's head-to-head, collapse replay and `SubagentStop` spike (and S6 shape tests). |
| C-001 | Hybrid | 69% | Dispatch rule and Agent path now; a `claude-p` launch only after the gates (H-gated and V2-bound agree on ship-now; they differ on the build commitment). |
| C-002 | Variant 1 | 70% | Raw ids reach models no class word names; packaged `reflect-pre` reaches five models for three words (`review-panel.reflect-pre.json:9-11`, `panel.py:545`); but nothing that ships now needs it. |
| C-003 | Hybrid | 73% | Neither a packaged class-word fill (wrong per seed) nor an `adapters` key (rejected, `panel.py:371-373`): bindings as data in a workspace or explicit `--tiers` file, packaged `gateway` and its hash untouched. |
| C-004 | Variant 2 | 71% | `_check_reflect_resolution` reads only `launch` (`panel.py:153-156`); the ceiling stays now, any widening is the reviewed edit after the read-only gate. |
| C-005 | Variant 2 | 69% | Agent-file allowlist is repo-owned and statically pinned (`reflect-reviewer.md:5-8`, `test_reviewer_readonly_tools.py`); `claude-p` is unproven, no gateway-id run exists. |
| C-006 | Hybrid | 65% | A's outcome row (`model_requested`, `model_observed`, `identity_source`, tool names) fed first by B's Agent sidechain transcript; home is slot C-08; both unbuilt. |
| C-007 | Variant 2 | 73% | `ClaudeProcess` already has `--model`, `reviewer_profile`, `extra_args` (`process.py:150-165`); A's rebuild of E2's shell is not needed (A's V1' now builds on it). |
| C-008 | Variant 2 | 57% | `--revagent` takes four class words; rf-qa lenses differ by lens; A's PR advantage for non-Claude reviewers is itself gated on the read-only probe. |
| C-009 | Neither | 50% | A's N children per PR round and B's lost hook-exchange families for subagents are both real and both unmeasured. |
| X-001 | Unresolved | 50% | A: Variant 1 (58%, only A names a probe and falsifier); B: Neither (55%, flags exist on 2.1.325, `ClaudeProcess` passes none, no gateway-id run). |
| X-002 | Variant 1 | 90% | The pin asserts `launch is None` (`test_review_panel.py:303-308`); A leaves `gateway.launch` `{}`, so it passes; B's "A rewrites it" was wrong for A's additive form. |
| X-003 | Variant 2 | 83% | `SKILL.md:320` lists "gateway" and "a null `launch`" as separate triggers; a fill does not change D4's routing. |
| X-004 | Variant 2 | 60% | A transcript read works on both paths; A's "only thing that catches it" overstates; no product code records it on either path. |
| X-005 | Neither | 75% | `run-reviewer.sh:75` logs each fallback; `:58` records the current `$MODEL`; both variants blur the script ladder and shim failover. |
| X-006 | Unresolved | 50% | A: Variant 2 (60%, B's account of the `ClaudeProcess` substrate is the more complete); B: Neither (60%, both true at scope; no caller launches several differently-modelled reviewers). |
| X-007 | Neither | 65% | The static tools test exists (B's "not found" was wrong); it does not pin `permissionMode` and defers the dynamic test; A claimed nothing. |
| X-008 | Variant 2 | 75% | E2 identity ran under `bypassPermissions` (`run-reviewer.sh:48`); `--restricted` refuses it, so E2's rows do not transfer to A's read-only adapter. |
| X-009 | Variant 2 | 80% | `panel.py:153-156` reads only `launch`; A's `adapter == claude-p` acceptance reads no `read_only`; both advocates agree the fix is to leave the ceiling alone until the read-only gate passes. |
| A-002 | Neither | 60% | Both read `message.model`; it is not an echo of the request but failover truthfulness is unproven; a second source (`modelUsage`, `resolvedModel`) is a candidate cross-check. Both QUALIFY. |
| A-003 | Unresolved | 50% | A: Neither (60); B: Hybrid (60, static allowlist plus A's dynamic probe on both paths). Both QUALIFY with the same substance (dynamic test deferred for both paths). |
| A-004 | Unresolved | 50% | A: Variant 1 (65); B: Variant 2 (55). Both QUALIFY: accept the cap of three; the packaged word map is not correct for random slots; sufficiency for diversity and quorum unmeasured. |
| A-005 | Neither | 72% | Shadow passes `--env anthropic-only` (`SKILL.md:340`), D4 lists "gateway" (`:320`); neither design is exercised by shadow; any packaged tier edit orphans recorded shadow runs by hash. Both ACCEPT. |
| A-006 | Unresolved | 50% | A: Variant 1 (55); B: Neither (55). Both REJECT: run A-r3 contradicts orchestrator compliance; neither position makes it mechanical on the class-word path today. |

Tally of points won (agreed winners only): Variant 1 2 (C-002, X-002); Variant 2 9 (S-001, C-004, C-005, C-007, C-008, X-003, X-004, X-008, X-009); Hybrid 5 (S-002, S-003, C-001, C-003, C-006); Neither 5 (C-009, X-005, X-007, A-002, A-005); unresolved 5 (X-001, X-006, A-003, A-004, A-006). Total 26.

## Convergence Assessment
- Points resolved: 21 of 26 (both Round 2 tables name the same winner; with two advocates agreement is unanimous or absent)
- Alignment: 80.77%
- Threshold: 80%
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement 80.77% is at or above the 80% threshold and all three taxonomy levels are covered, but 1 HIGH-severity UNADDRESSED invariant remains: INV-017)
- Unresolved points: X-001, X-006, A-003, A-004, A-006
- Unaddressed invariants: HIGH INV-017 (blocks); 12 MEDIUM and 3 LOW listed in `invariant-probe.md` (do not block)
- Early termination: none triggered (not unanimous; no 2-round stable majority because Round 1 agreement was 16 of 26 = 61.54% (the two Round 1 position tables differed on C-001, C-003, C-007, X-001, X-004, X-006, X-007, A-003, A-004, A-006); Round 3 not run at `--depth standard`).
- Convergence between Round 1 and Round 2: both advocates moved to a named hybrid in Round 2 on the substance (ship the dispatch rule, the reader and a read-only test now; keep the packaged `gateway` environment empty; gate any raw-id launcher on a read-only probe under the restricted flag set). The residual differences that remain are the commitment to build after the gates (A: ship together; B: only on a named consumer trigger) and the launcher's location (A: shared layer; B: consuming engine).
