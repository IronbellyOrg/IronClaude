# QA Task-Validation Fix Report (Consolidated, Serialized Fix Agent — I20)

**Task file:** `TASK-RF-troubleshoot-hardening-evals-20260611-160018.md`
**Findings source:** `qa/qa-task-validation-consolidated.md`
**Mode:** task-integrity / consolidated-fix / fix_authorization: true
**Date:** 2026-06-11

---

## Overall: FIXES_APPLIED summary below; all surgical Edits, no phase rewrites.

---

## FIX-1 (IMPORTANT) — Step 6.4 `{EXECUTOR_CLASS}` placeholder resolved + (MINOR) `git fetch origin` precondition

**Location:** Step 6.4 POST-reflect item, line 504.

**Before (excerpt):**
> ...then spawn a subagent that runs `/sc:reflect ... --depth standard --executor-model {EXECUTOR_CLASS}`, because the POST reflect gate...; record the returned `{verdict, run_id, report}` ... ensuring the diff base is the merge-base of HEAD and origin/master ...

The bare `{EXECUTOR_CLASS}` was an unresolved literal-brace placeholder (tripped TB-Add-1 placeholder scan; not self-contained; would spawn reflect with an invalid model name). The merge-base also had no `git fetch origin` precondition.

**After (excerpt):**
> ...then run `git fetch origin` FIRST (precondition: the merge-base must resolve against a current `origin/master` ref, mirroring Step 1.2 ...), then spawn a subagent that runs `/sc:reflect ... --depth standard --executor-model <EXECUTOR_CLASS>` where `<EXECUTOR_CLASS>` is the model class YOU (the executing agent) are running as — one of `opus` / `sonnet` / `haiku` — substituted in literally so reflect excludes your own class from its heterogeneous reviewer panel (this is what makes the reflect panel executor-disjoint); if you cannot determine your class, use `opus`, because the POST reflect gate is the independent UC-2 deviation audit ... ensuring `git fetch origin` ran before the merge-base, the diff base is the merge-base of HEAD and origin/master (not `start_commit..HEAD`), `<EXECUTOR_CLASS>` is replaced with your actual model class (never left as a literal placeholder), this item is a SELF-RUN check (NOT a human-handoff/HALT ...) ...

**Notes:**
- `--executor-model` flag KEPT (executor-disjoint intent preserved).
- `$(git merge-base HEAD origin/master)` unchanged — NO `^` caret introduced.
- SELF-RUN POST-reflect form preserved (NOT converted to human-handoff/HALT).
- `{verdict, run_id, report}` is a returned-field set-literal, not a placeholder — intentionally left.
- Placeholder scan: SPEC_PATH / TASK_FILE / DEPTH were already concrete (spec path, task-file path, literal `standard`). Post-fix grep `\{[A-Z_]{3,}\}` over the whole file → **zero matches**.

---

## FIX-2 (IMPORTANT) — `backtest_status=complete` anti-vacuity derivation tightened (model + schema + fidelity test)

### 2a — Model/derivation item (Step 3.2, line 258)

**Before (excerpt):**
> (3) a module-level `_derive_backtest_status(escapes) -> str` helper and a `__post_init__` ... or if `backtest_status != _derive_backtest_status(escapes)`; (4) a `proxy_limitation` note field **or module docstring** recording that NEW=CATCH is a documentation-presence proxy ...; ensuring ... the derivation rule is EXACTLY all-5-CATCH→`complete` / 1-4→`partial` ... / 0-or-not-run→`not_run` ...

**After (excerpt):**
> ... the derivation is ANTI-VACUITY-TIGHTENED per RELEASE-SPEC §5.4 / research/07 (lines ~136-137): `backtest_status = complete` ONLY when ALL 5 escapes have `verdict == CATCH` AND EACH escape ALSO carries a non-null/truthy `negative_witness` AND a non-null `card_path` (all three conjuncts per escape) — an all-CATCH report with any missing `negative_witness` or `card_path` MUST derive `partial`, NOT `complete` ...; `partial` whenever a replay ran but [the condition] is unmet, with the report exposing the escape IDs missing ANY of `{CATCH, negative_witness, card_path}`; `not_run` when no replay ran ...; and the `__post_init__` MUST additionally ASSERT `card_path` participates in the invariant ...; (4) a SERIALIZED `proxy_limitation` string field on `CatchRateReport` (NOT docstring-only) that reaches the JSON artifact via `to_dict()`/`_CATCH_RATE_FIELDS` ...

