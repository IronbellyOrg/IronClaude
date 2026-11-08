# Fix log: Phase 3 research gate (Gate 1), fix cycle 1

Source: `qa/qa-consolidated-findings-phase3.md` (3 blocking findings: #1, #2, #3; 9 minor findings stay as notes and are not fixed).
Fixer: rf-qa, `fix_authorization: true`. Files in scope: research files 01, 02, 03 only. `research-notes.md` is not edited (md5 before fixes: d2671ff214db5ce006c8a5f46e99896b).

## Resolutions

### Blocking finding #1: contradiction on the poller's routing/dedupe rule (IMPORTANT) - RESOLVED

Sources read this session before editing: `src/superclaude/skills/sc-issue-protocol/refs/claim.md:35-50` (Wave 2 items 3-4, Wave 3 item 1); `gh issue list --help` (lines 20, 48, 50: `--assignee`, example `--assignee "@me"`, search example `no:assignee`); `research-notes.md:108-112` (ADDENDUM 2).
Changes (all targeted Edit calls):
- `research/02-github-surface-and-cli-patterns.md` section 2b, the "skip issues that already have an assignee" sentence: rewritten to "skip only issues assigned to a login other than the own login", with an amendment note.
- `research/02-...md` section 2b Key Takeaways, the pre-filter sentence: narrowed to "skip only issues assigned to someone else; do not skip issues assigned to its own login when routing by assignee".
- `research/02-...md`: new section "2c. Reconciliation of the routing and dedupe rule" (inserted before section 3). States the single predicate, a table mapping file 01's four routing candidates to the selection rule, the role of the assignee check and the dedupe signal, and what stays [UNVERIFIED] (GitHub multi-assignee behaviour, the exact query form, whether a later owner decision names a routing candidate).
- `research/01-claim-flow-and-session-launch.md` section 9 Key Takeaways: added a reconciliation pointer bullet to 02 section 2c.
- `research/03-governance-and-security-surface.md` section 4.3: added a reconciliation pointer bullet to 02 section 2c, tying it to the "assigned to its own login" wording of section 7.

### Blocking finding #2: unlisted gap, where the poller runs and keeps its dispatch record (IMPORTANT) - RESOLVED as a recorded gap (no new investigation possible from the repo)

Nothing in the repo shows Coder scheduling, autostop or durable state; no Coder documentation was fetched here (the proposed fix says to tag [UNVERIFIED] and assign to web-02 and the live plan, which is what was done). `research-notes.md:85` confirms web-02's scope includes "autostop".
Changes:
- `research/01-...md` section 7 Key Takeaways, the "(cron, systemd, a shell loop)" sentence: appended an [UNVERIFIED] tag naming the three unverified points.
- `research/01-...md` Gaps and Questions: new item 9, tagged [UNVERIFIED], covering scheduler availability, survival across autostop/restart, durable state location, and a stopped workspace not polling; states the evidence that does exist (WORKER-CONTRACT.md:61 as read in section 7 of that file; Orca handler needs a running runtime, section 12) and assigns the question to web-02 and the live plan phase.
- `research/03-...md` section 5, the "(cron, systemd or a user loop)" sentence: appended an [UNVERIFIED] tag pointing to the new gap.
- `research/03-...md` Gaps and Questions: new item 15, tagged [UNVERIFIED], with the same unknowns plus the consequence for the section 7 at-most-once/audit/approver-allow-list properties; assigned to web-02 and the live plan phase.

### Blocking finding #3: `CCSESSION_PERMISSIONS=default` treated as deciding bypass versus stall (IMPORTANT) - RESOLVED

Sources read this session before editing: `src/superclaude/skills/ccsession-tag/README.md:534-535`; `src/superclaude/skills/ccsession-tag/ccsession:117-141`; `/home/coder/.config/orca/profiles/local-default/orca-data.json` (`"agentDefaultArgs":{"claude":"--dangerously-skip-permissions",...}`, `"agentCmdOverrides":{}`); `/opt/Orca/resources/app.asar.unpacked/out/shared/agent-launch-profile.js:12-14` and `.../shared/tui-agent-permissions.js:16` (Orca falls back to `--dangerously-skip-permissions` for `claude` when no typed setting exists).
Changes in `research/03-governance-and-security-surface.md` (the four places named by the finding, plus the summary sentence that repeated the same claim):
- Section 2.2 ccsession table row (finding's "line ~67"): appended an amendment stating the permission mode is decided by ccsession's `CCSESSION_PERMISSIONS`/`CC_CLAUDE_FLAGS`, the flags Orca passes from `agentDefaultArgs`, and whether Orca runs `ccsession-orca`; cites README:534-535, ccsession:141, the Orca config and the Orca code lines. Whether `orca agent launch` applies `agentDefaultArgs` was not traced: tagged [UNVERIFIED].
- Section 2.3 first bullet (finding's "line ~70"): "stalled (default mode) or unrestricted" rewritten so the stalled case requires both ccsession's bypass and Orca's default args to be absent; states `CCSESSION_PERMISSIONS=default` does not by itself produce a stall.
- Section 2.3 Key Takeaways (finding's "line ~77"): rewritten to the same effect; says `CCSESSION_PERMISSIONS=default` is not a sufficient mitigation on its own.
- Gaps and Questions item 5 (finding's "line ~211"): rewritten to name all three inputs and to cite README:534 and the local `agentDefaultArgs.claude` value.
- Summary: parenthetical added after "ccsession launches with permissions bypassed by default" noting Orca's default flag still applies under `CCSESSION_PERMISSIONS=default` (README:534).
- `research/01-claim-flow-and-session-launch.md` section 11 (Interactivity paragraph): added a reconciliation sentence cross-referencing file 03 section 2.2, so files 01 and 03 now agree.

## Verification

- `research/research-notes.md` md5 after fixes: d2671ff214db5ce006c8a5f46e99896b, identical to the value before (unchanged).
- Files edited: 01 (288 to 290 lines), 02 (211 to 228), 03 (231 to 233). No file was rewritten; every change was a targeted Edit.
- Minor findings #4 to #12 were not touched, per the finding file and the prompt.
- Every added statement cites a file:line read in this session or is tagged [UNVERIFIED]. No new research agent was spawned: none of the three gaps could be closed by reading the codebase, and the open Coder-side question belongs to web-02.
- Limitation: I did not re-run a QA pass over my own edits; the gate's re-review (fix cycle 2 check) is the orchestrator's next step.

