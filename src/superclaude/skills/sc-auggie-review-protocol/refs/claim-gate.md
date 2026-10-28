# Claim Gate

Wave 3 of the protocol uses this file to decide which reviewer candidates are published as defects. Location grounding only proves that a cited line exists. The claim gate adds one admission step after grounding and one ledger (`candidates.json`) that feeds `REVIEW.md`, the counts, PR posting, inline comments and the remediation offer.

The orchestrator decides. The reviewer supplies a structured `claim` block as input; the orchestrator re-Reads every cited line before it relies on it. "Verified" in this file means the orchestrator Read the cited line in this run. Reviewer `confidence`, `severity_hint` and `disposition_hint` are inputs only. This gate checks evidence and structure; it does not prove a model followed it.

## Dispositions

Every grounded candidate ends with exactly one disposition:

| Disposition | Meaning |
|---|---|
| `defect` | The claim is supported: a violated requirement and a harm are both shown. Published. |
| `unproven` | The evidence is missing, speculative or not verified. Kept locally. |
| `rejected` | A verified guard, producer or schema refutes the claim, or the mechanism is not present in the target. Kept locally. |
| `intentional_limitation` | A verified deliberate policy states the claimed harm as its trade-off. Kept locally. |
| `documented_prerequisite` | A verified documented prerequisite explains the claimed harm. Kept locally. |

Only `defect` carries a severity. Every other disposition has `severity: null`. Doubt is never expressed as a lower severity.

## Location grounding

Location grounding is a drop. A cited line that does not exist, or whose snippet does not match, goes to `dropped_ungrounded[]` with its reason and is never converted to another disposition.

Head-mismatch exception (PR mode with `head_match: false`): a cited line that cannot be checked at all (out of diff, with the head object unavailable or `head_object_check: mismatch`) is not a mismatch. Such a candidate is kept with `in_diff: false` and becomes `unproven` with reason `head_mismatch_context_unavailable`. When `head_object_check: match`, an out-of-diff cited line is validated with `git show <headRefOid>:<path>`. In-diff lines are still validated against the new side of `diff.patch`.

## Claim classes

The orchestrator derives the class from `category`:

| Class | Categories | Required verified evidence |
|---|---|---|
| `behavioral` | security, data-integrity, correctness, concurrency, resource-leak, error-handling, api-contract, performance, logging | `reachability.entrypoint` (plus `reachability.producer` for input-shape claims) and the guards checked |
| `structural` | architecture, layering, coupling, anti-pattern, dead-code, tests, docs, naming, style | The violating site plus a convention source, or a mechanical fact (line count, or a zero-hit Grep with pattern and roots) |

A structural claim that asserts a runtime consequence must meet the behavioral requirements for that consequence, or the consequence is excluded (see Claim scope).

Mocked-only dispatch does not count as an entrypoint.

### Protocol and instruction claims

For evidence kind `protocol_literal` the "entrypoint" is the `path:line` of the instruction that prescribes the step, inside a protocol path that is actually invoked. The "producer" is the `path:line` of the consumer's precondition or contract that the step must satisfy. This makes literal contract defects admissible without a model run (see Narrow contract defects).

## Claim scope

Admission evaluates each entry of `claim.consequences[]` separately against the class requirements and the admission table. The reviewer lists each distinct consequence as its own string; `claim.harm` is the one it considers best supported.

- The admitted record keeps only supported consequences in `claim.harm`. Every other consequence goes to `excluded_consequences[]` as `{consequence, reason}`, where `reason` starts with an admission row id (`A1` to `A6`) or `other:`.
- A candidate is a `defect` when at least one consequence is supported and every other table condition holds.
- Severity is graded only on the admitted harm. `severity_basis` names the rubric tier definition the admitted harm meets (see severity_basis ids). An excluded consequence never contributes to severity, the summary, inline comment text or remediation scope.
- When no consequence is supported, the disposition comes from the first matching table row (normally A6, `unproven`), and all consequences are listed in `excluded_consequences[]`.
- Rendering: a defect with non-empty `excluded_consequences[]` gets one line per excluded consequence in `REVIEW.md`: `Not established: <consequence> (<reason row>)`. `NOT-ADMITTED.md` lists the same lines under the defect's id.

## Narrow contract defects

