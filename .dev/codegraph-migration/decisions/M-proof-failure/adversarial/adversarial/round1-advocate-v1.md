# Round 1 advocate: Variant 1 (option A, draft PR with a label)

Persona: architect (structure, dependencies, long-term impact).

## Position Summary (1-3 sentences)

For behaviour failures (class 2) the draft PR with a label is the right artifact: it is the only hard non-mergeable state GitHub offers, it holds the diff a person must fix, and it is proven in Coder. Variant 1 is wrong to treat integrity failures (class 1) the same way, because the pinned SHA256 table is the trust root at install time; I concede class 1 to an issue-only rule (V2 and V3 agree) and would ship V3's split with V2's idempotency and V1's draft mechanics.

## Steelman of V2

V2's strongest case is structural simplicity with a hard safety guarantee: "No branch, no PR" means "nothing mergeable is ever created from failed or unverified bytes" (variant-2-original.md, line 4), so the safety property holds by construction rather than by a draft flag that is one "Ready for review" click from mergeable (diff-analysis.md X-001). Issues are the channel that is known to reach the owner ("issue and PR notifications reach the owner", context.md line 4), whereas draft PR notifications are unverified for this repo (A-006). V2 is also the only variant that addresses daily re-runs at all ("Open (or comment on, idempotently by title) one issue", variant-2-original.md line 3; U-002 rated High), and the only one that puts the run URL and local reproduce commands in the report (U-001). Its single failure path is the smallest test surface for classes 1 and 2.

## Steelman of V3

V3's strongest case is that it matches the artifact to what a person can actually do next (variant-3-original.md line 6). For an integrity failure there is nothing to fix in this repo; the right action is to investigate upstream, so no branch is pushed. For a behaviour failure the likely fix is a code change in this repo (`MCP_TOOLS` at install_codegraph.py line 35, or the registration entry), so a draft PR gives a branch to push onto. It is the only variant that satisfies both "no unverified bytes on a branch" and "a diff to push a fix onto" (U-003, High), and the only one that names the infrastructure path at all (U-004). It reuses Coder's neutral-exit behaviour for class 3, which is the proven half of the Coder pattern I am also relying on.

## Strengths Claimed (numbered, with evidence)

1. Draft is the only hard non-mergeable state. Coder's own comment: draft is "the only hard non-mergeable state available"; the label is "best-effort" (context.md line 4). Branch protection on a bot branch, a label, or a title marker do not block merge; draft does. Combined with "a human always merges (no auto-merge exists or is proposed)" (M-major-versions/context.md line 5), a draft requires two deliberate human actions (mark ready, then merge) before anything reaches master.
2. One artifact holds both the diff and the evidence. A behaviour failure (tools/list missing a tool, print-config drift) is usually fixed by editing this repo, for example `MCP_TOOLS = "node,search,callers,callees,impact,files,status"` (install_codegraph.py line 35). A draft PR lets the person push that fix onto the branch, and the next proof run judges the combined result. V2 forces the person to re-run the bump script by hand and open their own PR (variant-2-original.md line 5, "they must re-run the script by hand").
3. Proven in a sibling repo with the same owner. Coder's `ironclaude-upstream-monitor.yml` already pushes the bump branch first and opens a draft PR with a label on FAIL (context.md line 4). Reusing the same shape keeps two monitors maintained by one person consistent, which is a real long-term maintenance cost saving.
4. Visible marker. The "[proof failed]" title suffix (variant-1-original.md line 3, U-005) separates the draft from routine work in the PR list and in notification subjects, which partly answers V1's own cost line.
5. Natural idempotency key. A bump branch name derived from the version (for example `codegraph/bump-v1.7.0`) is a unique key that GitHub enforces: there can be only one open PR per head branch. That gives the draft path a cheaper and more reliable idempotency key than title search, once the rule is written down (it is not in V1 today; see Concessions).
6. Shared machinery with PASS. The PASS path already pushes a branch and opens a PR (M-major-versions/context.md line 3). The class 2 path differs only by `--draft`, a label and a title suffix, so it adds almost no new code path. V3 inherits this strength for class 2.

## Weaknesses Identified in Others (numbered, with evidence)

