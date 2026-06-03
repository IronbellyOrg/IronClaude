---
dd: DD-4
verdict: REFACTOR
confidence: 0.87
---

## Adversarial findings

The tiered architecture (hash → structural → git) is the correct base — it beats every
single-signal alternative debated:
- **Alt A (pure git-diff):** loses on untracked / dirty / detached-HEAD / no-upstream tasklists
  (R-offline). FR-3.2 itself only promises git "where a remote is available," so git cannot be
  the sole tier. But Alt A contributes the *right cosmetic classifier* the design is missing.
- **Alt B (full-content binary hash):** is literally today's rerun SHA-guard. Binary ⇒ a trailing
  space refuses resume ⇒ directly violates AC-4. This is the exact brittleness FR-3.3 was written
  to remove ("not a brittle byte-hash").
- **Alt C (mtime):** no content signal; `touch`/checkout/save flips it. Reject outright.

So DD-4's *structure* is upheld. Four substantive defects must be fixed before tasklist:

1. **[HIGH — blocks AC-4] Tier 0 is NOT trailing-whitespace-safe.** The design's §5 inline claim
   that the normalized hash is "trailing-space safe (AC-4)" is false. `_content_sha256_excluding_rerun_block`
   strips ONLY the `<!-- SUPERCLAUDE-RERUN … -->` block (regex) and does NO whitespace
   normalization. Appending a space changes the digest, Tier 0 misses, and AC-4's ≥0.8 must be
   delivered by **Tier 1**. Tier 1 therefore needs a real whitespace-insensitive comparator
   (`git diff --ignore-all-space` when tracked, else a normalize-then-rehash that collapses
   trailing/again-blank whitespace). AC-4 cannot be claimed as a Tier-0 property.

2. **[HIGH — wrong artifact] DriftAssessor hashes `index_path`, but task content lives in the
   per-phase files.** The rerun engine hashes `phase_obj.file`, not the index. Hashing the index
   over-trusts: edits to task bodies/checkpoints are invisible. Storage (`phase-N-result.json`)
   is already per-phase and correct — only the read-side signature is wrong, so this is an
   internal inconsistency, not a redesign.

3. **[HIGH — guard, from invariant probe INV-001] Baseline and current hash MUST use the same
   function on the same file.** If `tasklist_sha256` is stored with `compute_tasklist_sha256`
   (raw bytes) while drift compares with `_content_sha256_excluding_rerun_block`, Tier 0 never
   hits even on byte-identical content — every resume silently degrades to Tier 1. The spec must
   pin both sides to `_content_sha256_excluding_rerun_block(phase_obj.file)`.

4. **[MEDIUM — feasibility] Tier 1 "structural diff of checkpoints/deliverables" is a composition,
   not an existing call.** `parse_tasklist` yields task IDs + free-text `description` only;
   it parses no checkpoint or deliverable *paths*. Checkpoint paths come from a separate helper
   (`extract_checkpoint_paths`). Spec should state Tier 1 composes `parse_tasklist` (task IDs) +
   `extract_checkpoint_paths` (checkpoints); deliverable-path diffing is best-effort over the
   free-text description.

Upheld as-written: backward-compat (absent `tasklist_sha256` ⇒ Tier-1/2 only; verified trivial
dict-extend at executor.py:2059-2067), git-tier-behind-capability-gate, and the single-write-path
constraint. The confidence constants (0.9/0.3/0.85) are arbitrary but only the **0.8 gate** is
load-bearing (FR-3.4); recommend treating the rest as advisory buckets so their arbitrariness
never drives control flow.

## Code verification (file:line)

- `_content_sha256_excluding_rerun_block` — `src/superclaude/cli/sprint/rerun_tasks.py:688-701`:
  reads file, calls `_split_rerun_block`, hashes `without_block.encode()`. **No `.strip()` / no
  whitespace normalization.** Regex `_RERUN_BLOCK_RE` (`:661`) matches only `<!-- SUPERCLAUDE-RERUN … -->`.
- `compute_tasklist_sha256` — `src/superclaude/cli/sprint/recovery.py:238-247`: raw-byte SHA256,
  no normalization (the function imported at `rerun_tasks.py:48` and used for stored bundle SHA).
- Engine hashes per-phase file, not index — `src/superclaude/cli/sprint/rerun_tasks.py:1306` and
  `:1387` both call `_content_sha256_excluding_rerun_block(phase_obj.file)`.
- `_write_phase_result_json` — `src/superclaude/cli/sprint/executor.py:2053-2072`: payload dict at
  `:2059-2067`; adding `"tasklist_sha256": …` is a trivial, backward-compatible extension.
- `parse_tasklist` — `src/superclaude/cli/sprint/config.py:405-498`: extracts `task_id`, `title`,
  `dependencies`, `command`, `classifier`, and a free-text `description` (deliverables folded in at
  `:461-479`). `TaskEntry` (`models.py:31-42`) has **no** checkpoint/deliverable path field.
- `extract_checkpoint_paths` — `src/superclaude/cli/sprint/checkpoints.py:40` (separate parser).
- Per-phase file model: `discover_phases` builds `Phase(number, file=…)` per file
  (`config.py:126-146`); a sprint = index + N per-phase files.

## Proposed spec changes

EXACT existing design.md text to replace + EXACT replacement text (copy-pasteable):

### Change 1 — DD-4 row in §0 (design.md:26)

