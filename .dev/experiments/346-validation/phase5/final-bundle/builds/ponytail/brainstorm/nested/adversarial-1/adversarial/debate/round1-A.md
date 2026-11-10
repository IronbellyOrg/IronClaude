# Round 1, advocate A (variant-1-opus-architect)

## Position summary

Keep A's skeleton: one audit after fix cycle 2 and before review 3, scoped to cycle-2 hunks, run by a generic caller-agnostic skill whose script does every edit and computes the verdict. The evidence files show that A's revert channel is nearly worthless for the review-3 count (A-001) and weaker for growth than A predicted (A-004). They also show that A's other lever, shrinking blocking fixes by deletion, is the largest reachable cause. So the merged design should keep A's structure, take B's safety rules, and move the weight from reverts to deletion-shrinks.

## Steelman

**B (refactorer), strongest argument.** Most of the decision can be made deterministically: the script reads each id's severity from the report and classes each hunk as `minor-only`, `blocking-involved`, `unattributed` or `foreign-id` (B section 6). That leaves the model only as a veto and shrink layer. A `blocking-involved` hunk is never reverted whole (K6), so the audit "can close only findings the panel already graded minor" (B section 7). The verdict "cannot create a PASS that the review 3 report did not already state" (B section 8). B also builds its own falsifiers: the `--auto-minor` ablation (U-003), the K13 consistency check and the F4 blind re-grade (U-004). What B gets right: X-002 (no downgrade-and-revert of report-blocking findings), a byte-share `m` of 0.35 that sits close to the measured 27% for cycle 2, and the honest statement that the per-replicate bar is predicted to fail (B section 9.3).

**C (QA), strongest argument.** Only a terminal audit literally satisfies "never re-reviewed, decides the final verdict" (X-001). C refuses to relabel a terminal count as review 3: "Never relabel the latter as review 3" (C section 1, U-005). It is the only variant that predicts, correctly for its own placement, that the raw review-3 metric does not move (3.5, C section 10). And `minor-byte-share.md` partly vindicates C's ledger: "Larger growth cuts need sentence-level revert or shrink rows inside mixed lines, which a script cannot derive from the diff alone". C's edge-case table (U-006: shared paragraph, overwritten cycle-1 fix, CRLF, crash recovery) is the most complete test list of the three.

## Strengths claimed

1. **Deletion-first shrink is the lever the evidence supports.** A's brief says "prefer deleting over adding" and "no if a smaller change, or deleting the wrong claim, removes it too" (A section 5), and A names the deletion alternative as a design consequence (A section 2, item 2; U-001). In `evidence-attribution.md`, class B (a smaller fix would have avoided the R3 blocking finding) is 1.17 per run, about 25%, against 0.17 for class A. All 7 class-B remedies are deletions: ctl-r1 R3-2 "delete the attribution", R3-6 "delete two clauses", ctl-r2 R3-1 "drop guard case (1)", trt-r1 R3-2 "delete 'only'", R3-4 "drop the resume exception", flg-r1 R3-1 "delete the closed allow-list", R3-4 "delete 'report goes there too'".
2. **The cycle-2 scope matches where class-B defects come from.** Every class-B anchor in the six runs is a cycle-2 fix (N1/N2/N4/N7, R2-1, R2-2, or F5 reopened in cycle 2). A's scope is "exactly the cycle-2 fix set" (A section 3) and needs no new flag.
3. **A reusable boundary with one owner per concern.** "The script knows nothing about spec-panel or review numbers. Placement is the caller's choice" (A section 1). Each concern has one owner, and models never edit or decide PASS (A section 4 table). Moving to placement (a) is "a one-condition change in bullet 8" (A section 11), with no new code.
4. **The smallest drift surface in the command.** A changes the copy in exactly four kinds of edit plus one bullet-8 line, and pins them with a line-diff test (A section 14, rows 1 and 5). B adds a bullet, a new section, a Usage flag and three report lines (B section 12). C adds a section, a plugin mirror and a schema file (C section 12).
5. **One home for the brief and schema.** The brief and schema live in `sc-fix-audit/SKILL.md`, and `hunks` copies the brief into `brief.md` "so no model writes the brief" (A section 5). B relies on prose: the session "passes the brief verbatim", and B admits "nothing proves the brief was verbatim" (B section 10.2).
6. **Revert text cannot be mistyped or fail to be found.** "A revert is a hunk number. The script restores the baseline lines" (A section 8). B's old/new rows need 0 to 3 context lines to be unique and otherwise `SKIP` (B section 7). C needs a reviser ledger replayed against snapshots (C section 4).
7. **A shared-text guard.** "A hunk is reverted only when every id on it has verdict revert ... logged `REVERT_SHARED`" (A section 7). This anticipates the A-004 finding that most minor fixes share lines with blocking fixes.

