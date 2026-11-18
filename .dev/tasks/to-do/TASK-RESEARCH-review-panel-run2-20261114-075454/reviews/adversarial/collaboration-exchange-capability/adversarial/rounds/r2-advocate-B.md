# Round 2 rebuttal, Advocate B (Variant 2 = Proposal B), slot C-12 collaboration-exchange-capability

Status: Complete

Tags: [CODE-VERIFIED] I read the file or ran the search this session at HEAD `50d4d2b9d`; [UNVERIFIED] taken from a research, variant or round file and not re-read; [POST-BASELINE] read only after E2 pinned tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`. I read no post-baseline fact for this round. Read-only session. I did not touch the forbidden paths.

## Position after rebuttal
I concede the build-now question. At HEAD there is no launcher for my hook and adapter to run on, no family I would ship has a clean measured success, and the one existing exerciser for hooks cannot see an unregistered per-session hook. A's hybrid (A-layer now, transport built when a launcher decision, a metric of record and an owner exist, enabled only on a measured win) is close to where my own Round 1 concession already pointed. I accept it with amendments (section 3). The remaining disagreement is the order of work around slot C-07 plus four details: the trigger needs an expiry so it cannot silently never fire, the enable rule must be two-sided because "beats A2" may be undetectable at the available n, the `exchange: off` reserved key is itself a ladder question, and the F1 "portable" family is not buildable by reuse (section 1, V6).

One new fact neither paper cited: `--settings` is absent from the Python product code but present in the repo's `ccsession` shell launcher (V5). It does not rescue my build-now case; it narrows "the flag may not exist" to "no panel launcher uses it".

## 1. Facts re-verified this round
| # | Claim (whose) | Result | Tag |
|---|---|---|---|
| V1 | Gateway launch map is empty (A S1) | True. `src/superclaude/cli/review/data/review-tiers.default.json:25-29`: environment `gateway` has `"launch": {}` and note "dispatch mechanism per model not defined yet". The only populated map (`:35`, environment `anthropic-only`) maps model ids to bare CLI aliases (`"opus"`, `"sonnet"`, `"haiku"`, `"fable"`), not to a command, a session mode or settings. Even that map is not a launcher | CODE-VERIFIED |
| V2 | Unregistered script is inert; precedent `launch-level-pre-push.sh` (A V1, my R1 S3) | True. Grep of all of `src/superclaude` for `launch-level-pre-push` finds the script, `install_hooks.py:96` (list entry and the comment "never registered in settings.json"), `orca_worktree.py:837,1077,1194` and one skill ref; no match in `hooks/hooks.json`. The precedent has a live consumer (`orca_worktree.py:1194` reads `~/.claude/hooks/launch-level-pre-push.sh`). My hook would have none until a launcher exists, so the precedent proves inertness only, not that a consumer-less script is worth shipping | CODE-VERIFIED |
| V3 | Removing a shipped dormant script is "one directory, one script, one list entry" (my R1 A-003) | Incomplete. `install_hooks.py:267-291` only copies (`shutil.copy2`, `chmod`) over `_FRESHNESS_SCRIPTS` plus `_LEGACY_SCRIPTS`; nothing deletes. `:40-41` records `--no-orphans` as future work. Every installed `~/.claude/hooks/` keeps an inert orphan after removal. `Makefile:307-325` fails on a stale list entry, so the list entry must go with the source. A's V3 is right; I withdraw "mechanical and bounded" as a full answer: bounded, leaves inert orphans | CODE-VERIFIED |
| V4 | Does `make verify-sync` force a plugin mirror for a new hook script? | No. `Makefile:307-325` checks only that `hooks/scripts/*.sh` and `*.js` equal `_FRESHNESS_SCRIPTS`. A search of `Makefile` for `plugins/superclaude/hooks` and `launch-level-pre-push` returns nothing. Whether `make build-plugin` copies hook scripts was not read | CODE-VERIFIED (sync gate), UNVERIFIED (build-plugin) |
| V5 | `--settings` appears nowhere (A V5, my R1 S4) | Needs a scope correction. In `src/superclaude/**/*.py` it appears nowhere (no `--settings`, `--session-id`, `--continue`; the `roadmap/executor.py:8` hit is a docstring saying these flags are NOT passed). But it is used in shell: `skills/ccsession-tag/ccsession:1150,1259` builds `CC_SETTINGS_ARGS=(--settings "$_per_model")` (per-model compaction-window JSON for interactive gateway tiers) and `ccsession-orca:105` and `hooks/scripts/launch-level-guard.sh:453` list `--settings` among flags they recognise. So per-session settings has a precedent in this repo's interactive gateway launcher; no headless panel launcher uses it. `ClaudeProcess` keeps `--no-session-persistence` in both profiles (`pipeline/process.py:149-152`) and `reflect/runner.py:497-504` documents the same flag | CODE-VERIFIED |
| V6 | F1 (between-phase) can be built without a launcher by reusing the swarm transport or an existing `--resume` path (the question set to me) | Mostly no. (a) No existing path passes a session id to `claude`: every `--resume` in the product code is a product-level resume (`reflect/commands.py:291` "Skip the launch when the prior reflect_post is a pass", `sprint`, `swarm`, `pr_submit`, `cli_portify`); `pipeline/` has none. (b) The swarm transport is stateless: `Transport.send(prompt, timeout)` sends `[{"role": "user", "content": prompt}]` (`openai_compat.py:384-388`), and the only `transport.send` call site in `cli/swarm` is `dispatch.py:170` inside `_send_once`. A second prompt carrying a digest needs a new round-two dispatch step plus manifest and normalizer handling in swarm, and because no session exists the second prompt must carry the reviewer's own phase-1 report as well as the peer digest. That needs no launcher (so it is not blocked by C-07), but it is new swarm orchestration, not reuse. (c) Reflect Tier-2 already goes through the swarm run surface (`reflect/ensemble.py:1-5`), so F1 on swarm is the one family reachable from HEAD's real runtime | CODE-VERIFIED (a, b, c); no F1 run on swarm exists [UNVERIFIED] |
| V7 | `hook_latency_drift.yaml` scope (A W6) | Confirmed as A says. Header and description (`:22-24, :40`) frame it around "hooks shipped in src/superclaude/hooks/hooks.json" and the `hooks.json` budgets; its evals drive registered hooks in a sandbox HOME. A per-session, unregistered hook sits outside it, so a dormant exchange hook has no recurring exerciser unless a new suite is written (more scope) | CODE-VERIFIED |

Net: V1, V3, V5 (headless part), V7 support A. V2 and V4 shrink A's installer-cost argument and I agree with A that it is no longer decisive. V5 (shell part) and V6(c) are the two facts that favour the F1-on-swarm direction rather than the hook half.

## 2. Response to A's Weaknesses 1 to 7
**W1 no runtime exists for the adapter. Conceded in full.** V1 and V5 show no panel launcher, an empty gateway map and no headless `--settings` or session-resume path. My Round 1 S4 ("the only way to test hooks reach panel reviewers is to own the adapter") is true but it is an argument for building the adapter when the launcher design exists, not before: an adapter written first would be shaped by my fixtures, not by C-07's decision. The ccsession precedent (V5) shows the flag works for interactive gateway sessions; it says nothing about headless `claude -p` with persistence on.

**W2 the off-state test cannot see installer, `hooks.json` or telemetry effects (A-002). Conceded; fix is cheap.** My argv-diff test compares new adapter code with new adapter code, and the existing pins (`process.py:149-152` and the restricted-profile tests) pass vacuously because I do not touch that code. The test that actually guards "off costs nothing" is the one both papers agreed in Round 1: no `hooks.json` or merged-settings diff, no board directory, no `--settings`, no new run-record key, and a named installed-file-set diff. If the transport is ever built, that test is written first. It also applies to A's reserved key and kit catalogue, and A's off state passes it by construction (A V7, which I agree with after reading `Makefile:307-325`).

**W3 the transport is step 3 behind C-07 and C-08. Conceded.** The hook script itself does not need C-08 to be written, but its output (act rates, `delivered`) is uninterpretable without the served-model record, and the adapter needs C-07. Writing code whose first measurement cannot be read is the wrong order.

**W4 no family I would ship has a clean measured success. Conceded, with a scope note.** My Round 1 "recorded passes" are plumbing passes (S0 delivery, S2 resume) from the E2 launcher, not benefit. For F6 the only real row at the pinned tip is quarantined; I found no clean F3 success in anything I read (nothing re-read this round); r3's two collab rows with `phase2_timeout` 1 (A's E8) are [UNVERIFIED] by me this round. F1 is the family with no hook and (V6) the one reachable from HEAD's real runtime, but its only evidence is negative, so it is not a reason to build.

**W5 rot risk with no exerciser. Conceded as stronger than I argued.** V7 confirms the only recurring hook suite is bound to `hooks.json`. A dormant hook can only be exercised by a new exchange smoke eval, and that eval is the arm. Together with V3 (no clean removal) the honest reading is: the dormant script is cheap to ship and also has nobody to keep it alive, so it should arrive with its exerciser, not before.

**W6 the untrusted-anchor channel has no test in my list. Conceded.** Add: an adversarial-anchor test (injection text in an anchor, a 600-byte boundary case, a forbidden verdict key placed in a located-anchor field), plus a test that board files never enter the `review-telemetry` export. A's Round 2 already records these as preconditions; I agree they bind lifting `exchange: off`.

**W7 the divergence argument shows how, not when. Conceded** (my R1 concession 4 already said so). It is a requirement list for the single correct copy: `agent_id` skip, timed lock, seal before first delivery and fail closed, replay with two parallel calls. Not a reason to build.

**Where I still push back on A (three points).**
1. "A tested hook with no host" (A section 3) understates one thing: the single-copy replay test needs only a fixture, so it could run today. It would then test a script nobody ships. Same conclusion as A, different reason: not a host problem but a consumer problem (V2).
2. A's trigger names `--settings` as the activation channel (A section 5, trigger 1: "per-session settings"). V5 says the repo's only precedent is the interactive ccsession launcher; C-07 may pick another channel (for example a settings file the adapter writes into the reviewer's worktree). The trigger should name the capability (persistence on plus a per-session activation channel), not the flag.
3. A's reserved `exchange` key with one legal value is the same kind of thing A rejects in B: config with no implementation. A's own ladder rung 1 ("does it need to exist now") applies. I rate this a small point, and I have not read the profile validator to know whether an unknown key is already rejected [UNVERIFIED]; if unknown keys pass, recording the key name in the design note achieves the same pin with zero code and no INV-K layout item.

## 3. A's candidate hybrid, condition by condition
A's hybrid: now = A-layer (H1 to H4, kit catalogue behind `kit: off`, reserved `exchange: off`) plus a binding design note, no hook, adapter, board or validator code. Build trigger = three conditions. Enable trigger = two conditions.

| Condition | Verdict | Reason and amendment |
|---|---|---|
| Build 1: C-07 adjudicated to a launcher with session persistence and per-session settings | Accept, amend wording | V1, V5, V6 make this the true blocker. Amend: name the capability (persistence on, a per-session activation channel, a headless main-thread lane), not `--settings`; and state the branch for an outcome with no such launcher: the hook half is dropped and the F1 second-prompt on swarm (V6) goes to the swarm slot as a design question, still off. That is A's own fallback ("hook half shrinks"), made explicit. |
| Build 2: metric of record (X-14) and decision rule committed; C-08 records the served model | Accept | Without them an arm's result cannot bind a decision. Amend: the served-model and act-rate-probe record is cheap, has a consumer today (any per-model capability claim, kit gating) and needs no transport, so C-08 should land independently and early; I treat it as a precondition that can be satisfied now, not as a wait. |
| Build 3: a named owner and a time box | Accept in full, add an expiry | Strongest of the three. Amend: the design note must carry the owner, the date or event at which the trigger is re-evaluated, and the recorded state "unmeasured, not rejected" if it does not fire. Without an expiry the hybrid reproduces the A Round 1 defect (ownerless gate). The owner is the lead's decision, not C-12's. |
| Enable 1: an exchange arm beats A2 on a matched package set, hold-out of at least 4 unseen defects, power calculation, module-matching ground truth | Accept, amend to a two-sided pre-registered rule | E2's own text (`MR:1128`: only large effects separate at n = 12) is [UNVERIFIED] by me but both papers rely on it. If that holds, "beats A2" may never be observable, and the capability stays off forever by default. Amend: pre-register a rule on gain and cost against A2 (exchange costs elapsed time and tokens; A2 costs +59 percent elapsed on r5 by A's derived ratio, [UNVERIFIED] by me this round). Outcomes: arm clears the minimum gain with an interval that excludes zero, stay off with the record "no effect detected at n", or "underpowered, unmeasured". A hold-out of 4 is a floor for a sanity check, not a power guarantee. Module scope: tasklist review only (A-001); PR review and rf-qa stay off. |
| Enable 2: all section 4 preconditions of A's Round 2 met, including the adversarial-anchor test | Accept, add | Add the build-time tests from my Round 1 list that need a launcher: S0 and S2 on the product launcher for every gateway-class model in the panel resolution, fault injection (seal fails closed, review fails open), hook p95 over at least 30 calls per model (A's X-004 point stands: recorded figures are maxima over 4 to 10 calls), and the installed-file-set diff. |

**Does the hybrid differ materially from my position?** Not on the decisive question: it is the conditional form of my own R1 concession 2 ("if C-07 yields no launcher, B shrinks"). The material differences are four, none about whether to build exchange eventually:
1. It moves "when" from a calendar fact (now) to a dependency fact (C-07, C-08, X-14, owner). I accept that.
2. It builds no code now. I accept; I see no consumer for the validator as pure functions (see section 4).
3. It gates enabling on a measured win. I accept, with the two-sided rule above.
4. It leaves the single-correct-copy requirement list as prose. I accept, because V3 and V7 make a consumer-less script and a consumer-less suite both unmaintained.

The rest of the disagreement is the order of work around C-07, which is why both sides should accept the trigger form. I would record in the artifact that the three build conditions are cross-slot dependencies (C-07, C-08, X-14), not C-12 deliverables.

## 4. Updated points, resolution, and what I would still build now
### 4.1 Points whose position changed (Round 1 to now)

| Point | Round 1 (B) | Now | Why |
|---|---|---|---|
| S-002 | A 55 | Tie 50 | Presentation only; A's Round 2 agrees. |
| S-003 | B 52 | A 56 | The partition by trigger, not by build/no-build, is what the evidence supports (V1, V7). |
| C-001 | A 55 | A 66 | V1, V5, V6: no host at HEAD. |
| C-002 | A 60 | Merge 62 (trigger form) | A's gate is ownerless and conflates instrument with capability; my "build now" is not supported either. The hybrid with owner, expiry and two-sided rule is the answer. |
| C-004 | A 60 | A 70 | Adapter must be separate from `ClaudeProcess` (`process.py:149-152`) and depends on C-07; no code can pin it now. |
| C-005 | A 55 | A 62 | F1 needs no hook, but V6: no session-id path exists, swarm needs a new round-two step, no F1 run exists on swarm, and the only F1-like evidence is negative [UNVERIFIED by me this round]. |
| C-006 | Merge 60 | Merge 65 | If built, the sidecar is mandatory and harness-written (quorum counts over own-origin lines only); neither paper builds it now. |
| C-007 | Merge 55 | Merge 62 | Adopt both test lists plus the adversarial-anchor test; transport tests stay specifications until the trigger fires. |
| C-008 | B 55 | B 55 (unchanged) | At the pinned tip no E2 arm ran from its commit [UNVERIFIED by me this round, from R1]; a product-launcher repeat is still needed to bind a product decision; the hybrid grants that at trigger time. |
| C-010 | B 75 | B 78 | Validator table, forbidden keys, 600-byte cap, located-anchor rule and the attacker-anchor analysis stay valuable, as a binding precondition note. |
| C-011 | A 55 | A 60 | My argv-diff test cannot see installer or `hooks.json` effects; A's off state passes the stricter test by construction. |
| X-001 | A 55 | A 68 | Build the transport now: no. |
| X-002 | B 85 | B 82 | Recorded S2 passes stand but they are plumbing on the E2 launcher, not benefit and not a product launcher. |
| X-003 | A 55 | A 62 | Main-thread-only scope plus no lane at HEAD. |
| X-004 | B 70 | B 62 | Level fits 0.1 s but over 4 to 10 calls; my own 30-call test concedes it. |
| X-005 | B 62 | B 58 | Shows under-specification of the skeleton, not a maintenance cost. |
| X-007 | A 60 | A 58 | Waiting is free for the packages, not for repeatability of the measurement. |
| A-002 | QUALIFY | QUALIFY | Add the installed-file-set diff to both. |
| A-003 | QUALIFY | QUALIFY | Removal of a shipped dormant script leaves inert orphans (V3); a deferred build starts from a described, not a tested, skeleton. |

Unchanged: C-003 (A 75), C-009 (A 62), C-012 (A 52), X-006 (A 65, settled by the `launch-level-pre-push.sh` pattern, V2), S-001 (tie), A-001 (QUALIFY).

### 4.2 Resolution I think the evidence supports

1. Core now: A-layer (H1 to H4; kit catalogue behind `kit: off` until the cost per panel at n of at least 4 and the hold-out pass; brief lint for read-only lanes) plus the design note. Default-off posture for exchange stays; no hook script, `_FRESHNESS_SCRIPTS` entry, adapter, board or validator code.
2. Build trigger: C-07 adjudicated to a launcher with persistence and a per-session activation channel (named by capability), metric of record and decision rule fixed, served-model record landed, named owner and expiry. If C-07 yields no such launcher, the hook half is dropped and only F1 on swarm remains a design question for the swarm slot.
3. Enable trigger: a pre-registered two-sided gain-and-cost rule against A2, module-matched ground truth with a hold-out, all design-note preconditions green. Tasklist review is the only module with ground truth today.

### 4.3 What I would still build now that does not depend on C-07

- **The design note, as a tracked file with binding force** on lifting `exchange: off`. Minimum content: `panel-msg/1` per-kind keys, forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, harness-authored kinds only; the harness-written sidecar keyed by reviewer id and finding id (key not named `origin`); untrusted-text rules with the adversarial-anchor test; fault-injection list (seal fails closed, review fails open); the single-copy requirements (`agent_id` skip, timed lock, seal before first delivery, parallel-call replay); package named `exchange/` (not `lib/`, `.gitignore:13` [CODE-VERIFIED in R1]); no `src/superclaude/` path in installed text; installer footprint stated as a test item (list entry, no `hooks.json` entry, activation only by the adapter's per-session channel).
- **The stricter off-state test** for the A-layer key and catalogue: no new file under `~/.claude/hooks/`, no `hooks.json` or merged-settings diff, no new run-record key when off, named installed-file-set diff. This has a consumer now.
- **The served-model and act-rate probe record** (slot C-08 if that slot owns it): it has consumers today and needs no transport.
- Not built: the validator as pure functions, the sidecar schema as code, the `collab` record. I looked for a caller and found none at HEAD (no exchange arm, no launcher), so under the ladder they are speculation; a function with only fixture callers is a second dormant surface, which is A's point and I now agree with it.

## Evidence limits

- Not re-run: any E2 spike, hook script or transcript. The S0/S2 lines, r3 `phase2_timeout` rows, the +59 percent kit ratio, `MR:917` and `MR:1128` are [UNVERIFIED] by me this round; they come from my R1 reading and A's files.
- Not read: `make build-plugin`'s implementation (V4), the profile validator for unknown-key handling (section 2, push-back 3), `ccsession`'s `compact-settings` output beyond lines 1240-1265, any post-baseline commit.
- The `--settings` search covered all of `src/superclaude` (Python, shell, markdown); no other directory (tests, docs, plugins) was searched.
- The `--resume` search covered `src/superclaude/**`; the first 40 hits were read and the `pipeline/` directory and the `--session-id`/`--continue` pattern were searched separately. A product-level `--resume` I did not classify cannot be fully excluded, but none of the files I read passes a session id to `claude`.

Status: Complete
