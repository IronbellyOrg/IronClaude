## Response to criticisms

C should not be implemented unchanged. My revised position is a hybrid: A's explicit integration map and bounded command surface; B's distributed planner, visible writes, and executable tree comparisons; C's prepared evidence, exact reconciliation, and honest failure states.

**Steelman first.** A's objection is not merely that C is complicated: C must fit existing permission checks, parser contracts, and installation surfaces. B's objection is not merely that local state is inconvenient: each promised safety property needs a check against evidence that actually survives a crash. Those objections are correct. Conversely, reducing the number of files does not remove the need to define prepared state, ownership, and recovery precisely.

1. **Hidden mutation defeats the guard — X-008, S-008. Concede without qualification.** C's original helper-executed commit is unacceptable. A and B are right that the actual add, commit, and ref writes must be literal, host-visible Git calls. Split preparation, agent execution, and verification. Internal helper reads are not individually gated; B's Round 2 E6 correctly narrows the claim. Implementation-side inspection ignores submodule contents and refuses gitlinks; person-requested submodule inspection has its separately disclosed trust boundary. Never switch execution context to escape a denial.

2. **An instruction is not a testable switch — X-001, C-003/004, A-003. Concede the underspecification, not the claim that chat can never convey authority.** The seed explicitly offered a session instruction as an option, and the worker contract explicitly recognizes scoped owner confirmation recorded from chat. B's Round 1 steelman acknowledges this. But a parsed person-origin invocation flag is clearer. Adopt it, checked once for the current run, with C's scoped evidence, revocation, and fresh-run rules. A flag is mechanically parseable; its human provenance remains a protocol check, not something an editable sidecar can prove.

3. **Certain migration/test failures omitted — C-019, S-005/006/010. Concede.** Incorporate A's routing-row and S23 migration, removal of the merge example and its stale classification row, plugin parity and legacy-command absence checks; incorporate B's one-row-per-new-write-pattern inventory. Add A's Round 2 discovery that the retry Ruling text currently says no commit follows it. Use a lazily loaded implement-side `refs/commit-step.md`. Give every behavior a named test and AC mapping in the merged spec; keep executable observations where meaningful. C's deferred filenames were acceptable for exploration, not sufficient for this final handoff.

4. **Necessary STOP contract deferred — C-007. Concede.** Adopt two explicit tested codes: `E-COMMIT-PRECONDITION` before commit-feature writes, and `E-COMMIT-REFUSED` at a prepared boundary. The latter stops before the next Q0, leaves the task complete, and records refusal/failure/uncertainty outside the ledger. Update the closed STOP sentence and every exact-text consumer. No implicit exception to the existing closed table.

5. **Nested mutation and multi-repository machinery exceed this delivery — X-012. Concede.** Initial mutation supports selected top-level registered modules only, never recursive update or nested content commits. Report nested state as unsupported/not inspected rather than silently claiming completeness. Retain per-selection old/new IDs and completed/untouched/failed reporting when several selected top-level updates partially succeed; that is an honest result, not an added transaction service. No rollback of earlier successes.

6. **C refuses the common recorded-target advancement — X-013. Concede.** Adopt B's clean ancestor-only update: an initialized HEAD may advance to the recorded gitlink only when ancestry is established locally. Ahead, diverged, dirty, conflicted, or unknown ancestry refuses. No remote-tip update, force, stash, or unselected recursion. Preserve C's approved-remote and exact-target revalidation.

7. **C removes advertised branch behavior — C-001, X-009. Changed view.** A's strongest evidence is the current command's explicit branch-management trigger, not merely a generic usage placeholder. That does not prove a precise create/switch API already existed, but retaining a bounded branch create/switch surface is reasonable for this refactor. Accept A's clean-tree, no-force, attached-state and protected-name guards. Cleanup remains routing only; no deletion implementation.

8. **Message source and compatibility flags — C-002, X-003. Concede.** A supplies a real missing contract: exactly one of a person's `--message` or `--smart-commit`, delivered through an external message file and `-F`. B's fixture rationale for `--interactive` was false, but C's clarification-only meaning still leaves an extra interface with little value. Accept dropping it and the forbidden merge example, with the changed interface documented. Preserve the supported smart-commit example.

