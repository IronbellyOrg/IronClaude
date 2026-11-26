## Verdict
**still-relevant.** Keep issue #719 (the report page server security follow-up) open as a gate for a later restoration, not as an active-server claim about today's checkout. Checked on 2026-11-24 at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`; live issue is OPEN with no comments.

- **Current state:** the skill and its test file are absent from HEAD. Targeted `git ls-tree` returned no entries for the original source, test or plugin-copy paths. PR #700 merged the rollback at `471f10511c8e2e8176c0e2088720ece03beca317`; the local path history contains that removal and the original PR #684 merge. This removed the implementation from this checkout, not fixed its archived security defect, nor proved that older installed copies or detached servers stopped.
- **Retained source:** archive tag `archive/pr-684-agent-work-report` resolves to original merge `d7d645dddd42e49a72a734f9c8b6952bcbcb4527`. The four selected skill files and archived tests were copied only under this report directory; these are evidence, not a runnable installation. At `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/source/agent-work-report/scripts/page.py:308-342`, startup still launches generic HTTP serving over the whole state directory, has no application Host/path/token restriction, and reuses any successful response without checking page identity. Lines 324-325 bind only loopback; this is not evidence of direct LAN exposure.
- **Other acceptance gaps:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/source/agent-work-report/templates/report-template.html:7-10` has the report marker but still loads Google Fonts. Searches of the archived 4,005-line test file for `ensure_server`, `http.server` and `8765` found no matches. No issue-required server regression tests were found by those searches; no tests were run.
- **Live work check:** read PR #684 and #700 descriptions, general comments/review summaries, and searched all-state PRs for `719` (no results) and `agent-work-report` (no restore/fix PR identified; known original, rollback and unrelated mentions only). This does not prove that no unlinked branch exists. The exact original inline review reply/resolution is **UNVERIFIED**: allowed gh view fields do not expose that discussion. The issue's statement 'anything that answers' should be narrowed to a successful response at the report URL, because HTTP errors follow the exception path.
- **Analysis:** the required architecture command ran against the narrow archived source snapshot because the production directory is absent. Its report is `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/analyze/analyze-report.md`; its worker status is succeeded. This was static review only. DNS-rebinding exploitability in the actual browser, Coder forwarding, the live PrivateRepoA copy and other hosts' installed copies/processes remain **UNVERIFIED**.

## Complexity and size
**complexity medium; size M.** The remaining fix is localized but spans request validation, isolated page-copy freshness, listener identity, process lifetime, page assets and tests; this grades #719 alone, not the larger #720 restoration.

## Priority
**P2.** Serving private state is a material confidentiality defect and must block approval of #720's restored server, but this checkout no longer contains the skill and the restore is explicitly parked; no current production exposure was verified here.

## Concrete next steps
No partial implementation or active fixing PR was verified. These steps are for the later authorized restore, not authorization to start it now:

1. Respect #720's recorded trigger: owner asks for the daily per-issue page, or the report-entry writer stage is about to start. Follow its owner questions and decisions before restoring code. This review supplies no such approval.
2. In the restore branch's security amendment, serve a scratch folder containing only a copy of report.html. Explicitly reject other files and folder paths, disable listing, and allow only the exact Host `127.0.0.1:8765`. Keep the copy current on generation and living-report refresh so isolation does not freeze the displayed report. Test rejected state-file and folder requests with 403 or 404, including settings.json and action-log.jsonl.
3. Check the report's own identity marker before reusing a listener. A foreign success response must fail safely, not become the report. The existing overview-sha256 marker is a possible starting point, not authentication by itself.
4. Remove remote fonts or package them locally, then observe a page load with no third-party requests. State whether the server stops at run end; otherwise document that it persists and how to stop it.
5. Add at least the three required rejection tests (state file, folder, wrong Host), run them in the normal suite on restored code and provide evidence for the identity, asset and lifetime checks too. No successful run is claimed by this review.
6. Record in the restore PR whether an unguessable URL token is included, based on the local-account/browser threat model and tab reuse. A Host restriction or a public page marker alone must not be described as authenticating another local account. The token decision remains open in #719.
7. Only close #719 after all eight of its acceptance points have evidence on the restored code and an independent reviewer or owner accepts them. Removing code in #700 or resolving a GitHub thread does not satisfy those checks.

## Dependencies
- **#720, restore the report skill:** needs an authorized restoration branch to implement and observe the fix. #719 blocks approval of that restored server; it does not require #720 to merge first. Implementing both in the same restore PR avoids a circular dependency.
- **#718, dashboard/report views:** its state-location and copy-ownership choices are restoration prerequisites recorded by #720, not evidence that the security code depends on the entire dashboard being built.
- **#716, coordinator features:** report-entry display work is indirectly affected through restoration. It is not a prerequisite for fixing the isolated daily-page server, and this security issue does not block all coordinator or watcher work.

## Related issues
- [#720, parked report-skill restoration](https://github.com/IronbellyOrg/IronClaude/issues/720): explicit direct relationship and security merge gate; live OPEN, no comments at inspection.
- [#718, report and dashboard features](https://github.com/IronbellyOrg/IronClaude/issues/718): report-state location and copy ownership; its state-location section repeats the unsafe whole-state-folder serving concern.
- [#716, coordinator feature follow-up](https://github.com/IronbellyOrg/IronClaude/issues/716): report-entry content and issue-body-change entries wait on restoration; indirect relationship only. These relationships are recorded in the live issues, not inferred as whole-issue dependencies.

Live issue responses are preserved under `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/` as evidence. The local debate/spec documents named by the issues were not available in the targeted snapshot and were not relied on as independently verified sources.

## Related PRs
- [#684, original report-skill import](https://github.com/IronbellyOrg/IronClaude/pull/684): MERGED on 2026-11-20, commit `d7d645dddd42e49a72a734f9c8b6952bcbcb4527`; the vulnerable startup is present in the matching local archive. Review summaries confirm security review activity; exact linked inline thread contents/resolution remain UNVERIFIED independently of #719.
- [#700, rollback that removed the skill](https://github.com/IronbellyOrg/IronClaude/pull/700): MERGED on 2026-11-20, commit `471f10511c8e2e8176c0e2088720ece03beca317`; its changed-file listing deletes the skill and 4,005-line test file, consistent with the current tree and local history.
- No fixing/restoration PR was identified in the targeted all-state searches. This is a bounded search result, not a guarantee about every branch or unlinked PR.
