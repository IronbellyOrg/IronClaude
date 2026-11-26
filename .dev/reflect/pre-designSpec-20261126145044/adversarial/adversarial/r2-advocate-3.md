# Round 2, advocate 3 (variant 3, refactorer)

## 1 Answers to criticisms of variant 3

- C-007 (F-3), "plan:103 already gives a writer" (A1, A2). Conceded. `gate.py` "writes and checks `manifest.json`" (plan:103) and plan:107 tests mismatch refusal. What remains are fixable sentences: no `gate.py` subcommand for plan:156 to name, no command for `freeze` or `rule_freeze` (the CLI at plan:101 has only `record-tests` and `record-go`), and one evidence hash in `tests_passed` against "hashes" in Gate 2.
- C-012 (F-6), "run_meta decouples; synthetic tests" (A1, A2). Partly conceded. The pure `verdict` can be tested on synthetic inputs (plan:88). But the `score` command "reads the experiment folder" (plan:84) and must turn gate events into the "missing gate result" reason, and Task 5 defines those events ("Each gate writes its result as an event", plan:103). The command depends on Task 5; the function does not.
- C-013 (F-7). Conceded to Note. Task 5 depends on Task 2 (plan:97), which supplies `sha256_file` (plan:57). Journal reuse was withdrawn in Round 1 (journal.py:18,29).
- "F-5 and F-8 Blocking for fixable checks" (A1, Round 1). F-5 was conceded in Round 1. F-8 was already Medium (variant-3-original.md:48).
- C-003. I withdraw my Round 1 reason. A fake key set in the process after the gates is not an environment read (plan:119; client.py:133), so A2 is right that the gates can still come first. I hold Medium because no gate, task or acceptance check rests on the CLI dry run: plan:121-127 test responses through `live=True` and `MockTransport`, as plan:30 says. Also, `live=False` returns before the key is read (client.py:128-133).
- C-002. Conceded to Medium: plan:125 already requires all three stops. A2's point shapes the fix. A rerun after `model_mismatch` is a real paid call (client.py:173 settles usage), so the repaired sentence must say "stop, no rerun". `draw` still holds the cap (budget.py:77), so this is not Safety.

## 2 Changed positions

C-002 | Medium | 68 | plan:125 fixes the outcome; only the detection and precedence wording at plan:119 is wrong
C-007 | Medium | 62 | plan:103 supplies the writer; names and hash count are fixable sentences
C-008 | Blocking-Decision | 58 | correcting it changes plan:107's acceptance check, or whether the table step (plan:137) waits on open items Noul operators and failure count (source.md:120-121); the owner must choose
C-012 | Medium | 55 | narrowed to the `score` command reading Task 5's events
C-013 | Note | 65 | plan:57,97 make the loader's hashing available
S-001 | MERGE | 75 | V3 misses C-008 and C-014; V2 adds the Task 6 behaviour focus
A-004 | QUALIFY | 75 | "unchanged" is mandated (plan:21); claims rest on current behaviour, not on proven correctness

## 3 FINAL positions

C-002 | Medium | 68 | see section 2
C-003 | Medium | 62 | design departure (source.md:82); nothing rests on the CLI dry run; plan:30 covers the mock path in tests
C-007 | Medium | 62 | see section 2
C-008 | Blocking-Decision | 58 | plan:103,107 add an UNSET check absent from source.md:72
C-009 | Medium | 65 | source.md:42 lists `run-record.md` but the design gives it no job; placement of report and decision record is fixable (source.md:44; plan:84,151)
C-012 | Medium | 55 | see section 2
C-013 | Note | 65 | see section 2
S-001 | MERGE | 75 | see section 2
S-002 | winner 3 | 70 | `blocking_reason` on every finding makes grades checkable; small effect
A-004 | QUALIFY | 75 | see section 2

## 4 Other Round 1 majorities

I accept C-001 as Blocking-Missing (with `release_phase` at run end, budget.py:98-100), C-004 and C-015 as Note, C-005, C-006, C-010, C-011 and C-014 as Medium, and C-016 as not a defect. I dispute none of them.
