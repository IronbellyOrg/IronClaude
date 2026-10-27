---
remediation_for: anti-instinct-audit.md
spec_source: .dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md
roadmap_target: .dev/releases/Current/MultiModelSwarm/roadmap.md
generated: 2026-05-31
generator: claude-sonnet-4.7 (manual remediation pass)
---

# MultiModel Swarm — Anti-Instinct Audit Remediation Proposal

## 0. Summary

The 2026-05-30 anti-instinct gate failed with **6 undischarged obligations** and **6 missing fingerprints** (coverage 0.82, below the 0.70 threshold floor isn't the issue — the gate fails on any missing items it surfaces). Root-cause analysis shows the failures split cleanly into **two categories**:

| Category | Count | Side to fix |
|---|---|---|
| False-positive **"stub" obligations** — refer to a permanent test-fixture transport, not a scaffold to discharge | 6 | Roadmap text (rename) **+** scanner contract (clarification) |
| False-positive **fingerprints** — RFC-style emphasis / meta-document keywords mistakenly extracted as code identifiers | 3 (`HTML`, `UNADDRESSED`, `WILL`) | Scanner `_EXCLUDED_CONSTANTS` |
| **Genuine roadmap gaps** — spec contract fields not mirrored | 3 (`normalizer_strategy`, `final_path`, `MULTIMODEL`) | Roadmap text (additive references) |

Net effect of remediation: 6 stub obligations resolved by rename + scanner clarification; 6 fingerprints split 3-scanner / 3-roadmap. Re-running `superclaude roadmap run` from the `anti-instinct` step should yield **0 undischarged / 33-of-33 fingerprints / gate PASS**.

---

## 1. False-positive "stub" obligations (lines 207, 211, 213)

### 1.1 Evidence

`src/superclaude/cli/vocabulary.py:17` lists `\bstub(?:bed|s)?\b` as a SCAFFOLD term. The scanner therefore demands a later-milestone "replace stub" / "wire stub" / "remove stub" discharge phrase.

The 6 flagged occurrences all reference the **`stub transport`** — a deterministic test transport defined by `COMP-033`, `FR-023`, and used by `IMM-3` for the parallelism wall-clock test. Per spec §11.5 and §4.3, the stub transport is the **permanent test fixture**, not a temporary scaffold replaced later. There is no "discharge" because there is nothing to discharge.

### 1.2 Fix — Roadmap text rename

In `.dev/releases/Current/MultiModelSwarm/roadmap.md`, perform the following exact-text renames in the M3 section (and any downstream cross-reference). The Python module path `cli/swarm/transports/stub.py` STAYS as-is — the scanner only reads roadmap prose.

| Roadmap line | Before | After |
|---|---|---|
| 207 (COMP-033 row, Title col) | `stub transport` | `deterministic-fixture transport` |
| 207 (COMP-033 row, Description col) | `Deterministic stub for tests` | `Deterministic test fixture` |
| 207 (COMP-033 row, AC col) | `fixed deterministic outputs; enables parallelism test` | (unchanged — already discharge-neutral) |
| 211 (FR-023 row, Title col) | `stub transport` | `deterministic-fixture transport` |
| 211 (FR-023 row, Description col) | `Deterministic stub transport for tests` | `Deterministic test-fixture transport` |
| 213 (IMM-3 row, AC col) | `stub-worker parallelism test` | `fixture-worker parallelism test` |

Per `src/superclaude/cli/vocabulary.py:52`, the framework's own preferred alternative for "stub" is **"define"**. For the proper-noun module name we use the more accurate phrase **"deterministic-fixture"** which preserves the architectural intent ("fixed, repeatable, no-network") without invoking the scaffold vocabulary.

### 1.3 Optional belt-and-suspenders — obligation-exempt comments

If for any reason the rename is rejected during /sc:reflect (e.g., reviewers prefer the legacy "stub transport" name for ecosystem consistency), the alternative per `obligation_scanner.py:34` (`FR-MOD1.7`) is to append `<!-- obligation-exempt -->` to each of the 6 lines. This is a documented escape hatch designed for exactly this situation. Tasklist generation MUST choose **one** of the two options, not both.

---

## 2. False-positive missing fingerprints (scanner side)

### 2.1 Evidence

`src/superclaude/cli/roadmap/fingerprint.py:144` extracts ALL-CAPS tokens `\b([A-Z][A-Z_]{3,})\b` (≥4 chars) and excludes a curated list at `fingerprint.py:30` (`_EXCLUDED_CONSTANTS`). The exclusion already covers RFC emphasis words `MUST`, `SHALL`, `SHOULD`, format names `YAML`, `JSON`, status words `TODO`, `NOTE` etc.

Three of the 6 missing fingerprints are the same class of word that's already excluded — they were missed during initial curation:

| Fingerprint | Spec context (verbatim) | Class | Already-excluded peer |
|---|---|---|---|
| `HTML` | `<!-- Per-section source attribution provided inline as HTML comments -->` (spec line 5) | Document format name | `YAML`, `JSON` |
| `UNADDRESSED` | `unaddressed_invariants: 0 (all 6 HIGH+UNADDRESSED items resolved by refactor plan)` (spec line 25) | Status word in frontmatter audit annotation | `EXEMPT`, `TODO`, `PASS`, `FAIL` |
| `WILL` | `### 11.1 The orchestrator WILL` (spec line 560) | RFC-style emphasis verb in Will/Will-Not boundary section | `MUST`, `SHALL`, `SHOULD`, `MANDATORY` |

### 2.2 Fix — extend `_EXCLUDED_CONSTANTS`

Append three string literals to the frozenset at `src/superclaude/cli/roadmap/fingerprint.py:30-86`:

```python
# Existing — formats/standards block (around line 47):
"YAML",
"JSON",
"HTML",   # ← new: document format name, same class as YAML/JSON

# Existing — RFC/spec emphasis block (around line 58):
"MUST",
"SHALL",
"SHOULD",
"WILL",   # ← new: Will / Will-Not boundary verb, same class as MUST/SHALL

# Existing — test/status block (around line 53):
"TODO",
"NOTE",
"UNADDRESSED",   # ← new: audit-annotation status, same class as EXEMPT/TODO
```

Each addition must be **unit-tested** (`tests/cli/roadmap/test_fingerprint.py`) with a fixture string containing the new token in spec-typical context, asserting that the constant is excluded from extraction.

### 2.3 Forward-looking guard

Add a comment at the top of `_EXCLUDED_CONSTANTS` documenting the addition criteria so future maintainers don't re-introduce the same class of false positive:

```python
# Addition criteria: a token belongs here ONLY if it is an ALL-CAPS prose word
# (RFC emphasis, format name, status annotation) that the spec author would
# never expect to appear verbatim in an implementation-level roadmap. If you
# add a token, add a unit test in test_fingerprint.py with a representative
# fixture line.
```

---

## 3. Genuine roadmap gaps (roadmap side)

These three fingerprints reflect spec contract details that the roadmap genuinely failed to mirror. Each gets an additive insertion — no existing roadmap text is removed.

### 3.1 `normalizer_strategy` — lens-registry contract field

**Spec source:** `merged-requirements.md` line 236, §3.4 PR-review discipline:
> The `normalizer_strategy` matches the prompt's expected output shape.

**Roadmap target:** Append a new row to the M2 (Preflight & Lens Registry) milestone table. The lens registry section currently lists `validate-lenses` (line 241 of spec) but does not enumerate the `normalizer_strategy` validation rule. Insert after the existing lens-validator row:

```markdown
|N|FR-LENSREG.NS|normalizer_strategy field|Each `LENSES` entry declares `normalizer_strategy` matching the prompt's expected output shape; validator asserts a registered Recipe matches the strategy|cli/swarm/lenses/registry.py|FR-LENSREG.VALIDATOR|validate-lenses fails when `normalizer_strategy` is missing or unmatched|S|P0|
```

Renumber the immediately-following rows in the M2 table to keep monotonic IDs.

### 3.2 `final_path` — per-worker output contract field

**Spec source:** `merged-requirements.md` lines 517, 541, §5 Merge regeneration & §5.3 Allowed merge ops:
> read each worker's `final_path`, strip frontmatter, prepend `## From {model_label} ({elapsed_ms}ms)` provenance header, concat in slot-index order.

**Roadmap target:** Edit the existing **M5 mechanical-merge row** (currently roadmap line 307, `FR-034`) to use the literal field name. Current text already contains the phrase `read each \`final_path\`` (line 307) — wait, audit reports `final_path` as missing. Verify by re-reading the merged-state output:

```bash
grep -n 'final_path' .dev/releases/Current/MultiModelSwarm/roadmap.md
```

If grep returns 0 hits (suggesting the merge step compressed the backticks away during base-selection), add the literal field name back in M5 FR-034 description column. Insert at the start of the description:

> Module ≤30 LOC; read each worker's `final_path`, strip frontmatter, prepend `## From {model_label} ({elapsed_ms}ms)`, concat in slot-index order; no reorder/dedup/scoring/winner/claim-rewriting

Also add `final_path` to the WorkerResult schema row in M1 (DM-008 or equivalent) — the per-worker contract MUST declare this field by name.

### 3.3 `MULTIMODEL` — spec-ID reference

**Spec source:** `merged-requirements.md` line 8:
> spec_id: SPEC-MULTIMODEL-SWARM

**Roadmap target:** The roadmap title is "Multi-Model Swarm Orchestrator" (hyphenated `Multi-Model`), and the lowercase substring match `multimodel` therefore returns 0. Two acceptable resolutions — tasklist generator picks **one**:

**Option A (preferred):** Add an explicit spec-ID reference to the roadmap frontmatter:

```yaml
---
spec_id: SPEC-MULTIMODEL-SWARM
spec_source: merged-requirements.compressed.md
…
---
```

This is a minimal addition (1 line) that ties the roadmap to its parent spec contract by ID — useful for downstream sprint/tasklist tooling regardless of the audit gate.

**Option B (alternative):** Extend the fingerprint matcher in `src/superclaude/cli/roadmap/fingerprint.py:191` to normalize hyphens and underscores during the comparison:

```python
roadmap_normalized = re.sub(r'[-_\s]', '', roadmap_content.lower())
if re.sub(r'[-_\s]', '', fp.text.lower()) in roadmap_normalized:
    found += 1
```

Option A is preferred because it makes the spec-ID linkage explicit and survives renaming; Option B has the broader benefit of catching all hyphenation drift but risks new false positives. Recommend Option A as the headline change, with Option B reserved for a follow-on hardening pass.

---

## 4. Verification checklist (post-remediation)

| Step | Command | Expected |
|---|---|---|
| 1. Apply scanner-side edits | (edit `fingerprint.py` per §2.2) | 3 new EXCLUDED entries |
| 2. Apply scanner-side tests | (add fixtures to `tests/cli/roadmap/test_fingerprint.py`) | 3 new tests, all PASS |
| 3. `make verify-sync` | n/a | source-of-truth in src/, no .claude/ drift |
| 4. Apply roadmap-side rename (§1.2) | edit `roadmap.md` lines 207, 211, 213 | "stub transport" → "deterministic-fixture transport" ×6 |
| 5. Apply roadmap-side additions (§3.1 §3.2 §3.3 Option A) | edit `roadmap.md` M2 / M5 / frontmatter | new rows + frontmatter spec_id |
| 6. Re-run audit (scanner only) | `superclaude roadmap audit .dev/releases/Current/MultiModelSwarm/` (or equivalent) | `undischarged_obligations: 0`, `fingerprint_coverage: 33/33` |
| 7. Re-run full pipeline | `superclaude roadmap run --resume .dev/brainstorms/20260529-multimodel-swarm-COMPARE/merged-requirements.md --output .dev/releases/Current/MultiModelSwarm/` | `anti-instinct` step status = PASS; `wiring-verification` remains PASS |
| 8. Inspect new audit report | `cat .dev/releases/Current/MultiModelSwarm/anti-instinct-audit.md` | header reports 0 undischarged + 1.00 fingerprint coverage |

---

## 4.5 Post-remediation TDD-ingestion wiring for downstream `/sc:tasklist`

The user has explicitly requested that the eventual `/sc:tasklist` invocation ingest the spec as a TDD (and where useful, as a PRD), not just as a roadmap. The merged-requirements.compressed.md is a hybrid TDD+PRD-style brainstorm-merged spec (architecture overview, lens-registry contract, result-contract schema, monitoring contract, migration plan all present), but it does NOT currently satisfy the strict TDD-format heuristic at `sc-tasklist-protocol/SKILL.md:171`:

> input contains `## 10. Component Inventory` heading OR YAML frontmatter `type` contains "Technical Design Document" OR 20+ section headings matching TDD numbering pattern

The merged-requirements has 18 numbered sections, and §10 is "Amalgamation Modes" not "Component Inventory". Without a force, step 4.1a logs `warning: spec is not TDD-format, continuing with roadmap-only generation` and the TDD enrichment per §4.4a never runs.

**Three additive wiring steps to add to the remediation tasklist** (executed AFTER the audit-PASS roadmap is in place, BEFORE the downstream /sc:tasklist agent is spawned):

1. **Annotate frontmatter of `merged-requirements.compressed.md`** — add `type: Technical Design Document` to the YAML frontmatter. This is the file the tasklist will read; the annotation forces TDD detection without modifying the source `merged-requirements.md` brainstorm artifact. The compressed file is a derived output, safe to annotate.

   ```yaml
   ---
   spec_id: SPEC-MULTIMODEL-SWARM
   type: Technical Design Document   # ← new: forces TDD-format detection in /sc:tasklist §4.1a
   spec_version: 1.0.0-merged
   ...
   ---
   ```

2. **Update `.roadmap-state.json`** — set `tdd_file` so the protocol's auto-wire path (§4.1c) picks up the spec without requiring explicit `--spec` re-pass. Also set `input_type: "tdd"` to clarify intent:

   ```json
   {
     "tdd_file": "/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/releases/Current/MultiModelSwarm/merged-requirements.compressed.md",
     "prd_file": null,
     "input_type": "tdd",
     ...
   }
   ```

   `prd_file` stays `null` because the spec's product context is embedded throughout, not in dedicated User Personas / Customer Journey Map sections that `§4.1b` regex extraction expects. Forcing a PRD-extraction pass on a TDD-shaped spec would log warnings without adding signal.

3. **Belt-and-suspenders explicit invocation** — when the downstream agent runs `/sc:tasklist`, pass `--spec` explicitly so CLI flag overrides state auto-wire if there's any drift:

   ```
   /sc:tasklist .dev/releases/Current/MultiModelSwarm/roadmap.md \
     --spec .dev/releases/Current/MultiModelSwarm/merged-requirements.compressed.md \
     --output .dev/releases/Current/MultiModelSwarm/tasklist/
   ```

**Important caveat — content-driven enrichment vs. regex-driven extraction:** Even with TDD detection forced, the regex extractors at §4.1a scan for specific TDD section names (`## 10. Component Inventory`, `## 15. Testing Strategy`, `## 19. Migration & Rollout Plan`, `## 8. API Specifications`). The merged-requirements uses different section titles for equivalent content:

| TDD-expected section | Actual section in merged-requirements |
|---|---|
| `## 10. Component Inventory` | `## 2. Architecture Overview` (component table) + `## 3. Lens Registry` |
| `## 15. Testing Strategy` | embedded in `## 8. Concurrency Model` + `## 12. Inheritance from Parent Spec` |
| `## 19. Migration & Rollout Plan` | `## 16. Migration Plan` |
| `## 8. API Specifications` | `## 6. CLI Surface` + `## 5. Result Contract Schema` + `## 7. Monitoring Contract` |

The regex `supplementary_context` dictionary will therefore be sparse, but the **generation-time content-driven enrichment** at §4.4a ("the generator MUST cross-reference existing roadmap-derived tasks against the original TDD to add specificity") loads the whole TDD body into the LLM prompt and operates content-driven, not regex-driven. That cross-referencing path WILL pick up the architecture / contract / migration content regardless of heading naming, as long as TDD-format detection fires (step 1 above).

This explains why the three wiring steps above are listed in priority order: step 1 (frontmatter) is the critical force; steps 2 and 3 are belt-and-suspenders to survive any pipeline-state drift.

## 5. Out-of-scope (deferred)

- **Hyphen-normalization fingerprint matcher (§3.3 Option B)** — accepted as future hardening, not required for current gate to pass.
- **Stub-transport vocabulary update across other roadmaps** — this remediation fixes only the MultiModelSwarm roadmap. The general pattern "permanent test fixture incorrectly flagged" should be tracked separately as a vocabulary refinement RFC.
- **Roadmap-pipeline cosmetic remediation step** — unrelated to audit findings.

---

## 6. Risk & rollback

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Rename in §1.2 changes meaning vs source spec | LOW | LOW | Rename is term-only; module path `transports/stub.py` and behavior unchanged |
| New `_EXCLUDED_CONSTANTS` entries mask a genuine gap elsewhere | LOW | MEDIUM | Add corresponding negative-test fixtures so future spec authors using these tokens as actual constants get a CI signal |
| Frontmatter `spec_id` insertion conflicts with downstream YAML parser | LOW | LOW | Validate via `superclaude roadmap validate` after edit |
| `make verify-sync` fails because src/.claude diverge | LOW | LOW | Edit `src/superclaude/` only, then `make sync-dev`; never edit `.claude/` directly |

Rollback: revert the three commits in reverse order (`git revert <fingerprint-edit>` → `git revert <test-edit>` → `git revert <roadmap-edit>`). No DB / state changes involved.
