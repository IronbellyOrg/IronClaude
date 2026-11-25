# Merge Log: Orca Fleet Snapshot (adversarial Step 5)

## Metadata
- **Base**: Variant 3 (haiku:backend), `variant-3-haiku-backend.md`
- **Incorporated**: Variant 1 (opus:architect), Variant 2 (sonnet:analyzer)
- **Plan**: `refactor-plan.md` (16 changes, auto-approved 2026-11-05T20:15:00Z)
- **Supporting inputs**: `invariant-probe.md`, `base-selection.md`
- **Output**: `/home/coder/workspaces/IronClaude/.dev/research/orca-dashboard-20261105/snapshot-brainstorm/adversarial/merged-output.md` (20 top-level sections; 11 fenced blocks: 1 layer diagram and 10 rendered screens)
- **Date**: 2026-11-05
- **Method**: header stub with the full section skeleton and TODO placeholders, then one Edit per section. Each top-level section carries one provenance comment; section 9 carries a second comment on the retained Base run-reconciliation block (s.9.3), as Change 5 requires.
- **Scope**: UI research and design only. No product code, no external research, no tests, collector calls or operator trials.

## Changes Applied
| # | Change | Status | Merged sections | Notes |
|---|--------|--------|-----------------|-------|
| 1 | Layer model and Variant 1 organization | Applied | Whole document; s.1-2 | Order follows the plan: purpose, layers, requirements, data contract (Base s.3), integrity rules (Base s.4), frame, concepts A-E, comparison, default, states, overflow, evaluation, limits, risks, gates. Base s.3 and s.4 kept as their own sections (merged s.4 and s.5, INV-030), modified only by Changes 12-16. |
| 2 | Requirements with Layer, Basis and acceptance on one row | Applied | s.3 | Families DEC-1..7, BLK-1..6, COM-1..7, CHG-1..6, VER-1..5, COV-1..9, FMT-1..8, OVF-1, SYN-1. Every Base R01-R16 is cited in a Basis cell. DEC-1 (decisions first) and DEC-3 (OLDEST line mandatory) included. |
| 3 | Shared frame contract and printed legend | Applied | s.6.1-6.4 | Header, footer, field table, notation, stable identity. The frame is used by all 10 rendered screens. Modified by Change 15. |
| 4 | Concept A, Attention Brief, default | Applied | s.8 | Decision block first (DEC-1); ANSWERED, NOT RESOLVED band, WATCH row and SINCE strip from Variant 2; no worker VERIFY row above human questions. |
| 5 | Concept B, Ball-Holder Board | Applied | s.9 | Responsibility bands from Variant 2. Owner never names the relay (A-002); s.9.1 states that the Variant 2 `> coord` owner is replaced by the acting human or `?`. Base run reconciliation retained as s.9.3 with a `Base (original, modified)` comment. Items with owner `?` sit in the HUMAN band. |
| 6 | Concept C, Root-Blocker Tree, age-ranked | Applied | s.10 | Variant 1 tree layout with Base rules: roots ranked by age, cycles printed as `dependency conflict`, union count in the footer. OLDEST frame line repeated. |
| 7 | Concept D, Conversation Ledger, y/n/? ladder | Applied | s.11 | Variant 1 ladder; acting human kept distinct from requesting worker. The s.11.3 tradeoff citation was changed during the merge from "gate FG-5 in the cross-map" to gate FG-12 (delivery facts), matching the final gate table. |
| 8 | Concept E, Delta Journal under DEC-1 | Applied | s.12 | Decisions first; partial reads produce only `newly observed` additions; VANISHED only after a full read, labelled last-known unresolved with the capped-read qualifier, never as resolution (INV-018, INV-024, INV-027). The TRAIL line prints `n/a (no stored history in fixture)` until FG-6 closes. |
| 9 | Fixture, overflow screen, concept x state matrix | Applied | s.7, s.15, s.16.1 | One DEMO-marked fixture table (seq 0412). Variations declare their added fixture items beside the screen (s.16.1 declares Q-DEMO-20..35, w-DEMO-06, M-DEMO-108, TH-DEMO-08). Overflow arithmetic in whole bundles with `observed (census unknown)`. Matrix in s.15.5. |
| 10 | Comparison, data dependency, default, one switch rule | Applied | s.13, s.14 | Default is A with the SINCE strip. One switch rule: switch to E only if the s.17.3 decision rule shows E ties on the oldest-decision task and wins on change recall. The Variant 2 clause "beats on ET-1 by >5s" was removed as a second switch rule (INV-020). Comparison cells that differ from the source rating because the merged concept differs (B, C, E) are marked `*`. s.14 states that whichever concept is default keeps the frame and OLDEST line. |
| 11 | Evaluation, contract cases, gate table | Applied | s.17, s.20.1 | Variant 2 reader tasks adopted as ET-1..ET-10 and cross-mapped to Base E01-E07 and Variant 1 EV-1..EV-10. ET-11 ("Is everything fine?") added so Variant 1 EV-3 and the Base false all-clear blocker are not lost; EV-10 maps to MC-1 plus FG-11. Mechanical checks MC-1..8; contract cases from Base s.11 plus two (unclassified, end marker). Gates FG-1..FG-14 with FG-8 Cannot ship; INV-029 statement that gates block shipping a claim, not design exploration. |
| 12 | Unclassified fallback | Applied | s.4 "Message classification and the visible fallback", COM-7, s.8 | A message is a heartbeat only by matching an explicit routine form; anything else shows as `unclassified` in the decision block and is eligible for OLDEST. Gate FG-9 added. |
| 13 | No all-clear anywhere | Applied | COV-4, MC-4, s.15 intro, s.17.5, s.20.1 note | Empty state reads `no attention items observed in <scope>` with coverage and census qualifiers. MC-4 rewritten to forbid all-clear wording with no exception. Variant 2 R-INT-01 / s.7.2 and Variant 1 COV-4 / G1 conditional wording overridden. |
| 14 | One budget; over-budget line; transport gate; end marker | Applied | FMT-3, FMT-7, s.16.2 | 60 lines and 78 columns (2-column wrap margin in an 80-column block). The oldest complete question may exceed the budget and the report prints `over budget: oldest question kept whole`. Transport fit is gate FG-11 (A-003). A paste without its `=== END SNAPSHOT seq N ===` line is invalid. |
| 15 | Qualifiers in the header; seq identity | Applied | s.6.1-6.2 | Coverage, census and omitted counts in the header; footer repeats them with the end marker; title line carries `seq N`, and the end marker repeats the same N, so an older or truncated paste is recognizable (INV-003). |
| 16 | `OLDEST observed`; paging gate; qualified-age sort | Applied | s.4 "Census and the oldest claim", s.6.2, DEC-3, DEC-7 | OLDEST is labelled `oldest observed` while census is unknown; dropping the qualifier needs gate FG-10. Unknown-age, `seen>=` and `clock conflict` items sort above known-age items with their qualifier (DEC-7, INV-007). Unclassified items are ranked (tie to Change 12). |

