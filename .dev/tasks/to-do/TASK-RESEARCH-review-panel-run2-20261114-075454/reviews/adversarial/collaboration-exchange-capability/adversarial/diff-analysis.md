# Diff Analysis: Position Paper Comparison (slot C-12, collaboration-exchange-capability)

## Metadata
- Generated: 2026-11-15 (orchestrator run; session date 2026-11-14/15 boundary, see env)
- Variants compared: 2 (Variant 1 = Proposal A, "static kit unconditional, exchange deferred"; Variant 2 = Proposal B, "build the dormant exchange transport into the core now")
- Mode: A (compare). Depth standard. Focus: correctness, risk, test-coverage.
- Total diff points (debate denominator): 25 = structural 3 + content 12 + contradictions 7 + promoted shared assumptions 3
- Categories: structural (3), content (12), contradictions (7), unique (14), shared assumptions (6 surfaced, 3 promoted)
- Evidence staleness (binding on every agent): research pins E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`; later commit `c44c98a77` (2026-11-14 14:19) is [POST-BASELINE]. A fact that exists only at `c44c98a77` may not be the only evidence for a decisive point.

### Framing note (orchestrator observation, not a verdict)
B states that "the static kit and H1/H2 ship as well; nothing in B removes them" (B section 1). So the two papers agree on H1, H2, H3, H4, the catalogue/kit, the sidecar peer tag, the byte-identical off state, no change to `cli/reflect` and consistency with C-01/C-02/C-03. The whole dispute is the delta: whether the exchange transport (hook script, board reader and atomic appender, seal check, `panel-msg/1` validator, `collab` record, per-session `--settings` launch adapter) is built into the product now (B) or only after an exchange arm beats the static kit on ground truth (A, with one reserved `exchange: off` key).

## Structural Differences

| # | Area | Variant A | Variant B | Severity | Tax. |
|---|------|-----------|-----------|----------|------|
| S-001 | Section order | 0 evidence legend, 1 position, 2 consistency with C-01..C-03, 3 design consequence, 4 evidence, 5 invariants, 6 test, 7 PR/rf-qa, 8 objection | 0 conventions, 1 position, 2 design consequence, 3 evidence (A-F), 4 consistency with C-01..C-03, 5 invariants, 6 test, 7 PR/rf-qa, 8 objection | Low | L1 |
| S-002 | Evidence form | Numbered claim table E1-E12 with tag per row, plus a computed cost table | Lettered sub-sections A-F, bullets with file:line and tags; post-baseline kept in F | Low | L1 |
| S-003 | Core/non-core partition | Core = H1, H2, H4 principle, H3 rule, catalogue, `kit` key, reserved `exchange` key (value `off` only); everything else "stays on the E2 branch as design input" (A 3.1, 3.2) | Core = the same plus the exchange package, one installed hook script, a raw-id launch adapter with persistence and per-session `--settings`, kill switch (B 2.1-2.4) | High | L2 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Tax. |
|---|-------|--------------------|--------------------|----------|------|
| C-001 | What the core builds now | Reserved key and rules only; no hook library, board, seal, message-kind registry, per-session settings, `PANEL_COLLAB` switch, budget math or alarms (A 3.2) | Hook skeleton, board, seal, `panel-msg/1` validator, `collab` record, launch adapter, as a dormant capability (B 2) | High | L2 |
| C-002 | Gate for building exchange | Not built until an exchange arm beats A2 (kit) with a committed rule and power calculation (A 6.1) | Built now because the deciding measurement is only repeatable by others if a product transport exists (B 1, 8) | High | L2 |
| C-003 | Static kit mechanics | One catalogue source per module rendered by the brief builder; `kit: on|off` per profile; reflect starts off; cost gate per module (A 3.1 item 5, 3.4) | Kit "ships as well"; no profile key, no cost gate stated (B 1) | Medium | L2 |
| C-004 | Launch path and hook placement | None built; keeps the `--no-session-persistence` pins untouched | New raw-id adapter with persistence on and per-session `--settings`, not `ClaudeProcess.build_command()` (B 2.3); one hook in `src/superclaude/hooks/scripts/` plus `hooks.json` (B 2.2); tied to slot C-07, which is still open | High | L2 |
| C-005 | Between-phase family F1 | No clean measured success in any runtime; `--resume` on gateway ids not evidenced (A 4.4, E8) | The one portable family; no hook, no model-side write; swarm form is a second prompt; the swarm run is [UNVERIFIED] (B 2.8) | Medium | L2 |
| C-006 | Peer-origin tag | Sidecar preferred; open unknown key keeps in-line possible (A 3.2); `origin` name must be avoided (CL-X11) | Sidecar mandatory, harness-written, keyed by reviewer id and finding id (B 2.5) | Low | L2 |
| C-007 | Test and measurement plan | 7 items: matching-control A1/A2/exchange with power, kit cost n>=4 per panel, common act-rate probe, off-state equality, brief lint, existing pins, catalogue hold-out of >=4 defects (A 6) | 8 items: off-state argv identity, existing pins, product-launcher S0/S2 per model, fault injection R-22, hook latency p95 over >=30 calls, single-copy replay with `agent_id` and parallel calls, pre-registered arm comparison with served model recorded, echo/independence alarms (B 6) | Medium | L2 |
| C-008 | Where the decisive measurement can run | Same experiment either way; "costs nothing extra under either position" (A 6.1) | E2 arms could not run from the pinned commit (`lib/` absent) and are study scripts under `.dev/`; a product transport makes arms repeatable (B 3.D, 8) | High | L2 |
| C-009 | Reading of [POST-BASELINE] results | `k` is 0 in most cells; owner had to relax the +35% cap to run exchange; first counted rows no separation; kit rows ahead of A1 at n 2 vs 4; kit cost +10% to +35% (A 4.2, 4.3) | Same facts, listed as counter-evidence; a `collab` record of delivered 0, late 6, k 0 is itself a finding the transport would capture (B 3.F, 8) | Medium | L2 |
| C-010 | Message validation and untrusted text | Mentions that exchange board text would add document text that INV-H would have to cover (A 5) | Validator with forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, fixed templates; admits attacker-controlled diff text can be echoed to a peer (B 5) | Medium | L3 |
| C-011 | Off-state guarantee mechanism | Profile key `exchange` with one legal value `off`; test that argv and brief bytes equal a profile without the key (A 3.1 item 6, 6.4) | Adapter parameter whose off state emits no `--settings`, no board dir, no second phase; argv-diff test against the adapter without the package (B 2.4, 6.1) | Medium | L3 |
| C-012 | Effect on future PR review and rf-qa | Kit per lens brief; exchange never needs a lane there; conflict with C-11 read-only requirement does not arise (A 7) | Exchange off; PR profile declares `exchange: off`; PR needs mechanically read-only reviewers and untrusted-diff handling (B 7) | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Tax. |
|---|-------------------|--------------------|--------------------|--------|------|
| X-001 | Build the transport into the core now? | "does not build now" (A 3.2); defer until an arm beats the kit | Build now as a dormant capability (B 1, 2) | High | L2 |
| X-002 | Is `--resume` on gateway ids evidenced? | Not evidenced; F1 "has no clean measured success in any runtime" and resume dependency "not evidenced" (A 4.4, citing r09 OQ-2) [UNVERIFIED] | Evidenced by recorded S2 lines: r5 NOTES.md:23-30 and r2 RESULTS.md:8-14 pass for 3-4 gateway models; synth-05 OQ-2 statement is stale (B 0, 3.B) | Medium | L3 |
| X-003 | Does main-thread-only hook delivery make the transport worth owning? | Only `claude -p` main-thread lane can carry it; HEAD reviewers are swarm (HTTP) and Agent-tool (no Bash); delivery to a subagent model is unshown (A 4.4, E4, E5, E10) | Same facts accepted; hook skeleton skips subagents on purpose; relies on the headless lane and F1 for others (B 3.C, 5) | Medium | L3 |
| X-004 | Does the hook fit the 0.1 s budget? | "tens to about 150 ms against a 0.1 s planning budget" [UNVERIFIED] (A 8) | 57-85 ms p95 recorded (r5), 73 and 81 ms (r2); r4 143 and 90 unverified (B 3.C) | Medium | L3 |
| X-005 | Does divergence of the four hook copies justify one product copy? | Skeleton is "described line by line"; the packages "stay on the E2 branch as design input" (A 8 answer 1) | Copies already diverge: r2 has no `agent_id` branch; r1 `flock -w 4` vs r5 untimed `flock 9`; one tested copy is cheaper (B 3.A) | Medium | L3 |
| X-006 | Does installing the hook in `hooks.json` keep the off state inert? | Not addressed; reserved key off means nothing exists | Hook "registered as `~/.claude/hooks/...` in `hooks.json`" (B 2.2) while arguments are baked into per-reviewer `--settings` (B 2.2) and off emits no `--settings` (B 2.4): unclear whether a global registration fires in non-panel sessions | Medium | L3 |
| X-007 | Is waiting free? | Nothing is thrown away; retrofit is bounded by open keys, sidecar, run-record field, reserved key (A 8 answers 1, 2) | Waiting is not free for the measurement; three of five designs run only from `.dev/` with `git add -f` for `lib/`; r2 still cannot run (B 8) | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | H1: `driving_documents: [{role, path_template, sha256_source}]` rendered into the brief; evidence that HEAD's loop brief has no role for a second driving document | High |
| U-002 | A | Kit cost priced from the pinned r5 rows (1.59 elapsed, 1.55 tokens) and the [POST-BASELINE] Spike 4 means (+10% el2, +35% hl2) with spread caveat | High |
| U-003 | A | Brief lint test: no read-only lane's rendered brief may instruct running a command (guards INV-G against shell-form E2 recipes) | Medium |
| U-004 | A | Catalogue provenance hold-out: both catalogues induced from the same ten missed issues; >=4 unseen defects needed | Medium |
| U-005 | A | One common act-rate probe across models and instruction forms (5+ sessions per model), cheap, decides deliverability | Medium |
| U-006 | A | Link to X-13: the kit and class cards must render from one data source | Low |
| U-007 | A | Act-rate disagreement table (E6) for the same model across probes | Medium |
| U-008 | B | Product hook directory convention and recurring latency suite `hook_latency_drift.yaml` as the home for a latency pin | Medium |
| U-009 | B | Package name `exchange/` instead of `lib/` because `.gitignore:13` is `lib/` (the loss that hit E2) | Medium |
| U-010 | B | `panel-msg/1` per-kind key table, forbidden verdict keys, harness-authored kinds only (F1 digest, F3 move, F6 coverage); model-authored writers F4 and F7 excluded since `reflect-reviewer` cannot write | High |
| U-011 | B | Untrusted-text channel analysis: anchors from a reviewed PR diff are attacker-controlled and would be echoed to a peer; board files must never enter the `review-telemetry` export | High |
| U-012 | B | Fault-injection test (corrupt board line, missing transcript, lock timeout) and the seal that fails closed while review fails open | Medium |
| U-013 | B | Conditional concession: if slot C-07 yields no persistence plus per-session `--settings` launcher, B shrinks to validator, sidecar and the F1 second prompt | Medium |
| U-014 | B | Quorum interplay with C-02: counts of affirmations must be computable over own-origin lines only; exchange off wherever the C-02 quorum applies | Medium |

## Shared Assumptions

Agreement points scanned: H1/H2/H3/H4 and kit ship; exchange off by default; byte-identical off state with a test; sidecar peer tag; no change to `cli/reflect`, contract 1.8.0, `derive_verdict`; `reflect-reviewer` independent with no Bash; swarm transport has no tool loop; nobody has measured exchange benefit; E2 plan cannot detect the central gain; the deciding comparison is exchange arm against A2 on ground truth; consistent with C-01, C-02, C-03; exchange off for PR review and rf-qa.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both rely on "a package with real ground truth" as the arbiter | E2's 16 ground-truth items in 3 plans (3 items carry 91% of defect-rich catches, per r08) transfer to the modules the core serves (spec review, reflect, PR review, rf-qa), so an arm-against-kit result on them is decision-relevant | UNSTATED | Yes |
| A-002 | Both pin an off-state equality test (A 6.4, B 6.1) | Byte-identical argv/brief with the switch off is sufficient to prove the capability is inert, i.e. there are no other off-state side effects (registered hook entries, created directories, telemetry fields, extra files, new test fixtures, sync-gate layout items) | UNSTATED | Yes |
| A-003 | Both accept that exchange may later win or lose | The decision is cheaply revisitable: whichever side loses now can be added or removed later at bounded cost (A: retrofit bounded; B: dormant code costs nothing when off); neither measures maintenance or retrofit cost | UNSTATED | Yes |
| A-004 | B concession (B 8), A 8 | Exchange value, if any, depends on a launcher that offers session persistence and per-session `--settings` (slot C-07, still open) | STATED (B concession) | No |
| A-005 | A CL-C09, B 4 (C-03 condition 5) | The served-model identity can be recorded (slot C-08) so act rates are interpretable; until then independence is "requested, not served" | STATED | No |
| A-006 | A 6.1, B 6.7 | The metric of record (slot X-14) and the decision rule are fixed before the first arm run | STATED | No |

### Promoted [SHARED-ASSUMPTION] diff points
A-001, A-002, A-003 (counted in the convergence denominator; each advocate must answer ACCEPT / REJECT / QUALIFY).

## Summary
- Total structural differences: 3
- Total content differences: 12
- Total contradictions: 7
- Total unique contributions: 14
- Total shared assumptions surfaced: 6 (UNSTATED: 3, STATED: 3, CONTRADICTED: 0)
- Highest-severity items: S-003, C-001, C-002, C-004, C-008, X-001
- Taxonomy tagging: L1 = S-001, S-002; L2 = S-003, C-001..C-009, C-012, X-001, X-007, A-001, A-003; L3 = C-010, C-011, X-002..X-006, A-002
- Similarity check: not "substantially identical" on the disputed delta (build now versus defer); debate proceeds.
