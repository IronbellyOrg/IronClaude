# Round 2 — Advocate C (backend)

## Responses to criticisms

1. **No concrete launch argv or operator contract (A/B/D round 1). CONCEDED.** C's prose acceptance criteria are testable, but leave adapter behavior unspecified. Adopt A's fixed-agent argv, B's executable/origin checks and assumed-shape fixtures, and D's exit-action table, disable control, inspection, and rollout runbook. Add one configuration schema and numbered decisions. Syntax precision is independent of storage choice.

2. **SQLite, transition table, and initialization are heavy (A/B/E round 1; A/B round 2). PARTLY CONCEDED.** SQLite is unnecessary. One locked, versioned JSON document can atomically contain consumed keys and transition history. However, A/B's existing helper does not alone prove restart durability; see E1. Initialization remains a deliberate mutation, not an incidental effect of `check-config`. A validator that recreates lost state defeats the loss protection we agreed to preserve.

3. **Permanent suppression without recovery (A round 1). CONCEDED on operator support, not the invariant.** Status and the runbook must identify suppressed/unknown issues and explain investigation of the existing operation. A new submission after a consumed slot is a guarantee reset, not normal recovery. A/B's proposed `reset` must not be described as preserving lifetime at-most-once. Defer that mutating verb rather than ship an underspecified reset.

4. **Opaque IDs make setup harder; no lookup procedure (A/D round 1). CONCEDED.** Require reviewed setup instructions resolving display names into IDs, and show bindings in status. No lookup verb is necessary. Retain identity binding: deleting/recreating a label or Status option under the same name can satisfy name equality with a different policy object. A/B's claim that name changes only fail closed overlooks replacement under the old name. Owner/approver IDs also prevent trust following recycled names. Adapter support remains unverified until the controlled test.

5. **Bounded marker content weakens minimization (A/B/D round 1; A round 2). CONCEDED as an implementation choice.** Project marker recognition inside `gh` to booleans and author IDs; do not retain narrative in Python. This does not mean no component reads comments: gh must inspect bodies to recognize the marker. D3 restricts prompt content, not that inspection. Positive markers need authenticated-author matching; incomplete absence must never permit fresh submission.

6. **Full Project pagination costs grow with Project size; no hard request cap (E round 1). PARTLY CONCEDED.** C requires complete evidence but does not mandate whole-Project scans. Nevertheless it leaves query strategy and request ceiling unspecified. Adopt E's issue-local membership lookup and hard budget, with B's page accounting. A projectItems connection can itself paginate; unfinished reads cannot establish approval. Refresh requests count too.

7. **D's counters/JSON equal C's invariant (A/B round 2). ONLY WITH A CORRECTION.** Original D increments `launches` after a success/recognized-unknown reply. A generic error before that increment remains retryable. Increment the durable consumed-submission counter before invoking Orca. A/B still propose retryable `failed` after a “definite error”; error text is not a verified guarantee that no session started. Until the live API contract establishes otherwise, every submitted slot stays consumed.

8. **Final-refresh ordering (A/B round 2). AGREE WITH B'S DIRECTION.** Refresh first, persist launch intent, invoke Orca; canceled preflight need not create/delete an entry. Extend B's refresh beyond labels and Status: approval provenance, owner identity, Project membership, and marker evidence matter. State the unavoidable refresh-to-launch race. Never delete an existing consumed key on failed revalidation.

9. **Operational omissions (D round 1). CONCEDED.** Adopt the XDG default, disabled-by-default configuration, local-filesystem locking, kill switch, shadow rollout, and staleness signals. Neither `enabled=false` nor audited host names enforce one authority across machines; they reduce accidental activation and improve diagnosis only.

## Changed views

- **A:** Its trimmed seams are adequate; routing registries and future backends are unnecessary. Accept its JSON configuration and concrete launch contract, but reject mutation through `check-config` and unqualified resets.
- **B:** Complete evidence and executable checks are foundational. Its refresh-before-write ordering is simpler than C's reservation wording. B correctly corrects A: unassigned issues can pass the claim, so watcher preassignment is stricter policy.
- **D:** Its runbook, stop switch, and exit-action mapping are the operational base. Its reply-based counter is not the safety base; consume before submission. Repeated lock losses must not count as healthy work merely because they emit current audit lines.
- **E:** Candidate-scaled reads and request budgets replace vague cost accounting. Six-per-day is a proposed availability/spend policy, not an evidenced requirement. Terminal-key pruning remains unacceptable; daily limits cannot protect against whole-ledger loss if their counters disappear too.
- **C:** I no longer prefer SQLite specifically (S-005). I retain durable identity and consumed-slot semantics; JSON is acceptable if it meets the complete durability contract.

## New evidence

All checks used Read only; no tests, CLI probes, network requests, or live sessions ran. These source facts do not validate API response shapes.

