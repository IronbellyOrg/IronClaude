## Crossref-Chain-Integrity QA Report

**Report:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Phase:** report-lens-crossref-chain
**Date:** 2026-11-07
**Fix authorization:** false

**Lens:** one dimension only, Crossref-Chain-Integrity. Checks: (a) every S4 gap has an S8 step or an S9 entry; (b) every S6 option references evidence in S2 or S5; (c) the S7 recommendation traces to the S6 comparison; (d) every S2 or S3 finding that warrants action appears in S4 or S8.

**Method:** read the whole report in chunks. Traced every row of 4.2-4.9 against 8.1, "Gaps sent to Open Questions", 8.2 and 9.1-9.7. Traced each S6 citation back to S2 or S5. Checked both [CONTRADICTION] markers against repository source: `src/superclaude/core/HOW-WE-WORK.md` (`<!-- other-commands:v1 -->` at `:318`, `<!-- /other-commands -->` at `:337`) and the `allowed-tools` line of `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md:7`. Cross-checked `gaps-and-questions.md:107`, `:125`, `:137`, `:181`, `:199`.

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | S6 A1 (`:930-937`), A3 (`:968-991`); S7 trade-offs (`:1047-1053`), X-3; S8.4 X-3 | Check (b) fails for the main alternative. A3's premise (the sc-issue scripts layout, `docs/designs/sc-issue-command.md:355-363`, `:395-396`) and A1's leading Con and trade-off (sc-issue chose "No CLI", `:384`) rest on evidence that S2 and S5 never present. The only S2 mention of that design doc is its 20-heading format (`:231`). "No CLI" first appears at `:933`. Other S6 evidence with no S2 or S5 anchor: `reflect/config.py:103-109`, `sc-swarm-wizard-protocol/SKILL.md:7` (the allowed-tools precedent), `sc-crash-recovery/SKILL.md:137`, `research-notes.md:158-159` (the A2 precedent), and the `seed-brief.md` lines behind constraints K-1, K-2 and K-4. | Add S2 rows (2.4, or a new subsection) for the sc-issue design decision ("No CLI" `:384`; scripts layout `:355-363`, `:395-396`) and for the skill allowed-tools and skill-calls-CLI precedents. Cite those S2 rows from S6. Anchor K-1, K-2 and K-4 in S3, or tag them in S6 as new evidence with their source. |
| 2 | IMPORTANT | S1 `:38`; S4.4 `:531`; S8 Phase 1 Dependencies `:1158-1168`; 8.1 `:1275`, `:1319`; S9 row 52 | Check (d) fails. S1 records a sequencing constraint: contract edits for #339 should land after open PR #422. Phase 1 steps 1.17-1.19 are those contract edits (`WORKER-CONTRACT.md` and its test). Even so, S4.4 calls GQ-62 "outside Phase 1", 8.1 maps GQ-62 to "Later phases", and the Phase 1 Dependencies table has no PR #422 row. S9 row 52 says only "Owner decision". The S1-to-S8 chain drops a dependency that gates three Phase 1 steps. | Add a Phase 1 Dependencies row: "PR #422 merged (or owner sequencing decision, GQ-62) before steps 1.17-1.19". In 8.1, move GQ-62 to steps 1.17-1.19 as "gated on #422". Correct the S4.4 `:531` note. |
| 3 | IMPORTANT | S4.6 `:563`; 8.1 `:1297`, `:1321`; S9 (missing) | Check (a) fails, and the chain gives three conflicting statuses. S4.6 says the scope-01 `:100` "41 tests" item is "settled by GQ-84 (M1)". GQ-84 is the fenced/unreadable-transcript rule (`gaps-and-questions.md:107`) and has nothing to do with a test count; the mapping is copied from `gaps-and-questions.md:199`. 8.1 then marks the item "Sent to Open Questions". S9 has no row for it: 9.2 has only scope-01 `:118` and `:128`. | Correct the S4.6 cell: drop "settled by GQ-84 (M1)" and state the actual count or "open". Add an S9 9.2 row for scope-01 `:100` (resolution: re-count the worker-contract tests), or make 8.1 cite where it is settled. |
| 4 | IMPORTANT | [CONTRADICTION] marker `:1507-1509`; S9 row 21 (GQ-26); S8 steps 1.15, 1.16; S3.1 | The two sides of the marker disagree on a value that a Phase 1 test pins. S9 row 21 tells the implementer to pin the colon form `Bash(superclaude sweep:*)` / `Bash(uv run superclaude sweep:*)`. S8 step 1.15 and S3.1 use the space form, and step 1.16's static test asserts the exact form. The repository precedent cited in S6 and S8 uses the space form: `sc-swarm-wizard-protocol/SKILL.md:7` reads `Bash(uv run superclaude swarm *)`. Under this lens the marker is a real, unresolved chain break; the evidence favours the space form. | Change S9 row 21 to the space form, citing `sc-swarm-wizard-protocol/SKILL.md:7`. Keep GQ-26 open only for how command-level and skill-level patterns combine. Then mark the marker resolved, with the evidence. |
| 5 | IMPORTANT | S8.3 `:1359`; S5 `:749-750`, 5.9 D6 `:808`, `:817` | S8 claims external support that S5 does not give. 8.3 cites agents-fleet and Simple Agent Manager as support for WC-14 G1 and G2 (keep polling, re-arm). S5 records both as search results only, not fetched, with LOW relevance, about a stall watchdog with auto-abort. D6 rejects agents-fleet as context only. No S5 finding links either source to keep-polling or re-arm. G1 and G2 actually trace to the owner order (GQ-04). | Remove the `:1359` row, or relabel it "context only, unfetched (D6)" with no clause attribution. Keep G1 and G2 traced to GQ-04 (owner order, 2026-11-05). |
| 6 | MINOR | [CONTRADICTION] marker `:1078-1080`; S6 A1 Files `:935`; S7 Step 6 `:1075`; S8 step 1.21 | The marker can be decided from source: `HOW-WE-WORK.md` has the markers at `:318` and `:337`. S8 step 1.21 and S2.4/SC-11 are correct. S6 `:935` and S7 `:1075` cite `:314-337`, 4 lines off. The S7-to-S8 chain still reaches the right target, so this is a moved line number on a true claim. | Change `:314-337` to `:318-337` at `:935` and `:1075`, and record the marker as resolved. |
| 7 | MINOR | S2.4 Forbidden column `:208-214`; S6 K-5 `:878`; SC-2 `:424`; S8 step 1.10 | The forbidden list is not carried consistently. SC-2 and step 1.10 forbid `--format`; the S2.4 Forbidden column and constraint K-5 omit it. | Add `--format` to the S2.4 Forbidden column and to K-5. |
| 8 | MINOR | S8 step 1.4; 8.1 `:1280`; S9 row 63 | GQ-99 has two different resolutions. S8 uses a "per-sweep call bound" and never gives a value. S9 row 63 says "Batch where the policy allows", which is a different mechanism. | Choose one resolution, state the bound (or say the value is still open), and make 8.1 and S9 row 63 say the same thing. |
| 9 | MINOR | S9 row 18 (GQ-23); S6 A1 Cons; S8 step 1.1, 8.2 OQ-2 | S8 decides lazy init (step 1.1, 8.2 OQ-2). S9 row 18 still says "Pick one precedent", and S6 still says "undecided". The S9 entry is stale against S8. | Change S9 row 18 to "Plan takes lazy (step 1.1); open only as an owner check". |
| 10 | MINOR | S4.9 OQ-6; S9 row 93 (C12); 8.2; S8 step 1.4 | The K1 second-worker check (`gaps-and-questions.md:137`; C12 at `:181` was verified on one worker only) reaches S9 only through row 93. Row 93's resolution points at GQ-01, the worker-list schema, not at the K1/GQ-18 pane-key join. 8.2 does not carry the check, although step 1.4 depends on the join. | In row 93, cite K1/GQ-18 and say "check the pane-key join on a second worker". Add it to 8.2, or make it a step 1.4 acceptance item. |
| 11 | MINOR | S9 row 9 (GQ-11); S8 step 1.17 | S9 says to word WC-14 so it "does not override WC-1". Step 1.17, which writes WC-14, does not carry that constraint. | Add to step 1.17: "WC-14 text states it does not override WC-1 (GQ-11)". |
| 12 | MINOR | S9 rows 11 (GQ-14), 64 (GQ-100); S8 1E; Integration Checklist `:1404-1427` | Two S9 resolutions say "read before implementation" (`test_help_command.py`; APPROVED.md and the ccsession-tag README). Neither S8 nor the Integration Checklist has such a step. A `/sc:help` registry step may also be missing. | Add a pre-implementation read step or checklist lines. Add a conditional 1E step for `/sc:help` registration if the test enforces it. |
| 13 | MINOR | S6 A4 rejection table `:1004-1007` vs S4.1 `:483-485`; S5.9 C1/C2 `:814-815` vs codebase C1/C2 `:552-553`, 8.1 `:1286-1287` | Label collisions make cross-references ambiguous. The A4 rejection reasons R-1..R-4 reuse the S4.1 severity-rule IDs R-1..R-3. The external contradictions C1/C2 reuse the codebase C1/C2 IDs that 8.1 and S9 cite. | Rename them, for example A4-R1..A4-R4 and EC-1/EC-2. |
| 14 | MINOR | 8.1; 8.5 | 8.1 has no rows for C8, C10, C11, C12, C14 or C15, but 8.5 claims "C1-C13". All six reach S9 (rows 91, 1, 2, 93, 9.6 and 35), so check (a) holds, but 8.1 cannot serve as the single trace. | Add the six 8.1 rows and change 8.5 to "C1-C15". |