## Weaknesses identified in others

1. **B's prediction rests on A-001 too.** `f = s x (m x r + (1 - m) x h)` makes the review-3 count proportional to minor bytes removed (B section 9.2). The evidence gives 1 of 28 R3 blocking findings anchored on a minor fix. B's own caveat ("N12 came from a blocking row, which none of the three placements removes") already points this way, but B's `h` = 0.10 shrink weight is too small next to the measured 25% class B.
2. **B's verdict leaves the audit almost no say.** `final` = PASS only when the report also says PASS, and the closed ids are by construction ids the report already graded minor (B section 8). So the audit affects the verdict only through text it removed earlier. That is safe, but the owner's "decides the final verdict" becomes nominal, and B says so (B section 8).
3. **B adds more surface to maintain.** A fifth subcommand (`plan`), a `--apply-audit` flag, three required report lines and a K5 parse of severity tokens from free-form reports. B itself lists "severity token formats of reports other than flg-r2's" as UNVERIFIED (B section 17, Q10).
4. **C's placement cannot move the registered metric.** "This placement cannot improve the already-written raw review-3 count" (C section 1), and C predicts raw 3.5 (C section 10). Its terminal shrinks ship text no reviewer read. That is the same objection B makes against P-post (B section 9.4).
5. **C breaks 427 and changes the treatment.** C "deliberately differs from 427's unconditional CRITICAL and FR-8/FR-9 rules" (C section 7). It adds reviser ledgers to both cycles (C section 3), so the variant is no longer comparable with Arm B. C admits that "the new schema and recovery path may cost more maintenance than the deleted document text saves" (C section 13).
6. **C's growth model is contradicted.** C uses "a row-share indicator of 0.60" as removable exposure (C section 10). The measured minor-only byte share is 6% for cycle 1 and 27% for cycle 2 (`minor-byte-share.md`).
7. **C fails closed on a missing plugin.** E-PLUGIN discards the run (C section 3), so an infrastructure gap becomes a lost replicate rather than a separately reported inline-rubric run.

## Concessions

1. **A-001 refutes A's revert channel.** A assumed "reverts remove 15-30% of R3 critical+major" (A section 11). The evidence gives about 0.2 per run of 4.67, about 4%. Over Arm B critical+major alone, at most 0.5 per run (flg-r1 R3-7, which was non-blocking).
2. **A-004 lowers A's growth prediction.** A predicted 25% with 40-60% of cycle-2 bytes kept. Minor-only hunks are 27% of cycle-2 added characters in flg-r2, so a cycle-2 hunk revert removes about 1,726 characters, about 3 growth points. With shrinks, Arm B's 30.0% falls to about 26-28%, not 25%. This rests on one run.
3. **A's flagship example is contested.** For N5 to N12, the evidence reader classes N12 as C: "both halves of N5 are defective; dropping both reopens N5". C makes the same point (C section 2). The deletion principle stands on the seven other class-B cases, not on N5.
4. **Revised A prediction.** Over Arm B critical+major (A 0.5, B 1.0, C 1.0, D 1.0 per run), removing all class A plus 50-70% of class B, then adding 0.3 for new shrink surface, gives about 2.7-3.2. Central estimate 3.0, which sits on the bar. My "about 60%" chance falls to about 45-50%. This still assumes reviewers do not find replacement findings (UNVERIFIED in the evidence file).
5. **X-002 goes to B.** A lets MAJOR be downgraded and reverted. The evidence warns that "every B/C revert reopens a blocking finding". Downgrade-and-revert of MAJOR therefore buys little and risks a lot. Adopt B's rule.
6. **K6 needs a fix.** K6 requires `new` to contain the id, which blocks a pure clause deletion when the id sits outside the deleted span. Allow an empty or id-free `new` when the id still appears elsewhere in the same hunk.
7. **A's fixed-column table parse is fragile.** It fails closed on format drift (A section 16, item 5). B's `open-blocking:` machine line is more robust.

