# Q16 final: one trust design, or one shared vocabulary and one audit record?

Q16 is the owner question about what the program promises on trust (who may do what, and how it is checked) across three planned programs: the observer dashboard (issue #409), Orchestrator v2 (issue #423) and the workspace listener (issue Coder#477 in the IronbellyOrg/Coder repository).

## Debate result

Winner: proposal C (promise one shared vocabulary of permission names and one shared audit record shape, and let each program keep its own checking mechanism). Confidence 70 percent. The three advocates agreed 3 of 3: each one, including the advocates for A and B, judged C best overall (65, 70 and 65 percent). Convergence 100 percent on the 11 scored points (10 unanimous, one by 2 of 3).

Evidence that decided it:
- The spec's own scope section lists "One trust design" as out of scope and says "only one grant vocabulary and audit format is in reach (Q16)" (merged-requirements.md line 146). The advocate for B conceded this.
- The three programs sit behind different trust boundaries the spec already records: the observer is read-only on one host; the v2 first release reads only what the same OS user on the same host can read (line 401); the listener crosses workspaces and carries a nine-item security checklist (line 355). One shared mechanism would be over-built for one or too weak for another (ADJ lines 295 and 809).
- Signing does not stop poisoned content (#339 comment 2: "encryption alone is not enough", ADJ line 295). C sends that problem to an existing separate rule: relayed text stays typed data (V2-04, line 401).
- Only the vocabulary answer is written out in the spec's decision item (XC-08, the step that records Q16 and edits three issue texts, line 456).

Proposal A (promise nothing yet; this is the spec's default). Strength: adds no new public trust wording before any trust layer exists (lines 129, 201). Weaknesses: it is not neutral, because it leaves "Decide one design, not two." standing in #409, so the issues would disagree with each other; and its trigger for asking again is circular, because the trust-layer work (SW-12 Phase 4) is itself blocked by the Q16 decision step (lines 201 and 830). Its one unique strength, asking again when a real design exists, was adopted into the merged answer.

Proposal B (one trust design for all three programs). Strengths: one mechanism to build and review, one owner, and a written bar on any second format (review 03's Edit 7, quoted in the review diff analysis line 89). Weaknesses: outside the spec's stated scope (line 146), against the debate's lean (X-005, 66 percent, ADJ line 382), commits three issues to a design that does not exist, and risks a false sense of safety for relayed text. Its single-owner rule was adopted into the merged answer.

Proposal C (one vocabulary and one audit record). Strengths above. Weaknesses its own advocate named: three mechanisms to review; the same word can mean weaker protection in one program than another; a shared audit format is a shared target for injected text; the original debate confidence is only 66 percent and the point was judged "not decidable from sources" (review diff analysis line 89). The merge added mitigations for the second and third.

Merged answer: OUT/Q16/merged-proposal.md (C plus four additions: a single owner and no second vocabulary; the owner re-confirms the promise when the trust layer is opened; each term must state what it enforces in each program; audit records are treated as untrusted input).

Citation note: the advocates found off-row line numbers in question.md, proposal-A and proposal-C (for example the #409 correction pass row is line 256, not 257). They were corrected on 2026-11-14; no fact changed.

## Final recommendation

Promise one shared vocabulary of permission names and one shared audit record format, not one trust design. Each program keeps the checking mechanism its own risks need. Change #409 decision 6 to "Decide one grant vocabulary and one audit record." and have #423 and Coder#477 promise the vocabulary, not a design. Add the merged safeguards: one owner for the vocabulary, the owner re-confirms it when the trust layer is designed, and each term states what it really enforces in each program.

Confidence: 70 percent.

Single strongest reason: the spec itself puts one trust design out of scope and the three programs have different trust boundaries, so one design would either over-build the read-only observer or under-protect the cross-workspace listener.

Equals the spec's recommended answer: yes for the core choice. The merged additions (single owner, re-confirm checkpoint, per-program meaning of each term, audit records as untrusted input) go beyond the spec's row but do not change the answer.

## What would change the answer

If the owner decides that v2 will relay knowledge between agents across workspaces soon (so all three programs must verify each other's grants directly), proposal B's single design would gain weight, because a translation layer between three mechanisms would then be needed. If the owner closes Coder#477 (Q3, the listener question), the consumer set shrinks and the difference between B and C matters less.

## Criticality rating

- Security or trust boundary: high
- Reversibility: easy
- Who is affected: other people or repos
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The question sets the trust promise for three programs, one of them in a different repository (IronbellyOrg/Coder), and the debate found it "not decidable from sources", so it rests partly on the owner's plans for v2 relay. The debate converged and the text is reversible by issue history, but a high trust-boundary question that changes public issue text in another repo is the owner's to make.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q16/adversarial/ (diff-analysis.md, round1-advocate-1.md to round1-advocate-3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml)
- fallback_mode: false (three advocate sub-agents and a merge-executor sub-agent were spawned; the diff analysis, scoring and refactor plan were done by this worker session in the orchestrator role)
