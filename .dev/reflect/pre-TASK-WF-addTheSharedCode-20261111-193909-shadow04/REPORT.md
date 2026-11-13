# Reflect REPORT — UC-1 pre-execution coverage audit (shadow04)

```yaml
contract_version: 1.8.0
status: partial                        # 1 dropped citation (Makefile mis-point in MF-2), fixed at validation per §11.2
mode: pre
tier_reached: 2
confidence_calibrated: 0.83
citations_total: 19
citations_revalidated: 19
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Run: `pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04` (2026-11-13). Spec: 1-line source.md. Tasklist: 11 tasks. Tier pinned by `--tier 2`; engine `shadow` (panel ran offline for measurement; legacy rotation authoritative). Engine aliases: 3 distinct classes (full diversity), single vendor (warn-only). Executor class: unknown (UC-1, future work; anti-self-confirmation guarantee noted as weakened for this reason only).

## Coverage

- Pass 1 parsed requirement IDs: **0** (the spec carries no labeled IDs).
- Pass 2 inferred rows: **3**, all matched → `coverage_pct: null` (0/0 parsed), `coverage_pct_union: 1.0`, `unmapped_requirements: []`, `unmapped_requirements_union: []`, `S_dev_density` (union): 0.0.
- `coverage_degraded: parsed-sparse` (inferred 3 > parsed 0): Tier-1 stop was forbidden; Tier 2 ran (consistent with the explicit pin).
- Structural signals: S_scope 11 tasks, S_domains 2, no regression candidates (UC-1).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote (source.md:1) | Citation | Match result |
|--------|------------------------------|----------|--------------|
| INF-001 | "Add the shared codegraph rule (use codegraph only when the caller passes index_state: fresh with checked_at, worktree_root and projectPath; otherwise Grep/Glob/Read)" | source.md:1 | covered — Constraints:19 + Tasks 1-10 |
| INF-002 | "to the ten general-purpose agent files listed in .dev/issues/504/issue-summary.md" | source.md:1 | covered — Tasks 1-10 enumerate the exact ten files; list cross-verified outside the grounding root against issue-summary.md:24 (main checkout; the folder is absent from this worktree) |
| INF-003 | "following the wording in troubleshoot-analyst.md, reflect-reviewer.md, reuse-auditor.md and auggie-reviewer.md" | source.md:1 | covered-with-finding — the four files do NOT carry the mandated wording (MF-1) |

## Merged Tier-2 findings (adversarial merge, convergence 1.0)

Plain UC-1 plan-fidelity findings; no UC-2 deviation classes apply (unanimous 3-advocate debate; a false Drift label could trigger headless AUTO-FIX remediation).

### MF-1 (MEDIUM) — False wording attribution in Constraints

- **Location:** TASK-WF-addTheSharedCode-20261111-193909.md:19
- **Mapped tasklist item:** Constraints (drives Tasks 1-10)
- **Spec section:** source.md:1 (wording clause)
- **Evidence:** All four cited agents gate codegraph on `index_state: fresh` + `projectPath` only; none carries `checked_at`, `worktree_root`, "callees and impact", or "say so in your reply" (troubleshoot-analyst.md:27; reflect-reviewer.md:64; reuse-auditor.md:50; auggie-reviewer.md:79). The composed sentence is a new, stricter rule whose inclusion matches the spec's parenthetical; its attribution to the four files is false. Three of four reference agents also carry an explicit returns-nothing fallback the composed sentence omits; 14 agent files now hold two freshness-gate families under one "shared" label. Severity rests on false provenance in the exact sentence pasted into ten files, not on behavioral loss: the rule's own reference target preserves the effective fallback by reference (CODEGRAPH.md:32-76: continue on the native floor when a lookup fails or returns nothing; never read empty results as absence).
- **Classification rationale:** plan-fidelity finding (UC-1); attribution-vs-inclusion distinction from the qa reviewer; fallback count and severity rationale corrected by the Round-2.5 invariant probe (INV-002/003/006).
- **Default remediation:** Rewrite the Constraints sentence to state the rule is newly composed per the spec's field list, in the spirit of the four agents' wording — or paste one of the four agents' actual sentences and add the three fields as a delta.

### MF-2 (LOW) — Acceptance criteria cannot enforce the rule they gate

- **Location:** TASK-WF-addTheSharedCode-20261111-193909.md:31 (repeated at :38,45,52,59,66,73,80,87,94); Task 11 at :102,:105
- **Mapped tasklist item:** Tasks 1-10 ACs; Task 11
- **Spec section:** source.md:1 (three required fields)
- **Evidence:** The ACs check grep counts plus diff shape and absence of a tools line — real constraints, but no exact-text assertion: text missing `checked_at`/`worktree_root`/the fallback sentence still passes. `make verify-sync` (Makefile:166, diff-based, exits 1 on drift) compares src to .claude mirrors — populated by `make sync-dev` (Makefile:126-130) — not to the Constraints sentence. Task 11's "find the agent-file tests with grep" leaves the pass condition to the executor's choice of tests. [Citation note: the original draft cited Makefile:126-130 for the verify-sync claim; the evidence-validator dropped that citation (the range shows sync-dev) and it was repointed to Makefile:166 at validation.]
- **Default remediation:** Add `grep -F "<the Constraints sentence>" <file>` (or floor checks `grep -c checked_at`/`grep -c worktree_root` ≥ 1) to each AC, and name the agent-file tests in Task 11.

### MF-3 (LOW) — Spec self-contradiction resolved silently

- **Location:** source.md:1 vs TASK-WF-addTheSharedCode-20261111-193909.md:19
- **Mapped tasklist item:** Constraints
- **Evidence:** The spec demands both "following the wording in [four agents]" and the three fields those agents lack. The tasklist adopts the stricter reading without recording the choice; MF-1 is the symptom, this is the cause.
- **Default remediation:** Add one Constraints line recording the resolution (spec fields win; four-agents wording is directional).

### MF-4 (LOW) — Placement instruction looser than the files

- **Location:** TASK-WF-addTheSharedCode-20261111-193909.md:28 (pattern for Tasks 1-8, 10)
- **Mapped tasklist item:** Tasks 1-8, 10
- **Evidence:** Every `## Key Actions` list is numbered with bold labels (system-architect.md:30-35); "one bullet" left the number and the "**Use Codegraph Safely**" label to the executor, and no AC can distinguish a correct item from a stray bullet. The sanctioned variants are correct: self-review's own list style (self-review.md:36; plan:82-94) and technical-writer's code-fact-only scope (technical-writer.md:35; plan:89-94).
- **Default remediation:** Change "one bullet" to "one numbered item in the section's existing bold-label style" while editing the ACs (MF-2).

