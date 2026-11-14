# Q15: must v2 ever deliver a course correction to a session that is not an Orca worker

## Question (verbatim from the spec row)

merged-requirements.md section 3, row Q15: "Must v2 ever deliver a correction to a non-worker session?"

ADJ Part 7 wording (alignment-findings-adjudicated.md:785): "Must v2 ever deliver a course correction to a session that is not a worker, or does it report to a person or the coordinator only?"

## Spec's recommended answer

"Report only (advisory)" (merged-requirements.md:542). ADJ: "Report only (advisory); no delivery to non-worker sessions" (alignment-findings-adjudicated.md:785). Origin: V4 Q4 and D-8 (variant-4-original.md:172; round2-rebuttal-V4.md:68).

## Default if unanswered

"PLAN INFERENCE: report only" (merged-requirements.md:542).

## What it gates

- V2-01: the rewrite of issue #423 (Orchestrator v2, the planned advisory knowledge layer, not built) (merged-requirements.md:398).
- V2-03: the v2 brainstorm and research, whose design must state for each session class how a course correction is delivered (merged-requirements.md:400; ADJ acceptance criterion at line 714).
- V2-04: the deferred v2 first release (merged-requirements.md:401).
- Wave W3.

## Facts the question depends on

1. Session classes: Orca workers (started by a coordinator through Orca), watcher-launched sessions (started by the issue watcher), person-started sessions, and sessions without a Run (ADJ line 714). #409 decision 9: "A session the watcher launches is an ordinary session to the sweep" (variant-4-original.md:74).
2. Workers receive coordinator follow-ups only by pulling them: "WC-12. Coordinator follow-ups are pulled, not pushed. The worker runs the preamble's `check` at natural checkpoints" (src/superclaude/core/WORKER-CONTRACT.md:61, re-read 2026-11-14).
3. A worker never starts other workers or agents (WC-13, WORKER-CONTRACT.md:62); "the contract has no worker-to-worker channel" (ADJ line 715).
4. "Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged" (WORKER-CONTRACT.md:288, re-read).
5. #423's current acceptance criteria ask v2 to "relay them to affected agents" (round2-rebuttal-V4.md:68, D-8). ADJ's proposed #423 text: "The first release delivers to the person or the coordinator only" and, per session class, "a coordinator follow-up (WC-12) for workers, a report to the person for the rest" (ADJ lines 705, 714; line 705 corrected from 707 after an advocate's re-read, confirmed by grep 2026-11-14).
6. The sweep "recommends nothing"; v2's course correction is a recommendation, so v2 is a separate command or skill (round2-rebuttal-V4.md:118; ADJ line 294).
7. #339 comment 2 proposes a trust layer for messages between sessions: same permission mode, fixed message types, signed narrow grants (.dev/issues/339/issue-summary.md, "What the issue asks for"); comment 2 also says "encryption alone is not enough" (ADJ line 295). The trust layer is #339 Phase 4, unbuilt (SW-12, merged-requirements.md:201).
8. ADJ Part 2.6: if the brainstorm decides v2 relays to agents and not only to the person, the #339 trust decisions become prerequisites for v2 (ADJ line 699). This links Q15 to Q14 (the v2 start gate) and Q16 (one grant vocabulary and audit format).
9. Relayed knowledge rules already proposed for v2: fixed typed fields, free text only in `detail`, never acted on; relay passes through the coordinator; LLM-derived entries marked inferred (ADJ lines 705, 715).
10. No channel exists today that delivers a message into a person-started or watcher-launched session; this was not searched beyond the contract text above (UNVERIFIED whether Orca has a terminal-input verb that could be used).