## Shared-assumption responses

- **A-001: REJECT.** I reject the assumption itself and accept the evidence: 1 of 28 R3 blocking findings sit on a minor fix, so reverts cut about 0.2 per run.
- **A-002: QUALIFY.** 427 bullet 6 requires inline ids and flg-r2 obeys it. flg-r1 uses bare numbers, so the script must class those hunks as untagged, and that rate must be logged before trusting the mapping.
- **A-003: QUALIFY.** UNVERIFIED for all three variants. One smoke dispatch before the replicates settles it (A section 17, Q3; B Q2).
- **A-004: REJECT.** Whole-hunk reverts reach only 6% and 27% of added bytes in flg-r2. Minor text inside mixed lines needs model-written exact old/new trims.
- **A-005: ACCEPT.** 427 bullet 2 defines it, and flg-r1 R3 shows 6 critical+major against 4 blocking, so the strict test does lower labels.

## Per-point positions

- **X-001: A and B.** An audit before review 3 keeps review 3 as the registered instrument. C concedes its terminal placement leaves the raw count at 3.5.
- **X-002: B.** No whole revert of report-blocking hunks, because every B/C revert reopens a blocking finding. Keep shrink of MAJOR fixes and A's CRITICAL/FR-8/FR-9 lock.
- **X-003: merge.** Proceed with the inline rubric (A, B), but void that run as ponytail evidence and report it separately (B). Do not fail closed and lose the replicate (C).
- **X-004: all agree (no).** Adopt C's naming rule: never call a terminal or audit-computed count "review 3".
- **X-005: none as written.** All three overweight reverts. The evidence puts the reachable cut in deletion-shrinks of blocking fixes (class B, about 25%), not in reverts (about 4%).
- **X-006: A.** Use the one-line name substitution. C's reviser ledgers change the treatment and confound the Arm B comparison. Add B's `--apply-audit` only if the owner rules that a `--re-review` run is not consent.
- **C-001: A and B.** Before review 3, so every shrink byte is seen by an independent reviewer and the registered metric can move.
- **C-002: A and B, cycle 2.** All seven class-B anchors are cycle-2 fixes. Keep B's "pass the original as `--baseline`" as a pre-registered widening, not the default.
- **C-003: merge.** Use A/B diff hunks with B's four script classes, plus model-written trim rows inside mixed hunks (A-004). Reject C's reviser ledger, which changes the treatment.
- **C-004: merge.** B's rule (never whole-revert a report-blocking hunk) with A's lock and A's shrink of MAJOR fixes. Reject C's FR-8/FR-9 override.
- **C-009: merge.** With X-002 adopted, A's `closed_minor` holds only report-minor ids, so A's and B's formulas converge. Take B's `open-blocking:` line and K13 consistency check for robustness, and C's separate raw and terminal reporting.
- **C-011: none as written.** Revised for a before-review-3 audit on the Arm B base: critical+major about 2.7-3.2 and growth about 26-28%. C's raw 3.5 is right for C's own placement only.