**Applied: 16 of 16. Partial: 0. Not applied: 0.**

Merge-time consistency edits (no new content):
- Section 20 provenance comment corrected to cite Variant 1 s.17 (gates G1-G8), not s.15.
- Gate numbering: Variant 2 FG-1..FG-8 kept; added gates numbered FG-9..FG-14, each cross-mapped to Variant 1 G1-G8 and Base G01-G08 in s.20.1. Base G08 (density decision) is footnoted as an evaluation question, not a gate.

## Open Questions and Limits Carried
| Item | Severity | Where in merged output | Form |
|------|----------|------------------------|------|
| INV-001 partial-read pointer and duplicate `new` | MEDIUM | s.20.2 | Open question with interim rule |
| INV-002 first-run, empty-store state | MEDIUM | s.20.2 | Open question with interim rule |
| INV-004 uncertain-identity candidates | MEDIUM | s.20.2 | Open question with interim rule |
| INV-021 whether ANSWERED, NOT RESOLVED items count for DEC-1 and OLDEST | MEDIUM | s.20.2 | Open question with interim rule |
| INV-022 WATCH clock uses evidence time | MEDIUM | s.20.2 | Open question with interim rule |
| INV-023 redaction changes meaning | MEDIUM | s.20.2 | Open question with interim rule |
| INV-009 | LOW | s.18.2 limit 12 | Limit (proposed "strictly greater") |
| INV-015 | LOW | s.18.2 limit 13 | Limit |
| INV-017 | LOW | s.18.2 limit 14; s.15 intro | Limit |

