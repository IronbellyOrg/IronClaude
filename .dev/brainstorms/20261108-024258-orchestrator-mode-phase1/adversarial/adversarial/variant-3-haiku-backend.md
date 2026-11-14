# Orchestrator Mode Phase 1 Requirements

Variant: 3
Model label: haiku
Discipline: backend
Status: proposed requirements, not implementation

## Problem and scope

A coordinator needs one local view of workers, ordinary sessions and child worktrees.
The report must answer who needs a person, what is still working and what needs inspection.
Safety takes precedence over completeness, which takes precedence over convenience.
Phase 1 observes one feature worktree and its Orca child-worktree tree, not unrelated Runs.
It creates a static report, not a controller, daemon, durable queue or database.
The report describes observations collected over time, not an atomic runtime snapshot.
No class or recommendation grants permission to perform an action.

The selected architecture is option A1 from the supplied research summary.
Proposed components are a Python CLI, pure classifier, probe module and report writer.
A thin `/sc:sweep` command invokes `sc-sweep-protocol`; the CLI is `superclaude sweep run`.
The new package location proposed by the seed is `src/superclaude/cli/sweep/`.
Module names are `models.py`, `classify.py`, `probes.py`, `report.py` and `commands.py`.
These are proposed deliverables, not claims that these files already exist.

Evidence read for this specification:
- The complete seed brief, including its constraints and success criteria.
- Research report Section 8 excerpts covering Phase 1 steps and dependency gates.
- The gaps log rows GQ-101 through GQ-113 and its current count statement.
- The Phase 7 summary and supplied enrichment context.
- The worker contract terms, WC-2 through WC-13 and coordinator rules through the freeze rules.

Claims copied from research about runtime schemas remain UNVERIFIED in this variant.
No live runtime, QA report, installed decision file or referenced code implementation was inspected.
All additional API details below are proposed requirements, not discovered runtime behavior.

## Out of scope and later-phase blockers

| Later phase | Recorded scope | Blocker before design or execution |
|---|---|---|
| Phase 2 | Close or release sessions and remove worktrees | Positive ownership, admission, unread-report and open-PR evidence; fresh authorization |
| Phase 3 | Resume or retry work | WC-6 new-Task rules, freeze hand-back evidence and isolated report directories |
| Phase 4 | Trust layer | Owner-approved trust model and security review; no inferred approval |
| Phase 5 | Orchestrator of orchestrators | Explicit parent-child authority and bounded cross-tree ownership |
| Phase 6 | Management-server relay | Approved transport, authentication, privacy and delivery semantics |

No later-phase endpoint, message protocol or action executor is designed here.
No close, resume, kill, remove, stash, message, acknowledgement or outward operation is allowed.
No consuming question read is allowed as a workaround for missing waiting-state evidence.
No automatic staging, commit, archive repair or `.dev/tasks/` deletion is permitted.
No new security model or background service is installed.
WC-14 specifies coordinator duties; Phase 1 does not implement its scheduler.
Existing worker command semantics and WC-6, WC-9 and WC-10 remain unchanged.

## Functional requirements

FR-001. Protect the live Git index before adding any other probe behavior.
Acceptance: every executed `_git` argv contains global `--no-optional-locks`; negative fixtures fail before subprocess execution.

FR-002. Scope discovery to explicit Run IDs or the current Run binding and one worktree tree.
Acceptance: no binding and no `--run` exits 2, requests `--run <id>` and makes no `run-list` call.

FR-003. Enumerate workers with pagination and enrich at most 50 distinct Dispatch IDs.
Acceptance: duplicate rows are deduplicated; a fixture above the cap retains all discovered rows and marks unenriched rows unknown.

FR-004. Discover ordinary sessions from scoped transcripts, labels and ccsession tab-map files.
Acceptance: a transcript with no Orca tab-map join is person-started; no ccsession executable runs.

FR-005. Read contracts, package ledgers and archive markers without modifying them.
Acceptance: missing and malformed inputs have distinct reasons; `.archiving` remains byte-identical.

