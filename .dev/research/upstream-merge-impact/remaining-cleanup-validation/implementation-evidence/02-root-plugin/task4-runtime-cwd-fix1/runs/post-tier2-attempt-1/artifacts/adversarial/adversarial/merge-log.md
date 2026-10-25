# Merge Execution Log

## Metadata
- Base: Variant 2 (haiku:qa, reviewer-2), `variant-2-original.md`. Force-selected under BLOCKED_BY_INVARIANTS (INV-006).
- Grafted source: Variant 1 (sonnet:analyzer), `variant-1-original.md`. Only the cited lines were read: V1:1-27 (covers V1:6-9 and V1:22-26) and V1:78-96 (covers V1:80, V1:82, V1:91, V1:93-96).
- Plan: `refactor-plan.md` (13 changes, G-1..G-5, threshold table, changes-not-made). Auto-approved 2026-10-25T00:00:00Z.
- Executor: sc:merge-executor agent
- Output: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/adversarial/merged-card.yaml`
- Changes applied: 13 of 13 planned
- Status: success
- Timestamp: 2026-10-25T14:35:43Z
- INV-006 note: Change 1 carries the INV-006 correction. Per the plan, INV-006 stays UNADDRESSED in the return contract because the debate did not adjudicate it. The executor did not change that status.

## Global constraints
- G-1 Shape: applied. The card has the 10 base top-level keys in base order and no added keys. `needs_human_decision` and the deviation counts appear only in list text and comments.
- G-2 Provenance: applied. The header block has the four mandated lines, filled in with the merge date and the S path. Two extra comment lines follow it. One says the card is merged from reviewers 1 and 2 (required by G-4). The other carries the base's two orchestrator `#` comment lines verbatim. There are 28 requirement-level `# Source: ...; Anchor: ...; Disposition: ...` tags: findings 1, grounding_gaps 3, agreements 7, disagreements 2, risks 6, recommendations 5, verdict fields 3, self_reported_confidence 1.
- G-3 Concrete-over-generic: applied. See the dropped-anchor audit below.
- G-4 Identity: `reviewer: 2`, `persona: qa`, `self_reported_confidence: 0.8` are kept. A comment says the confidence is self-reported and not calibrated (V1 0.90, V2 0.92).
- G-5: Only merged-card.yaml and this merge-log.md were written. No variant, plan, snapshot, audit-root or plugin file was modified. `attempt-1-interrupted/` was not read.

## Changes Applied

### Change 1: Replace the pytest verifier with the full exit-code mapping (V1:91, corrected per INV-006)
- **Status**: Applied
- **Source**: Variant 1 recommendations[1].verifier (V1:91); deviation-taxonomy.md:105-113; INV-006, INV-014
- **Target**: Base recommendations[1] (V2:47-50), `change` and `verifier`. `file: "tests/test_greeting.py"` and `priority: high` are kept.
- **Before**: The change said to run both pytest commands and, if plain pytest failed to collect, add src/__init__.py or a pythonpath config. The verifier was "Both commands exit 0 with 2 passed ... do not treat execution.log:5 as a run."
- **After**: The change is the plan's text verbatim: a user action, invocation preferred over adding files, and any added file named as an unmapped-hunk Drift signal (deviation-taxonomy.md:62). The verifier is the plan's text verbatim, plus the plan-permitted detail "(expected success detail: 2 passed)" on the exit-0 case. It covers exit codes 0, 1 (Regression only if tests were collected, ran, and an assertion failed), retry/flaky (:112), 2/3 (:108), 5 (:109), 124 (:111), other (:113), the case where the two invocations disagree, "clears G2 only", and execution.log:5.
- **Provenance tag**: `# Source: Base (original, modified) — Change #1, with Variant 1 (sonnet:analyzer) V1:91 — Change #1; Anchor: recommendations[1] (V2:47-50), exit codes 0/1/2/3/5/124, "2 passed", INV-006, INV-014; Disposition: merged-from-multiple ...; Decision basis: INV-006 / INV-014`
- **Validation**: Structural integrity ✅ | References ✅ (recommendations[1] exists; G1/G2/G3 exist) | Contradictions ✅