All nine carried; none dropped.

## Changes NOT Made (base kept)
| Diff point | Base behavior kept | Where |
|------------|--------------------|-------|
| C-005, X-007 | Oldest pointer kept on any override, within DEC-1 ordering | s.5 rule 2; DEC-3 |
| C-006, X-003 | Census stays `unknown` independent of worker coverage | s.4 "Census and the oldest claim"; header census field |
| C-009 | Last-known unresolved until explicit resolution | s.5 rule 3; s.12 VANISHED wording |
| C-012, X-004 | No conditional fleet-wide all-clear | COV-4; MC-4 (reinforced by Change 13) |
| C-013 | Full last-known bundles under a not-confirmed-current banner | s.15.2 (seq 0502) |
| C-014 | Distinct unavailable / stale / mismatched / failed labels | s.4 source statuses; s.15.2-15.3 |
| C-017 | Exact question text with marked redaction | s.5 rule 10; INV-023 in s.20.2 |
| A-002 | Acting human distinct from requesting worker; missing owner `?` | s.9.1; s.11 |
| A-004 | No assumption that the latest paste is the one read | seq identity (Change 15) |
| S-003 | Layer, Basis and acceptance all kept | s.3 table columns |
| A-003 | Transport fit not assumed | FG-11 |

## Contradictions Resolved During Merge
| # | Contradiction between sources | Resolution in merged output | Status |
|---|-------------------------------|-----------------------------|--------|
| K-1 | Line budget: Base 44, Variant 1 about 40, Variant 2 60 | One budget of 60 lines and 78 columns (Change 14); s.16.2 states the others are superseded | Resolved |
| K-2 | Base rule 2 "coverage first" vs DEC-1 decisions first | Coverage moves into the frame header (Change 15); the body starts with decisions | Resolved |
| K-3 | Concept C ranking: Variant 1 by impact vs Base by age | Age (X-002, C-007) | Resolved |
| K-4 | Comparison ratings written for Variant 1 Control Board, merged B is Ball-Holder | Re-rated cells marked `*` with an explanation in s.13.1 | Resolved |
| K-5 | Task sets: Variant 1 EV-1..10, Variant 2 ET-1..10, Base E01-E07 | ET adopted, cross-mapped columns; ET-11 added for EV-3 | Resolved |
| K-6 | Variant 2 `> coord` owner vs A-002 | Acting human or `?` (s.9.1) | Resolved |
| K-7 | Variant 2 s.7.2 / R-INT-01 "none observed" all-fine banner and Variant 1 G1 complete-coverage empty-state wording vs X-004 | Dropped per Change 13; s.20.1 note says no gate unlocks all-clear wording | Resolved |
| K-8 | Variant 2 s.9.3 second switch clause ("beats on ET-1 by >5s") vs one switch rule | Removed (INV-020) | Resolved |
| K-9 | B items with owner `?`: Variant 2 put them under the coordinator | HUMAN band with owner `?` | Resolved |
| K-10 | E TRAIL needs history the fixture does not have | TRAIL prints `n/a (no stored history in fixture)`; gated by FG-6 | Resolved |
| K-11 | Gate numbering: Variant 2 FG-1..8, Variant 1 G1-G8, Base G01-G08 | FG kept and extended to FG-14 with cross-map column; s.11.3 citation changed to FG-12 | Resolved |
| K-12 | Busy-world fixture vs state variations needing extra items | Each variation declares its added items beside its screen (e.g. s.16.1) | Resolved |
| K-13 | ANSWERED, NOT RESOLVED items: counted for DEC-1 / OLDEST or not | Not decided by any source or the plan | **Unresolved: open question INV-021 in s.20.2** |

