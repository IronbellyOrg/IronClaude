# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe)
- Mode: A (compare); Variant A = proposal-a (anthropic-only, class launch), Variant B = proposal-b (gateway, launch adapters, dated tier data)
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Task agents, subagent_type general-purpose, dispatched with the Agent tool; fallback_mode false)
- Convergence threshold: 80%
- Diff points in denominator: 29 (S 7, C 15, X 3, A 4)
- Rounds completed: 2 plus Round 2.5 (invariant probe); Round 3 not run (depth standard)
- Convergence achieved: 86% by agreement (25 of 29 points); status BLOCKED_BY_INVARIANTS (2 HIGH UNADDRESSED invariants: INV-009, INV-013)
- Taxonomy coverage gate: passed (L1, L2, L3 all debated in both rounds; no forced round needed)


## Round 1: Advocate Statements

Dispatch: two Agent calls in ONE message (parallel), subagent_type general-purpose, names advocate-A-r1 and advocate-B-r1. Each advocate read both variants, the diff analysis and C03 context, and verified claims against the repo with read-only tools. Statements are reproduced verbatim from the advocates final messages (headings demoted one level).

### Variant A Advocate (general-purpose, default persona)

#### Position summary
Variant A is the safer design for C03 today. Verified in the code, nothing in `src/` reads `launch` except the resolver and the reflect check (`panel.py:153`, `:595`), and `SKILL.md:342` says "Dispatch is the legacy dispatch". B therefore adds `cli-model:` data that nothing executes, which is B's own R1. B is better than A on the preflight check, the provenance coupling, the packaged-data completeness test and staged delivery. The strongest outcome is a MERGE: A's scope and default flip, plus B's grammar, version coupling and V2 slot check.

#### Steelman of Variant B
B's strongest case runs as follows.

- **A's "anthropic-only" label is false here.** On this machine `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]`, and tier2's first model is `gpt-6.1-sol` (`review-tiers.default.json:7`). A makes the false label the default for everyone and relies on after-the-fact recording to expose the lie.
- **The module is already built for data-only changes.** `panel.py:1-9` states that design, and `test_adding_a_model_family_is_a_data_edit_only` pins it. A bare-string launch parsing as `agent-class:<string>` is a strict superset, so nothing existing breaks.
- **C09 is decided.** It says the launch names an adapter and an argument, so a grammar is coming either way. A defers the schema work the decided C09 already implies.
- **The tier file already rots, and the repo has no guard.**
  - The `MODEL-TIERS.md` checklist lists three files and omits `review-tiers.default.json`.
  - I verified `T4Model04=muse-ember-1.0` is set in this shell, while `muse-ember` appears in no file under `src/` or `tests/`.
  - So the packaged data already lags the environment. B's `provenance` plus a version-coupling test is the only proposal that addresses this.
- **B ships a read-only preflight.** `panel verify` V2 closes the D12 gap, and V3 would have warned about the 2026-11-13 haiku to `gpt-6.1-sol` case before any run. A only notices after the fact.
- **B is staged.** Only B-1 and B-2 are needed for the defects. Gateway entries are gated on owner acceptance of R1.

#### Strengths claimed (numbered, with evidence)
1. **The unsupported cell stays honest.**
   - Gateway `launch: {}` carries the note "dispatch mechanism per model not defined yet" (`review-tiers.default.json:26`).
   - `test_gateway_resolution_prints_launch_null` (`test_review_panel.py:303-308`) pins it.
   - A keeps that honest signal. B replaces it with 12 `cli-model:` entries that nothing executes. B's own R1 concedes this, and its P-intro claim of "removing the false property" does not hold.
2. **No consumer can dispatch a gateway reviewer today.** I grepped `src/**/*.py` for `launch` readers. The only hits are `panel.py:72`, `:153-155`, `:364` (validator) and `:595` (resolve). `SKILL.md:342` says "Dispatch is the legacy dispatch". A needs no new dispatch capability, and B's gateway default needs C09 Option C (rated L).
3. **The `select_env` flip is a bounded, real fix.**
   - `select_env` (`panel.py:485-494`) reads only `T3Model01`.
   - Its sole production caller is `panel_cmd.py:96`.
   - In this shell (`T3Model01=glm-5.3`, `T2bModel01` set, `SUPERCLAUDE_REVIEW_ENV` unset) a bare `panel resolve` selects `gateway` and prints `launch: null` for every reviewer.
   - The loop prompt calls the resolver without `--env` (`document_review_loop_prompts.md:70`).
   - So E3 users today get a panel with no launch instruction.
   - Tests to flip: `test_review_panel.py:339` and `test_review_cli.py:83-88`, both verified.
4. **A's platform claim matches the docs.** I fetched code.claude.com/docs/en/sub-agents. It says: "On an Agent tool call, that parameter takes a model alias: `sonnet`, `opus`, `haiku`, or `fable`. Claude can't pass a full model ID or `inherit` on that call." That makes class names the only in-session launch form, which is the core of A's correctness argument. A also flagged the family-alias caveat as R2, and the docs confirm it exists.
5. **The tier file and goldens stay byte-identical.** The packaged-tier golden stays valid. B must regenerate it, plus the live7 coupling test, the gateway-null test and the skill needles.
6. **`launch_binding` needs no schema change.** `advance_stage` (`manifest.py:277-316`) validates only `outputs`, `reviewers_requested` and `reviewers_resolved`. Any other payload key is hashed, and a different payload on the same stage raises `Conflict` (`:295-298`).
7. **A names real unpinned gaps.** `grep` in `tests/` finds no `panel_fallback_reason` (it appears only in `SKILL.md:320,338,466,972`). Reflect-in-gateway failing closed is also unpinned. A's tests 2 and 3 cover both. B's test table omits D4 coverage.
8. **A's scope matches what the decided conflicts can enforce.** C08 and C09 are decided, and A builds on the class adapter without claiming more than exists.

