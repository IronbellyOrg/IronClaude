# Extract: gates, risks, snapshot, write-back, unverified register

Source folder: `_bmad-output/specs/spec-orca-observer/`. Abbreviations: ODR = owner-decisions-and-risks.md, RG = release-gates.md, SES = snapshot-export-schema.md, WB = write-back-future-stage.md, UR = unverified-register.md. All quoted text is verbatim; labels kept as written. Extractor notes are marked `[note]`.

## 1. Releases and gates

Staging (RG:3): "R1 = Signal Bridge's worker ledger on the verified `worker-list`, carrying Attention Ledger's "question source UNVERIFIED" notice. Attention Ledger (B) follows QUESTION-OBSERVATION. Decision Desk (C) sits behind QUESTION-LINK. Whether this staging satisfies DIRECTION-SELECTED is for the owner to say"

Data-gate rule (RG:5): "A data gate passes only on recorded, redacted samples of four kinds, **success**, **missing**, **stale** and **contradictory**, each pinned in a contract test. Without all four the gate stays closed. A failed gate keeps the screen on the previous release's view."

| Release | Adds (verbatim; "..." marks elision) | Gate (verbatim) | Ref |
|---|---|---|---|
| R0 Fixture replay and design material | "Ledger screen, inspector, text export at 160/116/80, sanitizer, cell-width truncation, NO_COLOR, ID-anchored selection, every fixture variant, a redacted golden `worker-list` fixture. Spike: Rich Live with the raw stdlib key reader; on failure switch to Textual, never both. ..." | "None from Orca; offline only. Fixtures labelled SYNTHETIC; the PROPOSED schema is used only inside fixture mode." | RG:9 |
| DIRECTION-SELECTED (gate, not a release) | "Nothing ships." | "Owner's dated selection record (below). Status in the source: NOT passed." | RG:10 |
| R1 Live worker-list | "COUNTS strip, freshness strip, worker ledger with verbatim `nextAction.kind`, `result.counts`, capped paging, stale handling, changes since last look, the selected view, the question-source gap notice, the JSON snapshot export (recorded owner decision 2)." | "DIRECTION-SELECTED passed and production integration permitted under the reading the owner confirms. `worker-list --json` fields and paging are verified (seed brief); add a redacted golden sample of each of the four kinds and contract test T32." | RG:11 |
| R2 Question ledger (B) | "`OPEN HUMAN QUESTIONS` with observer-side retention, the 100-row disclosure, "bounded best effort; coverage unknown"." | "QUESTION-OBSERVATION (below). The candidate verb is used only after it passes." | RG:12 |
| R3 Links and C's inspector | "For the selected question, affected sessions with worker-list evidence (Decision Desk)." | "QUESTION-LINK: authoritative mapping from IDs in a message to `dispatchId`/`worktreeId`, verified on this host first. Optional owner re-confirm of the post-link default (B or C)." | RG:13 |
| R4 Remote fleet | "`--include-remote` rows grouped by `projection.host.id`." | "Cross-host ownership joins. Not established." | RG:14 |
| Later: closure evidence | "`closed by evidence` count; closed items move to a closed list." | "A source recording explicit resolution (e.g. a reply row linked to the question ID). Not established." | RG:15 |
| Later: history | "Questions older than the 100-row window." | "Durable, non-consuming message history or event replay. Not established." | RG:16 |
| Later | "Admission and verification, cost, deep links." | "Each needs its own feed; none established." | RG:17 |
| Future stage: write-back | "See `write-back-future-stage.md`." | "Boundary change on #409 plus TUIBBS FR-X-13 amendment. Never R1." | RG:18 |

