# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 92.9% (13 of 14 points)
- Convergence threshold: 80%
- Focus areas: safety of Phase 3 skills that call codegraph tools; reviewer burden; code paths to test; fit with the user's rule that a human merges
- Advocate count: 3 (Mode A, one advocate per input file, current model, default personas: Variant 1 architect-leaning, Variant 2 security/qa-leaning, Variant 3 analyzer-leaning)
- Agent failures: none
- Shared-assumption omissions: none (all three advocates answered A-001, A-002, A-003)

## Round 1: Advocate Statements

### Variant 1 Advocate (Option A, ready PR for majors)

**Position summary.** A is the minimal design (one path, full evidence every time), but its safety story is too thin for a major. On safety the advocate voted for a merged C, not A as written.

**Steelman of B.** A major is where tool arguments and outputs are most likely to change and the proof cannot see that; B makes the safe outcome the default because nothing mergeable exists until a person acts. B alone keeps 1.x patches flowing ("later minors of the old major still bump") and alone states idempotency.

**Steelman of C.** C reuses every verified step, so the reviewer gets "the full evidence ... without doing the bump by hand", and uses the only hard non-mergeable state ("a draft cannot be merged until a person marks it ready") for the cost of "one comparison".

**Strengths claimed.** (1) Fewest code paths: "no extra branch in the bump logic beyond the title word". (2) Full evidence for every bump. (3) Technically honours the human-merge rule.

**Weaknesses in others.** (1) B moves evidence away from the reviewer: "majors need a manual run". (2) B adds the most test surface: issue path, `--allow-major`, within-major selector. (3) C overloads draft state; labels are best-effort and do not exist yet. (4) C leaves release-notes delivery open. (5) C does not state idempotency.

**Concessions.** A major that keeps tool names "passes the proof and lands as a normal-looking ready PR"; one word is a soft signal and a merged pin reaches every Coder workspace. Inlining 76,281-character notes is probably unworkable. A never defines the candidate when a major is pending, so a declined 2.0 also blocks 1.x patches. A has no idempotency. "the proof plus the human merge is the review" is false by the verified facts.

**Shared assumptions.** A-001 QUALIFY (strict vX.Y.Z parse; skip and log prerelease and malformed tags). A-002 QUALIFY (semver likely, not guaranteed; minors can also break Phase 3 skills). A-003 ACCEPT (every run updates the existing branch/PR/issue).

### Variant 2 Advocate (Option B, issue only for majors)

**Position summary.** B is the safest for Phase 3 skills and the only variant that defines what happens to 1.x patches while a major waits, but it loses to C on evidence and reviewer effort. Honest recommendation: C's draft mechanics plus B's selection rule, idempotency and link-only notes.

**Steelman of A.** One code path is the cheapest to build and test; the human merge already gates everything; the reviewer gets full evidence every time.

**Steelman of C.** C attacks the real gap with full evidence plus a checklist that names the Phase 3 skills, and a draft is the only hard non-mergeable state. The reviewer never has to repeat the bump by hand.

**Strengths claimed.** (1) Strongest guard: "the monitor does not create a branch or PR". (2) Rationale names the real gap. (3) Only B defines the selection rule. (4) Only B states idempotency. (5) Link avoids inlining huge notes. (6) No draft overload.

**Weaknesses in others.** A: "the reviewer must notice the 'MAJOR' word" is not a control; inline notes may exceed the body limit. A and C: no candidate rule; no idempotency for major branch/PR. C: label best-effort and absent; a draft can be marked ready in one click.

**Concessions.** "majors need a manual run", so no proof evidence until a person runs it. More code than C (issue create/update needing issues:write, `--allow-major`, selector). The selection rule is hedged ("if the script picks ..."). An issue can sit unread just like a draft.

**Shared assumptions.** A-001 QUALIFY (skip and report prerelease and malformed tags, never bump on them). A-002 QUALIFY (semver discipline unverified; minors carry smaller but similar semantic risk). A-003 ACCEPT (idempotency on every path).

### Variant 3 Advocate (Option C, draft PR for majors)

**Position summary.** C is the best base: same integrity checks and proof, always a draft, so full evidence plus the only hard non-mergeable state. C should adopt B's within-major candidate rule and idempotency.

**Steelman of A.** Fewest paths and least to test; the human-merge rule already means nothing lands without a person.

**Steelman of B.** Most conservative, nothing to merge by accident; idempotent issue; keeps 1.x patches flowing; never overloads draft state.

