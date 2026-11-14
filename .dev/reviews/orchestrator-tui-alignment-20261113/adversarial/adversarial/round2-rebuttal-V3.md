# Round 2 rebuttal for variant 3 (Coder#477 listener review)

Role: ADVOCATE for V3, Round 2. Read-only. Date: 2026-11-14. "Re-verified" = opened in this round. "R1-Vn" = round1-advocate-Vn.md, "R2-Vn" = round2-rebuttal-Vn.md. X, A, SC ids are from diff-analysis.md.

## 1. Response to each criticism raised against V3

Sources: R1-V1 section 4 items 1, 2, 10, 11; R1-V2 items 4 to 6, 8; R1-V4 items 5, 6; R1-V5 items 4, 6, 12 and concession 9; R2-V1 section 2 and rows 5 and 6; R2-V2 sections 2 and 5.1. Repeats are grouped.

| # | Criticism (who) | Response | New evidence verified now |
|---|---|---|---|
| 1 | Edit 5 is unachievable: "without any write" is false for `sweep run` (V1 #1, V2 #5, V4 #5, V5 #4) | **Concede in full** (R1-V3 concession 1). R2-V1 adds that the obvious repair, a stored `<stem>.json` beside the report, is also blocked by the pinned one-file rule, so Edit 5 cannot be fixed by "persist the JSON" inside the current sweep contract. I accept that and drop the sweep JSON as the payload of any #477 route in Phase 1. | `tests/sweep/test_readonly.py:400` asserts `sorted(p.name for p in sweep_env.sweeps.iterdir()) == [report.name]`; `tests/sweep/test_cli_contract.py:1192` and `:1361` pin the report-folder listing. Confirmed: a sidecar file changes a pinned requirement, not one line. Replacement for Edit 5 is in section 5.6 (the route carries a named record and age; the producer is not specified by #477). |
| 2 | Edit 8 omits the second governed agent (V1 #2, V2 #4, V4 #5, V5 #5) | **Concede in full** (R1-V3 concession 3). R2-V2 D-D narrows the effect: a re-claim is mostly idempotent (`already_launched`), so the extra agent appears once per issue, not per cycle. That lowers the severity, not the omission. | New, and it matters for Edit 8's live-test line: the shipped Coder image launches every Claude session with permission checks off. `README.md:60-66`: "Permission checks are off for every call the wrapper routes (a deliberate choice, #455): `ccsession` adds `--dangerously-skip-permissions --allowedTools=Grep` to every launch". `ccsession:135-141` sets those flags unless `CCSESSION_PERMISSIONS=default`; a search of `templates/VSCode-AIDev02` finds no `CCSESSION_PERMISSIONS` setting and `CC_CLAUDE_FLAGS` only in that README sentence. So both the watcher's first session and the claim's second agent start in bypass mode on a stock image. Edit 8 must record the mode of every session the claim starts, and the owner must accept it explicitly (section 5.5). |
| 3 | Cites are against a stale scratch copy of #409 (V2 #6, V4 #6, V1) | **Concede.** Fix: cite the live body by `updatedAt` plus heading or item number, not by line. Live body `updatedAt` 2026-11-13T16:57:51Z; the diagram sits under "How the pieces fit", the read/send sentence is item 5, the trust sentence is item 6, the boundary sentence is item 8 (all re-read now). | `gh issue view 409 --json body` (re-read). |
| 4 | Twelve edits are mostly contingent; posting before Q1 is premature (V1 #10) | **Partly counter, partly concede.** V3 said so itself ("Edits 1, 2, 10, 11 and 12 hold whatever the owner answers"; "post nothing before the answers") and posted nothing, so there is no premature post. But the criticism is right that twelve edits is the wrong shape for a one-line owner comment. Section 5.6 replaces them with three exact rewrites keyed to the owner's answer. | Coder#477 re-read: still one comment (2026-11-13T16:20:07Z), body unchanged. |
| 5 | F12 adopts "decide one design, not two" without reconciling the watcher's local trust model (V4 #5) | **Partly counter.** V3 F12 says in terms that under option A "the watcher's trust is the approvers file plus labels plus the integer-only prompt ... a different, local model". What V3 did not do is write that reconciliation into Edit 7. Fix: Edit 7 states that the grant format governs a listener route only and does not replace the watcher's approver, label and integer-only checks. | `launch.py:30-37` (integer-only pattern), `issue-watcher.md:43-45` (D1 to D3). |
| 6 | V3 never checked that a built observer exists or what "TUI Panel" means (V5 #6, V4 concession context) | **Concede.** Done now in section 5.2, with a text-based finding and a single settling question for the owner. | Section 5.2. |
| 7 | The identity-versus-human-gate conflict (a launched session that the sweep can identify via `ccsession-orca` also defaults to bypass) is where V3's F8 and F12 meet the real launch, and V3 lacks it (R2-V2 section 2) | **Concede, and settle half of it.** R2-V2 D-C lists the actual mode as UNVERIFIED. The image-level half is now verified (row 2): the shipped default is bypass. What stays UNVERIFIED is a given workspace's user-set environment. | `README.md:51` says every launch, including Orca's, goes through the wrapper that hands the call to `ccsession-orca`; `README.md:60-66` as in row 2. |

**Net.** I withdraw: Edit 5 as written, the restated launch in Edit 8, all `/tmp` line cites, and the twelve-edit shape. I keep: F1, F2, F6, F8 (with its two answers), F10 to F14, F17, and the read/send split as the central requirement of any cross-workspace route.

## 2. Updated assessment of V1, V2, V4, V5 and of their Round 2 claims

**V1 (and R2-V1): up on method, still not on the Coder edge.** Accepted from R2-V1: NFR-001 blocks a sidecar JSON (verified, row 1); #541 needs no rebase of #539 (V1 and V2 now agree); the live-Run "0 pending" measurement does not show non-consumption, so X-016 is "unproven both ways" (R2-V1 section 5 item 2, which R2-V2 also accepts; I did not re-derive it, it follows from `--all` listing acknowledged rows). Where I differ: R2-V1 D-1 frames persistence as the only way to give a second consumer the sweep's facts. A third route exists and is already built: the observer's snapshot is atomically written at mode 0600 (SC-17) and carries no message subject, body or handle (V5 S5), so a #477-style status record can start from the snapshot (Orca facts) and treat the sweep's per-Run facts as local-only until Phase 2. R2-V1's source-sharing point (section 5, item 1: two programs resolve the Orca binary differently) is correct but not a #477 matter.

**V2 (and R2-V2): up.** Section 5.1 (the launched session's permission mode) and 5.5 (the decision matrix: `--pipeline none` plus option A is "a notifier that opens a session for a person"; default level plus B or C is "a remote agent-spawner") are the clearest statement of the stake in #477, and I adopt both. 5.4's warning that `reset --forfeit-guarantee` on an `unknown` entry can permit a second launch of an issue whose first session is alive is a state risk any listener inherits. I settle part of 5.1 (row 2 above). I do not agree that W-04 ("no Run record") matters for #477; it matters for the observer.

**V4 (R1 only; its Round 2 is not written): up on F1, F7, F8, F9, F14, F17 and on conceding C8, F17 and F13.** My remaining difference: its #423 edit 3 conditions "all workspaces" on #477, but #477's own design status (unnecessary under option A, `issue-watcher.md:47-49`) means the condition should read "if #477 is kept". That is one clause.

**V5 (R1 only; its Round 2 is not written): still decisive on the observer, but its D9 is a guess and its D1 omits the third party.** R1-V5 concessions 5 and 9 accept both. My finding on D9 is in section 5.2 and it differs from R1-V5's "probably `observe`" only in weight: textual evidence favours the #409 TUI dashboard over TUIBBS, and the requirement set is the same for both. Its concession 4 ("nothing needs code today" is too strong) does not apply to #477: nothing should be built on #477 today.

## 3. Final verdict on the 13 contested points

| id | verdict | winner | conf. | concrete course of action |
|---|---|---|---|---|
| A-002 | The unit differs per program: sweep = one Run for rows plus host-global worktrees and transcripts (`probes.py:1203-1214`); observer = all Runs on one host, paged; watcher = one workspace and one `gh` login (`issue-watcher.md:15`). Across workspaces there is a fourth unit nobody lists: the workspace, keyed by Coder's workspace id, not by path (every workspace has `/home/coder`) or name (reusable). | V5 (observer), V1 (sweep), V2 (blind spot), V3 (workspace unit) | 82% | In the relationship note, give each unit one line and add "workspace = Coder workspace id plus owner, taken from Coder". Add the host-global caveat to the sweep line. |
| A-004 | PR #539 is open, UNSTABLE, MERGEABLE, two unresolved threads (one security, `probes.py:1203-1214`, `:309`); no keys, no sidecar file and nothing for #477 belongs inside it; #541 changes one file and needs no rebase of #539. | V1 | 90% | Merge #541, re-run #539 CI, resolve the two threads. Log in #534: identity block for JSON, persisted or no-report mode (with the NFR-001 change it needs), stale design lines. |
| A-005 | No one defends the assumption; Phase 2, #534 and "later" have no owners beyond a reading list; observer R3 and R4 have no package. V3's own "Phase 1 follow-up or a Phase 2 item" shared the fault. | process (V1, V5) | 85% | One table in #534: item, owner, trigger; unowned items labelled "unowned". Add three rows from V3: workspace identity block, read-only status route (trigger: observer R4 or TUIBBS package), machine-started-session label (trigger: FU-1 capture). |
| A-007 | True today (one owner, one OS user, one host, one enabled watcher per login: `issue-watcher-setup.md:642`). For #477 it must be written down because the only existing trust edge is the owner: both Orca apps are `share = "owner"` (`orca/module.tf:36,54`). The live exposure is also untrusted repo and issue content, not other users (V1, V2). | V3 and V4 (state it, add a read-permission AC), with V1's untrusted-content angle | 78% | State in #477 Out of Scope: "serves the workspace owner's own observers only; other users' access is a separate decision." Add V4's read-permission AC before any cross-workspace read. |
| A-008 | The sweep needs a bound Run and an active coordinator; the observer's worker ledger needs neither but sees only Orca Workers; watcher-launched and person-started sessions have no Run and are a blind spot in both. A listener does not cure this: a session it starts through `orca agent launch` is Run-less too. | V2 with V5 | 85% | Name the blind spot in both docs. In #477, "its project's orchestrator" is not an address (no orchestrator marker exists, #339 accuracy check row 3); never promise delivery to a coordinator. |
| A-009 | Holds inside one image (Claude Code pinned at 2.1.289, `Dockerfile.coder:110`; Orca pinned and monitored by `orca-upstream-monitor.yml`); fails across a fleet during rollout (image hash in the image name, `main.tf:111`). The observer records no Orca version (V5). Unresolved by evidence for a second host. | none (V2 on the watcher fixtures) | 72% | Put Orca version, Claude Code version and image hash in the #477 identity record; record `orca --version` in the FU-1 record and both golden captures; treat other hosts as UNVERIFIED. |
| A-011 | Rejected by all five; no advocate has proposed the mechanism except as an action. | process | 92% | One editor, one ordered edit set per issue, every cite pinned to a head sha or `updatedAt`. Order: Q1 and "TUI Panel" answers; #450 claim level; #477 rewrite; #409 pass; #423 pass; relationship note after #539 merges. V3's #477 edits touch no sentence any other report edits. |
| A-013 | Polling Orca CLI verbs is the only verified source for Workers; event replay is unverified (#409). For workspace-level facts there is a second source that is already authoritative and push-capable in principle: the Coder control plane. Docs fetched now: `GET /api/v2/workspaces` returns `owner_name`, `id`, `name`, `latest_build.status`, and per-agent `status` and `last_connected_at`, with the `Coder-Session-Token` header; the page's example values do not establish "running" and "stopped" (UNVERIFIED). Claude Code "Channels" were listed in the docs but not evaluated. | V5 and V2 (polling for Orca facts), V3 (Coder API for workspace facts) | 66% | No separate research. Add one read-only call to the D3 capture list: the owner lists their workspaces through the Coder API and records the real `latest_build.status` values. Use Coder as the source of workspace identity and state in any #477 design (section 5.4). |
| X-006 | The decision is not one decision. Contracts in play: sweep JSON v1 (golden-tested in #539), observe snapshot v1, the watcher's `status --json` and `dispatch.json` (R2-V2), and any #477 status record. Venue for sweep keys: #339 after #539 merges. | V4 (venue), V5 (two contracts), V2 (third contract), V3 (fourth) | 76% | Write the relationship note first, naming all four with owners and join keys. Decide sweep keys in #339 after #539. Confirm `dispatchId` = `row_id` minus `orca:` on one real Run before the note calls it a join key (R2-V1 D-5). |
| X-008 | V1's verdict line is wrong; its F-02 table is right and V5 widens it to three vocabularies. No V3 effect. | V5 on the fact; V1's tables stand | 92% | Drop the verdict sentence; publish one observer / sweep / Orca word mapping. |
| X-009 | V1's tally miscounts; no decision depends on it. | none | 95% | None. |
| X-019 | V5 overgeneralised. V1 stated "no observer exists"; V2 W-10 and V4 F13 assumed it; V3 wrote generically and also did not find it. | none (V5 slip, accepted in R1-V5) | 88% | Cite as "V1 stated it; V2 W-10 and V4 F13 assumed it; V3 did not check". |
| X-020 | W-3 is V1's proposed wording, not body text. | none (V5 slip) | 95% | Read as "do not add V1's W-3"; no body edit. |

## 4. Remaining disagreements and the single fact that would settle each

| # | Disagreement | Sides | Single fact that would settle it | Who can check |
|---|---|---|---|---|
| D-1 | Is #477 still wanted at all? | V3 (rescope to read-only status; keep prompt routing disabled), V2 Q2, design (unnecessary under option A) | The owner's reply on Coder#477 to: "keep, narrow, or close?" | Owner only |
| D-2 | What "TUI Panel" means | V5 (probably `observe`), R1-V5 concession 5 and V3 (TUIBBS possible) | The owner's one-line answer on #477 | Owner only. My textual reading (section 5.2): #409's TUI dashboard, about 75% |
| D-3 | Persist the sweep JSON now or in Phase 2 | R1-V5 concession 4 vs R2-V1 D-1 and R2-V2 D-E | Whether the owner relaxes the pinned "exactly one report file" rule (`test_readonly.py:400`, `test_cli_contract.py:1192,1361`). Not needed by #477 if the first status record is the observer's snapshot | Owner; PR #539 author |
| D-4 | Do `check --all --types question` reads consume on a live coordinator Run? | R1-V5/O-05 vs R2-V1 D-2, R2-V2 D-F | A seeded test: known `worker_done`, heartbeat and question messages, two reads with the observer template, then one consuming `check`; all seeded messages must still be returned. Until then #477 must forbid any message read in its route | Owner or the 409 session with live Orca |
| D-5 | Is the stock image's bypass default really in force on a given workspace? | R2-V2 D-C (UNVERIFIED) vs `README.md:60-66` (documents it) | One observation: in a fresh workspace started from the stock image, launch Claude through Orca and read the process arguments or the mode shown in the session (`/status`) | FU-1 runner, or any workspace owner |
| D-6 | Does `agent launch` create a Run or Dispatch? | R2-V2 D-A | `run-list` and `worker-list` immediately before and after one real `agent launch` | FU-1 runner |
| D-7 | Can a monitor identify and reach a workspace through Coder alone, with no self-registration? | V3 (proposal, section 5.4) | One read-only owner call to `GET /api/v2/workspaces` on the real deployment, recording `latest_build.status` values and `last_connected_at`; and one test that the `share = "owner"` Orca app is reachable with an owner API token (UNVERIFIED for subdomain apps) | Coder owner or admin; I have no token and did not call it |
| D-8 | Can a same-user process on a workspace assert a Claude Code permission class when posting to a session's inbox socket? If yes, the "held message" protection is advisory against a compromised local daemon | V3 F8 (assumes held) vs docs wording "asserts no permission class" | A test posting to the socket with and without a class assertion, in a bypass session | Anyone with a throwaway session; docs do not say |

## 5. Not yet examined by the debate: Coder#477 and workspace-to-orchestrator routing

Nothing below is posted. Each item gives the state or boundary at risk, what I verified now, what stays UNVERIFIED, and the check.

### 5.1 Is the listener still needed under watcher option A?

- **For the watcher: no.** `issue-watcher.md:28` (out of scope: "Any listener, port, webhook, GitHub Action or service"), `:43` (D1 option A: "No listener, inbound port or address registry"), `:47-49`; the owner's decision is in `seed-brief.md:46`; both files are tracked. The 2026-11-13 owner comment does not reverse it (#477 still has one comment).
- **For the observer on one host: no.** `superclaude observe` reads the local Orca CLI only (SC-15) and is single-host. Remote fleet is its release R4, gated on cross-host ownership joins "Not established" (V5 S10).
- **Possibly, for a cross-workspace read.** That need is real only when R4 or a TUIBBS screen gets a package. Neither has one (V5 S10: no R3 package; TUIBBS is "Background, not deciding", sibling `owner-decisions-20261108.md` item 4).
- **A per-workspace listener cannot solve the one revisit condition most likely to trigger a rethink.** The first of the nine revisit conditions is "stopped workspaces cause excessive waiting" (`issue-watcher.md:60`); the runbook says "a stopped workspace polls nothing (risk R9)" (`issue-watcher-setup.md:559`). A listener runs inside the workspace, so it is equally silent when the workspace is stopped; only the Coder control plane can start a workspace. So options B and C, which add a listener, do not cure it; a poller outside the workspace with Coder API access would (inference from the design text; not tested).
- **Another revisit condition is not met today.** "Account binding becomes available" (same line): #477 AC3 asks that workspace information be "securely associated with the appropriate GitHub account", which is the thing the design says does not yet exist. A registration cannot carry a verified GitHub binding until it does; at most it carries the workspace's own claim of its `gh` login.
- **Verdict.** Do not build a listener for the watcher. Keep #477 only as a narrowed read-only status feature if the owner confirms a cross-workspace reader (section 5.6). Otherwise close it.

### 5.2 What "TUI Panel" means in the owner's 2026-11-13 comment

- **The words.** The comment (2026-11-13T16:20:07Z, ironbelly) reads "Ensure this aligns with Orchestrator and TUI Panel". Titles: #339 is "[Feature]: Orchestrator - To Run and manage ALL sessions within a worktree"; #409 is "[FEATURE] TUI Dashboard to Manage Orchestration at Scale" (both re-read). The comment's two nouns mirror those two titles. The phrase "TUI Panel" appears in no owner-written file in either repo: a search of `/home/coder/workspaces` (excluding JSON) finds it only in this debate's own review files. So the reading "panel" = "dashboard" of #409 is a textual inference, about 75%.
- **TUIBBS is a real but weaker candidate (about 15%).** The owner's 2026-11-08 record item 4: "The owner is also exploring TUIBBS as an internal communication tool and platform for all human staff who manage agent teams; the observer may become a TUIBBS module" and the same file marks it "Background, not deciding for release 1". The sibling TUIBBS review: "TUIBBS runs on a separate SSH host ... Orca and the planned observer run in this Coder development environment", so Orca data must reach that host "by some other channel" (`tuibbs-review/notes-3.md:78-82`); the snapshot schema exists so a read-only Go screen can read it later (V5 S9). If TUIBBS is meant, a cross-workspace read route is not optional; if the #409 dashboard is meant, it is optional until R4.
- **The answer changes the transport, not the requirements.** Both candidates are read-only readers that need identity, freshness and no send path. TUIBBS additionally needs a Coder-to-another-host channel (push or pull). The one fact that settles it is the owner's reply (D-2).
- **A boundary risk either way.** The #409 draft says "Decide whether the observer reads through that registration" (item 5). The built observer has no network or credential path; it should not gain one until the route exists and the owner has decided (V5 D9 and R1-V5 concession 5 agree).

### 5.3 What a registered workspace may expose read-only

Rule: expose the smallest record that lets a reader tell workspaces apart and judge freshness; never expose content.

| Allowed (read-only, typed, with an age) | Why safe | Source |
|---|---|---|
| Workspace id, owner name, workspace name, build status, agent last-connected | Coder already holds these | Coder API fields (docs fetched now) |
| Profile slugs; "has Orca / has IronClaude" flag | Needed to show a Minimal workspace as "no orchestrator" | `image/catalogue/profiles.yaml:14-21` |
| Image hash, Claude Code and Orca versions | Version skew (A-009) | `main.tf:111`; `Dockerfile.coder:110` |
| The observer snapshot v1 (rows keyed by `dispatchId`, counts, `source.status`, `generatedAt`) | Already minimised: questions carry no subject, body or handle (V5 S5); atomic, mode 0600 | `snapshot.schema.json`; SC-17 |
| The watcher's `status --json` counts | Typed scalars only | `cycle.py:1326-1335` (V2 W-10) |

| Never exposed | Why |
|---|---|
| Orca pairing offer, device token, `CODER_AGENT_TOKEN`, `LITELLM_API_KEY`, any standing credential | `#195` PRD: the offer "is a bearer credential with no expiry" and whoever holds it "can control the workspace's Orca, including its terminals"; env keys are in the workspace environment (`runtime.sh:28`) |
| Addresses and ports | They change on restart; resolve at call time through the Coder app URL (5.4) |
| `retry[].argv` from the watcher status | A runnable launch command (V2 W-10) |
| Transcripts, prompts, issue bodies, message bodies, worker-written contract fields | Untrusted content; whether contract strings reach the sweep report is UNVERIFIED (R2-V1 5.1) |
| The sweep's Markdown or JSON, until the git-config thread on #539 is closed and a no-write form exists | `probes.py:309,1203-1214`; NFR-001 pins |

Every read must be non-consuming (D-4) and re-sanitised by the reader (two sanitizers exist, V5 O-12). A record older than a stated limit is shown stale, never current (the observer's own rule is 45 s for its feed; a registry needs its own).

### 5.4 How a monitor would learn workspace identity

- **Do not self-register for identity.** The existing heartbeat is anonymous and best-effort: `collector/app.py:5` ("anonymous (no auth)"), `emit-heartbeat:7-9` (workspace id and owner are positional arguments the workspace chooses), `collector/Dockerfile:11` binds `0.0.0.0:8080`. Anyone who can reach it can claim any id. #477 AC4 forbids that.
- **Take identity and lifecycle from Coder.** The Coder API lists owner, id, name, build status and agent connectivity (docs fetched now: `GET /api/v2/workspaces`, `Coder-Session-Token`). The workspace already authenticates to Coder with its agent token (`startup-git-askpass.sh:96-121`, endpoint `/api/v2/workspaceagents/me/external-auth`), so no new workspace secret is needed for Coder to know who is who. The agent token itself must never be given to a monitor.
- **Reach by name, not by address.** The Orca app has its own origin `orca--<workspace>--<owner>.<access host>` (`modules.tf:75-77`) and is `share = "owner"`, `subdomain = true` (`orca/module.tf:36-38`). A registry that stores "address and port" (AC3) would store values that change and could go stale; the app URL is derived from ids Coder already holds. Whether an owner API token can drive that app non-interactively is UNVERIFIED (D-7).
- **Use the workspace's own `gh` login as a claim, not a proof.** The watcher's identity is the workspace's own `gh` login (`issue-watcher.md:15`). Until Coder-owner-to-GitHub binding exists (revisit condition, `issue-watcher.md:60`), a monitor can record it as "reported by workspace, unverified".
- **Key by workspace id, never by name.** Image names embed owner and workspace name (`main.tf:111`); names can be reused after deletion. A registration keyed by name can route to a different workspace than the one registered.

### 5.5 The listener as a second command channel to bypass-permission sessions

- **Stock state (verified).** Every Claude launch in a stock workspace has permission checks off: `README.md:60-66` (deliberate, #455), `ccsession:135-141`, no override in the template, and the Orca launch goes through the same wrapper (`README.md:51`). Every orchestrator and every watcher-started session is therefore in the bypass class.
- **What a listener can and cannot do to such a session.** (a) Peer messages: the docs say a bypassing receiver holds each message unless the sender also identifies as bypassing, drops it after `dialogExpiry` (default five minutes), and never runs a slash command in it. A non-Claude listener process is not a bypassing sender, so peer messaging is not a usable route (V3 F8, re-read now). Whether a same-user process can assert a class is UNVERIFIED (D-8). (b) `orca agent launch --prompt`: starts a new top-level session in bypass mode with the given prompt; this is the only route that works, and it is exactly what the watcher does (`launch.py:95-116`).
- **Consequence.** A listener that accepts a prompt from outside is a remote-trigger for a permission-free session that holds the workspace's secrets (`LITELLM_API_KEY`, GitHub credentials in the environment) and can write and push. Today the guards sit in the watcher, not in any listener: a fixed prompt pattern, integer issue number (`launch.py:30-37`), allow-listed approver, label and unchanged-since-approval checks (`issue-watcher.md:659-661`, per R2-V2), day cap of 6 (`issue-watcher.md:501`, per R2-V2). A new listener must re-create them or it is weaker than the thing it replaces. The claim also reads untrusted issue text (R13, R18 in the runbook, per R2-V2), so even the watcher-started session needs the approver gate; a listener with a free-text route removes it.
- **An existing channel of the same strength already exists.** The Orca pairing offer is a no-expiry bearer credential that controls the workspace's Orca, terminals included (#195 PRD). The Orca server is loopback-only (`runtime.mjs:285`) and reached through owner-shared Coder apps (`orca/module.tf:36,54`). A new listener is justified only if it adds no new reachable surface and no weaker authentication than those. Hence the acceptance criteria below ban any free-text route and any standing credential in the registry.
- **UNVERIFIED.** What a paired Orca device can do beyond terminals (V3 relied on the PRD text); the host-level `CCSESSION_PERMISSIONS` value on each live workspace (D-5).

### 5.6 Exact proposed rewrite of Coder#477

Recommendation: **narrow** (about 65%), and only after the owner answers D-1 and D-2. If the owner says the observer stays single-host and TUIBBS is not near, **close**. Keep-as-written is the least defensible: its premise (a watcher that sends prompts to a listener) contradicts the built watcher.

Nothing here edits the issue. Paths are relative to the Coder repo root.

**A. NARROW (recommended).**

Title: `Read-only workspace status and identity for the Orchestrator observer (no prompt routing)`

Feature Summary:
> Let a read-only observer outside a workspace (IronClaude's `superclaude observe`, IronbellyOrg/IronClaude#409, and a possible later TUIBBS screen) see which of one owner's Coder workspaces exist, whether each is running, whether it has Orca and IronClaude, and its supervision status record. Nothing can be sent to a workspace through this feature.

Problem Statement:
> The IronClaude issue watcher (IronbellyOrg/IronClaude#331, rollout #450) runs inside each workspace and starts a claim with a local `orca agent launch`. By its design (IronClaude `docs/designs/issue-watcher.md` section 2.1, decision D1 option A, 2026-11-07) it needs no listener, inbound port or address registry, so this issue no longer carries watcher routing. What is still missing: the observer reads one host's Orca only (remote fleet is its release R4, gated on cross-host ownership joins) and cannot see another workspace.

Proposed Solution:
> Workspace identity and running state come from the Coder control plane (workspace id, owner, name, build status, agent last-connected), not from a value the workspace reports about itself. Each workspace also exposes one read-only record: profile slugs, Orca and Claude Code versions, image hash, a last-written time, the observer snapshot (`observe snapshot v1`) and the watcher's status counts. It is reached through an owner-authenticated route (for example the existing owner-shared Coder app mechanism), never an unauthenticated port. No address or port is stored; the route is resolved from the workspace id at read time.

Acceptance Criteria:
> - [ ] Identity (workspace id, owner, name) and running or stopped state are read from Coder. A workspace that reports another workspace's id is rejected and the event is logged.
> - [ ] No address, port, Orca pairing offer, device token, agent token, API key or other standing credential is stored in the registry or sent through this feature.
> - [ ] The read route returns only the fields listed under Proposed Solution, as a named, versioned record with an age. It runs no `superclaude sweep run`, writes nothing, and consumes no Orca message.
> - [ ] This feature has no prompt, command or session-start route. A test shows the route rejects every non-read request and every request type other than "status".
> - [ ] Only the workspace owner, or a read credential the owner issued, can read. Unauthenticated and other users' requests are rejected and logged; no unauthenticated port is exposed; transport is protected.
> - [ ] A stopped, deleted or never-registered workspace is reported as stopped, deleted or none, with a time. A record older than [N minutes: owner decides] is reported stale, never current.
> - [ ] A Minimal-profile workspace is reported as "no orchestrator", not as missing.
> - [ ] Each read writes an audit line (time, reader, workspace id, result) that the workspace owner can read.

Out of Scope:
> - Routing a prompt or command to any workspace, session or orchestrator.
> - The issue watcher (IronbellyOrg/IronClaude#331, #450); it needs no listener.
> - Choosing a grant format (IronbellyOrg/IronClaude#339) and Claude Code cross-session messaging.
> - Reusing the central heartbeat collector (`templates/VSCode-AIDev02/collector/`); its endpoint is anonymous.
> - Upstream component monitors (#419, `.github/workflows/orca-upstream-monitor.yml`).
> - Changing the sweep or the observer.

Components Affected (corrected paths): `templates/VSCode-AIDev02/main.tf`; `templates/VSCode-AIDev02/startup.tf`; `templates/VSCode-AIDev02/modules.tf`; `templates/VSCode-AIDev02/image/catalogue/orca/module.tf`; `templates/VSCode-AIDev02/image/catalogue/profiles.yaml`; `templates/VSCode-AIDev02/image/orca/runtime.mjs`.

Related: IronbellyOrg/IronClaude#339 and PR #539; #409 (and PRs #503, #514); #450; Coder#195; Coder#419. Depends on: the owner's answers to D-1 and D-2; observer release R4.

**B. KEEP (only if the owner revisits option B or C). Replace the Problem Statement with the status paragraph above plus "the owner has chosen to revisit option A", and replace the acceptance criteria with:**
> - [ ] The listener exists only in workspaces whose profile includes the `orca` and `ironclaude` slugs (`image/catalogue/profiles.yaml`). Minimal workspaces are reported as "no orchestrator".
> - [ ] A request is one of a fixed list of types. For the issue watcher the only type is `claim` plus one integer issue number (IronClaude decision D3); no free text ever reaches a session prompt, and the requester cannot choose a flag, a working directory or a permission mode.
> - [ ] An accepted `claim` starts a new top-level session in the workspace checkout whose `origin` is the issue's repository, with the same fixed prompt and launch the watcher uses (the claim level is decided in IronbellyOrg/IronClaude#450). It is not sent as a message to a running session.
> - [ ] The owner has accepted in writing the permission mode of every session the request starts. The stock image launches every Claude session with permission checks off (`README.md`, "Permission checks are off", #455); a live test records the actual mode.
> - [ ] Every request carries sender identity, a grant naming the workspace, the request type and an expiry, and a one-use nonce. Unsigned, expired, wrong-workspace and replayed requests are rejected and logged. The grant format is the one chosen in IronbellyOrg/IronClaude#339; the route stays disabled until it exists. The grant does not replace the watcher's approver, label and integer-only checks.
> - [ ] A request for a stopped, stale or deleted workspace is refused with a reason; it is never queued. A per-type rate cap applies (the watcher's is 6 a day).
> - [ ] Reading status and sending a request use separate credentials; a read credential is rejected by the request route; a test shows it. No address, port, offer or standing credential is stored.
> - [ ] Each decision is audited with time, sender, workspace id, request type, issue number and reason, and can be joined to the watcher's `audit.jsonl` by issue number and workspace id.

**C. CLOSE (comment text).**
> Closing as superseded. The IronClaude issue watcher was built as a poller inside each workspace (IronbellyOrg/IronClaude#331, rollout #450; design `docs/designs/issue-watcher.md` section 2.1, decision D1 option A, 2026-11-07), so no listener, inbound port or address registry is needed. Reopen, or open a new issue from the narrowed text in [link to the comment holding option A], when (1) one of the nine revisit conditions in that design section 2.3 occurs, or (2) the IronClaude observer's release R4 (remote fleet) or a TUIBBS screen has a task package that needs to read another workspace.

### 5.7 State, guard and boundary risks specific to #477 (checklist for any version)

1. **Stale registration.** A registry entry for a stopped or deleted workspace must not look live; key by workspace id; show age; remove on delete. Coder, not the workspace, reports deletion.
2. **Name reuse.** Names are reusable; ids are not (`main.tf:111` embeds names). Never route by name.
3. **Spoofed identity.** The existing collector accepts any caller; a registry that copies it fails AC4.
4. **Credential leakage into Coder's own stores.** The #195 PRD forbids putting a standing credential in agent metadata, `coder_metadata` or build logs because Coder stores them. A registration must not do so either.
5. **Read credential escalation.** A reader's credential must be rejected by any route that can start a session; the observer must never hold a credential that can.
6. **Consumed state.** A status read must not consume Orca messages (D-4).
7. **Version skew.** Carry Orca, Claude Code and image versions in the record (A-009).
8. **Untrusted content in records.** Records come from workspaces that read untrusted issue and repo text; readers re-sanitise and treat every string as data.
9. **Bypass by default.** Any route that can start a session starts it with permission checks off on the stock image (5.5). That is the strongest reason the narrowed version has no send route.