A `protocol_literal` claim that a prescribed instruction cannot be completed as written is admissible as a `defect` with harm "the prescribed step cannot be completed as written". Examples: a required input is not supplied, two instructions cannot both be satisfied, or a prescribed command's precondition is unmet by the prescribed arguments.

Both anchors must be verified: the prescribing instruction (the entrypoint) and the violated precondition (the producer). A downstream stop that catches the failure does not refute the narrow defect; it only bounds its harm. Claims of additional consequences (wrong success, data loss, silent pass) are evaluated separately under Claim scope and are excluded unless they are traced.

## Admission table

The orchestrator evaluates this table top to bottom for each candidate and records the matching row ids in `disposition_reasons[]`. "Verified" means the orchestrator Read the cited line in this run.

| Row | Condition | Disposition |
|---|---|---|
| A1 | A verified guard on every verified entrypoint blocks the trigger, or the only path to `observed_at` is a seam whose documented caller precondition the claim violates | `rejected` |
| A2 | The triggering input is shown refused or not produced by the verified producer or schema | `rejected` |
| A3 | `intent_finding = deliberate_policy` verified, the claimed harm is the trade-off the policy states, and no higher-precedence requirement is shown violated through a supported input | `intentional_limitation` |
| A4 | `intent_finding = documented_prerequisite` verified, and no evidence shows the prerequisite unmet in an actual supported rollout | `documented_prerequisite` |
| A5 | The mechanism is fixed at the attribution reference and the target is current state (`target.mode` is `diff` or `snapshot`) | `rejected` with reason `not_present_in_target` |
| A6 | Any of: `evidence_kind = speculative`; class-required evidence missing or not verified (REQ-006, REQ-007); every consequence excluded; `harm` equal to the cited `evidence` text; `violated_requirement` empty; `qualification` present without a verified `scope_citation`; `confidence: low` without `hedge_resolved`; category `security` or `data-integrity` without a `severity_basis` naming the rubric definition the harm meets | `unproven` |
| A7 | Everything else holds and the refutation record is complete with no blocking entry | `defect` |

In row A6, REQ-006 and REQ-007 are the requirements of the sections "Claim classes" and "Protocol and instruction claims" above.

Reason strings in `disposition_reasons[]` and `excluded_consequences[].reason` start with a row id or `other:`. Examples: `A6 head_mismatch_context_unavailable`, `A5 not_present_in_target`, `A6 admission_incomplete`, `other:mechanism_conflict`, `other:harm_below_floor`.

### Policy challenge

A3 does not apply when the candidate cites a higher-precedence requirement that the policy violates (a spec over a doc comment; a safety or availability requirement over a convenience behavior) and cites harm through a supported input. The row is then A7 and the record keeps `policy_challenge: <path:line>`.

### Availability and visibility

Availability and visibility harm counts: a supported input that silently stalls, hides or discards valid work is harm without data corruption. A fail-closed refusal of unsupported or ambiguous input is not harm by itself.

### Unknown evidence

Unknown, missing or ambiguous evidence (absent identity, unorderable events, revoked state) is never treated as positive evidence for a less-safe path.

### Synthetic input

Synthetic input is admissible only through `producer`: the input must be accepted by the verified producer, schema or an official contract. No record claims live frequency unless `evidence_kind: runtime_reproduced` with a measured rate.

### Low confidence

`confidence: low` is `unproven` unless the orchestrator records `hedge_resolved: <path:line>` citing the line that resolves the doubt stated in the reviewer's `why`.

### Qualification

`claim.qualification` is `null` or `{scope, scope_citation}`, where `scope_citation` is the `path:line` of a documented supported configuration. A qualified defect whose category is not `security` or `data-integrity` and whose harm does not meet a rubric Critical criterion is capped at Medium. An unestablished condition is `unproven` (A6). Demonstrated harm with unknown frequency is not a qualification and is not capped.

## Refutation record

Every `defect` carries `refutation[]` with one entry per applicable row A1 to A5. Each entry is a string in exactly one of three forms:

| Form | Syntax | Example |
|---|---|---|
| Checked line | `checked: <path:line>`; guard entries append one space and `blocks` or `does_not_block` | `checked: src/app/handler.py:12 does_not_block` |
| Not applicable | `not_applicable: <reason>` | `not_applicable: no policy comment exists for this path` |
| Mechanical fact | `mechanical: <fact>`, where `<fact>` is `grep <pattern> in <root>[,<root>...] = 0 hits` or `lines <path> = <n>` | `mechanical: grep retry_limit in src/,plugins/,tests/ = 0 hits` |

