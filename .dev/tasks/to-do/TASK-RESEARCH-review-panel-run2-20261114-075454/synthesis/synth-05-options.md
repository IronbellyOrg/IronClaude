# Synthesis 05: Options Analysis

**Date:** 2026-11-14
**Status:** Complete
**Report sections produced:** 6.1 to 6.11 (one block per decision axis) of the Technical Research Report on the unified central Review Panel (run 2).
**Research question context:** which ONE unified central Review Panel design captures all the value of E1, E2 and E3 and keeps future PR code review and rf-qa replacement unblocked.
**Rule of this file:** options and evidence only. No winner is picked here (the recommendation is Section 7). Where the evidence cannot separate options the axis is marked `UNDECIDABLE-BY-EVIDENCE` with the reason so the conflict log can route it to a debate. The adjudicated winners of the closed axes are recorded in one place only, the section "Adjudicated winners by axis" before "Interactions between axes" (added by the adjudication fold); no option text above that section was changed.

## Reading guide

| Item | Meaning |
|---|---|
| Citation keys | `R01` to `R18` = `research/01-*.md` to `research/18-*.md` (R01 overlap matrix, R02 finding contract, R03 merge/ledger/verdict, R04 dispatch and tiers, R05 input and brief, R06 reflect two engines, R07 E1 evidence, R08 E2 evidence, R09 collaboration, R10 process redesign, R11 tasklist/workflow consumers, R12 spec-review consumers, R13 PR review and rf-qa, R14 E3 variants, R15 telemetry/run record, R16 evaluation governance, R17 defect register, R18 repo constraints). `W01` to `W04` = `research/web-01-*.md` to `web-04-*.md` (external context with source URLs). `RN` = `research/research-notes.md` (Decision axes). |
| Line cites | `path:line` is at HEAD `50d4d2b9d` (branch `ironbelly/shadow-runs`) unless prefixed `E2@6c09843:` (E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`, read through git only). A cite is copied from a research file that tagged the claim [CODE-VERIFIED]; the research file is named beside it. |
| Fact status | Only claims the research files tagged [CODE-VERIFIED] (read, re-run or recomputed) are stated as fact. [CODE-CONTRADICTED] claims appear only in corrected form (list in "Corrected claims" at the end). [UNVERIFIED] claims are marked `(OQ-n)`, are listed in "Open questions" at the end, and never carry a pro, a con or an option. |
| Effort (XS, S, M, L, XL) | Qualitative size of the option as the evidence shows it (modules, pinned tests, primitives it touches). An option attribute only. |
| Risk (Low, Medium, High) | Per-option attribute: how likely, on the evidence, that the option leaves a verified defect in the path of a stated use case or breaks a pinned behaviour. Not a risk register. |
| "Blocks future PR review or rf-qa replacement" | yes / no / how: whether the option, as evidenced, keeps the exposures in R13 section 8 (M1 to M14: locator-agnostic finding, module-declared vocabularies, per-slot lens, mechanically read-only reviewers, separate reviser, module caps, one reviewer-failed finding, checklist mode, purity, adapter spec, replay fixture, plugin decision) reachable later. |
| Web evidence | External context only (W01 to W04). It never overrides a code-verified fact; most transfer from QA, NLI, SQL or benchmark tasks to PR code review is `[UNVERIFIED]`. |

## 6.1 Core shape

**Description:** which structure carries the unified Review Panel. The four candidates come from RN "Decision axes": (A) the v2 kernel as the core with the v1 loop as a thin module; (B) the v1 package as the core with reflect as a module; (C) a thin shared contract with per-module engines; (D) fix the harness and the two parsers only and defer unification.

**How it works:**

| Option | Mechanism | What stays outside the core |
|---|---|---|
| A: v2 kernel core | `findings_v2.py` + `cluster.py` + `verify_cmd.py` + `manifest.py` + `panel.py` (with the `reflect-*` profile) become the pipeline every module uses; the v1 loop (`findings.py` anchors, `ledger.py`, `merge_cmd.py`, the spec-panel Review Loop text) becomes a module that supplies its brief, anchor locator and ledger status machine. | spec brief, anchor locator, v1 ledger statuses, reflect contract 1.8.0 consumers |
| B: v1 package core | `findings.py`, `ledger.py`, `merge_cmd.py`, `panel.py` stay the core; reflect becomes a module that supplies its lens, templates, contract 1.8.0 fields and v2-only extras. | reflect grammar extras (`citations`, `lens`, `deviation_class`, `coverage_rows`), cluster/manifest/verify on the reflect side |
| C: thin shared contract | The core is a contract: finding schema with module-declared vocabularies, id and reference grammar, hash and fingerprint rules, run record, eval harness. Engines stay per module (v1 loop and ledger, reflect shell, PR adapter). | every engine |
| D: fix and defer | Only the harness fixes (H1 to H4), the whole-finding drop D1 in both parsers and brief item B-1 are changed; no shared core is built. | everything else |

**Shared facts that bear on all four options (R-cited, all [CODE-VERIFIED]):**

| Fact | Source |
|---|---|
| E2 changed no product code at any commit; E2 = data, harness and designs. A unified core merges E1 and E3 code and imports E2 evidence. | R01 section 1.1 |
| `findings.py`, `ledger.py`, `merge_cmd.py` are byte-identical in E1 HEAD, E2 tip and master, so E2's drop-and-warn evidence applies to E1's code. | RN pattern 2; R16 section 5.2 |
| v1 and v2 share only the block container, `refs_norm`, `_ID`, `_check_flat` and `panel.py`; a v2 citation-only finding crashes the v1 ledger path (`KeyError: 'anchor'`, `findings.py:349`, called from `ledger.py:136`). | R01 section 3 probe P-a |
| E1 (v2 kernel) is a superset of E3s (v1) for panel resolution and the line grammar, and conflicts with it on location type, blocking rule, fingerprint, verdict model and run record (C-1 to C-6 in R01 section 5). | R01 section 4 key takeaways |
| `cli/review` and `cli/reflect` are independent packages at HEAD (no import in either direction in `src/`). | R18 section 6.1 |
| Reflect has two Tier-2 engines that share only `contract.py` (`derive_verdict`, `parse_contract`). | R06 section 7 |
| The installed-only E3 variants re-implement the loop in stdlib-only scripts (no import of `cli/review`, no shared schema string or grammar). | R03 section 3.1 |
| The CLI ledger is the only multi-reviewer merge in the codebase; the variants are single-reviewer loops. | R03 section 3 key takeaways |

### Option A: v2 kernel as the core, v1 loop as a thin module

| Aspect | Assessment |
|---|---|
| Effort | L (basis: the ledger and merge path must accept citation-only findings; `ledger.merge_round` calls `fnd.annotate` on every parsed finding, `ledger.py:127-138`, and `annotate` does `locate(text, finding["anchor"])` with no `.get`, `findings.py:346-349`; R01 P-a; R13 M1) |
| Risk | Medium (basis: six of eight pins read in R03 section 2 encode the fail-open ledger behaviour as intended and must be rewritten with any verdict fix; the v1 loop wording is pinned in both `src` and plugin copies, R12 section 2.1) |
| Reuse of existing code | `findings_v2.py` (304 lines; parser already accepts `anchor` OR `citations`, `:122-125`), `cluster.py` (487), `verify_cmd.py` (184), `manifest.py` (534), `panel.py` (707, `validate_reflect_profile` at `:80`), `card_convert.py` (517), six `reflect-*` templates; `findings.py`, `ledger.py`, `merge_cmd.py` reused by the loop module (R18 section 9 sizes; R01 section 2) |
| Files and systems affected | `src/superclaude/cli/review/{findings,findings_v2,ledger,merge_cmd,cluster,panel}.py`; `tests/review/` (19 modules, several pin defects D-1, D-2, D-3, D-5, D-6, D-11); `src/superclaude/rules/prompts/document_review_loop_prompts.md`; `src/superclaude/commands/spec-panel.md` and its plugin copy; `tests/skills/test_review_severity_mapping.py`, `test_review_brief_placement.py`, `test_spec_panel_review_loop.py` (R12 section 2.1) |
| Pros | The kernel was built for reflect and already has the pieces a panel needs: `reflect-*` templates and profile validation (`panel.py:80-136`), run-state manifest (`manifest.py:38-54`), chain-aware clustering with `cluster_agreement` (`cluster.py:119-181`), advisory citation precheck (`verify_cmd.py:11-12`), per-lens primary-role table (`cluster.py:67-71`) (R01 rows 4, 5, 8, 12; R05 Unit 2). v2 already represents file:line locations with roles `plan/spec/source/test/diff/artifact` (`findings_v2.py:35`, `:59-81`) (R13 section 6). The sidecar `{assigned, observed}` container exists and is validated (`findings_v2.py:166-176`, `:196-212`) (R10 Unit 4). |
| Cons | v2 has no ledger, rounds or reviser (R01 row 7); one bad line makes a v2 block `invalid` and `cluster` drops the whole reviewer (`cluster.py:256-257`, `:416`; R02 section 5.3); the v2 fingerprint ignores line numbers (`cluster.py:119-123`; R02 section 4.3); the v2 parser rejects `calibrated_confidence` and `prior` lines the v1 loop needs (`findings_v2.py:96-97`, `:279-283`; R01 C-1); category, lens and severity sets are closed to the spec and reflect values (`findings_v2.py:36`, `:109-110`; R13 P2, P3); `refs_norm` misses tasklist ids `T01.02` in both parsers (`findings.py:29`; R02 section 4). |

### Option B: v1 package as the core, reflect as a module

| Aspect | Assessment |
|---|---|
| Effort | M to L; rated M (basis: the loop engine, ledger, merge, spec brief and pins already exist; the work is a reflect adapter plus whatever v1 must gain to carry file:line locations, which is the same locator work as option A, R13 M1) |
| Risk | Medium (basis: the reflect shadow path consumes `findings-v2`, `cluster`, `verify-citations`, `manifest` through SKILL.md prose at `SKILL.md:340-349`; moving them behind a module boundary touches contract 1.8.0 pins and the 36-test verdict matrix, R06 section 8(a), R18 F8, F9) |
| Reuse of existing code | v1 `findings.py` (457), `ledger.py` (494), `merge_cmd.py` (118), `ledger_cmd.py` (137); shipped loop prompts and `spec-panel.md` Review Loop; `review-ledger/1` is named in the brief, tests, CLI group and schema string (R10 Unit 3) |
| Files and systems affected | v1 files above; reflect adapter in `src/superclaude/skills/sc-reflect-protocol/` (edit fence: `tests/cli/reflect/test_shadow_skill_contract.py:42-98`); `src/superclaude/cli/reflect/panel_lint.py`; `scripts/reflect_*.py` which import the v2 kernel (R12 section 7) |
| Pros | The shipped consumer is spec-panel (loop bullets identical in src and plugin copies and pinned by static tests, R12 sections 1.3, 2.1); E2's merge-drop evidence is about exactly this code (R08 section 5); the v1 ledger is the only multi-reviewer merge (R03 section 3). The `blocking` boolean plus CRITICAL/MAJOR/MINOR is the pair the repo's canonical rule already uses (R12 section 2.1, `pragmatic.md:224-231`). |
| Cons | v1 has one location type: quoted `anchor` 12..200 characters, required (`findings.py:104-106`); a PR or reflect finding with file:line only cannot enter it (R13 P1, M1). The merge fails open on a partial panel (`ledger.py:150-157`; R03 section 1.2) and clears rows by absence (`ledger.py:254-258`; R03 section 1.1). Tasklist ids are not refs (`findings.py:29`; R02 section 4.2). A reflect module would still need v2-only fields (`lens`, `deviation_class`, `coverage_rows`, `reflect_category`, `findings_v2.py:84-187`), so the v1 grammar must grow toward v2 or the reflect module keeps its own parser. |

### Option C: thin shared contract, per-module engines

| Aspect | Assessment |
|---|---|
| Effort | M (basis: contract-level work only; engines are not merged; R13 section 8 lists the exposures as interface specification, "no code written") |
| Risk | Medium (basis: contract-constant names are reserved under `cli/` and a duplicate fails `make lint-architecture` Check 11, R18 F6; the contract is versioned once consumers pin it, R13 section 8 header) |
| Reuse of existing code | `_ID` and `_check_flat` (`findings.py:26`, `:79-87`); `refs_norm` as a per-module pattern list (R05 Unit 8); `PRIMARY_ROLES` table pattern (`cluster.py:67-71`); `contract.derive_verdict` as a pure verdict shell (R03 section 4.2); `review-telemetry/1` as cross-run store (R15 section 8.5); the E2 harness files as evaluation inputs (R16 Part 1) |
| Files and systems affected | a new contract surface in `src/superclaude/cli/review/` (home already exists, 25 tracked files with optional-module registration, `__init__.py:14-36`; R18 section 9); the telemetry and manifest modules; `tests/review/`; modules keep their own engines (`cli/reflect/`, `pr_submit/`, `ledger.py`) |
| Pros | Few cells are identical across E1, E2, E3 (id regex, findings-v1 grammar, cap constant 3, E2's unchanged use of merge; R01 section 4 key takeaways), so a contract captures what is already shared without forcing an engine merge. Twelve spec-shaped hard-codings are "one fact, two copies" a contract removes by generation (R05 Unit 7). Every consumer except spec-panel and the reflect shadow path has its own review path that never touches `cli/review` (R12 section 7), so per-module engines match today's reach. |
| Cons | Duplicates survive: two ledgers with different statuses (C-5; R03 section 4.1), two clustering implementations (`findings.cluster` and `cluster_v2`; R01 row 4), two verdict models (R03 section 4.2), reflect's two engines (R06). The contract only helps modules that adopt it; the engines' verified defects (D-1, D-2, D-11, D-13) stay engine-local (R03). |

### Option D: fix the harness and the two parsers only, defer unification

| Aspect | Assessment |
|---|---|
| Effort | S (basis: H1 to H4, D1 in `findings.py` and `findings_v2.py`, B-1; R09 section 5, R02 section 5) |
| Risk | Low for breakage; Medium for leaving verified defects in the path of the use cases (basis: the items listed under Cons are reproduced at HEAD, R01 probes, R03 section 1) |
| Reuse of existing code | `findings.py:104,118` and `findings_v2.py:80,111,126,132,136` (the limit sites); `card_convert.py:199-201` (the one existing truncation); `document_review_loop_prompts.md:15-21,60` (brief); `refs/reviewer-spec.md:39` |
| Files and systems affected | `findings.py`, `findings_v2.py`, the parse step before `ledger.merge_round`, the loop and reflect briefs, `tests/review/test_review_findings*.py`; E2 harness files are not in HEAD (R16 section 5.1) |
| Pros | Smallest change on the evidenced largest loss: 92 finding lines dropped, 49 of them blocking, 3 verdicts flipped to PASS plus 5 total-loss merges (R08 section 5); truncation addresses up to 88 of 92 lines and 48 of 49 blocking lines (R02 section 5.2). H1 and H2 are the items R09 section 5 finds independent of collaboration. Nothing in B-1 to B-5, B-7 is fixed at HEAD in a shipped file (R05 Unit 4). |
| Cons | Leaves open, all verified at HEAD: a citation-only finding crashes the v1 ledger path (R01 P-a); one valid reviewer of N passes the round (D-2, `ledger.py:150-157`); rows clear by silence (D-1); a human `defer` rewrites the stored verdict (D-11); tasklist ids are not refs (R02 section 4); two ledgers and four run-record formats (R01 section 5; R15 section 1.3); the served model is recorded nowhere in product code (R04 section 4.2). The location-type exposure (M1) and the vocabulary exposures (M2, M3) are not provided (R13 section 8). |

### Options comparison table (6.1)

| Criterion | A: v2 kernel core | B: v1 package core | C: thin shared contract | D: fix parsers and harness only |
|---|---|---|---|---|
| Maintainability | One pipeline for loop and reflect; v1 stays as a module with its own statuses. Two ledgers collapse only if the loop module adopts the kernel's (R03 section 4.1). | One grammar and one ledger; reflect keeps a v2 extension, so two grammars remain unless v1 grows (R01 C-1 to C-4). | Contract removes copied constants (R05 Unit 7); engines and their defects stay duplicated (R03, R06). | Least new code; every duplicate and defect above remains. |
| Integration complexity | High: ledger/merge/annotate become locator-agnostic (R13 M1) and loop pins are rewritten (R03 section 2). | Medium: reflect adapter plus v1 location growth; reflect edit fence (R18 F8). | Medium: each module adopts the contract at its own pace; versioning discipline (R18 F6). | Low. |
| Reuse potential | Highest for kernel pieces (manifest, cluster, verify, reflect profile) (R01 rows 4, 5, 8, 12). | Highest for shipped v1 loop, ledger and pins (R10 Unit 3; R12 section 2). | Highest for constants, verdict shell and run-record adapter (R15 section 8). | Parsers and briefs only. |
| Evidence strength | Code-verified assets and blockers (R01 P-a to P-e, R02 section 5.3, R03 section 1); no run compares core shapes. | Code-verified merge defects and E2 merge evidence on the same code (R08 section 5); no run compares core shapes. | Code-verified overlap census (R01 section 4); the contract contents come from R13 section 8 (interface specification, not exercised code). | Strongest: numbers recomputed for the 92/49/3 loss (R08 section 5) and the limits reproduced (R01 P-c). |
| Blocks future PR review or rf-qa replacement | Partly: file:line is representable in v2 but the ledger path still needs `anchor` (R13 M1, P-a); category and lens sets closed (P2, P3) until made module-declared. | Yes for the ledger path: `anchor` required (`findings.py:104-106`), no file:line field in v1; same P2, P3 blockers. PR can still enter through an adapter to `pr_submit.Finding` (R13 P1). | No if the contract carries M1 to M4; the engines per module still need their own work (R13 R1 to R3). | Does not unblock: M1 to M4 absent; PR adapter route stays open (R13 P1); rf-qa still needs a read-only reviewer and a checklist mode (R13 R1, R2). |

**Axis status: UNDECIDABLE-BY-EVIDENCE between A, B and C.** Reason: no run compares core shapes; all three need the same locator-agnostic annotate (R13 M1) and the same verdict fixes (R03 section 5); they differ in where the engine boundary sits, which R01 gap 9 and R02 gaps 11 and 12 list as design questions the code does not answer. What the evidence does decide: (1) neither reflect engine is a safe base alone (R06 section 8(d)); (2) option D leaves the verified defects listed under its Cons in place, so D defers rather than unifies. Whether deferring is acceptable is an owner scope decision.

## 6.2 Finding contract

**Description:** the line-level record every reviewer returns and every downstream step (merge, cluster, ledger, verdict, export) reads: location type, id and reference grammar, closed vocabularies (category, severity, lens), unknown-key policy, and what a violation costs. The candidates in RN "Decision axes" are v1 anchor quotes, v2 `path:line` citations, the reflect deviation table, variant ledger rows and E2 `panel-msg/1` with `origin`.

**How it works (the contracts that exist at HEAD or in E2/E3; all [CODE-VERIFIED] unless marked):**

| Contract | Location type | Vocabularies | Unknown keys | Violation costs | Source |
|---|---|---|---|---|---|
| `findings-v1` (`findings.py`) | quoted `anchor` 12..200 characters, required; `anchor2`; `refs` at most 8 | severity CRITICAL/MAJOR/MINOR; 6 categories (`findings.py:14-22`); id `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` (`:26`) | accepted and carried (`parse_block` appends the whole object, `:193-195`) | the line is dropped, the block becomes `ok: false`, other lines are kept in the ledger (`ledger.py:135-138`) | R02 sections 1, 9 |
| `findings-v2` (`findings_v2.py`) | `citations[{role, path, line_start, line_end, quote?}]` 1..8, or `anchor`; roles plan, spec, source, test, diff, artifact (`:35`, `:59-81`, `:122-134`) | same severity and categories by import (`:15-22`); lens spec/reflect-pre/reflect-post (`:36`); `reflect_category`, `deviation_class`, `channel`, `coverage_rows`, `self_confidence` | accepted except `calibrated_confidence` (`:96-97`) | line dropped, block `invalid`, `cluster` ignores the whole reviewer (`cluster.py:256-257`) | R02 sections 2, 5.3 |
| Reflect card (E1 shadow) | markdown card with `persona:`, `model_class:`, `model:` headers, one `findings-v2` block, fenced `calibration:` yaml outside the line | as v2 | n/a | `card_convert` truncates claims to 297 + `...`, never builds a quote (`card_convert.py:199-201`) | R02 section 6 |
| `reflect-reviewer` agent output | markdown Deviations table, `file:line` locations, severity HIGH/MEDIUM/LOW, 4 deviation categories (`reflect-reviewer.md:69-99`) | free-form `persona_lens` in the brief | n/a | n/a | R13 section 2.2 |
| Installed variants | `review_ledger.py` rows `{grade, rule, wrong_outcome, anchor, finding, label}` (`:64`); `diffgate.py` key=value lines (`:328-339`); `stoprule.py` sealed claims (`:306-335`) | own grades, own id spaces (`R<n>`, `R<n>.<m>`) | rejected in `review_ledger.py:809-817` and `diffgate.py:507-508`; `stoprule.py` not found [UNVERIFIED] (OQ-1) | whole input refused, nothing written (`E-SCHEMA`) | R02 section 7 |
| E2 `panel-msg/1` | message, not a finding: `anchor` 12..200 exact substring, `items` at most 8 paths, 600-byte cap | kinds move, fact, challenge, card, coverage | rejected | message refused | R02 section 8 |
| `pr_submit.Finding` | `path`, one integer `line`, `in_diff`, `original_line` | 18 categories, 5 severities (`models.py:106-113`, `severity_router.py:34-53`) | n/a (dataclass) | a finding with no positive integer line is dropped (`fsm.py:364-372`) | R13 sections 1.2, 1.3, 1.5 |

Facts that bear on every option: the two parsers cannot feed each other's downstream code (v2 citation-only finding crashes v1 `annotate`; a v1 anchor-only finding parses in v2 but gets no fingerprint and only forms singleton clusters, `cluster.py:133-147`) (R01 section 3). `T01.02` is a legal finding id but not a reference token in `findings.py:29` or `telemetry.py:23`; the finding is kept and the ref silently ignored (R02 section 4). The unknown-key behaviour of `origin` is "accepted and inert": no `cli/review` module reads it and the ledger member record keeps only round, reviewer id, finding id and blocking (`ledger.py:172-202`) (R02 sections 3, 8). `origin` already names two other things in two E3 variants (R02 section 7). Medium has at least six uses and seven severity vocabularies are in the repo (R12 sections 2.2, 3); the canonical repo rule is binary blocking/minor with a 2-fix-cycle cap, copied into ten primitives and pinned by static tests (`pragmatic.md:224-231`; `tests/skills/test_review_severity_rule.py:181-210`) (R12 section 2.1).

### Option 1: keep two grammars and add adapters (status quo plus)

| Aspect | Assessment |
|---|---|
| Effort | XS (basis: no parser change; adapters only, R13 M11, P1) |
| Risk | Medium (basis: the verified incompatibilities stay: P-a, P-b, C-2, C-4 in R01 section 5) |
| Reuse of existing code | both parsers as they are; `card_convert.py`; `pr_submit.Finding` adapter reads `citations[0].line_start` as `line` (R13 P1) |
| Files and systems affected | adapter modules per consumer; no change to `findings.py`, `findings_v2.py`, `ledger.py`; no new pinned behaviour |
| Pros | No pinned test or contract changes (R12 section 2.1; R06 section 8(a)). Open unknown keys let E2's in-line `origin` tags work today (R02 section 3). PR review enters through its own `Finding` without a ledger (R13 P1: SOFT). |
| Cons | A line valid in v1 can be invalid in v2 (`calibrated_confidence`, probe P-b); blocking rules differ (`findings_v2.py:161-162` forces `blocking == (severity != MINOR)` when `reflect_category` is set; spec text lets MAJOR be non-blocking, `spec-panel.md:259`) (R01 C-2); fingerprints differ (`sha256("v1|section|refs")[:16]` vs `sha256("v2|role|path||refs|class")`) (R01 C-4); the whole-line drop and the `T01.02` gap exist in both parsers (R01 P-c, P-d); the ledger path cannot take a citation-only finding (R13 M1). |

### Option 2: one open superset grammar, vocabularies declared by each module

| Aspect | Assessment |
|---|---|
| Effort | M (basis: R13 M1 to M3 and R05 Unit 8: location list with optional anchor and a locator-agnostic `annotate`, module-declared category/lens/severity sets, passthrough fields, per-module reference patterns) |
| Risk | Medium (basis: tests pin the closed sets and the limits; one fact has two copies today, `findings.py:29` and `telemetry.py:23`, R05 Unit 7) |
| Reuse of existing code | `findings_v2.check_finding` structure (`:84-187`), `_check_citation` (`:59-81`), the `REFLECT_CATEGORIES` mapping onto the six categories (`:41-48`), the `PRIMARY_ROLES` table (`cluster.py:67-71`), `refs_norm` as a pattern list (`findings.py:321-337`) |
| Files and systems affected | `findings.py`, `findings_v2.py`, `ledger.py` (locator-agnostic annotate, citation-keyed rows), `cluster.py`, `telemetry.py` (`_ID_TOKEN`), briefs, `tests/review/test_review_findings*.py`, `test_review_cluster.py`, `test_review_card_convert.py` |
| Pros | Both existing grammars become projections of one record; v2 already accepts `anchor` OR `citations` (`findings_v2.py:122-125`). The pair CRITICAL/MAJOR/MINOR plus `blocking` is already the schema both E3 (v1) and E1 (v2) validate; "Medium" has no schema value in `cli/review` (only `card_convert.py` words), so a module label map avoids M1 to M6 collisions (R12 sections 2.2, 3, 8). Unknown keys stay accepted, so E2 `origin` works unchanged (R02 section 3). |
| Cons | A later whitelist would be a breaking change to every E2 tool that tags lines (R02 section 3 key takeaways). Carried keys stay inert unless the ledger member record is extended (`ledger.py:172-202`; R02 section 8). `origin` collides with two E3 variant meanings if variants fold (R02 section 7). The reflect lens keeps a stricter blocking rule (`findings_v2.py:161-162`), so the blocking rule must become a module or lens property, not a constant (R12 section 8 E-b). Module label maps are lossy in both directions (6 spec categories vs 18 PR categories; R12 section 2.3). |

### Option 3: one closed, versioned contract with a registered extension namespace

| Aspect | Assessment |
|---|---|
| Effort | L (basis: new schema id, key whitelist, validators, migration of every producer; R15 section 8.3 sketches `ext{<module>}` with typed per-module counters, a design derived from evidence, not code) |
| Risk | Medium (basis: breaks E2's in-line tags and the research-time tolerance of extra keys; whole-input refusal changes the cost of one bad key, R02 section 9) |
| Reuse of existing code | the variants' reject-unknown-keys patterns (`review_ledger.py:809-817`, `diffgate.py:507-508`); `panel-msg/1` per-kind key tables (R02 section 8, `merged-requirements.md:204-226` as requirement text); `findings_v2` per-field validators |
| Files and systems affected | new schema module in `cli/review/`; every producer (briefs, `card_convert.py`, E2-style tag tools); `ledger.py`; telemetry validators (value types are unchecked outside `context`, `telemetry.py:213-225`; R15 section 1.4) |
| Pros | The record projects onto export formats: SARIF (`ruleId`, relative path, `region.startLine`, fingerprint), reviewdog rdjson (path, range, severity, code) and the GitHub review `comments[]` fields (`path`, `line`, `side`, `commit_id`) (W04 sections 1 to 3 and 6; external, https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html, https://github.com/reviewdog/reviewdog/blob/master/proto/rdf/README.md, https://docs.github.com/rest/pulls/comments); W04 recommends keeping confidence off the finding, which matches v2 rejecting `calibrated_confidence` in the line and keeping calibration in a card sidecar (`findings_v2.py:96-97`, `cluster_cmd.py:31-47`; R02 section 6.1). Type-checked group values make the telemetry "no document text" promise enforceable (R15 section 1.4). |
| Cons | Breaks every tool that adds keys today (R02 section 3). The E3 variants split on this policy (ledger and diffgate reject, stoprule not found, findings-v1/v2 accept), so there is no single precedent (R02 section 9). Whole-input refusal for one bad key is the opposite of drop-the-line and compounds the 49 blocking findings lost unless a repair policy (6.3) runs first. W04 itself judges full SARIF too large to be the internal format (external, researcher judgement). |

### Sub-decision 6.2.b: input and brief contract (what the reviewer is told and given)

| Option | Mechanism | Evidence for | Evidence against | Effort / Risk |
|---|---|---|---|---|
| (a) per-module briefs as today | five brief families deliver input four ways: path in prose, sandbox copy, inline hunks, inline paste (R05 Unit 6) | each family is pinned or in use; reflect brief already states roles by section (`reviewer-spec.md:35-74`) | the loop brief has five placeholders and no driving-document role (`document_review_loop_prompts.md:15-21`); the code-driven reflect engine reviews a tasklist without the spec (`ensemble.py:619-630`, `runner.py:471-472`); B-1 to B-5, B-7 are open at HEAD (R05 Unit 4) | XS / Medium |
| (b) core brief assembler with an input manifest by role | ordered roles `{role, path, sha256, required, inline|by-path}`; limits and categories generated from parser constants; per-module grading and heading blocks (R05 Unit 8) | roles already exist in v2 (`findings_v2.py:35`); four of twelve hard-codings are "one fact, two copies" (R05 Unit 7); `card_convert.py` resolves roles by file name `source.md` and `<id>.md` (`:15-18`, `:466-470`), a fragile bridge | not exercised anywhere; brief placement is test-pinned (`test_review_brief_placement.py:66-103`) and primitives may not name `src/superclaude/` paths (R18 section 5) | M / Medium |
| (c) patch the loop brief only | name the driving document, state parser limits, fix the blocking sentence (B-1 to B-5, B-7) | all open brief items are brief-text items (R05 Unit 4 key takeaways); thinking-budget and source-reading effects are unproven (R05 Unit 5, R08 G6) | does not give the tasklist fidelity prompt (HIGH/MEDIUM/LOW, `cli/tasklist/prompts.py`) or the code-driven reflect engine a role contract (R05 Unit 6) | S / Low |

### Options comparison table (6.2)

| Criterion | Option 1: two grammars + adapters | Option 2: open superset | Option 3: closed versioned contract |
|---|---|---|---|
| Maintainability | Two grammars and two fingerprints stay (R01 C-1 to C-4). | One record; module vocabularies declared as data (R13 M2). | One record plus whitelist; every new field needs a registration. |
| Integration complexity | Lowest for existing consumers; every new consumer writes an adapter. | Medium: `annotate` and ledger rows become locator-agnostic (R13 M1). | Highest: all producers migrate; refusal semantics change. |
| Reuse potential | Keeps both parsers. | Reuses v2 structure and the lens/role table pattern. | Reuses variant validators and the `panel-msg/1` key-table pattern; export adapters (W04). |
| Evidence strength | Code-verified incompatibilities (R01 probes). | Code-verified parser behaviour (R02 section 3) and consumer needs (R13); no run exercises the merged record. | Verified for the variants' behaviour (R02 section 7); external projection evidence is web-only (W04). |
| Blocks future PR review or rf-qa replacement | Partly: PR works through its own `Finding` (R13 P1); a ledger-based rf-qa replacement cannot take citation-only findings (R13 M1). | No if M1 to M3 are met; closed sets become inputs (R13 P2, P3). | No if the registered record carries file:line, lens and module vocabularies; adds a registration step per module. |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE` for open versus closed unknown-key policy: a whitelist breaks E2's in-line `origin` unless `origin` is registered, and the variants disagree (R02 gap 12); no source measures which fails less. `UNDECIDABLE-BY-EVIDENCE` for one wire format versus an adapter per consumer: R13 question 1 reads "adapter now, extensible v2 later" as the evidence-supported direction, which is a reading, not a measurement. Decided by evidence: for the ledger/merge path (spec review, and any rf-qa replacement on the same ledger) a citation-only finding cannot flow until `annotate` and ledger rows stop requiring `anchor` (`findings.py:346-349`, `ledger.py:127-138`; R13 stale-documentation fix-cycle note). The severity and cap policy shown in R12 section 8 (blocking boolean as the only verdict driver, `max_fix_cycles = 2` default) is labelled a design inference in R12 and carries no option here.

## 6.3 Limits policy

**Description:** what the pipeline does with a finding line that breaks a parser limit (anchor or anchor2 over 200 characters, claim over 300, refs over 8, id over 16, bad severity, MINOR with `blocking`). The candidates in RN are truncate, reject and re-ask, or keep drop-and-warn.

**How it works (today and per option):** today both parsers drop the whole line and continue; v1 keeps the reviewer's other lines in the ledger, v2 marks the block `invalid` and `cluster` ignores the whole reviewer (R02 sections 5.3, 9). The three policies differ in where the repair sits and what it costs.

| Figure (unit) | Value | Source |
|---|---|---|
| merges examined (merge = row x package) | 264 (89 rows x 3 packages) | R02 section 5.1; R08 section 5 |
| finding lines dropped, all severities ("92") | 92: anchor over 200 = 56, anchor2 over 200 = 18, claim over 300 = 14, bad severity = 3, refs bad = 1 | R02 section 5.1 (recomputed); R08 section 5 |
| reviewer-package runs with `block ok false` ("80") | 80 (a count of reviewer runs, not findings) | R08 section 5 |
| blocking finding lines dropped ("49") | 49: anchor over 200 = 24, anchor2 over 200 = 14, claim over 300 = 10, refs bad = 1; in 44 distinct (row, package, reviewer) triples | R02 section 5.1 |
| verdicts flipped FAIL to PASS | 3 (`audit2.json` `verdict_flip`), plus 5 total-loss merges that did not flip | R02 section 5.1; R08 section 5 |
| the per-model list (luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1) | sums to 92; it is not the breakdown of the 49 blocking lines | R08 section 5 |

### Option 1: truncate (E2 "H2 normaliser")

| Aspect | Assessment |
|---|---|
| Effort | S (basis: one pre-parse step; cut `anchor` and `anchor2` to 200 and `claim` to 300 as an exact prefix, then validate with the real `parse_block`; R02 section 5.2) |
| Risk | Medium (basis: recovery is an upper bound; luna's measured verbatim anchor fidelity is 91.4 percent, `COMBO-REPORT.md:294`, so part of the cut anchors may not locate; R02 section 5.2) |
| Reuse of existing code | `card_convert.py:199-201` (the only truncation in the package: claim to 297 characters plus `...`, `MAX_CLAIM = 300` at `:86`; pinned at `tests/review/test_review_card_convert.py:495-501`); `findings.locate` (`findings.py:276-304`); `parse_block` as the validator (R02 section 6.3) |
| Files and systems affected | a pre-parse repair step before `findings_v2.parse_block` and before `ledger.merge_round` (R02 section 5.3: "the repair policy has to sit BEFORE `findings_v2.parse_block`, or `parse_block` has to be made repair-aware"); `tests/review/test_review_findings.py:111-122` (limits tests); briefs |
| Pros | Addresses up to 88 of 92 dropped lines (95.7 percent) and 48 of 49 blocking lines (98.0 percent) by reason (R02 section 5.2). No extra model call. A prefix of a verbatim quote is a verbatim substring, so `locate` finds it (R02 section 5.2). |
| Cons | Cannot address 4 lines (3 bad severity, 1 bad refs; 1 of them blocking) (R02 section 5.2). A claim cut mid-sentence loses text and possibly meaning (R02 section 5.2). E1's protocol says the orchestrator "never edits, remaps or normalizes a reviewer's findings itself" (`SKILL.md:343`), so truncation conflicts with the E1 text (R02 section 5 key takeaways). The recovery figure is a derivation, not a measurement. |

### Option 2: reject and re-ask once

| Aspect | Assessment |
|---|---|
| Effort | M (basis: needs the reviewer session to persist or a second prompt that carries the first answer; E2's design uses `claude -p --resume`, R02 section 5.2) |
| Risk | Medium (basis: recovery rate unmeasured; the E2 spike for it was not run, R02 gap 5; `--resume` for gateway ids is only partly evidenced: the E2 r2 spike S2 passed for ember, luna, sonnet and haiku, `E2@6c09843:.../r2-idle-shift-sweeper/spikes/RESULTS.md:11-14` (R09 section 4.1), while official docs are silent on gateway ids, W02 section 3) |
| Reuse of existing code | E1's one bounded re-ask and the first-pass metric (`SKILL.md:343`, `:988`; `scripts/reflect_shadow_exit.py:247`); the parser already returns line number and message per rejected line (`findings.py:188-192`, `findings_v2.py:284-287`) |
| Files and systems affected | the dispatch layer (session persistence, `--session-id`, `--resume <explicit id>`, W02 section 10); the manifest attempt record; `merge_cmd.py` and `ledger.py` for the dropped-line accounting |
| Pros | All 92 lines are re-askable in principle, including the 4 that truncation cannot fix (R02 section 5.2). Keeps the reviewer's own wording. Matches E1's documented single bounded re-ask (R02 section 5 key takeaways). |
| Cons | Adds wall-clock time for each affected reviewer: 44 reviewer-runs held a dropped blocking line (R02 section 5.2). Recovery is unmeasured (R02 gap 5). Swarm workers get one user message and no session (`openai_compat.py:384-388`), so a re-ask there needs a second prompt carrying the first answer (R09 section 4.2). One design places the re-ask outside every time bound (R02 section 5.2). |

### Option 3: keep drop-and-warn (today) and add visibility

| Aspect | Assessment |
|---|---|
| Effort | XS (basis: stop keeping only the first error; store dropped counts and ids; R15 section 7.3, R16 Part 7) |
| Risk | High (basis: recovers nothing; the 3 flipped verdicts and 5 total-loss merges stay lost unless a separate fail-closed rule exists, and that rule has not been implemented; R02 section 5.2) |
| Reuse of existing code | `ledger.py:127-134` (warning keeps the error count and the first message), `ledger.py:141-149` (entry stores `block_ok`, `report_sha256`, no raw or kept counts); `parse_block` already returns the full error list (`findings.py:124-196`) |
| Files and systems affected | `ledger.py`, `merge_cmd.py`; an audit-style conservation check `raw == kept + rejected-with-reason` (R16 Part 7.1 audit D row) |
| Pros | No behaviour change and no model call. It is the form E2 reported against ("discarded with no error" is corrected: merge emits a first-error warning, `merge-stdout.txt` carries it, R08 section 5). |
| Cons | Recovers 0 of 92 and 0 of 49 (R02 section 5.2). Under findings-v2 clustering one bad line removes a whole reviewer, so the loss unit is larger than in v1 (`cluster.py:256-257`; R02 section 5.3). 45 merges have no `merge-stdout.txt` and `merge` exits 0 (R08 section 5). |

### Option 4: truncate length violations, then one re-ask for the rest (E2 R-02)

| Aspect | Assessment |
|---|---|
| Effort | M (basis: both components plus `dropped_lines` accounting) |
| Risk | Medium (basis: inherits the unmeasured parts of options 1 and 2) |
| Reuse of existing code | as options 1 and 2; E2's one real row recorded `reask: 1` and `dropped_lines: 0` (`E2@6c09843:.../r1-move-radar/results/el2-c0-r0.json`, R09 section 2.3) |
| Files and systems affected | as options 1 and 2; E2 requirement text `merged-requirements.md:1006` (R02 section 5 key takeaways) |
| Pros | Truncation covers the 88 length lines without calls and re-ask covers the 4 others; both E1 and E2 text allow one re-ask (R02 section 5 key takeaways). |
| Cons | The E1 "never normalizes" rule conflicts with the truncation step (R02 section 5 key takeaways); the combination has no measured result. The E2 requirement names only anchor, anchor2 and claim; the citation `quote` (12..200, `findings_v2.py:80`) is not named. |

**Related levers (not alternatives):** generate the limits in the brief from the parser constants, because the loop brief states only the anchor limit and the reflect brief omits the quote length (`document_review_loop_prompts.md:60`; `reviewer-spec.md:39`; R02 section 6.2; R05 B-2). E1 first-pass compliance was a pilot mean 0.704 over 9 runs and a combo mean 0.867 (R07 E1-F12; the two means are not an A/B of the skill fix). Raising the anchor limit is listed as a prerequisite in `COMBO-REPORT.md:371` and has not been tested (R08 section 7, point 9).

### Options comparison table (6.3)

| Criterion | 1: truncate | 2: re-ask once | 3: keep and warn | 4: truncate then re-ask |
|---|---|---|---|---|
| Maintainability | One deterministic step; must cover every limited field. | Needs dispatch support and a re-ask attempt record. | Least code; a larger audit surface. | Two mechanisms to maintain. |
| Integration complexity | Low: before `parse_block`. | High: sessions or a second prompt per runtime (R09 section 4). | Low. | High. |
| Reuse potential | `card_convert` truncation (`:199-201`). | E1 re-ask text and metric (`SKILL.md:343`). | Existing warning path. | Both. |
| Evidence strength | Recovery upper bound from recounted reasons (R02 section 5.2); not measured. | Recovery unmeasured (R02 gap 5). | Loss recounted (R08 section 5). | Not measured. |
| Blocks future PR review or rf-qa replacement | No: the step is parser-level; it must also cover citation `quote` for file:line findings. | No; needs a session mechanism the PR path may not have (pr-submit runs in the main session, R13 P8). | No, but the loss stays in any module that adopts the parser. | No. |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE` between truncate, re-ask and the combination: re-ask recovery was never measured (E2 Spike 5 not run), the truncation figure assumes truncated anchors still locate, and the E1 and E2 texts disagree on whether anything may edit a reviewer's finding (R02 gaps 4, 5, 11). Decided by evidence: keep-and-warn recovers nothing (R02 section 5.2), and the repair step belongs before `findings_v2.parse_block` (R02 section 5.3).

## 6.4 Quorum and verdict

**Description:** how many valid reviewers a round needs, who decides what is blocking, and who computes the round verdict (reviewer-typed, script-computed from ledger rows, or the reflect `derive_verdict` contract map). RN lists: one valid reviewer passes (pinned by `tests/review/test_review_ledger.py:376-385`), a quorum, or a manifest-driven rule.

**How it works (verdict authority today, [CODE-VERIFIED], R03 section 4.2):**

| Mechanism | Who types what | Who computes the verdict | Fail-closed on a missing review |
|---|---|---|---|
| Master Review Loop (prose, `spec-panel.md:260`) | reviewer types `verdict:` last line | the reviewer, checked by the host command's rules | prose: no prior table, missing or ambiguous `verdict:` line, or an unknown cited id = FAIL |
| CLI ledger (`ledger.py`) | reviewer types `severity` and `blocking` per line; the typed `verdict:` line is ignored | script: FAIL iff any row is `blocking` and `open`/`regressed` (`ledger.py:99-104`, `:273-275`); stored, not derived (`:363-372`) | only when no reviewer produced a valid block (`ledger.py:150-157`) |
| Variant ledger (`review_ledger.py`) | reviewer proposes grade, rule, `wrong_outcome` | script predicate `_blocking_spec_panel` (`:41-49`); `decide` (`:1900-1914`) | yes: an unanswered row or `cannot-verify` gives ESCALATE (`:1903-1907`) |
| Variant stoprule (`stoprule.py`) | reviewer types claims only; a blind `finding-grader` decides blocking | script `compute_verdict` (`:1162-1205`); "silence never passes" (`:1189`) | yes, strongest of the four |
| Variant diffgate (`diffgate.py`) | reviewer types `FINDING`/`PRIOR` lines | script (`:796`); a prior blocker with no `PRIOR` line stays `open` (`:754-756`) | yes for priors |
| Reflect `contract.derive_verdict` (`contract.py:138-260`) | orchestrator or engine writes contract fields | pure function over 19 fields; BLOCKED 2, DEGRADED 11, HALTED 10, PASS 0 | yes: missing contract, non-zero child rc, malformed booleans are BLOCKED |

**Reproduced at HEAD (R03 section 1, [CODE-VERIFIED] by execution):** D-1 a row is cleared by the absence of a re-find, including by one reviewer who took no part in round 1 (`ledger.py:254-258`; the packaged templates carry `"apply_to": ["first"]`, so a standard re-review resolves one reviewer, `panel.py:600`); D-2 one valid block of three yields PASS and exit 0 (`ledger.py:150-157`); D-11 a deferred row re-found as blocking leaves the round PASS and a human `defer` at the cap turns ESCALATE into PASS (`ledger.py:99-104`, `:235-238`, `:350-360`); D-13 the stored verdict is stale after `revise` (`ledger.py:363-372`); a round 4 is accepted after ESCALATE at round 3. Tests pin D-1, D-2, D-11, missing-anchor rows, the narrow reference grammar and reviewer re-classification as intended behaviour (`tests/review/test_review_ledger.py:193-217`, `:376-385`, `:396-405`, `:408-417`, `:518-546`; `tests/review/test_review_cli.py:274-292`, `:298-313`; R03 section 2). The refusal rule at zero valid blocks came from a review finding "an invalid review must never certify PASS" (`tests/review/test_review_ledger.py:346`; R03 section 2 key takeaways).

### Option 1: keep the CLI ledger rule (reviewer-typed `blocking`, any one valid block)

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Medium (basis: three reproduced fail-open paths; whether they are bugs or contract is an owner question, R17 questions) |
| Reuse of existing code | `ledger.py`, `ledger_cmd.py` (exit codes 0/10/11, `:13`, `:109`), `merge_cmd.py`; all existing pins stay valid |
| Files and systems affected | none beyond documentation; the loop brief and ledger behave as pinned (R03 section 2) |
| Pros | Fail-closed at the 0-valid boundary is intentional and tested (R03 section 2 key takeaways). Exit-code contract 0/10/11 exists (`ledger_cmd.py:13`). Any blocking flag from any one reviewer fails the round however many are silent (R03 section 1.2). |
| Cons | One valid reviewer of N passes (D-2), silence clears rows (D-1), a human `defer` rewrites the verdict and a deferred row never re-opens (D-11), the stored verdict is stale after `revise` (D-13) (R03 section 1). A reviewer-typed `CRITICAL` with `blocking: false` is accepted and yields PASS; the reviewer's own `verdict:` line is dead input (R03 section 1.2). `confidence` is rendered and never read (`ledger.py:86-90`, `:435`). |

### Option 2: ledger-derived verdict with a recorded quorum and explicit clearing

| Aspect | Assessment |
|---|---|
| Effort | L (basis: R03 section 5 lists seven implications I-1 to I-7; six of the eight pins read assert the defect behaviour and must be rewritten with the fix) |
| Risk | Medium (basis: pinned tests are named as features, for example `test_cleared_after_the_next_round...`, `test_one_valid_block_is_enough...`; R03 section 2) |
| Reuse of existing code | variant semantics to port, not import (`review_ledger.py:1829-1853` per-row verify answer, `:1903-1907` unanswered means ESCALATE; `diffgate.py:754-760` silence keeps a prior blocker open; owner counting rule `SKILL.md:117`, metrics code `review_ledger.py:2394-2405`); `manifest.reviewers_complete` exists and `ledger.py` never reads the manifest (R03 section 1.2) |
| Files and systems affected | `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `manifest.py`; `tests/review/test_review_ledger.py`, `test_review_cli.py`; the loop prompts text that names the ledger (`document_review_loop_prompts.md:62,70`) |
| Pros | Unanswered means open, the inverse of the CLI rule (R03 section 4.1). The owner counting rule's verdict side is already shipped as prose: a finding the reviser deferred or withdrew, or one the reviewer cannot match with certainty, counts as open (`spec-panel.md:262`; R14 section 7.1 c1). The CLI ledger is the only multi-reviewer merge, so the port adds discipline to the code that already merges panels (R03 section 3 key takeaways). |
| Cons | The variants have no valid repeated result and no measured effect (R14 section 7.3). The quorum count is not given by the code (R03 gap 6). It adds a second status vocabulary question: `resolved_check/resolved/regressed` against `fixed/verified/reopened` (R03 section 4.1). Variant scripts are single-reviewer loops, so panel behaviour of the ported rules is untested (R03 section 3). |

### Option 3: reflect `derive_verdict` as the shared verdict shell, fed from ledger and manifest

| Aspect | Assessment |
|---|---|
| Effort | M (basis: the function is pure and exists; a mapper from ledger and manifest to its 19 fields is the new part; R03 section 4.2, R06 section 1.4) |
| Risk | Medium (basis: the 36-test verdict matrix and contract 1.8.0 pins bind any change, R06 section 8(a), R18 F8, F9; the 0.75 versus 0.80 threshold is decided by the code, 0.80 enforced and pinned, with the skill prose to be reconciled, 6.8) |
| Reuse of existing code | `contract.py:138-382` (4-state map, 14 degraded triggers at `:263-358`, halted triggers at `:361-382`); `tests/cli/reflect/test_verdict_mapping.py` (36 `def test_`); `scripts/reflect_verdict_replay.py` (replays 42 recorded legacy contracts, 0 differences) |
| Files and systems affected | `cli/reflect/contract.py` becomes shared; a ledger-to-contract mapper; `tests/cli/reflect/`; the tasklist post gate that reads exit 0/10/11/2 (R11 section 4) |
| Pros | Supplies the missing DEGRADED state for partial panels: three of four reviewers invalid would be a degraded outcome instead of a PASS (R03 section 4.2). Pure, fail-closed on missing or malformed input (R06 section 1). |
| Cons | It reads orchestrator-typed contract fields, not findings or ledger rows (R06 section 1.4). Engine A fills several of those fields with constants (merge method set by reviewer count, `verification_ran: False`, zero deviations), so a PASS rests on defaults (`ensemble.py:772-832`; R06 section 2.2). Wrapper coverage is UC-2 only (R11 section 4.3). |

### Option 4: a separate blind grader decides blocking; the reviewer never types the verdict

| Aspect | Assessment |
|---|---|
| Effort | L (basis: 14 subcommands and 11 coordinator steps in the stoprule protocol, R14 section 7.2) |
| Risk | High (basis: installed-only, no valid live run; the integrity check returns `EXIT_OK` in every branch including `grader-integrity: mismatch`, `stoprule.py:1793`, `:1802`, `:1812`, `:1815`; R14 section 7.1 c3) |
| Reuse of existing code | `finding-grader` agent (35 lines, tool Read), `stoprule.py` `compute_verdict` (`:1162-1205`), rubric B1 to B3 (15 lines), canaries (58 lines) (R14 section 7.2); all under `~/.claude/`, none in `src/` |
| Files and systems affected | new product skill and agent; a CLI subcommand set; `tests/` (the variant tests live only in the archived bundle, R03 gap 2) |
| Pros | Strongest fail-closed rule of the four: "silence never passes"; a hand-typed `verdict:` makes `finalize` refuse (R03 section 4.2; R14 section 7.1 c3). The grader runs on a different model class under a frozen rubric. |
| Cons | A grader decides blocking per claim; it is not a multi-reviewer merge (R03 section 3). No variant has a valid repeated result (R14 section 7.3). The live trial was invalid at transport (R14 section 7.2). |

**Cap policy (sub-axis, [CODE-VERIFIED] R12 section 4):** the master loop, rf-qa, `/task` and pr-submit's default already agree on 2 fix cycles (3 reviews) (`spec-panel.md:261`; `rf-qa.md:110`; `task/SKILL.md:340-372`; `fsm.py:32-33`); the CLI ledger defaults `cap_reviews` to 3 (`ledger.py:37-38`); pr-submit's hard cap is 5 and `/sc:implement` is exempt by rule S4. A text in any primitive that states another cap outside `sc-implement-protocol` fails `tests/skills/test_review_severity_rule.py` `test_f` (`:320-339`; R12 section 2.1). A core that hard-codes 3 reviews or 2 fix cycles versus one that lets a module declare an override is a design choice; R12 section 8 states the override form as a design inference.

**External evidence (W01, context only):** no peer-reviewed study compares any-pass, majority and unanimous rules on findings with ground truth for PR review (W01 discrepancies). Strict unanimity cut false accepts on SQL correctness (F1, https://arxiv.org/abs/2602.18492, transfer unverified); a 2-of-3 filter that discards single-reviewer findings is used to build a golden set (D3, https://entelligence.ai/code-review-benchmark-2026) while a union of independent reviews raised recall on SWR-Bench (D1, https://arxiv.org/abs/2509.01494); nine judges from seven families carried about two independent votes (B3, https://arxiv.org/html/2605.29800v1), so "k of n agree" is weak evidence. W01 recommends measuring TPR and FPR per rule with the E1 or E2 ground truth and keeping single-reviewer findings as unconfirmed rather than discarding them.

### Options comparison table (6.4)

| Criterion | 1: keep CLI rule | 2: derived verdict + quorum | 3: `derive_verdict` shell | 4: blind grader |
|---|---|---|---|---|
| Maintainability | Defects stay; pins named as features. | One ledger with derived verdict; rewritten pins. | Reuses a pure, frozen, tested function. | 2,050-line stdlib script and 14 subcommands to port or rebuild. |
| Integration complexity | None. | High: ledger, manifest, CLI, brief text. | Medium: mapper; threshold and vocabulary decisions (6.8). | High: new skill, agent, state files. |
| Reuse potential | Existing ledger. | Variant discipline plus CLI clustering. | `contract.py`, 36-test matrix, replay script. | Grader agent, rubric, canaries. |
| Evidence strength | Reproduced defects and pins (R03 section 1, 2). | Reproduced gaps (R03 section 1); the variants' rules have no valid repeated result (R14 section 7.3). | Verified function and matrix (R06 section 1); PASS on engine A rests on defaults (R06 section 2.2). | Code read; live trial invalid (R14 section 7.2). |
| Blocks future PR review or rf-qa replacement | How: the panel verdict is ignored in the PR flow, only findings enter (R13 P12); an rf-qa replacement needs regression and monotonicity halts, which this rule lacks (R13 R7). | No: halts are additive (R13 R7); the checklist mode (R13 R2) is separate. | No: HALTED exists; wrapper is UC-2 only. | Unknown for PR; rf-qa has its own severity rule (R12 section 2.1). |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE`. Reasons: (1) the quorum count (all, two of three, majority) has no rule in the code (R03 gap 6) and no external study on findings (W01); (2) whether the reproduced fail-open paths (D-1, D-2, D-11) are bugs or contract is an owner question that existing tests pin the other way (R17 questions for the owner); (3) no run compares verdict authorities. Decided by evidence: the stored verdict is stale after `revise` and `defer` rewrites it (D-13, D-11, reproduced), and every verdict model above leaves the PR flow's own routing untouched (R13 P12).

## 6.5 Dispatch

**Description:** how a resolved reviewer is launched and how the model that actually ran is known. RN lists: by class through the orchestrator Agent call (E1), raw id per reviewer process (E2), and the tier alias in the product path. R04 finds a fourth mechanism in code (the swarm HTTP transport) and that the product package only resolves.

**How it works (four mechanisms that exist, [CODE-VERIFIED], R04 sections 3.1 to 3.5):**

| Property | E1 class on the Agent call | E1 code engine (swarm HTTP) | E2 `claude -p --model <raw id>` | Product `review` package |
|---|---|---|---|---|
| Unit named at dispatch | class word on the Agent `model` argument, or agent frontmatter `sonnet` | raw model id in the request body | raw model id | none; resolution prints `alias` and `launch` (class word or `None`) |
| Reaches a non-first model of a tier | no: class word to `ANTHROPIC_DEFAULT_*_MODEL` alias to the first non-cooling model of the tier (`local-gateway-alias-proxy.py:694-697`, `:834-839`) | yes (`T2Model0N` pool) | yes | not applicable |
| Reviewer tools | read-only agent (`reflect-reviewer.md:5-8`) | none (plain completion) | Bash allowed, `Edit Write NotebookEdit` disallowed (`run-reviewer.sh:48`) | not applicable |
| Served model recorded by | transcript only (`message.model` of the sidechain) | not recorded; `WorkerResult.model_id` is the requested id (`openai_compat.py:467-470`) | `OBS` from the transcript JSON (`run-reviewer.sh:51-56`) | not recorded |

Product facts: `launch` is empty under the `gateway` environment (`review-tiers.default.json:29`); a `reflect-*` template accepts only `launch` values sonnet, opus or haiku and at most 3 reviewers (`panel.py:72-73`, `:153-156`), so `--env gateway` is refused (reproduced, R04 section 2); `review panel validate --kind panel` does not exercise that profile (`panel_cmd.py:124`). No product code records the served model (`telemetry.py:49` and `:364` define `model_observed` with no writer; R04 section 4.2). Three hand-kept copies of the tier lists exist (Coder env, `ccsession-models.json` with `MODEL-TIERS.md`, `review-tiers.default.json`); only a count and two first-model names are tested (`tests/review/test_review_panel_live7.py:92-98`) (R04 section 5). `muse-ember-1.0` is absent from every tier data file at HEAD although the live workspace env carries it as `T4Model04` and `ccsession-models.json` lists only three tier-4 slots (R04 section 7). "Class" has three vocabularies: the tier file `classes`, the reflect vendor substring table, and the SKILL.md class set that includes `kimi` and `deepseek` (R04 section 8).

### Option 1: dispatch by class word through the orchestrator Agent call

| Aspect | Assessment |
|---|---|
| Effort | XS (exists in the reflect legacy rotation and shadow mode) |
| Risk | Medium (basis: collapse and class drift below) |
| Reuse of existing code | `agents/reflect-reviewer.md` (tools Read, Grep, Glob, search and codegraph; `permissionMode: plan`; `model: sonnet`), `panel resolve` with the `anthropic-only` environment `launch` map, `SKILL.md:340-349` shadow steps |
| Files and systems affected | `src/superclaude/skills/sc-reflect-protocol/` (edit fence `test_shadow_skill_contract.py:42-98`), `ccsession` exports of `ANTHROPIC_DEFAULT_*_MODEL`, agent frontmatter |
| Pros | Reviewers are mechanically read-only (`reflect-reviewer.md:5-8`). Official docs say hooks also fire inside subagents with `agent_id` and `agent_type`, and `SubagentStop` carries `last_assistant_message` and `agent_transcript_path`, so reviewer returns can be observed without a `claude -p` child (W02 section 9; external, https://code.claude.com/docs/en/hooks). |
| Cons | The Agent `model` enum is sonnet, opus, haiku, fable; it cannot name tier-2b, tier-3, tier-4 or non-first-slot models (E2 probe, R04 section 3.2). The same class word is a different model in a non-tier workspace (`docs/reference/model-aliases.md:38`; R04 section 3.5). In this workspace the haiku class was served `gpt-6.1-sol` in five reviewer calls (A1, A2, B1, B2, B3) (R04 section 4.3). Run A-r3: three reviewers and three calibrators were dispatched with no `model` argument, all were served `claude-sonnet-5-5`, and the contract still reports `calibrator_diversity: full` (R04 section 4.3); the calibrator lost its class in 6 of 15 combo runs (R07 E1-F5). `--env gateway` is refused by the reflect profile. |

### Option 2: raw model id per reviewer process (`claude -p --model <id>`)

| Aspect | Assessment |
|---|---|
| Effort | M (basis: the E2 launcher `run-reviewer.sh` (87 lines) and its judge and audit scripts are not in HEAD and hard-code an absolute worktree path, R16 Part 1 and section 5.1) |
| Risk | Medium (basis: not read-only by construction; fallback overwrite; hooks and `--resume` for gateway ids are only partly evidenced (OQ-2)) |
| Reuse of existing code | `E2@6c09843:.../tools/run-reviewer.sh` identity check (`:51-56`), ladder (`:23-43`, `:66-83`); the Claude Code flags `--session-id`, `--settings`, `--tools`, `--restricted` (W02 sections 4, 10; external, https://code.claude.com/docs/en/cli-reference) |
| Files and systems affected | a new launcher in the product (none exists, R04 section 3.1); the tier file `launch` map; E2-style identity audit as a product check |
| Pros | Reaches every gateway model, which tier aliases do not (`probe.json` alias findings: tier2 serves `gpt-6.1-sol`, tier2b `gpt-6.1-terra`, tier3 `glm-5.3`, tier4 `gpt-6-luna`; R04 section 3.4). A transcript check of the served model exists (`run-reviewer.sh:51-56`). One `--model` per process is a documented pattern (W02 section 7). The E2 r2 spikes recorded hook delivery and `--resume` passing for ember, luna, sonnet and haiku on main-thread sessions (R09 sections 2.3, 4.1). |
| Cons | A raw-id request still passes the shim's tier failover (`local-gateway-alias-proxy.py:698-702`, `:432-449`), so a later model of the tier may serve it; only the transcript audit sees that (R04 section 3.4). The fallback ladder overwrites `MODEL` before the meta file is written (`run-reviewer.sh:76`, `:58`), so a silent swap passes `MODEL_OK` (R04 section 4.2; R16 section 1.1). Reviewers have Bash. E2's exclusion list and ladder live in a script, not in data (R01 C-7). A launch with `--bare` loses hooks passed through `--settings` (W02 section 2; external). |

### Option 3: in-process HTTP transport by raw id (swarm)

| Aspect | Assessment |
|---|---|
| Effort | M (basis: `cli/swarm` transports and `cli/reflect/ensemble.py` exist; the review package would need to call them, and `cli/review` has no `swarm` reference today, R13 section 3) |
| Risk | Medium (basis: no tool loop; requested id recorded; tasklist text only) |
| Reuse of existing code | `swarm/transports/openai_compat.py`, `ensemble.py:276-285`, `fallback.py` (bounded ladder), `StubTransport` (credit-free lane, `ensemble.py:123-174`) (R06 section 4.4) |
| Files and systems affected | `cli/swarm/`, `cli/reflect/{ensemble,fallback,_diversity}.py`, `T2Model0N` env pool |
| Pros | Runs headless without the Agent tool; `T2Model0N` reaches non-first models; bounded fallback ladder; `--transport stub` lane (R04 section 3.3; R06 section 8(d)). |
| Cons | Workers get one user message and no session (`openai_compat.py:384-388`), so no hook point and no resume (R09 section 4.2). Reviewers see the tasklist body only, not the diff or the spec (`ensemble.py:601-630`; R05 Unit 6 family 4). Diversity is computed from requested ids and the response `model` field is never read (`openai_compat.py:467-470`; R04 section 3.3). The engine emits contract `1.0` with 10 keys outside the frozen lists and no executor-class exclusion (R06 sections 2.4, 4.2). |

### Option 4: resolution as the dispatch contract (the tier file's `launch` map defines the mechanism per model)

| Aspect | Assessment |
|---|---|
| Effort | L (basis: no launcher exists; the `launch` map would need values for gateway models and a consumer) |
| Risk | Medium (basis: three hand-kept tier lists with only a count test; `muse-ember-1.0` absent; reflect profile allows only three `launch` words) |
| Reuse of existing code | resolution fields `alias`, `launch`, `model`, `fallbacks` (`panel.py:666-681`); the `classes` map as the single class owner (`review-tiers.default.json:18-23`; R04 section 8 key takeaways); `select_env` (`panel.py:485-494`) |
| Files and systems affected | `review-tiers.default.json`, `panel.py`, `panel_cmd.py`, `ccsession-models.json`, `MODEL-TIERS.md`, `tests/review/test_review_panel*.py` and the frozen golden fixtures (R18 F15) |
| Pros | Data-driven: `launch` and `alias` are already printed per reviewer; one owner for "class" and "vendor" is already half there. A single tier source removes the drift risk of three copies (R04 section 5 key takeaways). |
| Cons | Not implemented anywhere. The reflect profile caps `launch` at sonnet, opus, haiku (`panel.py:72`); a gateway value needs a profile change. It still needs a launcher, which is option 2 or 3. A `reflect-*` template with N greater than 3 is refused by the profile, so a seven-reviewer tasklist template cannot reuse it unchanged (R04 section 2 key takeaways). |

### Sub-decision 6.5.b: the run record that carries served model, usage and stage (R15 section 8)

| Option | What it is | Evidence for | Evidence against | Effort / Risk |
|---|---|---|---|---|
| (a) per-run `events.jsonl` + manifest state machine + `review-telemetry` export | one append-only row per agent attempt under `flock`; cost only on those rows; served model and usage from a transcript adapter; hash pointers, no document text; module counters in a namespaced `ext` object (R15 section 8, a design derived from evidence) | manifest attempts hold only hashes: the payload is hashed and discarded (`manifest.py:348-354`) and all six attempts of one run share one `payload_sha256`; `metrics.json` and `runs.jsonl` values are orchestrator estimates (round numbers; two null rows) (R15 sections 4.2, 4.3); orchestrator output-token share median 0.59 over 15 combo runs, so reviewer-only accounting under-reports (R15 section 9.1; the share is an upper bound in combos B, C, D, R07 section 1.1) | the transcript adapter's availability in every harness is open (R15 gap 3, OQ-3); `review-telemetry/1` changes version if kinds are added | L / Medium |
| (b) extend `review-telemetry/1` to `/2` only | add an `agent_run` kind, value type checks, one live outcome per `(reviewer_record_id, truth_basis)` | the store has the cost group and a SQLite loader (`telemetry.py:74-80`, `:382-447`) | no writer in product code; reviewer-session-centric; D-17 cost fan-out reproduced (400 versus 200 per true positive with two live outcomes); group values not type-checked, so the "no document text" rule is a convention (R15 sections 1.1, 1.4, 2) | M / Medium |
| (c) manifest gains `usage` per attempt | store the attempt payload instead of its hash | smallest change (`manifest.py:353`) | D-23 lost updates reproduced by deterministic interleaving (no lock, no revision check) with zero incidents in 29 real manifests; holds no orchestrator or calibrator rows (`PER_REVIEWER_STAGES`, `manifest.py:53`) (R15 sections 3, 4.2, 7) | S / Medium |
| (d) keep the five E2 result schemas | none | none | five schemas, keys and units differ (R15 section 5.2) | XS / High |

The memory write is a third lock-free LLM read-modify-write store (`SKILL.md:585-608`); R15 section 6 proposes one writer at publish keyed by run id and a study-mode switch to freeze memory reads, a proposal with no measured effect.

### Options comparison table (6.5)

| Criterion | 1: class via Agent call | 2: raw id process | 3: swarm HTTP | 4: resolution as contract |
|---|---|---|---|---|
| Maintainability | Depends on workspace env state; class not reproducible across workspaces (R04 section 3.5). | Launcher plus audit scripts to own; paths hard-coded today (R16 section 5.1). | Exists; two registries (`T2Model0N`, tier JSON) (R06 section 4.3). | One data source if the three lists are merged; drift risk otherwise (R04 section 5). |
| Integration complexity | Lowest (exists). | Medium: product launcher, session handling. | Medium: bridge `cli/review` and `cli/swarm`. | High: data plus a launcher. |
| Reuse potential | `reflect-reviewer`, `panel resolve`. | E2 identity check and ladder. | Transports, stub lane, fallback ladder. | Resolution fields, `classes` map. |
| Evidence strength | Observed collapse and class drift in 15 combo runs (R07 E1-F4 to F7); hooks in subagents from official docs (W02). | E2 audit A recorded model identity per run and found two `b4-muse-luna2` "wonder" runs served by terra and no other mismatch, with a raw-JSON part that is not committed (R08 section 7 G14, graded S2); hooks and resume on gateway ids only single smoke rows (R09 section 2.3). | Code read; no quality evidence (R06). | Code read; not implemented. |
| Blocks future PR review or rf-qa replacement | How: class words cannot reach non-Claude reviewers; `--revagent` accepts only four native aliases (R13 P11). | No for model reach; reviewers need a read-only restriction at process level (R13 R1; W02 section 4). | How: no tools, so it cannot ground a code review. | No if a launcher exists; adds no reach by itself. |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE` between mechanisms: the choice depends on whether non-Claude gateway models are in scope for the panel, which R04 question 8(ii) leaves open, and no run compares two mechanisms on one input. Decided by evidence: (1) a class word cannot name tier-2b, tier-3, tier-4 or non-first-slot models; (2) the served model exists only in the transcript, and every contract field that claims diversity or identity is a function of requested values (R04 section 4.2 key takeaways); (3) class, vendor and tier lists need one owner (R04 section 8). The hooks-and-resume behaviour for gateway ids rests on single E2 smoke rows and has no official statement (OQ-2).

## 6.6 Collaboration

**Description:** whether reviewers exchange anything before the merge, and in what form. RN candidates: none (independent reviewers), a static move kit (A2), and the exchange families F1 axis-flip (r3), F3 move radar (r1), F4 idle-shift sweeper (r2), F6 coverage deflection (r5), F7 flag-and-adjudicate (r4).

**How it works (the five E2 packages, [CODE-VERIFIED], R09 sections 1 to 3):**

| Family (package) | Content exchanged | Author | Delivery | Needs |
|---|---|---|---|---|
| F3 Move Radar (r1) | one catalogue move text or a "source.md not opened" check | harness (jq classifier on the reviewer's own telemetry) | PostToolUse hook, JSON `additionalContext` | per-session `--settings` hook, persistence |
| F4 Sweeper (r2) | repo facts (paths, counts, `path:line`, the command) | a helper ember session via Bash helper `panel-post` | PostToolUse hook on two receivers | hook, a Bash-capable helper session |
| F1 Axis-Flip (r3) | a peer anchor or a gap-card line plus one move, in a digest | harness from sealed phase-1 findings | between-phase `claude -p --resume <session_id>` second pass | resume; no hook |
| F7 Flag-Adjudicate (r4) | a card (anchor plus move) | a flagger model via `panel-post` | PostToolUse hook on two adjudicators | hook, Bash helper |
| F6 Deflection (r5) | task ids not covered by any finished scout (`kind: "coverage"`) | harness watcher | PostToolUse hook on the receiver | hook |

Only F1 needs no hook; four hook scripts implement one skeleton four times (baked arguments, always exit 0, `agent_id` skip, `flock` counter, finish signal, transcript seal, JSON output) (R09 section 1.3). Evidence status is the same for every design: built in part, `lib/` absent from the commit for r2 to r5 (`.gitignore:13` is `lib/`; the call sites exist, for example `r3 bin/launch-panel.sh:5,:55`, `r4 bin/r4-hook:10`), claimed test counts 138, 358, 89, 106, 108 are self-reports (static `def test_` counts 103, 163, 89, 90, 82 match only for r3), one to six single smoke rows on a two-item control package, no Spike 4, no defect-package row (R09 section 2). The one weighty number: the static kit alone on sonnet cost +59 percent elapsed (281.567 s against 176.9175 s) and +55 percent output tokens on one package, three runs (`r5 results/results.jsonl`; R09 section 2.3). E2's own text says "The static kit (A2) may beat every exchange design" (`merged-requirements.md:917`) and the plan "cannot detect the central estimates of any slot" (`:1128`) (R09 section 7). Of 36 logged conflicts, 13 are decided by evidence, 4 partly, 4 cannot be decided without a common act-rate probe, 15 are design decisions (R09 section 6).

### Option 1: no collaboration in the core (independent blind reviewers)

| Aspect | Assessment |
|---|---|
| Effort | XS (exists) |
| Risk | Low (basis: nothing new is added; the central gain of exchange is simply not claimed) |
| Reuse of existing code | E1 shadow reviewers are mutually blind (`reviewer-spec.md:84`); merge by `sc-adversarial` Mode A or the CLI merge |
| Files and systems affected | none |
| Pros | Consistent with the E1 design and the E2 process-redesign principle of no reviewer-to-reviewer messaging (R10 Unit 9 item 19). External evidence on benchmark tasks says independent review plus aggregation is a sound default and debate adds little over voting (W01 C1, https://arxiv.org/abs/2508.17536; transfer to finding-set review unverified). No hook transport is needed, and three of HEAD's reviewer runtimes (swarm workers, Agent-tool reviewers, headless sessions) cannot all carry hooks (R09 section 5). |
| Cons | Recorded reviewer overlap is sparse: 7 unchained multi-reviewer clusters among 216 in the combo runs, a figure compromised because citation resolution failed in 7 of 15 combo runs (R07 E1-F10). The collaboration designs target defect classes the isolated panel misses (R09 section 1), and none of them has a measured effect. |

### Option 2: a static move kit or class-recipe text in every brief (no communication)

| Aspect | Assessment |
|---|---|
| Effort | S (basis: brief text per module; no transport) |
| Risk | Medium (basis: the only measured cost is large on sonnet, +59 percent elapsed and +55 percent tokens, one package, three runs) |
| Reuse of existing code | class cards `recipe_text` and `question_template` (R10 Unit 5 card fields); the moves M1 to M10 map one-to-one into classes C1 to C8 (R10 Unit 11); brief builder (6.2.b) |
| Files and systems affected | the briefs (`document_review_loop_prompts.md`, `reviewer-spec.md`), per-module card files |
| Pros | The cheapest design if no exchange beats it: "the harness fixes plus the kit in the brief" (`merged-requirements.md:917`). It gives every reviewer all moves from the first second. It needs no hook, no session and no model-side write. |
| Cons | The effect on found defects is unmeasured. Both catalogues were induced from the same ten issues (R10 Unit 11). The recipes assume a shell while `reflect-reviewer` has no Bash (`reflect-reviewer.md:5`; R10 Unit 5). |

### Option 3: an optional between-phase exchange capability (F1 style)

| Aspect | Assessment |
|---|---|
| Effort | M (basis: two prompts and a seal by process exit; no hook; the engine of r3 is absent from the commit, `r3 bin/launch-panel.sh:5,:55`) |
| Risk | Medium (basis: no clean measured success in any runtime) |
| Reuse of existing code | `panel-msg/1` kinds and the digest design (R02 section 8); the seal by process exit (R09 section 1.2); `claude -p --resume <id>` where sessions persist |
| Files and systems affected | a second-pass step in the dispatch layer (6.5); a message-kind registry; E2 r3 package files as design input only |
| Pros | The only family that needs neither a hook nor a model-side write, so the only one whose text is expressible in each of HEAD's runtimes in principle (R09 section 4.2). |
| Cons | Both r3 A3 smoke rows record `phase2_timeout: 1`; the A1 baseline alone spans 95.2 to 154.8 s, so a +30 percent overhead is not readable as a design effect (R09 section 2.3). No F1 run exists on a swarm worker (one user message, no session) or on an Agent-tool agent (R09 section 4.2). The `--resume` dependency for gateway ids is only partly evidenced (OQ-2). |

### Option 4: optional in-flight exchange through hooks (F3, F4, F6, F7) behind a kill switch

| Aspect | Assessment |
|---|---|
| Effort | XL (basis: a shared hook library replacing four copies, board, seal, message-kind registry, `lib/` engines absent for r2 to r5; R09 section 4.1) |
| Risk | High (basis: no measured gain; hooks bind to main-thread `claude -p` sessions; recorded act rates disagree) |
| Reuse of existing code | the hook skeleton (R09 section 1.3); `reflect --resume` at HEAD means "skip the launch if the prior post is a pass", not a session resume (`commands.py:290-294`; R09 section 4.2) |
| Files and systems affected | the dispatch layer (persistence on, per-session `--settings`), a board path outside the reviewed tree, transcript seal, `PANEL_COLLAB` switch whose off state must restore the isolated arm (R09 section 4.1) |
| Pros | The most mature designs: five packages with partial gate-0 results and a common hook skeleton (R09 section 1). `PostToolUse` is the documented per-call event, and `PostToolUseFailure` covers failed calls (W02 section 1; external, https://code.claude.com/docs/en/hooks). |
| Cons | The packages' own hooks skip subagent calls (`r1 radar-hook.sh:24-28`, `r4-hook:55-59`, `r5 hook-posttool.sh:14-15`), and `reflect-reviewer` has no Bash and cannot be a sweeper or flagger (R09 section 4.2). Recorded luna act rates range from 0 to 1.00 across four probes (r1 item 0.33 next call and 1.00 later, r2 4 of 5, r4 0 and 0.4, r5 1 of 5 and 3 of 5) (R09 section 6.1 X2). Measured hook cost is tens to about 150 ms per call (R09 section 6.2 C-15). A launch with `--bare` loses hooks; official docs do not cover gateway ids (W02 sections 2, 7; external). |

### Options comparison table (6.6)

| Criterion | 1: none | 2: static kit | 3: between-phase exchange | 4: hook exchange |
|---|---|---|---|---|
| Maintainability | Nothing to maintain. | Per-module card text. | A second-pass step and a kind registry. | Hook library, board, seal, kill switch. |
| Integration complexity | None. | Brief only. | Dispatch layer. | Dispatch layer plus runtime constraints. |
| Reuse potential | Existing. | Class cards, brief builder. | `panel-msg/1`, r3 design. | Hook skeleton, five packages. |
| Evidence strength | E1 and E2 independent-reviewer data; no exchange measured. | One measured cost (r5); no measured benefit. | Two smoke rows with a timeout; no benefit measured. | Single smoke rows; no benefit measured. |
| Blocks future PR review or rf-qa replacement | No. | No; recipes need a Grep/Glob form for read-only reviewers (R10 Unit 5). | No; needs a session or a second prompt. | How: hook delivery excludes read-only subagent reviewers and swarm workers (R09 section 4.2). |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE`. Reason: no measurement compares any exchange arm with the static kit, the design's own plan cannot detect the central gain, and the act-rate probes disagree between designs (R09 sections 6.1, 7; X1, X2, C-14 are class N). Decided by evidence: H1 (name the driving document) and H2 (repair of over-limit lines before the merge; the form is the 6.3 axis) belong to the core independent of collaboration, H3 and H4 are per-module snapshot rules, and the transport rules (board, seal, hooks) are conditional on an exchange arm being on (R09 section 5).

## 6.7 Process redesign

**Description:** whether the panel gets a written process in front of the free review: typed items assigned to reviewers by a script (Sweep Sheet), written class recipes per reviewer lens (Recipe Ledger), or neither. RN lists Sweep Sheet versus Recipe Ledger, the class cards C1 to C8, the extra classes X1 to X7 and the gates G0 and D1 to D7.

**How it works (E2 process-redesign brainstorm, design only, [CODE-VERIFIED] as text at the E2 tip, R10 Unit 5):**

| Element | Sweep Sheet (Redesign 1) | Recipe Ledger (Redesign 2) |
|---|---|---|
| Pre-pass | serial deterministic script, no model, byte-identical for the same input and seed; killed at min(15 s, 0.10 x b) with fallback to the isolated brief | none; no extractor |
| What a reviewer gets | up to 12 typed items from extractors E1 to E7, each assigned to 2 of 3 blind reviewers over 24 slots; caps ember 8, luna at most 8 each | a lens of 2 to 4 class recipes; row budget per recipe and at most 14 rows per lens |
| What a reviewer returns | normal findings block | findings block plus a per-reviewer row block (`ledger-v1`) with verdict OK/PROBLEM/UNSURE, `quote_plan`, `quote_other`, `problem`, `ran`, placed in the final message |
| Post-run | script checks and promotion, no re-ask | quote checks; a PROBLEM row whose quote check fails is "unsupported" and its linked finding is demoted; a PROBLEM row with no finding is promoted as a MINOR non-blocking finding tagged `src=ledger` |
| Binding to reviewers | items assigned by the script | lens table bound to model names (ember {C4, C5, C6, C8}, luna 1 {C1, C2, C3}, luna 2 {C2, C4, C7}) |

Both rest on class cards C1 to C8 (`id, name, definition, recipe_text, question_template, extractor, route, replicas, applies_to, instances, known_weakness`) and gates G0 and D1 to D7. Nothing of either exists in code: a search of `src/superclaude/cli` for `PROBLEM`, `UNSURE`, `quote_plan`, `ledger-v1`, `Sweep Sheet`, `Recipe Ledger` returns 0 matches (R10 Unit 3). All probabilities and time figures in the brainstorm are planning values built from cited counts (`merged-requirements.md:24`), so they carry no option here (OQ-4).

**What E1 already has that either redesign would otherwise duplicate (R10 Unit 6, [CODE-VERIFIED]):** the assignment container `{reviewer: {assigned, observed}}` in `coverage.json`, read by `cluster --coverage` and `verify-citations --coverage` and validated by `findings_v2.coverage_context` (`:196-212`, `:166-176`); the quote normaliser (`verify_cmd._norm` equals `findings.flat`); an advisory citation precheck that "drops nothing" (`verify_cmd.py:11-12`). What E1 lacks: class-keyed row producers (only the UC-1 requirement rows exist as prose, `SKILL.md:278`, `refs/coverage-mapping.md:50-60`), a per-row verdict with a quote pair, and any demote or promote step. Recorded E1 use of the container is ad hoc: 13 `coverage.json` files, free-form row ids, a range token and duplicates in the first one read, 11 of 13 files with a row id assigned more than once, 2 of 13 with `observed` empty for every reviewer (R10 Unit 10). The recorded precheck flagged 510 of 1,047 citations (48.7 percent): 472 `not-in-snapshot` (92.5 percent of flags), 7 out-of-range, 31 quote-not-found (3.0 percent of all citations) (R10 Unit 10), so the snapshot boundary matters more than quote exactness in that data.

**What is decidable about the classes (R10 Unit 7):** recorded instances of C2, C4, C5, C6 and C8 are re-readable in `.dev/reflect` reports at HEAD (10 of 10 spot-checked cites exist); C4 and C8 have mechanical instance tests; C1, C3, C7 and X3 to X6 need judgment; C3 is "plausible only" in E2's own table (`merged-requirements.md:103`); the class list is evidence about one repository and one owner's plan pipeline. The gate D2 asks for a mean found fraction at least Z0 + 0.12 absolute, which is 0.12 x 14 = 1.68 items on the 14-item scale (arithmetic, R10 Unit 5); every gate is a design choice and none can be evaluated at HEAD because no arm, extractor, hold-out ground truth or planted set exists (R10 Unit 7 key takeaways).

### Option 1: Sweep Sheet (script pre-pass assigns typed items)

| Aspect | Assessment |
|---|---|
| Effort | XL (basis: extractors E1 to E7 have 0 code; hold-out ground truth and planted set not built; R10 Unit 7) |
| Risk | High (basis: nothing implemented; extractor E6 is "experimental ... high false-positive rate" (`merged-requirements.md:433`); promotion writes a finding the reviewer did not write while E1's checks are advisory only, `verify_cmd.py:11-12`) |
| Reuse of existing code | the sidecar container, `findings.flat`, `verify_cmd._check`; for C2 the extractor E5 and E1's Wave 1B extraction are the same capability (R10 Unit 6) |
| Files and systems affected | a new pre-pass module; `verify_cmd.py`, `findings_v2.py` (`coverage_rows`), the brief; `tests/review/`; no `src` file exists for it today |
| Pros | Deterministic and model-free; "the script never writes a claim" (`merged-requirements.md:378`); a script does the searching, which avoids the shell assumption of the recipes (R10 Unit 5 tool-assumption conflict); C4 and C8 are fully mechanical (R10 Unit 7). |
| Cons | C1, C3, C7 extractors are candidate listers only (R10 Unit 7); the gate D2 is stricter than the design's own central estimate in arithmetic terms (R10 Unit 5, inputs are planning values); no arm has run. |

### Option 2: Recipe Ledger (written recipes by lens, per-reviewer row block)

| Aspect | Assessment |
|---|---|
| Effort | XL (basis: recipes, lens table, row block, post-run checks, promotion; none exist) |
| Risk | High (basis: recipes assume a shell and `reflect-reviewer` has none; the lens table binds to model names the core does not resolve by; the row block's carrier rule is a property of the E2 study launcher, R10 Unit 5) |
| Reuse of existing code | recipe texts R-C1 to R-C8 (`merged-requirements.md:738-752`); the sidecar container; `verify_cmd._check` for substring checks |
| Files and systems affected | briefs, panel slot data (slot keys are closed: `_SLOT_KEYS = {slot_id, tier, count, strategy, seed}`, `panel.py:46`, unknown keys rejected at `:215-216`), `findings_v2.py`, `verify_cmd.py`; the `ledger-v1` name collides with the shipped `review-ledger/1` and its CLI group in five places (R10 Unit 3) |
| Pros | No pre-pass and no extractor. Needs no extra process before the review. |
| Cons | R-C4 says "run it on a scratch string with Bash" and R-C8 uses `git grep -l -F` while `reflect-reviewer` has no Bash (`reflect-reviewer.md:5`, `:8`; R10 Unit 5). The "ledger must sit in the final message" rule follows from the E2 launcher keeping only the first result message (`run-reviewer.sh:50`, `:57`) and is not a product property (R10 Unit 5). Demote and promote conflict with E1's advisory-only precheck and validator-decides-drops rule (R10 Unit 5 key takeaways). The lens binding has no home in the panel template (R10 Unit 9 item 10). |

### Option 3: neither now; keep the isolated panel with the harness and brief fixes

| Aspect | Assessment |
|---|---|
| Effort | S (basis: H1, H2 and brief items B-1 to B-5, B-7, all open at HEAD in shipped files, R05 Unit 4) |
| Risk | Medium (basis: no valid-era E2 row exceeds 4 of 14 defects, and three of the defects carry 89 percent of the catches while four were never caught in 106 runs, R08 section 7 G2, G3; the classes target the missed kinds) |
| Reuse of existing code | the existing briefs and parsers |
| Files and systems affected | the loop and reflect briefs, parser limit step (6.3) |
| Pros | Smallest change; every redesign number is a planning value and no arm has run (R10 Unit 5 key takeaways). The seed claims "no missing-task category, no severity levels" are partly wrong as written (corrected in the last section), which narrows the stated gap to: no definition of CRITICAL versus MAJOR, Medium outside the enum, no named driving document, and a brief and schema that disagree on `blocking` for `missing-requirement` (R10 Unit 8). |
| Cons | Leaves the recurring recorded classes C2, C4, C5, C6, C8 to chance (R10 Unit 7). |

### Option 4: the core absorbs only the reusable pieces, without choosing either redesign

| Aspect | Assessment |
|---|---|
| Effort | M (basis: card schema as data, the existing sidecar, flat-based quote checks, a renamed optional row block, counts-only telemetry; R10 Unit 9) |
| Risk | Medium (basis: promotion and demotion stay on HOLD; the row block's name and carrier are open) |
| Reuse of existing code | `coverage.json` container, `findings.flat`, `verify_cmd._check`, `REFLECT_CATEGORIES`-style mapping (`findings_v2.py:41-48`), `LENSES`, `CHANNELS` constants as the nearest registry (R10 Unit 9 item 7) |
| Files and systems affected | `cli/review/` (card loader, optional block parser), module-owned card files; telemetry stays counts and ids only (`telemetry.py:3`) |
| Pros | Avoids building a second assignment container and a second normaliser (R10 Unit 6). One taxonomy suffices: class cards subsume the move catalogue (R10 Unit 11). Classes stay module data. |
| Cons | A card schema without extractors has no producer. The row block's rename is an open design question (the noun must not be `ledger`, `review-ledger/1` being shipped; R10 Unit 3). The telemetry "no document text" rule is enforced only for `context` values (`telemetry.py:243-251`; R15 section 1.4). |

### Options comparison table (6.7)

| Criterion | 1: Sweep Sheet | 2: Recipe Ledger | 3: neither now | 4: absorb reusable pieces |
|---|---|---|---|---|
| Maintainability | Extractors per class and module. | Recipes per class; row block and checks. | Nothing new. | Card data per module. |
| Integration complexity | New pre-pass step and assignment. | Lens binding and a new block in every review. | None. | Low to medium. |
| Reuse potential | Sidecar, `flat`, `_check`, Wave 1B for C2. | Sidecar, `_check`, recipe text. | n/a | Highest reuse of E1 pieces. |
| Evidence strength | Design only; 0 code; planning numbers (R10 Unit 5). | Design only; 0 code. | Open items verified at HEAD (R05 Unit 4). | E1 container and recorded runs verified (R10 Units 4, 10). |
| Blocks future PR review or rf-qa replacement | How: classes are plan-review evidence from one repository; hard-coded classes would bind future modules (R10 Unit 7). | Same; lens binds to model names. | No. | No if classes remain module data. |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE` between Sweep Sheet and Recipe Ledger: no arm ran, extractors have 0 code, no hold-out set exists and every gate is a design choice (R10 Unit 7 key takeaways). Whether a failed quote check may demote or promote a finding is on HOLD: E1's precheck is advisory and the validator alone decides drops (R10 Unit 9 item 13; question Q3). Decided by evidence: neither redesign exists in code; E1 already has the container, the normaliser and the quote check, so building either as a separate module would duplicate them (R10 Unit 6).

## 6.8 Reflect engine

**Description:** what to do with reflect's two Tier-2 implementations and the Stage 2 exit that currently fails. RN lists: keep both engines, make the swarm engine gain the calibrator and validator, or retire it for the skill panel, plus one convergence threshold (0.75 versus 0.80) and one single-vendor posture.

**How it works (the two engines, [CODE-VERIFIED], R06 section 7):**

| Property | Engine A: swarm ensemble (`cli/reflect/ensemble.py`) | Engine B: skill panel (`SKILL.md` Waves 3 to 5, `--t2-engine legacy|shadow`) |
|---|---|---|
| Reached by | `ReflectRunner._audit_once` for every production `standard` or `deep` run (`runner.py:538-545`) and the sc-tasklist terminal gate | `/sc:reflect` through the Skill: sc:workflow Wave 4 (`SKILL.md:89`), sc-tasklist Stage 10.5 (`:1630`); `shadow` is named only in `SKILL.md`, `refs/reviewer-spec.md` and `manifest_cmd.py`, so no caller passes it |
| Reviewers | external proxy models in `T2Model0N` slots, text in and out; tasklist body and base-ref header only (`ensemble.py:601-630`) | read-only `reflect-reviewer` agents with search tools; briefs hold a card excerpt, grounding hunks and a coverage slice |
| Calibration and evidence gate | none | blind `confidence-calibrator` and a mandatory `evidence-validator` |
| Deviation classes | all zero and `regression_present: False` by construction (`ensemble.py:779-785`, `:820-823`) | four classes decided from evidence (`SKILL.md` section 10) |
| Contract | `contract_version 1.0`, 32 keys, 10 outside the frozen lists, 89 of 110 stable names absent | 1.8.0, 110 stable plus 27 telemetry names |
| Diversity evidence | from the requested model id stamped by the transport (`WorkerResult.model_id` = `self._model`, `openai_compat.py:467-470`; the response `model` field is never read); vocabulary `full | insufficient` (`_diversity.py:8-15`) | from the requested rotation or pin; vocabulary `full | degraded` |
| Executor exclusion | none in production (`executor_model` reaches only the Tier-1 prompt, `runner.py:480-481`) | `SKILL.md:648-658`; `review panel resolve --hard-exclude-class` in shadow |
| Verdict | `derive_verdict` 0/10/11/2; HALTED and the `--fix` loop are structurally dormant (no remediation producer) | no exit code of its own |

Stage 2 exit at HEAD: `OVERALL: FAIL (shadow runs 13 of 20)`, EV-1 failure rate 8 of 13 (three unparseable contract files because unquoted `[1m]` aliases sit inside a flow sequence, four with `merged-verdict.yaml` absent, one empty `reviewer-cards/`), parity failing in 6 of 13, lint problems in 9 of 13, new contract keys in 7 of 28 counted runs of which 5 come from `reviewer_briefs_materialized`, a key the skill's own ref instructs and that is in neither frozen list (R06 sections 3.3, 6; R07 E1-F8, E1-F13). Every failing line is a presence, name, membership or equality check; in 13 pilot plus 15 combo runs no failure was a review-content failure (R06 section 6.2). The exit script treats an empty legacy baseline as 0.0 (`scripts/reflect_shadow_exit.py:313`), so a runs root without legacy runs fails on any shadow failure (R06 section 6.3). The unquoted-alias parse failure also makes `parse_contract` return `None`, which routes BLOCKED `contract-missing` in production (R06 section 6.1).

**Must stay byte-identical (R06 section 8(a)):** the consumer-read 1.8.0 field names (SKILL.md 9.1 and 9.2, tied to `panel_lint.STABLE_FIELDS_1_8_0` (110) and `TELEMETRY_FIELDS` (27) by `test_pinned_field_lists_match_skill_md`), the `merge_method` pair `{adversarial, single-reviewer-fallback}`, the verdict map with its 36 tests, the four deviation keys, the three-section reviewer brief and the findings-block grammar, and the EV-1 layout (`adversarial/merged-verdict.yaml`, `reviewer-<N>-card.*`, an `audit.log` row `F2|F3`). The literal `1.8.0` and "no new key" are a Stage 2 convention with a documented minor-bump path (`SKILL.md` 9.4; `contract.py` accepts any major 1). The byte-identity tests compare with the current `HEAD`, so they bind uncommitted edits only (R06 section 5.6).

### Option 1: keep both engines and reconcile vocabulary only

| Aspect | Assessment |
|---|---|
| Effort | S (basis: one decision per vocabulary point plus doc fixes; R06 section 5.4 lists six conflicts) |
| Risk | Medium (basis: the production wrapper and the skill stay two producers of two contract shapes) |
| Reuse of existing code | everything as is; `contract.py`, `panel_lint.py`, `runner.py`, `ensemble.py`, SKILL.md |
| Files and systems affected | `SKILL.md` (edit fence `test_shadow_skill_contract.py:42-98`), `contract.py` constants, `panel_lint.py` lists, `sc-tasklist-protocol/SKILL.md` and `task-builder/SKILL.md` statements |
| Pros | No pins change if the vocabulary decisions go the way the pins already read. Each engine keeps what the other lacks (R06 section 8(d)). |
| Cons | Documents claim the wrapper "spawns an executor-disjoint reflect ensemble" and resolves to the skill; the code applies no exclusion and does not run the skill in production (`sc-tasklist-protocol/SKILL.md:1141, :1152, :1165`; `task-builder/SKILL.md:2247`; `runner.py:538-545`; [CODE-CONTRADICTED], R06 section 4.2). Engine A fails the lint at L1, L2 and L7 by construction (R06 section 3.2). The six skill-versus-code disagreements stay unless decided (R06 section 5.4). |

### Option 2: the swarm engine gains calibrator, evidence validator, executor exclusion and diff-grounded briefs

| Aspect | Assessment |
|---|---|
| Effort | XL (basis: transports are plain completions with no tool loop, so grounding, calibration and validation need new machinery; R06 section 2, R09 section 4.2) |
| Risk | High (basis: 89 of 110 stable contract names are absent from engine A's contract; its reviewers see tasklist text only) |
| Reuse of existing code | `ensemble.py`, `fallback.py`, `_diversity.py`, `runner.py`; the calibrator and validator agents would need a transport that carries tools |
| Files and systems affected | `cli/reflect/*`, `cli/swarm/*`, the `reflect-review` lens (`lenses/reflect_review.py`), contract and lint constants |
| Pros | Keeps the code-driven, headless, credit-free (`--transport stub`) path as the single engine (R06 section 4.4). |
| Cons | The missing capabilities are exactly what engine B has: grounding chain, blind calibration, evidence validator, the four-class deviation taxonomy, executor-class exclusion, promotion and the findings-v2 kernel (R06 section 8(d)). `--fix` only becomes live if the engine supplies deviation fields and a remediation pointer (R06 section 4.2). |

### Option 3: retire the swarm engine; the wrapper runs the skill panel

| Aspect | Assessment |
|---|---|
| Effort | L (basis: the production path reaches the skill only from a test double today, `runner.py:540`; the Tier-1 child launch `_build_prompt` exists at `runner.py:453-483`) |
| Risk | High (basis: the loss list below) |
| Reuse of existing code | the skill panel, `panel_lint`, `reflect_shadow_exit.py`; `runner.py` verdict and write-back stay |
| Files and systems affected | `runner.py` Tier-2 branch, `ensemble.py`, `fallback.py`, `_diversity.py` (retired), SKILL.md, consumers that call `superclaude reflect run` (`sc-tasklist-protocol/SKILL.md:1157-1163`) |
| Pros | One engine with grounded reviewers, calibration, validation and deviation classification (R06 section 5.1). |
| Cons | Loses, per R06 section 8(d): headless operation without the Claude Code Agent tool (stub lane), the bounded fallback ladder and the snapshot-grounded children. Engine A's diversity is over the requested ids, like engine B's (R04 sections 3.3, 4.1; `openai_compat.py:467-470`), so retiring it does not lose a served-model measurement (R06's "served" wording is corrected by R04, see synth-01 2.6). The fail-closed verdict map, atomic write-back and recursion marker live in `runner.py` and do not depend on the engine (R06 section 4.4). The engine becomes a prose pipeline whose correctness depends on an LLM orchestrator performing deterministic steps (R06 section 5.1). |

### Option 4: engine B's data model and kernel as the shared core inside engine A's execution shell; deterministic steps move into code

| Aspect | Assessment |
|---|---|
| Effort | L (basis: a contract serializer, a card writer that owns file names, a `merged-verdict.yaml` finalizer, parity recorded by code; the checking code already exists, R06 section 8(b)) |
| Risk | Medium (basis: the byte-identical set above must hold; R06 labels this composition "my reading ... not a verified fact about the repo") |
| Reuse of existing code | `panel_lint._ev1` and `lint_panel_contract`, `reflect_shadow_exit.recompute_parity` and `card_headers`, `ensemble.parse_adversarial_contract`, `extract_convergence_score`, `extract_adversarial_status` (`ensemble.py:633-697`), the `superclaude review` kernel commands (R06 section 8(b)) |
| Files and systems affected | `cli/reflect/{runner,contract,panel_lint,ensemble}.py`, `cli/review/*`, SKILL.md shadow steps 1, 2, 5 (assembly), 6, 7, 8, 10, `reviewer_briefs_materialized` in `refs/reviewer-spec.md:78` versus the two lists |
| Pros | All observed Stage 2 failures are deterministic file, copy or key-set defects that code can write (R06 section 6.2); review judgment stays with the reviewers: reviewing, deviation classification, blind calibration, the debate and the validator's re-read stay LLM work (R06 section 8(b)). Keeps the fail-closed shell and its 36-test matrix (R06 section 8(d)). |
| Cons | Precondition: engine A's contract has no producer for `remediation_*` or deviation fields, so `--fix` becomes live only if the core supplies them (R06 section 4.2). The diversity vocabulary and `merge_method` meaning still need a single decision (the threshold, 0.80, and the single-vendor posture, degrade, are decided by the code, 6.8.c). Passing 20 clean runs would still not measure review quality (R06 section 6 key takeaways). |

### Sub-decision 6.8.b: where the panel enters for workflow and tasklist (DO4, R11)

| Option | Mechanism | Evidence |
|---|---|---|
| (a) keep reflect UC-1 as the only entry | the panel is selected inside reflect (`--t2-engine`); call sites unchanged (`sc-workflow-protocol/SKILL.md:89`, `sc-tasklist-protocol/SKILL.md:1630`) | neither call site passes `--t2-engine`, so no consumer run reaches panel code today; a Stage 10.5 phase scoring 0 to 3 runs `--depth quick --tier 1` and never reads the flag (R11 sections 2.2, 3.2). Interfaces to keep: the closed enum `reflect_status: success | partial | failed | skipped` and `reflect_report_path`, read by workflow, its eval companion test, troubleshoot and auggie-review (R11 section 5.3). Pins: `tests/commands/test_workflow_command.py:243-261`, `tests/tasklist/test_tasklist_cli.py:573-580` stay. |
| (b) direct panel call replacing `:89` and `:1630` | new flag set and new contract keys beside `reflect_status` | needs rewrites of those two pins and a plugin decision: the plugin ships no `sc-reflect-protocol` and no `sc-tasklist-protocol` (R11 section 5.4). |

### Sub-decision 6.8.c: one convergence threshold and one single-vendor posture

| Point | Side 1 | Side 2 | Decision record |
|---|---|---|---|
| convergence score routing | skill: at least 0.75 PASS, at least 0.60 PARTIAL, below 0.60 FAIL (`SKILL.md:703`, `:1317`) | code: any present score below 0.80 degrades, comment names "the incident 0.75" (`contract.py:317-326`); tests pin 0.75 degrades and at or above 0.80 passes (`test_verdict_mapping.py:432-458`); tasklist T5 uses 0.80 (`sc-tasklist-protocol/SKILL.md:1171, :1179`) | Decided by the code: 0.80 is the enforced threshold (`contract.py:310-326`, pinned by the 36-test matrix; synth-06 CV-1, DECIDED-BY-EVIDENCE); the skill prose (0.75 PASS, 0.60 PARTIAL) is to be reconciled with it as a follow-up; no decision record was found for either number (R06 gap 11, OQ-5) |
| single vendor | skill: "warn-only in v1.0" (`SKILL.md:839`, `:1481`) | code: DEGRADED unless `--allow-single-vendor` (`contract.py:286-288`) | Decided by the code: the wrapper degrades on a single vendor unless `--allow-single-vendor` and tests pin it (synth-06 CV-2, DECIDED-BY-EVIDENCE); the skill's warn-only text is to be reconciled with it as a follow-up; no decision record was found (R06 section 5.4) |

### Options comparison table (6.8)

| Criterion | 1: keep both, reconcile | 2: swarm gains B's capabilities | 3: retire swarm | 4: B data model in A shell |
|---|---|---|---|---|
| Maintainability | Two producers, two contract shapes. | One engine, large new machinery. | One engine, prose pipeline. | Deterministic steps in code, judgment in prose. |
| Integration complexity | Low. | Very high. | High. | Medium to high. |
| Reuse potential | Everything. | `ensemble`, `fallback`. | Skill, lint, exit script. | Existing checkers and extractors (R06 section 8(b)). |
| Evidence strength | Verified code and doc conflicts (R06 sections 4, 5). | Verified capability gap (R06 section 2). | Verified loss list (R06 section 8(d)). | Verified failure classes (R06 section 6); composition is an analysis. |
| Blocks future PR review or rf-qa replacement | No by itself; neither engine is a code-review engine: swarm sees tasklist text only, B reviewers are read-only with tools (R13 section 2.2). | How: no tools means it cannot ground code. | No: read-only tool-grounded reviewers fit R13 M5. | No: keeps the contract the future consumers read. |

**Axis status:** `DECIDED-BY-EVIDENCE` for the convergence threshold (0.80) and the single-vendor posture (degrade unless `--allow-single-vendor`): the code enforces both (`contract.py:286-288`, `:310-326`) and the 36-test verdict matrix pins them; only skill prose says 0.75 and warn-only, and that prose is to be reconciled with the code as a follow-up (synth-06 CV-1, CV-2; R06 gap 11 records that no decision record exists for either number). `UNDECIDABLE-BY-EVIDENCE` between options 1 to 4 on the engine: R06 gap 1 leaves open whether the intended design is that the wrapper switches to engine B or that engine A gains exclusion. Decided by evidence: neither engine can absorb the other without losing a capability (R06 section 8(d)); every observed Stage 2 exit failure is a deterministic defect with existing checking code, so those steps can move into code without touching reviewer judgment (R06 sections 6.2, 8(b)); the documents that say the wrapper applies executor-class exclusion are contradicted by the code.

## 6.9 Evaluation

**Description:** what counts as acceptance evidence that a unified panel design works, and who owns the harness. RN lists: shared ground truth (E2: 16 defects, 10 GT of which 5 blocking on designSpec, alias 4 and 3, control 2 and 0), E1 seeded defects (never run), held-out sets, a blind judge, and audits A to F as a reusable `verify-run`.

**How it works (what exists, [CODE-VERIFIED] or recomputed unless marked, R07, R08, R16):**

| Element | E1 | E2 |
|---|---|---|
| Ground truth | none for the 15 combo or 13 pilot runs (`FINDINGS.md:3`, `:42`); a seeded-defect pilot (60 defects = 12 plans x 5) designed and never run (`pilot-design.md:28`, `:68`) | 3 files, 16 items, draft-then-verify-then-drop with `quote_grep_count`, `evidence_ok` and `dropped` reasons; derived from one implement run per plan; authorship unrecorded (OQ-6) |
| Judge | none; AI-labelled 50 cluster pairs (three labelers; TP 21, FP 4, FN 1, TN 24; precision 0.84, recall 0.9545; "NOT human labels") | one Opus call per (row, package), N=1; blindness is id and path anonymisation; completion is only `rc == 0` and parseable `judge.json` (`judge-one.sh:28-30`); no judge transcript and no 12-row re-judge artifact in git |
| Pre-set rule | code gate `scripts/reflect_shadow_exit.py` (13 of 20 runs); thresholds T-1 to T-10 and stop rule S-0 to S-5 are `draft-for-owner-review`, only T-9 was redefined by the owner (R07 section 4) | prose rule in the pilot report; every prose rule reached git together with or after its data (R16 section 3.2) |
| Audits and gates | exit script defects: an empty legacy baseline counts as 0.0 (`:313`); the lint card regex `^reviewer-(\d+)-card\.` (`panel_lint.py:188`) differs from the exit script's `^reviewer-(\d+)\.md$` (`reflect_shadow_exit.py:59`) | six audits A to F, 1,300 flag rows, 257 EXCLUDE; only A and D have a `summary.md`; `fullpkg()` maps 59 control-package flags to designSpec and 11 to all packages, so the AUDIT-CLEAN table is wrong (69 reproduced, corrected 71 to 76); batch j1 is in none of the audits, but a hand audit of its 45 runs found no identity or drop problem and two luna refusals, and the unaudited status does not change "not confirmed" (R08 section 6) |
| Metric definitions | structural and cost signals only | judge-blocking 65 versus real-blocking 38 over 71 valid rows; tokens are reviewer output tokens only (R08 G4) |

**Independence (R16 section 6):** the E1 package is byte-identical to the E2 designSpec candidate (sha256 `044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481`); E1 chose it for E2's ground truth and picked panels from E2's results; both run the same kernel code; two E2 session scripts write into E1's evidence tree (`snap.py`, `rlog-r3.sh`; R01 section 1.2). E1 and E2 are one evidence family, one derivation set. E2's ground truth is concentrated: three of the 14 defect-rich defects account for 131 of 147 catches (89 percent) and four were never caught in 106 runs (R08 G3). No ground truth exists for reflect UC-2, PR code review or rf-qa replacement (R16 section 4.3). The harness files (`run-reviewer.sh`, `judge-one.sh`, `anon-combos.sh`, `final-table.py`) are not tracked at HEAD, hard-code an absolute worktree path, and no `CODEOWNERS` exists (R16 section 5.1).

### Option 1: E2 ground truth and blind judge as the acceptance set (tasklist review)

| Aspect | Assessment |
|---|---|
| Effort | M (basis: the GT and judge scripts live only on the E2 branch; they must be imported with their path arguments fixed, R16 section 5) |
| Risk | Medium (basis: small, concentrated, single-judge, one-run-derived GT; E1 results are not independent confirmation, R16 section 6.3) |
| Reuse of existing code | `ground-truth.json` (3 files), 319 `score.json*` files that all parse and reproduce the per-issue table, `three-way.py` and `final-table.py` (reproduced after patching 5 hard-coded paths) (R08 sections 3, 4) |
| Files and systems affected | a tracked fixture set and judge wrapper (`.dev/eval-workspaces/`, `scripts/`, or the kernel CLI, see 6.9.b); `final-table.py` `fullpkg()` replaced by exact keys |
| Pros | The only ground truth with mechanical checks and a written drop reason per item (R16 section 3.1). Counts, the per-issue table and the committed final table are recomputable from committed data (R08 sections 1, 3, 4). External: gold labels are the remedy the literature uses to separate judge bias from quality (W01 A3, https://aclanthology.org/2025.emnlp-main.86.pdf). |
| Cons | Sixteen items from three plans, one implement run each, so a true novel defect scores as a wrong blocker (R16 section 3.1). Judge N=1 with no committed transcripts (R08 section 8). E1 and E2 are not two replications (R16 section 6.3). |

### Option 2: seeded defects with clean twins (E1 pilot design, E2 planted-set design)

| Aspect | Assessment |
|---|---|
| Effort | L (basis: 12 plans x 5 seeded defects designed, never planted; hold-out sets not built) |
| Risk | Medium (basis: thresholds and stop rule were never approved; seeding author separate from design author is attested, not machine-checked, R16 section 4.1 rows 7, 8) |
| Reuse of existing code | `pilot-design.md` (defect kinds: ordering, missing acceptance, spec-uncovered requirement, wrong file path, cross-task contradiction); the E2 redesign's planted set with a clean twin per plan (`merged-requirements.md:1180`) |
| Files and systems affected | a seeded-plan generator and manifest (hash before the first arm), a judge, scoring scripts |
| Pros | The only route to a ground truth where no implement outcome exists: reflect UC-2, PR review and rf-qa have none and no run in any effort (R16 section 4.3). Clean twins measure false positives. External: ReviewBench-style deduplicated multi-source golden sets and run-to-run variance reporting (W01 D2, https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review). |
| Cons | Designed and never run; thresholds T-1 to T-10 are `draft-for-owner-review` (R07 section 4). Seeded plan defects are plan or spec defects, not code defects (R16 section 4.3). |

### Option 3: a pre-registered hold-out protocol (hash before run, new packages, second judge)

| Aspect | Assessment |
|---|---|
| Effort | L (basis: rule, values file and analysis script committed before the first arm; hold-out documents; confirmation on at least two new packages, `merged-requirements.md:974`, `:986`) |
| Risk | Medium (basis: design only; both source designs state low power: "The plan cannot detect the central estimates of any slot", `:980`) |
| Reuse of existing code | the two brainstorm designs' rules (collaboration `merged-requirements.md:957-992`, redesign `:1000`, `:1079`, `:1180-1197`); the E2 judge scripts, which the collaboration design requires "unchanged and sha256-pinned" (`:953`, `:1061`) though the committed file carries a hard-coded worktree path (R16 section 5.1) |
| Files and systems affected | commit ordering discipline, hold-out store, analysis script, judge pinning |
| Pros | Proves rule-before-data by `git log` instead of mtime (R16 section 4.1 row 2). Names a package set neither E1 nor E2 touched. Second-judge sample and per-batch API-error audit (R16 section 3.3). |
| Cons | A second judge on 15 percent of run-packages is the same Opus family, so it measures agreement and not an independent family (R16 section 3.3). Depends on files that exist only on the E2 branch. External: raw agreement overstates chance-corrected agreement by 33 to 41 points and stable verdicts across reruns are not correctness (W01 AE-1; external, transfer unverified). |

### Option 4: structural acceptance only (executable `verify-run`, Tier S), quality later

| Aspect | Assessment |
|---|---|
| Effort | M (basis: audits B, D, F re-run today from committed data; A, C, E need run-time records the product does not write, R16 section 7.1) |
| Risk | Low (basis: structural checks only; but see Cons) |
| Reuse of existing code | the uniform `flags.tsv` layout of audits A to F, `report_sha256` already stored per ledger entry (`ledger.py:146`), the full parse-error list already returned by `parse_block` (`findings.py:124-196`), the fixed E1 exit script |
| Files and systems affected | the ledger entry (raw, kept, rejected counts: `ledger.py:141-149` stores five fields), a run record with served model, tool use and judge completion (6.5.b), a manifest of expected (row, package, reviewer) cells |
| Pros | Removes the verified classes: exact-key lookups, judge completion checked in code, "unaudited" as a reported state (R16 section 7.2). Conservation `raw == kept + rejected-with-reason` turns audit D into a one-line read (R16 Part 7 key takeaways). |
| Cons | It measures orchestration and structure, not review quality: the Stage 2 exit scores file-name and copy discipline, and passing 20 clean runs would not show quality (R06 section 6 key takeaways; R07 N-1, N-2). Model-identity and judge-completion checks depend on kernel records that do not exist yet (R16 section 7.3). |

### Sub-decision 6.9.b: who owns judge, ground-truth registry and `verify-run`

| Option | Moves | Evidence for | Evidence against |
|---|---|---|---|
| O1 kernel-owned invariants and a `superclaude review verify-run` command | served-model record, `incomplete` outcome, raw and kept counts, the verifier | skills reach package behaviour only through the `superclaude` CLI (R18 section 4 a4); the kernel already owns the `findings.py` rules audit D copied (R16 section 2.4) | grows the shipped CLI with maintainer tooling; judge and GT still need a home |
| O2 repo-relative `scripts/` plus tests | judge, anonymiser, table builder, GT registry check | five `scripts/reflect_*.py` each with a test file (R16 section 5.2) | not installed for users; skills cannot call it (R16 section 5.3) |
| O3 stay under `.dev/` | everything as is with paths fixed | matches `.dev/README.md:5` | untested; this is the state that produced the `fullpkg()` bug and the unaudited batch (R16 section 5.4) |

### Options comparison table (6.9)

| Criterion | 1: E2 GT and judge | 2: seeded defects | 3: pre-registered hold-out | 4: structural only |
|---|---|---|---|---|
| Maintainability | Fixture and scripts with paths as arguments. | Generator plus manifest. | Process discipline plus pinned scripts. | A checker plus run-time records. |
| Integration complexity | Medium (import from the E2 branch). | High. | High. | Medium. |
| Reuse potential | Highest (data exists). | E1 pilot design, E2 planted-set design. | Both brainstorm designs. | Audit flag layouts, ledger fields. |
| Evidence strength | Recomputed counts; weak inference (R08 section 7). | Design only. | Design only. | Verified defects and reproducible audits B, D, F (R16 section 7). |
| Blocks future PR review or rf-qa replacement | How: no GT for PR review or rf-qa, so acceptance there has nothing to run against (R16 section 4.3). | No: the route for modules without natural GT. | No: per-use-case hold-out. | No. |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE` on the metric of record (GT items found at any severity, found in a row flagged blocking where the item is blocking-in-implement, wrong blockers, or control found; only the pilot rule names two, R16 question 1), on whether the E2 GT is acceptable as the tasklist GT, and on who writes the hold-out and seeded sets (R16 questions 1 to 3). Decided by evidence: E1 and E2 are one evidence family and acceptance needs a package set neither used (R16 section 6.3); no tier-G evidence exists in either effort (R16 section 4.2); the harness has no owner and absolute paths.

## 6.10 Variants

**Description:** what to do with the installed-only E3 variants (five `spec-panel-*` commands, the `finding-grader` agent, four skills) and the ideas in them. RN lists: keep them installed, archive them, or fold their ideas (owner counting rule, scoped-PASS coverage statement, fail-closed parsing, provenance of the actual model, fix map per hunk, computed re-review surface).

**How it works (state at 2026-11-14, [CODE-VERIFIED], R14 sections 3, 4, 7):**

| Fact | Evidence |
|---|---|
| 17 installed files (5 commands: armb 472, ponytail 483, diffgate 481, ledger 475, stoprule 481 lines; `finding-grader.md` 35; skills `sc-diffgate`, `sc-fix-audit`, `sc-review-ledger`, `sc-spec-panel-stoprule-protocol` with scripts of 1,740, 1,131, 2,668 and 2,050 lines) match the install log by full sha256 (17 of 17, mtime 2026-11-08 23:42:21). | R14 section 3.1 |
| They are not in `src/`, not in `.claude/`, not in `tests/`, and `superclaude install` neither installs nor removes them (`install_commands.py:41-79`, `install_skills.py:88-115`); the only copies in the repo are archives under `.dev/experiments/346-validation/phase5/final-bundle/builds/` and a mirror under `.dev/research/346-review-loop-experiments/exp346/`. | R14 sections 3.1, 3.2 |
| The variant commands lack `follow-up candidates` and the prompts hard gate; only stoprule has an `## Activation` heading; none has the headless `--unattended` contract the master command and nested calls depend on (stoprule has no `## Unattended mode`, ledger refuses `--unattended`). The variants are built on the 472-line PR 427 text (ARM B differs from it in one line, the `name:`), and the 486-line `spec-panel.md.bak.20261111T164114Z` that the install log hashes as the pre-install `spec-panel.md` is the master text of 2026-11-08, not the PR 427 text (corrects the "PR 427 era" wording of slice 12). | R14 sections 3.1, stale-documentation rows 4 and 9 |
| They re-implement the loop in stdlib-only scripts and share no code, schema string or grammar with `cli/review`; two of them use `origin` with other meanings. | R03 section 3; R02 section 7 |
| Phase-5 FINAL-REPORT states "Convergence not proven; no validated winner" (`FINAL-REPORT.md:42`); every figure that can be recomputed here is exact (sizes, hashes, growth, ledger counts, the 91-byte ponytail audit, three model changes read from surviving transcripts); six control and 427-arm measurement files are absent, so the control baseline stays unverified (OQ-7). The control arm 2 read the finished answer (`origin/master` peeks), and excluding it would move the control proxy from 6 to 8, which the final report does not mention. | R14 sections 1, 2, 6 |
| PR #479 with #478 is the shipped prose-only substitute for the never-written refactor spec: the 346Claude plan says "REFACTOR-SPEC was never written; A2 replaces it" (`346-plan-merged.md:202`) and every A2 clause is in `spec-panel.md:256-264` except the words "command version"; the owner's formal acceptance is not documented (OQ-8). | R14 section 4 |
| Personal-over-project shadowing: D9 measured that `~/.claude/commands/sc/spec-panel.md` beat the worktree copy on 2026-11-08; official docs state it for skills; today the two copies are identical, so nothing is shadowed. | R14 section 3.3 |

**The six values and their evidence (R14 section 7.1):**

| Value | In shipped master already | What only a variant adds | Variant-produced measured support |
|---|---|---|---|
| c1 owner counting rule (deferred, demoted, outside CRITICAL/MAJOR stays counted open) | verdict side as prose (`spec-panel.md:262`) | `U3`/`W`/`O` metrics (`review_ledger.py:2389-2445`) | none (single loops) |
| c2 scoped-PASS coverage statement | the fixed string `scoped PASS: changed lines + prior blockers` (`:262`) | held-count disclosure and a deferred list (`diffgate.py:1287-1292`) | none; no matched control audit |
| c3 fail-closed parsing | report level (`spec-panel.md:260`) | quorum is absent in the CLI: per-line fail-open (`ledger.py:150-157`) | incident evidence: ponytail's invalid zero, stoprule's integrity mismatch |
| c4 provenance of the actual model | a self-reported header line (`:258`) | observed model per response from the transcript | incident evidence: 3 of 3 measured loops changed model |
| c5 fix map per hunk | prose (`:263`); `fixmap-v1` exists in the CLI | the hunk-coverage check (`diffgate.py:1394-1468`) | none; the cause of diffgate's smaller growth was not separated |
| c6 computed re-review surface | prose only | `begin` hunk building (`diffgate.py:1108`) | the final restricted review covered about 2 percent of the document and a later audit found 4 MAJOR |

### Option 1: keep the variants installed-only (status quo)

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Medium (basis: private machine state that cannot be rebuilt from `src/`; shadowing hazard on edit of the same-named command) |
| Reuse of existing code | the installed scripts as they were measured (17 of 17 hashes) |
| Files and systems affected | `~/.claude/commands/sc/spec-panel-*.md`, `~/.claude/skills/sc-{diffgate,fix-audit,review-ledger,spec-panel-stoprule-protocol}/`, `~/.claude/agents/finding-grader.md` |
| Pros | Keeps the measured instruments runnable; nothing to do. |
| Cons | They add five command names and four skill names to every session on this machine (R14 section 3.2, a reasoning from discovery rules, not separately tested); they lack the headless contract; the word "ledger" would be a third meaning next to the CLI ledger and the research variant (R10 Unit 3). A reader of a clean checkout cannot see them. |

### Option 2: archive them (remove from `~/.claude/`, keep the `.dev/` archives)

| Aspect | Assessment |
|---|---|
| Effort | XS (basis: a manual removal under `~/.claude/`, because the installer does not remove them, R14 section 3.2) |
| Risk | Low |
| Reuse of existing code | the archives under `.dev/experiments/346-validation/phase5/final-bundle/builds/` and `.dev/research/346-review-loop-experiments/exp346/` |
| Files and systems affected | the same 17 installed files, removed; `docs/reference/review-panel-live7.md` and the experiment docs keep their links |
| Pros | No variant has a valid repeated result and none is recommended by the final report (R14 section 7.3). Removes the shadow hazard and the session clutter. `minfix` was never built (R14 section 7.2). |
| Cons | The ponytail audit depends on an external plugin skill (`ponytail:ponytail-review`, `auditor-brief.md:7-10`); the scripts would only be runnable from the archive. The owner decides (R14 question 5). |

### Option 3: fold the ideas into the core and modules (contracts, not scripts)

| Aspect | Assessment |
|---|---|
| Effort | L (basis: the six values above; scripts total 7,589 lines and are not reachable from `src/`) |
| Risk | Medium (basis: each value is a design hypothesis; two have incident evidence, the rest none) |
| Reuse of existing code | `fixmap-v1` and `ledger revise` (CLI), `review-capture/1`, `telemetry.py:49` `model.observed`, the master prose clauses (R14 sections 7.1, 7.4) |
| Files and systems affected | `ledger.py` (a status that records why a finding is not blocking), `spec-panel.md` clause 262 (held-count disclosure, "command version"), a transcript reader for the observed model, module-level hunk checks |
| Pros | Carries what has incident evidence: provenance from the transcript (3 of 3 measured loops changed model and only the transcript shows it) and fail-closed parsing (R14 section 7.3). Diffgate's changed-surface and fix-map ideas map onto the PR diff, where `in_diff` and commit-delta handling already exist in `pr_submit` (R14 section 7 key takeaways). |
| Cons | The value of each fold is untested; "which status machine" (`resolved_check` versus `fixed/verified`) is an open decision (R14 question 2); the observed model needs a transcript source in headless workers (R14 question 4). |

**Not offered by the evidence:** promoting a variant script as a product path. No variant has a valid repeated result, the scripts are stdlib-only and 7,589 lines, and the ponytail audit edited 91 bytes (R14 sections 6.2, 7.3).

### Options comparison table (6.10)

| Criterion | 1: keep installed-only | 2: archive | 3: fold the ideas |
|---|---|---|---|
| Maintainability | Private state outside any checkout. | Nothing to maintain. | Contract text and small code per value. |
| Integration complexity | None. | None. | Medium: ledger statuses, transcript reader, brief text. |
| Reuse potential | Instruments only. | Archive only. | Highest for the six values. |
| Evidence strength | 17 of 17 hashes verified (R14 section 3.1). | Final report: no validated winner (R14 section 2.4). | Two values with incident evidence; four hypotheses. |
| Blocks future PR review or rf-qa replacement | No: shadows nothing (R14 section 3.2). | No. | No: c5 and c6 generalise to PR diffs (R14 section 7 key takeaways). |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE` between keep and archive: it is a machine-state and owner decision (R14 question 5), and the only evidence is that the installed state equals what was measured. Decided by evidence: no variant is validated (`FINAL-REPORT.md:42`), a variant script is not supported as a product path (R14 section 7.3), and the transferable pieces are contracts and invariants, not scripts (R14 section 7 key takeaways).

## 6.11 Future modules (PR code review and rf-qa / rf-qa-qualitative replacement)

**Description:** how the design treats the two future uses so neither is blocked later. RN: PR code review (location type, 18 versus 6 categories, 5 versus 3 severity tiers, cap, third-party reviewers, fork-only rules) and rf-qa replacement (read-write semantics, checklist plus confidence gate, 8-lens pack, the `/task` lens-gate pattern as a first step).

**How it works (blockers per use case, [CODE-VERIFIED], R13 section 7):**

| Use case | Blocker | Evidence | Class |
|---|---|---|---|
| PR | `pr_submit` needs one integer `line` per finding and drops findings without it | `fsm.py:364-372` `is_groundable`; `models.py:168-194` | SOFT through an adapter (`citations[0].line_start`); HARD for a text-anchor-only finding |
| PR | categories: findings-v2 accepts 6 spec categories, the router knows 18; an unknown category passes the router un-clamped | `findings_v2.py:109-110`; `severity_router.py:34-53`, `:166-168` | HARD for v2; SOFT in the router |
| PR | lens vocabulary closed to spec, reflect-pre, reflect-post | `findings_v2.py:36`, `:143-145` | HARD |
| PR | 5 severity tiers with floors and ceilings against 3 labels plus `blocking`; Medium has at least six uses | `models.py:106-113`; R12 section 3 | SOFT (lossy mapping) |
| PR | two named third-party reviewers, bot identities, completion markers; `Output Contract` `reviewers` object has two keys | `reviewers.py:41, 47-60, 395` | SOFT adapter; additive contract key |
| PR | skill must run in the main session; fork-only rule is code (`pr_target_ok`, `origin_ok`, `fsm.py:542-665`) plus prose; a panel must contain no `gh` or `git` | `SKILL.md:47-49`; `severity_router.py:10-13` | HARD constraint on where it is invoked |
| rf-qa | rf-qa reviews and edits (`fix_authorization`); `/task` lens agents are "report-only" by prompt but spawned with `bypassPermissions` and write-capable tools | `task/SKILL.md:225, 241, 254`; `rf-qa.md:4-5` | HARD design point: reviewers mechanically read-only |
| rf-qa | checklist plus computed confidence gate `VERIFIED / (TOTAL - UNVERIFIABLE) * 100` (`rf-qa.md:505`), untested | `rf-qa.md:484-534`; no test (R13 section 5) | HARD for finding-driven panels |
| rf-qa | lens pack and floors: 8 standard lenses, 3+3 to 6+6 agents by output size, "1-2 agent QA gates are PROHIBITED" | `task/SKILL.md:196-203`, `:226-245` | HARD for `/task`; templates have neither lens nor agent-count rule |
| rf-qa | 44 structured `subagent_type: rf-*` lines in 8 SKILL.md files and 175 prose spawn lines in 7 skills; tests are 23 static-pin files with no behavioural oracle | R13 sections 4.2, 5 | SOFT but wide |

The minimum exposure R13 section 8 derives (M1 to M14): M1 finding location as a citation list with optional anchor and a locator-agnostic `annotate` and citation-keyed ledger rows; M2 category, lens and severity vocabularies as module inputs; M3 optional passthrough fields (`in_diff`, `confidence`, `original_line`, `reviewer`); M4 an optional `lens` per panel slot; M5 mechanically read-only reviewers with the lens as free text; M6 a separate optional reviser role; M7 cap, blocking rule and severity-to-route mapping as module parameters; M8 one "reviewer failed" finding plus regression and monotonicity guards; M9 an optional checklist output mode; M10 purity (no network, `gh`, `git` or repo constants); M11 an adapter spec to `list[Finding]`; M12 the main-session invocation rule; M13 a replay fixture as a behavioural oracle; M14 a decided shipping form with the plugin mirror. R13 states that only M1 to M4 are places where today's code would reject a use case outright; everything else is policy passed in as parameters or adapter work in the consumer. The two use cases overlap on exactly three needs: module-supplied category, lens and severity sets; per-slot lens in the template; mechanically read-only reviewers (R13 section 7 key takeaways).

### Option 1: exposure-first (the core ships M1 to M14 now; no consumer is ported)

| Aspect | Assessment |
|---|---|
| Effort | M (basis: M1 to M4 touch the parser, ledger and template; M5 to M14 are interface and policy statements, R13 section 8) |
| Risk | Medium (basis: closed sets and limits are pinned by tests; templates have no lens key and slot keys are closed, `panel.py:46`, `:215-216`) |
| Reuse of existing code | `findings_v2` citations and roles; `reflect-reviewer`'s free-form `persona_lens` (`reflect-reviewer.md:56`); `evidence-validator` as the shared "does the cited line exist" gate (`SKILL.md:304` of pr-submit; R13 section 2.2); the `/task` lens-gate shape (R13 section 4.3) |
| Files and systems affected | `findings.py`, `findings_v2.py`, `ledger.py`, `panel.py` and templates, `tests/review/`; the plugin mirror decision (M14: the plugin ships no pr-submit, auggie-review, rf-* or reflect-reviewer, R13 P14, R11 section 5.4) |
| Pros | Cheap now and expensive to retrofit once E1, E2, E3 consumers pin the formats (R13 section 8 header). It removes the only outright rejections (M1 to M4). |
| Cons | Ships interface for consumers that do not use it yet; M13 adds a behavioural fixture scope (R13 section 5: rf-qa has none). |

### Option 2: consumer-first through adapters (PR via an adapter to `pr_submit.Finding`; rf-qa replacement starts at the `/task` phase gate)

| Aspect | Assessment |
|---|---|
| Effort | L (basis: an adapter and a completion rule for a local panel; the `/task` gate call changes; mechanical read-only enforcement and a checklist mode, R13 R1 to R3) |
| Risk | Medium (basis: 50 test files pin `Finding`, the severity router and the FSM, so they stay untouched; `/task` lens agents run with `bypassPermissions` today) |
| Reuse of existing code | `reviewers.py` ("Everything after a normalized Finding is shared"); `severity_router.remap_severity`, `route`; `/task` gate (8 lenses, floors, one fix agent, verification round, max 2 fix cycles) |
| Files and systems affected | a new adapter module (no `gh` or `git` in it), `pr_submit/reviewers.py` or a pre-step, `task/SKILL.md` lens-gate text (`:188-286`), `rf-qa` agent files, the Output Contract `reviewers` object if the panel becomes a third reviewer name |
| Pros | Smallest blast radius: `Finding`, `Severity` and the FSM stay untouched (R13 P13). The `/task` gate is the one place that already separates read-only lens agents from one fix agent, so replacing rf-qa starts there and not at seven skills (R13 section 4.3). A local panel enters without a bot login or a GitHub thread (R13 section 1.4). |
| Cons | A local panel has no completion marker, so its own completion rule is needed (R13 section 1.4). Adding a third reviewer name changes the pr-submit Output Contract (an additive key; not checked against the tests, R13 P6). The text-anchor loop cannot enter: findings need a positive integer line (R13 section 2.1). |

### Option 3: defer both (build neither exposure nor adapter; add on demand)

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | High (basis: location type, vocabularies and lens are hard-coded and pinned today, `findings.py:14-22`, `findings_v2.py:36`; rf-qa has no behavioural oracle, R13 section 5) |
| Reuse of existing code | n/a |
| Files and systems affected | none now; each later consumer retrofits the parser, ledger and templates |
| Pros | Scope discipline: R13 lists porting `auggie-review` or `pr_submit`, touching `conflicts.py`, `merge_guard.py`, `classifier.py`, rewriting seven rf-* skills and an rf-analyst replacement as not needed now. |
| Cons | Every later consumer retrofits after the formats are pinned (R13 section 8). The PR path can still use an adapter (R13 P1), but a ledger-based rf-qa replacement cannot take citation-only findings until M1 is done. |

**External context (W04, W01; not evidence of repo behaviour):** a finding record projects onto reviewdog rdjson, SARIF and the GitHub review `comments[]` fields (`path`, `line`, `side`, `start_line`, `commit_id`), so export adapters are the extension point and the posting step needs a "postable" check because lines outside the diff are rejected at posting (user-reported, https://github.com/orgs/community/discussions/202426; W04 sections 3, 6). Severity routers in practice are configuration over an internal ordinal, and vendor vocabularies differ (Codex P0 to P3 with only P0 and P1 shown on GitHub, CodeRabbit critical to trivial, SARIF error, warning, note) (W04 sections 4.1, 4.2, 4.5). The resolvable unit of a PR thread is a GraphQL thread id (user-reported; W04 section 5.1). The union of four automated reviewers passed 41.5 percent of tests built from human reviews, a limit on any replacement claim (W01 D4, https://arxiv.org/html/2603.23448v2).

### Options comparison table (6.11)

| Criterion | 1: exposure-first | 2: consumer-first via adapters | 3: defer both |
|---|---|---|---|
| Maintainability | One contract surface with module inputs. | Adapters per consumer; core small. | Retrofit later per consumer. |
| Integration complexity | Medium: parser, ledger, templates. | Medium to high: adapter, `/task` gate, read-only enforcement. | None now. |
| Reuse potential | `findings_v2` roles, `persona_lens`, `evidence-validator`. | `reviewers.py` normalisation, router, `/task` gate shape. | n/a |
| Evidence strength | Blockers verified (R13 section 7); the M-list is an interface derivation (R13 section 8). | Blockers and call sites verified; no run of either use case. | Retrofit cost inferred from pinned formats. |
| Blocks future PR review or rf-qa replacement | No: it removes M1 to M4. | PR: no (adapter). rf-qa: only the `/task` gate path opens; a ledger-based replacement still needs M1. | How: yes for a ledger-based rf-qa replacement until M1 to M4 exist; PR via adapter stays open. |

**Axis status:** `UNDECIDABLE-BY-EVIDENCE` between exposure-first and consumer-first: R13 question 1 (findings-v2 as the single wire format versus PR keeping its own `Finding`) reads "adapter now, extensible v2 later", a reading and not a measurement; question 4 (panel as a third reviewer name in pr-submit's `REVIEWERS` versus a separate pre-step), question 2 (is the `/task` gate the agreed first rf-qa target) and question 5 (which "eight lenses": the swarm registry's or `/task`'s QA lenses, two different sets) are owner decisions; the cost of a local panel per PR round is not measured anywhere (OQ-9). Decided by evidence: M1 to M4 are the only places where today's code rejects a future use case outright, and the two use cases overlap on three needs (R13 section 7 key takeaways).

## Axis status summary (for the conflict log; no option is ranked)

| Axis | Status | Reason in one line |
|---|---|---|
| 6.1 Core shape | `UNDECIDABLE-BY-EVIDENCE` (A, B, C); D decided as "defers, leaves verified defects" | no run compares shapes; same locator and verdict work under A, B, C |
| 6.2 Finding contract | `UNDECIDABLE-BY-EVIDENCE` (open versus closed keys; one wire format versus adapters); ledger path needs locator-agnostic annotate is decided | variants split on unknown keys; R13 Q1 is a reading |
| 6.3 Limits policy | `UNDECIDABLE-BY-EVIDENCE` (truncate, re-ask, combination); keep-and-warn recovers nothing is decided | re-ask recovery never measured; truncation bound assumes locate success; E1 and E2 texts conflict |
| 6.4 Quorum and verdict | `UNDECIDABLE-BY-EVIDENCE` | no quorum rule in code, no external study on findings, tests pin the fail-open behaviour |
| 6.5 Dispatch | `UNDECIDABLE-BY-EVIDENCE` (mechanism); served-model-from-transcript is decided | depends on whether non-Claude reviewers are in scope; no run compares mechanisms |
| 6.6 Collaboration | `UNDECIDABLE-BY-EVIDENCE` | no exchange arm measured against the static kit; act-rate probes disagree |
| 6.7 Process redesign | `UNDECIDABLE-BY-EVIDENCE` (Sweep Sheet versus Recipe Ledger); duplication finding is decided | design only, 0 code, planning numbers, no hold-out |
| 6.8 Reflect engine | `UNDECIDABLE-BY-EVIDENCE` (engine choice); threshold (0.80) and single-vendor posture (degrade) are decided by the code (synth-06 CV-1, CV-2); "mechanical steps can move into code" is decided | R06 gap 1 (engine intent); no decision record exists for the threshold or vendor posture, the code decides them |
| 6.9 Evaluation | `UNDECIDABLE-BY-EVIDENCE` (metric of record, GT acceptability); E1 plus E2 is one evidence family is decided | R16 questions 1 to 3 |
| 6.10 Variants | `UNDECIDABLE-BY-EVIDENCE` (keep versus archive); "no variant validated" is decided | machine-state owner decision |
| 6.11 Future modules | `UNDECIDABLE-BY-EVIDENCE` (exposure-first versus consumer-first); M1 to M4 are the outright rejections is decided | R13 questions 1, 2, 4, 5 |

## Adjudicated winners by axis (added by the adjudication fold, item 5.50)

The rule at the top of this file (no winner is picked here) holds for every section above: those sections are unchanged. This section is the only place in this file that records a winner, and every entry is the winner of a `/sc:adversarial --compare` debate read from `reviews/adversarial/<slug>/ADJUDICATION-RESULT.md` (paths relative to the task folder; slot names and conditions in synth-06 6.12.9.1). Every debate returned a hybrid it produced itself on a named base, status `partial`, depth `standard`; "winner" below names the option the hybrid is built on and what it takes from the others. An axis is "closed" when its debate returned a winner; the unaddressed invariants stay open (synth-07 7.3, synth-10 9.10).

| Axis | Debate slot (synth-06 name) and folder | Winning option | What the winner takes from the other options | Status of the axis |
|---|---|---|---|---|
| 6.1 Core shape | C-01 `core-shape-and-finding-contract` | Option C: thin shared contract, per-module engines (base Variant B) | Option A's single anchor-status change (surface anchor status in the per-row `### Lx` block); convergence to one engine (Option A) only when trigger T-a, T-b or T-c fires; Option D's "fix the shared defects" for the parts that are shared (limits, repair, ids, references); Option B (v1 package as the core) not adopted | Closed; HIGH invariant INV-003 open |
| 6.2 Finding contract | C-01 (keys, locator) and C-10 `pr-review-wire-format-and-slot` (PR wire format) | Option 1 (two grammars, adapters) with shared ids, limits constants, repair step and reference list; unknown keys open in both parsers; for PR review an adapter to `pr_submit.Finding` | Option 2's superset grammar and locator-agnostic `annotate` were withdrawn in C-01 (the "ledger path needs a locator-agnostic annotate" fact stays true; the design keeps citation-only findings out of the v1 ledger instead); Option 3 (closed contract) not adopted | Closed for keys, locator and PR wire format; the `prior` semantics belong to 6.4 |
| 6.3 Limits policy | C-06 `limits-repair-policy` | Option 4 as modified: cut of the three location fields (`anchor`, `anchor2`, citation `quote`) to 200 flattened characters in code behind `repair=False`, one re-ask for the rest | Option 2's fail-closed rule (dropped-blocking refusal with acknowledgement) and Option 3's visibility (itemised drop record with `blocking_state`) added; the claim cut (Option 1 for `claim`) is unresolved | Closed for location fields and refusal; claim cut open (synth-10 Q-60) |
| 6.4 Quorum and verdict | C-02 `ledger-clearing-and-verdict-authority` and C-03 `merge-verdict-policy-and-quorum` | Option 2 (ledger-derived verdict, recorded quorum, explicit clearing) for the v1 ledger; any-blocking union with a quorum refusal as the merge policy | Option 3 (reflect `derive_verdict` as shell) stays the reflect engine's verdict; Option 4 (blind grader) not adopted for the core; Option 1 (today's rule) rejected for clearing | Closed; three HIGH invariants of C-02 and two of C-03 open |
| 6.5 Dispatch | C-07 `dispatch-and-launch-mechanism` | Option 1 (class word on the Agent `model` argument) shipped now, stated as data per environment (the Option 4 idea) | Option 2 (`claude -p --model <raw id>`) is gated by G1-G3, not built; Option 3 (swarm HTTP) unchanged inside reflect engine A; no packaged `gateway.launch` fill | Closed for what ships now; the later launcher is conditional |
| 6.5.b Run record | C-08 `run-record-and-served-model-capture` | Option (a) (per-run `events.jsonl`, manifest with a lock, `review-telemetry` as the cross-run export) as modified | `review-telemetry/1` with a `strict` mode instead of `/2` (Option (b) in part); no `rev`, no usage in the manifest (Option (c) rejected); memory-writer move deferred | Closed; 13 HIGH invariants open |
| 6.6 Collaboration | C-12 `collaboration-exchange-capability` | Option 2 (static move kit) as the unconditional layer, `kit: off` until gated | Option 3 and Option 4 (exchange) not built; built only on a three-part trigger; Option 1 (no collaboration) is the off state | Closed (staged); premise re-check open (Q-39) |
| 6.7 Process redesign | X-13 (synth-06 C-13) `process-redesign-modules` | Option 1 (Sweep Sheet shape), built only as the optional reusable pieces of Option 4 (card format, row block, advisory rowcheck) | Option 2 (Recipe Ledger) demotion and promotion not built; extractors and slot-keyed binding reserved in the document | Closed; 2 HIGH invariants open |
| 6.8 Reflect engine | C-04 `reflect-tier2-engine-composition` | Option 1 (keep both engines) now, plus the code-owned write side of Option 4 as comparison helpers | Option 4's engine composition, Option 2 and Option 3 deferred: one named single-engine decision, not scheduled | Closed for now; owner question open (Q-09) |
| 6.8.b Entry for workflow and tasklist | C-05 `consumer-entry-effect-and-delivery` | Reflect UC-1 stays the only entry; advisory at Wave 4; Stage 10.5 "advisory-blocking"; blocking at T5; no plugin copy | A direct panel call rejected for this release | Closed; 7 HIGH invariants open |
| 6.8.c Threshold and single vendor | none (decided by the code, synth-06 CV-1, CV-2) | 0.80; degrade unless `--allow-single-vendor` | none | Decided by evidence |
| 6.9 Evaluation | X-14 (synth-06 C-14) `eval-acceptance-and-harness-owner` | A combination: Option 4 (structural acceptance, Tier S) plus Option 3 (pre-registered rule, Tier Q) plus Option 2 (seeded defects with clean twins, Tier G); Option 1 (E2 ground truth) is a derivation set | The metric of record is items found in a blocking row where the item is blocking in implement | Closed; 12 HIGH invariants open |
| 6.9.b Harness owner | X-14 | Judge, ground-truth registry and `verify-run` as a tested `scripts/` plus `tests/` set | Kernel `verify-run` deferred, not rejected | Closed |
| 6.10 Variants | none (no debate slot) | not adjudicated | none | Open owner machine-state decision (synth-10 Q-38) |
| 6.11 Future modules | C-10 and C-11 `rfqa-first-step-and-readonly-scope` | Option 2 (consumer-first through adapters): PR review through a pure converter, report-only first release; rf-qa from a lens-level first change at the `/task` phase gate | Option 1's exposures remain prerequisites (FX-5 category parameters, read-only reviewers); no panel engine inside any rf-qa gate in the first change | Closed for the first step of each; promotion decisions open |
| Tasklist Medium (6.2 sub-question) | X-15 (synth-06 C-15) `tasklist-medium-and-fidelity-vocab` | Module-data label map, nothing new in the core, fidelity prompt outside the core | Whether Medium blocks is UNRESOLVED (H+ versus A+) | Partly closed; the Medium question open (synth-10 Q-89) |

## Interactions between axes (shared prerequisites, not an order)

| Shared item | Appears in | Source |
|---|---|---|
| a locator-agnostic `annotate` and citation-keyed ledger rows (M1) | 6.1 A and B, 6.2 options 2 and 3, 6.11 option 1 | R13 M1; `findings.py:346-349` |
| a repair step before `findings_v2.parse_block` | 6.3 options 1, 2, 4; 6.2 option 3 (whole-input refusal) | R02 section 5.3 |
| served model taken from the transcript | 6.5 all options and 6.5.b, 6.9 option 4, 6.10 option 3 | R04 section 4; R14 section 6.1 |
| the verdict function and its inputs | 6.4 option 3, 6.8 options 1 and 4, 6.8.c | R03 section 4.2; R06 section 5.3 |
| mechanically read-only reviewers | 6.5 option 1, 6.6 option 4, 6.7 option 2, 6.11 | R09 section 4.2; R10 Unit 5; R13 R1 |
| the `blocking` boolean, label maps and the "Medium" token | 6.2, 6.4 cap policy, 6.11 | R12 sections 2, 3, 8 |
| one owner for class, vendor and tier lists | 6.5 option 4, 6.8 | R04 sections 5, 8 |

## Corrected claims (the [CODE-CONTRADICTED] items met while writing; the corrected form is used above)

| Claim as written in a source | Corrected statement | Source |
|---|---|---|
| E2 run-2: the `cli/review` change is "#519 + #518" | #519 alone changed 17 `cli/review` files; #518 changed none (one test file under `tests/review`) | R01 section 1.3 |
| E2 run-2: "reflect has no panel/tier code" | true only for the code-driven wrapper; `SKILL.md:87, :338-349` run the panel through the tier JSON in shadow mode and the kernel is reflect-shaped | R01 section 2 |
| E2 run-1 D14: "No tasklist review step exists" | `sc-workflow-protocol/SKILL.md:89` and `sc-tasklist-protocol/SKILL.md:1630` call reflect UC-1; neither passes `--t2-engine` | R11 section 5.2 |
| E2 run-1: "alias GT3 found once" | alias GT1 was found once; GT3 twice | R08 section 3 |
| `COMBO-REPORT.md:292`: dropped lines are "discarded with no error" | merge emits a first-error warning and `merge-stdout.txt` carries it; the dropped ids and count are not itemised | R08 section 5 |
| `COMBO-REPORT.md:292`: "four verdicts flipped" | 3 flips plus 5 total-loss merges | R02 section 5.1; R08 section 5 |
| the per-model list (luna 30, ember 33, ...) as the "49 blocking" breakdown | it sums to 92 (all dropped lines); the 49 are split by reason only | R08 section 5 |
| "16 empty terra reviews" | 14 terra plus 2 luna | R08 section 5 |
| slice 12: Medium "has four meanings" | at least six; seven severity vocabularies is definition-dependent (six label sets plus two orthogonal axes) | R12 sections 2.2, 3 |
| slice 12: "185 spawn lines over 7 skills" | 175 prose spawn lines in 7 skills (247 per line and agent); 44 structured `subagent_type: rf-*` lines in 8 SKILL.md files is exact | R13 section 4.2 |
| E2 run-2: `T2bModel01` "not referenced anywhere in src/ or tests/" | 18 line occurrences in 11 files; no panel code reads it | R04 section 6 |
| E2 seed: "no missing-task category, defines no severity levels" | `missing-requirement` and CRITICAL/MAJOR/MINOR exist; Medium is outside the enum; the brief does not define CRITICAL versus MAJOR and names no driving document | R10 Unit 8 |
| E2 hand-off: "159 functions" | the notes' table sums to 179 | R17 open item (e) |
| memory lesson: "fenced yaml calibration not parsed by cluster" | `cluster_cmd.py:27-34` tries fenced yaml first; the installed-CLI version at run time is unverified | R17 open item (e) |
| pilot EV-1: "no `return-contract.yaml`" in runs 04, 08, 09 | the file exists and fails `yaml.safe_load` at line 103 (unquoted `[1m]` aliases) | R06 section 6.1; R07 E1-F8 |
| "every shadow and combo contract records `requested-pinned`" | 1 of 15 combo contracts records `observed`; all 13 pilot contracts record `requested-pinned` | R04 section 4.2 |
| `sc-tasklist-protocol` and `task-builder`: the wrapper spawns an executor-disjoint ensemble or resolves to the skill | production Tier 2 runs the swarm engine and applies no executor exclusion | R06 section 4.2 |
| slice 12: spec-panel depends on the rf-qa Fix Cycle and the plugin copy "softens" the hard gate | the loop rules "stand alone when that file is unread" (`spec-panel.md:262`); the plugin sentence is extended with a `${CLAUDE_PLUGIN_ROOT}` fallback | R12 section 1 |
| E1 FINDINGS: only A3 collapsed | the calibrator also lost its class in 6 of 15 combo runs | R07 E1-F5 |
| E1 "7 multi-reviewer clusters among 216" | 13 clusters have 2 or more reviewers, 6 chained and 7 unchained | R07 section 1 |

## Open questions raised by the options analysis ([UNVERIFIED] items; none carries an option)

| ID | Item | Where it matters | Source |
|---|---|---|---|
| OQ-1 | whether `stoprule.py` rejects unknown keys; `fix_audit.py` and the archived builds not read | 6.2 | R02 gap 6 |
| OQ-2 | whether hooks and `--resume` behave the same for gateway model ids: only single E2 smoke rows (r2 spikes) exist; the r4 haiku "strict fail" and r3 luna kill-text FAIL are slice-sourced; official docs are silent; whether `PostToolUse` `additionalContext` reaches a subagent's model is untested | 6.3, 6.5, 6.6 | R09 section 4.1 and gap 4; W02 section 7 and gaps |
| OQ-3 | whether a transcript adapter can supply per-agent usage and served model in every harness; whether Claude Code prices an alias by alias or served model | 6.5.b | R15 gaps 2, 3 |
| OQ-4 | all collaboration and process-redesign planning values (reach and act probabilities, the +29 percent kit estimate, central net shares, time budgets) | 6.6, 6.7 | RN ambiguities; R09; R10 |
| OQ-5 | whether any decision record exists for the 0.75 in the skill prose (none found); the enforced threshold is 0.80 and the code decides it (synth-06 CV-1), so what remains is reconciling the skill prose | 6.4, 6.8 | R06 gap 11 |
| OQ-6 | authorship of the E2 ground truth; whether T-1 to T-10 were approved beyond T-9; the 12-row re-judge has no artifact | 6.9 | R16 gap 1; R07 section 4; R08 G15 |
| OQ-7 | the six control and 427-arm measurement files of the phase-5 report are absent | 6.10 | R14 gap 1 |
| OQ-8 | whether the owner formally accepted #479 as the outcome of the refactor spec | 6.10 | R14 question 1 |
| OQ-9 | the cost of a local panel per PR round | 6.11 | R13 P15 |
| OQ-10 | the unit behind the gap between 109 raw-minus-kept findings and 92 dropped by validity rules | 6.3 | R02 gap 3; R08 gap 3 |
| OQ-11 | whether a truncated anchor still locates, and the re-ask recovery rate (E2 Spike 5 not run) | 6.3 | R02 gaps 4, 5 |
| OQ-12 | the pilot dispatch-collapse rate "6 of 9" cannot be re-derived (logs gone); the tier-3 orchestrator effect rests on 1 of 3 runs | 6.5 | R04 gap 1; R07 E1-F4 |
| OQ-13 | whether the gateway lists `muse-ember-1.0` today and whether it is tier-4 slot 2 or 4 | 6.5 | R04 gap 4 |
| OQ-14 | a common act-rate probe for the collaboration designs | 6.6 | R09 gap 7 |
| OQ-15 | how `hooks` blocks merge across settings sources (replace or add) | 6.6 | W02 section 6 |

## Coverage of the research files' Summary and Key Takeaways

| File | Key findings and where they appear | Excluded from this file (reason) |
|---|---|---|
| R01 overlap matrix | E2 changed no product code, shared core cells, conflicts C-1 to C-12, `snap.py` writes into E1's tree: 6.1, 6.2, 6.4, 6.5, 6.9; #519/#518 and reflect contrast: Corrected claims | the full 15-capability matrix itself belongs to Section 2.9 |
| R02 finding contract | v1/v2 limits, `origin`, `T01.02`, 92/49 figures, truncate/re-ask/keep: 6.2, 6.3 | none |
| R03 merge, ledger, verdict | D-1, D-2, D-11, D-13, pins, variants versus CLI ledger, status machines: 6.4, 6.1, 6.10 | none |
| R04 dispatch and tiers | four dispatch paths, served versus requested, `muse-ember`, class vocabularies: 6.5 | the nine `T2bModel01` uses: correction listed; it is not a panel concept |
| R05 input and brief | brief families, hard-codings, per-module exposures: 6.2.b, 6.3 levers, 6.7 | the `theory.py` HARD-set analysis: it limits one E2 claim ("not a thinking-budget ceiling") and carries no option, so that claim is not used as a fact |
| R06 reflect two engines | engines, Stage 2 failures, byte-identical set, threshold conflicts: 6.8, 6.4 | none |
| R07 E1 evidence | collapse, calibrator class loss, citation resolution faults, overlap, weak leads: 6.5, 6.6, 6.9 | model-combination leads (weak, plan rule "leads, not findings"; no option depends on them) |
| R08 E2 evidence | 92/80/49 units, 3 flips, GT concentration, j1, `fullpkg()`: 6.3, 6.7, 6.9 | the E2 default panel `ember + 2x luna` (it rests on a source-blind measurement; no option depends on a model choice) |
| R09 collaboration | five families, evidence status, H1 to H4, conflict classes, kit-versus-exchange: 6.6 | the 36-conflict list beyond the class counts (belongs to the conflict log) |
| R10 process redesign | Sweep Sheet, Recipe Ledger, E1 container, classes, gates, seed corrections: 6.7 | none |
| R11 tasklist and workflow | entry points, interfaces to keep, 36-test matrix: 6.8.b, 6.4 option 3 | tasklist mechanisms T1 to T4 detail (Section 2 current state) |
| R12 spec-review consumers | canonical binary rule, Medium meanings, caps, brief differences: 6.2, 6.4 cap policy, 6.2.b | plugin mirror gaps for `design.md` and `brainstorm.md` and brainstorm/design having no review step (current-state facts; plugin delivery belongs to the sequence inputs in Section 8.2) |
| R13 PR review and rf-qa | blockers, M1 to M14, call-site census: 6.11 | none |
| R14 E3 variants | installed state, six values, #479 mapping, model-change recount: 6.10 | per-round recomputations (evidence trail, Section 10) |
| R15 telemetry and run record | run-record options, D-17, D-23, memory: 6.5.b | none |
| R16 evaluation governance | acceptance tiers, independence, harness ownership, `verify-run`: 6.9 | none |
| R17 defect register | used as evidence rows (D-1 to D-13 numbering, reproduction status) | the 171-row register itself belongs to Section 8.1 |
| R18 repo constraints and branching | pins and gates named in Files-affected rows | the branch-name ref rule, CI and pre-commit gates and layout traps are inputs for Section 8.2 and are not a decision axis here |
| W01 multi-model evidence | quorum and merge rules, diversity limits, bias, independent review plus merge: 6.4, 6.6, 6.9, 6.11 | none |
| W02 hooks and headless | hooks in subagents, `--bare`, `--restricted`, gateway ids: 6.5, 6.6 | none |
| W03 branch hierarchy and stacked PRs | none | the whole file: branch names, stacked PRs and rebase practice are sequence and gate inputs for Section 8.2, not an options axis |
| W04 finding schemas and review bots | minimal record, export adapters, severity as configuration, thread ids: 6.2, 6.11 | Augment comment format was not researched (W04 gap) |

**Status: Complete**

