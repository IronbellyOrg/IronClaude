---
title: "Auggie Claim Gate"
type: architecture
format: spec
status: draft-for-planning
created: "2026-10-20"
feature_baseline: 713d8e423bd9a2469ea1418fafd6edccbb88caaa
master_snapshot: c4606ce72979838dd730044a08be79cc416ccfe6
driving_requirements: /config/workspace/IronClaude/.dev/brainstorms/20261020-043737-auggieClaimGate/merged-requirements.md
enrichment:
  - /config/workspace/IronClaude/.dev/brainstorms/20261020-043737-auggieClaimGate/enrichment/codebase-context.md
  - /config/workspace/IronClaude/.dev/brainstorms/20261020-043737-auggieClaimGate/enrichment/evidence-context.md
  - /config/workspace/IronClaude/.dev/brainstorms/20261020-043737-auggieClaimGate/enrichment/consumer-followup.json
---

# Auggie Claim Gate: Design Specification

## 0. How to read this document

This is the authoritative design for the implementation session. It is produced by `/sc:design` from the brainstorm's merged requirements, which ended with adversarial status `partial` (BLOCKED_BY_INVARIANTS, one open HIGH invariant and twelve open MEDIUM/LOW items in its section 17). This design resolves every section 17 item in section 9. Where this design and the merged requirements differ, this design wins; the merged requirements remain the rationale record and are cited as `MR §n`.

Requirements carry stable ids `REQ-001` to `REQ-046`. Acceptance tests carry ids `AT-01` onward. Every REQ maps to at least one AT (section 10).

Nothing in this design is a measured improvement. It specifies a gate, its checks and its tests. Semantic effectiveness on real reviews stays unproven until the separately authorized live evaluation in section 11.3 runs.

## 1. Problem and decision summary

auggie-review's only truth gate between a reviewer candidate and a published defect is location grounding: the cited `file:line` exists and the snippet matches (feature-baseline `SKILL.md` Wave 3 step 3). A candidate that passes becomes a graded defect. Category floors can raise it; low confidence lowers it one tier. There is no "not a defect" outcome, no causal evidence fields, no attribution model and location-only dedupe (MR §4 gaps G1-G5).

The design adds one admission step and one ledger. Decisions:

| Decision | Choice |
|---|---|
| Where | One seam: Wave 3 step 3b, after location grounding, before dedupe and severity |
| What decides | The orchestrator, from reviewer-supplied structured `claim` evidence that it must re-Read. Reviewer hints are inputs only |
| Outcomes | Exactly one disposition per grounded candidate: `defect`, `unproven`, `rejected`, `intentional_limitation`, `documented_prerequisite`. Only `defect` gets a severity |
| Single source | `candidates.json` ledger feeds `REVIEW.md`, counts, PR posting, inline comments and the remediation offer |
| Determinism | One fenced `jq -e` program checks structure and ledger-to-report consistency only. Semantics stay with the orchestrator |
| New files | One ref, `refs/claim-gate.md`; tests under `tests/skills/` |
| Not added | No new agent, Python production module, CLI flag, tool permission, or `pr_submit/*.py` change |

## 2. Baseline and touched surfaces

The implementation targets the feature-baseline sources. Installed `/config/.claude/skills/sc-auggie-review-protocol/{SKILL.md,refs/*}` match those blobs exactly (verified by git blob hash). The installed global agent and command are stale and are not edited (REQ-045).

| Path (repo-relative, `src/` is source of truth) | Change |
|---|---|
| `src/superclaude/skills/sc-auggie-review-protocol/refs/claim-gate.md` | New. Dispositions, claim classes, admission table, claim-scope rules, refutation record, attribution, mechanism dedupe, ledger schema, report-tag grammar, exactly one fenced `jq` block |
| `src/superclaude/skills/sc-auggie-review-protocol/refs/auggie-prompts.md` | `claim` block added to the output contract for `findings[]` and `cross_cutting_observations[]`; quality-bar bullets |
| `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` | Output Contract fields; Wave 0 target provenance; Wave 2 exit criterion; Wave 3 steps 3b/3c/4/5/5b/6/6b/7 as pointers into `claim-gate.md`; report template; Wave 4 gates; Will Do/Will Not |
| `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` | New section "Admission precedes grading"; two decision-mode rows |
| `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` | Offer gate, Phase A scope sentence, WHERE list |
| `src/superclaude/agents/auggie-reviewer.md` | Responsibilities 5 and 6 and Output Format |
| `src/superclaude/commands/auggie-review.md` | Boundaries bullets |
| `tests/skills/test_auggie_claim_gate_contract.py` | New. Protocol-text presence/absence checks |
| `tests/skills/test_auggie_claim_gate_jq.py` | New. Extracts and runs the jq block against fixtures |
| `tests/skills/test_auggie_claim_gate_oracle.py` | New. Test-only `admit()` oracle and the frozen contrastive corpus |
| `tests/skills/fixtures/auggie_claim_gate/` | New fixture directory (ledgers, report files, corpus) |

