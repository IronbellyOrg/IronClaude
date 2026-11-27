## Position summary

C is the strongest foundation for data integrity: its versioned results, prepared journal, exact candidate validation, and explicit uncertainty make interrupted local commits reconcilable rather than merely repeatable. I advocate retaining those contracts while adopting B's host-visible commit execution and mechanically parsed opt-in, and A's more explicit migration inventory; C is not safe to implement unchanged.

## Steelman

### A

A offers the clearest implementation map. Its operation registry, extension checklist, safety-rule parity tests, explicit resume/last-task positions, and T-05 verification of unrelated staged entries turn a broad refactor into a maintainable, testable interface (FR-006–013, FR-057, T-05). Its strongest safety argument is that a read-only planner followed by visible Git writes preserves the host's existing permission checks, rather than replacing them with a new trust boundary (NFR-002). A also correctly removes merge despite the old example and explicitly inventories routing and packaging changes (D7, FR-015–017).

The strongest version of A is therefore not merely a simpler C: it is an integration-oriented design that makes existing enforcement visible and minimizes ambiguous agent decisions. Those are real advantages, even though its ledger changes and missing crash reconciliation create integrity gaps.

### B

B best explains the coupled invariants that made this work difficult: HEAD must remain fixed within a task, Q0 captures pre-existing changes, ledger parsing is closed, and installed components must actually ship their helper (RC-2, RC-3, RC-6). Its per-path `foreign-change` check and committed-tree comparison are concrete, executable checks rather than general assurances (FR-027, FR-020–021). Its sidecar avoids archive-parser churn, and its deferred pins preserve the evidence those checks require (FR-029).

B also identifies a decisive operational constraint: literal Git commands must remain visible to the launch-level guard (FR-016), and submodule commands remain denied in launched sessions (FR-037b). I independently re-read the guard and confirmed both facts. B's strongest argument is that new safety checks must compose with existing enforcement, not disappear inside a wrapper. That argument defeats C's current commit-execution design, even though B's merge operation violates the decided scope.

## Strengths claimed

1. **A proper operation-result contract, not success inferred from an exit code.** C FR-021 defines a versioned request, rejects unknown fields, and returns exactly `committed`, `already-committed`, `no-change`, `refused`, `failed`, or `uncertain`. Only the first three permit continuation. NFR-001 requires validation of parent, changed paths, and candidate contents. This separates an observed commit from an attempted one and makes timeout or unexpected hook history a first-class failure to establish the outcome.

2. **Prepared evidence and stable identity address duplicate commits after interruption.** C FR-022 requires a journal before the attempt and reconciliation before task selection and the all-complete shortcut. It checks expected parent and exact authorized changes, not just matching task names in a message. FR-034 injects failures at five interruption points and repeats resume twice to assert at most one commit per boundary key. B's recovery is useful but weaker; A has no equivalent reconciliation protocol.

3. **The specification admits the post-commit evidence problem.** C FR-023 says a terminal record written after a commit cannot be included in that same commit. It keeps that evidence staged without inventing another housekeeping commit and does not pretend the journal's reported commit contains its own result. This applies equally to A's post-commit ledger line and B's sidecar line, neither of which makes this lifecycle explicit.

4. **Task isolation means content isolation, not merely a filename allowlist.** C FR-017 refuses same-file pre-existing changes and changes outside the reviewed increment; FR-018 freezes repository identity, expected parent, paths, and contents. NFR-005 explicitly covers leading dashes, pathspec metacharacters, traversal, and symlink escapes. A's initial dirty-tree check is too coarse and can trust old ledger paths; B has a valuable Q0 comparison but lacks C's complete literal-path contract.

5. **Concurrency claims are appropriately limited.** C FR-014 requires every writer to join before the batch boundary; NFR-002 serializes cooperating helpers but explicitly states that a lock cannot prevent editors, hooks, or arbitrary Git processes from changing state. Revalidation remains necessary. This is stronger than equating a completed ledger with a quiescent worktree.

