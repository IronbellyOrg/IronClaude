# Diff Analysis: Design proposal comparison for conflict C03 (model-tier-config)

## Metadata
- Generated: 2026-11-13T23:06:00+00:00
- Mode: A (compare). Variant A = `proposal-a.md` (copy: `variant-1-original.md`); Variant B = `proposal-b.md` (copy: `variant-2-original.md`)
- Variant A: "central panel targets anthropic-only, launching by class name" (synth-04 Option A). Variant B: "central panel targets the gateway, with launch adapters and dated tier data" (synth-04 Option B).
- Variants compared: 2
- Focus areas: correctness, risk, test-coverage
- Total differences found: 29 diff points (structural 7, content 15, contradictions 3, shared-assumption points 4); unique contributions 21 (not debate points)
- Categories: structural (7), content (15), contradictions (3), unique (21), shared assumptions (6 analysed: 3 UNSTATED promoted, 1 CONTRADICTED flagged, 2 STATED)
- Similarity check: both variants share the same 7 H2 sections in the same order, but their proposed designs are incompatible on target environment, launch contract and scope. Difference is far above the 10% threshold; debate proceeds.
- Orchestrator ground-truth checks done before analysis (read-only, this checkout, branch ironbelly/shadow-runs): `select_env` (`panel.py:485-494`) reads only `T3Model01`; its only production caller is `panel_cmd.py:64/96`; gateway `launch: {}` and anthropic-only `launch` map confirmed in `review-tiers.default.json`; `_check_reflect_resolution` (`panel.py:137-157`) confirmed; `advance_stage` hashes the whole payload and validates only `reviewers_requested`, `reviewers_resolved`, `outputs` (`manifest.py:~277-316`), a different payload on the same stage raises `Conflict`; `telemetry.py:49` has `"model": ("resolved", "launch", "observed")`; `test_gateway_resolution_prints_launch_null` is at `test_review_panel.py:303-308`; `select_env` tests at `:331-341` and `test_review_cli.py:84`; the loop prompt at `document_review_loop_prompts.md:70` calls `panel resolve` without `--env`; the shell has `T3Model01=glm-5.3`, `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b[1m]`, `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]`, and `T4Model04=muse-ember-1.0`; `uv run superclaude review panel resolve --run-id vcheck` resolves `environment: gateway` with `launch: null` on this machine. `muse-ember` appears in no file under `src/`.

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Preamble | Position paragraph, "Source of the conflict" paragraph, and a long evidence-tag legend (CR, RR, `[external]`) | One-sentence side/conflict/status line plus tag legend (`[CODE]`, `[RES]`, `[E2@4a22d74]`, `[EXT]`, `[UNVERIFIED]`) | Low |
| S-002 | Design section organisation | "Core" list of 5 items, then a consumer table; no rival-option section | "Core" list of 6 items, a consumer table, plus a paragraph "What B decides that the provisional Option C does not" | Low |
| S-003 | Evidence presentation and tagging | 6 bullet groups, 22 items EV-1..EV-22, tags CODE-VERIFIED / RUN / OBSERVED-RUNTIME / DOC-SOURCED / external; claims "I ran the command while writing" | 5 tables A-E, 27 numbered rows with columns claim / research file / code location / tag; tag `[RES]` means "taken from a research file and not re-read in code" | Medium |
| S-004 | Form of the correctness argument | 7 numbered steps plus an explicit "What this argument does not show" paragraph | 7 properties P1-P7, P7 states what B does not claim | Low |
| S-005 | Placement of the weakest point | Separate paragraph "The weakest point" before the 10-row risk table | Folded into row R1 of a 9-row risk table | Low |
| S-006 | Test-coverage layout | Three groups (changes / stay-green list / 7 new tests) plus an exact `uv run pytest` run set | Three groups as tables (5 changing rows, stay-green list, 11 new-test rows) plus an explicit "not in scope" line; no run command | Low |
| S-007 | Cost and staging | One flat size table, XS to S total, no stages, recurring-cost paragraph, "Items I did not check" | Four stages B-1..B-4 each with size and gate, overall L, rollback paragraph | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | Environment the central panel (non-reflect consumers) targets | `anthropic-only`. `select_env` loses its `T3Model01` rule; default becomes the one supported cell on every machine | `gateway` for every consumer except reflect's Stage 3 gate; `select_env` precedence unchanged (`T3Model01` still selects gateway, else anthropic-only) | High |
| C-002 | The gateway environment's empty `launch: {}` | Keep it empty as an accepted fact; a consumer that selects it runs the legacy path and records `panel_fallback_reason` (rule D4) | Fill it with real entries `cli-model:<raw id>` for 12 ids; treat the empty map as a defect | High |
| C-003 | Launch contract and schema | Class names only (`sonnet`, `opus`, `haiku`); tier file bytes unchanged; both goldens stay valid | `<adapter>:<argument>` grammar (`agent-class`, `cli-model`, `swarm`), bare string means `agent-class:<string>`; `parse_launch`; schema id stays `review-tiers/1`; packaged-tier golden regenerates | High |
| C-004 | Dated facts and provenance | Nothing dated enters the tier file; the dated fact is the run's `launch_binding` in the manifest | Tier file gains a `provenance` object (`tiers_as_of`, `gateway_observed_on`, `ccsession_models_version`, `evidence[]`); resolution gains optional `tiers_as_of`; a test couples provenance version to `ccsession-models.json` | Medium |
| C-005 | Handling of the label-vs-serving mismatch (haiku slot served by `gpt-6.1-sol`) | Record `launch_binding` (the three `ANTHROPIC_DEFAULT_*_MODEL` values) in the `resolved` payload; add C08 triple; launch-vs-observed built-in check; warn when two classes bind the same model; no route computation | New read-only `panel verify` with V3 route check: class, env var, tier alias, first model, class; emits `warn` with an expected served model (derived, not observed) | High |
| C-006 | Alias-existence check (D12) and environment detection | Removes the single-variable detection by changing the default; no alias check added ("no gateway dispatch to protect") | Keeps `T3Model01` detection; adds `check_required_env` in the command layer and `verify` V2 (tier to Coder slot `T<N>[letter]Model01`); `resolve` stays pure | Medium |
| C-007 | Missing data: `tier0` and `muse-ember-1.0` | Neither added; ember named as absent (EV-14); no `tier0` (reflect "no tier0" rule stays inert) | Adds `tier0` (+ `gpt-6-astra` class, names) so the rule is live; ember only in one coordinated PR with `ccsession-models.json`, `MODEL-TIERS.md`, Coder slot, else declared out of scope in `provenance.evidence` | Medium |
| C-008 | Reflect profile check | `_check_reflect_resolution` unchanged; D4 reason stays `launch None is not one of sonnet, opus, haiku` | The check tests the parsed adapter and argument; gateway error names the adapter; the message becomes the `panel_fallback_reason` | Medium |
| C-009 | New CLI surface | None; one default changes | `panel verify` (V1 completeness, V2 alias existence, V3 route check, V4 provenance age); `panel validate --kind tiers` checks grammar and provenance | Medium |
| C-010 | Code-driven Tier 2 engine (C17) | Out of C03; "when Stage 5 replaces it, its reviewers must be expressible as classes" (R7) | `swarm:` adapter reserved in the grammar for it; no packaged data uses it | Medium |
| C-011 | How E2's best panels (mixed vendors, `haiku + 2x luna`) become expressible | Operator binds the three class variables to raw ids before the session (combination runs: 15 of 15 reached `published`); at most 3 distinct models | Per-slot `cli-model:<raw id>` entries and the alias order already in the tier file; runs only through a `claude -p` dispatcher that C09 Option C must supply (not delivered by B) | Medium |
| C-012 | Test impact | 2 existing tests flipped (`test_select_env_precedence`, `test_panel_resolve_gateway_when_t3model01_is_set`); both goldens untouched; 7 new tests (1, 2, 3, 7 C03-specific; 4, 5, 6 shared with C08/C09) | 5 existing test groups touched (gateway-null test rewritten, packaged golden regenerated, coupling test extended, live7, skill needles); about 11 new tests incl. packaged-data completeness and old-vs-new backward-compat | Medium |
| C-013 | Effort and risk | XS to S, Medium risk (synth rating XS/Medium) | L overall, High risk (synth rating L/High); B-1 is M | Medium |
| C-014 | Reversibility and owner-decision safety (O-2) | Nothing deleted; gateway adapter later is additive; `select_env` flip reversible with one line | Entries and `provenance` are data; removing them returns today's behaviour; grammar is a superset; owner must accept R1 before gateway entries ship | Low |
| C-015 | Use of external and E2 evidence | Platform docs (Agent `model` parameter takes only an alias) as `[external]`; E2 used only as supporting, DOC-SOURCED | Adds external self-preference literature (rows 26-27) with its own qualification; E2 rows read via `git show` only | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Can a panel with non-Claude members run through in-session Agent dispatch? | Yes by operator class binding: "Raw model ids work as class values" (EV-9), combos C, D, E served `claude-haiku-5-5` and `gpt-6-luna` through classes; 14 of 15 runs passed a class on every call (EV-7) | R3: "In-session Agent calls cannot pass a raw gateway id ... a gateway panel with non-Claude members cannot run inside reflect's in-session dispatch. Certain for that combination." B's own evidence row 4 records the haiku class serving `gpt-6.1-sol` in-session | High |
| X-002 | What the default environment is for non-reflect consumers | Default is the defect: omitting `--env` on a ccsession machine gives `gateway` and a panel with no launch values (EV-1, EV-3, EV-20); fix by changing the default | Consumers table says "Default environment is the gateway", but the CLI section keeps `--env` precedence (`T3Model01` set means gateway, else anthropic-only), so a machine without `T3Model01` resolves anthropic-only; B treats the single-variable detection as acceptable behind a D12 check | Medium |
| X-003 | Does filling the gateway launch map remove a record that describes something that did not run? | The anthropic-only label already describes a route that did not serve (EV-11, EV-12); the gateway `{}` honestly says "no dispatch defined" | P-intro: B "removes the one property that is false today (a launch label that does not match what serves)", yet R1 (weakest point): the new `cli-model:` entries "describe a route that nothing executes yet" until C09 Option C exists, "repeating the defect research 04 §10 calls the highest-risk gap" | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | `select_env` default flip: removes the `T3Model01` rule so forgetting `--env` cannot silently yield a no-launch panel; blast radius is one production caller (`panel_cmd.py`) | High |
| U-002 | A | `launch_binding` recorded as an extra key of the `resolved` payload, no manifest schema change (`advance_stage` validates only 3 keys); replay-identical and `Conflict` on a different binding | High |
| U-003 | A | Platform-documentation evidence that an Agent call's `model` parameter takes only an alias (EV-5), with the family-alias-runs-on-parent-model caveat (R2) | High |
| U-004 | A | Class binding as the gateway reachability route, backed by dated observed runs (combos C, D, E; 15 of 15 reached `published`) | High |
| U-005 | A | Dispatcher precondition tests: `launch` null, outside class set or `fable` is a dispatch error; every Agent call carries `model == launch`; absent class never falls to the frontmatter default (the A3 collapse) | High |
| U-006 | A | Swap fixture test: recorded stream where haiku was served by `gpt-6.1-sol` must fail launch-vs-observed; no stream gives `observed: unknown` with `identity_source: requested-pinned`, never `observed` | High |
| U-007 | A | Gateway-stays-fail-closed-for-reflect test through the CLI (no test pins `launch None is not one of` today) and a D4 `panel_fallback_reason` test (rule exists only as skill text) | Medium |
| U-008 | A | Class-ceiling test and risk R4: at most 3 distinct models per panel; warn when two classes bind the same model | Medium |
| U-009 | A | Explicit "What this argument does not show" paragraph and "Items I did not check" list (candid limits) | Medium |
| U-010 | A | Risk R6: the default template resolves `sonnet + 3x haiku class` in anthropic-only, three reviewers on one bound model flagged only by `stand_in: true` | Medium |
| U-011 | B | Launch grammar `<adapter>:<argument>` with bare-string backward compatibility and `parse_launch`; matches the adapter names the decided C09 already uses | High |
| U-012 | B | `panel verify` read-only preflight V1-V4 including the V3 route check that would flag the 2026-11-13 haiku to `gpt-6.1-sol` case from the live environment | High |
| U-013 | B | D12 alias-existence check (`check_required_env`) in the command layer, keeping `resolve` pure; covers the untested `T2bModel01` case | High |
| U-014 | B | Evidence that the repo's own update checklist (Coder env, `ccsession-models.json`, `MODEL-TIERS.md`) leaves `review-tiers.default.json` out, with only a length-coupling test; fix: provenance version coupling test, fourth checklist file | High |
| U-015 | B | Packaged-data completeness test (every gateway-reachable model has a parsing `launch`), the test that would have caught `launch: {}` | High |
| U-016 | B | Backward-compatibility test: old and new tier files resolve identically for `default` and `live7` in anthropic-only after removing `tiers_sha256` and `tiers_as_of` | High |
| U-017 | B | `tier0` added so the reflect "no tier0" rule (`panel.py:95-117`) is no longer inert, with a positive test | Medium |
| U-018 | B | Staged delivery B-1..B-4 with a gate per stage; ember handled as a coordinated PR or declared out of scope | Medium |
| U-019 | B | Slot-name derivation test (`tier2b` to `T2bModel01`) against `ccsession-models.json` `models_env[0]` | Low |
| U-020 | B | External self-preference evidence (NeurIPS 2024, arXiv 2601.22548 reanalysis) used to bound claims about vendor mix | Low |
| U-021 | B | Schema-evolution note R5: `review-tiers/1` accepts a newer file in an older package; option to bump to `review-tiers/2` | Low |