### Change 2: Add the no-Drift-signal basis to the no-deviation agreement (V1:6-9, V1:22-26; INV-011)
- **Status**: Applied
- **Source**: Variant 1 V1:6-9, V1:22-26; INV-011
- **Target**: Base agreements_with_t1[0] (V2:26), appended
- **Before**: No 4-class deviation; one hunk (changes.patch:5-9); unmapped_hunks empty (task-diff-map.yaml:29); precedence :89-97 does not fire.
- **After**: The base text is kept verbatim, followed by the plan sentence: no run (task-diff-map.yaml:38), unmapped_hunks: [], none of the Drift signals at deviation-taxonomy.md:62/:65/:67/:109 fire. It says "signals", not "definition" (INV-011).
- **Provenance tag**: `# Source: Base (original, modified) — Change #2, with Variant 1 (sonnet:analyzer) V1:6-9, V1:22-26 reasoning; Anchor: agreements_with_t1[0] (V2:26), INV-011; Disposition: merged-from-multiple; Decision basis: S-001 / INV-011`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 3: Correct the diff-regeneration recommendation (C-009, A-002, INV-001, INV-015, INV-017a)
- **Status**: Applied
- **Source**: Debate consensus C-009, A-002; INV-001, INV-015, INV-017(a)
- **Target**: Base recommendations[0] (V2:43-46): `file`, `change`, `verifier`. `priority: high` is kept.
- **Before**: `file: "changes.patch"`; change "Regenerate the diff so tests/test_greeting.py:1-13 is a hunk, not only src/greeting.py."; verifier "Patch contains a tests/test_greeting.py hunk whose body matches tests/test_greeting.py:1-13; G1 can close."
- **After**: `file` is the absolute audit-root changes.patch path (from task-diff-map.yaml:3). The change and verifier are the plan's texts verbatim: one patch covering both files, scope widened beyond `--scope src/` (task-diff-map.yaml:27), the snapshot is read-only, H1 preserved (git-inventory.txt:2-9). The verifier checks that H1 still maps to T-101/T-102 and that a new hunk maps to T-103 (task-diff-map.yaml:26). G1 can then close; R-003 execution still needs the Change 1 run.
- **Provenance tag**: `# Source: Base (original, modified) — Change #3; Anchor: recommendations[0] (V2:43-46), C-009, A-002, INV-001, INV-015, INV-017(a); Disposition: modified ...`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: The verifier text says "the Change 1 run". That is a plan-internal reference and is reproduced verbatim as the plan specified. In the card it refers to the run in recommendations[1].

### Change 4: G1 scope note, owner unchanged (A-002, INV-005)
- **Status**: Applied
- **Source**: A-002; INV-005
- **Target**: Base grounding_gaps[0] (V2:7-12)
- **Before**: why_not_classifiable ended at "...would be a guess." next_evidence_needed started "A changes.patch hunk for tests/test_greeting.py covering the same 13 lines..."
- **After**: why_not_classifiable has the plan's scope sentence (task-diff-map.yaml:27) appended. next_evidence_needed is the plan's prefix "A regenerated diff with the scope widened beyond src/ (see recommendations[0]) containing" followed by the base text verbatim. The only edit is lower-casing the base's opening article "A" to "a" so the prefix reads as one sentence. `hunk_ref`, `evidence_missing`, `owner: user` and `decision_needed_by_user: true` are verbatim. No `orchestrator` owner was emitted.
- **Provenance tag**: `# G1. Source: Base (original, modified) — Change #4; Anchor: grounding_gaps[0] (V2:7-12), A-002, INV-005; Disposition: modified ...; Decision basis: A-002 / INV-005`
- **Validation**: Structural integrity ✅ | References ✅ (recommendations[0] resolves to the changes.patch rec) | Contradictions ✅