### Items checked and found intact

- **(a)** Every G-A, G-B, G1-G7, K1-K4 and 4.4 GQ group has an 8.1 step or an S9 row. S9 9.1 lists exactly the 75 open GQs, and 25 are resolved; this matches `gaps-and-questions.md:125`. The stale-doc rows S-01..S-14 go to 9.3. The 4.8 contradictions go to 8.4 and S9 98a. OQ-1..OQ-8 all reach S9. The exceptions are findings 3 and 10.
- **(c) PASS.** The S7 trade-offs (`:1051-1053`) answer A1's Cons from `:937`: registry footprint, "No CLI" and pipx. The lazy-vs-eager Con goes to 7.1 OQ-2 and is decided in S8 step 1.1. The S7 implementation steps map onto S8 1A-1F.
- S5.10 R1-R9 trace to steps 1.3 and 1.5. L1 goes to Phase 4, and L2 is excluded.
- **NB-4 exception record:** the chain is intact, running from S2.4 (qa-nb4-fix-log) to 4.5 GQ-03, 8.1 `:1281` (GQ-03 -> 1.4 and 1.10 under SC-2), 9.6 `:1583` and S10 `:1651`.
- The six-versus-seven classes question is carried by 4.8, 8.2 OQ-13, 8.4 X-7 and S9 98a.

### [CONTRADICTION] markers and NB-4, judged under this lens

- `:1078` is decidable from source (`:318-337`); recorded as MINOR (finding 6).
- `:1507` is unresolved and gates a Phase 1 static test; recorded as IMPORTANT (finding 4).
- The NB-4 pass-by-exception record is traceable end to end; no finding.

### Summary

- Checks:
  - (a) S4 gap -> S8/S9: FAIL (finding 3; finding 10 is minor).
  - (b) S6 -> S2/S5 evidence: FAIL (finding 1; finding 5 is the related S8-to-S5 break).
  - (c) S7 -> S6: PASS.
  - (d) S2/S3 -> S4/S8: FAIL (finding 2).
- Cross-section consistency inside the chain: FAIL (finding 4).
- Counts: CRITICAL 0, IMPORTANT 5, MINOR 9, total 14.
- The MINOR findings are notes only.
- The 5 IMPORTANT findings block, under the severity rule.
- Fix authorization: false. No changes were made to the report.

Verdict: FAIL