`.claude/` mirrors are regenerated by `make sync-dev` and are never staged (project CLAUDE.md). Unchanged and required to stay green: `src/superclaude/pr_submit/severity_router.py`, `tests/pr_submit/test_severity_router.py`, `tests/pr_submit/test_static_grep.py`, `tests/pr_submit/test_cosmos_protocol.py`, `tests/cli/reflect/test_remediation_source_template.py`, and the skill's existing `evals/evals.json` markers (`# Code Review:`, `## Findings`, `## Audit`).

## 3. Architecture

### 3.1 Data flow

```text
Wave 0  resolve target; record target provenance (mode, base, head, head_match,
        local_sha, worktree_dirty, head_object_check)                        REQ-020..024
Wave 1  collect inputs (unchanged)
Wave 2  reviewer passes -> findings-<stem>.json with `claim` blocks           REQ-001..004
        exit: one or more findings files, OR every chunk skipped             REQ-036
        preflight: jq available, else status failed (invariant_check_unavailable)  REQ-037
Wave 3  step 2   parse; mint ids <stem>#<n> (one sequence per file)           REQ-028
        step 3   location grounding (unchanged; mismatch = drop)             REQ-005
        step 3b  ADMISSION: claim scope, class, table A1-A7, refutation      REQ-006..019
        step 3c  attribution: introduced_in, current_status                  REQ-020..024
        step 4   mechanism dedupe                                            REQ-025..027
        step 5   severity: defects only, rubric steps 1, 2, 4                REQ-029..031
        step 5b  write candidates.json                                       REQ-028
        step 6   write REVIEW.md (defects only, id-tagged) and NOT-ADMITTED.md  REQ-032..034
        step 6b  run the ONE jq program; record jq_exit                      REQ-035
        step 7   audit.log + SUMMARY header
Wave 4  post / inline / offer: read only defect records; nothing on failed   REQ-038..040
```

### 3.2 Component responsibilities

| Component | Owns | Does not own |
|---|---|---|
| `auggie-reviewer` agent | Candidates with `claim` evidence and hints | Dispositions, severity, publication |
| Orchestrator (SKILL Wave 3) | Re-Reads, admission, attribution, dedupe, grading, writing ledger and reports, running jq | Model-free proof of semantics (residual R-1) |
| `refs/claim-gate.md` | All admission rules and the jq program, in one place | Severity tier definitions (rubric owns them) |
| `refs/severity-rubric.md` | Tier definitions; scoping of steps for auggie-review | Admission |
| jq program | Structure, enums, invariants, ledger/report consistency | Whether a guard blocks or a sentence states intent |
| `evidence-validator` (optional) | Citation re-check only | Defect validity, reproduction, re-grading |

## 4. Reviewer contract (auggie-prompts.md, auggie-reviewer.md)

REQ-001. The reviewer output contract SHALL add a `claim` object to every entry of `findings[]` and `cross_cutting_observations[]` with exactly these keys: `observed`, `observed_at[]`, `expected`, `violated_requirement`, `intent_sources[]`, `intent_finding` (`none_found | supports_claim | contradicts_claim | deliberate_policy | documented_prerequisite`), `reachability{entrypoint, producer, guards_checked[], caller_search}`, `harm`, `consequences[]`, `counterevidence[]`, `evidence_kind` (`runtime_reproduced | static_traced | protocol_literal | speculative`), `qualification` (`null` or `{scope, scope_citation}`), `disposition_hint` (one of the five dispositions). Existing fields keep their meaning (MR §6.2).

REQ-002. `consequences[]` SHALL list each distinct consequence the reviewer claims as a separate string, so that the orchestrator can admit or exclude each one (section 5.3). `harm` is the single consequence the reviewer considers best supported.

REQ-003. The quality bar SHALL instruct the reviewer to: trace a production entrypoint or prescribing instruction for every behavioral claim; search for intent and documented prerequisites and record what was found, including "none found" with the pattern; express doubt as `disposition_hint: unproven` or `harm: null`, never as a lower `severity_hint`; never claim live frequency.

REQ-004. `auggie-reviewer.md` SHALL replace "Flag every one" with "record every one as a candidate with a `claim`; a mismatch is not a defect until violated requirement and harm are shown", SHALL require the `claim` block in its Output Format, and SHALL change responsibility 5 so that out-of-diff concerns under head mismatch are still emitted as candidates with `in_diff: false` (admission decides) instead of being moved to cross-cutting notes.

## 5. Admission (claim-gate.md)

### 5.1 Location grounding stays a drop

REQ-005. Location grounding (baseline Wave 3 step 3) is unchanged: a cited line that does not exist or whose snippet does not match is dropped into `dropped_ungrounded[]` with its reason, never converted to another disposition. Exception: under PR head mismatch, a cited line that cannot be checked at all (out of diff, head object unavailable or `head_object_check: mismatch`) is not a mismatch; it becomes `unproven` with reason `head_mismatch_context_unavailable` (resolves INV-039). When `head_object_check: match`, an out-of-diff cited line is validated with `git show <headRefOid>:<path>`.

### 5.2 Claim classes