### DIRECTION-SELECTED (RG:20-27) -- decided by the owner only
- Evidence (RG:22): "a dated selection record written by the owner, never an agent. Names the date, option and decider, and where the owner's statement lives (agents may cite, never write it). Holds: default while no question rows exist, default after QUESTION-OBSERVATION, post-link choice or explicit deferral, fallback date, stack confirmation, command name, confirmed production-integration reading."
- Input (RG:23): "R0 renders of A, B, C at 160/116/80 marked synthetic, with degraded versions and C's find-and-inspect task."
- Missing (RG:24): "no production integration; R0 work continues." Stale (RG:25): "a later gate that changes what a direction can show, or the fallback date passing, triggers a re-confirm. Expiry never grants permission to switch direction."
- Contradictory (RG:26): "A selection never clears a gate; a gate is never bypassed to honour a selection." Acceptance (RG:27): "reviewer check AC-S (`acceptance-tests.md`); never reported as an automated test."
- Status (ODR:66): "DIRECTION-SELECTED has NOT passed; the INV-019 design defect is resolved but no owner selection record exists in the source."

### Production integration readings (RG:29-34) -- "both UNVERIFIED as the issue's intent"
- Reading 1 (V1) (RG:31): "the first change that registers `superclaude observe` in the shipped CLI, or lets the adapter run a live Orca subprocess outside the fake runner."
- Reading 2 (V3) (RG:32): "the first change that wires or enables the observer in the shipped product; separately authorized read-only capture counts as research."
- RG:34: "Until the owner confirms one in the selection record, the stricter reading applies: offline work only (R0)."

### QUESTION-OBSERVATION (RG:36-48) -- before R2; owner inputs decisions 8 and 6
- RG:38: "Candidate verb: `orca orchestration check --all --run <runId> --json`. A candidate, never an available source, until all are recorded:"
- RG:40 "**Proof (a), UNVERIFIED:** `--run` narrows `--all`, shown with samples from at least 2 Runs."
- RG:41 "**Proof (b), UNVERIFIED:** which handle receives human-addressed messages, and whether the read works from an unbound observer terminal."
- RG:42 "**Proof (c), UNVERIFIED:** measured message rate, recorded. A measured rate does not prove completeness, so the label stays "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost" after the gate."
- RG:43 "**Non-consumption (INV-022):** repeated before/after readings on a quiet scope show the read does not consume. ... Help text and an empty peek `count` cannot clear the gate. A pass covers only the visible effects tested (T51)."
- RG:44 "**Question identity:** a verified source-scoped question identity is recorded. A worker `dispatchId` is never a question's identity."
- RG:45 "**Owner inputs:** decision 8 (what identifies a human question) and decision 6 (acquisition permission for the actual read scope, before any call)."
- RG:46 "**Budget:** message calls per cycle set by measurement inside the 5-call cap; V3 default at most 1."
- Fallback rule (RG:48): "if QUESTION-OBSERVATION is not verified by the owner's fallback date, the owner re-confirms the direction. If A is picked, A stays the default on the same adapter and renderer; B's retention model stays in the code..."

### QUESTION-LINK (RG:13)
- Pass condition quoted in the R3 row above. `[note]` No separate section or named decider for QUESTION-LINK beyond "verified on this host first" and "Optional owner re-confirm".

## 2. Owner decisions

Rule (ODR:3): "Each carries a recommendation; none is settled until the owner records it. Labels: "recorded owner decision N" refers to the first table (1-5); "open owner decision N" refers to the numbered open list (1-10)."

### Recorded (ODR:5 "Recorded owner decisions (2026-11-08, binding)") -- DECIDED
| # | Decision (verbatim) | Status (verbatim) | Ref |
|---|---|---|---|
| 1 | "Staged releases: R1 = A's worker ledger on `worker-list` plus B's "question source UNVERIFIED" notice; B after QUESTION-OBSERVATION; C behind QUESTION-LINK" | "Recorded in the dispatch brief. Whether it counts as the DIRECTION-SELECTED selection record is UNVERIFIED (`release-gates.md`)" | ODR:9 |
| 2 | "Stack: Python + Rich, `superclaude observe`-style subcommand in IronClaude, plus versioned additive-only JSON snapshot with a schema test; key-reader spike first, Textual only if it fails, never both" | "CONFIRMED (owner-decisions-20261108.md item 5)" | ODR:10 |
| 3 | "R1 is read-only. Write-back is a future stage needing an issue 409 boundary change and a TUIBBS FR-X-13 amendment" | "Recorded; `write-back-future-stage.md`" | ODR:11 |
| 4 | "TUIBBS (private Go BBS, AGPL-3.0) is background only; no dependency, no copied code" | "Recorded. Licence opinion and "TUIBBS as staff platform" remain open" | ODR:12 |
| 5 | "Every fact keeps its evidence label; no invented Orca field; schema PROPOSED; Orca and coordinator policies keep authority" | "Recorded" | ODR:13 |