FR-006. Classify through the stated precedence using explicit `now` and `window` inputs.
Acceptance: one fixture per rule plus a changed-window fixture proves the classifier does not use a hidden default.

FR-007. Preserve absent, explicit null and unreadable evidence as different input states.
Acceptance: live `agentWait: null` can be working; absent `agentWait` cannot establish no wait.

FR-008. Preserve blocked-gate policy and possible same-session re-execution.
Acceptance: live blocked under `ask the coordinator` is not labeled a person question solely from that contract.

FR-009. Separate lifecycle classification from policy, result and closure assessments.
Acceptance: a blocked Ruling halt can appear in both waiting groups while counting as one affected session.

FR-010. Compute package contention only from worktree-local activity evidence.
Acceptance: unchanged committed packages shared across three worktrees cause no contention flag; changed active evidence names all three roots.

FR-011. Represent conflicting and incomplete archive states explicitly.
Acceptance: both package locations yield conflict; `to-do` plus `FINAL:` yields archive-blocked; incomplete ledger without `FINAL:` does not.

FR-012. Make terminal release and worktree removal separate REVIEW assessments.
Acceptance: an observed blocker yields no; unobserved admission, report-reading or PR facts yield could not determine, never yes.

FR-013. Apply the activity window without hiding unresolved work.
Acceptance: old open Tasks, explicit waits and unread-report candidates remain visible; inactive old ordinary sessions appear in Historical sessions.

FR-014. Use one status acquisition per worktree.
Acceptance: a complete fixture sweep calls `status --porcelain --branch` exactly once per root and reuses its parse for dirt, ahead and task-path checks.

FR-015. Produce one dated Markdown report and one versioned stdout JSON result.
Acceptance: JSON `report_path` names the completed report; no other persistent artifact is produced.

FR-016. Report incomplete discovery and source failures without inventing resolution.
Acceptance: unavailable Orca or removed roots yield source reasons and coverage counts; no failed read clears a wait or freeze.

FR-017. Limit recommended next steps to inspection and human decisions.
Acceptance: report fixtures contain no executable action controls or recommendation to stop, retry, release, merge or remove.

FR-018. Add WC-14, coordinator-only eligibility and installed routing documentation.
Acceptance: contract pins name `/sc:sweep`, no Unattended mode is added, routing copies agree and sync checks pass.

FR-019. Escape all untrusted report text, including Markdown separators.
Acceptance: injected pipes, newlines, terminal sequences, controls and bidi characters cannot create rows, headings or hidden instructions.

FR-020. Account for every discovered session without silently hiding overflow.
Acceptance: stable IDs appear once in the inventory; visible, historical and omitted counts reconcile, with unknown totals labeled lower bounds.

## Non-functional requirements

NFR-001. Observation is read-only except for the report and its required directories.
Acceptance: isolated filesystem hashes and metadata differ only at that output; real subprocess entry points are blocked in seam-mocked tests.

NFR-002. Classification and rendering are deterministic and perform no I/O.
Acceptance: identical normalized inputs, `now` and window produce byte-identical classifications and rendered text.

NFR-003. Probe work is bounded by 10 seconds per call and 90 seconds overall.
Acceptance: remaining time limits each call; after either deadline no new call starts and partial coverage is reported.

NFR-004. Imported modules have no runtime or filesystem side effects.
Acceptance: registration/help tests run with subprocess and file-write traps and start no client.

NFR-005. Unknown evidence never increases operational authority.
Acceptance: replacing any safety-critical input with unreadable evidence cannot produce a yes closure assessment or a new action proposal.

NFR-006. Report publication does not overwrite another observation.
Acceptance: same-second and concurrent sweeps produce separate files or fail cleanly; existing reports remain byte-identical.

NFR-007. Source parsing is bounded and defensive.
Acceptance: proposed limits of 1 MiB per contract/ledger, 256 KiB transcript tail and 8 MiB subprocess output stop oversized reads with explicit coverage loss.

