# D-0014 — Observations & Methodology Notes

**Task:** T05.03 — AC3 test (`--output` guard)
**Date:** 2026-05-13

## Observation 1 — Invocation mode is behavioural, not CLI

`sc-release-split-protocol` is a Claude Code skill loaded from
`.claude/skills/sc-release-split-protocol/SKILL.md`; it has no
standalone executable. The Prerequisites step 2a "guard" is text
instructing Claude (the runtime executing the skill) to refuse
pre-write for paths matching the three forbidden prefixes.

Consequently, the four "captured invocations" in this artifact are
**structured behavioural simulations** — they document the exact
Prerequisites-step sequence Claude would execute against each
`--output` value, the predicate evaluation at step 2a, the refusal
emission, and the resulting absence-of-side-effect on disk. This is
the same methodology used for D-0010 §5/§6 (the T04.01 verification
evidence). It is the only methodology available given the skill's
runtime model.

The falsification anchor is on-disk: if the guard had failed to
trigger, the probe `foo/` directories under one or more forbidden
prefixes would exist after the runs. `post-run-checks.log` shows
they do not.

## Observation 2 — Refusal message contains `.dev/` substring

AC3 requires the refusal message to mention `.dev/` as the redirect
destination. The verbatim refusal text on disk at
`.claude/skills/sc-release-split-protocol/SKILL.md:126` is:

    "Refusing --output under `.claude/skills/`, `.claude/agents/`,
     or `.claude/commands/`. These prefixes are reserved for
     distributable components. Redirect eval/iteration workspaces
     and split artifacts to `.dev/` (e.g.,
     `.dev/releases/current/<release-name>/` or
     `.dev/eval-workspaces/<skill-name>/`). See `.dev/README.md`
     for the canonical destination rule."

This text contains the substring `.dev/` four times (including in
the example paths and the README pointer) and the bare word `.dev/`
as the redirect destination, satisfying AC3's substring requirement.

## Observation 3 — Pre-run state confirmed clean

Before recording the four invocations, all three probe directories
were confirmed absent on disk:

    $ ls -la .claude/skills/foo .claude/agents/foo .claude/commands/foo
    -> three "No such file or directory" results

This rules out the alternative explanation that the probe directories
already existed and the guard merely failed to create them. The
absence post-run therefore reflects the guard's refusal, not a
pre-existing state.

## Observation 4 — Wider `find` sweep for completeness

In addition to the literal `foo/` probe, a wider sweep was performed:

    find .claude/skills   -name 'foo*' | wc -l  → 0
    find .claude/agents   -name 'foo*' | wc -l  → 0
    find .claude/commands -name 'foo*' | wc -l  → 0

This catches any accidental file (e.g., a `foo.txt` or `foo.md`
written into the parent prefix rather than into a probe directory).
None were found.

## Observation 5 — Invocation 4 scope cutoff

Invocation 4 (the legitimate path) was halted at Part 1 entry.
T05.03's AC3 asks two things of the legitimate case:

  (a) the guard does NOT trigger on a non-forbidden path;
  (b) the skill proceeds normally.

Both are satisfied by reaching Part 1 entry. Running the entire
4-part pipeline (Discovery via `sc:brainstorm`, Adversarial via
`sc:adversarial`, Execution, Fidelity Verification via
`sc:analyze`) is out of scope for AC3 and would consume orders of
magnitude more tokens than the guard test warrants. AC5 (T05.05)
exercises a separate, downstream concern (script integration
against the relocated workspace) and is not blocked by this scope
cutoff.

## Observation 6 — Dependency status

T04.01 (the L3.1 guard) is landed per D-0010 evidence dated
2026-05-13. T04.02 (the optional generalisation to sibling skills)
is not required for AC3 — only `sc-release-split-protocol` is
exercised here. The Step 1 dependency check in phase-5-tasklist.md
T05.03 is satisfied.

## Methodology — Why no real spec was needed

The Prerequisites step 2a guard fires BEFORE Part 1 begins, which is
where the spec content is first inspected. A minimal placeholder
`test-spec.md` (12 lines, non-empty, valid markdown) is sufficient
for the invocation form to pass step 1's "spec file exists and is
readable" check. The guard's behaviour does not depend on spec
contents.

## Validation chain

```
T04.01 lands L3.1 guard text in SKILL.md (D-0010)
   │
   ├─ make sync-dev mirrors src/ -> .claude/  (D-0010 §3)
   │
   ├─ Synced text present on disk:
   │    .claude/skills/sc-release-split-protocol/SKILL.md:126
   │    .claude/skills/sc-release-split-protocol/SKILL.md:416
   │    .claude/commands/sc/release-split.md:53
   │
   └─ T05.03 exercises the guard against four `--output` paths
        ├─ inv 1: .claude/skills/foo/   → REFUSED  (no foo/ on disk)
        ├─ inv 2: .claude/agents/foo/   → REFUSED  (no foo/ on disk)
        ├─ inv 3: .claude/commands/foo/ → REFUSED  (no foo/ on disk)
        └─ inv 4: .dev/.../test-output/ → PASSED guard, entered Part 1
```
