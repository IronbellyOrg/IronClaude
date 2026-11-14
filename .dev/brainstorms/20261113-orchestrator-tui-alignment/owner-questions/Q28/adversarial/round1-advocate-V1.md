# Round 1 advocate statement: Variant 1 (Proposal A)

Advocate: Variant 1. Persona: architect (structure, dependencies, long-term impact). Depth: quick, Round 1 only.

## Position summary

Variant 1 is the only answer that brings PR #539, the largest open PR (1003 files, merge state UNSTABLE on 2026-11-14), back onto the project's one standard review loop, with the tool's mechanical push checks, once the owner's INV-008 ruling is applied and its thread is closed. It needs three amendments to hold up: the gate must be "Codex thread resolved", not "replied to"; the pre-ruling level-1 option should be dropped; and the grant row must make up for the PR-open check that `--merge-guard off` may skip.

## Steelman of Variant 2

Variant 2 turns spec rule SW-05 (6), "a new finding that needs an owner ruling stops the run before any fix, reply or resolve" (`merged-requirements.md:194`), into a structural property instead of a judgment call. At level 2 the state machine halts at `S4'_HALT_BEFORE_PUSH` "with NO commit, NO push, NO reply" (`sc-pr-submit-protocol/SKILL.md:307`). So even if Codex posts a new git-configuration finding after SW-02's push, the tool can at most leave an uncommitted local edit; a person sees every change before it leaves the machine. It still gets most of the tool's value: verification by `evidence-validator` (`SKILL.md:304`), deduplication across reviewers (`:303`), diagnosis through `sc:troubleshoot` (`:306`), and VAL validation (`:307`). It also needs no draft-toggle decision, because the merge guard has no effect below level 3 (`SKILL.md:241`). On a PR whose central open question is a security ruling, "a person approves every push" is a defensible default.

## Steelman of Variant 3

Variant 3 is the spec's own default if Q28 goes unanswered (`question.md:15`), so it needs no grant row and no new authority, and it cannot produce an unlisted write. It removes every way a tool can design, push or resolve anything near INV-008, which matches the hardest spec rule, "no tool designs or pushes an INV-008 fix" (`merged-requirements.md:191`), with zero interpretation. It also avoids every open uncertainty about the tool on this PR: whether the session can recognise "needs an owner ruling" (fact 5, PLAN INFERENCE), the pre-push guard that misses a merged PR (owner memory `pr-submit-check-pr-open-before-push.md:13`), and the late Codex security review (same memory). With only SW-02, SW-03 and the SW-05 refresh push left, the hand workload may be small.

## Key strengths claimed

1. **Follows the project standard and the spec's recommended answer.** The project rule is that PRs go through `/sc:pr-submit --monitor 3` (project `CLAUDE.md`, "The mandatory way to open a PR"); the spec's recommended answer to Q28 is level 3 with `--merge-guard off` after the ruling (`question.md:11`); the #539 author row already plans it: "after that, `/sc:pr-submit --monitor 3` on #539 only under the #539 GRANT row" (`merged-requirements.md:965`). Variant 1 is the only one that matches all three.
2. **Mechanical push safety that a hand push does not have.** At level 3 the tool binds the PR head at attach (`pr_head_ok`, `SKILL.md:299`), re-checks it before every push and refuses if the head moved (`:308`, reason `pr_head_mismatch`), refuses a push that would carry unrelated local commits (`push_parent_ok`, `:308`, reason `push_range_mismatch`), stages only the paths its edits changed and refuses files that held the operator's own pending changes (`OPERATOR_PENDING`, `:306`, `:308`), never force-pushes and never targets the default branch (`:308`). A person pushing by hand in Variants 2 and 3 has none of these checks.
3. **Verification before any fix.** Unverified findings become report-only and consume no round (`SKILL.md:304`); a dedup group gets one diagnosis and one fix (`:303`, `:306`). Variant 3 loses this entirely (its own risk list says a finding "can be missed or fixed without verification").
4. **Handles the late Codex review structurally better than a person.** The tool re-triggers both reviewers after each pushed fix (`@codex review`, `SKILL.md:308`) and polls until completion on the expected head (`refs/detection-contract.md:125-130`); a person must notice a late comment unaided.
5. **One session, one checkout.** The #539 author is the PR session (`merged-requirements.md:965`), so no hand-off of uncommitted edits between a tool session and a pushing session is needed.
6. **Complete grant row.** Variant 1 is the only one that lists every write the tool makes (attach, fix commits, troubleshoot artifacts, push, replies, resolves, the re-trigger comment, `--merge-guard off`, resume effects, never merge; variant-1 step 2), which rule 2 of section 6.4 requires (`merged-requirements.md:975`: "bounded by its `GRANT(<item>,pr-submit)` row, which lists every write the tool makes").