NFR-008. Inputs are data, never executable instructions or configuration.
Acceptance: malicious titles, YAML tags, report paths and shell metacharacters trigger no shell, unsafe parser or command dispatch.

NFR-009. Report content stays local and uses existing user access boundaries.
Acceptance: no network posting occurs; new output files are owner-readable/writable only and transcript bodies are not copied wholesale.

NFR-010. Failures are diagnosable without raw transcript or secret dumps.
Acceptance: stderr and report source entries identify operation, stable reason code and affected scope, but omit command output bodies by default.

## CLI contract and re-run idempotency

Proposed invocation: `superclaude sweep run [--run <id>] [--window 6h]`.
Additional proposed options follow the research plan, not an existing CLI assertion:
- `--run <id>` is repeatable; duplicate IDs are deduplicated without broadening scope.
- `--window <N>h|<N>d` accepts positive integers only; default is `6h`.
- `--root <dir>` defaults to the current Git top-level and defines the feature-tree scope.
- `--output <dir>` defaults to `<root>/.dev/sweeps/`.
- Resolved output must remain under `<root>/.dev/`, including through symlinks.
- Reject overlap with input package or transcript directories before collecting evidence.
- Unknown flags, empty Run IDs, invalid windows and ambiguous roots are usage errors.
- `/sc:sweep` passes these options unchanged; it adds no independent state inference.

Exit 0 means collection completed and the report was successfully published.
Exit 0 includes bounded, partial and Orca-unavailable observations, not an all-clear.
Exit 1 means an internal safety invariant, unexpected failure or report write failed.
Exit 2 means invalid arguments or missing Run selection; no report is required.
If Orca is unavailable, an explicitly selected Run permits root-only degraded reporting.
If Orca is unavailable and no Run was supplied, binding cannot be established: exit 2.
Print one JSON object on stdout only after successful report publication; diagnostics use stderr.

Schema version 1 has these required top-level keys:
`schema_version`, `observed_at`, `scope`, `window`, `orca_available`, `sources`,
`rows`, `waiting`, `summary`, `report_path`.
Absent optional values are null, never omitted; class counts include zero values.
`scope` is the canonical root string; the report also records selected Run IDs.
`waiting` has `a` and `b` lists of stable session IDs, not duplicate session records.
`summary` contains counts per class, `total` and `bound_reached`.
`rows` include stable ID, origin, Worktree, ten dimensions, class, evidence, notes and safety.
The Markdown and JSON representations derive from the same frozen observation model.

Re-run idempotency means no lifecycle changes and no consuming cursor advancement.
It does not mean one shared output path: each invocation deliberately preserves a new observation.
Use the dated base name `<YYYYMMDD-HHMMSS>-sweep.md`; add a collision suffix if needed.
Reserve the final path exclusively; never truncate an existing report or overwrite on retry.
Render in memory first; write only that reserved report path, not a temporary artifact or latest pointer.
On handled write failure, remove only this invocation's incomplete output if it can be identified safely.
Do not print success JSON after a failed or incomplete write.
An uncatchable process termination can leave a partial report; no atomic-publication claim is made.
A final `Report complete` footer distinguishes fully written files when inspecting crash leftovers.

## Data model and classification precedence

Use immutable records; collect first, classify second, render last.
Every observation carries source identity, observation time, readable status and a reason if unavailable.
Booleans that cannot be proved are null; missing fields do not silently become false.
Session identity is Dispatch ID for workers and scoped transcript identity for ordinary sessions.
Task ID and Run ID remain separate keys; path co-location is never proof of ownership.
Duplicate or contradictory observations retain source notes instead of using last-write-wins silently.
Record the collection interval and mark contradictory lifecycle evidence could not determine.

