# Static Attention Snapshot: Design Specification (Variant 2, analyzer lens)

Status: design only. Nothing here was runtime-validated, scheduled or implemented.
All mockup names, IDs, times and numbers are synthetic.

## 1. Purpose, Scope and Evidence Basis
**Goal.** A read-only, plain-ASCII report that an operator can read in chat every
five minutes and, within one screen, find the oldest blocking human decision,
see what changed, and tell whether the report covers everything it claims to.

**Evidence labels used in this spec.** Each claim is tagged by its basis.

| Tag | Meaning |
|---|---|
| [E] | Stated in the seed brief or REPORT.md sections 1-5 as observed on 2026-11-05 |
| [P] | Proposed by this design; not an existing Orca capability |
| [G] | Feasibility gate: cannot be promised until a source is verified |

**What the evidence supports** [E]:
- `orchestration worker-list` returns structured attention, requiresAction,
  nextAction, outcome, stage, liveness (time and source), evidence freshness and
  resource ownership, with opaque cursor paging and limits of 1-100.
- Non-consuming run message reads (`check --peek`, `--all`) are capped at 100
  rows with no advertised read-only paging. `inbox` has a row limit but no cursor.
- `worktree ps` reports host scope and omissions; uncovered hosts are not empty.
- Assignment completion, terminal existence, process liveness and independent
  verification are different facts. A completed task can still own a live terminal.

**What the evidence does not support** [G]:
- A complete, non-consuming enumeration of durable pending human decisions.
- Independent verification records bound to a revision.
- Any usage, cost or token source. Any expected-host inventory.
- Any claim that a design below was tried with real operators or real fleet data.

**Consequence for every concept.** The count of open decisions is written as
"N observed" and carries a coverage marker until the gate in section 12 (FG-1)
is closed. This is a design property, not a styling choice: a number without its
coverage is the main way a snapshot produces a false all-clear.

**Method.** The five concepts were chosen by asking "what single question does the
whole report answer first?" Each concept answers a different question, so each
sorts, groups and truncates differently. Widgets (a bar, a table, a sparkline)
were not counted as concepts. Constraints from the seed brief were turned into the
requirements in section 3 before any screen was drawn, and each screen was then
checked against them (section 5 lists the check).


## 2. Shared Report Contract
All five concepts share one contract so that they differ in organization, not in
honesty rules. [P] unless stated.

### 2.1 Header block (identical in every concept)

| Field | Rule |
|---|---|
| as-of | Collection end time in UTC, and the previous successful observation time |
| scope | Run ids and host scope actually queried, not the intended scope |
| sources | One line per source: name, status (OK / PARTIAL / STALE / FAIL), last success time, paging coverage ("pages 4/4" or "page 1 of ?"), cap note |
| coverage | Plain words: "reported hosts only" when the expected-host list is unknown |
| cadence note | "5-minute sample, not an alert channel" on every report |
| synthetic mark | Mockups only: the string DEMO in the title and in every id |

### 2.2 Symbols and words

| Mark | Meaning |
|---|---|
| `!` | A human action is required by this item |
| `?` | Unknown. Never rendered as 0, "none" or healthy |
| `~` | Stale: last known value from an earlier successful collection |
| `*` | Partial: lower bound ("at least"), because a source is capped or unpaged |
| `X` | Failed, or a check result that failed |
| `>` | "from > to" for requester > owner |
| `+` `-` `.` | In delivery ladders: reached, not reached, unknown |

Words beat symbols where they fit. No emoji. No colour is needed to read any row.

### 2.3 Actionable row schema (R-ROW)

Every row that asks the operator to act carries: stable id, question or reason,
requester, acting owner, age since original creation, impact, evidence reference.
Age is computed from the original creation time of the request, never from the
last update, so repeated reminders cannot make an old request look new.

### 2.4 Ordering, grouping and counting

- Human-required items first, oldest original creation first, ties broken by
  stable id. The order is deterministic so two consecutive reports are comparable.
- Grouping under a root blocker never merges two distinct decisions. Each decision
  keeps its own row; the group only shows the shared dependents once.
- Impact counts are distinct tasks. Direct and indirect are shown separately.
  A task blocked by two decisions is counted once in the report total and marked
  "shared" in each decision's row.
- Heartbeats collapse to one "last seen" per worker. A worker is only listed when
  its liveness crosses a stated threshold, with the threshold written in the report.

### 2.5 Overflow (R-OVF)

Each section has a line budget. When observed items exceed it the report prints
"+N more observed, not shown" plus up to one line of stable ids in the same sort
order, then the count only. The report never says "see the dashboard" or points to
a drill-down, because none is verified to exist (FG-5). Totals shown must equal
shown rows plus omitted rows, so the arithmetic can be checked by eye.

### 2.6 Synthetic fixture world used by all mockups

One invented world keeps the five screens comparable. All values are fake.

| Item | Fixture |
|---|---|
| Report time | 2026-01-01T09:05Z; previous OK collection 09:00Z |
| Runs | run-DEMO-A, run-DEMO-B; host: local |
| Oldest decision | Q-DEMO-01, from w-07 on T-DEMO-04, created 06:51Z (age 2h14m); blocks T-DEMO-04, 05, 06, 07 |
| Second decision | Q-DEMO-02, from w-03 on T-DEMO-06, created 08:20Z (45m); T-DEMO-06 is shared with Q-DEMO-01 |
| Newest decision | Q-DEMO-03, from w-11 on T-DEMO-09, created 08:58Z (7m); a resource retain-or-release question |
| Answered, not resolved | Q-DEMO-04, from w-02 on T-DEMO-08, asked 07:30Z, human reply 08:55Z, no resolution linkage |
| Failure | A-DEMO-12 on w-12, T-DEMO-10, failed 08:41Z, no replacement attempt seen |
| Complete but failing | T-DEMO-03 on w-05 reported done 08:40Z; checks on revision demo-b7 at 09:02Z: 2 failed, 14 ran |
| Liveness | w-09 last seen 08:49Z (16m), threshold 15m |
| Resolved since 09:00Z | Q-DEMO-00, created 05:59Z, answered and resolved 09:01Z |
| Thread ids (C4 only) | TH-DEMO-11 = Q-DEMO-01, TH-DEMO-14 = Q-DEMO-04, TH-DEMO-19 = Q-DEMO-02, TH-DEMO-22 = Q-DEMO-03, TH-DEMO-02 = Q-DEMO-00 |
| Fleet | 12 workers listed: 8 live, 3 exited, 1 unverifiable (w-09); T-DEMO-02 reported done with no independent check seen |

The fixture checks are real counts from the invented world, each with its own
denominator. No cost, token, percentage or trend appears anywhere in the mockups.


