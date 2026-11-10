# Review of SPEC.md (spec-panel-minfix, issue #346)

verdict: FAIL

Target: `.dev/brainstorms/346-minfix/SPEC.md` (236 lines, read in full). Reviewer did not write it. All file content was treated as data. Line numbers below are SPEC.md lines unless a file is named.

## Blocking issues

### SR-B1. With Arm B's flags, the cycle-2 baseline the Reviser brief names is the wrong copy, so cycle 2 is never checked or enforced
- SPEC sections: 2.1 step 2 item 1 (line 37), 3.2 Reviser brief item 1 (line 121), 4 "one-line substitution" (lines 170-176), 6 risk table (line 214), 2.1 step 3 (line 44).
- Evidence:
  - The Reviser brief says "Baseline: <the saved copy, when this review's brief supplied its path>" (SPEC.md:121; same rule at :37).
  - Arm C = Arm B briefs (SPEC.md:170). Arm B's R2 review brief passes `--baseline .dev/orca-command-refactor/specs/history/spec-v1-draft.md` and the R3 brief passes `--baseline .../spec-v2-after-round1.md` (`exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md:60-61`; `phase4/coordinator-log.md:59-69`). 427 defines that copy as the text the PRIOR review saw (`docs/designs/spec-panel-review-loop.md:50`).
  - So review 2's brief names exactly one saved copy, v1, which is the cycle-1 baseline. Cycle 2 needs v2, the text review 2 saw. v2 exists (the coordinator saves it before review 2, `DECISIONS.md:62`), but no review brief names it.
  - The reviser takes v1. `check` then exits 4 on the hash mismatch (SPEC.md:146, "`check` on a mismatched baseline exit 4"). That happens after the edits, at step 4 (SPEC.md:124). The reviser then "edit[s] nothing further", so `--enforce` never runs in cycle 2. V7 fails in every replicate where the reviewer follows the text literally (SPEC.md:181), so Arm C produces no valid treatment replicate.
  - The design missed this because it assumed the S1 review briefs name no saved copy (`merged-requirements.md:149`, "not true of the S1 review briefs T05, T07 and T09 today"). SPEC.md:214 repeats that assumption ("no S1 review brief names a saved-copy path"). It is false for Arm B/Arm C, where T07 and T09 carry `--baseline`.
  - SPEC.md:44 stops the re-review only on the reviewer's own `check` exit 3/4/5/70. The merged text also stopped when the disposition's last `FIXCHECK` line showed exit 3/4/5/70 (`merged-requirements.md:185`). The SPEC dropped that rule, so an unenforced cycle 2 continues into review 3 and nothing flags it.
  - Using `snapshot` in cycle 2 collides with T08's ownership clause, which is stricter than T06's: "edit ONLY the spec and write ONLY disposition-round2.md" (`phase2/S1/briefs/templates/T08-R2-reviser.TEMPLATE.txt:1`). The risk row at SPEC.md:214 quotes only T06's wording.
- Exact correction:
  1. Replace Reviser brief item 1 (SPEC.md:121) and step 2 item 1 (:37) with: "Baseline: a copy whose sha256 equals this report's `reviewed_sha256`. The `--baseline` passed to a re-review is the text the PREVIOUS review saw and is never this cycle's baseline. If this review's brief names no such copy, run `snapshot` before the first edit." Have the reviewer check any candidate with `hash` before naming it.
  2. Add to step 3 (SPEC.md:44) and to the Fix Budget re-review sentence (:117): "or the disposition's last `FIXCHECK` line shows exit 3, 4, 5 or 70".
  3. Correct SPEC.md:214. In Arm C, T07 and T09 name the previous cycle's copy. In cycle 2 the reviser must run `snapshot` against T08's "write ONLY disposition-round2.md". The pilot must therefore cover both fix cycles, not only cycle 1 (amend SPEC.md:179). The alternative is to name `specs/history/spec-v2-after-round1.md` in T08 and declare that as a second brief change in section 4.

