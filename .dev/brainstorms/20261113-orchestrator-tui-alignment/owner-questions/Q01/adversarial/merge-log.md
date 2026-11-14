# Merge Log: Q1

## Metadata

- Base: Variant 2 (proposal-B), file `variant-2-original.md`
- Plan: `refactor-plan.md` (5 planned changes, overall risk Low, auto-approved 2026-11-14)
- Context read: `debate-transcript.md`, `../question.md`, `variant-1-original.md`, `variant-3-original.md`
- Output: `../merged-proposal.md`
- Merge date: 2026-11-14
- Hard constraint carried: no change specifies the code fix. The answer itself (fix before merge, F1 or F2 chosen by the #539 author and the owner, all channels in scope) is unchanged.

## Changes Applied

### Change 1: state the premise the ruling relies on

- Status: Applied
- Target: "What happens next if the owner picks it", step 1
- Before: step 1 said the owner posts the ruling, authorises the allow-list edit for this purpose only, and lists the channels in scope. No premise was stated.
- After: step 1 first states the premise, as SW-01 (2) requires (`merged-requirements.md:190`): the worst-case lens of `SECURITY.md:168-170`. It names the counterweight (every launched session already runs with permission checks off, ADJ E-11) and says the ruling does not rely on it. The original allow-list and channel wording follows unchanged.
- Provenance tag: `Base (original, modified), Variant 3 merged per Change #1`
- Validation: premise wording matches the plan rationale; no code design added; the other three steps unchanged.

### Change 2: phrase the scope by outcome, list as a minimum

- Status: Applied
- Target: "Answer", part (b)
- Before: part (b) listed the channels covered and said the ruling names any channel it leaves out.
- After: one sentence appended: the ruling states its scope by outcome (no program named by config or by the environment runs during the sweep's `git status`, or the worktree is reported `unscanned`) and treats the listed channels as the measured minimum, not a complete list (`merged-requirements.md:36`).
- Provenance tag: `Base (original, modified), debate consensus on A-001 merged per Change #2`
- Validation: outcome covers both F1 and F2 so neither fix route is preferred; part (a) untouched; no mechanism named.

### Change 3: say what the fix does and does not remove

- Status: Applied
- Target: "What stays unresolved"
- Before: two bullets (which fix outcome and the code; other git versions).
- After: a third bullet: the fix removes the sweep's added exposure, the widest automatic one (fan-out across every listed worktree on every coordinator wake, `HOW-WE-WORK.md:406`); it does not cover other sessions that run `git status` themselves (example from debate A-003: the Claude Code harness's session-start git status), and whether they honour the same config is UNVERIFIED.
- Provenance tag: `Base (original, modified), Variant 1 merged per Change #3`
- Validation: UNVERIFIED marker kept as in the plan and transcript; no new fact added.

### Change 4: keep the fix reviewable on its own

- Status: Applied
- Target: "What it costs or risks", first bullet
- Before: the bullet ended "This lengthens the #539 lane and everything queued behind its merge."
- After: appended: the fix goes in as its own push with its own description, because #539 is a 1003-file PR.
- Provenance tag: `Base (original, modified), Variant 1 merged per Change #4`
- Validation: process only; no code design, flag or implementation step.

### Change 5: record the XC-04 reading conflict

- Status: Applied
- Target: "What it unlocks", second bullet
- Before: the bullet said XC-04 can run on master code as soon as the sweep is runnable, because the master sweep is the fixed sweep.
- After: qualifier appended: the advantage over an acceptance is certain only under the strict reading (`merged-requirements.md:452` and `:889`); `merged-requirements.md:630` (TB-GIT) would also let a recorded acceptance satisfy the git trust boundary; the conflict is recorded and not resolved.
- Provenance tag: `Base (original, modified), CONTRADICTION-1 from the debate transcript merged per Change #5`
- Validation: consistent with the transcript (the fixed sweep can run XC-04 under either reading; only the advantage over the other variants depends on the reading).

## Post-Merge Validation

- Structural integrity: pass. One H1 title (unchanged from the base), five H2 sections in the base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. Provenance header comments at the top; one source comment before each section. Step numbering 1 to 4 unchanged.
- Internal references: pass. Every id and path cited (SW-01, SW-02, SW-05, NFR-014, INV-009, INV-011, INV-039, ADJ E-11, XC-04, TB-GIT, `merged-requirements.md:36`, `:190`, `:452`, `:630`, `:889`, `SECURITY.md:168-170`, `HOW-WE-WORK.md:406`) comes from the base, the plan, the debate transcript or `question.md`. No new id, path or line number was invented.
- New contradictions: none found. The answer (fix before merge, F1 or F2 picked by the #539 author and the owner, all channels in scope) is unchanged. The premise added in step 1 does not rely on ADJ E-11, so it does not conflict with the risk section. The outcome phrasing in part (b) agrees with the "names any channel it leaves out" clause and with the second risk bullet. CONTRADICTION-2 (`.process` measurement) is outside the plan and was not merged. No em or en dashes; no code fix specified.

## Summary

- Planned: 5
- Applied: 5
- Failed: 0
- Skipped: 0
