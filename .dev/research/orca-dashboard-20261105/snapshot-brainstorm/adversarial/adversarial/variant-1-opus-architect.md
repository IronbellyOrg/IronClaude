# Spec Variant 1 (Architect): Static ASCII Attention Snapshots for Orca

## 1. Status, Scope and Reading Guide

**Status:** design proposal only. Nothing in this document was implemented, scheduled, run against Orca, or validated with users. Every screen is a hand-drawn mockup.

**Source basis:** the seed brief (`seed-brief.md`) and sections 1-5 of `../REPORT.md`. Sections 6-10 of that report are unfilled placeholders and are not used as evidence. No web research was done for this variant.

**What this spec defines:**

- A read-only static snapshot, pasted into chat about every five minutes, that puts required human action first and makes meaningful change visible.
- Five complete report concepts. Each one has a different organizing principle for the whole report, not a different widget inside the same report.
- One recommended default, and how it renders in four states: empty/healthy, busy, stale/unavailable, and reported-complete-but-checks-failing.

**Architect's angle (custom instruction: maintainable architecture):** the five concepts are treated as five *renderers over one shared report model and one shared frame*. Collection, derivation and rendering are separate layers. This keeps the honesty rules (coverage, staleness, unknown-is-not-zero) in one place, makes the default choice reversible, and lets the five concepts be evaluated against the same seeded fixture.

**Synthetic data rule:** every run, worker, task, decision, host, time and count in this document is invented. Synthetic identifiers use the `DEMO` marker (`run-DEMO-A`, `D-DEMO-0042`, `w-07`) and the date 2026-01-01. No value was taken from a real Orca run.

**Width:** every screen in this document is plain ASCII and at most 78 columns, inside an 80-column budget.

## 2. Architectural Model: One Report Model, Many Renderers

This is a logical design, not an implementation plan. It names boundaries so that the honesty rules live in exactly one layer and the five concepts stay swappable.

```
  sources (read-only)          layer 1            layer 2          layer 3
 +--------------------+    +-------------+    +-------------+   +-----------+
 | worker-list (paged)|--->|  collector  |--->| observation |-->| derivation|
 | check --peek (cap) |--->|  adapters   |    |    store    |   |  (report  |
 | inbox (no cursor)  |--->| one per src |    | last-good + |   |   model)  |
 | worktree ps (hosts)|--->|             |    | gap records |   +-----+-----+
 +--------------------+    +-------------+    +-------------+         |
                                                                       v
                                       +---------------------------------+
                                       | layer 4: frame + concept render |
                                       | A brief | B board | C tree |    |
                                       | D ledger | E journal            |
                                       +---------------------------------+
```

| Layer | Owns | Must never |
|---|---|---|
| 1. Collector adapters | One adapter per source. Records what was asked, what came back, page/cap status, errors and the collection time. | Consume, acknowledge or deliver a coordinator message. Turn an error into an empty result. |
| 2. Observation store | Last successful observation per source; an explicit gap record for each failed or partial collection. | Overwrite last-good data with a failed collection, or store a failure as zero. |
| 3. Derivation | Builds the report model: attention items with stable keys, root-blocker groups, deltas against the last successful observation, coverage and omission totals. | Invent a value a source did not supply; sum overlapping dependents; compute a percentage without a known denominator. |
| 4. Frame + renderer | Pure function from report model to ASCII text. The frame (header, coverage, footer) is shared; the body is concept-specific. | Read sources directly, hide coverage gaps, or drop an item without counting it as omitted. |

**Report model (logical fields, proposed):**

- `frame`: as-of time, previous successful as-of, scope (runs, hosts), per-source status (`ok`, `partial`, `capped`, `failed`, `stale since T`), paging coverage, omitted-row totals.
- `attention_items[]`: stable key, kind (`decision`, `failure`, `verify-gap`, `resource`, `unassigned-ready`), question or reason, requester, acting owner, original age, impact (direct/indirect dependents as distinct sets), evidence references, source and freshness, first-seen and last-changed observation.
- `groups[]`: root blocker to distinct dependent task keys, with a `shared-with` list for tasks under more than one root.
- `threads[]`: thread key, original question text, last message summary, delivery ladder state per field (enqueued/delivered/processed/answered/resolved, each `yes`/`no`/`?`).
- `deltas[]`: new, escalated, aged-past-threshold, resolved, disappeared-without-resolution, all relative to the previous successful observation only.
- `fleet`: liveness counts deduplicated by authoritative identity with an explicit `?` bucket; outcome counts kept separate from liveness.

**Why this shape is the maintainable choice:**

1. **Honesty is centralized.** Coverage, staleness and unknown handling live in layers 2-3 and the shared frame. A new renderer cannot accidentally print an all-clear because it never decides coverage.
2. **The default is reversible.** Switching from concept A to E is a renderer swap, not a data change. Evaluation (section 14) can render all five from one seeded fixture.
3. **Source churn is contained.** If a complete decision source is found later (gate G1, section 17), only one collector adapter changes; the `>= N observed` labels flip to exact counts without renderer edits.
4. **Rendering is testable as golden text.** A pure model-to-text function suits fixture-based snapshot tests and an 80-column width assertion. This is a property of the proposed design, not a test that exists.
5. **Interactive reuse.** The later interactive-terminal brainstorm can reuse layers 1-3 unchanged and replace only layer 4.

## 3. Requirements

All requirements are proposed product requirements, not claims about existing Orca fields or behavior. "Must" applies to every concept unless a concept section says otherwise. The layer column shows where the requirement is enforced in the section 2 model.

### 3.1 Decisions (DEC)

| ID | Requirement | Layer |
|---|---|---|
| DEC-1 | Every report shows pending human decisions before any other content (after the frame header). | 4 |
| DEC-2 | Each decision row carries: stable key, the question in its original wording (truncated with a marker, never paraphrased only), requester, acting owner, original age, impact and at least one evidence reference. | 3, 4 |
| DEC-3 | The oldest observed blocking decision is findable without scanning: concept A ranks it first; other concepts must repeat it in a fixed `OLDEST` line in the frame. | 3, frame |
| DEC-4 | Decision counts read `N` only when the decision source is complete; otherwise `>= N observed`. | 3 |
| DEC-5 | Age is measured from the original creation time when the source gives it; otherwise from first observation and labelled `seen>=`. | 3 |
| DEC-6 | A decision stays listed until a resolution is observed. A reply, a read flag or a vanished message is not resolution; disappearance without resolution is shown as a delta (CHG-3). | 3 |

### 3.2 Blocked and failing work (BLK)

| ID | Requirement | Layer |
|---|---|---|
| BLK-1 | Failed authoritative attempts without an accepted replacement or disposition are listed as attention items. | 3 |
| BLK-2 | Blocked work is grouped under its root blocker, but each distinct decision stays its own row; grouping never merges two decisions. | 3 |
| BLK-3 | Dependent-task impact counts distinct task keys. A task blocked by two roots is counted once in the fleet total and marked `shared` under each root. | 3 |
| BLK-4 | Unknown outcomes are a separate bucket from failures and from successes. | 3 |
| BLK-5 | Repeated reports of one blocker (for example one connectivity incident across ten workers) collapse into one item with an affected-worker count. | 3 |

### 3.3 Communication context (COM)

