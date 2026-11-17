# Proposal B: slot C-01 (core-shape-and-finding-contract)

Status: Complete
Position: B (thin shared contract with per-module engines)
Conflicts in scope: C-S1, CO-1, CO-2, CO-3, CO-4, CL-X11 (placement), FX-1, FX-2 (synth-06 6.12.1, 6.12.2, 6.12.5; undecidable-conflicts.md row C-01)
Axis: synth-05 6.1 (core shape, option C) and 6.2 (finding contract, option 1 with a module-scoped unknown-key policy)
Tag convention: [CODE-VERIFIED] = I read the cited line at HEAD 50d4d2b9d in this session, or ran a Grep whose result is quoted; [CODE-CONTRADICTED] = the code differs from the stated claim; [UNVERIFIED] = taken from a research or synthesis file and not re-read in code by me (the file is named).

## 1. The position in one paragraph

The shared core is a thin, versioned contract, not a merged engine. It owns only what is already shared or can be fixed once for every engine: the finding id grammar, the shared limit constants and the one pre-parse repair or itemise step (the policy is chosen in C-06), the per-module reference-token pattern list (so `T01.02` is fixed once), hashing and identity helpers, panel resolution (`panel.py`, already shared), the run record (location chosen in C-08), and the evaluation harness (X-14). Engines stay per module: the v1 anchor parser, `merge_round` and `review-ledger/1` keep serving spec review as they are; the v2 citation kernel (`findings_v2.py`, `cluster.py`, `verify_cmd.py`, `manifest.py`) serves reflect and PR review; the unknown-key policy is per module (open for the two shipped grammars, closed where one module owns both producer and consumer); and convergence of the two pipelines is deferred until a consumer needs a multi-reviewer re-review ledger over citation-located findings. Position B treats the missing locator-agnostic `annotate` as an engine boundary to guard, not a rewrite to schedule now.

## 2. Design consequence for the shared core and the named modules

### 2.1 What the contract contains (and nothing else)

| Contract element | Content | Today | Cost under B |
|---|---|---|---|
| Finding id grammar | `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` | one regex; v2 imports it from v1 (`findings_v2.py:15-22`, used at `findings_v2.py:99-100`) [CODE-VERIFIED] | none (already shared) |
| Limit constants and repair step | anchor and quote 12..200, claim at most 300, refs at most 8, citations 1..8; one normalise-or-itemise function that runs before either `parse_block` | v2 restates the numbers as literals (`findings_v2.py:111,114-120,126,128,132,136`) [CODE-VERIFIED]; v1 has the same numbers at `findings.py:104,108,111-117,118` [UNVERIFIED], research/02:17 | one constants module imported by both parsers; one repair function (policy: C-06) |
| Reference-token list | per-module pattern list behind `refs_norm`, with `T<PP>.<TT>` added for the tasklist module | `findings.refs_norm` (`findings.py:321-337`) is called by `cluster.annotate` (`cluster.py:141`) [CODE-VERIFIED]; the pattern `_REF_TOKEN` is `findings.py:29` [UNVERIFIED re-read, research/02:72]; a second copy sits at `telemetry.py:23-27` [UNVERIFIED], research/02:79 | fixed once in `refs_norm`; both clusterers inherit it |
| Hash and identity helpers | `sha256_text`, manifest-frozen input hashes, requested, resolved and observed model | ledger entries keep `report_sha256` and `model` from the resolution only (`ledger.py:144,146`) [CODE-VERIFIED]; manifest side [UNVERIFIED], research/01:110 | helper functions plus a schema id per record |
| Panel resolution | `panel.py`, tier JSON, templates, `resolve_slot` | the one module both pipelines share besides the container, `refs_norm` and `_ID` [UNVERIFIED], research/scope/09:454 | none; C-09 decides the data owner |
| Run record | one adapter that writes the cross-run row from either engine's own state | four formats today [UNVERIFIED], research/01 s5 C-10 | decided in C-08, not here |
| Evaluation harness | tiers S, Q, G and `verify-run` | none in product | decided in X-14, not here |
| Projection view | a read-only function that turns either engine's finding into `{id, severity, blocking, category, location, claim, refs_norm, module}` for telemetry, export and the eval harness | none | one function per engine, tested by the conformance suite in section 5 |