REQ-006. The orchestrator SHALL derive a class from `category`: `behavioral` = security, data-integrity, correctness, concurrency, resource-leak, error-handling, api-contract, performance, logging; `structural` = architecture, layering, coupling, anti-pattern, dead-code, tests, docs, naming, style. Behavioral claims need a verified `reachability.entrypoint` (plus `producer` for input-shape claims) and verified guards. Structural claims need a verified violating site plus a verified convention source or a mechanical fact (line count, zero-hit Grep with pattern and roots). A structural claim that asserts a runtime consequence must meet the behavioral requirements for that consequence or the consequence is excluded (REQ-010).

REQ-007. Protocol and instruction claims (evidence kind `protocol_literal`): the "entrypoint" is the `path:line` of the instruction that prescribes the step inside an invoked protocol path, and the "producer" is the `path:line` of the consumer's precondition or contract the step must satisfy. This makes literal contract defects admissible without a model run (section 5.4).

### 5.3 Claim scope: narrow subclaims and bundled consequences

REQ-008. Admission SHALL evaluate each entry of `consequences[]` separately against the class requirements and table 5.5. The admitted record keeps only supported consequences in `harm` and records every other one in `excluded_consequences[]` as `{consequence, reason}`, where `reason` starts with an admission-row id (A1-A6) or `other:`.

REQ-009. A candidate is `defect` when at least one consequence is supported and every other table condition holds. Severity SHALL be graded only on the admitted `harm`, and `severity_basis` SHALL name the rubric tier definition that the admitted harm meets. An excluded consequence never contributes to severity, the summary, inline comment text or remediation scope.

REQ-010. When no consequence is supported, the candidate's disposition comes from the first matching table row (normally A6 `unproven`). Its consequences are all listed in `excluded_consequences[]`.

REQ-011. `REVIEW.md` SHALL render, for any defect with non-empty `excluded_consequences[]`, one line "Not established: <consequence> (<reason row>)" per excluded consequence, so a reader sees the narrowed scope. `NOT-ADMITTED.md` SHALL list the same lines under the defect's id.

### 5.4 Narrow contract defects