#### Weaknesses identified in Variant B (numbered, with evidence)
1. **Data ahead of the executor (B's own R1).** Gateway `launch` entries become the default for new consumers while no reader exists (see Strength 2). That recreates the "record describes something that did not run" defect B cites from research 04 §10. B's mitigation is "do not ship the gateway entries before the owner accepts that gap", which concedes B-1 is not safely shippable alone.
2. **V3's route derivation is incomplete.**
   - V3 expects class, then `ANTHROPIC_DEFAULT_<CLASS>_MODEL`, then tier alias, then first model.
   - The docs I fetched say a family alias resolves to the main conversation's exact model when the parent belongs to that family, including any `[1m]` suffix.
   - B's V3 ignores that rule. It also depends on "alias serves its first model", which B's own P7 marks UNVERIFIED.
   - So V3 can emit false `warn` or false `ok`. B labels it "derived, not observed", which limits the damage but also limits its value.
3. **B's R3 overstates.** "A gateway panel with non-Claude members cannot run inside reflect's in-session dispatch. Certain." This contradicts B's own evidence row 4 (the haiku class served `gpt-6.1-sol` in-session). Raw ids cannot be passed on the call, but classes can be bound to gateway ids. A's EV-9 records this working in runs C, D and E. I did not re-read `results.md`, so A's EV-7 and EV-9 run evidence is unverified by me.
4. **`cli-model` reviewers lose reflect's read-only guard.**
   - `agents/reflect-reviewer.md` carries a read-only tool allowlist, `model: sonnet` and `permissionMode: plan`. I confirmed the file.
   - A `claude -p --model <raw id>` subprocess has none of that unless a dispatcher supplies it.
   - B never mentions the read-only allowlist. A names it as C18 (R9).
5. **B's "gateway is the default" is incoherent.** The consumer table says default is gateway. The CLI section keeps the precedence where `T3Model01` unset means anthropic-only. So the default depends on one variable, which is the D12 fragility B claims to fix, and B only adds a post-hoc slot check.
6. **`swarm:` is speculative.** It is reserved in the grammar but no packaged data uses it, and the engine it serves is replaced at UC-2 Stage 5.
7. **Scope: L effort and High risk.** The packaged-tier golden, two coupling tests, tier0 data, ember coordination with Coder and `ccsession-models.json` (fetched live from master at launch) all move together. B-3 depends on changes outside this repo.
8. **Unverified:** whether `validate_tiers` ignores an unknown top-level `provenance` key. B asserts it, and I did not read `panel.py:258-374`. B's "closed key sets at `:371-373`" also sits awkwardly with it.

#### Concessions (weaknesses in Variant A)
1. **The label stays false.** Flipping the default makes `anthropic-only` the default on a machine where the haiku class serves `gpt-6.1-sol`. The resolution then shows `sonnet, haiku, haiku, haiku`, three reviewers on one bound model. That is a false-diversity record, flagged only by `stand_in: true` (A's R6).
2. **`launch_binding` records raw env values, not served models.** It stores `claude-gw-tier2[1m]`. Interpreting that needs the tier-file chain, which is B's V3. Without it the binding is a recorded variable, not a finding. A's mitigation is "warn when two classes bind the same model", which is much weaker than V3.
3. **R2 is untested.** Per the docs, a family alias can run on the parent's exact model, which can falsify `launch_binding`. Only observation fixes that, and no in-session observation exists (A's EV-13).
4. **Brittle replay.** A different `ANTHROPIC_DEFAULT_*` set on resume makes `advance_stage('resolved')` raise `Conflict`. A did not list this.
5. **Three-model ceiling and no fallbacks.** At most 3 distinct models per panel, and every `fallbacks` list is empty. A accepts both.
6. **Changes behaviour for `T3Model01` machines.** The default flip does that, and A's R5 is only a release note.
7. **Does not fix tier-file rot.** No version coupling, no `tier0`, no D12 check. `muse-ember-1.0` is set in this shell (`T4Model04`), and A's "absent" framing misses that.
8. **Quality claim is unmeasured.** A's anti-gateway argument leans on E2 ("model choice is the weakest lever"), which is DOC-SOURCED from one gateway on one day. A says so itself.

#### Shared assumptions
- **A-001: ACCEPT.** I verified it: no reader of `launch` outside `panel.py`, and `SKILL.md:342` says "Dispatch is the legacy dispatch". Neither variant delivers enforced behaviour without C09. The risk is asymmetric. If C09 slips, A's state equals today's, while B's adds unexecuted data.
- **A-002: QUALIFY.** The docs say a family alias resolves to the parent's exact model when the parent is in that family. Both `launch_binding` and V3 are derived expectations, not observations. Only C08's observed identity settles it.
- **A-003: QUALIFY.** For Python code it holds: `select_env` has one caller (`panel_cmd.py:96`), and `launch` has one resolver reader plus the reflect check. It is not enumerated for skill and prompt text, plugin mirrors or `tests/` (UNVERIFIED beyond the greps I ran).
- **A-004: REJECT.** The flat "absent" reading is false for this environment. `T4Model04=muse-ember-1.0` is set in this shell. What holds is "absent from packaged data" (no file under `src/` or `tests/` mentions it). I did not verify whether the model serves. This supports B's staleness point and A's "keep dated facts out of packaged data" point equally.

#### Per-point positions
| Point | Superior approach | Confidence | One-line evidence |
|---|---|---|---|
| S-001 | NEITHER | 55 | Preamble style only. |
| S-002 | NEITHER | 55 | B's rival-option paragraph is useful context, but it is not substance. |
| S-003 | MERGE (A's RUN/verified tags, B's claim-research-code-tag table) | 60 | A's tags say what was re-verified. B's table is easier to audit. |
| S-004 | NEITHER | 55 | Both state their limits (A's "does not show", B's P7). |
| S-005 | A | 55 | A's standalone weakest-point paragraph, but B's R1 is equally candid. |
| S-006 | MERGE (A's run set and uncovered-gap tests, B's completeness and backward-compat tests) | 62 | A lists the run command. B has the test that would have caught `launch: {}`. |
| S-007 | B | 65 | B's gated stages fit an L change. A's single XS-S table fits A's smaller change. |
| C-001 | A | 68 | Nothing can dispatch a gateway reviewer today. This shell resolves `gateway` with `launch: null`. |
| C-002 | A | 70 | `launch: {}` plus its note is honest. Filling it ahead of an executor is B's R1. |
| C-003 | MERGE (B's grammar and `parse_launch` with bare-string compatibility, A's rule to fill only anthropic-only now) | 62 | C09 already decided adapter plus argument. Gateway entries wait for a dispatcher. |
| C-004 | MERGE (B's `tiers_as_of` and version-coupling test, A's `launch_binding` in the manifest) | 65 | The checklist omits the tier file (`MODEL-TIERS.md`), and the only guard is a length test. |
| C-005 | MERGE (A's binding and launch-vs-observed check, B's V3 as warn-only preflight) | 62 | A has no pre-run warning. V3 ignores the parent-family rule. Neither observes. |
| C-006 | B | 62 | A flips the default and leaves D12 uncovered for explicit `--env gateway`. B's V2 slot check is unreached by A. |
| C-007 | B | 58 | The tier0 rule is inert with packaged data (`panel.py:95-117`). Ember is in the environment but not in data. B's ember handling is coordinated. |
| C-008 | NEITHER | 55 | B's adapter-naming message is nicer but has low value. A's unchanged check has zero risk. |
| C-009 | MERGE (A's no new flag, B's V2 only if gateway is chosen) | 55 | A new `verify` command is only worth it once gateway entries execute. |
| C-010 | A | 60 | `swarm:` unused in B's data. A's R7 defers it, though A flags it High if ignored. |
| C-011 | A | 65 | Class binding works now (A's run evidence, not re-read by me). B's route needs a C09 dispatcher B does not deliver. |
| C-012 | MERGE (A's tests 1, 2, 3, 7 and flips, B's completeness and backward-compat tests) | 60 | Verified no `panel_fallback_reason` test exists. B's old-vs-new resolution test is strong. |
| C-013 | A | 68 | XS-S and Medium risk against L and High. B-1 alone is not safely shippable (B's R1). |
| C-014 | NEITHER | 55 | Both are reversible. A flips one line back and B removes data. |
| C-015 | A | 62 | Platform doc verified by me. B's self-preference literature is 2023-era and B qualifies it. |
| X-001 | A | 72 | Docs confirm raw ids can't be passed on the call. Classes bound to gateway ids can run, and B's R3 contradicts B's row 4. |
| X-002 | A | 68 | A's diagnosis is verified. B keeps `T3Model01` detection while calling gateway the default. |
| X-003 | A | 62 | B's R1 contradicts its own "removes the false property" claim. A's anthropic-only label has the same problem, though. |
| A-001 | NEITHER (ACCEPT) | 85 | No reader of `launch` outside the resolver. |
| A-002 | NEITHER (QUALIFY) | 75 | The docs' family-alias rule applies to both designs. |
| A-003 | NEITHER (QUALIFY) | 70 | Python callers verified. Markdown, plugin and test consumers not enumerated. |
| A-004 | NEITHER (REJECT) | 80 | `T4Model04=muse-ember-1.0` is set here, while `src/` and `tests/` have no mention. |

#### Facts I verified or could not verify
- **`select_env` reads only `T3Model01`:** verified, `panel.py:485-494`.
- **`select_env` has one production caller:** verified, `panel_cmd.py:96`.
- **`_check_reflect_resolution` rejects any launch outside sonnet, opus, haiku:** verified, `panel.py:153-156`.
- **`_REFLECT_LAUNCH`:** verified, `panel.py:72`.
- **Gateway `launch: {}` and the anthropic-only launch map:** verified, `review-tiers.default.json:25-30` and `:31-36`.
- **Tier2's first model is `gpt-6.1-sol`:** verified, `review-tiers.default.json:7`.
- **`advance_stage` validates only 3 payload keys and `Conflict` on a different payload:** verified, `manifest.py:277-316`.
- **`telemetry.py:49` has `"model": ("resolved", "launch", "observed")`:** verified.
- **`test_gateway_resolution_prints_launch_null`:** verified, `test_review_panel.py:303-308`.
- **`select_env` tests:** verified, `test_review_panel.py:331-341` and `test_review_cli.py:83-88`.
- **Loop prompt calls `panel resolve` without `--env`:** verified, `document_review_loop_prompts.md:70`.
- **`SKILL.md:342`:** "Dispatch is the legacy dispatch". `:320` D4 verified. `:340` step 1 and the `resolved` payload text verified.
- **`reflect-reviewer.md` frontmatter:** verified. It has a read-only tools list, `model: sonnet` and `permissionMode: plan`.
- **No `panel_fallback_reason` or `launch_binding` in `tests/`:** verified by grep. No `parse_launch` in `src/` or `tests/`.
- **Shell values:** `T3Model01=glm-5.3`, `T2bModel01=gpt-6.1-terra`, `T4Model04=muse-ember-1.0`, HAIKU, SONNET and OPUS bound to `claude-gw-tier2[1m]`, `claude-gw-tier1b[1m]` and `claude-gw-tier1a[1m]`, and `SUPERCLAUDE_REVIEW_ENV` unset. All verified.
- **`muse-ember` in `src/` or `tests/`:** verified absent.
- **`ccsession-models.json` `"version": "2026-11-11.1"`:** verified. I did not count the tier4 slots.
- **Sub-agents doc (Agent `model` takes aliases only; family-alias parent rule):** verified by fetch.
- **A's run evidence (EV-7, EV-9, EV-11, EV-12) and B's E2 rows 14, 22, 23:** UNVERIFIED by me. I read neither `results.md` nor E2 via `git show`.
- **`validate_tiers` ignoring an unknown `provenance` key:** UNVERIFIED. I did not read `panel.py:258-374`.
- **Whether `SKILL.md` step 1 or `test_shadow_skill_contract.py` needles would break on A's added `launch_binding` key:** UNVERIFIED.
- **Whether a family alias on a gateway-bound class actually inherits the parent's model here:** UNVERIFIED.

| Status | Result |
|---|---|
| DONE | Verified the 15 code and doc claims above and gave positions on all 29 points plus the four shared assumptions. |
| NEXT | None. |

I did not read the research files `04`, `12` and `13` or `results.md`, so A's run-based evidence stands as documented, not re-checked.

### Variant B Advocate (general-purpose, default persona)

#### Position summary

Neither variant should ship whole. Variant A's smaller design is the only one that can run today. Variant B's strongest parts are the tier-data drift guards and the pre-run alias check, and those don't depend on the gateway `cli-model` entries. B's weakest part is filling `gateway.launch` for an adapter nothing executes. The evidence points to a MERGE: A's class launch and `launch_binding` as the shipping core, and B's grammar, provenance, completeness test, D12 check and `verify` on top.

#### Steelman of Variant A

The platform docs I fetched state: "On an Agent tool call, that parameter takes a model alias: `sonnet`, `opus`, `haiku`, or `fable`. Claude can't pass a full model ID or `inherit` on that call." So the only launch form an in-session orchestrator can use is a class name. A builds on that.

- **The default flip is a real fix.** `select_env` (`panel.py:485-494`) returns `gateway` whenever `T3Model01` is set. On ccsession machines that is the default, so any consumer that omits `--env` gets `launch: null` for every reviewer. A removes that failure by changing the default. `select_env` has one production caller, `panel_cmd.py:96` (grep). The change touches two tests.
- **Gateway models stay reachable.** The class-binding route ran 15 of 15 combination runs to `published`. The docs also say `ANTHROPIC_DEFAULT_OPUS_MODEL` makes the `opus` alias resolve to the model you set.
- **A already supplies the schema half of identity recording.** `launch_binding` fits in the `resolved` payload. I confirmed `advance_stage` validates only `reviewers_requested`, `reviewers_resolved` and `outputs` (`manifest.py:307-316`).
- **A is the smallest diff.** No tier-file byte changes, so both goldens stay valid. It is also candid about its limits ("What this argument does not show", "Items I did not check").
- **A rests on the defensible E2 finding.** E2 says model choice does not lift the ceiling; the levers are harness fixes and a repeat.

#### Strengths claimed

1. **The drift problem is real and checked live.** The repo's `ccsession-models.json` (version `2026-11-11.1`) has tier3 as `T3Model01`-`T3Model02` and tier4 as `T4Model01`-`T4Model03`. This shell has `T3Model01` through `T3Model06` and `T4Model04=muse-ember-1.0`. The tier file's only date is a prose note, "owner decision 2026-11-10" (`review-tiers.default.json:32`). The only coupling test (`test_review_panel_live7.py:92-106`) compares list lengths for tier2b, tier3 and tier4, so it cannot see this. B's `provenance` plus version-coupling test addresses this (B §Design item 3, evidence rows 15-16). A has no answer to it.
2. **The label problem is detectable before a run.** `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]` in this shell, and tier2's first model is `gpt-6.1-sol` (`review-tiers.default.json:7`). B's V3 route check would warn on exactly this.
3. **The grammar is a safe superset.** `validate_tiers` only checks that `launch` maps strings to strings (`panel.py:364-368`). It does not reject unknown top-level keys: the unknown-key loop at `:371-373` covers environment entries only. So `provenance` is additive, and a bare string means `agent-class:<string>`, so today's anthropic-only table stays valid.
4. **`resolve` stays pure.** It reads no environment (`panel.py:565-707`). B puts the D12 slot check in the command layer and in `verify`, and `select_env` already reads `os.environ` there.
5. **Existing `launch: {}` is an unpinned defect.** `test_gateway_resolution_prints_launch_null` (`test_review_panel.py:303-308`) pins the null. B's packaged-data completeness test is the check that would catch an incomplete launch table. A has no equivalent.
6. **Staged delivery.** B-1 and B-2 (grammar, provenance, `verify`, D12) have standalone value and do not need the dispatcher. Only the gateway entries need the owner to accept R1.
7. **D12 is uncovered today.** `T2bModel01` is set here but never read, and `live7` needs `claude-gw-tier2b`. A's flip does not cover an explicit `--env gateway` run with a missing slot.

#### Weaknesses identified in Variant A

1. **The flip makes the default label false on the machines it targets.** Under A, anthropic-only becomes the default on a ccsession machine. There the haiku class is bound to `claude-gw-tier2[1m]` (env, verified). The `default` template is t1b fixed, t2 x1 random, t3 x2 random (`review-panel.default.json`). The anthropic-only stand-ins for tier2, tier3 and tier4 are all `claude-haiku-5-5` (`review-tiers.default.json:34`). So the loop's default panel becomes sonnet plus three haiku-class reviewers. Here those three are served by `gpt-6.1-sol` while the record says Claude Haiku 5.5. A concedes this in R6 and EV-11. Today's gateway default gave four distinct models, although with null launch.
2. **`launch_binding` records an alias, not a model.** The recorded value would be `claude-gw-tier2[1m]`. Turning that into "served by `gpt-6.1-sol`" needs the alias-to-first-model data that A refuses to put in the tier file (core item 3, correctness step 6). So the binding is opaque without B-style data.
3. **A depends on observation that does not exist yet.** A's EV-13 says no in-session tool returns the served model of an Agent call. Until C08 observation exists, interactive runs get `requested-pinned`, which is the same blind spot as today. B's V3 offers a pre-run expectation, though derived and not observed.
4. **"Facts that rot stay out of packaged data" is not accurate.** The packaged file already holds dated facts (alias lists, the 2026-11-10 note), and they have rotted (see Strengths 1). A leaves them undated and unchecked.
5. **A makes the mislabel the supported mechanism.** To express "haiku + 2x luna", A binds two classes to `gpt-6-luna`. The record then names Claude models for gpt runs, and A's EV-12 shows parity reported `True` while two distinct models served. A treats this as a recording defect, but the design depends on recording that is not built.
6. **`launch_binding` changes the stage-hash behaviour.** `advance_stage` raises `Conflict` for a different payload on the same stage (`manifest.py:292-299`). A resume in a shell with different `ANTHROPIC_DEFAULT_*` values would fail. A tests this as a feature and lists no risk for it, though failing closed is arguably right.
7. **`panel_fallback_reason` has no code or test.** A's test 3 is the right fix. I grepped `src` and `tests` for the name and it appears only in `sc-reflect-protocol/SKILL.md`. A's "D4 fallback" evidence is skill text only.

#### Concessions

1. **R1 is real and I cannot defend it away.** The `cli-model:` gateway entries describe a route nothing executes. The #346 loop dispatches in-session, and B's own R3 says in-session Agent calls cannot pass a raw id. So for the loop, B's gateway entries cannot be acted on without a new subprocess dispatcher (C09 Option C, effort L, not delivered). A's class launch works with today's dispatch path.
2. **B's item 6 is optional polish.** `_check_reflect_resolution` (`panel.py:153`) already rejects any launch not in `("sonnet","opus","haiku")` and prints the offending value. A `cli-model:x` launch would already give `launch 'cli-model:x' is not one of ...`. Parsing the adapter only improves the message.
3. **"Default environment is the gateway" is loose.** B keeps `select_env` unchanged, so the gateway is the default only where `T3Model01` is set.
4. **V3 rests on an unverified rule.** "An alias serves its tier's first model" is observed once and E2's statement of it is UNVERIFIED (research 04 §4.2). V3 can emit false warnings, and B labels it derived.
5. **`provenance` labels decay, it does not stop it.** Age is printed but no threshold is set, and the data can still be wrong the day after.
6. **Scope and sequencing.** B is L effort with High risk (synth rating). The grammar has one executing adapter today, so the `swarm` slot is speculative under the repo's own scope discipline. B's evidence for the gateway's value is one gateway over 2026-11-11 to 2026-11-13, and E2 shows a ceiling near 2-2.5 of 14.
7. **B's D4 and `panel verify` wiring is untested prose.** Its test is a skill-text needle, the same weakness as A's D4 path.

#### Shared assumptions

- **A-001: QUALIFY.** Both depend on C09, but asymmetrically. A's dispatcher rule (`model == launch`) needs only a skill-text edit and the existing Agent call. B's `cli-model` needs a subprocess dispatcher that does not exist. Evidence: the docs say the Agent call takes only an alias, and B's R1 and R3 concede the gap.
- **A-002: QUALIFY.** The docs say a family alias resolves to the main conversation's model when the parent belongs to that family. They explicitly address `ANTHROPIC_DEFAULT_OPUS_MODEL` only for the Bedrock-unknown-family case ("`opus` then resolves to the model you set"). They give no equivalent statement for the sonnet or haiku overrides. The combination runs support the chain empirically, for two ids on one day, so neither design should treat it as general.
- **A-003: ACCEPT, with a limit.** For Python callers I verified one production caller of `select_env` (`panel_cmd.py:96`) and `_REFLECT_LAUNCH` only in `panel.py:72,153`. Telemetry names `launch` in the `model` group (`telemetry.py:49`). Skill and prompt text that compares raw `launch` strings I did not enumerate, which is UNVERIFIED.
- **A-004: REJECT as stated.** `T4Model04=muse-ember-1.0` is set in this shell (verified). The accurate fact is that ember is present in the live Coder env and absent from the repo's `ccsession-models.json` (T4 has 3 slots) and the tier file. That is drift, which supports B's C-004 and R4 more than it supports A's "absent".

#### Per-point positions

| Point | Superior approach | Confidence | One-line evidence |
|---|---|---|---|
| S-001 | NEITHER | 60% | Cosmetic preamble differences. |
| S-002 | B | 55% | B states what it decides beyond Option C. |
| S-003 | MERGE: A's [RUN] provenance, B's per-row claim/research/code/tag table | 55% | A ran commands; B's `[RES]` tag marks what it did not re-read. |
| S-004 | NEITHER | 60% | Both include a "does not claim" section. |
| S-005 | A | 60% | A's separate weakest-point paragraph is more visible than B's R1 row. |
| S-006 | MERGE: B's table layout, A's exact `uv run pytest` run set | 55% | B has no run command; A's list is runnable. |
| S-007 | B | 65% | Four gated stages with standalone value; A's flat table hides sequencing. |
| C-001 | MERGE: A's class launch to ship now, B's gateway target as a staged follow-on | 55% | Only the in-session class path is executable today (docs, EV-5). |
| C-002 | A | 58% | B's R1 says entries describe a route nothing executes; ship them with the dispatcher. |
| C-003 | B | 60% | Superset grammar, validator unchanged (`panel.py:364-368`), matches decided C09 adapter names. |
| C-004 | B | 72% | Live env has T3Model01-06 and T4Model04 vs repo's 2 and 3 slots; the file has no date beyond a note. |
| C-005 | MERGE: B's V3 pre-run expectation, A's `launch_binding` and observed triple | 70% | A's observation does not exist for in-session runs (A EV-13); `launch_binding` holds an alias, not a model. |
| C-006 | B | 60% | A's flip leaves explicit `--env gateway` and `T2bModel01` unchecked; B's check sits outside `resolve`. |
| C-007 | B | 62% | Env has T0Model01/02 and ember set; repo has neither in the tier file. |
| C-008 | A | 60% | Existing check at `panel.py:153-156` already rejects any non-class launch; B's change is cosmetic. |
| C-009 | B | 52% | A read-only preflight catches D12 and drift, but adds surface and rests on an unverified rule. |
| C-010 | NEITHER | 55% | Both defer to C17; `swarm` slot is unused data. |
| C-011 | A | 60% | Class binding ran 15 of 15 and docs support it; B's route needs an undelivered dispatcher. |
| C-012 | MERGE: A's dispatcher and swap-fixture tests, B's completeness and backward-compat tests | 60% | Each variant's unique tests cover the other's gap. |
| C-013 | A | 70% | XS to S against L with High risk. |
| C-014 | A | 55% | One-line flip back and no golden regeneration; B also reversible by data removal. |
| C-015 | A | 65% | A's EV-5 is decisive and I confirmed it; B's self-preference evidence is tangential. |
| X-001 | A | 60% | Raw ids work as class values by env binding; B's R3 is right only for raw ids in launch data. |
| X-002 | A | 55% | Under B, omitting `--env` can still reach a launch the in-session dispatcher cannot act on. |
| X-003 | NEITHER | 60% | Both labels can differ from what served; B adds a detector, A adds a record, until C08 observation exists. |
| A-001 | QUALIFY | 65% | Asymmetric dependence on C09 (see Shared assumptions). |
| A-002 | QUALIFY | 70% | Docs cover only the Bedrock `opus` case for the override. |
| A-003 | ACCEPT | 65% | One production caller of `select_env`; skill text unverified. |
| A-004 | REJECT | 80% | `T4Model04=muse-ember-1.0` is set in this shell. |

#### Facts I verified or could not verify

- `select_env` reads only `T3Model01` and has one production caller, `panel_cmd.py:96`: verified (`panel.py:485-494`, grep).
- `_check_reflect_resolution` rejects any launch outside sonnet/opus/haiku: verified (`panel.py:137-157`, `:72`).
- `validate_tiers` checks `launch` as a string map only, rejects unknown keys inside environments only, and ignores unknown top-level keys: verified (`panel.py:364-373`).
- `advance_stage` validates only three payload keys and raises `Conflict` on a different payload for the same stage: verified (`manifest.py:292-316`).
- Gateway `launch: {}`; anthropic-only stand-ins map tier2, tier2b, tier3 and tier4 to haiku: verified (`review-tiers.default.json:25-35`).
- `default` template is 1 fixed tier1b, 1 random tier2, 2 random tier3: verified (`review-panel.default.json`).
- Telemetry `model` group is `("resolved","launch","observed")`: verified (`telemetry.py:49`).
- Env here: haiku class bound to `claude-gw-tier2[1m]`, `T3Model01`-`T3Model06`, `T4Model04=muse-ember-1.0`, `T0Model01/02`: verified. Repo `ccsession-models.json` has 2 tier3 and 3 tier4 slots, version `2026-11-11.1`: verified.
- The Agent call `model` parameter takes only an alias, and frontmatter accepts a full ID: verified via WebFetch of the sub-agents docs.
- `panel_fallback_reason` appears only in `sc-reflect-protocol/SKILL.md`: verified by grep over `src` and `tests`, which listed only that file.
- Not verified: the `panel.py:95-117` tier0 rule and `SKILL.md:320/342` text; whether sonnet and haiku class overrides resolve like the documented `opus` case; that alias serves only the first model; E2 figures (not re-aggregated); default-template resolution output (I read the template, not a run).

| Status | Result |
|---|---|
| DONE | Read both variants and the diff analysis, and checked the code, env and docs. |
| NEXT | None. |

### Orchestrator notes on Round 1

- No [OMISSION]: both advocates answered A-001, A-002, A-003, A-004 (A: ACCEPT, QUALIFY, QUALIFY, REJECT; B: QUALIFY, QUALIFY, ACCEPT, REJECT).
- Both advocates conceded their own variant main weakness (A: false label, binding is an alias not a served model, three-model ceiling; B: R1 data ahead of executor, V3 rests on an unverified rule, scope). Both leaned to a MERGE, so Round 1 agreement may be partly courtesy. Round 2 is instructed to hold positions that the evidence supports and to test the opposing concessions, not to ratify them.
- New facts raised in Round 1 and not in the diff analysis: (a) docs say a family alias on an Agent call can run on the parent exact model, which neither launch_binding nor V3 models (A R2; advocate A weakness 2); (b) a claude -p --model subprocess loses the read-only allowlist and permissionMode of agents/reflect-reviewer.md (advocate A weakness 4); (c) a different ANTHROPIC_DEFAULT_* set on resume makes advance_stage(resolved) raise Conflict because launch_binding is part of the payload hash (advocate A concession 4, advocate B weakness 6); (d) live env has T3Model01-06 and T4Model04=muse-ember-1.0 while ccsession-models.json 2026-11-11.1 lists 2 tier3 and 3 tier4 slots (advocate B strength 1); (e) under A the default template becomes sonnet + three haiku-class reviewers, all on one bound model on this machine (A R6).


## Round 2: Rebuttals

Execution: sequential, input order. Variant A rebuttal first (agent advocate-A-r2, general-purpose, fresh spawn that reads the Round 1 transcript); the Variant B rebuttal follows and sees the Variant A rebuttal below. Both were told not to ratify the Round 1 MERGE lean by default and to test the merge shape.

### Variant A Rebuttal

#### Response to criticisms

I ran `panel resolve` here before answering. Today, with no `--env`, it prints `gateway` and four reviewers: sonnet-5-5, Qwen3.8-max, glm-5.3, glm-5.3, all with `launch: null`. With `--env anthropic-only` it prints sonnet (`launch: sonnet`) plus three `claude-haiku-5-5` (`launch: haiku`, all `stand_in: true`). The env here is `HAIKU=claude-gw-tier2[1m]`, `SONNET=claude-gw-tier1b[1m]`, `OPUS=claude-gw-tier1a[1m]`.

1. **The flip makes the default label false (B weakness 1, question a).**
   - **Answer:** PARTLY.
     - Per the tier file, only the haiku class is mislabeled here. `claude-gw-tier1a` serves opus first, `tier1b` serves sonnet first, `tier2` serves `gpt-6.1-sol` first (`review-tiers.default.json:4-7`).
     - So under A the default panel serves sonnet plus three `gpt-6.1-sol`, while the record says Claude Haiku 5.5 three times. That label is false.
     - Today's gateway default is not more honest. It names Qwen and glm, but `launch: null` means nothing instructs the dispatcher to launch either.
     - The one collapse that was observed (A3, from Round 1) put the reviewers on the frontmatter default model. The gateway record therefore claims three vendors that nothing launched.
     - Under A a class really is passed, and the same bound model repeated three times is visible as `stand_in: true`. A false vendor label is better than a false independence claim. A also stays easy to undo, because `--env gateway` still works.
   - **Concession:** `stand_in` alone is a weak flag. The tier file already contains `aliases.tier2.models`, so A's "keep dated facts out of packaged data" rule was too broad. The binding should carry a derived `expected_first_model` lookup, marked as derived.
   - **Evidence:** the resolve outputs above; `review-tiers.default.json:4-7,33-35`; `SKILL.md:342`.
   - **Status:** PARTLY.

2. **`launch_binding` stores an alias, not a model (B weakness 2, question b).**
   - **Answer:** PARTLY.
     - It is opaque only when a class is bound to a tier alias, which is the ccsession default on this machine.
     - When an operator binds a raw id, which is A's recommended gateway route, the binding is the model. Examples are `gpt-6-luna` in runs D and E, and `muse-ember-1.0` for T4Model04 if bound the same way (untested).
     - The alias-to-first-model data needed to read the opaque case is already in the packaged file. Reading it takes a lookup in the same record, not B's `verify` command.
   - **Evidence:** tier file `aliases` block; Round 1 EV-9 (A's run evidence, not re-read by me).
   - **Status:** PARTLY.

3. **A depends on observation that does not exist (B weakness 3).**
   - **Answer:** PARTLY.
     - True for in-session runs: no tool returns the served model of an Agent call.
     - B has the identical dependency. V3 is derived, and B's identity story also waits on C08.
     - A's binding plus the lookup in item 1 gives the same pre-run expectation without a new command.
   - **Evidence:** `telemetry.py:49` group exists; no code writes `observed`.
   - **Status:** PARTLY.

4. **"Facts that rot stay out of packaged data" is inaccurate (B weakness 4).**
   - **Answer:** PARTLY. The file already holds dated facts (the alias lists and the 2026-11-10 note).
   - **Concession:** the rule should read "no new dated facts".
   - **Held part:** B's remedy catches only repo-internal drift. The coupling test at `test_review_panel_live7.py:92-106` compares the tier file with the repo's `ccsession-models.json`. The drift B cites is live env versus repo: here `T3Model01..06` and `T4Model04` are set.
     - The tier file has tier3 with 2 models and tier4 with 3.
     - B's V2 reads only `T<N>Model01`, so V2 sees neither the tier3 extras nor `T4Model04`.
     - A provenance field and a version-coupling test close the checklist omission. They do not close the ember gap.
   - **Status:** PARTLY.

5. **A makes the mislabel the supported mechanism (B weakness 5).**
   - **Answer:** PARTLY. Once `launch_binding` stores raw ids and parity is computed from binding or observed values instead of tier-file names, the record stops naming Claude models for gpt runs. The parity fix belongs to C08 and C04. As proposed in Round 1, A does not yet do it.
   - **Status:** PARTLY.

6. **A different `ANTHROPIC_DEFAULT_*` set on resume raises `Conflict` (B weakness 6, question c).**
   - **Answer:** feature, not defect.
     - `advance_stage` returns False on an identical replay and raises `Conflict` on a different payload (`manifest.py:292-299`).
     - `SKILL.md:1507` already says that when the env alias set re-resolves differently, the run must STOP and emit `alias_set_changed_mid_run`, and that the Wave 0 alias set is canonical.
     - So `Conflict` is the same rule enforced by a second mechanism.
   - **Gap:** the `Conflict` message does not name the alias set. A should map it to `alias_set_changed_mid_run` and add a test.
   - **Status:** HELD.

7. **`panel_fallback_reason` has no code or test (B weakness 7).**
   - **Answer:** true. A grep of `src` finds it only in `SKILL.md:320,466,972`, which matches the Round 1 finding.
   - **Not a differentiator:** B's D4 reason is untested skill text too, and B conceded that. A's tests 2 and 3 fill it.
   - **Status:** CONCEDED as a fact, no differentiator.

8. **B's conceded points I exploit (B concessions 1, 2, 3, 4, 6).**
   - **R1:** the gateway entries describe a route nothing executes. It also contradicts B's claim of "removing the false property". HELD.
   - **Cosmetic check change:** `_check_reflect_resolution` already rejects any launch outside sonnet, opus and haiku at `panel.py:153`. So C-008 is cosmetic. HELD.
   - **Loose "gateway is the default":** the default is the gateway only where `T3Model01` is set. HELD.
   - **V3's rule unverified, scope L and High risk:** HELD.

#### Updated assessment of Variant B

**Survives, with evidence:**
- D12 has no test today.
- The packaged-data completeness test and the old-versus-new backward-compat test are real. Both apply only once gateway entries or a grammar actually ship.
- The version-coupling test closes the documented checklist omission. `MODEL-TIERS.md` lists three files and leaves the tier file out.
- Staged delivery is right for an L change.

**Fails, or is weaker than claimed:**
- **V3 cannot model the family-alias rule.** `verify` runs as a CLI subprocess and cannot see the parent conversation's model. An "ok" from V3 is therefore unsound whenever the parent is in the class's family. At best it can emit `warn` or "unverified".
- **B's drift guards do not catch the drift it cites.** V2 checks Model01 only, and the coupling test compares repo with repo. Live `T4Model04=muse-ember-1.0` and `T3Model01..06` are invisible to both.
- **A single-string adapter argument cannot carry a read-only guard.**
  - `agents/reflect-reviewer.md` has a tools allowlist, `permissionMode: plan` and `model: sonnet`.
  - On an Agent call the model parameter overrides only the model. The docs' resolution order is parameter, then frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main model. So A's route keeps the allowlist and plan mode.
  - A `claude -p --model <id>` subprocess keeps neither unless the dispatcher adds them. Grammar `cli-model:<id>` has nowhere to say so.
  - This is a C09 design question. It is also a reason not to freeze the grammar in C03 before C09 exists.
- **Provenance `evidence[]` and `gateway_observed_on` are free text that nothing checks.** Only `tiers_as_of` and the ccsession version are enforceable.

#### New evidence

1. **Family-alias rule (docs, fetched today).** A family alias on the per-invocation parameter or in frontmatter resolves to the main conversation's exact model, including `[1m]`, when that model belongs to the family. The documented `ANTHROPIC_DEFAULT_OPUS_MODEL` exception covers only the Bedrock case where the family is unknown. Nothing is documented for the sonnet and haiku overrides.
   - It undermines `launch_binding` and V3, but not equally.
   - The orchestrating skill knows its own model, so the binding can add `parent_model` and flag any class whose family equals the parent family as `overridden-by-parent`. V3 cannot, because a CLI cannot read the parent model.
   - Whether `claude-gw-tier1b[1m]`, this session's own model, counts as the sonnet family is UNVERIFIED.
2. **Read-only guard.** Verified in the `reflect-reviewer.md` frontmatter. The loss comes from the `claude -p` path. The guard is a C09 concern, and it is also a defect in B's claim that the grammar covers `cli-model` now.
3. **Env versus repo data.** `T4Model04=muse-ember-1.0` is set here, and tier4 in the tier file has 3 models. I did not re-read `ccsession-models.json`, so the "3 slots" count there is B's claim.
4. **Duplicate draw today.** Today's gateway default drew glm-5.3 twice. The gateway default is not distinct either.
5. **Readers of `launch`.**
   - Python readers are `panel.py:153`, `:595` and `:679`.
   - `telemetry.py:49` is only the group name, not a reader of the value.
   - `select_env` has one caller at `panel_cmd.py:96`.
   - `launch` appears nowhere under `rules/` or `commands/`, except in unrelated senses.
   - In `sc-reflect-protocol/SKILL.md`, lines 340 and 371 were truncated in my grep, so I did not read them.
   - Tests and the plugin mirror are not enumerated.

#### Merge-shape test

**Strongest case against "A core + B grammar, provenance, verify":**
- It ships a grammar with one executing adapter. `agent-class` is the only adapter anything executes. `cli-model` and `swarm` would parse and then be validated and reported as supported with no executor behind them. The existing validator already accepts any string at `panel.py:364-368`.
- It ships a `verify` whose headline check (V3) is unsound in exactly the family-alias case the docs describe.
- It ships in the wrong order. Provenance changes tier-file bytes, which regenerates the packaged golden and erases A's "both goldens stay valid" advantage if done in the same PR.

**What I still support:**

| B piece | Position | Reason |
|---|---|---|
| Grammar (C-003) | Decide it now; code later | Write the decision down: `<adapter>:<arg>`, a bare string means `agent-class`. Add `parse_launch` in the C09 dispatcher PR, where it has a reader and where the argument shape (permissions, allowlist) is known. |
| Provenance (C-004) | Yes, minimal | Only `tiers_as_of`, `ccsession_models_version`, the coupling test and a fourth line in the `MODEL-TIERS.md` checklist. It goes in its own PR to take one golden regeneration. |
| D12 check (C-006) | Yes, command layer | Support B's `check_required_env`, with `resolve` kept pure. It protects little while gateway `launch` is null. Ship it with, or just before, the dispatcher. |
| tier0 (C-007) | No for C03 | A positive test of the reflect "no tier0" rule works with a synthetic tier file, as `test_adding_a_model_family_is_a_data_edit_only` does. Add tier0 when a template needs Fable. Ember is Coder-first and outside this repo. |
| `verify` (C-009) | Defer; keep V1, V2, V4 | V3 only as warn-only and never "ok". Do not ship a new command ahead of any gateway dispatch. |
| Adapter-naming check (C-008) | No | B conceded it as polish. |

**Proposed order:**
1. **PR 1 (A core, no tier-file bytes):**
   - the `select_env` flip and its two test flips;
   - `launch_binding` with `parent_model`, the derived `expected_first_model` and the family-collision flag;
   - `Conflict` mapped to `alias_set_changed_mid_run`;
   - tests 1, 2, 3 and 7, a family-collision test and a resume-`Conflict` test.
2. **PR 2:** minimal provenance, the coupling test and the checklist line.
3. **PR 3, with the C09 dispatcher:** `parse_launch`, the D12 check, gateway `cli-model` entries, the completeness and backward-compat tests, `verify` V1, V2 and V4 with V3 as warn-only, and the read-only guard design.

#### Shared assumptions (final)

- **A-001: ACCEPT.** Neither variant gives enforced behaviour without C09. Write down that C03 alone enforces nothing. The cost is asymmetric: A needs a skill-text rule (`model == launch`) and B needs a subprocess dispatcher. B's own R1 concedes that gap.
- **A-002: QUALIFY.** Write down these four points:
  - Docs resolution order: parameter, frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, main model.
  - Family aliases run on the parent's exact model when the parent is in the family.
  - The override is documented only for Opus.
  - The binding and V3 are expectations, and only observation settles the served model.
- **A-003: ACCEPT, with a limit.** Write down the reader list from New evidence item 5. Tests and the plugin mirror are not enumerated.
- **A-004: REJECT as stated.** Write: "ember is set in the live env (`T4Model04`) and is absent from packaged data, with no evidence either way on whether it serves". B's V2 does not detect this drift.

#### Per-point positions (updated)

| Point | Superior | Confidence | What changed since Round 1 and why |
|---|---|---|---|
| S-001 | NEITHER | 55 | Unchanged. |
| S-002 | NEITHER | 55 | Unchanged. |
| S-003 | MERGE (A's RUN tags, B's claim/research/code/tag table) | 60 | Unchanged. |
| S-004 | NEITHER | 55 | Unchanged. |
| S-005 | A | 55 | Unchanged. |
| S-006 | MERGE (A's run set, B's table layout) | 62 | Unchanged. |
| S-007 | B | 65 | Unchanged. The staged order I propose borrows B's staging. |
| C-001 | A | 72 | Up from 68. Today's resolve was re-run: gateway with `launch: null` for all four reviewers. |
| C-002 | A | 70 | Unchanged. B conceded R1. |
| C-003 | MERGE (B's grammar as a recorded decision, A's "fill only anthropic-only now", code in the C09 PR) | 58 | Down from 62. A single-string argument cannot carry the read-only guard, and the one executing adapter is `agent-class`. |
| C-004 | MERGE (B's `tiers_as_of` and coupling test, A's `launch_binding`) | 66 | Roughly unchanged. B's guards catch the repo-internal checklist gap but not the live-versus-repo drift (V2 reads Model01 only). |
| C-005 | MERGE (A's binding plus `parent_model` and the derived lookup, B's V3 as warn-only) | 64 | V3 cannot see the parent model, so it can never say "ok". The in-session binding can. |
| C-006 | B | 58 | Down from 62. Right to add, but low value until gateway dispatch exists. Ship with the dispatcher. |
| C-007 | A | 58 | Flipped from B. A positive tier0 test works with a synthetic tier file, and ember is Coder-first. |
| C-008 | A | 62 | Moved from NEITHER. B conceded it is cosmetic. |
| C-009 | MERGE (A's no new command now, B's V1, V2, V4 later) | 55 | Unchanged. V3 is unsound without the parent model. |
| C-010 | A | 62 | `swarm:` has no packaged data. B-side R1 and my merge test agree. |
| C-011 | A | 68 | The Agent path keeps the read-only allowlist and plan mode. A cli-model path needs a C09 design. |
| C-012 | MERGE (A's tests 1, 2, 3, 7 and flips plus family-collision and resume tests, B's completeness and backward-compat tests when the pieces ship) | 62 | Tests follow the pieces actually shipped. |
| C-013 | A | 70 | Unchanged. B advocate agrees. |
| C-014 | NEITHER | 55 | Unchanged. |
| C-015 | A | 62 | Unchanged. |
| X-001 | A | 70 | Slightly down from 72. The family rule limits generality. |
| X-002 | A | 70 | Up from 68. The bare resolve was re-run. B keeps `T3Model01` detection. |
| X-003 | A | 58 | Down from 62. A's label is false too, but controlled and flagged. B ships entries nothing executes. Conceded in item 1. |
| A-001 | NEITHER (ACCEPT) | 85 | Unchanged. The asymmetry is recorded. |
| A-002 | NEITHER (QUALIFY) | 78 | Docs order and the Opus-only exception verified. |
| A-003 | NEITHER (ACCEPT with limit) | 72 | Moved from QUALIFY. Readers enumerated for Python and markdown under `src`. |
| A-004 | NEITHER (REJECT) | 85 | Confirmed in env and the tier file. V2 would not detect it. |

#### Remaining disagreements with the B advocate

- **C-001:** B says MERGE. I say A, because only the class path is executable, and the merged order ships it first anyway.
- **C-003:** B says B at 60%. I say grammar as a decision only, with code in the C09 PR. The read-only guard cannot be expressed in `cli-model:<id>`.
- **C-004:** B says B at 72%. I say MERGE. The coupling test is right, but it does not catch live drift.
- **C-006, C-009:** B says B (60, 52). I say right idea, wrong time. Ship with the dispatcher. V3 is warn-only, never "ok".
- **C-007:** B says B. I say A. The tier0 positive test needs no packaged data, and ember is outside the repo.
- **C-008:** B says A, so we agree. The point is listed only because Round 1 moved it from NEITHER.
- **X-003:** B says NEITHER. I say A at 58%. This is the narrowest call.
- **S-002, S-006:** minor wording differences. B says B and "B's table layout, A's run set".

| Status | Result |
|---|---|
| DONE | Verified by run: today's default resolve (gateway, `launch: null`), the anthropic-only resolve, env bindings, tier file, `reflect-reviewer.md` frontmatter, `manifest.py:277-319`, `SKILL.md:1507` and the sub-agents docs. |
| DONE | Gave positions on all 29 points. |
| NEXT | None for this round. |

I did not re-read `results.md`, the E2 rows or `ccsession-models.json`. I did not check `CLAUDE_CODE_SUBAGENT_MODEL` here, or whether `claude-gw-tier1b[1m]` counts as the sonnet family.

### Variant B Rebuttal

(agent advocate-B-r2, general-purpose, fresh spawn; read the Round 1 transcript and the Variant A rebuttal above)

#### Response to criticisms

I verified these against the repo this round. Facts first:
- `ccsession-models.json` (repo) has `models_env` counts tier0=2, tier1a=2, tier1b=3, tier2=6, tier2b=4, tier3=2, tier4=3.
- This shell has `T3Model01..06` (6 slots) and `T4Model01..04` (4 slots, including `muse-ember-1.0`).
- The tier file's tier3 has 2 models and tier4 has 3.
- `ANTHROPIC_DEFAULT_HAIKU/SONNET/OPUS_MODEL` are `claude-gw-tier2[1m]`, `claude-gw-tier1b[1m]` and `claude-gw-tier1a[1m]`.
- `ANTHROPIC_MODEL` is empty and `CLAUDE_CODE_SUBAGENT_MODEL` is unset.
- This session's own model is `claude-gw-tier1b[1m]`.

**1. V3 cannot model the family-alias rule.** PARTLY.
- True of V3 as written, which maps class, env var, tier alias, first model.
- Not unique to B. `launch_binding` as A wrote it reads the same three variables and has the same gap until A adds `parent_model`.
- A's `parent_model` is a value the orchestrating skill supplies. `panel verify --parent-model <id>` takes the same value, so V3 can flag a family collision exactly as A's binding would.
- On this machine the rule cannot bite for the sonnet class: the parent model equals the SONNET binding. It is UNVERIFIED for haiku and opus, because I cannot tell whether Claude Code puts `claude-gw-tier1b[1m]` in any family.
- Conceded: V3 must be warn-only and never print "ok". B already labels it derived.

**2. B's guards miss the live drift.** CONCEDED for B as specified, HELD that it is cheap to fix.
- V2 reads `Model01` only. The coupling test at `test_review_panel_live7.py:92-106` compares the tier file with the repo JSON by list length. Neither sees `T3Model02..06` or `T4Model04`.
- A cheap fix (not run, not coded): V2 enumerates `T<N>[letter]Model\d+` per tier, using the same injectable-environ seam as `cli/sprint/aienv.py`. It compares the set of env ids with `aliases[tier].models`, flags ids absent from `names` and `classes`, and flags tiers present in env or `ccsession-models.json` but absent from the tier file (tier0 today).
- On this machine that check would warn on tier3 (6 vs 2), tier4 (4 vs 3), `muse-ember-1.0` and tier0. It must compare sets, because live T3 lists `Qwen3.8-max` twice.
- A's `launch_binding` detects none of this, so A cannot use it against B.

**3. `cli-model:<id>` cannot carry the read-only guard.** PARTLY.
- The guard comes from the reviewer agent profile (`reflect-reviewer`: tools allowlist, `permissionMode: plan`), not from the model route.
- `claude --help` lists `--agent`, `--model`, `--permission-mode` and `--allowedTools`. A C09 dispatcher can therefore compose `--agent reflect-reviewer --model <id>`.
- I did not run it, so whether `--model` overrides the frontmatter `model: sonnet` in `-p` mode is UNVERIFIED.
- This is a gap in the not-yet-designed C09 dispatcher, not in the grammar. No C03 path loses the guard, because reflect stays on `--env anthropic-only` in both variants.
- Conceded: B should not call `cli-model` "supported" until C09 states how the guard composes.

**4. tier0 is testable with a synthetic tier file, and C-008 is cosmetic.** CONCEDED on both, with one rider.
- Adding tier0 data now is not needed. The positive test of the reflect "no tier0" rule can use a synthetic file, as `test_adding_a_model_family_is_a_data_edit_only` does.
- Rider: `ccsession-models.json` and this env both define tier0 (`T0Model01=claude-fable-5-1`, `T0Model02=gpt-6-astra`) while the tier file has none. The drift check should report that, whatever is decided about adding data.

**5. `evidence[]` and `gateway_observed_on` are unchecked free text.** CONCEDED. Only `tiers_as_of` and `ccsession_models_version` are enforceable, and the second is the only one worth a test.

**6. Merge-shape test (one executing adapter; provenance regenerates the golden).** PARTLY.
- Right that B-1 bundles gateway entries, provenance, tier0 and the golden into one stage. Splitting fixes that.
- Not right that a grammar with one live adapter is empty. A closed adapter set of `{agent-class}` with a bare-string default does real work (see 7).

**7. Should `parse_launch` and the gateway entries land before C09?** PARTLY, and A is mostly right.
- Gateway entries before a dispatcher exists: A is right. That is B's R1, and I see no correctness or test reason to land them early.
- A minimal `parse_launch` has a small reason to land earlier. `validate_tiers` accepts any string for `launch` (`panel.py:364-368`), so a typo like `haikuu` passes validation and fails only at dispatch or in the reflect check. A closed-adapter parse at validate time is about 15 lines and changes no bytes.
- The decision on the recorded form should be written now: the raw string is persisted and `parse_launch` is derived. That avoids a later manifest hash change (see Staging test).
- I would put the parse in A's PR 2, not in the dispatcher PR. This is a small point, not decisive.

#### Updated assessment of Variant A

Where A is stronger than I credited:
- Class launch is the only form an in-session Agent call can use (platform docs, verified in Round 1).
- It keeps the allowlist and plan mode.
- The staging order is sensible.
- A's drift position is more defensible than I credited: first-model route chains are intact today. Slot 1 of every tier in the live env equals the tier file's first model (tier0, 1a, 1b, 2, 2b, 3, 4). The drift narrows what the resolver can draw from. It does not falsify the haiku-to-`gpt-6.1-sol` route.

Where A is weaker than A's Round 2 says (verified this round):
- **The flip is a relabel for the loop unless the loop dispatches by `launch`.**
  - `document_review_loop_prompts.md:70` says to run each review "with the reviewers that `panel resolve` prints ... each in a fresh context". It says nothing about passing `model` from `launch`.
  - A's rule "model = reviewers[i].launch on every Agent call" sits in the reflect skill (variant-1 lines 23 and 37), not in the loop prompt.
  - So after the flip, a ccsession machine's loop prints sonnet plus 3× `claude-haiku-5-5` instead of sonnet, Qwen3.8-max, glm-5.3, glm-5.3, but dispatches the same way as before.
  - That is a record change with no executed change, the defect X-003 names.
- **The "two classes bind the same model" warning misses the main collapse.** The default template under anthropic-only resolves to 1 sonnet plus 3 reviewers of ONE class (haiku, `stand_in: true` ×3). That is one model three times by construction. On this machine the haiku class is bound to tier2, whose first model is `gpt-6.1-sol`.
- **Today's default is not diverse either.** It draws glm-5.3 twice. So the flip is not a loss of real diversity, but it is not a fix for it either.
- **`expected_first_model` should not live in the hashed payload.** The manifest already carries `tiers_sha256`, so derived values can be recomputed from the binding plus that hash. Hashing them makes a mid-run data upgrade raise `Conflict`.

#### New evidence

1. Counts above: the repo JSON and the live env disagree on tier3 (2 vs 6) and tier4 (3 vs 4). Tier0 is in both the repo JSON and the env but not in the tier file.
2. Verified this session's model and the SONNET binding are the same string, `claude-gw-tier1b[1m]`, with `ANTHROPIC_MODEL` empty and `CLAUDE_CODE_SUBAGENT_MODEL` unset.
3. `claude --help` shows `--agent`, `--model`, `--permission-mode`, `--allowedTools` and `--disallowedTools`. Combined behavior is UNVERIFIED.
4. Both resolves were re-run. Default gives `gateway` with `launch: null` for all four reviewers. `--env anthropic-only` gives sonnet plus haiku×3 with `stand_in: true`. This matches A's Round 2 output.
5. The loop prompt at `:70` has no `model` or `launch` instruction. `SKILL.md:340` writes the reflect `resolved` payload as `{"reviewers_requested", "reviewers_resolved"}` only.

#### Staging test

I keep A's 3-PR order but change PR 1.

**What could go wrong in A's PR 1 as written:**
1. **Flip without a consumer.** The loop prompt does not read `launch`, so on ccsession machines the flip only changes the printed names. If PR 1 does add dispatch-by-launch to the loop prompt, the loop's actual models change from the session default to sonnet plus 3× `gpt-6.1-sol` (via the haiku binding). That is a real behavior change with no test pinning it.
2. **Resume `Conflict` interaction.**
   - `advance_stage` hashes the whole payload.
   - A reflect shadow run started before PR 1 has no `launch_binding`. Replaying `resolved` after the upgrade raises `Conflict`, which is an upgrade artifact and not an alias change.
   - `SKILL.md:1507` already says the Wave 0 alias set is canonical and a re-resolve difference means STOP. The `Conflict` mapping to `alias_set_changed_mid_run` is therefore consistent, but only for genuine env changes.
3. **Test blind spots.**
   - The `select_env` tests inject an environ, so none exercises a real ccsession env.
   - The flipped tests assert only the environment name.
   - No planned test checks that a panel of N same-class reviewers is reported as one model.
   - The tests 1, 2, 3 and 7 pin the reflect path, not the loop.

**What I would change in PR 1:**
- Make the flip and a one-line loop-prompt edit (pass `model` from `launch`, refuse a null launch) a single unit, with a needle test on the loop prompt. Otherwise do not flip.
- Add a single-model warning in the command layer (stderr from `panel_cmd.py`), keyed on N reviewers sharing one class. Keep `resolve` output byte-identical so no resolve goldens change. Which tests pin resolve output bytes is UNVERIFIED.
- Store only the raw `launch_binding` and `parent_model` in the hashed payload. Compute the expected-first-model at report time from `tiers_sha256`.
- Add a legacy-replay test: a payload without `launch_binding` must either be accepted as "not recorded" or fail with a clear message. Decide which, and write it down.

**PR 2** (the one that takes the golden regeneration): `tiers_as_of`, `ccsession_models_version`, the coupling test, the `MODEL-TIERS.md` checklist line and the minimal closed `parse_launch`. Add the env-slot drift check here as well. It touches no tier-file bytes and can start as a `panel validate` option; whether it needs a new `verify` command is a later call.

**PR 3** is with the C09 dispatcher: gateway `cli-model` entries, the completeness and backward-compat tests, the D12 check if not already in PR 2, V1/V2/V4 and V3 warn-only, and the guard composition design.

#### Shared assumptions (final)

- **A-001: ACCEPT.** Write down that C03 alone enforces nothing. Also write down that the loop prompt (`:70`) has no consumer of `launch`, and that A's dispatch rule is a reflect-skill edit. A's PR 1 must add the loop line, or the flip is a relabel.
- **A-002: QUALIFY.** Write down:
  - the docs resolution order and the family-alias rule;
  - that the override is documented only for Opus;
  - that on this machine the parent model equals the SONNET binding;
  - that slot 1 equals the tier file's first model for every tier, but env slots are not routing evidence;
  - that the binding and V3 are expectations, and only C08 observation settles the served model.
- **A-003: ACCEPT with limit.** Python readers of `launch` are `panel.py:153`, `:595` and `:679`, and `select_env` has one caller. Skill and prompt text, tests and the plugin mirror are not enumerated.
- **A-004: REJECT.** Write: "ember is set live (`T4Model04`), absent from `names`, `classes` and `ccsession-models.json`; whether it serves is unknown". B's V2 as specified and A's binding both miss this. A set-comparison check catches it.

#### Per-point positions (updated)

| Point | Superior | Confidence | What changed since Round 1 and why |
|---|---|---|---|
| S-001 | NEITHER | 60 | Unchanged. |
| S-002 | NEITHER | 55 | Was B 55. A's note on rival options is context only. |
| S-003 | MERGE (A's RUN tags, B's claim/research/code/tag table) | 58 | Unchanged. |
| S-004 | NEITHER | 60 | Unchanged. |
| S-005 | A | 55 | Unchanged. |
| S-006 | MERGE (A's run set and uncovered-gap tests, B's table, completeness and backward-compat tests) | 60 | Add the loop-prompt, legacy-replay, same-class-collapse and env-slot-drift tests. |
| S-007 | MERGE (B's gated stages, A's PR order) | 62 | Was B. A's 3-PR plan is itself staged. |
| C-001 | MERGE (A's class launch ships first, B's gateway as a later stage) | 58 | Held from Round 1. The flip is a relabel unless the loop dispatches by `launch`. |
| C-002 | A | 62 | Up from 58. R1 conceded, and `{}` is honest while nothing reads it. |
| C-003 | MERGE (B's grammar as a decision plus a minimal closed `parse_launch` in PR 2, A's no gateway entries now) | 62 | Was B 60. Gateway entries wait for C09. |
| C-004 | MERGE (B's `tiers_as_of` and coupling test, A's `launch_binding`, plus the env-slot drift check) | 68 | Down from B 72. The coupling test alone is repo against repo. |
| C-005 | MERGE (A's binding with `parent_model`, B's V3 as warn-only with `--parent-model`) | 68 | The family-alias rule is a shared gap, fixed the same way in both. |
| C-006 | MERGE (B's command-layer D12 check, A's timing) | 55 | Was B 60. The check is the same code as the drift check, so ship it in PR 2. |
| C-007 | A | 58 | Was B 62. A synthetic tier file tests the rule. Keep a drift guard that reports the missing tier0. |
| C-008 | A | 65 | Cosmetic; B conceded. |
| C-009 | MERGE (A's no new command in PR 1, B's V1, V2 extended, V4 later, V3 warn-only) | 55 | Unchanged in shape. |
| C-010 | A | 60 | Was NEITHER. `swarm:` has no data or executor. |
| C-011 | A | 66 | Up from 60. The Agent path keeps the allowlist. The `claude -p` guard is a C09 design question. |
| C-012 | MERGE (A's tests 1, 2, 3, 7, B's completeness and backward-compat tests) | 62 | Plus the four tests listed under S-006. |
| C-013 | A | 70 | Unchanged. |
| C-014 | NEITHER | 55 | Unchanged. A payload key added to the hash is not free to revert for in-flight runs. |
| C-015 | A | 62 | Unchanged. |
| X-001 | A | 60 | Unchanged. B's R3 holds only for raw ids in launch data. |
| X-002 | A | 55 | Unchanged. The diagnosis is right, but its impact is narrower: the loop does not read `launch`. |
| X-003 | NEITHER | 62 | Held. A's flip also labels `claude-haiku-5-5` ×3 for runs that served `gpt-6.1-sol`. |
| A-001 | NEITHER (ACCEPT) | 85 | Added the loop-prompt fact. |
| A-002 | NEITHER (QUALIFY) | 75 | Added the parent and binding facts above. |
| A-003 | NEITHER (ACCEPT with limit) | 70 | Unchanged. |
| A-004 | NEITHER (REJECT) | 85 | Counts verified. Neither guard as specified detects it. |

#### Remaining disagreements with the A advocate

- **C-001, X-002:** A says A at 70 to 72. I say the flip is label-only unless PR 1 edits the loop prompt, so I hold MERGE and A at 55.
- **C-004:** A and I both say MERGE. I add the env-slot drift check to PR 2. A leaves live-versus-repo drift unguarded.
- **C-005:** A says V3 can never say "ok" because it cannot see the parent. A `--parent-model` input fixes that exactly as A's `parent_model` does. The gap is shared.
- **C-006, C-009:** A says ship with the dispatcher. I say the slot-set check ships in PR 2, since it is the same code as the drift check. Only V3 and gateway entries wait for C09.
- **C-003:** I want the minimal closed parse at validate time in PR 2. A defers all of it to the dispatcher PR.
- **X-003:** A says A at 58. I hold NEITHER.
- **PR 1 contents:** I would keep derived values out of the hashed payload and add the legacy-replay test. A does not list either.

| Status | Result |
|---|---|
| DONE | Verified live-versus-repo slot counts, parent and binding match, `claude` flags, loop prompt text and both resolves; updated all 29 points. |
| NEXT | None. The `--agent` plus `--model` composition and the family rule for haiku and opus remain UNVERIFIED. |

## Round 2.5: Invariant Probe

Single independent fault-finder agent (fault-finder-r25, general-purpose, not an advocate), run after the Round 2 convergence check and the taxonomy coverage check. Full findings table: `invariant-probe.md`. Result: 14 findings, 4 ADDRESSED (all LOW), 10 UNADDRESSED (2 HIGH, 7 MEDIUM, 1 LOW).

- HIGH INV-009 (interaction_effects): the proposed dispatch rule "every Agent call carries model == launch" collides with the reflect shadow-mode contract. `SKILL.md:342` "Dispatch is the legacy dispatch"; `SKILL.md:341` records `panel_parity` between the resolution and the legacy rotation as it ran. Forcing dispatch to follow `launch` makes parity true by construction. Neither advocate saw this; Advocate A cited `:342` only as proof that nothing reads `launch`.
- HIGH INV-013 (sufficiency_challenge): "PR 1 alone makes every dispatched reviewer launch with a valid class" is falsified by two verified conditions: the loop prompt (`document_review_loop_prompts.md:70`) never tells the loop to pass `model` from `launch`, and reflect passes `--env anthropic-only` itself so the `select_env` flip never reaches it. This is the reasoning behind the C-001 split (B advocate: the flip is a relabel unless the loop prompt is edited), now confirmed by an independent party.
- Orchestrator verified both HIGH items against the files (see invariant-probe.md header).
- MEDIUM items feed the refactor plan as required tests or text: INV-001 (binding written by the model from no mechanical source), INV-003 (no code check of a null or out-of-set launch outside reflect templates), INV-004 (no D4 in the loop), INV-005 (N_eff versus resolution count), INV-006 (class-ceiling test is near vacuous), INV-010 (flip is a no-op for reflect; changes `live7` for loop runs), INV-014 (nothing reads `launch_binding`).

## Taxonomy Coverage Gate (AD-5)

| Level | Points | Addressed in debate | Result |
|-------|--------|---------------------|--------|
| L1 surface | S-001, S-003, S-004, S-005 | positions in R1 and R2 from both advocates | covered |
| L2 structural | 15 points | positions in R1 and R2 | covered |
| L3 state-mechanics | 10 points | positions in R1 and R2 plus INV probe | covered |

No forced round was required.

## Scoring Matrix

Winner rule (protocol): both advocates name the same label in their final Round 2 table = agreed; confidence is the mean of the two stated confidences, +10 when the losing side explicitly conceded the point in its rebuttal, capped at 95; different labels = unresolved at 50%. For a MERGE label both advocates must name the same direction (elements may differ in detail; the residual detail is recorded). Shared assumptions are scored as the agreed stance, not as a winner.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | NEITHER (tie) | 58% | Preamble style only; both advocates NEITHER. |
| S-002 | NEITHER (tie) | 55% | B's rival-option paragraph is context, not substance (B advocate withdrew its R1 B vote). |
| S-003 | MERGE | 59% | A's RUN-verified tags plus B's claim/research/code/tag table. |
| S-004 | NEITHER (tie) | 58% | Both state what they do not claim. |
| S-005 | Variant A | 55% | Standalone weakest-point paragraph is more visible; contested only on style. |
| S-006 | MERGE | 61% | A's run set and gap tests plus B's table, completeness and backward-compat tests; plus loop-prompt, legacy-replay, same-class and env-slot-drift tests. |
| S-007 | UNRESOLVED (B-leaning) | 50% | A: B (65); B: MERGE (B's gated stages, A's PR order, 62). Both adopt staged delivery; label differs. |
| C-001 | UNRESOLVED | 50% | A: A (72); B: MERGE (58). Both ship the class path first; B holds that the flip is only a relabel unless the loop prompt is edited too; INV-013 supports that reading. |
| C-002 | Variant A | 76% | `launch: {}` is honest while nothing reads it; B conceded R1 (data ahead of executor). |
| C-003 | MERGE | 60% | Grammar decided now, bare string means agent-class, no gateway entries until C09; closed `parse_launch` timing disputed (PR 2 vs C09 PR). |
| C-004 | MERGE | 67% | Minimal `tiers_as_of`, `ccsession_models_version`, coupling test, checklist line, plus A's `launch_binding`; live-env drift needs a set-comparison check. |
| C-005 | MERGE | 66% | A's binding plus `parent_model`; B's V3 only as warn-only, never "ok", with a parent-model input; shared family-alias gap. |
| C-006 | UNRESOLVED (B-leaning) | 50% | A: B (58, "right idea, wrong time"); B: MERGE (55). Both want a command-layer check; timing (PR 2 vs with the dispatcher) differs. |
| C-007 | Variant A | 68% | Add no tier0 or ember data in C03; synthetic tier file tests the rule (B conceded); drift guard must still report tier0 and ember. |
| C-008 | Variant A | 74% | `_check_reflect_resolution` already rejects any non-class launch; adapter-naming message is cosmetic (B conceded). |
| C-009 | MERGE | 55% | No new command in PR 1; V1, V2, V4 later; V3 warn-only. |
| C-010 | Variant A | 71% | `swarm:` has no data and no executor; B's grammar slot is speculative (B conceded). |
| C-011 | Variant A | 77% | Class path keeps the allowlist and plan mode; the `claude -p` read-only guard is an open C09 design question (B conceded). |
| C-012 | MERGE | 62% | A's tests 1, 2, 3, 7 and flips plus B's completeness and backward-compat tests when the pieces ship, plus the four added tests. |
| C-013 | Variant A | 80% | XS-S Medium against L High (B conceded). |
| C-014 | NEITHER (tie) | 55% | Both reversible; a payload key added to the hash is not free to revert for in-flight runs. |
| C-015 | Variant A | 72% | Platform-doc evidence is decisive; B's self-preference literature is tangential (B conceded). |
| X-001 | Variant A | 75% | Class binding serves non-Claude models in-session; B's R3 holds only for raw ids passed on the call (B conceded). |
| X-002 | Variant A | 72% | Default is the defect A names; B's "gateway is the default" is loose (B conceded); impact narrower than A states because the loop does not read `launch` (INV-010). |
| X-003 | UNRESOLVED | 50% | A: A (58); B: NEITHER (62). Both labels can differ from what serves; B ships unexecuted entries, A ships a false but flagged label. |
| A-001 | ACCEPT (agreed) | 85% | No reader of `launch` outside the resolver; C03 alone enforces nothing; loop prompt has no consumer. |
| A-002 | QUALIFY (agreed) | 77% | Family-alias rule, Opus-only documented override; binding and V3 are expectations; sonnet benign on this machine. |
| A-003 | ACCEPT with limit (agreed) | 71% | `select_env` one caller; readers of `launch` not fully enumerated (skills, tests, plugin mirror). |
| A-004 | REJECT (agreed) | 85% | `T4Model04=muse-ember-1.0` set live; absent from data; serving unknown. |

Points won (S, C, X only): Variant A 10 (S-005, C-002, C-007, C-008, C-010, C-011, C-013, C-015, X-001, X-002); Variant B 0 outright; MERGE 7 (S-003, S-006, C-003, C-004, C-005, C-009, C-012); NEITHER 4 (S-001, S-002, S-004, C-014); UNRESOLVED 4 (S-007, C-001, C-006, X-003).

## Convergence Assessment

- Points resolved: 25 of 29 (agreed label in both advocates' final tables, shared assumptions included)
- Alignment: 86.2% (25/29)
- Threshold: 80%
- Unresolved points: S-007, C-001, C-006, X-003
- Taxonomy gate: all levels covered
- Invariant probe gate: BLOCKED, 2 HIGH UNADDRESSED (INV-009, INV-013)
- Status: BLOCKED_BY_INVARIANTS (agreement is above threshold, but convergence cannot be declared)
- Sycophancy check: Round 1 both advocates leaned to MERGE with A as the core. Round 2 prompts told both to test that shape. Several Round 2 moves were evidence-driven and verifiable (tier0 and ember moved from B to A; V3 downgraded to warn-only; B advocate verified live-env slot counts and A's flip being a relabel for the loop; the fault-finder then found two HIGH problems neither advocate had raised). The residual risk is shared blind spots: both advocates leaned on the same two doc fetches and did not re-read E2 results; no advocate observed an in-session dispatch.
