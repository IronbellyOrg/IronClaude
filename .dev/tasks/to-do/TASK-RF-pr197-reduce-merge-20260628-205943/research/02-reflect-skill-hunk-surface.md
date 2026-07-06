# R2 — Reflect SKILL.md hunk-surgery surface (HIGHEST RISK)

**Target file:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
**Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation`
**Diff command:** `git diff origin/master...HEAD -- src/superclaude/skills/sc-reflect-protocol/SKILL.md`
**Goal of Step 3:** revert the #197 instance-level rewrite back to master's executor-class-EXCLUSION canonical state, WHILE RETAINING the net-new EV-1/EV-2/§12 on-disk-verification value #197 added.
**Status:** Complete

---

## 0. CRITICAL HAZARD (read first)

**`git checkout origin/master -- src/superclaude/skills/sc-reflect-protocol/SKILL.md` IS FORBIDDEN.**
A full file-level checkout would DELETE the four net-new EV hunks (EV-1 §8 STOP, EV-2 §9.2 + metrics.json `merge_method` guards, §12 `file_present + card_count` detector) because those tokens have **0 hits on origin/master** (verified). Surgery MUST be hunk-level (manual `Edit` per hunk).

**Line-count sanity:** master blob = 1989 lines; branch = 1993 lines (+4 net). After surgery the file should be LONGER than master (EV additions stay), so a "restored to exactly 1989" check would be WRONG.

---

## 1. Hunk enumeration & classification

The diff has **11 hunks**. Classification:

| # | Diff @@ anchor | Branch lines | Section | Class | Action |
|---|----------------|--------------|---------|-------|--------|
| H1 | @@ -86,6 +86,7 | branch 89 | Input-resolution `--executor-model` line | RESTORE-MASTER (delete-only) | DELETE the added line; master has NO such line |
| H2 | @@ -617,17 +618,23 | branch 621–637 | §7.1 reviewer-composition rewrite | RESTORE-MASTER | Replace instance-level block with master executor-class-exclusion block |
| H3 | @@ -661,7 +668,7 | branch 671 | §8 adversarial invoke `--compare` card paths | **RETAIN-BRANCH** (see §3.5) | Keep branch (yaml card naming; not instance-level) |
| H4 | @@ -678,6 +685,8 | branch 688 (+blank 687) | §8 EV-1 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK STOP | **RETAIN-BRANCH (EV-1)** | KEEP — must NOT revert |
| H5 | @@ -687,7 +696,7 | branch 699 | §9.1 contract_version changelog comment | RESTORE-PARTIAL (reword) | Reword: drop instance-level/"replaces exclusion" clause, keep EV-1/EV-2 note |
| H6 | @@ -798,7 +807,7 | branch 810 | §9.2 `merge_method` EV-2 legal-values note | **RETAIN-BRANCH (EV-2)** | KEEP — must NOT revert |
| H7 | @@ -855,7 +864,7 | branch 873 | §9.x "Contract version is v1.7.0" footnote sentence | RESTORE-MASTER | Restore master's plain sentence |
| H8 | @@ -907,9 +916,6 | branch ~916 (3 deleted) | §9.3 telemetry block (3 executor_* fields) | RESTORE-MASTER | Re-add the 3 deleted telemetry fields |
| H9 | @@ -1208,7 +1214,7 | branch 1217 | §11.3 partition rule (three-way → two-way rewrite) | RESTORE-MASTER | Restore master three-way-partition paragraph |
| H10 | @@ -1423,7 +1429,7 | branch ~1435 | §13 fallback table `merged_output_path` row | RESTORE-MASTER (judgment) | Restore master "FAIL Wave 4" row (see §2.6 caveat) |
| H11 | @@ -1709,9 +1715,7 | branch ~1736 | metrics.json `ensemble` block (2 fields deleted) + `adversarial.merge_method` EV-2 (1 line) | MIXED — see §2.7 | RESTORE the 2 metrics fields; RETAIN the EV-2 metrics comment |
| H12 | @@ -1908,7 +1912,7 | branch 1915 | §12 eval-matrix Adversarial-delegation row | **RETAIN-BRANCH (§12 detector)** | KEEP branch `file_present + card_count` — must NOT revert |

> Note: H11 and H12 fall in one diff region each; H11 spans two logically distinct edits (one RESTORE, one RETAIN) inside the same hunk — must be split at Edit time.

---

## 2. RESTORE-MASTER hunks — exact master content to put back

All master line numbers from `git show origin/master:src/superclaude/skills/sc-reflect-protocol/SKILL.md`.
All branch line numbers from the working-tree file (current HEAD).

### 2.1 H1 — Input-resolution `--executor-model` line (DELETE-ONLY)

- **Branch line 89** (ADDED by #197):
  > `- \`--executor-model <class>\` (back-compat / CLI flag) is ACCEPTED and IGNORED. Reflect does NOT class-exclude (instance-level independence, see the §7.1 instance-level independence guarantee): the named class stays in the reviewer pool, no tier degrade occurs, and no \`executor_exclusion_degraded\` signal is emitted. The flag is recorded provenance only.`