9. **Protected policy has no discovery mechanism — C-017. Concede C's unspecified verification requirement.** A and B correctly distinguish local availability from ideal knowledge. Adopt a concrete conservative floor and a truthful unknown-default notice, not an imagined remote-policy query. See the six-point resolution. This explicitly accepts a residual for differently named shared branches; it does not claim local refs reproduce server rules.

10. **Live-writer evidence ownership cannot be detected — X-005. Concede the proposed detector and scope.** There is no general liveness oracle. Adopt A's split: stage all mandatory `.dev/tasks` evidence, commit only the expanded current package plus authorized product paths. Other packages remain staged, not committed. Within the current package, sole-writer operation and joined delegates remain preconditions; known ownership conflict stops. Do not infer exclusive access from an old timestamp. This preserves the always-staged rule without pretending it mandates committing every other package.

11. **Lock cannot span visible calls and can survive a crash — NFR-002. Partly concede.** A lock file could span processes, so the claim that no process can hold a lock is not a proof that serialization is impossible. Also, never deleting a lock merely because it is old is not the same as forbidding owner-confirmed cleanup: the existing managed archive has such a recovery rule. Nevertheless, a new lock protocol is unnecessary here. Drop C's extra lock, retain one executor per ledger/worktree as an explicit unsupported-concurrency boundary, join writers, and revalidate state. No claim of protection from arbitrary same-user writers.

12. **Journal directory/request schema are heavier than needed — S-011, FR-021/022. Concede the container, defend the information.** Accept one append-only sidecar, not a new journal directory. Use small fixed prepare/verify interfaces and a versioned output; no general request-envelope framework. But the prepared parent, exact paths, candidate identity, task generations, durable result, and malformed-state refusal remain necessary. A version field alone cannot substitute for validating the actual fields. A and B now explicitly accept prepared evidence, so this is mostly agreement.

13. **Q0 cleanup destroys required proof — C-011. Concede.** Preserve Q0/review evidence until boundary preparation has captured and pinned the necessary candidate, and amend both completion cleanup and resume row 1. A pending prepared boundary must not depend on references a later unflagged resume deletes. B's dedicated boundary pin is useful, but retain it through unresolved or uncertain outcomes, not just through success. A terminal attempt failure is not proof that boundary recovery no longer needs evidence.

14. **Self-reference and weak crash reconciliation — C-010, S-011. Concede the unresolved construction; strengthen the amendments.** B correctly identifies that A's whole-tree hash cannot include a line naming that same tree hash. C already warned about this in Round 1. B's exclusion of the sidecar helps, but comparing a committed sidecar with its *current* working copy fails once a resume appends a run line. The resolution below freezes the prepared sidecar independently of later appends and pins the final candidate outside the sidecar.

15. **Deadlines, trailer spelling, results and message validation left open — C-012/013, NFR-003. Concede.** Use `Implement-Boundary:` with plan/task/verdict trailers; independently enforce a 72-character subject and required session attribution. Use B's external temporary message file. Specify per-Git-read timeout of 10 seconds and per-mutation timeout of 120 seconds, bounded captured diagnostics, and no automatic retry after timeout. These are proposed acceptance limits, not measured hook compatibility. A timeout or signal requires read-back and yields `uncertain` until proved otherwise; never disable signing or hooks to meet the deadline.

16. **Configured hooks are not installed hooks; runtime-directory claims are false — X-020/021. Concede factual errors while preserving policy.** Follow B's separation of configured policy from observed installation. Validate messages independently and install hooks deliberately in fixtures. All three misstate which runtime files are tracked; an existing tracked cache does not waive the user's explicit staging ban. Automatic staging remains settings-only there, with scoped explicit authorization for that exception, and no force-add. Conflicts require a person, not a widened allowlist.

