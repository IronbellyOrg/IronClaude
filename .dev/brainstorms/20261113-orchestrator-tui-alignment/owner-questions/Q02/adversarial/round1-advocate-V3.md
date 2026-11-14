# Round 1 advocate statement: Variant 3 (proposal C, claim-only plus written acceptance for the one test issue)

Persona: analyzer (evidence quality and logical consistency). Depth quick, Round 1 only.

## Position summary

Variant 3 is the only answer that matches the recorded owner decision D2 and keeps the permission-free exposure to one session on one test issue. It also lets the first live test go ahead once its real preconditions hold. Its weak point is that it overstates "FU-1 can run": the claim command's "claim at any level" gate (OB-H1 item 5) applies to `--pipeline none` as well, and the design document records it as not yet run. Variant 3 also leaves out the `live-test` grant, Orca availability and Q20. Those preconditions have to be written into the answer.

## Steelman

### Variant 1 (claim-only, decline the acceptance, FU-1 waits)

Strongest version: INV-012 is rated HIGH. The spec itself lists "WA-01 (`--pipeline none`) alone makes a watcher claim safe" as a claim that downstream conditions falsify: "the first session still assigns, comments and reads untrusted issue text with permission checks off (INV-012); a non-empty `CC_CLAUDE_FLAGS` replaces the flags (INV-011)" (`merged-requirements.md:1158`). An owner who has not accepted that risk for anything else should not be pushed into accepting it for convenience. Variant 1 gets the claim level right and also proposes the one investigation the other two leave out: whether a watcher-launched session can run with permission checks on (the two knobs `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS`, INV-011) and still finish unattended (U-001).

Critique: Variant 1 gives no route to that answer that avoids a live launch. Its own risk section says a permission-on session "may stop at a permission prompt with nobody to answer it", which "could make FU-1 impossible in that form". So the hold may never end. Meanwhile D-A, D-B and the operation-id path stay unsettled, and so do WA-05, WA-06, SW-10, SW-13 and WA-07 (`merged-requirements.md:812`, `:886`). The risk it declines is already bounded by the spec's own rules:
- the consent covers the test issue only and authorises no later issue (`:572`, `:983`);
- the writes are inventoried (`:331`; WA-04 (i), `:306`);
- the test issue is closed or unlabelled afterwards (WA-04 (i)).

What Variant 1 buys with the hold is mostly the absence of data. It does not reduce a risk that the scoped acceptance leaves unbounded.

### Variant 2 (keep the default `worktree` level as a deliberate chain, gated on the ship gates)

Strongest version: an approval in a work tracker plausibly means "start the work". The default level delivers a plan that a person approves, and nothing merges (`issue.md:16`). Variant 2 is also the most rigorous of the three on gates. It names OB-H1 item 1 **and item 5**, OB-H2 and OB-H3 as preconditions. That matches `claim.md:131` more fully than the spec's own WA-01 default branch, which lists only "OB-H1 item 1, OB-H2, OB-H3" (`merged-requirements.md:303`) and ADJ action 1, which does the same (`alignment-findings-adjudicated.md:271`). Its FU-1 would also collect data about a second session for the later handoff design (U-002).

Critique:
1. **It overrides a recorded owner decision.** D2 "claim-only" is quoted verbatim from the owner's seed brief, and its consequence reads "The claim stops at `next-steps.md`" (`docs/designs/issue-watcher.md:39`, `:44`). Variant 2's "what an approval most plausibly wants" is an inference that has no source. Variant 2 does put the amendment to the owner, so this is a fair option, but its case rests on intent that no document records.
2. **It doubles the permission-free surface.** There are two sessions per approval, and the second one runs in a worktree and starts from an untrusted issue (TB-UNTRUSTED, `merged-requirements.md:632`).
3. **It is blocked on four gates that the design records as not run.** The design says: "Pending, none run: OB-H1 items 1 to 9, OB-H2, OB-H3" (`docs/designs/sc-issue-launch-level-hook.md:625`). Whether they have run since is UNVERIFIED, but the only documentary evidence says they have not.
4. **Every approval creates an unowned worktree agent.** Q20 covers only the watcher worktree, a gap Variant 2 itself admits.

## Strengths claimed