A second mechanical example: `mechanical: lines src/app/service.py = 412`.

A structural defect's mechanical fact (Claim classes) uses the `mechanical:` form.

- `refutation_citation: <path:line>` is required on every `rejected`, `intentional_limitation` and `documented_prerequisite` record. It is the guard, producer, policy or prerequisite line. Each such record also carries a reason row id in `disposition_reasons[]`.
- Caller search runs only when no entrypoint is cited or the cited one fails the Read. It Greps under `src/`, `plugins/` and `tests/` and records the pattern and the roots.
- `admission_budget{candidates_total, checked, incomplete, wall_seconds}` is recorded. Candidates not finished are `unproven` with reason `A6 admission_incomplete` and set `coverage.complete = false`.

## severity_basis ids

`severity_basis` is `<tier>:<n>`, where `<n>` is the 1-based position of the matching bullet in that tier's definition list in `refs/severity-rubric.md`, section "The five tiers". The valid ids, one per bullet:

| Tier | Ids | Bullets in order |
|---|---|---|
| Critical | `critical:1` to `critical:4` | 1 exploitable security defect; 2 data-integrity defect; 3 crash on startup or default path; 4 regulatory or compliance defect |
| High | `high:1` to `high:6` | 1 latent security weakness; 2 correctness defect on a non-default path; 3 resource leak; 4 API contract break; 5 concurrency hazard; 6 significant architectural drift |
| Medium | `medium:1` to `medium:5` | 1 code-quality issue with concrete consequences; 2 performance concern without immediate user impact; 3 anti-pattern manifesting once; 4 test gap on non-trivial logic; 5 stale or contradictory docs |
| Low | `low:1` to `low:3` | 1 cost of fixing exceeds cost of living with it; 2 opportunistic improvement; 3 pattern exists elsewhere |
| Nit | `nit:1` to `nit:3` | 1 naming; 2 comments; 3 style |

Valid id list: `critical:1`, `critical:2`, `critical:3`, `critical:4`, `high:1`, `high:2`, `high:3`, `high:4`, `high:5`, `high:6`, `medium:1`, `medium:2`, `medium:3`, `medium:4`, `medium:5`, `low:1`, `low:2`, `low:3`, `nit:1`, `nit:2`, `nit:3`.

Every defect's `severity_basis` is one of these ids. The id names the definition the admitted harm meets, so it need not equal the final tier: rubric step 4 can drop a pre-existing defect one tier. A qualified defect whose `severity_basis` is a `critical:<n>` id is exempt from the Medium cap.

## Attribution

### Target fields

Wave 0 records `target{mode, base, head, head_match, local_sha, worktree_dirty, head_object_check, evidence_source}`. Snapshot mode records `base: null`. `head_object_check` is `match` or `mismatch`, or `null` when no head-object check was needed.

### Evidence-source rules

`evidence_source` is `local_read`, `head_object` or `diff_new_side`.