Required model groups:
- Orca observation: liveness, status, outcome, agent-wait value and presence, parent and worktree.
- Orca completion: `worker_done` evidence, body, terminal state, next action and unsupervised status.
- Task context: blocked-gate policy, ready state and creator evidence, nullable when unavailable.
- Contract: path, `worker_status`, question, reason, `report_path` and `artifacts`.
- Transcript: path, readable flag, last activity and bounded-tail coverage.
- Worktree: canonical path, dirt, unmerged, unpushed, unsaved task files and freeze evidence.
- Package: ID, location, ledger readability, `FINAL:` presence, marker and active-local evidence.
- Coverage: source, complete/partial/unavailable, age, omitted count or unknown and reason.
- Classification: class, waiting kind, evidence and notes.
- Safety: independent terminal and worktree values of yes, no or could not determine, with reasons.

Preserve ten dimensions independently: lifecycle, phase, health, approval, freshness, result,
admission, evidence packet, policy and tests/review.
No admission, approval, tests or report-reading event is inferred from a successful contract.
A complete evidence packet means referenced files exist, not that their content is correct or admitted.
Unknown ledger halt/Ruling syntax stays unknown; synthetic cases do not establish runtime support.

Apply the following ordered rules, retaining independent policy and health dimensions:
1. A blocked contract means waiting on a person (a) when settled, under report-blocked policy,
   or when an implement Ruling halt requires a person regardless of the brief policy.
   Live ask-coordinator re-execution skips this contract branch; unknown policy stays unknown.
2. Positive Orca exit proof with known absent completion and known absent fencing is stalled (proved).
   Unreadable fencing/completion evidence defeats this rule and yields could not determine.
3. Positive `consumer_fenced` evidence means fenced, not stalled or failed.
4. Non-null `agentWait` means waiting on a person (a); frozen policy or ready-Task review is (b).
   The rule-1 skip also applies to blocked-contract branches here; it does not erase explicit waits.
   Without creator evidence, list ready Tasks for ownership review, never label them definitively foreign.
5. Live plus `in_progress` plus explicitly null `agentWait` means working.
6. Settled outcome plus a parsed terminal contract, or a guard-refused body, means finished.
   A partial result remains usable-not-yet-judged; finished never means admitted.
7. Everything else is could not determine, including unverifiable liveness and missing critical fields.

A known context-only unsupervised Dispatch bypasses liveness-based working/stalled rules.
It remains unknown unless the contract-based waiting or finished rules prove another class.
Idle applies only to readable person-started sessions with activity older than the supplied window.
Active person-started sessions are could not determine with a person-session-active note.
Unknown timestamps never become idle; old ordinary sessions are shown in Historical sessions.
Open Tasks, waits and unread-report candidates are exempt from activity-window exclusion.
A late heartbeat, transcript final turn or stale projection is never stall proof.

Package state has four report values: normal, archive-blocked, interrupted archive and conflict.
Precedence is conflict over interrupted archive over archive-blocked over normal; retain all raw flags.
Conflict means the same ID occurs in both `to-do/` and `done/` in one root.
Interrupted archive means `.archiving` exists; it must not be cleared.
Archive-blocked means still in `to-do/` with a `FINAL:` line, not merely all tasks complete.
An unfinished ledger remains a separate blocker even when package state is normal.
Active-local evidence means a package folder or ledger differs from the fixed base reference.
Unchanged committed folders are excluded from cross-root contention checks.
A changed folder is conservative contention evidence, not proof of a live executor.
If the base or change evidence cannot be established, contention is unknown, never cleared.

Any known dirty, unmerged, unpushed, frozen, unfinished, conflicting or contended state blocks removal.
No upstream is treated conservatively as an unpushed blocker.
Open PRs and whether the coordinator read reports are unobservable here: worktree yes is unreachable.
Reclaimable plus release does not prove reports were read: terminal yes is likewise unreachable.

## Probe seams and argv allowlist

Proposed signatures are `_orca(*args: str) -> str` and `_git(cwd: Path, *args: str) -> str`.
Only these seams may execute external processes; disk readers are separately mocked plain reads.
Use argv arrays with no shell, closed stdin, bounded output and bounded timeout.
Validate the complete argv shape before spawn, including cardinality and token order.
Dynamic IDs and paths are single validated tokens, never interpolated shell fragments.
An unknown verb or option is a programmer/safety error and causes exit 1, not degraded success.
Expected OS, timeout, runtime and parse failures become source coverage reasons.