### Change 5: G2 absence evidence cites the audit-root inventory (A-001, INV-003)
- **Status**: Applied
- **Source**: A-001; INV-003
- **Target**: Base grounding_gaps[1].evidence_missing (V2:14), appended
- **Before**: The absence of a package marker was evidenced by the snapshot glob, task-diff-map.yaml:38 and execution.log:5.
- **After**: The base text is verbatim, followed by the plan sentences (git-inventory.txt:2-8 shows no package marker or config; the snapshot is not a complete mirror because proposed.md, git-inventory.txt:5, is missing). All other G2 fields are verbatim.
- **Provenance tag**: `# G2. Source: Base (original, modified) — Change #5; Anchor: grounding_gaps[1] (V2:13-18), A-001, INV-003; Disposition: modified ...`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: G3 forces partial; decision_needed_by_user: false only marks it as not urgent (INV-004)
- **Status**: Applied
- **Source**: INV-004; C-001/X-002
- **Target**: Base grounding_gaps[2].why_not_classifiable (V2:21), appended
- **Before**: Ended "...so it is not an unmapped Drift hunk."
- **After**: Base text verbatim, then the plan sentences: the row forces partial and needs_human_decision (deviation-taxonomy.md:149-152); false only means not urgent; the correctness-gaps channel needs two sibling symbols (deviation-taxonomy.md:175). `decision_needed_by_user: false` and all other fields are kept.
- **Provenance tag**: `# G3. Source: Base (original, modified) — Change #6; Anchor: grounding_gaps[2] (V2:19-24), INV-004, C-001/X-002; Disposition: modified ...; Decision basis: INV-004`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: completed.md recommendation covers line 8, re-snapshot, G3 exit criterion (INV-002, INV-017c)
- **Status**: Applied
- **Source**: INV-002, INV-017(c); C-006
- **Target**: Base recommendations[2] (V2:51-54): `change`, `verifier`. `file` and `priority: high` are kept.
- **Before**: change "Set frontmatter status to partial until the test hunk is in the diff and a real run is recorded."; verifier "completed.md:2 is done only after those two artifacts exist."
- **After**: Plan texts verbatim. They cover completed.md:2 and completed.md:8 (uncheck T-103), the stale-snapshot warning, and the point that the reflect status stays partial while any gap, including G3, remains (deviation-taxonomy.md:149).
- **Provenance tag**: `# Source: Base (original, modified) — Change #7; Anchor: recommendations[2] (V2:51-54), completed.md:2, completed.md:8, INV-002, INV-017(c), C-006; Disposition: modified ...`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: R-002 spec-clarification recommendation is spec-first, priority low (C-007, INV-016)
- **Status**: Applied
- **Source**: C-007 tie; INV-016; V1:93-96 priority calibration
- **Target**: Base recommendations[3] (V2:55-58): `change`, `verifier`, `priority`. `file: "spec.md"` is kept.
- **Before**: change "State R-002 behavior for None, non-str, and whitespace-only, then align src/greeting.py:2 and add assertions."; verifier "Each stated case has an assertion that passes."; priority medium.
- **After**: Plan texts verbatim: clarify spec.md:9 first, change src/greeting.py:2 only after that, and do not edit before then. The verifier is "spec.md:9 amended; each newly stated case then has a passing assertion." Priority is `low`.
- **Provenance tag**: `# Source: Base (original, modified) — Change #8, priority calibration from Variant 1 (sonnet:analyzer) V1:93-96 — Change #8; Anchor: recommendations[3] (V2:55-58) ...; Disposition: modified (... priority medium -> low); Decision basis: C-007 tie / INV-016`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: proposed.md risk and recommendation rewritten (U-001, A-001)
- **Status**: Applied
- **Source**: V2 advocate R2 concession; V1 advocate R1/R2; the orchestrator verified proposed.md:3-10 (the executor did not re-read it)
- **Target**: Base risks[5] (V2:41) and recommendations[4] (V2:59-62)
- **Before**: risks[5] said proposed.md is not in the snapshot, gave "[INFERRED] it might hold extra task text", and said it was not classified because spec.md:1-12 and completed.md:1-8 were read in full. recommendations[4] said to copy proposed.md in and confirm it adds no MUST beyond spec.md:6/9/12; the verifier allowed "readable in snapshot, or user confirms out of scope".
- **After**: risks[5] is the plan text verbatim. The snapshot hole is kept, and the audit-root copy (proposed.md:3-10) only restates T-101/T-102/T-103. recommendations[4] keeps `file: "proposed.md"` and `priority: low`. Its change is "Include proposed.md in future snapshots so snapshot-absence claims stay sound." and its verifier is "proposed.md is readable inside the snapshot."
- **Provenance tags**: risks[5] `# Source: Base (original, modified) — Change #9; Anchor: risks[5] (V2:41) ...; Disposition: modified ...; Decision basis: U-001 / A-001`; recommendations[4] `# Source: Base (original, modified) — Change #9; Anchor: recommendations[4] (V2:59-62) ...`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: needs_human_decision / zero-deviation-count agreement, as text (INV-017d, INV-012)
- **Status**: Applied
- **Source**: INV-017(d), INV-012; deviation-taxonomy.md:152
- **Target**: Base agreements_with_t1[5] (V2:31), appended
- **Before**: Status done not supported; 2/3 = 0.667 (task-diff-map.yaml:34); non-empty gaps force partial (:149-153).
- **After**: Base text verbatim, then "needs_human_decision is true (deviation-taxonomy.md:152). Deviation counts by class are all zero (authorized 0, necessary 0, drift 0, regression 0). G1-G3 are ordinal labels for the grounding_gaps rows." No keys were added.
- **Provenance tag**: `# Source: Base (original, modified) — Change #10; Anchor: agreements_with_t1[5] (V2:31), threshold 2/3 = 0.667, INV-017(d), INV-012; Disposition: modified ...`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: Verdict comments state the 3-row forcing basis (INV-008)
- **Status**: Applied
- **Source**: INV-008
- **Target**: Base verdict (V2:63-66), comments only
- **Before**: Three verdict values with no comments.
- **After**: Values are verbatim. Inline comments were added exactly as the plan wrote them: on `tasklist_completion_pct: 0.667`, "# 2/3 tasks diff-backed (task-diff-map.yaml:34); completed.md claims 3/3; executed coverage 0/3"; on `status_recommendation: partial`, "# forced by non-empty grounding_gaps (3 rows: G1, G2, G3) per deviation-taxonomy.md:149-152; needs_human_decision: true". V1's "(G1, G2)" comment was NOT carried. Each verdict field also has a preceding provenance tag.
- **Provenance tag**: `# Source: Base (original); Anchor: verdict.<field>; Disposition: preserved-exact (comment added per Change #11; Decision basis: INV-008)`
- **Validation**: Structural integrity ✅ (the parser confirms the comments do not alter the values) | References ✅ | Contradictions ✅

