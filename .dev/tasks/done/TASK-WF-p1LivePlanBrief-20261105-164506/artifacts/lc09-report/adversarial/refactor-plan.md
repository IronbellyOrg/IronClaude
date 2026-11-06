# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (original, `option-a.md`: explicit `--unattended` flag), combined score 0.855
- Incorporating strengths from: Variant B (`option-b.md`) and from findings both advocates made against the base
- Planned changes: 6
- Risk level: Low to Medium (overall Medium only because Changes 1 and 3 rewrite the two bullets that carry the safety argument)
- Line references: A:N and B:N are lines of `variant-1-original.md` and `variant-2-original.md` in this directory. A's line map: citation key A:5; Safety A:7-10; Reliability A:12-15; day to day A:17-19; Implementation cost A:21-23.
- Wording rule for the merge: only claims already in a variant, in the advocates' verified spot-checks, or checked by the orchestrator (live spec line 401, spec item 13 at line 448) may be written into the merged output.

## Planned Changes
### Change 1: Limit the "misfire" claim to the environment variable and mark the observation unverified (from Variant B)
- **Source**: Variant B, Safety, B:13-14 (environment detection unsafe; preamble route "safer for people")
- **Target**: Base, Safety bullet A:9 (replace)
- **Rationale**: C-002 won by Variant B at 78%; Variant A's advocate conceded the A:9 headline "Detection would misfire" rests on an environment-variable observation only. Both advocates answered A-001 with QUALIFY: the 2026-11-02 observation cannot be checked from repository files, and `worker-list` omits remote workers unless `--include-remote` is passed (CAPS:127-128).
- **Integration point**: Keep A:9's evidence and its conclusion that the flag is immune. Rewrite the first sentence so it says environment-variable detection would misfire, report the observation as made in the 2026-11-02 session and not verifiable from the repository files, and add one sentence that the observation does not show a preamble-based route misfiring.
- **Risk**: Medium, because it edits the main safety bullet; wording must not weaken the claim that the flag cannot switch a person's run.

### Change 2: Say where the Orca worker signal belongs (from Variant B)
- **Source**: Variant B, Strongest case, B:8 (Orca defines a worker by the live preamble with Task and Dispatch IDs); debate point A-003 (hybrid)
- **Target**: Base, Reliability, new bullet after A:14 (insert)
- **Rationale**: U-005 (Medium value). Both advocates agree the preamble is Orca's own definition of a worker (CAPS:148); both reject "flag and detection are mutually exclusive" (A-003) and point to the hybrid in the current spec (line 401, checked) and `~/.claude/WORKER-CONTRACT.md` "Brief guard".
- **Integration point**: New bullet: Orca itself defines a worker by a live preamble (CAPS:148); that signal is used only in the worker session, as a refuse-only brief guard from P1, never inside a command; commands never detect Orca (current spec line 401).
- **Risk**: Low (additive).

### Change 3: Replace the "known weakness" bullet with the weakness plus its pre-run guard and residual risk (from Variant B)
- **Source**: Variant B, B:9 (the silent stall is the main argument for detection) and B:17; debate points C-003 and A-003
- **Target**: Base, day-to-day bullet A:19 (replace)
- **Rationale**: C-003 won by Variant B at 70%; Variant A's advocate conceded the catches in A:19 come only after the fact. The current spec adds a guard before the run: with a live preamble and every command copy carrying an `## Unattended mode` section, a line without the flag is refused (`WORKER-CONTRACT.md` Brief guard, case 1).
- **Integration point**: Keep the sentence that a forgotten flag makes the command prompt and the worker stall with no `worker_done`, which Orca reports as healthy (SPEC:47, CAPS:52). Replace "caught only after the fact" with: the brief guard now refuses such a brief before any work, the brief template and stall proof remain as later catches, and the residual risk is that the guard depends on the model recognizing the preamble and reading every command copy.
- **Risk**: Medium, because it rewrites a stated limitation; the residual-risk sentence must stay.

### Change 4: Move the "add detection later" path into the worker session (base weakness)
- **Source**: Variant B, B:18 (detection ties commands to Orca; non-goal 1, SA-2); concessions by both advocates
- **Target**: Base, Implementation cost bullet A:23 (replace)
- **Rationale**: Variant A's advocate conceded that A:23 ("detection can be added later as an extra trigger") conflicts with non-goal 1 (SPEC:314) and SA-2 (SPEC:170); Variant B's advocate conceded C-005 to Variant A on the same ground.
- **Integration point**: Keep "Changing later is cheap". Replace the extra-trigger clause with: any later detection belongs in the worker session as a refuse-only guard, as the brief guard is, never as a trigger inside commands.
- **Risk**: Low.