- **Master:** confirmed `grep -- "--executor-model"` over master input-resolution (lines 84–92) returns **nothing**; the only master `--executor-model` mentions are inside the §7.1 rule prose (master 620, 622). Master input-resolution section ends with `--promote-resume` then `(See refs/input-resolution.md ...)`.
- **Surgery:** **DELETE branch line 89 entirely** (plus its now-leftover state). Do NOT try to "restore master" — there is no master line here. This is the one hunk where the revert is a pure deletion.

### 2.2 H2 — §7.1 reviewer composition (the core rewrite)

- **Branch (current):** lines **621, 627, 637** carry the instance-level guarantee + class-diversity-preference rewrite; the rotation table header at branch 631 reads `Model rotation (class-diversity-preferring)`.
- **Master content to restore** (master lines **620–632**), verbatim, three paragraphs + table-header + post-removal sentence:
  - Master **620**: `**Executor-class exclusion rule (anti-self-confirmation, structural).** The *executor* (the agent whose work is under review) MUST NOT appear in the reviewer pool. Reflect resolves the executor's model class at Wave 0 step 0.5b ... emit \`executor_class_source: flag | env | log-heuristic | unknown\` to telemetry). When the executor's class is in the candidate rotation, it is **removed** ... reflect emits \`executor_exclusion_degraded: true\` and degrades to T1 with WARN: \`"executor class collides with reviewer pool; N=2 floor cannot be satisfied with disjoint set."\` This rule extends the §11.3 disjoint-set principle ... the three classes (executor, reviewers, calibrator) form a partition ...`
  - Master **622**: `When \`executor_class_source == unknown\` ... emits \`executor_class_resolved: false\` + WARN: \`"executor class not resolved — anti-self-confirmation guarantee weakened; pass --executor-model to enforce."\` This is fail-open by design ...`
  - Master table header **626**: `| Reviewer count | Model rotation (BEFORE executor-class removal) | Persona rotation |` (the 3 data rows 627–629 are IDENTICAL on both sides — no change needed).
  - Master **630**: `Post-removal: if the executor is \`sonnet\`, the N=3 default rotation becomes \`haiku, (qwen|kimi|deepseek|opus)\` and reflect adds the next-available class ... or degrades to N=2 if no replacement is available. The N=2 minimum is hard — below it, T2 cannot fire.`
  - Master **632** ("The merge judge in Wave 4 is ...Khan et al...") is IDENTICAL on both sides — keep.
- **Branch block to remove** = branch 621 (instance-level guarantee + 1/2/3 list at 623–625) + 627 (executor-class-never-removed para) + the new `**Class-diversity preference**` paragraph + table-header branch 631 (`class-diversity-preferring`) + branch 637 (`The rotation is filled to prefer distinct classes ...`).
- The branch ALSO inserts a numbered list (1. Fresh subagent spawn / 2. No formation context / 3. Blind calibration) and the `t2_model_class_diversity: full | degraded` "diversity preference" prose — all #197 net-new, all REMOVED by this revert.

### 2.3 H7 — §9.x "Contract version is v1.7.0" footnote sentence

- **Branch line 873:** `Each flag has a one-line semantics description in \`refs/report-template.md\`. Contract version is \`v1.7.0\` (runtime/semantic hardening through 1.5.1 -- instance-level anti-self-confirmation §7.1, EV-1 Wave-4 merge gate, EV-2 merge_method guard -- and additive reachability fields 1.7.0).`
- **Master line 862:** `Each flag has a one-line semantics description in \`refs/report-template.md\`. Contract version is \`v1.7.0\`.`
- **Surgery decision:** Per the plan, EV value is retained, so the master plain sentence may be restored OR a trimmed variant kept. RECOMMENDED: restore master's plain sentence (`... Contract version is \`v1.7.0\`.`) to drop the "instance-level anti-self-confirmation §7.1" claim. (The EV-1/EV-2 facts still live verbatim at their own §8/§9.2 sites, so no information is lost.) Tasklist should specify the master form as the target to keep the revert unambiguous.

### 2.4 H8 — §9.3 telemetry block (3 deleted executor_* fields)