1. V2 discards the fix surface for class 2. A tools/list or drift failure needs a code change; with no branch, the reviewer reconstructs the bump by hand (variant-2-original.md line 5). That is a recurring manual cost on the most likely failure class and invites hand-edited SHA256 tables, which is exactly where mistakes are dangerous (install_codegraph.py lines 328 to 330 trust that table).
2. V2 is silent on class 3. A persistent infrastructure failure (expired token, changed API) produces nothing under V2 (diff-analysis.md X-002 applies to all three variants).
3. V3 as written makes class 3 silent forever. "no issue (retries next schedule)" (variant-3-original.md line 5) plus "Nobody watches IronClaude Actions run summaries" (context.md line 4) means a broken monitor is never noticed. Coder's neutral exit is acceptable for a short outage, not for a permanent one.
4. V3 does not define the integrity/infrastructure boundary. A truncated download produces a hash mismatch, and `gh attestation verify` exits non-zero when the API is unreachable (X-003). Without a tie-break, a transient network fault raises a false tamper alarm or, worse, a real tamper is dismissed as a flake.
5. V3 gives no idempotency rule for either its issue or its draft PR (C-004), and no rule for human commits on the bump branch (A-002), even though letting a person push a fix is V3's whole reason for the branch. A daily force-push would erase the very fix V3 exists to allow.
6. V3 adds a third path but specifies no title for the draft PR (S-002).

## Concessions

1. Class 1 on a branch is wrong. V1's own cost line says it: the branch pin "points at unverified bytes" (variant-1-original.md line 6). The repo source makes this worse than "unverified": install_codegraph.py lines 328 to 330 compare the download against `SHA256[asset]` and, on a match, report "installed codegraph ... (SHA-256 verified)" (line 361). Whatever hash the monitor writes onto a branch becomes the trust root. If the tampered tarball and a tampered SHA256SUMS agree but the attestation fails, merging that draft makes the installer accept the attacker's bytes and call them verified, and the pin flows to every Coder workspace (M-major-versions/context.md line 5). One "Ready for review" click is too thin a guard for that. V2 and V3 win C-001; I adopt their rule.
2. V1 states no idempotency rule. V2 wins C-004 as the only variant with one; it needs extending to the branch case.
3. V1 is silent on class 3. V3 wins C-003, with an escalation added.
4. The label does not exist (context.md line 4 lists the nine labels). V1 assumed it; the workflow must create it or treat the label as optional.
5. V1's report lacks the run URL and reproduce commands. V2 wins C-005.
6. A-006 is a real gap for V1: if a new draft PR does not notify the owner, V1's failure path is silent. I add an explicit notification step rather than assume it.

## Shared Assumptions (A-001..A-006, each ACCEPT/REJECT/QUALIFY + reason)

- A-001 (failure class detectable at runtime): QUALIFY. Detectable only if the monitor separates fetch from verify. Rule: a fetch counts as complete only on HTTP 2xx with byte length equal to the asset size reported by the release API; any fetch error is class 3. A hash mismatch on a complete fetch, or `gh attestation verify` failing after a successful API reachability check in the same run, is class 1. If still ambiguous after one in-run retry, fail closed to class 1 (issue, no branch).
- A-002 (re-runs never clobber human commits): ACCEPT, as a hard rule it is not today. Rule: the monitor may update the bump branch only when every commit on it since `master` was authored by the workflow bot; if any other author is present, it never pushes, and instead proves the branch head as-is and reports the result by PR comment.
- A-003 (newer release supersedes older artifact): QUALIFY. Supersede by comment-and-close only for bot-only artifacts (close the old issue or draft, delete the bot-only branch, link the new artifact). If the old branch has human commits, comment with the link and leave it open; a human fix (for example `MCP_TOOLS`) may need carrying forward and only the person knows.
- A-004 (later PASS for same version resolves the artifact): ACCEPT. Class 1 issue: close with a comment linking the new ready PR. Class 2 draft: on a bot-only branch, remove the label, drop the title marker and mark ready (identical to the PASS path); on a branch with human commits, remove the label and comment "proof passed at <sha>", leaving the ready click to the person.
- A-005 (label exists, token permissions in place): REJECT as an assumption, it is false today. Rule: the workflow runs `gh label create needs-codegraph-proof --force` before use, applies the label in a separate non-fatal step after PR creation, and declares `contents: write`, `pull-requests: write`, `issues: write` in the job's `permissions:` block.
- A-006 (draft PRs notify like ready PRs): QUALIFY. Unverified for this owner's settings. Rule: after opening a draft, assign it to the repo owner so an assignment notification is sent regardless of draft notification behaviour; a test asserts the assignee is set.

