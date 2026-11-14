<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (Proposal A) -->
<!-- Merge date: 2026-11-14 -->

# Merged position for slot C-12 (slug `collaboration-exchange-capability`)

<!-- Source: Base (original, modified) - Change 1, Change 10: title, position line and lead paragraph; lead facts from base-selection.md and the debate-transcript.md convergence assessment -->

Status: Complete
Position: Staged hybrid on the Proposal A base (static kit as the unconditional layer, `kit: off` by default for every module until measured; no exchange transport built now; a build trigger and a separate enable trigger in 6.0; the transport design kept as binding preconditions in 3.2.1)
Date: 2026-11-15 (date of the base proposal); merged 2026-11-14
Code state read: HEAD `50d4d2b9d` (branch `ironbelly/shadow-runs`); E2 branch `origin/ironbelly/eval-tasklist-review-panel` read only through `git show`.

Lead. Base: Variant A (Proposal A, `variant-1-original.md`). Winner basis: combined score 0.9198 against 0.8747 for Variant B (Proposal B); the margin of 4.51% is below the 5% threshold, so the tiebreaker applied, and at level 1 (debate performance) Variant A won 12 diff points and Variant B 5. Convergence: 24 of 25 diff points were agreed (96%, threshold 80%); the one unresolved point is C-002, open only on its label. The invariant gate is BLOCKED_BY_INVARIANTS because INV-005 and INV-009 (both HIGH) are unaddressed; section 9 lists them and the other 14 findings without claiming any resolved. The resolution the debate reached (both advocates' Round 2 files) is a staged hybrid: Proposal A's static kit is the unconditional layer and defaults to `off` for every module until measured; nothing of the exchange transport is built now; Proposal B's transport design is kept as binding preconditions (3.2.1); a build trigger and a separate enable trigger govern what comes later (6.0). Reading note: first-person sentences come from the base author; 3.2.1, 6.0 and 9 and the sentences marked with a change number come from the refactoring plan.

## 0. Evidence base and tag legend

<!-- Source: Base (original, modified) - Change 2 (legend line on later E2 commits), Change 10 -->

- Baseline pin: E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` (called "pinned tip"). Facts from there carry no extra tag besides the verification tag.
- `[POST-BASELINE]`: a fact read at the later E2 commit `c44c98a77` (2026-11-14 14:19, "progress note, issue links, spike results and time-cap exceptions for the collaboration designs"). Later E2 commits up to `e2f2ac268` were not read by either advocate (section 9, INV-016). No decisive claim below rests on a `[POST-BASELINE]` fact alone; each one is paired with a pinned-tip or HEAD fact.
- `[CODE-VERIFIED]`: I re-read the file or blob at the cited line in this session. `[CODE-CONTRADICTED]`: the code or record shows the opposite. `[UNVERIFIED]`: taken from a research or synthesis file and not re-derived by me.
- Tags added by the merge: `[OPEN: ...]` marks an item the debate did not decide (listed in section 9). A fact added from a Round 2 file keeps the tag that file gave it and names the file; the merge executor re-read none of them. `[merge-author correction ...]` marks a wording fix the debate did not conclude.
- Paths: `BP` = `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/` at the named commit. `MR` = `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` at the pinned tip (1130 lines). Research files are `r09` = `research/09-collaboration-designs.md`, `r05`, `r10`; synthesis files `s05` = `synthesis/synth-05-options.md`, `s06`, `s07`.
- Not run: pytest, and none of the E2 harnesses. Everything below is read-only.

## 1. The position in one paragraph

<!-- Source: Base (original, modified) - Change 1: the tail of the third sentence group (from "and nothing of the hook transport") replaced by the staged resolution; the first, second and last sentences kept verbatim. Staged text from Debate Round 2, r2-advocate-A.md section 5(c) and r2-advocate-B.md sections 3 and 4.2 -->

The core ships, now and independent of any exchange decision, three things: H1 (every driving document is named in the brief by role, path and sha256), H2 (an over-limit finding line is repaired or re-asked before the merge, by one shared step; the form of the repair is slot C-06) and the H4 principle (no earlier review output is reachable by a reviewer; the exclusion list is module data), plus H3 as a per-module snapshot-base rule. It also ships a per-module move and lens catalogue, the "static kit", as module data that the brief builder renders into each module's briefs (E2's arm A2). Reviewers stay independent and blind. Exchange between reviewers (hook delivery, a board, a between-phase second pass) stays an optional capability: the module profile has one reserved key whose only legal value today is `off`, the off state is byte-comparable to the isolated panel, and nothing of the transport (the hook transport, the board, the seal, the message-kind registry, the launch adapter) is built now. Two separate triggers govern what comes later (6.0). The build trigger needs all three of: (1) C-07 adjudicated to a launcher with session persistence and a per-session activation channel, named by capability; (2) the X-14 metric of record and decision rule committed, and the C-08 served-model record landed; (3) a named owner and an expiry, with the recorded state "unmeasured, not rejected" if the trigger does not fire. The enable trigger, which is separate, lifts `exchange: off` for a module only on a pre-registered two-sided result against the static kit and the preconditions of 3.2.1. "Unconditional" here means "not gated on an exchange decision"; each module's profile still decides whether its briefs carry the kit (see 3.4).

## 2. Consistency with the adjudicated slots C-01, C-02 and C-03

<!-- Source: Base (original) -->

I read the three `ADJUDICATION-RESULT.md` files in `reviews/adversarial/core-shape-and-finding-contract/`, `ledger-clearing-and-verdict-authority/` and `merge-verdict-policy-and-quorum/`. This proposal agrees with all three outcomes. It depends on them at the points below and disagrees with none.

| Slot outcome (as the debate left it) | How this position relates | Dependency or residue |
|---|---|---|
| C-01: thin shared contract now, per-module engines, one limits-constants module, one repair step called inside both `parse_block` functions, shared `refs_norm`, hash and identity helpers; unknown keys open in both parsers; ledger passthrough keys deferred; no change to `cli/reflect` | H1 uses the shared hash and identity helpers. H2 is the "one repair step" of C-01; this proposal asks only that the step exist in the core, not for a particular policy. An exchange tag, if one is ever added, rides the open unknown-key rule (an in-line key is accepted by both parsers) or a sidecar, so no ledger schema change is on the critical path | Depends on C-01 INV-003 (HIGH, left unaddressed): whether a rescuing repair can coexist with "every existing pin unmodified" (`tests/review/test_review_findings.py:113` and `:117` pin `ok` False for anchor 201 and claim 301, as the C-01 result states). My H2 claim survives either way, because a re-ask without truncation is still a repair step; see 3.1 item 2 |
| C-01 withdrew the typed re-review line kind and `cluster_v2` for new ledgers | Nothing here needs a peer or own tag in the ledger row. `origin` already means three things (E2 own/peer, ledger rows `find/changed/outside/sweep`, diffgate `full/changed/unchanged`) [UNVERIFIED, from s06 CL-X11] | If exchange is built later it needs a key name other than `origin` (CL-X11, decided) and the "ledger passthrough keys" step that C-01 deferred |
| C-02: explicit per-row verification; a quorum of distinct `block_ok`-true reviewers typing `prior <lid> resolved`; the re-review panel is one reviewer (`apply_to: ["first"]`, `panel.py:600`, as the C-02 result states) | The kit and H1 are brief content for the first review; the re-review brief (`document_review_loop_prompts.md:48` [UNVERIFIED, r05 Unit 1]) is unchanged. Exchange text delivered to a re-reviewer would blur "a reviewer examined the revised region", which C-02 records with a quote | Depends on C-02 only in that the clearing record stays reviewer-authored and free of peer influence. C-02 holds "no effect on reflect for this slot only" (A-004); this proposal does not touch that |
| C-03: any-blocking union default, quorum over recorded completion states, partial panel is DEGRADED never PASS, `requested` count, independence recorded as "requested, not served" | The union and the quorum count reviewers as independent votes. A peer-delivered finding is not an independent vote. A hang-killed receiver is an incomplete reviewer and trips the quorum refusal, whose reviewer spend sits outside `cap_reviews` (C-03 INV-001, MEDIUM) | Depends on C-03 INV-006 and INV-007 (HIGH, unaddressed) only in that the exchange-off panel is the one those fixes are designed for. This proposal adds no new incomplete state |

## 3. Design consequence for the shared core and the named modules

<!-- Source: Base (original) -->

### 3.1 What the core carries now (unconditional layer)

<!-- Source: Base (original) - items 1, 3, 4 and 5; items 2 and 6 modified as marked inside them -->

1. H1, document roles in the brief. A module profile declares `driving_documents: [{role, path_template, sha256_source}]` using the roles the v2 citations already use (`plan/spec/source/test/diff/artifact`) [UNVERIFIED, r05 Unit 2]. The brief builder renders one line per document: role, path, sha256. At HEAD the shipped loop brief has five placeholders, all naming documents of the candidate's own revision chain, and no role for a second driving document; `document_review_loop_prompts.md:32` says "against the requirements it states" [UNVERIFIED, r05 Unit 1, quoted from the research file]. The E2 harness copied `source.md` into the sandbox and never named it in `BRIEF` (`run-reviewer.sh:13-17` at the pinned tip) [UNVERIFIED, r05 Unit 3].
2. <!-- Source: Base (original, modified) - Change 9b: tag only, no resolution --> H2, the pre-merge repair step. Required by every module because HEAD rejects `anchor` over 200 and `claim` over 300 characters in both parsers: `src/superclaude/cli/review/findings.py:104,118` and `findings_v2.py:111,126,132,136` [CODE-VERIFIED, re-read at HEAD]. In the E2 study, 88 of 92 dropped lines (48 of 49 blocking) were length failures [UNVERIFIED, r08 section 5 and s07 axis 3]. The step is the single one C-01 placed inside both `parse_block` functions; its policy (exact-prefix truncation with a repair flag, or reject with one re-ask) is C-06's. A re-ask is a new attempt and needs the served-model identity check (CL-C09, decided in s06). [OPEN: INV-009, see section 9]
3. H4 as a principle: "no earlier review output reachable by a reviewer". The exclusion list (E2: `.dev/reflect`, `.dev/research`, `.dev/eval-workspaces`, `.dev/tasks/done`, `MR:317-318`) is module data. At HEAD the reflect isolation snapshot exists and is pinned off: the flag comment at `src/superclaude/cli/reflect/models.py:92-95` reads "PINNED OFF by default" [CODE-VERIFIED]; `create_review_snapshot` at `config.py:155-210` [UNVERIFIED, r09 section 4.2].
4. H3 per module: the snapshot base is a module rule (PR review: the PR base; reflect: the committed ref of the audit). The E2 packages disagree on it (r3 and r5 the parent commit; r4 the T1-start tree with an empty `first_commit` in `manifest.json`), and r5's snapshot drops tracked-but-ignored files because `bin/sandbox-build.sh:25` runs `git add -A` without `-f` (CL-C01 routed here; CL-C11 decided) [UNVERIFIED for the line, from s06].
5. The catalogue: one source file per module holding the moves (E2 M1 to M10 for plan-versus-source review; other modules add their own). One file, no wrapper variants (CL-X10, decided). The brief builder renders it. The catalogue text is the only collaboration-adjacent content every runtime can carry, because every runtime takes a brief (3.3).
6. <!-- Source: Base (original, modified) - Change 5 (test sentence replaced) and amendment 6 (Open note on the reserved key) --> One reserved profile key, `exchange`, with the single legal value `off`. Any other value is refused at profile validation until an implementation registers. Open (INV-003): the key is code (`panel.py:37-46,160-176` rejects unknown panel keys) or a design-note entry (B R2 push-back 3); not decided in this slot. [OPEN: INV-003] The off state is pinned by the stricter test of 6.4 (no new file under `~/.claude/hooks/`, no `hooks.json` or merged-settings diff, no new run-record key attributable to exchange, a named installed-file-set diff), not by launch-argv and brief-byte equality alone: that equality proves the launched session unchanged, not inertness (A-002). E2 pinned the byte-equality property with an argv-diff test (r2 `test_launch_command_diff.py`, r1 T-10) [UNVERIFIED, r09 section 5].

### 3.2 What the core does not build now

<!-- Source: Base (original) - first paragraph; second paragraph modified by Change 8 (last two sentences added) -->

The shared hook library (baked arguments, always exit 0, `agent_id` skip, `flock` counter, finish signal, transcript seal, JSON `additionalContext`), the board path and atomic appends, the seal, the `panel-msg/1` message-kind registry with per-kind validators, per-session `--settings`, the `PANEL_COLLAB` switch implementation, the hook-side budget math (`B_f`, `turn_p90`, `T_report_p90`, `k`), and the alarm set (CONVERGENCE, ECHO, SNAPSHOT, SLO). All of these exist as designs and, in part, as packages on the E2 branch; they stay there as design input.

What the core keeps open for a later build at no cost now: unknown keys accepted (C-01); a sidecar placement preferred over an in-line tag (CL-C02; both parsers tolerate an extra key, and a search for `origin|ext` over `src/superclaude/cli/review/*.py` found no match, so nothing reads such a key [CODE-VERIFIED]); the run record (slot C-08) recording whether session persistence was on for each reviewer attempt; the `exchange` profile key above. The served-model and act-rate probe record (the served model, and the act rate per model and instruction form) is a now item: both advocates accept it as cheap, with consumers today (any per-model capability claim, kit gating) and no transport needed (B R2 sections 3 and 4.3; 6.3). Its home is not decided in this slot; B R2 4.3 names only "slot C-08 if that slot owns it" as a candidate, and no schema is specified here. [OPEN: INV-002, see section 9]

#### 3.2.1 Design note: preconditions for lifting `exchange: off`

<!-- Source: Variant B (Proposal B), Sections 2.1, 2.2 (as corrected), 2.5, 3.A, 5 and 6 (tests 4 and 6); Debate Round 2, r2-advocate-A.md section 4 and r2-advocate-B.md sections 3 and 4.3 - merged per Change 4 and amendments 2 and 11 -->

This is the content of the design note both advocates endorsed in Round 2 (Variant B's validator, sidecar and untrusted-anchor analysis kept as preconditions, not as code). It binds the lift of `exchange: off` for any module. None of it is built now. Its tracked-file home is not decided in this slot. Minimum contents:

1. Message validation (C-010). `panel-msg/1` with per-kind keys; forbidden keys `claim verdict blocking severity category note`; a 600-byte cap; the located-anchor rule (a located anchor is a 12 to 200 character substring of the reviewed document); harness-authored kinds only (the model-authored writers are not in the core).
2. Peer-origin tag (C-006). A harness-written sidecar keyed by reviewer id and finding id; the key is not named `origin` (CL-X11); quorum counts over own-origin lines only (U-014, C-02). [OPEN: INV-008 and INV-011, see section 9]
3. Untrusted text. An anchor taken from a reviewed PR diff is attacker-controlled and would be echoed into a peer's context; board files never enter the `review-telemetry` export; an adversarial-anchor test (injection text in an anchor, the 600-byte boundary, a forbidden key placed in a located-anchor field) (B R2 W6; A R2 section 4 item 3).
4. Fault injection. The seal fails closed and the review fails open (corrupt board line, missing transcript, lock timeout) (U-012; Variant B 6.4).
5. A single copy of the hook. The requirement list for the one correct copy: skip any call that carries `agent_id` (the r2 copy has no such branch), a timed lock (r1 uses `flock -w 4`, r5 an untimed `flock 9`), seal before first delivery and fail closed, and a replay test with a call that carries an `agent_id` and with two parallel calls (X-005; Variant B 3.A and 6.6).
6. Installer footprint, declared as a test item. The script lives in `src/superclaude/hooks/scripts/`, its name is in `_FRESHNESS_SCRIPTS`, and there is NO `hooks.json` entry (the `launch-level-pre-push.sh` pattern, `install_hooks.py:94-96`); activation only through a per-session channel baked by the adapter; no `src/superclaude/` path in installed text; the package is named `exchange/` because `.gitignore:13` is `lib/` [CODE-VERIFIED in B R1] (U-009). Variant B 2.2 wrote that the hook is "registered ... in `hooks.json`"; B conceded this as a defect (a `hooks.json` entry fires in every session), and this item replaces it (X-006).

Enable-side tests that need a launcher (B R2 Enable 2; A R2 section 3, Accept): when the transport exists, the enable trigger of 6.0 also requires S0 (hook delivery) and S2 (`--resume`) passes on the product launcher for every gateway-class model in the panel resolution, hook p95 over at least 30 calls per model against the 0.1 s planning budget, the fault-injection list above, and the installed-file-set diff of 6.4.

### 3.3 Named modules

<!-- Source: Base (original) - one cell (Tasklist and workflow) modified by Change 9b: tag only, no resolution -->

| Module | Consequence |
|---|---|
| Spec-review loop (v1 engine, `document_review_loop_prompts.md`, `spec-panel.md`) | H1 adds role lines to the first-review brief. The kit block is added to the first-review brief only; the re-review brief is unchanged. The loop prompt copies are outside `make verify-sync` (C-03 INV-013, LOW), so installed prompt skew is a known residue |
| Reflect Tier 2, engine B (`reflect-reviewer`, `reviewer-spec.md`) | `reflect-reviewer` has no Bash: `tools: Read, Grep, Glob, mcp__litellm__augment_code-augment_code_search, ... codegraph_impact`, `permissionMode: plan` (`src/superclaude/agents/reflect-reviewer.md:5-8`) [CODE-VERIFIED]. It is told it does not coordinate with the other reviewers, and the brief "MUST NOT instruct you to run anything" (`reflect-reviewer.md:28,59`) [CODE-VERIFIED]. Kit moves for this module are therefore written in Read/Grep/Glob/codegraph form, and the reflect profile starts with the kit off (3.4) |
| Reflect Tier 2, engine A (swarm, HTTP) | The swarm transport sends one user message and reads text back: `"messages": [{"role": "user", "content": prompt}]` (`src/superclaude/cli/swarm/transports/openai_compat.py:384-388`) [CODE-VERIFIED]. `ensemble.py:1-12` says Tier 2 invokes the swarm run surface with no in-process agent fan-out [CODE-VERIFIED]. There is no tool loop, so no PostToolUse point and no session to resume; a brief is the only thing it can carry |
| Tasklist and workflow (through reflect UC-1, slot C-05 default) | H1 (the tasklist's driving spec by role, path, hash) and the kit arrive through the reflect brief; no call-site change [OPEN: see section 9, INV-005] |
| PR code review (future) | Kit per lens in the lens brief; H3 base is the PR base; the adapter to `pr_submit.Finding` (slot C-10) is untouched |
| rf-qa replacement (future) | Read-only panel reviewers with kit text in Grep/Glob form; no exchange constraint on the first change (slot C-11) |

### 3.4 Where the kit is on or off

<!-- Source: Base (original, modified) - Change 6 (last sentence of the first paragraph replaced; second paragraph kept verbatim) -->

The catalogue, the brief slot and a profile key `kit: on|off` are core. A module's profile sets the value. The reflect profile, and every module whose result bytes are pinned (reflect contract 1.8.0, the 36-test verdict matrix), starts `off`, so adding the core element changes no pinned result. The spec-review and tasklist modules, whose briefs H1 already changes, also start `kit: off`: they turn `on` only after the cost measurement (6.2) and the hold-out of at least 4 unseen defects (6.7) pass (C-003; Debate Round 2, r2-advocate-A.md B-W2, which withdrew "first candidates for `on`"). The kit evidence is n = 2 against 4, one judge (4.2). The cost-gate dimension (elapsed or tokens, and the panel size it is read at) is an open item. [OPEN: INV-006, see section 9]

The catalogue and the class-card data of slot X-13 (process-redesign-modules) are one object if X-13 adopts class cards as data: a "move" text is a class card's `recipe_text`, and the moves M1 to M10 map one-to-one into classes C1 to C8 [UNVERIFIED, r10 Unit 11]. This proposal does not decide X-13; it requires that whichever shape X-13 picks, the kit is rendered from that single data source and not a second one.

## 4. Evidence

<!-- Source: Base (original) -->

### 4.1 What no exchange arm has shown (pinned tip and HEAD)

<!-- Source: Base (original) -->

| # | Claim | Evidence | Tag |
|---|---|---|---|
| E1 | E2's own requirements say the static kit may beat every exchange design and that, if none does, "the right design is the cheapest one: the harness fixes plus the kit in the brief" | `MR:917` (pinned tip) | [CODE-VERIFIED] |
| E2 | The E2 plan "cannot detect the central gain estimate of any slot"; only large effects separate from noise at n = 12 | `MR:1128` (pinned tip) | [CODE-VERIFIED] |
| E3 | At the pinned tip `lib/` is absent for all five packages (count of `/lib/` paths: 0 for r1 to r5), and the root `.gitignore:13` is `lib/` | `git ls-tree -r --name-only 6c09843...` per package; `.gitignore:13` and `:79` read from the blob | [CODE-VERIFIED] |
| E4 | Four hook scripts skip any call that carries `agent_id`: `r1 tools/radar-hook.sh:24-28`, `r4 bin/r4-hook:55-59`, `r5 bin/hook-posttool.sh:14-15`; the r2 receiver hook has no `agent_id` branch (zero occurrences). A reviewer that is itself a subagent would receive nothing from r1, r4 or r5 | blobs at the pinned tip | [CODE-VERIFIED] |
| E5 | Whether a PostToolUse `additionalContext` reaches a subagent's own model is not shown: E2 delivery evidence is main-thread `claude -p` sessions only | r09 section 4.2, section 9 gap 4 | [UNVERIFIED] |
| E6 | Act rates on injected text disagree for the same model: luna r2 4/5 and 5/5, r4 0 and 0.4, r5 1/5 and 3/5; ember r2 0/4 and 0/5, r4 0 and 0 | `r2 spikes/RESULTS.md:25-28`; `r4 spikes/out/act-rates.json`; `r5 spikes/NOTES.md` REQ-S3 | [CODE-VERIFIED] (pinned for r2, r4; r5 read at `c44c98a77`, the REQ-S3 text predates it) |
| E7 | r4's own gate says the F7 arm runs only with a non-zero luna act rate; the measured rate is 0/5, "so by the design's own rule the F7 arm is not run" | `r4 IMPLEMENTATION.md:159` (pinned tip) | [CODE-VERIFIED] |
| E8 | r3's two collab smoke rows both record `phase2_timeout` 1; its two baseline rows record 0 | `r3 results/smoke.jsonl`, `collab.phase2_timeout` (pinned tip) | [CODE-VERIFIED] |
| E9 | r5's one real exchange row (`smoke-f6diag-sl2-1`, sonnet receiver) delivered one card at call 18, then the receiver ran to the hang guard (266.4 s against a 1.5 x 176.9 s guard), was recorded INVALID, and the row is `quarantined` | `r5 results/results.jsonl` (pinned tip: status `quarantined`, 266.372 s); narrative in `spikes/NOTES.md` | [CODE-VERIFIED] for the row; narrative read at `c44c98a77` |
| E10 | At HEAD the Tier 2 swarm path is text in, text out (no tool loop); `reflect-reviewer` has no Bash and is told not to coordinate; the reflect child is launched with `--no-session-persistence`; `reflect --resume` means "skip the launch when the prior post is a pass", not a session resume | `openai_compat.py:384-388`; `ensemble.py:1-12`; `reflect-reviewer.md:5-8,28,59`; `runner.py:496-505`; `commands.py:290-294` | [CODE-VERIFIED] |
| E11 | HEAD reviewers are described as independent: "your independence is the point. You do not coordinate with the other reviewers" | `reflect-reviewer.md:28` | [CODE-VERIFIED] |
| E12 | External evidence on benchmark tasks says independent review plus aggregation is a sound default and debate adds little over voting; transfer to finding-set review is not shown | W01 C1, arXiv 2508.17536, as quoted in `s05` option 1 | [UNVERIFIED] |

### 4.2 The one measured cost of the kit (pinned tip) and the update at the later commit

<!-- Source: Base (original, modified) - Change 2: the last sentence of the "Reading, and its limits" bullet; all other text kept verbatim -->

- Pinned tip: `r5 results/results.jsonl`, same package `TASK-WF-design-20261108-041415`, sl2 panel (sonnet plus 2 luna): A2 (kit) 281.567 s and 46,018 output tokens against A1 rows 179.561 s / 29,688 and 174.274 s / 29,622. Ratio 281.567 / 176.9175 = 1.59 (+59 percent elapsed) and 46,018 / 29,655 = 1.55 (+55 percent tokens); three runs, one package [CODE-VERIFIED, row values re-read; the ratio is derived by me].
- `[POST-BASELINE]` Spike 4 rows of r5 at `c44c98a77` (`BP r5-coverage-deflection/results/s4-a1-*.json`, `s4-a2-*.json`; same harness, switches `PANEL_KIT` 0 or 1, `PANEL_COLLAB` 0, all three plan packages summed per row). I computed the means from the row files; status `quarantined` rows are included (one A1 hl2 row, one A2 hl2 row):

| Panel | Arm | n | Elapsed sum, mean (s) | Output tokens, mean | `found_14`, mean | `real_blocking_8`, mean | wrong blockers, mean |
|---|---|---|---|---|---|---|---|
| el2 (ember + 2 luna) | A1 | 4 | 390.9 | 67,664 | 0.75 | 0.00 | 1.75 |
| el2 | A2 (kit) | 2 | 430.8 (+10.2%) | 73,622 (+8.8%) | 2.50 | 0.50 | 1.50 |
| hl2 (haiku + 2 luna) | A1 | 4 | 696.5 | 205,564 | 1.50 | 0.50 | 2.25 |
| hl2 | A2 (kit) | 2 | 939.1 (+34.8%) | 300,462 (+46.2%) | 3.00 | 2.00 | 2.00 |

  Reading, and its limits: the kit cost is not +59 percent everywhere (+10 percent on el2, +35 percent on hl2), and the kit arm found more of the 14 known defects on both panels, with n = 4 against 2, one judge, one harness and a `found_14` that is not the metric of record of slot X-14. Part of that difference is within the spread of the A1 rows (A1 el2 `found_14` 0, 1, 1, 1; A1 hl2 2, 1, 1, 2). I do not claim the kit works. I claim that the only treatment in the study that has been run with a matching control shows a cost that can be priced and a direction that is not negative, and no exchange arm has a row matched against the A2 kit arm at a size that separates from noise (Advocate B's Round 1 weakness 3, conceded by Advocate A in Round 2 as B-W3: counted rows against the same-harness baseline exist at `c44c98a77`, 4.3).
- `[POST-BASELINE]` The pinned-tip statements "only single smoke rows exist" and "`lib/` is absent for r2 to r5" are stale at `c44c98a77`. Counts of `/lib/` paths there: r3 3, r4 7, r5 11 (committed with `git add -f`, per `PROGRESS-20261114.md` "Notes"), r1 0 by design, r2 still 0 [CODE-VERIFIED, `git ls-tree -r --name-only c44c98a77`]. r1's `results/results.jsonl` holds 14 rows (11 collab-0 or collab-0-extra rows and 3 collab-1 rows, two of them `incomplete`), and Spike 4 values files exist for all nine package-panel cells of r1 and r2 and for r5's el2 and hl2 cells.

### 4.3 What the later commit says about exchange arms (all `[POST-BASELINE]`, each paired with a pinned fact)

<!-- Source: Base (original) -->

- The measured `k` (how many messages a role may receive inside the time budget) is zero almost everywhere. r1 values files: 15 of the 18 role values are 0 (two are 2, one is 1) over the nine panel-package cells (`BP r1-move-radar/values/<panel>/<pkg>.json`, read with `jq`). r5 Spike 4 (`spikes/NOTES.md`): `k` 0 in all six el2 and hl2 package cells, `budget_ok` false in two of them. r2's values files show `k` 0 on el2 and 2 on hl2 and sl2, but r2 measures turns without the rule that s06 CL-X5 decides is correct (group by `message.id`, skip subagent entries, drop the first response), so I do not rely on r2's 2. Pinned corroboration: the r5 pilot already gave `k` 0 and `budget_ok` false on sl2 (`spikes/NOTES.md:50`, `{"k": 0, "budget_ok": false}`) [CODE-VERIFIED].
- Because of that, the owner authorised a time-cap exception: "the +35% elapsed-time rule may be exceeded so that the collaboration arm runs on el2, hl2 and sl2" (`r1 OVERRIDE.md:3`), under which every role with measured `k` 0 is forced to `k` 1 and the hang guard becomes 3.0 x the baseline (`OVERRIDE.md` section 2 table). The same exception was added to all five designs (`PROGRESS-20261114.md`, "Stages done") [CODE-VERIFIED, blobs read at `c44c98a77`]. So the exchange arms as designed do not fit their own time rule on these panels.
- First counted snapshot, ember panel, one row per cell, `found` of 14 on the two defect-rich packages (collaboration against the same-harness baseline): design 1 1 vs 0; design 2 0 vs 2 (one of three packages invalid in both arms); design 3 1 vs 3; design 4 2 vs 1; design 5 1 vs 1 (`PROGRESS-20261114.md`). Sums 5 against 7. The note itself says these differences "are inside the noise" and that delivered-message counts were not yet checked [CODE-VERIFIED as a statement of the note]. I use it only to say that no exchange arm has separated from its baseline in the first counted rows, not to say exchange loses.
- The r5 note reports that the kit run was the same size effect seen again in a real F6 run ("sonnet with the catalogue kit takes about 280 s against 177 s for A1: this is the kit slowdown the pilot measured (0.59 against a limit of 0.34)", `spikes/NOTES.md`) [CODE-VERIFIED, `c44c98a77`]. That is a cost that has to be priced per module, which section 6 does.
- The progress note records that the unit-test counts 138, 358, 89, 106 and 108 were "re-run independently" (`PROGRESS-20261114.md`) [CODE-VERIFIED as a statement; not re-run by me]. At the pinned tip these were self-reports and the static `def test_` counts were 103, 163, 89, 90 and 82 [UNVERIFIED, r09 section 2.2]. The statement narrows, but does not settle, the pinned-tip doubt about test counts.

### 4.4 Why the kit, and not exchange, is the layer every module can carry

<!-- Source: Base (original, modified) - Change 2 (the `--resume` clause replaced, with the pinned-tip citations) and Change 7 (one sentence appended) -->

The runtimes at HEAD are swarm workers (HTTP, one user message), Agent-tool reviewers (read-only, no Bash, `permissionMode: plan`) and headless `claude -p` sessions. Only the third can carry a PostToolUse hook, and only if persistence is on and `--settings` is supplied per session (r09 section 4.1) [UNVERIFIED]; E10 shows the first two cannot. A brief reaches all three. F1 (between-phase) is the only exchange family that needs neither a hook nor a model-side write, but it has no clean measured success in any runtime (E8). Its `--resume` dependency on gateway ids is recorded as passing: S2 (`--resume`) PASS for four gateway ids in two packages at the pinned tip (`BP r5 spikes/NOTES.md:23-30`; `BP r2 spikes/RESULTS.md`) [CODE-VERIFIED as recorded lines, B R1 and A R1 concession 1; the runs were not re-run and the r5 transcripts are not committed]. That is plumbing on the E2 launcher, not benefit and not a product launcher (X-002, B 82%); the base statement that the dependency "is not evidenced" was stale. F1 is also not buildable by reuse: no existing path passes a session id to `claude`, the swarm transport is stateless (`openai_compat.py:384-388`), so F1 on swarm needs a new round-two dispatch step and the second prompt must carry the reviewer's own phase-1 report; no F1 run exists on swarm [CODE-VERIFIED for the code facts, B R2 V6; the absence of a run is [UNVERIFIED]].

## 5. Invariants

<!-- Source: Base (original) - two cells modified by Change 9b (tags only, no resolution): the INV-A row (consistency tag, see merge-log) and the INV-G row -->

Preserved (and why):

| Invariant | Why this position keeps it |
|---|---|
| Reflect contract 1.8.0 byte-identical (INV-A) | No change to `src/superclaude/cli/reflect` and no contract key [OPEN: see section 9, INV-005]. The reflect profile starts with `kit: off`, so engine B's briefs and outputs do not change (3.4) |
| The 36-test verdict matrix (INV-B) | `derive_verdict` is not touched; no exchange state enters the verdict |
| findings-v1 grammar and `review merge` unchanged; unknown keys accepted (INV-C) | The kit asks reviewers for findings in the existing grammar; no new line kind; H2 sits inside the `parse_block` step that C-01 already placed |
| Reviewers mutually blind and mechanically read-only (INV-G, HIGH) | Exchange off means no reviewer sees another's text [OPEN: INV-013]; no new lane is added, so no Bash-capable lane is introduced into the PR or rf-qa modules |
| Telemetry carries no document text (INV-H) | The kit adds a catalogue hash to the run record, not text; an exchange board would add message text that INV-H would have to cover |
| Shadow mode changes no verdict (INV-L) | Reflect stays `kit: off`; nothing in the shadow path changes |
| Installed-path rule (INV-F) and `.claude/` never staged | The brief builder reads the catalogue through the installed form (`~/.claude/skills/<name>/refs/...` or a project `.claude/` copy), never a `src/superclaude/...` path in an installed primitive |
| UV only; fork-only PR target; `.dev/tasks/` staged | Unaffected |

Endangered (by this position):

| Invariant | How, and the mitigation |
|---|---|
| INV-G (read-only) | Kit recipes written for a shell ("run grep ...") would instruct a no-Bash reviewer to run something, against `reflect-reviewer.md:59`; r10 Unit 5 notes the E2 recipes assume a shell [UNVERIFIED]. Mitigation: a test over the rendered briefs of every read-only lane that fails on an instruction to execute a command |
| INV-L / INV-A if the kit is turned on in reflect | It would change reviewer output, though not the verdict map. Mitigation: `kit: off` in the reflect profile until a reflect-specific measurement exists |
| INV-K (sync gates) | A catalogue file and a profile key add a layout item; `make verify-sync` must cover it. The loop prompt copies are already outside the gate (C-03 INV-013) |
| Cost caps | The kit alone cost +59 percent elapsed (pinned, one package) and +10 to +35 percent in the later spike rows; the repository rule on the +35% cap is a study rule (`MR` S3.3 via r09), not a product constant [UNVERIFIED] |

## 6. The test or measurement that would show it right or wrong

<!-- Source: Base (original, modified) - Change 3 (new 6.0, 6.1 modified), Change 5 (6.4 replaced), Change 6 (6.2 modified), Change 8 (6.3 sentence added); the base numbered list is now headings 6.1 to 6.7 with the same numbers -->

Sections 6.1 to 6.7 are the base's numbered measurements 1 to 7; text that says "measurement N" refers to 6.N. Section 6.0 is new: it fixes when the transport is built and when exchange is enabled.

### 6.0 When the transport is built and when exchange is enabled

<!-- Source: Debate Round 2, r2-advocate-B.md section 3 (Build 1-3, Enable 1-2 with amendments) and r2-advocate-A.md section 5(c) - merged per Change 3 and amendments 1, 2 and 9 -->

Two triggers, kept apart. Building the transport (the instrument for the comparison) is not the same act as enabling exchange (the capability). The base's single gate, "not built until an exchange arm beats the kit", had no owner and conflated the two (Advocate A Round 2, B-W1; Advocate B Round 2, C-002). Both advocates endorsed the form below; C-002 stayed unresolved only on its label (A 52 against "Merge 62").

Build trigger. The transport is built, still off by default, only when all three hold:

1. Launcher (slot C-07, `dispatch-and-launch-mechanism`). C-07 is adjudicated to a launcher with session persistence, a per-session activation channel and a headless main-thread lane. The condition names the capability, not the `--settings` flag: the repository's only `--settings` precedent is the interactive ccsession shell launcher (`skills/ccsession-tag/ccsession:1150,1259`), and C-07 may choose another channel (B R2 push-back 2 and V5). Today the gateway launch map is empty (`review-tiers.default.json:25-29`, `"launch": {}`, note "dispatch mechanism per model not defined yet") and `--settings` is absent from `src/superclaude/**/*.py` [CODE-VERIFIED, A R2 V5 and V6; B R2 V1 and V5]. If C-07 yields no such launcher, the hook half is dropped (section 8, answer 6).
2. Metric and record (X-14, C-08). The X-14 metric of record and the decision rule are committed, and the C-08 record of the served model has landed, so that act rates and outcomes can be interpreted.
3. Owner and expiry. A named owner and an expiry (the date or event at which the trigger is re-evaluated), with the recorded state "unmeasured, not rejected" if the trigger does not fire. The owner is the lead's decision, not C-12's. Residual: a design note has no mechanical consumer, so an expiry triggers nothing by itself (INV-001, section 9).

Conditions 1 and 2 are cross-slot dependencies (C-07; X-14 and C-08), not C-12 deliverables. The C-08 served-model and act-rate record is satisfiable now and does not wait on the transport (B R2 section 3, Build 2).

Enable trigger. `exchange: off` is lifted for a module only when all three hold:

1. A measured result against A2. An exchange arm is run against A2 (the static kit, not the isolated panel) on module-matched ground truth, with a hold-out of at least 4 unseen defects (a floor for a sanity check, not a power guarantee), a power calculation, and a rule on gain and cost against A2 registered before the first run. The rule is two-sided because "beats A2" may be undetectable at the available n (the E2 plan cannot detect the central gain at n = 12, E2 in 4.1). Outcomes: "the arm clears the minimum gain with an interval that excludes zero" (enabling may proceed); "no effect detected at n" (stay off, recorded so); "underpowered, unmeasured" (stay off, recorded so).
2. Module scope. Tasklist review only, where ground truth exists (A-001: 16 items in 3 plans, 6.1); PR review and rf-qa stay off because no ground truth exists for them. [OPEN: INV-014, see section 9: whether tasklist review reaches a lane that can host exchange]
3. Preconditions met. Every item of the design note (3.2.1) is met, including the adversarial-anchor test, and the launcher-side tests listed at the end of 3.2.1 pass.

### 6.1 Matching-control comparison (feeds the enable trigger of 6.0)

<!-- Source: Base (original, modified) - Change 3 and amendment 1: the first two sentences kept verbatim; the wrong-if/right-if sentences replaced by the two-sided rule and the corrected "costs nothing extra" sentence -->

On a package set with ground truth (E2: 16 items in 3 plans, where 3 items carry 91 percent of defect-rich catches, 194 of 214 [UNVERIFIED, r08 section 3]), run A1, A2 and each exchange arm at one panel with the metric of record chosen in slot X-14, the decision rule committed before the first run, and replicates sized by a power calculation. The E2 plan itself cannot detect the central gain at n = 12 (claim E2 in 4.1). The result is read by the pre-registered two-sided rule of 6.0 (enable trigger), not by "beats A2 or not": the outcomes are "clears the minimum gain with an interval that excludes zero", "no effect detected at n" and "underpowered, unmeasured". The minimum gain is fixed before the first run; E2's own requirements name a margin for an exchange arm over A2 (`MR` section 4, referenced at `MR:917`). This is the same experiment Proposal B would need to justify the transport. It costs nothing extra for running the arms on the E2 launcher; the result binds a product decision only after a repeat on a product launcher with the served model recorded (C-08). (C-008, B 57%: partly overtaken at `c44c98a77`, [POST-BASELINE] and secondary evidence only; the pinned-tip fact is E3: no E2 arm ran from its commit.)

### 6.2 Kit cost per module

<!-- Source: Base (original, modified) - Change 6 and amendment 8: the `kit: on` condition extended -->

Repeat A2 against A1 with n of at least 4 per arm on each panel the module uses; record elapsed ratio and token ratio; the module profile turns `kit: on` only if the ratio is inside a cap the module owner states and measurement 7 (6.7, a hold-out of at least 4 unseen defects) passes. Until both pass, the kit stays `kit: off` for every module (3.4). The cost-gate dimension (elapsed or tokens, and the panel size it is read at) is an open item. [OPEN: INV-006, see section 9] This proposal is wrong if the kit gain is indistinguishable from the A1 spread, as the 4.2 means partly are.

### 6.3 One common act-rate probe

<!-- Source: Base (original, modified) - Change 8: one sentence added -->

One common act-rate probe (s06 CL-X1, CL-X2, CL-C14 are class N): one probe, all models, same instruction form, 5 or more sessions per model. It decides whether any hook family is deliverable to a given model and costs hours, not a build. Recording its result (the served model, and the act rate per model and instruction form) is a now item whose home is not decided in this slot (3.2). [OPEN: INV-002, see section 9]

### 6.4 Off-state test (core, cheap, run now)

<!-- Source: Base (original, modified) - Change 5 and amendments 6 and 7: replaced by the stricter test from Debate Round 1 (A-002, both advocates QUALIFY) and Round 2 (B R2 W2). The baseline sentence is a merge-author correction -->

With the `exchange` key at `off` and `kit: off`, all of the following hold:

1. Launch argv and brief bytes with `exchange: off` equal those of a profile without the key; with `kit: off` the brief equals the baseline, which is today's brief plus the H1 lines. [merge-author correction of the base 3.1/6.4 contradiction (the base said "equal today's brief" while H1 ships unconditionally); not debate-concluded; INV-004 stays open, section 9]
2. No new file under `~/.claude/hooks/`.
3. No `hooks.json` or merged-settings diff.
4. No new run-record key attributable to exchange.
5. A named installed-file-set diff: the test lists the installed files, so that a dormant file is a declared item, not an accident.

Reason: byte equality of argv and brief proves the launched session unchanged, not inertness; it cannot see installer, `hooks.json` or telemetry effects (A-002; C-011). The off state of the reserved key and the catalogue passes checks 2, 3 and 5 by construction for hooks, `hooks.json` and `~/.claude/hooks/`; if the key is code, the key itself is not covered by that argument [OPEN: INV-003, see 3.1 item 6]. The test fails if the reserved key leaks behaviour.

### 6.5 Brief lint test (core, run now)

<!-- Source: Base (original) -->

Every rendered brief names each driving document by role, path and sha256 (H1); no read-only lane's brief contains an instruction to run a command.

### 6.6 Existing pins

<!-- Source: Base (original) -->

The full current suite passes unmodified apart from the C-06-dependent pins named in C-01 INV-003; `make verify-sync` and `make lint-architecture` pass.

### 6.7 Catalogue provenance control

<!-- Source: Base (original) -->

Both E2 catalogues (M1 to M10 and C1 to C8) were induced from the same ten missed issues [UNVERIFIED, r10 Unit 11]. A hold-out of at least four defects not in those ten is needed before any kit gain is read as general. Measurement 1 must include it.

## 7. Effect on future PR code review and on rf-qa replacement

<!-- Source: Base (original) - first two bullets; third bullet modified (consistency adjustment following Change 1 and Change 3, see merge-log) -->

- PR code review. The module gets H1 (the PR description and diff by role, path, hash), H3 (the PR base), and a lens catalogue in each lens brief, all brief text. It needs no hook, no persistence and no Bash. The adapter to `pr_submit.Finding` (slot C-10), the `Finding` type and the FSM are untouched. Each PR review round is one panel run with no second pass, so the cost of a round does not grow with an exchange phase; the cost of the kit per round is the A2-over-A1 ratio of measurement 2, to be measured on PR-sized inputs before `kit: on`.
- rf-qa replacement. The first-change candidate, the `/task` phase gate, replaces read-only lens agents with mechanically read-only panel reviewers. The kit is brief text in Grep/Glob form and adds no lane. Hook-delivered exchange would need a main-thread `claude -p` lane, and s05 comparison row 6.6 records that "hook delivery excludes read-only subagent reviewers and swarm workers" (`s05` options table) [UNVERIFIED]; adding such a lane to rf-qa would conflict with slot C-11's read-only requirement and with the E2 launcher's open Bash (`run-reviewer.sh:48`, via `s07` axis 5) [UNVERIFIED]. With this position that conflict does not arise for either module.
- What would change this: an exchange arm meeting the enable rule of 6.0 (measurement 1) on a module-matching package. Then `exchange: off` is lifted for that module once the preconditions of 3.2.1 hold. The transport itself is built earlier, on the build trigger of 6.0, as the instrument for that comparison; it is a new capability behind `exchange`, with the hook skeleton written once from the four copies, and the open-key and sidecar choices of 3.2 keep the ledger and parsers ready for it.

## 8. The strongest objection and my answer

<!-- Source: Base (original, modified) - Change 2 (answer 2 corrected on two stale facts, with the retrofit qualifier from amendment 3) and Change 7 (answer 6 appended after answer 5); the objection and the residual-risk paragraph kept verbatim -->

Objection: the exchange designs are the most mature artefacts the study produced (five packages, one common hook skeleton written four times, partial gate-0 results, and, at the later commit, `lib/` for three of them and counted rows in progress). Deferring the transport throws that work away and risks a costly retrofit once an arm wins, while the kit is itself not free (+59 percent, then +10 to +35 percent) and has no measured quality benefit beyond rows with n = 2.

Answer. (1) Nothing is thrown away: the packages stay on the E2 branch as design input, and the one reusable part, the skeleton, is described in r09 section 1.3 line by line. (2) The retrofit is bounded because the core keeps the open-key grammar, a sidecar option, a run-record field for persistence and a reserved `exchange` key. "Retrofit is bounded" is argued, not measured (A-003, both QUALIFY), and removing a shipped dormant script leaves an inert orphan in installed `~/.claude/hooks/` (`install_hooks.py:35-41`) [CODE-VERIFIED, A R2 V3 and B R2 V3]. The heavy parts (board, seal, message-kind registry, per-session settings) depend on runtime facts that are not settled: delivery to a subagent model remains unshown, and the launcher (C-07) is undecided. Two facts the base listed as unverified are corrected: `--resume` on gateway ids is recorded as passing at the pinned tip (4.4), and the recorded hook cost (p95 57 to 85 ms in r5, 73 and 81 ms in r2) fits the 0.1 s planning budget but consists of maxima over 4 to 10 calls, not a 30-call p95 [CODE-VERIFIED as recorded lines, B R1 and A R1 concession 2]; r4's 143 and 90 ms stay [UNVERIFIED] (`r09` section 6.2 C-15). Building the heavy parts first would fix a design on facts that are not settled. (3) Every exchange arm must be compared with A2 to separate prompting from collaboration (CL-C13: "exchange designs without A2 cannot be separated from prompting"); r3 and r4 did not build A2 and cannot separate them. So the kit is the control the transport would need anyway; shipping the kit first is the first step of any path, not a detour. (4) The kit cost is a priced, measurable number per module, with the later rows showing it is not uniformly high; the exchange cost has no priced number, and its own timing rule gives `k` 0 on most cells so that the owner had to relax the cap to run it at all. (5) Even if the kit's benefit is no larger than A1's spread, the unconditional parts H1 and H2 stand on their own evidence (3.1 item 1: the shipped brief names no driving document at HEAD; 3.1 item 2: HEAD rejects over-limit lines in both parsers, re-read), independent of the kit and of exchange. The part of the proposal that would be lost if the kit fails is the catalogue; the part that would be lost if exchange wins is only the timing of the transport. (6) Fallback and scope. If C-07 yields no launcher with persistence and a per-session activation channel, the hook half is dropped and the F1 second prompt on swarm remains a design question for the swarm slot, still off (Variant B section 8 concession; B R2 V5 and V6). Scope correction on `--settings`: it is absent from `src/superclaude/**/*.py` but present in the ccsession shell launcher (`skills/ccsession-tag/ccsession:1150,1259`), which is not a headless panel launcher [CODE-VERIFIED, B R2 V5; the search covered `src/superclaude` only].

Residual risk I cannot answer from the evidence: whether an exchange arm yields a large gain on a defect class the isolated panel misses (r09 section 1 says the designs target exactly those classes). The measurement in section 6 point 1 is the only thing that answers it, and it needs n larger than E2 planned.

## 9. Residual open items carried from the debate

<!-- Source: Debate Round 2.5, invariant-probe.md (all 16 findings; INV-005 and INV-009 HIGH) and the team lead's new-evidence note on `e2f2ac268` - merged per Change 9 and amendment 11 -->

Convergence gate: BLOCKED_BY_INVARIANTS. Diff-point agreement is 96% (24 of 25), which meets the 80% threshold, but two HIGH-severity UNADDRESSED invariants block a CONVERGED declaration: INV-005 and INV-009. Neither was debated: both concern H1 and H2, which both advocates treat as shared ground, and depth `standard` ran no Round 3. They are carried here as acknowledged open risks. Nothing below is claimed resolved.

The two blocking items, as the probe recorded them:

- INV-005 (HIGH): H1 into reflect needs an edit in `cli/reflect/ensemble.py` while "no change to cli/reflect" is adjudicated.
- INV-009 (HIGH): H2 re-ask inside C-01's `parse_block` placement while C-01 INV-003 is open and C-06 is open.

All 16 findings (2 ADDRESSED, 14 UNADDRESSED: 2 HIGH, 12 MEDIUM):

| ID | Status | Severity | One-line assumption |
|----|--------|----------|---------------------|
| INV-001 | ADDRESSED | LOW | The build trigger can sit unfired and the product state meanwhile is defined ("unmeasured, not rejected"). Residual: a note has no mechanical consumer, so an expiry triggers nothing |
| INV-002 | UNADDRESSED | MEDIUM | The served-model and act-rate probe record is "cheap and needed now" and has a home, so per-model capability facts survive the "unmeasured" state |
| INV-003 | UNADDRESSED | MEDIUM | A reserved profile key `exchange` (and `kit`, `driving_documents`) is "a pin, not an implementation"; whether it is code (`panel.py:37-46,160-176`) or a design-note entry is not decided |
| INV-004 | UNADDRESSED | MEDIUM | The off-state test "brief bytes with `kit: off` equal today's brief" coexists with H1 shipping unconditionally |
| INV-005 | UNADDRESSED | HIGH | H1 reaches reflect "through the reflect brief; no call-site change" while `cli/reflect` stays unchanged and reflect results stay pinned |
| INV-006 | UNADDRESSED | MEDIUM | A single kit cost figure can gate `kit: on` per module ("inside a cap the module owner states") |
| INV-007 | UNADDRESSED | MEDIUM | "Hold-out of at least 4 unseen defects" plus a power calculation is a satisfiable, consistent threshold |
| INV-008 | UNADDRESSED | MEDIUM | A peer-origin sidecar "keyed by reviewer id and finding id" identifies the tagged line unambiguously |
| INV-009 | UNADDRESSED | HIGH | H2 (one pre-merge repair step) is core "now", and a re-ask without truncation is compatible with C-01's placement inside both `parse_block` functions |
| INV-010 | UNADDRESSED | MEDIUM | One catalogue source per module rendered through the installed form, and the kit renders from X-13's single data source |
| INV-011 | UNADDRESSED | MEDIUM | "Quorum counts over own-origin lines only" protects C-02 and C-03 once exchange exists |
| INV-012 | ADDRESSED | LOW | Kit moves in shell form would instruct no-Bash lanes to execute something (INV-G); addressed by the brief lint of 6.5 |
| INV-013 | UNADDRESSED | MEDIUM | The A-layer alone gives mutually blind reviewers and an inert off state (INV-G, H4 principle) |
| INV-014 | UNADDRESSED | MEDIUM | The enable trigger can be satisfied on a lane that can host exchange (tasklist review is the only module with ground truth) |
| INV-015 | UNADDRESSED | MEDIUM | The A-layer alone is cost-safe because the kit is the only priced item and defaults off (H2's repair may be a re-ask, with no cap or counter) |
| INV-016 | UNADDRESSED | MEDIUM | The central premise of the deferral ("no exchange arm has been measured against the static kit") still holds at the current E2 head |

Open item on new evidence (INV-016, [POST-BASELINE]): the tasklist-study branch gained commits up to `e2f2ac268` (2026-11-14 19:19, "counted results, replicates and write-up for the five collaboration designs") which neither advocate read. The central premise (no exchange arm measured against the static kit) may be answered there and must be re-checked when the unification folds the tasklist branch in. The debate was not rerun on it.

Status: Complete