## 3. Enumerated Requirements
Words "must" and "must not" apply to any concept that is built. "Basis" cites the
seed brief (SB) or REPORT.md section (RP n). Each requirement is testable by
inspecting a rendered report.

### 3.1 Decisions

| ID | Requirement | Basis |
|---|---|---|
| R-DEC-01 | Every item that needs a human answer must appear in a block that precedes all non-decision content | SB attention first |
| R-DEC-02 | The oldest observed unresolved decision must be identifiable without scrolling past other items; its age is from original creation | RP 3, SB success |
| R-DEC-03 | Each decision row must meet R-ROW (id, question, requester, owner, age, impact, evidence reference) | SB constraints |
| R-DEC-04 | The decision count must be labelled "observed" or "at least" whenever its source is capped, unpaged or stale | RP 2, RP 4 |
| R-DEC-05 | A reply, a snooze or a defer must not remove a decision from the list; only a resolution linkage may | RP 3, RP 5 (incident lifecycle) |

### 3.2 Blocked and failing work

| ID | Requirement | Basis |
|---|---|---|
| R-BLK-01 | Blocked tasks must be linked to their blocking decision or failure by id | SB |
| R-BLK-02 | Impact counts must be distinct tasks, split direct and indirect, never a sum of overlapping descendants | RP 3 metrics |
| R-BLK-03 | Root-blocker grouping must keep distinct decisions as distinct rows | SB constraints |
| R-BLK-04 | A failed authoritative attempt with no accepted replacement must be listed; unknown outcomes must be listed separately from failures | RP 3 |
| R-BLK-05 | Superseded attempts and unassociated sessions must not override the current authoritative attempt, and must be counted apart | RP 3 |

### 3.3 Communication context

| ID | Requirement | Basis |
|---|---|---|
| R-COM-01 | Each decision row must carry the original question text, shortened, not only a summary | RP 3 |
| R-COM-02 | Unanswered context must persist across reports until a resolution linkage exists, not only when it changes | SB |
| R-COM-03 | Delivery states (enqueued, delivered, coordinator-processed, human-seen, answered, resolved) must not be collapsed into one flag | RP 3 |
| R-COM-04 | Heartbeats and routine progress messages must be collapsed to a last-seen time and not listed as rows | SB |
| R-COM-05 | The report must not consume, acknowledge or otherwise write to any mailbox; transcript text is shown as untrusted data, truncated, with control characters removed | RP 2, RP 3 |

### 3.4 Meaningful changes

| ID | Requirement | Basis |
|---|---|---|
| R-CHG-01 | Changes must be computed against the last successful observation, with its time shown | SB |
| R-CHG-02 | A failed or partial collection must never be used as a baseline, and must never be treated as zero | SB, RP 3 |
| R-CHG-03 | Only these changes are listed: decision opened or resolved, item worsened or recovered, failure new, check result flipped, coverage changed | [P] |
| R-CHG-04 | If one or more collections were missed, the report states the gap length; transitions inside the gap are declared unobserved | RP 3, RP 4 |
| R-CHG-05 | Trends, rates and response times appear only with a source, a window and a sample size; otherwise omitted | SB, RP 3 |

### 3.5 Evidence-backed verification

| ID | Requirement | Basis |
|---|---|---|
| R-VER-01 | "Reported complete" must be shown as a worker claim, never as "done" or "green" by itself | RP 3 |
| R-VER-02 | Check results must name the revision they ran against and their time; results for an older revision must be shown as stale | RP 3, RP 4 |
| R-VER-03 | A task reported complete with failing checks must be listed in the attention block, not only in a fleet summary | SB success |
| R-VER-04 | A task reported complete with no independent verification must read "unverified", counted apart from failing | RP 3 |
| R-VER-05 | Evidence labels (claim, accepted settlement, artifact, checks, review, human approval) are words, not a confidence percentage | RP 3 |

### 3.6 Fleet coverage

| ID | Requirement | Basis |
|---|---|---|
| R-FLT-01 | The report must state hosts covered and hosts omitted as reported by the source; with no expected-host list it says so and shows no coverage percentage | RP 2, RP 3 |
| R-FLT-02 | Paging coverage per source must be shown ("pages 4/4" or "stopped at page 2, more exist") | SB |
| R-FLT-03 | Each source has its own freshness line; the oldest source drives the report banner | SB |
| R-FLT-04 | Liveness, process existence, task outcome and verification are separate fields and never merged into one status word | SB, RP 3 |
| R-FLT-05 | Fleet context (counts of live, exited, unverifiable workers) goes after all attention content; unknown counts print `?` | RP 3 |

### 3.7 Format and integrity

| ID | Requirement | Basis |
|---|---|---|
| R-FMT-01 | Plain ASCII, fenced, at most 80 columns by default; any wider report states its width in its title line | SB |
| R-FMT-02 | No cursor control, no emoji dependence, no font or colour dependence; colour is an optional extra for terminal export | SB |
| R-FMT-03 | Default line budget of 60 lines per report, stated in the footer when rows were omitted | [P] |
| R-FMT-04 | Order and column positions are stable between reports | RP 5 (btop stable focus) |
| R-OVF-01 | When observed items exceed a section's line budget, the report prints shown + omitted = observed, lists omitted ids in the same order up to one line, and does not imply any drill-down exists | SB open questions |
| R-INT-01 | The words "all clear", "healthy" or "none" may appear only when every required source is OK and fully paged; otherwise the text is "none observed" with the coverage reason | SB |
| R-INT-02 | Unknown is never rendered as 0, blank or green | SB |
| R-INT-03 | Costs, tokens, trends and percentages must be omitted or `unavailable` unless a source and a denominator are stated | SB |
| R-INT-04 | Every mockup uses synthetic names; no real run record is reused | SB |
| R-INT-05 | Every concept must keep a fixed-position summary near the top of the form "N needs you*, M failing, K unverified" with markers, so that a concept's organizing principle cannot push these counts out of view | [P] |


## 4. The Five-Concept Set
**Set name: the Five-Question Snapshot Set (5Q).** Each member is a whole report
built around one first question. Widths are 80 columns unless stated.

| # | Concept | Organizing principle | First question it answers |
|---|---|---|---|
| C1 | Oldest-Ask Ledger | Time: unresolved asks sorted by original age | "What has waited longest for me?" |
| C2 | Ball-Holder Board | Responsibility: who must move next | "Is this mine, the coordinator's, a worker's, or nobody's?" |
| C3 | Blocker Tree | Dependency: root cause above dependents | "Which single answer unblocks the most work?" |
| C4 | Thread Ledger | Conversation: delivery ladder per thread | "Which questions are stuck, and at which step?" |
| C5 | Since-Last-Look Delta | Change: new / worse / resolved / carried | "What is different since I last looked, and what is still open?" |