**Strengths claimed.** (1) Hard stop without manual toil. (2) Full evidence up front. (3) Only variant that names Phase 3 skills in a checklist. (4) One comparison; the major path runs the same tested pipeline so it cannot rot. (5) Adds one deliberate human step at the moment it matters.

**Weaknesses in others.** A: a semantic 2.0 arrives as a normal ready PR; inline notes risk. B: proof evidence only after a manual run; the rarely used `--allow-major` path is the code most likely to break unnoticed; B has the most test surface.

**Concessions.** Draft has two meanings if the failed-proof decision also uses drafts; the label does not exist, so only the title disambiguates. The checklist enforces nothing. C-005 is a real gap that B fixes. No stated idempotency. Notes delivery unspecified.

**Shared assumptions.** A-001 QUALIFY (skip prereleases; malformed tag opens an issue). A-002 QUALIFY (major gate reduces, does not remove, risk; minor PRs also deserve the semantic-gap warning). A-003 ACCEPT (deterministic branch/title; update, never duplicate).

## Forced Rounds
- None. Taxonomy coverage after Round 1: L1 1 point (S-001), L2 4 points, L3 9 points. All levels covered.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|------------|-------|--------|--------|--------|--------|------------|------------------|
| S-001 | L1 | Tie | Tie | Tie | None (tie) | 95% | Identical five-bullet shape; nothing turns on it. |
| C-001 | L2 | 3 | 3 | 2+3 | Variant 3 | 85% | Draft PR keeps full evidence and stays non-mergeable; V3 advocate adds B's candidate rule. |
| C-002 | L3 | 3 | 2 | 2/3 tie | Unresolved | 50% | No PR (B) is a stronger barrier; draft (C) is the hard stop that keeps evidence attached. Real trade-off. |
| C-003 | L2 | 3 | 3 | 3 | Variant 3 | 95% | Unanimous: full evidence plus a Phase 3 checklist, no manual rerun. |
| C-004 | L2 | 1 | 1 | 1 | Variant 1 | 90% | Unanimous: one path; C a close second (one comparison); B adds three behaviours. |
| C-005 | L3 | 2 | 2 | 2 | Variant 2 | 100% | Unanimous and conceded by V1 and V3 advocates: newest release within the pinned major keeps 1.x flowing. |
| C-006 | L3 | 3 | 3 | 3 | Variant 3 | 95% | Unanimous: checklist names Phase 3 skills and draft forces a deliberate step. |
| C-007 | L3 | 2 | 2 | 2 | Variant 2 | 100% | Unanimous and conceded: link the notes; 76,281 chars is too large to inline. |
| X-001 | L3 | 3 | 2+3 | 3 | Variant 3 | 90% | Proof is necessary but not sufficient for a major; V1 advocate conceded A's claim is false. |
| X-002 | L2 | 3 | 3 | 3 | Variant 3 | 95% | Unanimous, V2 advocate conceded: automation prepares the bump, a human decides. |
| X-003 | L3 | 3 (qualified) | 2 | 2 | Variant 2 | 75% | B avoids overloading draft; V3 advocate conceded; all agree the title prefix must disambiguate. |
| A-001 | L3 | merge | merge | merge | None (all QUALIFY) | 90% | No variant defines tag parsing; merged rule must skip prerelease and malformed tags. |
| A-002 | L3 | none | none | none | None (all QUALIFY) | 90% | Semver discipline unverified for a single-maintainer project; the major gate reduces risk only. |
| A-003 | L3 | 2 | 2 | 2 | Variant 2 | 100% | Unanimous ACCEPT: only B states idempotency; every path needs it. |

Points won: Variant 3 = 5 (C-001, C-003, C-006, X-001, X-002); Variant 2 = 4 (C-005, C-007, X-003, A-003); Variant 1 = 1 (C-004). Agreed with no single-variant winner: S-001, A-001, A-002. Unresolved: C-002.

## Convergence Assessment
- Points resolved: 13 of 14
- Alignment: 92.9%
- Threshold: 80%
- Taxonomy gate: passed (L1, L2, L3 all covered)
- Invariant gate: not applied (Round 2.5 skipped at --depth quick)
- Status: CONVERGED
- Unresolved points: C-002 (barrier strength: no PR vs draft PR)
- Notable: all three advocates independently proposed the same merge (C's draft PR as the base, plus B's within-major candidate rule, idempotency and link-only notes).