- **Branch (current ~line 916):** the three fields are GONE; branch shows `fallback_path: null | F1 | F2 | F3` immediately followed by `citations_dropped_extrapolated:`.
- **Master lines 910–912** to re-insert (verbatim), between `fallback_path:` (master 909) and `citations_dropped_extrapolated:` (master 913):
  ```
  executor_class_source: flag | env | log-heuristic | unknown
  executor_class_resolved: bool                                  # false → §7.1 anti-self-confirmation WARN emitted
  executor_exclusion_degraded: bool                              # true when executor class collision dropped reviewer count below N=2 → T1 fallback
  ```

### 2.5 H9 — §11.3 partition rule

- **Branch line 1217:** `**Calibrator/reviewer disjoint-set (two-way).** The disjoint-set principle separates the calibrator class from the reviewer classes ONLY ... The executor class is deliberately NOT separated ... so no executor-class exclusion is applied and no \`executor_class ∉ reviewer_classes\` assertion is graded ...`
- **Master line 1211** to restore (verbatim):
  > `**Three-way partition (executor / reviewers / calibrator).** The disjoint-set principle is extended from "calibrator ≠ reviewers" to a three-way partition: \`executor_class\`, \`reviewer_classes\`, and \`calibrator_class\` SHOULD be pairwise disjoint. §7.1's executor-class exclusion rule enforces \`executor_class ∉ reviewer_classes\` at Wave 3A reviewer composition; §11.3 enforces \`calibrator_class ∉ reviewer_classes\` at Wave 1D/3C. When all three pools cannot be made pairwise disjoint, the partition degrades and the affected pool emits its \`*_diversity: degraded\` telemetry. The grader assertion \`executor_model_class NOT IN reviewer_model_classes\` is asserted whenever \`executor_class_resolved == true\`.`

### 2.6 H10 — §13 fallback table `merged_output_path` row (JUDGMENT CALL)

- **Branch (current ~1435):** `| \`merged_output_path\` from sc-adversarial does not exist on disk | EV-1 MALFORMED at Wave 4 (missing-file guard before status routing): bounded remediate, do NOT halt-and-end | F2 |`
- **Master line 1426:** `| \`merged_output_path\` from sc-adversarial does not exist on disk | FAIL Wave 4 (missing-file guard before status routing) | F2 |`
- **Caveat for tasklist:** the branch row was reworded to REFERENCE EV-1 ("EV-1 MALFORMED ... bounded remediate, do NOT halt-and-end"). Restoring master's plain `FAIL Wave 4` row makes the table CONSISTENT with the EV-1 STOP that we are RETAINING — but it removes the explicit cross-reference to EV-1's bounded-remediate semantics. RECOMMENDED: restore master's plain `FAIL Wave 4` row (the EV-1 §8 STOP paragraph itself already owns the bounded-remediate semantics; the table cell only needs to be non-contradictory). Tasklist should call this out as a deliberate choice, not silent drift. (Lowest-risk alternative: leave the branch wording — it is not instance-level and does not contradict the retained EV-1; but it is #197-introduced prose, so the cleaner revert restores master.)

### 2.7 H11 — metrics.json block (MIXED: split required)

This single diff hunk contains TWO independent edits:

**(a) RESTORE — `ensemble` block dropped 2 fields.**
- **Branch (current ~1736):** ensemble block ends `"reviewer_count": <int>` then `},`.
- **Master lines 1713–1714** to re-add after `"reviewer_count": <int>,`:
  ```
      "executor_class_resolved": <bool>,
      "executor_exclusion_degraded": <bool>
  ```
  (master form: `reviewer_count` gets a trailing comma; the two added lines close the block).

**(b) RETAIN (EV-2) — `adversarial.merge_method` comment.**
- **Branch line 1738:** `"merge_method": "adversarial | single-reviewer-fallback",   // [EV-2] LEGAL VALUES ARE EXACTLY {adversarial, single-reviewer-fallback}; any other (inline, convergence-inline, in-context "convergence") is MALFORMED -> reject; non-adversarial merge legal ONLY via F2/F3 fallback; reflect MUST NOT synthesize its own merge`
- **Master line 1738:** `"merge_method": "adversarial | single-reviewer-fallback",` (no EV-2 comment).
- **Surgery:** KEEP the branch EV-2 comment. Do NOT revert this line.

---

## 3. RETAIN-BRANCH hunks — EV value that MUST NOT be reverted

### 3.1 EV-1 — §8 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK STOP (H4)

