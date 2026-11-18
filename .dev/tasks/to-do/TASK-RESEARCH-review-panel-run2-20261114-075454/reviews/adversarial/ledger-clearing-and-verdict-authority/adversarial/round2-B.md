# Round 2 rebuttal, Advocate for Variant B (slot C-02, ledger clearing and verdict authority)

Date: 2026-11-14. Re-read this session: `ledger.py` 1-494, `findings.py` 85-196 and 276-298 and 340-457, `findings_v2.py` 140-179, `merge_cmd.py` whole, `ledger_cmd.py` whole, `panel.py` 186-199 and 590-610, `document_review_loop_prompts.md` 26-75, `spec-panel.md` 254-265, `tests/review/test_review_ledger.py` 15-40, 66-88, 316-340, 518-546 and grep hits, `synth-06-conflict-log.md` VM-3/VM-6 rows (178, 181, 400), all five adversarial papers. Not re-read: `test_review_rules_text.py`, `stoprule.py`, research files, `locate` past line 298.

## 1. Replies to the criticisms of B (round1-A.md, round2-A.md)

| Criticism | Reply |
|---|---|
| A-R1 W1/W2: the quote is not evidence of examination and adds an unmeasured false-hold source | Concede, and act on it (C-002 below). New reason beyond A's: the span a row carries is lossy for replacements (`findings.py:431` docstring "maps to the start of its new range"; the author's own comment at `ledger.py:224-225` says a defect can sit farther down the replacement), so a span-restricted quote check, my round-1 narrowing, falsely holds long replacements. A deletion leaves no AFTER text to quote at all. |
| A-R2 §1: "B's narrowing is vacuous exactly where `map_span` returns None for a deletion (`ledger.py:345-346`)" | **Wrong reason, right conclusion.** `map_span` returns `None` only when the input span is `None` (`findings.py:434-435`); a deleted line maps to `(j1, j1+1)`, the line after the deletion (`findings.py:419-427, 439`). And a row can reach `resolved_check` only if `hunks_touch` is true on `span` or `span2` (`ledger.py:331-333`), and `hunks_touch(None)` is false (`findings.py:446-447`), so a reached row always has a live span. The check is not vacuous there; it is satisfiable by quoting a neighbour, which is the same "proves reading, not fixing" limit I conceded in round 1. |
| A-R2 §1: the shipped quotes (`prompts.md:44,46`) are diff lines for a role-swap check, not per-row quotes | Concede. My round-1 strength 2 was overstated. The AFTER lines exist; a per-row quote is new reviewer work. |
| A-R1 W3 / A-R2: B6 predicate misgrades line 31 and `spec-panel.md:259` | Concede, re-read `prompts.md:31`: Medium "even when its label is MAJOR" is not category-expressible. Predicate dropped (C-004). |
| A-R1 W4: B7 expiry "has no machine meaning" | Concede; no expiry in the core (C-006). |
| A-R1 W5: B derives the verdict on read but may leave a stored copy | Concede, and VM-3 is stricter than I treated it (C-009). |
| A-R1 W6 / INV-H: quote copies document text into history | Mitigated, not removed: `evidence` bounded at 200 characters and never copied into telemetry (anchors already live in rows). |
| A-R1 W2 / X-001: B1 breaks the pinned rule and B's pin list omits the test | Concede. Re-read `test_review_ledger.py:318-338`: its assertions (L4, L2 stay `open`) survive, the stated rule does not. B1 also wrote "`prior open` sets the row" for any row, which would let a hearsay line reopen a human-deferred row, the thing I attacked A for. Narrowed (C-005). |

## 2. Updated assessment of A's final positions

**Accept**: need gate with `block_ok` filter, priors map built first, dissent routed to `regressed`, no quote gate, CRITICAL floor in `merge_round`, no expiry, terminal deferral with `refound_deferred`, `verify_ids`/`held_ids` and the `next` field, `pending_new_sha256`.