## Shared Assumptions

Agreement points scanned: (1) both keep reflect's Stage 3 gate on `--env anthropic-only` with class launch; (2) both treat C08 (identity triple) and C09 (dispatcher) as decided and delivered elsewhere; (3) both accept that the anthropic-only label is untrue at serving time on this machine; (4) both cite E2 only as supporting, with a model-choice ceiling near 2-2.5 of 14; (5) both leave the code-driven Tier 2 engine to C17; (6) both rely on one gateway, 2026-11-11 to 2026-11-13.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|-----------|----------------|----------|
| A-001 | Agreement 2 | A resolution-driven dispatcher (C09) that enforces `model == launch` (A) or reads the adapter (B) will exist before C03's guarantees matter. Today `SKILL.md:342` says "dispatch is the legacy dispatch" and the resolver writes no file the dispatcher reads. Both define "correct" relative to a component absent from code. | UNSTATED (each cites C09 as a dependency; neither states that C03 delivers no enforced behaviour without it, A in cost, B in R1 only) | Yes |
| A-002 | Agreements 3, 4 | A class alias passed on an Agent call is resolved by the subagent through the same `ANTHROPIC_DEFAULT_*_MODEL` values the orchestrator read at Wave 0 (A's `launch_binding`) or at `verify` time (B's V3), and the alias-to-first-model chain holds. Both rest on one observed day; A's R2 flags a documentation caveat as untested; B's P7 flags first-model as UNVERIFIED. | UNSTATED as an assumption about subagent inheritance; partially STATED as an unverified chain | Yes |
| A-003 | Agreement 1, 5 | No consumer other than those named reads `select_env` or compares a raw `launch` string (so A's default flip and B's grammar change do not break an unnamed caller). Orchestrator check: `select_env` has one production caller (`panel_cmd.py`); the consumers of the raw `launch` string (`_REFLECT_LAUNCH`, telemetry `model.launch`, reflect skill text, the code-driven engine) were not enumerated by either variant. | UNSTATED | Yes |
| A-004 | Agreement 3 | `muse-ember-1.0` is not available through the gateway / is absent from the environment (A EV-14: not in the gateway list on 2026-11-13; B R4: tier4 has 3 models, `ccsession-models.json` has 3 slots). Orchestrator observation in this session's shell: `T4Model04=muse-ember-1.0` is set. A set variable is not proof that the model serves, but it contradicts a flat "absent" reading. | CONTRADICTED (partially) | Yes (flagged for debate) |
| A-005 | Agreement 1 | Reflect's Stage 3 gate semantics (class launch, at most 3 reviewers, no Fable, no tier0) remain as they are during C03. | STATED (A core 1; B core 6, P3) | No |
| A-006 | Agreement 6 | One gateway on 2026-11-11 to 2026-11-13 is sufficient evidence to design against. | STATED (A R10; B P7, row limits) | No |

## Summary
- Total structural differences: 7
- Total content differences: 15
- Total contradictions: 3
- Total unique contributions: 21
- Total shared assumptions surfaced: 6 (UNSTATED: 3, STATED: 2, CONTRADICTED: 1); promoted to debate points: 4
- Total diff points in the convergence denominator: 29 (7 + 15 + 3 + 4)
- Highest-severity items: C-001, C-002, C-003, C-005, X-001, X-003

## Taxonomy tagging (AD-5, auto-tag by signal terms, L3 over L2 over L1)

| Level | Points |
|-------|--------|
| L1 surface | S-001, S-003, S-004, S-005 |
| L2 structural | S-002, S-006, S-007, C-001, C-003, C-004, C-009, C-010, C-011, C-012, C-013, C-014, C-015, A-003, A-004 |
| L3 state-mechanics | C-002, C-005, C-006, C-007, C-008, X-001, X-002, X-003, A-001, A-002 |

Every level has points, so the taxonomy coverage gate starts satisfiable. The focus areas (correctness, risk, test-coverage) put weight on L3 points and on S-006, C-012.