| ID | Requirement | Layer |
|---|---|---|
| COM-1 | The original question is kept beside any summary for every unresolved thread. | 3, 4 |
| COM-2 | Delivery state is shown as separate facts (enqueued, delivered, coordinator-processed, answered, resolved), each `yes`, `no` or `?`. | 3 |
| COM-3 | Unanswered context persists across reports; it is not shown only when it changes. | 3 |
| COM-4 | Heartbeats and routine progress messages never become rows; they update a last-seen time only. | 3 |
| COM-5 | Message reads used for the snapshot are non-consuming. If the only available read would consume or acknowledge, that source is reported `unavailable (would consume)`. | 1 |
| COM-6 | Transcript and message text is untrusted data: printed inside quotes, truncated, never interpreted as instructions to the renderer. | 4 |

### 3.4 Meaningful changes (CHG)

| ID | Requirement | Layer |
|---|---|---|
| CHG-1 | Deltas compare only against the last successful observation of the same source. | 2, 3 |
| CHG-2 | A failed or partial collection never supplies a zero baseline; deltas for that source print `n/a (no baseline)`. | 2, 3 |
| CHG-3 | Change kinds are: new, escalated (impact grew or kind changed), crossed-age-threshold, resolved (with evidence), disappeared-without-resolution. | 3 |
| CHG-4 | Liveness flaps and heartbeat changes are not deltas. | 3 |
| CHG-5 | Each report states the window it compares (previous good as-of to current as-of). Gaps longer than one cadence are called out because a five-minute sample can miss transitions. | frame |

### 3.5 Evidence-backed verification (VER)

| ID | Requirement | Layer |
|---|---|---|
| VER-1 | Assignment completion, terminal existence, process liveness and independent verification are four separate fields; none implies another. | 3 |
| VER-2 | Evidence is labelled by kind: worker claim, accepted settlement, artifact exists, checks for a named revision, independent review, human approval. No confidence percentage is invented. | 3, 4 |
| VER-3 | A task reported complete whose checks fail, or whose checks are for a different revision, is an attention item of kind `verify-gap` and is never rendered as done/green. | 3 |
| VER-4 | Reported complete with no verification evidence renders `complete (claim only)`, not `done`. | 4 |
| VER-5 | A completed task that still owns a live terminal or other resource is shown as a resource item, not as a liveness problem. | 3 |

### 3.6 Fleet coverage and freshness (COV)

| ID | Requirement | Layer |
|---|---|---|
| COV-1 | Every report prints as-of time (UTC), previous successful as-of, scope, per-source status and freshness, missing sources, paging coverage and omitted rows. | frame |
| COV-2 | Uncovered hosts are named and never treated as empty. Without a known expected-host inventory, the host line reads `N covered of ? expected` and no percentage is shown. | 3, frame |
| COV-3 | If any source relevant to a section is failed, capped or stale, that section header carries the marker, and an empty section reads `0 observed (partial)`, never `none`. | 3, 4 |
| COV-4 | The phrase `all clear` (or any equivalent green summary) may only appear when every source is `ok`, complete and fresh. The default renderer never prints it; the best possible state is `no attention items observed; coverage complete`. | frame |
| COV-5 | Unknown is printed as `?`. Unknown is never summed, averaged or rendered as zero. | 3, 4 |
| COV-6 | Cost, token, trend and percentage figures appear only with a reliable source and a printed denominator; otherwise they are omitted. The default renderer has no cost or token line. | 3 |

### 3.7 Format and safety (FMT)

| ID | Requirement | Layer |
|---|---|---|
| FMT-1 | Output is one plain-ASCII fenced block. No ANSI cursor control, no emoji, no box-drawing Unicode, no reliance on a specific font. Optional ANSI color is a separate terminal export and carries no meaning that the plain text lacks. | 4 |
| FMT-2 | Default width is 78 columns of content in an 80-column budget. A concept that needs more width declares it in its header. | 4 |
| FMT-3 | Each section has a fixed row budget; items beyond it are counted and listed by stable key in an overflow line (section 13). | 4 |
| FMT-4 | Row order is deterministic for the same model (sort keys documented per concept) so consecutive reports can be compared by eye. | 3, 4 |
| FMT-5 | The report is read-only: it performs no writes, acknowledgements, retries or scheduling, and suggests next actions only as text. | all |
| FMT-6 | The report states that it is a five-minute sample and not an urgent-alert channel. | frame |

## 4. Shared Report Frame Contract

Every concept renders the same header and footer. Only the body between them differs. This is the single most important maintainability decision in this spec: it means coverage, freshness and the oldest decision are always in the same place, whichever concept is chosen.

### 4.1 Frame header and footer (all concepts)

```
=== ORCA SNAPSHOT [A:BRIEF] ===================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z  prev-ok 09:00Z  window 5m  (sample, not an alert)
scope runs DEMO-A DEMO-B DEMO-C | hosts 2 covered of ? expected
src   workers ok 3/3pg | msgs CAPPED 100/100 | inbox ok,no-cursor | ps ok
OLDEST D-DEMO-0042 47m DECISION run-DEMO-A "Approve schema v7 or keep..."
------------------------------------------------------------------------
   ... concept-specific body ...
------------------------------------------------------------------------
omitted: 3 decisions, 0 failures, 0 verify-gaps (keys in overflow lines)
legend: ?=unknown  >=N=partial lower bound  seen>=N=age from first sight
```

### 4.2 Frame fields

| Line | Content | Requirement |
|---|---|---|
| Title | Concept code, `SYNTHETIC DEMO DATA` marker in mockups only. | FMT-1 |
| `as-of` | Current collection time, previous successful time, window, sample disclaimer. | COV-1, CHG-5, FMT-6 |
| `scope` | Runs in scope; hosts covered of expected (`?` when inventory unknown). | COV-2 |
| `src` | One token per source: `ok`, `ok,no-cursor`, `CAPPED n/cap`, `PARTIAL`, `FAILED`, `STALE since T`. Paging as `pages read/pages known` or `more?`. | COV-1, COV-3 |
| `OLDEST` | Oldest observed blocking decision key, age, kind, run, quoted question. `none observed (partial)` when sources are incomplete. | DEC-3 |
| `omitted` | Totals per kind of items not shown in the body. | FMT-3 |
| `legend` | Fixed glossary for `?`, `>=N`, `seen>=N`. | COV-5, DEC-4, DEC-5 |

### 4.3 Shared notation

| Token | Meaning |
|---|---|
| `?` | Unknown. Never zero. |
| `>=5` | At least 5 observed; the source is capped or partial. |
| `seen>=12m` | Original creation time unavailable; age counted from first observation. |
| `[claim]`, `[settled]`, `[artifact]`, `[checks@rev]`, `[review]`, `[human]` | Evidence kind (VER-2). |
| `ev:` | Evidence reference: a source plus a stable record reference (message, page, check run). |
| `STALE` | Data is last-good from an earlier collection; age printed. |
| `n/a` | Not applicable or no baseline (deltas after a failed collection). |

### 4.4 Stable identity rule

Row keys come from source-native identifiers (decision record, thread, task, attempt) when the source provides them. When a source provides none, the derivation layer prints the composite source reference (`run/task/attempt + message ref`) and tags it `id:derived`. A derived key is not promised to survive across reports; the tag tells the reader that cross-report comparison of that row is best effort. Display keys may be shortened, but the shortening must be deterministic and collision-checked within a report.

## 5. The Five-Concept Set

The complete set is: **A Attention Brief, B Control Board, C Root-Blocker Tree, D Conversation Ledger, E Delta Journal.**