Closed initial Orca forms, described with placeholders rather than shell commands:
- `orca-ide orchestration run-current` for binding resolution only.
- `orca-ide orchestration worker-list --run <id> --json`.
- `orca-ide orchestration worker-show --dispatch <id> --json`.
- `orca-ide orchestration task-list --ready --run <id> --json`.
- `orca-ide worktree ps --json`, the sole non-orchestration exception.
The exact JSON mode of run-current and worker-list continuation argv are UNVERIFIED.
Before release, verified syntax must become explicit allowlist tuples and pinned fixtures.
Do not guess continuation flags: if unsupported, show partial coverage rather than silently stop.
No runtime-dependent wildcard or arbitrary suffix is acceptable in the final allowlist.
No `run-list`, `gate-list`, `worker-read`, inbox, check, ask, send, reply or stash operation is allowed.
No `--agent-wait` or `--include-remote` is enabled by default; remote coverage stays explicit.

Every Git form starts `git --no-optional-locks -C <root>`.
The single status form is `status --porcelain --branch`.
The only additional read families permitted are `rev-parse`, `log` and `branch`.
Exact arguments for base identity and ancestry checks are a pre-implementation design gate,
not permission to run arbitrary arguments under those three read-family prefixes.
Package activity must use the existing status parse and a bounded plain-read comparison
against a fixed base tree; select and verify any required base-reading argv before expanding the list.
Never solve GQ-101 by adding a second status invocation per worktree.

Read ccsession metadata directly, never invoke its CLI, which the research reports can migrate names.
Read only fixed source patterns under admitted roots and scoped transcript project keys.
A child root outside the feature directory is permitted only through verified child-tree membership.
Reject escaping symlinks; never follow contract artifact paths outside that admitted root's read scope.
Deduplicate canonical roots; discover no unrelated worktree merely because a local path exists.
Stop further Orca reads after runtime_unavailable; continue admissible local reads within budget.

## Report format

Use a local Markdown document with these sections in order:
1. Header: READ ONLY, UTC observed time, collection interval, root, Run IDs and activity window.
2. Source coverage: source ages, failures, lower-bound totals and omissions, never implied completeness.
3. Attention Ledger (a): explicit questions, oldest known wait first, stable-ID ties, unknown-age group last.
4. Attention Ledger (b): policy freezes and ready-Task ownership review, with no invented question text.
5. Retained problems: stalled proof, fencing, failed results, source loss, archive problems and contention.
6. Sessions: stable ID, owner, Worktree, class, waiting-on, evidence, next inspection and ten dimensions.
7. Worktrees: safety REVIEW, blockers, unknown facts and package-state entries.
8. Historical sessions: older ordinary-session records, with no silent exclusion.
9. Shift Brief: counts, unresolved decisions and evidence to inspect next.
10. What I could not determine, followed by Inspection only and the Report complete footer.

Every section lists shown/known-total counts; unknown totals read at least N.
Any truncated source names its limit and reason; unknown age is never displayed as zero.
Questions count distinct affected session IDs using a union, not a sum across groups.
Messages coverage always reads partial: pending Orca questions are not enumerated.
Empty attention sections say No matching records. This is not an all-clear.
Fixed cautions include Seen is not resolved and Answered: could not determine.
Closure values are REVIEW only; no yes is emitted from the available Phase 1 sources.
Next steps name inspection, ownership confirmation or the person's decision, not action execution.
Sanitize all cells and free text, escape `|`, flatten embedded newlines and neutralize Markdown HTML.
Do not emit active links from untrusted source text or copy full transcript bodies.

## WC-14 contract rule proposal

Proposed heading: `### WC-14. Coordinator loop`.

