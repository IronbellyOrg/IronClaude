# Round 2: Advocate A (rebuttal)

Model: opus. Persona: architect + qa. Focus: correctness, risk, test-coverage. Code checked read-only at HEAD 50d4d2b9d. No file under the forbidden run-1 paths was read.

## Response to criticisms

B Round 1, "Weaknesses identified in Variant A", answered one by one.

1. **"A-001 is false for A" (E2, CO-1, T4, section 8 point 3).** CONCEDED, as I already did in Round 1, concession 1. `findings.py:104` with `:80-81` drops a line with no anchor at parse time, and `ledger.py:135-136` annotates only lines that parsed. Section 8 point 3 is withdrawn as a reason to converge now.
2. **"A's clustering plan (CO-3) breaks the loop it says it keeps."** CONCEDED. I re-checked it myself (New evidence N1):
   - `cluster.annotate` builds its view from citations only.
   - The fingerprint is None without a resolved primary citation.
   - `same_defect_v2` needs a resolved citation on both sides.
   - `test_review_cluster.py:279-293` pins that two identical anchor-only findings stay as two clusters.

   The section-resolver idea does not rescue it, because the fingerprint does not exist in the first place. A's CO-3 answer is withdrawn.
3. **"`findings-v2` is the superset overstates the kernel."** CONCEDED, with one qualification. The superset claim holds for the eight v1 fields; that is pinned by `test_review_findings_v2.py:70-81`, which I read. It does not hold for vocabularies (`findings_v2.py:109-110` enforces v1 `CATEGORIES`) or for clustering (N1). "Profile as data" is a design still to be built, not something already reachable.
4. **"The new re-review line type is a cost with no effect today."** CONCEDED. `prior` lines are only logged as a `prior_note` (`ledger.py:259-272`). The typed line kind is withdrawn from C-01.
5. **"A adds new on-disk ledger state for no current consumer."** CONCEDED. The clustering marker in the header and the `citations` list in rows put the stored-ledger invariant (INV-D) at risk, and nothing reads them today. Both are withdrawn and deferred to the convergence trigger.
6. **"The fix for A's best point does not need A's design."** PARTLY CONCEDED.
   - A v1-local fix is possible, so A's merged engine is not needed for it.
   - What B does not show is which v1-local fix is safe. N3 shows the stuck row hits exactly the case where the fix worked: nobody re-finds the defect, so nothing re-anchors the row.
   - The only v1-local ways to release such a row are (a) a policy that marks it unlocated and asks the next round to locate it or say it is gone, or (b) letting a fix map entry for a row with no span reach `resolved_check`. Option (b) then clears purely because nobody re-found it, which is the fail-open clearing rule owned by C-02.
   - So the fix fits inside v1, but its safety depends on C-02. C-01 should fix only the locator policy, as data (`on_missing`, `on_ambiguous`), and hand the clearing semantics to C-02.

B's other claims I checked:
- **B concession 1** (the existing refusal raises `LedgerError`, and `merge` turns it into exit 1): VERIFIED. `merge_cmd.py:111-112` re-raises `LedgerError` as `click.ClickException`, which exits 1.
- **B strength 3** ("profile is data" is new work): ACCEPTED.
- **B C-002 ruling** ("defer and pin today's parser rejection"): ACCEPTED. That is now my position too (see the hybrid).

## Updated assessment of Variant B
- B's core shape is right for C-01 now. The pipelines are separate, the v1 parser already enforces the anchor boundary, and the v2 kernel cannot host the anchor loop without new clustering code.
- B's two self-corrections are correct: withdraw the 2.3 guard, and rewrite 5.2 to pin today's rejection.
- Two B items still fail B's own rule of building only when a consumer needs it:
  - the projection view (2.1), which has no consumer;
  - "closed at the PR adapter" for unknown keys, which has no evidence behind it.
- B's trigger item 2 ("two defects in one quarter") has no measured basis and should be replaced by a mechanical test (see the hybrid).
- B's remaining gap: it gives no answer for the verified stuck row (E11). B conceded this in Round 1 (concession 2) but did not propose a locator policy.