Each concept answers a different first question for the whole report. They share the frame (section 4) and the report model (section 2), so they differ only in how the body is organized.

| Code | Concept | Organizing principle of the whole report | First question it answers | Inspiration (REPORT.md section 5) |
|---|---|---|---|---|
| A | Attention Brief | One queue of human-required items, oldest blocking decision first, then failures and verification gaps, then a one-line fleet summary | "What do I need to decide, starting with the oldest?" | gh-dash queues, incident triage |
| B | Control Board | A fixed matrix: one row per run, one column per attention lane, with cell keys pointing to a short legend list | "Where in the fleet is attention concentrated?" | btop stable layout, Agent Deck status filters |
| C | Root-Blocker Tree | A forest of root causes with distinct dependent tasks beneath each, shared dependents marked once | "Which single unblock frees the most work?" | otel-tui hierarchical timeline |
| D | Conversation Ledger | Open communication threads, each with original question, last reply and delivery ladder | "Who is waiting on whom, and what was actually asked?" | PagerDuty triggered/acknowledged/resolved separation |
| E | Delta Journal | What changed since the last good observation, followed by a carried-forward list of still-open items | "What is different from five minutes ago?" | Dolphie observation/replay separation |

Concept boundaries are deliberate: A is ranked by age and need, B by location, C by causal structure, D by conversation, E by time. A widget-level variant (for example a different column order in A) is not counted as a separate concept.

## 6. Concept A: Attention Brief (oldest-decision queue)

**Organizing principle:** the report is a triage queue. Everything a human must do is ranked by age of the blocking need; everything else is compressed below it.

### 6.1 Body grammar

| Order | Section | Row budget | Sort key | Requirements |
|---|---|---|---|---|
| 1 | NEEDS YOU (decisions) | 3 rows of 3 lines | original age desc; `seen>=` ages sorted by their lower bound and flagged; ties by key | DEC-1..6, COM-1 |
| 2 | FAILING / NOT VERIFIED | 3 rows of 2 lines | failures before verify-gaps, then age desc | BLK-1, BLK-4, VER-1..4 |
| 3 | CHANGED SINCE prev-ok | 5 lines | kind (new, escalated, resolved, vanished), then key | CHG-1..5 |
| 4 | FLEET | 3 lines | fixed; third line lists answered-but-unresolved decisions by key | COV-5, VER-5, DEC-6 |

Answered-but-unresolved decisions leave NEEDS YOU, because the next actor is no longer the human, but stay listed by key in FLEET until resolution evidence is observed (DEC-6).

A `seen>=` age is a lower bound, so such an item may be older than an item ranked above it. The flag makes that visible instead of hiding the uncertainty.

### 6.2 Busy screen (synthetic)

```
=== ORCA SNAPSHOT [A:BRIEF] ===================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z  prev-ok 09:00Z  window 5m  (sample, not an alert)
scope runs DEMO-A DEMO-B DEMO-C | hosts 2 covered of ? expected
src   workers ok 3/3pg | msgs CAPPED 100/100 | inbox ok,no-cursor | ps ok
OLDEST D-DEMO-0042 47m DECISION run-DEMO-A "Approve schema v7 or keep..."
------------------------------------------------------------------------
1 NEEDS YOU   >=6 observed (msgs capped)          oldest first, 3 shown
 #1 D-DEMO-0042  47m        run-DEMO-A/T-A3/att-2    blocks 3 direct
    Q "Approve schema v7 or keep v6 for this release?"
    req w-07 planner -> human | ev msg:m-DEMO-311
 #2 D-DEMO-0047  31m        run-DEMO-B/T-B1/att-1    blocks 1 direct
    Q "Two specs disagree on retry limit (3 vs 5). Which wins?"
    req w-02 builder -> human | ev msg:m-DEMO-318
 #3 D-DEMO-0051  seen>=19m  run-DEMO-C/T-C4/att-1    blocks ? (no deps)
    Q "OK to delete fixture dir tmp-DEMO before rerun?"
    req w-11 tester -> human | ev inbox:i-DEMO-09
 +3 more: D-DEMO-0040 15m (not re-seen, kept open)
          D-DEMO-0053 9m | D-DEMO-0055 4m
------------------------------------------------------------------------
2 FAILING / NOT VERIFIED                                   2 shown of 2
 F T-DEMO-B2 att-3  failed, no replacement  [settled]  22m  owner w-04
   "pytest exit 1 in tests/demo_retry" | next(wl): dispose or retry
   ev wl:p2#B2
 V T-DEMO-A1 att-1  reported complete, checks FAIL      8m  owner w-05
   [claim] [checks@d3m0a1:fail] | not done | ev chk:c-DEMO-77
------------------------------------------------------------------------
3 CHANGED SINCE 09:00Z (vs last good observation)
 + new        D-DEMO-0055 decision in run-DEMO-A
 ^ escalated  D-DEMO-0042 blocks 2 -> 3 direct
 - resolved   D-DEMO-0039 [human] answered+resolved ev msg:m-DEMO-305
 ! vanished   D-DEMO-0040 not re-seen, no resolution observed: kept open
 V verify-gap T-DEMO-A1 checks FAIL @d3m0a1, first seen this window
------------------------------------------------------------------------
4 FLEET  workers live 9 | exited 2 | ? 1   (dedup by worker identity)
  attempts running 6 | settled-ok 3 | failed 1 | ? 2 | res-held 1
  answered, unresolved: D-DEMO-0036 1h12m (no resolution evidence)
------------------------------------------------------------------------
omitted: 3 decisions (keys above), 0 failures, 0 verify-gaps
legend: ?=unknown  >=N=partial lower bound  seen>=N=age from first sight
```

Reading notes: `blocks ? (no deps)` means dependency data was unavailable for that run, not that nothing is blocked. `res-held 1` is a settled attempt that still owns a live terminal (VER-5); it is a resource fact, not a failure. `next(wl)` quotes the worker-list `nextAction` suggestion as text only; it is not a control.

### 6.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Answers the success criterion directly: the oldest observed blocking decision is row #1 and repeated in `OLDEST`. | Location context is thin: the reader sees runs per row but no fleet-wide shape. |
| Each decision row carries question, requester, impact and evidence; no transcript needed for the common case. | Three-line rows cap the visible queue at three decisions; a busy fleet relies on the overflow line. |
| Lowest learning cost; reads top-down. | Root-cause structure is reduced to a `blocks N` number, so one unblock that frees many tasks is not obvious. |
| Change section is small, so unanswered context dominates (COM-3). | Dependent-task counts per row can overlap between rows; the fleet line does not total them, by design (BLK-3). |

**State handling:** see section 12, which renders all four states for this concept.

## 7. Concept B: Control Board (run-by-lane matrix)

**Organizing principle:** the report is a fixed-position map of the fleet. Rows are runs in a stable order; columns are attention lanes. Below the map, a compact item list names each counted item in one line, keyed by run letter and lane. Positions do not move between reports, so the eye can compare consecutive pastes.

### 7.1 Body grammar