### Open (ODR:15-26) -- OPEN unless noted
1. (ODR:17) "**Visual direction (DIRECTION-SELECTED).** A dated selection record written by the owner, never an agent ... Recommendation: A plus the COUNTS strip for R1; B after QUESTION-OBSERVATION with A one key away; C behind QUESTION-LINK. V3 dissents (C post-link). NOT passed." -- OPEN
2. (ODR:18) "**Stack.** Settled by recorded owner decision 2 above (the source listed it as open; it departed from the issue's Go Bubble Tea v2 preference)." -- DECIDED
3. (ODR:19) "**Command name and placement.** Recommend `superclaude observe`, registered in `cli/main.py` (deferred import, then `add_command`). Name is the owner's." -- OPEN
4. (ODR:20) "**Production-integration boundary.** Reading 1 (V1) or reading 2 (V3), both UNVERIFIED; stricter applies until confirmed" -- OPEN
5. (ODR:21) "**Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option." -- OPEN
6. (ODR:22) "**Sample capture and acquisition permission.** ... Recommend yes, owner sets redaction rules. Unblocks B's headline panel." -- OPEN
7. (ODR:23) "**Message-content exposure.** What may be displayed and what exported; kept as separate permissions; no recommendation beyond that." -- OPEN
8. (ODR:24) "**Question-type choices.** What makes a message a "human question", which `type` values count, which handle or Run carries it. Needs the owner or Orca. Recommend an explicit message type, never text inference." -- OPEN
9. (ODR:25) "**Multi-observer restriction.** Caps are per process, no singleton. Recommend disclosure only." -- OPEN
10. (ODR:26) "**Still open from owner-decisions-20261108.md:** write-back stage (summary decision 3), TUIBBS licence opinion (decision 4), TUIBBS as staff platform (decision 5)." -- OPEN

Settled by engineering, not owner votes (ODR:28-35): fixture replay before live adapter (ODR:30); "100-row window for the question panel" (ODR:31); "`--include-remote` off until cross-host joins are verified (R4)" (ODR:32); "No persisted "last look"; session memory only." (ODR:33); "Polling: 15 s cycle, at most 5 subprocesses per cycle, STALE after 45 s monotonic, per-call timeout measured in R0, message calls per cycle by measurement." (ODR:34); "POSIX interactive mode plus `--once` text export on every platform." (ODR:35)

## 3. Risks (ODR:37-52)

`[note]` The source risk table has columns Risk / Effect / Mitigation only: no risk ids and no owner column. Ids below (K1-K12) are extractor row numbers, not source ids; INV-ids are the source's own where present.

| # | Risk (verbatim) | Effect (verbatim) | Mitigation (verbatim) | Ref |
|---|---|---|---|---|
| K1 | "Message row contract never verifies" | "B's panel stays empty; product becomes relabelled A" | "Decisions 6 and 5; shared adapter and renderer, so a switch costs one layout" | ODR:41 |
| K2 | "Worker ledger read as "questions"" | "False sense that human attention is covered" | "Ledger titled `worker-reported, not questions`, gap notice above it (T9)" | ODR:42 |
| K3 | "`page.total` includes historical dispatches" | "Inflated denominators" | "`reported T`; `result.counts` shown separately (T18)" | ODR:43 |
| K4 | "Bound scope shows one Run as the fleet" | "Missed orchestrators" | "`scope.source` in the header, `one Run only`, `read k of N Runs since start`" | ODR:44 |
| K5 | "Hand-written key reader misbehaves" | "Terminal left in raw mode" | "Restore in `finally` and on SIGINT/SIGTERM; `--once` needs no raw mode; R0 spike decides, Textual fallback" | ODR:45 |
| K6 | "Sanitizer gaps" | "Escape-sequence injection from worker text" | "Own allow-printable sanitizer, literal rendering, `injection` fixture (T29, T44)" | ODR:46 |
| K7 | "Retention grows in a long session" | "Memory, clutter" | "1,000-record bound; `unknown (retention exceeded)`; eviction never lowers the open total (T46)" | ODR:47 |
| K8 | "Fixture schema mistaken for an Orca API" | "Coupling to PROPOSED fields" | "Separate fixture loader; live model built only from verified fields (`unverified-register.md`)" | ODR:48 |
| K9 | "`_find_orca()` lives in `install_user_setup.py`" | "Observer import pulls installer code" | "Import as is; moving it is a separate owner-approved refactor" | ODR:49 |
| K10 | "Oldest rows not read at the paging cap (INV-007, accepted)" | "Long-running active workers missed" | "Strip disclosure; earlier rows kept as `not reobserved`; state filter UNVERIFIED" | ODR:50 |
| K11 | "Message bodies acquired without permission (INV-017)" | "Sensitive content in the stdout buffer" | "Permission checked before the call; call skipped if a narrow read cannot honour it; raw output never logged, fixtured or exported" | ODR:51 |
| K12 | ""Non-consuming" read consumes (INV-022)" | "Deliveries lost to real recipients" | "Quiet-scope before/after test in QUESTION-OBSERVATION (T51)" | ODR:52 |

