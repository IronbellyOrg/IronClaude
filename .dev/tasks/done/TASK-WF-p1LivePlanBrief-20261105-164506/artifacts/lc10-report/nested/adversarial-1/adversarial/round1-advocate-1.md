# Round 1, advocate for Variant 1 (scribe)

## Position summary

Variant 1's dedicated root `.dev/orca/<runStamp>-<runSlug>/` keeps coordinator reports out of folders that other tools already own, and it groups one run so that a reader can audit it. X-001 confirms this risk for Variant 2's per-command root. Variant 2 is better on the state rules: the WC-3 exception, guard refusals and fan-out subjects. The best result keeps V1's root and audit trail and adds V2's state rules.

## Steelman of Variant 2

V2 generalizes the contract's own worked example (`.dev/tdd/auth-1/` then `auth-2/`, WORKER-CONTRACT section 4), so it adds no new convention and gives the shortest path. Its root-cause framing (U-004) is the clearest reason in either draft: the command's refusal catches a collision only after the fact, so the coordinator must be the sole source of names. It covers state rules that V1 misses:
- FR-013 is the WC-3 re-invocation. The contract says a re-invocation "keeps every token of the brief's `Command:` line" (WORKER-CONTRACT lines 22 and 98), so the report directory is in fact reused inside one Task.
- FR-012 counts guard refusals as attempts, at most 3 (contract line 126).
- FR-004 says that siblings differ in subject, not in attempt number.
- FR-016 states honestly that merge-back of child report folders is undecided.

## Strengths of Variant 1

- **Root isolation (C-001, X-001).** One new root never shares a parent folder with tool-owned paths. I verified this in `.dev/README.md`. Line 63 names `.dev/workflow/<slug>/` (legacy plans) and `.dev/implement/` (path-hashed ledgers) as preserved, and `src/superclaude/commands/reflect.md:101` defaults `--output` to `.dev/reflect/<mode>-<slug>-<ts>/`. Under V2, report folders for `workflow`, `implement` and `reflect` would land next to, or inside, those trees.
- **A run is a unit.** The run folder with a coordinator-chosen stamp (U-001) separates runs without any counter recovery. It also partly hedges A-003: a new run gets a fresh namespace even if notes from an old run are lost.
- **Audit trail (FR-009, U-002).** Each name has one run-notes line (directory, Task ID, command line, worktree, `replaces`), with a concrete example. V2 says only "recorded" (FR-008).
- **Decisions table (S-002, U-003).** Each open question in the seed brief maps to one decision and its reason, which helps a reviewer check the choices.
- **Risks named honestly.** R1 is the only place in either draft that notices a guard-refused attempt leaves no contract (contract line 126: "No contract ... nothing ran"). That fact is what breaks A-003.

## Weaknesses of Variant 2

- `.dev/<command>/` collides with tool-owned folders (X-001), and V2 never mentions this, even though A-002 is high impact.
- Its counter recovery ("list the directories", risk 2) assumes every attempt leaves a directory or contract. A guard refusal runs nothing, so listing can undercount.
- With no date and no run folder, every run of a long-lived feature worktree shares one counter space. That makes subject collisions across runs more likely (its own risk 4).

## Concessions

- V1's FR-004 ("never written again") is wrong as an absolute rule: WC-3 rewrites the same directory inside one Task (X-002). V2 is right here.
- V1 omits the guard-refusal attempt cap (U-006), the sibling-versus-attempt rule (U-005, C-004) and the merge-back question (U-008).
- V1's FR-010 claims merge-back "does not collide". That holds only if `<subject>` is unique across the whole run, which V1 never states for child worktrees. V2's FR-002 states it.
- `.dev/orca/` is new and longer, and it moves away from the contract's own example (R4, R5).
- Neither variant settles the trailing-digit ambiguity (V2 risk 3), and camelCase in V1 does not remove it either.

## Shared assumptions

- **A-001: QUALIFY.** The placement map is the right primary mechanism (contract section 4), but it is not enough on its own. A free-path check before dispatch (V1 FR-006, V2 FR-005) is required, and the counter must persist in written run notes, not in memory.
- **A-002: REJECT** for V2's root, and **QUALIFY** for V1's. The assumption is false for `.dev/<command>/` (README:63, reflect.md:101). For `.dev/orca/` it is plausible but UNVERIFIED until a grep shows that no tool writes there.
- **A-003: REJECT.** A guard-refused attempt writes no contract and may create no directory (contract line 126), so a listing undercounts attempts. Recovery must come from run notes, and the run-stamp namespace limits the damage.

## Per-point verdicts

S-001 | winner: MERGE | confidence 60% | V2's root-cause opening explains why the coordinator owns names; V1's sources list helps auditing.
S-002 | winner: V1 | confidence 70% | A table that ties each open question to its decision and reason is easier to review than one paragraph.
S-003 | winner: V2 | confidence 65% | Topic groups (Retries, Nested, Child worktrees) make 16 requirements easier to navigate than a flat list.
C-001 | winner: MERGE | confidence 70% | Keep V1's dedicated root and run folder (X-001) with V2's `<command>-<subject>-<n>` leaf, which both drafts already share.
C-002 | winner: V1 | confidence 65% | One coordinator-chosen stamp per run separates runs, and the time is known before dispatch, which satisfies WC-4.
C-003 | winner: V2 | confidence 80% | FR-002 makes run-wide uniqueness explicit across worktrees; V1 FR-010 assumes it.
C-004 | winner: V2 | confidence 80% | FR-004 states the sibling rule; V1 shows it only in examples.
C-005 | winner: MERGE | confidence 70% | Only the attempt changes (V1 FR-005), and the path is one token (V2 FR-011): both together make WC-6's comparison mechanical.
C-006 | winner: V2 | confidence 55% | Lowercase kebab avoids case-sensitivity problems on some filesystems, and V2 flags trailing digits; V1 matches the workflow package's camelCase rule (README:47).
C-007 | winner: V1 | confidence 65% | V1 makes the `-1` suffix a requirement (FR-011) rather than leaving it as a risk.
C-008 | winner: V2 | confidence 85% | Contract lines 22 and 98 confirm that a WC-3 re-invocation keeps the same `Command:` line and so the same directory.
X-001 | winner: V1 | confidence 80% | Verified: README:63 names `.dev/workflow/<slug>/` and `.dev/implement/`, and reflect.md:101 uses `.dev/reflect/`, so the claim holds.
X-002 | winner: V2 | confidence 85% | V1 FR-004 has to be narrowed to "never written by a different Task".
A-001 | winner: MERGE | confidence 70% | Both drafts check before dispatch; add persistent run notes (V1 FR-009) as the store for the counter.
A-002 | winner: V1 | confidence 75% | Only V1 flags that the root choice is UNVERIFIED (R4), and its separate root avoids the verified clash.
A-003 | winner: V1 | confidence 70% | V1 R1 correctly notes that guard-refused attempts leave no trace, which breaks V2's recovery by listing directories.