| Part | Content | Rules |
|---|---|---|
| Matrix | One row per run in scope (stable order: run key), lanes DECIDE, FAIL, VERIFY, BLOCKED, LIVE/EXIT/?, SRC, OLDEST; a `fleet` total row | Cells are counts, `>=N`, or `?`. BLOCKED fleet total counts distinct tasks (BLK-3). A run whose collection failed keeps last-good values with a trailing `*` and SRC `STALE` (CHG-2). |
| Item list | One line per item: run letter, lane, key, age, quoted question or reason, requester | Budget 8 lines, DECIDE lane first; overflow per lane. |
| Change strip | One line: counts of new / resolved / vanished since prev-ok | Counts only; keys appear in the item list with `+` or `!` markers. |

### 7.2 Busy screen (synthetic)

```
=== ORCA SNAPSHOT [B:BOARD] ===================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z  prev-ok 09:00Z  window 5m  (sample, not an alert)
scope runs DEMO-A..D | hosts 2 covered of ? expected
src   workers ok 3/4 runs, DEMO-D FAILED | msgs CAPPED 100/100 | ps ok
OLDEST D-DEMO-0042 47m DECISION run-DEMO-A "Approve schema v7 or keep..."
------------------------------------------------------------------------
RUN         DECIDE  FAIL  VERIFY  BLOCKED  LIVE/EXIT/?  SRC       OLDEST
A DEMO-A      >=4     0      1       3      4/1/0       msgs>=    47m
B DEMO-B      >=1     1      0       1      3/0/1       msgs>=    31m
C DEMO-C      >=1     0      0       ?      2/1/0       deps?     s>=19m
D DEMO-D       0*    1*     0*      2*      2/0/0*     STALE 25m  ?
----------  ------  ----  ------  -------  -----------  --------  ------
fleet         >=6    1+1*   1+0*   >=4+2*   9/2/1+2*
------------------------------------------------------------------------
A DECIDE  D-DEMO-0042 47m "Approve schema v7 or keep v6..."  w-07
B DECIDE  D-DEMO-0047 31m "Two specs disagree on retry limit"  w-02
C DECIDE  D-DEMO-0051 s>=19m "OK to delete fixture dir tmp-DEMO?" w-11
A DECIDE  D-DEMO-0040 15m ! not re-seen, kept open  w-03
A DECIDE  D-DEMO-0053 9m "Pin lint config to v2 or v3?"  w-08
A DECIDE+ D-DEMO-0055 4m "Merge order for T-A5 and T-A6?"  w-09
B FAIL    T-DEMO-B2 att-3 22m failed, no replacement [settled]  w-04
A VERIFY  T-DEMO-A1 att-1 8m complete, checks FAIL @d3m0a1  w-05
------------------------------------------------------------------------
changes vs 09:00Z: +1 new  +1 verify-gap  -1 resolved  !1 vanished
DEMO-D: last good 08:40Z; values marked * are 25m old, not current
omitted: 0 decisions, 0 failures, 0 verify-gaps
legend: ?=unknown >=N=lower bound s>=N=age from first sight *=last-good
```

Totals that mix current and last-good values are never added together: `1+1*` reads "1 current plus 1 last-good". This avoids a single false number.

### 7.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Best fleet shape at a glance; a failed run is impossible to miss because its whole row is starred. | The question text is cut to one line; communication context (COM-1) is weaker than A or D. |
| Stable cell positions make five-minute comparison by eye easy. | Width pressure: more than about eight lanes or long run names will not fit 80 columns. Scales poorly beyond roughly 15 runs without paging the matrix. |
| Per-run source status (SRC column) localizes partial coverage instead of one global warning. | Readers may treat counts as the point and skip the item list; the oldest decision depends on the frame `OLDEST` line. |
| Clean mapping to the later interactive terminal (matrix as navigation, item list as queue). | Mixed current/last-good totals are honest but harder to read. |

**State handling:** empty/healthy prints the matrix with all `0` cells only when the run's SRC is `ok`; any partial source keeps `>=0`. Stale shows starred rows (as DEMO-D above). Reported-complete-but-checks-failing lands in the VERIFY lane and cannot be shown as zero. Busy relies on the item-list budget and per-lane overflow.

## 8. Concept C: Root-Blocker Tree (dependency-oriented)

**Organizing principle:** the report is a forest of root causes. Each root (a decision, a failure, or a verification gap) is listed once, with the distinct tasks waiting on it drawn beneath. The reader sees which single unblock affects the most work.

### 8.1 Body grammar

| Part | Content | Rules |
|---|---|---|
| ROOTS | Root items ranked by distinct affected tasks (direct plus indirect), then age | A task under two roots is drawn under the first root and listed as `see [n]` under the other; it is counted once (BLK-3). Each distinct decision is its own root, even if two decisions block the same task (BLK-2). |
| UNROOTED | Decisions and failures with no observed dependents or no dependency data | `deps?` when dependency data is missing for that run; never omitted because they have no tree. |
| Tally | Distinct blocked tasks with keys; runs with unknown dependencies | No percentage; unknown runs are named. |

Tree depth is capped at 3 levels; deeper descendants fold into `+N deeper (keys)`.

### 8.2 Busy screen (synthetic)

```
=== ORCA SNAPSHOT [C:TREE] ====================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z  prev-ok 09:00Z  window 5m  (sample, not an alert)
scope runs DEMO-A DEMO-B DEMO-C | hosts 2 covered of ? expected
src   workers ok 3/3pg | msgs CAPPED 100/100 | inbox ok,no-cursor | ps ok
OLDEST D-DEMO-0042 47m DECISION run-DEMO-A "Approve schema v7 or keep..."
------------------------------------------------------------------------
ROOTS (by distinct tasks affected, then age)                     4 roots
[1] DECISION D-DEMO-0042 47m run-DEMO-A          affects 5 (3 direct)
    Q "Approve schema v7 or keep v6 for this release?"   req w-07
    |- T-DEMO-A4 waiting                                       direct
    |- T-DEMO-A5 waiting                                       direct
    |  `- T-DEMO-A7 waiting                                    indirect
    `- T-DEMO-A6 waiting  (also needs [3])                     direct
       `- T-DEMO-A8 waiting                                    indirect
[2] DECISION D-DEMO-0047 31m run-DEMO-B          affects 1 (1 direct)
    Q "Two specs disagree on retry limit (3 vs 5). Which wins?"
    `- T-DEMO-B3 waiting                                       direct
[3] VERIFY   T-DEMO-A1 att-1 8m  complete, checks FAIL @d3m0a1
    [claim] [checks@d3m0a1:fail] ev chk:c-DEMO-77  affects 1 (shared)
    `- T-DEMO-A6  see [1] (counted once)
[4] FAILURE  T-DEMO-B2 att-3 22m failed, no replacement   affects 0 obs
------------------------------------------------------------------------
UNROOTED (no observed dependents, or dependency data missing)
 D-DEMO-0051 s>=19m run-DEMO-C deps? "OK to delete fixture dir tmp..."
 D-DEMO-0040 15m run-DEMO-A ! not re-seen, kept open
 D-DEMO-0053 9m run-DEMO-A | D-DEMO-0055 4m run-DEMO-A (+ new)
