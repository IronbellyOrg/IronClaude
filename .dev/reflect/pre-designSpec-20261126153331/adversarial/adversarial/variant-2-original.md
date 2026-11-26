reviewer: qa
model_class: haiku
findings:
  - id: F-1
    grade: Blocking
    blocking_reason: Decision
    claim: "Task 6 requires exactly one post for missing-key and exhausted-budget stops, but the existing client stops both before transport. Its T-13 acceptance check cannot pass with the required client behaviour."
    evidence: "TASK-WF-designSpec-20261126-152817.md:165; jevlib/client.py:113-137"
    consequence: "Require zero posts for pre-transport stops; retain one post for HTTP 401 and returned-model mismatch, with no rerun."
  - id: F-2
    grade: Blocking
    blocking_reason: Missing
    claim: "Task 4 specifies refusal of existing manifest keys only for freeze-corpus, leaving freeze-table and freeze-rule without the write-once requirement or acceptance checks mandated by M-7."
    evidence: "TASK-WF-designSpec-20261126-152817.md:101-115; source.md:144"
    consequence: "Repeated freezes must refuse rather than replace frozen hashes; otherwise changed table answers could be re-frozen and escape changed-file invalidation."
  - id: F-3
    grade: Blocking
    blocking_reason: Decision
    claim: "Task 1 snapshots only existence, size and modification time of runs/ itself. Editing an existing nested run file need not change that directory's metadata, so the fixture can pass despite the real-run mutation M-13 requires it to detect."
    evidence: "TASK-WF-designSpec-20261126-152817.md:41-46; source.md:150"
    consequence: "The snapshot and its acceptance test must cover existing descendants, not just the directory entry."
  - id: F-4
    grade: Blocking
    blocking_reason: Missing
    claim: "M-5 requires a person to read the six definitions before freeze, but the plan covers only the automated cue scan and provides no human-review handoff step. The coverage matrix also drops this requirement-bearing sentence, representing M-5 only through its automated scan."
    evidence: "source.md:142; TASK-WF-designSpec-20261126-152817.md:39-47; coverage-matrix.yaml:470-480"
    consequence: "The freeze procedure must require the human reading; passing the cue scan alone does not complete M-5."
coverage_assessment: "The named test requirements have tasks, but M-5's human reading lacks a handoff step and M-7's write-once requirement is incomplete for two freeze commands. The matrix omits those requirement-bearing spans, so its apparent coverage does not establish complete adherence."
checked_and_found_clean:
  - "Exact Noul boundaries for all four operator pairs, empty statistics, and no-answered-run invalidation have explicit checks."
  - "Integer sign-test cases, twice-failed scoring, latency limits, ledger carry-over, deterministic reports and non-decisional rescoring are covered."
  - "Gate 1 accepting UNSET and Gate 2 refusing it match Revision 1."
  - "The T1 hash-check wording lead is not a defect: 'either gate' permits Gate 2 to check rule, table and code hashes."
  - "Read-only review; no tests or live calls were run."
recommendations:
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
    change: "Correct stop-specific post counts, require write-once behaviour for every freeze command, test nested-run mutation detection, and add the pre-freeze human reading."
    verifier: "Confirm each finding has an explicit task instruction and an observable acceptance check or handoff requirement."