- `local_read` is not used when `target.mode == pr` and `head_match == false`.
- Under PR head mismatch, context hops (entrypoint, guards, producer, intent) use the head object only when `head_object_check == match`. `match` requires `headRefOid` equal before and after `gh pr diff`, `git cat-file -e <oid>` success, and agreement of every cited in-diff line with the diff's new side.
- Otherwise the source is `diff_new_side`, and any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`.

### Head-object check

Evaluate the `match` test once per review (`headRefOid` is compared before and after `gh pr diff` when the diff is collected) and record the result in `target.head_object_check`. A `head_object` hop in a defect's `evidence_sources[]` is legal only when that value is `match`.

### Explicit diff committed reads

In explicit `--diff` mode the target is committed history. Reads for admission and for `current_status` use `git show HEAD:<path>`, not the working tree, even when `worktree_dirty` is true. Only implicit dirty-tree diff mode and snapshot mode use `local_read` of uncommitted edits. In explicit `--diff` mode these committed reads are recorded in `evidence_sources[]` with source `local_read`; the `head_object` label is reserved for PR head-mismatch reads that pass the head-object check.

### Introduced and current status

- Each record carries `attribution.introduced_in`: `head`, `base`, `unknown` or `not_applicable_snapshot`, from comparing `git show <base>:<path>` at the mechanism. Hunks absent from `HEAD` get `unknown`.
- `attribution.current_status` is `present`, `absent` or `unchecked`, and is set to `present` or `absent` only when a distinct current ref is known.
- Snapshot mode uses `not_applicable_snapshot` everywhere and never says "introduced", "regression" or "this PR".

### Mode-derived scope

Scope comes from `target.mode`: `pr` is as-submitted; `diff` and `snapshot` are current state. A `pr` defect that was fixed later keeps `defect` with `current_status: absent` and `remediation_eligible: false`; `current_status: absent` on a defect requires `target.mode == pr`. A pre-existing defect (`introduced_in: base`) stays admissible and is labeled pre-existing; rubric step 4 applies.

## Mechanism dedupe

Set `mechanism_key = <root-cause path>::<enclosing symbol or heading>::<normalized expected behavior>` and group by it across chunks, personas and lines. Two candidates on one line with different keys stay separate.

- **Members.** Keep all member ids and citations; never count votes. The group root (the decider, `merged_into: null`) lists every member id in `members[]`, its own first; an unmerged singleton lists only its own id. Every other member record has `members: []` and `merged_into: <decider id>`, so each member id appears in exactly one `members[]`.
- **Ranking.** Rank members by evidence kind: `runtime_reproduced` > `static_traced` = `protocol_literal` > `speculative`.
- **Refutation union.** When the group's final disposition is `defect`, every blocking citation recorded on any member (its `refutation_citation`, or a `refutation[]` entry marked `blocks`) must be answered in the decider's `refutation[]` as `checked: <same path:line> does_not_block`, with that citation. A group that is not a defect has nothing to answer: its blocking citation is the reason it is not a defect.
- **Strict dominance.** The group is a `defect` only if the decider strictly outranks every non-defect member. Otherwise the group is `unproven` with reason `other:mechanism_conflict`.
- **Non-defect groups.** The group takes the highest-rank member's disposition. Equal rank gives `unproven` with `other:mechanism_conflict`.
- **Losers.** Losers carry `merged_into: <id>`, take the group's final `disposition`, and copy the decider's final `severity`. A loser of a defect group has the same non-null severity; a loser of a non-defect group has `severity: null`. So that every per-record invariant holds for a loser, it also copies the rest of the decider's final admission fields (every field except `id`, `members`, `merged_into`, `file`, `line`, `in_diff`, `evidence_sources`, and the two blocking-evidence fields in the next sentence). A loser keeps its own non-null `refutation_citation` and its own `refutation[]` entries marked `blocks`, so the refutation union can still see them; its `refutation[]` is those entries followed by the decider's entries, and it takes the decider's `refutation_citation` only when its own is null. Losers are never graded, counted, rendered or remediated on their own.
- **No maximum severity.** Severity is computed after the merge from the decider's admitted harm, never as a maximum of hints.
- **Excluded consequences.** The excluded consequences of all members are unioned into the group.
- **Caveat rule.** A finding that restates a caveat in the PR description is no longer dropped. It is evaluated by rows A3 and A4, and its record stays in the ledger.

## Ledger schema

`<output-dir>/candidates.json` follows `schema: auggie-review-candidates/1`. The schema id stays at version 1 because the schema has never been released.

Top-level fields:

| Field | Content |
|---|---|
| `schema` | `auggie-review-candidates/1` |
| `target` | The Attribution target fields |
| `coverage` | `{chunks_planned, chunks_completed, chunks_skipped[], persona_passes[], input_truncated, complete}` |
| `admission_budget` | `{candidates_total, checked, incomplete, wall_seconds}` |
| `jq_exit` | Exit code of the invariant check. `null` or absent while the check runs; the program never reads it |
| `candidates[]` | One record per grounded finding (below) |
| `remediation_ids[]` | Ids of unmerged, `remediation_eligible`, Critical/High defects |
| `remediation_count` | `{critical, high}`, computed from `remediation_ids` |
| `dropped_ungrounded[]` | `{id, reason}` for each finding dropped at grounding |
| `run_status` | `success`, `partial` or `failed`: the status computed under "Status mapping" before the invariant check runs |
| `findings_count` | `{critical, high, medium, low, nit}`: the same values the Output Contract reports |

Candidate fields: `id`, `members[]`, `mechanism_key`, `merged_into`, `disposition`, `disposition_reasons[]`, `severity`, `severity_basis`, `category`, `class`, `confidence`, `hedge_resolved`, `file`, `line`, `in_diff`, `claim`, `excluded_consequences[]`, `refutation[]`, `refutation_citation`, `attribution{introduced_in, current_status}`, `remediation_eligible`, and `evidence_sources[]`.

- `claim` is the reviewer's claim block as verified: `observed`, `observed_at[]`, `expected`, `violated_requirement`, `intent_sources[]`, `intent_finding`, `reachability{entrypoint, producer, guards_checked[], caller_search}`, `harm`, `consequences[]`, `counterevidence[]`, `evidence_kind`, `qualification`, `disposition_hint`. After admission `harm` holds only supported consequences.
- `evidence_sources[]` has one `{hop, path_line, source}` entry per Read used for admission. `hop` is one of `observed`, `entrypoint`, `producer`, `guard`, `intent`, `prerequisite`, `scope`. `source` is one of `local_read`, `head_object`, `diff_new_side`.
- `run_status`, `findings_count` and every candidate's `evidence_sources[]` are all written before the invariant check runs, so every invariant is evaluable from `candidates.json` and `REVIEW.md` alone.
- Ids are `<findings-file-stem>#<n>`, with one `n` sequence across `findings[]` and `cross_cutting_observations[]` of the same file. Ids are unique across the ledger.
- A merged loser keeps its own record; the rules for its fields are in Mechanism dedupe.
## Status mapping