- **E1 — Atomic replacement is not the complete durability contract.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/swarm/atomic.py`, `write_prepared_bytes`, fsyncs the temporary file and calls `os.replace`, but contains no parent-directory fsync. It is useful reuse, not proof that the replaced directory entry survives host/storage failure. State the crash boundary and verify required filesystem durability rather than infer it from the helper's name.
- **E2 — The Orca probe bypasses the proposed injected runner.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/install_user_setup.py`, `_find_orca`, directly calls `shutil.which` and `subprocess.run` with a ten-second timeout. Reusing it unchanged while asserting every effect goes through `Runner` is inconsistent. Mock that boundary explicitly or adapt the probe behind the runner; include probe time in the cycle budget.
- **E3 — Authorized claim effects include ClickUp.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/skills/sc-issue-protocol/refs/claim.md` assigns GitHub in Wave 3 and invokes `clickup_claim.py`; later waves write local artifacts and GitHub comments. Risk acceptance must enumerate the existing claim effects, not call it only “read-and-assign” or authorize GitHub writes alone. The same file permits unassigned issues and posts the marker in Wave 6.
- **E4 — Pagination precedent also rejects repeated IDs.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`, `fetch_rest`, uses bounded pages and rejects repeated IDs, including a server ignoring page numbers. Carry that progress check into event/comment reads. Its GraphQL thread reader also demonstrates why read-only cannot mean every request uses GET.

## Updated positions

All 28 UNRESOLVED points are covered. Requirement texts below are at most 45 words each. AGREE accepts that advocate's round-2 ruling for the point, except where this table explicitly replaces or qualifies it.

| Point | Superior variant (letter/HYBRID/NONE) | Confidence % | Merged ruling or AGREE with X |
|---|---|---|---|
| C-001 | HYBRID | 94 | Configure trigger and approval labels by approved immutable IDs, with proposed display names `issue-watch:trigger` and `issue-watch:approved`. Setup resolves and displays bindings; missing or replaced IDs fail closed. Name equality alone never rebinds policy. The poller never creates labels. |
| C-004 | C | 97 | Intended owner requires exactly one assignee whose account ID equals the authenticated, configured authority account. Retain current login for claim compatibility. Unassigned and foreign/multiple assignees receive explicit skip reasons. Preassignment is stricter than the claim and must be documented. |
| C-005 | HYBRID | 97 | Default disabled. Nominate one active authority and persistent ledger per repository/account; independent authorities are unsupported. Audit account ID, current login, authority ID, and host. Local configuration and host auditing do not provide distributed exclusion. |
| C-006 | HYBRID | 94 | AGREE with B; additionally, every Project connection page and final-refresh request counts toward the same budget. |
| C-007 | HYBRID | 99 | Persist states, stable repository/issue IDs, attempts, consumed submissions, approval actor/event IDs, operation ID, invocation context, timestamps, and reason. Increment consumed submissions durably before Orca invocation; fresh submission requires zero. Label changes, expiry, login changes, and reapproval never reset it. |
| C-008 | HYBRID | 92 | Proposed defaults: ten candidates, one fresh submission per cycle and issue, three safe pre-submission attempts, 60-minute reporting threshold, 35 GitHub calls, 20-second GitHub and 120-second Orca deadlines within 240 seconds. Six submissions per rolling day requires owner approval and durable accounting. |
| C-009 | HYBRID | 98 | Under the cycle lock, refresh all eligibility evidence immediately before committing consumed launch intent; stale or unreadable evidence skips without consuming a slot. Commit before invoking Orca. Preserve existing consumed keys. Eligibility is established only at the last completed refresh, not atomically with launch. |
| C-010 | HYBRID | 96 | AGREE with A on literal argv, fixed agent, existing absolute worktree, and origin validation. Probe executable identity through a mockable boundary; account for probe calls and deadlines. |
| C-011 | C | 99 | Timeout, malformed output, interrupted invocation, or unverified error becomes unknown with its slot consumed. Reconcile a known operation only through its stored operation ID and invocation context. Missing ID requires investigation. Expiry and explicit post-submission failure never authorize a fresh launch. |
| C-012 | HYBRID | 98 | AGREE with A. |
| C-013 | HYBRID | 95 | Trusted operator configuration admits human approvers by account ID after role verification. Reject missing/empty lists and unsafe ownership or write permissions, including writable parent paths. Display governance and update procedure. The template never silently supplies approval authority. |
| C-014 | HYBRID | 98 | Disable deployment until an owner-run test verifies slash-command execution and session permission policy, and the owner explicitly accepts live narrative-read risk and existing claim effects, including GitHub, local artifacts, and conditional ClickUp assignment. Bypass permissions require explicit written acceptance. |
| C-015 | HYBRID | 97 | Shared authentication, authorization, discovery, configuration, storage, or rate-limit failures halt further dispatch. Candidate-local unreadable or incomplete evidence skips that candidate. Preserve prior committed outcomes; do not promise retroactive zero launches. Report partial failure distinctly from a clean cycle. |
| C-018 | HYBRID | 96 | AGREE with A on lock, kill switch, and exit 75. Track last completed cycle separately from overlap audit timestamps; repeated overlaps must remain unhealthy. |
| C-020 | HYBRID | 96 | Provide `once --dry-run`, offline `status --json`, read-only `check-config`, and explicit `init-state`. Initialization is operator-controlled, never automatic during validation or polling. Status/runbook describe consumed-slot investigation. Defer reset; any later reset must explicitly acknowledge forfeiting the previous at-most-once guarantee. |
| C-023 | HYBRID | 94 | AGREE with A; add actual Orca reply/reconciliation validation, restart/restore and lock verification, Project ID/query compatibility, and account/approval governance before activation. |
| C-024 | HYBRID | 97 | Recognize the existing marker only with authenticated author-ID matching; project body inspection inside gh to structured evidence. Positive recognized evidence establishes posted claim, not artifact completion. Incomplete absence cannot permit dispatch. Assignment alone proves no claim; marker recognition never resets consumed keys. |
| S-001 | HYBRID | 96 | AGREE with A. |
| S-004 | HYBRID | 92 | Use A's trimmed module separation and mockable runner/store/launch boundaries; reuse existing helpers only where their effect and durability contracts fit. No routing registry, interchangeable backends, or audit plugin surface is required. Do not name a module `select`. |
| S-005 | HYBRID | 96 | Use one locked, versioned JSON document containing consumed keys and transitions. Persist via same-directory replacement with file and parent-directory durability verified on supported storage. Polling never initializes missing storage. Corrupt/incompatible state fails closed; initialization and restore require explicit operator procedures. |
| S-007 | HYBRID | 95 | AGREE with A; distinguish source-verified facts, proposed policies, and externally unverified adapter contracts. |
| S-008 | HYBRID | 94 | AGREE with A. |
| X-001 | HYBRID | 99 | Confirmed launch never permits another fresh submission. Missing claim evidence after the reporting threshold raises `claim_not_observed` without releasing the consumed slot. A later recognized marker may still establish claimed; threshold expiry is not proof the session stopped. |
| X-002 | C | 99 | A recovered record with committed consumed launch intent and no stored outcome becomes unknown; never submit fresh. Only unconsumed preflight work may retry. Absence of a marker or operation ID does not prove non-start. |
| X-003 | HYBRID | 99 | AGREE with A; storage loss and incompatible schema also fail closed. |
| X-005 | HYBRID | 98 | AGREE with A. |
| X-007 | HYBRID | 94 | AGREE with A's exit mapping and action table. Unknown launch or storage-integrity failure outranks ordinary transient errors; terminal output preserves all reasons. A partial cycle is never reported as clean success. |
| X-008 | HYBRID | 98 | AGREE with A; marker projection includes trusted author identity, not narrative content. |

