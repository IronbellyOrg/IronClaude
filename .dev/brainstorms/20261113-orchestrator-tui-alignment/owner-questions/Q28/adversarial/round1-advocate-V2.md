# Round 1 advocate statement: Variant 2 (Proposal B, level 2 after the ruling, hand pushes)

Persona: security (vulnerabilities, trust boundaries, blast radius). Evidence read 2026-11-14.

## Position summary

On the one PR that carries an open, owner-reserved security ruling (INV-008), the tool's verification and fixing are worth having, but nothing the tool produces should leave the machine without a person seeing it first. Level 2 gives that as a property of the state machine (`SKILL.md:307`: "NO commit, NO push, NO reply"), not as a promise about the running session's judgment, which is what Variant 1 relies on. Two corrections found while checking (below) must be folded into Variant 2 before the owner picks it.

## Steelman of Variant 1

Variant 1 is exactly the spec's recommended answer (`merged-requirements.md:555`) and the project's standard way of working (`CLAUDE.md`, "The mandatory way to open a PR"). The tool's push path carries mechanical hygiene a person typing by hand does not: a pre-push head guard against the stored PR head, a parent check so a push carries only the cycle's one fix commit, named-path staging, refusal to commit files with the operator's own pending changes, and a write-ahead push record (`SKILL.md:306`, `:308`). Variant 1 also gives the most complete grant row of the three (attach, fix commits, troubleshoot artifacts, push, replies, resolves, re-trigger comment, `--merge-guard off`, resume effects, never merge; `variant-1-original.md:10`), which matches what the spec says a `pr-submit` row must list (`merged-requirements.md:1050`). It keeps a single session in the #539 checkout (`merged-requirements.md:965`), and it avoids a visible draft flip on a 1003-file, long-open PR. On a PR whose merge state is UNSTABLE today, an automated loop that fixes red checks and verified findings without hand work is a real benefit, and Variant 1 is honest about its main risk (`variant-1-original.md:21`).

## Steelman of Variant 3

Variant 3 has the smallest blast radius possible: no automated write of any kind on the PR that holds the open INV-008 thread (`variant-3-original.md:16`). It is the only variant that fully honours "no tool designs or pushes an INV-008 fix" (`merged-requirements.md:191`) for findings that arrive after the ruling, because no tool ever reads a finding. It needs no grant row, so there is no unlisted-write risk (`variant-3-original.md:17`). It is also the spec's default if the owner does not answer (`question.md:15`), so choosing it costs no new ledger work.

## Key strengths claimed