## New evidence
All read by me at HEAD, outside the forbidden paths.

- **N1. `cluster_v2` cannot join anchor-only findings.**
  - `cluster.py:128-134` builds `citations` from `finding.get("citations")` only.
  - `:134` gives `primary` None when there are no citations.
  - `:143-147` gives `fp` None unless the primary citation is resolved.
  - `same_defect_v2` (`:163-181`) has no anchor or span branch.
  - The test `test_finding_without_citations_has_no_primary_and_stays_alone` (`test_review_cluster.py:279-293`) asserts two clusters for two identical anchor-only findings, and `primary_citation is None`.
  - The test helper `fnd` always adds a default citation (`test_review_cluster.py:35`, `list(cits) or [cit()]`), so 279-293 is the only test of the anchor-only case. It would be one of the pins A's original CO-3 plan had to break, and A's T1 pin list missed it.
- **N2. Clearing ignores block validity, and this is not new: a test pins it as intended.**
  - Outside rendering and telemetry, `block_ok` is read only at `ledger.py:129,147,150,295`. The rest are the merged-report render (`:423`) and telemetry (`telemetry.py:67`).
  - The clearing loop at `ledger.py:254-258` never reads it.
  - `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`test_review_ledger.py:376-385`) asserts that L1 becomes `resolved` while reviewer `t2-1` has a broken block.
  - This is the "single-valid-block pass" defect that A section 5 item 6 already assigns to C-02 and C-03. I correct my Round 1 framing: it is not a new finding.
  - What is specific to C-01: `merge_round` keeps an invalid reviewer's lines that do parse (`ledger.py:135-138` runs whatever `parsed["ok"]` is), so only the dropped line is lost. A re-find that is dropped for format reasons (citation-only, anchor over 200 characters, claim over 300) therefore cannot hold its row open, and the row can clear in that round.
  - The docstring "skipped for clearing" (`ledger.py:112`) is not implemented for each reviewer.
- **N3. The stuck row hits exactly the "fix worked" case.**
  - A row with `span None` is kept open and blocking (`test_review_ledger.py:408-417`).
  - `apply_revision` records it as `named_not_touched` (`ledger.py:331-339`; `hunks_touch(None)` is False at `findings.py:446-447`).
  - The only way such a row gets a span is a later re-find with an anchor that can be located, since `merge_round` re-anchors from the current report (`ledger.py:226-231`).
  - If the fix worked, nobody re-finds the defect, so the row stays open and blocking until escalation.
  - No test pins this outcome. The 408-417 test pins only the state after round 1.
- **N4. Nothing outside tests reads `anchor_status` or `anchor_ambiguous`.**
  - A Grep over the repo (excluding `.dev/tasks/`) finds them written only at `findings.py:350-351`.
  - They are read only by `tests/review/test_review_findings.py:219,223,227,230`.
  - The remaining hits are vendored copies and notes under `.dev/research/` and `.dev/brainstorms/`, which are not product code.
  - The ledger row does not store them (`ledger.py:184-202`). Both flags are computed and then thrown away in the product path.
- **N5. The v1 parser has no key whitelist.** `_check_finding` (`findings.py:90-121`) checks only id, severity, blocking, category, anchor, anchor2, refs and claim. v2 rejects only `calibrated_confidence` (`findings_v2.py:96-97`), and its `check_finding` (`:84-187`) has no whitelist either. Unknown keys are open in both parsers today.
- **N6. The limit literals are duplicated in two places.** v1 has them at `findings.py:104` (anchor 12..200), `:108` (anchor2), `:114` (refs at most 8) and `:118` (claim at most 300). v2 restates them at `findings_v2.py:111,117,126,132,136` plus the citation quote at `:80`. That makes B's shared constants module a real, bounded deduplication.

## Concrete hybrid you now stand behind

C-01 decision: **B's thin shared contract now, per-module engines, with A's locator policy as data added to the v1 engine. A's merged engine is recorded as the target if and when the convergence trigger fires.**

### Shared core NOW
1. The finding id grammar `_ID`, already shared.
2. One limits constants module imported by both parsers (N6). Names must be checked against the reserved contract-constant names (`make lint-architecture` Check 11, INV-K).
3. One repair step that runs before either `parse_block`. The policy is decided by C-06; C-01 fixes only where it sits.
4. The `refs_norm` token list, already shared (`cluster.py:64,141`), with the `T01.02` pattern added once.
5. Hash and identity helpers.

### Engines
- The spec loop stays on v1 `findings.py`, `ledger.py`, `review-ledger/1` and v1 clustering.
- reflect stays on the v2 kernel.
- No change to `cli/reflect` (contract 1.8.0, INV-A).

### Withdrawn from both proposals
- A: locator-agnostic `annotate` now, `citations` in ledger rows, the clustering marker, the typed re-review line kind, and `cluster_v2` for new ledgers.
- B: the 2.3 `LedgerError` guard, the projection view (until a consumer exists), and "closed at the PR adapter" (left to C-10).

### Deferred, with a trigger
The convergence to one engine (A's profile parser, a span taken from either locator, rows keyed by citation) happens at the first of these:
- **(T-a)** A module needs re-review rounds over citation-located findings from several reviewers. B 5.4 item 1, kept.
- **(T-b)** The pre-registered measurement shows citations resolve at least as often as anchors locate on the document target. B 5.4 item 3, kept.
- **(T-c, replaces B item 2)** A verified defect fix needs a non-helper edit to both `findings._check_finding` and `findings_v2.check_finding`, or to both clusterers, beyond the shared constants and repair step. This can be checked mechanically on the fix's diff; it needs no quarterly count.

When convergence happens, it must first give `same_defect_v2` an anchor-span branch, or derive a `spec`-role citation from the located anchor span. N1's test then changes as a planned pin.

### Stuck-row defect (E11, FX-2)
- C-01 adds a locator policy as data to the v1 engine: `on_missing` and `on_ambiguous`.
- `spec-loop` default: keep the row (as today, `test_review_ledger.py:408-417`), and surface `anchor_status` and `anchor_ambiguous`. Today they are thrown away (N4). They should appear in the merged report and the reviser brief, so the row is visibly marked unlocated and the next round is asked to locate it or say it is gone.
- How an unlocated row may clear goes to C-02, because the only release that needs no re-find depends on C-02's clearing rule (N3).

### Clearing that ignores block validity (N2)
- This is not a C-01 defect. It goes to C-02 and C-03, together with `test_review_ledger.py:376-385`, which pins it.
- C-01 adds one constraint: the shared repair step must run before the parser decides validity, so that a re-find is not dropped for format reasons alone.

### `cluster_v2` cannot cluster anchors (N1)
- Resolved for now by keeping the spec loop on v1 clustering.
- Recorded as the first step of any convergence (see Deferred).

### Unknown keys
- Open in both parsers, as today (N5). No whitelist.
- `calibrated_confidence` stays accepted by v1 and rejected by v2 (`test_review_findings_v2.py:95-100`).
- Storing pass-through keys in the ledger member record (`ledger.py:172-180`) is deferred until a consumer reads provenance from the ledger.

### Prior lines
- Unchanged: v1 accepts them (`findings.py:175-187`), v2 rejects them (`findings_v2.py:279-283`), and both are pinned (`test_review_findings_v2.py:106-113`).
- What they should do goes to C-02.
- No change to the brief, so the plugin mirror (INV-N) is untouched.

### Tests
| Test | Fate | Content |
|---|---|---|
| T1 (A) | Survives | Every `tests/review/` and loop pin under `tests/skills/` passes unmodified after the constants module and repair step land. Add `test_review_cluster.py:279-293` to the named pins. |
| T2 (A) + 5.1 (B) | Merged | Differential replay: committed v1 ledger fixtures and a golden set of about 20 lines, run with and without the repair step. Parser output on lines that are already valid must be byte-equal, and the ledger file must be equal. 5.1's projection-totality check is dropped along with the projection view. |
| T3 (A) + 5.3 (B) | Merged | B's pre-registered rule, plus A's per-finding record (anchor found exactly once, path in the snapshot the core built, range inside the file, quote inside the range). Run only after the E1 snapshot plumbing is fixed and after A-002 (how line numbers reach reviewers) is stated. |
| T4 (A) + 5.2 (B) | Rewritten as one | Pin today's rejection of a citation-only line in a `findings-v1` block. One reviewer: `LedgerError` "no reviewer produced a valid findings block" and the ledger unchanged. Several reviewers: a warning, `block_ok` false, the line lost, the other reviewers merged. |
| T5 (A) | Rewritten | A missing anchor gives a row with `span None` whose `anchor_status` is surfaced in the merged report and reviser brief. A fix map entry naming it records `named_not_touched`. The clearing assertion is left to C-02. |
| 5.4 (B) | Survives as the trigger | Items 1 and 3, with item 2 replaced by T-c. |

## Updated per-point table
| Point | Superior | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 65% | A's answer to each routed row is easier to check than answers spread across sections. |
| S-002 | B | 75% | B's trigger, sharpened with T-c, is a falsifiable rule for when to converge; A's open points are not. |
| S-003 | NEITHER | 55% | Grouping the evidence differently changes no conclusion. |
| S-004 | A | 55% | A rates each invariant's level; the coverage is otherwise similar. |
| S-005 | HYBRID | 75% | T1, the merged T2/5.1, the merged T3/5.3, the rewritten T4/5.2 and the rewritten T5 (see the table above). |
| C-001 | B | 70% | CHANGED. Thin contract and per-module engines now; the pipelines are separate and the v2 kernel cannot host the anchor loop (N1). |
| C-002 | B | 65% | CHANGED. No reachable crash, so defer the locator-agnostic `annotate` and pin today's parser rejection; B's guard is withdrawn too. |
| C-003 | B | 65% | `prior` is inert (`ledger.py:259-272`), so no new line kind. |
| C-004 | B | 85% | `cluster_v2` never joins anchor-only findings (N1, `test_review_cluster.py:279-293`). |
| C-005 | HYBRID | 55% | Open in the core (N5); any adapter-side strictness belongs to C-10. |
| C-006 | HYBRID | 55% | CHANGED. The ledger drops pass-through keys (`ledger.py:172-180`), but no consumer reads them from the ledger yet, so defer. |
| C-007 | B | 70% | The shared constants module and repair step deduplicate real copied literals (N6) without merging parsers. |
| C-008 | HYBRID | 65% | CHANGED. A's verified defect, fixed as a locator policy inside the v1 engine (B's point); its clearing rule goes to C-02 (N3). |
| C-009 | HYBRID | 60% | PR review needs no ledger, and both designs need vocabularies as data (`findings_v2.py:109-110`). |
| C-010 | HYBRID | 60% | Citations are untested, not disproved; measure under the merged T3/5.3. |
| X-001 | B | 70% | Converge on a trigger; no current consumer, and converging needs new clustering code. |
| X-002 | B | 65% | The duplicated items are helpers and literals that the shared contract removes; git history shows no cost paid twice. |
| X-003 | B | 75% | The rewrite would break the pinned anchor-only clustering test and the loop's agreement between reviewers. |
| X-004 | HYBRID | 55% | Same as C-005. |
| X-005 | NEITHER | 85% | Neither fix closes a real path. The real issues are the stuck row (N3) and dropped re-finds that cannot hold a row open (N2). |
| A-001 | NEITHER | 90% | Contradicted by `findings.py:104` and `ledger.py:135-136`. |
| A-002 | NEITHER | 60% | CHANGED. Neither variant states how line numbers reach reviewers; it must be stated before the merged T3/5.3 runs. |
| A-003 | B | 75% | The kernel is one commit old, runs in shadow mode, enforces v1 categories and cannot cluster anchors; it is fit to share helpers with, not to host the loop. |

Not checked: B's claim that INV-K Check 11 would catch a constant-name clash (not run); the E1 and E2 run counts; and how line numbers reach reviewers in the loop brief (A-002).
