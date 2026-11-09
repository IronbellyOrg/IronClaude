# Self-review of fix F1 (review 1 of at most 3)

Lens: self-review (troubleshoot-analyst); persisted by parent at 2026-11-07T07:49:32Z. Raw verdict: **FAIL** (4 findings; maps to a documented blocker for F1 as originally worded).

## Findings (condensed; quotes as returned)

1. README overlap: no contradiction, but F1 would sit beside README line 241 ("`Default` (Orca, IronClaude, BMad, core MCP servers; pre-selected)") and line 308 (`bmad-planning/ # cloned the same way`), which read as if BMad works everywhere; F1 did not say it edits them. The same BMad text already lives at catalogue/bmad/manifest.yaml:12-14, so a README copy can drift.
2. CI pins: no contract test reads templates/VSCode-AIDev02/README.md (test-52-browser-usability-evidence.sh:1418 reads the catalogue README). Caveats: .github/upstream-monitor/releases.json:113 anchors on "upstream GitHub CLI release v" in the template README (not confirmed in the README by the reviewer); markdownlint.yml lints **/*.md on PRs; .markdownlint-cli2.yaml not read.
3. F1 documents the status quo; it fixes none of the three asks (global BMAD declined by owner-decisions.md:5; first-use creation left to a future owner decision; Ponytail only documented, diagnosis UNDETERMINED). "Consensus on the remediation" overstated; the issue could be closed as fixed by mistake; the reporter's environment is "Not known yet" (.dev/issues/478/issue-body.md:7-8,20) and F1 does not ask for it.
4. The README claim "Ponytail via the ironclaude slug, Default profile only" is an unverified inference: only docs/operations/upstream-monitor.md:62 names Ponytail; ironclaude/install.sh:139 is a code comment; the manifest never mentions Ponytail. "Default profile only" is also incomplete: profiles.yaml:22-23 describes a Custom selector that composes the active set from picked slugs.

## Root-cause versus Tier 1 (reviewer confirms the parent's resolution, with one wording fix)

Quoted lines support: global or user-level ask forbidden (owner-decisions.md:5; gap-closure .memlog.md:32); first-use creation inside a project is a non-goal and scope expansion, an open question for the owner (catalogue-bundle SPEC.md:141,174; gap-closure SPEC.md:77 is a Non-goals entry, line 72 heading), not owner-forbidden. Parent wording should say "unruled" rather than imply approval. Tier 1 likely read .memlog.md:32 ("integration work is CANCELLED") as not limited to the gap-closure spec. An owner decision superseding the non-goal should cite SPEC.md:77 and .memlog.md:32-33.

## Reviewer self-audit

Not read: .markdownlint-cli2.yaml; README neighbours beyond lines 220-330; the releases.json:113 anchor line in the README; README readers elsewhere (e.g. under templates/). No commands run, no edits.

## Disposition (parent)

Findings 1, 3 and 4 are blocking (false-claim or overstated-completeness risk) and were applied to F1 in candidate-fixes.md (revised wording: owner-decision request plus documentation only; README note limited to BMAD scope, reconciling lines 241 and 308; no Ponytail claim until E-3 is observed; reporter asked for profile, seed repo and boot outcome; #478 stays open). Finding 2 is minor and was folded into F1's constraints (keep the releases.json:113 anchor; markdownlint-clean). A re-review of the revised F1 follows (review 2 of at most 3).