Checks of A's new claims (all hold unless noted):
- Priors from invalid-block reviewers are collected: `findings.py:186` appends before `ok` goes false at `:190`; `ledger.py:139-140` collects without a `block_ok` test. Confirmed.
- Priors not de-duplicated: the prior branch `continue`s at `findings.py:187`, before `seen.add` at `:193`. Confirmed. Count distinct reviewers, not lines.
- Clear loop runs before the prior loop (`ledger.py:254-258` vs `:259-272`). Confirmed. Also `lid not in members_by_lid` is redundant: a re-found row was already set to `regressed` at `:235-238`, so any row still `resolved_check` at `:254` was not re-found.
- `apply_revision` skips non-open rows (`ledger.py:328`). Confirmed.
- `--resolution`: A's correction is right (`merge_cmd.py:73-83` builds only a model map), but the ids are in hand there; the real gap is that `--resolution` is optional (`merge_cmd.py:50-56`).
- No test pairs CRITICAL with `blocking: false`: confirmed for the ledger tests. `fl` defaults `severity="CRITICAL"` (`test_review_ledger.py:28`), but all four `blocking=False` calls pass `severity="MINOR"` (`:77-78, :313, :537-538, :560`). Caveat: a future `fl(..., blocking=False)` without severity hits the floor.
- Parser-side floor wrong: confirmed (`findings.py:188-192` drops the line and sets `ok` false).
- Only `defer` and `verdict()` read stored round keys in `cli/review` (grep outside reflect: `ledger.py:358-370`, `ledger_cmd.py:109` through `verdict()`). Tests do read them (`test_review_ledger.py:133-134`, and `:280-298` where the variable source was not re-read).
- **CRITICAL floor vs `findings_v2.py:161-162`: no conflict.** That rule applies only when `reflect_category` is set and demands `blocking == (severity != "MINOR")`, so CRITICAL must be blocking there too; the floor is a subset. They differ in action (v2 returns an error; the floor flips and warns), one behaviour per lens, a minor inconsistency.
- **VM-3 exact wording** (`synth-06-conflict-log.md:178`, repeated `:400`): "The verdict is derived from rows on every read and is never stored", status DECIDED-BY-EVIDENCE [CODE-VERIFIED]. A's primary C-009 form (keep a merge-time snapshot of `verdict`, `decision`) is a stored verdict under another name, so A's own conditional fires. I take the drop form.
- VM-6 is decided but unbuilt: `merge_round` checks only `n == len(rounds)+1` (`ledger.py:114-118`); the row is a "plan item" (`synth-06:181`). A's evidence 5 holds only once it lands; I supply a derived form in C-008.

**Still dispute**: (a) A's fallback "without `--resolution`, requested is the reports passed" silently weakens the gate; (b) A is silent on `revise` non-idempotency (section 3); (c) A's primary C-009 form.

## 3. New evidence

1. **`ledger revise` is not idempotent.** `ledger.py:343-347` maps every row's span through the old-to-new opcodes on each call; a second call with the same files re-maps spans already in new coordinates (nothing checks that a revision is pending; the old-hash check at `:308-314` passes again). C-003's recovery from a hash mismatch invites exactly that re-run. The pending hash is the natural guard.
2. **`locate` already solves quote normalisation** (`findings.py:276-298`: whitespace-flattened, returns half-open 0-based line ranges). The record-only flag is one call; my round-1 "module work" hand-wave was unneeded.
3. **A bad optional key must not be able to kill a line.** Any parser error drops the line and sets `ok` false (`findings.py:188-192`). An overlong or non-string `evidence` that raised an error would invalidate the reviewer's whole block and lose every clear. Rule: ignore a bad `evidence`, no error.
4. **A free proxy for quote false-hold rate**: `annotate` already computes `anchor_status` missing/found (`findings.py:350`); the miss rate of anchors in existing reports is the miscopy rate a quote gate would inherit. Not yet measured.
5. **Dissent can be masked by a same-round non-blocking re-find**: `ledger.py:213-218` lets `current` (not blocking) overwrite `row["blocking"]`, so `prior L1 open` plus a MINOR re-find leaves a `regressed`, non-blocking row outside `brief_ids` (pinned by `test_review_ledger.py:518-546`, which has no prior line).