### Change 5: Record why no command-side headless signal exists for Orca workers (from Variant B)
- **Source**: Variant B, Reliability, B:19 (reflect's `claude --print` with no TTY)
- **Target**: Base, Reliability, new bullet after the Change 2 bullet (insert)
- **Rationale**: U-006 (Medium value). Verified by the orchestrator: the headless-signal text is in `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (section "Headless auto-accept under `--print` (FR-9)"). B:19 states "would not fire" as fact; the spec marks it assumed (item 9, v4 line 391), so the merged text must say assumed.
- **Integration point**: New bullet: the one existing command-side headless signal (reflect: `claude --print`, no TTY) does not apply because Orca launches Claude interactively with the task on the command line (CAPS:47); that this signal would not fire for an Orca worker is assumed, not verified (spec item 9).
- **Risk**: Low (additive; carries an UNVERIFIED flag).

### Change 6: State which spec version the citations point to (base weakness)
- **Source**: Findings of both advocates, checked by the orchestrator
- **Target**: Base, citation key A:5 (replace)
- **Rationale**: Every `SPEC:N` number in both variants matches `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md`, not the current spec; in the current spec those line numbers point to unrelated text. The current spec records the decision at line 401 as "Option (c): `--unattended` is the only switch; from P1 the worker session also applies the brief guard. Commands never detect Orca."
- **Integration point**: Rewrite the key: `SPEC:N` = line N of `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md` (the version before the decision); add that the current `orca-worker-contract-spec.md` records this decision at line 401. Leave `CAPS:N` unchanged.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)
| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| S-001 | Leading "Strongest case for it" section (B:7-10) | Unresolved presentation point (50%); Variant A's Position line (A:3) does the same job and the base already holds the evidence. |
| S-002 | Third citation key `[G] N` (B:5) | Unresolved (50%); the verbatim `[G]` quote could not be confirmed. Change 2 cites the same fact through CAPS:148, which is checked. |
| C-001 | Command detects it is an Orca worker (B:3) | Variant A won at 90%: the approved decision is the flag; commands never detect Orca. |
| C-004 | "Not mechanically testable" trigger (B:17) | Variant A won at 95%; Variant B's advocate conceded. |
| C-005 | Detection tied to Orca (B:18) | Variant A won at 95%; Variant B's advocate conceded. |
| C-006 | "Low per brief" cost claim and the AC-C1 grep exception (B:25) | Variant A won at 75%; both advocates call the AC-C1 grep claim overstated. |
| C-007 | Outward-defaults exposure only on the environment route (B:13) | Variant A won at 65%; the flag is a coordinator-written guard. |
| X-001 | "Preamble detection is safer for people" (B:14) | Unresolved (50%). Not merged as stated: Advocate A raised that a preamble persists in a terminal a person takes over, and quick depth had no rebuttal. Change 1 keeps only the narrower point both agree on. |
| X-002 | "Removes that whole failure class" (B:9) | Variant A won at 85%; Variant B's advocate conceded the contradiction. Change 3 takes B's stall insight without that claim. |
| A-001 | Treating the single observation as general | Unresolved (50%); handled by marking it unverified (Change 1). |
| A-002 | Model applies the trigger rule reliably | Variant A won at 58%; the residual risk is named in Change 3. |
| (U-007) | Preamble arrives on the same command line as the task (B:14) | Not merged: both advocates note CAPS:47 shows only that the task is passed on the command line, so this is an inference. |
| (B:10) | "Shorter briefs and no new flag on 35 commands" | Not merged: SPEC:189-195 lists which commands accept the flag and does not support shorter briefs; B:25 itself says each command needs detection text. |

## Risk Summary
| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | The safety bullet could read as weaker than the evidence supports | Restore A:9 from `variant-1-original.md` |
| 2 | Low | An extra bullet that overstates the guard | Remove the inserted Reliability bullet |
| 3 | Medium | The known weakness could be understated | Restore A:19 from `variant-1-original.md` |
| 4 | Low | Minor wording change | Restore A:23 |
| 5 | Low | Assumption presented as fact if the UNVERIFIED flag is lost | Remove the inserted bullet |
| 6 | Low | Wrong version named in the key | Restore A:5 |

## Review Status
- [x] Auto-approved (default; run is `--unattended`, which refuses `--interactive`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-05T19:44:33+00:00
