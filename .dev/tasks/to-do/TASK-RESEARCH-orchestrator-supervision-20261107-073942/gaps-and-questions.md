# Gaps and Questions: Orchestrator mode (#339)

**Task:** TASK-RESEARCH-orchestrator-supervision-20261107-073942 (checklist item 182)
**Date:** 2026-11-07
**Purpose:** one gap register for Phase 4 synthesis, merged from the research files, their gaps sections, `research/research-notes.md` AMBIGUITIES 1-11 and C1-C12, and the consolidated and verification reports in `qa/`.

**Research gate status:** ended by coordinator exception, not a clean PASS. The gate ran 2 fix cycles; blocking findings went 28 -> 3 -> 1. The coordinator authorized proceeding with one open blocking finding, NB-4 (`qa/qa-research-verification-qualitative-cycle1.md:42`), carried below as an OPEN gap.

**Files read:**

- `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`
- `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `research/07-gate-gap-fill.md` (added by a gate fix agent)
- `research/research-notes.md`
- `qa/qa-consolidated-findings-phase3.md`, `qa/qa-consolidated-findings-phase3-cycle1.md`, `qa/qa-research-verification.md`, `qa/qa-research-verification-qualitative.md`, `qa/qa-research-verification-cycle1.md`, `qa/qa-research-verification-qualitative-cycle1.md`

---

## (a) Merged gap table

One table, deduplicated. When several sources name the same gap, one row carries all of them in the Source column. Severity follows the source where it gives one (`research-notes.md:270-273`; G1-G7 per `qa/qa-consolidated-findings-phase3.md` N-32; every B-/NB- finding is IMPORTANT per its QA report); otherwise Minor for open questions the sources call non-blocking (N-15). Status is `resolved` or `open`; an open item that is an owner or plan decision says so.

| ID | Gap | Severity | Source file | Status | Resolution or evidence |
|---|---|---|---|---|---|
| GQ-01 | G-A: worker-list row schema (does a row carry the 16-field `projection`, the four guide-named fields, or `agentWait`?) | Critical (N-29 suggests downgrading once the fallback is accepted) | `research/research-notes.md:270`, C10 `:328`; `research/05-orca-row-schema.md:157`, Gap 1 `:186`; `research/scope-01-contract.md` Q1 `:142`; `research/scope-02-orca-recovery.md` Q1 `:223`; `qa/qa-consolidated-findings-phase3.md` B-08, N-29 | open (partly answered) | 05 Answer (1) `:157`: no populated row was captured (`lc01-step7.txt:28` is `[]`), so the row's content is [UNVERIFIED]; `agentWait` is not inside `projection` (`lc16-show-4.json:180,185`). Design fallback (05 `:165`, Gap 1 `:186`): rely only on the envelope and Dispatch id, call `worker-show` once per row; worst case ceil(N/100) list calls plus N show calls. Closes only with a live `worker-list --run <id> --json` capture. B-08 was accepted as a documentation fix (`qa/qa-research-verification.md:27`). |
| GQ-02 | G-B: no non-consuming read of pending questions | Critical | `research/research-notes.md:271`, C11 `:329`; `research/06-orca-open-questions.md:77`, Gap 5 `:162`, Gap 17 `:174`; `research/scope-04-409-layout.md` Q2 `:357`; `qa/qa-consolidated-findings-phase3.md` B-17 | open (answered for the design; no read path exists) | 06 `:77`: Orca question enumeration is reported as "could not determine". "Waiting on a person" uses the contract fallbacks: WC-3 `blocked_question` in `return-contract.yaml`, non-null `agentWait` from `worker-show`, the frozen-plan test at `WORKER-CONTRACT.md:133-136`. The report header says message coverage is partial. B-17 RESOLVED (`qa/qa-research-verification.md:36`). |
| GQ-03 | NB-4: the `scope-03:99` default argv allowlist omits `task-list`, `run-list`, `run-current` and `gate-list`, which Section C rule 4(b) and the scope-04 Owner/Approval columns read | Important | `qa/qa-research-verification-qualitative-cycle1.md:42` (against `research/scope-03-cli-patterns.md:99`, `research/research-notes.md:172`, `:197`, `research/05-orca-row-schema.md:175`, `research/scope-04-409-layout.md:330`, `:339`, `:345`, `research/07-gate-gap-fill.md:41-47`) | resolved | fix applied 2026-11-07 by NB-4 fix pass; re-check at Phase 5 synthesis gate |
| GQ-04 | G1: WORKER-CONTRACT has no rule that the coordinator keeps polling | Critical (N-32) | `research/scope-01-contract.md:78`; `qa/qa-consolidated-findings-phase3.md` N-30 | open (WC-14 must state it) | scope-01 leaves the owner-order source UNVERIFIED; N-30 says the memory note `coordinator-never-stop-polling.md` (owner order 2026-11-05) is readable and should be cited. |
| GQ-05 | G2: no rule to re-arm the wait after it expires | Important (N-32) | `research/scope-01-contract.md:79` | open (WC-14) | Filled by the proposed coordinator-loop rule; no current text. |
| GQ-06 | G3: no periodic sweep | Critical (N-32) | `research/scope-01-contract.md:80` | open (the feature itself) | The sweep command and skill are the fill (`research/research-notes.md` A1-A4, `:153-162`). |
| GQ-07 | G4: no classification vocabulary | Critical (N-32) | `research/scope-01-contract.md:81`; `research/research-notes.md` C14 `:332` | resolved | `research/research-notes.md` Section C (`:188-200`) is the one canonical vocabulary and precedence; B-01 and B-28 RESOLVED (`qa/qa-research-verification.md:20`, `:47`). |
| GQ-08 | G5: no rule for when to tell the person | Important (N-32) | `research/scope-01-contract.md:82` | open (WC-14) | No current text; design decision for the plan. |
| GQ-09 | G6 / AMBIGUITY 8: whether the sweep reports person-started (peer) sessions at all | Important (N-32) | `research/scope-01-contract.md:83`, Q7 `:148`; `research/research-notes.md:310` | open (owner decision, WC-14) | The evidence route exists (pane-key join, GQ-18); "at all" stays an owner decision (`qa/qa-research-verification.md:28`, B-09). "Idle" applies only to these sessions (Section C, `research/research-notes.md:188`). |
| GQ-10 | G7 / AMBIGUITY 3: where the sweep report is written | Important (N-32) | `research/scope-01-contract.md:84`, Q4 `:145`; `research/research-notes.md:305` | open (owner decision) | No source fixes a location. |
| GQ-11 | Rule ID: new WC-14 versus amending WC-1 (AMBIGUITY 4) | Minor | `research/scope-01-contract.md` Q2 `:143`; `research/research-notes.md:306` | open (owner decision) | WC-14 is the working name. |
| GQ-12 | `/sc:sweep` on the never-as-worker list and the tests that must change (AMBIGUITY 7 in part) | Minor | `research/scope-01-contract.md` Q3 `:144`; `research/research-notes.md:309`; `qa/qa-consolidated-findings-phase3.md` N-34 | open (plan) | N-34: the test named "all_seven" checks a `NEVER_AS_WORKER` list of 8 entries, so WC-14 work must not rely on the test name. |
| GQ-13 | Whether `AUDIT_ROOTS` scans `commands/` | Minor | `research/scope-01-contract.md` Q5 `:146` | resolved | Yes: `test_worker_contract.py:1090-1094` `AUDIT_ROOTS`, used at `:1134` (re-read in `qa/qa-research-verification.md:40`, B-21). |
| GQ-14 | Whether a test requires registering the command in help / HOW-WE-WORK | Minor | `research/scope-01-contract.md` Q6 `:147` | open | [UNVERIFIED] in scope-01; see GQ-24 and GQ-28 for the scope-03 side. |
| GQ-15 | `liveness.reason` values and when the field is present | Minor | `research/scope-02-orca-recovery.md` Q2 `:224`; `research/05-orca-row-schema.md` Gap 3 `:188` | open (answered as far as evidence allows) | Guide names six reasons for `unverifiable` (05 `:159`) [UNVERIFIED]; every capture shows only `live` with no `reason`. |
| GQ-16 | Shape of a `runtime_unavailable` result | Minor | `research/scope-02-orca-recovery.md` Q3 `:225` | open | [UNVERIFIED]; no capture. |
| GQ-17 | Whether heartbeat age feeds `projection.liveness` | Minor | `research/scope-02-orca-recovery.md` Q4 `:226`; `research/06-orca-open-questions.md` Gap 12 `:169` | open | [UNVERIFIED]; inventory open item 7 (`orca-capabilities.md:182`) unchanged. The sweep never infers stalled from a late heartbeat (WC-10). |
| GQ-18 | Known gap 1: join from an Orca pane key to a ccsession transcript | Important (`research/research-notes.md:273`) | `research/scope-02-orca-recovery.md` Q5 `:227`; `research/research-notes.md:273`, C12 `:330`; `research/07-gate-gap-fill.md` D; `qa/qa-consolidated-findings-phase3.md` B-09, N-31 | resolved (for one worker) | CODE-VERIFIED for lc16: `assigneePaneKey` `ec61f494-...:2844c731-...` with `:` replaced by `+` names the orca-tabs file, whose line 3 is the `assigneeHandle` `term_1a6fde09-...` (`lc16-show-4.json:11-12`; `qa/qa-research-verification.md:28`). Whether the sweep uses it for person-started sessions is GQ-09. |
| GQ-19 | Known gap 2: fix `sc-crash-recovery/scripts/bootstrap_scan.sh` or write a new scanner | Important (`research/research-notes.md:273`) | `research/scope-02-orca-recovery.md` Q6 `:228`; `research/research-notes.md:160`, `:273` | open (plan decision) | Known bugs: `:31` encoding, `:73` treats `.git` as a directory (fails for a worktree's `.git` file), `:136` JSON escaping. Option A4 (reuse crash-recovery as-is) is CODE-CONTRADICTED (`research/research-notes.md:160`); nothing builds on A4 (`qa/qa-research-verification-qualitative-cycle1.md:53`). |
| GQ-20 | `stage.activity` as a work signal | Minor | `research/scope-02-orca-recovery.md` Q7 `:229`; `research/05-orca-row-schema.md` Gap 7 `:192`; `research/research-notes.md` C5 `:323` | resolved | [CODE-CONTRADICTED]: `stage.activity` stays "working" after settlement (`lc17-show-1.json:132`, `lc01-show-1.json:132`); not used as a signal. Whether it ever changes is unknown. |
| GQ-21 | Exclude `git stash *` and `ccsession --list` from the sweep | Important | `research/scope-02-orca-recovery.md` Q8 `:230`; `research/research-notes.md` C3 `:321` | open (plan decision) | crash-recovery is not "pure read-only" (`git stash *` in `sc-crash-recovery/SKILL.md:4`, CODE-CONTRADICTED); `ccsession --list` writes (cited in scope-02). research-notes lists `ccsession --list` among excluded sources. |
| GQ-22 | Cost of `--include-remote` | Minor | `research/scope-02-orca-recovery.md` Q9 `:231` | open | [UNVERIFIED]; remote rows read `unverifiable` without it (05 `:163`). |
| GQ-23 | Known gap 4: lazy versus eager start (package `__init__` import) of the Orca client in the CLI | Important (`research/research-notes.md:273`) | `research/scope-03-cli-patterns.md` OQ1 `:206`; `research/research-notes.md:273` | open (plan decision) | Both patterns exist: lazy `__getattr__` at `recommend/__init__.py:12-20` (scope-03 recommends it), eager imports at `reflect/__init__.py:17-30`. |
| GQ-24 | "Other commands" versus the excluded set in HOW-WE-WORK routing (AMBIGUITY 7 in part) | Minor | `research/scope-03-cli-patterns.md` OQ2 `:207`; `research/research-notes.md:309`; `qa/qa-consolidated-findings-phase3.md` N-37 | open (plan) | `test_how_we_work_routing_table.py:299-309`. N-37: `commands/README.md:10` step 4 also allows the routing table, which scope-03 did not analyse (`test_how_we_work_routing_table.py:186-259`, `:314-340`). |
| GQ-25 | Known gap 3: `uv run superclaude` outside a uv project (pipx installs) | Important (`research/research-notes.md:273`) | `research/scope-03-cli-patterns.md` OQ3 `:208`; `research/research-notes.md:157`, `:273`; `qa/qa-consolidated-findings-phase3.md` B-19; `qa/qa-research-verification-qualitative.md:38` NB-3 | open (decision made; runtime check pending) | Decision (B-19): bare `superclaude sweep ...` on PATH first, `uv run superclaude sweep ...` only as the dev-checkout fallback, both in `allowed-tools`, a static test pins the order. Pipx PATH behaviour stays [UNVERIFIED] until the plan runs `superclaude sweep --help` once outside a uv project. |
| GQ-26 | How command-file `allowed-tools` patterns combine | Minor | `research/scope-03-cli-patterns.md` OQ4 `:209` | open | [UNVERIFIED]; OQ4 now lists `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)` (NB-3 fix, `qa/qa-research-verification-cycle1.md:22`). |
| GQ-27 | Where the Orca probe module lives | Minor | `research/scope-03-cli-patterns.md` OQ5 `:210` | open (plan) | Pattern to follow: one `_orca(*args)` seam modelled on `reflect/config.py:64-78` (`qa/qa-research-verification.md:32`). |
| GQ-28 | Whether a test pins the UTILITIES table | Minor | `research/scope-03-cli-patterns.md` OQ6 `:211` | open | [UNVERIFIED]. |
| GQ-29 | #409 layout: sort tie-break (AMBIGUITY 9) | Minor | `research/scope-04-409-layout.md` Q1 `:356`; `research/research-notes.md:311` | open | #409 sort rule is only partly age-ranked (C6, `agent_focus.py:46`). |
| GQ-30 | #409 layout: what counts as closure evidence | Minor | `research/scope-04-409-layout.md` Q3 `:358` | open | Plan decision. |
| GQ-31 | #409 layout: print every source's coverage | Minor | `research/scope-04-409-layout.md` Q4 `:359` | open | Plan decision; GQ-02 already requires "Messages coverage: partial". |
| GQ-32 | #409 layout: the scope line | Minor | `research/scope-04-409-layout.md` Q5 `:360` | open | Plan decision. |
| GQ-33 | #409 layout: omission bound for a static file | Minor | `research/scope-04-409-layout.md` Q6 `:361` | open | #409 wide-view omission counts are CODE-CONTRADICTED (C7, `agent_focus.py:46-50`, `:164-167`). |
| GQ-34 | #409 layout: Approval label and its `gate-list` mapping (AMBIGUITY 9) | Minor | `research/scope-04-409-layout.md` Q7 `:362`, `:345`; `research/research-notes.md:311`; `research/07-gate-gap-fill.md` B; `qa/qa-consolidated-findings-phase3.md` N-36 | open | The gate-list to Approval mapping is [UNVERIFIED] (07 B). `gate-list` itself is a plain read (07 B), so N-36 is answered; its use depends on GQ-03. |
| GQ-35 | #409 version pinning (`495eb96d`, unmerged) (AMBIGUITY 9) | Minor | `research/scope-04-409-layout.md` Q8 `:363`; `research/research-notes.md:311` | open | #409 is not on master; the layout is read from `git show 495eb96d`. |
| GQ-36 | Shape of a non-null `agentWait` | Minor | `research/05-orca-row-schema.md` Gap 2 `:187`, Answer (3) `:161` | open | [UNVERIFIED] beyond "evidence kind hook / prompt-text / title" (`[H:worker-show]` 16). Three states documented: object, `null`, absent. |
| GQ-37 | `unverifiable` and `exited` verdicts never captured | Important (Section C rules 2 and 7 depend on them) | `research/05-orca-row-schema.md` Gap 4 `:189`; `qa/qa-consolidated-findings-phase3.md` N-29 | open | Meanings and the six reason codes are guide text only (`[G:recovery]` 34-38, 58-59). N-29: resolve by capturing a live stalled row. |
| GQ-38 | `page.hasMore` past 100 rows | Minor | `research/05-orca-row-schema.md` Gap 5 `:190` | open | Proven only for an empty page (`lc01-step7.txt:35`). The sweep pages on `page.nextCursor` and passes `--run` (05 `:163`). |
| GQ-39 | `counts` keys other than `released` | Minor | `research/05-orca-row-schema.md` Gap 6 `:191` | open | [UNVERIFIED] (`lc01-step7.txt:30`). |
| GQ-40 | Nested workers: guide `[G]` 130-131 (workers start helpers) versus `orca-capabilities.md:97-102` (depth 1 forbids it) (C15) | Important | `research/05-orca-row-schema.md` Gap 8 `:193`, `:202`; `research/research-notes.md` C15 `:333`; `research/06-orca-open-questions.md` Gap 16 `:173`; `qa/qa-consolidated-findings-phase3.md` B-06 | open (Orca behaviour); resolved for the sweep | Which matches Orca is [UNVERIFIED]. The sweep reports a non-null worker-show `parent` (`lc16-show-4.json:115`) as a WC-13 violation for review (`WORKER-CONTRACT.md:39`, `:61`); a helper's question never reaches the coordinator directly (06 `:173`). B-06 RESOLVED (`qa/qa-research-verification.md:25`). |
| GQ-41 | CLI version of the captures not recorded | Minor | `research/05-orca-row-schema.md` Gap 9 `:195` | open | Captures predate 1.4.245. [UNVERIFIED] |
| GQ-42 | Other read surfaces (`run-list`, `run-current`, `task-list`, `gate-list`, `inbox`) | Important | `research/05-orca-row-schema.md` Gap 10 `:194`; `research/07-gate-gap-fill.md` B; `qa/qa-consolidated-findings-phase3.md` B-07 | resolved | All plain reads on the CLI side; only `run-list` paged (100, `--cursor`); `inbox` read-marking [UNVERIFIED], so not used. B-07 RESOLVED (`qa/qa-research-verification.md:26`). Allowlist follow-up is GQ-03. |
| GQ-43 | Whether plain `check` marks rows read | Important | `research/06-orca-open-questions.md` Gap 1 `:158` | open | [UNVERIFIED]; the CLI sends every check through `callOrchestrationMutation` (`message-check-handler.js:30`). Design treats plain `check` as draining and forbids it. |
| GQ-44 | Whether `check --peek` / `check --all` are side-effect-free | Important | `research/06-orca-open-questions.md` Gap 2 `:159`, `:72`; `research/07-gate-gap-fill.md` C | open | Not side-effect-free by construction: older runtimes ignore `--peek` (`:17`), both modes can trigger `compatibilityAck` (`:58-71`). Default is contracts only; `check` is a gated addition at `scope-03:99` (NB-2 fix, `qa/qa-research-verification-cycle1.md:21`). |
| GQ-45 | Semantics of `check --unread` | Important | `research/06-orca-open-questions.md` Gap 3 `:160` | resolved | [CODE-VERIFIED]: sets `unread: true` (`message-check-handler.js:33-34`), destructive with `--peek` on older runtimes (`:17`). Forbidden. |
| GQ-46 | Whether `orchestration inbox` marks messages read, and its row cap | Minor | `research/06-orca-open-questions.md` Gap 4 `:161`, `:75` | open | [UNVERIFIED] runtime side; CLI side is a plain read (`message-inbox-handlers.js:20-25`). Not used; stays forbidden (GQ-03). |
| GQ-47 | Whether `reply` changes a question's read or answered state | Minor | `research/06-orca-open-questions.md` Gap 6 `:163`; `qa/qa-consolidated-findings-phase3.md` B-16 | open | [UNVERIFIED]; the sweep reports "answered: could not determine". Gap 5 (question-reply link) is merged into GQ-02. |
| GQ-48 | Non-consuming enumeration past 100 rows | Important | `research/06-orca-open-questions.md` Gap 7 `:164`, `:73`; `qa/qa-consolidated-findings-phase3.md` B-18 | open | [UNVERIFIED]; `--all` and Run `--peek` cap at 100 with no cursor (`[H:check]:37`). A 100-row result is reported as "could not determine: message listing truncated at 100". |
| GQ-49 | Meaning of `ask --dispatch-capability` | Minor | `research/06-orca-open-questions.md` Gap 8 `:165` | open | [UNVERIFIED] (`[H:ask]:16`). |
| GQ-50 | Whether a peer session can `ask --to run:<id>` and how it shows | Minor | `research/06-orca-open-questions.md` Gap 9 `:166`; `qa/qa-consolidated-findings-phase3.md` N-35 | open | [UNVERIFIED]. N-35: pending `ask` questions wait on the coordinator, not a person; only unresolved escalations become "waiting on a person". |
| GQ-51 | Whether `--agent-wait` / the `agentWait` probe sends anything to the agent's terminal | Minor | `research/06-orca-open-questions.md` Gap 10 `:167`; `qa/qa-consolidated-findings-phase3.md` B-15 | open | [UNVERIFIED]; `--agent-wait` is excluded from the sweep (B-15). |
| GQ-52 | Whether Orca sets `agentWait` on a worker blocked in `ask` | Minor | `research/06-orca-open-questions.md` Gap 11 `:168` | open | [UNVERIFIED]; until settled a non-null `agentWait` is "waiting on a person", not a breach. |
| GQ-53 | Why `status --json` showed no `caller` for a dispatched worker | Minor | `research/06-orca-open-questions.md` Gap 13 `:170` | open | [UNVERIFIED]; inventory open item 10 (`orca-capabilities.md:185`). |
| GQ-54 | Cross-host owner / session / worktree joins for peer rows | Minor | `research/06-orca-open-questions.md` Gap 14 `:171` | open | [UNVERIFIED] (integration-gaps line 12). |
| GQ-55 | Meaning of `check --format` | Minor | `research/06-orca-open-questions.md` Gap 15 `:172`; `research/07-gate-gap-fill.md` C(f) | resolved | [CODE-VERIFIED]: a local text switch (`message-check-handler.js:38`, `:55`; `orchestration-check-output.js:49-59`); `[H:check]:28` is a mislabel. Not used. |
| GQ-56 | Whether `check --all` returns `run:<id>` rows, and which end the 100-row cap keeps on a current runtime | Important | `research/06-orca-open-questions.md` Gap 17 `:174`, `:74` | open | [UNVERIFIED]; older runtimes keep the newest 100 (`message-check-handler.js:82-83`). Feeds GQ-02. |
| GQ-57 | Whether a `--peek` / `--all` result can carry `legacyCompatibility.ackMessageIds` (CLI then sends a `compatibilityAck`) | Important | `research/06-orca-open-questions.md` Gap 18 `:175`; `research/07-gate-gap-fill.md` C | open | [UNVERIFIED]; resolve by reading the runtime handler under `out/main/chunks/` or a throwaway-Run test. Until then any `check` is possibly state-changing. |
| GQ-58 | Meaning of a null `agentWait`: help versus guide | Important | `research/06-orca-open-questions.md` Gap 19 `:176`, `:144`; `research/research-notes.md:198`; `qa/qa-consolidated-findings-phase3.md` B-10 | open | `[H:worker-show]:16` "looked and found no wait" versus `[G:recovery]:58-61` "same absence seen again". Sweep rule: null = no wait observed, valid for working, never stall proof; absent = could not determine. |
| GQ-59 | Runtime-version or `legacyCompatibility` probe before trusting `--peek` | Important | `research/06-orca-open-questions.md:72` constraint (3); `research/07-gate-gap-fill.md` C | open | No read-only verb that reports the runtime version was found; probe [UNVERIFIED]. |
| GQ-60 | Where the sweep logic lives (A1-A4) (AMBIGUITY 1) | Important | `research/research-notes.md:303`, `:153-162` | open (leaning A1) | A1: CLI `superclaude sweep` plus a thin skill; A4 CODE-CONTRADICTED (`:160`). |
| GQ-61 | Default window 6 h versus 72 h (AMBIGUITY 2, F11) | Important | `research/research-notes.md:304`; `qa/qa-consolidated-findings-phase3.md` N-41 | open (owner decision) | The window should bound activity only, not open Tasks or unread reports (N-41). |
| GQ-62 | Sequencing with PR #422 (AMBIGUITY 5, F8) | Minor | `research/research-notes.md:307` | open | Owner decision. |
| GQ-63 | `pragmatic` DONE/NEXT rule has "No exceptions" and no exception mechanism (AMBIGUITY 6, F10) | Important | `research/research-notes.md:308`; `research/07-gate-gap-fill.md` A; `qa/qa-consolidated-findings-phase3.md` B-04 | open (owner decision) | `pragmatic.md:22`, `:53`; `launch-job-identity.sh` sets no environment variable. B-04 RESOLVED as evidence (`qa/qa-research-verification.md:23`); the decision stays open. |
| GQ-64 | Whether `identify` writes state | Minor | `research/07-gate-gap-fill.md` A | open | [UNVERIFIED]. |
| GQ-65 | `task-list` and `gate-list` row caps | Minor | `research/07-gate-gap-fill.md` B | open | [UNVERIFIED]; only `run-list` is known to page. |
| GQ-66 | "Management server" meaning (AMBIGUITY 10, F14) | Minor | `research/research-notes.md:312` | open | Owner clarification. |
| GQ-67 | Worktree-first versus trigger-based placement (AMBIGUITY 11, F12); CR-01 unread | Minor | `research/research-notes.md:313`; `qa/qa-consolidated-findings-phase3.md` N-02 | open | CR-01 was not read (N-02). |
| GQ-68 | B-02: "safe to close" treated as a class | Important | `qa/qa-consolidated-findings-phase3.md` B-02 | resolved | A separate two-part REVIEW dimension (terminal releasable / worktree removable): `research/scope-02-orca-recovery.md:103`, `:237` (`qa/qa-research-verification.md:21`). Wording residual GQ-87. |
| GQ-69 | B-03: bare verb form instead of `orca-ide orchestration <verb>` | Important | `qa/qa-consolidated-findings-phase3.md` B-03 | resolved | C13 CODE-VERIFIED (`research/research-notes.md:331`); bare form CODE-CONTRADICTED at `research/scope-02-orca-recovery.md:16`, `:235-236` (`qa/qa-research-verification.md:22`). Residual GQ-85. |
| GQ-70 | B-05 / NB-1: stalled without proof that the turn was final; fenced evaluated after stalled | Important | `qa/qa-consolidated-findings-phase3.md` B-05; `qa/qa-consolidated-findings-phase3-cycle1.md` NB-1; `qa/qa-research-verification-qualitative.md:36` | resolved | Rule 2 now needs positive stop proof and carries the fenced exclusion (`research/research-notes.md:193`); copies at `05:172-173`, `06:137`, `scope-02:107` (`qa/qa-research-verification-qualitative-cycle1.md:21`). Edge case GQ-84. |
| GQ-71 | B-11: "waiting on a person" not split into kinds | Important | `qa/qa-consolidated-findings-phase3.md` B-11 | resolved | Rule 4 (a) explicit question, (b) frozen or blocked by policy (`research/research-notes.md:195-197`); `scope-04:285-286`, `:318` (`qa/qa-research-verification.md:30`). |
| GQ-72 | B-12: class versus report dimensions; every class needs a report home | Important | `qa/qa-consolidated-findings-phase3.md` B-12 | resolved | `research/scope-04-409-layout.md:320-332` (`qa/qa-research-verification-qualitative-cycle1.md:31`). Residual GQ-91. |
| GQ-73 | B-13 / NB-2: no test proving the sweep's Orca calls are read-only; allowlist combined read modes, allowed `check` ungated, stated read-marking as fact | Important | `qa/qa-consolidated-findings-phase3.md` B-13; `qa/qa-consolidated-findings-phase3-cycle1.md` NB-2; `qa/qa-research-verification-qualitative.md:37` | resolved | `research/scope-03-cli-patterns.md:99`: local-write proof (`test_contract_status_cli.py:44-66`) plus an `_orca(*args)` argv-allowlist test; `check --peek` / `--all` separate and probe-gated, read-marking [UNVERIFIED] (`qa/qa-research-verification-qualitative-cycle1.md:22`). The allowlist's missing verbs are GQ-03 (NB-4). |
| GQ-74 | B-14: missing report columns (Approval, Evidence, Tests/review) | Important | `qa/qa-consolidated-findings-phase3.md` B-14 | resolved | `research/scope-04-409-layout.md:293`, per-column sources `:336-351` (`qa/qa-research-verification.md:33`). |
| GQ-75 | B-20: untagged doc claims in 05 | Important | `qa/qa-consolidated-findings-phase3.md` B-20 | resolved | 05 `:43-48` now tagged (`qa/qa-research-verification.md:39`). |
| GQ-76 | B-21: "no test globs every skill" | Important | `qa/qa-consolidated-findings-phase3.md` B-21 | resolved | Suite-wide scans listed at `research/scope-03-cli-patterns.md:152-157`; old claim struck as [CODE-CONTRADICTED] at `:165` (`qa/qa-research-verification.md:40`). |
| GQ-77 | B-22: "drained only by `--ack`" | Important | `qa/qa-consolidated-findings-phase3.md` B-22 | resolved | Check modes are help-documented; runtime read-marking [UNVERIFIED] (`06:72`, `:158-159`; `qa/qa-research-verification-qualitative-cycle1.md:32`). |
| GQ-78 | B-23: false STALE DOC for `orca-capabilities.md:58` | Important | `qa/qa-consolidated-findings-phase3.md` B-23 | resolved | `:58` removed from the stale bullet (`06:181`; `qa/qa-research-verification.md:42`). |
| GQ-79 | B-24: check-mode claims without handler evidence | Important | `qa/qa-consolidated-findings-phase3.md` B-24 | resolved | 06 relabel rule `:16`, constraints `:72`; `07` C(a)-(g) (`07:57-65`) (`qa/qa-research-verification.md:43`). Residual GQ-88. |
| GQ-80 | B-25: "agentWait is the only non-consuming signal" stated as fact | Important | `qa/qa-consolidated-findings-phase3.md` B-25 | resolved | 05 Answer (1) corrected (`05:157`) (`qa/qa-research-verification.md:44`). Residual GQ-95. |
| GQ-81 | B-26: read path for each "waiting on a person" case | Important | `qa/qa-consolidated-findings-phase3.md` B-26 | resolved | `research/scope-02-orca-recovery.md:99-109`, `scope-04:328` (`qa/qa-research-verification.md:45`). Residual GQ-93. |
| GQ-82 | B-27: lint-architecture gates the new files must pass | Important | `qa/qa-consolidated-findings-phase3.md` B-27 | resolved | `research/scope-03-cli-patterns.md:143-150` lists Checks 1-11 (Makefile `:362-489`) (`qa/qa-research-verification.md:46`). |
| GQ-83 | NB-3: option A1 and OQ4 kept the uv-only call form after the B-19 decision | Important | `qa/qa-research-verification-qualitative.md:38` | resolved | `research/research-notes.md:157` and `research/scope-03-cli-patterns.md:109`, `:209` now PATH first plus both forms (`qa/qa-research-verification-qualitative-cycle1.md:23`). The runtime check is GQ-25. |
| GQ-84 | Fenced exclusion when an `exited` row's transcript cannot be read: rule 2 fires before rule 7 | Minor | `qa/qa-research-verification-cycle1.md:60` (M1); `qa/qa-research-verification-qualitative-cycle1.md:46` | open (plan) | Plan should state that rule 2 needs the transcript read; exited, no `worker_done`, unreadable transcript gives could not determine. Not a WC-10 break. |
| GQ-85 | `scope-03:99` mixes full and bare verb forms | Minor | `qa/qa-research-verification-qualitative-cycle1.md:47` | open (plan) | An argv-pinning test must use `orca-ide orchestration <verb>` (C13). |
| GQ-86 | `scope-03:99` says `check --unread` is destructive, but `message-check-handler.js:17` says the `--unread --peek` combination is | Minor | `qa/qa-research-verification-cycle1.md:61` (M2) | open | Wording only; `--unread` is forbidden either way. |
| GQ-87 | `scope-01:64` still calls safe-to-close a "class" | Minor | `qa/qa-research-verification.md:57` (N1); `qa/qa-research-verification-qualitative.md:48` | open | Wording only; it is a dimension (`scope-02:237`). |
| GQ-88 | `06:57-58` tag `--ack` and `--wait` rows [CODE-VERIFIED] on help text only | Minor | `qa/qa-research-verification.md:58` (N2) | open | Should be [UNVERIFIED] / help-only per 06 `:16`. |
| GQ-89 | `06:187` original Summary is stale (inbox / `--unread` "undocumented", `worktree ps --agent-wait`) | Minor | `qa/qa-research-verification.md:59` (N3); `qa/qa-research-verification-qualitative.md:50` | open | Superseded by `06:189`; not marked superseded. |
| GQ-90 | `filterLegacyPeekResult` (`message-check-handler.js:74-95`) runs on every peek, not only on legacy runtimes | Minor | `qa/qa-research-verification.md:60` (N4) | open | Not recorded in 06. |
| GQ-91 | `scope-04:290` Retained problems omits stalled / could not determine; `:320` maps a stale row against rule 6 | Minor | `qa/qa-research-verification.md:61` (N5); `qa/qa-research-verification-qualitative.md:49` | open | Section C rule 6 governs. |
| GQ-92 | "Needs a human" / "needs-a-human" wording left at `research-notes.md:225` and `scope-04:356` | Minor | `qa/qa-research-verification.md:62` (N6); `qa/qa-research-verification-qualitative.md:43` | open | Canonical term is "waiting on a person". |
| GQ-93 | `research-notes.md:175`, `:196` point to G-A for the pending-`ask` read; the gap is G-B | Minor | `qa/qa-research-verification.md:63` (N7); `qa/qa-research-verification-qualitative.md:42`; `qa/qa-research-verification-qualitative-cycle1.md:48` | open | Confirmed still unchanged in cycle 1 (grep this pass: `research-notes.md:175`, `:196`). |
| GQ-94 | `research-notes.md:241-242` still list 05 and 06 as "MISSING, planned" | Minor | `qa/qa-research-verification.md:64` (N8, N-01 carry-over) | open | Both files exist. |
| GQ-95 | Conservative default phrased as fact at `05:165` and `scope-01:142` | Minor | `qa/qa-research-verification.md:65` (N9); `qa/qa-research-verification-qualitative.md:45` | open | `05:165` says "because `agentWait` is only on worker-show" while `:157` says that is UNVERIFIED. Same design outcome. |
| GQ-96 | A blocked `/sc:implement` contract fits both waiting kinds (a) and (b) | Minor | `qa/qa-research-verification.md:66` (N10) | resolved | Accepted: dimensions are independent. |
| GQ-97 | Small citation residuals: `research-notes.md:182` should cite 06 Gap 1; 05 lists Gap 10 before Gap 9; `05:178` gives worker-show as the source for a missing contract (it is a file read, `research-notes.md:176`); `05:174` source column says "row" for transcript proof | Minor | `qa/qa-research-verification-qualitative.md:44`, `:46`, `:47`; `qa/qa-consolidated-findings-phase3.md` N-39 | open | Wording and ordering only. |
| GQ-98 | `[G:recovery]` row 9 "Start a replacement with `--retry-of`" conflicts with WC-6 | Minor | `qa/qa-consolidated-findings-phase3.md` N-33 | open | WC-6 settles it: a retry is a new Task, never `--retry-of`. |
| GQ-99 | N worker-show calls per sweep versus the Bash inspection batching policy and a per-sweep call bound | Minor | `qa/qa-consolidated-findings-phase3.md` N-40 | open (plan) | Follows from GQ-01's worst case. |
| GQ-100 | APPROVED.md decision texts (D1-D5) and the ccsession-tag README not verified | Minor | `qa/qa-consolidated-findings-phase3.md` N-02; `research/scope-01-contract.md` (UV tags) | open | scope-01 tags the APPROVED.md decision texts [UNVERIFIED]. |
| GQ-101 | NB-2 (Phase 6 anti-omission gate): the report's one-package-in-two-worktrees pre-pass (step 1.3 rule (i), `mark_shared_packages`) counts committed `.dev/tasks/{to-do,done}/*/` folders, which every worktree shares (master has 44 to-do and 26 done folders), so nearly every worktree would be flagged not removable. The source rule is about a package being run in two worktrees. | Important | `src/superclaude/core/WORKER-CONTRACT.md:108`; `qa/qa-anti-omission-verification-qualitative-cycle1.md` NB-2 | open (plan, fix at /sc:design) | Owner decision 2026-11-08: carried as an open gap, no further fix pass. Fix at /sc:design: count only packages actually running in a worktree (a ledger or folder that differs from the base branch), ignore unchanged committed packages, let the line name 3 or more worktrees, and add a shared-folders fixture asserting no flag. |
| GQ-102 | NB-4c (Phase 6 anti-omission gate): a package folder present in both `to-do/` and `done/` is a conflict state; the report's package states (step 1.2 `archive_states`, step 1.3 rule (iii)) lack it | Important | `~/.claude/skills/sc-crash-recovery/refs/pipelines.md:198`; `~/.claude/skills/sc-implement-protocol/SKILL.md:39` (`E-MANAGED-CONFLICT`); `qa/qa-anti-omission-verification-qualitative-cycle1.md` NB-4c | open (plan, fix at /sc:design) | Owner decision 2026-11-08: carried as an open gap, no further fix pass. Fix at /sc:design: add "conflict" as a fourth package state that blocks worktree removal, plus a fixture and a test. |
| GQ-103 | /ponytail-review of the Phase 1 plan (owner request, 2026-11-08), 3 blocking: (1) plain `git status` can take a worker's `index.lock`, and WC-9 tells a worker that finds it to report `blocked`; (2) `classify` is not given the `--window` value; (3) the step 1.2 types lack fields the rule-1 and GQ-84 tests read (brief blocked-gate policy, `worker_done`, transcript readable, contract `report_path` / `artifacts`) | Important | `qa/ponytail-review-phase1-plan.md` findings 1-3; `src/superclaude/core/WORKER-CONTRACT.md:44` (WC-9 `index.lock`) | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816): carried as an open gap, no fix pass. Required plan fixes at /sc:design: (1) SAFETY ITEM, the design must carry it first: run every `_git` call with `--no-optional-locks`, so a sweep never makes a live worker report a false `blocked` under WC-9; (2) pass the window into `classify`; (3) add the missing fields. The review's 7 minor findings are GQ-104 to GQ-110. |
| GQ-104 | /ponytail-review finding 4: the fallback to every Run from `run-list` spends the 50-call `worker-show` bound on history | Minor | `qa/ponytail-review-phase1-plan.md` finding 4 | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816). Fix: delete the `run-list` fallback; with no `--run` and no `run-current` binding, exit 2 asking for `--run <id>`. |
| GQ-105 | /ponytail-review finding 5: "archive-blocked" cannot be read from `progress.md` alone | Minor | `qa/ponytail-review-phase1-plan.md` finding 5 | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816). Fix: archive-blocked = package in `to-do/` whose `progress.md` has a `FINAL:` line; add one step 1.9 case for an unfinished ledger. |
| GQ-106 | /ponytail-review finding 6: reports under `<root>/.dev/sweeps/` are untracked, so each sweep makes its own worktree look dirty | Minor | `qa/ponytail-review-phase1-plan.md` finding 6 | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816). Fix: add `.dev/sweeps/` to `.gitignore` and to the rollback table. |
| GQ-107 | /ponytail-review finding 7: `sanitize()` does not escape the Markdown table separator `\|` | Minor | `qa/ponytail-review-phase1-plan.md` finding 7 | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816). Fix: escape `\|` in `sanitize()` and add one case to the step 1.12 injection fixture. |
| GQ-108 | /ponytail-review finding 8: no rule defines a "person-started" session (this host has 347 transcripts) | Minor | `qa/ponytail-review-phase1-plan.md` finding 8 | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816). Fix: one step 1.3 rule: a transcript under a scanned root's project key that the tab map joins to no Orca row; older than the window goes to Historical sessions. |
| GQ-109 | /ponytail-review finding 9 (lean): three allowlisted reads (`gate-list`, `worker-read`, stash) feed nothing in Phase 1 | Minor | `qa/ponytail-review-phase1-plan.md` finding 9 | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816). Fix: drop them from the step 1.4 allowlist, step 1.0a and step 1.10 until a phase uses them. |
| GQ-110 | /ponytail-review finding 10 (lean): one `git status --porcelain --branch` call answers three worktree conditions | Minor | `qa/ponytail-review-phase1-plan.md` finding 10 | open (plan, required fix at /sc:design) | Owner decision 2026-11-08 (msg_22c5c0692816). Fix: one call per worktree, parsed once; collapse the step 1.8 `patch_git` fixtures. |
| GQ-111 | Stale report citation (reflection D-1, Medium): report lines 229, 597, 1127, 1474 and 1496 cite `gaps-and-questions.md:125` with the old count ("Open 75 / Resolved 25"). Line 125 is now the GQ-102 row; the row count is at line 138 of this file: 113 rows, 88 open, 25 resolved | Medium | `reflect/post/REPORT.md` D-1 (R-1) | open (known stale citation, carried; report not edited) | Coordinator decision 2026-11-08 (msg_47abd629a610): carried as a known stale citation, no report edit outside a gate. Fix when the report is next edited: re-anchor to the row-count line and use the current counts. |
| GQ-112 | Stale report citation (reflection D-2, Low): report line 1754 cites the gaps log count as "GQ-01 to GQ-103; 78 open, 25 resolved (`:125`)". Correct now: line 138, GQ-01 to GQ-113, 88 open, 25 resolved | Low | `reflect/post/REPORT.md` D-2 (R-2) | open (known stale citation, carried; report not edited) | Coordinator decision 2026-11-08 (msg_47abd629a610): carried, no report edit. |
| GQ-113 | Stale report claim (reflection D-13, Low): report line 1537 says "Every open GQ row is cited", but GQ-101 to GQ-113 were added after it and are not cited in the report | Low | `reflect/post/REPORT.md` D-13 (R-5) | open (known stale citation, carried; report not edited) | Coordinator decision 2026-11-08 (msg_47abd629a610): carried, no report edit. Read the sentence as covering GQ-01 to GQ-100 only. |

**Row count:** 113 rows. Open: 88. Resolved: 25. (GQ-104 to GQ-110 were added after the Phase 6 gates by owner decision msg_22c5c0692816, and GQ-111 to GQ-113 record stale report citations by coordinator decision msg_47abd629a610; the report's Gaps Log still says "GQ-01 to GQ-103; 78 open" because the owner ruled out report edits outside a gate.) Resolved list (GQ-03, 07, 13, 18, 20, 42, 45, 55, 68-83, 96). GQ-40 is counted as open although its sweep-side rule is settled. Open Critical: GQ-01, GQ-02, GQ-04, GQ-06. Open blocking QA finding: none at the research and synthesis gates; GQ-03 (NB-4) was fixed by the NB-4 fix pass (`qa/qa-nb4-fix-log.md`) and is re-checked at the Phase 5 synthesis gate. Phase 6 anti-omission gate: GQ-101 (NB-2) and GQ-102 (NB-4c) are open blocking findings carried by owner decision to /sc:design; GQ-103 adds the 3 blocking /ponytail-review findings.

**Coverage of the six gaps sections:** scope-01 Q1-Q7 -> GQ-01, 11, 12, 10, 13, 14, 09; scope-02 Q1-Q9 -> GQ-01, 15, 16, 17, 18, 19, 20, 21, 22; scope-03 OQ1-OQ6 -> GQ-23, 24, 25, 26, 27, 28; scope-04 Q1-Q8 -> GQ-29, 02, 30, 31, 32, 33, 34, 35; 05 Gaps 1-10 -> GQ-01, 36, 15, 37, 38, 39, 20, 40, 41, 42; 06 Gaps 1-19 -> GQ-43, 44, 45, 46, 02, 47, 48, 49, 50, 51, 52, 17, 53, 54, 55, 40, 56, 57, 58. B-01 and B-28 -> GQ-07; B-04 -> GQ-63; B-06 -> GQ-40; B-07 -> GQ-42; B-08 -> GQ-01; B-09 -> GQ-18; B-10 -> GQ-58; B-15 -> GQ-51; B-16 -> GQ-47; B-17 -> GQ-02; B-18 -> GQ-48; B-19 -> GQ-25; every other B- and NB- finding has its own row.

---

## (b) The four known non-critical gaps

Source: `research/research-notes.md:273` ("Important but not Critical ... synthesis handles them as open questions, no agent").

| # | Gap | Table row | Status | Evidence |
|---|---|---|---|---|
| K1 | Join from an Orca pane key (`dispatch.assigneePaneKey`) to a ccsession transcript (`orca-tabs`) | GQ-18 | resolved for one worker; reporting person-started sessions stays an owner decision (GQ-09) | `research/07-gate-gap-fill.md` D; `research/research-notes.md` C12 `:330`: lc16 `assigneePaneKey` with `:` replaced by `+` names the orca-tabs file, whose line 3 is the `assigneeHandle` (`lc16-show-4.json:11-12`). One worker only, so the plan should still check a second worker. |
| K2 | Reuse `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` (`:31`, `:73`) or write a new scanner | GQ-19 | open (plan decision) | `research/scope-02-orca-recovery.md` Q6 `:228`: bugs at `:31` (encoding), `:73` (`.git` file in a worktree), `:136` (JSON escaping). research-notes lists "bootstrap_scan.sh as-is" among excluded sources, and option A4 is CODE-CONTRADICTED (`research/research-notes.md:160`). |
| K3 | `uv run superclaude` outside a uv project (pipx installs) | GQ-25 | open (decision made, runtime unverified) | `research/scope-03-cli-patterns.md` OQ3 `:208`: PATH form `superclaude sweep ...` first, `uv run` only in a dev checkout, both in `allowed-tools`. Pipx behaviour [UNVERIFIED] until `superclaude sweep --help` runs once outside a uv project. |
| K4 | Lazy versus eager start of the Orca client in the CLI | GQ-23 | open (plan decision) | No research file studies an Orca client object; the closest evidence is package-import style, `research/scope-03-cli-patterns.md` OQ1 `:206`: lazy `__getattr__` (`recommend/__init__.py:12-20`, recommended) versus eager (`reflect/__init__.py:17-30`). The probe seam itself is GQ-27. |

---

## (c) AMBIGUITIES 1-11

Source: `research/research-notes.md:303-313` (item N at line 302+N).

| # | Ambiguity | Current status | Table row |
|---|---|---|---|
| 1 | Where the logic lives (A1-A4) | open, leaning A1 (CLI `superclaude sweep` called by a skill, `:157`); A4 CODE-CONTRADICTED (`:160`) | GQ-60 |
| 2 | Default window 6 h versus 72 h (F11) | open owner decision; the window bounds activity only (N-41) | GQ-61 |
| 3 | Report location | open owner decision | GQ-10 |
| 4 | Rule ID WC-14 versus WC-1 | open owner decision; WC-14 is the working name | GQ-11 |
| 5 | Sequencing with PR #422 (F8) | open | GQ-62 |
| 6 | `pragmatic` DONE/NEXT exception (F10) | open owner decision; evidence settled by `07` A ("No exceptions", no mechanism) | GQ-63 |
| 7 | Routing placement, `_POST_REFRESH_ADDITIONS`, never-as-worker list (F6, F7) | open plan decision; the routing-table option is also allowed (N-37) | GQ-12, GQ-24 |
| 8 | Person-started sessions (F2) | open owner decision; the evidence route is verified for one worker | GQ-09, GQ-18 |
| 9 | #409 pinning, sort tie-break, approval label | open; #409 is still unmerged at `495eb96d` | GQ-29, GQ-34, GQ-35 |
| 10 | "Management server" (F14) | open, needs owner clarification | GQ-66 |
| 11 | Worktree-first versus trigger-based placement (F12) | open; CR-01 unread (N-02) | GQ-67 |

---

## (d) C1-C12 and their current tags

Source: `research/research-notes.md:319-330` (C N at line 318+N). C13-C15 (`:331-333`) are listed after them for completeness.

| # | Claim | Current tag | Note |
|---|---|---|---|
| C1 | scope-01's F1-F12 numbering of the analysis findings | [CODE-CONTRADICTED] | The analysis now has F1-F14 and S1-S5 (`.dev/issues/339/analysis/analyze-worker-contract.md:30-55`); use the current numbers. |
| C2 | `tests/core/test_how_we_work_routing_table.py` is about 360 lines | [CODE-CONTRADICTED] | `wc -l` gives 1202. |
| C3 | sc-crash-recovery is read-only | [CODE-CONTRADICTED] | allowed-tools includes `Bash(git stash *)` (`sc-crash-recovery/SKILL.md:4`) (GQ-21). |
| C4 | crash-recovery `--all` scans `~/workspace/` | [CODE-CONTRADICTED] on this host | Worktrees live under `~/workspaces/` (`SKILL.md:25-27`). |
| C5 | `stage.activity` signals work in progress | [CODE-CONTRADICTED] | Use `projection.*` instead (GQ-20). |
| C6 | #409 Attention Ledger is age-ranked | [CODE-CONTRADICTED] (partial) | No sort at `agent_focus.py:46` at `495eb96d` (GQ-29). |
| C7 | #409 wide views carry omission counts | [CODE-CONTRADICTED] | Absent at `agent_focus.py:46-50`, `:164-167` (GQ-33). |
| C8 | Orca guide-sourced statements in `orca-capabilities.md` (liveness meanings `:125-126`, `check --wait` consumption) | [UNVERIFIED] | Guide text, not repo code; partly addressed by 05 and 06; see section (f). |
| C9 | The recommend docstring's `python -m` usage claim | [CODE-CONTRADICTED] | Low impact; recorded in scope-03. |
| C10 | A worker-list row carries `projection` | [UNVERIFIED] | G-A, GQ-01. |
| C11 | A non-consuming question read exists | [UNVERIFIED] | G-B, GQ-02. |
| C12 | Pane-key to transcript join | [CODE-VERIFIED] for one worker | `research/07-gate-gap-fill.md` D (GQ-18). |
| C13 | Verb form `orca-ide orchestration <verb>` | [CODE-VERIFIED] | B-03, GQ-69. |
| C14 | Classifier mappings | RESOLVED by Section C | GQ-07. |
| C15 | Nested workers | CONTRADICTION, open | GQ-40. |

---

## (e) [UNVERIFIED] and [CODE-CONTRADICTED] claims in the research files

Source: read-only grep of the tags `UNVERIFIED` and `CODE-CONTRADICTED` in the eight files under `research/`. Each row cites the file and line. "UV" = [UNVERIFIED], "CC" = [CODE-CONTRADICTED]. Where a later file or a GQ row settles the claim, the last column says so; otherwise the claim stands as tagged.

### research/scope-01-contract.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :50 | UV | APPROVED.md decision texts | GQ-100 (N-02) |
| :78 | UV | Memory note behind G1 | GQ-04 |
| :99 | UV | AUDIT_ROOTS roots | later answered in scope-01 |
| :100 | CC | "41 tests" cross-reference | GQ-84 (M1) |
| :111 | CC | analysis :54 level-table claim | C1, GQ-84 |
| :118 | UV | test_help_command coverage | open |
| :128 | UV | peer-sessions memory claim | open |
| :129-138 | CC / UV | F-ID re-mapping (F7, F8, F10, F11, F12 outside the slice; F12 issue-body naming UV) | C1 |
| :142 | UV | Q1 | GQ-04 (merged) |
| :147 | UV | Q6 | GQ-14 |
| :152 | count | 54 CODE-VERIFIED, 12 CC, 4 UV | - |

### research/scope-02-orca-recovery.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :16 | CC | bare `orca` command form | C13, GQ-69 |
| :36 | UV | worker-list row shape equals worker-show shape | G-A, GQ-01 |
| :61 | UV | pane-key to transcript join | verified for one worker: C12, GQ-18 |
| :74 | CC | `projection.stage.activity` as a work signal | C5, GQ-20 |
| :82-94 | UV | orca-capabilities guide rows | partly 05 and 06; C8 |
| :97 | UV | derived classifier | Section C, C14, GQ-07 |
| :115-117 | UV | error rows (`runtime_unavailable`, `runtime_access_denied`, bare `orca`) | open; GQ-15 |
| :119 | UV | inbox behaviour | 07 (GQ-03 keeps inbox forbidden) |
| :120 | UV | row shape | G-A, GQ-01 |
| :122 | UV | `stale_status` | open |
| :124 | UV | executable-failure handling | open |
| :131 | CC | crash-recovery is "pure read-only" (`git stash *` allowed) | C3, GQ-21 |
| :132 | CC | `~/workspace/IronClaude` script path on this host | C4 |
| :133 | CC | `--all` sweeps `~/workspace/`, default 72h | C4 |
| :146 | CC | Bug 1: ENCODED_CWD replaces only `/` | GQ-19 |
| :157 | UV | `parse_session_log` reuse | open |
| :165 | CC | `ccsession --list` is read-only (it migrates names) | open |
| :219 | UV | (gaps summary) | - |
| :223-231 | UV / CC | Q1-Q9 tags | GQ-15..GQ-22 |
| :235 | CC + UV | summary: CC items plus row-equality UV | G-A |
| :241 | CC | A4 (`~/workspace` path) | C4 |
| :242 | count | 30 UV lines | - |

### research/scope-03-cli-patterns.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :76 | CC | recommend docstring's `python -m` | C9 |
| :99 | UV | plain `check` read-marking (allowlist test) | 06; NB-4, GQ-03 |
| :108 | CC | recommend.md `name:` shape | open (low impact) |
| :111 | CC | Activation uses an "identical form" | open (low impact) |
| :140 | UV | enforcement of the command surface | open |
| :165 | CC | no-glob claim | open |
| :208 | UV | pipx install path (OQ3) | GQ-25 |
| :209 | UV | allowed-tools combination (OQ4) | GQ-26 |
| :211 | UV | UTILITIES table (OQ6) | GQ-28 |
| :215 | count | 3 CC, 3 UV | - |

### research/scope-04-409-layout.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :33 | CC | generated files ("Not read") | open |
| :93 | CC (partial) | Attention Ledger is age-ranked; no sort at `agent_focus.py:46` | C6, GQ-29 |
| :247 | CC | wide views carry an omission count; none at `agent_focus.py:46-50`, `:164-167` | C7, GQ-33 |
| :345 | UV | gate-list mapping | GQ-65 |
| :357 | UV | `run:<id>` rows, cap end, `compatibilityAck` | 06 (check handler), GQ-30 |
| :368 | CC | "age-ranked" (repeat of :93) | C6 |
| :371 | CC | omission counts (repeat of :247) | C7 |
| :374 | count | 3 CC, 0 UV | - |

### research/05-orca-row-schema.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :42-50 | UV | guide claims (heartbeat at :50) | GQ-36, GQ-58 |
| :63-69 | UV | row fields from the guide | G-A, GQ-01 |
| :83-88 | UV | row fields from the guide | G-A, GQ-01 |
| :107-108 | UV | row schema details | G-A |
| :125 | UV | `reason` field | open |
| :132, :137 | CC | `stage.activity` | C5, GQ-20 |
| :144 | count | UV count | - |
| :157, :159, :165, :172, :177 | UV | key takeaways | G-A / GQ-36..GQ-41 |
| :186-195 | UV (Gap 7 :192 CC) | Gaps 1-10 | GQ-01, GQ-15, GQ-36..GQ-42, GQ-20 |
| :206 | UV | summary | - |

### research/06-orca-open-questions.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :15-16 | UV | live-only behaviour | open |
| :25-26 | UV | `ask` timeout and usage-line meaning | stale doc, section (f) |
| :28 | UV | reply effect | GQ-44 |
| :33 | UV | check "potentially draining" | G-B, GQ-02 |
| :39, :46 | UV | answered state | G-B, GQ-02 |
| :56-60 | UV | check-mode table | G-B; check handler `:18-19`, `:30` |
| :63 | CC | `--format` help | GQ-55 |
| :64 | UV | inbox | GQ-03 |
| :72-75 | UV | probe results | GQ-59 |
| :81, :84 | UV | check behaviour | G-B |
| :85 | CC | `--format` help is self-contradictory | GQ-55 (resolved) |
| :100 | UV | caller identity | open |
| :102 | UV | peer `ask` | open |
| :104, :111, :118 | UV | agent-wait probe | GQ-50 |
| :127, :130, :132 | UV | wait semantics | open |
| :144 | CC (by help) | null `agentWait` | open |
| :145 | UV | heartbeat | GQ-58 |
| :152 | UV | summary | - |
| :158-175 | UV / CC | Gaps 1-19 (Gap 3 resolved, Gap 15 CC resolved) | GQ-43..GQ-59 |
| :180 | UV | ask timeout, stale | section (f) |

### research/07-gate-gap-fill.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :8 | UV | runtime behaviour not exercised | - |
| :31 | UV | `identify` writes | GQ-64 |
| :43-44 | UV | task-list and gate-list row caps | GQ-65 |
| :49 | UV | inbox read-marking | GQ-03 (inbox stays forbidden) |
| :70 | UV | probe | GQ-59 |
| :71 | UV | `ackMessageIds` | G-B, GQ-02 |
| :92 | UV | inbox | GQ-03 |

### research/research-notes.md

| Line | Tag | Claim | Settled by |
|---|---|---|---|
| :31 | CC | test file "~360 lines" | C2 |
| :40 | CC | F1-F12 numbering | C1 |
| :75 | CC | `python -m` | C9 |
| :145 | CC | `stage.activity` | C5 |
| :157 | UV | bare PATH form works from a non-uv project | GQ-25 (B-19: PATH first, `uv run` fallback) |
| :160 | CC | A4, `~/workspace` | C4 |
| :168 | UV | row shape | G-A, GQ-01 |
| :172 | UV | task-list cap | GQ-65 |
| :174 | UV | inbox | GQ-03 |
| :182 | UV | `check --wait` | G-B, GQ-02 |
| :186 | UV | "unverifiable is absence" | WC-10 |
| :193 | UV | end-of-turn marker | open |
| :225 | CC | #409 sort and omission | C6, C7 |
| :319-329 | CC / UV | C1-C11 | section (d) |

---

## (f) Stale documentation

Each entry names the stale document, what is out of date and the research line that found it.

| # | Document and location | What is stale | Found at |
|---|---|---|---|
| S-01 | `orca-capabilities.md:8`, `:12` | Names Orca CLI 1.4.237 and a 202-line guide; the installed CLI is 1.4.245 and the guide is 215 lines, so its `[G]` line numbers are off | `research/05-orca-row-schema.md:199` |
| S-02 | `orca-capabilities.md:127` | Paging rule does not mention `page.hasMore` | `research/05-orca-row-schema.md:200` |
| S-03 | `orca-capabilities.md` inventory | Missing `[H:worker-list]` line 22, the default scope | `research/05-orca-row-schema.md:201` |
| S-04 | `orca-capabilities.md:97-102` | Candidate stale text versus guide `[G]` 130-131 | `research/05-orca-row-schema.md:202` |
| S-05 | `orca-capabilities.md:68`, `:177` | `ask` timeout; the help now documents 600000 ms, range 1 to 1800000 | `research/06-orca-open-questions.md:180` |
| S-06 | `orca-capabilities.md:8`, `:63` | Guide line numbers shifted (coordinator wait is `[G]:113`, not 108) | `research/06-orca-open-questions.md:181` |
| S-07 | `.dev/issues/339/analysis/analyze-worker-contract.md` as cited by scope-01 | scope-01 used an older 55-line F1-F12 version; the current file has F1-F14 and S1-S5 | `research/research-notes.md:319` (C1) |
| S-08 | `sc-crash-recovery/SKILL.md:13`, `:155` | Claims "pure read-only, enforced by allowed-tools", but `Bash(git stash *)` is allowed | `research/scope-02-orca-recovery.md:131` (C3) |
| S-09 | `sc-crash-recovery/SKILL.md:4`, `:25-27`, `:53` | Hardcodes `~/workspace/...`; this host uses `~/workspaces/...` | `research/scope-02-orca-recovery.md:132-133` (C4) |
| S-10 | #409 docs (`concepts.md:23`) | Say the Attention Ledger is age-ranked; the code has no sort | `research/scope-04-409-layout.md:93`, `:368` (C6) |
| S-11 | #409 `DESIGN-CONTRACT.md:11` | Requires omission counts; the wide views have none | `research/scope-04-409-layout.md:247`, `:371` (C7) |
| S-12 | recommend command docstring | Shows `python -m` usage, against the UV rule | `research/scope-03-cli-patterns.md:76` (C9) |
| S-13 | `research/06-orca-open-questions.md:187` | Its summary is stale against its own gap rows | QA note N3, GQ-89 |
| S-14 | `research/research-notes.md:241-242` | Lists 05 and 06 as MISSING though both exist | QA note N8, GQ-94 |

Not stale (checked and current): the WORKER-CONTRACT lines that 06 read (`research/06-orca-open-questions.md:182`) and `integration-gaps:11` (`research/06-orca-open-questions.md:183`).


