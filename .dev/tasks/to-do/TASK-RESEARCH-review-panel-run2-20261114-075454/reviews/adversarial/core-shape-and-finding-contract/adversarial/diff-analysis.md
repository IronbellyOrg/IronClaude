# Diff Analysis: Review Panel core shape and finding contract (slot C-01) Comparison

## Metadata
- Generated: 2026-11-14
- Variants compared: 2
  - Variant A = `variant-1-original.md` (Proposal A: one core schema and one engine; findings-v2 as the superset; the v1 loop becomes the `spec-loop` profile)
  - Variant B = `variant-2-original.md` (Proposal B: thin shared contract, per-module engines; convergence deferred to a named trigger)
- Mode: A (compare), depth standard, focus: correctness, risk, test-coverage
- Total differences found: 25 (debate points: 23 = S 5 + C 10 + X 5 + promoted A 3)
- Categories: structural (5), content (10), contradictions (5), unique (11), shared assumptions (5; 3 promoted)
- Orchestrator code checks done while building this file (read-only, HEAD 50d4d2b9d): `findings.py:_check_finding` requires `anchor`; `findings.py:annotate` indexes `finding["anchor"]`; `ledger.py:merge_round` parses with `fnd.parse_block` then calls `fnd.annotate`; `findings_v2.py:122-125` accepts anchor OR citations.

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Per-row answers | Section 4 answers each routed row (CO-1, CO-2, CO-3, CO-4, CL-X11, FX-1, FX-2) in a table | No per-row table; rows are answered inside section 2.2 (module table), 2.4 (defers) and 3.2 (defects) | Medium |
| S-002 | Open points / trigger | Section 9 lists open points carried, not resolved | Section 5.4 states a convergence trigger (when B hands over to A's work); no open-points section | Medium |
| S-003 | Evidence grouping | E1-E20 in three tables: reachability, locator cost, clustering cost | E-1..E-17 in four tables: disjoint pipelines, shared vs local defects, no location measurement, consumers | Low |
| S-004 | Invariants | Table of INV-A..INV-N with level and "why it holds", plus six "endangered" items | Preserved table plus four "endangered or left open" items | Low |
| S-005 | Tests | Five tests T1-T5 (pin parity, differential replay, locator comparison, crash regression, row-clearing) | Conformance suite (5.1), boundary test (5.2), location-reliability measurement with a preregistered rule (5.3), convergence trigger (5.4) | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | Core shape (axis 6.1) | One parser, one locator, one ledger; v1 loop re-expressed as a `spec-loop` profile of the engine; effort L | Thin shared contract (id grammar, limits constants, one repair step, ref-token list, hash helpers, panel resolution, projection view); per-module engines stay | High |
| C-002 | Locator-agnostic `annotate` and ledger rows | `annotate` derives a span from anchor or citation; ledger rows gain `citations`; row key is a span (single document) or (path, range) (multi-document) | `merge_round` rejects a finding with no anchor with a typed `LedgerError`; `annotate` and rows unchanged until the trigger fires | High |
| C-003 | Re-review contract (`prior` lines, CO-2) | Typed re-review line kind in the one grammar; v1 `prior` is its first spelling; semantics left to C-02 | `prior` stays a v1-engine feature; v2 kernel has no re-review round | Medium |
| C-004 | Clustering and fingerprint (CO-3) | New ledgers use `cluster_v2`; section resolver passed into the v2 fingerprint (default empty, byte-identical); ledger header gets a marker naming the clustering; old ledgers stay on v1 | Both clusterers stay with declared owners; whether the v2 fingerprint's line-insensitivity is intended is answered inside the reflect engine | High |
| C-005 | Unknown keys (CO-4) | Open in every profile; strictness is a per-profile option, off by default; typo detection as warning | Per module: open for the two shipped grammars, closed at the PR adapter | Medium |
| C-006 | `origin` placement (CL-X11) | Ledger member record extended to keep module-declared passthrough keys | In-line `origin` keeps working; no ledger change | Low |
| C-007 | Over-limit whole-line drop (FX-1) | One drop rule in one parser; that is the one place a repair step sits | Shared constants module plus one pre-parse repair function run before both parsers | Medium |
| C-008 | Exact-substring anchors (FX-2) | Locator policy as profile data (`on_missing`, `on_ambiguous`); citation fallback; fixes the span-less row that never clears (E11) | Not changed in the engine; location type chosen per target; reliability measured by 5.3 first | Medium |
| C-009 | Effect on PR code review and rf-qa | Panel finding already carries `citations`; adapter is a pure map from `citations[0]`; passthrough keys by declaration; multi-file remap does not yet exist | v2 engine plus pure adapter, no ledger needed; rf-qa starts at the `/task` gate with read-only reviewers and a replay oracle; v1 ledger usable for document targets | Medium |
| C-010 | Use of the citation-reliability evidence | E1 flags are mostly path plumbing; the core supplies the snapshot in the ledger path; evidence is a reason to run T3, not an advantage | Citation reliability untested, not disproved; so both location types stay and the target kind chooses | Medium |

Note (reconciled by the orchestrator against research/10 line 194 and research/07 line 49): Variant A's 372/2/26 (400 flags) are the 15 combo runs (772 checked, 51.8 percent); Variant B's 472/7/31 (510 flags, 1,047 checked, 48.7 percent) add the 13 shadow runs (275 checked, 110 flagged). The two sets of figures are consistent; they are different scopes, not a contradiction.

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Converge now or on a trigger | "A rewrite bounded by T1 and T2 ... blast radius is five source files"; cheap before consumers pin it | "Deferring leaves the v1 path pinned as it is and adds work only when a consumer pays for it"; trigger in 5.4 | High |
| X-002 | Duplicated cost of two engines | "every future fix to the limit, repair or locator policy has to be made in two parsers" | Of six cross-engine defects, two (T01.02 ref token, over-limit drop) sit in shared helpers or a pre-parse step; fingerprint and tolerance differences follow from the location type; "no duplicate cost has been paid yet" (E-5) | Medium |
| X-003 | Whether rewriting the pinned v1 path is the larger risk | Risk bounded by unmodified pins and a differential replay; INV-C and INV-D are "HIGH at stake" but kept | The rewrite touches the only shipped, pinned, measured path to carry a location type no run showed reliable | High |
| X-004 | Unknown-key policy | One policy: open everywhere, strictness per profile | Per-module policy; closed at the PR adapter | Medium |
| X-005 | What the crash closes | Locator-agnostic `annotate` removes the `KeyError` and the span-less never-clearing row | A typed `LedgerError` at `merge_round` is "one function and one test" | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Parser profile as data (location types, categories, lenses, severities, rejected keys, `prior` acceptance, `on_missing`, `on_ambiguous`) | High |
| U-002 | A | Verified stuck-row defect: a row with `span None` never reaches `resolved_check` (E11) and test T5 | High |
| U-003 | A | Section resolver for the v2 fingerprint with byte-identical default; clustering marker in the ledger header | Medium |
| U-004 | A | T2 differential replay over committed ledger fixtures (anchor-only input, compare ledger files) | Medium |
| U-005 | A | Ledger member record keeps declared passthrough keys | Low |
| U-006 | B | Defect-locality table: which defects are shared helpers and which are engine-local (3.2) | High |
| U-007 | B | Preregistered decision rule for location-type reliability (5.3) and a named convergence trigger (5.4) | High |
| U-008 | B | Git-history evidence: both pipelines are 2-3 days old with one commit each, so duplicate cost is a projection (E-5) | Medium |
| U-009 | B | Read-only projection view over both engines' findings for telemetry, export and the eval harness | Medium |
| U-010 | B | Conformance suite: golden set of about 20 finding lines, parity of repair step on already-valid lines | Medium |
| U-011 | B | Module-by-module engine table including rf-qa starting at the `/task` gate | Low |

## Shared Assumptions

Agreement points scanned: both keep the v1 grammar, `review-ledger/1` and `review merge` unchanged (INV-C, INV-D); both say no measurement shows which location type reviewers produce reliably; both route clearing, verdict and quorum to C-02, C-03; both claim a citation-only finding crashes the ledger path at `annotate`; both defer the PR wire format (C-10) and the reflect engine (C-04).

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|-------|-----------|------------------|----------------|----------|
| A-001 | A citation-only finding can reach `annotate` through `merge_round` and crash the ledger path (A: E2, CO-1, T4; B: E-3, 2.3, 5.2) | Both build a fix on this crash (A: locator-agnostic `annotate`; B: typed `LedgerError` guard) | CONTRADICTED (orchestrator code check: `merge_round` takes findings from `fnd.parse_block`, whose `_check_finding` requires an anchor of 12..200 characters, so a citation-only line is dropped as an invalid line before `annotate`; the `KeyError` is reproduced only by calling `findings.annotate()` directly, research/01 probe P-a) | Yes |
| A-002 | Reviewers can give correct line numbers and ranges for a document under review, so a citation locator is usable in the loop (the document is delivered with line numbers or the quote check catches errors) | A: span from `(line_start - 1, line_end)` and a quote check; B: citation locator for code targets and a measured document arm | UNSTATED (neither says how line numbers reach the reviewer in the ledger path; E1 flags were dominated by plumbing, so line-level reliability is a count of 38 with no stated denominator) | Yes |
| A-003 | The v2 kernel (two days old, one commit, shadow-mode, dormant) is stable enough to be the base for the shipped spec loop (A) or the base the contract is shared with (B) | A rests the superset on `findings_v2.py` and `cluster.py`; B cites their age (E-5) only to argue duplicate cost | UNSTATED (maturity of v2 under a pinned, shipped consumer is not examined by A) | Yes |
| A-004 | Neither location type is shown reliable enough to make the other redundant | A: T3 sets module defaults; B: 5.3 and E-12, E-13 | STATED | No |
| A-005 | Verdict, clearing and quorum fixes (C-02, C-03) are made in the one multi-reviewer ledger whichever core shape wins | A section 5 item 6; B E-10 | STATED | No |

## Summary
- Total structural differences: 5
- Total content differences: 10
- Total contradictions: 5
- Total unique contributions: 11
- Total shared assumptions surfaced: 5 (UNSTATED: 2, STATED: 2, CONTRADICTED: 1); promoted to debate points: 3 (A-001, A-002, A-003)
- Highest-severity items: C-001, C-002, C-004, X-001, X-003, A-001 (contradicted)