6. **Submodule inspection models independent facts instead of forcing one label.** C FR-024 reports pointer change, tracked dirt, untracked dirt, initialization, conflicts, and attachment independently, with null/unknown states and deterministic order. A's single closed state can obscure simultaneous pointer movement and dirt. C FR-028 further states that multiple repositories have no atomic transaction: report completed, untouched, and failed paths with old/new IDs, without resetting earlier successes.

7. **Authority is scoped to effects, including network effects.** C FR-010–012 distinguishes implementation approval, local commit authority, selected submodule update authority, and publication. FR-026 explicitly acknowledges initialization may fetch and rejects substituted remote identities. A's absolute no-remote requirement contradicts its initialization operation. B acknowledges fetching but gives less detail about approved remote identity.

8. **Cleanup discovery does not silently acquire publication authority.** C FR-029 distinguishes inspection from the existing archive operation, which writes to the evidence repository without `--apply`. Independent repository verification confirms this in `/home/coder/workspaces/worktrees/IronClaude/issue-326/src/superclaude/commands/worktrees.md`, especially its Usage and Options sections. C correctly routes the person rather than invoking cleanup or exposing its private deletion function.

## Weaknesses identified in the others

1. **A loses the distinction between a committed task and an empty task after a crash.** FR-061 writes the commit before `COMMIT: sha=`, but FR-060/R0 only replans the current changes. If the session stops between those writes, an empty tree becomes `COMMIT: none`, not a recovered commit. This is an audit-integrity failure even if no duplicate happens in that particular case (C-010).

2. **A introduces a new state grammar across multiple consumers unnecessarily.** FR-068–070 changes the ledger, archive parser, and STOP table. Its parity tests are genuinely useful, but B and C keep commit state outside the closed ledger grammar. A's persisted `COMMIT: on` also makes tasks completed during a later unflagged invocation eligible on a subsequent flagged resume (FR-056; X-006), violating the clearer per-invocation boundary.

3. **A's read-only helper placement weakens distribution completeness.** A places the helper in package CLI code while the plugin ships primitives from its plugin tree (S-008, C-020). Mirroring a skill is insufficient if its executable dependency is not available in plugin-only installations. B's skill-local script is the more complete distribution unit.

4. **A's hook handling does not prove the reviewed candidate was committed.** FR-064 distinguishes failures by exit and HEAD movement, but does not compare successful committed contents with a prepared candidate. FR-065 then includes hook rewrites on resume without explicitly requiring renewed review. B's tree verification and C's reviewed-candidate requirement are stronger (C-009, X-007).

5. **A cannot simultaneously promise no remote contact and initialize submodules.** NFR-001 forbids touching a remote; FR-041 initializes uninitialized modules. The diff analysis records the contradiction as X-015. The contract must acknowledge a possible clone/fetch and obtain appropriate scope, rather than make a false no-network guarantee.

6. **B retains an explicitly forbidden operation.** B FR-006/013 supports merge with preview and confirmation, and FR-002 preserves the merge example to avoid fixture churn. The seed Constraints explicitly say `/sc:git` never merges. A preview or extra confirmation cannot authorize expanding that decided scope; A and C correctly remove it (X-002).

7. **B overstates recovery and read-only behavior.** Its `recovered` classification checks parent and plan/task trailers, but the stated recovery predicate does not require an exact prepared candidate or a unique boundary generation (FR-021). Its private-index `add`/`write-tree` operations can write objects despite claiming to write nothing in the repository (FR-019; X-017). These checks are valuable, but their guarantees need narrower wording and stronger evidence.

8. **B's unpublished test is not proof of remote availability.** FR-035 refuses pointers absent from remote-tracking branches, but stale local refs can falsely imply publication after remote history changes. Conversely, safe local-only work is blocked even though publishing is outside scope. C's explicit unknown/not-ready report fits the local-only contract better; actual publication readiness remains with the publication workflow (A-004, X-014).

9. **B contains fixable but consequential contract inconsistencies.** FR-023 places preflight after ledger creation while promising no ledger writes (X-016). Its header regex permits more than its stated 72-character limit (X-018). Its assertion that S23 requires `--interactive` is contradicted by the diff's repository spot-check (X-003). These are not reasons to discard B, but precise interfaces cannot rely on its prose alone.

