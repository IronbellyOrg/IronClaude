# Variant 1 — DESIGN AS WRITTEN (tiered hash→structural→git + tasklist_sha256 field)

## Claim
Drift assessment uses deterministic tiered scoring:
- Tier 0: `_content_sha256_excluding_rerun_block` equality ⇒ confidence 1.0, cosmetic_only.
- Tier 1: structural diff of completed-phase task IDs / checkpoint paths / deliverable paths.
  - whitespace/format/comment-only in completed regions ⇒ ≈0.9
  - identifier/checkpoint/deliverable change ⇒ ≈0.3
  - changes only in not-yet-run phases ⇒ ≈0.85
- Tier 2: `git diff @{upstream}` annotation when tracked+online.
Storage: add `tasklist_sha256` to `phase-N-result.json` via `_write_phase_result_json` (executor.py:2053-2072), backward-compatible (absent ⇒ Tier-1/2 only).

## Strengths
- Deterministic core, LLM only an explainer (NFR-3 compliant).
- Reuses the existing rerun SHA-guard helper, so no new hash semantics.
- Storage change is genuinely a one-field dict-extend; backward-compat is real.
- Tiering gives graceful degradation: hash miss → structural → git, never a hard crash offline.

## Verified weaknesses (must be fixed)
- **AC-4 is NOT satisfied by Tier 0.** `_content_sha256_excluding_rerun_block` (rerun_tasks.py:688-701) strips ONLY the `<!-- SUPERCLAUDE-RERUN ... -->` block (regex rerun_tasks.py:661). It does NO whitespace normalization. Appending a trailing space changes the digest ⇒ Tier 0 fails ⇒ AC-4's ≥0.8 must be delivered by Tier 1. The design's §5 inline claim "(cosmetic block already stripped) → trailing-space safe (AC-4)" is false.
- **Wrong file in the DriftAssessor signature.** §5 calls the hash on `index_path`, but task content lives in per-phase files; the rerun engine hashes `phase_obj.file` (rerun_tasks.py:1306,1387). Hashing the index will miss edits to task bodies and over-trust.
- **Tier-1 structural inputs are not first-class.** `parse_tasklist` (config.py:405) yields task_id + free-text `description`; it does not parse checkpoint paths or deliverable paths as fields. Checkpoint extraction is a separate helper (`extract_checkpoint_paths`, checkpoints.py:40). So "structural diff of checkpoints/deliverables" requires composing 2-3 parsers, not a single existing call.
- 0.9/0.3/0.85/0.8 numbers are asserted, not derived.
