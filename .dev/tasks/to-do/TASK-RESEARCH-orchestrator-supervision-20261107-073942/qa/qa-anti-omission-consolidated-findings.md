# Consolidated findings: Phase 6 anti-omission gate, cycle 0

- Sources: `qa/qa-anti-omission-report-1.md` (FAIL, 8 IMPORTANT, 13 MINOR), `qa/qa-anti-omission-report-2.md` (FAIL, 10 IMPORTANT, 13 MINOR, 3 dedup), `qa/qa-anti-omission-report-3.md` (PASS, 0 blocking, 1 MINOR, 3 dedup), `qa/qa-anti-omission-report-4.md` (PASS, 0 blocking, 1 MINOR, 7 dedup)
- |F_0| = 18
- Gate status: FAIL
- Merge rule: every omission from all four reports is listed below. A blocking row from one report absorbs a MINOR row on the same finding from another (AO-04 absorbs report 2 MINOR row 11). No blocking omission is marked JUSTIFIED; all 18 are RECOVER.
- Constraints for the fix agent: keep the NB-4 exception record (about `:13`, `:1644`) and both [CONTRADICTION] markers with their resolutions. Do not reopen findings resolved by the lens gate or the fidelity gate. Add content with targeted Edits in the section where it belongs, using the source file's wording and evidence.

## Blocking omissions (all RECOVER)

| ID | Severity | Source finding | Source file | Where it belongs in the report | Disposition |
|---|---|---|---|---|---|
| AO-01 | IMPORTANT | The coordinator never runs one managed package in two worktrees at once (WORKER-CONTRACT cleanup rule, `:108`). | scope-01 rule 9 (`:64`); report 1 row 1 | Contract rules the sweep checks (S3.1 / step 1.3) | RECOVER |
| AO-02 | IMPORTANT | Fan-in allows at most 10 inputs; a sweep reporting a fan-in group shows settled/admitted counts against N. | scope-01 rule 13 (`:68`); report 1 row 2 | Fan-in trigger (G5) and report rows | RECOVER |
| AO-03 | IMPORTANT | A worktree removed mid-sweep is reported and must not crash the run (`seed-brief.md:45`). | research-notes (`:178`); report 1 row 3 | Sweep behaviour and step 1.8/1.9 tests | RECOVER |
| AO-04 | IMPORTANT | Affected counts are a set union across sources, not a sum ("Distinct affected sessions: N (set union, not a sum)"). | research-notes (`:143`); scope-04 `:194`, `:217`, `:283`; report 1 row 4, report 2 MINOR row 11 | S3.1 report rules, step 1.5 renderer | RECOVER |
| AO-05 | IMPORTANT | Coordinator turn guard: when `worker-list --run <id> --terminal-state reclaimable --json` returns rows, the coordinator must not end its turn. | scope-02 (`:94`); report 1 row 5 | WC-14 coordinator loop / terminal-releasable rule | RECOVER |
| AO-06 | IMPORTANT | Context-only Dispatches from `orchestration dispatch` are listed as `unsupervised` with terminal state `retained` [CODE-VERIFIED]; the classifier must say how these rows are classified. | scope-02 (`:95`); report 1 row 6 | Classifier precedence (S3.1 / step 1.3) | RECOVER |
| AO-07 | IMPORTANT | Package state "archive-blocked" (non-Linux refusal, folder stays in `to-do/`) and the `.archiving` marker (interrupted archive) must be recognised, not reported as unfinished or ignored. | scope-02 (`:192`); research-notes (`:177`); report 1 row 7 | Package reading of `.dev/tasks/{to-do,done}` and classifier | RECOVER |
| AO-08 | IMPORTANT | The new HOW-WE-WORK routing row needs a row ID registered in `_EXPECTED_IDS` (`:56-97`) of the routing-table test, or the test fails. | scope-01 (`:117`); report 1 row 8 | Registry list (step 1.21) and rollback "Four registries" row | RECOVER |
| AO-09 | IMPORTANT | Imported evidence is inert: sanitize ESC/CSI/OSC, C0/C1 controls, carriage returns and bidi controls before rendering (`PKG/PLAN.md:38`, `canvas.py:10-17`). | scope-04 `:219`; report 2 row 1 | S3.1 report rules, step 1.5 renderer, step 1.12 tests | RECOVER |
| AO-10 | IMPORTANT | B-14 source field for each column (Lifecycle, Health, Freshness, Evidence, Phase/Admission "not observed", Tests/review null, Owner, Worktree); step 1.5 has only a bare citation. | scope-04 `:334-351`; report 2 row 2 | Step 1.5 column derivation | RECOVER |
| AO-11 | IMPORTANT | B-12 fallback sources for question, requester, decision-owner and evidence cells, and the (a) table columns ID / Age / Question / Requested by / Decision owner / Affected / Evidence. | scope-04 `:129`, `:311`, `:322-330`; report 2 row 3 | S3.1 (a) list skeleton, step 1.5 | RECOVER |
| AO-12 | IMPORTANT | Empty-state rule "No matching records. This is not an all-clear." (`PKG/render.py:116`), including under the waiting heading. | scope-04 `:225`, `:276`; report 2 row 4 | S3.1 skeleton, step 1.5 fixed strings, step 1.12 tests | RECOVER |
| AO-13 | IMPORTANT | Source loss does not resolve questions, fail sessions, unlock a policy freeze or authorize retries; "source read and item absent" differs from "source lost". | scope-04 `:101`, `:221`; report 2 row 5 | S3.1 report rules, SC-7, step 1.12 | RECOVER |
| AO-14 | IMPORTANT | Workspace co-location alone is not ownership (`PKG/integration-gaps.md:12`). | scope-04 `:222`; report 2 row 6 | Session-to-worktree mapping rule | RECOVER |
| AO-15 | IMPORTANT | A peer row's ownership is unknown unless it carries `linked: true`; never attribute a peer by workspace membership. | 06-orca-open-questions `:99`, `:110`; report 2 row 7 | Peer attribution rule (next to AO-14) | RECOVER |
| AO-16 | IMPORTANT | `worktree ps` hosts reported "not covered" print "could not determine", never "no sessions"; `worktree ps` is paged by a shared `--limit`, so a truncated page under-reports. | 06-orca-open-questions `:97`, `:109`; report 2 row 8 | Orca probe rules (step 1.2 / 1.3) | RECOVER |
| AO-17 | IMPORTANT | Source position: "The sweep must not propose stop/abandon/retry/release; those need positive proof and are coordinator decisions." Record it against steps 1.15/1.17, which have the sweep recommend those actions. | 06-orca-open-questions `:138`; report 2 row 9 | Where the report records the conflict with #409 rule 5 | RECOVER |
| AO-18 | IMPORTANT | Global counts name scope and collection completeness; a selected filter (`--run`, time window) states its denominator. | scope-04 `:67`; report 2 row 10 | S3.1 header/scope line, step 1.5 | RECOVER |