10. **Neither A nor B fully addresses accidental candidate drift and path ambiguity.** Both plan explicit path arguments, which is good, but neither specifies literal interpretation of all implementation `files=` entries. Neither resolves nonexistent/mistyped entries before a multi-path add. C improves literal handling but shares the missing nonexistent-path policy (C-021, A-001).

## Concessions

1. **X-008 is a release-blocking defect in C, not a stylistic preference.** FR-006/021 and NFR-002 imply a helper that executes the mutation while holding its lock. I independently read `/home/coder/workspaces/worktrees/IronClaude/issue-326/src/superclaude/hooks/scripts/launch-level-guard.sh`: its Git-word detection and COMMIT classification inspect submitted command text, and its level rules deny COMMIT below the permitted level. C cannot claim compatibility while concealing the actual commit inside its script. Adopt A/B's literal host-visible Git execution; preserve C's prepared/result contracts through explicit prepare and verify phases. How lock ownership spans those calls must be designed and tested, not assumed solved.

2. **X-001: C's session instruction is a valid kind of human authority but an underspecified switch.** The seed explicitly permits considering it, so it is not intrinsically out of scope. However, a narrowly parsed flag on the person's invocation is easier to validate and explain. C does not define same-invocation authority across later turns or compaction. I prefer B's person-origin check and per-invocation opt-in, augmented by C's quoted scope, revocation, and fresh-session rules. A stored flag or quotation must never manufacture authority.

3. **X-012: nested mutation is more scope and complexity than this delivery needs.** C supplies sensible parent-first initialization and deepest-first commit ordering, but nested discovery, selection, remote approval, and partial-failure cases multiply the safety surface. Prefer A's bounded initial mutation scope and an explicit unsupported nested-operation result; retain C's visibility into nesting where safely available. Do not perform recursive updates of unselected modules.

4. **X-013: C makes update needlessly weak.** Refusing every initialized checkout that differs from the recorded pointer means a common legitimate recorded-target update cannot run. B's clean ancestor-only rule is a better default: distinguish advancement from ahead/diverged work and refuse the latter. The selected recorded target and preservation checks should remain explicit.

5. **C is less implementation-ready in its interface and migration details.** The boundary trailer token, concrete schema, deadline values, message-file location, implement-side lazy ref, and STOP integration are left open. A provides a better registry, test matrix, and concrete routing/fixture inventory; B identifies classification-table maintenance. These should be incorporated before implementation rather than left to incidental edits (S-005/006/010, C-007/012/013/019).

6. **C's unchanged Q0 lifetime needs a stronger handoff contract.** It commits after task cleanup and says retry restoration is unchanged, but it does not specify precisely when reviewed candidate evidence survives deletion of the task pin. FR-017's initial snapshot is not by itself proof of the reviewed task increment. B's deferred pin deletion is useful until C's prepared journal contains all required verifiable evidence. No pending boundary may depend on an already-deleted reference (C-011).

7. **C's journal adds real state-management work.** Atomic persistence, schema validation, movement during archive, and lock conflicts need executable tests. Including a prepared journal in mandatory evidence also requires a non-self-referential digest definition: the candidate fingerprint cannot recursively include its own fingerprint. FR-023 narrows reconciliation exclusions but does not fully specify this construction. Stable identity must distinguish new task generations without allowing a changed candidate to masquerade as an old attempt.

8. **X-020 and X-021 require separating policy from observation.** The diff reports that configured commit hooks are not installed in this clone; C must not imply that leaving hooks enabled proves the message was checked. Validate required message structure independently and test with deliberately installed hooks. The diff also reports another tracked development-cache file despite all three variants' settings-only factual claim. Correct that claim without automatically relaxing the user's explicit prohibition on staging other development-runtime paths; legitimate conflicting work requires a user decision.

9. **C is incomplete on shared assumptions.** It lacks a nonexistent-path rule (A-001), explicit same-invocation authorization lifetime (A-003), and a real pre-commit-framework test with `--only` and unrelated unstaged changes (A-005). Its local locks and post-read verification cannot promise protection against arbitrary same-user writers or malicious trusted hooks; NFR-007 correctly limits that guarantee.