## 4. Final positions (exact rules for the merged design)

| ID | Final rule | Differs from A's final? |
|---|---|---|
| C-001 | Build the prior map first (`ledger.py:259-272` moves above `:254`). A `resolved_check` row becomes `resolved` iff (a) distinct `block_ok`-true reviewers typing `resolved` for it >= `need`, (b) no `block_ok`-true reviewer typed `open` or `regressed`, (c) not re-found this round. A `block_ok`-true `open|regressed` moves it to `regressed` (history `dissent`). Unanswered: stays `resolved_check`, listed in `verify_ids`. `need = min(Q_kind, requested)` where `requested` = reviewers in `--resolution` when given; **when absent, `need = Q_kind` (fail closed), not the report count.** Ask C-03 to set `Q_kind(re-review) = 1` so the unknown case cannot deadlock the standard flow (`panel.py:600`). | Yes: the `--resolution`-absent rule and the `Q_kind` request. |
| C-002 | Optional string `evidence` on a prior line, kept only if it is a string of at most 200 characters after flatten, else ignored with no error. Ledger writes it to the `prior_note` event with `quote_in_doc = bool(fnd.locate(doc_text, quote))`. Never gating. Reviewers are asked for it (line 61) so M1 has data. Promotion to a gate only on M1 evidence, and only with both a deletion carve-out and a fix for the lossy replacement span. | No (converged). |
| C-003 | `apply_revision` stores top-level `pending_new_sha256`; `merge_round` refuses (ledger unchanged) on mismatch, then clears it; **`apply_revision` refuses while one is pending** (guard for evidence 1). Recovery from a mismatch: restore the file to the stored hash. | Addition (the revise guard). |
| C-004 | In `merge_round`, at the point findings are annotated (`ledger.py:135-138`): `blocking = typed or severity == "CRITICAL"`; member records keep `blocking_typed`; each flip adds a warning. No category predicate in the core, `verdict:` line stays parser-neutral. M3 stays an offline measurement, not a code path. | No. |
| C-005 / X-001 | A `prior` line moves only a `resolved_check` row (clear or dissent). On any other status it is a `prior_note` plus a warning. Edit docstring `ledger.py:3-4`; rename `test_prior_lines_never_change_a_status`; add `resolved_check` cases. | No. |
| C-006 | `defer` needs `--owner` and `--reason`, allowed on a blocking row in `open`, `regressed` or `resolved_check`; writes no round record; terminal and counted open; no expiry. | No. |
| C-007 | Re-found deferred row stays `deferred`; `refound_deferred` in the merge result and in the Escalation text. | No. |
| C-008 | `brief_ids` = blocking `open|regressed`; `verify_ids` = blocking `resolved_check`; `held_ids` = blocking `deferred`; all derived on read. PASS iff all three empty; else FAIL, REVISE while `n < cap`, ESCALATE at the cap or when only `held_ids` remain. Exit codes 0/10/11 unchanged. Empty `brief_ids` with non-empty `verify_ids`: Reviser-brief section says "no revision needed; re-review the same candidate against the same baseline"; `verdict` JSON adds `next`. The report detail section and the Escalation paragraph list all three lists (`ledger.py:438-466, 482` today cover `brief` only). **VM-6 derived form**: `merge_round` refuses when `len(rounds) >= cap_reviews` or the derived decision before the merge is ESCALATE. | Addition (VM-6 form). |
| C-009 | **Drop** `verdict`, `decision`, `brief_ids` from new round records; `defer` stops writing them; `verdict()` derives from rows and ignores stored keys in old files; schema string kept. Store facts (`pending_new_sha256`, `blocking_typed`, `owner`, history), derive judgments (`verify_ids`, `held_ids` too). | Yes (A's primary is the snapshot; this is A's conditional form, triggered by VM-3). |
| A-005 | Independent of C-03 except the `Q_kind` interface above. | Minor. |