### ADV-1 (advisory, non-finding) — Plugin mirror divergence, pre-existing

plugins/superclaude/agents/ holds 22 tracked files (21 agent .md files plus `__init__.py`), including copies of all ten targets with zero `index_state` (plugins/superclaude/agents/system-architect.md:30-35); no make target syncs them; `make build-plugin` ships that folder verbatim into dist (scripts/build_superclaude_plugin.py:74-77). The spec never names plugins/, and the four reference agents are absent from the mirror entirely, so the gap predates this plan. Action for the operator: decide whether the mirror must track src/superclaude/agents/; if yes, a separate task adds the rule there.

## Reviewer ensemble (Tier 2)

3 heterogeneous reviewers (sonnet/analyzer, haiku/qa, opus/refactorer), all blind-calibrated (card confidences 0.56/0.58/0.61; per-finding calibrations 0.45-0.92). Identity note: the haiku-slot reviewer self-reported a non-Anthropic model; recorded as `identity_mismatch_suspected` (requested-pinned identity source; not asserted). Merge: adversarial Mode A, convergence 1.0 after Round 2; Round-2.5 invariant probe 0 HIGH-unaddressed, 1 MEDIUM correction applied (severity rationale of MF-1). Judge: inline orchestrator (sonnet class — collision with reviewer-1 recorded in panel/notes.md).

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 19` = 0.00

## Recommendations

### Recommendation R-001: Correct the wording-attribution sentence

- **File:** .dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md (Constraints, line 19) — or the successor tasklist if this work is re-planned
- **Change:** Replace "It is the wording of the rule in src/.../reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md" with an accurate statement (newly composed per the spec's field list, in the spirit of those agents' wording).
- **Verifier:** Re-read line 19; `grep -c "It is the wording"` returns 0.
- **Linked finding(s):** MF-1, MF-3
- **Priority:** P1

### Recommendation R-002: Add exact-text assertions to Tasks 1-10 ACs

- **File:** same tasklist, AC lines 31-94
- **Change:** Append to each AC: `grep -F "<Constraints sentence>" <agent file>` succeeds (or `grep -c checked_at` and `grep -c worktree_root` each ≥ 1).
- **Verifier:** Run the grep for one representative file (src/superclaude/agents/system-architect.md) and observe exit 0.
- **Linked finding(s):** MF-2
- **Priority:** P1

### Recommendation R-003: Name the agent-file tests in Task 11

- **File:** same tasklist, line 102
- **Change:** Replace "find them with grep under tests/" with the concrete test paths (e.g. the tests covering agent-file sync/content).
- **Verifier:** The named paths exist (`ls` exit 0).
- **Linked finding(s):** MF-2
- **Priority:** P2

### Recommendation R-004: Fix the placement wording

- **File:** same tasklist, line 28 and siblings
- **Change:** "one bullet" → "one numbered item in the existing bold-label style" (label suggested: **Use Codegraph Safely**).
- **Verifier:** Re-read the line; grep for "one bullet" returns 0.
- **Linked finding(s):** MF-4
- **Priority:** P2

### Recommendation R-005: Decide the plugin-mirror policy

- **File:** n/a (cross-cutting decision)
- **Change:** Decide whether plugins/superclaude/agents/ must mirror src/superclaude/agents/; if yes, open a follow-up task to add the rule to the ten mirror copies (and the four reference agents' copies, absent today).
- **Verifier:** A recorded decision; if "yes", `grep -rln index_state plugins/superclaude/agents/ | wc -l` ≥ 10 after the follow-up.
- **Linked finding(s):** ADV-1
- **Priority:** P2

## Grounding Gaps (dropped citations, §11.2)

### Dropped citation C-17

- **Citation:** Makefile:126-130 (as originally cited in MF-2)
- **Original claim text:** "`make verify-sync` compares src to .claude mirrors, not to the Constraints sentence (Makefile:126-130)"
- **Why dropped:** the cited range shows the `sync-dev` copy loop, not `verify-sync`; the claim's supporting target is Makefile:166 (verify-sync, diff-based, exits 1 on drift).
- **Resolution applied:** citation repointed to Makefile:166 in MF-2 (verified by the evidence-validator); `status: partial` retained per the §11.2 mechanical rule (the shipped draft carried one unfounded citation).