1. **The stop for "a finding that needs an owner ruling" is structural for every outward effect.** SW-05 (6) requires that such a finding "stops the run before any fix, reply or resolve" (`merged-requirements.md:194`). The skill has no switch for this (`question.md:29`; `refactor-plan.md:118` per `question.md:28`). At level 2 the state machine halts at `S4'_HALT_BEFORE_PUSH` with no commit, push, reply or resolve (`SKILL.md:307`), so a tool-designed fix to a new git-configuration finding cannot reach the PR or close its thread without a person. Variant 1's level 3 commits, pushes, replies and resolves on every verified Medium-or-higher finding, Codex P-badges included (`SKILL.md:303`, `:308`).
2. **No tool resolve can close a security thread.** Codex findings are selected from unresolved threads only (`refs/detection-contract.md:132-136`). At level 3 the tool resolves the thread it fixed (`SKILL.md:308`), which removes the finding from every later poll; a wrong fix then hides itself. Level 2 cannot resolve.
3. **No draft toggle and no `--merge-guard off` ambiguity.** The guard has no effect below level 3 (`SKILL.md:241`). Variant 1's `--merge-guard off` matters more than the "no visible draft flip" framing suggests: the PR-is-OPEN pre-push read is documented in `refs/merge-guard.md:94-97` as applying "whatever the guard phase is, including `disabled`", but `SKILL.md:309` loads that ref at Wave 6 only for "L3 with `--merge-guard draft` only". Whether the OPEN check runs under `off` is therefore UNVERIFIED, and that check is exactly the one whose absence let a push re-create a merged PR's deleted branch (owner memory `pr-submit-check-pr-open-before-push.md`, PR #368, 2026-11-04). Level 2 never pushes, so the question does not arise.
4. **It keeps the tool's real value.** Detection over both reviewers, verification by the `evidence-validator` (`SKILL.md:304`), deduplication (`:303`), troubleshoot diagnosis and validated edits (`:306`, `:307`). Variant 3 throws this away on a 1003-file PR, where a missed or unverified finding is the likelier failure (`variant-3-original.md:22`).
5. **Matches the spec's rule boundary.** The spec forbids attaching at `--monitor 2` or `3` only before the ruling (`merged-requirements.md:192`, `:965`); Variant 2 attaches only after it, and keeps the spec's ban on any tool INV-008 fix push (`:191`, `:577`).

## Weaknesses identified in Variant 1

1. **The owner-ruling stop rests on session judgment.** Variant 1 admits it (`variant-1-original.md:21`). Codex re-reviews each push and a security review can land after a clean code review (owner memory). A Codex P1 or P2 that touches git configuration again would be routed to `sc:troubleshoot --depth deep --fix` (`SKILL.md:303`), fixed, pushed and its thread resolved, which is the R25-INV-005 bypass the question exists to prevent (`question.md:28`).
2. **`--merge-guard off` widens the push blast radius.** The PR stays mergeable during a fix cycle (`variant-1-original.md:22`), and the PR-OPEN pre-push check may not run under `off` (Strength 3, UNVERIFIED). A mid-cycle merge followed by a tool push is the documented #368 failure.
3. **Optional level 1 before the ruling contradicts the spec's own fix ban.** Level 1 still sends verified findings, including the unresolved Codex INV-008 thread, to `sc:troubleshoot` for diagnosis and proposes a fix (`SKILL.md:306`; diff-analysis X-004), which is a tool designing an INV-008 fix (`merged-requirements.md:191`, `:577`).
4. **The gate wording "closed by your reply" is not enough.** A reply alone leaves the thread unresolved and selectable (`refs/detection-contract.md:132-136`; diff-analysis A-001). If the owner replies without resolving, a level 3 run would pick up the INV-008 thread itself.

## Weaknesses identified in Variant 3

1. **No verification step on a 1003-file PR with an UNSTABLE merge state.** Every finding and red check is read, judged and fixed by hand (`variant-3-original.md:21-22`); a fix applied without the evidence check is its own security risk on a security-sensitive diff.
2. **A late Codex security review must be noticed by a person** (`variant-3-original.md:23`); the tool's poll loop, with the owner memory's re-poll, is better at that than a person, and Variant 2 keeps it.
3. **"Nothing stays unresolved" understates the cost.** Every SW-05 hand push lacks the tool's head and parent checks (diff-analysis A-003), the same weakness Variant 2 has, with no tool help at all for findings.

## Concessions

1. **Variant 2's grant row as written is incomplete.** At level 2 the Wave 6b decline fallback still runs: if Augment posts an "abnormally large" decline, the skill invokes `/sc:auggie-review` with `--post-pr` on by default, which auto-posts its report to the PR, and `--no-post-pr` "must NOT be passed" (`refs/auggie-fallback.md:35`; `SKILL.md:310`: "At L2 this can apply and validate local fixes but still halts before push/reply"). So level 2 can make one outward write, a PR comment, which `variant-2-original.md:10` does not list. A 1003-file PR is the case that decline exists for; no decline is on #539 today (read 2026-11-14: 5 issue comments, none matching "abnormally large"). Fix: the #539 grant row lists "one `/sc:auggie-review` report comment" or the owner refuses it and the run is held on a decline (`merged-requirements.md:1050`: "without consent the run is held").
2. **Level 2 still designs fixes locally.** For a new INV-008-class finding after the ruling, the tool diagnoses and edits the working tree (`SKILL.md:306`). That is "designing" in the sense of `merged-requirements.md:191`. Variant 2 stops it from leaving the machine, not from being written. Only Variant 3 avoids it entirely.
3. **Hand pushes lose the tool's mechanical push hygiene** (A-003). Variant 2 should require, before each hand push, the owner memory's checks: `gh pr view 539 --repo IronbellyOrg/IronClaude --json state,headRefOid` shows OPEN and the expected head, `git ls-remote origin refs/heads/<branch>` shows the branch exists, and only named paths are staged.
4. **Two sessions in one checkout** (`variant-2-original.md:24`; X-003) is avoidable only if the #539 author is also the PR session, which `merged-requirements.md:965` already allows. Variant 2 should say so instead of describing a hand-off.
5. **Variant 2 departs from the spec's recommended answer** (`merged-requirements.md:555`) and the project standard, and it is slower; the owner may reasonably decide the INV-008 risk ends at the ruling.

## Shared assumption responses

| Assumption | Response | Reason |
|---|---|---|
| A-001 (resolved thread is ignored) | QUALIFY | Verified at `refs/detection-contract.md:132-136`, but only for a thread marked resolved. The gate for every variant that runs the tool must read "the Codex thread at `probes.py:1211` is resolved", not "closed by the owner's reply" (wording at `merged-requirements.md:194`, `:555`). Variant 2 adopts that wording. |
| A-002 (no new git-config finding after SW-02) | REJECT | Codex re-reviews pushes and a security review can post after a clean code review (owner memory). No variant should rely on it. Variant 2 contains its outward effect (no push, reply or resolve); Variant 1 does not; Variant 3 never reads findings with a tool. |
| A-003 (hand pushes stay safe without the tool's checks) | QUALIFY | Safe only with the owner memory's checks (PR OPEN, branch exists, head as expected, named paths) run by hand before each push. Variant 2 and Variant 3 should both write those checks into the push grant. |
| A-004 (top-level session only) | ACCEPT | `SKILL.md:47-48` and `merged-requirements.md:975` rule 2 agree; no variant departs from it. |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie | All three use the same five sections and four steps; nothing to choose. |
| C-001 | V2 | Level 2 keeps verification and fixing but every outward effect passes a person (`SKILL.md:307`); level 3 acts on a security PR by itself, and "never" discards verification. |
| C-002 | V2 (tie with V3) | Nothing before the ruling; V1's optional level 1 sends the INV-008 finding to troubleshoot, a tool-designed fix proposal against `merged-requirements.md:191`, `:577`. |
| C-003 | V2, with A-003's checks added | A person is the last gate on each push, reply and resolve on a security-sensitive PR; V1's tool push has better mechanics, so V2 must borrow them by hand. |
| C-004 | V2 | No toggle question and no exposure to the UNVERIFIED PR-OPEN check under `--merge-guard off` (`SKILL.md:309` vs `refs/merge-guard.md:94-97`). |
| X-001 | V2 | The only variant where the SW-05 (6) stop is enforced by the state machine for every outward effect rather than by session judgment. |
| X-002 | V1 | V1 alone follows the project's level 3 loop; the weight is limited because #539 is already open (`question.md:33`). |
| X-003 | V1 (tie with V3) | One session in the checkout; V2 matches only if the #539 author is the PR session, which it should state. |
| X-004 | V2 (tie with V3) | Neither allows any tool level before the ruling. |
| A-002 | V3 | Only V3 has no tool response at all to a new git-configuration finding; V2 is second (local design only). |
| A-003 | V1 | The tool's pre-push head guard, parent check and write-ahead record beat a hand push; V2 and V3 must replicate them by hand. |

## Overall pick

Variant 2, amended: gate on the Codex thread being resolved, list the possible `/sc:auggie-review` PR comment in the grant row (or hold on a decline), run the owner memory's pre-push checks by hand, and make the #539 author the one session that runs level 2.