### 4.1 C1 Oldest-Ask Ledger (recommended default)

Attention rows come first as a ledger sorted by original age. Below them sit
failures and reported-complete-but-failing work, a one-line delta strip, a short
watch list and fleet context last. Busy-state screen:

```text
ORCA ATTENTION LEDGER [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 09:00Z
scope run-DEMO-A run-DEMO-B | host local | 5-min sample, not an alert channel
SRC worker-list OK 09:05Z pages 4/4 | checks OK 09:02Z | msg-peek PARTIAL*
    msg-peek: cap 100, no paging | hosts: local only, expected list unknown
================================================================================
NEEDS YOU  3 observed*   oldest wait 2h14m = Q-DEMO-01   distinct tasks held 4
--------------------------------------------------------------------------------
 ! Q-DEMO-01  2h14m  w-07 > coord  Approve schema change for T-DEMO-04?
                     holds 4 (1 direct, 3 indirect)         ref M-DEMO-118
 ! Q-DEMO-02    45m  w-03 > coord  Target API v2 or v3 for T-DEMO-06?
                     holds 1 (direct; shared with Q-DEMO-01) ref M-DEMO-131
 ! Q-DEMO-03     7m  w-11 > coord  Retain or release worktree wt-DEMO-9?
                     task link: none seen                    ref wt-DEMO-9
ANSWERED, NOT RESOLVED  1
   Q-DEMO-04  1h35m  w-02 > coord  human replied 08:55Z (10m ago); T-DEMO-08
              still waiting; a reply is not a resolution
--------------------------------------------------------------------------------
FAILING
 X A-DEMO-12   24m  w-12 T-DEMO-10  attempt failed 08:41Z; no replacement seen
 X T-DEMO-03   25m  w-05 CLAIMS DONE 08:40Z; checks rev demo-b7 @09:02Z:
                    2 FAIL of 14 ran -> not verified
UNVERIFIED (claimed done, no independent check seen)  1: T-DEMO-02
--------------------------------------------------------------------------------
SINCE 09:00Z  NEW Q-DEMO-03 | WORSE T-DEMO-03 checks | RESOLVED Q-DEMO-00
WATCH  w-09 last seen 08:49Z (16m, limit 15m) source terminal; holds T-DEMO-07
FLEET  12 workers listed: live 8, exited 3, unverifiable 1 (w-09)
OMITTED  none: 7 attention items observed (3+1+2+1), 7 shown
```

Reading order: lines 1-4 say when and what was and was not read; the first block
under the rule is the decision ledger. The oldest ask is row 1 by construction
(R-DEC-02). The "3 observed*" carries the star because the message source is
capped, so the true number may be higher (R-DEC-04).

**Strengths.** Directly serves the success test (oldest blocking ask in one glance).
Smallest conceptual load; stable position of the oldest ask. Holds distinct
decisions as distinct rows (R-BLK-03).
**Weaknesses.** Dependency relationships appear only as a count per row, so a
reader cannot see which tasks are held. Many asks of similar age give a flat list
with no hint of which matters most. Failures and asks are separate lists, so
cross-cause reading takes effort.
**Use when.** The operator's job is to clear asks and the decision source is
broadly trustworthy.

### 4.2 C2 Ball-Holder Board

The page is split by who has the next move. The operator sees at once which items
are theirs and which are waiting on someone else, so coordinator backlog stops
masquerading as human work. Busy-state screen:

```text
ORCA BALL-HOLDER BOARD [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 09:00Z
SRC worker-list OK pages 4/4 | checks OK 09:02Z | msg-peek PARTIAL* cap 100
scope run-DEMO-A run-DEMO-B | host local only | 5-min sample, not an alert
================================================================================
 NEXT MOVE:   HUMAN 3*   COORDINATOR 2   WORKER 1   NOBODY KNOWN 2
================================================================================
HUMAN  (oldest first)
 ! Q-DEMO-01  2h14m  w-07 > coord  Approve schema change for T-DEMO-04? holds 4
 ! Q-DEMO-02    45m  w-03 > coord  Target API v2 or v3 for T-DEMO-06?    holds 1
 ! Q-DEMO-03     7m  w-11 > coord  Retain or release worktree wt-DEMO-9?
--------------------------------------------------------------------------------
COORDINATOR  (not yours unless it stays here past 30m)
   Q-DEMO-04  1h35m  human replied 08:55Z; coordinator has not resolved it
 X T-DEMO-03    25m  w-05 claims done; checks rev demo-b7 2 FAIL of 14;
                     nextAction as reported by source: fix failing checks
--------------------------------------------------------------------------------
WORKER  (acting; listed only when silent past limit 15m)
   w-09  silent 16m (last 08:49Z, source terminal)  holds T-DEMO-07
--------------------------------------------------------------------------------
NOBODY KNOWN  (no owner seen; these do not move by themselves)
 X A-DEMO-12  24m  attempt failed 08:41Z, no replacement attempt seen
   T-DEMO-11  ready? unknown: dependency and gate data not seen
--------------------------------------------------------------------------------
SINCE 09:00Z  NEW Q-DEMO-03 | WORSE T-DEMO-03 | RESOLVED Q-DEMO-00
QUIET  8 workers live, no listed issue | 12 listed | unverifiable 1 | exited 3
OMITTED  none
```

**Strengths.** Answers "is this mine" without reading text. Isolates coordinator
backlog and orphaned work. Makes missing ownership visible rather than assumed.
**Weaknesses.** Depends on a reliable "who holds the ball" field; the evidence only
shows `nextAction` and `requiresAction` as structured fields (RP 2), so
ownership for messages is inferred and may be wrong. The oldest ask is not
guaranteed to be first if the human block is long. The threshold (30m in the
coordinator header) is a design choice, not an observed norm.
**Use when.** Several humans or a coordinator agent share responsibility.

### 4.3 C3 Blocker Tree

Roots (decisions or failures) are drawn once, with their dependent tasks beneath
them. A task under two roots is drawn once under the older root and referenced
under the other, so impact is never double counted. Busy-state screen:

