# Diff Analysis: cut-list comparison (cuts debate, 2026-11-16)

## Metadata

- Generated: 2026-11-16 (main session, Step 1 of /sc:adversarial, Mode B derived from the user's instruction; depth quick)
- Variants compared: 3. V1 = opus architect (defend cuts, concede where unprotected), V2 = sonnet analyzer (attack cuts), V3 = haiku qa (test and regression risk). Files: `variant-1-opus-architect.md`, `variant-2-sonnet-analyzer.md`, `variant-3-haiku-qa.md` (V3 persisted from messages; the agent may not write files).
- Source: `../source.md` (14 proposed cuts C1 to C14).
- Categories: structural (3), content (14 per-cut rows), contradictions (5), unique (9), shared assumptions (5).

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Verdict vocabulary | CUT / SHRINK, with a "do NOT cut if" column | CUT / SHRINK / KEEP, with a "do NOT cut when" column | CUT / SHRINK / KEEP, with an evidence key E1 to E8 | Low |
| S-002 | Added sections | five missed cuts or keeps (M1 to M5), final list with 3-package outcome | five missed items, final list with task estimate (about 33 of 54) | five consistency checks, final list of 7 grouped cuts, no task total | Low |
| S-003 | Evidence style | verified facts F1 to F7, with an explicit not-verified list | eight facts, UNVERIFIED marks inline | evidence key E1 to E8, plan-requirements-not-passes caveat | Low |

## Content Differences (verdict per cut: V1 / V2 / V3)

| # | Cut | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | C1 classifier | CUT, keep T13 as scan | CUT, keep scan as stand-alone function | CUT, keep Jev investigation separate | Low (unanimous) |
| C-002 | C2 ledger tooling | CUT, and also drop the plain list file (M1) | SHRINK to plain list, scan, offer once, `--repo` | SHRINK to plain list, capture, safety routing, offer | Medium |
| C-003 | C3 `/sc:implement` carrier | SHRINK: keep print-only carrier, cut S3 T10 | CUT, flag as reversal of owner approval | KEEP carrier, cut sweep dependency | High |
| C-004 | C4 skill folder, registry, doctor, T-tests | CUT (existing test already does it) | CUT (agree) | SHRINK to existing copy test, reverse scan and installed-path checks | Low |
| C-005 | C5 allow-list, MDTM rows, parity | SHRINK, copy S1 to S3 into the MDTM templates | SHRINK, cut concept, edit the tuple and S5 slice | SHRINK mechanism, keep coverage, no blanket exemption | Medium |
| C-006 | C6 seeded recall | CUT | CUT, rewire stage 3 T6 to the regrade ruling | SHRINK to bounded discovery checks | Medium |
| C-007 | C7 shadow stage | CUT stage 2 except shrunk T3, cut S3 T1 | CUT stage 2 except reduced T4 | SHRINK: drop classifier shadow and five-run gate, keep active-flow smoke | Medium |
| C-008 | C8 audit window | SHRINK to RT1 + owner reads first 5 lists | SHRINK, RT1 worded "any real blocker in a Medium list" | SHRINK, first-five-run review + safety rollback | Low |
| C-009 | C9 stage 0 | CUT T2, T3, T5 to T9; keep T1, T4 | CUT T2, T5 to T8; keep T1, T4, T10; T9 as errata | SHRINK: keep inventory, regrade, small discovery check, reconciliation | Medium |
| C-010 | C10 summaries | CUT | SHRINK, keep one short summary a later entry check reads | SHRINK, keep hash binding where results control a gate | Medium |
| C-011 | C11 merge stages 3 and 4 | CUT (merge) | KEEP separate | KEEP separate | High |
| C-012 | C12 defer rule prompts and templates | SHRINK, copy S1 to S3 atomically | CUT with a tuple edit | KEEP pending reachability evidence | High |
| C-013 | C13 Review Panel | CUT listed build items | SHRINK, quorum only when 2 or more launched, keep parsable-finding behaviour and Q68 | SHRINK, keep integrity checks, verify launcher suitability | Medium |
| C-014 | C14 open questions | SHRINK, record as recommendations pending the owner | SHRINK, OD3 stays open | SHRINK into pending, decided and out-of-v1 | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Does `/sc:implement` already carry minors? | `qa.md:225` prints only in legacy, N=1 or skip-final runs | same correction; stage 2 T3 admits no ledger is written | same: scoped, not universal | Low (all three correct the source) |
| X-002 | Can C11 (merge) and C12 (defer) both stand? | merge is safer: a staged S1 change cannot pass `test_c_s1_s3_copied_verbatim` in between | keep stage 4 separate, defer prompts by editing the test tuple | keep stages separate and keep the pins strong, do not weaken them | High |
| X-003 | Plain follow-ups list file | drop it (M1) | keep it, no codec | keep it, reliable capture | Medium |
| X-004 | Weaken `S1_S3_FILES` tuple vs update all ten files | update all ten atomically | drop the four prompts from the tuple and edit the S5 slice | do not weaken pins, scope them correctly | High |
| X-005 | Two-report quorum | build as listed (kept build item) | warn: it halts a round on one malformed report; apply only when 2 or more launched | two reports alone insufficient with obvious failure | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | M2: the S1 to S3 copy into all ten tuple files is one atomic task (links C5, C11, C12) | High |
| U-002 | V1 | M3: re-pin tasks must also cover `test_review_severity_mapping.py:23` and `test_review_prompt_overrides.py:24`, which read `pragmatic.md` | Medium |
| U-003 | V1 | M4: the plugin twin of `/sc:implement` is forced by `test_h_implement_protocol_plugin_twins_byte_equal` | Medium |
| U-004 | V1 | M5: the reverse scan must target the old sentence after the opening; the test requires the opening to stay | Medium |
| U-005 | V2 | Dependency rewiring list: stage 3 T6 (T3, T4), T7 and T8 (T5), stage 0 T9 (T5, T8), stage 3 T14 (all) | High |
| U-006 | V2 | RT1 must be worded "any real blocker found in a Medium list", not a rate (n = 60 proves under 5% only) | Medium |
| U-007 | V2 | Keep at least two mechanisms against under-blocking: the stage 0 T4 regrade (a lower bound) and RT1 plus the owner reading the first five lists | High |
| U-008 | V3 | Keep capture-failure handling: simplification must not weaken durable notes or silently discard safety findings | High |
| U-009 | V3 | Do not cut the post-fix helper (stage 3 T5) with the ledger tooling; keep test strength by replacing literals with consequence checks, not deleting tests | Medium |

## Shared Assumptions

| # | Agreement source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three accept cutting about two thirds of the plan | Trimming the plans in place without a new full review is acceptable, because no package has run | UNSTATED | Yes |
| A-002 | All three keep stage 0 T4 as the main check | The stage 0 T4 regrade is a sufficient measure of whether the new text keeps the 82 real blockers, although its graders carry the old-rule injection confound (a lower bound only) | UNSTATED | Yes |
| A-003 | All three shrink C14 | Open-question answers stay recommendations until the owner states them; the debate cannot answer them | STATED | No |
| A-004 | V1, V2 and V3 on C2 and C7 | After the cuts, the only writer of any follow-up list is tech-research (stage 2 T4) or the reviewer's own report, so "first five runs" evidence comes from tech-research runs | UNSTATED | Yes |
| A-005 | All three | A security, data-loss or safety hit stays blocking and is never deferred; this rests on the safety vocabulary scan only | UNSTATED | Yes |

## Summary

- Structural differences: 3. Content differences: 14 rows. Contradictions: 5. Unique contributions: 9. Shared assumptions surfaced: 5 (UNSTATED 4, STATED 1, CONTRADICTED 0).
- Unanimous cuts: C1 (keep the safety scan). Majority cuts: C4, C6 (V3 shrinks), C7, C9 (shrinks differ).
- Contested, highest severity: C-003 (C3), C-011 (C11), C-012 (C12), X-002, X-004.
- Debate points for Round 1: C-002/X-003 (list file), C-003 (C3 form), C-006 (seeded recall), C-009 (stage 0 T9 and T10), C-010 (summaries), C-011 (merge), C-012/X-004 (atomic copy versus tuple edit), C-013/X-005 (quorum), A-001, A-002, A-004, A-005.
