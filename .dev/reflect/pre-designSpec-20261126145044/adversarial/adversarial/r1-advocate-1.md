# Advocate for variant 1 (analyzer)

## 1 Position
Variant 1 has the widest verified evidence base and the best-calibrated grades on most points, but it under-graded the missing whole-run estimate and the missing freeze mechanism, and over-graded two fixable checks. A merge that keeps its unique finds (UNSET in Gate 1, band mapping) and takes V3's Missing grades is best.

## 2 Steelman of variants 2 and 3
V2 saw that one rule in Task 6 (rerun on any non-ok, stop on four named signals) cannot work against client.py:114-117 and 127-131, and that the plan's own line 30 shows the mock-backed path exists. Its focus is sharp. V3 found the most structural gaps: no freeze or manifest-write command, a `tests_passed` event with one hash against several checked files, a README that omits "how to rescore" (source.md:34), and untracked paths in the spec layout. Its blocking_reason field on every finding is cleaner.

## 3 Strengths of variant 1
- F-3 is exact: `jevlib/__init__.py:5` exports only MODEL, API_URL, KEY_ENV; `client.py:114-117` returns `refused`/`budget_exhausted`.
- F-8 is unique and true: plan:103 adds "no UNSET" to Gate 1; source.md:72 does not, and plan:29 says only the scorer refuses UNSET.
- F-1 is true: plan:47 greps the word "keyword", not a cue.
- F-7 is true: plan:71 names operators only, no band mapping.
- Its clean list recomputed the sign test (8-2: tail 56, 1120 < 1024 false) and the plan matches.

## 4 Weaknesses of variants 2 and 3
- V2 has four findings, all Task 6, all Blocking. It misses Gate 1/UNSET, the band, README, paths. Its F-3 ignores that plan:30 documents the `live=False` choice with a verified reason (client.py:127-131). Its F-1 (imports) is wording that the first test run exposes.
- V3 F-6 (order inverted) is unverified: `verdict(result, rule, run_meta)` at plan:84 takes run_meta, so it need not read Task 5 formats. F-7 (reuse Journal) is an improvement, not a defect; plan:57 already offers `sha256_file` to Task 5, which depends on Task 2. F-5 and F-8 are Blocking for a fixable check. V3 misses UNSET-in-Gate-1 and the band.

## 5 Concessions
- C-001: plan:103,119,124 have no whole-run estimate that source.md:82 requires, so Missing is right; V1's Medium was too low.
- C-007: no freeze, manifest-write or gate command exists, though plan:156 requires one; V1's Medium was too low.
- C-005 and C-006 are fixable checks, so Not Decision; V1's Blocking-Decision was too high under the grade rule.
- V1 bundled the imports point into F-3 and graded it Medium; it is wording.

## 6 SCORING
C-001 | valid yes | grade Blocking-Missing | confidence 65 | source.md:82 vs plan:103,119,124; budget.py:63 reserve_phase unused
C-002 | valid yes | grade Medium | confidence 58 | client.py:114-117,127-131; validate.py:32-33; plan:125 acceptance already demands the stops
C-003 | valid yes | grade Medium | confidence 72 | plan:30 documents the departure; plan:119 contradicts itself on --live and gates
C-004 | valid yes | grade Note | confidence 68 | jevlib/__init__.py:5; plan:117 wording only
C-005 | valid yes | grade Medium | confidence 65 | plan:47 greps "keyword"; SKILL.md:154,156 option names hit cues; fixable check
C-006 | valid yes | grade Medium | confidence 62 | plan:159 vs session git status (untracked .dev/brainstorms, issues, reflect); fixable check
C-007 | valid yes | grade Blocking-Missing | confidence 52 | plan:99-103,156; no freeze/manifest command
C-008 | valid yes | grade Blocking-Decision | confidence 52 | plan:103,107 vs source.md:72, plan:29; needs an owner choice
C-009 | valid yes | grade Medium | confidence 70 | source.md:42,44 vs plan:84,151; no run-record.md in the plan
C-010 | valid yes | grade Medium | confidence 55 | source.md:34 vs plan:153,156-157
C-011 | valid yes | grade Medium | confidence 60 | source.md:104; no plan task mentions Refs #611
C-012 | valid no | grade Not-a-defect | confidence 55 | plan:84 takes run_meta; plan:97 dependency is for hashing
C-013 | valid yes | grade Note | confidence 60 | plan:57 vs plan:101,103; source.md:68; implementer would import it
C-014 | valid yes | grade Medium | confidence 60 | plan:71,76; source.md:77; no band mapping stated
C-015 | valid yes | grade Note | confidence 65 | SKILL.md:152-159 (152 heading, 153-158 rows, 159 ambiguity rule); plan:137,141
C-016 | valid no | grade Not-a-defect | confidence 85 | plan:19,21 cover it

X-001 | Blocking-Missing | 65 | required whole-run estimate absent in substance
X-002 | Medium | 58 | fixable sentence; plan:125 acceptance already requires the stops
X-003 | Medium | 72 | reason stated at plan:30; V2's Blocking over-grades
X-004 | Note | 68 | wording
X-005 | Medium | 65 | fixable check, not Decision
X-006 | Blocking-Missing | 52 | gates have no freeze path; borderline Medium

S-001 | winner MERGE | 70 | V1 breadth and calibration with V3's structural finds; V2 too narrow
S-002 | winner 3 | 60 | blocking_reason on every finding is more consistent

U-001 | incorporate yes | plan:103 vs source.md:72 and plan:29 is a real contradiction
U-002 | incorporate yes | T-05 needs expected values
U-003 | incorporate yes | source.md:34 requires it
U-004 | incorporate no | run_meta at plan:84 decouples; unverified
U-005 | incorporate yes | placement part only (run-record, report, decision-record paths); Journal reuse no
U-006 | incorporate yes | C-006 wording only; the C-015 range is harmless

## 7 SHARED ASSUMPTIONS
A-001 QUALIFY: the design wins unless the plan states a verified reason; plan:30 does (client.py:127-131), though the owner should be told.
A-002 QUALIFY: literal reading suits acceptance checks, but plan:125 constrains the implementer, so the imports point stays a Note.
A-003 REJECT: the reviewers did not apply it alike (V2 graded all Blocking); the rule excludes fixable checks and sentences.
A-004 ACCEPT: plan:21 makes jevlib read-only and the cited client.py, validate.py and budget.py lines support every claim.
