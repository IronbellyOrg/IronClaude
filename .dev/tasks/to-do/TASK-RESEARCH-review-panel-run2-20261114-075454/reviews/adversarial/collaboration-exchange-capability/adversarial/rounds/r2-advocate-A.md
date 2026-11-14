# Round 2 rebuttal, Advocate A (Variant 1 = Proposal A), slot C-12 collaboration-exchange-capability

Status: Complete

Tags: [CODE-VERIFIED] I read the file or ran the search this session at HEAD `50d4d2b9d`; [UNVERIFIED] taken from a research or variant file, not re-read; [POST-BASELINE] read only at E2 commit `c44c98a77`, never the only evidence for a decisive point. E2 pinned tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`. Read-only session; I read B's Round 1 (`r1-advocate-B.md`), my Round 1, both variants and the diff analysis. I did not touch the forbidden paths.

## Position after rebuttal

I now concede more than in Round 1. Three of B's points land: (1) my gate "not built until an exchange arm beats the kit" conflates building the measuring instrument with enabling the capability, and is ownerless as written; (2) my installer-cost argument against B's script is much weaker than I made it, because three existing scripts are shipped dormant on purpose; (3) B's validator, sidecar and untrusted-anchor analysis is real value that must not be lost. I still hold that nothing should be built now, because the only product launcher B's hook needs does not exist at HEAD (slot C-07 open, `--settings` appears nowhere in code). My updated resolution is a conditional hybrid (section 5): build B's transport as the instrument for the pre-registered comparison when a launcher decision, a metric of record and a named owner all exist, still off by default.

## 1. Response to B's Weaknesses 1 to 6

### B-W1: "The gate is circular without an owner"

Re-checked against my own text. [CODE-VERIFIED, `variant-1-original.md` 6.1 and 8]. The gate is not self-referential: it needs an exchange arm that can run, and arms do run from `.dev/eval-workspaces` (B concedes this as "A's best counter"). But B is right on two things.
- Ownerless: 6.1 names a decision rule, a metric slot (X-14) and a power calculation, but no person, date or home for the experiment. "Costs nothing extra under either position" is true only if someone runs it. That is a gap in A, not a rebuttal.
- Instrument versus capability: 6.1 says the build waits for "an exchange arm beats A2". But an arm result produced on the E2 launcher (open Bash, `run-reviewer.sh:48` via synth-05 [UNVERIFIED]) does not bind a product decision until it is repeated on a product launcher with the served model recorded (slot C-08). Under my own text the product transport would then be built after the result it is needed to make repeatable. That ordering is defensible only if the E2 result is read as a trigger to port, which is what A 7 last bullet says; but it leaves the porting step with no home until after the trigger.
Concession: A's gate should be split in two (section 5). Held: the claim "the transport is not the unlock" survives, because the launcher (C-07) and the served-model record (C-08) block the repeat, not the hook script. [CODE-VERIFIED] `review-tiers.default.json:26-29`: gateway note "dispatch mechanism per model not defined yet", `"launch": {}`.

### B-W2: "A applies its own principle unevenly" (kit shipped on thin evidence)

Partly conceded. [CODE-VERIFIED reading of my own 3.4 and 4.2]. I distinguish by cost (brief text versus code), which is a legitimate rung of the ladder, and the kit sits behind `kit: on|off` with a per-module cost gate; but I agree the kit's benefit evidence is thin (n = 2 against 4, one judge, same ten missed issues for both catalogues). The honest version: the kit is cheap to ship and cheap to turn off, so shipping it default `off` for modules without a hold-out is as defensible as B's dormant transport. I will not claim "first candidates for `on`" for spec-review and tasklist without the hold-out test (my measurement 7). The pinned-tip kit cost is +59 percent elapsed (r5 rows `s4pilot-a2-sl2-r1` 281.567 s against 179.561 and 174.274 s, derived ratio [UNVERIFIED by me this round; recomputed in Round 1]), and no pinned-tip gain row exists. Position changed to: kit ships `kit: off` by default until measurement 2 and 7 pass.

### B-W3: "No exchange arm has a matching control row" overstated

Concede the wording. [POST-BASELINE, from my own 4.3]. Later commits do have counted rows for collaboration arms against the same-harness baseline. The accurate statement is: no exchange arm has a row matched against the A2 kit arm at a size that separates from noise; E2's own plan says only large effects separate at n = 12 (`MR:1128`) [UNVERIFIED re-read; pinned-tip statement quoted in Round 1]. I should have written "no matched A2 control" and did not.

### B-W4: "A ships a reserved key that can only be off"

Concede the footprint is not zero. [CODE-VERIFIED, `Makefile:307-327`]. The `verify-sync` Installer Registration block checks only that `src/superclaude/hooks/scripts/*.sh|*.js` equals `_FRESHNESS_SCRIPTS` (both missing and stale entries fail). It does not check profile keys. So my reserved key needs a profile validator, an off-state byte test and (INV-K) a layout item, but it adds nothing to `hooks/scripts/`, `_FRESHNESS_SCRIPTS` or the user's `~/.claude/hooks/`. Smaller and in a different place, not zero. Held: a key with one legal value is a pin, not an implementation, and A-002's stricter test ("no new file under `~/.claude/hooks/`, no `hooks.json` entry, no new run-record key when off") passes for it by construction.

### B-W5: "A leans on UNVERIFIED research for 'runtime facts unverified'"

Concede two of three. `--resume` on gateway ids is evidenced at the pinned tip (X-002, conceded in Round 1). The "about 150 ms" figure mixes in r4's unverified numbers (X-004 below). Held: delivery to a subagent model remains unshown, the swarm transport sends one user message and no tool loop, and `reflect-reviewer` has no Bash. [CODE-VERIFIED in Round 1: `openai_compat.py:384-388`; `agents/reflect-reviewer.md:5,8,28,59`.] These are code facts, not research claims, and they remain the reason the transport has no host lane at HEAD.

### B-W6: "E4 (subagent skip) is argued as evidence there is no runtime"

Concede the framing. The skip scopes the transport to main-thread sessions; it is an argument for one correct copy of the skip, not against the transport. But "main-thread headless `claude -p` with persistence on and per-session settings" is a lane with no code at HEAD: `"--settings"` has zero matches in `src/superclaude/**/*.py` [CODE-VERIFIED this session; searched with the flag escaped as `\-\-settings` so the pattern was not read as a tool option]. So the narrowing helps B's hook correctness and still leaves C-07 as the blocker.

## 2. Verifications of the decisive facts (the ones B's merge proposal depends on)

| # | Claim | Result | Tag |
|---|---|---|---|
| V1 | `launch-level-pre-push.sh` is installed but never registered, so an unregistered script is inert in ordinary sessions | True. `src/superclaude/hooks/hooks.json` has 0 matches for the name. `install_hooks.py:94-96` comment: "installed into a worktree's hooks/pre-push by the Orca launcher, never registered in settings.json". Its consumer is a real launcher: `orca_worktree.py:1194` reads `~/.claude/hooks/launch-level-pre-push.sh` | CODE-VERIFIED |
| V2 | The precedent shows a dormant script is cheap | Partly. It proves inertness. It does not prove cheapness or that B's script would be analogous: the precedent has a live consumer (the Orca L2 claim path) and carries its own pins: `_FRESHNESS_SCRIPTS` membership, a byte-equal mirror at `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh`, executable bit, a sha256 pin and a version line (`tests/cli/test_install_hooks.py:1098-1124`). Only list membership is forced by `make verify-sync`; the mirror and sha tests are per-script choices (two test files reference the mirror path, no global mirror test) | CODE-VERIFIED |
| V3 | A shipped dormant script is removable | Not cleanly. `_install` paths only copy: the loop over `_FRESHNESS_SCRIPTS` plus `_LEGACY_SCRIPTS` copies and chmods (`install_hooks.py:265-289`); nothing deletes. The comment at `:35-41` says a `--no-orphans` flag is future work. Removing a script means: delete the source, delete the list entry (a stale entry fails `verify-sync`, `Makefile:318-322`), delete any mirror and tests, and accept an orphan copy in every installed `~/.claude/hooks/` that stays inert because it is unregistered. Harmless, not free | CODE-VERIFIED |
| V4 | Footprint of a dormant script on the sync gate | One list entry. For `.sh` and `.js` only (`Makefile:308`). Whether `make build-plugin` copies the script to `plugins/superclaude/hooks/scripts/` automatically: not read | UNVERIFIED |
| V5 | Any `--settings` in cli | Zero matches in `src/superclaude/**/*.py` | CODE-VERIFIED |
| V6 | The gateway launcher is undefined | `review-tiers.default.json:26-29` `"launch": {}` with note "dispatch mechanism per model not defined yet" (line 35 maps four subscription models to aliases, a different environment) | CODE-VERIFIED |
| V7 | Does A's reserved key create installer drift | No. Not read by `_FRESHNESS_SCRIPTS`; a profile validator and one off-state test only | CODE-VERIFIED (by reading `Makefile:307-327` and `install_hooks.py:42-97`) |

Net effect of V1 to V3: B's "an installed-but-unregistered script is inert" is right, and my Round 1 installer-cost argument (strength 5) was an over-reach: three existing scripts (`reject-workspace-writes.sh`, `sc-recommend-phase0.sh`, `launch-level-pre-push.sh`) are shipped dormant on end-user installs by the repo's own rule (`install_hooks.py:54-65, 69-78`). I withdraw "recurring cost" as a decisive point. B's A-003 removal claim ("one directory, one script, one list entry") is incomplete (V3) but the omissions are inert leftovers, so I also do not treat them as decisive.

## 3. Response to B's per-point wins and its merge proposal

| Point | B's R1 position | My response |
|---|---|---|
| S-002 evidence form | A 55 | Tie. B's labelled sub-section for [POST-BASELINE] material serves the staleness rule at least as well as my per-row tags. Presentation only; 50. |
| S-003 partition | B 52 | Moves toward the middle: the merge in section 5 moves the partition to a trigger, not a build/no-build line. A 58. |
| C-006 sidecar | Merge 60 | Concede. If exchange is ever built the sidecar must be harness-written and mandatory, because C-02 quorum counts must be computable over own-origin lines only (U-014). Neither paper builds it now; record it as a precondition. Merge 62. |
| C-008 where the measurement runs | B 55 | Concede in part. At the pinned tip no E2 arm ran from its commit (0 `/lib/` paths, [CODE-VERIFIED in Round 1]); at `c44c98a77` three run [POST-BASELINE]. My "nothing extra under either" holds for running the arms, not for repeating them on a product launcher. B 60. |
| C-010 validation and untrusted text | B 75 | Concede fully. B has a validator table, forbidden verdict keys, a located-anchor rule and the attacker-controlled-anchor analysis; I have one sentence. B 80, recorded as preconditions (section 4). |
| X-002 resume | B 85 | Concede (done in Round 1). |
| X-004 latency | B 70 | Concede the level (57 to 85 ms r5, 73 and 81 ms r2 fit 0.1 s). Held: those are maxima over 4 to 10 calls, not a p95 over 30; B's own test 5 admits it. B 62. |
| X-005 divergence | B 62 | Concede it shows the skeleton is under-specified (r2 `agent_id` count 0 against r1, r4, r5 present; r1 `flock -w 4` against r5 untimed `flock 9`). It argues for recording the requirements of the one correct copy (skip on `agent_id`, timed lock, seal before first delivery and fail closed), not for building it now. B 58. |
| X-006 `hooks.json` | A 65 | B conceded the defect. As written A holds; resolved by B's fix (the `launch-level-pre-push.sh` pattern, V1). No residual dispute. A 60 and settled. |
| X-007 waiting is free | A 60 | Narrow: waiting is free for the packages (they stay on the branch), not free for the measurement's repeatability (C-008). A 55. |

**B's merge proposal:** "A's layer plus B's validator, sidecar and one tested hook script, kept unregistered and dormant, with A's three extra tests."

- Accept: A's three extra tests (brief lint, kit cost per panel at n of at least 4, catalogue hold-out) and the act-rate probe stay; B's off-state tests extended per A-002 (no `hooks.json` or merged-settings diff, no board directory, no `--settings`, no new telemetry key, named installed-file-set diff).
- Accept as preconditions, not code: validator table, sidecar, untrusted-anchor channel, fault-injection list, single-copy replay test spec.
- Reject now, accept conditionally: the tested hook script. A tested hook with no host. Tested only against B's fixtures, since there is no launcher to exercise it (V5, V6). The script's recurring costs are small (V1 to V3) but its value is zero until a launcher decision exists. The ladder's first rung ("does it need to exist now") fails; the same logic admits it the moment a launcher exists (section 5).

## 4. Are B's validator, sidecar and untrusted-anchor analysis preconditions or code?

Preconditions, recorded as a design note (not built). Reasons: the validator and sidecar have no caller without an exchange arm (the validator's kinds F1, F3, F6 are harness-authored, and the only real F6 row I found is quarantined, [CODE-VERIFIED in Round 1]); the forbidden-key table and 600-byte cap are best tested against a real hook output, which does not exist in the product; and a validator written now would be a second unexercised dormant surface. The note is not low-value: it is exactly the content that is expensive to rediscover, so it must be a binding precondition on lifting `exchange: off`. Its minimum contents:
1. `panel-msg/1` per-kind keys, forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, harness-authored kinds only (U-010).
2. Peer-origin tag as a harness-written sidecar keyed by reviewer id and finding id; key name not `origin` (CL-X11); quorum counts over own-origin lines only (U-014, C-02).
3. Untrusted text: an anchor taken from a reviewed PR diff is attacker-controlled and would be echoed to a peer; board files never enter the `review-telemetry` export; an adversarial-anchor test (injection text, 600-byte boundary, forbidden key in a located-anchor field), which B's own test list lacks (my Round 1 W3).
4. Fault injection: seal fails closed, review fails open (corrupt line, missing transcript, lock timeout) (U-012).
5. Single copy of the hook: `agent_id` skip, timed lock, seal before first delivery, replay with parallel calls (X-005).
6. Installer footprint declared as a test item: `_FRESHNESS_SCRIPTS` entry, no `hooks.json` entry, activation only via per-session settings baked by the adapter, no `src/superclaude/` path in installed text, package named `exchange/` because `.gitignore:13` is `lib/` [CODE-VERIFIED in Round 1] (U-009).

## 5. Updated assessment

### (a) What I now concede
X-002, X-004 (level), X-005 (as evidence of under-specification), C-006 (mandatory sidecar if built), C-008 (in part), C-010, X-006 (settled by B), B-W1 (gate conflates instrument and capability, and has no owner), B-W2 (kit needs the same discipline as the transport), B-W3 (wording), B-W4 (not zero footprint), installer-cost as a decisive argument (V1 to V3).

### (b) Updated winners and confidence on changed points

| Point | Round 1 | Now |
|---|---|---|
| S-002 | B 55 | Tie 50 |
| S-003 | A 68 | A 58 |
| C-001 | A 70 | A 60 |
| C-002 | A 62 | A 52 (my gate is ownerless and conflates instrument with capability) |
| C-004 | A 75 | A 70 (launcher dependency stands; B's adapter-separate-from-`ClaudeProcess` is correct and A's pins argument is the same fact) |
| C-006 | B 55 | Merge 62 |
| C-007 | A 55 | Merge 60 (adopt both lists plus the adversarial-anchor test) |
| C-008 | A 58 | B 60 |
| C-010 | B 75 | B 80 |
| C-011 | A 60 | A 55 (my off state passes the stricter test by construction; B's passes if B adds the installed-file-set test) |
| X-001 | A 66 | A 58 |
| X-004 | B 62 | B 62 (unchanged) |
| X-005 | B 55 | B 58 |
| X-006 | A 72 | A 60, settled |
| X-007 | A 58 | A 55 |
| A-001, A-002, A-003 | QUALIFY | Unchanged. A-002: add the installed-file-set test to both. A-003: both retrofits are bounded, neither measured; removal of a shipped dormant script leaves inert orphans (V3), retrofit of a deferred build starts from a described, not tested, skeleton. |
| C-003, C-012, S-001, C-005, C-009 | As Round 1 | Unchanged (C-003 A 70: the kit key is better specified, but defaults `off` per B-W2). |

### (c) Candidate resolution of the core dispute (build now versus defer)

**Hybrid, staged on a launcher, with explicit conditions.**

Now (unconditional, core):
- A's layer: H1, H2, H3, H4 principle, catalogue behind `kit: off` default, reserved key `exchange` with the single legal value `off`.
- The design note of section 4 as a binding precondition list, with A's three extra tests and B's off-state tests (extended per A-002) specified in it.
- No hook script, no `_FRESHNESS_SCRIPTS` entry, no adapter, no board, no validator code.

Build trigger (the transport is built as the instrument for the comparison, still off by default). Build only when all three hold:
1. Slot C-07 is adjudicated to a launcher with session persistence and per-session settings (today `launch: {}`, `"--settings"` absent, V5, V6). If C-07 yields none, B's concession applies and the hook half shrinks to validator, sidecar and F1 second prompt; those also stay deferred until an arm wants them.
2. The metric of record (slot X-14) and the decision rule are committed, and slot C-08 records the served model, so act rates and outcomes are interpretable.
3. A named owner and a time box for the comparison. If no owner exists, the trigger cannot fire by design and the transport stays unbuilt; the record is then "unmeasured", not "rejected".

Enable trigger (`exchange: off` lifted for a module):
- An exchange arm beats A2 on a matched package set with a hold-out of at least 4 unseen defects, the power calculation, and a module-matching ground truth (A-001: tasklist review only today; none for PR review or rf-qa, which stay `off`).
- All section 4 preconditions are met, including the adversarial-anchor test.

What this changes against my Round 1: the build trigger no longer waits for an arm to win; it waits for the launcher and the owner. What it keeps: no product code on an undecided launcher, and the enable decision still needs the measured win.

**Where I could be wrong (honest):** the dormant-script cost is small (V1 to V3), so if C-07 lands early a "build now" side loses almost nothing by building at that point instead of now; and if C-07 never lands, B's narrow fallback (validator, sidecar, F1 prompt) has no consumer and A is right to leave it. The whole disagreement reduces to the order of work around C-07, which is why both sides should accept the trigger form.

## Evidence limits
- Not re-run: any E2 spike (S0 or S2 lines are recorded; transcripts for r5 not committed per B, not checked).
- Not re-verified this round: the kit +59 percent ratio, r4 143 and 90 ms, r5 and r4 luna act rates, `MR:917` and `MR:1128` quotations, r08 and r09 statements; all remain [UNVERIFIED] by me.
- [POST-BASELINE] items used only as secondary evidence: `k` counts, `OVERRIDE.md` quote, `lib/` counts at `c44c98a77`.
- Whether `make build-plugin` mirrors a new hook script automatically (V4): not read.
