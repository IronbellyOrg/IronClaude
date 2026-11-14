# Adversarial Debate Transcript (Q28)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 91% (10 of 11 points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned in parallel (general-purpose, session default model): V1 architect, V2 security, V3 qa
- Variants: V1 = proposal-A (nothing before the ruling, then level 3, `--merge-guard off`), V2 = proposal-B (nothing before, then level 2 with hand pushes), V3 = proposal-C (never)

## Round 1: Advocate Statements

Full statements: `round1-advocate-V1.md`, `round1-advocate-V2.md`, `round1-advocate-V3.md`. Summaries:

### Variant 1 Advocate (architect)
Level 3 after the ruling brings the tool's mechanical push checks (head binding, parent check, named-path staging, operator-pending refusal, `SKILL.md:299`, `:306`, `:308`) and verification to the riskiest PR. Concedes: the owner-ruling stop is judgment only; the gate must be "resolved", not "replied"; drop the pre-ruling level 1 option; `--merge-guard off` may skip the PR-open check. Pick: V1 amended (stop rule and PR-open check in the grant row).

### Variant 2 Advocate (security)
Level 2 makes every outward effect pass a person by state machine (`SKILL.md:307`). Found that level 2 can still post one PR comment: the Augment-decline fallback runs `/sc:auggie-review` with `--post-pr` on by default (`refs/auggie-fallback.md:35`; `SKILL.md:310`), so the grant row must list it or hold on a decline. Concedes level 2 still designs fixes locally. Pick: V2 amended.

### Variant 3 Advocate (qa)
Only "never" meets "no tool designs or pushes an INV-008 fix" (`merged-requirements.md:191`) and "stops the run before any fix" (`:194`) by construction; SW-02 changes the very git-status code INV-008 is about and the tool re-triggers Codex after each push, so a new git-configuration finding is likely. Concedes heavy hand work, no verification pass, and no exit clause. Pick: V3 now, revisit once the Codex thread is resolved and Codex has gone quiet.

### Orchestrator verification (2026-11-14, read-only)
- `refs/detection-contract.md:132-136`: resolved Codex threads are excluded; unresolved stay visible. Confirmed: a reply without a resolve leaves the INV-008 thread selectable.
- `refs/merge-guard.md:94-97` says the PR-OPEN pre-push read applies "whatever the guard phase is, including `disabled`"; `SKILL.md:309` loads that ref at Wave 6 only for "L3 with `--merge-guard draft` only". Confirmed: the two texts disagree; under `off` a session following SKILL.md may skip the OPEN read.
- `refs/auggie-fallback.md:35`: `--post-pr` defaults on and `--no-post-pr` "must NOT be passed". Confirmed.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie | 95% | identical structure |
| C-001 | L2 | V1 | V2 | V3 | unresolved | 50% | each advocate kept its own level after the ruling |
| C-002 | L2 | V2 | V2 (=V3) | V2 (=V3) | V2 (V3 equal) | 92% | nothing before the ruling; level 1 would diagnose the INV-008 thread |
| C-003 | L2 | V1 | V2 | V1 | V1 | 68% | tool pushes carry head and parent checks |
| C-004 | L2 | V2 | V2 | V2 | V2 | 90% | no toggle question and no `off` ambiguity |
| X-001 | L3 | V2 | V2 | V3 | V2 | 70% | level 2 stops outward effects by state machine |
| X-002 | L2 | V1 | V1 | V1 | V1 | 90% | only V1 uses the standard loop |
| X-003 | L3 | V1 | V1 (=V3) | V1 (=V3) | V1 | 85% | one session in the checkout |
| X-004 | L3 | V2 | V2 (=V3) | V3 (=V2) | V2 (V3 equal) | 90% | no level 1 before the ruling |
| A-002 | L3 | V2 | V3 | V3 | V3 | 70% | only V3 does not rely on "no new git-configuration finding"; all three REJECT A-002 |
| A-003 | L3 | V1 | V1 | V1 | V1 | 85% | tool pre-push checks beat hand pushes |

Points won: V1 4 (C-003, X-002, X-003, A-003), V2 4 (C-002, C-004, X-001, X-004), V3 1 (A-002); C-001 unresolved; S-001 tie.
Shared assumptions: A-001 all QUALIFY (gate on "resolved", not "replied"); A-002 all REJECT; A-003 V1 ACCEPT as a risk, V2 and V3 QUALIFY (add the owner-memory checks); A-004 all ACCEPT.

## Convergence Assessment
- Points resolved: 10 of 11
- Alignment: 91%
- Threshold: 80%
- Taxonomy coverage: L1 1, L2 5, L3 5 (all covered)
- Invariant probe gate: not applied (depth quick)
- Status: CONVERGED on points; the central point C-001 (which level after the ruling) is unresolved and each advocate's overall pick was its own variant, so the headline is split.
- Unresolved points: C-001
- Unanimous corrections every variant needs: no tool before the ruling (drop level 1); gate on the Codex thread being resolved, not only replied to; a PR-open and head check before every push, by the tool or by hand.