------------------------------------------------------------------------
distinct blocked tasks: 6 (A4 A5 A6 A7 A8 B3) | run-DEMO-C deps ?
changes vs 09:00Z: +1 new  +1 verify-gap  ^1 escalated  -1 resolved
answered, unresolved: D-DEMO-0036 1h12m (not a root; next actor w-03)
omitted: 0 roots, 0 unrooted
legend: ?=unknown >=N=lower bound s>=N=age from first sight
```

### 8.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Shows leverage: which unblock affects the most work, without double counting. | Ranking by impact can push an old, low-impact decision down; the oldest is only guaranteed in the frame `OLDEST` line. |
| Makes shared dependents and the decision-vs-failure relation explicit. | Depends entirely on complete dependency data; with `deps?` on many runs the tree degrades into the UNROOTED list. |
| Natural precursor to an interactive otel-tui-style drill-down. | Tall: deep or wide trees exceed a chat-friendly height quickly; folding loses detail. |
| Separates "blocking others" from "merely open" decisions. | Communication context is limited to the question line. |

**State handling:** empty/healthy prints `ROOTS: 0 observed` plus the source status, and `0 observed (partial)` when any source is incomplete. Stale renders the last-good tree under a `STALE since T` banner and suppresses the change line (`n/a`). Reported-complete-but-checks-failing is itself a root of kind VERIFY, as `[3]` shows. Busy folds depth and uses the UNROOTED line for low-impact items.

## 9. Concept D: Conversation Ledger (communications-oriented)

**Organizing principle:** the report is a ledger of open conversations. Each thread shows what was originally asked, the last thing said, and which delivery facts are known. Work status appears only as context for a thread.

### 9.1 Body grammar

| Part | Content | Rules |
|---|---|---|
| WAITING ON HUMAN | Threads whose next actor is the human, oldest first | Delivery ladder `enq dlv proc ans res`, each `y`, `n` or `?` (COM-2). Original question always shown (COM-1). A coordinator relay is labelled `(not an answer)`. |
| ANSWERED, NOT RESOLVED | Threads with an observed answer but no resolution evidence | A reply is not resolution (DEC-6). |
| STUCK AGENT-TO-AGENT | Worker-to-coordinator threads unprocessed beyond a threshold | Only those past the threshold; routine traffic is never listed. |
| QUIET | One line: heartbeat-only workers folded into a count with last-seen bound | COM-4. |

Repeated messages in one thread fold into `(repeat xN folded)` (BLK-5).

### 9.2 Busy screen (synthetic)

```
=== ORCA SNAPSHOT [D:LEDGER] ==================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z  prev-ok 09:00Z  window 5m  (sample, not an alert)
scope runs DEMO-A DEMO-B DEMO-C | hosts 2 covered of ? expected
src   workers ok 3/3pg | msgs CAPPED 100/100 | inbox ok,no-cursor | ps ok
OLDEST D-DEMO-0042 47m DECISION run-DEMO-A "Approve schema v7 or keep..."
------------------------------------------------------------------------
WAITING ON HUMAN   >=6 observed (msgs capped)               3 shown
 thread        age      from -> to       enq dlv proc ans res
 D-DEMO-0042   47m      w-07 -> human     y   y   y    n   n
   Q "Approve schema v7 or keep v6 for this release?"
   last 08:52Z coord "Forwarded to operator." (not an answer)
 D-DEMO-0047   31m      w-02 -> human     y   y   ?    n   n
   Q "Two specs disagree on retry limit (3 vs 5). Which wins?"
   last 09:01Z w-02 "Still blocked, holding T-B1." (repeat x3 folded)
 D-DEMO-0051   s>=19m   w-11 -> human     y   ?   ?    n   n
   Q "OK to delete fixture dir tmp-DEMO before rerun?"
   last none observed
 +3 more: D-DEMO-0040 15m (not re-seen) D-DEMO-0053 9m D-DEMO-0055 4m
------------------------------------------------------------------------
ANSWERED, NOT RESOLVED                                       1 shown
 D-DEMO-0036   1h12m    w-03 -> human     y   y   y    y   n
   Q "Use branch feat-DEMO-x or rebase onto main-DEMO?"
   A 08:20Z human "Rebase." | no resolution evidence observed yet
------------------------------------------------------------------------
STUCK AGENT-TO-AGENT (unprocessed > 15m)                     1 shown
 m-DEMO-290    18m      w-04 -> coord     y   y   n    n   n
   "T-DEMO-B2 failed twice, requesting disposition."
------------------------------------------------------------------------
WORK CONTEXT  F T-DEMO-B2 failed 22m | V T-DEMO-A1 complete, checks FAIL
QUIET  7 workers heartbeat-only, last-seen <=5m | 2 workers last-seen ?
omitted: 3 waiting (keys above), 0 answered, 0 stuck
legend: ?=unknown >=N=lower bound s>=N=age from first sight
```

### 9.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Strongest communication context: original question, last statement and delivery facts side by side. | Most dependent on message sources, which are exactly the capped, non-paged ones; counts are almost always `>=N`. |
| Makes "relayed but not answered" and "answered but not resolved" visible, which other concepts compress. | Work status (failures, verification gaps) is pushed to a single context line and can be missed. |
| Shows agent-to-agent stalls that may become human decisions later. | Delivery ladder fields (`proc`, `res`) need sources not yet verified; many cells will be `?`. |
| Folding repeats suppresses spam without losing the thread. | Tall per item (3 lines), so only a few threads fit. |

**State handling:** empty/healthy prints `WAITING ON HUMAN: 0 observed` with message source status, and never prints "inbox zero" while any message source is capped. Stale keeps last-good threads under `STALE since T`; the ladder is not advanced. Reported-complete-but-checks-failing appears in WORK CONTEXT and, if a worker asked about it, as a thread. Busy relies on the overflow line in each section.

## 10. Concept E: Delta Journal (change-oriented)

**Organizing principle:** the report is a journal entry for the window since the last successful observation. Changes come first; a carried-forward list keeps every still-open item visible so unanswered context is not lost when nothing changes (COM-3). A short trail summarizes earlier windows so a reader joining late sees recent history and collection gaps.

### 10.1 Body grammar

| Part | Content | Rules |
|---|---|---|
| THIS WINDOW | Change entries: NEW, ESCALATED, AGED (crossed 15m/30m/60m thresholds), VERIFY-GAP, RESOLVED, VANISHED | Only against prev-ok (CHG-1). Budget 7 lines. Heartbeats and liveness flaps excluded (CHG-4). |
| STILL OPEN | Every open attention item not in THIS WINDOW, oldest first, one line each | Budget 5 lines; overflow by key. This is what keeps the journal from becoming change-only. |
| TRAIL | Previous windows, one line each, counts only | A failed window prints `COLLECTION FAILED (src) - no deltas`, never zeros (CHG-2). Needs stored history of observations. |

### 10.2 Busy screen (synthetic)

```
=== ORCA SNAPSHOT [E:JOURNAL] =================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:05Z  prev-ok 09:00Z  window 5m  (sample, not an alert)
scope runs DEMO-A DEMO-B DEMO-C | hosts 2 covered of ? expected
src   workers ok 3/3pg | msgs CAPPED 100/100 | inbox ok,no-cursor | ps ok
OLDEST D-DEMO-0042 47m DECISION run-DEMO-A "Approve schema v7 or keep..."
------------------------------------------------------------------------
THIS WINDOW 09:00Z -> 09:05Z (transitions inside it may be missed)
 + NEW        D-DEMO-0055 4m  run-DEMO-A "Merge order for T-A5, T-A6?"
 ^ ESCALATED  D-DEMO-0042 47m blocks 2 -> 3 direct
 > AGED 30m   D-DEMO-0047 31m run-DEMO-B "Two specs disagree on retry"
 V VERIFY-GAP T-DEMO-A1 complete -> checks FAIL @d3m0a1 (ev c-DEMO-77)
 - RESOLVED   D-DEMO-0039 [human] answered+resolved ev msg:m-DEMO-305
 ! VANISHED   D-DEMO-0040 no resolution observed: kept open below
