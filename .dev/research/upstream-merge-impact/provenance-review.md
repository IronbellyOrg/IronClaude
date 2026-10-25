# Research: Independent upstream provenance and scope review

- **Topic type:** Adversarial evidence review
- **Scope:** Git enumeration, upstream attribution, unit assignment, date boundaries and reversal-check labeling only
- **Status:** Complete
- **Date:** 2026-10-23
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md
- **Verdict:** PASS

---

## Findings

### Independent enumeration and attribution

[CODE-VERIFIED] Independently traversing all 973 reachable commits, then filtering UTC committer timestamps rather than using a prunable date-limited walk, finds 679 commits in the requested window. There are exactly two reachable in-window merge subjects naming SuperClaude-Org, with the expected first and second parents: `0ceb2955` and `1e8c6e16`. Their upstream ancestry contains exactly 47 in-window commits, and every one matches the inventory. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:2-38`.

[CODE-VERIFIED] The original fork commit's parent is `ad6b2e99`. Forty-five of the 47 upstream commits are already in that base ancestry. The only later additions are `55c658c7` and `b061b2f7`, matching the February and March named merges. The merge net paths are respectively the MCP installer and the two sync workflow/script paths, so the two importing merge records must not be counted as two additional independent patches. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:306`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:363-390`.

[CODE-VERIFIED] All five reachable bot-authored commits in the window are the five requested framework syncs: `465797ad`, `ff5f73ad`, `ec9f066f`, `66d54204`, and `f14f0cca`. The inventory has no missing or extra bot-sync hash. The 47 original commits include 27 authored by mithun50. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:33-36`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:65-125`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:368-379`.

[CODE-VERIFIED] The only non-Ironbelly-domain authors outside upstream ancestry and the five sync commits are the two Claude-authored fork additions, `93cb9758` and `51a8e118`. Their exact parent links and commit subjects match fork development rather than either upstream parent chain. A scan of all non-upstream commit bodies finds no cherry-pick attribution trailer. This supports the stated local ancestry-based classification without pretending that an author name establishes origin. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:39-64`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:289`.

[CODE-VERIFIED] All 54 unique Git records (47 upstream commits, five bot syncs, two importing merges) are assigned exactly once, with no missing commit or duplicated assignment. Independently recomputing every parent-to-commit default path list finds no mismatch with the unit manifest. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:35-38`.

### Resolved rename-source omission

[CODE-VERIFIED] Git's default name-only list omitted the old endpoint of a rename from the architecture-migration group's per-unit count. The correction is materialized in `endpoint-inventory.json`: the group's complete old/new endpoint count is **269**, not the original manifest's 268, adding `docs/User-Guide/mcp-installation.md`. An independent no-renames, NUL-delimited path comparison confirms all eight complete endpoint manifests exactly. The repository-wide union remains **563** paths because that old endpoint was already represented by the MCP unit. No other group has an omitted endpoint. Evidence: `.dev/research/upstream-merge-impact/endpoint-summary.txt:1-15`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:310-362`. The final table must use 269 and identify the endpoint manifest as the complete historical path list.

### Window and pending-ref boundary

[CODE-VERIFIED] Normalizing both author and committer timestamps to UTC produces no selected-commit window discrepancy in either direction. The local repository is not shallow. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:127-128`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:381`.

[CODE-VERIFIED] The pending sixth sync, `d3cf5938`, is an ancestor of the recorded `origin/sync/framework` but of neither HEAD nor recorded `origin/master`. It is correctly kept outside the five landed imports. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:307-309`.

### Strict patch checks are not true reverts

[CODE-VERIFIED] The check implementation only feeds each parent-to-commit binary diff to `git apply --reverse --check`; it does not invoke a revert or change source. Every stored result expressly labels actual Git revert behavior UNVERIFIED. There are five successful strict checks, 48 unsuccessful strict checks, and one empty-input result. The return code 128 for `67449770` means its tree patch is empty, not a source conflict or missing dependency: there is no content change to reverse. A failed strict check does not prove a three-way revert would conflict; a successful strict check does not prove a reversal is safe. Evidence: `.dev/research/upstream-merge-impact/prepare_units.py:30-36`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:290-304`.

### Self-Audit

[CODE-VERIFIED] Checked full reachable history rather than only merge subjects; case-insensitive named-merge search; base ancestry versus post-fork imports; all bot-authored commits; external-author candidates; cherry-pick trailers; author and committer UTC boundaries; all 54 unique assignments; every per-commit path list; every old/new endpoint with renames disabled; HEAD versus both recorded remote refs; and the empty-patch exception. The computed mismatch lists are empty and every complete endpoint manifest matches. This PASS applies only to provenance, assignment and method labeling, not to the still-running architecture decisions or their source citations. Evidence: `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:2-38`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:127-128`, `.dev/research/upstream-merge-impact/provenance-audit-evidence.json:289-390`.

## Gaps

[UNVERIFIED] Ancestry and preserved attribution cannot rule out an upstream patch copied manually into a fork-owned commit with no provenance marker, rewritten authorship, or unmarked cherry-pick. The complete local subject/body scan found no cherry-pick trailer, but this is bounded negative evidence, not cryptographic proof of absence. Remote history newer than the recorded refs, deleted/unavailable remote branches and GitHub account identity were not fetched or independently authenticated.

[UNVERIFIED] Actual three-way Git revert behavior, post-reversal tests and a combined reversal sequence remain unexecuted because no reverts or repository mutation are authorized. The empty patch `67449770` must be described as a no-content change, not included among strict-check conflicts. The unit analyses and final synthesis were deliberately outside this review's scope.

## Key Takeaways

**PASS.** No unresolved defect was found in local upstream enumeration or assignment after incorporating the corrected rename-endpoint manifest. The verified scope is 47 original upstream commits, five landed bot syncs, and two merge records, grouped into eight units, covering 563 unique historical path endpoints. Use 269 endpoints for the architecture migration unit, retain the pending sixth sync outside the landed count, and keep actual revert applicability labeled UNVERIFIED.