```text
ORCA BLOCKER TREE [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 09:00Z
SRC worker-list OK 09:05Z pages 4/4 | msg-peek PARTIAL* | checks OK 09:02Z
GRAPH  task links seen for 7 of 11 listed tasks; the rest are UNLINKED, not free
DISTINCT BLOCKED  5 tasks (3 direct to a root, 2 only indirect) | local only
================================================================================
ROOT 1 ! Q-DEMO-01  2h14m  w-07 > coord  Approve schema change?   ref M-DEMO-118
 +- T-DEMO-04  w-07  direct    waiting on the answer
 |   +- T-DEMO-05  w-04  indirect   queued behind T-DEMO-04
 |   +- T-DEMO-06  w-03  indirect   (also held by ROOT 2; counted once here)
 |       +- T-DEMO-07  w-09  indirect   worker silent 16m
--------------------------------------------------------------------------------
ROOT 2 ! Q-DEMO-02  45m  w-03 > coord  Target API v2 or v3?       ref M-DEMO-131
 +- T-DEMO-06  direct   (listed under ROOT 1)
--------------------------------------------------------------------------------
ROOT 3 X A-DEMO-12  24m  attempt failed 08:41Z, no replacement seen
 +- T-DEMO-10  w-12  direct    dependents: unknown (links not seen)
--------------------------------------------------------------------------------
NOT UNDER ANY ROOT (still need you or checking)
 ! Q-DEMO-03     7m  w-11 > coord  Retain or release wt-DEMO-9?  task link: none
   Q-DEMO-04  1h35m  answered 08:55Z, not resolved (T-DEMO-08 waiting)
 X T-DEMO-03    25m  w-05 claims done; rev demo-b7 checks 2 FAIL of 14
--------------------------------------------------------------------------------
SINCE 09:00Z  NEW Q-DEMO-03 | WORSE T-DEMO-03 | RESOLVED Q-DEMO-00
FLEET  12 listed: live 8, exited 3, unverifiable 1 | OMITTED none
```

**Strengths.** Shows the leverage of one answer. Prevents the double count that
a per-decision "blocks N" figure invites. Naturally shows indirect victims such as
a silent worker under a blocked task.
**Weaknesses.** Needs a complete dependency graph, which REPORT.md section 3 lists as a
prerequisite of the blocked-by-decision metric and no inspected source was shown
to provide, so on a real fleet much work may fall under "not under any root". Deep trees blow the line budget. Reads worse when asks are
independent. The oldest ask is first only because the roots are age-sorted.
**Use when.** The graph source is verified and work is dependency-heavy.

### 4.4 C4 Thread Ledger

The unit is the conversation, not the task. Each thread shows how far the question
travelled: enqueued, delivered, coordinator-processed, human-seen, answered,
resolved. A stuck question is located by where its ladder stops. Busy-state screen:

```text
ORCA THREAD LEDGER [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 09:00Z
SRC msg-peek PARTIAL* cap 100, no paging | worker-list OK pages 4/4
LADDER  E enqueued  D delivered  P coord-processed  S human-seen  A answered
        R resolved    + reached   - not reached   . unknown
scope run-DEMO-A run-DEMO-B | local only | 5-min sample, not an alert channel
================================================================================
OPEN THREADS  4 observed*, oldest first         E D P S A R
THREAD       AGE    FROM > TO       QUESTION
 TH-DEMO-11  2h14m  w-07 > coord    Approve schema change?       + + + . - -
             stuck at: human-seen unknown (read flags do not name a person)
 TH-DEMO-14  1h35m  w-02 > coord    Which fixture set for T-08?  + + + . + -
             stuck at: answered 08:55Z, no resolution linkage
 TH-DEMO-19    45m  w-03 > coord    Target API v2 or v3?         + + + . - -
             stuck at: human-seen unknown
 TH-DEMO-22     7m  w-11 > coord    Retain or release wt-DEMO-9? + + - - - -
             stuck at: delivered, coordinator has not processed (7m)
--------------------------------------------------------------------------------
CLOSED THIS WINDOW  TH-DEMO-02 (Q-DEMO-00) answered+resolved 09:01Z  + + + + + +
COLLAPSED  heartbeats and routine progress: 31 messages seen*, 0 shown
           (count is within the 100-row read cap, so it is a lower bound)
--------------------------------------------------------------------------------
NOT A THREAD BUT NEEDS EYES
 X A-DEMO-12 failed 08:41Z, no replacement seen | X T-DEMO-03 claims done,
   checks rev demo-b7 2 FAIL of 14 | w-09 silent 16m
FLEET  12 listed: live 8, exited 3, unverifiable 1 | OMITTED none
```

**Strengths.** Keeps enqueued, delivered, processed, seen, answered and resolved
apart (R-COM-03). Shows an answered-but-unresolved ask honestly. Pinpoints
transport problems (nothing processed) separately from human delay.
**Weaknesses.** The human-seen step is unknown on every row with current evidence
(RP 4), so a full-width column is mostly dots. Failures that are not messages are
pushed to a footer, which breaks "attention first" for non-conversation work.
Impact on tasks is not visible. The "31 messages" figure is only as good as the
capped read.
**Use when.** Message delivery problems are the suspected cause of delays.

### 4.5 C5 Since-Last-Look Delta

The page leads with change since the last successful observation (NEW, WORSE,
RESOLVED), then repeats everything still open and unchanged, oldest first, so
nothing unanswered drops out merely because it did not change (R-COM-02).
Busy-state screen:

```text
ORCA DELTA [DEMO]  as-of 2026-01-01T09:05Z  vs last OK 09:00Z (0 missed)
SRC worker-list OK 09:05Z pages 4/4 | checks OK 09:02Z | msg-peek PARTIAL*
    msg-peek: cap 100, no paging
scope run-DEMO-A run-DEMO-B | local only | 5-min sample, not an alert channel
================================================================================
CHANGED SINCE 09:00Z  3 changes
 NEW      ! Q-DEMO-03     7m  w-11 > coord  Retain or release wt-DEMO-9?
 WORSE    X T-DEMO-03    25m  checks rev demo-b7 @09:02Z: 2 FAIL of 14
                              was: claims done, no checks seen at 09:00Z
 RESOLVED   Q-DEMO-00  answered+resolved 09:01Z (waited 3h02m)
--------------------------------------------------------------------------------
STILL OPEN, NOT CHANGED (carried forward, oldest first)
 ! Q-DEMO-01  2h14m  w-07 > coord  Approve schema change?   holds 4  M-DEMO-118
   Q-DEMO-04  1h35m  w-02 > coord  answered 08:55Z, not resolved      T-DEMO-08
 ! Q-DEMO-02    45m  w-03 > coord  Target API v2 or v3?      holds 1  M-DEMO-131
 X A-DEMO-12    24m  w-12  attempt failed 08:41Z, no replacement seen
   w-09 silent 16m (08:49Z, limit 15m) holds T-DEMO-07
--------------------------------------------------------------------------------
NOT COMPARED  heartbeats collapsed; 8 live workers: no listed change
UNVERIFIED  1 (T-DEMO-02)  | FLEET 12 listed: live 8, exited 3, unverifiable 1
OMITTED  none | transitions between samples are unobserved
```

