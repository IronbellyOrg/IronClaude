# Round 1 advocate statement: Variant 3 (proposal C, no `/sc:pr-submit` on PR #539 at any level)

Persona: qa (edge cases, failure scenarios, risk). Depth: quick, Round 1.

## Position summary

Variant 3 is the only answer that meets the spec's two hard rules on #539 by construction rather than by a session's judgment: "no tool designs or pushes an INV-008 fix" (`merged-requirements.md:191`) and "a new finding that needs an owner ruling stops the run before any fix, reply or resolve" (`merged-requirements.md:194`, SW-05 (6)). Its cost is real hand work on a 1003-file, UNSTABLE PR, which I concede below, but every failure mode it carries is a person being slow, not a tool silently acting on the security thread.

## Steelman of Variant 1

Variant 1 is the spec's own recommended answer, almost word for word (`merged-requirements.md:555`), so it is the answer the requirements were written around. It keeps one session in the #539 checkout (the #539 author is the PR session, `merged-requirements.md:965`) and puts every tool write under one grant row that lists them all (`merged-requirements.md:1050`, Variant 1 step 2). After the ruling, the tool brings real guards a person does not: evidence-validator verification before any fix (`SKILL.md:304`), one fix commit per cycle staging named paths only and refusing operator-pending files (`SKILL.md:306`, `:308`), a pre-push head guard and a parent check so a push carries only the cycle's commit (`SKILL.md:308`), and re-trigger of both reviewers after each push (`SKILL.md:308`). On a 1003-file PR whose merge state is UNSTABLE (question.md fact 6), that loop is the project's standard way to reach green (project `CLAUDE.md`, "The mandatory way to open a PR"). It gates the start on the Codex thread being closed, and the detection contract does exclude resolved Codex threads (`refs/detection-contract.md:132-136`), so the original INV-008 thread is out of reach once resolved.

## Steelman of Variant 2

