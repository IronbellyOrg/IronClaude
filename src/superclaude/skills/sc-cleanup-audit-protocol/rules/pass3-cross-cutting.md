# Pass 3: Cross-Cutting Sweep Rules

## Goal

Find duplication, sprawl, and broken references spanning directory boundaries — problems per-directory audits inherently miss. Requires diff/overlap quantification.

## Guiding Question

**"Does this file duplicate or conflict with another file elsewhere in the repo?"**

## Scope rule (inherited from `repo-inventory.sh`)

You will only ever receive in-scope paths in your batch — the orchestrator
applies the default exclusion filter (`^\.` for hidden, `^_bmad/`,
`^_bmad-output/`, `^_planning-input/` for BMAD) before sharding. **Do not
compare against or classify any path that starts with `.` or one of the
BMAD prefixes**, even if it appears in your duplication/overlap analysis
as a candidate. Such paths are legitimate cross-references but are managed
outside the cleanup audit and must not be flagged as duplication targets.

When you grep for duplicate content across the repo, hidden and BMAD paths
MAY appear as siblings (e.g. `.dev/research/foo.md` may mirror `docs/foo.md`).
Noting them in cross-cutting commentary is fine — they just don't get
proposed for consolidation or deletion themselves.

---

## Extended Classification Taxonomy

| Category | Meaning | Action | Evidence Required |
|----------|---------|--------|-------------------|
| DELETE | Confirmed dead | Remove | Grep proof + no dynamic loading |
| CONSOLIDATE | Merge with identified similar file | Keep canonical, merge unique parts | Both files read + overlap quantified + canonical chosen |
| MOVE | Valid but wrong location | Relocate | Target rationale + refs to update |
| FLAG | Needs code changes | Developer action | Issue + specific action + impact scope |
| KEEP | Verified unique purpose with evidence | Leave in place | Reference citation |
| BROKEN REF | References non-existent paths | Fix reference | Source file:line → missing target |

## Per-File Profile (7 Fields — ALL REQUIRED)

| # | Field | Requirement |
|---|-------|-------------|
| 1 | **What it does** | 1-2 sentence explanation |
| 2 | **Nature** | File type classification |
| 3 | **References** | Grep results with files + line numbers |
| 4 | **Similar files** | Other files serving same/overlapping purpose; quantify % overlap or key differences |
| 5 | **Superseded?** | Newer/better version exists? |
| 6 | **Currently used?** | Referenced by running app, CI/CD, build? Evidence required |
| 7 | **Recommendation** | DELETE / CONSOLIDATE (with what) / MOVE / FLAG / KEEP |

## 6 Critical Differentiators from Pass 2

1. **Compare, don't just catalog**: When similar files found, DIFF them and quantify overlap percentage. State "X and Y are 80% identical, differing in sections A, B"
2. **Group audit**: Audit similar files together — all docker-compose files, all deploy scripts, all playwright configs. Compare within the group
3. **Mandatory duplication matrix**: Produce a matrix for compose/deploy/tests/configs with overlap percentages (see format below)
4. **Already-known issues list**: Receive all findings from Passes 1-2 as context. Note "Already tracked as issue #N" and move on — do not re-flag
5. **Auto-KEEP for previously audited source**: Do not re-audit files already deep-profiled in Pass 2. Focus on cross-cutting relationships only
6. **Directory-level assessments**: For directories with 50+ files, use strategic sampling (10-15 representative files) with directory-level assessment

## Focus Areas

- Multiple docker-compose / Dockerfile / deploy scripts
- Config and .env file proliferation
- Root-level clutter (files that belong in subdirectories)
- Cross-directory duplication (same file type in multiple directories)
- Stale artifacts from old architecture

## Tiered P3 Depth Strategy

| Tier | Target | Depth | Est. Files |
|------|--------|-------|-----------|
| **Deep** (per-file profile) | Root configs, infrastructure, CI/CD, deploy scripts | Full 7-field profile per file | ~200 files |
| **Medium** (directory assessment + sampling) | Source code directories | Sample 10-15 per dir, directory-level assessment | ~800 files |
| **Light** (reference-grep only) | Assets, documentation, generated files | Reference check only, no content analysis | ~400 files |

## Mandatory Duplication Matrix Format

```markdown
## Duplication Matrix

| File A | File B | Overlap % | Key Differences | Recommendation |
|--------|--------|-----------|-----------------|----------------|
| docker-compose.yml | docker-compose.dev.yml | 85% | Dev adds debug ports, volume mounts | CONSOLIDATE with env-based switching |
| deploy.sh | deploy-prod.sh | 70% | Prod adds backup step, different target | FLAG: extract shared logic |
```

The duplication matrix is **mandatory** when similar files are detected. Pass 3 is not considered complete without it.

## Incremental Save Protocol

Save after every 5-10 files. Never accumulate more than 10 unwritten results.