`run_status` is computed before the invariant check:

- `failed` only for a ledger or invariant failure: missing `candidates.json`, a missing or non-zero `jq_exit` after Wave 2 starts, or `jq` absent at the preflight (reason `invariant_check_unavailable`).
- `partial` keeps the baseline causes (for example findings dropped at grounding, a skipped chunk or failed agent run, or a failed PR post) and is also the status whenever `coverage.complete == false`.
- `success` otherwise. `coverage.complete == false` never yields `success`. The empty-diff short-circuit stays `success`.
- `REVIEW.md` and `audit.log` are written on every status.

The reported status equals the ledger's `run_status` when `jq_exit == 0`, and is `failed` otherwise. The Output Contract's `findings_count` equals the ledger's `findings_count`.

## Report tag grammar

`REVIEW.md` has one place per defect. Tags are how the invariant check ties report entries to ledger ids.

- Heading entries use `#### C1. <Short title> (id: <id>)`: the tag `(id: <id>)` ends the heading line.
- List-item entries are top-level list items that start with `<!-- id: <id> -->` immediately after the list marker.
- Only these two tag forms are recognized. Fenced code blocks are removed from the scanned text before matching, so excerpts and quoted template text are never scanned. Text such as `(id: x)` in a paragraph is not a tag.
- Entry boundaries: column-0 field bullets under a heading entry belong to that entry and are not entries. A heading entry runs to the next heading of the same or higher level. A list-item entry runs to the next list item at the same or shallower indentation, or to the next heading; its continuation lines are blank or indented, so a non-blank line at column 0 that is not a list item also ends it.
- Every Critical and High defect, including a cross-cutting one, is a heading entry under `## Findings`.
- Top-level list-item entries are used only for Nits (in the Nits subsection of `## Findings`) and for Medium or Low defects in `## Architectural / Cross-Cutting Observations`. Cross-Cutting list items appear only in that section.
- Each defect entry carries `**Evidence kind**: <evidence_kind>` and, when present, its `Not established` lines and qualification.
- A `path:line` pattern appears only inside defect entries, except in the header block above the first section.
- `REVIEW.md` has no `## Not Admitted` heading. It has one counts line instead: `Not admitted: U unproven, R rejected, L intentional limitations, P documented prerequisites, M merged (see NOT-ADMITTED.md)`.

## Invariant check

The invariant program below checks the structure of `candidates.json` and its consistency with `REVIEW.md`. It checks invariants J1 to J22 plus a shape check (`SHAPE`) that fails a ledger missing `run_status`, `findings_count`, `coverage`, `target` or any candidate's `evidence_sources`. It does not judge whether a guard really blocks or a sentence really states intent; those stay with the orchestrator.