------------------------------------------------------------------------
STILL OPEN (carried, no change this window), oldest first
 D-DEMO-0042 47m    decision run-DEMO-A  (escalated above)
 D-DEMO-0047 31m    decision run-DEMO-B  (aged above)
 F T-DEMO-B2 22m    failed, no replacement  owner w-04
 D-DEMO-0051 s>=19m decision run-DEMO-C "OK to delete fixture dir...?"
 D-DEMO-0040 15m    decision run-DEMO-A  not re-seen this window
 +3 more: D-DEMO-0053 9m | V T-DEMO-A1 8m | D-DEMO-0055 4m
------------------------------------------------------------------------
TRAIL (earlier windows, counts only)
 08:55Z->09:00Z  +2 new  -0 resolved  !0 vanished
 08:50Z->08:55Z  COLLECTION FAILED (msgs) - no deltas, baseline kept
 08:45Z->08:50Z  +0 new  -1 resolved  !0 vanished
------------------------------------------------------------------------
omitted: 3 open items (keys above), 0 changes
legend: ?=unknown >=N=lower bound s>=N=age from first sight
```

Open items that changed in this window are repeated in STILL OPEN with a pointer, so the open list is always complete within its budget. This duplication is deliberate: it keeps the "what is open" answer independent of the "what changed" answer.

### 10.3 Tradeoffs

| Strength | Weakness |
|---|---|
| Best for an operator who reads every paste: the top lines are exactly what is new. | The oldest blocking decision is not structurally first; it depends on the STILL OPEN ordering and the frame line. |
| TRAIL makes collection gaps visible over time, which no other concept shows. | Requires a durable observation history to render TRAIL and AGED; without it, the journal degrades to a two-section diff. |
| Threshold-based AGED entries make slow drift visible without a trend metric. | Change wording can create urgency bias: a new low-impact item appears above an old high-impact one. |
| Natural fit for chat, where earlier pastes scroll away. | Duplication between THIS WINDOW and STILL OPEN costs lines. |

**State handling:** empty/healthy prints `THIS WINDOW: no changes observed` and `STILL OPEN: 0 observed`, each with the coverage qualifier; "no changes" is never phrased as "healthy". Stale prints `THIS WINDOW: n/a, collection failed` and carries the last-good STILL OPEN list under a `STALE since T` banner. Reported-complete-but-checks-failing appears as a VERIFY-GAP entry when first seen and stays in STILL OPEN until checks pass for the current revision. Busy relies on budgets and the trail.

## 11. Comparison and Recommended Default

### 11.1 Comparison

Ratings are design judgments about the mockups in this document, not measured results. `+` strong, `o` adequate, `-` weak.

| Criterion | A Brief | B Board | C Tree | D Ledger | E Journal |
|---|---|---|---|---|---|
| Oldest blocking decision is structurally first (success criterion) | + | o (frame line) | o (frame line) | + | o (frame line) |
| Needed action understandable without a transcript | + | - | o | + | o |
| Partial coverage visible where it matters | o (global) | + (per run) | o | o | + (trail) |
| Stale/unavailable without false zero | + | + | o | o | + |
| Reported-complete-but-checks-failing visible | + | + | + | - | + |
| No double counting of dependents | + (no totals) | o (mixed totals) | + | + | + |
| Fleet shape at a glance | - | + | o | - | - |
| Change visibility | o | - | - | - | + |
| Works with only the sources inspected so far | + | + | - (needs dependency data) | - (needs delivery ladder) | o (needs history) |
| Reuse as the interactive terminal's default view | + (queue) | + (navigation) | o (drill-down) | o (thread pane) | - |

### 11.2 Data dependency per concept (architectural coupling)

| Concept | Needs beyond worker-list and capped message reads | Degrades to |
|---|---|---|
| A | Nothing required; dependency data improves `blocks N` | `blocks ?` |
| B | Per-run collection status | Starred stale rows |
| C | Complete task dependency graph | UNROOTED list only |
| D | Delivery ladder facts (processed, resolved) and thread identity | Mostly `?` cells |
| E | Durable observation history across windows | Two-section diff without TRAIL or AGED |

### 11.3 Recommended default: Concept A, Attention Brief

**Rationale:**

1. **It matches the stated success criterion directly.** The operator's success test is finding the oldest blocking decision without opening every transcript. A ranks that decision first and carries question, requester, impact and evidence on the row.
2. **Lowest source coupling.** A renders honestly with only the sources already inspected (paged worker-list, capped non-consuming message reads, host scope from worktree ps). C, D and E each depend on a source or history that is not yet verified (section 11.2). A default should not depend on an open feasibility gate.
3. **Honest under uncertainty.** A prints no fleet totals of dependents, so it cannot double count; it shows `>=N` and `seen>=` inline; it never prints all-clear (COV-4).
4. **Cheapest to replace.** Because every concept is a renderer over the same model and frame (section 2), choosing A now does not lock out B, C, D or E. Adding one later is a layer-4 change.
5. **Best bridge to the interactive terminal.** A's queue is the natural list pane of a later gh-dash-style interface, with B's matrix as an optional navigation pane.

**Runner-up:** E, Delta Journal, for an operator who reads every paste and once observation history exists. Its TRAIL line is the best defence against silently missed collection gaps.

**Not recommended as default:** C (blocked on dependency data), D (blocked on delivery facts), B (weak communication context for decisions).

## 12. Recommended Default Across the Four States

All four states use the same frame and the same four body sections, so the reader's eye always lands in the same place. The bottom status banner is the only line whose wording changes by state, and none of its permitted wordings is an all-clear unless COV-4 holds.

| State | Banner wording (fixed set) |
|---|---|
| Empty, complete coverage | `NO ATTENTION ITEMS OBSERVED. All sources ok and complete.` |
| Empty, partial coverage | `NO ATTENTION ITEMS OBSERVED. This is not an all-clear: coverage partial.` |
| Busy | none (the queue is the message) |
| Stale/unavailable | `!! STALE: body is the <T> observation, <N>m old. Not current. !!` (top of body) |
| Complete but checks failing | `NO DECISIONS OBSERVED, BUT <N> COMPLETED TASKS FAIL VERIFICATION.` |

The complete-coverage wording requires a known expected-host inventory and a complete decision source (gates G1 and G3, section 17). Until those gates pass, the default renderer can only ever print the partial-coverage wording.

### 12.1 Empty / healthy (partial coverage, the realistic case today)

```
=== ORCA SNAPSHOT [A:BRIEF] ===================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T14:10Z  prev-ok 14:05Z  window 5m  (sample, not an alert)
scope runs DEMO-A DEMO-B | hosts 1 covered of ? expected
src   workers ok 2/2pg | msgs ok 37<100cap | inbox ok,no-cursor | ps ok
OLDEST none observed (inbox has no cursor: completeness unverified)
------------------------------------------------------------------------
1 NEEDS YOU   0 observed (partial: inbox no-cursor, hosts ? expected)
------------------------------------------------------------------------
2 FAILING / NOT VERIFIED   0 failing observed
  reported complete, verification unknown: T-DEMO-A2, T-DEMO-B5 [claim]
------------------------------------------------------------------------
3 CHANGED SINCE 14:05Z (vs last good observation)
 - resolved   D-DEMO-0061 [human] answered+resolved ev msg:m-DEMO-402
