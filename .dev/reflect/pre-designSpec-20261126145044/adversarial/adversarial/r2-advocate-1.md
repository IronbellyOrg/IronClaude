# Round 2, advocate 1 (variant 1, analyzer)

## 1 Answers to the Round 1 criticisms of variant 1

- Under-graded C-001. Conceded. I re-read plan:119 and plan:124. Both give only a per-request guard. source.md:82 asks for a whole-run estimate before the first request, and `Budget.reserve_phase` (budget.py:63-70) exists for it. It is absent, so Missing. It is not Safety: `draw` still enforces the cap (budget.py:77).
- Over-graded C-005 and C-006 as Decision. Conceded. They are fixable checks (plan:47, plan:159).
- Bundled the imports point into F-3. Conceded. It is wording that fails loudly.
- Under-graded C-002 (V2 and V3 say Blocking-Decision). Countered. Variant 1 did find the defect. client.py:114-117 returns `refused/budget_exhausted`. client.py:135 and :190 raise `KeyMissing` and `KeyRejected`. So plan:119 is right for two of its four stop signals and wrong for the other two. But plan:125 already requires that a 401, a wrong model id and a spent ledger each stop the run. source.md:82 already says to rerun on a status other than ok. The stop behaviour is therefore stated, and the plan's sentence on rerun precedence needs repair. That is a fixable sentence. Reruns of refusals cost nothing, since the budget draw is settled at 0 (client.py:129 and :189).
- Under-graded C-007 (V3 says Blocking-Missing). Partly conceded, and my grade moved the other way. plan:103 says `gate.py` "writes and checks" the manifest, so a writer exists in substance. What is missing is a command name, a README line that lists commands which do not exist (plan:156), and a clear count of hashes in `tests_passed`. Those are fixable sentences.

## 2 Changed positions

C-007 | Medium | 55 | plan:103 gives a writer; the gaps are command names and the hash count, which are fixable sentences (was Blocking-Missing, 52)

## 3 FINAL positions

C-002 | Medium | 55 | stop behaviour already required at plan:125; the rerun-precedence sentence is fixable; Blocking-Decision is a minority I dispute
C-003 | Medium | 68 | plan:30 gives a reason supported by client.py:127-131; only plan:119 contradicts itself; no acceptance check rests on it
C-007 | Medium | 55 | see section 2
C-008 | Blocking-Decision | 52 | plan:103 and plan:107 add a Gate 1 acceptance check absent from source.md:72; it blocks table answers (plan:137) on fields the table never uses; the owner must choose
C-009 | Medium | 65 | run-record.md has a layout row but no described behaviour (source.md:42); report.md placement is a fixable choice
C-012 | Not-a-defect | 65 | plan:84 takes `run_meta`, and plan:88 tests with synthetic inputs
C-013 | Note | 55 | plan:57 offers `sha256_file`; plan:101 and plan:103 do not forbid it; reusing Journal is optional
S-001 | MERGE | 65 | variant 1 for calibration, variant 2 for the Task 6 behaviour, variant 3 for the structural gaps
S-002 | winner 3 | 55 | its `blocking_reason` field makes each grade checkable; the effect is small
A-004 | ACCEPT | 80 | plan:21 keeps jevlib read-only; client.py:114-117, :127-131 and :188-190 match every claim

## 4 Other Round 1 majorities

I accept C-001 as Blocking-Missing, C-004 and C-015 as Note, C-005, C-006, C-010, C-011 and C-014 as Medium, and C-016 as not a defect. I dispute only C-002 (Blocking-Decision), because the plan already requires the stops. I also dispute any majority that grades C-008 as Medium: it changes a Gate 1 acceptance check, and I hold it at Blocking-Decision with low confidence.