REQ-012. A `protocol_literal` claim that a prescribed instruction cannot be completed as written (a required input is not supplied, two instructions cannot both be satisfied, a prescribed command's precondition is unmet by the prescribed arguments) SHALL be admissible as `defect` with harm "the prescribed step cannot be completed as written", provided the prescribing instruction (REQ-007 entrypoint) and the violated precondition (producer) are both Read-verified. A downstream stop that catches the failure does not refute the narrow defect; it bounds its harm. Claims of additional consequences (wrong success, data loss, silent pass) are evaluated separately under REQ-008 and are excluded unless traced. This replaces MR §11.2 family F15's negative member (section 7.2).

### 5.5 Admission table

REQ-013. `claim-gate.md` SHALL contain this table; the orchestrator evaluates it top to bottom per candidate and records the matching row ids in `disposition_reasons[]`. "Verified" means the orchestrator Read the cited line in this run.

| Row | Condition | Disposition |
|---|---|---|
| A1 | A verified guard on every verified entrypoint blocks the trigger, or the only path to `observed_at` is a seam whose documented caller precondition the claim violates | `rejected` |
| A2 | The triggering input is shown refused or not produced by the verified producer or schema | `rejected` |
| A3 | `intent_finding = deliberate_policy` verified, the claimed harm is the trade-off the policy states, and no higher-precedence requirement is shown violated through a supported input | `intentional_limitation` |
| A4 | `intent_finding = documented_prerequisite` verified, and no evidence shows the prerequisite unmet in an actual supported rollout | `documented_prerequisite` |
| A5 | The mechanism is fixed at the attribution reference and the target is current state (`target.mode` is `diff` or `snapshot`) | `rejected` with reason `not_present_in_target` |
| A6 | Any of: `evidence_kind = speculative`; class-required evidence missing or not verified (REQ-006, REQ-007); every consequence excluded; `harm` equal to the cited `evidence` text; `violated_requirement` empty; `qualification` present without a verified `scope_citation`; `confidence: low` without `hedge_resolved`; category `security` or `data-integrity` without a `severity_basis` naming the rubric definition the harm meets | `unproven` |
| A7 | Everything else holds and the refutation record is complete with no blocking entry | `defect` |

REQ-014. Policy can be challenged: A3 does not apply when the candidate cites a higher-precedence requirement (spec over doc comment; safety or availability requirement over convenience behavior) that the policy violates and cites harm through a supported input. Then the row is A7 and the record keeps `policy_challenge: <path:line>`.

REQ-015. Availability and visibility harm counts: a supported input that silently stalls, hides or discards valid work is harm without data corruption. A fail-closed refusal of unsupported or ambiguous input is not harm by itself. Unknown, missing or ambiguous evidence (absent identity, unorderable events, revoked state) SHALL NOT be treated as positive evidence for a less-safe path.

REQ-016. Synthetic input is admissible only through `producer`: the input must be accepted by the verified producer, schema or an official contract. No record claims live frequency unless `evidence_kind: runtime_reproduced` with a measured rate.

REQ-017. Low confidence: `confidence: low` is `unproven` unless the orchestrator records `hedge_resolved: <path:line>` citing the line that resolves the doubt stated in the reviewer's `why`. Reviewer `confidence`, `severity_hint` and `disposition_hint` are inputs only.

REQ-018. Qualification: `qualification` is `{scope, scope_citation}` where `scope_citation` is the `path:line` of a documented supported configuration. A qualified defect whose category is not `security` or `data-integrity` and whose harm does not meet a rubric Critical criterion is capped at Medium. An unestablished condition is `unproven` (A6). Demonstrated harm with unknown frequency is not a qualification and is not capped (resolves INV-040).

### 5.6 Refutation record

REQ-019. Every `defect` SHALL carry `refutation[]` with one entry per applicable row A1-A5, each `checked: <path:line>` (guard entries add `blocks` or `does_not_block`) or `not_applicable: <reason>`. Mocked-only dispatch does not count as an entrypoint. Caller search runs only when no entrypoint is cited or the cited one fails the Read; it Greps under `src/`, `plugins/` and `tests/` and records pattern and roots. Every `rejected`, `intentional_limitation` and `documented_prerequisite` record SHALL carry `refutation_citation: <path:line>` (the guard, producer, policy or prerequisite line) and a reason row id (resolves INV-042). `admission_budget{candidates_total, checked, incomplete, wall_seconds}` is recorded; candidates not finished are `unproven (admission_incomplete)` and set `coverage.complete = false`.

## 6. Attribution, dedupe, ledger, publication

### 6.1 Attribution

REQ-020. Wave 0 SHALL record `target{mode, base, head, head_match, local_sha, worktree_dirty, head_object_check, evidence_source}`. Snapshot: `base: null`.

REQ-021. `evidence_source` is `local_read`, `head_object` or `diff_new_side`. `local_read` is not used when `target.mode == pr` and `head_match == false`. Under PR head mismatch, context hops (entrypoint, guards, producer, intent) use the head object only when `head_object_check == match`; `match` requires `headRefOid` equal before and after `gh pr diff`, `git cat-file -e <oid>` success, and agreement of every cited in-diff line with the diff's new side. Otherwise `diff_new_side`, and any row needing the head object is `unproven (head_mismatch_context_unavailable)`.

REQ-022. In explicit `--diff` mode the target is committed history: reads for admission and `current_status` use `git show HEAD:<path>`, not the working tree, even when `worktree_dirty` is true. Only implicit dirty-tree diff mode and snapshot mode use `local_read` of uncommitted edits (resolves INV-044).

REQ-023. Each record SHALL carry `introduced_in` (`head`, `base`, `unknown`, `not_applicable_snapshot`) from comparing `git show <base>:<path>` at the mechanism, and `current_status` (`present`, `absent`, `unchecked`) only when a distinct current ref is known. Hunks absent from `HEAD` get `introduced_in: unknown`. Snapshot mode uses `not_applicable_snapshot` everywhere and never says "introduced", "regression" or "this PR".

REQ-024. Scope comes from `target.mode`: `pr` is as-submitted, `diff` and `snapshot` are current state. A `pr` defect fixed later keeps `defect` with `current_status: absent` and `remediation_eligible: false`. A pre-existing defect (`introduced_in: base`) stays admissible and is labeled pre-existing; rubric step 4 applies.

### 6.2 Mechanism dedupe

REQ-025. The orchestrator SHALL set `mechanism_key = <root-cause path>::<enclosing symbol or heading>::<normalized expected behavior>` and group by it across chunks, personas and lines. Two candidates on one line with different keys stay separate.

REQ-026. Merge rule: keep all member ids and citations; never count votes. Rank members by evidence kind `runtime_reproduced` > `static_traced` = `protocol_literal` > `speculative`. Every blocking citation recorded on any member (`refutation_citation`, or a `refutation[]` entry marked `blocks`) must be answered in the decider's `refutation[]` as `does_not_block` with a citation. The group is `defect` only if the decider strictly outranks every non-defect member; otherwise `unproven (mechanism_conflict)`. Non-defect groups take the highest-rank member's disposition; equal rank gives `unproven (mechanism_conflict)`. Losers carry `merged_into: <id>`. Severity is computed after the merge, never as a maximum of hints. Excluded consequences of all members are unioned into the group.

REQ-027. The baseline rule "restatements of PR caveats are dropped" becomes A3/A4 evaluation; the record stays in the ledger.

### 6.3 Ledger

REQ-028. `<output-dir>/candidates.json` SHALL follow `schema: auggie-review-candidates/1` with: `target`, `coverage{chunks_planned, chunks_completed, chunks_skipped[], persona_passes[], input_truncated, complete}`, `admission_budget`, `jq_exit`, `candidates[]` (each with `id`, `members[]`, `mechanism_key`, `merged_into`, `disposition`, `disposition_reasons[]`, `severity`, `severity_basis`, `category`, `class`, `confidence`, `hedge_resolved`, `file`, `line`, `in_diff`, `claim`, `excluded_consequences[]`, `refutation[]`, `refutation_citation`, `attribution{introduced_in, current_status}`, `remediation_eligible`), `remediation_ids[]`, `remediation_count{critical, high}`, `dropped_ungrounded[]`. Ids are `<findings-file-stem>#<n>` with one `n` sequence across `findings[]` and `cross_cutting_observations[]` of the same file, and are unique.

### 6.4 Grading

REQ-029. Only unmerged `defect` records reach the severity remap. Non-defects have `severity: null`.

REQ-030. `severity-rubric.md` SHALL gain a section "Admission precedes grading" stating: auggie-review grades only admitted defects; a category floor applies only when the admitted harm meets that floor's tier definition, otherwise `harm_below_floor` is recorded; step 3 (low-confidence drop) is not applied to auggie-review defects because low confidence is resolved at admission (REQ-017); step 4 (diff locality) still applies; the qualification cap (REQ-018). Steps 1-4 text stays unchanged for the `pr_submit/severity_router.py` consumer (resolves INV-038; router and its tests are untouched).

REQ-031. The decision-mode summary SHALL gain a first row "Inconclusive — review incomplete" when `coverage.complete == false`, regardless of counts, and a row "No defects admitted" for a non-empty ledger with zero defects.

### 6.5 Publication

REQ-032. `REVIEW.md` `## Findings` and `## Architectural / Cross-Cutting Observations` SHALL contain only unmerged defects. Heading entries use `#### C1. <Short title> (id: <id>)`. Every Nit and every Cross-Cutting defect is one top-level list item starting with `<!-- id: <id> -->`. An entry runs to the next heading of the same or higher level, or for list items to the next list item at the same or shallower indentation or the next heading. `## Summary` names findings only by id. Each defect entry carries `**Evidence kind**: <evidence_kind>` and, when present, its "Not established" lines (REQ-011) and qualification. Section headers `# Code Review:`, `## Findings`, `## Audit` stay.

REQ-033. `REVIEW.md` SHALL NOT contain a `## Not Admitted` section. It carries one counts line: "Not admitted: U unproven, R rejected, L intentional limitations, P documented prerequisites, M merged (see NOT-ADMITTED.md)".

REQ-034. `<output-dir>/NOT-ADMITTED.md` is mandatory and generated from the ledger: every non-defect record with id, title, disposition, reason row and citation; merged members under "Merged into <id>"; excluded consequences of defects. It is never posted and never passed to `/sc:design`.

REQ-035. The jq program in `claim-gate.md` runs once per review after `REVIEW.md` and `NOT-ADMITTED.md` are written and before any Wave 4 action, as `jq -e -n --slurpfile ledger candidates.json --rawfile review REVIEW.md -f <extracted block>`, with the scan regex written in single quotes and fenced code blocks removed from the scanned text before matching. Its exit code is recorded as `jq_exit` in `candidates.json` and `audit.log`. It SHALL check invariants J1-J22 (section 8).

### 6.6 Status and coverage

REQ-036. `coverage.complete = false` when a chunk or persona pass is skipped, input is truncated, or any candidate is `admission_incomplete`. Wave 2's exit criterion SHALL include "or every chunk skipped" so an all-skipped run reaches Wave 3 and produces an Inconclusive `partial` report. The Wave 3 precondition is "Wave 2 complete".

REQ-037. Status: `failed` only for a ledger or invariant failure (missing `candidates.json`, missing or non-zero `jq_exit` after Wave 2 starts, jq absent at the preflight with reason `invariant_check_unavailable`). `partial` keeps the baseline causes. `coverage.complete == false` never yields `success`. The empty-diff short-circuit stays `success`. `REVIEW.md` and `audit.log` are written on every status. jq availability is preflighted explicitly before Wave 3; `allowed-tools` is not a prerequisite check.

### 6.7 Wave 4 consumers

REQ-038. Posting and inline comments read only unmerged defects. Nothing is posted and no offer is made when status is `failed`. The posted bytes are the checked `REVIEW.md`.

REQ-039. The SKILL Output Contract SHALL add `candidates_path`, `not_admitted_path`, `disposition_count{defect, unproven, rejected, intentional_limitation, documented_prerequisite, merged}`, `remediation_count`, and `coverage_complete`; `findings_count` keeps its shape and counts unmerged defects. The SUMMARY header carries the four non-defect counts and `coverage_complete`.

REQ-040. `remediation-handoff.md` SHALL fire the offer on `remediation_count.critical + remediation_count.high >= 1`; `remediation_ids` equals the set of unmerged, `remediation_eligible`, Critical/High defects (resolves INV-037); Phase A gets the sentence "address only findings whose id is in `remediation_ids`; ignore every other part of the report"; the MDTM WHERE list is built from `remediation_ids`.

### 6.8 pr-submit fallback boundary

REQ-041. No `pr_submit` code or pr-submit refs change. The attended fallback normalizes posted output only; after this change posted output contains only admitted defects, so non-defects cannot re-enter through that seam. The proposed `fsm.py` `_run_fallback` guard (MR Change 12, FR-20) is excluded (section 9, D-12).

## 7. Tests

### 7.1 Deterministic layer (pytest, no model calls)

REQ-042. Tests SHALL be ordinary pytest modules in `tests/skills/` with fixtures in `tests/skills/fixtures/auggie_claim_gate/`, reading canonical `src/` files. The jq test extracts the single fenced `jq` block from `refs/claim-gate.md` and runs the real jq binary; when jq is absent the test fails with a clear message rather than skipping.

### 7.2 Frozen contrastive corpus and test-only oracle

REQ-043. A test-only `admit(record) -> (disposition, reasons, excluded_consequences)` oracle lives under `tests/` and takes orchestrator-verified facts as explicit fixture booleans (it reads no files, git or network). A test SHALL assert the oracle's row ids, order, fallback dispositions and class rules equal the table extracted from `claim-gate.md`. The corpus SHALL contain single-factor contrastive pairs for families F1-F16 (MR §11.2), with F15 restated as: positive = prescribed command cannot run as written and the trace reaches a wrong success (defect, both consequences admitted); negative = same omission, a downstream stop catches it (defect admitted for the narrow "cannot be completed as written" harm only, "wrong success" excluded with A6). At least four pairs are marked held back and are used only for the acceptance run. The corpus SHALL contain the genuine-positive retention set (MR §11.3 base list of six, the eight classic defects and the four publish cases). Corpus text SHALL contain no diagnostic case ids, PR numbers 266/267/269/270 or symbols from the 18 diagnostic claims (frozen token list).

The oracle proves the rule table is consistent and that single facts flip outcomes as designed. It does not prove a model follows the protocol.

## 8. jq invariants

The jq program SHALL fail (exit non-zero) when any of these is violated:

| Id | Invariant |
|---|---|
| J1 | Every `disposition` is one of the five values; `class` is `behavioral` or `structural` |
| J2 | `severity != null` iff `disposition == "defect"` |
| J3 | Every defect: `evidence_kind != speculative`, non-null `harm`, non-empty `violated_requirement`, non-empty `refutation[]` with entries of the form `checked: <path:line>` or `not_applicable: <reason>`; behavioral defects have a non-null `reachability.entrypoint`; structural defects have `intent_sources` or a mechanical-fact refutation entry |
| J4 | Every `rejected`, `intentional_limitation`, `documented_prerequisite` has a reason row id and a `refutation_citation` matching `path:line` |
| J5 | Every `disposition_reasons` and `excluded_consequences[].reason` entry starts with `A1`-`A7` or `other:` |
| J6 | Ids unique; every grounded member appears exactly once |
| J7 | No `merged_into` is dangling or cyclic |
| J8 | Every refutation-union blocking citation in a merged group is answered `does_not_block` with a citation in the decider |
| J9 | `findings_count` totals equal counts of unmerged defects by severity |
| J10 | `remediation_ids` equals the set of unmerged, eligible Critical/High defect ids; `remediation_count` is computed from it |
| J11 | `remediation_eligible == false` when `current_status == absent`; `current_status == absent` on a defect requires `target.mode == pr` |
| J12 | Snapshot mode: every `introduced_in == not_applicable_snapshot` |
| J13 | No `evidence_source == local_read` when `target.mode == pr` and `head_match == false`; any defect hop on `head_object` requires `head_object_check == match` |
| J14 | `qualification != null` implies `scope_citation` matches `path:line`; a qualified non-security/non-data-integrity defect has severity in `{medium, low, nit}` unless its `severity_basis` names a rubric Critical criterion |
| J15 | `confidence == low` on a defect implies non-null `hedge_resolved` |
| J16 | `coverage.complete == false` implies status is not `success`; `coverage.complete == true` implies no skipped chunk, no truncated input and no `admission_incomplete` record |
| J17 | Every id tag scanned in `REVIEW.md` (fenced blocks removed; heading-line tags and `<!-- id: ... -->` list-item tags only) is an unmerged defect id |
| J18 | Every unmerged Critical/High defect id appears under `## Findings` |
| J19 | The number of entries under `## Findings` and the Cross-Cutting section equals the number of scanned id tags (no untagged entry; resolves INV-036) |
| J20 | No `path:line` pattern appears outside defect entries, except in the header block above the first section |
| J21 | Each defect entry's `**Evidence kind**` value equals the record's `evidence_kind` |
| J22 | `REVIEW.md` contains no `## Not Admitted` heading |

## 9. Resolution of merged-requirements section 17

| Item | Decision |
|---|---|
| INV-034 (HIGH) id scan captures code text | Resolved: heading-line and HTML-comment list-item tags only, fenced blocks removed, single-quoted regex (REQ-032, REQ-035); fixtures in AT-09 include a `def f(id: str)` fenced excerpt and a quoted template text |
| INV-016 all chunks skipped never reaches Wave 3 | Adopted (REQ-036) |
| INV-043 id sequence | Adopted (REQ-028) |
| INV-035 entry boundary | Adopted as defined in REQ-032 |
| INV-036 untagged entry passes | Resolved by J19 |
| INV-037 subset-only remediation check | Resolved by J10 equality |
| INV-038 rubric step 3 lowers hedge-resolved defects | Resolved: step 3 is not applied to auggie-review defects (REQ-030); router text and behavior unchanged |
| INV-039 out-of-diff line dropped under head mismatch | Resolved: head-object read when `match`, otherwise `unproven`, not drop (REQ-005) |
| INV-040 wrong premise text and compliance cap | Resolved: `severity_basis` must name the rubric definition; Critical criteria (including regulatory/compliance) are exempt from the qualification cap (REQ-013 A6, REQ-018, J14) |
| INV-041, INV-045 pr-submit fallback paths | Out of scope with MR Change 12 (D-12). Recorded as pr-submit follow-up; not repaired here |
| INV-042 refutation union gaps | Resolved: `refutation_citation` required on all three citation-bearing non-defects (REQ-019, J4) |
| INV-044 dirty worktree in explicit diff mode | Resolved: explicit diff reads committed `HEAD` (REQ-022) |
| INV-028 / A-003 orchestrator rubber-stamp | Accepted residual R-1 (section 12). Measured by `false_promotion` in the live evaluation; no further mechanism added |
| INV-009 floor-premise placement | Confirmed inside A6 via `severity_basis` (REQ-013) |
| Critical/High presence location | Decided: under `## Findings` (J18), the stricter V3 position |
| Wave 6b echo; guard placement | Not applicable: no pr-submit edits |
| M-1/M-2 gate scope | Confirmed: held-back pairs plus at least one held-back item from each retention list (section 11.3) |
| AC-32 part (2) evidence-kind label | Decided: the template carries `**Evidence kind**`; checked deterministically by J21, so no live run is needed for this check |
| D-12 MR Change 12 (`fsm.py` guard) | Excluded. It changes pr-submit product code, which the request excludes ("keep the mechanism minimal", "do not repair validated product defects"). auggie-review's own status and published content are corrected; pr-submit's handling of a `failed` fallback review is a separate follow-up |
| Held-out real-PR check (MR §11.6) | Excluded from this plan. Re-running the reviewed PR heads would make the diagnostic cases a tuning target, and the request forbids altering the experiment. Acceptance evidence is the synthetic held-back corpus plus the separately authorized live evaluation (11.3) |
| Literal-contract usability defects | Resolved by REQ-012 and the restated F15 |
| Bundled consequences | Resolved by REQ-008 to REQ-011 |

## 10. Acceptance tests

Deterministic tests run with `uv run pytest tests/skills/test_auggie_claim_gate_contract.py tests/skills/test_auggie_claim_gate_jq.py tests/skills/test_auggie_claim_gate_oracle.py -v`.

| AT | Check | Covers |
|---|---|---|
| AT-01 | `auggie-prompts.md` output contract contains every `claim` key, the four evidence kinds, the five dispositions, `consequences`, and no `scope_condition` | REQ-001, REQ-002 |
| AT-02 | Quality bar contains the four REQ-003 instructions | REQ-003 |
| AT-03 | `auggie-reviewer.md` lacks "Flag every one", requires `claim`, and keeps out-of-diff candidates with `in_diff: false` | REQ-004 |
| AT-04 | `claim-gate.md` exists, has rows A1-A7 in order with the dispositions of REQ-013, the class table, claim-scope rules, the narrow contract rule, and exactly one fenced `jq` block | REQ-006, REQ-007, REQ-008, REQ-012, REQ-013 |
| AT-05 | SKILL Wave 3 step order by extraction: parse, grounding, admission, attribution, dedupe, defect-only remap, ledger, reports, jq, audit | REQ-005, REQ-029, REQ-035 |
| AT-06 | SKILL Output Contract and SUMMARY header contain the REQ-039 fields; `findings_count` unchanged shape | REQ-039 |
| AT-07 | SKILL Wave 0 records the REQ-020 target fields and the REQ-021/REQ-022 evidence-source rules; snapshot wording rule present | REQ-020 to REQ-024 |
| AT-08 | jq passes every `valid-*` fixture ledger/report pair | REQ-028, REQ-035 |
| AT-09 | jq fails one `invalid-*` fixture per invariant J1-J22, including the INV-034 fixtures (fenced `def f(id: str)`, quoted `(id: x)` template text must not be scanned and must pass; untagged entry must fail) | REQ-032 to REQ-035, section 8 |
| AT-10 | `severity-rubric.md` has "Admission precedes grading" with the REQ-030 rules and the two REQ-031 rows | REQ-030, REQ-031 |
| AT-11 | `remediation-handoff.md` offer gate, Phase A sentence and WHERE rule of REQ-040; `test_remediation_source_template.py` passes | REQ-040 |
| AT-12 | SKILL report template has id-tag forms, Evidence kind line, "Not established" line, counts line, keeps `# Code Review:`, `## Findings`, `## Audit`, has no `## Not Admitted` | REQ-011, REQ-032, REQ-033 |
| AT-13 | SKILL defines `NOT-ADMITTED.md` contents and forbids posting it or passing it to `/sc:design` | REQ-034 |
| AT-14 | SKILL Wave 2 exit includes "or every chunk skipped"; jq preflight and status rules of REQ-036/REQ-037 present | REQ-036, REQ-037 |
| AT-15 | SKILL Wave 4 reads only defects and posts nothing on `failed` | REQ-038 |
| AT-16 | Oracle row table equals the table extracted from `claim-gate.md` | REQ-013, REQ-043 |
| AT-17 | Every contrastive pair: positive member `defect`, negative member its expected non-defect disposition (or narrowed defect for F15) | REQ-008 to REQ-018, REQ-043 |
| AT-18 | Every retention item is `defect`; availability and visibility items included | REQ-015, REQ-043 |
| AT-19 | Bundled-consequence fixtures: narrow subclaim admitted, unsupported consequence in `excluded_consequences` with a row reason, severity graded on admitted harm only | REQ-008 to REQ-011 |
| AT-20 | Anti-overfit scan: new and edited `src/` files and corpus contain no frozen diagnostic tokens, case ids or PR numbers | REQ-043 |
| AT-21 | SKILL line 22 hallucination sentence byte-identical; `uv run pytest tests/pr_submit/test_severity_router.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_cosmos_protocol.py tests/cli/reflect/test_remediation_source_template.py` passes | REQ-044 |
| AT-22 | `git diff --stat 713d8e423bd9a2469ea1418fafd6edccbb88caaa` touches only section 2 paths; `src/superclaude/pr_submit/` unchanged; `make verify-sync` passes; no `.claude/` path other than `settings.json` staged | REQ-041, REQ-045, REQ-046 |
| AT-23 | `commands/auggie-review.md` Will Not states non-defect candidates are never promoted to findings and doubt is never expressed as lower severity | REQ-003, REQ-029 |
| AT-24 | `claim-gate.md` states the refutation record (REQ-019), the merge rule with ranking, refutation union, strict dominance, `mechanism_conflict`, `merged_into` and no maximum severity (REQ-025, REQ-026), the caveat rule (REQ-027), the policy-challenge, availability/visibility, synthetic-input, low-confidence and qualification rules (REQ-014 to REQ-018); jq fixtures J7/J8 cover merge structure | REQ-014 to REQ-019, REQ-025 to REQ-027 |
| AT-25 | Test modules live in `tests/skills/`, read canonical `src/` files, run real jq and fail with a clear message when jq is absent | REQ-042 |

## 11. Non-functional requirements and evaluation

REQ-044. Compatibility: SKILL line 22, `severity_router.py` behavior, its tests, the posted inline-comment `**Severity:**` line format and the existing evals markers are unchanged.

REQ-045. Scope: no edits to installed global copies, settings, `evidence-validator.md`, `finding-verify.md`, any `pr_submit` file, the review-comparison experiment or validation packets, or `.dev/reviews/**`. No new agent, Python production module, CLI flag or tool permission. No repair of the eight qualified product defects. No gateway work.

REQ-046. Protocol cross-references added by this change cite section names, not line numbers.

### 11.3 Live evaluation (not part of this plan)

The semantic measures M-1 (held-back positives not admitted) and M-2 (held-back negatives admitted), the false-negative split (`under_specified`, `over_rejected`, `false_promotion`, `admission_incomplete`, below-tier) and the stale-agent and incomplete-review controls require running the changed protocol with a model on synthetic mini-repos. No ready reviewer replay runner exists; the workflow companion's private staging pattern can be adapted, with the source reviewer agent staged explicitly and activation verified. This needs separate user authorization and is a pre-merge gate, not a task in this plan. Counts are reported with sample sizes and model provenance, never as accuracy rates; the 32-session experiment is never a denominator.

## 12. Risks and residuals

| Id | Risk | Response |
|---|---|---|
| R-1 | Orchestrator rubber-stamps its own refutation (plausible citations) | Accepted residual; structural checks only; measured by `false_promotion` in 11.3, which is the trigger for a second reader |
| R-2 | Over-rejection hides real defects | Availability/visibility rule, narrow-contract rule, claim splitting, retention corpus; non-defects visible in `NOT-ADMITTED.md` |
| R-3 | Cost and latency grow | Existing tools only; caller search only when needed; `admission_budget` recorded; overflow becomes `unproven` and Inconclusive, never silent admission |
| R-4 | Run-wide `failed` from a scan false match | Tag grammar, fenced-block stripping and AT-09 fixtures |
| R-5 | Wrong baseline in the implementation session | Revalidate feature commit; edits by section name; AT-22 |
| R-6 | pr-submit treats a `failed` fallback review as clean | Pre-existing seam behavior, recorded follow-up (D-12); out of scope |
| R-7 | jq missing on a host or CI | Explicit preflight gives `failed (invariant_check_unavailable)`; tests fail rather than skip; CI provisioning not claimed |

## 13. Rollback

Full revert of the implementation commit(s), then `make sync-dev` and `make verify-sync`, is the only rollback. No skip flag and no partial rollback: removing admission while keeping the ledger would restore grounded-equals-defect behavior. Old review outputs stay on disk. Rollback touches no product safety code.

## 14. Implementation-session preconditions

- The implementation runs in the main checkout, because `/sc:implement` accepts only a plan package under the current checkout's `.dev/tasks/`. Before the new session, the user puts that checkout on a new feature branch created from `713d8e423bd9a2469ea1418fafd6edccbb88caaa` (never master). The untracked `.dev/` package survives the switch; the existing tracked modification to `.dev/releases/current/cliEval/evidence/T02.15/perf.json` may need to be stashed or committed by the user first. Re-verify the section 2 files against that commit before editing.
- Do not install, update globals, post to GitHub or rerun the review-comparison experiment.
- Run the AT commands in section 10 and record outputs under the plan package `artifacts/`.