## Post-Merge Validation
All checks below were run on the final `merged-output.md` with grep and awk on 2026-11-05. Results are what the commands printed.

| Check | Method | Result | Verdict |
|-------|--------|--------|---------|
| (a) Concept count and distinctness | Heading grep `^#{1,3} ` | Five concept sections: s.8 A Attention Brief, s.9 B Ball-Holder Board, s.10 C Root-Blocker Tree, s.11 D Conversation Ledger, s.12 E Delta Journal. Each has its own body grammar subsection, its own busy screen (seq 0412) and tradeoffs. Primary axes differ: decision age (A), responsibility owner (B), dependency root (C), conversation ladder (D), change since last observation (E). | Pass. Count is mechanical; distinctness is a reading of the body grammars, not a mechanical test. |
| (b) All-clear wording | `grep -niE 'all clear\|all-clear\|healthy\|no problems\|\bclear\b'` | 9 hits (lines 59, 106, 237, 739, 741, 998, 1011, 1025, 1121). Every hit is prose that forbids, negates or names the wording (COV-4, MC-4, notation `?` "never healthy", provenance comment, ET-11 note, s.20.1 note). Zero hits inside any fenced screen. | Pass |
| (c) OLDEST line and qualifiers on every screen | awk per fenced block counting `=== ORCA`, `OLDEST observed`, `cover`, `attn`, `=== END SNAPSHOT` | All 10 screen blocks (lines 200, 299, 378, 468, 547, 629, 747, 778, 831, 906): title 1, `OLDEST observed` 1, `cover` 3-4, `attn` 1, end marker 1. Block at line 25 is the layer diagram, not a screen. | Pass |
| (d) Dangling references to variant section numbers | `grep -nE 'Variant [0-9]\|\bV[123]\b\|\bs\.[0-9]\|\bG0[1-8]\b\|\bC[1-5]\b'` excluding `<!-- Source` lines | No `s.N` variant section number appears outside provenance comments. Remaining hits are intentional named cross-maps with no section number: line 2 base marker comment; s.3 intro and COV-4 (requirement IDs absorbed); s.9.1 line 374 ("Where Variant 2 printed `> coord`"); s.16.2 FMT-3 row ("Variant 1 OVF-8"); s.17.2 cross-map columns and ET-11 note; s.20.1 cross-map column and footnote (V1 G1-G8, Base G01-G08). | Pass (intentional mentions listed) |
| (e) Unresolved contradictions | Review of the contradictions table above | One unresolved: K-13 (INV-021), carried as an open question in s.20.2 as the plan requires | 1 unresolved, marked |
| Width and budget | awk on fenced blocks for lines over 78 columns and line counts | No line over 78 columns; every title line exactly 78. Block line counts 13, 13, 41, 50, 44, 43, 39, 22, 42, 44, 44; maximum 50, under the 60-line budget. | Pass |
| DEMO IDs from one fixture | IDs in all text minus IDs in the s.7 fixture (lines 251-278) | Outside-fixture IDs: Q-DEMO-20..24, Q-DEMO-34, Q-DEMO-35, w-DEMO-06, M-DEMO-108, TH-DEMO-08. All declared in the s.16.1 variation text (line 902) as additions to the seq 0412 world. | Pass |
| One default, one switch rule | Read of s.14 | Default A; one switch rule to E, tied to s.17.3 | Pass |
| Provenance per section | awk counting `<!-- Source` per `## ` section | 19 sections have 1; s.9 has 2 (second marks the retained Base block per Change 5) | Pass |
| Placeholders | `grep -n TODO` | No output | Pass |
| Gate references | grep for `gate`/`G[0-9]` | Every gate citation in body text uses FG-n and matches the s.20.1 table (FG-1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14 cited) | Pass |

Failed checks: 0.

## Summary
- Changes applied: 16 of 16 (0 partial, 0 not applied).
- Open questions and limits carried: 9 of 9.
- Base positions kept per "Changes NOT Being Made": 11 of 11 rows.
- Failed post-merge checks: 0.
- Unresolved contradictions: 1 (INV-021, ANSWERED, NOT RESOLVED counting for DEC-1 and OLDEST), recorded as an open question in s.20.2.
