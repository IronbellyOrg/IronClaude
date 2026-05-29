# `sc-bare-review` — Compressed-Markdown Output Template

Canonical reference for the per-reviewer output artifact. Source of truth: spec
`merged-requirements.md` §4.1 (template) and §4.2 (field semantics). The bare-reviewer
prompt (`refs/prompts.md`) instructs the external model to emit **this exact shape**;
`scripts/t2_normalize.py` parses model output against it and fills the frontmatter the
model cannot reliably produce (checksum, elapsed_ms, generated timestamp).

---

## Template (§4.1)

```markdown
---
schema_version: 1.0
tier: T2
suspect: true
reviewer_model_id: <e.g., deepseek-v4-pro>
reviewer_model_label: <e.g., DeepSeek V4 Pro>
target: <absolute path>
target_checksum: <sha256-12>
target_truncated: <bool>
generated: <ISO-8601>
caller_label: <optional label from --label flag>
elapsed_ms: <int>
finding_count: <int>
---

# T2-Bare Review — <target slug>

## Findings

| ID | Sev | Claim | Cite | SelfConf |
|----|-----|-------|------|----------|
| F-01 | crit | <≤120 chars> | <file:line OR "none"> | 0-100 |
| F-02 | high | <≤120 chars> | <file:line OR "none"> | 0-100 |
| F-03 | med  | <≤120 chars> | <file:line OR "none"> | 0-100 |
| F-04 | low  | <≤120 chars> | <file:line OR "none"> | 0-100 |
| F-05 | nit  | <≤120 chars> | <file:line OR "none"> | 0-100 |

## Verdict
<≤300 chars: overall judgment, no prose padding>

## Notes
<optional, ≤200 chars: anything not fitting a finding row>
```

---

## Field semantics (§4.2)

| Field | Meaning | Owner |
|-------|---------|-------|
| `schema_version` | Bumped when template structure changes (validator-consumable). Current: `1.0`. | normalizer |
| `tier` | Always `T2` for bare reviewers. | normalizer |
| `suspect` | Always `true` — non-negotiable; this is the whole framing (AC-1.9). | normalizer |
| `reviewer_model_id` | The model identifier passed to the proxy. | preflight/manifest |
| `reviewer_model_label` | Human-readable; for display in merged-report provenance comments. Defaults to `reviewer_model_id` when no `T2Model0N_Label`. | preflight/manifest |
| `target` | Absolute path of the reviewed file. | preflight/manifest |
| `target_checksum` | First 12 hex of SHA-256 of the (possibly truncated) target content (AC-1.10). | preflight |
| `target_truncated` | `true` if `--target-line-cap` triggered. | preflight |
| `generated` | ISO-8601 UTC timestamp of normalization. | normalizer |
| `caller_label` | Optional context tag from `--label`; surfaces in adversarial diff-analysis. May be empty. | preflight |
| `elapsed_ms` | Wall-clock for this reviewer's proxy call (from dispatch `.meta.json`). | dispatch → normalizer |
| `finding_count` | Number of `F-NN` rows successfully parsed. | normalizer |

### Findings table columns

| Column | Meaning |
|--------|---------|
| `ID` | `F-NN` row id, sequential per reviewer. |
| `Sev` (severity) | One of `crit`, `high`, `med`, `low`, `nit` (compressed — saves table width). |
| `Claim` | The finding, ≤120 chars, no newlines. |
| `Cite` | `file:line` reference if the model grounded the claim; literal string `none` otherwise. **Mandatory** — forces ground-or-admit. |
| `SelfConf` | Model's self-reported confidence 0-100. **Informational only** — NOT used in adversarial scoring (bare-reviewer self-confidence is itself suspect). |

---

## Why this shape (§4.3)

- **Tabular findings.** Diff-analysis can `grep` rows; scoring can count by `Sev` bucket;
  provenance annotation can point to `F-NN`.
- **Citation field is mandatory.** Either ground a claim or admit `none` — the cleanest
  separation for validator triage in `/sc:adversarial` Step 5.5.
- **No narrative.** `Notes` capped at 200 chars; prevents prose padding that bloats
  merged outputs.
- **`SelfConf` captured but disclaimed.** Useful debugging signal (which model is most
  confident in its hallucinations?) without polluting downstream scoring.

---

## Normalizer contract

- If the model returns output already conforming to this template → wrap/validate
  frontmatter and write final `.md`.
- If free-form → run lightweight regex + heuristic extraction into this shape; on
  irrecoverable parse failure mark the reviewer `parse_error` and retain the `.raw`.
- Severity tokens are normalized case-insensitively; unknown severities map to `med`.
- A `Cite` that is empty / `n/a` / `N/A` is normalized to the literal `none`.