Covers consolidated Issue-1 (derivation), Issue-2 (`proxy_limitation` serialized JSON field, not docstring-only), Issue-3 (`card_path` asserted in invariant).

### 2b — Schema item (Step 3.4, line 266)

**Before:** `required: [... "escapes"]`; escapeResult `verdict` enum only.
**After:** `required: [... "escapes","proxy_limitation"]` (proxy-honesty note cannot be dropped); escapeResult now also pins `negative_witness` `{"type":"boolean"}` and `card_path` `{"type":["string","null"]}`. Keeps model↔schema in sync with the new serialized field.

### 2c — Schema-fidelity test item (Step 3.5, line 270)

**Before (excerpt):**
> (e) assert the derivation: all-5-CATCH → `complete`, a mix → `partial` with the missing escape IDs surfaced, empty → `not_run`; AND ALSO create the fixtures `valid_minimal.json`, `valid_full.json`, `invalid_bad_status.json`, `invalid_bad_verdict.json`; ...

**After (excerpt):**
> (e) assert the ANTI-VACUITY-TIGHTENED derivation [all three conjuncts]; AND CRITICALLY (f) assert the anti-vacuity edge case directly — a report where ALL 5 escapes are `verdict==CATCH` but at least one has a null/falsy `negative_witness` (and a second variant where one has a null `card_path`) derives `partial`, NOT `complete` ..., and that `card_path` is asserted in the invariant (a `complete`-claimed escape with null `card_path` raises); AND (g) assert `proxy_limitation` is present in `render_catch_rate_json` output (serialized to JSON, not docstring-only); AND ALSO create the fixtures `... valid_minimal.json`, `valid_full.json`, `invalid_bad_status.json`, `invalid_bad_verdict.json`, and `all_catch_missing_witness.json` (all 5 `CATCH` but one with null `negative_witness`, asserted to derive `partial` not `complete`); ...

New fixture `all_catch_missing_witness.json` + clauses (f)/(g) implement the consolidated file's required fixture case (all-CATCH-but-missing-witness → expect `partial`).

---

## MINOR — applied / deliberately not applied

- **`git fetch origin` precondition (B2 Issue#3 / structure):** APPLIED — folded into the FIX-1 Edit on Step 6.4 (single item, surgical).
- **Borderline-atomic Step 3.2 multi-symbol (B2 Issue#2):** NOT touched (acceptable per consolidated guidance; "do NOT churn").
- **TB-Add-6 "ensuring..." verification dialect:** NOT touched (consistent RF B2 dialect across file; not a defect).

## Out of scope (no change, per consolidated file)
- MINOR-3 (CI zero OLD=MISS coverage on shallow CI) — documented in Risks/OQ-1, designed behavior.
- Upward QA deviation (7-agent gates) — intentional.

---

## Load-bearing content preserved (verified post-edit)
- G1 no-caret parent SHAs intact: E1=`94d5baa0` (9×), E2=`10723863` (12×), E3=`e97aa4fd` (12×), E4=`1b0264f1` (24×), E5=`d878bc6d` (10×).
- Caret scan `[0-9a-f]{7,8}\^` over whole file → **zero matches** (no `^` introduced).
- E4 pinned to `1b0264f1`; skipif/no-xfail, collision boundary, `parents[3]`, parent `__init__` only-if-absent — untouched.
- SELF-RUN POST-reflect form preserved (1× "SELF-RUN check (NOT a human-handoff").

## Verification tool engagement
- Read: 4 | Grep/Bash-grep: 5 | Edit: 4 | Write: 1
- Post-edit greps confirm: 0 brace placeholders, 0 carets, proxy_limitation ×3 (model+schema+test), all_catch_missing_witness ×1, ANTI-VACUITY ×2.

---

FIXES_APPLIED: 4, REMAINING: 0