## Weaknesses identified in Variant 2

1. **Hand pushes lose the tool's push checks.** After level 2 halts, the author commits and pushes by hand: no `pr_head_ok`, no `push_parent_ok`, no `OPERATOR_PENDING` refusal (`SKILL.md:306-308`). The owner memory records the failure mode this invites: a push after a merge re-created a deleted branch (`pr-submit-check-pr-open-before-push.md:13`).
2. **Re-reviews are not re-triggered.** Level 2 never posts `@codex review` or `auggie review` (re-trigger is Wave 6, level 3 only, `SKILL.md:291`, `:308`); Variant 2 admits this ("the tool cannot re-request a review after the push"). Each cycle needs a hand comment, which is itself an outward write needing a grant.
3. **Every action needs its own grant.** Push, reply, resolve and re-trigger each need a separate row per cycle (`merged-requirements.md:975`), which multiplies owner decisions on the one PR that already gates SW-07 to SW-14 (`merged-requirements.md:194`, blocks column).
4. **The hand-off between tool output and person is not specified.** Variant 2 admits two live sessions must not share the #539 checkout. If they are the same session, the "person reviews" property depends on that session's own judgment, which is the same weakness Variant 2 attributes to Variant 1.
5. **Level 2 can still loop.** Each new run starts a new cycle with no shared round counter across hand pushes; the `max_rounds` cap (`SKILL.md:235`, `:311`) bounds one run, not the sequence of hand-separated runs. UNVERIFIED whether `--resume` would be used across hand pushes.

## Weaknesses identified in Variant 3

1. **Throws away the project's verification loop on the riskiest PR.** No `evidence-validator`, no dedup, no VAL gate; Variant 3 concedes a finding "can be missed or fixed without verification".
2. **Hand pushes without checks**, as in Variant 2 weakness 1, for every push to SW-05.
3. **The late Codex security review must be noticed by a person** (Variant 3 risk 3), exactly the case the owner memory says was missed (`pr-submit-check-pr-open-before-push.md:13`).
4. **Long-term cost.** #539 blocks SW-07, SW-08, SW-10 to SW-14 and more (`merged-requirements.md:194`); a manual loop on a 1003-file PR in UNSTABLE state is the slowest path to merge, and the default answer is meant as a fallback, not a design.
5. **Does not distinguish before and after the ruling.** Once INV-008 is ruled, applied and its thread resolved, the reason for a total ban is gone, but Variant 3 keeps it.

## Concessions

1. **X-001: Variant 2 is structurally stronger on the stop rule.** At level 3 the tool applies, commits, pushes, replies and resolves without a confirmation point (`SKILL.md:306`, `:308`); "stop on a finding that needs an owner ruling" has no switch in the skill (fact 5; `refactor-plan.md:118` per `question.md:28`). Variant 1 relies on the session's judgment. My amendment: the grant row states the stop rule in words the session checks before Wave 4 (any verified finding whose body or cited lines touch git configuration, `ALLOWED_GIT`, `core.fsmonitor`, `filter.*` or `include*` stops the run before any edit). That is still a procedural guard, not a mechanical one.
2. **The gate must be "resolved", not "replied".** For Codex, "Resolved threads are excluded; older unresolved Codex roots stay visible" (`refs/detection-contract.md:132-136`). Variant 1 says "closed by the owner's reply"; a reply alone leaves the INV-008 thread selectable, and at level 3 the tool would route a Codex P1 or P2 there to `sc:troubleshoot --depth deep --fix` (`SKILL.md:303`). The gate must read "the Codex thread at `probes.py:1211` is resolved (by the owner, or under `GRANT(SW-01,thread-resolve)`, `merged-requirements.md:190`)".
3. **Level 1 before the ruling should be dropped (X-004).** Level 1 still sends verified findings to `sc:troubleshoot` for diagnosis and proposes fixes (`SKILL.md:306`), so on the unresolved INV-008 thread it would design a fix proposal, which is in tension with "no tool designs or pushes an INV-008 fix" (`merged-requirements.md:191`). Variant 1 inherited this option from the spec's recommended answer; it adds risk for little value.
4. **`--merge-guard off` may drop the PR-open check.** `SKILL.md:309` scopes the Wave 6 merge-guard bullet, including "the guard's read must show the PR `OPEN`", to "L3 with `--merge-guard draft` only". `refs/merge-guard.md:94-97` says that read "applies whatever the guard phase is, including `disabled`". The two texts disagree; which one a session follows is UNVERIFIED. With `off`, the owner memory's failure (push after a merge, `pr-submit-check-pr-open-before-push.md:11-13`) may be reopened. Amendment: the grant row requires the session to run `gh pr view 539 --repo IronbellyOrg/IronClaude --json state` and require `OPEN` before each push, as the memory instructs, and the owner does not merge while a fix cycle runs (Variant 1 already says so).
5. **Re-poll before declaring clean** is a session instruction, not tool behaviour (owner memory, line 15); Variant 1 lists it as a risk only.