**Already-agreed points needing precision:** C-003 retains issue-local Project reads plus configured Project/field/option IDs; C-016/X-006 persist server retry timing and stop further requests without erasing earlier outcomes. C-025 permits body inspection inside gh only for marker recognition. No request cap, record pruning, or rate-limit rule may discard consumed keys.

## Shared-assumption changes

- **A-001 — QUALIFY, strengthened:** JSON is acceptable; persistence remains an external activation prerequisite, not something path validation proves. `once` and `check-config` never recreate the store. Whole-directory loss, cloned backups, and operator reinitialization remain guarantee hazards; a sentinel in the lost directory cannot detect them.
- **A-003 — REJECT, refined:** Separate identity from current display names. Pin owner/approver IDs and policy-object IDs; show readable bindings during setup/status. Name replacement can authorize a new object, not merely cause a harmless mismatch.
- **A-005 — QUALIFY, clarified after A/B disagreement:** Sole-assignee routing is stricter than the claim, which permits unassigned issues. Assignment is required at eligibility evaluation, not chronologically before approval. Document the human assignment step and audit `unassigned` skips.
- **A-007 — QUALIFY, made concrete:** Verify cross-process locking and replacement durability on supported persistent local storage. Existing helper reuse is insufficient evidence for host-failure durability; no cross-host exclusion follows.
- **A-010 — QUALIFY, hardened:** Trusted administrators may govern approval configuration; protection includes parent-directory replacement permissions, not just file mode. Updating authority is an explicit administrative action, never issue-controlled input.

A-002, A-004, A-006, A-008, and A-009 retain round-1 positions. Actor metadata proves application identity rather than human intent, and no marker-duration or clock assumption may reopen a consumed slot.