The projection is a view, not a merge: it never feeds a ledger. This keeps the contract at interface level, where research/13 section 8 places the exposures M2 to M5, M10 and M11 (none of them needs a ledger) [UNVERIFIED], research/13:209-224.

### 2.2 Module by module

| Module | Engine under B | Location type | Unknown keys | Change needed |
|---|---|---|---|---|
| Spec review loop | v1 `findings.py`, `ledger.py`, `merge_cmd.py`, `ledger_cmd.py`, unchanged in shape; fixes for D-1, D-2, D-11, D-13 belong to C-02 and C-03 and land inside this engine | quoted `anchor` (12..200) | open (INV-C) | adopt shared constants and the repair step; add the boundary guard of 2.3 |
| Reflect UC-1 and UC-2 (Tier 2) | v2 kernel inside the existing fail-closed shell (shell choice: C-04) | `citations` | open, as today | adopt shared constants, repair step and `refs_norm` list; no change to contract 1.8.0 names |
| PR code review | v2 citations, a pure adapter to `pr_submit.Finding`, no ledger (wire format: C-10) | `citations[0].line_start` becomes `line` (research/13:176, P1) [UNVERIFIED] | closed at the adapter, because the adapter is the only producer | module-supplied category, lens and severity sets (M2) in the v2 engine; `Finding`, `Severity` and the FSM untouched |
| rf-qa replacement, first step at the `/task` gate | v2 kernel plus the module's checklist mode; reviewer contract mechanically read-only | module's choice (a task file or phase output is a document; a code review is a path) | module's choice | per-slot lens, checklist output, agent-count rule (research/13 R1 to R3) [UNVERIFIED], all independent of the ledger shape |
| Tasklist and workflow | reached through reflect UC-1 (C-05) | as reflect | as reflect | `T01.02` ref pattern |

### 2.3 The one boundary guard B adds

The verified hole: a citation-only finding raises `KeyError: 'anchor'` inside `annotate` (`findings.py:346-349`), reached from `merge_round` at `ledger.py:135-138` [CODE-VERIFIED by Read of both ranges; reproduced as probe P-a in research/01:53 and as D-12 in research/scope/09:260]. B closes it at the ledger entry: `merge_round` rejects a finding that has no `anchor` with a typed `LedgerError` that names the finding id and says the ledger is anchor-located, instead of a `KeyError` from inside `annotate`. That is one function and one test. It turns an accidental crash into a declared engine boundary. It does not make `annotate` locator-agnostic and does not add citation-keyed ledger rows.

### 2.4 What B defers, on purpose

1. A v2-native re-review contract that replaces `prior` lines (CO-2). Under B, `prior` lines stay a v1-engine feature (`document_review_loop_prompts.md:61` [CODE-VERIFIED by Grep]); the v2 kernel has no re-review round because reflect has no finding ledger or rounds today [UNVERIFIED], research/01:150.
2. Which clustering the core adopts (CO-3). Both clusterers stay, each with a declared owner. Whether the line-insensitive v2 fingerprint is intended (`cluster.py:119-123` hashes role, path, an empty section, refs and class and never a line number [CODE-VERIFIED]; GQ-023, OQ-25) is answered inside the reflect engine with its own test, not by the core.
3. A single unknown-key policy (CO-4). Per module, as in 2.2.
4. A locator-agnostic ledger. It becomes work only when the trigger in section 5.4 fires.

## 3. Evidence

### 3.1 The two pipelines are disjoint, so a thin contract matches the code that exists

