# QA Report — Task Integrity (Lens: B2 Self-Containment)

**Topic:** Differential Backtest/Eval Harness for sc:troubleshoot Pipeline Hardening Closure (E1-E5 OLD=MISS vs NEW=CATCH)
**Date:** 2026-06-11
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix authorization:** false (report-only)
**Fix cycle:** N/A

---

## Scope

Adversarial B2 self-containment audit of every checklist item in the task file. Each item must carry all 5 B2 components (context + action + output + verification + completion gate), restate prior context rather than reference it, embed full agent prompts, cite specific file paths, use measurable verification criteria, and stay 1:1 per escape/component. Special-attention check: per-escape PARENT shas must appear concretely (E1=94d5baa0, E2=10723863, E3=e97aa4fd, E4=1b0264f1, E5=d878bc6d) with NO `^`.

---

## Items Reviewed (B2 lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| B2-1 | Every checklist item has all 5 B2 components (context+action+output+verification+completion gate) | FAIL | All work items carry context ("because…"), action, output path, "ensuring…" verification clause, and "Once done, mark this item as complete." The QA-gate aggregation/fix/verify items are well-formed. EXCEPTION: Step 6.4 carries an unresolved `{EXECUTOR_CLASS}` placeholder (line 504) — a self-containment hole (see Issue #1). |
| B2-2 | No item references prior-item context without restating it | PASS | Items that depend on earlier outputs (e.g. Step 2.2 reads `git_replay.py`, Step 4.8 reads the 5 runners) restate the full path + the specific symbols/shape they expect. No "see above"/"continue from previous"/"as above" found via grep (only Step 6.4 hit, which is the placeholder, not a back-ref). |
| B2-3 | Agent-spawning items embed the full prompt (not "see SKILL.md") | PASS | Every QA-gate spawn item embeds: agent type, `fix_authorization`, verbatim ADVERSARIAL STANCE string, the exact files to read, the precise verification predicate, the output report path, and the binary PASS/FAIL verdict rule. No "use the template from SKILL.md" deferrals. grep for "see SKILL"/"per the template"/"use the template from" → 0 hits. |
| B2-4 | File paths specific; per-escape PARENT shas concrete with NO `^` | PASS (with 1 clarity note) | Every OLD=MISS runner (Steps 4.3-4.7) names its bare parent sha: E1=`94d5baa0`, E2=`10723863`, E3=`e97aa4fd`, E4=`1b0264f1`, E5=`d878bc6d`. `REPLAY_ESCAPES` (Step 2.1), the replay table (Step 1.4), and the G1 constraint (line 125) all agree. Verified against authoritative `research/08-gap-fill-reconciliation.md` (lines 56-62, 80-84, 121-125) — exact match. NO `^`-decrement anywhere. The only `^{commit}` occurrences (G2 skipif, lines 129/204/515) are git peel-to-commit syntax, NOT caret-parent decrement — task explicitly disambiguates this (Issue #4, clarity-only). |
| B2-5 | Verification criteria measurable (not "verify it works") | PASS | "ensuring…" clauses are concrete and checkable: "REPLAY_ESCAPES contains exactly 5 records", "NO prefix_parent_sha contains a `^`", "0 failed AND 0 errored", "both ruff commands pass", "backtest_status == complete ONLY when all 5 CATCH". No vacuous "verify it works". |
| B2-6 | No batch items — each escape + each component its OWN item | PARTIAL | E1-E5 each have a dedicated item (4.3-4.7). Each harness component (git_replay, replay_executor, catch_rate model/writer/schema, conftest) has its own item. EXCEPTION: Steps 6.2.2 (spawn 3 agents) and 6.2.3 (spawn 4 agents) each batch multiple agent spawns into a single checklist item (Issue #2). |
| B2-7 | No items based on [CODE-CONTRADICTED]/[UNVERIFIED]; NEW-gate refs handled as skip-guarded proxies | PASS | The UNVERIFIED-greenfield NEW=CATCH refs are never hard-asserted. Every NEW=CATCH half (4.3b-4.7b) is decorated `requires_impl_ref(...)` skip-guard; the model/report items record the "documentation-presence PROXY" limitation (Steps 3.2(4), 3.3(4)). The E4 [CODE-VERIFIED] HEAD-drift (healed via `20693bb8`) is correctly handled by pinning replay to `1b0264f1`, not HEAD. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 6.4, line 504 (`--executor-model {EXECUTOR_CLASS}`) | **Unresolved template placeholder breaks B2 self-containment.** The POST-reflect item embeds a literal `{EXECUTOR_CLASS}` token in the `/sc:reflect` command. An executor processing this item in isolation cannot resolve it — it is neither a concrete model id (e.g. `sonnet`/`opus`) nor a documented substitution rule restated in the item. Every other command in the file is fully concrete; this is the one templating leak. This also trips TB-Add-1 (placeholder scan: title/body must contain no unresolved `{…}` token an executor would have to guess). | Replace `{EXECUTOR_CLASS}` with a concrete value (e.g. `--executor-model sonnet`) OR drop the flag if `/sc:reflect` defaults are acceptable, OR add a restated one-line resolution rule inside the item ("substitute `{EXECUTOR_CLASS}` with the same model class this task is being executed under"). The item must be executable without external lookup. |
| 2 | MINOR | Steps 6.2.2 (line 474) + 6.2.3 (line 478) | **Final-QA spawn items batch 3 and 4 distinct agent spawns into a single checklist item.** B2 atomicity (and item-10 granularity) prefers one atomic unit per item. Each of these items embeds 3-4 separate lens prompts (lens 1/2/3 in 6.2.2; content-lens 1/2/3 + domain-lens 4 in 6.2.3). They are parallel-by-design (the item says "IN PARALLEL, one message, multiple Agent calls"), so the batching is intentional and the per-lens assignments ARE individually self-contained inside the item. This is a soft granularity note, not a self-containment failure: the per-lens prompts are all present. Contrast with the per-phase QA gates (Phases 2-5) which correctly give each lens its OWN item (e.g. 2.QA.2 through 2.QA.7). | Optional: split 6.2.2 into 3 items and 6.2.3 into 4 items for consistency with the per-phase gate granularity. Acceptable as-is IF the executor reliably emits all spawns in one message. Flagging for consistency, not as a blocker. |
| 3 | MINOR | Step 6.4, line 504 (`--diff $(git merge-base HEAD origin/master)`) | **Command-substitution subshell inside an embedded command.** The `$(git merge-base …)` is correct and the surrounding prose restates the intent ("the diff base is the merge-base of HEAD and origin/master, not `start_commit..HEAD`"), so it IS self-contained. Noting only that the command relies on `origin/master` being fetched; the item does not restate a `git fetch origin` precondition the way Step 1.2 does. An executor on a stale clone could get a wrong/empty merge-base. | Optional: add "(ensure `origin/master` is fetched first)" to the item, mirroring Step 1.2's explicit `git fetch origin`. Self-containment is otherwise satisfied. |
| 4 | MINOR (clarity) | G2 skipif, lines 129, 204, 515 (`git cat-file -e <parent>^{commit}`) | **`^{commit}` peel-syntax visually resembles the forbidden `^` caret-decrement** that G1 prohibits. This is NOT a defect: `<sha>^{commit}` is git's peel-to-commit-object syntax (the `^{...}` brace form), categorically different from `<sha>^` (first-parent decrement). Step 2.3 explicitly disambiguates ("with f-string-escaped literal braces (NOT a bare `cat-file -e <sha>`)"). Raising only because a B2 executor skimming for "no caret" could mis-flag it; the task already pre-empts the confusion. | No fix required. Optionally add a one-clause note "(`^{commit}` is git peel-syntax, not the G1-forbidden `^` parent-decrement)" at the G2 constraint (line 129) to remove all ambiguity for the executor. |
| 5 | MINOR | Step 1.4 (line 184) replay-table spec | **fix_sha column reuses values that are also parent_shas of sibling escapes — potential executor confusion, but NOT an error.** E2's fix_sha `e97aa4fd` equals E3's parent_sha; E5's fix_sha `10723863` equals E2's parent_sha. This interleaving is CORRECT per the linear-history note in `research/08` (line 64) and is restated in the item. A careless executor could swap a fix_sha for a parent_sha. The item mitigates this by labeling `fix_sha (provenance only)` vs `prefix_parent_sha (the BARE checkout target)` and the OLD=MISS runners (4.3-4.7) each independently name only the parent sha as the checkout target. | No fix required; the labeling + per-runner restatement is sufficient. Flagging as the most error-prone surface for the executor to watch. |
| 6 | OBSERVATION | Steps 2.1, 3.2, 3.3, 4.x | **Several work items are long (≈single dense paragraph each) but remain single-paragraph and self-contained per B2.** They embed file-to-read + source line refs + multi-part numbered create-spec + "ensuring" clause in one paragraph. This is the template-02 self-contained style (context+action+output+verification fused), not a multi-line split, so it satisfies B2 component-structure. Granularity (item-10) borders on heavy for Steps 2.1/3.2/4.6 (multiple sub-parts (1)-(4)), but each produces ONE file, so atomicity holds. | No fix required under the B2 lens. Item-10 granularity is out of this lens's scope; another lens may weigh in. |

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep (Bash) : 3 | Glob: 0 | Bash: 3
  - Note: Read calls = 6 (full task file in 5 paged Reads + 1 report re-Read for freshness). Bash/grep calls = 3 (sha cross-check vs research/08, placeholder/back-ref scan, per-escape checkout-target scan). Tool calls (9) ≥ checklist items (7) → engagement minimum satisfied.
- Every B2 sub-check was verified against the actual file text (no reliance on other QA reports). Sha pins independently cross-validated against `research/08-gap-fill-reconciliation.md`.

## Summary

- B2 sub-checks passed: 5 / 7 (B2-2, B2-3, B2-4, B2-5, B2-7)
- B2 sub-checks failed/partial: 2 (B2-1 FAIL via Issue #1; B2-6 PARTIAL via Issue #2)
- Issues found: 6 (IMPORTANT: 1 | MINOR: 4 | OBSERVATION: 1)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

**The single blocking B2 defect is Issue #1** — the unresolved `{EXECUTOR_CLASS}` placeholder in Step 6.4. It is the only place an executor cannot proceed without external information, which is the precise failure B2 self-containment exists to prevent. All other findings are MINOR consistency/clarity notes or non-defects.

**The special-attention check PASSED cleanly:** all five per-escape PARENT shas appear concretely and verbatim (E1=`94d5baa0`, E2=`10723863`, E3=`e97aa4fd`, E4=`1b0264f1`, E5=`d878bc6d`) in every place they are needed — the replay table, `REPLAY_ESCAPES`, the G1 constraint, and each OLD=MISS runner — with NO `^` caret-decrement anywhere, cross-validated against authoritative `research/08`. E4 is correctly pinned to `1b0264f1` (not HEAD) and the NEW=CATCH refs are correctly skip-guarded proxies, never hard-asserted.

## Recommendations

1. **Before execution (blocking):** Resolve Issue #1 — replace `{EXECUTOR_CLASS}` in Step 6.4 with a concrete model id or a restated in-item substitution rule.
2. **Optional consistency pass:** Address Issues #2 (split the batched final-QA spawn items) and #3 (restate the `git fetch origin` precondition for the merge-base) to match the discipline used elsewhere in the file.
3. **Optional clarity:** Add the one-clause `^{commit}` peel-syntax disambiguation at the G1/G2 constraint (Issue #4) to remove any executor mis-flag risk.

---

## Overall Verdict: FAIL

**Rationale:** A single IMPORTANT B2 self-containment defect (Issue #1, the unresolved `{EXECUTOR_CLASS}` placeholder in Step 6.4) blocks a clean B2 PASS — under zero-tolerance, any item that cannot be executed without external information fails the lens. The defect is narrowly scoped and trivially fixable (one token). Everything else in the file — including the load-bearing per-escape sha pinning, the embedded agent prompts, the skip-guarded UNVERIFIED-ref handling, and the measurable verification clauses — satisfies B2. Once Issue #1 is resolved, this file would PASS the B2 lens.

## QA Complete

---

## Findings (appended incrementally)