## Per-Point Verdicts

| Point | Superior approach | Confidence % | One-line reason |
|---|---|---|---|
| S-001 | V3 | 85 | Classes need different artifacts; one path either leaks unverified bytes (V1) or drops the fix surface (V2). |
| S-002 | merge of V1+V2 | 70 | Title must carry version and stage (V2) plus a visible failure marker (V1). |
| C-001 | V3 (same as V2) | 92 | The pinned SHA256 table is the install-time trust root (install_codegraph.py 328-330); unverified hashes must never reach a branch. |
| C-002 | V3 (same as V1) | 85 | Behaviour fixes are repo edits; a draft PR gives a branch to push them onto. |
| C-003 | merge of V3+escalation | 75 | Neutral exit is right for a blip, but a persistent outage must reach a person. |
| C-004 | V2, extended to branches | 80 | Only V2 has a rule; it needs a branch-name key for the draft path. |
| C-005 | V2 | 80 | Run URL and reproduce commands make any artifact actionable. |
| C-006 | V1/V3 with creation step | 70 | Label aids filtering but does not exist; create it, never depend on it. |
| C-007 | V3 with shared helpers | 70 | Four routings over two helpers (upsert issue by title, upsert PR by branch) keep the test cost near V1's. |
| X-001 | V3 | 80 | Draft is safe enough for class 2 bytes that passed integrity, not for class 1. |
| X-002 | merge of V3+escalation | 80 | No variant reaches a person on persistent infra failure; add an issue. |
| X-003 | V3 with fail-closed tie-break | 70 | Separate fetch from verify; ambiguous after retry means integrity. |
| A-001 | QUALIFY (merge) | 75 | Classifiable only with explicit fetch-completeness checks and a fail-closed default. |
| A-002 | ACCEPT as new rule | 90 | Never push to a branch carrying non-bot commits. |
| A-003 | QUALIFY | 75 | Close bot-only stale artifacts; only comment on ones with human work. |
| A-004 | ACCEPT | 85 | Same-version PASS closes the issue or promotes the bot-only draft. |
| A-005 | REJECT (false today) | 90 | Label must be created and permissions declared. |
| A-006 | QUALIFY | 65 | Unverified; assign the owner to force a notification. |

## Proposed Merged Rule (the rule you would ship if forced to merge; bullets)

- Classify each run: fetch errors or incomplete downloads are class 3; hash mismatch on a complete download or attestation failure with the API reachable is class 1; any failure in install, index, tools/list or drift after integrity passed is class 2. Ambiguous after one retry: class 1.
- Class 1: issue only, no branch. Title "codegraph vX.Y.Z: integrity check failed". Body: run URL, asset, expected and actual hash, attestation output, reproduce commands. Key: exact open-issue title.
- Class 2: push `codegraph/bump-vX.Y.Z`, open a draft PR titled "chore(codegraph): bump to vX.Y.Z [proof failed: <stage>]", label `needs-codegraph-proof` (created with `--force`, applied non-fatally), assigned to the owner. Body: stage, log tail, run URL, reproduce commands. Key: head branch.
- Class 3: retry with backoff in-run; on final failure exit neutral with `::warning::` and a step summary, and open-or-comment one issue "codegraph monitor: infrastructure check failing", closed by the next run that reaches the API.
- Next daily run, same version, same failure: no new artifact; comment only if the failure fingerprint (class, stage, hashes) changed.
- Human commits on the bump branch: never push; prove the branch head and report by comment.
- Later PASS, same version: close the class 1 issue with a link; promote a bot-only draft to ready; on a human-touched draft, remove the label and comment.
- Newer release: close bot-only stale artifacts with a link to the new one and delete bot-only branches; comment on human-touched ones.