**Strengths.** Rewards a returning reader: the first screen is "what is new".
Naturally suppresses noise. Carries the old asks forward so nothing vanishes.
**Weaknesses.** A reader who only scans the top block can miss the oldest ask
because it sits in the lower block (the success test fails if the carried block is
not read). Depends entirely on a valid baseline: after a failed collection the top
block must be replaced by a "no valid comparison" notice (see section 8), and the
design degrades to a list. Two changes of the same item inside one gap collapse
into one line.
**Use when.** The operator reads every report and the main risk is overlooking new
events.


## 5. Concept Comparison
Ratings are design judgments from reading the mockups against the requirements.
They are not measurements and no operator saw these screens. "Gate load" means how
many open feasibility gates (section 12) the concept leans on to be honest.

| Criterion | C1 Ledger | C2 Ball-Holder | C3 Blocker Tree | C4 Thread | C5 Delta |
|---|---|---|---|---|---|
| Oldest ask visible first (R-DEC-02) | Strong, by construction | Medium: first in HUMAN band | Medium: first root, if age-sorted | Medium: first thread | Weak: lives in lower block |
| Distinct decisions kept distinct (R-BLK-03) | Strong | Strong | Strong, with dedupe | Strong | Strong |
| No double counting (R-BLK-02) | Medium: per-row "shared" note | Weak: counts per row | Strong | Not applicable | Medium |
| Partial coverage visible (R-FLT-02) | Strong: header block | Strong | Strong, plus graph coverage | Strong | Strong |
| Resists false all-clear (R-INT-01) | Strong | Strong | Medium: "no root" can read as "free" | Medium | Medium: empty delta reads calm |
| Preserves unanswered context (R-COM-02) | Strong | Strong | Medium | Strong | Strong, by design |
| Keeps done-versus-verified apart (R-VER) | Strong | Medium | Medium | Weak | Medium |
| Noise suppression (R-COM-04) | Strong | Strong | Strong | Medium | Strong |
| Gate load | Low: needs FG-1 only for the count label | Medium: ownership fields | High: dependency graph | High: message ladder, human-seen | Medium: durable baseline |
| Lines in the busy mockup (counted, inside the fence) | 27 | 26 | 24 | 25 | 21 |
| Lines when quiet | 13 (drawn, 7.2) | not drawn | not drawn | not drawn | not drawn |

**Requirement check performed on the five screens.** Each screen was inspected for:
as-of, previous OK time, scope, per-source freshness, cap or paging note, `*` on
every capped count, ages from original creation, requester and owner on every
ask, no unit-less number, no percentage, no cost, and no word "healthy" or "clear".
All five carry these in the busy state. Known misses against R-ROW: C4 rows have
no impact and no message reference, and C2 and C3 omit the message reference on
some rows. A built version would need to add them. Differences are in the stronger
properties above. This is a by-eye check on mockups, not a conformance test.

**What the comparison shows.**
1. Only C1 and C5 hold up when the dependency graph and the human-seen signal are
   missing, which is the situation the evidence describes today.
2. C3 and C4 are the most useful when their data exists and the most misleading when
   it does not (empty-looking sections read as safe). They are poor defaults and
   good optional views.
3. C2 is the best answer to "why is the list long?" when many items belong to the
   coordinator, but its ownership mapping is inferred.
4. C5 helps a reader who watches every report and hurts a reader who opens one
   report cold.


## 6. Recommended Default and Rationale
**Recommendation: C1, the Oldest-Ask Ledger, with three borrowed elements.**

| Borrowed from | Element kept inside C1 | Requirement served |
|---|---|---|
| C5 | One-line "SINCE last-ok" strip with the baseline time | R-CHG-01..04 |
| C3 | "holds N (direct, indirect)" and "shared with" notes; distinct total in the section header | R-BLK-02 |
| C2 | "ANSWERED, NOT RESOLVED" band, so coordinator-held items stay visible but separate | R-DEC-05 |

**Rationale, in order of weight.**

1. **It matches the stated success test.** The seed brief defines success as
   finding the oldest blocking decision without opening transcripts. Only C1 makes
   that a fixed-position fact (first row under the first rule) instead of something
   the reader has to compute.
2. **It needs the fewest unverified sources to stay honest.** C1 requires an
   observed-count label (FG-1) and nothing else to be correct. C3 needs the
   dependency graph (FG-3), C4 needs a per-message human-seen signal (FG-4), and C5
   needs a durable valid baseline (FG-6). When those sources are absent the other
   concepts show empty-looking sections that invite a false all-clear. C1 shows
   `?` and `*` in the same places it would show data.
3. **It degrades gracefully.** If the dependency graph is missing, the "holds"
   line becomes `holds ?` and the row stays valid. If the baseline is missing, the
   SINCE strip becomes one sentence and the ledger is unchanged.
4. **It is stable.** Row order is age, which does not change between reports; this
   follows the btop and gh-dash lesson in REPORT.md section 5 (stable selection
   and honest retrieval coverage).
5. **It stays short.** The busy mockup is 27 lines for 7 attention items, so the
   proposed 60-line budget would hold roughly twice that before overflow. This is
   arithmetic on one synthetic screen, not a measured limit; C5 is shorter (21 lines)
   but only because it omits the failing/unverified summary (R-INT-05).

**Costs accepted.** A reader cannot see the dependency shape. Items with the same
age have no priority signal beyond tie-break order. "Who must move" is expressed
only by the ANSWERED, NOT RESOLVED band. These are the reasons C2 and C3 stay as
named alternates, not discards.

**Why not the others as default.**
- C2: ownership is partly inferred; a wrong placement would hide an ask under
  COORDINATOR (R-INT-02 risk).
- C3: highest gate load; unlinked work reads as unblocked.
- C4: human-seen unknown on every row today; mostly dots.
- C5: the oldest ask is in the lower block, which fails the success test for a cold
  reader.

**Conditions that should change the choice.** Switch the default to C5 if
evaluation task ET-1 shows readers finding the oldest ask equally fast in C1 and
C5, and ET-6 shows C5 readers list new, worse and resolved items with higher recall. Offer C3 as a companion when
FG-3 closes. These are test-gated, not decided.

**Relationship between concepts.** All five can be projections of one normalized
read model (hosts, runs, tasks, attempts, threads, decisions, checks, sources).
That is a [P] design statement; it makes the five concepts comparable and lets a
later interactive terminal reuse the same model, but the model is not specified here.


## 7. Recommended Default: The Four States
Each state uses C1. The busy state is the screen in section 4.1; 7.1 adds the
overflow case. In every state the same header block, the same section order and the
same symbols are used, so the reader learns one layout.

### 7.1 Busy, with overflow

Fixture variant: 19 decisions observed, line budget reached. Rows collapse to one
line each and the remainder is counted. The arithmetic shown + omitted = observed
is printed so it can be checked.