## MINOR omissions (notes, not recovered, not blocking)

| Report | Row | Finding (short) |
|---|---|---|
| 1 | 15 | core/CLAUDE.md `### Orca session launches` must not be contradicted (scope-01 `:112`) |
| 1 | 16 | F12 naming question `sc:sessionsweep` vs `sc:sweep` (scope-01 `:138`) |
| 1 | 17 | Refused person-mode flag writes `worker_status: failed` (scope-02 `:180`) |
| 1 | 18 | `lastFailure` is a JSON-encoded string, parse twice (scope-02 `:60`) |
| 1 | 19 | Tally of observed worker state enum values (scope-02 `:76`) |
| 1 | 20 | `orca-titles` as a title source (scope-02 `:166`) |
| 1 | 21 | Slugify naming of sessions/worktrees (scope-02 `:162`) |
| 1 | 22 | Shape of the `worker-release` receipt (scope-02 `:206`) |
| 1 | 23 | Custom titles ignored when matching sessions (scope-02 `:156`) |
| 1 | 24 | `ccsession --here` grouping when a worktree is removed (scope-02 `:164`) |
| 1 | 25 | Why the field is named `worker_status` (scope-02 `:176`) |
| 1 | 26 | `json.dumps(..., ensure_ascii=False)` in the reused output pattern (research-notes `:130`) |
| 1 | 27 | #409 footer "source coverage is not fleet-wide assurance" wording (research-notes `:143`) |
| 2 | 12 | Meaning in words, not color; stale/frozen not shown as failure (scope-04 `:220`) |
| 2 | 13 | Events deduplicated by id, latest seq kept, seq order (scope-04 `:174`, `:227`) |
| 2 | 14 | Do not clip IDs in a static report (scope-04 `:245`) |
| 2 | 15 | Footer and Worktrees reassurance lines (scope-04 `:74`, `:300`, `:307`) |
| 2 | 16 | Scope-line detail: current vs historical, inventory vs mapped, unmapped count (scope-04 `:60-61`, `:272`) |
| 2 | 17 | Join on stable IDs, never display names (scope-04 `:218`) |
| 2 | 18 | "oldest observed" age label; timeline gap is missing observation (scope-04 `:194`) |
| 2 | 19 | "Not registries" list (scope-03 `:159-164`) |
| 2 | 20 | Deferred heavy imports in command bodies (scope-03 `:74`) |
| 2 | 21 | `_ORCA_NAME_RE` bans Orca command names in Unattended sections (scope-03 `:156`) |
| 2 | 22 | `--peek` hides read questions; only `--all` shows read-but-unanswered (06 `:74`) |
| 2 | 23 | Peek must use the coordinator's own identity (06 `:67`) |
| 2 | 24 | integration-gaps line 28 walkthrough step is untested (06 `:139`) |
| 2 | 25 | Unknown optional fields are absent; absence never authorizes action (05 `:65`, `:77`) |
| 3 | 1 | Research-gate trajectory 28 to 3 to 1 and 2 fix cycles not restated (gaps `:7`) |
| 3 | 5 | GQ-09 status changed from owner decision to settled; basis stated in report §9.2 row 66 (status change, not a loss) |
| 4 | 1 | synth-05 "Tag conventions" paragraph and parent-folder check (synth-05 `:12`) |

## Covered by dedup (no action)

- Report 3 rows 2-4: gaps section (e) rows covered by report §9.1 rows 12 (GQ-15), 41 (GQ-49/50) and 42 (GQ-51). Note: the gaps file maps the agent-wait probe to GQ-50; the report's GQ-51 is the right one.
- Report 4: synth-04 implementation steps 1-7, covered by report Section 8 Phase 1.
- Reports 1 and 2: 6 and 3 dedup rows as listed in those reports.

## Cycle control

- Gate counter: anti-omission gate, own counter, independent of the lens and fidelity gates. Cycle 0 is the first review; fix pass 1 follows.
