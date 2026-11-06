# Round 1: Advocate for Variant 2 (analyzer)

## Position summary

Variant 2 is the safer base. Its pattern `.dev/<command>/<subject>-<n>/` is the contract's own worked example generalized (WORKER-CONTRACT section 4, `.dev/tdd/auth-1/` then `auth-2/`). It also states the one real exception (WC-3 re-run) and labels what it could not confirm. It has two real gaps: it ignores tool-owned folders under `.dev/` (X-001), and its counter recovery is internally inconsistent (A-003).

## Steelman of Variant 1

Variant 1 has the strongest answer to "how do I stop two runs colliding and keep one run's reports together". The `<runStamp>-<runSlug>` folder separates runs with no counter recovery. It reuses a convention the repo already has (`.dev/README.md:47`: UTC stamp plus 16-character camelCase subject). Its `.dev/orca/` root cannot clash with any tool that writes under `.dev/`. FR-009 gives an audit line per name, and its decisions table answers the four seed questions in one place. It is also candid that the root is new (R4). Its design avoids the X-001 problem and Variant 2's does not.

## Strengths of Variant 2

- **Contract fidelity.** The contract fixes the shape of its example (`.dev/tdd/auth-1/`, retry `auth-2/`). Variant 2 adds no new root and no new state. Variant 1's extra layer needs a stamp and a slug that the contract never asks for.
- **Root-cause framing (U-004).** Collisions are caught only after the fact, by a command refusing an existing `return-contract.yaml` (WC-4). So the coordinator must be the sole source of names. That justifies FR-001 and FR-007.
- **FR-013 and X-002.** WC-3 says the re-invocation uses "the same report directory" and "the second run's contract replaces the blocked one whole". Variant 1's FR-004 reads as an absolute "never written again" and misses this case.
- **FR-012.** A guard refusal consumes an attempt, and the section 4 limit is 2 fixes (3 attempts). Variant 1 never says so.
- **FR-004.** Siblings differ in subject, not in attempt. This keeps "which sibling" and "which attempt" apart, which matters for the fan-in rule.
- **FR-016 and risk 3.** It flags undecided merge-back of child report folders, and the ambiguity of subjects ending in digits.

## Weaknesses of Variant 1

- Its date and run layer is the only thing that avoids a counter, yet it still needs a per-subject attempt counter (FR-004) and a unique run slug (R2). It adds state and does not remove any.
- It creates a root nobody asked for. R4 admits that whether any tooling scans `.dev/` by folder name is UNVERIFIED.
- FR-010 says the relative part is the same in every worktree, and names stay unique only because subjects are unique within the run. Two children share the same relative path by design; this works only if the subject rule holds.
- Its contract-adjacent claims are thin: no WC-3 exception, no guard-refusal accounting.

## Concessions

- **X-001 holds in part.** I read `.dev/README.md` lines 40 to 65. Line 63 says plans generated before the current layout (`.dev/workflow/<slug>/`) and "their path-hashed ledgers under `.dev/implement/`" keep working unchanged. So both folders exist, but only as legacy, not migrated. Current packages keep `progress.md` inside `.dev/tasks/to-do/TASK-WF-<id>/` (lines 51 to 54). The claim that `.dev/implement/` is "the home of implement ledgers" overstates it; the legacy label is the accurate reading. The clash is still real: `.dev/implement/<subject>-1/` would sit among hash-named ledger folders, and `.dev/workflow/<slug>-1/` could be mistaken for a legacy plan slug. I did not verify the `reflect.md:101` part of the claim.
- Variant 2 does not mention this. A reserved-name rule is needed.
- FR-011 ("path exactly once") is not quite right. The contract's own example passes the path twice for tdd (`--output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`). The circuit-breaker comparison must handle that.
- Variant 2 has no audit line per name (Variant 1's FR-009 is better).
- Variant 2's camelCase departure from `.dev/README.md:47` is unexplained.

## Shared assumptions

- **A-001: QUALIFY.** The placement map and counter are the right sole mechanism, but they live only in run notes. The brief of every Task carries its report directory, so a replacement coordinator can rebuild the counter from the Task specs. Whether Orca lets it list them is UNVERIFIED.
- **A-002: QUALIFY.** `README.md:63` confirms overlap only for legacy `.dev/implement/` and `.dev/workflow/`. Add a rule: for those two commands, and for `reflect` and `brainstorm(s)` if confirmed, never put report folders directly in the tool's own folder.
- **A-003: REJECT.** A guard-refused attempt writes no contract and may leave no directory (WC section 1, "Brief guard"). Listing directories undercounts. Variant 2's own FR-012 contradicts its FR-005 and risk 2.

## Per-point verdicts

S-001 | winner: V2 | confidence 55% | Starting from the root cause (collision caught late by WC-4) tells the reader why the coordinator owns names.
S-002 | winner: V1 | confidence 65% | A decisions table answers each seed question in one place, easier to audit than a paragraph.
S-003 | winner: V2 | confidence 55% | Topic sections (Retries, Nested, Child worktrees) let a reader find a rule faster than a flat list.
C-001 | winner: V2 | confidence 62% | It matches the contract's worked example and adds no root; the clash risk in X-001 needs a reserved-name patch.
C-002 | winner: V2 | confidence 58% | Time is in git history; a run stamp is a second piece of state and the contract never asks for it.
C-003 | winner: V2 | confidence 68% | FR-002 requires global uniqueness and FR-016 names the merge-back gap that V1 skips.
C-004 | winner: V2 | confidence 72% | FR-004 states the subject-versus-attempt rule that V1 only shows in examples.
C-005 | winner: MERGE | confidence 55% | V1's "only the attempt changes" is accurate; V2's single-token rule fails on the contract's two-path tdd example.
C-006 | winner: V1 | confidence 60% | camelCase 16 matches `.dev/README.md:47` and avoids V2's own digit-ambiguity risk 3.
C-007 | winner: V1 | confidence 60% | V1 makes the `-1` suffix a requirement (FR-011) where V2 leaves it as a risk.
C-008 | winner: V2 | confidence 82% | WC-3 explicitly reuses "the same report directory" on re-invocation; V1 omits it.
X-001 | winner: MERGE | confidence 60% | README:63 shows a real but legacy-only overlap; keep per-command roots and add a reserved-name rule.
X-002 | winner: V2 | confidence 85% | FR-013 is the correct reading of WC-3, which V1's absolute rule contradicts.
A-001 | winner: MERGE | confidence 60% | Keep the placement map and add recovery from Task specs and an audit line (V1 FR-009).
A-002 | winner: MERGE | confidence 62% | The risk is real but narrow; a reserved-name rule fixes it without a new root.
A-003 | winner: V1 | confidence 75% | V1 R1 correctly notes that guard-refused attempts leave no directory, which breaks V2's listing recovery.