### SR-B2. The re-review's `check` needs the ledger file, but the command interface never says where it comes from
- SPEC sections: 2.1 step 3 (line 44), 3.2 region 1 and Fix Budget (lines 94, 117), 3.5 (line 151).
- Evidence:
  - The re-review runs `check ... --ledger <disposition file>`. A missing input "stops the review ... and escalates" (SPEC.md:44, :117).
  - The variant's Usage line changes only the command name (SPEC.md:94). It keeps 427's flags, which carry only the prior report and the saved copy (`src/superclaude/commands/spec-panel.md:22`). No rule tells the reviewer how to find the disposition file.
  - In S1 this works only because T07 and T09 happen to list `disposition.md` and `disposition-round2.md` as inputs (`templates/T07-R2-reviewer.TEMPLATE.txt:1`, `T09-R3-reviewer.TEMPLATE.txt:1`).
  - Any other invocation stops at review 2 every time. That includes the later adopters (SPEC.md:151) and the fold-back (SPEC.md:234). At review 3 the folder `review/` holds two files with `fixledger` blocks, so a guessed lookup would be ambiguous.
- Exact correction: Add to Reviser brief item 3 (SPEC.md:123): "the `fixledger` block's first line is `report: <this report's file name>`". Add to step 3 and the Fix Budget re-review sentence: "the ledger is the one file in the prior report's directory whose `fixledger` block names the prior report; none or more than one is an input error (exit 3)". Teach `parse_ledger` and `check` that lookup (SPEC.md:130), and add a test for it in 3.4. This keeps the one-line brief substitution valid.