- **Branch line 688** (and the blank line 687 that precedes it). Net-new; master §8 (master 681–690) has NO Wave-4 STOP paragraph at all (verified — master goes straight from the null-convergence-routing bullets into `---` / `## 9.`).
- Carries: `merged-verdict.yaml`, `merge_method: adversarial`, reviewer-cards `>= --reviewers` (min 2 N=2 floor), the loud-fallback `adversarial_unavailable: true` corroboration, MALFORMED-state bounded-remediate semantics.
- **MUST NOT REVERT.**

### 3.2 EV-2 — §9.2 `merge_method` legal-values note (H6)

- **Branch line 810:** `merge_method: adversarial | single-reviewer-fallback   # F2 path. [EV-2] LEGAL VALUES ARE EXACTLY {adversarial, single-reviewer-fallback}: any other value (inline, convergence-inline, an in-context "convergence" of the cards) is MALFORMED -> reject. A non-adversarial merge is legal ONLY via the F2/F3 fallback ... Reflect MUST NOT synthesize its own merge.`
- Master line 807 has only `merge_method: adversarial | single-reviewer-fallback   # F2 path`.
- **MUST NOT REVERT.** (metrics.json mirror at branch 1738 = §2.7(b), also retained.)

### 3.3 EV / §12 — eval-matrix `file_present + card_count` detector (H12)

- **Branch line 1915:** `| Adversarial delegation artifacts | \`file_present + card_count\` | \`<output>/adversarial/merged-verdict.yaml\` present with \`merge_method: adversarial\` AND \`<output>/reviewer-cards/\` count \`>= --reviewers\` (min 2, the §7.1 N=2 T2 floor) |`
- Master line 1911: `| Adversarial delegation artifacts | \`dir_count\` | \`<output>/adversarial/ min_files=6\` |`
- **MUST NOT REVERT.** The branch detector is the testability-map belt-and-suspenders companion to EV-1 (EV-1 §8 STOP explicitly references "The §12 eval-matrix detector ... stays as belt-and-suspenders"). Reverting to master's `dir_count min_files=6` would orphan the EV-1 STOP's cross-reference and re-introduce the brittle raw-count threshold EV-1 deliberately replaced.

### 3.4 §7.1 note on the master N=2 floor reference

EV-1, EV-2, and §12 all cite "the §7.1 N=2 T2 floor". After H2 restores master's §7.1, the N=2 floor STILL exists in master prose (master 630: "The N=2 minimum is hard — below it, T2 cannot fire") — so the EV cross-references remain valid. **No conflict.** This is the key reason the revert is safe: master's §7.1 retains the N=2 floor that the EV hunks depend on.

### 3.5 H3 — §8 `--compare` card path naming (RETAIN, clarification)

- **Branch line 671:** `--compare <output>/reviewer-cards/reviewer-1-card.yaml,reviewer-2-card.yaml,reviewer-3-card.yaml`
- Master 664: `--compare <output>/reviewer-cards/card-1.md,card-2.md,card-3.md`
- This is a #197 naming change (`card-N.md` → `reviewer-N-card.yaml`). It is NOT instance-level and the `reviewer-N-card.yaml` naming is what EV-1 §8 STOP + §12 detector REFERENCE ("one card per reviewer", "reviewer-cards/" count). **RETAIN branch** for internal consistency with the EV hunks. (Tasklist note: reverting this to `card-N.md` would create a naming mismatch against the retained EV-1/§12 reviewer-card expectations — do NOT revert.)

---

## 4. Changelog line to reword (H5) — verbatim + draft replacement

**EXACT line to reword — branch line 699:**

```
contract_version: "1.7.0"   # 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics; 1.5.1: instance-level anti-self-confirmation (§7.1) replaces executor-class exclusion (removed NON-STABLE telemetry executor_class_source / executor_class_resolved / executor_exclusion_degraded -- no §9.3 consumer reads them, so non-breaking) AND adds EV-1 (Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate) + EV-2 (merge_method legal-values guard), both runtime/semantic with no stable-field change; 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields); 1.7.0 (FR-RH1) ADDITIVE ONLY: +reachability_* fields
```

