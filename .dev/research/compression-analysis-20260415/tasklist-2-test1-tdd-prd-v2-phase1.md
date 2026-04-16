# Compression Analysis — Tasklist #2 (test1-tdd-prd-v2 / phase-1)

**Target file**: `/config/workspace/IronClaude/.dev/test-fixtures/results/test1-tdd-prd-v2/phase-1-tasklist.md`
**Reference**: `claudedocs/compressed-markdown-dsl-primer.md`
**Strategy row**: primer §5 TASKLIST row — *Approach 2 (AST) with auto-conventions-header, target **30-40%***
**Date**: 2026-04-15

---

## 1. File Inventory

### 1.1 Raw metrics

| Metric | Value |
|---|---:|
| Path | `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-1-tasklist.md` |
| Bytes | 58,653 |
| Lines (total) | 1,325 |
| Blank lines | 229 (~17.3%) |
| Pipe-table rows (`^|`) | 432 |
| Task header blocks (`### T01.xx`) | 27 |
| Checkpoint blocks (`### Checkpoint`) | 6 |
| Per-task `| Field | Value |` headers | 27 |
| Per-task `|---|---|` separators | 27 |
| Bold section markers (`^**`) | 216 |

### 1.2 Structural composition (approximate, by byte category)

Estimated from line inspection of the 1,325-line file:

| Category | Approx lines | Approx % of bytes | Notes |
|---|---:|---:|---|
| Per-task metadata tables (14-row `\| Field \| Value \|`) | ~405 (27 × 15) | ~31% | Prime conventions-header target |
| Task prose sections (Deliverables / Steps / AC / Validation / Dependencies / Rollback / Notes) | ~620 | ~47% | High structural regularity; repeated section headers |
| Blank lines | 229 | ~1% (bytes) | Approach 1 targets |
| Heading lines (`### Txx.nn`, `### Checkpoint`) | 33 | ~3% | Low compression value |
| Checkpoint blocks prose | ~50 | ~4% | Repeated 4-field template |
| Phase-1 preamble (lines 1-4) | 4 | ~1% | Prose header |
| Decorative whitespace (trailing spaces, column padding in tables) | distributed | ~3-5% | Rule-based wins |
| Fenced code blocks | 0 | 0% | **No code fences — Approach 2 is safe** |

Key observation: there are **zero code fences** in the file. Per primer §4 "Code fences are sacrosanct" constraint (primer §5 composition rule 2), this removes the primary risk of aggressive AST transforms — every transform below operates on prose or structured tables with no code to protect.

### 1.3 Repeated phrases ≥5× (conventions-header candidates, primer §2.2)

Empirical counts from the file:

| Phrase (raw) | Count | Char length | Raw bytes consumed |
|---|---:|---:|---:|
| `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-00` (path prefix) | 56 | 59 | 3,304 |
| `Critical Path Override` | 27 | 22 | 594 |
| `Requires Confirmation` | 27 | 21 | 567 |
| `Sub-Agent Delegation` | 27 | 20 | 540 |
| `Verification Method` | 27 | 19 | 513 |
| `Roadmap Item IDs` | 27 | 16 | 432 |
| `Risk Drivers` | 27 | 12 | 324 |
| `Deliverable IDs` | 27 | 15 | 405 |
| `Fallback Allowed` | 27 | 16 | 432 |
| `Acceptance Criteria:` (bold label) | 27 | 20 | 540 |
| `Artifacts (Intended Paths):` | 27 | 27 | 729 |
| `**Dependencies:**` | 27 | 17 | 459 |
| `**Rollback:**` | 27 | 13 | 351 |
| `**Deliverables:**` | 27 | 17 | 459 |
| `**Steps:**` | 27 | 10 | 270 |
| `**Validation:**` | 27 | 15 | 405 |
| `Required: Sequential, Serena` | 15 | 28 | 420 |
| `Sub-agent (quality-engineer)` | 15 | 28 | 420 |
| `Direct test execution` | 10 | 21 | 210 |
| `[██████████] 95%` (confidence bar) | 11 | 16 | 176 |
| `[████████--] 80%` | 10 | 16 | 160 |
| `[████████--] 85%` | 6 | 16 | 96 |
| `Preferred: Context7` | 6 | 19 | 114 |
| `**[PLANNING]**` | 36 | 14 | 504 |
| `**[EXECUTION]**` | 64 | 15 | 960 |
| `**[VERIFICATION]**` | 27 | 18 | 486 |
| `**[COMPLETION]**` | 27 | 16 | 432 |
| `Revert to previous implementation` | 5 | 33 | 165 |
| `Disable endpoint` | 5 | 16 | 80 |