```text
ORCA ATTENTION LEDGER [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 09:00Z
scope run-DEMO-A..D | host local | 5-min sample, not an alert channel
SRC worker-list OK 09:05Z pages 6/6 | checks OK 09:02Z | msg-peek PARTIAL*
    msg-peek: cap 100, no paging | hosts: local only, expected list unknown
================================================================================
NEEDS YOU  19 observed*   oldest wait 5h40m = Q-DEMO-31   distinct tasks held 23
--------------------------------------------------------------------------------
 ! Q-DEMO-31  5h40m  w-21 > coord  Rotate signing key now?       holds 6  M-201
 ! Q-DEMO-33  4h12m  w-22 > coord  Merge order for B-DEMO-2?     holds 3  M-207
 ! Q-DEMO-34  3h55m  w-25 > coord  Accept flaky test skip?       holds ?  M-209
 +16 more observed, not shown (shown 3 + omitted 16 = 19*)
   next in order: Q-DEMO-35 Q-DEMO-38 Q-DEMO-39 Q-DEMO-41 Q-DEMO-42 +11 more
   no drill-down is available from this report
--------------------------------------------------------------------------------
FAILING  4 observed: X A-DEMO-40 X A-DEMO-41 X A-DEMO-44 X T-DEMO-31 (oldest 3h)
UNVERIFIED  6 claimed done, no independent check seen (oldest T-DEMO-22, 2h40m)
--------------------------------------------------------------------------------
SINCE 09:00Z  NEW 2 (Q-DEMO-47, Q-DEMO-48) | WORSE 1 | RESOLVED 1
FLEET  31 workers listed: live 24, exited 5, unverifiable 2
OMITTED  16 decisions as above | failing and unverified fully shown
```

The oldest ask stays first. Arithmetic is on screen. The overflow line makes no
promise of a way to see the rest (R-OVF). "holds ?" appears where the dependency
link was not seen (R-INT-02).

### 7.2 Empty / healthy (nothing observed)

```text
ORCA ATTENTION LEDGER [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 09:00Z
scope run-DEMO-A | host local | 5-min sample, not an alert channel
SRC worker-list OK 09:05Z pages 2/2 | checks OK 09:02Z | msg-peek OK 22/100
    hosts: local only, expected list unknown
================================================================================
NEEDS YOU   none observed
FAILING     none observed
UNVERIFIED  none observed (6 settled tasks; 6 with passing checks rev demo-c3)
--------------------------------------------------------------------------------
SINCE 09:00Z  no change observed
FLEET  5 workers listed: live 5, exited 0, unverifiable 0
NOT AN ALL-CLEAR FOR: hosts not reported, transitions between samples, and
anything no source above can see.
```

Rules visible here. "none observed" is allowed only because every source is OK and
read below its cap (R-INT-01). Even so, the wording stays "observed" until FG-1 is
closed. The final line is printed in every healthy report; it is not optional.
If any source were PARTIAL, the line "NEEDS YOU none observed" would become
"NEEDS YOU none seen in the part read: PARTIAL*", with the cap reason.

### 7.3 Stale or unavailable

Fixture variant: the 09:00Z and 09:05Z collections both failed for worker-list.

```text
ORCA ATTENTION LEDGER [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 08:55Z
!! COLLECTION FAILED: worker-list FAIL at 09:05Z (timeout); 09:00Z also failed.
!! Rows below are LAST KNOWN from 08:55Z (~). They may have changed or grown.
SRC worker-list FAIL (last OK 08:55Z, 10m ago) | checks STALE 08:51Z, 14m
    msg-peek FAIL (no data) | hosts: unknown
================================================================================
NEEDS YOU  at least 3 last-known~   oldest wait 2h14m = Q-DEMO-01 (by timestamp)
--------------------------------------------------------------------------------
~! Q-DEMO-01  2h14m  w-07 > coord  Approve schema change for T-DEMO-04?
~! Q-DEMO-02    45m  w-03 > coord  Target API v2 or v3 for T-DEMO-06?
   (Q-DEMO-03 and any newer asks, if they exist, cannot be seen)
--------------------------------------------------------------------------------
FAILING     unknown (source down); last known: X A-DEMO-12 (08:41Z)
UNVERIFIED  unknown
SINCE       NO VALID COMPARISON. Baseline kept at 08:55Z; 2 samples missed.
            Transitions in the gap are unobserved.
FLEET       ? (unknown; unknown is not zero and not healthy)
```

Age is still computed from the original creation time, so the oldest ask is still
ordered correctly; only its status is stale. The report refuses a delta, never
uses 09:00Z as a baseline, and renders fleet figures as `?`.

### 7.4 Reported complete, checks failing

Fixture variant: only these two tasks need attention. Both are "reported complete".

```text
ORCA ATTENTION LEDGER [DEMO]  as-of 2026-01-01T09:05Z  prev-ok 09:00Z
scope run-DEMO-A | host local | 5-min sample, not an alert channel
SRC worker-list OK 09:05Z pages 2/2 | checks OK 09:02Z | msg-peek OK 18 of 100
    hosts: local only, expected list unknown
================================================================================
NEEDS YOU   none observed
--------------------------------------------------------------------------------
REPORTED DONE, NOT ACCEPTED  2
 X T-DEMO-03   25m  w-05 claims done 08:40Z, task outcome: success (as claimed)
                    checks rev demo-b7 @09:02Z: 2 FAIL of 14 ran
                    failed: lint-DEMO, unit-DEMO-3      evidence: claim + checks
 ? T-DEMO-08   40m  w-02 claims done 08:25Z; head rev demo-b9 pushed 08:58Z
                    checks seen only for older rev demo-b7 (stale); none for b9
                    independent review: none seen   evidence: claim only
--------------------------------------------------------------------------------
SINCE 09:00Z  WORSE T-DEMO-03 (no checks seen -> 2 FAIL of 14)
FLEET  5 workers listed: live 4, exited 1, unverifiable 0
NOT AN ALL-CLEAR: 2 tasks reported done are not verified done.
```

Two different problems are separated: a failing result (X) versus no result for the
current revision (?). "success" is shown as the worker's claim and is not turned
green (R-VER-01, R-VER-02, R-VER-03).

## 8. Other Concepts Under the Four States
Described in words (not drawn) because the header, symbols and wording rules from
section 7 apply unchanged. The last column of each cell names the residual
false-all-clear risk that remains for that concept.