Dissents (ODR:54-60): "`page.total` (C-008 / A-003): V1 wants it required ... Merge keeps it optional" (ODR:56); "Post-link default (C-001): V3 recommends C." (ODR:57); "A-008 label: V1, V2 QUALIFY; V3 REJECT. QUALIFY applied" (ODR:58); "Message calls per cycle (C-002 / X-007): open, set by measurement; V3 default at most 1." (ODR:59); "Production-integration boundary (S-007): both readings UNVERIFIED; stricter applies." (ODR:60)

## 4. Snapshot export

- Title label (SES:1): "Snapshot export schema (PROPOSED, not an Orca contract)"
- Function and consumer (SES:3): "R1 writes a versioned, additive-only JSON snapshot from `export(view)`, with a schema test, for a later read-only Go screen in TUIBBS. This is the observer's own contract; Orca keeps authority over its source fields."
- Evidence label (SES:5): "Source key names were checked read-only against live `orca orchestration worker-list --json` on Orca 1.4.245 (2026-11-08), as reported in the source. The schema built on them is PROPOSED."
- Additive-only / versioning (SES:9): "new optional fields may appear; no field is removed, renamed or retyped without a new major `schemaVersion`." Version (SES:20): "`1` for release 1. Consumers reject an unknown major."
- Missing values (SES:10): "A value the source did not give is the string `UNKNOWN`, never a guess, an empty string, 0 or `null`."
- Content limit (SES:11): "No message bodies, prompts, file contents or credentials in R1. Every string has passed the adapter sanitizer"
- One-way (SES:12): "the snapshot carries no write-back path"
- Schema test (SES:14): "The schema lives in one schema file beside the export function, pinned by one schema test (`acceptance-tests.md`)."
- Consumer status (SES:13): "A licence opinion is required before any Go (AGPL) screen reads the snapshot (summary.md decision 4, still open per owner-decisions-20261108.md item 5)." Option table (SES:66): "(d) Go port first | Not for R1; home for the later Go screen and write-back". Transport (SES:70): "Transport of the snapshot from the Coder host to the TUIBBS host is unexamined (UNVERIFIED)."
- Envelope fields (SES:16-30): `schemaVersion`, `producer`, `cycle`, `generatedAt`, `source.namespace`, `source.status` ("`OK`, `STALE` (older than 45 s), `ERROR` or `UNKNOWN`"), `source.observedAt`, `source.error`, `page.hasMore`/`page.total`/`page.limit` ("`total` is optional upstream, so it may be `UNKNOWN`"), `scope` ("optional upstream"), `counts` ("passed through as a map of state to number (never summed)").
- Row fields (SES:32-47): `dispatchId`, `taskId`, `runId`, `workerState`, `dispatchStatus`, `terminalState`, `role`, `provider`, `hostKind`, `hostId`, `stage.worker`/`stage.dispatch` ("value sets UNVERIFIED; worker-reported, sanitized", SES:42), `outcome`, `liveness.*`, `evidence.*` ("owner correction: the evidence timestamp is `projection.evidence.lastObservedAt`", SES:46), `nextAction` ("raw, never classified", SES:47).
- Withheld (SES:43): "`stage.detail`, `stage.activity` | Withheld from the R1 snapshot. CONTRADICTION: architecture-options.md lists them; merged-requirements.md keeps them inspector-only because whether they carry question text is UNVERIFIED."
- Not frozen (SES:57): "Terminal handles (`agentTerminalHandle`, `resource.terminalHandle`), worktree and endpoint ids, ownership and release state."
- PROPOSED vs verified: `[note]` the source labels the whole schema PROPOSED (SES:1, SES:5); the source key names are reported as checked against Orca 1.4.245 (SES:5), which UR:49 lists under UNVERIFIED as "Snapshot key names checked read-only against Orca 1.4.245 on 2026-11-08; the schema itself is PROPOSED". No per-field VERIFIED/PROPOSED split exists in SES.