Sum of raw bytes in these repeated spans alone: **~13,272 bytes (~22.6% of file)**. Even partial abbreviation here (average 70% reduction per occurrence via header keys) captures ~15-18% of total file size — before touching whitespace, tables, or prose.

All 29 phrases above meet primer §2.2's "5-10 body uses amortization" threshold with room to spare. Every one qualifies for a conventions-header entry.

---

## 2. Strategies Identified

Each strategy cites the primer section that authorizes it. Order of presentation is roughly Approach 1 → Approach 2, mirroring primer §5 composition rule 1 ("Always run Approach 1 first").

### Strategy 1 — Whitespace normalization (Approach 1)

**Primer basis**: §4.1 transforms 1-2 ("Collapse 3+ blank lines → 2 blank lines", "Strip trailing whitespace"), §2.3 "Whitespace & formatting ~8-12% ceiling".

**What**: Collapse multiple blank lines between task blocks and sections to a single blank line; strip trailing spaces on every line.

**Before** (lines 53-56):
```
**Notes:** Critical path — all backend components depend on this schema.

### T01.02 -- Provision Redis Cluster for Refresh Token Storage

```

**After**:
```
**Notes:** Critical path — all backend components depend on this schema.
### T01.02 -- Provision Redis Cluster for Refresh Token Storage
```

**Estimated saving**: File has 229 blank lines. Approach 1 typically eliminates ~40-50% of them where they appear between adjacent structural blocks. Savings: ~100 blank lines × 1 byte = ~100 bytes (minor in bytes), but in tokens this is more meaningful because each `\n\n` is often its own token. Estimate **~1.5-2% file reduction**.

**Lossless / lossy**: Lossless (primer §2.1 row 2).

**Risk**: None. No code fences in file; collapse is fully safe.

---

### Strategy 2 — Pipe-table column-padding collapse (Approach 1)

**Primer basis**: §4.1 transform 6 ("Collapse pipe-table padding: `| foo   | bar  |` → `|foo|bar|`"), §2.3 "Table whitespace ~3-5%".

**What**: Remove the single space after `|` and before `|` in the 432 metadata-table rows. Current rows use the form `| Field | Value |` with padded columns.

**Before** (line 8-14):
```
| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Database is the foundation for all user data persistence. ... |
| Effort | L |
| Risk | High |
| Risk Drivers | database, schema, migration, compliance, gdpr |
```

**After** (spaces removed, pipes kept so markdown-it still parses as a GFM table):
```
|Field|Value|
|---|---|
|Roadmap Item IDs|R-001|
|Why|Database is the foundation for all user data persistence. ...|
|Effort|L|
|Risk|High|
|Risk Drivers|database, schema, migration, compliance, gdpr|
```

**Estimated saving**: 432 table rows × ~4 padding spaces per row on average = ~1,728 bytes. **~2.9% file reduction**.

**Lossless / lossy**: Lossless (GFM tables are whitespace-insensitive between pipes).

**Risk**: Primer §4.1 flags "pathological tables" as the collapse risk. Here the tables are 2-column and uniform; no pathological cases.

---