**Master line 699 (for reference — what #197 expanded FROM):**

```
contract_version: "1.7.0"   # 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics; 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields); 1.7.0 (FR-RH1) ADDITIVE ONLY: +reachability_* fields
```

**DRAFT reworded replacement (per the plan: keep `contract_version: "1.7.0"`; DROP the instance-level/"replaces executor-class exclusion" clause + the "removed telemetry" claim, since that telemetry is being RESTORED by H8/H11(a); KEEP only an EV-1/EV-2 runtime-hardening note):**

```
contract_version: "1.7.0"   # 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics; 1.7.x runtime/semantic hardening: EV-1 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate + EV-2 merge_method legal-values guard (no stable-field change); 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields); 1.7.0 (FR-RH1) ADDITIVE ONLY: +reachability_* fields
```

**Rationale for dropping the "removed ... telemetry" clause:** the branch changelog asserts `executor_class_source / executor_class_resolved / executor_exclusion_degraded` were REMOVED. After H8 + H11(a) restore those exact fields, that clause would be FALSE. The reworded line must NOT claim a removal that the revert un-does. Keep only the EV-1/EV-2 note (those genuinely ARE retained and ARE net-new vs master).

---

## 5. Post-surgery validation greps (for the tasklist) + EXPECTED results

Run from worktree root against `src/superclaude/skills/sc-reflect-protocol/SKILL.md`.

| # | Grep | Expected POST-surgery |
|---|------|------------------------|
| V1 | `grep -n "executor_exclusion_degraded\|executor_class_source\|executor_class_resolved" <file>` | **PRESENT as real telemetry** — expect hits at §7.1 (restored 620, 622, 630-area), §9.3 (restored 3 fields), §11.3 (restored grader assertion), metrics.json (restored 2 fields). Master had **8** such hits; branch-now has only changelog-prose hits. Target ≈ master's 8 (give or take the reworded changelog line, which after rewording should contain **0** of these tokens). KEY ASSERTION: more than just the changelog mention — the §9.3 raw fields + §7.1 rule text must be back. |
| V2 | `grep -n "ORCHESTRATOR-VERIFIES-ON-DISK\|merge_method legal\|merged-verdict.yaml" <file>` | **EV-1/EV-2 PRESENT** — expect EV-1 §8 (688), §12 detector (1915), EV-1 §8 STOP also names `merged-verdict.yaml`; EV-2 uses "LEGAL VALUES" (note: the literal string "merge_method legal" may not match — EV-2 says "merge_method legal-values guard" in changelog after rewording + "LEGAL VALUES" in §9.2; recommend the grep be `ORCHESTRATOR-VERIFIES-ON-DISK\|LEGAL VALUES ARE EXACTLY\|merged-verdict.yaml` for a reliable non-zero hit). Must be NON-ZERO. |
| V3 | `grep -n 'contract_version: "1.7.0"' <file>` | **PRESENT** (branch 699 + §9.1 header 696 + reachability refs). `contract_version` string itself unchanged by the revert. |
| V4 (negative) | `grep -n "instance-level independence guarantee\|class-diversity-preferring\|Class-diversity preference (prefer, never require)" <file>` | **ZERO hits** — the #197 instance-level prose is fully reverted. |
| V5 (negative) | `grep -n "replaces executor-class exclusion\|instance-level anti-self-confirmation" <file>` | **ZERO hits** — changelog reworded; no "replaces exclusion" claim remains. |
| V6 (line count) | `wc -l <file>` | **> 1989** (master count) and **< 1993** (current branch). The revert deletes more instance-level prose than the EV additions it keeps; exact target depends on rewrap, so assert the inequality, not an exact number. Do NOT assert == 1989 (that would mean EV got deleted). |

> Tasklist authoring note for V2: the spec's literal `merge_method legal` substring does NOT appear verbatim in §9.2 (which says "LEGAL VALUES ARE EXACTLY"); it only appears in the reworded changelog ("EV-2 merge_method legal-values guard"). Use the broadened alternation above so V2 cannot false-negative.

---

## 6. Summary for Step 3 author

- **9 RESTORE-MASTER edits** (H1 delete-only, H2, H5 reword, H7, H8, H9, H10 judgment, H11(a)) + **4 RETAIN-BRANCH** (H3, H4=EV-1, H6=EV-2, H11(b), H12=§12). H11 must be SPLIT.
- **Forbidden:** whole-file `git checkout origin/master --`. Hunk-level `Edit` only.
- **Safe because:** master's restored §7.1 keeps the `N=2` floor that EV-1/EV-2/§12 cross-reference; the EV hunks live in §8 / §9.2 / §9.3-metrics / §12 — disjoint from the §7.1 / telemetry / §11.3 sections being reverted, so the two operations do not collide except in the changelog line (H5), handled by rewording.
- **Subtle traps:** (1) H1 has no master counterpart — pure delete; (2) the changelog "removed telemetry" claim becomes false after restore — must be dropped, not preserved; (3) reviewer-card naming (H3) and §12 detector (H12) and fallback-table row (H10) all reference each other — keep EV-side naming consistent, restore only H10 to master plain text; (4) V2 literal substring footgun (use broadened grep).
