# Reviewer verdict for attempt 3 (A3), verbatim

**Verdict: extra.** The guides' claims check out against live source, but there is one extra-scope hunk (D3) and a few small wording defects (D1, D2, D4).

Per AC
- T1.AC1: met, apart from the sentence in D1. Directory order, the two paths, the signature keys, digit and 100-character normalization, first-match, inclusive 0.7, no ranking/status, the MindBase stub and the export claims all match live source. Cited: docs/user-guide/memory-system.md:27-31,66-69,71-77,20; docs/memory/README.md:19,21. The README's description of the sample file (D1) contradicts the live file.
- T1.AC2: met. No automatic secret removal is promised, and both outputs are covered. Cited: memory-system.md:131-137; README.md:140-144. No recipe writes to production data; cp .bak and tar backups are the only writes.
- T1.AC3: met. Example 1: 9 shared of 10 distinct, 0.90, match. Example 2: 6 shared of 12 distinct, 0.50, no match. Cited: memory-system.md:79-89.
- T1.AC4: met. The claim-matrix line citations are accurate and the table renders. Cited: t1-claim-matrix.md:3-23; reflexion.py:68-74,76-82,127-136,153-170,198-244. The protected-hash check printed no non-OK lines.

extra_scope: D3 below. misunderstood: none.

Defects
- D1 (wrong statement): docs/memory/README.md:35 says reflexion.jsonl.example has "Synthetic sample rows showing the fields the recorder and lookup use". The live file still has the old ts/task/mistake/evidence/rule/fix rows. None have error_type, error_message or test_name, so the lookup can never match them. Fix: reword to "Synthetic sample rows in an older task/mistake/rule/fix layout; the lookup cannot match them (they have no error_type, error_message or test_name)". Task 2 can then replace the sentence.
- D2 (misleading recipe): README.md:175-181 says "To find invalid lines" with `jq -c .`. That only finds lines the lookup skips. The lines that actually raise (non-object JSON, non-string signature fields) pass `jq -c .`. Fix: add a read-only finder after it, for example `jq -c 'select(type != "object")' docs/memory/solutions_learned.jsonl`, plus a finder for non-string error_type/error_message/test_name (select(type=="object" and ((has("error_type") and (.error_type|type)!="string") or (has("error_message") and (.error_message|type)!="string") or (has("test_name") and (.test_name|type)!="string")))). Alternatively, add a sentence saying the jq check does not catch those rows.
- D3 (extra scope, low): README.md:8-9 rewords Overview bullets 2 and 3 (Workflow Metrics and Pattern Learning), which the plan reserves for Task 4. The original text was "Performance tracking and optimization" and "Successful implementation patterns". Fix: restore those two bullet descriptions verbatim. Keep the numbered list and the new bullet 1.
- D4 (ambiguous, low): memory-system.md:9 says "Nothing in the framework calls them for you, except the pytest recorder". The recorder calls only record_error(), never get_solution() (pytest_plugin.py:185-196). Fix: "Nothing in the framework calls get_solution(). The only automatic record_error() call is the opt-in pytest recorder described below."

Self-Audit: read reflexion.py in full, pytest_plugin.py:55-204, tests/conftest.py:1-125, the __init__ exports, pm-agent.md; grepped src for callers; confirmed the Python snippet is isolated (reflexion.py:76-82); confirmed failure modes (non-object line breaks get_statistics via record.get at reflexion.py:343; can break get_solution at reflexion.py:155-168; non-string signature field breaks only get_solution at reflexion.py:164,170); conftest sentence correct; all referenced paths exist; solutions_learned.jsonl is tracked with 4 pattern-style rows; git diff outside .dev shows only the two guides. Did not execute the snippet.
