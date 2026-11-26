review: 2 of 3

# Review 2 of 3 (re-review after the surgical repair): revised Jev versus keyword table build plan (issue 611)

Scope: changed lines plus the prior blocking findings (M-1, M-2, M-3 of `REPORT.md`). Candidate: `.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/TASK-WF-designSpec-20261126-162725.md` (sha256 86c2e1e2dbb34d409dbcc2d2a9a8f97b3f470a15d557f2d6e1fe1868205cbd6a). Baseline: the archived `TASK-WF-designSpec-20261126-152817` plan (sha256 cac5150528c4f8a7f3911dda2f543df6a8068c597a11f4f5cb4123a806c35b28). Reviewer: `reflect-reviewer` on opus, read-only. The coordinator ran `diff -w` (`/tmp/sc611-plan2.diff`) and supplied it; the reviewer could not run commands and did not check the sha256 values.

**Result:** all three prior blocking findings are resolved. No new blocking finding. Two Medium follow-up candidates. The two additions made on the owner's instruction (M-11, M-12) have no blocking defect.

## Prior blocking findings

- **M-1: resolved.** The new criterion (candidate line 166) matches what the unchanged client can do: `KeyMissing` is raised before any post (client.py:133-137, zero posts); HTTP 401 raises `KeyRejected` after one post (client.py:188-190); a wrong model id returns `invalid`/`model_mismatch` after one post (validate.py:32-33; client.py:168-174); the `spend_bound` refusal comes before `first_request` (candidate lines 153-154, zero posts); `refused`/`budget_exhausted` cannot occur naturally under the whole-run reservation (budget.py:72-78), so the criterion injects it through a stand-in.
- **M-2: resolved.** The human reading of the six definitions (source.md:142) is carried in three places: the `table-procedure.md` step (candidate line 184), the README order of work immediately before `gate.py freeze-corpus` (candidate line 202), and a Task 8 criterion that checks both (candidate line 213). The recording command matches the `events.py owner-input` interface (candidate line 99). Nothing else reads `owner_input_received` events, so the extra event breaks nothing.
- **M-3: resolved.** `freeze-table` and `freeze-rule` now refuse when their keys already exist (candidate lines 104-105), and the tests cover a second `freeze-table` and a second `freeze-rule` (candidate line 116). Together with `freeze-corpus` this meets source.md:144.

## The two owner-instructed additions

- **M-11 (candidate lines 202, 215): no defect.** `keyscan.py` reads only `JEV_API_KEY` and prints SKIP when it is unset (keyscan.py:80-83), so the mapping is what makes a real scan possible. The example uses a single-quoted `bash -c '...'`, so the outer shell does not expand `$TYPESAFE_API_KEY` and only the variable name reaches the command line. The `export` happens inside the one subshell, as J2 requires (SHARED-CONTRACT.md:147-149).
- **M-12 (candidate lines 32, 217): one wording slip, F1 below.** The approach is sound, and the `--help` test detects an import failure.

## Follow-up candidates (non-blocking, both Medium)

- **F1:** candidate line 32 says each command-line module "inserts the existing `jevlib` folder" into `sys.path`. Elsewhere the plan uses "the existing `jevlib` folder" for `p15/jev/jevlib`. Read literally, putting that folder on the path makes `from jevlib.client import ...` fail, because the package's parent folder `p15/jev` must be on the path (probe.py:16-17; candidate line 42). The `--help` test at candidate line 217 would catch the wrong reading. Fix: say "the folder that contains `jevlib` (`.dev/research/346-review-loop-experiments/p15/jev`)".
- **F2:** the reading event records the hash of `questions.py` at the time of reading, and `freeze-corpus` freezes its own `questions` hash; nothing compares the two, so wording edited after the reading could be frozen unread. Not blocking: following the text (read, record, freeze) does not produce this. Fix: have `freeze-corpus` refuse unless the latest reading event's evidence hash equals the current hash of `questions.py`, or have the README say to read again after any edit.

Covered: every line of the diff and the inherited text each change depends on (candidate lines 22, 42, 60, 99, 102-107, 130, 153-160, 167), `jevlib/client.py`, `budget.py`, `validate.py:32-33`, `transport.py:50-102`, `keyscan.py`, `probe.py:1-60`, `p15/jev/tests/conftest.py`, `SHARED-CONTRACT.md:140-169`, all of `source.md` and the whole prior report. Not checked: the sha256 values. Not re-raised, as instructed: the prior report's Medium and Note findings (M-4 to M-21).

Final verdict: PASS

## Findings block

```findings-v1
{"id": "F1", "severity": "MINOR", "blocking": false, "category": "contradiction", "anchor": "inserts the existing `jevlib` folder and the experiment folder into `sys.path` itself", "refs": ["M-12"], "claim": "Read literally, putting the jevlib folder itself on sys.path makes `from jevlib.client import ...` fail when the CLIs run as scripts; the parent folder p15/jev is the one that must be inserted, as probe.py and the conftest line do."}
{"id": "F2", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "the person reads the six definitions in `questions.py` once and records that with `events.py owner-input --evidence <questions.py path>", "refs": ["M-2"], "claim": "Nothing compares the reading event's hash of questions.py with the hash freeze-corpus freezes, so wording edited after the reading can be frozen unread and unnoticed."}
{"prior": "M-1", "status": "resolved"}
{"prior": "M-2", "status": "resolved"}
{"prior": "M-3", "status": "resolved"}
```