## 5. Write-back future stage

- What it is (WB:3): "users send confirmations or corrections from the BBS to their agents. This departs from issue 409's read-only boundary. It is a FUTURE stage, design only, and never part of R1."
- Preconditions (WB:5): "**Boundary change needed in two places before any build:** issue 409 (merged-requirements.md:183, reply kept out of scope) and TUIBBS FR-X-13 "no write-back" (internal/serve/menu.go:637-640). Neither moves without an owner decision."
- Go/no-go gates before stage 1 (WB:40-50): 0 "**Boundary:** owner records the issue 409 boundary change; TUIBBS owner amends FR-X-13 for this one capability." (WB:42); 1 "**Identity:** operator-maintained UserID-to-Run mapping" (WB:43); 2 "**Authorization:** a new per-user capability (reserved `{control}` or a new `AI[orca-answer]` grant) plus the owner check; default deny." (WB:44); 3 "**Input:** answer is one of the question's options or Confirm / Decline" (WB:45); 4 "**Replay and rate:** one accepted answer per question id; nonce as `--retry-request`; per-user rate rule." (WB:46); 5 "**Audit:** `orca.answer.submit` before the send and `orca.answer.result` after" (WB:47); 6 "**Delivery state:** pending until `request-show` or the coordinator says completed; absent shown as "unknown, do not resend"." (WB:48); 7 "**Credential:** narrowest Orca credential; if a pairing code cannot be scoped, stage 1 waits on Orca." (WB:49); 8 "**Orca sender:** confirm with the Orca owner how `reply` authenticates its sender (UNVERIFIED); relaying through the coordinator is required until answered." (WB:50)
- Location (WB:35): "inside the later Go TUIBBS screen (architecture option d) ... Not in the Python observer, not in the snapshot (which stays one-way)."
- Threat model (WB:15-28): 10 threats with controls (identity, authorization, audit, prompt injection, flooding, replay, false success, spoofed Message Base author, stolen BBS host, forged audit trail).
- What R1 must NOT do (WB:38): "R1, Attention Ledger and Decision Desk stay read-only. Decision Desk may show a pending question and the exact `orca orchestration reply` command for the human to run themselves; the observer never sends anything." Also RG:18 "Never R1."; SES:12 "the snapshot carries no write-back path".
- UNVERIFIED in WB: `--options` enforcement on reply (WB:9); "Who Orca accepts a `reply` from is UNVERIFIED" (WB:13); pairing-code scoping (WB:13); Message Base spoofing (WB:26).

## 6. Unverified register (UR:29-50)

`[note]` The source table has columns Item / "How the MVP shows it" only: no entry ids and no "how it would be verified" column. Ids U1-U19 are extractor row numbers. The verification route is given only where the source states one (quoted in the third column, or "not stated").

