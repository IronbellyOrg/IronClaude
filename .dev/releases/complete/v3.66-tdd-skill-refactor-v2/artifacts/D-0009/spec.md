# D-0009: Tier Selection Table Migration Evidence

**Task:** T03.02 -- Migrate Tier Selection Table from SKILL.md to Command File
**Date:** 2026-04-05
**Roadmap Item:** R-009
**Requirement:** FR-TDD-CMD.2b

---

## 1. Source Content (from D-0004 Baseline, Block B: Lines 82-88)

```markdown
Match the tier to component scope. **Default to Standard** unless the component is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Bug fixes, config changes, small features (<1 sprint), <5 relevant files | 2–3 | 0–1 | 300–600 |
| **Standard** | Most features and services (1-3 sprints), 5-20 files, moderate complexity | 4–6 | 1–2 | 800–1,400 |
| **Heavyweight** | New systems, platform changes, cross-team projects, 20+ files | 6–10+ | 2–4 | 1,400–2,200 |
```

## 2. Destination

**File:** `src/superclaude/commands/tdd.md`
**Section:** Options → Tier Selection Reference (subsection after Options table)
**Location:** Lines 53-60 (after `--from-prd` row, before Behavioral Summary)

## 3. Verification Results

| Check | Pattern | Line | Status |
|-------|---------|------|--------|
| Header row | `Tier \| When \| Codebase Agents \| Web Agents \| Target Lines` | 56 | PASS |
| Lightweight row | `Lightweight.*Bug fixes.*2–3.*0–1.*300–600` | 58 | PASS |
| Standard row | `Standard.*Most features.*4–6.*1–2.*800–1,400` | 59 | PASS |
| Heavyweight row | `Heavyweight.*New systems.*6–10+.*2–4.*1,400–2,200` | 60 | PASS |

**All 4 checks passed.** Table header and all 3 data rows present in command file with all 5 columns intact.

## 4. Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| Lightweight tier row with all 5 columns in command file | PASS |
| Standard tier row with all 5 columns in command file | PASS |
| Heavyweight tier row with all 5 columns in command file | PASS |
| Table header row present in command Options section | PASS |

---

**Result:** Migration complete. Tier selection table (7 lines) copied from SKILL.md lines 82-88 into command file Options section as `--tier` reference material per FR-TDD-CMD.2b.
