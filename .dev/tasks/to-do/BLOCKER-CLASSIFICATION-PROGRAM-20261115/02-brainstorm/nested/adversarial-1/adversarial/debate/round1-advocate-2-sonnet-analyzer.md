# Round 1 advocate: Variant 2 (sonnet, analyzer)

Status: complete (round 1 of 2). Paths are relative to the repo root `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` unless stated. Short names: V1 = `variant-1-opus-architect.md`, V2 = `variant-2-sonnet-analyzer.md`, V3 = `variant-3-haiku-backend.md`, DA = `diff-analysis.md`.

## 1. Position summary

V2 is the only variant that asks why the old rule over-blocked before rewriting it, and it found that rewording the definition fixes one of six causes (RC1); the other five (highest-severity-wins merging, fix-induced defects, upstream gates with no decision basis, no record path, the overloaded word Medium) need loop and ledger changes that V1 and V3 mostly leave unchanged. Its measured guardrails (blind audit with sample sizes that can support the claim, seeded-defect recall, interval-based revert triggers) are what make "loosen blocking" safe to ship. V2 has real errors, listed in section 6, and it should borrow V3's ledger safety, V3's treatment of a missing safety answer and V1's registry idea.

## 2. Steelman of Variant 1

Strongest version: the rule is a maintenance problem as much as a wording problem, so the right answer is a structure that makes the next change cheap and mechanical. V1 puts the full rule, a scale map and the ledger format in one delegate-only skill folder, carries a short fenced digest in each of the 11 carriers, and drives the drift tests from `refs/registry.yaml`. Each stage switch and each revert is then a registry edit that tests check. That solves three genuine problems:

- Today's test reads the rule by position (`canonical_rule_bullets()`, `tests/skills/test_review_severity_rule.py:78-96`) and the copy list is a hard-coded tuple, so a new copy is invisible. V1's reverse scan (T2) fixes that. V2 also proposes a reverse scan, but V1's registry is the better carrier of stage and version.
- A skill folder gets the project `.claude/` copy through `make sync-dev` and drift checking through `make verify-sync`. I confirmed `Makefile` has no `core/` step and `.claude/WORKER-CONTRACT.md` does not exist, so a `core/` document has no second surface at all.
- V1 gives the classifier an installable shape (a `superclaude review classify` CLI) that respects the project rule that installed primitives reach package code only through the CLI.

V1 is also right that `D = UNSET` never gives FOLLOW_UP for a wrong-outcome finding. I re-ran the sketch: `(W=Y, D=UNSET)` returns SHOW_USER.

## 3. Steelman of Variant 3

Strongest version: the dangerous failures here are operational, not conceptual. A ledger that two writers can corrupt, a resume that double-offers, and a `/sc:issue --create` that posts with no preview or dry-run can each create duplicate or wrong-fork issues or silently lose findings. V3 specifies a single writer, a `revision` counter with atomic rewrite, run-scoped identifiers that are never recycled, an Observations table so repeated imports change nothing, consent bound to a snapshot digest, and a prepared/posting/reconcile/filed state machine that never blind-retries creation. Its handling of the classifier is also the most careful about unknowns: "Unknown is not no", and a missing safety answer must not look safer than an uncertain one. I verified that this last point is a real defect in the sketch: with `S = UNSET`, `W = Y`, `D = N` the sketch returns FOLLOW_UP, but with `S = U` it returns SHOW_USER. Of the 1,024 states with `S = UNSET`, 511 give BLOCKING, 297 SHOW_USER, 108 FOLLOW_UP and 108 NOTE. V3 saw this; V1 and V2 did not.

## 4. Strengths claimed for Variant 2

