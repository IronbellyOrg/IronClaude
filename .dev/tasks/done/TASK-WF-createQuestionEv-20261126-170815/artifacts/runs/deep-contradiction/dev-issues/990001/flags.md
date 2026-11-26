<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (flags-user.md) -->
# Flags decision

- Decided by: user (taken as given); issue-worker-t1 independently agreed on every value (deep adversarial compare, no disagreement)
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | bug | passed as `--mode bug`; issue-worker-t1 chose bug independently (a crash is broken behaviour). Note from issue-worker-t1: the named crash site `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` does not exist (scripts/ holds only `clickup_claim.py`, `origin_repo.py`, `orca_worktree.py`) |
| Type | skill | passed as `--type skill`; issue-worker-t1 chose skill independently (the create flow is defined by the sc-issue-protocol skill, `refs/create.md`) |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |
