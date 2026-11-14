# Round 1 advocate statement: Variant 2 (keep the default `worktree` level as a deliberate chain)

Persona: architect (structure, dependencies, long-term impact). Depth quick, Round 1 only.

## Position summary

Variant 2 is the only option that names the claim command's own ship gates as hard FU-1 preconditions, and one of those gates (OB-H1 item 5) binds a claim at any level, including `--pipeline none`. On the core choice, however, the architecture favours claim-only: the built default is a confirmed accident against design decision D2, and keeping it doubles the permission-free surface. My honest recommendation is Variant 3 with Variant 2's gate precondition folded in.

## Steelman

### Variant 1 (claim-only, acceptance declined, FU-1 waits)

Strongest version: TB-PERM says every launched session on this host runs with permission checks off (`merged-requirements.md:631`), and TB-UNTRUSTED says issue text is untrusted input (`:632`). A session that reads untrusted text with no permission checks is a risk that a written sentence does not reduce; it only moves the blame. Variant 1 fixes the design contradiction in code and refuses the one risk it cannot bound. It is the only variant that does not rest on shared assumption A-002, and its U-001 (find out whether a permission-on session can finish unattended through `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS`) addresses the root cause instead of accepting it.

Critique: it trades a bounded, one-issue, reversible test for an open-ended hold. Its own risk section admits a permission-on session "may stop at a permission prompt with nobody to answer it" (`variant-1-original.md:23`), so its reopen condition may never be met. Every downstream item (WA-05, SW-10, SW-13, WA-07) stays blocked, and the open facts only FU-1 can settle (operation-id path, agent row, whether `agent launch` creates a Run; ADJ line 271 action 2 (d) to (f)) stay open. The spec already scopes the consent to the test issue and says it authorises no future issue (`merged-requirements.md:572`), which is the control Variant 1 wants for later issues.

### Variant 3 (claim-only, acceptance given for the one test issue)

Strongest version: it is exactly what the spec and ADJ recommend (`merged-requirements.md:529`; ADJ line 271 action 1: "Recommended `--pipeline none` ... exactly design decision D2"). It makes the code obey the recorded design (`docs/designs/issue-watcher.md:44`: "The claim stops at `next-steps.md`"), removes the second permission-free session, costs one small PR with no file shared with #539, and lets FU-1 produce the facts every later design needs. Its scoping sentence "for the test issue only" (U-004) is the correct shape for a risk acceptance.

Critique: its Unlocks section says "FU-1 can run" (`variant-3-original.md:17`) while its risk section concedes the "claim at any level" gate (OB-H1 item 5) may still hold it (`:24`). It treats that gate as a risk footnote rather than a precondition. It also omits that FU-1 sits behind `GRANT(WA-04,live-test)`, ORCA-AVAILABLE and Q20 (`merged-requirements.md:719`, `:811`). These are fixable gaps, not flaws in its choice.

## Strengths claimed

1. **The ship gates are made explicit FU-1 preconditions (U-003).** `refs/claim.md:131`: "no governed claim (`--pipeline worktree` or `full`) is used on a real issue until OB-H1 item 1 ..., OB-H2 and OB-H3 have passed", and the same line says the hook design "requires ... OB-H1 item 5 (self-started turns wrapped) before a claim at any level". Variant 2 is the only variant that lists item 5 as a precondition. ADJ action 1 lists only item 1, OB-H2 and OB-H3 for the default branch (ADJ line 271), so Variant 2 is also more complete than the ADJ there. Because item 5 applies at any level, this precondition is needed whichever variant the owner picks.
2. **No watcher code change now.** `launch.py:33` (`PROMPT_PATTERN = ^/sc:issue --claim [1-9][0-9]{0,8}$`) stays as built and tested. One fewer PR, one fewer review cycle.
3. **The watcher defers to the claim command's own default.** `issue.md:43` sets `worktree` as the default `--pipeline`. If the claim command's governance (launch-level guard, `W-ENFORCEMENT-ABSENT` refusal, plan-approval stop; `issue.md:16`) is trusted, the watcher does not need its own policy on how far a claim goes. This keeps one source of policy.
4. **FU-1 would test the chain the owner may eventually want (U-002).** A live second-agent launch gives later handoff design (SW-13, WA-07) real data about a second session. This is data for a design, not a handoff; no watcher-to-orchestrator handoff exists.
5. **The design amendment is named (U-005).** Variant 2 does not leave D2 contradicted silently; it says D2 must be amended so the design and the code agree.