## Shared assumptions

- **A-001 — REJECT:** A ledger path is untrusted input; classify absent-both-before-and-after paths explicitly and refuse ambiguous or mistyped entries before staging anything.
- **A-002 — QUALIFY:** Current managed FINAL reads current delivery files, but preserve that reviewer input contract and verify the legacy whole-list route too.
- **A-003 — QUALIFY:** Bind authority to the same invocation across turns with explicit revocation rules; persisted evidence alone cannot authorize a new session.
- **A-004 — REJECT:** Remote-tracking refs are local observations, not fresh proof that another person can fetch the selected commit.
- **A-005 — QUALIFY:** Preserve edits as an acceptance requirement, but prove real framework stash/restore behavior under `--only`; plain-hook fixtures are insufficient.
- **A-006 — ACCEPT:** The diff found no test pinning the K3 wording; still run worker-contract regressions because behavioral requirements remain coupled.

## Per-point votes

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | HYBRID | 88 | C's compact contract plus A's navigation tables preserves operational detail without B's repeated evidence burden. |
| S-002 | B | 90 | Explicit resolution instructions are clearer than C's single-letter aliases or A's overloaded package alias. |
| S-003 | B | 94 | Falsifiable root causes explain which existing invariants the new behavior must preserve. |
| S-004 | C | 90 | Contiguous identifiers simplify traceability; test obligations remain legitimate requirements. |
| S-005 | HYBRID | 95 | A's test mapping plus C's interruption and integrity scenarios gives navigable, behavior-focused coverage. |
| S-006 | A | 92 | Acceptance-to-test mapping is easier to audit than shell-text checks or broad FR ranges. |
| S-007 | B | 87 | Root cause and residual columns expose what mitigation does not establish. |
| S-008 | HYBRID | 98 | B's distributed skill-local planner and visible writes, with C's versioned preparation/result contracts. |
| S-009 | A | 85 | Registry and operation-specific references provide the clearest extension seam; omit branch mutation content outside scope. |
| S-010 | B | 90 | A lazy commit-step reference clearly isolates executor behavior without overloading its main protocol. |
| S-011 | C | 97 | Prepared durable journal supports reconciliation without changing the ledger grammar. |
| S-012 | A | 85 | Explicit merge-removal and evidence-scope decisions surface important policy choices for review. |
| S-013 | C | 96 | Integrity, bounded execution, uncertainty, and honest concurrency limits directly address operational failure. |
| C-001 | C | 91 | Narrow operation scope avoids introducing extra branch mutations; merge remains forbidden. |
| C-002 | C | 85 | Preserve existing flags with restricted meanings instead of adding a message-source interface unnecessarily. |
| C-003 | HYBRID | 93 | B's person-origin enforcement plus C's repository, path, target, and effect scope. |
| C-004 | B | 96 | Runtime provenance validation is stronger than banning a flag string in selected primitives. |
| C-005 | HYBRID | 95 | A's named entry points plus C's cleanup, writer-join, and pending-journal barriers. |
| C-006 | HYBRID | 94 | A's before-ledger placement plus C's initial state capture avoids writes before preconditions pass. |
| C-007 | B | 87 | One explicit tested refusal code is sufficient; C defers a necessary consumer contract. |
| C-008 | HYBRID | 97 | B's executable Q0 comparison plus C's same-file overlap and reviewed-increment refusal. |
| C-009 | HYBRID | 98 | B's prepared-tree comparison plus C's exact-path validation and uncertain-outcome handling. |
| C-010 | C | 98 | Durable preparation and exact reconciliation preserve commit identity across the crash window. |
| C-011 | B | 94 | Retain pins until boundary evidence is durable; unchanged deletion timing risks losing required proof. |
| C-012 | HYBRID | 90 | A's explicit message schema plus C's stable boundary-key trailer; independently enforce length and required attribution. |
| C-013 | B | 92 | An external temporary message file avoids unintended evidence churn and accidental message-file inclusion. |
| C-014 | C | 97 | Independent state fields preserve simultaneous dirt and pointer changes; null states avoid fabricated cleanliness. |
| C-015 | C | 91 | Explicit target equality and detached-new-target preservation make the intended pointer unambiguous. |
| C-016 | C | 96 | Correctly distinguishes archive writes from inspection and preserves person-selected cleanup authority. |
| C-017 | C | 95 | Verified repository-specific policy is safer than assuming three branch names protect every installation. |
| C-018 | HYBRID | 91 | B's exact commands plus C's before/after state and refusal reasons; omit generic history-changing undo advice. |
| C-019 | HYBRID | 97 | A's merge-removal and routing migration plus B's exhaustive write-classification updates. |
| C-020 | HYBRID | 96 | B's mirrored skill-local helper plus C's version mismatch and missing-helper failure contract. |
| C-021 | C | 98 | Literal paths, traversal checks, and symlink containment protect the actual write set. |
| X-001 | HYBRID | 93 | B's person-origin invocation flag plus C's scoped evidence, revocation, and new-session reauthorization. |
| X-002 | HYBRID | 100 | A and C remove merge, as the seed explicitly requires. |
| X-003 | C | 90 | Retain clarification-only compatibility; reject B's false fixture rationale and forbidden merge example. |
| X-004 | HYBRID | 98 | B and C keep commit state outside the closed ledger and archive-parser grammars. |
| X-005 | C | 94 | Stage mandatory evidence, show its full scope, and stop on live-writer conflicts rather than silently absorbing it. |
| X-006 | HYBRID | 94 | B and C reject retroactive commits without an attempt initiated under valid authority. |
| X-007 | C | 97 | Hook-modified files require renewed review, not merely a newly flagged invocation. |
| X-008 | HYBRID | 100 | A/B visible Git writes are mandatory; retain C's journal and verification without hiding mutations. |
| X-009 | C | 87 | New branch mutations are unnecessary to the decided scope and enlarge operational risk. |
| X-010 | C | 87 | Default read-only status is safe and useful; unknown operations still stop. |
| X-011 | A | 96 | Uses the developer guide's documented front-matter vocabulary, unlike B's unsupported complexity value. |
| X-012 | HYBRID | 85 | A's bounded initial mutation scope plus C's explicit nesting visibility and selected-path containment. |
| X-013 | B | 93 | Clean ancestor-only advancement is useful while preserving ahead or diverged local work. |
| X-014 | C | 94 | Local pointer recording need not require publication; report readiness unknown and leave publication checks downstream. |
| X-015 | HYBRID | 98 | B acknowledges possible clone/fetch; C additionally scopes authority to approved remote identity. |
| X-016 | A | 98 | Preflight before ledger creation satisfies the promised no-write refusal behavior. |
| X-017 | A | 95 | Its allowlist avoids object-writing verbs; B's private index does not make object writes read-only. |
| X-018 | A | 95 | A's explicit total-header limit avoids B's demonstrably overlong regex acceptance. |
| X-019 | B | 96 | Distinguishes source package from managed task package instead of overloading the same alias. |
| X-020 | B | 95 | Separates configured hook policy from actual installation and independently validates message structure. |
| X-021 | NONE | 96 | All misstate tracked files; actual tracking does not automatically override the user's staging prohibition. |
| A-001 | NONE | 97 | None defines invalid or vanished ledger-path handling before a multi-path add. |
| A-002 | HYBRID | 91 | A/B/C boundary timing fits managed current-file FINAL; preserve that input contract and check legacy review too. |
| A-003 | NONE | 94 | None fully defines authority lifetime across later turns and compaction within one invocation. |
| A-004 | C | 94 | Readiness remains unknown from stale local refs; B's publication gate claims more than its evidence proves. |
| A-005 | NONE | 96 | None tests actual pre-commit stash/restore behavior with temporary-index commits and unrelated unstaged edits. |
| A-006 | HYBRID | 91 | A/B/C wording change has no identified exact-text pin, but worker-contract behavioral regressions remain necessary. |