1. **Root-cause decomposition that changes the design (S-003, U-006).** V2 section 2.2 names six causes and maps each to a remedy. I verified RC2: `src/superclaude/skills/task/SKILL.md:252` and `src/superclaude/skills/tech-reference/SKILL.md:513` both say "Preserve the highest severity rating when duplicates disagree". With 15 reviewers per gate the chance that someone calls a borderline item blocking approaches 1. V1 and V3 keep this merge rule, so under their designs the loosened definition still gets overridden at consolidation. Only V2 has a replacement (L1) and a pin that the phrase is gone (T5).
2. **Fix-pass mechanical checks (C-017, U-007).** NEW-1 and NEW-2 forced Gate 1's second fix cycle. I verified `gate1-cycle-control.md:9` (NEW-1 and the Destination cell) and that the gate ended "PASS at review 3" (line 38). A pipe-count check over edited rows before hand-back (L2) would have prevented the cycle regardless of how the finding was graded. Neither V1 nor V3 addresses this cause.
3. **A consumer test the reviewer must write down (C-001, C-004).** `rests_on` plus `why not blocking` makes the downgrade checkable: code can verify a named consumer, and an auditor can contest it. V1's `why_not_blocking` names only which condition failed; V3's `nonblocking_basis` is similar. V2's `consumer-unknown` tag gives upstream gates (where no decision basis exists yet) a place to land without either blocking or silently passing (X-003), and GR7 re-tests those rows at the final gate when the basis does exist.
4. **Honest use of the run-2 evidence (C-021, X-010).** V2 shows the five Gate 1 downgrade candidates were fixed anyway. I confirmed the corrected figures in `R2/RESEARCH-REPORT-review-panel-unification-run2.md` ("14 terra plus 2 luna", "Six uses of Medium", "175 prose spawn lines", lines 331, 1015 and 3066 to 3068 all read as V2 says). It also shows the "about 25 minutes" claim is not supported by file times (cycle 2 about 4.5 minutes; header "12:23" is later than the file's last write). V1 repeats the 25-minute claim as fact.
5. **Measurement a small sample can support (U-008, U-009).** V2 states that zero escapes in 60 only supports "under 5 percent" (3 over n) and writes revert triggers as Wilson interval bounds (RT2), so a trigger is testable. It adds a seeded-defect recall test and a retrospective escape test on run 2 (stage 0b) that does not rely on the rule that graded the findings. V1's M3 threshold of 5 percent and trigger of 10 percent in two runs cannot be tested at the sample sizes V1 proposes.
6. **Six gating questions, not ten (C-012).** The sketch's `verdict()` reads only S, M, C, W, E, D; T, F, I and G reach no cell. V2 keeps the four out of the gating path and rewords S ("in a way the task did not ask for") so a recipe that deliberately deletes its own temp directory does not score yes. That reduces calls, over-fitting surface and the number of thresholds fitted on 30 to 40 rows.
7. **Worked grading on real findings (S-004, U-012).** The 14-case table, ten of them from Gate 1, lets a reader see what the rule does to P3-001, P3-002, P3-009 and the NEW rows, including a bundled finding that is split (P3-007). Neither other variant shows the rule applied to real data, so neither can show it differs from the run-2 override on cases 6 and 8.
8. **Stage 1 runs with the old rule still deciding (S-009).** V2 first collects `rests_on` data while the old definition decides, so a reviewer who cannot name consumers honestly costs nothing. V1 and V3 move to the new default before that evidence exists.

## 5. Weaknesses identified in Variants 1 and 3

1. **V1 states NEW-1 and NEW-2 as NOTE examples (X-011).** V1 section 3 lists them under "a table-pipe defect that changes no cell a later phase reads". `gate1-cycle-control.md:9` says the Destination cell reads wrong. Under V1's own table-shape rule that is condition 1 if a parser reads the cell. V1's rule is better than its example, but the example would mis-teach reviewers.
2. **V1's confirm score `min(pW, pD)` is an upper bound (X-006).** `jev-uses.md:194` says so ("the min is an upper bound under any correlation"). V1 uses it for "auto-confirm needs 0.70" without restating the limit. V2's ordinal bands avoid presenting an upper bound as confidence.
3. **V1's T6 "monotone in every input" fails against the sketch (X-008).** The sketch's own check skips any move involving UNSET (the `not (UNSET in (base[i], new))` clause). V2 states the property holds on N, U, Y only.
4. **V1 and V3 leave "highest severity wins" in place (C-017).** Verified above: the rule survives in `task/SKILL.md:252` and `tech-reference/SKILL.md:513`. A consolidator following it re-inflates blockers after a reviewer correctly grades them down.
5. **V3 is thin on evidence for its design and carries no run-2 data.** V3 has no worked examples (S-004) and no root-cause section, so it cannot say which of its mechanisms would have prevented a run-2 cycle. Its ledger machinery is larger than any observed failure: four tables, a 13-column Items table, revision counters. Run 2 produced 838 "(minor under grading override)" markers with no consolidated list, which is a read-and-offer problem, not a concurrent-writer problem. The project rule on scope discipline asks for what is asked; the identity, revision and observation tables are not.
6. **V3's confirmation lower bound does not fix its non-blocking bound.** `max(0, pW + pD - 1)` is the right conjunction bound, but its downgrade score `1 - min(1, pS + pM + pC + min(...))` is the same union bound V2 criticizes: with four mid-sized terms it reaches zero and sends nearly everything to SHOW_USER. V3 still calls it a "routing score" without a band or replicate spread.
7. **V3 omits the open question on "21 files" (diff analysis coverage table).** It says the figure is not reproduced but does not explain it (19 listed paths plus two, 8 of which carry the cap not the definition). V1 and V2 do.
8. **V1 adds extension machinery nobody asked for (S-008).** Registries for hypothetical gates, judges, scales and deliverable kinds are speculative additions under the user's scope rule. V1's `registry.yaml` for the existing 11 carriers is justified; the generic extension contracts are not.

## 6. Concessions

I accept every V2 error DA lists and add three of my own.

1. **"UNSET means send to a person" is false** (DA X-007, V3 right). Verified: `S = UNSET, W = Y, D = N` returns FOLLOW_UP; 108 FOLLOW_UP plus 108 NOTE states of 1,024 with S unset. V2's 432-lowering-moves count is true but V2 presented the effect as intended. The spec must require that an unset S or unsettled safety question never yields FOLLOW_UP or NOTE.
2. **"Eight test modules"** is incomplete (DA X-013). I confirmed `tests/review/test_review_rules_text.py`, `tests/audit/test_invariant_preservation_NFR_6_through_10.py` and `tests/audit/test_nfr_conv_9_zero_trust.py` all reference the pinned text or bullets. V2 listed neither of the first two. The union is 10 and no variant has all.
3. **V2 lists UNDETERMINED as a table verdict (A-009).** The sketch's `ORDER` has only NOTE, FOLLOW_UP, SHOW_USER, BLOCKING; an all-UNSET input returns SHOW_USER. V2 inherited this from `jev-uses.md` without testing it.
4. **V2's `[E]` claim that the highest-severity line also exists in `task-builder` and `tech-research`** is wrong on my check: the phrase "Preserve the highest severity" appears in `task/SKILL.md` and `tech-reference/SKILL.md` only. The phrase list in L1 needs correcting.
5. **V1 is right on the shared-rule location (X-001, S-005).** A skill folder gives a project `.claude/` copy and `make verify-sync` coverage; `core/` gives neither. I confirmed both installers skip only existing destinations (`install_core.py:70`, `install_skills.py:102`), so a new skill folder installs on an existing machine just as a new core file does. V2's D1 should adopt the skill location while keeping the inline block.
6. **V3's ledger identity (C-008) is stronger than V2's** `location plus quote hash` key, which breaks when a line number moves. V3's idempotent-filing protocol (C-011, U-014) is justified because `/sc:issue --create` has no preview (DA V-26). V2's ledger should adopt single-writer, atomic rewrite and a batch marker, and keep its two-table Note/Medium split.
7. V2's section 2.1 "Gate 2: 23 reviewer-level counts became 8 by consolidation" mixes the override and de-duplication; V2 says so itself. I do not claim it as evidence for the override.

## 7. Shared assumptions

| A-NNN | Verdict | One sentence |
|---|---|---|
| A-001 | ACCEPT | Re-grepped `Grade every review finding as blocking or minor` under `src/superclaude`: 11 files; V2 also notes `pragmatic.md:221` tells reviewers to hunt "false claims", a paraphrase the single-sentence count misses. |
| A-002 | QUALIFY | True for downstream gates; upstream gates have no decision basis yet (RC4), so the rule needs a consumer line from the task builder, `consumer-unknown` and the final-gate sweep. |
| A-003 | ACCEPT | `pragmatic.md:227` carries the cap word for word and the tests pin it; no variant needs to touch it. |
| A-004 | QUALIFY | Holds only if a coordinator or person opens the ledger after an unattended run, so the coordinator reading rule must name the ledger count (V2 R5). |
| A-005 | QUALIFY | The seed brief says the step 01 inventory was empty, and a blocking-only table cannot reveal real blockers called minor; the rule and loop changes must stand without it. |
| A-006 | QUALIFY | A Markdown table is the exact structure that broke in NEW-1 and NEW-2, so the plan needs one tested escaping convention and a pipe-count check on the ledger itself. |
| A-007 | QUALIFY | I confirmed `src/superclaude/hooks/hooks.json:173` registers `pragmatic-subagent.js`, but `plugins/superclaude/hooks` has no match for "pragmatic", so plugin-only installs do not get the broadcast and need per-file blocks. |
| A-008 | QUALIFY | Required-section lists and decision-basis anchors exist for some kinds (acceptance criteria, quoted constraints in `qa.md`) and not for others; where absent the question must be UNSET or `consumer-unknown`. |
| A-009 | REJECT | The sketch's `ORDER` has no UNDETERMINED and an all-UNSET input returns SHOW_USER, so the trigger to try the next judge is undefined in table terms. |
| A-010 | ACCEPT | `pragmatic.md:228` names `/sc:implement` as the protocol with its own model, and nothing in run 2 argues for changing it. |
| A-011 | ACCEPT | No key exists per `jev-uses.md` and the step makes no Jev call; shadow mode first is the only evidence-respecting order. |
| A-012 | QUALIFY | `pragmatic.md:226` says minors are not rechecked, which is safe only with the sampled audit or the final-gate sweep that catch the ones that mattered. |
| A-013 | QUALIFY | `/sc:issue --create @file` has no preview or dry-run (DA V-26), so attended filing still needs a batch marker and reconcile step to avoid duplicates. |
| A-014 | QUALIFY | `install_core.py:70` skips existing destinations unless forced, so an existing install keeps the old `pragmatic.md`; mixed versions must be detected, not assumed away. |

## 8. Point table

Preferred = the single variant whose handling is best for the final spec; for A points the verdict is shown.

| Point | Preferred | Confidence | One-line evidence |
|---|---|---|---|
| S-001 | V2 | 62 | Root-cause and worked-examples sections come before the ledger; V1 and V3 start from design. |
| S-002 | V2 | 70 | Per-statement [V]/[E]/[J]/[U] tags and 18 checks; V2 still had a false [E] claim, so the labels need a re-check. |
| S-003 | V2 | 92 | Six causes RC1 to RC6; I verified `task/SKILL.md:252` and `tech-reference/SKILL.md:513` still say highest severity wins. |
| S-004 | V2 | 90 | 14 graded cases, 10 from Gate 1; the others have none. |
| S-005 | V1 | 58 | Skill folder gets `.claude/` copy and `make verify-sync`; `core/` has neither (Makefile has no `core/` step). |
| S-006 | V2 | 52 | Two tables bound volume against 838 markers in run 2; V3's four tables exceed the observed failure. Borrow V3's identity rules. |
| S-007 | V1 | 70 | Four-layer split and a package CLI respect the rule that primitives reach code only via the CLI. |
| S-008 | V2 | 58 | Generic extension contracts are speculative under the scope rule; keep only V1's registry for existing carriers. |
| S-009 | V2 | 68 | Stage 1 collects `rests_on` data with the old rule deciding, so failure costs nothing. |
| S-010 | V1 | 52 | Nine existing modules plus T1 to T8 is closest to the union of 10; V2's T5 and T4 pins should be added. |
| S-011 | V2 | 85 | Wilson-bound triggers and a power column; V1's 5 percent target is untestable at its sample size. |
| S-012 | V2 | 55 | Evidence column on risks; low stakes. |
| C-001 | V2 | 70 | Named-consumer counterfactual plus "stated reasons count" handles P3-008 versus P3-002. |
| C-002 | V3 | 55 | "Name the affected action"; unverified protected-risk claims are not notes; pair with V2's invented-requirement guard. |
| C-003 | V2 | 55 | Keeping the word Medium avoids churn in pinned tests; RC6 shows the overload and needs a glossary line. |
| C-004 | V2 | 75 | `rests_on` names a checkable consumer; V1 and V3 only say which condition failed. |
| C-005 | V1 | 60 | Registry-driven T1 to T5 carries stage and digest version per carrier. |
| C-006 | V2 | 52 | Counts plus five rows and `consumer-unknown` first; V1's one-line low-volume form is a close second. |
| C-007 | V2 | 55 | Fix agent stops if a picked Medium proves decision-bearing and runs L2 checks; V3's separate authorization is the safer frame. |
| C-008 | V3 | 70 | V2's `location plus quote hash` breaks when line numbers move; V3 normalizes and keeps the full tuple. |
| C-009 | V2 | 52 | Keeps `notes.md` and pr-submit's own list, adding no new ledger paths; marginal over V1. |
| C-010 | V1 | 55 | `follow_up_counts` with a `show_user` key tells a coordinator when to open the ledger; V3's six keys are heavy. |
| C-011 | V3 | 62 | Batch marker and reconcile state because `/sc:issue --create` has no dry-run. |
| C-012 | V2 | 85 | The sketch reads only S, M, C, W, E, D; T, F, I, G reach no verdict cell. |
| C-013 | V2 | 80 | Three ways to get a basis and the upstream gap (no basis for research inputs today). |
| C-014 | V3 | 60 | V3 catches S=UNSET giving FOLLOW_UP (verified); V2 adds the 432 count; the spec needs both. |
| C-015 | V3 | 55 | Time budgets, circuit breaker, cache key, labels hidden from the judge; V2's field-order replicates should be added. |
| C-016 | V2 | 75 | Blind audit, seeded recall, GR1 vocabulary scan and final-gate sweep; V3's "review all protected-risk disagreements" is added. |
| C-017 | V2 | 88 | Only V2 replaces "highest severity wins" and adds fix-pass checks; verified in two skill files. |
| C-018 | V1 | 55 | Broadest own-scale coverage (11 families); V2's spec-panel reasoning is good and `pragmatic.md:231` already carries the safety clause. |
| C-019 | V3 | 55 | Wider file list (issue.md, Makefile, build script) and the correct explanation of 120 versus 139. |
| C-020 | V3 | 55 | Flags the transitive module; the union is 10 and the spec should list all. |
| C-021 | V2 | 90 | Verified Gate 1 PASS at review 3 and corrected figures in the final report; V1 repeats the 25-minute claim. |
| C-022 | V3 | 58 | Running loop pins its rule version and a mismatched consumer keeps the old gate; V2 says drift is not solved. |
| X-001 | V1 | 60 | Both installers copy a new name; only a skill gets `.claude/` sync and `verify-sync` (V2 should adopt it). |
| X-002 | V2 | 55 | One short inline block keeps the broadcast `pragmatic.md` small; V1's digest is nearly the same; V3's reference-only is the weakest. |
| X-003 | V2 | 62 | `consumer-unknown` Medium listed first covers upstream gates; V3's keep-the-old-label keeps over-blocking at the gates that caused run 2. |
| X-004 | V2 | 65 | Once per run plus at an escalation halt; `pragmatic.md:230` says once per loop and run 2 had 5 gate control files. |
| X-005 | V2 | 68 | Never auto-downgrade, only route to a person; calibration at n of 30 cannot support more. |
| X-006 | V2 | 60 | Ordinal bands with replicate spread; V3's lower bound is correct but its non-blocking bound degenerates. |
| X-007 | V3 | 80 | Verified: S=UNSET with W=Y, D=N returns FOLLOW_UP; V2 is wrong here. |
| X-008 | V2 | 70 | Precise on scope: the check skips UNSET moves; 432 lowering moves. |
| X-009 | V3 | 55 | Privacy denial skips every unapproved external judge; V2's in-session judge needs the same wording. |
| X-010 | V2 | 90 | File times and gate PASS at review 3 contradict "about 25 minutes". |
| X-011 | V2 | 85 | Verifier says the Destination cell reads wrong; V1's NOTE example is contradicted. |
| X-012 | V2 | 50 | Tag `unsettled` on a reviewer-labelled row; V3's separation is cleaner but low stakes. |
| X-013 | V3 | 55 | States the count is not exhaustive; verified there are at least 10 modules. |
| A-001 | ACCEPT | 90 | P1 grep: 11 files. |
| A-002 | QUALIFY | 80 | Upstream gates lack a basis; needs a consumer line and final sweep. |
| A-003 | ACCEPT | 90 | Cap text pinned at `pragmatic.md:227`. |
| A-004 | QUALIFY | 75 | Needs the coordinator to read the ledger count. |
| A-005 | QUALIFY | 85 | Seed brief says step 01 inventory was empty; blocking-only table is biased. |
| A-006 | QUALIFY | 80 | Markdown pipes are the NEW-1 defect. |
| A-007 | QUALIFY | 85 | hooks.json:173 registers it; plugin hooks have no match. |
| A-008 | QUALIFY | 65 | Basis anchors exist for some kinds only. |
| A-009 | REJECT | 90 | `ORDER` has no UNDETERMINED; all-UNSET gives SHOW_USER. |
| A-010 | ACCEPT | 85 | `pragmatic.md:228` names the exemption. |
| A-011 | ACCEPT | 85 | No key, no call. |
| A-012 | QUALIFY | 75 | Needs the audit or sweep. |
| A-013 | QUALIFY | 75 | No preview or dry-run on create. |
| A-014 | QUALIFY | 85 | `install_core.py:70` skips existing files. |

## 9. Own live checks (beyond DA)

1. `pragmatic.md` lines 219 to 232 read: S1 at 225, cap at 227, exemption at 228, Medium and `once per loop` at 230, spec-panel scale with a safety clause at 231.
2. `grep -rlF` for the P1 sentence under `src/superclaude`: 11 files.
3. "Preserve the highest severity" appears in `task/SKILL.md` and `tech-reference/SKILL.md` only.
4. `gate1-cycle-control.md`: line 9 has NEW-1 and Destination; line 38 "Final verdict: PASS at review 3"; five `gateN-cycle-control.md` files exist in `R2/qa/`.
5. The sketch (`uv run python`): `S=UNSET,N,N,Y,N,N` gives FOLLOW_UP, `S=U` gives SHOW_USER; S=UNSET distribution 511/297/108/108; all-UNSET gives SHOW_USER.
6. `R2/RESEARCH-REPORT...run2.md` lines 1015 and 3066 to 3068 read as V2 says.
7. `install_core.py:70` and `install_skills.py:102` both skip existing destinations unless forced.
8. `hooks.json:173` registers `pragmatic-subagent.js`; `plugins/superclaude/hooks` has no "pragmatic" match; `Makefile` has no `core/` step; `.claude/WORKER-CONTRACT.md` is absent.
9. `jev-uses.md:194`: "the min is an upper bound under any correlation".
10. Not verified by me: whether the value-inventory step parses ledgers by column position (decides NEW-1), and whether `plugins/superclaude/hooks/hooks.json` registers the broadcast under another name.