Variant 2 keeps the tool's verification and diagnosis but makes the outward writes structurally impossible: level 2 halts at `S4'_HALT_BEFORE_PUSH` "with NO commit, NO push, NO reply" (`SKILL.md:307`). So no tool can reply to or resolve a thread that needs the owner's ruling (Variant 2, "What it unlocks"), and every change to a security-sensitive PR passes a person's eyes before it leaves the machine. It also removes the draft-toggle decision entirely, because the merge guard has "No effect below L3" (`SKILL.md:241`). It is the closest thing to a mechanical version of the SW-05 (6) stop that the skill allows today, since the skill has no switch to exclude one thread (question.md fact 4, `refactor-plan.md:118`).

## Key strengths claimed

1. **Only variant where no tool designs an INV-008 fix.** Line 191 bans a tool that "designs or pushes" an INV-008 fix. At level 1 the tool still sends verified findings to `sc:troubleshoot` for diagnosis (`SKILL.md:306`); at level 2 and 3 it applies the diagnosed edits itself (`SKILL.md:306`). Any new Codex finding on git configuration after SW-02's push is therefore designed by a tool under Variants 1 and 2. Under Variant 3 it is not.
2. **Only variant that satisfies "stops the run before any fix" structurally.** SW-05 (6) says the stop comes "before any fix, reply or resolve" (`merged-requirements.md:194`). Variant 2 stops before push, reply and resolve, but not before the fix: level 2 applies and validates the edit first (`SKILL.md:307`). Variant 1 relies on the session noticing; the skill has no built-in way to recognise a finding that needs an owner ruling (question.md fact 5). Variant 3 has no run to stop.
3. **Immune to the reply-versus-resolve gap.** Variants 1 and 2 gate on the Codex thread being "closed by the owner's reply". A reply alone leaves the thread unresolved, and unresolved Codex roots "stay visible" to the tool (`refs/detection-contract.md:132-136`; diff-analysis A-001 note). If the owner replies but the resolve is not done (it is a separate write), a level 3 run selects the INV-008 thread itself. Variant 3 cannot.
4. **Immune to a late Codex security finding.** Owner memory records that a Codex security review can post minutes after the code review reported clean (`pr-submit-check-pr-open-before-push.md:13`). The tool re-triggers `@codex review` after every fix push (`SKILL.md:308`), so on #539 each tool push invites a new security pass on the same git-status code. Variant 3 makes fewer pushes and none of them auto-fix what Codex says next.
5. **No grant row to get wrong.** An unlisted write needs a new row and holds the run (`merged-requirements.md:1050`). Variant 3 needs no #539 pr-submit row at all, so there is no "unlisted write" failure path (Variant 3, "What it unlocks").
6. **Matches the spec's stated default.** The default if unanswered is exactly Variant 3 (`merged-requirements.md:555`), and the spec already makes SW-02 and SW-03 hand pushes either way (`:191`, `:192`). Variant 3 extends an approved pattern; it adds no new mechanism.

## Weaknesses identified in Variant 1

1. **The ruling stop is a judgment, not a gate.** Variant 1 admits "the 'stop on a finding that needs an owner ruling' rule rests on the session's judgment, not on a switch in the tool" (Variant 1, "What it costs or risks"). At level 3 a verified Medium or higher finding is routed to `--fix` or `--depth deep --fix` automatically (`SKILL.md:303`), and a Codex P1 or P2 badge is its severity (`refs/detection-contract.md:136-137`). A git-configuration P1 is exactly the case the rule exists for.
2. **`--merge-guard off` may also switch off the PR-open check before a push.** `SKILL.md:309` scopes the Wave 6 merge-guard step, which loads `refs/merge-guard.md` and runs its Pre-push read that "must show the PR `OPEN`", to "L3 with `--merge-guard draft` only". `refs/merge-guard.md:94-97` says that read "applies whatever the guard phase is, including `disabled`, and at every ordinal that reaches the push", but with `off` the ref is loaded only on resume or when the run log already holds guard events (`SKILL.md:301`). The two texts disagree, so whether a `--merge-guard off` run checks that the PR is still open is UNVERIFIED. If it does not, Variant 1 reopens the exact failure in owner memory: a PR merged mid-cycle, a head guard that still passes, and a push that re-creates the deleted branch (`pr-submit-check-pr-open-before-push.md:13`).
3. **No draft toggle means the PR is mergeable mid-cycle.** Variant 1 concedes "the owner must not merge mid-cycle". That is an instruction to a person, on a PR open for days with 1003 files (question.md fact 6).
4. **The level-1-before-ruling option breaks line 191.** Level 1 still dispatches the verified Codex INV-008 finding to `sc:troubleshoot`, which designs a fix proposal (diff-analysis X-004; `SKILL.md:306`). Leaving that open "if the grant row says so" makes a spec violation depend on how a row is worded.
5. **The gate wording is wrong by one write.** "Closed by your reply" is not "resolved" (strength 3 above).

## Weaknesses identified in Variant 2

1. **It still designs the fix.** Level 2 applies the diagnosed edits in the working tree (`SKILL.md:306-307`). For a new git-configuration finding that is a tool designing an INV-008 fix, which line 191 forbids, and it happens before the stop that SW-05 (6) wants "before any fix".
2. **Two actors in one checkout.** Variant 2 admits the PR session and the #539 author "must not both have live sessions in the #539 checkout at once" (Variant 2, "What it costs or risks"; diff-analysis X-003). The spec names the #539 author as the one PR session (`merged-requirements.md:965`), so either they are the same session (then the hand-off is just Variant 3 plus tool-applied edits) or a second session is added, which the spec does not provide for.
3. **Uncommitted tool edits meet hand edits.** Each cycle ends with "validated, uncommitted changes in the #539 checkout" (Variant 2 step 3). The tool's operator-pending refusal only guards its own commit at level 3 (`SKILL.md:308`); at level 2 the person commits, so tool edits and hand edits can mix in one file with no tool check.
4. **Hand pushes lose the tool's pre-push guards anyway.** Variant 2 pushes by hand, so it shares A-003 with Variant 3 while still paying for the tool's level-2 risk.
5. **No re-trigger.** The tool cannot re-request a review after the person's push (Variant 2 concedes this), so the late Codex security pass must still be noticed by a person, the same burden Variant 3 carries.

## Concessions

1. **Hand work is large and real.** Every finding and red check on a 1003-file PR with merge state UNSTABLE (read 2026-11-14) is handled by a person (Variant 3, "What it costs or risks"; question.md fact 6).
2. **Hand pushes lack the tool's guards.** A person's push has no pre-push head guard, no parent check that only one commit is published, and no operator-pending refusal (`SKILL.md:308`). Owner memory gives the manual check (`gh pr view <N> --repo IronbellyOrg/IronClaude --json state` and `git ls-remote origin refs/heads/<branch>`, `pr-submit-check-pr-open-before-push.md:11`), but Variant 3 does not write that check into its steps. It should.
3. **No verification pass.** Variant 3 gives up the evidence-validator step (`SKILL.md:304`), so a finding can be fixed without checking it reproduces (Variant 3 admits this).
4. **It departs from the spec's recommended answer** (`merged-requirements.md:555`) and from the project's habit of running the review loop at level 3 (project `CLAUDE.md`), although the project rule is about opening a PR and #539 is already open (question.md fact 9).
5. **It has no exit.** Variant 3 never revisits the decision, even after #539's review settles. A "no tool until X, then ask again" clause would cost nothing.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | Verified: resolved Codex threads are excluded and unresolved ones stay visible (`refs/detection-contract.md:132-136`). But Variants 1 and 2 gate on the thread being "closed by your reply", and a reply does not resolve it; the gate must say "resolved", and the resolve is a separate write needing its own grant. Variant 3 does not depend on it. |
| A-002 | REJECT | Nothing supports it. The tool re-triggers `@codex review` after every fix push (`SKILL.md:308`), Codex P-badges map to severity (`refs/detection-contract.md:136-137`), and a security review can land after a clean code review (owner memory, `:13`). SW-02 changes the very git-status code INV-008 is about, so a new git-configuration finding is a likely event, not an edge case. |
| A-003 | QUALIFY | True that hand pushes lack the tool's head guard and parent check (`SKILL.md:308`). But the tool's own guard missed a merged PR (owner memory), and whether a `--merge-guard off` run reads PR state before pushing is UNVERIFIED (`SKILL.md:309` versus `refs/merge-guard.md:94-97`). Variant 3 should add the owner-memory check (state `OPEN`, branch exists) before every hand push. |
| A-004 | ACCEPT | `merged-requirements.md:975` rule 2 and `SKILL.md:42-48` (top-level activation required) agree. |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | none (tie) | All three use the same five sections and four steps; no structural difference to judge. |
| C-001 | V3 | Only level "none" keeps any tool from designing a git-configuration fix, which line 191 forbids; levels 2 and 3 both apply diagnosed edits (`SKILL.md:306-307`). |
| C-002 | V2 (tied with V3) | "None before the ruling" is clean and matches line 192; V1's optional level 1 still sends the INV-008 finding to troubleshoot (X-004). |
| C-003 | V1 | One session writing under one listed grant with the tool's head and parent guards is less error-prone than per-action hand writes. |
| C-004 | V2 | No toggle and no push by the tool, so there is no question of whether `--merge-guard off` also drops the PR-open read (`SKILL.md:309` vs `refs/merge-guard.md:94-97`). |
| X-001 | V3 | Only V3 stops a ruling-needing finding "before any fix"; V2 stops after the local fix, V1 depends on judgment. |
| X-002 | V1 | V1 is the only one that uses the project's standard review loop in full after the ruling. |
| X-003 | V1 (tied with V3) | Both keep one session in the checkout; V1 adds the tool's checkout guards, V2 needs an explicit two-actor hand-off. |
| X-004 | V3 (tied with V2) | Neither allows level 1 before the ruling, so neither lets troubleshoot design an INV-008 proposal. |
| A-002 | V3 | Only V3 does not need "no new git-configuration finding" to be true. |
| A-003 | V1 | Tool pushes keep the head guard and parent check that hand pushes lack, provided the PR-open read is confirmed under `--merge-guard off`. |

## Overall pick

Variant 3 now, because it is the only answer that meets lines 191 and 194 without depending on a session's judgment. Add the owner-memory PR-open check before each hand push and revisit the question once the Codex security thread is resolved and Codex has gone quiet.