Invocation, once per review, after `REVIEW.md` and `NOT-ADMITTED.md` are written and before any Wave 4 action: `jq -e -n --slurpfile ledger candidates.json --rawfile review REVIEW.md -f <extracted block>`.

- The exit code is recorded as `jq_exit` in `candidates.json` and in `audit.log`. Exit 0 means every invariant holds. The program never reads `jq_exit`, which is `null` or absent while it runs.
- The program reads only the slurped ledger and the raw `REVIEW.md` text. It ends in a single boolean expression, so an empty ledger or empty report yields `true`, never "no output".
- The program is passed with `-f`, so no shell quoting applies. It contains no single-quote character, so pasting it inline inside single quotes is also safe.
- Fenced code blocks are removed from `REVIEW.md` before scanning. Only heading-line `(id: <id>)` tags and `<!-- id: <id> -->` list-item tags are recognized (see Report tag grammar).
- Each check is a key of the `checks` object (`SHAPE`, `J1` to `J22`). Tests and diagnostics replace the last line of the block to list the failing keys.
- J3 and the other per-defect checks apply to every record whose disposition is `defect`, merged losers included (they copy the decider's fields, see Mechanism dedupe). J8 applies to each defect decider whose group has more than one record.
- A record is an entry of `REVIEW.md` when it is a `####` heading under `## Findings`, a top-level list item in the Nits subsection of `## Findings`, or a top-level list item under `## Architectural / Cross-Cutting Observations`.

Preflight: before Wave 3 check that `jq` is available (for example `command -v jq`). If it is not, the status is `failed` with reason `invariant_check_unavailable`, and `REVIEW.md` and `audit.log` are still written. `allowed-tools` is not a prerequisite check.

```jq
# Invariant program J1-J22. Reads only $ledger (slurped candidates.json) and $review (raw REVIEW.md).
# Never reads jq_exit. Contains no single-quote character, so it is safe to paste inside single quotes.
def L: ($ledger[0] // {});
def C: (L.candidates // []);
def PL: "^[^\\s:]+:[0-9]+(-[0-9]+)?$";
def ispl: type == "string" and test(PL);
def nz: type == "string" and length > 0;
def DEF: C | map(select(.disposition == "defect"));
def UD: DEF | map(select(.merged_into == null));
def IDS: C | map(.id);
def BYID: C | map({key: (.id | tostring), value: .}) | from_entries;
def root_of($m; $id; $lim):
  {cur: $id, n: 0}
  | until(($m[.cur].merged_into // null) == null or .n > $lim; {cur: $m[.cur].merged_into, n: (.n + 1)})
  | if .n > $lim then null else .cur end;
def BASIS: ["critical:1","critical:2","critical:3","critical:4","high:1","high:2","high:3","high:4","high:5","high:6","medium:1","medium:2","medium:3","medium:4","medium:5","low:1","low:2","low:3","nit:1","nit:2","nit:3"];
def SEV: ["critical","high","medium","low","nit"];
def formok: type == "string" and (
  test("^checked: [^\\s:]+:[0-9]+(-[0-9]+)?( blocks| does_not_block)?$")
  or test("^not_applicable: \\S")
  or test("^mechanical: (grep .+ in [^ ]+ = 0 hits|lines [^ ]+ = [0-9]+)$"));
def blocking: [(.refutation_citation // empty), ((.refutation // [])[] | strings | capture("^checked: (?<c>[^ ]+) blocks$").c)];
def FENCE: "^ {0,3}(?<f>" + ([96] | implode) + "{3,}|~{3,})(?<info>.*)$";
def rows:
  reduce (($review | split("\n"))[] | rtrimstr("\r")) as $l ({f: null, o: []};
    ([$l | capture(FENCE)] | .[0]) as $m
    | if .f == null then
        if $m != null then .f = {c: ($m.f | .[0:1]), n: ($m.f | length)} else .o += [$l] end
      elif $m != null and ($m.f | .[0:1]) == .f.c and ($m.f | length) >= .f.n and ($m.info | test("^\\s*$")) then .f = null
      else . end) | .o;
def ann:
  reduce rows[] as $l ({sec: "header", sub: null, ent: null, kind: null, n: 0, out: []};
    ($l | test("^#{1,6}\\s")) as $head
    | (if $head then ($l | capture("^(?<h>#{1,6})\\s").h | length) else 0 end) as $lvl
    | (($l == "") or ($l | test("^\\s"))) as $cont
    | if $head then
        if $lvl == 2 then
          .sec = (if ($l | test("^##\\s+Findings")) then "findings" elif ($l | test("^##\\s+Architectural")) then "cross" else "other" end)
          | .sub = null | .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: true}]
        elif $lvl == 3 then
          .sub = (if ($l | test("[Nn]its")) then "nits" else "other" end) | .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: true}]
        elif $lvl == 4 and .sec == "findings" then
          .n += 1 | .ent = .n | .kind = "h"
          | .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: true}]
        elif $lvl >= 5 and .kind == "h" then
          .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: true}]
        else
          .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: true}]
        end
      elif ($l | test("^[-*]\\s")) then
        if .kind == "h" then
          .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: false}]
        elif (.sec == "cross" or (.sec == "findings" and .sub == "nits")) then
          .n += 1 | .ent = .n | .kind = "l"
          | .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "l", head: false}]
        else
          .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: false}]
        end
      elif $cont then
        .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: .kind, head: false}]
      elif .kind == "h" then
        .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: false}]
      else
        .ent = null | .kind = null
        | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: false}]
      end) | .out;
def HTAG: "^#{1,6}\\s.*\\(id: (?<id>[^)\\s]+)\\)\\s*$";
def LTAG: "^\\s*[-*]\\s+<!-- id: (?<id>[^\\s]+) -->";
def tagof: (try capture(HTAG).id catch null) // (try capture(LTAG).id catch null);
def TAGS: [ann[] | .t | tagof | select(. != null)];
def ENTRIES: [ann[] | select(.e != null)] | group_by(.e) | map({sec: .[0].sec, k: .[0].k, start: .[0].t, lines: map(.t), id: ((.[0].t | tagof) // null)});
def haspl: test("(?:[A-Za-z0-9_@+.-]+/)+[A-Za-z0-9_@+.-]+:[0-9]+|[A-Za-z0-9_@+-]+\\.[A-Za-z0-9]{1,10}:[0-9]+");
def checks:
  {
    "SHAPE": (try (
      (L.run_status | IN("success","partial","failed"))
      and ((L.findings_count | type) == "object")
      and all(SEV[]; . as $s | (L.findings_count[$s] | type) == "number")
      and ((L.candidates | type) == "array")
      and all(C[]; (.evidence_sources | type) == "array"
        and all(.evidence_sources[]; (.hop | IN("observed","entrypoint","producer","guard","intent","prerequisite","scope"))
          and (.source | IN("local_read","head_object","diff_new_side")) and (.path_line | ispl)))
      and ((L.target | type) == "object")
      and ((L.coverage | type) == "object") and ((L.coverage.complete | type) == "boolean")
      and ((L.coverage.chunks_skipped | type) == "array") and ((L.coverage.input_truncated | type) == "boolean")
    ) catch false),
    "J1": (try all(C[]; (.disposition | IN("defect","unproven","rejected","intentional_limitation","documented_prerequisite")) and (.class | IN("behavioral","structural"))) catch false),
    "J2": (try all(C[]; ((.severity != null) == (.disposition == "defect")) and (.severity == null or (.severity | IN(SEV[])))) catch false),
    "J3": (try all(DEF[];
        (.claim.evidence_kind | IN("runtime_reproduced","static_traced","protocol_literal"))
        and (.claim.harm | nz) and (.claim.violated_requirement | nz)
        and ((.refutation | type) == "array") and ((.refutation | length) > 0) and all(.refutation[]; formok)
        and (if .class == "behavioral" then (.claim.reachability.entrypoint | nz)
             else (((.claim.intent_sources // []) | length) > 0) or any((.refutation // [])[]; startswith("mechanical: ")) end)) catch false),
    "J4": (try all(C[] | select(.disposition | IN("rejected","intentional_limitation","documented_prerequisite"));
        any((.disposition_reasons // [])[]; test("^A[1-7]")) and (.refutation_citation | ispl)) catch false),
    "J5": (try (all(C[]; all((.disposition_reasons // [])[]; type == "string" and test("^(A[1-7]|other:)")))
        and all(C[]; all((.excluded_consequences // [])[]; (.reason | type) == "string" and (.reason | test("^(A[1-7]|other:)"))))) catch false),
    "J6": (try (((IDS | length) == (IDS | unique | length))
        and (([C[].members[]?] | length) == ([C[].members[]?] | unique | length))
        and (((L.dropped_ungrounded // []) | map(if type == "object" then .id else . end)) as $d
             | all(([C[].members[]?] + IDS)[]; . as $i | ($d | index($i)) == null))) catch false),
    "J7": (try (BYID as $m | (C | length) as $n | all(C[] | select(.merged_into != null);
        ($m[.merged_into] != null) and (root_of($m; .id; $n) as $r | $r != null and $m[$r] != null))) catch false),
    "J8": (try (BYID as $m | (C | length) as $n | all(C[] | select(.disposition == "defect" and .merged_into == null);
        . as $r
        | ([C[] | select(root_of($m; .id; $n) == $r.id)]) as $g
        | if ($g | length) < 2 then true
          else all(($g | map(blocking) | flatten | unique)[]; . as $c | any(($r.refutation // [])[]; . == ("checked: " + $c + " does_not_block")))
          end)) catch false),
    "J9": (try (L.findings_count as $f | all(SEV[]; . as $s | $f[$s] == (UD | map(select(.severity == $s)) | length))) catch false),
    "J10": (try (([UD[] | select(.remediation_eligible == true and (.severity | IN("critical","high"))) | .id] | sort) as $e
        | ((L.remediation_ids // []) | sort) == $e
        and (L.remediation_count.critical == ([UD[] | select(.id | IN($e[])) | select(.severity == "critical")] | length))
        and (L.remediation_count.high == ([UD[] | select(.id | IN($e[])) | select(.severity == "high")] | length))) catch false),
    "J11": (try (all(C[] | select(.attribution.current_status == "absent"); .remediation_eligible == false)
        and all(DEF[] | select(.attribution.current_status == "absent"); L.target.mode == "pr")) catch false),
    "J12": (try (if L.target.mode == "snapshot" then all(C[]; .attribution.introduced_in == "not_applicable_snapshot") else true end) catch false),
    "J13": (try ((if L.target.mode == "pr" and L.target.head_match == false then
          (L.target.evidence_source != "local_read")
          and all(C[]; all((.evidence_sources // [])[]; .source != "local_read"))
        else true end)
        and all(DEF[]; all((.evidence_sources // [])[] | select(.source == "head_object"); L.target.head_object_check == "match"))) catch false),
    "J14": (try (all(C[] | select(.claim.qualification != null); .claim.qualification.scope_citation | ispl)
        and all(DEF[];
          (.severity_basis | IN(BASIS[]))
          and (if .claim.qualification != null and (.category | IN("security","data-integrity") | not) and ((.severity_basis | startswith("critical:")) | not)
               then (.severity | IN("medium","low","nit")) else true end))) catch false),
    "J15": (try all(DEF[] | select(.confidence == "low"); .hedge_resolved | nz) catch false),
    "J16": (try ((if L.coverage.complete == false then L.run_status != "success" else true end)
        and (if L.coverage.complete == true then
               ((L.coverage.chunks_skipped // []) | length) == 0 and L.coverage.input_truncated == false
               and all(C[]; all((.disposition_reasons // [])[]; contains("admission_incomplete") | not))
             else true end)) catch false),
    "J17": (try ((UD | map(.id)) as $u | all(TAGS[]; . as $t | ($u | index($t)) != null)) catch false),
    "J18": (try ([ENTRIES[] | select(.sec == "findings" and .k == "h") | .id] as $f | all(UD[] | select(.severity | IN("critical","high")); . as $d | ($f | index($d.id)) != null)) catch false),
    "J19": (try ((ENTRIES | length) == (TAGS | length) and all(ENTRIES[]; .id != null)) catch false),
    "J20": (try all(ann[] | select(.sec != "header" and .e == null); .t | haspl | not) catch false),
    "J21": (try (BYID as $m | all(ENTRIES[]; . as $e
        | ([$e.lines[] | capture("\\*\\*Evidence kind\\*\\*:\\s*`?(?<k>[a-z_]+)`?").k]) as $k
        | ($k | length) > 0 and $m[$e.id].claim.evidence_kind == $k[0])) catch false),
    "J22": (try all(rows[]; test("^#{1,6}\\s+Not Admitted"; "i") | not) catch false)
  };
checks | all(.[]; .)
```