## Weaknesses identified in other variants

1. **Variant 3 over-claims FU-1 readiness (X-001).** "FU-1 can run" (`variant-3-original.md:17`) conflicts with `refs/claim.md:131` (item 5 before a claim at any level) and with `merged-requirements.md:719` (WA-04 also needs `GRANT(WA-04,live-test)` and ORCA-AVAILABLE). The probe found Orca not reachable on 2026-11-13 (`merged-requirements.md:604`; the spec does not claim that outage is still current).
2. **Variant 3 treats a gate as a risk.** Its risk line (`:24`) is correct in fact but wrong in kind: a gate that "may still hold" FU-1 belongs in the preconditions, as Variant 2 lists it.
3. **Variant 1 has no reachable exit.** Its reopen condition depends on a permission-on unattended session being feasible, which it marks UNVERIFIED and possibly impossible (`variant-1-original.md:12`, `:23`). An indefinite hold on a built and reviewed feature is a structural cost: the code ages while its untested assumptions (the operation-id path, a guess pinned by fixtures, ADJ line 271 (f)) stay unchecked.
4. **Variants 1 and 3 do not name the grant row.** Both say what happens next without `GRANT(WA-04,live-test)` (`merged-requirements.md:331`, `:719`). Variant 2 shares this omission (see A-001).

## Concessions

1. **Variant 2 doubles the permission-free surface.** Two sessions per approved issue run with permission checks off, the second in a worktree with a launched agent, both downstream of untrusted issue text (`variant-2-original.md:22`; TB-PERM, TB-UNTRUSTED). Variant 3 has one. For a first live test, a smaller blast radius is the better architecture.
2. **Keeping the default ratifies an accident.** ADJ X-001 (line 372, 91 percent) records the default as a confirmed contradiction caused by an omission, not a design choice. D2 is a recorded decision ("D2 claim-only", `issue-watcher.md:40`). Amending the design to fit the accidental code inverts the normal direction: the code should conform to the decision. My strength 2 (no code change) is real but small; the ADJ sizes the fix as "one small PR" (ADJ line 271).
3. **Per-claim worktrees and agents with no owner.** Every approval creates a worktree and an agent, up to 6 sessions a day, none owned by a coordinator (`merged-requirements.md:313`; Q20 covers only the watcher worktree, `:547`). That is unbounded long-term operational load.
4. **Variant 2's gate list is the wrong list for claim-only.** Items 1, OB-H2 and OB-H3 apply to governed claims only; under `--pipeline none`, only item 5 binds. Variant 2's contribution is correct for its own branch and partly transferable, not wholesale.
5. **Strength 4 (data for the handoff design) is speculative.** The handoff is unbuilt and deferred (WA-07, SW-13); collecting data for it is not a reason to run a second permission-free agent now.
6. **Variant 2 is gated on facts nobody has checked.** Whether OB-H1 items 1 and 5, OB-H2 and OB-H3 have passed is UNVERIFIED; if they have not, Variant 2 runs nothing at all.

## Shared assumption responses