The coordinator keeps watching its Run until every Task it created is settled and every result
has been inspected and its admission or rejection recorded. It never stops watching on its own.
When an Orca wait expires, the coordinator re-arms it. On every coordinator wake it runs
`/sc:sweep` and reads the report before acting; it also keeps a periodic sweep scheduled while
work remains. Phase 1 adds this duty, not a scheduler or a new Orca lifecycle protocol.
A missing heartbeat is absence, never death. Only Orca's positive stall proofs justify a stalled label.
Anything the sweep cannot prove stays could not determine and never authorizes a retry or release.
The coordinator reports unresolved blocked or failed results, unusable partial results, third brief
refusals, unfamiliar ready Tasks and frozen plans to the person and retains them in its run notes.
Where the existing fan-in rule applies, insufficient admitted inputs remain an unresolved decision.
Person-started sessions are observed only, never messaged. Reports are dated local files, never posted.
The sweep recommends no stop, retry, release, merge or removal; those remain coordinator decisions
under the existing contract and the person's authorization. Every retry remains a new Task under WC-6.

Add `/sc:sweep` to the never-as-worker list and keep it out of unattended commands.
Coordinator-only is contractual eligibility, not a new identity or access-control mechanism.
Do not claim the CLI mechanically identifies callers; no such mechanism is designed here.
Owner approval of the rule ID and exact text is required before changing the shared contract.

## Operational failure modes

| Failure | Required behavior |
|---|---|
| Orca absent or runtime_unavailable | Stop Orca calls; local-only report if Run selection is valid; unavailable banner |
| No current Run binding | Exit 2 with explicit Run-selection request; never enumerate Run history |
| Worker list schema or cursor unknown | Keep discovered IDs, show coverage loss; no fabricated fields or guessed argv |
| Enrichment cap or budget exhausted | Retain discovered rows as unknown; report omitted discovery separately |
| Worktree disappears | Mark affected rows unscanned: worktree removed during sweep; continue other roots |
| Unreadable contract or transcript | Unknown evidence, not finished, idle, stalled or cleared policy |
| Input changes during reading | Retry a plain read once within budget; otherwise mark inconsistent observation |
| Duplicate Dispatch with contradictory state | One identity with conflict reason; no last-row-wins classification |
| No upstream or ancestry unknown | Respect blocker or unknown; never infer removable from clean status |
| Output denied, full disk or partial write | Exit 1; no success JSON; preserve previous reports |
| Process killed during output | Partial file may remain without completion footer; next sweep uses a new path |
| Remote host not covered | Print unknown coverage and lower-bound count, never no sessions |

## Risks and mitigations

- False blocked from sweep index refresh: require `--no-optional-locks` at the seam, before any other work.
- Wrong safe-to-close inference: separate two safety dimensions and make yes unreachable in Phase 1.
- Stale blocked contract during re-execution: carry brief policy and completion evidence explicitly.
- Overstated read-only runtime behavior: argv tests prove local intent only; runtime non-consumption remains a release gate.
- Shared package false positives: compare active-local evidence with a fixed base, not folder presence.
- Changed artifacts mistaken for execution: describe contention evidence conservatively and keep review with the person.
- Report injection or private-data exposure: sanitize text, restrict path reads and retain minimal evidence excerpts.
- Live-source races: record collection interval and source age; make every later action require fresh checks.
- Unbounded transcript population: bounded tails, deadline checks and explicit scan omissions preserve honest coverage.
- Contract overlap with other work: verify PR #422 status and changed-file overlap before WC-14 edits.
The current status of PR #422 and the referenced #409 layout commit is UNVERIFIED here.

## Gap resolutions