1. **It agrees with the recorded owner decision and with every reviewed recommendation.**
   - D2: "The claim stops at `next-steps.md`" (`docs/designs/issue-watcher.md:44`).
   - The spec recommends "`--pipeline none`; yes, in writing, for the test issue only" (`merged-requirements.md:529`).
   - ADJ Part 7 Q2 recommends the same (`alignment-findings-adjudicated.md:772`).
   - ADJ action 1 says `--pipeline none` is "exactly design decision D2" (`:271`).
2. **It has the smallest permission-free surface that still allows a live test.**
   - `none` "creates no worktree and launches no agent" (`issue.md:16`, `:43`), so there is one permission-free session instead of two.
   - The consent is scoped "for the test issue only" (WA-04 (b), `merged-requirements.md:306`; `:983`), and the variant records that scope in the ledger (U-004; `:572`).
3. **It is reversible and small.** ADJ action 1: "Undo: yes, a small PR" (`alignment-findings-adjudicated.md:271`). WA-01 shares no file with #539 (`merged-requirements.md:303`).
4. **It escapes the governed-claim gates.** OB-H1 item 1, OB-H2 and OB-H3 apply only to a "governed claim (`--pipeline worktree` or `full`)" (`claim.md:131`). Under Variant 3, only item 5 is left, against Variant 2's four.
5. **It is the only path that produces FU-1's evidence.** FU-1 settles D-A, D-B and the operation-id path (WA-04 (d), (e), (f), `merged-requirements.md:306`). WA-05, WA-06, SW-10, SW-13 and WA-07 depend on it (`:812`, `:886`).
6. **It records its own residual risk honestly.** It keeps INV-012 alive ("does not remove it"), flags the item-5 gate as UNVERIFIED, and flags the ClickUp write as of unknown reversibility. These match ADJ action 2 (b) and (i) (`alignment-findings-adjudicated.md:271`).

## Weaknesses identified in other variants

1. **Variant 1 may hold with no end.** No step in Variant 1 settles permission-on feasibility without a live launch. Its own risk section expects that an unattended permission-on session may stall. The data FU-1 would produce (WA-04 (d) to (f)) stays missing.
2. **Variant 1's decline does not reduce exposure for later issues either.** The consent already authorises no future issue (`merged-requirements.md:572`). What Variant 1 withholds is one bounded test, not a standing permission.
3. **Variant 2 contradicts D2.** It needs a design amendment that rewrites an owner decision recorded verbatim (`docs/designs/issue-watcher.md:39`, `:44`), on an intent claim with no source.
4. **Variant 2 doubles the permission-free sessions.** Each approval gets two sessions and a launched agent working from untrusted issue text, and the written acceptance has to cover both (C-002).
5. **Variant 2 is the most blocked option.** All four gates it names are "Pending, none run" in the design document (`sc-issue-launch-level-hook.md:625`; live status UNVERIFIED).
6. **Variant 2 leaves agents unowned.** The `issue-<N>` worktree agents have no named owner; Q20 covers only the watcher worktree (`question.md`, last fact row; `merged-requirements.md:547`, cited there).

## Concessions

1. **Variant 3's "FU-1 can run" is wrong as written (X-001).**
   - `claim.md:131` and `sc-issue-launch-level-hook.md:201` say "no claim at any level until item 5 shows self-started turns wrapped", and `:625` lists item 5 as "Pending, none run".
   - FU-1 also needs GRANT(WA-04,live-test) (`merged-requirements.md:331`, row 72 at `:719`, `:811`), ORCA-AVAILABLE (`:604`; Orca was not reachable on 2026-11-13) and Q20 through WA-03 (`:811`).
   - Variant 3 should list all four as FU-1 preconditions instead of putting one of them in a risk bullet.
2. **The spec has the same gap.** Its WA-04 predecessors (`merged-requirements.md:306`) do not list OB-H1 item 5 for the `none` path, and WA-01's default branch omits item 5 (`:303`). Variant 2 is more complete than Variant 3, and than the spec, on gate naming (U-003).
3. **The written acceptance bounds INV-012; it does not remove it.** The spec says so (`merged-requirements.md:1158`).
4. **Less is delivered per approval.** Under Variant 3 an approval yields a claim and comments, not a ready plan. If the owner's real intent differs from D2, Variant 2 serves it better.
5. **Variant 1's U-001 is worth adopting.** FU-1 already records the permission variables and argv (WA-04 (c)). Adding an explicit feasibility note on permission-on operation would let a later, non-test decision rest on data.