------------------------------------------------------------------------
4 FLEET  workers live 4 | exited 0 | ? 0   (dedup by worker identity)
  attempts running 4 | settled-ok 2 | failed 0 | ? 0 | res-held 0
  answered, unresolved: none observed
------------------------------------------------------------------------
NO ATTENTION ITEMS OBSERVED. This is not an all-clear: coverage partial.
omitted: 0 decisions, 0 failures, 0 verify-gaps
legend: ?=unknown  >=N=partial lower bound  seen>=N=age from first sight
```

Claim-only completions are listed even in the healthy state (VER-4), so "nothing to do" never hides "nothing verified".

### 12.2 Busy

The busy state is the screen in section 6.2. Its load-bearing behaviors are: `>=6 observed` because messages are capped; three full decision rows plus a keyed overflow line; a vanished-but-unresolved decision kept open; the verification gap shown as `not done`; and no summed dependent totals.

### 12.3 Stale / unavailable

```
=== ORCA SNAPSHOT [A:BRIEF] ===================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T09:20Z  prev-ok 09:05Z  window 15m (3 attempts failed)
scope runs DEMO-A DEMO-B DEMO-C | hosts 1 covered of ? expected
src   workers FAILED 09:10Z 09:15Z 09:20Z | msgs STALE since 09:05Z
      inbox STALE since 09:05Z | ps PARTIAL host-DEMO-2 unreachable
OLDEST D-DEMO-0042 62m if still open (last seen 09:05Z) "Approve sch..."
------------------------------------------------------------------------
!! STALE: body is the 09:05Z observation, 15m old. Not current. !!
1 NEEDS YOU   >=6 at 09:05Z (stale, may have changed)         1 shown
 #1 D-DEMO-0042  62m if open  run-DEMO-A/T-A3/att-2   blocks 3 @09:05Z
    Q "Approve schema v7 or keep v6 for this release?"
    req w-07 planner -> human | ev msg:m-DEMO-311 (as of 09:05Z)
 +5 at 09:05Z: D-DEMO-0047 D-DEMO-0051 D-DEMO-0040 D-DEMO-0053
               D-DEMO-0055
------------------------------------------------------------------------
2 FAILING / NOT VERIFIED   2 at 09:05Z (stale): T-DEMO-B2 F, T-DEMO-A1 V
------------------------------------------------------------------------
3 CHANGED   n/a - no successful collection since 09:05Z (no baseline)
------------------------------------------------------------------------
4 FLEET  workers ? now (last good 09:05Z: live 9 | exited 2 | ? 1)
  host-DEMO-2 unreachable since 09:12Z: its workers are unknown, not 0
------------------------------------------------------------------------
omitted: 5 decisions (keys above), 0 failures, 0 verify-gaps
legend: ?=unknown  >=N=partial lower bound  seen>=N=age from first sight
```

Key behaviors: the body is shrunk to one full row so the stale banner and source failures dominate; ages are projected only as "if still open"; the change section prints `n/a` rather than zero (CHG-2); an unreachable host is named and its workers are unknown (COV-2).

### 12.4 Reported complete but checks failing

```
=== ORCA SNAPSHOT [A:BRIEF] ===================== SYNTHETIC DEMO DATA ===
as-of 2026-01-01T17:30Z  prev-ok 17:25Z  window 5m  (sample, not an alert)
scope runs DEMO-C | hosts 1 covered of ? expected
src   workers ok 1/1pg | msgs ok 12<100cap | inbox ok,no-cursor | ps ok
OLDEST none observed (inbox has no cursor: completeness unverified)
------------------------------------------------------------------------
1 NEEDS YOU   0 observed (partial: inbox no-cursor, hosts ? expected)
------------------------------------------------------------------------
2 FAILING / NOT VERIFIED                                   2 shown of 2
 V T-DEMO-C3 att-2  reported complete, checks FAIL      6m  owner w-10
   [settled] [checks@d3m0c3:fail] | NOT DONE | ev chk:c-DEMO-91
 V T-DEMO-C4 att-1  complete, checks are for another revision  3m
   [claim] [checks@d3m0c1:pass] head d3m0c4 | NOT VERIFIED | owner w-12
------------------------------------------------------------------------
3 CHANGED SINCE 17:25Z (vs last good observation)
 V verify-gap T-DEMO-C4 checks revision mismatch, first seen
------------------------------------------------------------------------
4 FLEET  workers live 1 | exited 3 | ? 0   (dedup by worker identity)
  attempts running 0 | settled-ok 4 | failed 0 | ? 0 | res-held 1
  answered, unresolved: none observed