## 5. Positions changed since Round 1

| ID | Old (round 1) | New | Why |
|---|---|---|---|
| C-001 | Per-row quoted answer, B-style | Quorum gate `need`, dissent to `regressed`, no quote | Gate power of the quote is unmeasured (X-002); A's gate plus dissent route covers the reproduced paths; `ledger.py:328` |
| C-002 | Quote gates clearing | Record-only with `quote_in_doc` | Span lossy (`findings.py:431`, `ledger.py:224-225`), deletions leave nothing to quote, no test separates a lazy yes |
| C-004 | Parser-side floor; lens predicate as warning | Floor in `merge_round`; no predicate | `findings.py:188-192` drops the line; `prompts.md:31` is not category-expressible |
| C-005 | `prior open|regressed` sets any row | Only `resolved_check` rows move | Would reopen a human park; `ledger.py:3-4` |
| C-009 | Additive; stale `verdict` meaning changes | Drop stored `verdict`, `decision`, `brief_ids` | VM-3 literal wording (`synth-06:178`) |
| C-006 | Expiry recorded as metadata | No expiry | Nothing reads it |
| C-003 | Hash binding | Same, plus refuse `revise` while pending | Non-idempotent revise |
| C-008 | `verify_ids` outside brief | Accept A's `next` field and VM-6 derived refusal | Exit code stays 10 with no pinned change |
| A-005 | QUALIFY | Independent except `Q_kind` | `panel.py:600` one-reviewer re-review |

## 6. Unaddressed by either side (for the fault-finder)

1. **Exit-code-only callers.** `ledger verdict` exits 10 (REVISE) when `brief_ids` is empty and only `verify_ids` remain. A caller that reads the code alone runs a reviser with no ids, then re-reviews an empty diff, and the brief says an empty diff leaves every prior blocker open (`prompts.md:44`, `spec-panel.md:262`): the verify rows regress. The `next` field helps only callers that read it, and `prompts.md:70` does not tell coordinators to.
2. **Unanswered burns a review of the cap.** Alternative not weighed: refuse-and-rerun (like the zero-valid-block refusal, `ledger.py:150-157`), which costs no cap but is unbounded without a coordinator retry limit.
3. **Id vocabulary.** Priors key on ledger ids `L<n>` (`ledger.py:185, 261`); reviewers type finding ids `F<n>`. Whether PRIOR is the merged report (which carries `L` ids, and claim detail only for brief rows, `ledger.py:438-466`) is UNVERIFIED (`prompts.md:43` says "previous review report"). A wrong-vocabulary answer only warns (`ledger.py:263`) and holds. M2 must count compliance by ledger id, not presence of prior lines.
4. **Dissent from an invalid-block reviewer is ignored** though `findings.py:186` collects it. Fail-closed asymmetry argues for a hold-only (no status move) veto; unspecified.
5. **Completion state.** `block_ok` is the only reviewer-quality test; a reviewer that returned "incomplete" with a valid block (`prompts.md:48`) counts toward `need` (A's round-1 concession 6, absent from A's final).
6. **Dissent plus same-round non-blocking re-find** (new evidence 5): the row can drop out of every list. Rule needed: a valid `open|regressed` prior stops `row["blocking"]` being lowered this round.
7. **No undefer or reopen command**: a mistaken `defer` is permanent; a deferred `resolved_check` row loses its fix state.
8. **Held-only ESCALATE at `n < cap` plus VM-6** refuses any further round, so a human who defers the last open row cannot get a confirming re-review. Policy question.
9. **Mid-loop version change**: an older installed `verdict()` reads `last["verdict"]` (`ledger.py:366-369`) and `ledger_cmd.py:104-107` catches only `LedgerError`.
10. **Test churn**: stored-key reads at `test_review_ledger.py:133-134` (and probably `:280-298`), plus the silence-clear pins (`:193-217`, `:376-385` per B's round-1 E7, not re-read).
