reviewer: refactorer (simplicity, ordering, reuse)
model_class: opus
findings:
  - id: F-1
    grade: Blocking
    blocking_reason: Decision
    claim: "Task 6 expects each stop signal to end the run with exactly one post. This cannot hold for KeyMissing or refused/budget_exhausted. The client raises KeyMissing and returns budget_exhausted before it calls the transport. After the whole-run reservation, a draw never runs short, so budget_exhausted cannot happen inside execute at all."
    evidence: "plan:165; plan:152; client.py:114-117; client.py:133-135; budget.py:72-78"
    consequence: "The check needs zero posts for KeyMissing. The budget_exhausted case needs a ledger the test changes during the run, or it is replaced by the spend_bound case."
  - id: F-2
    grade: Blocking
    blocking_reason: Decision
    claim: "This confirms T1 F-2 and raises its grade. Task 5 reads jev-rows.jsonl and run-record.md, but only Task 6 defines them. Task 5 does not depend on Task 6, and it is tested only on hand-built rows. No test passes runner output to the scorer, so every named check can pass while the scorer cannot read real rows."
    evidence: "plan:123; plan:125; plan:129; plan:138; plan:155-156; source.md:62; source.md:157"
    consequence: "Either the row and run-record format moves into Task 5, or Task 5 depends on Task 6. A test that scores rows written by execute is added."
  - id: F-3
    grade: Blocking
    blocking_reason: Decision
    claim: "Gate 2's spend_bound needs the whole-run estimate, which is built from the frozen prompts. The plan also says gate2 'hash files only and never call the corpus loader', and nothing records the estimate for gate2 to read. Gate 2 therefore has no stated input, which repeats M-1. It also pushes gate2 to build requests a second time, apart from execute."
    evidence: "plan:106; plan:108; plan:101; plan:152; source.md:132; source.md:155"
    consequence: "freeze-corpus already runs load_corpus. It should store spend.estimate_run_tokens in the manifest, gate2 should read that number, and execute should refuse if its own estimate differs."
  - id: F-4
    grade: Medium
    blocking_reason: null
    claim: "This confirms T1 F-3. A spend_bound stop writes run_end, and Gate 2's prior_run check then refuses forever, through an append-only log. The run command also never refuses an empty TYPESAFE_API_KEY before execute. A missing key would then write first_request and run_end and use up the experiment."
    evidence: "plan:106; plan:152-153; plan:156; plan:159; plan:166"
    consequence: "run refuses an absent key before any event is written, and the plan states whether a zero-post run_end uses up the go."
  - id: F-5
    grade: Note
    blocking_reason: null
    claim: "The plan says jevlib has '31 importers'. The files show 22 with an import statement and 26 .py files that mention jevlib."
    evidence: "plan:173"
    consequence: "The number is corrected or dropped."
  - id: F-6
    grade: Note
    blocking_reason: null
    claim: "sign_test_passes(b, c) has no rule parameter, yet the plan says it reads alpha_inverse from the rule. The check that it 'agrees with a reference loop' cannot fail if the loop is the same formula."
    evidence: "plan:79; plan:85"
    consequence: "The signature takes alpha_inverse, and the smallest-b table stays as the real check."
coverage_assessment: "All 14 test ids are covered. The 9 requirements the matrix left unmapped (INF-001/002/003/005/006/014/018/021/027) are covered in other words at plan:19-22, 80, 98, 102, 149 and 154. Every path in section 3 has a creating task, apart from the runtime outputs and parts B and C."
checked_and_found_clean:
  - "The six cue rows and the ambiguity rule are at SKILL.md:153-159, and the M-5 cue list matches."
  - "MAX_RETRIES=1 and ATTEMPT_TIMEOUT_S=20.0 (config.py:15,17) are read at call time through C (client.py:192,158)."
  - "The estimate formula matches client.py:100."
  - "__init__ exports only MODEL, API_URL and KEY_ENV."
  - "Result.latency_ms includes local work (client.py:87). The transport wrapper is required by the spec (source.md:82)."
  - "Sign-test smallest b values 5, 7, 9, 10, 12, 13, 15 and 8-2 = 56/1024 are correct (arithmetic checked by hand)."
  - "Task order 1 -> 2 -> {3, 4} -> 6 -> 7 -> 8 is sound apart from F-2."
  - "No second client is built."
recommendations:
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
    change: "Change Task 6's signal criterion to zero posts for KeyMissing, and replace the budget_exhausted case with the spend_bound case or a ledger the test changes mid-run."
    verifier: "Compare the criterion with client.py:114-135."
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
    change: "Make Task 5 depend on Task 6, or move the row schema into Task 5, and add a test that scores rows written by execute."
    verifier: "A Task 5 acceptance criterion names rows from execute with MockTransport."
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
    change: "Have freeze-corpus write the whole-run token estimate into the manifest, have gate2's spend_bound read it, and have execute refuse a mismatch."
    verifier: "The gate2 description names its spend input, and the load_corpus-patched test still passes."
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
    change: "Make run refuse an empty TYPESAFE_API_KEY before any event is written."
    verifier: "A test with no key shows no new lines in events.jsonl."