### Change 12: Disagreement list gains the INV-006 caution on T1's verifier shape
- **Status**: Applied
- **Source**: V2 advocate R2; INV-006
- **Target**: Base disagreements_with_t1 (V2:33-34). One entry was appended; the existing entry is verbatim.
- **Before**: One entry (G1 wording).
- **After**: Two entries. The new one is the plan text verbatim (t1-card.md:89 is success-only; classify per deviation-taxonomy.md:105-113; see recommendations[1]).
- **Provenance tag**: `# Source: Base (original, modified) — Change #12 (V2 advocate R2); Anchor: disagreements_with_t1[1] (new), t1-card.md:89, INV-006; Disposition: modified (appended entry); Decision basis: INV-006`
- **Validation**: Structural integrity ✅ | References ✅ (recommendations[1] is the pytest rec carrying the taxonomy mapping) | Contradictions ✅

### Change 13: Carry V1's worked whitespace example into base risks[4]
- **Status**: Applied
- **Source**: Variant 1 risks[2] (V1:80)
- **Target**: Base risks[4] (V2:40), appended
- **Before**: "src/greeting.py:2 rejects every falsy value and accepts whitespace (src/greeting.py:4). Unspecified (spec.md:9); surprise for callers, not a contradiction."
- **After**: Base text verbatim, then ` For example, src/greeting.py:4 returns "Hello,   !" for a whitespace-only name (V1:80).` V1's literal is copied exactly, with three spaces. The inner quotes are escaped as `\"`, and the parser returns the exact literal.
- **Provenance tag**: `# Source: Base (original, modified) — Change #13, with Variant 1 (sonnet:analyzer) V1:80 — Change #13; Anchor: risks[4] (V2:40), worked example "Hello,   !"; Disposition: merged-from-multiple`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