17. **Missing shared-assumption coverage — A-001/002/004/005/006. Concede missing rules/tests.** Refuse ambiguous or unrepresentable ledger paths before staging; skip a proven transient create-then-delete path only with evidence, never every absent typo. Preserve current-file FINAL inputs and test legacy as well as managed review. Local remote refs are not current remote proof. Run a real pinned pre-commit-framework fixture with `--only`, partial staging and unrelated unstaged edits; a plain shell hook is insufficient. Keep worker-contract regressions even where no exact K3 wording test exists. No tests or Git experiments were executed in this round.

## Updated assessment of A and B

### A

**Steelman.** A has become much more implementation-ready after accepting a skill-local helper, sidecar state, prepared evidence, per-path integrity checks, visible mutations, and no automatic retry. Its registry, parity tests and integration inventory are now useful scaffolding rather than a competing state machine.

**Arguments that changed my mind:**

- Existing branch-management wording supports retaining a narrow create/switch interface; C's categorical exclusion was unnecessarily disruptive.
- `--message` resolves an actual message-source hole in one turn. Keeping clarification-only `--interactive` is not worth preserving that ambiguity.
- Stage-all/commit-current-package is both narrower and more implementable than C's attempt to discover live owners of all evidence.
- A single sidecar can carry prepared and terminal evidence. C does not need a directory or an additional cooperating-helper lock.
- The concrete routing, fixture, and retry-Ruling inventory should be part of the requirements, not left to the implementation author.

**Arguments that did not change my mind:**

- A new flagged invocation typed *before* its Wave 0 prints a hook diff cannot logically prove that the person reviewed that later-displayed diff. C requires actual renewed review, not a temporal fiction. A protocol reviewer may review the changed candidate; a Ruling can accept a precisely explained gap, but neither is inferred from an earlier flag.
- A missing reviewed-tree header must not silently weaken candidate integrity to a pre-Q0 check. B's same-file check proves a different property. Without an accepted candidate snapshot, refuse the boundary, not the completed quality verdict.
- A's proposed 12-hex start-tree key is not a unique start generation. Content identity is not execution identity.
- A server rule does not necessarily stop a local commit on a differently named shared branch. Accepting the fallback is a stated limitation, not equivalent protection.

### B

**Steelman.** B gives the strongest operational corrections: prepared tree comparisons, durable pinning, no helper-hidden writes, no unnoticed submodule inspection in implementation, and explicit detection of hooks modifying hash-pinned plan/source evidence. B's Round 2 analysis improves the merged design substantially.

**Arguments that changed my mind:**

- E1/E2 establish the need for both a non-self-referential candidate definition and a reachable tree object through recovery. Adopt those requirements with the correction below.
- E4 means hook outcome verification must recompute plan/source byte hashes even when the Git commit succeeds. Changed pinned evidence is not a harmless formatter result.
- E6 means visible commit enforcement cannot be advertised as enforcement of every helper subprocess. Implementation inspection must avoid entering submodules.
- The absence of a downstream publication check removes C's claimed safety net. I change X-014 to a conservative local-ref eligibility gate, while explicitly rejecting its description as verified publication.
- B's bounded authority record is safer than storing a full inline prompt, which may contain secrets, newlines or misleading command text.

**Arguments that did not change my mind:**

- A last-fetch timestamp does not prove the selected remote-tracking ref was refreshed. It cannot repair the false-positive case after a remote rewrite. Report the observation as local, not current publication.
- Comparing the sidecar in a recovered commit with its current working copy is insufficient once the resume itself writes an `off`/`on` run record. Freeze and compare the prepared version instead.
- `refused` being a terminal attempt record must not make a hook-failed boundary permanently disappear. Distinguish attempt termination from boundary satisfaction.
- "Last compliant review" excludes valid non-compliant tasks completed under a scoped Ruling. The required snapshot is the latest reviewed-and-accepted candidate, including that path.

## New evidence