REPLACE:
```
| **DD-4** | Drift assessment algorithm | **Deterministic tiered scoring**, LLM optional explainer. Tier 0: normalized-content hash equal (`_content_sha256_excluding_rerun_block`) ⇒ 1.0. Tier 1: structural diff of **completed-phase** task IDs / checkpoint paths / deliverable paths only. Tier 2: `git diff` vs remote when tracked+online. Whitespace/format/comment-only deltas in completed regions ⇒ ≥0.8; identifier/checkpoint/deliverable changes ⇒ <0.8. | `rerun_tasks.py:688-701` |
```
WITH:
```
| **DD-4** | Drift assessment algorithm | **Deterministic tiered scoring**, LLM optional explainer. Tier 0: per-phase normalized-content hash equal (`_content_sha256_excluding_rerun_block(phase_obj.file)`, same function on both stored and current side) ⇒ 1.0 — **exact-match only, NOT whitespace-tolerant**. Tier 1 delivers AC-4: a whitespace-insensitive comparator (`git diff --ignore-all-space` when tracked, else normalize-then-rehash) classifies trailing/format/comment-only deltas in completed `phase_obj.file` regions ⇒ ≥0.8; structural diff composes `parse_tasklist` (task IDs) + `extract_checkpoint_paths` (checkpoint paths), with deliverable-path diff best-effort over `description`; identifier/checkpoint/deliverable changes ⇒ <0.8. Tier 2: `git diff` annotation when tracked+online (skip gracefully on detached-HEAD / no upstream). Only the 0.8 value gates; other confidences are advisory. | `rerun_tasks.py:688-701,1306,1387`; `config.py:405`; `checkpoints.py:40` |
```

### Change 2 — DriftAssessor algorithm in §5 (design.md:179-184)

REPLACE:
```
assess(index_path, plan) -> DriftAssessment:
  current_sha = _content_sha256_excluding_rerun_block(index_path)        # rerun_tasks.py:688
  recorded_sha = source_tasklist_sha256 from latest RecoveryBundleRef OR
                 stored at last phase_complete (see DD-4 note below)
  # Tier 0 — normalized hash (cosmetic block already stripped) → trailing-space safe (AC-4)
  if current_sha == recorded_sha: return Drift(confidence=1.0, tier="hash", cosmetic_only=True)
```
WITH:
```
assess(index_path, plan) -> DriftAssessment:
  phase_file  = plan boundary phase's phase_obj.file        # per-phase, NOT index_path
  current_sha = _content_sha256_excluding_rerun_block(phase_file)        # rerun_tasks.py:688
  recorded_sha = tasklist_sha256 stored in phase-N-result.json for that phase  # DD-4 note below
               # MUST be produced by the SAME function (_content_sha256_excluding_rerun_block)
               # over the SAME file, or Tier 0 can never match (invariant INV-001).
  # Tier 0 — exact normalized-hash match only (block stripped; NOT whitespace-tolerant).
  if recorded_sha and current_sha == recorded_sha: return Drift(confidence=1.0, tier="hash", cosmetic_only=True)
  # AC-4 (trailing whitespace) is handled in Tier 1, not here.
```

### Change 3 — Tier-1 line in §5 (design.md:186-189)

REPLACE:
```
  changed = structural_diff(parse_tasklist(now), recorded_completed_task_ids/checkpoints/deliverables)
  if changed ⊆ {whitespace, comments, formatting}:        confidence≈0.9
```
WITH:
```
  cosmetic = (git diff --ignore-all-space clean) OR (normalize-then-rehash equal)   # AC-4 path
  changed  = structural_diff(parse_tasklist(phase_file)+extract_checkpoint_paths(phase_file),
                             recorded_completed_task_ids/checkpoints)                 # deliverables best-effort
  if cosmetic and not changed:                            confidence≈0.9  (≥0.8 ⇒ AC-4 passes)
```

### Change 4 — DD-4 storage note in §5 (design.md:195-200)

REPLACE:
```
**DD-4 storage note:** today `source_tasklist_sha256` is only persisted inside a
`RecoveryBundle` after a rerun (`recovery.py:111`). For fresh-run drift detection we need a
baseline hash captured at **each phase_complete**. Minimal addition: write
`tasklist_sha256` into `phase-N-result.json` (extend `_write_phase_result_json`,
`executor.py:2053-2072`) — one field, backward-compatible (absent ⇒ Tier-1/2 only, no Tier-0
shortcut). This is the **only change to the write path** in the whole feature.
```
WITH:
```
**DD-4 storage note:** today `source_tasklist_sha256` is only persisted inside a
`RecoveryBundle` after a rerun (`recovery.py:111`). For fresh-run drift detection we need a
baseline hash captured at **each phase_complete**. Minimal addition: write
`tasklist_sha256 = _content_sha256_excluding_rerun_block(phase_obj.file)` into
`phase-N-result.json` (extend `_write_phase_result_json`, `executor.py:2053-2072`, payload dict
`:2059-2067`) — one field, backward-compatible (absent ⇒ Tier-1/2 only, no Tier-0 shortcut).
**The stored hash MUST use `_content_sha256_excluding_rerun_block` over the per-phase
`phase_obj.file`** — the identical function/file the DriftAssessor uses on the current side, or
Tier 0 can never match (INV-001). Pre-v4.3.5 phases carry no stored hash, so their first
post-upgrade resume skips Tier 0 by design. This is the **only change to the write path** in the
whole feature.
```