## Post-Merge Validation

### YAML parse (actually executed)
- `uv run --no-project python -c "import yaml"` failed with `ModuleNotFoundError: No module named 'yaml'` (PyYAML is not available under --no-project alone).
- `uv run --no-project --with pyyaml python -c "import yaml,sys; d=yaml.safe_load(open(sys.argv[1])); ..." <merged-card.yaml>` succeeded. uv installed pyyaml into an ephemeral environment from cache ("Installed 1 package in 13ms"). Output:
  - keys: `['reviewer', 'persona', 'findings', 'grounding_gaps', 'agreements_with_t1', 'disagreements_with_t1', 'risks', 'recommendations', 'verdict', 'self_reported_confidence']`
  - verdict: `{'tasklist_completion_pct': 0.667, 'regression_present': False, 'status_recommendation': 'partial'}` (the assert passed)
  - findings `[]`; grounding_gaps 3; recommendations 5; agreements 7; disagreements 2; risks 6
  - priorities `['high', 'high', 'high', 'low', 'low']`; owners `['user','user','user']`; decision_needed_by_user `[True, True, False]`; reviewer 2, persona qa, confidence 0.8
- A second executed check parsed the base and the merged card and compared them. Every field this log marks preserved-exact is string-equal to the base. Every append-type change starts with the full base string. The G1 next_evidence_needed ends with the base text, apart from its first character (the lower-cased "A").

### Structural Integrity
- Top-level key set and order: ✅ exact G-1 list, no added keys.
- grounding_gaps subkeys: ✅ all 3 rows have exactly `hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user`.
- recommendations subkeys: ✅ all 5 have exactly `file, change, verifier, priority`.
- verdict subkeys: ✅ exactly `tasklist_completion_pct, regression_present, status_recommendation`.
- Provenance coverage: ✅ 28 `# Source:` tags (Grep count), one per required element.
- Quoting style: ✅ double-quoted single-line strings as in the base. Inner quotes are escaped (`f\"Hello, {name}!\"`, `\"Hello,   !\"`).

### Internal References
- Total references checked: 8. Resolved: 8. Broken: 0.
  - G1 (agreements[5], disagreements[0], rec[0], rec[1], verdict comment) resolves to grounding_gaps[0].
  - G2 (rec[1], verdict comment) resolves to grounding_gaps[1].
  - G3 (rec[1], rec[2], verdict comment) resolves to grounding_gaps[2].
  - "G1-G3 are ordinal labels" (agreements[5]) matches the `# G1./G2./G3.` comment labels.
  - recommendations[0] (G1 next_evidence_needed) resolves to the changes.patch regeneration rec.
  - recommendations[1] (disagreements[1]) resolves to the pytest run rec that carries the :105-113 mapping.
  - "the Change 1 run" (rec[0] verifier) is plan-verbatim wording and resolves in practice to recommendations[1]. This is flagged as plan-internal wording, not broken.
  - "3 rows" (verdict comment) matches len(grounding_gaps) == 3.

### Contradiction Re-Scan
- New contradictions introduced: 0.
- Checked:
  - rec[1] no longer advises adding src/__init__.py, consistent with INV-014 and agreements[0] (no unmapped hunk).
  - G2 why_not_classifiable and risks[1] say exit 2/3 is a Grounding Gap, consistent with the rec[1] verifier.
  - G3 `decision_needed_by_user: false` vs "forces partial / needs_human_decision" is reconciled by the Change 6 text and is consistent with agreements[5] and the verdict comment.
  - rec[3] priority low is consistent with G3 not being urgent.
  - risks[5] says the snapshot is not a complete mirror, consistent with the G2 append and rec[4].
  - risks[0] (completed.md:8) is consistent with rec[2] (uncheck T-103).
  - regression_present false is consistent with rec[1] (exit 1 is a Regression only on a real assertion failure) and disagreements[1].