------------------------------------------------------------------------
NO DECISIONS OBSERVED, BUT 2 COMPLETED TASKS FAIL VERIFICATION.
omitted: 0 decisions, 0 failures, 0 verify-gaps
legend: ?=unknown  >=N=partial lower bound  seen>=N=age from first sight
```

Key behaviors: `settled-ok 4` describes assignment outcome only and sits beside two `NOT DONE` / `NOT VERIFIED` rows; a check that passed for an older revision does not count as verification (VER-3); `res-held 1` reports a settled attempt that still owns a live terminal, which explains `workers live 1` with zero running attempts (VER-1, VER-5).

## 13. Overflow, Paging and Omission Rules

These rules answer the seed brief's open question on where overflow goes. They are part of the shared frame contract, so every concept obeys them.

| ID | Rule |
|---|---|
| OVF-1 | Each body section has a fixed row budget (per concept grammar). Items beyond the budget are never silently dropped. |
| OVF-2 | Overflow is printed in-section as `+N more:` followed by stable keys and ages, wrapped across at most two lines. |
| OVF-3 | When keys do not fit in two lines, print the first keys in sort order and then `... and K more keys not printed`. The footer `omitted:` line always carries the full count per kind. |
| OVF-4 | Overflow text never implies a drill-down exists. Keys are references the operator can use to ask the coordinator or read the source; the snapshot itself offers no link or command. |
| OVF-5 | Paging coverage is distinct from overflow. Overflow is "observed but not printed"; paging coverage is "not observed because the source was capped or not fully paged". The `src` line reports paging; the `omitted` line reports overflow. Both can be non-zero at once. |
| OVF-6 | A worker-list collection reads every page the cursor offers within a stated limit; if the limit stops it, the `src` token reads `n/m+ pg, more?` and counts derived from it become `>=N`. |
| OVF-7 | A capped message read (rows returned equal the cap) marks every decision and thread count `>=N` and suppresses "none observed" wording in favor of `0 observed (partial)`. |
| OVF-8 | Total report height target: at most about 40 lines for the busy state, so one paste fits a typical chat viewport without scrolling far. This is a design target, not a measured constraint. |

## 14. User Evaluation Tasks

**Status:** proposed protocol only. No participant has performed these tasks and no result is claimed.

**Method (proposed):** build one seeded synthetic fixture per state (empty/healthy, busy, stale/unavailable, complete-but-checks-failing) with a written ground truth. Render every fixture through all five concepts using the shared model, so concept differences cannot come from data differences. Each participant sees a concept for one fixture at a time, in a counterbalanced order, with no transcript access. Measure task time with a stopwatch, correctness against the ground truth, and wrong-confidence errors (a confident wrong answer).

| ID | Task given to the participant | Measure | Proposed pass threshold |
|---|---|---|---|
| EV-1 | "Which pending decision has waited longest, and what is being asked?" (busy fixture) | Correct key and paraphrase of the question; time | Correct in at least 9 of 10 trials; median under 30 s |
| EV-2 | "Is this report complete? If not, which source is incomplete?" (busy and empty fixtures) | Names the capped or partial source | At least 9 of 10 correct; zero answers of "complete" for a partial fixture |
| EV-3 | "Is anything wrong right now?" (empty fixture with partial coverage) | Participant does not answer with an unqualified "no" | Zero unqualified all-clear answers |
| EV-4 | "Is this data current?" (stale fixture) | Identifies staleness and its age | At least 9 of 10 correct within 15 s |
| EV-5 | "Which tasks are done?" (complete-but-checks-failing fixture) | Does not list a task whose checks fail or are for another revision | Zero such tasks listed |
| EV-6 | "How many distinct tasks are blocked?" (busy fixture with a shared dependent) | Distinct count, or "unknown for run X" when deps are missing | Exact match to ground truth, including the unknown qualifier |
| EV-7 | "What changed since the last report?" (busy fixture plus its predecessor) | Lists the new, escalated, resolved and vanished keys | At least 4 of 5 change items named |
| EV-8 | "Which decision disappeared without being resolved?" (busy fixture) | Names the vanished key and says it is still open | Correct in at least 8 of 10 trials |
| EV-9 | "Who asked, and who needs to act?" for a named decision key | Requester and acting owner correct | At least 9 of 10 correct |
| EV-10 | Width check: paste each screen into the target chat client at 80 columns | No wrapped or truncated line | Zero wrapped lines (mechanical check, no participant needed) |

Thresholds are starting proposals for the debate, chosen to make each task falsifiable. They should be revised once the participant pool and chat client are known.

## 15. Limits and Out of Scope

**Explicit limits of this design:**

- A five-minute snapshot is a sample. Transitions between collections can be missed, and the report is not an urgent-alert channel (FMT-6, CHG-5).
- Decision counts are lower bounds (`>=N`) until a complete, non-consuming decision source is verified (gate G1). The default concept is built to be honest under that limit, not to remove it.
- The report cannot tell whether a particular person has seen, claimed or snoozed an item. That requires separate storage that does not exist in the inspected surfaces.
- Ages from `seen>=` are lower bounds; ordering among such items is approximate and flagged.
- Verification labels can only reflect evidence the sources expose. When no independent verification source exists, every completion stays `[claim]` or `[settled]`.
- No cost, token, spend, trend or percentage line appears in any concept (COV-6). None was verified in the sampled Orca surfaces.
- The mockups are hand-drawn. Column alignment and row budgets were checked by eye and by a width count, not by rendering real data.

**Out of scope:**

- Scheduling, posting automation and any five-minute timer.
- Any control, write, acknowledgement, retry, claim or resolution action.
- Implementation, data collection code and Orca command execution.
- The interactive terminal design (a separate, later brainstorm), and the fork/adopt/build recommendation.
- Selection of a terminal framework or third-party dashboard.
- ANSI color export beyond the rule that it adds no meaning (FMT-1).

## 16. Risks and Mitigations

| ID | Risk | Effect | Mitigation in this design |
|---|---|---|---|
| R-1 | Capped message reads hide older or newer decisions | The real oldest decision is not shown; false sense of completeness | `>=N` counts, `CAPPED` in the frame, `OLDEST` qualified as "observed"; gate G1 |
| R-2 | A failed collection is treated as "nothing happening" | False all-clear | Observation store keeps last-good plus gap records (layer 2); stale banner; `n/a` deltas; COV-4 forbids all-clear |
| R-3 | Derived keys change between reports | A decision appears as new and an old one as vanished | `id:derived` tag; vanished items kept open; prefer source-native IDs (section 4.4) |
| R-4 | Transcript text contains instructions or misleading formatting | Renderer output altered, reader misled | Quoted, truncated, ASCII-sanitized text (COM-6); renderer never interprets content |
| R-5 | Observation path consumes or acknowledges coordinator messages | Coordinator misses messages | COM-5: only non-consuming reads; a source that would consume is reported unavailable |
| R-6 | Liveness or completion read as verification | Unverified work treated as done | Four separate fields (VER-1); `NOT DONE` / `NOT VERIFIED` labels; claim-only listed even when healthy |
| R-7 | Root-blocker grouping double counts or hides decisions | Wrong impact sense; a decision missed | Distinct-set counting, `shared`/`see [n]` markers, every decision its own row (BLK-2, BLK-3) |
| R-8 | Renderer drift: each concept reimplements honesty rules differently | Inconsistent or dishonest reports when switching concepts | Shared frame and single derivation layer (section 2); renderers cannot compute coverage |
| R-9 | Report grows past chat height in a busy fleet | Decisions pushed off screen | Fixed row budgets, keyed overflow, footer totals (section 13) |
| R-10 | Operators rely on the snapshot for urgent issues | Late response | FMT-6 disclaimer on every report; urgent alerting left to a separate channel |
| R-11 | Synthetic mockup values mistaken for real data | False evidence in later documents | `SYNTHETIC DEMO DATA` title marker and `DEMO` identifiers in every mockup |

## 17. Open Questions and Feasibility Gates

Gates are checks that must pass before a capability is promised. Failing a gate does not block the default concept; it keeps the corresponding labels in their partial form.

| Gate | Question | What passing unlocks | If it fails |
|---|---|---|---|
| G1 | Is there a complete, non-consuming source that enumerates durable pending decisions (a cursor or event API beyond the 100-row capped reads)? | Exact decision counts; the complete-coverage empty-state wording; a guaranteed oldest decision | Keep `>=N` and "oldest observed" permanently |
| G2 | Do decision and thread records carry source-native stable identifiers and original creation times? | Reliable cross-report deltas; exact ages instead of `seen>=` | Derived keys with `id:derived`; first-seen ages |
| G3 | Is there an authoritative expected-host inventory? | `N of M hosts` and a coverage fraction with a real denominator | `N covered of ? expected` |
| G4 | Is a complete task dependency graph readable per run? | Concept C as a viable alternative; `blocks N` numbers in A | `blocks ?`; C degrades to its UNROOTED list |
| G5 | Which sources expose delivery facts (processed, answered, resolved) per thread? | Concept D's delivery ladder | `?` cells; D not viable as default |
| G6 | Which source can bind checks or reviews to the current revision of a task (independent verification)? | `[checks@rev]` and `[review]` labels; verify-gap detection | All completions remain `[claim]`/`[settled]`; verification unknown |
| G7 | Where will last-good observations and gap records be stored durably across five-minute runs? | Deltas, vanished detection, Concept E TRAIL | Deltas limited to in-session memory; first report after restart prints `n/a` |
| G8 | Which source, if any, will hold human ownership and resolution state (seen, claimed, snoozed, resolved)? | Owner column beyond "human"; separation of seen versus answered | Owner stays `human`; no claimed/snoozed states shown |

**Open design questions for the debate:**

1. Is three lines per decision row (concept A) the right density, or should the busy state switch to two-line rows to show more decisions before overflow?
2. Should the frame's `OLDEST` line be mandatory in every concept, as this spec requires, or only where the body does not already rank by age?
3. Should Concept E's TRAIL line be adopted into the default once gate G7 passes, as a fifth section of A?
4. What age thresholds (15m, 30m, 60m are placeholders) should mark an aging decision, and should they differ by decision kind?
