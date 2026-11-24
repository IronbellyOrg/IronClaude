# Hypothesis: CLI completion omits the configured done-marker publication
**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-11-23T19:22:11Z
**Cause class**: Other: missing completion-policy wiring; regression history unestablished.
**Claim class**: `mixed`
**Evidence class**: `runtime_repro`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned: OnCompletion defines default-on publication; descriptive docs record the limitation the issue requests repairing.
runs-in=src/superclaude/cli/swarm/commands.py:2145-2169 @ current worktree .venv/bin/superclaude, stub transport, dedicated artifacts/home

## Claim
The foreground and resume completion bodies discard the returned result contract, persist terminal state, and exit without calling the done-marker writer. This leaves the configured completion policy unapplied. Parent-captured successful foreground and resume CLI runs independently demonstrate the omission; detached and unsuccessful completion remain source-only or unobserved.

## Evidence
- `source_citation`: src/superclaude/cli/swarm/commands.py:2145-2178,2578-2599: bare `reduce_wave3(...)` calls precede `_write_swarm_state(...)` and `raise click.exceptions.Exit(EXIT_OK)`; neither continuation calls `emit_done_sentinel`.
- `source_citation`: src/superclaude/cli/swarm/models.py:563-573: "on terminal status" and `write_done_sentinel: bool = True`; commands.py:931-937 explicitly enables the flag for fresh lens shortcuts; reduce.py:701-704 emits the contract then returns it without marker publication.
- `executed_reproducer`: tier1-observation.md:10-23 records local-foreground-1 real CLI/stub exit0 and command provenance; artifacts/foreground.stdout.txt:1 contains `swarm run: dispatched job (mode=lens, workers=3, results=3)`; artifacts/foreground-check.json:1 contains `{"done_exists": false, "state": "terminal"}`; artifacts/foreground/return-contract.yaml:2 is success.
- `executed_reproducer`: tier1-observation.md:25-37 records local-resume-1 exit0 and command provenance; artifacts/resume.stdout.txt:1 contains `workers=3 skipped=3 redispatched=0`; artifacts/resume-check.json:1 contains `{"done_exists": false, "state": "terminal"}`; artifacts/resume/return-contract.yaml:2 is success. artifacts/import-paths.txt:1-2 records commands.py and reduce.py imported from this exact worktree.

## Proposed Fix
Retain the result contract in both completion continuations, persist terminal state, then use the existing writer to publish beside the persisted contract with its actual status, only when the effective JobSpec enables runtime.on_completion.write_done_sentinel. Do not publish without a persisted contract, duplicate contract emission, change stdout, or signal completion from the detached launching parent.
- src/superclaude/cli/swarm/commands.py: connect both continuations to reduce.py:383-440, preserving its atomic writer.
- tests/swarm/test_commands_run.py: new fresh/resumed CLI regressions, disabled-policy and partial/failed verdict cases; verify marker status/path and contract -> terminal -> marker ordering.
- docs/swarm/README.md:116-120: replace affected limitation guidance.
Acceptance requires new assertions failing before repair and passing afterward, plus isolated CLI captures of parseable matching markers. Detached acceptance additionally needs a supported confined tmux run proving child-owned publication. None is claimed executed.

## Confidence
Self-reported confidence: 0.90 (integration cause, not production readiness).
- Evidence grounding: 1.0: source boundaries, policy, writer, tests read.
- Runtime check: 1.0: real foreground/resume captured by parent, not generated fixture results.
- Symptom coverage: 1.0: explains both successful terminal runs missing the marker.
- Reproducibility fit: 1.0: two separate local stub outputs reproduce omission.
- Fix directness: 1.0: omitted operation is connected at owning completion boundaries.
- Domain coherence: 1.0: single completion-policy domain and intended ordering.

## Risks
Early publication falsely signals completion; assumed success mislabels partial/failed outcomes; ignored flag violates opt-out. Paths without reduction must not reference a nonexistent contract. Resume policy recovery is incomplete, so honor effective policy without promising arbitrary original override recovery. Fresh output roots prevent stale-marker false positives. Preserve kill semantics and unrelated staged work.

## If I'm wrong, it's probably because...
Another completion publisher outside the inspected continuations executes and then fails or its marker is removed.

## Falsification standard
An unmodified default-on failing CLI trace showing emit_done_sentinel actually called from the completion continuation despite a subsequently absent marker refutes this omitted-call explanation for that run.

## Evidence classification
Claim class mixed: source omission, observed runtime symptom, documented contract. Evidence class runtime_repro supplemented by source_static/doc_static. Runtime check performed by parent for successful foreground and all-successful-workers resume only; worker executed nothing. REFUTE coverage not applicable (AFFIRM). Producer-citation check skipped: header-only trace menu, no enum exclusions/passing-control claim. No unobserved library/OS behavior asserted: project function bodies and measured filesystem absence are the evidence.

## Alternatives considered
Writer/library failure not selected because completion boundaries omit the call; external failures are not excluded.

## Grounding gaps
Diagnosability partial: diagnosability-context.md; no required diagnostic measurement remains. Detached, redispatch, unsuccessful completion, disabled-policy acceptance, repaired ordering remain unverified. Existing25 passing tests are not new marker-regression acceptance. No Augment retrieval supplied to this worker. Proposal remains inert.