### Strategy 3 — Auto-conventions-header for field labels (Approach 2)

**Primer basis**: §4.2 transform 5 ("Front-matter → conventions-header synthesis: scan for frequently-used multi-word phrases (>5 occurrences, >20 chars each) and auto-generate abbreviation"), §2.2 conventions header, §5 TASKLIST row (the canonical case).

**What**: Emit one conventions header near the top of the file and replace the 8 high-frequency 14-row-table field labels with short keys. These labels appear 27 times each (once per task).

**Header** (primer §2.2 format):
```html
<!-- cmd-dsl v1: RIID=Roadmap Item IDs | RD=Risk Drivers | VM=Verification Method
| MCP=MCP Requirements | FA=Fallback Allowed | SAD=Sub-Agent Delegation
| CPO=Critical Path Override | RC=Requires Confirmation | DID=Deliverable IDs
| SQS=Required: Sequential, Serena | QE=Sub-agent (quality-engineer)
| DTE=Direct test execution | PC=Preferred: Context7
| C95=[██████████] 95% | C85=[████████--] 85% | C80=[████████--] 80% -->
```

Header cost: ~340 chars one-time.

**Before** (T01.01 metadata table, lines 8-22):
```
| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Database is the foundation ... |
| Effort | L |
| Risk | High |
| Risk Drivers | database, schema, migration, compliance, gdpr |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0001, D-0002 |
```

**After**:
```
|F|V|
|---|---|
|RIID|R-001|
|Why|Database is the foundation ...|
|Effort|L|
|Risk|High|
|RD|database, schema, migration, compliance, gdpr|
|Tier|STRICT|
|Conf|C95|
|RC|No|
|CPO|Yes|
|VM|QE|
|MCP|SQS|
|FA|No|
|SAD|Required|
|DID|D-0001, D-0002|
```