## Shared assumption responses

| id | response | reason |
|---|---|---|
| A-001 | QUALIFY | True only if the thread is marked resolved: resolved Codex threads are excluded, unresolved ones stay visible (`refs/detection-contract.md:132-136`). V1 and V2 must gate on "resolved", not on "closed by the owner's reply". Also, at level 3 the tool itself resolves only threads it fixed (`SKILL.md:308`), so it cannot close the INV-008 thread by accident once that thread is already resolved. |
| A-002 | REJECT | Nothing guarantees no new git-configuration finding: the level-3 tool itself re-triggers `@codex review` after each fix push (`SKILL.md:308`), and a Codex security review can land after a clean code review (owner memory line 13). V1 must carry a stated stop rule in the grant row (Concession 1); V2 is safe on this point by structure. |
| A-003 | ACCEPT (as a real risk for V2 and V3) | Hand pushes have no head binding, parent check or pending-file refusal (`SKILL.md:299`, `:306`, `:308`), and nobody checks the PR is still open unless the author remembers (owner memory lines 11-13). V1 is exposed to the PR-open half too under `--merge-guard off` (Concession 4). |
| A-004 | ACCEPT | `SKILL.md:47-49` requires a top-level session; `merged-requirements.md:975` rule 2 and `:964` forbid a worker or the coordinator. All three variants comply. |

## Per-point verdicts

| point | superior variant | one-line reason |
|---|---|---|
| S-001 | none (tie) | All three use the same five sections and four steps; structure does not separate them. |
| C-001 | V1 (with amendments) | After the ruling is applied and its thread resolved, level 3 gives verification plus mechanical push checks and re-triggers; level 2 drops the push checks onto a person. |
| C-002 | V2 | No tool before the ruling is cleaner; V1's optional level 1 would diagnose the open INV-008 thread (`SKILL.md:306`). |
| C-003 | V1 | The tool's pushes carry `pr_head_ok`, `push_parent_ok` and named-path staging (`SKILL.md:299`, `:308`); hand pushes carry none. |
| C-004 | V2 | Level 2 removes the toggle question entirely, while V1's `--merge-guard off` may also drop the PR-open read (`SKILL.md:309` versus `refs/merge-guard.md:94-97`). |
| X-001 | V2 | Level 2 stops before commit, push, reply and resolve by design (`SKILL.md:307`); V1's stop rests on session judgment. |
| X-002 | V1 | Only V1 follows the project's `--monitor 3` standard and the spec's planned #539 author role (`merged-requirements.md:965`). |
| X-003 | V1 | One session does fix, commit and push in the one checkout; V2 needs an explicit hand-off between tool output and person. |
| X-004 | V2 | No level 1 before the ruling keeps the tool from designing an INV-008 fix proposal (`merged-requirements.md:191`); V1 should drop that option. |
| A-002 | V2 | A new git-configuration finding cannot be pushed or resolved at level 2; V1 needs a grant-row stop rule. |
| A-003 | V1 | The tool's pre-push checks cover the head and push range that hand pushes leave unchecked; V1 still needs the manual PR-open read under `off`. |

## Overall pick

Variant 1, amended: gate on the Codex INV-008 thread being resolved, drop the pre-ruling level-1 option, and put a git-configuration stop rule plus a PR-open check before each push into the #539 grant row.
