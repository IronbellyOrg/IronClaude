# Post-release architecture analysis

Structure: analysis template in .dev/issuecleanup/g1/362/report-template.md, limited to issue 429.

## Scope and grounding
Command: `/sc:analyze src/superclaude/skills/sc-post-release-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/429/analyze`.

Reviewed checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, 2026-11-23. The protocol package is the narrowest source directory covering issue #429's suggested extension point. The wrapper, release procedure, release records and related GitHub issues/PRs were inspected as boundary evidence.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:10:33Z; degraded: graph:empty.

Access: mcp. Readiness ran once. The graph lists the manifest template but does not index the Markdown protocol (the outline lookup returned no indexed file); direct Read/Grep supplied the architecture evidence. No indexing, source modification or dynamic testing was performed.

## Architecture and metrics
The source directory contains nine files: one protocol, four reference documents and four templates. Its five workstreams cover user documentation, technical documentation, install/deploy proof, user test guides and operator test guides (`SKILL.md:43-51`). The command delegates to that protocol (`src/superclaude/commands/post-release.md:60-66`). Scanners gather evidence, a consolidator forms a coverage matrix, and writers create approved artifacts (`SKILL.md:161-171`).

The package has usable building blocks: tag anchoring, clean install targets, saved transcripts, explicit gaps and incremental manifests. Its matrix measures document/guide presence, not execution of every capability (`refs/workstream-playbook.md:19-27,114-134`; `templates/post-release-manifest.json:22-30`). Its return contract contains eight fields for status, mode, install classification, report/manifest paths, per-workstream results, installation result and gaps (`SKILL.md:287-296`). There is no release score or threshold among those fields.

Boundary evidence: the existing release procedure requires nine manual go/no-go checks before tagging (`docs/developer-guide/release-procedure.md:64-78`), then invokes post-release (`:107-115`). The 6.0.0 saved transcript ends GREEN (`docs/testing/v6.0.0/c-e2e-transcript.txt:2194-2202`), while that release's report deliberately excludes new human guides (`docs/testing/v6.0.0/post-release-report.md:129-135`). These are recorded runs, not runs repeated by this audit.

## Severity-rated findings
These are requirement gaps against #429, not regressions in the intentionally post-release command.

1. **High impact: reporting follows publication rather than controlling final sign-off.** The command requires a tagged release (`commands/post-release.md:15`); the separate release procedure tags after manual checks and only then invokes this command (`docs/developer-guide/release-procedure.md:86-115`). Its RED result is valid reporting (`SKILL.md:300-306`), not a failed scored release decision. Consequence: using the present command alone cannot satisfy #429's before-sign-off gate.
2. **Medium impact: functional execution and abuse coverage are missing from the current five-workstream scope.** Installation must run, but user capability coverage means authored human guides (`SKILL.md:187-191`; `refs/workstream-playbook.md:114-134`). No explicit abuse/malicious-input campaign appears in the scoped package. Consequence: a present guide does not prove the behavior was exercised, and no general agent-versus-human routing criterion is specified.
3. **Medium impact: the manifest/report schema cannot express the requested standardized scored result.** The manifest records guide presence and install execution (`templates/post-release-manifest.json:22-30,45-69`); the reporting contract has no score/threshold (`SKILL.md:287-296`). Consequence: no common scoring criteria or minimum score can be evaluated consistently from these artifacts alone.

No source change is needed for this review. Security/performance correctness and runtime reliability were not tested.

## Recommendations and roadmap
Keep #429 open as still-relevant, complexity complex, size L, priority P1 (judgment, not an existing GitHub label). First turn #354's retained ledger and the manual nine-check release procedure into a scoped requirement set; next choose the release gate's entry point and define a versioned scorecard and agent/human evidence rules; then build and verify the route with both passing and rejected candidates. Reuse discovery, clean targets, transcripts and manifests; do not build another general experiment scheduler or mistake a written guide for executed coverage. No live defect or incident justifies P0 from this evidence.

## Verification limits
Static quick analysis only. No fresh install, abuse test, real release, live model test or whole-suite run was authorized or performed. The existing transcript was read, not reproduced. Source security/performance is outside this architecture pass.

Negative evidence: scoped grep found no scoring/abuse/pre-release implementation in the post-release package; broader `src` searches found other unrelated scoring and gate mechanisms, not evidence that they implement #429. Workflow grep for post-release/pre-release/release-gate names returned no matches. Test searches located install/routing/worker-contract coverage, not an observed runtime release approval test. None of those searches proves global absence.

GitHub reads used only allowed issue/pr view/list commands with the fork explicit. #429's body, its sole comment, dependency fields and linked-closing-PR field were read. **UNVERIFIED: full event timeline** (the allowed issue-view JSON surface exposes no timeline field). No API, browser or other GitHub route was used to bypass the brief. PR #667 is merged remotely but its directory is absent locally, so claims about its recorded run remain attributed to its PR body.

The first issue read failed because this installed `gh` rejects combining `--comments` with `--json`; it was retried successfully with the JSON comments field. Codegraph's Markdown outline returned no match and fell back to Read. Two direct reads of the missing 6.1.0 report failed; a directory Glob confirmed the local absence. Broad `.dev` searches were noisy/truncated and did not establish absence of a design; a tighter phrase/#429 search returned only an unrelated historical HTTP-429 reference. Any unlinked or unmerged #429 implementation is UNVERIFIED.