All paths in the following source citations are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-326/`. Repository checks were read-only. Logical counterexamples below are deductions, not executed tests.

1. **N1 — The start SHA is a tree, not a unique run generation.** `src/superclaude/skills/sc-implement-protocol/SKILL.md` defines Q0 by snapshotting content with `write-tree`; `refs/ledger.md` defines a start line as only task ID plus SHA and reuses it on resume. Two distinct starts with identical contents can have the same tree SHA, even before considering a 12-hex truncation collision. A/B's key therefore does not prove a new start occurrence differs. Bind the key to ledger identity, source identity, full task IDs and the ordinal of each actual start record, plus its full SHA; never invent a new start on resume.

2. **N2 — A/B's resume run-line order breaks B's sidecar success comparison.** Both Round 2 proposals append a run line before reconciliation. B's E1 then compares the sidecar blob in HEAD with the working-tree sidecar before appending the terminal line. On a crash after commit, the working copy already contains the *new run line*, which that prior commit could not include. The comparison necessarily fails even when the commit was exactly right. Compare against immutable prepared bytes/tree, not today's sidecar. Add this exact managed crash → unflagged resume scenario to acceptance tests.

3. **N3 — Accepted non-compliant tasks have no required last compliant review.** `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` explicitly preserves a non-compliant verdict on a post-Ruling complete line; `refs/qa.md` permits that completion after scoped user acceptance. A/B's latest-*compliant*-review condition can select no snapshot, or an obsolete one, for a legitimate task. Capture the exact candidate the reviewer inspected and the person accepted. Re-review if its bytes change, without changing the accepted verdict to compliant.

4. **N4 — Re-review may append another complete line without a new start.** The ledger's "Re-review complete line" section explicitly allows this after a defective saved-prompt FINAL recovery. Therefore a new complete line is not automatically a new boundary generation and must not trigger another product commit. Tie eligibility to start occurrence and existing satisfied boundary identity; later evidence remains staged unless separately authorized.

5. **N5 — Literal Git arguments do not fix the ledger's path encoding.** `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` defines `files=` as comma-separated repo-relative paths and expressly disallows commas in evidence paths. A real filename containing a comma is ambiguous before Git receives it. Do not widen the ledger grammar in this feature: refuse an unrepresentable/ambiguous touched path before staging, naming the encoding limitation. Also reject newline/control-character encodings that the line grammar cannot faithfully carry.

6. **N6 — Step 5 preflight cannot promise absolutely no earlier repository writes.** The currently read Wave 0 step 3 persists inline prompt `source.md` before step 5. A and B's preflight placement is right relative to ledger creation, but "before any write" is stronger than the existing intake order supports. State "before ledger creation, product edits, or commit-feature state writes; existing inline-source intake may already have occurred", or explicitly move commit-only identity checks ahead of intake. Do not claim to have changed ordinary unflagged intake by accident.

7. **N7 — No downstream publication gate is present in the checked implementation.** A targeted search of `src/superclaude/pr_submit/` for submodule/publication-related terms found only the conflict halt. This corroborates A/B's narrow claim about that package; it is not proof about every external user publication route. C must remove its assertion that the existing publication command checks availability.

8. **N8 — Refusal/pin cleanup needs an explicit distinction.** B deletes the boundary pin after a terminal line, but also declares candidate-change refusal terminal. A retry after hook review is still required by all three revised positions. If refusal means both "attempt ended" and "boundary settled forever", the resume either skips needed work or loses its prepared proof. Keep unsuccessful attempts auditable; retain needed pins while unresolved, and require an explicit reprepare under fresh authority/review for changed contents. Never retry an uncertain outcome.

## Proposed resolution for the six open points

### A-003 — Authorization lifetime

**Accept A's run-scoped flag and revocation proposal; accept B's bounded record, after-step-6 write, and informed-Ruling amendments. Reject treating a sidecar as independent human authority.**

The merged spec shall say:

1. Parse `--commit-tasks` only from the option prefix of the person's own `/sc:implement` invocation. Other origins refuse before commit-feature writes. Off by default; off under unattended execution. The static no-auto-insertion check is secondary to runtime provenance.
2. Check provenance once for this run. After preflight and ledger opening, record a bounded option/source identity, repository/worktree identity, monotonically increasing run number and on/off state. Never store a full inline prompt or credential-bearing text. A run without opt-in and without existing commit state creates no sidecar.
3. That grant covers continuation turns and compaction of the same active run. It expires at run stop, new invocation or new session; resume always runs Wave 0 and requires fresh opt-in for mutations. A stored `on` is evidence only; helper state validation is necessary, not proof of personhood.
4. A plain-language revocation takes effect before the next attempt. A Ruling neither grants nor renews commit authority. When authority is still active, explain the commit consequence before asking for acceptance.
5. Reconciliation of an already-created commit does not require commit authority, but writing recovery evidence is still an evidence write, not a read-only operation. Do not run add/commit merely to reconcile. An unflagged resume may record and stage recovery evidence under the normal evidence rule.
6. Show pending boundary identities and intended paths. For a changed/re-written candidate, obtain actual renewed review *after* showing the changes; the already-typed flag alone is insufficient. Test later-turn Rulings, compaction, revocation, unflagged resume, stale run records and fresh-session default-off.

### C-010 — Crash between commit and record

**Accept A's prepared-before-add structure, strict expected parent and fail-closed HEAD-only recovery. Accept B's non-self-reference, pinning and pinned-file checks. Reject their start-SHA-only key and current-sidecar recovery comparison.**

The merged spec shall say:

1. Boundary identity is SHA-256 over a canonical tuple of repository/worktree identity, stable ledger/source identity, ordered full task IDs, and each task's start-record ordinal plus full start SHA. Persist that binding; resume reuses it. Repeated complete lines for the same start do not create new boundaries. Hash prefixes are display-only.
2. Prepare while task proof still exists. Validate no pre-Q0 product delta and equality with the latest reviewed-and-accepted candidate. Expand the exact commit set to literal files; include authorized deletions and both rename endpoints. Reject ambiguous/missing proof, absent typos and encoding limitations. An unchanged transient deleted file may be skipped only when its lifecycle is established.
3. Compute a tree from the expected parent plus selected contents **excluding only the sidecar**. Durably append a prepared record with that tree ID, exact selected paths, expected parent, boundary identity, source/plan hashes and attempt number. No user-index/ref/working-tree mutation by a helper is hidden in this claim; sidecar persistence and object creation are disclosed effects.
4. After that prepared append, build the **full final candidate tree**, including the frozen prepared sidecar bytes for managed runs. Have the agent visibly pin this full tree under the boundary identity before add/commit. The sidecar never names this full tree's own hash, so there is no self-reference. The deterministic ref points to it externally. Its sidecar blob freezes the prepared bytes even if future run/result records are appended to disk. If interruption leaves a prepared record without its required pin, return `uncertain`; never infer permission to commit from incomplete preparation.
5. The visible commit carries `Implement-Boundary:` plus plan and ordered task/verdict trailers. Verify exactly one parent equals the prepared parent, the full committed tree equals the pinned final candidate, changed paths equal the authorized changed subset, the key matches, and managed plan/source hashes still match. No exclusion of arbitrary evidence changes. Legacy sidecar stays outside the commit set.
6. Reconcile before task selection, all-complete return, or archive short-circuit. HEAD exactly proves success → `already-committed` and append recovered evidence. HEAD still equals parent → pending; an authorized attempt may proceed only with unchanged validated inputs. Changed candidate requires renewed review and a new prepared attempt under the same unsatisfied boundary. Other history, absent proof, duplicate/conflicting evidence or uncertain effects → stop, no retry or repair. Inspecting only HEAD is conservative: a person's later commit produces uncertainty, not a history search or duplicate.
7. Stage terminal evidence without a housekeeping commit. Preserve a boundary pin through pending/uncertain state; delete only after verified committed/recovered/no-change satisfaction, or explicit owner-resolved abandonment. Failed attempt versus satisfied boundary are distinct. Tests include C's five crash points, two resumes, unflagged managed recovery with a new run line, pin loss/GC, changed hooks, pinned plan/source changes and repeated complete lines.

This is a small extension of B's pin: point it at the final frozen candidate, rather than relying on a live sidecar to reconstruct prepared bytes. It adds no journal directory or daemon.

### C-015 — Pointer commit eligibility

**Accept A's clean/registered/one-level/exact-path checks and B's inspection-boundary clarifications. Accept detached-at-referenced-target behavior; reject C's unconditional attached-branch requirement. Add C's exact target binding.**

The merged spec shall say:

- Only explicitly selected top-level registered gitlinks, with initialized clean indexes/worktrees, no conflicts, and an exact full target object ID captured in the authorized plan. Revalidate that module HEAD still equals that target immediately before and after parent commit.
- A detached HEAD at a target contained in a local remote-tracking branch is eligible; no invented preservation branch is needed. A detached target contained in no local or remote-tracking branch refuses `detached-new-commits`. An attached but non-remote-contained target refuses the conservative X-014 check below.
- Parent preconditions, literal isolated path set, hook verification and normal message rules apply. Commit only the selected gitlink changes, no `.gitmodules`/config change and no inner dirty content. Existing mandatory evidence staging remains separate.
- Multiple selected pointer targets in the same parent may use one authorized parent commit with its explicit set; no nested traversal or inner-repository content commit is implied. A zero pointer delta is `no-change`.
- Helper inspections do not bypass a denied operation. Report that direct `git submodule` calls are denied in launched sessions and that helper subprocess reads are not separately gated. No workaround for a denied mutation.

### C-017 — Other repositories' protected branches

**Accept A's practical fallback and B's additive-default correction. Reject C's unresolved-policy blanket block as insufficiently operationalized.**

The merged spec shall say:

- Always refuse local-history mutation on detached HEAD and on `master`, `main`, `integration`, plus any locally resolved `origin/HEAD` target. Resolve per actual target repository, including a module when operating inside it. Never remove a fixed name because the local default differs.
- Incorporate additional protected names explicitly established by the current repository's verified instructions or a scoped person-confirmed policy; report the source. No remote query or parent-repository inference.
- If `origin/HEAD` is absent, show `default unknown` and the enforced names, then allow an otherwise authorized local operation. If instructions conflict or explicitly protect the target, refuse; missing discovery is not permission to override known policy.
- Do not state that fetch always creates or never creates this ref; B correctly identifies version/config differences. A local default ref may also be stale. Do not present server protection as protection against local commits. Differently named unknown shared branches are an accepted, visible residual.

### S-011 — Commit-state location and grammar

**Accept A/B's single sidecar locations, unchanged ledger/archive grammar, lazy ref and post-commit evidence lifecycle. Accept B's boundary-pin exception to resume cleanup. Reject current-working-sidecar comparisons and deletion of unresolved proof.**

The merged spec shall say:

- Use `commits.md`: managed `<package>/artifacts/commits.md`; legacy `<run>/commits.md`, unstaged like legacy evidence. Preserve state through archive movement by stable package identity, not an absolute old package path.
- Document versioned `run`, `prepared` and `result` record forms once, with bounded, unambiguous escaping for option/source/path data. The parser rejects unknown versions, malformed records and truncated tails; no silent repair. One writer, flushed durable appends before side effects. Record attempt number separately from stable boundary identity.
- Preparation stores exact paths and immutable candidate binding as C-010 specifies. Terminal result fields are outside their own commit; keep managed evidence staged and report final outstanding evidence honestly. A later run line is not part of an earlier prepared candidate.
- `committed`, `already-committed`, `no-change` satisfy a boundary. `refused`, `failed`, `uncertain` end an attempt and stop advancement; they do not implicitly erase eligibility or permit retry. Uncertainty requires resolution. An unchanged-input retry still needs active authority; changed contents need renewed review and preparation.
- Q0/review refs survive until required proof has been durably transferred; pending boundary refs survive ordinary complete-task cleanup even on unflagged resume. No new lock, directory or ledger record. Ref/helper schema, atomicity, corrupt-tail, archive, and pin-cleanup tests are required.

### X-014 — Target absent from remote-tracking branches

**Change my vote: accept A/B's conservative refusal, reject their description of containment or FETCH_HEAD time as proof of publication. Reject C's reliance on an existing downstream availability gate.**

The merged spec shall say:

- A selected pointer target must be contained in at least one local remote-tracking branch of that module, otherwise refuse `submodule-unpublished` and make no parent pointer commit. No override is added here. This is a conservative *local-ref eligibility condition*, not verified publication.
- Print matching local ref names and, if available, FETCH_HEAD file modification time labelled exactly as a local fetch-file observation. Do not say every displayed ref was fetched then, that every absent ref is genuinely unpublished, or that a contained commit is still downloadable remotely.
- No automatic push/fetch, including to remedy the refusal. Any separate person-performed publication/fetch remains subject to repository permission and remote-identity policy; do not promise the person can push a third-party module.
- State both residuals: stale refs can falsely refuse a locally safe target, and remote rewrite/deletion can falsely suggest availability. The current publication workflow has no checked module-availability gate; adding one is out of scope. The local gate reduces a common failure without claiming to eliminate it.

## Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | HYBRID | 88 | C's compact contracts with A's navigation tables; retain essential evidence without B's repetition. |
| S-002 | B | 94 | Explicit alias resolution prevents A's package ambiguity and C's opaque single letters. |
| S-003 | HYBRID | 94 | A's verified baseline plus B's falsifiable root causes explains facts and preservation obligations. |
| S-004 | C | 82 | Contiguous identifiers simplify final traceability; renumber once after merging. |
| S-005 | HYBRID | 98 | A's named test matrix, B's existing-consumer inventory, C's fault injection and integrity assertions. |
| S-006 | HYBRID | 94 | A's acceptance-to-test mapping plus B's runnable observations; behavior tests outrank text counts. |
| S-007 | B | 90 | Root cause and residual columns distinguish mitigation from proof. |
| S-008 | HYBRID | 99 | B's mirrored planner and visible execution, A's shared constants, C's versioned results and durable preparation. |
| S-009 | HYBRID | 91 | A's registry and safety reference, B's lazy read-path loading. |
| S-010 | B | 96 | Dedicated lazy commit-step reference makes implementation integration concrete. |
| S-011 | HYBRID | 98 | B's sidecar, C's prepared evidence, A's unchanged-parser discipline; freeze sidecar bytes and retain unresolved pins. |
| S-012 | A | 91 | Merge-removal and explicit evidence-scope decisions prevent silent scope drift. |
| S-013 | HYBRID | 98 | C's integrity and uncertainty, A's parity/version rules, B's bounded distribution and execution budgets. |
| C-001 | A | 90 | Retain advertised branch management with tight guards; remove forbidden publication and merge; add bounded submodule operations. |
| C-002 | A | 92 | Explicit message or smart drafting closes the message-source gap; remove ambiguous interactive compatibility. |
| C-003 | HYBRID | 96 | B's person-origin refusal plus C's repository, path and target scope; no replayable unauthorized write plan. |
| C-004 | HYBRID | 96 | B's provenance check once per run, A's static anti-insertion check; neither sidecar nor flag proves personhood. |
| C-005 | HYBRID | 99 | A's named resume/last-task positions plus C's writer barrier and pre-short-circuit reconciliation. |
| C-006 | HYBRID | 95 | A's before-ledger preflight plus C's state capture; acknowledge existing inline-source intake writes. |
| C-007 | A | 95 | Two explicit STOP codes preserve precondition versus boundary effects; update all closed-table consumers. |
| C-008 | HYBRID | 99 | B's Q0 comparison plus C's reviewed-and-accepted candidate equality; no missing-proof fallback. |
| C-009 | HYBRID | 99 | B's frozen-tree comparison plus C's exact scope, pinned-evidence checks and uncertainty classification. |
| C-010 | HYBRID | 99 | C's stable prepared boundary and fault tests, B's pinned candidate, A's strict parent recovery; correct sidecar comparison. |
| C-011 | B | 97 | Defer cleanup until durable proof transfer; unresolved boundary pins survive unflagged resumes. |
| C-012 | HYBRID | 97 | A's validated subject/verdict schema, B's plan trailer, C's full boundary identity and attribution preservation. |
| C-013 | B | 97 | External temporary message file avoids accidental evidence inclusion. |
| C-014 | HYBRID | 97 | C's independent nullable facts plus A's explicitly derived action-state precedence. |
| C-015 | HYBRID | 93 | B's clean referenced target, C's exact gitlink binding, A's isolated top-level parent commit. |
| C-016 | C | 98 | Person-selected cleanup route correctly distinguishes archive writes from inspection. |
| C-017 | HYBRID | 90 | A/B conservative floor and additive local default, C's repository-policy sources and truthful limitations. |
| C-018 | HYBRID | 96 | B's commands and preconditions, C's before/after effects; no automatic or blanket history-changing undo advice. |
| C-019 | HYBRID | 99 | A's routing/fixture migration, B's write classifications, C's regression boundaries; include retry-Ruling correction. |
| C-020 | HYBRID | 98 | B's mirrored skill-local distribution plus C's missing/version-mismatch refusal without installation fallback. |
| C-021 | C | 99 | Literal path containment is essential; separately refuse ledger-unrepresentable names. |
| X-001 | HYBRID | 97 | A/B parsed flag and person provenance, C's scope, revocation and fresh-run authority limits. |
| X-002 | HYBRID | 100 | A/C remove merge; the seed explicitly forbids it. |
| X-003 | A | 92 | Remove interactive and merge example; false fixture rationale cannot justify preserving an unnecessary interface. |
| X-004 | HYBRID | 99 | B/C external commit state preserves ledger and archive-parser contracts. |
| X-005 | A | 96 | Stage all mandatory evidence; commit current package and authorized paths only, avoiding other packages without a liveness oracle. |
| X-006 | HYBRID | 98 | B/C prohibit retroactive unflagged-task commits; only an authorized boundary generation is eligible. |
| X-007 | C | 99 | Changed hook contents need actual renewed review after disclosure, not merely an earlier flagged invocation. |
| X-008 | HYBRID | 100 | A/B visible Git mutations preserve guard enforcement; C's preparation and verification remain separate. |
| X-009 | A | 90 | Preserve advertised branch management through clean-tree and no-force guarded create/switch operations. |
| X-010 | C | 95 | Bare invocation defaults to read-only status; unknown operations still stop. |
| X-011 | A | 96 | Developer-guide vocabulary meets the explicit seed criterion; practice drift is separate. |
| X-012 | HYBRID | 95 | A's top-level-only mutation plus C's explicit unsupported nesting and selected-path containment. |
| X-013 | B | 98 | Clean ancestor-only recorded-target advancement preserves ahead/diverged work and supports the common update. |
| X-014 | HYBRID | 91 | B's conservative containment gate, C's honest stale-ref limitations; no claim of fresh remote availability. |
| X-015 | HYBRID | 97 | B/C disclose clone/fetch effects; A's concrete URL comparison supports C's approved-identity scope. |
| X-016 | A | 98 | Preflight precedes ledger creation; qualify absolute no-write claims for existing inline intake. |
| X-017 | HYBRID | 98 | B's private-index comparison is useful; C's honest effects distinguish object/evidence writes from visible repository mutations. |
| X-018 | A | 99 | Check total subject length directly; B's regex tail bound violates its own limit. |
| X-019 | B | 98 | Distinct source-package and task-package aliases avoid incorrect destinations. |
| X-020 | B | 98 | Configured hooks are not installed enforcement; independently validate and test deliberately installed fixtures. |
| X-021 | NONE | 99 | All misstate tracking; preserve explicit staging policy rather than infer authorization from tracked caches. |
| A-001 | NONE | 99 | None originally defines safe absent-path policy; refuse typos, skip only proven transient deletions. |
| A-002 | HYBRID | 95 | A/B/C current-file final review remains valid; pin both legacy and managed reviewer inputs in regressions. |
| A-003 | HYBRID | 97 | A's run lifetime, B's bounded provenance record, C's revocation and fresh-session rule; stored records cannot manufacture authority. |
| A-004 | C | 98 | Local refs and fetch-file timestamps cannot establish current remote availability, even with a conservative eligibility gate. |
| A-005 | NONE | 99 | No original fixture exercises real pre-commit stash/restore with partial staging and temporary-index commits. |
| A-006 | HYBRID | 94 | A/B/C identify no exact K3 text pin; behavioral worker-contract regressions still apply. |