- Known residual, not new: G2 next_evidence_needed (base, verbatim) names `python -m pytest tests` / `pytest tests` without `-q`, while rec[1] uses `-q`. This is a flag difference, not a contradiction. It was left as is because G-3 requires verbatim base text.

### Threshold Preservation Check (against plan table)
| Value | Location | Plan disposition | Result |
|---|---|---|---|
| 0.667 | verdict.tasklist_completion_pct | preserved-exact | ✅ 0.667 |
| 2/3, 0.667 | agreements_with_t1[5] | preserved-exact | ✅ present (base prefix string-equal) |
| 0/3 executed coverage | risks[2] | preserved-exact | ✅ string-equal (also repeated in the verdict comment) |
| "2 passed" | recommendations[1] | preserved as success detail | ✅ in the verifier, "0 (expected success detail: 2 passed)" |
| 0.8 | self_reported_confidence | preserved-exact + comment | ✅ 0.8, with a not-calibrated comment |
| 13 lines (tests/test_greeting.py:1-13) | grounding_gaps[0], recommendations[0] | preserved-exact | ✅ in both (G1 hunk_ref/evidence/next_evidence; rec[0] change/verifier) |
| V1 exit codes 0 / 1 / 2/3 | V1:91 | merged-from-multiple (+5, 124, flaky, other) | ✅ rec[1] verifier has 0, 1, 2/3, 5, 124, flaky (:112), other (:113) |
| V1 66.7 | V1:99 | dropped-with-rationale | ✅ absent; rationale X-001 (out of `<float 0.0-1.0>`, SKILL.md:1136; V1 conceded) |
| priority medium | recommendations[3] | modified -> low | ✅ low (C-007, Change 8) |
- Result: PASS.

### Dropped-Anchor Audit (against plan)
Variant 1 anchors absent from the merged card. Each is accounted for in the plan:
| Anchor / verbatim text | Source | Change # | Decision basis | Replacement target |
|---|---|---|---|---|
| V1:36 "The audit root's pyproject.toml and pytest config are not in the snapshot" | Variant 1 | none (plan omission table) | Factual error; no pyproject.toml in the audit root (Step 3 K1 re-evaluation; base-selection.md) | none |
| V1:82 "Evidence gap. I did not read git-inventory.txt, reuse-audit.yaml or execution.log..." | Variant 1 | none (C-004/X-003) | Contradicts the base citations, which read the files; V1 conceded in R2 | none |
| V1:99 `tasklist_completion_pct: 66.7` | Variant 1 | none (X-001) | Out of contract range; V1 conceded | verdict 0.667 (base) |
| V1:85 absolute frozen-snapshot changes.patch as rec #1 target | Variant 1 | Change 3 (C-009) | The frozen copy is read-only | audit-root changes.patch path |
| V1:94 "Route the falsy-input behavior to correctness-gaps.yaml" | Variant 1 | none (C-001/X-002) | Channel needs sibling symbols (deviation-taxonomy.md:175) | G3 row kept and clarified (Change 6) |
| V1:91 citation "deviation-taxonomy.md:107-108" | Variant 1 | Change 1 | INV-006 | deviation-taxonomy.md:105-113 (superset) in the rec[1] verifier |
| V1 G1 "no commits, so no tracked-state signal" (V1:20-21) | Variant 1 | none (C-002) | Untracked status is tree-wide | base G1 evidence_missing |
| V1 G2 "weakly grounded / not a likely failure" grade | Variant 1 | none (C-003) | No likelihood grade without a run | none |
| V1:81 "adequate for R-003 but weak as a regression guard" | Variant 1 | none (C-008) | V2:39 is the precise version | risks[3] (base) |
| V1 "owner could be the orchestrator" | Variant 1 | none (INV-005) | Not a legal owner (deviation-taxonomy.md:145) | owner: user |
| V1:6-14 `#` rationale comment block | Variant 1 | Change 2 (S-001) | Basis carried as structured text, not a comment block | agreements_with_t1[0] append |
| V1 "(G1, G2)" verdict comment | Variant 1 | Change 11 | INV-008 | "3 rows: G1, G2, G3" comment |
| V1:80 `"Hello,   !"` worked example | Variant 1 | Change 13 | concrete-over-generic | risks[4], preserved exactly |