| # | Claim | Evidence | Tag |
|---|---|---|---|
| E-1 | No code path leads from v2 findings to the ledger. The v2 modules are imported by exactly six files: `scripts/reflect_cluster_pairs.py`, `scripts/reflect_stage0a_replay.py`, `cli/review/verify_cmd.py`, `cli/review/cluster_cmd.py`, `cli/review/card_convert.py`, `cli/review/cluster.py`. `ledger.py`, `merge_cmd.py` and `ledger_cmd.py` are not among them. | Grep `findings_v2\|cli\.review\.cluster\|from \.cluster\|\.manifest import\|cluster_v2` over `src` and `scripts` `*.py`, files-with-matches | [CODE-VERIFIED] |
| E-2 | The reflect Python package imports nothing from `cli/review`. | Grep `^(import\|from) .*(cli\.review\|\.review\b)` over `src/superclaude/cli/reflect`: no matches. research/01:40 reports the same result for all of `src` outside `cli/review` (one hit, `main.py:568`) | [CODE-VERIFIED] for `cli/reflect`; [UNVERIFIED] for the whole-`src` claim |
| E-3 | A citation-only finding crashes the v1 ledger path: `annotate` does `locate(text, finding["anchor"])` with no `.get` (`findings.py:349`); `merge_round` calls `fnd.annotate` for every parsed finding (`ledger.py:135-138`). | Read of both ranges; probe P-a in research/01:53 | [CODE-VERIFIED] |
| E-4 | The v1 side of the loop is the shipped consumer and is pinned: `review-ledger/1` or `findings-v1` appears 26 times in 10 files: the loop brief in `src/` and `plugins/` (1 each), `findings.py` 6, `findings_v2.py` 3, `ledger.py` 2, and five test files (`test_review_cli.py` 2, `test_review_findings.py` 5, `test_review_findings_v2.py` 1, `test_review_ledger.py` 4, `test_review_rules_text.py` 1). Further static pins of the loop bullets sit in `tests/skills/test_review_severity_mapping.py`, `test_review_brief_placement.py` and `test_spec_panel_review_loop.py`. | Grep `review-ledger/1\|findings-v1` over `src`, `plugins`, `tests`, count mode; the three skill tests: research/12:48-49 | [CODE-VERIFIED] for the 26 / 10; [UNVERIFIED] for the three skill tests |
| E-5 | Both pipelines are two to three days old and each has one commit: `findings.py` and `ledger.py` last changed in `9163bd1c7` (2026-11-11, #498); `findings_v2.py` and `cluster.py` have only `d2d8a2d16` (2026-11-12, #519). There is no history of paying a divergence cost twice, so "B fixes each shared defect twice" is a projection, not a measurement. | `git log --format='%h %ad %s' -- <file>` for the four files | [CODE-VERIFIED] |

### 3.2 Which defects are shared and which are engine-local (this is what bounds B's duplication)

| # | Defect | Where it lives | Fixed once under B? | Tag |
|---|---|---|---|---|
| E-6 | `T01.02` is not a reference token | one function, `findings.refs_norm` (`findings.py:321-337`), called by both `findings.annotate` (`findings.py:357`) and `cluster.annotate` (`cluster.py:141`); the pattern `_REF_TOKEN` at `findings.py:29` | yes | [CODE-VERIFIED] for the functions and call sites; pattern text [UNVERIFIED], research/02:72 |
| E-7 | Whole-line drop at anchor over 200, claim over 300, quote over 200 | literals in both parsers (`findings_v2.py:111,126,132,136`; v1 `findings.py:104,108,118` [UNVERIFIED]) | yes, through a constants module and one pre-parse repair step (the requirement "one policy before `parse_block`" is decided in synth-06 CO-6; the policy itself is C-06) | [CODE-VERIFIED] for v2 lines |
| E-8 | Union-find with a 3-line tolerance and no chain guard | v1 `same_defect` and `cluster` (`findings.py:367-407`, the 3 is an inline literal at `findings.py:377`) | no, engine-local; v2 has `SPAN_TOLERANCE` and a chained flag (`cluster.py:161-181` read; flag at `cluster.py:324,370` [UNVERIFIED]) | [CODE-VERIFIED] for v1 and for `same_defect_v2`; chain flag [UNVERIFIED] |
| E-9 | Fingerprints differ: v1 `sha256("v1\|section\|refs")[:16]` (`findings.py:340-343`); v2 `sha256("v2\|role\|path\|\|refs\|class")` full hex (`cluster.py:119-123`) | engine-local, each consistent with its own location type | no, and no need: a v1 fingerprint depends on a document section and a v2 one has no document text | [CODE-VERIFIED] |
| E-10 | Fail-open ledger: clearing by silence (`ledger.py:254-258`), one valid block of N passes (`ledger.py:150-157`) | v1 ledger only | n/a here: these are C-02 and C-03 and are fixed inside the one multi-reviewer ledger in the product whichever core shape wins; position A would rewrite the same lines | [CODE-VERIFIED] |
| E-11 | One bad line costs one finding in v1 (`ledger.py:135-138` keeps every parsed finding and records `block_ok` only) but one reviewer in v2 clustering (`cluster.py:256-257`) | engine behaviour | the repair step before `parse_block` removes the difference for both | [CODE-VERIFIED] for v1; v2 line [UNVERIFIED], research/02:118 |

Result of the table: of six verified cross-engine defects, two (E-6, E-7) and the cost difference of E-11 sit in shared helpers or in a function that runs before both parsers, so they are fixed once under B. E-8 and E-9 are consequences of the two location types, not duplicated bugs. E-10 is fixed once because only one ledger exists. B's real duplication is the second clusterer and the second location type with its own fingerprint, which is the price of keeping two location types.

### 3.3 No measurement says which location type reviewers produce reliably

| # | Fact | Source | Tag |
|---|---|---|---|
| E-12 | Anchor fidelity: luna quotes verbatim in 91.4 percent of anchors (363 of 397), the other models 98 to 100 percent; ember 860 of 878 (97.9 percent). | research/scope/04:155 (audit-B stats), COMBO-REPORT:294 | [UNVERIFIED] |
| E-13 | Citation precheck in E1: 1,047 citations checked, 510 flagged (48.7 percent); 472 of the flags are `not-in-snapshot` (92.5 percent), 7 `out-of-range`, 31 `quote-not-found`. The cause traced in one run is the orchestrator-built snapshot or `--root` argument, not reviewer error; 0 resolved citations in 7 of 15 combo runs. | research/10:194; research/07:49 (E1-F9) | [UNVERIFIED] |
| E-14 | No run compares core shapes; all three of synth-05 options A, B, C need the same verdict fixes and the same locator work; they differ only in where the engine boundary sits. | synth-05:101 | [UNVERIFIED] |

These facts cut both ways and B does not claim them as a win. E-12 says anchors are good but not perfect for one model; E-13 says citations looked bad but for a plumbing reason, so citation reliability is untested, not disproved. What B takes from them: because neither type is shown reliable enough to make the other redundant, B keeps both and lets the target kind choose.

### 3.4 Consumers outside the loop do not need a ledger today

| # | Fact | Source | Tag |
|---|---|---|---|
| E-15 | PR review needs one integer `line` per finding; `pr_submit` drops a finding without one (`is_groundable`, `fsm.py:364-372`); `citations[0].line_start` maps to `line`. The PR path has a pure core around ONE normalised `Finding` and no panel ledger. | research/13:61, 176 (P1) | [UNVERIFIED] |
| E-16 | The `/task` phase gate is already the master-loop shape (read-only lens reviewers, one fix agent, verification round, cap 3 reviews); replacing rf-qa starts by making this gate call a panel core, and the blockers are a mechanically read-only reviewer, a checklist output mode, per-slot lens and an agent-count rule (R1 to R3), none of which is a ledger-shape question. | research/13:145-149, 195-197 | [UNVERIFIED] |
| E-17 | Reflect has no finding ledger or rounds; its per-run state machine is the manifest. | research/01:150 | [UNVERIFIED] |

## 4. Invariants

### 4.1 Preserved

| Invariant | How B preserves it |
|---|---|
| INV-A (MEDIUM): contract 1.8.0 consumer-read names and the `merge_method` pair, byte-identical | B changes no `cli/reflect` file and no reflect field name. The only edit to the v2 kernel is importing shared constants, the repair step and the `refs_norm` list; none of them is a contract 1.8.0 field. The existing contract tests stay unchanged. |
| INV-B (HIGH in other slots): `derive_verdict` map and the 36-test matrix | `contract.py` and `test_verdict_mapping.py` are not in B's file set. |
| INV-C (HIGH): findings-v1 grammar, `review merge` unchanged, unknown keys accepted | The v1 parser, the merge command and the open unknown-key behaviour are untouched; E2 in-line `origin` keeps working (v1 and v2 accept it: research/02:48-55 [UNVERIFIED], not re-run by me; v2 `check_finding` shows only `calibrated_confidence` rejected in lines 96-97 [CODE-VERIFIED]; lines 174-187 of that function not read). |
| INV-D (HIGH): `review-ledger/1`, the `ledger` command group, exit codes 0/10/11, `merge` exit 0 | Untouched. The 2.3 guard changes only the failure for an input that cannot occur today in the shipped flow (a v2 finding fed to the v1 merge): a typed `LedgerError` instead of a traceback; the CLI maps `LedgerError` from `merge` to exit 1 (research/03:73 [UNVERIFIED]). |
| INV-E (MEDIUM): `pr_submit.Finding`, `Severity`, FSM, no `gh` or `git` in the core | The adapter is pure and lives on the consumer side; nothing in the contract names `gh`, `git` or a repository. |
| INV-F: installed-path rule | The contract is Python package code reached through the `superclaude` CLI; B adds no primitive text that names `src/superclaude/...`. |
| INV-J: S1 to S5 (binary blocking, Medium non-blocking, 2 fix cycles) | B carries no cap or severity rule in the contract. |
| INV-L: shadow mode changes no verdict | Not touched. |
| INV-N: plugin mirror parity | The v1 brief, `spec-panel.md` loop bullets and their mirrors are unchanged. |

### 4.2 Endangered or left open

1. INV-K (MEDIUM): reserved contract-constant names under `cli/`; a duplicate fails `make lint-architecture` Check 11 (synth-05:74, citing research/18 F6 [UNVERIFIED]). A new shared constants module must choose names that do not collide. Watch item for the plan, checked by running the gate.
2. INV-I (HIGH): B does not improve it. The fail-open v1 ledger (E-10) stays as it is until C-02 and C-03 land inside that engine. Under B that work is smaller (one engine, pins already identified in research/03 section 2), but B is not the reason INV-I is fixed.
3. INV-C (HIGH), the repair step: any pre-parse repair changes what reaches `parse_block`. This is not specific to B (A needs the same step), but B must prove byte-equal parser output on already-valid lines. Covered by test 5.1.
4. Engine-count cost: two clusterers, two fingerprints and two location types remain to be maintained, documented and explained to every new module author. This is a cost, not an invariant.

## 5. The test or measurement that would show B right or wrong

### 5.1 Conformance suite (shows the contract is real)

A golden set of about 20 finding lines: anchor-only, citation-only, both, a `T01.02` ref, an over-limit anchor, an over-limit claim, an `origin` key, a `calibrated_confidence` key, a 17-character id. Run each through the shared constants, the repair step, `refs_norm` and both parsers. B holds if: the constants are one object imported by both parsers; `refs_norm` output is identical for both engines; on lines that are already valid, parser output with the repair step equals output without it; the projection view is total over every valid line of both engines with no engine-specific escape hatch. B fails if the projection needs more than a small fixed number of engine-specific fields to stay lossless.

### 5.2 Boundary test

A citation-only finding passed to `merge_round` raises `LedgerError` that names the finding id, and the ledger file is unchanged (the same shape as the existing no-valid-block refusal tests, `tests/review/test_review_ledger.py:345-373` [UNVERIFIED], research/03:148).

### 5.3 Location-type reliability measurement (decides between per-target locator and one locator)

Same reviewers, same three targets (a spec document, a tasklist with source paths, a code diff), after the E1-F9 snapshot plumbing is fixed. Per arm record: anchor locate rate (`anchor_status == "found"`), anchor ambiguity rate (`anchor_ambiguous`), citation resolved rate (`status == "resolved"`), and blocking findings lost to the parser. Pre-register the rule before the first run:
- B is supported if anchors locate at least as often as citations resolve on the document target and citations resolve at least as often as anchors locate on the code target. Per-target locators are then the evidence-supported shape.
- A is supported if citations resolve at least as often as anchors locate on the document target as well, because then one location type serves every target and the v1 anchor engine has no remaining advantage.

### 5.4 Convergence trigger (the condition under which B hands over to A's work)

B is wrong, and the locator-agnostic `annotate` plus citation-keyed rows must be built, when the first of these occurs:
1. a module needs re-review rounds over citation-located findings from several reviewers (candidates: an rf-qa replacement over code, the tasklist post gate over source paths);
2. two or more verified defects in one quarter need the same non-helper edit in both clusterers or both parsers;
3. test 5.3 shows citations at least as reliable as anchors on documents.

The numbers are a proposal for the debate, not findings; no recorded run supplies a threshold.

## 6. Effect on future PR code review and rf-qa replacement

| Use | Effect under B | Evidence | Tag |
|---|---|---|---|
| PR code review | Works through the v2 engine and a pure adapter to `pr_submit.Finding`; no ledger is needed because `pr_submit` owns remap, verify, route, round cap and push. The blockers that remain are vocabulary, not core shape: module-declared category, lens and severity sets (P2, P3, P4, M2), passthrough fields `in_diff`, `confidence`, `original_line`, `reviewer` (M3), and a "completion" rule for a local panel (research/13 P6). | research/13:176-181, 214-216 | [UNVERIFIED] |
| rf-qa replacement | Starts at the `/task` phase gate with reviewers that are mechanically read-only, a checklist mode with the computed confidence gate (R2), per-slot lens plus an agent-count floor (R3), and a replay oracle built first (R10; the gate has about 23 files of static pins and no behavioural oracle). Re-review rounds in the rf-qa Fix Cycle (steps 1 to 5) can use the v1 ledger when the target is a document. | research/13:195-204, 153-163; `spec-panel.md:262` shows the loop's rf-qa coupling is soft | [UNVERIFIED] |
| Spec review | No change in shape; the loop keeps its pinned bullets and the single multi-reviewer ledger. | E-4 | [CODE-VERIFIED] for the pin count |
| What B costs these uses | If a future PR or rf-qa design needs a multi-reviewer ledger over `file:line` findings, B leaves that to be built later (trigger 5.4). Research/13 M1 asks the core to expose a locator-agnostic `annotate` and citation-keyed rows now because it is cheap before consumers pin it; B accepts the retrofit risk in exchange for not rewriting the pinned v1 path before any consumer needs it. | research/13:214 | [UNVERIFIED] |

## 7. Strongest objection and the answer

Objection (the strongest form of position A's case): B fixes the same class of defect in two places for as long as both engines live, every new module must choose an engine, and the first module that needs both file:line locations and a multi-reviewer re-review ledger (rf-qa on code, tasklist with source paths) forces the locator-agnostic ledger anyway, at a later date when more tests pin the v1 path and more consumers read `anchor`. The core never becomes one pipeline, so unknown-key policy, fingerprint, blocking rule and run record stay four decisions with two answers each. research/13 M1 says the exposure is cheap now and expensive to retrofit.

Answer:
1. The duplicated-defect claim is smaller than it looks. Section 3.2 shows the two defects that appear in both parsers are in shared helpers or in a step that runs before both parsers, so they are fixed once. The differences that remain (fingerprint, tolerance, chain guard) follow from the location type and are not bugs to fix twice. E-5 shows no duplicate cost has been paid yet; the cost is a projection.
2. The forcing function is observable and cheap to detect. B names its trigger (5.4) and its guard (2.3), so "the first consumer that needs a citation ledger" arrives as a failing typed error, not a silent loss. Position A pays now for a case no consumer has shown: PR review needs no ledger (E-15), reflect has no ledger (E-17), and the `/task` gate's blockers are not about a ledger (E-16).
3. The retrofit argument is weaker than the rewrite argument. Rewriting `annotate` and the ledger rows now means changing the one path that is shipped, pinned in tests (E-4) and described in the brief, in order to carry a location type no run has shown reliable (E-12, E-13). Deferring leaves the v1 path pinned as it is and adds work only when a consumer pays for it; the pins that exist today (six of eight tests that pin ledger behaviour as intended, research/03:151 [UNVERIFIED]) already have to be rewritten once for C-02 and C-03, and B does not add a second rewrite on top.
4. B does not close A. The contract adopts the shared constants, the repair step and the `refs_norm` list, so a later move of the v1 loop to a profile of the v2 kernel starts from a shared base. What B gives up is an earlier, cheaper start on that move.
5. What B does not answer: it does not say how many module authors must learn two location types, and it does not say who decides, per new module, which engine fits. That is an owner decision, together with the open question whether the v2 fingerprint's line-insensitivity is intended (GQ-023).

Status: Complete