### SR-B3. What `check` returns after `--enforce` contradicts the spec's own exit-1 rules, and no action is defined when `--enforce` exits 1
- SPEC sections: 2.1 step 2 item 5 (line 41), 2.3 exit codes (line 60), 3.2 Reviser brief item 4 (line 124), 3.4 property test (line 146).
- Evidence:
  - "Blocking id neither fixed nor deferred" is a policy failure, exit 1 (SPEC.md:60). `--enforce` writes only the spec, never the ledger or disposition (SPEC.md:60, "Only `check --enforce` writes the spec").
  - Case 1: a blocking id the reviser neither edited nor deferred, and still missing after the one cut-down pass. `--enforce` has nothing to revert, so its own re-check exits 1.
  - Case 2: a finding that `--enforce` reverted whole. Its ledger entries remain, but no hunk matches them. The SPEC never defines how a later plain `check` (the re-review's authoritative run, SPEC.md:44) scores such an entry.
  - Both cases contradict the promised property "always ends with `check` = 0 after `--enforce`" (SPEC.md:146). Reviser brief item 4 (SPEC.md:124) gives actions for exit 1 (before enforce), 2, 3, 4, 5 and 70, but none for `--enforce` itself exiting 1.
- Exact correction: In 2.3 and 3.3, define three things:
  - `--enforce` lists every reverted finding, and every blocking id with no entry and no deferred line, as `escalated`, then exits 0.
  - A plain `check` scores an entry as `reverted` (status escalated, not a policy failure) when its `old`/`anchor` text is intact and its `new` words are absent.
  - Reviser brief item 4 gains: "if `--enforce` exits non-zero, edit nothing further and paste the output".
  
  Restate the property test as "after `--enforce`, a plain `check` on the same four inputs exits 0".

### SR-B4. `attacks: L<n>/<finding id>` cannot be computed from the specified checker output
- SPEC sections: 2.1 step 3 (line 44), 2.1 step 2 item 4 (line 40), 3.3 report example (lines 133-141), 5 extra metrics and derivation (lines 183, 187).
- Evidence:
  - Every `origin=changed` finding must carry `attacks: L<n>/<finding id>`, "taken from the run's hunks". The reviewer must copy only ids and numbers from the run (SPEC.md:44).
  - The specified output has per-finding totals and unattributed hunks only (SPEC.md:133-141). There is no per-hunk line giving a revised-spec line range and its ledger entry.
  - The ledger entry format (SPEC.md:40) never defines entry numbering `L<n>`. Only `depends: L<n>` hints that numbers exist. The merged text defined `## L<n>` entries (`merged-requirements.md:339`) and a lookup "by the finding's quoted line in this run's hunks" (`merged-requirements.md:183`). The SPEC dropped both.
  - The measurement plan depends on this column: "the arm measures both [assumed inputs] through `attacks:`" (SPEC.md:187; also :183).
- Exact correction:
  - In 2.1 step 2 item 4: "entries are `## L1`, `## L2`, ... inside the `fixledger` block".
  - In 2.2/3.3, `render_report` prints one line per hunk: `h<k> L<n>|unattributed <finding id> revised:<first line>-<last line> +<added words>/-<deleted words>`. Add it to the report example.
  - In step 3: the reviewer takes `L<n>` from the hunk whose revised line range contains the line the finding quotes.
  - Add a test that the per-hunk lines exist and are deterministic.

### SR-B5. The review-3 prediction (3.3, band 1.1 to 5.6) does not follow from the derivation printed beside it, and the derivation's class letters are never defined
- SPEC sections: 5 (line 187), 1 (line 8), 2.4 (line 66).
- Evidence:
  - The SPEC's own derivation gives review 3 = 2.1, 3.0 or 4.0 (SPEC.md:187). The middle case, 3.0, sits at the bar, not 3.3. Nothing in the SPEC produces 1.1 or 5.6.
  - The source labels 3.3 "central 3.3 (judgment)" and takes the band from elsewhere (`merged-requirements.md:459`). The SPEC drops the "judgment" label, so a reader takes 3.3 as computed.
  - The removal weights "A 0.9, D 0.6, B 0.5, C 0.3, E 0" and "shapes A-D" (SPEC.md:66, :187) use letters SPEC.md never assigns. Section 1 (line 8) lists the shapes without letters.
  - The 0.49 figure is reproducible only with the source's mapping (`merged-requirements.md:82-86`: A non-blocking 3, B universal 2, C check recipe 3, D mechanism 3, E other 2; (3x0.9+2x0.5+3x0.3+3x0.6)/13 = 0.49). The acceptance criteria require the spec to stand alone.
- Exact correction:
  - In section 1, line 8, label the shapes: "A fixing a non-blocking finding (3), B universal/closed claim (2), C check recipe or acceptance step (3), D mechanism where a deletion was offered (3), E flawed recommendation or interacting fixes (2)".
  - In section 5, write: "Derived: 2.1 / 3.0 / 4.0 at 25 / 50 / 75% replacement (central 3.0). Stated prediction 3.3 is a judgment adjustment upward because <reason>." Then either give the band's derivation or replace 1.1-5.6 with the derived 2.1-4.0 and label any widening as judgment.

### SR-B6. The growth prediction and its "hard ceiling" are in words, but the bar's growth metric is bytes
- SPEC sections: 5 (lines 185, 194), 2.4 (line 72).
- Evidence:
  - The A/B and Arm B growth figures, and so the 63.5% control mean and the 44.4% bar, are byte growth. flg-r2 `growth_percent_cumulative_vs_v1` is 32.14, from 57,763 to 76,328 bytes. Its word growth is 33.05 (`exp346-ab-flg-r2/.dev/experiments/346-validation/phase4/flg-r2/metrics.json:405-414`). ARMB-REPORT.md:16 reports +32.1%.
  - SPEC.md:185 compares its replay to "the actual 33.1%", which is the word figure, not the reported 32.1%. It then states the prediction "about 13% (range 8% to 14.7%)". 14.7% is the WORD ceiling. In the metric the bar uses, the checker allows up to 21.3% (12,288 / 57,763) with exit 0 (SPEC.md:72).
  - A valid replicate at, say, 17% byte growth with exit 0 falls outside the stated range. Under the ambiguous falsifier at SPEC.md:194 ("growth above the 14.7% / 21.3% ceiling while the script reports exit 0 (a checker bug)") it could be voided as a checker bug.
- Exact correction: In section 5, state that the growth metric is M4 byte growth (the recorders' `growth_percent_cumulative_vs_v1`). Give the prediction in bytes, with the range's upper end at the 21.3% byte ceiling; the word replay of 14.4% and 13.4% stays as supporting evidence. Change "the actual 33.1%" to "the actual 33.1% in words (32.1% in bytes)". Rewrite the falsifier as "word growth above 14.7% or byte growth above 21.3% while the script reports exit 0".

## Minor notes

- **m1. Scope sentences disagree.** The Fix Budget opening sentence says it "Applies to a critique-mode report that ends `verdict: FAIL` below `review: 3`" (SPEC.md:103). The same section says "In every critique-mode review, run `hash`" (:117), and Step 0 runs on "every run" (:17), which includes discussion and socratic modes. Make all three "every critique-mode run".
- **m2. Exit-code lists drift.** SPEC.md:60 lists "quote not in baseline, mislabelled op, blocking id neither fixed nor deferred". The Fix Budget line (:115) says "ledger incomplete". Step 2 item 5 (:41) omits the exit-2 action that the Reviser brief (:124) has. Use one list everywhere, as the test at :147 pins it to the constants.
- **m3. Word lists differ.** The normative list includes lowercase `shall` (SPEC.md:48), but the Fix Budget column header omits it (:107).
- **m4. `refs:` undefined.** `refs: SPEC` / `refs: <prefix>` (SPEC.md:24, :117) is never defined. It presumably means the citation prefix whose `path:line` tokens are not counted as words.
- **m5. Regressed ids.** "Per prior blocking id still open" (SPEC.md:19, :117) should read "open or regressed". Otherwise a `regressed` id named in the Reviser brief has no `fixbudget` line, and `parse_fixbudget` exits 3 (:130).
- **m6. Control numbers under a 427 claim.** Section 1 line 7 says "Revisers still add 955-3,327 words ... against 84-379 deleted" right after the 427 sentence. 3,327 and 379 are control numbers (ctl-r2). The 427 loops alone are 955-2,244 added and 84-258 deleted (`merged-requirements.md:28-33`).
- **m7. Missing UNVERIFIED mark.** The 13-chain shape classification (SPEC.md:8) is "measured by one analyst, UNVERIFIED by a second reader" in its source (`merged-requirements.md:453`, also :53). SPEC states it without that mark.
- **m8. Wrong decision cited.** "D9: parallel arms need different command names" (SPEC.md:154). D9 is about user copy beating project copy (`DECISIONS.md:45-47`). The parallel-arms fact is `phase4/AB-REPORT.md:47`.
- **m9. Watcher not yet built.** "The install watcher logs the three sha256 values" (SPEC.md:166) describes a watcher that does not exist yet. The D10 watcher logs only the spec-panel sha256 and WORKER-CONTRACT.md presence (`DECISIONS.md:51`). Say it must be extended.
- **m10. Concurrent controls.** "Or new controls run at the same time, which the different command name allows" (SPEC.md:179) conflicts with the install note that never writes `spec-panel.md` (:166). The owner's copy is the 486-line master text, not the pre-427 control text, so a concurrent control needs its own command name.
- **m11. Region 3 changes more than its path.** It replaces the template path with "the inline output schema" (SPEC.md:96). That schema is not defined anywhere, and the change alters TDD release-spec behaviour. S1 does not exercise it, but name the schema or keep the step's behaviour.
- **m12. Briefs checked in the wrong folder.** The substitution was verified on `task-text/` (SPEC.md:176), but Arm B actually used `briefs/templates/T07/T08/T09-*.TEMPLATE.txt` (`coordinator-log.md:59-69`). I checked both: each of T05, T07 and T09 contains `/sc:spec-panel @` exactly once, and T06/T08 contain none, so the substitution holds. Cite the templates.
- **m13. Experiment file not listed.** The experiment build file `<experiment build>/spec-panel-minfix.md` (SPEC.md:161) is not in the 3.1 file table. State where it is produced and that it is not committed under `src/`.
- **m14. Byte ceiling not strictly hard.** Normalisation drops whitespace, table padding and emphasis (SPEC.md:48), so re-padding a table adds uncounted bytes. The byte ceiling is therefore not strictly hard, and the "checker bug" falsifier (:194) could fire on a correct checker.
- **m15. Reviser brief incomplete.** Item 2 (SPEC.md:122) omits the CRITICAL entries limit (6) and the add-only limits. It also does not restate 427 bullet 6's "revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for", which bullet 6 requires the brief to restate (`spec-panel.md:263`).
- **m16. Permission prompt not checked.** Whether an Orca worker's permission mode runs `uv run --no-project python ~/.claude/skills/...` without a prompt is UNVERIFIED. Add it to the pilot check (SPEC.md:168).
- **m17. Stale skill copies.** `cp -rn` onto an existing stale `~/.claude/skills/sc-fixcheck/` keeps old files silently (SPEC.md:162). The printed sha256 covers only `fixcheck.py`; hash `SKILL.md` too.
- **m18. 0.66 is the plain average.** It is the arithmetic mean of eight per-cycle ratios (`merged-requirements.md:102`). With zero removal it gives 12 x 0.66^2 = 5.2, while the four 427 loops actually averaged 4.5 at review 3 (ARMB-REPORT.md:13). Note that the baseline of the derivation is pessimistic.
- **m19. Unlisted risk from the S1 review briefs.** They say "any finding of any severity is FAIL" (`templates/T07-R2-reviewer.TEMPLATE.txt:1`, `T09-...:1`), which contradicts 427 bullet 7. This is the same in Arm B and not a minfix defect, but it can block the "clean pass" outcome predicted at SPEC.md:187. List it as a risk.

## Self-Audit

What I checked, with the source read:
- **SPEC.md** in full (236 lines).
- **Merged design.** `merged-requirements.md` sections 1.1-1.6 (lines 20-114), step 2-3 text (170-189), predictions (436-475), plus targeted greps for the hash, ledger and `attacks:` rules.
- **427 ground truth.** `src/superclaude/commands/spec-panel.md` Usage (19-24), lines 205-284 (template path at 220, Review Loop 256-264), and 430-487 (`## Unattended mode` at 451). Grep confirmed line 220 is the only `src/superclaude` hit, so region 3 removes the only source path. The Fix Budget literal text names none.
- **427 design.** `docs/designs/spec-panel-review-loop.md` in full: the quote at :73 is correct, C6 at :30, saved-copy meaning at :50.
- **Tests.**
  - `tests/skills/test_spec_panel_review_loop.py` in full. Its pins (T3-T9) apply only to the two spec-panel files. Bullets 1-5 and 7 of the variant stay byte-identical, and bullet 6 keeps `Reviser brief` and `byte size before and after`, so the 427 literals hold in the variant.
  - `test_worker_contract.py:740-860`: `_check_no_unattended_sections` scans `src/superclaude/commands/*.md` for an exact set, so the region-2 removal is required and correct.
  - `test_review_severity_rule.py` matchers (any-severity, old cap, sweep F1-F6, zero tolerance): no Fix Budget sentence trips them, by hand check (not run).
- **Installer.** `install_skills.py:40-104`: `sc-fixcheck` has no `commands/fixcheck.md`, so it installs as a skill.
- **Precedents.** `sc-issue-protocol/SKILL.md:72` (`uv run --no-project` precedent) and `rf-qa.md:379-416` (Fix Cycle) are correct.
- **Experiment data.**
  - AB-REPORT.md and ARMB-REPORT.md in full. Correct as quoted: 63.5 / 29.7 / 30.0%, 6.0 / 5.5 / 3.5, bar 3 and 44.4%, 89-100% `origin=changed`, controls 8 and 4, c8d80346a96c, 472 lines.
  - DECISIONS.md D9-D13.
  - The coordinator log lines for Arm B, brief texts T05-T09 in `task-text/` and `templates/`, with occurrence counts by grep.
  - The flg-r2 history file sizes and `metrics.json` growth fields.
  - Quotes "The Task 6 brief wins" (flg-r1 `disposition.md:10`), "Residue of round-1 finding 5" (ctl-r1 `spec-panel-round2.md:195`) and the N4 "only two files" chain (flg-r2 `spec-panel-round2.md:113-114`).
- **Arithmetic re-done.** 1,200/8,148 = 14.7%; 12,288/57,763 = 21.3%; 0.49 removal; ratios 0.42/0.50/0.58; review-3 values 2.1/3.0/4.0; 0.66 as the mean of eight transitions; cost totals 11-28 calls; 8-18 of 78 minutes = 10-23%.
- **Loop walk-through.** Review 1, cycle 1, review 2, cycle 2, review 3 under Arm B's actual flags. Every exit (0/1/2/3/4/5/70, `--enforce`, E-FIXCHECK-MISSING) traced to a PASS, an escalation or a defined next step. The gaps found are SR-B1 to SR-B4.

Not checked: 95f2c6e4's file content (no git allowed), the brainstorm's `nested/` artifacts, the routing and plugin-parity tests the SPEC already marks "check first", and whether any test actually passes (nothing was run).
