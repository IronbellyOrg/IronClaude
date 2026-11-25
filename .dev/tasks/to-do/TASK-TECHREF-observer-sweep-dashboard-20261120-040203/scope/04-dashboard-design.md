# Scope 04: Orca dashboard / TUI design package (issue 409)
**Scope:** .dev/design/orca-observer-20261106/, .dev/issues/409/, .dev/research/orca-dashboard-20261105/
**Status:** Complete
**Date:** 2026-11-20
---

Paths: P = /home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106 ; R = .../.dev/research/orca-dashboard-20261105 ; I = .../.dev/issues/409. Cites are file:line unless noted. All read on branch docs/409-orca-dashboard-designs (HEAD 495eb96d1, commit "docs: publish Orca dashboard design collaboration package (#409)", 440 files, 101,520 insertions). That branch is NOT merged and has no PR (issue 409 comment 2026-11-17 07:09Z). UNVERIFIED here: whether it is merged since.

## 1. Inventory

Counts: 20 designs (set 1 = 10 "observation companions", set 2 = 10 "agent-supervision", dir `agent-focus/`); 18 scenario JSONs (9 variants + 9 scale: 5/8/10 owners x 50/80/100 sessions); 360 export files (2 sets x 3 widths x 60) = per width per set 10 concepts x 6 (.ansi .svg .txt .ascii.txt .png .mono.png); 2 contact sheets, 2 PDFs (10 pages each, QA.md:11), 2 offline galleries (set 1 `gallery.html` 15,653,280 B; set 2 `agent-focus/gallery.html`), `index.html`; 406 package files excluding `__pycache__` (I/package-manifest.json; ZIP 14,438,526 B, sha256 5e169bec...). Fixture sha256 1f17a907... (P/manifest.json:152). Tests: 19 `def test_` in `tests/test_designs.py` + 1 Node DOM test.