| # | Item (verbatim) | How the MVP shows it (verbatim) | Ref |
|---|---|---|---|
| U1 | "Message row fields and the inbox JSON shape; only an empty peek `result.{count,dispatchId,runId}` has been seen" | "Not parsed before QUESTION-OBSERVATION" | UR:33 |
| U2 | "Meaning of `result.count`" | "No count is ever derived from it" | UR:34 |
| U3 | "Proof (a) `--run` narrows `--all`; proof (b) which handle receives human-addressed messages and whether an unbound observer can read; proof (c) message rate" | "Gate stays closed" (verified via QUESTION-OBSERVATION proofs, RG:40-42) | UR:35 |
| U4 | "Whether a `--types` value identifies a human question" | "Open owner decision 8" | UR:36 |
| U5 | "Message IDs, inbox lease fields, terminal-attribution fields" | "Required before the non-consumption test (T51)" | UR:37 |
| U6 | "Value set of `projection.nextAction.kind`, and whether any value means "a human must answer"" | "Raw string, never classified" | UR:38 |
| U7 | "Whether `projection.stage.activity` or `.detail` carries question text; value sets of `stage.*`" | "Inspector only, sanitized, labelled `worker-reported`; `stage.detail`/`.activity` withheld from the R1 snapshot" | UR:39 |
| U8 | "Meaning of `projection.evidence.durable` beyond presence" | "Shown raw" | UR:40 |
| U9 | "Whether `page.total` counts historical dispatches ("Showing 2 of 287 Dispatches" suggests it, not proven); semantics of `result.counts`" | "Labelled `reported T`, never "workers"; counts never summed" | UR:41 |
| U10 | "Whether `worker-list` offers a state filter for active workers" | "INV-007 accepted risk, `not reobserved`" | UR:42 |
| U11 | "Clock and format of `liveness.observedAt` / `evidence.lastObservedAt`" | "No per-row STALE; plain age only" | UR:43 |
| U12 | "Per-call timeout value" | "Measured in R0" | UR:44 |
| U13 | "Orca parser support for `--opt=value`" | "Separate arguments only" | UR:45 |
| U14 | "Which production-integration reading the issue intends" | "Stricter reading applies until the owner confirms" (owner confirms in selection record, RG:34) | UR:46 |
| U15 | "Stack table facts (seed brief, nothing run)" | "`stack.md`" | UR:47 |
| U16 | "AC-1..AC-10 mapping to the issue's acceptance list (restated from the seed brief)" | "`acceptance-tests.md`" | UR:48 |
| U17 | "Snapshot key names checked read-only against Orca 1.4.245 on 2026-11-08; the schema itself is PROPOSED" | "`snapshot-export-schema.md`" | UR:49 |
| U18 | "Orca reply sender rule and pairing-code scoping (future stage)" | "`write-back-future-stage.md`" (verified by asking the Orca owner, WB:50; WB:49) | UR:50 |
| U19 | `[note]` Recorded owner decision 1 as DIRECTION-SELECTED record: "Whether it counts as the DIRECTION-SELECTED selection record is UNVERIFIED" | not in UR table | ODR:9 |

Verified list (UR:5-23): "The MVP (R0, R1) needs exactly one live source." (UR:7) -- `orca orchestration worker-list --json --limit 100` (UR:11) plus `_find_orca()` "validated through `skills list --json`" (UR:18). "Plain `check` consumes deliveries; the observer never calls it." (UR:21)
Not established (UR:54): "Complete message history (beyond the 100-row window), cross-host ownership joins, admission and revision-pinned evidence feeds, cost/usage accounting, durable event replay, native deep links."

## 7. Open questions (verbatim, with ids)

`[note]` These five files contain no section titled "Open questions"; open items are the open owner decisions (section 2, OD1-OD10, ODR:17-26) plus the following.
- SES:43 (stage fields): "The stricter reading applies until the open question in `SPEC.md` is answered."
- SES:53 (ordering): "Which order is authoritative for consumers is an open question (`SPEC.md`)."
- ODR:59 (C-002 / X-007): "Message calls per cycle (C-002 / X-007): open, set by measurement; V3 default at most 1."
- ODR:60 (S-007): "Production-integration boundary (S-007): both readings UNVERIFIED; stricter applies."
- SES:70: "Transport of the snapshot from the Coder host to the TUIBBS host is unexamined (UNVERIFIED)."
- WB:50 (gate 8): "confirm with the Orca owner how `reply` authenticates its sender (UNVERIFIED)"
