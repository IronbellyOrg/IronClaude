# Evidence-validator result (Wave 5)

Written by the orchestrator verbatim from the evidence-validator's returned block (the agent is Read-only). The block is YAML-shaped but not strictly parseable (unquoted inner quotes on two claim_excerpt lines), so it is stored as a record, not as a .yaml file.

```yaml
citations_total: 117   # my own enumeration of distinct cited ranges came to 116 to 117; the draft's figure is used
citations_revalidated: 108
citations_dropped: 8
dropped:
  - report_line: 122-126
    citation: "TL:184"
    claim_excerpt: "Further anchors from the merged verdict: ... TL:184 ..." (F-01 owner-gate deadlock)
    reason: "TL:184 reads 'These files persist across all batches and session rollovers. Later items read them by path.' It has no HALT, Branch or owner-answer text. Within plus or minus 3 lines (181-187) there is only the handoff folder list and the QA Gate Protocol heading. The HALT rule is at TL:192, 8 lines away."
  - report_line: 126
    citation: "TL:1298-1314"
    claim_excerpt: "Further anchors from the merged verdict: ... TL:1298-1314" (F-01 owner-gate deadlock)
    reason: "These are the QA decisions lens items 7.22 to 7.24: spawn instructions and lens prompts. None has a Branch 1 or Branch 2 test or an owner-answer step. The only link to F-01 is the record-form lens naming `Chosen:`, which is not a deadlock. The 7.24 lens at TL:1314 stays supported as a D-03 citation."
  - report_line: 139
    citation: "DESIGN:466"
    claim_excerpt: "The check does not list the names it expects. DESIGN:466 and the constants line DESIGN:468 ... are not spelled out"
    reason: "The line does hold SweepResult. The claim it is attached to is refuted: TL:1431 lists SweepResult (line 466) and the other classes by name. TL:1434 checks 'every class and constant name in DESIGN section 7.2'. Only the Verification line omits an explicit list."
  - report_line: 139
    citation: "DESIGN:468"
    claim_excerpt: "the constants line DESIGN:468 (JSON_SCHEMA_VERSION, CLASSES, PACKAGE_STATES, SAFE_VALUES) are not spelled out"
    reason: "The names do appear at DESIGN:468. The claim that the 8.3 name set leaves the constants out is refuted by TL:1431, which says 'the constants JSON_SCHEMA_VERSION = 1, CLASSES (8 names), PACKAGE_STATES, SAFE_VALUES'. TL:1434 says 'class and constant name' and TL:1435 says 'holds every DESIGN 7.2 name'. DESIGN:447-468 stays valid in R-02, where it is only a list of names to write out."
  - report_line: 319, 602
    citation: "conftest.py:59-74"
    claim_excerpt: "Make the fake record the argv and env it receives, as `patch_git` does"
    reason: "Lines 58-80 of tests/cli/reflect/conftest.py hold a patch_git whose _fake_git returns canned values. It records no argv, no env and no calls. A grep of that file for argv, record and calls finds nothing. The claim that patch_git records argv and env is unsupported."
  - report_line: 316, 602
    citation: "TL:1467"
    claim_excerpt: "The 8.8 fake seam does not record argv and env"
    reason: "TL:1467 says 'patch_git (records (cwd, args, timeout) and the env the real _git would build ...); patch_orca (records argv, ...)'. The cited line shows argv and env ARE recorded, which contradicts the claim. At most patch_orca lacks env, and the draft does not say that. TL:1467-1476 stays valid as the D-08 range, which is a different claim."
  - report_line: 329, 610
    citation: "DESIGN:940"
    claim_excerpt: "Item 14.5 counts the whole tree instead of the five DESIGN folders ... DESIGN:939, DESIGN:940"
    reason: "DESIGN:940 is step 1.29, the pipx `superclaude sweep --help` check. It names no folders. The draft itself says the pipx clause was dropped (X-006). DESIGN:939 does name the five folders (commands, skills, agents, core, hooks) and stays."
  - report_line: 360
    citation: "TL:1784"
    claim_excerpt: "Several FR and NFR ids are not written on their delivery items (Location TL:1784)"
    reason: "TL:1784 is the Context of item 10.2 (test_classify.py). It is not one of the mapped items 12.1, 8.10, 8.6, 10.7 or 10.3, and it does write FR and NFR ids. It cannot show an id is missing. TL:1784-1785 stays valid as the D-23 NFR-004 evidence."
corrected:
  - report_line: 178
    citation: "TL:1326-1331 (D-05 Location, and R-05 Change)"
    correct_line: "TL:155-165"
    note: "The claim is true: the Key Constraints carry no GAPS line 138 rule. But TL:1326-1331 is item 7.26, the QA decisions downstream-actionability lens, not the Key Constraints. The '### Key Constraints' heading is at TL:155 and its bullets run to TL:165. The bullets at TL:156-165 contain no 'GAPS line 138' or '113 rows, 88 open, 25 resolved' text. The R-05 verifier 'Re-Read TL:1326-1331' should also point at TL:155-165."
inf_rows_dropped: []
special_checks:
  - id: D-02
    result: "REFUTED as worded; the counting-method gap holds."
    evidence: "TL:1431 lists the constants JSON_SCHEMA_VERSION = 1, CLASSES (8 names), PACKAGE_STATES and SAFE_VALUES. TL:1434 checks 'every class and constant name in DESIGN section 7.2 appears once (`grep -c` per name)'. TL:1435 says the module 'holds every DESIGN 7.2 name'. The 8.3 name set therefore does NOT omit the DESIGN 7.2 constants. The synthesis note in the draft is right: the defect is that `grep -c` counts every line containing a name (SessionRow also appears at TL:1431 as `row: SessionRow`) and the check prints no explicit list in the Verification line. DESIGN:466 and DESIGN:468 were dropped from the 'not spelled out' sentence. The 'omits the constants' reading must not reach the final report. ClassifiedRow is a builder decision at TL:1431 and DESIGN:466 uses the name inside SweepResult.rows, so 'is not a DESIGN 7.2 name' is only partly accurate."
  - id: D-05
    result: "CONFIRMED."
    evidence: "DESIGN:78 reads: 'GQ-111 and GQ-112: wherever this design or a later task needs the gaps-log count, it cites GAPS line 138: 113 rows, 88 open, 25 resolved.' DESIGN:80 holds the /task-builder copy rule quoted for INF-001. The Location TL:1326-1331 is wrong (see corrected); the Key Constraints are at TL:155-165."
  - id: D-10
    result: "CONFIRMED with one caveat."
    evidence: "TL:233 is item 1.4's Verification. It handles status MOVED ('reads its current line from this file when the status is MOVED') and 'If a file is missing, log the blocker ... and stop'. It has no CHANGED HALT. TL:231 lists CHANGED as a status value, and TL:229-234 is the whole of item 1.4. A grep of the tasklist for CHANGED returns only TL:231, TL:829 and TL:831. TL:829 and TL:831 are item 5.10's DESIGN-edit rule, not a HALT, and not item 1.4. So no CHANGED HALT exists for item 1.4. Caveat: TL:224 is in item 1.3 (base-sha drift). It does only add a note to '### Phase 1 Findings' that anchors must be re-checked. It is accurate as 'only adds a note' but is not item 1.4's CHANGED handling. WORKER-CONTRACT.md:110 ('The sweep.') and test_worker_contract.py:25 (RULE_PHRASES) and :155-173 (WC-13 to heartbeats entries) are anchors that match the TL:230 inventory, so they are retained."
self_audit: |
  I read the whole draft in 150-line chunks. I then Read each cited range in the tasklist, DESIGN, research/04, WORKER-CONTRACT.md, test_worker_contract.py, conftest.py, contracts/__init__.py and coverage-matrix.yaml. I used Grep to test for absence (CHANGED, FR-010, Key Constraints, WC-16 in DESIGN, argv or record in conftest.py).
  Verified with no change:
  - All 15 INF verbatim quotes match their DESIGN lines exactly (80, 88, 101, 103, 215, 217, 218, 219, 705, 707, 708, 719, 731, 902, 942). INF-013's quote at DESIGN:731 is a faithful prefix of the line. The coverage-matrix rows at 849-880 also match the quotes for INF-005 to INF-008.
  - D-01: TL:989, 982, 978, 1140, 1151, 1165, 1179, 1193, 1207, 1221, 1242, 192, 2481-2484, 988, 1138, 1242-1248 and 2488 (which shows a resume pattern in branch B).
  - D-03: TL:1248-1260 and 1314. The 1260 grep does not contain `check`, while the 1257 forbidden list does.
  - D-04, D-06 to D-09, D-11 to D-16, D-19 to D-23 and R-01 to R-23 citations.
  - D-11: TL:827 is the 5.10 header and its Action at TL:829, 2 lines away, holds the bare 'line N' wording.
  - D-12: research/04:90, 115-116 and 148.
  - D-16: contracts/__init__.py:1-6, 35-36 and 302-313.
  - D-23: coverage-matrix:232-237 (the NFR-004 row) and 849-880 (INF-005 to INF-008, which skip B2).
  Reasons for dropping rather than keeping: the F-01 'further anchors' list is a bag of lines with no individual claim, so each line was judged on whether it touches HALT or owner-answer text. Two did not. DESIGN:466 and DESIGN:468 were dropped because the sentence they sit in is refuted by TL:1431. The conftest.py:59-74 citation was dropped because the reflect conftest's patch_git records nothing. DESIGN:940 and TL:1784 were dropped because they do not carry the claim they are attached to.
  Weaker items I kept, which the orchestrator may want to look at:
  - D-06 labels DESIGN:5 and DESIGN:988 'WC-16', but those unrevised lines say WC-14. TL:779 explains that these are the WC-14 lines R4 renames, so they stay.
  - D-12 cites TL:423 (a header) and research/04:115-116 (window fixtures). They are context, not wording evidence.
  - D-07 says 'one PASS'. Item 8.1 does write one PASS or FAIL line per check, and the grep check covers six files, so the claim holds.
  - D-18 and D-20 map to item numbers I did not re-derive (14.5 and the 9.2 item). I confirmed only the cited lines.
  I did not Read research/04 lines 87-88 directly. The draft cites them only through TL:1431, which quotes them.
  Total count: I enumerated about 116 to 117 distinct ranges, in line with the draft's stated figure of about 117. 'Revalidated' = 117 - 8 dropped - 1 corrected = 108.
```
