# Primitive Differential + Threshold Bracketing

Shared probe contract of the sc:troubleshoot protocol. Loaded on demand by Wave 1.6 and later probe/tasklist consumers.

This ref defines the six-kind probe-form table, the 2×2 differential procedure, threshold bracketing, and the card-citation rule used when Wave 1.6 writes discriminator rows for every `surviving=yes` producer.

---

## Section 1: Probe-form table (six primitive kinds)

For each `surviving=yes` producer, list every external primitive the line touches; classify each by the table (the one table; S1.6.4 copies from it):

| kind | exact form | reference form | control (when no passing arm) |
|---|---|---|---|
| read/parse | the read/parse idiom in source, isolated | bulk read of the whole node/stream | read of a file known present |
| call/return | the call with its real args, rc captured | the documented minimal call, same callee | no-op control |
| lookup | the key/name resolution in source | resolution of a key known to exist / direct dump | known key |
| reach | the client as invoked against the producer's endpoint | raw connect to the producer endpoint / same client, known endpoint | known-reachable endpoint |
| permission | the operation on the producer's path | existence/permission probe of the producer path / same op on a path known writable | no-op control on cwd |
| timing | the wait/threshold with elapsed captured | same op with a generous bound | elapsed of a no-op |

---

## Section 2: Differential procedure (2x2)

1. Run exact AND reference on the failing environment AND a passing one (`CONTROL-PROOF: yes: <file:line>`), via the venue Wave 1 step 1b `OBSERVE-VIA` names; one `key=value` line each, pasted verbatim; write the 2×2 into `## Discriminator rows`.
2. Decision: exact≠reference on failing AND both equal on passing ⇒ cause class `substituted primitive` (triage Substituted primitive row); fix form = reference form at every producer hit; propose the fix with its paired verification; apply only through existing fix authorization, never automatically with diagnostic probes. Any cell unobserved or single environment ⇒ `comparator=none`, Diagnosis begins `UNDETERMINED — no comparator`, cap 0.4 (orchestrator cap applied at Wave 5; not a calibrator C-rule).
3. If `refs/probe-packs/<kind>.md` exists for a surviving producer's kind, append its pre-existing rows after the core discriminator rows, once per `(pack path, pack row, producer file:line)` in this invocation. Packs remain optional, append-only and informational, never a decision input; preserve their incident citations and add no rows at run time. Record `core-rows=C`, `pack-rows=P`, `total-rows=C+P` in the tasklist: C ≤ 19; P is bounded by the sum of pre-existing matching-pack row counts over the captured surviving producer identities, not the core cap. One producer's three-row read/parse pack plus full core gives C=19, P=3, total=22. `probe-rows-truncated` still counts omitted base pairs only. Execute core rows first under the shared execution gate; packs never displace core rows. Each core row may run once per applicable failing/reference venue (at most two venues); optional packs get at most three row/venue execution attempts total per S1.6.4 invocation, ordered by pack path, pack row, producer identity, then failing before reference venue. Retain every unexecuted optional row/venue as pending with its budget or authorization/transport reason; no automatic retry or runtime pack extension. Thus full core permits at most 38 core attempts plus 3 optional attempts, not an unbounded pack rerun; captured evidence reads are not execution attempts.

---

## Section 3: Threshold bracketing

Threshold bracketing: trigger = error text or `producers.md` names a numeric limit, OR the same input passes at a smaller value of a countable quantity N. Record N; run N-2/N-4/N-6 in the venue where the symptom reproduces (the failing arm named on the locus card; CI matrix as a worked example of task-type-5 rows), one fixed exit line per cell; no pass ⇒ one extension N-8/N-10/N-12; cap two rounds (own cap, not the shared diagnosability round counter); report `bracket=[<pass>,<fail>] width=<w>` or `UNDETERMINED — no passing value in [N-12, N]`; guard = highest passing value; append to `<output-dir>/bracket.md`; audit line `bracket_trigger=<limit-in-text|passes-smaller>`. The report says the bracket width, never the incident's numbers. Bracket rows follow diagnosability-audit Section 7's viable capture-route and measurement preregistration rules; name the threshold evidence they measure, not S14 unless an actual disputed-datum loss/substitution exists. Enabling CI/upload tasks link these rows and verify capture operationally; unknown outcomes remain unobserved, not passing or false.

---

## Section 4: Card citation rule

A hypothesis card naming an environment property MUST cite a 2×2 row; absent ⇒ Notes `uncited`, calibrated cap 0.5 (C7).

---

## Section 5: Constraints

- Do not name an OS, runtime, or tool in a mandatory row.
- Do not compare one environment to a table of expected values.
- Do not run mutating commands beyond a self-removed temp file.
- Do not require root.
- Do not extend packs at run time.
- Every execution, including brackets and optional packs, obeys SKILL Wave 1 step 1b's authorization/transport gate and S1.6.4's round cap. Artifact-only access reads captured cells; unavailable or refused executions remain pending, never fabricated.
- Do not halt for an unknown measurement; preserve authorization/cap blocks and proceed to the common reporting epilogue.

---

## Loading discipline

Load only needed sections at first use (S1 probe-form table, S2 differential, S3 threshold bracketing, S4 card citation, S5 constraints): S1.6.0b step 4 classifies producer expressions with Section 1 (no pattern column or mandatory per-kind regex), S1.6.4 copies the pair shape, and Wave 3 splitting may load Section 1 after audit bypass. Tasklist creation/extension always consumes diagnosability-audit Section 7's schema, eligibility, counter and execution gates once, without rerunning the skipped audit.