- **A-001 (FU-1's outward writes need nothing beyond the Q2 answer): REJECT.** The spec requires a separate grant: "The first rollout is therefore a bounded test under `GRANT(WA-04,live-test)` with the owner's consent" (`merged-requirements.md:331`), and the dependency row for WA-04 lists `GRANT(WA-04,live-test)` alongside Q2 (`:719`, also `:811`). Every variant needs one more owner step.
- **A-002 (a permission-free session reading untrusted text makes only the intended writes): REJECT.** Nothing mechanical bounds it: permission checks are off (TB-PERM, `merged-requirements.md:631`) and issue text is untrusted (TB-UNTRUSTED, `:632`). D3 (`issue-watcher.md:44`) keeps issue text out of the prompt, but the session itself reads the issue during the accuracy check (`issue.md:16`). The FU-1 write list is what the claim intends, not what the session could do. The written acceptance should say it covers whatever the session does on the test issue, not only the listed writes. This hits Variant 2 hardest (two sessions).
- **A-003 (Orca is reachable and Q20 is answered when the owner answers): QUALIFY.** Both are hard preconditions of FU-1 under every variant (`merged-requirements.md:719`, `:811`; Q20 default at `:547` says WA-04 does not run). Orca was not reachable on 2026-11-13 (`:604`), current state UNVERIFIED. They do not change which variant is better, but every variant's "what happens next" should list them, and Variant 3's "FU-1 can run" is false until they hold.

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (tie) | 50 | Section sets are identical by design of the brief. |
| C-001 | V3 (V1 equal on this point) | 80 | `--pipeline none` matches recorded D2 and removes the second permission-free session; the default is a confirmed accident (ADJ X-001). |
| C-002 | V3 | 70 | A one-issue, scoped, non-precedent acceptance (`merged-requirements.md:572`) is bounded; V1 blocks indefinitely; V2 accepts twice the exposure. |
| C-003 | V3, amended with V2's item-5 gate | 65 | FU-1 should run after WA-01 to WA-03 once OB-H1 item 5, the grant row, ORCA-AVAILABLE and Q20 hold; V2 lists the wrong gate set for claim-only. |
| C-004 | V3 (V1 equal) | 75 | Code should conform to a recorded decision; the fix is one small PR (ADJ line 271). |
| C-005 | V3 | 75 | Only V3 has a reachable path to WA-05, SW-10, SW-13 and WA-07. |
| C-006 | V3 (V1 equal) | 75 | Removing the contradiction in code keeps D2 and its enforcement intact; amending D2 to fit an omission inverts the source of truth. |
| X-001 | V2 | 60 | V2 is the only variant that states FU-1 is gated; V3's "FU-1 can run" contradicts its own risk line and `refs/claim.md:131`. |
| X-002 | V3 (V1 equal) | 70 | D2 "claim-only" is the recorded decision (`issue-watcher.md:40`); V2's "ready plan" is a plausible but unrecorded reading of owner intent. |
| X-003 | V3 | 65 | One session, one test issue, written and scoped; V1 never tests, V2 doubles exposure. |
| A-001 | none (all share the gap) | 80 | All three omit `GRANT(WA-04,live-test)` (`merged-requirements.md:331`, `:719`). |
| A-002 | V1 | 60 | V1 alone does not rely on the unbounded assumption; V3 is acceptable only if its acceptance names the unbounded scope. |
| A-003 | V2 (marginal) | 55 | V2 alone treats FU-1 as gated on external preconditions, though it names the ship gates rather than Orca and Q20. |

## Overall

If I were neutral I would recommend **Variant 3**, at **75 percent** confidence, amended with three things: (1) OB-H1 item 5 ("before a claim at any level", `refs/claim.md:131`) listed as an FU-1 precondition, taken from Variant 2; (2) `GRANT(WA-04,live-test)`, ORCA-AVAILABLE and Q20 listed as FU-1 preconditions; (3) the written acceptance worded to cover whatever the one session does on the test issue, not only the listed writes (A-002). Variant 2's core choice (keep the default `worktree` level) I would not recommend for a first live test: it ratifies a confirmed omission and doubles the permission-free surface.