## Shared assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | REJECT | The spec requires a separate grant row: "The first rollout is therefore a bounded test under `GRANT(WA-04,live-test)` with the owner's consent" (`merged-requirements.md:331`). Row 72 lists `GRANT(WA-04,live-test)` as a WA-04 predecessor (`:719`), and so does the chain at `:811`. Q2 alone does not authorise FU-1's outward writes under any variant. |
| A-002 | REJECT | No source shows that a permission-free session bounds its own writes. The FU-1 write list (WA-04 (i)) is the list of *intended* writes, not a limit. D3 keeps issue text out of the prompt (`issue-watcher.md:45`), but the session still reads that text during the accuracy check (`issue.md:16`). `--dangerously-skip-permissions` is in effect (TB-PERM, `merged-requirements.md:631`). Whether the accompanying `--allowedTools=Grep` restricts anything under skip-permissions is UNVERIFIED. The acceptance therefore covers more than it names, and the owner should be told so. |
| A-003 | QUALIFY | It is true that every live option needs ORCA-AVAILABLE (`merged-requirements.md:604`) and Q20 through WA-03 (`:811`). It is not true that they hold now: the probe found Orca not reachable on 2026-11-13, and the spec does not claim that outage is still current. These are shared preconditions, not differentiators. Each variant should state them, and none should claim FU-1 "can run" before both hold. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (identical) | 95 | Same five sections in the same order, by design of the brief. |
| C-001 | V3 (tied with V1) | 85 | `none` matches D2 (`issue-watcher.md:44`), halves the permission-free sessions and avoids three of the four gates (`claim.md:131`). |
| C-002 | V3 | 65 | A scoped, recorded acceptance for one inventoried test is a bounded risk (`:572`, `:331`). V1's decline is defensible but may leave the hold with no end. V2 widens the acceptance to two sessions. |
| C-003 | V3, amended | 60 | V3's timing is closest, but it must name OB-H1 item 5, GRANT(WA-04,live-test), ORCA-AVAILABLE and Q20 as explicit preconditions. V2's explicit-precondition style is the better form. |
| C-004 | V3 (tied with V1) | 80 | One small reversible PR (ADJ `:271`) makes the code match an owner decision. V2 instead rewrites the decision to match the code. |
| C-005 | V3 | 65 | Only V3 unblocks downstream work on a gate set that can actually be met (one pending gate, not four). The unblock is conditional on the C-003 preconditions. |
| C-006 | V3 (tied with V1) | 80 | Removing the contradiction in code keeps a verbatim owner decision intact (`issue-watcher.md:39`). |
| X-001 | V2 | 60 | V2 says honestly that FU-1 cannot run until gates pass. V3 contradicts itself ("FU-1 can run" against its own item-5 risk). V2's gate set is wrong for `none`, but its stance is the more consistent one. |
| X-002 | V3 (tied with V1) | 80 | D2 is the owner's recorded intent. V2's "ready plan" intent has no source. |
| X-003 | V3 | 65 | One bounded test session is accepted, with its consent scoped and recorded. V1 refuses all data; V2 accepts twice the exposure. |
| A-001 | none (shared gap) | 85 | All three omit GRANT(WA-04,live-test) (`merged-requirements.md:331`, `:719`). |
| A-002 | V1 | 60 | V1 alone declines to rely on the assumption. V3 and V2 both rely on it implicitly and should state the residual risk to the owner. |
| A-003 | none (shared gap) | 80 | ORCA-AVAILABLE and Q20 bind every live option equally (`:604`, `:811`). |

## Overall

If I were neutral, I would recommend **Variant 3**, at confidence 70, with three amendments:
1. FU-1's preconditions are stated in full: OB-H1 item 5 (`claim.md:131`; recorded as "Pending, none run" at `sc-issue-launch-level-hook.md:625`), GRANT(WA-04,live-test), ORCA-AVAILABLE and Q20.
2. The acceptance text tells the owner plainly that a permission-free session reading untrusted text is not bounded by the intended-write list (A-002).
3. Variant 1's permission-on feasibility check (U-001) is folded into the FU-1 record.

Variant 1 is the right fallback if the owner will not accept A-002's residual risk. Variant 2 is right only if the owner states that D2 no longer reflects what an approval should deliver.
