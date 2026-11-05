# Wave 1.5 Branch A (release docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

- release_slug: none (section 15 adds a CHANGELOG [Unreleased] entry, no version bump; source.md:1448, :1458)
- artifact_paths: [.dev/tasks/done/TASK-WF-design-20261104-164423/source.md, .dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md, .dev/brainstorms/issue-305-pr-submit-conflict-resolution/adversarial/debate-transcript.md, .dev/brainstorms/issue-305-pr-submit-conflict-resolution/adversarial/round-inv-advocate-A.md]
- summary (citations are source.md unless named):
  1. "untrusted", "security", "threat", "malicious", "credential", "build backend", "backend-path" never appear; "sandbox" once (:1440), meaning the V4 test repository.
  2. DEFAULT_CONFLICT_MAX_TIER = 1 (:602, :67, :1461); OQ-1 (:1139) picks 1 to keep model-resolved merges off, says nothing about code execution.
  3. Fixed rule `MechanicalRule("uv.lock", ..., ("uv","lock"), ("uv","lock","--check"))` (:465; R-189 at :1274); OQ-6 seeds from the PR side then runs `uv lock` (:1144).
  4. UV_OFFLINE=1 cited only for hermetic tests (:129).
  5. Risk table section 16 (:1473-1483): K3 (:1478) "`uv lock` needs the network or moves unrelated pins"; no row for PR-controlled PEP 517 backends or path/editable sources; K8 (:1479) calls Tier 1 "mechanical".
  6. OQ-31 (:1169) treats the tracked pyproject.toml as safe; OQ-10 (:1148) sends a conflicted pyproject.toml to Tier 2, so a clean-merging malicious pyproject.toml with a conflicted uv.lock stays in Tier 1.
  7. merged-requirements.md:839: cross-repo heads are report-only (a push rule, not an execution rule); same-repo branches by other authors are not covered.
  8. debate-transcript.md:287, round-inv-advocate-A.md:11: "sandbox" means a test repository.
  9. INV-033 (:119, :1482): uv.lock is gitignored in this repo, so Tier 1 never runs here and the risk cannot appear in local runs.
- confidence: 0.85
- consistency: the design has no security rule; the fix adds a new trust boundary rather than contradicting one.