GQ-103(1) comes first: every Git invocation carries `--no-optional-locks`; FR-001 is the first build gate.
GQ-101: unchanged committed task folders do not count as execution; active-local differences drive contention.
List all affected roots for a contended package, including three or more; unknown base comparison stays unknown.
GQ-102: conflict is an explicit package state, has highest package-state precedence and blocks removal.
GQ-103(2): the pure classifier receives the parsed window explicitly alongside injected UTC `now`.
GQ-103(3): model brief policy, completion, transcript readability, contract report path and artifacts explicitly.
GQ-104: delete the Run-history fallback; absent selection/binding exits 2 rather than spending the cap on history.
GQ-105: use `to-do/` plus a `FINAL:` ledger line for archive-blocked, with an incomplete-ledger negative test.
GQ-106: add `.dev/sweeps/` to the project ignore rules and rollback inventory, never `.dev/tasks/`.
GQ-107: escape table pipes as well as control characters; injection fixtures must preserve table structure.
GQ-108: person-started means scoped transcript with no Orca tab-map join; old activity goes to Historical.
GQ-109: exclude gate-list, worker-read and every stash form until a later approved phase consumes them.
GQ-110: one full porcelain/branch status parse supplies the worktree status checks; no filtered repeat status.

GQ-111 and GQ-112 are documentation debt, not runtime requirements.
Use the gaps log's read count of 113 rows, 88 open and 25 resolved; do not reuse superseded counts.
GQ-113: the report's prior all-open-rows claim covers GQ-01 to GQ-100 only, not subsequently added rows.
This variant records GQ-101 through GQ-113 without editing the research report or closing its gap rows.
Acceptance for these three items is accurate local citations and explicit carry-forward, not a report rewrite.

## Open questions and recommended answers

- Populated worker-list schema: keep list-plus-show, bounded at 50; require approved captured fixtures before release.
  Synthetic exited/fenced fixtures test logic but do not verify a production evidence mapping.
- Pending questions: use only parsed blocked contracts and explicit agentWait; always state partial message coverage.
- Fencing proof: absent transcript literals are not proof of no fencing; keep exited rows unknown without readable evidence.
- Pagination and base-read argv: verify exact forms at design review before admitting tuples; otherwise ship no unsupported probe.
- Runtime read-only proof: require a separately authorized disposable-Run check before release, excluding removed verbs.
  This specification-writing task authorizes no live check and performs none.
- Periodic sweep cadence: recommend five minutes while unresolved work remains; exact timer integration is later coordinator setup.
- WC-14 approval and PR #422 sequencing: require owner acceptance and current overlap checks; do not silently omit WC-14 from done.
- #409 layout adoption: use the section contract stated here; do not depend on unmerged implementation imports.
- Output consistency: choose exclusive final-file writes plus a completion footer rather than an extra temporary file.
  This honors one-file output, at the documented cost of possible crash leftovers.
- Action recommendations: choose inspection-only next steps; this removes ambiguous advice before action evidence exists.

## Verification and rollback

All Phase 1 behavior must be tested with `_orca` and `_git` mocks and temporary file fixtures.
Tests must never start live Orca, ccsession or Claude sessions.
Cover rules 1 through 7, idle, precedence collisions, null versus absent, source loss and the explicit window.
Cover package contention with unchanged shared folders and multiple changed roots, conflict and incomplete archives.
Cover exact argv rejection, per-call/overall deadlines, pagination omissions, 50-show cap and one status per root.
Cover two concurrent same-second reports, write failure, escaping output paths, input races and hostile report text.
Snapshot bytes and metadata under isolated root, HOME and XDG state; only report output may differ.
Keep runtime non-consumption claims UNVERIFIED until the separately authorized release gate has evidence.
Affected tests, lint, sync verification, contract pins and routing-copy parity are required before release.
Installed primitives must name installed and project lookup surfaces, never source-tree runtime paths.

Rollback removes the new CLI registration/package, command, skill, routing entries and documentation additions.
Restore WC-14 and never-as-worker changes together so eligibility and shared text cannot diverge.
Revert the `.dev/sweeps/` ignore addition only after deciding where existing reports should remain.
Retain existing sweep reports by default; rollback is not authorization to delete local observations.
Never remove `.dev/tasks/`, its ledgers or artifacts; no data migration or runtime record rollback exists.
Re-run the pre-existing registration, contract and routing tests after rollback.
Acceptance: prior commands remain usable, no sweep entry is advertised and no session lifecycle state changed.