| Path (under P unless noted) | Kind | Size | Purpose |
|---|---|---|---|
| README.md | doc | 4,911 B / 53 L | package guide; scope, reproduce cmds, evidence boundaries, framework direction, "Honest completion" (README.md:50-52) |
| DESIGN-CONTRACT.md | doc | 2,951 B / 17 L | internal contract for the two layout workers: render-fn interface, required semantics, geometry (DESIGN-CONTRACT.md:6-14) |
| PLAN.md | doc | 11,349 B / 73 L | approved build plan: ten concept table (PLAN.md:40-52), verification (PLAN.md:64-70) |
| PREVIEWS.md | doc | 5,123 B / 135 L | GitHub-renderable page embedding the 20 PNGs + 2 compact examples |
| QA.md | doc | 6,638 B / 52 L | automated checks, independent review FAIL, limitations |
| concepts.md | doc | 6,593 B / 51 L | concept comparison tables (both sets), compact-mode rules, provisional top three |
| data-dictionary.md | doc | 4,098 B / 50 L | synthetic entities, state dimensions, measurements |
| integration-gaps.md | doc | 2,727 B / 28 L | verified vs not-established source facts |
| sources.json | evidence ledger | 4,103 B | E01-E13 sources, each tagged verified/inferred/unavailable/proposed |
| manifest.json | generated | 6,461 B | 10 concepts: name/question/omits/tradeoff/data/missing/slug/export paths; fixture sha |
| fixtures.py | code | 122 L | synthetic fixture generator `fixture(owners,count,variant)`, `metrics`, `normalize_events` |
| canvas.py | code | 122 L | char-cell Canvas, `sanitize`, `clip`, wcwidth, PALETTE, `selected_summary` |
| render.py | code | 130 L | exporter + gallery builder; CLI `--batch {1,2}`, `--show`, `--width` (render.py:127) |
| layouts/group_a.py, group_b.py, agent_focus.py | code | 230/224/183 L | the 20 render functions (+ `__init__`/pycache) |
| tests/test_designs.py, test_gallery.cjs | tests | 117 L / 22 L | 19 unittest cases; headless DOM-contract script |
| requirements.txt | config | 30 B | Pillow==13.0.0, wcwidth==0.9.4 |
| fixture.json | data | 116,780 B | base fixture (8 owners/80 sessions) |
| scenarios/*.json | data | 18 files | duplicate-out-of-order, empty, historical, injection, long-identifiers, missing-fields, shared-unmapped, source-loss, uneven + 9 scale-{5,8,10}-{50,80,100} |
| exports/{160,116,80}/ | generated | 9.1 MB, 180 files | set-1 renders (not read, counted only) |
| agent-focus/ | generated | 23 MB, 184 files | set-2: exports(180) + gallery.html + manifest.json + contact-sheet.png + portfolio.pdf |
| contact-sheet.png, portfolio.pdf, gallery.html, index.html | generated | 1.4 MB, 1.4 MB, 15 MB, 3.9 KB | set-1 aggregate views |
| I/ README, description, flags, scout, draft-notes, issue-body, posted-body, branch-links, create-result.json, attachment-status.json, package-manifest.json, ZIP, attachments/ (22 PNG) | issue record | ZIP 14.4 MB | record of `/sc:issue --create` for #409 (I/flags.md: mode feature, type cli, complexity simple, depth quick) |
| R/REPORT.md | research | 36,283 B / 264 L | 2026-11-05 tech-research report (10 sections) |
| R/MOCKUPS.txt | ASCII mockups | 19,164 B / 323 L | 10 plain-ASCII concepts (5 snapshot, 5 interactive) |
| R/snapshot-brainstorm/ | adversarial brainstorm | merged-requirements.md 123,967 B / 1,134 L (byte-identical copy `adversarial/merged-output.md`, same size) | static snapshot-report requirements; partial |
| R/interactive-brainstorm/ | adversarial brainstorm | merged-visual-design.md 16,193 B / 180 L | interactive TUI visual design; partial |
| R/visual-v2/ | images | 32 files | 10 earlier "v2" mockups (.ansi/.png/.txt) + contact-sheet + index |
| R/render-analytics-mockups.py, dashboard-study.html | code/html | 9.8 KB, 10 KB | earlier mockup renderer / study page |

## 2. What the design would read, write, and who consumes it

Governing statement: the whole fixture is "proposed fixture schema, never Orca API schema" (DESIGN-CONTRACT.md:11; data-dictionary.md:3 "NOT undocumented Orca API names"; sources.json E13 "proposed ... NOT Orca wire fields").

### 2.1 Sources the design assumes (README.md / sources.json / integration-gaps.md)
Fixture source ids are `demo:workers`, `demo:messages`, `demo:checks`, `demo:usage`, `demo:resources` (fixtures.py:14-18), each with `observed_at`, `age_s`, `coverage` ("complete fixture" / "partial" / "stale"). Intended real analogues, by the research REPORT.md:30-37 and sources.json:
- Orca `worker-list` (cursor paging, run scope, 1-100 limit; terminal resource state separate from task outcome) -> E01 verified from `--help`.
- Orca `orchestration check --peek/--all` (non-consuming; capped at 100 rows; no read-only paging) -> E02 verified; REPORT.md:36.
- Orca `worktree ps` (host scope, truncation flag) -> E03: one-row live call, "26 total workspaces and truncated=true"; no live records used in designs. (Note REPORT.md:34 saw 29 workspaces on 2026-11-05; different day, not a contradiction.)
- Orca `orchestration inbox` (row limit, no cursor) REPORT.md:37 (not in the package's ledger).
- IronClaude `WORKER-CONTRACT.md` (source + installed copy) for lifecycle vs result admission vs policy freeze -> E04; installed vs source differ (integration-gaps.md:7).
- GitHub / ClickUp: NOT read by the design. A case-insensitive grep of the .py, layouts, fixture.json, README, data-dictionary, concepts and sources.json for clickup|github|PR finds only license/repo URLs and prose, no data source; the session fixture has no PR/issue/link field (fixtures.py:30-43). ClickUp appears only in the issue record: the 2026-11-11 reviewer reply says it answers a ClickUp DM (issue comment, clayphi) and asks for PR/issue links.
- Historical template at commit 99bdf77d5 (E05/E06): visual inspiration only; "not proof of implemented integration".

### 2.2 Proposed fixture schema (fixtures.py:11-87; data-dictionary.md:7-40)
Top level: `synthetic, as_of, variant, sources{5}, orchestrators[], sessions[], worktrees[], requests[], edges[], events[], scope{host,expected_hosts,collection}, previous{as_of,source}`.
Session fields (fixtures.py:30-43): id, owner, worktree (nullable), lifecycle (running/settled/unknown), phase (work/review/queue/dependency), health, approval, freshness+age_s, result (succeeded/partial/failed/null), admission, evidence (complete/partial packet), policy (frozen/not), revision vs check_revision, tests, review, report, cost_usd+cost_window, cpu_pct, rss_mib, retry_count+retry_source, historical, label, timeline[20].
Worktree: id, branch, base, head, dirty, paths[], conflict="not established", policy. Request: id, question, owner "Human operator", requester, age_min, affected[], evidence, state. Edge: id, from, to, reason, sessions[], evidence. Event: id, seq, kind (new/worsened/resolved/unchanged), text, ref.
Derived metrics (fixtures.py:98-111): set-union `affected`, `cost` = sum of measured only plus `cost_measured` count, `unmapped`, counts by lifecycle, `normalize_events` (dedupe by id, keep highest seq).
Independent dimensions (data-dictionary.md:17-28): lifecycle, phase, health, approval, freshness, result, admission, evidence, policy, tests/review. 20 timeline buckets x 3 min, 07:00-08:00 UTC; "gap is missing observation, not idle time" (data-dictionary.md:40).

### 2.3 integration-gaps.md in full (28 lines) - real vs assumed
VERIFIED (integration-gaps.md:5-7): installed Orca version (`orca-ide` 1.4.245-aidev02.dfe1eb410300, sources.json:7) and version-matched docs read; worker-list is read-only with paging and scope; terminal resource accounting is separate from task outcome; one bounded live fleet observation returned explicit totalCount and truncation, no message contents or credentials captured; source and installed worker contracts read. Source test suite pins P0 converted-command set but installed contract describes P1 for 16 commands; sampled installed analyze/brainstorm/workflow have "Unattended mode" sections absent from sampled repo counterparts => "copy-specific rollout difference, not a claim that every documented phase is deployed". "The design never uses worker_done alone as report validation or admission."
NOT ESTABLISHED (integration-gaps.md:11-16), six items: (1) complete durable non-consuming decision/message enumeration beyond the inspected 100-row CLI view; (2) authoritative mission/owner/task/session/worktree joins across hosts ("workspace co-location alone is not ownership"); (3) population-wide coordinator admission record, revision-pinned verification feed, human-owner linkage; (4) provider cost/resource telemetry with coverage, currency, observation time, dedup identity; (5) durable event replay/ordering across host restarts and source-loss recovery; (6) native deep-link formats (no custom schemes invented).
PROPOSED ONLY (integration-gaps.md:20): fixture schema, derived metrics, display buckets, source ids, navigation interactions. "Original tools retain task lifecycle, retries, scheduling, worker management, approvals and Git/worktree ownership."
MISSING-DATA RULES (integration-gaps.md:24): show unavailable/stale/unknown explicitly; keep last-known qualified; global counts name scope and completeness; a filter states its denominator; source loss does not resolve questions, fail sessions, lift a freeze or authorise retries; "partial result with complete files is inspectable but not necessarily admitted".
NEXT EXPERIMENT (integration-gaps.md:28): supervised synthetic walkthrough (find cross-owner decision, tell stale test from failed worker, locate frozen worktree, identify incomplete cost coverage); "Only then investigate a small read-only adapter against confirmed source contracts, with no operational controls and no LLM polling loop."
sources.json other tags: E11 "inferred" (cross-record analysis feasible, joins/coverage need validation); E12 "unavailable" (complete message history, authoritative cost, population-wide admission ledger, 100-session runtime performance); limitations list sources.json:24 (original "beautiful final historical mockup" not recovered; no deep link invented).

### 2.4 What it writes
Nothing operational. README.md:17 "Nothing invokes operational controls. Evidence-inspector navigation and fixture playback are local only"; README.md:31 "No process is started for live observation and no periodic collection occurs"; README.md:42 no installs/config/commits/pushes/PRs/deployments. DESIGN-CONTRACT.md:11 "Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only." Only file writes are the generator's own exports (render.py writes exports/, gallery.html, manifest.json). Gallery: no `fetch(` and no `setInterval(` (test_gallery.cjs:19 asserts both absent).
Contrast (R/): the 2026-11-05 interactive mockups list "proposed: r reply . a acknowledge . x resolve" as three separate future actions (merged-visual-design.md:26; MOCKUPS.txt Triage Rail), and the REPORT.md plan step 6 "Add deliberate actions only after authority tests" (REPORT.md:217). The 2026-11-06 package removed all actions. Issue #409 out-of-scope list bans approve/retry/terminate/spawn/merge/rebase/delete/instruct (issue-body.md:89).

### 2.5 Who consumes it
A single human supervising 5-10 orchestrators / 50-100 sessions (description.md "Context"; PLAN.md:3). Package audience = the issue owner choosing a visual direction ("The human chooses the visual direction before production implementation", PREVIEWS.md:3). Named reviewer feedback (issue comment 2026-11-11, clayphi): wants plain-English task summary, done/left, "needs me", PR/issue links, step-flow colours, click-to-open session; picks Fleet Quilt, Decision Desk, Loop Detector/Mission Pulse, Signal Bridge. These asks require data the fixture lacks (PR/issue link, session-open link, step flow): issue body "Alignment decisions" item 3 (issue 409 live body line 114).

## 3. Status: built vs only designed

### 3.1 Built (inside the design package; all synthetic)
- Prototype renderer: Python + Pillow 13.0.0 + wcwidth 0.9.4 (requirements.txt:1-2); text-cell Canvas is the single source for ANSI/plain/ASCII/SVG/PNG/PDF (PLAN.md:30; canvas.py, render.py). 20 layout functions in layouts/group_a.py (5), group_b.py (5), agent_focus.py (10). Reproduce cmds README.md:22-29; render.py CLI `--batch 1|2`, `--show <slug> --width N` (render.py:127).
- Exports: 60 colour + 60 mono PNG, plus SVG/ANSI/plain/ASCII, at 160/116/80 (QA.md:11) -> 360 export files; 144 col is tested but not exported (QA.md:9). Two contact sheets, two 10-page PDFs, two offline galleries.
- Fixtures: 1 base + 18 scenario JSONs generated by fixtures.py; fixture sha256 1f17a907... (manifest.json:152).
- Tests: 19 unittest cases (test_designs.py) + 1 Node DOM-contract script (test_gallery.cjs:1 "Headless DOM-contract test, not a browser-rendering or physical-keyboard test"). I did not run them (read-only rule); results below are the package's own claims.

### 3.2 Quoted results
"Honest completion" (README.md:50-52): "Check QA.md and the export manifest for observed runs. Five-second readability is a target, not a measured human result. No capacity, latency, operational correctness or live Orca integration benchmark is claimed."
QA.md:9: "Final package suite: 19 tests passed, no skips ... covering 20 designs across 18 scale/scenario cases and four widths (160/144/116/80)". QA.md:11: gallery JS "syntax and DOM-contract simulations passed ... This is not a real-browser or physical-keyboard test."
QA.md:19: "**Verdict: FAIL for the inspected pre-correction snapshots.**" (independent reviewer read all 20 native 160-col images). 4 blocking findings: Delta Deck/Watchkeeper reused ledger layouts; missing report outcomes shown as pending; Worktree Atlas lacked branch/base geometry; compact Revision Drift overwrote the footer (QA.md:22-25). QA.md:29: "all four blocking corrections are in source and regenerated exports ... No new independent post-correction verdict was requested. Do not describe this as an independent PASS, measured aesthetics success or user approval."
Known limitations (QA.md:31-38): schema proposed; message enumeration/cost/admission joins unverified; source vs installed worker-contract rollout differs; Playwright real-browser check failed (Chrome absent at /opt/google/chrome/chrome, QA.md:36); Pillow output "not a claim of Bubble Tea runtime behavior"; TUIBBS AGPL components not extracted.
Contrast-checked palette ratios (QA.md:13): ink 14.56:1 ... failed-result 7.63:1.

### 3.3 Designed only (no code in the package)
Production TUI; Bubble Tea v2.0.6 / Lip Gloss v2.0.3 / Bubbles v2.1.0 "leading production candidate for a separate observer executable after a human chooses a design" (README.md:48; versions verified at TUIBBS-scp a6d7e7f, sources.json:19); Wish/Huh/Harmonica optional (description.md); Textual and Ratatui compared (REPORT.md:133-137); live Orca adapter ("a small read-only adapter", integration-gaps.md:28); real-user walkthrough; measured readability; any performance claim. The package says "No BBS application code or third-party screenshot is copied" (README.md:48).
Count of designs "chosen" by a human: none. concepts.md:44 "Provisional design judgment, not user approval": top three Signal Bridge, Proof Gate, Fleet Quilt; pairs Time Loom+Relay Map; set 2 starts Leverage Board, Collision Lens, Revision Drift (concepts.md:49).
Earlier research-stage status (REPORT.md:4): "Research and ten visual mockups assembled for review; design validation incomplete ... parent retains a failed budget gate. No product implementation authorized or performed." Interactive brainstorm: partial merge, 5/8 agreement (0.625), 284,611 tokens > 230,000 ceiling (REPORT.md:258). Snapshot brainstorm: partial, "No tests, collector calls, performance measurements or operator trials were performed" (merged-requirements.md:1037).

### 3.4 Where the package physically lives (checked with git, read-only)
- Commit 495eb96d1 (branch docs/409-orca-dashboard-designs) adds the package + `.dev/issues/409` record; it is NOT an ancestor of origin/master (61ac2c2e6) and the branch has no PR (issue comment 2026-11-17 07:09Z).
- BUT `git ls-tree origin/master -- .dev/design` lists 406 files and `git diff 495eb96d1 origin/master -- .dev/design` is empty: the identical package reached master inside PR #503 (commit 9e2608b03 "feat(observe): release 1 of the Orca terminal observer, superclaude observe (#409)", merged 2026-11-11). `.dev/issues/409` on master has 178 files incl. bmad/{prd,ux,architecture,spec}-orca-observer, final-review, visual-parity, ponytail-review-20261116. The export snapshot at /home/coder/.cache/ic-snap-20261120/master omits `.dev/`, so it shows none of this.
- `.dev/research/orca-dashboard-20261105/` is UNTRACKED locally (git status) and has 0 files in both 495eb96d1 and origin/master: the research REPORT/brainstorms exist only in this checkout working tree.

## 4. Relationship to the shipped observer (`superclaude observe`, src/superclaude/cli/observe/, 6,011 lines of Python in the snapshot)

Short answer from the evidence: the package is the observer's DESIGN SOURCE (visual and semantic reference), the observer is a SEPARATE, Python/Rich re-implementation that shares no code with it. The package itself never mentions the observer (written 2026-11-06, before it existed); later documents say so.

Explicit statements (all read):
1. Package says it is not an implementation: README.md:9 "design collaboration branch, not a production integration or deployment"; README.md:48 Charm stack is the candidate "for a separate observer executable after a human chooses a design"; issue-body.md:89 "This issue request does not authorize production code changes".
2. Issue 409 live body, correction banner (live body line 13, dated 2026-11-13 17:05 UTC): "A read-only observer, `superclaude observe`, is already on master: Release 1 (PR #503, merged 2026-11-11) and Release 2 ... (PR #514)". Status comment 2026-11-17 07:09Z: "The observer (`superclaude observe`) is built ... The issue text itself is stale."
3. Stack decision supersedes the package's framework direction: `.dev/issues/409/bmad/spec-orca-observer/stack.md:3` (on origin/master) "Recorded owner decision 2 (CONFIRMED 2026-11-08): Python + Rich ... This supersedes issue 409's stated preference for Go with Bubble Tea v2, Lip Gloss v2 and Bubbles v2." A Go/TUIBBS reader is deferred as a "later reader of the snapshot file" (ARCHITECTURE-SPINE.md:141,177,287,318, CD-12).
4. No code reuse, by rule: ARCHITECTURE-SPINE.md:172 "no code, import or vendored file from TUIBBS or the design prototype (`canvas.py` is never imported)"; SPEC.md:76 same; observe/sanitize.py:4 "the design prototype are not used" (own sanitizer, AD-9).
5. Visual reuse: observe/theme.py:5 "uses the design-mockup palette exactly" at truecolor; observe/view.py:96-109 has a "DECISION DESK" block (R3); sub-issue #606 (CLOSED) "Bring the theme, styling and layout of `superclaude observe` up to the Signal Bridge, Attention Ledger and Decision Desk design references" using the package PNGs `.dev/issues/409/attachments/{attention-ledger,decision-desk,signal-bridge}.png` and its 160/116/80 text exports (#606 body); delivered by PR #673 (merged 2026-11-19, "observer visual parity at 160, 116 and 80 columns"). Only 3 of 20 designs are cited as the visual targets.
6. Fixture-name parity (UNVERIFIED as a derivation): observe/fixtures/ has base, uneven, empty, missing-fields, long-identifiers, duplicate-out-of-order, historical, injection, source-loss, shared-unmapped (same 9 variant names as the package's scenarios) plus golden-* files; I did not diff contents.
7. Semantics inherited: the #606 body names "SEEN IS NOT RESOLVED" (count tile) and "RETAIN CONTEXT" (panel) as parts of the design references; the QUESTION-LINK gate name comes from the bmad spec (release-gates.md), not the package. Observer questions panel exists only for one named Run (`--run <runId>`), gate `QUESTION_GATE_PASSED = True` (observe/commands.py:67) citing `.dev/issues/409/owner-pass-record-20261112.md`.
8. Sweep link: docs/designs/orchestrator-mode.md:609 "layout is SPEC section 9 ..., copied from #409 at `495eb96d` because #409 is unmerged" and :463/:1018 "the ten #409 dimensions"; sweep/models.py:162 "The #409 dimensions, nine fields (OQ-11)". Live issue body line 21: "The sweep report in PR #539 is laid out from this issue's design package (the header, the Attention Ledger and the Shift Brief views, and the ten per-session dimensions)". (Sweep is another slice; noted for cross-ref.)
9. Proposed (not built) data coupling: live body alignment item 1 (line 112): observer should read the sweep's JSON rather than build a second collector. Observer today reads Orca directly via its own collector (observe/collector.py, adapter.py; UNVERIFIED in detail, owned by another slice).

Contradictions / stale statements to flag:
- C1. Live #409 body line 19 "No observer code exists yet: there are twenty synthetic designs, waiting for a human to choose a direction" and line 36 "the observer does not exist" vs banner line 13 and shipped code. Banner itself says treat such sentences as stale. Comment 2026-11-17 lists a pending "correction pass" waiting on owner grant.
- C2. "design package branch ... is not merged (no PR)" (comment 2026-11-17) and sweep design "#409 is unmerged" (orchestrator-mode.md:609) vs `git diff 495eb96d1 origin/master -- .dev/design` = empty: the same 406-file package is on master via PR #503. True reading: the branch/commit is unmerged; the content is merged. The sweep design's pin (495eb96d) is unreachable from master but its content is identical.
- C3. Framework: package README.md:48, issue-body.md:25, description.md say Bubble Tea/Lip Gloss/Bubbles preferred; shipped observer is Python/Rich by owner decision 2 (2026-11-08, stack.md:3). README.md:46 itself says the Python/Pillow renderer "is not a production-stack commitment".
- C4. Actions: research mockups (2026-11-05) propose reply/acknowledge/resolve actions (merged-visual-design.md:26); the package (2026-11-06) bans even greyed actions (DESIGN-CONTRACT.md:11); the sweep report prints a "next inspection" line which the live body flags as a contradiction (alignment item 2, line 113).
- C5. Counts of what is "built" in issue text: local issue-body.md:23 says ZIP "405 files, 14,435,766 bytes"; posted-body.md/package-manifest.json say 406 files, 14,438,526 bytes (refreshed); both are historical records of different moments (I/README.md chronology).

## 5. Requirements/decisions a later design must respect

From the package (DESIGN-CONTRACT.md:9-14, README.md:35-42, data-dictionary.md, integration-gaps.md:24):
S1. Worker result is not admission; lifecycle settlement, report status, acceptance, current tests and human approval are independent (README.md:37; data-dictionary.md:17-28). Admission only from an explicit fixture/source record, never inferred from settlement, packet completeness or passing tests (data-dictionary.md:25).
S2. Dirty != dangerous; stale != failed; overlap != conflict (worktree `conflict: "not established"`, fixtures.py:47); inspectable evidence != admitted; partial cost subtotal != total spend; tokens != progress (DESIGN-CONTRACT.md:11).
S3. Unknown stays unknown; null cost is not zero (data-dictionary.md:32, test `test_cost_missing_is_not_zero`); gap in timeline = missing observation not idle (data-dictionary.md:40).
S4. Evidence counts as current only when `check_revision == revision` (data-dictionary.md:28; DESIGN-CONTRACT.md:11).
S5. Affected counts are set unions, not sums (data-dictionary.md:39). No one-to-one session/worktree assumption (README.md:38; issue-body.md:80). Historical sessions counted separately.
S6. Filtered vs global counts always labelled; overview stays global (README.md:33; data-dictionary.md:46).
S7. Source loss does not resolve questions, fail sessions, unlock a freeze or authorise retries (integration-gaps.md:24). Policy-frozen work stays inert and for explicit human handling (data-dictionary.md:27; issue-body.md:82).
S8. Navigation only; no approve/dispatch/retry/merge, not even greyed (DESIGN-CONTRACT.md:11). Header always prints scope/freshness; narrow views keep first human decision + owner + affected scope (DESIGN-CONTRACT.md:11,14). Omission counts when lists are limited.
S9. Untrusted text inert: sanitize ESC/CSI/OSC, C0/C1, CR, bidi before any renderer; width by display cells; NO_COLOR and strict ASCII exports; no blinking/forced motion; no network, no LLM polling (PLAN.md:38,66-67; README.md:31,33; issue-body.md:79-83).
S10. Widths 160/116/80 composed separately, 80 = selected detail (PLAN.md:57; concepts.md:36). Hold/pause freezes display only and queues; resume discloses skipped observations (README.md:33).
S11. Data model is a proposed schema, never Orca API fields (DESIGN-CONTRACT.md:11; sources.json E13). Unverified source contracts must be named, not papered over (issue-body.md:84).

From research merged-requirements.md (static snapshot design; chat 80-col; 5-min cadence, so only the semantics transfer):
R1. DEC-6 (:77): a decision stays listed until explicit resolution; "A reply, read flag, snooze or vanished message is not resolution." COM-2 (:86): enqueued/delivered/processed/answered/resolved are separate facts. INV-021 (:1132): answered-but-unresolved items shown in own band, not counted as decisions, not eligible for OLDEST (interim rule; open).
R2. DEC-3/DEC-4 and §4 "Census and the oldest claim" (:160-167): while the message read is capped at 100 with no paging, counts print `>=N observed` and the frame says `OLDEST observed`, never `OLDEST`.
R3. COV-4 (:106): no concept prints a fleet-wide all-clear. Empty state reads `no attention items observed in <scope>` + coverage qualifiers. COV-3 (:105): a partial/failed source gives `0 observed (partial)`, never `none`. COV-5: unknown `?` never summed or zero.
R4. COM-5 + FG-8 (:89,1113): reads must be non-consuming; "FG-8 ... Cannot ship" if any mailbox is consumed or acknowledged. REPORT.md:41 "never consume or acknowledge the coordinator's mailbox merely to observe it."
R5. COM-4/COM-7 (:88,91): heartbeat only by matching an explicit closed routine form; anything unmatched is `unclassified` and shown in the decision block (noise preferred to a hidden decision).
R6. CHG-1/2 (:92-93): deltas only against the last successful comparable observation per source; a failed/partial read never gives a zero baseline; "vanished" never reads as resolved.
R7. VER-1..4 (:98-101): completion, terminal existence, process liveness, independent verification are four fields; reported-complete with failing/mismatched checks = `verify-gap` not green; `complete (claim only)` otherwise.
R8. BLK-6 (:84): run/task/attempt identities separate from host/workspace/session; superseded attempts never override current; workspace parentage is not a dependency (REPORT.md:49).
R9. COM-6 (:90): source text untrusted: quoted, truncated, controls escaped, secrets redacted and marked.
R10. Interactive (merged-visual-design.md:13-26): selection held by identity not row position; pause freezes rendering only ("PAUSED, N queued"); urgency double-encoded (glyph + colour); "Reported-done is shown as 'self-reported', not verified"; exact ids only in selected detail; asks pinned oldest-first with `+N more`; "Workers, asks and blockers are overlapping views ... overlap, not a sum".
R11. Feasibility gates FG-1..FG-14 (merged-requirements.md:1104-1119) are still the open-source-contract checklist: FG-1 complete non-consuming decision source, FG-2 revision-bound checks, FG-4 per-person human state, FG-6 persisted baseline, FG-7 expected-host inventory, FG-10 paging to the oldest decision, FG-14 cursor stability. REPORT.md:221-232 repeats as open questions.
Decision record: default for snapshot design = Concept A "Attention Brief" (merged-requirements.md:720) with one switch rule to E Delta Journal (:732); default interactive screen = A "Attention Rail + Fleet" "Provisional, not user approval" (merged-visual-design.md:161-162); package provisional top three Signal Bridge, Proof Gate, Fleet Quilt (concepts.md:44-47). No concept was approved by the owner in the files read; the owner's recorded direction decision is in later docs (#577; bmad spec, other slice).

## 6. Proposed assignments for 2 deep-investigation agents (this slice)

Agent A: "Design package vs shipped observer, requirement-by-requirement trace." Inputs: package S1-S11 and R1-R11 above; origin/master `.dev/issues/409/bmad/spec-orca-observer/{SPEC,rendering-rules,release-gates,unverified-register}.md`, `.dev/issues/409/visual-parity/REDESIGN-SPEC.md`, and src/superclaude/cli/observe/{view,render,theme,collector,adapter,questions,sanitize}.py + tests/observe/ (read via `git show origin/master:` or the snapshot at /home/coder/.cache/ic-snap-20261120/master). Deliver: (1) a table mapping each semantic rule to the observer code line that enforces it or "not enforced"; (2) which of the 20 designs the observer implements in whole/part (expected: Decision Desk, Signal Bridge, Attention Ledger; check others) and which package ideas are absent (PR/issue links, step flow, plain-English summary, session-open link from the 2026-11-11 reviewer comment); (3) diff the 9 same-named scenario fixtures (package scenarios/ vs observe/fixtures/) to settle the UNVERIFIED derivation in section 4 item 6; (4) confirm or refute C1-C5 against current live issue 409 body and PR #503/#514/#577/#592/#598/#673 file lists (read-only `gh pr view --repo IronbellyOrg/IronClaude`).

Agent B: "Integration-gap status: which not-established items have since been closed." Inputs: integration-gaps.md items 1-6, sources.json E01-E13, REPORT.md:30-37 and merged-requirements.md FG-1..FG-14, PLUS observer/sweep evidence: adapter-contract.md, snapshot-export-schema.md, observe/adapter.py + collector.py + questions.py (what Orca commands are allow-listed, 100-row cap handling, QUESTION-LINK), PR #586/#589 live tests (41 questions read twice, burst loss 30 of ~415), sweep collection (docs/designs/orchestrator-mode.md section 7.4 JSON schema; src/superclaude/cli/sweep/). Deliver per gap: closed / partly / still open, with the code or record cite, and which Orca fields are now REAL (observed from live CLI output) vs still assumed. Also locate the ClickUp/GitHub reads the reviewer asked for and state whether any shipped component reads them (design package reads neither).

Both agents: read-only; cite file:line; mark UNVERIFIED; note that `.dev/research/orca-dashboard-20261105/` is untracked and exists only in this checkout (not on master), so a tech reference must cite it as local-only or omit it.