Base (Variant 2) anchors rewritten or dropped by planned changes:
| Anchor / verbatim text | Change # | Decision basis | Replacement target |
|---|---|---|---|
| rec[1] change "add src/__init__.py or a pythonpath config, then re-run" | 1 | INV-014 (unmapped-hunk Drift signal) | src/__init__.py, conftest.py and pytest config are still named, but discouraged; "pythonpath config" is now covered by "pytest config" |
| rec[1] verifier "Both commands exit 0 with 2 passed" | 1 | INV-006 | "0 (expected success detail: 2 passed) clears G2" plus the full exit mapping |
| rec[0] `file: "changes.patch"` (relative) | 3 | C-009 / INV-001 | absolute audit-root changes.patch |
| rec[0] verifier "Patch contains a tests/test_greeting.py hunk ...; G1 can close" | 3 | INV-015 / INV-017(a) | H1-preservation + T-103 mapping verifier; "G1 can then close" kept |
| rec[2] change "Set frontmatter status to partial ..." / verifier "completed.md:2 is done only after those two artifacts exist" | 7 | INV-002 / INV-017(c) | plan text; completed.md:2 kept, completed.md:8 added |
| rec[3] change "State R-002 behavior ... then align src/greeting.py:2" / priority medium | 8 | C-007 / INV-016 | spec-first text; src/greeting.py:2 and spec.md:9 kept; priority low |
| risks[5] "[INFERRED] it might hold extra task text. Not classified: designated spec.md:1-12 and completed.md:1-8 were read in full and every MUST line is already in the matrix." | 9 | U-001 / A-001 (orchestrator verified proposed.md:3-10) | "adds no MUST beyond spec.md:6/9/12" (from proposed.md:3-10). The citations spec.md:1-12 and completed.md:1-8 no longer appear in risks[5]. The plan rewrote this entry. |
| rec[4] change "Copy the untracked proposed.md from git-inventory.txt:5 into the snapshot and confirm it adds no MUST line beyond spec.md:6, spec.md:9, and spec.md:12." / verifier "... or the user confirms it is out of scope." | 9 | U-001 / A-001 | "Include proposed.md in future snapshots..."; git-inventory.txt:5 and spec.md:6/9/12 are kept in risks[5]; the "user confirms out of scope" alternative was dropped by the plan |

- Unaccounted-for accepted anchors: 0. Every R-001..R-003, T-101..T-103 and H1 anchor, and every base file:line citation, is still present unless listed above with its plan change.
- Result: PASS.

## Deviations
- G1 next_evidence_needed: the base's opening "A" was lower-cased to join it to the plan-mandated prefix. No other wording changes.
- Change 1 verifier: "(expected success detail: 2 passed)" was inserted at exit 0. The plan explicitly allows this ("'2 passed' may remain as the expected success detail"), and the threshold table requires it to be preserved.
- Header: after the four G-2 lines, one line states the reviewer 1+2 merge (G-4 requirement). The base's two orchestrator comment lines are retained verbatim, under a label.
- PyYAML parse required `uv run --no-project --with pyyaml`. The package resolved from uv's local cache with no project install.

## Summary
- Total changes planned: 13
- Successfully applied: 13
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (YAML parse executed; structure, references, contradiction re-scan, threshold preservation and dropped-anchor audit all pass)
- Open item carried forward, not resolved by the executor: INV-006 stays UNADDRESSED in the debate return contract per the plan, even though Change 1 applies its correction.