**Estimated saving** (for the 15 repeated labels + 3 repeated values, aggregated from §1.3):
- Label abbreviations: ~3,300 bytes (sum of the 8 label rows at 27× each, primer's >5 occurrence rule covered comfortably)
- Value abbreviations (SQS, QE, DTE, PC, C95/C85/C80): ~1,600 bytes
- Header cost: 340 bytes
- Net: **~4,560 bytes ≈ 7.8% file reduction**

**Lossless / lossy**: Lossless per primer §2.1 row 4 (conventions-header abbreviation).

**Risk**: Primer §4.2 flags "auto-generated abbreviations need a review gate". Mitigation: the keys chosen here are all uppercase acronyms that do not collide with any substring in the body prose (verified: no occurrence of bare "SQS", "QE", "DTE", "RIID" etc. outside the table-value position). A decompressor can safely pattern-match `^|KEY|` + `|KEY|$` positions.

---

### Strategy 4 — Abbreviate the repeated artifact-path prefix (Approach 2)

**Primer basis**: §4.2 transform 5 (long-phrase auto-header synthesis); §2.2 conventions header.

**What**: The literal path prefix `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-00XX/spec.md` appears **56 times** (verified by grep). Declare a base path macro.

**Header addition**:
```html
<!-- ART=.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts -->
```

**Before** (line 25):
```
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0001/spec.md`
```

**After**:
```
- `$ART/D-0001/spec.md`
```

**Estimated saving**: Per occurrence, 59 chars → 5 chars = 54 byte save. 56 × 54 = **~3,024 bytes ≈ 5.2% file reduction** (header cost ~55 bytes already absorbed).

**Lossless / lossy**: Lossless (string substitution, reversible).

**Risk**: None — path substring is unique and cannot collide. The `$ART` convention must be documented in the header so a consumer LLM expands it mentally; primer §2.2 confirms the header "pays for itself" at ≥5-10 uses (here: 56).

---

### Strategy 5 — Workflow-phase marker abbreviation (Approach 2)

**Primer basis**: §4.2 transform 5 (auto-abbreviation of >5-occurrence phrases); §5 TASKLIST row example: "e.g., `[P1][B:task-42][>]`" — the primer explicitly endorses bracket-tag style abbreviation for tasklists.

**What**: The four bolded workflow markers `**[PLANNING]**`, `**[EXECUTION]**`, `**[VERIFICATION]**`, `**[COMPLETION]**` appear 36+64+27+27 = **154 times**. Drop the markdown bold and shorten to single-letter tags.

**Header addition**:
```html
<!-- [P]=PLANNING [E]=EXECUTION [V]=VERIFICATION [C]=COMPLETION -->
```

**Before** (T01.01 Steps, lines 33-39):
```
1. **[PLANNING]** Review TDD §7 Data Models for `UserProfile` schema ...
2. **[PLANNING]** Verify INFRA-DB-001 dependency is resolved ...
3. **[EXECUTION]** Create `UserProfile` table with all fields ...
4. **[EXECUTION]** Create audit log table with structured columns ...
5. **[EXECUTION]** Configure database connection pool ...
6. **[VERIFICATION]** Run schema validation: all columns exist ...
7. **[COMPLETION]** Document schema in evidence directory
```

**After**:
```
1. [P] Review TDD §7 Data Models for `UserProfile` schema ...
2. [P] Verify INFRA-DB-001 dependency is resolved ...
3. [E] Create `UserProfile` table with all fields ...
4. [E] Create audit log table with structured columns ...
5. [E] Configure database connection pool ...
6. [V] Run schema validation: all columns exist ...
7. [C] Document schema in evidence directory
```

**Estimated saving**:
- `**[PLANNING]**` (14 chars) → `[P]` (3 chars): 11 × 36 = 396
- `**[EXECUTION]**` (15) → `[E]` (3): 12 × 64 = 768
- `**[VERIFICATION]**` (18) → `[V]` (3): 15 × 27 = 405
- `**[COMPLETION]**` (16) → `[C]` (3): 13 × 27 = 351
- Total: **~1,920 bytes ≈ 3.3% file reduction**

**Lossless / lossy**: Lossless (header-declared substitution).

**Risk**: Minor — `[P]` must not collide with any existing bracketed literal in the body. Verified: no `[P]`/`[E]`/`[V]`/`[C]` standalone tokens elsewhere in the file (confidence bars use `[██...]`, not letters). Safe.

---

### Strategy 6 — Section-label abbreviation for task sub-blocks (Approach 2)

**Primer basis**: §4.2 transform 5; §2.3 "Abbreviable phrases ~10-15%".

**What**: Shorten the 7 repeated bold section labels that appear once per task (27×):

| Original | Short | Saving per hit |
|---|---|---:|
| `**Deliverables:**` | `**D:**` | 11 |
| `**Steps:**` | `**S:**` | 4 |
| `**Acceptance Criteria:**` | `**AC:**` | 17 |
| `**Validation:**` | `**Val:**` | 7 |
| `**Dependencies:**` | `**Dep:**` | 9 |
| `**Rollback:**` | `**RB:**` | 7 |
| `**Artifacts (Intended Paths):**` | `**Art:**` | 23 |

**Header addition**:
```html
<!-- D=Deliverables S=Steps AC=Acceptance Criteria Val=Validation
Dep=Dependencies RB=Rollback Art=Artifacts (Intended Paths) -->
```

**Before** (lines 24-32):
```
**Artifacts (Intended Paths):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0001/spec.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/artifacts/D-0002/spec.md`

**Deliverables:**
1. PostgreSQL 15+ instance with `UserProfile` table (id, email, ...)
2. Audit log table with 12-month retention policy ...

**Steps:**
```

**After**:
```
**Art:**
- `$ART/D-0001/spec.md`
- `$ART/D-0002/spec.md`
**D:**
1. PostgreSQL 15+ instance with `UserProfile` table (id, email, ...)
2. Audit log table with 12-month retention policy ...
**S:**
```

**Estimated saving**: Sum over 27 tasks: (11+4+17+7+9+7+23) × 27 = 78 × 27 = **~2,106 bytes ≈ 3.6% file reduction**.

**Lossless / lossy**: Lossless (header-declared substitution, primer §2.1 row 4).

**Risk**: `**AC:**` could be confused with an acronym if it appears inline in body text — verified only appears as section label. Safe with header gate.

---

### Strategy 7 — Checkpoint block template compression (Approach 2)

**Primer basis**: §4.2 transform 3 ("List compaction: convert multi-paragraph bullets into single-line bullets"); §4.2 transform 2 ("Table normalization … hoist into a caption").

**What**: The 6 checkpoint blocks follow an identical 4-field template (Purpose / Checkpoint Report Path / Verification / Exit Criteria). Shorten the labels using a second conventions-header line and collapse one-line bullets.

**Before** (lines 238-249, T01-T05 checkpoint):
```
### Checkpoint: Phase 1 / Tasks 01-05

**Purpose:** Verify infrastructure provisioning is complete before component implementation begins.
**Checkpoint Report Path:** `.dev/test-fixtures/results/test1-tdd-prd-v2/checkpoints/CP-P01-T01-T05.md`
**Verification:**
- PostgreSQL schema with all UserProfile columns and audit log table operational
- Redis cluster accessible with TTL operations verified
- Feature flags configured and toggleable in staging
**Exit Criteria:**
- All infrastructure dependencies resolved (INFRA-DB-001, SEC-POLICY-001)
- Local dev environment functional via Docker Compose
- No blocking issues for component implementation
```

**After** (with header declaring `P=Purpose CRP=Checkpoint Report Path V=Verification EC=Exit Criteria CP=$ART/../checkpoints`):
```
### CP: Phase 1 / Tasks 01-05
**P:** Verify infrastructure provisioning is complete before component implementation begins.
**CRP:** `$CP/CP-P01-T01-T05.md`
**V:**
- PostgreSQL schema with all UserProfile columns and audit log table operational
- Redis cluster accessible with TTL operations verified
- Feature flags configured and toggleable in staging
**EC:**
- All infrastructure dependencies resolved (INFRA-DB-001, SEC-POLICY-001)
- Local dev environment functional via Docker Compose
- No blocking issues for component implementation
```

**Estimated saving**: per-block label savings (~70 bytes) × 6 = ~420 bytes; path prefix savings already counted in Strategy 4. **~0.7% file reduction**.

**Lossless / lossy**: Lossless.

**Risk**: Negligible.

---

### Strategy 8 — Drop structural restatement from "Why / Acceptance Criteria / Validation / Notes" (Approach 2, bounded)

**Primer basis**: §4.2 transform 6 ("Prose summarization of introduction paragraphs (bounded, deterministic): if an `## Introduction` section restates content found verbatim later, elide the restated sentences"); §2.3 "Prose redundancy (restatement) ~8-15%".

**What**: Several tasks restate the same fact across `Why`, `Acceptance Criteria`, and `Validation` rows. Example from T01.06 (lines 256, 285-287, 291):

**Before** (fragments from T01.06):
```
| Why | Secure password hashing via bcrypt cost factor 12 per NFR-SEC-001. ... |
...
- Unit tests for hash/verify pass: `UT-001` (per TDD §15 Testing Strategy)
- bcrypt cost factor 12 confirmed in generated hash string
- Timing-invariant comparison: no measurable timing difference ...
...
- Manual check: Unit test `UT-001` passes with bcrypt cost factor 12 verified in hash output
```

The phrase "bcrypt cost factor 12 [verified/confirmed in hash output]" appears 3 times within a ~40-line span — pure restatement of the same fact for human reading.

**After**: Keep the assertion exactly once in `**AC:**` (the contractual field), elide from `Val:` where it restates.

```
**Val:** Unit test `UT-001` passes; evidence `$ART/D-0007/evidence.md`
```

**Estimated saving**: Applied conservatively across the 27 tasks where Validation restates AC (observed in ~20 of 27 tasks, averaging ~40 bytes saved per task): ~800 bytes. **~1.4% file reduction**.

**Lossless / lossy**: **Lossy for humans, lossless for LLM consumption** per primer §2.1 definition ("task-equivalent — the downstream agent's output is unchanged whether it reads the original or the compressed version"). Because the elided sentences are verbatim restatements, task-equivalence holds.

**Risk**: Primer §4.2 flags "cross-reference deduplication can break navigation for humans". Mitigation: this transform should be gated per-task with a diff reviewer; safer to apply only to clearly-verbatim restatements (not paraphrases). Also, the primer §4.2 deterministic-summarization rule requires that the content appear "verbatim later" — strictly enforce that gate.

---

### Strategy 9 — Value-set abbreviation for Tier / Effort / Risk columns (Approach 2)

**Primer basis**: §4.2 transform 2 ("Table normalization: detect repeated column values and hoist into a caption or eliminate via default"); §2.3 "Abbreviable phrases".

**What**: `Tier` takes only 3 values (STRICT=15, STANDARD=10, LIGHT=2). `Risk` takes 3 (High / Medium / Low). `Effort` takes 5 (XS/S/M/L/XL). These are already short — but combined with Strategy 3, the full row `| Tier | STRICT |` → `|Tier|STRICT|` benefits from pipe-collapse and can further use single-letter tier codes if header-declared.

**Header addition**:
```html
<!-- T1=STRICT T2=STANDARD T3=LIGHT -->
```

**Before**:
```
| Tier | STRICT |
```

**After**:
```
|Tier|T1|
```

**Estimated saving**: (STRICT→T1 saves 4; STANDARD→T2 saves 6; LIGHT→T3 saves 3): 15×4 + 10×6 + 2×3 = 60+60+6 = **~126 bytes ≈ 0.2% file reduction**. Small; include only if Approach 2 is already running.

**Lossless / lossy**: Lossless.

**Risk**: Very low, but this is borderline cost-effective — the savings barely exceed the header cost. Marginal inclusion.

---

### Strategy 10 — Heading normalization: single-dash task titles (Approach 1)

**Primer basis**: §4.1 transform 3 ("Normalize heading underline syntax → ATX"); §2.3 whitespace & formatting ceiling.

**What**: Task headings use the pattern `### T01.01 -- Provision PostgreSQL with UserProfile Schema and GDPR Fields`. The double-dash `--` is a humanizing separator with no semantic value. Replace with single dash, or drop entirely if task ID is followed immediately by title.

**Before**:
```
### T01.01 -- Provision PostgreSQL with UserProfile Schema and GDPR Fields
```

**After**:
```
### T01.01 Provision PostgreSQL with UserProfile Schema and GDPR Fields
```

**Estimated saving**: 4 bytes × 27 tasks = **~108 bytes ≈ 0.2% file reduction**. Trivial, but free.

**Lossless / lossy**: Lossless.

**Risk**: None.

---

## 3. Recommended Strategy Stack

Per primer §5 composition rule 1 ("Always run Approach 1 first"), I order rule-based transforms before AST transforms. Per primer §5 TASKLIST row prescription, Approach 2 with auto-conventions-header is the core technique.

### Ordered pipeline

| Step | Strategy | Approach | Est. saving | Cumulative | Lossless? |
|---:|---|---|---:|---:|---|
| 1 | S1  Whitespace normalization | A1 | 1.8% | 1.8% | Y |
| 2 | S2  Pipe-table padding collapse | A1 | 2.9% | 4.7% | Y |
| 3 | S10 Heading `--` cleanup | A1 | 0.2% | 4.9% | Y |
| 4 | S3  Auto-conventions-header for field labels | A2 | 7.8% | 12.7% | Y |
| 5 | S4  Artifact-path prefix macro | A2 | 5.2% | 17.9% | Y |
| 6 | S5  Workflow-phase marker abbreviation | A2 | 3.3% | 21.2% | Y |
| 7 | S6  Section-label abbreviation | A2 | 3.6% | 24.8% | Y |
| 8 | S7  Checkpoint block template | A2 | 0.7% | 25.5% | Y |
| 9 | S9  Tier value abbreviation (marginal) | A2 | 0.2% | 25.7% | Y |
| 10 | S8  Prose restatement elision (gated) | A2 | 1.4% | **27.1%** | Lossy-to-humans, lossless-to-LLM |

### Projected total compression

**Conservative projection**: **~25% file reduction (≈14.7 KB saved, 58,653 → ~43,900 bytes).**

**Aggressive-but-defensible projection** (with Strategy 8 applied across all 20 restatement-heavy tasks rather than conservatively): **~30-32%.**

### Rationale for landing below the 30-40% target

The primer §5 target for tasklists is 30-40%. This file is somewhat below mid-range because:

1. **The 14-row metadata tables are already dense** — they use minimal prose per cell. The biggest win is abbreviating field *labels*, not values. Label-only compression caps the table savings.
2. **Task prose is unusually concrete** — `Deliverables`, `Steps`, `Acceptance Criteria` contain substantive content, not restatement. Approach 3 (LLM rewriting) could push this higher, but primer §5 TASKLIST row explicitly says "LLM rewriting offers no marginal gain" for tasklists. Respecting that guidance.
3. **No code fences** means no protective dead weight, but equally no fenced sections where Approach 1 gets free wins by collapsing surrounding whitespace aggressively.

**To reach 33-36%** (matching V-B's measured -33.4% reference point): a tighter Strategy 8 pass that identifies cross-task prose overlap (e.g., the identical 4-step PLANNING/EXECUTION/VERIFICATION/COMPLETION flow structure) and synthesizes a shared template header would add ~4-6 percentage points. This is a stronger version of primer §4.2 transform 6 and should be considered a stretch goal, gated by a round-trip test.

### Compliance with primer §5 composition rules

- **Rule 1** (Approach 1 first): satisfied — steps 1-3 are rule-based.
- **Rule 2** (Code fences sacrosanct): satisfied trivially — no code fences in the file.
- **Rule 3** (Run Approach 2 when structural regularity > prose density): satisfied — the file is ~78% structured (tables + templated sections).
- **Rule 4** (Approach 3 only when Approach 2 exhausts gains and prose density is high): not triggered; primer explicitly deprecates A3 for tasklists.
- **Rule 6** (Auditor gate for lossy transforms): Strategy 8 requires a diff-reviewer gate; recommend golden-file round-trip test + spot-check.
- **Rule 7** (Conventions header amortization ≥5 reads): header keys all have 27-154 body uses. Strongly amortized; header is cheap insurance.

---

## 4. Risks & Caveats Specific to This File

### 4.1 Tokenizer uncertainty (INV-1)

Primer §6 carries forward INV-1: all byte/char savings above are proxies for token savings. The actual token reduction under Claude's native tokenizer may drift by ±2-8 percentage points. Byte counts here are presented as the *first-order* estimate; before relying on the 27% figure for pipeline decisions, re-measure with Anthropic `messages.count_tokens`.

### 4.2 Conventions-header drift risk

Eight strategies add entries to the conventions header. The full header is estimated at ~600 chars (~150 tokens). Primer §2.2 assumes "~40-60 tokens"; this file pushes past that budget. Justification: §2.2 says the header "pays for itself after roughly 5-10 body uses of each abbreviation" — every abbreviation here has ≥5 uses (most have 27+), and the path-prefix macro alone (56 uses) pays for the entire header three times over. But:

- **If the tasklist is read once per sprint** (not per-task-execution), header amortization is still fine (27 task blocks per read).
- **If the tasklist is read sub-section by sub-section** via a tool like `Read offset=… limit=…`, the header at line 1 may be outside the read window and the abbreviations become opaque. This is the INV-3 "consumer DAG unmapped" risk carried forward from primer §6. Mitigation: either (a) emit the header redundantly at the start of every 200-line chunk, or (b) limit Approach 2 transforms to only those whose abbreviations are self-describing in context (e.g., `[P]` less safe than `**D:**` for "Deliverables" because the latter has a visible colon-delimited label).

### 4.3 Value-column collisions (Strategy 3)

Approach 2 auto-abbreviation must guard against value-level collisions. Example: `| Fallback Allowed | No |` — the abbreviation `FA` for the label is fine, but `No`/`Yes` values must NOT be abbreviated further because they collide with English prose elsewhere. Verified that Strategy 3 only abbreviates labels and value-strings that are uppercase acronyms (`SQS`, `QE`) with no English-prose collision.

### 4.4 Round-trip testing is mandatory for Approach 2 steps

Primer §4.2 "Determinism ★★★★☆" warns that serializer round-trips must be golden-tested. Given this file has 27 tasks with identical schema, a round-trip test is easy to write: parse → abbreviate → expand → parse → AST-diff should be empty. This should be a prerequisite to applying Strategies 3-9 in any automated pipeline.

### 4.5 Strategy 8 is the primary lossy gate

Of all 10 strategies, only Strategy 8 (prose-restatement elision) is potentially lossy. Primer §2.1 distinguishes "task-equivalent lossless" from byte-lossless, and Strategy 8 sits on that boundary. **Recommendation**: apply Strategy 8 only with an auditor-pass safeguard (primer §5 rule 6), even though Approach 2 usually doesn't need one — the risk is minimal per occurrence but aggregates across 27 tasks.

### 4.6 Human-readability impact

This file is likely read by human reviewers during sprint planning and task execution. After full compression, raw readability drops noticeably — `**D:**` and `[P]` are opaque without the header. Mitigations:

- Keep an uncompressed copy alongside the compressed one for humans; only feed the compressed version to LLM consumers. Primer §1 says compressed MD DSL is "fully reversible to human-readable Markdown via the conventions header plus a decompressor" — build that decompressor and make it one command.
- Alternatively, apply only Strategies 1, 2, 4, 5, 10 (the safest subset) for a ~13% reduction that preserves human reading. This sacrifices the 30-40% target but stays in "human-auditable" territory, matching primer §5's SPEC row philosophy ("fidelity > savings").

### 4.7 Known gap: no empirical tokenization here

All percentages above are **character/byte estimates**, not tokenizer-measured. Before this analysis flows into the compression pipeline design, the top-3 strategies (S3, S4, S5) should be spot-measured with `tiktoken` to calibrate the proxy. Expected reliability: char-count ↔ token-count correlate at ~0.85-0.95 for structured Markdown, so the 27% figure should land within ±4 percentage points of the true token saving.

---

## Summary

| Question | Answer |
|---|---|
| Primer strategy row applied | §5 TASKLIST → Approach 2 (AST) + auto-conventions-header |
| Strategies identified | 10 (3 rule-based, 7 AST-aware) |
| All strategies grounded in primer? | Yes — each cites §4.1, §4.2, §2.2, §2.3, or §5 |
| Projected compression | **~25% conservative / ~30-32% aggressive** |
| Primer target (30-40%) met? | Low-end of target with aggressive stack; below target with conservative stack |
| Losses introduced? | Only Strategy 8 is lossy (human-facing); all others lossless including for LLM |
| Code-fence risk | None — file has zero code fences |
| Recommended next step | Round-trip test (S3-S9) on one task block before full-file application; re-measure with Claude-native tokenizer |
