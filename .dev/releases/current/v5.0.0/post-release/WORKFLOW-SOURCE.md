# Source spec: apply the /sc:post-release v5.0.0 consolidated plan (Wave 4 writers)

**What:** update and create IronClaude's external-surface artifacts for the shipped 5.0.0 release, exactly as itemized in
`.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md` (the gated, consolidated output of the post-release
scanners; read it in full; it carries per-item doc line → corrected statement → code evidence).

**Why:** `/sc:post-release v5.0.0` (ground-up run) found 70 fix-this-run gaps across user docs, technical docs and install
docs, and no human test guides exist. The release's docs must agree with the tagged code (v5.0.0 = d953b983).

## In scope (every item)

1. **Writer worklist, Workstream A** — items A-W1 … A-W22 (section "Writer worklist" → "Workstream A"), including the new
   `docs/user-guide/codegraph.md` (A-W22). A-W3 edits `src/superclaude/core/HOW-WE-WORK.md` and its byte-identical mirror
   `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (and the repo CLAUDE.md note about re-running the
   level-table copy applies if the level table changes; it should not).
2. **Writer worklist, Workstream B** — items B-W1 … B-W22, including the four new technical notes under
   `docs/developer-guide/` (B-W19 codegraph-integration.md, B-W20 session-memory.md, B-W21 review-severity-rule.md,
   B-W22 release-procedure.md). B-W1 edits `src/superclaude/rules/core/changelog_maintenance.md` (an installed primitive).
3. **Writer worklist, Workstream C** — items C-W1 (docs/getting-started/installation.md), C-W2
   (docs/user-guide/mcp-installation.md), C-W3 (new docs/getting-started/upgrading.md). The verified install/upgrade
   evidence is the Workstream C e2e transcript `docs/testing/v5.0.0/c-e2e-transcript.txt` (GREEN, new user and
   4.3.5→5.0.0 upgrade) and `docs/testing/v5.0.0/c-e2e-run.sh`.
4. **Workstream D** — 16 user-facing human-test guides `docs/testing/v5.0.0/user/D01-…md` … `D16-…md` exactly as listed
   in "Test guide plan (D and E)", each built from `~/.claude/skills/sc-post-release-protocol/templates/user-test-guide.md`
   (Read the template; every expected result cites real code file:line, `--help` output or the e2e transcript; anything
   not derivable is marked UNVERIFIED; every step carries its cost tag `[FREE]`/`[LOCAL-WRITE]`/`[CLAUDE-SESSION]`/
   `[API-LONG]`/`[PROXY]`/`[EXTERNAL]`). Code-derived inputs live in `.dev/releases/current/v5.0.0/post-release/scan/`
   (DE1-cli-surface.md, DE2-claude-surface.md, C-install-surface.md, A2-feature-user-docs.md).
5. **Workstream E** — 2 sysop guides `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` and
   `E02-ccsession-model-data-publishing.md` from `templates/sysop-test-guide.md`, with the gate evidence listed in the plan.
6. `docs/testing/v5.0.0/README.md` — index of D01-D16 and E01-E02 with cost tags, plus pointers to the e2e transcript and
   script.

## Out of scope (do not do)

- Deferred gaps 71-84 and the out-of-scope code findings O1-O22 (no code changes; no issue filing in this plan).
- `docs/releases/v5.0.0.md`, `CHANGELOG.md` (published record), the GitHub release, the tag.
- `post-release-report.md` and `post-release-manifest.json` (the post-release orchestrator writes them after this plan).

## Constraints

- Match on quoted text, not on scan line numbers (lines are from d953b983).
- After editing anything under `src/superclaude/` or `plugins/`, run `make sync-dev` and `make verify-sync`; never stage
  `.claude/` (only `.claude/settings.json` is tracked). No `src/superclaude/...` paths inside installed primitives.
- Repo is a fork: every `gh` call uses `--repo IronbellyOrg/IronClaude`; issue links point at IronbellyOrg/IronClaude.
- Do not run installs against the real `~/.claude`, real pipx, or running ccsession shims.
- Verification per item: re-read the edited/created file against its plan item and the cited code; markdownlint
  (`make lint` covers markdown via pre-commit config if configured; otherwise `npx markdownlint-cli2` per repo config)
  and the repo's doc/primitive tests (`uv run pytest tests/ -q -k "doc or primitive or how_we_work or severity"` as a
  smoke, then the full `make test` once at the end).
- Commit nothing in this plan; the orchestrator commits and opens one PR with `/sc:pr-submit --monitor 3`.
