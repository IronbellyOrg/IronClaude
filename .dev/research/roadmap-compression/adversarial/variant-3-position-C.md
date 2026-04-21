# Position C: Normalized Table Format with Inline Diff Markers

## Strategy

Normalize both roadmaps into an identical table schema:
1. **Extract** all task rows into a unified TSV/CSV format with fixed columns
2. **Compress** acceptance criteria into keyword tags
3. **Strip** all markdown formatting, prose sections, and narrative content
4. **Normalize** field names and values for direct line-by-line comparison

## Compression Mechanics

### Step 1: Schema Normalization

Both roadmaps use similar but not identical table schemas:

Opus columns: `# | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority`
Haiku columns: `# | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority`

Normalized output schema:
```
PHASE\tROW\tID\tTASK\tCOMPONENT\tDEPS\tAC_TAGS\tEFFORT\tPRIORITY\tMILESTONE
```

### Step 2: Acceptance Criteria Compression

Transform verbose AC prose into keyword tags:

**Before** (Opus, row 18):
> Valid creds → 200 with AuthToken; invalid → 401; non-existent email → 401 (no enumeration); locked → 423 after 5 failures in 15 min

**After**:
> `200:valid|401:invalid|401:no-enum|423:lockout-5-15min`

**Before** (Haiku, row 1 Phase 2):
> Valid credentials return 200 with `AuthToken`; invalid/non-existent email returns generic 401; failed-attempt tracking supports lockout rule

**After**:
> `200:valid|401:generic|lockout-tracking`

### Step 3: Non-Table Content Extraction

Non-table sections compressed to metadata header:

```tsv
# META
source\troadmap-opus-architect.md
total_rows\t181
phases\t6
milestones\tM1,M2,M3,M4,M5
complexity\t0.72:HIGH
target_release\tv1.0
exec_summary\tJWT dual-token auth, bcrypt-12, RS256, 3-phase rollout, SOC2/GDPR
risks\tR-001:XSS:Med:High|R-002:bruteforce:High:Med|R-003:migration:Low:High
critical_path\tINFRA-DB-001→DM-001→COMP-005→COMP-001→FR-AUTH-001→M1→COMP-003→COMP-002→FR-AUTH-003→M2→FR-AUTH-005→M3→COMP-006→M4→MIG-001→M5
timeline\tP1:2026-04-01/04-14:2w|P2:04-15/04-28:2w|P3:04-29/05-26:4w|P4:05-27/06-02:1w|P5:06-03/07-07:5w|P6:05-27/07-07:cont

# INTEGRATION_POINTS
AuthService_DI\tTokenManager,PasswordHasher,UserRepo\tP1\txref:P2
Auth_Router\tlogin,register,me,refresh,reset-req,reset-confirm\tP1\txref:P2,P3
Bearer_Middleware\tJwtService.verify\tP2\txref:P3
AuthProvider_Context\tLoginPage,RegisterPage,ProfilePage\tP3\txref:P4
Feature_Flags\tAUTH_NEW_LOGIN,AUTH_TOKEN_REFRESH\tP5\txref:P5
Rate_Limit\t10/min/IP:login,5/min/IP:register,60/min/user:me,30/min/user:refresh\tP1\txref:P2,P4

# TASKS
PHASE\tROW\tID\tTASK\tCOMPONENT\tDEPS\tAC_TAGS\tEFFORT\tPRIORITY
1\t1\tAUTH-001-TDD\tBaseline TDD\tDocumentation\t-\treview:auth-team|baseline:complete\tS\tP0
1\t2\tAUTH-PRD-001\tPRD traceability\tDocumentation\tAUTH-001-TDD\t5-FR-pairs:mapped|no-orphans\tS\tP0
1\t3\tSEC-POLICY-001\tSecurity policy review\tSecurity\tAUTH-001-TDD\tbcrypt:12|RS256:2048\tS\tP0
1\t4\tINFRA-DB-001\tProvision PostgreSQL 15+\tInfrastructure\t-\tpg-pool:100|connection:verified\tM\tP0
...
```

### Step 4: ID Normalization

Haiku uses additional ID categories not in Opus:
- JTBD-001, PERSONA-001, STORY-001, JOURNEY-001, ERROR-001
- These are normalized with a `[PRD]` tag to distinguish from technical IDs

## Estimated Compression

- Opus: 60KB → ~18-21KB (65-70% reduction)
- Haiku: 76KB → ~22-26KB (65-70% reduction)
- Combined for diff: ~40-47KB (from 136KB)

## Strengths

1. **Trivial line-by-line diff** — normalized TSV with identical column order makes standard diff tools work perfectly
2. **Merge-friendly** — TSV rows can be merged with standard tools (sort, join, paste)
3. **Acceptance criteria preserved semantically** — keyword tags retain the WHAT if not the HOW of each criterion
4. **Sortable and filterable** — phase/effort/priority columns enable quick filtering
5. **Deterministic** — same input always produces same output
6. **Independent compression** — no cross-file dependency
7. **Integration points preserved** — structured format with wired components and cross-references

## Weaknesses

1. **AC keyword extraction is lossy and subjective** — different extractors may produce different tags for the same prose
2. **Prose nuance lost** — "no user enumeration" compressed to `no-enum` loses the security rationale
3. **Non-standard format** — original markdown cannot be reconstructed from TSV
4. **Narrative sections severely compressed** — risk mitigations become single keywords
5. **Structure normalization may lose model-specific organization** — Haiku's per-phase integration points flatten into the same format as Opus's separate section
6. **AC tag vocabulary is unbounded** — without a controlled vocabulary, tags across files may not align (e.g., `401:invalid` vs `401:generic` for the same concept)

## Diff Behavior

The diff tool sees:
- Rows that exist in one file but not the other (clear: added/removed tasks)
- Rows with same ID but different fields (clear: changed effort, priority, deps)
- Rows with same ID but different AC tags (visible but potentially misleading due to vocabulary mismatch)
- Metadata differences (clear: different totals, different timelines)
- BUT: cosmetic differences in AC tag extraction create false positives in diff output

## AC Tag Vocabulary Problem

The biggest challenge: when Opus says "valid creds → 200 with AuthToken" and Haiku says "Valid credentials return 200 with AuthToken", these should produce the SAME tag. But without a controlled vocabulary, the extraction might produce:
- Opus: `200:authtoken:valid-creds`
- Haiku: `200:authtoken:valid-credentials`

These look different in a diff even though they mean the same thing. This creates **false-positive diff noise** that undermines the purpose of compression.

Possible mitigation: Use a stemming/lemmatization step on AC tags, or define a controlled vocabulary specific to auth roadmaps. But this adds complexity and domain-specificity.