| State | C2 Ball-Holder | C3 Blocker Tree | C4 Thread Ledger | C5 Delta |
|---|---|---|---|---|
| Empty / healthy | Four bands all print "none observed"; NOBODY KNOWN stays visible with its count so a gap in ownership is not hidden. Risk: four empty bands look calmer than one line | One line "no roots observed" plus graph coverage ("links seen for 5 of 5 listed"). Risk: with graph coverage unknown, "no roots" can mean "no links seen" | "OPEN THREADS none observed; N messages collapsed" with the cap note. Risk: collapsed count hides that a capped read dropped a message | CHANGED block prints "no change observed"; STILL OPEN prints "none observed". Risk: "no change" reads as "fine" when the open block is also empty because the source is partial |
| Busy | Human band sorted by age; coordinator and nobody-known bands visible. Overflow is per band, so totals add up per band | Roots by age; deep trees truncated with "+N dependents under ROOT k". Distinct total stays in header | Threads by age with ladders; overflow lists ids only. Ladder columns remain | CHANGED block capped first, CARRIED block capped second; both print shown + omitted = observed. Risk: operator reads only the capped top |
| Stale / unavailable | Bands print last-known with `~`; header counts replaced by `at least`. NEXT MOVE line prints `?` for workers. Risk: a failed source for one band makes only that band stale and the rest look fresh unless each band carries its source | All roots `~`; new roots cannot appear. Banner "graph STALE". Risk: stale tree looks authoritative because of its structure | Ladders freeze; a stale `+` could be wrong in either direction; ladders are replaced by `~` marks. Risk: ladder dots hide that nothing was read | Top block replaced by "NO VALID COMPARISON". Carried block remains with `~`. Risk: lowest, because the top block is replaced rather than emptied |
| Reported complete, checks failing | Lands under COORDINATOR (nextAction) or NOBODY KNOWN if no owner. Risk: if filed under COORDINATOR it may be taken as "being handled" | Appears under NOT UNDER ANY ROOT unless it blocks tasks. Risk: low prominence | Appears in the "not a thread" footer. Risk: highest, easy to miss | WORSE block when the check result flipped; otherwise only in carried block. Risk: if checks were failing at the last baseline too, it never appears as a change |

**Common repair applied to all four.** Each concept must keep a minimum
non-droppable block at the top: header with sources, then a fixed-position line
"ATTENTION: N needs you*, M failing, K unverified" (counts with markers). With that
line, even the weaker concepts keep R-DEC-01, R-VER-03 and R-INT-01 satisfied. The
line is requirement R-INT-05. The mockups only approximate it: C1 has the NEEDS
YOU header, C2 the NEXT MOVE strip, C3 the DISTINCT BLOCKED line, while the C4 and
C5 mockups in section 4 do not carry a failing/unverified summary, so a built C4
or C5 would have to add it. This is a known gap in those two mockups, and it is one
reason they are not the default.


## 9. Evaluation Tasks
None of these tasks has been run. Targets are initial proposals to be calibrated
on a pilot; they are not results and not claims about any concept.

**Protocol (proposed).** Synthetic fixtures only (section 2.6 and variants).
Within-subject: each participant sees several concept/state combinations with
the order counterbalanced. Participants are people who supervise multi-agent work;
at least 8 for a quantitative read, otherwise report as qualitative with the number
of participants. Report each measure as a proportion or median with its sample size.
No statistical significance claim without a pre-stated test and sufficient sample.
Time is measured from first display to a spoken or typed final answer; no transcript
drill-down exists in the test, matching the chat setting.

### 9.1 Reader tasks

| ID | Task | Fixture | Measure | Initial target |
|---|---|---|---|---|
| ET-1 | Name the id, age and requester of the oldest observed blocking request | Busy, each concept | Correct answers; time to answer | C1 at least 90% correct, median 15 s or less; other concepts reported, no target |
| ET-2 | State what is being asked and who must answer, in one sentence | Busy | Rubric score on action and answerer | At least 90% match the rubric |
| ET-3 | "Could there be more open decisions than shown?" | Busy with msg-peek PARTIAL | Share answering yes | At least 95% yes |
| ET-4 | "Is anything waiting for you?" | Stale/unavailable | Share answering "unknown / cannot tell"; any "no" is a critical failure | 100% no critical failures; at least 95% "unknown" |
| ET-5 | "How many distinct tasks are held by decisions?" | Busy with shared T-DEMO-06 | Exact answer versus double count | At least 85% exact |
| ET-6 | After viewing report N-1 then N, list what is new, worse, resolved | Two consecutive busy reports | Precision and recall of the list | Precision and recall at least 85% |
| ET-7 | "Is T-DEMO-03 done?" and "Is T-DEMO-08 done?" | Reported complete, checks failing | Share answering "claimed done, not verified" | At least 95%; any "done" is a critical failure |
| ET-8 | "Is Q-DEMO-04 still open?" | Busy | Share answering yes, with reason | At least 90% |
| ET-9 | "How many decisions are not shown, and can you open them from this report?" | Busy with overflow | Exact count and "no" | At least 90% both correct |
| ET-10 | Without the source rows, restate the coverage in one sentence | Busy | Rubric: names the capped source and the unknown host list | At least 80% name both |

### 9.2 Mechanical checks (no participants)

| ID | Check | Pass rule |
|---|---|---|
| MC-1 | Width and character set | Every line 80 columns or fewer; only printable ASCII; no escape bytes |
| MC-2 | Line budget | Busy report at most 60 lines; footer states omissions |
| MC-3 | Header completeness | as-of, previous-OK, scope, one line per source, cadence note present |
| MC-4 | Forbidden wording | "healthy", "all clear" and bare "none" absent unless every source OK and fully paged |
| MC-5 | Unknown handling | Every `?` or "unknown" field is not rendered as 0, blank or a green word |
| MC-6 | Arithmetic | shown + omitted = observed for every capped section |
| MC-7 | Synthetic marker | Every id and name in fixtures matches the DEMO pattern; no real record used |
| MC-8 | No invented metrics | No percentage, cost, token or trend line without a stated source and denominator |

### 9.3 Decision rule for the default

C1 remains the default if it meets ET-1 and ET-4 targets with no critical failure
and no other concept beats it on ET-1 median time by more than 5 seconds at equal
accuracy. A critical failure in ET-4 or ET-7 disqualifies the concept in that
state until its wording is fixed. These thresholds are proposals.


## 10. Limits and Out of Scope
**Out of scope for this document.**
- Scheduling or posting the report every five minutes; no scheduler is designed.
- Controls, acknowledgement, snooze, claim, reply or any write action. The report is
  read-only and must not consume or acknowledge any mailbox (R-COM-05).
- Product code, data-collection code, parsers or renderer implementation.
- The interactive terminal brainstorm and the fork/build recommendation, which are
  separate deliverables.
- Any use of web research, Orca commands or live fleet data in this variant.

**Explicit limits of the design.**
1. Nothing in this spec was runtime-validated. Mockup layouts were checked for width
   and consistency by reading, and the ratings in section 5 are judgments.
2. Five-minute sampling can miss any transition that starts and ends between
   samples. The report is not an urgent-alert channel and says so every time.
3. The accuracy of decision counts is bounded by the weakest source. Until FG-1 closes,
   no count may be presented as complete.
4. Hosts: the report covers only what the source reports. Without an expected-host
   list there is no coverage percentage (REPORT.md section 3).
5. Cost, token, retry-burden, response-time and trend figures are excluded because
   no verified source or denominator exists (REPORT.md sections 3-4).
6. Ranking is by age only. The design does not model urgency or priority, since
   no source for either was verified.
7. Thresholds shown in mockups (15-minute silence, 30-minute coordinator hold) are
   placeholders, not observed norms; real values need operator input.
8. Chat rendering varies; the design assumes a monospace code fence and gives no
   guarantee for proportional-font clients.
9. Transcript or message text may be hostile or malformed. The report shows
   truncated text with control characters removed and never executes or follows it.
10. Terminal ANSI colour is an optional export and nothing in the designs depends on it.


## 11. Risks and Mitigations
| ID | Risk | Likelihood / impact (judgment) | Mitigation | Requirement |
|---|---|---|---|---|
| RK-1 | The decision source is capped, so a real decision is missing and the report looks complete | High / High | `*` and "observed" on every count; header names the cap; "none observed" wording; MC-4 | R-DEC-04, R-INT-01 |
| RK-2 | A failed collection is mistaken for a calm fleet | Medium / High | FAIL banner, last-known rows with `~`, no delta, fleet `?` (section 7.3); ET-4 | R-CHG-02, R-INT-02 |
| RK-3 | A delta against a partial baseline reports phantom "resolved" items | Medium / Medium | Only a fully successful collection becomes a baseline; the gap is stated | R-CHG-01, R-CHG-02, R-CHG-04 |
| RK-4 | A worker claim of completion is read as done | High / High | Words "claims done", checks with revision and time, UNVERIFIED line; ET-7 | R-VER-01..04 |
| RK-5 | Checks are bound to an old revision and look current | Medium / High | Show revision and time; stale revision appears as `?` (section 7.4) | R-VER-02 |
| RK-6 | Root-blocker grouping hides a distinct decision or double counts a task | Medium / Medium | One row per decision; shared tasks counted once; ET-5 | R-BLK-02, R-BLK-03 |
| RK-7 | Reply is read as resolution, so an answered ask vanishes | Medium / Medium | ANSWERED, NOT RESOLVED band; only a resolution linkage removes a row | R-DEC-05 |
| RK-8 | Overflow hides the most important items | Medium / High | Age ordering puts the oldest first; omitted ids listed; arithmetic shown; failing and unverified shown before the cut | R-OVF, MC-6 |
| RK-9 | The report becomes noisy and operators stop reading it | Medium / High | Heartbeats collapse; only threshold crossings listed; line budget 60 | R-COM-04, R-FMT-03 |
| RK-10 | Hostile message text injected into the report misleads the reader or the chat client | Low-Medium / High | Truncate, strip control characters, show as quoted data, never act on it | R-COM-05 |
| RK-11 | Placeholder thresholds (15 m, 30 m) are taken as facts | Medium / Low | Thresholds printed in the report and flagged as configurable in the spec | Limit 7 |
| RK-12 | A reader has learned one layout and an alternate concept confuses them | Low / Medium | Use one default; alternates only on explicit request; same header, symbols, wording | Section 6 |
| RK-13 | Mockup numbers are mistaken for real data | Low / Medium | DEMO in title and ids; MC-7; no cost or percentage | R-INT-04 |
| RK-14 | Design is mistaken for validated | Medium / Medium | Status line at top, limit 1, ratings labelled judgments | Section 10 |
| RK-15 | A stale-looking `~` row misleads in the other direction: an ask already answered shows as open | Medium / Low | Banner says "may have changed"; report never silently drops it | R-DEC-04 |


## 12. Open Questions and Feasibility Gates
### 12.1 Feasibility gates

A gate must be closed by verifying a source (not by assuming one) before the
dependent claim may be printed without a marker.

| Gate | Question | If open | Closing evidence | Concepts affected |
|---|---|---|---|---|
| FG-1 | Which complete, non-consuming source enumerates durable pending human decisions? | Counts print as "N observed*" / "at least"; never "none" without scope | A read-only API or event source with paging and a known total, or a documented guarantee that peek covers all pending items | All; C1 least |
| FG-2 | Where do revision-bound check results and independent review records come from? | Verification lines show `?` or "claim only" | A source that names revision, result, time and reviewer | C1, C2, C5 verification lines |
| FG-3 | Is a task dependency graph readable, and how complete is it? | "holds ?"; C3 not offered | Graph source with a coverage indicator | C3, impact counts in C1 |
| FG-4 | Can a human-seen or human-claimed state be read per person? | Ladder S column stays `.` | Per-person state, not the transport read flag | C4 |
| FG-5 | Does any drill-down exist for omitted rows? | Overflow says none available | A named, verified read-only command or view | Overflow in all |
| FG-6 | Is the last successful observation stored durably, with gaps recorded? | No delta; "NO VALID COMPARISON" | Persisted baseline with success flag | C5, SINCE strip |
| FG-7 | Is there an expected-host or expected-workspace inventory? | "reported hosts only"; no coverage percentage | Inventory the report can compare against | Fleet coverage line |
| FG-8 | Can the report be produced without consuming or acknowledging any mailbox? | Cannot ship | Evidence that every read used is non-consuming and idempotent | All |

### 12.2 Open design questions

1. **Default density.** C1 is recommended on reasoning, not on measurement. ET-1,
   ET-4 and the section 9.3 rule decide whether C5 or a hybrid should replace it.
2. **Overflow destination.** The design prints totals and ids and promises nothing
   more. Whether a companion "full list" message or a later interactive terminal
   should hold the rest depends on FG-5.
3. **Ownership and resolution.** Who writes human-resolved state and from which
   source? This also decides whether ANSWERED, NOT RESOLVED can ever clear.
4. **Independent verification.** Which party records an independent check, and does
   its record bind to a revision (FG-2)?
5. **Thresholds.** Real values for worker silence and coordinator hold times need
   operator input; the mockups use placeholders.
6. **Report variants.** Should the report be a single fixed layout, or may the
   operator switch concept on request? The design assumes one fixed default and
   treats switching as a later question.
7. **Chat length.** Is 60 lines acceptable in the target chat client, or must the
   budget be lower? No chat client was tested.

### 12.3 Recommended next step

Close FG-1 and FG-8 first; they decide whether any count may drop its `*` and whether
the report is safe to produce at all. Then run the mechanical checks MC-1..MC-8 on
fixtures for all four states, and the pilot of ET-1, ET-4 and ET-7 before choosing
a default for build.

