# Adversarial Debate Transcript

## Metadata
- Slot: C-12, slug `collaboration-exchange-capability`
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential A then B) plus Round 2.5 invariant probe; Round 3 not run (depth standard)
- Convergence achieved: 96% of diff points (24 of 25 agreed); gate status BLOCKED_BY_INVARIANTS (see Convergence Assessment)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Variant 1 = Proposal A; Variant 2 = Proposal B)
- Evidence staleness: research pins E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`; later commits `c44c98a77` and up to `e2f2ac268` are [POST-BASELINE]. Neither advocate read beyond `c44c98a77`; `e2f2ac268` is an open item (INV-016).
- Omission check (shared assumptions A-001..A-003): Advocate A answered all three (QUALIFY, QUALIFY, QUALIFY); Advocate B answered all three (QUALIFY, QUALIFY, QUALIFY). No [OMISSION] flagged.
- Round files (verbatim below): `rounds/r1-advocate-A.md`, `rounds/r1-advocate-B.md`, `rounds/r2-advocate-A.md`, `rounds/r2-advocate-B.md`. Round 2.5: `invariant-probe.md`.

### Orchestrator summary of how the debate moved
- Round 1: A argued defer (no HEAD launcher, no arm separated from its control); B argued build a dormant transport now but conceded it shrinks if slot C-07 yields no launcher. Both conceded points to each other (A: X-002, X-004 stale/loose; B: kit gating, hooks.json wording defect in its own X-006).
- Round 2: both advocates re-verified facts in code. A conceded its gate was ownerless and conflated instrument with capability and withdrew its installer-cost argument; B conceded the build-now question (no launcher, no clean measured family, no exerciser for an unregistered hook). Both then endorsed one staged resolution: A-layer now plus a binding design note; transport built only when C-07, X-14/C-08 and an owner with expiry exist; exchange enabled only on a pre-registered two-sided win against A2 on module-matched ground truth.
- Remaining differences (all small): C-002 labelling (A 52 vs "Merge" 62), whether the reserved `exchange: off` key should be code or a design-note entry, C-008 residual, and B's V5 correction that `--settings` exists in the ccsession shell launcher but in no headless panel launcher.

---

## Round 1: Advocate Statements

## Round 1 statement: Advocate A (slot C-12, collaboration-exchange-capability)

Variant 1 = Proposal A. Tags: [CODE-VERIFIED] re-read by me in this session; [UNVERIFIED] taken from a research or variant file; [POST-BASELINE] read only at E2 commit `c44c98a77`, never the sole evidence for a decisive point. Pinned E2 tip: `6c0984326cbb8fb06c4a36065de58b171d3f8175` (`BP` = `.dev/eval-workspaces/tasklist-review-panel/20261113-collab`, `MR` = `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md`). Read-only session: no tests, no mutation.

### Position summary

The two papers already agree on everything except one delta: whether the hook transport, board, seal, validator and a new persistence-plus-`--settings` launch adapter are built into the product now (B) or only after an exchange arm beats the static kit on ground truth (A, with one reserved `exchange: off` key). A should win that delta because the product has no reviewer launcher for B's transport to run on (the gateway `launch` map is `{}` and its slot C-07 is undecided), no exchange arm has separated from its control, and the one decisive measurement is not unlocked by shipping a dormant transport. I concede that B is right on two evidence points where A was stale or loose: `--resume` on gateway ids is evidenced (X-002) and recorded hook latency fits the 0.1 s budget (X-004).

### Steelman of Variant B

B's strongest form is narrow and honest. It does not claim exchange improves findings; B says nobody measured that. It claims four things. (1) The deciding comparison (exchange arm against the kit on ground truth) is only repeatable by someone other than the study author if a product transport exists, because at the pinned tip no design could run from the commit. [CODE-VERIFIED: `git ls-tree` of the pinned tip counts 0 `/lib/` paths for r2, r3, r4 and r5.] (2) The skeleton is written four times and the copies already diverge. [CODE-VERIFIED: `agent_id` occurrences at the pinned tip are r1 1, r2 0, r4 1, r5 2; r2's receiver hook cannot tell a subagent call from a main call, which r5 handles at `hook-posttool.sh:14-15`.] (3) The transport is where the open runtime questions become answerable, and the recorded spikes already show delivery and `--resume` working on gateway ids. [CODE-VERIFIED: r5 `spikes/NOTES.md` S0 PASS for sonnet, haiku, luna with `hook_ms_p95` 59, 57, 85 and S2 PASS for four models; r2 `spikes/RESULTS.md` S0 p95 73 and 81 ms and S2 PASS for four models.] (4) The off state costs nothing by construction and a test pins it. B also bounds its scope well: harness-authored kinds only (F1, F3, F6), sidecar origin tag, no `lib/` folder because `.gitignore:13` is `lib/` [CODE-VERIFIED], an engine-local package, no change to `cli/reflect`, and an explicit concession that if C-07 yields no suitable launcher the hook half shrinks to validator, sidecar and the F1 second prompt. What B genuinely gets right beyond that: the untrusted-anchor channel analysis (an anchor from a reviewed PR diff is attacker text echoed to a peer), the fault-injection list (seal fails closed, review fails open), and the point that a per-package-script `collab` record is a poor home for facts like `delivered 0, late 6, k 0`.

### Strengths claimed

1. **No runtime exists at HEAD for B's launch adapter.** `src/superclaude/cli/review/data/review-tiers.default.json:25-29` says of the gateway environment: "dispatch mechanism per model not defined yet", with `"launch": {}`. `panel.py` has no launcher; its only `subprocess.run` is `git rev-parse --show-toplevel` (`panel.py:380-394`) [CODE-VERIFIED]. B's adapter (B 2.3) is therefore a new launcher, built outside `ClaudeProcess`, and its shape is the open question of slot C-07 (`dispatch-and-launch-mechanism` has proposals and rounds but no `ADJUDICATION-RESULT.md`) [CODE-VERIFIED: directory listing]. B concedes the dependency (B 8, last bullet). Building a transport on an undecided launcher is the order-of-operations error; the kit has no such dependency.
2. **The two product runtimes cannot host a hook at all.** The swarm transport sends one user message and reads text back: `"messages": [{"role": "user", "content": prompt}]` (`openai_compat.py:384-388`) [CODE-VERIFIED]. `reflect-reviewer` has `tools: Read, Grep, Glob, ...` with no Bash and `permissionMode: plan` (`agents/reflect-reviewer.md:5,8`), is told "You do not coordinate with the other reviewers" (`:28`) and that its brief "MUST NOT instruct you to run anything" (`:59`) [CODE-VERIFIED]. B's own hook skeleton skips subagent calls by design (`r5 hook-posttool.sh:14-15`) [CODE-VERIFIED], and no spike tested delivery to a subagent model (research 09 gap 4, `09-collaboration-designs.md:205`) [CODE-VERIFIED as a statement in that file]. So the transport serves exactly one lane, headless `claude -p` main-thread sessions, that does not exist in the product yet.
3. **No exchange arm has separated from its control, and the arms mostly cannot fire.** At the pinned tip: r3's two collab smoke rows both record `phase2_timeout` 1 and its two baseline rows 0 (`BP/r3-axis-flip-challenge/results/smoke.jsonl`, arms A3 and A1) [CODE-VERIFIED]; r5's one real exchange row `smoke-f6diag-sl2-1` is `quarantined`, with `cards_delivered` 1, `requests_acted` 0, `dup_card` 1, `hang_kill` 1 and `slo` SLO_BREACH (`BP/r5-coverage-deflection/results/results.jsonl`) [CODE-VERIFIED]; the pinned r5 pilot rows `s4pilot-a1-sl2-r1`, `-a2-sl2-r1` and `smoke-a1-sl2-1` all record `k` 0 [CODE-VERIFIED]; r4's gate says the F7 arm does not run because luna's act rate is 0/5 (`r4 IMPLEMENTATION.md:159`) [CODE-VERIFIED]. [POST-BASELINE, from A's variant, not re-read by me, and paired with the pinned facts above] `k` is 0 in 15 of 18 r1 role values, the owner relaxed the +35 percent time cap so the exchange arm can run at all (`r1 OVERRIDE.md:3`), and the first counted rows are "inside the noise" (`PROGRESS-20261114.md`).
4. **Delivery is not action, and act rates are unstable.** r2 at the pinned tip: ember `act_rate=0/4` (probe) and `0/5` (finish), luna `4/5` and `5/5` (`BP/r2-idle-shift-sweeper/spikes/RESULTS.md`, REQ-S3 lines) [CODE-VERIFIED]; r4's finish-signal note: "ignored by luna in 3 of 5 sessions and by ember and haiku every time" (`r4 IMPLEMENTATION.md:160`) [CODE-VERIFIED]; r5 and r4 luna rates that differ from r2's are from A's variant [UNVERIFIED by me]. The same r2 file labels REQ-S3 FAIL at 21:32:18Z and PASS at 21:32:55Z with identical rates, and r5 says "No pass threshold (R-47)" [CODE-VERIFIED]. So the "S0/S2 PASS" lines show the pipe works, not that a receiver benefits.
5. **The off state is not free for B at the installer.** `install_hooks.py:42-65` keeps a list `_FRESHNESS_SCRIPTS`; the comment at `:63-64` says `make verify-sync` "requires every entry of `src/superclaude/hooks/scripts/*.sh` to be a member of this list", and `:35-41` notes there is no `--no-orphans` flag yet [CODE-VERIFIED]. B's "one installed hook script" (B 2.2) therefore lands in every user's `~/.claude/hooks/` whether or not exchange ever runs. The precedent `reject-workspace-writes.sh` ("sits dormant ... harmless", `:54-65`) shows this is accepted, but it is a recurring cost for an unmeasured capability.
6. **`hooks.json` is global.** `src/superclaude/hooks/hooks.json:136-160` registers `PostToolUse` for matcher `Read` (`freshness-post-read.sh`, timeout 1, async) and for an auggie matcher [CODE-VERIFIED]; the installer merges these into user settings. B 2.2 says the new hook is "registered as `~/.claude/hooks/...` in `hooks.json`" while B 2.4 says the off state "emits no `--settings`". These do not both hold: a `hooks.json` entry fires on every PostToolUse of every session on every project; a per-session `--settings` entry needs no `hooks.json` line. B must pick the second, and then the `hooks.json` remark is wrong or only means "installed, unregistered" (point X-006).
7. **The unconditional layer stands on code evidence, independent of exchange.** HEAD rejects `anchor` over 200 and `claim` over 300 characters in both parsers: `findings.py:104,118` and `findings_v2.py:111,126,132,136` [CODE-VERIFIED, re-read]. The reflect isolation snapshot exists and is pinned off: `reflect/models.py:94-97` "PINNED OFF by default" [CODE-VERIFIED]. Nothing under `src/superclaude/cli/review/*.py` matches `origin` or `\bext\b` (0 matches) [CODE-VERIFIED], so an open-key or sidecar tag can be added later with no parser change; `findings_v2.py:96-97` rejects only `calibrated_confidence` [CODE-VERIFIED].
8. **The kit is the control any exchange arm needs.** E2's own text: "The static kit (A2) may beat every exchange design on gross gain ... If none does, the right design is the cheapest one: the harness fixes plus the kit in the brief" (`MR:917`) and "The plan cannot detect the central gain estimate of any slot ... only large effects separate from noise at n = 12" (`MR:1128`) [CODE-VERIFIED at the pinned tip]. The kit's cost is priced: pinned r5 rows `s4pilot-a2-sl2-r1` 281.567 s against 179.561 s and 174.274 s for the two A1 rows, about +59 percent elapsed [CODE-VERIFIED rows, ratio derived]. [POST-BASELINE, from A's variant] +10 percent on el2 and +35 percent on hl2. The exchange cost has no priced number.

### Weaknesses identified in Variant B

1. **B's off-state test cannot catch the off-state risk that matters.** B 6.1 compares the new adapter's argv with and without the exchange package; B 6.2 says the existing pins in `tests/cli/reflect/` pass unmodified. But B 2.3 builds the adapter outside `ClaudeProcess.build_command()`, which keeps `--no-session-persistence` in both profiles (`pipeline/process.py:149-152`) [CODE-VERIFIED]. So the existing pins pass vacuously (B does not touch the code they pin), and the argv-diff test compares new code with new code. Neither covers a `hooks.json` registration or the installed script (strengths 5 and 6), which are the real off-state side effects. Test coverage of the claim "off costs zero" is weaker than B states.
2. **The recorded latency and delivery evidence is small-sample and from a different launcher.** The r5 S0 lines record `main_tool_calls` 4, 4, 5 and the r2 S0 lines `tool_use=10`; a "p95" over 4 to 10 calls is effectively the maximum (r5 `NOTES.md` S0; r2 `RESULTS.md`) [CODE-VERIFIED]. B's own test 5 asks for at least 30 calls per model, which concedes the recordings do not meet its bar. B 5 also says the E2 launcher gives reviewers open Bash (`run-reviewer.sh:48`, via synth-05) [UNVERIFIED], so the spike results are for a launcher the product would not ship.
3. **No test of the untrusted-text channel.** B 5 says an anchor from a reviewed PR diff is attacker-controlled text echoed into a peer's context and "B does not claim it is closed". B's eight tests (6.1 to 6.8) contain no adversarial-anchor test (injection text in an anchor, a 600-byte boundary, a forbidden key smuggled into a located-anchor field). The channel is shipped dormant, so the first profile that enables it enables an untested path into INV-G (HIGH).
4. **The transport is step 3 of a chain, not the unlock.** B 6.7 needs the served model recorded (slot C-08) and a launcher (slot C-07); both are open. B 4 says an act-rate measurement "is uninterpretable until the served model is recorded". Shipping the transport first does not make the arm comparison runnable; the two prerequisites do. And the transport's own record only answers the question if `delivered` is above 0: B concedes "delivers in fewer than half of the cells" is plausible (B 6.7), which is the outcome the pinned rows already point to (strengths 3).
5. **No family B would ship has a clean measured success.** B ships harness-authored kinds F1, F3, F6. The only real F6 row is quarantined (`smoke-f6diag-sl2-1`), the between-phase family F1 is the one A cites E8 for, and r3's two collab rows both time out in phase 2 (`phase2_timeout` 1) [CODE-VERIFIED for the quarantined row and the r3 rows; mapping r3 to F1 is A 4.4's, not re-derived by me]. I found no clean measured success for F3 in anything I read. The dormant code has no positive record to protect.
6. **Rot risk with no exerciser.** A hook and launcher that no profile enables run only in unit tests. The runtime facts they depend on move: r4 records that Claude Code updated itself mid-run and `claude` failed to exec (`r4 IMPLEMENTATION.md:158`) [CODE-VERIFIED]. The recurring suite B names, `hook_latency_drift.yaml`, is framed around the `hooks.json` budgets (`:23`: "The hooks.json budgets are short (PreToolUse=1s, PostToolUse=1s ...") [CODE-VERIFIED header], so a per-session `--settings` hook sits outside it unless the suite is extended; that extension is more scope.
7. **The divergence argument shows how, not when.** r2 has no `agent_id` branch (count 0) and r1 uses `flock -w 4` against r5's `flock 9` [CODE-VERIFIED counts]. Those are four study scripts that stop mattering if no arm wins. B concedes the maintenance saving is "argued from divergence already seen, not from a measured maintenance cost" (B 8, last bullet). It justifies one tested copy at build time, not building now.

### Concessions

1. **X-002: A was wrong or stale.** A's section 4.4 says the `--resume` dependency on gateway ids "is not evidenced". At the pinned tip r5 `spikes/NOTES.md` records S2 PASS for claude-sonnet-5-5, claude-haiku-5-5, gpt-6-luna and muse-ember-1.0 with `resume_model` equal to `first_model`, and r2 `spikes/RESULTS.md` records S2 PASS for four models [CODE-VERIFIED as recorded lines]. Remaining caveats: transcripts for r5 are not committed (B says so; I did not check), these are E2-launcher runs, and an F1 run on the swarm HTTP transport does not exist.
2. **X-004: A overstated the latency risk.** A cited "tens to about 150 ms against a 0.1 s planning budget". The recorded main-thread figures are 57 to 85 ms (r5) and 73 and 81 ms (r2) [CODE-VERIFIED lines]; the 143 ms is r4's and I did not re-verify it. The budget fits in the recordings; my objection is the sample size (weakness 2), not the level.
3. **X-005 and U-010 to U-014 have real value.** r2's hook has no `agent_id` branch (0 occurrences) and the skeleton diverges. B's validator design (forbidden verdict keys, 600-byte cap, located-anchor rule, harness-authored kinds only), the untrusted-anchor analysis, the fault-injection list (seal fails closed, review fails open), the C-02 interplay (counts over own-origin lines only) and the `exchange/` package name because `.gitignore:13` is `lib/` [CODE-VERIFIED] should survive any merge as build-time requirements. I propose they be recorded as the preconditions for lifting `exchange: off`, not discarded.
4. **C-008 has force.** The deciding measurement would be easier to repeat from a product transport. My answer is that the studies already run from the E2 working tree ([POST-BASELINE] `lib/` committed for r3, r4, r5: counts 3, 7, 11 at `c44c98a77`, verified by `git ls-tree`; pinned counts are all 0), so a product transport is not what blocks the experiment now; the launcher (C-07) and served-model record (C-08) are. But B is right that at the pinned tip no design could run from its own commit.
5. **A's own weaknesses.** (a) The kit's benefit is unproven: the [POST-BASELINE] means come from n = 2 against n = 4 and overlap the A1 spread; both catalogues were induced from the same ten missed issues; I do not claim the kit works, only that H1 and H2 stand without it. (b) A's trigger ("an exchange arm beats the kit on a package with real ground truth") may never fire: E2 ground truth is 16 defects in 3 tasklist packages, with no hold-out and 3 items carrying 91 percent of defect-rich catches (`research/08-e2-evidence-grading.md:52,134`) [CODE-VERIFIED as statements]. Indefinite deferral then leaves no product-level home for per-model capability facts. Mitigation I would add to A: record the act-rate probe result and served model in the run record (slot C-08), with no transport. (c) A's retrofit-is-bounded claim is argued, not measured (A-003). (d) Several A citations are [UNVERIFIED] research quotes, including the stale `--resume` one. (e) The catalogue file and `kit` key also add layout items to `make verify-sync` (A already concedes this under INV-K).

### Shared-assumption responses (A-001..A-003)

**A-001: QUALIFY.** E2 ground truth is defects that surfaced during implementation of three tasklist packages: designSpec 10 items (5 blocking), alias 4 (3), control 2 (0); no held-out package; 4 of 16 never caught; a true novel defect scores as a wrong blocker (`research/08-e2-evidence-grading.md:134`) [CODE-VERIFIED as statements; the underlying `ground-truth.json` I did not re-read]. It can arbitrate "exchange arm against kit" for tasklist review only. It says nothing about PR review, rf-qa or reflect, and its scoring penalises novel findings, which is the very thing exchange is supposed to produce. So the trigger is valid for the tasklist module only, with a hold-out added (A section 6.7); for other modules exchange stays off with no ground truth to turn it on. This cuts against both papers: A's trigger may rarely fire, and B's transport has no ground truth for any module where it would be enabled.

**A-002: QUALIFY, leaning REJECT as worded.** Argv and brief-byte equality proves the launched session is unchanged. It does not prove there are no other off-state effects. For B the list is concrete and verified: a script copied into every user's `~/.claude/hooks/` (`install_hooks.py:42-65`), an entry in `_FRESHNESS_SCRIPTS` required by `make verify-sync` (`:63-64`), no `--no-orphans` escape (`:35-41`), possible global `hooks.json` registration (`hooks.json:136-160`), a new package and tests, and a latency-suite extension. For A the list is shorter but not empty: a profile key, a catalogue file and a layout item for `make verify-sync` (A's INV-K). Both papers should add a second test: "no new file under `~/.claude/hooks/`, no new `hooks.json` entry, no new key in the run record when the switch is off". A's off state passes that test by construction; B's does not.

**A-003: QUALIFY.** Neither paper measured retrofit or maintenance cost, so "cheaply revisitable" is an assumption in both. The costs are asymmetric in two verified ways. Adding later is additive: both parsers accept unknown keys (`findings_v2.py:96-97` rejects only `calibrated_confidence`), nothing in `cli/review/*.py` reads `origin` or `ext`, and `reflect` is untouched. Removing a shipped dormant script is not supported today: `install_hooks.py:40-41` records the `--no-orphans` flag as future work, so an installed orphan stays in `~/.claude/hooks/`. A's cost of waiting is real too: the four E2 copies live on a study branch, and a build later starts from the described skeleton (`09-collaboration-designs.md` section 1.3) rather than a tested product copy. I rate A's retrofit bounded, with that cost named, and B's dormant cost recurring but small.

### Per-point table (all 25 points)

"Winner" is who should win the point. Confidence is 50-100 (50 = coin flip). Cites are to this file's numbered sections (S = Strengths, W = Weaknesses, C = Concessions).

| # | Point | Winner | Conf. | Evidence in one sentence |
|---|-------|--------|-------|--------------------------|
| S-001 | Section order | Tie | 50 | Both orders carry the same required sections; no correctness or risk effect. |
| S-002 | Evidence form | B | 55 | B keeps [POST-BASELINE] material in one labelled sub-section, which serves the binding staleness rule better than A's per-row tags alone. |
| S-003 | Core / non-core partition | A | 68 | Core = H1-H4, catalogue, reserved key is the part with code evidence (`findings.py:104,118`, `reflect/models.py:94-97`); B's extra exchange package, hook, launcher have no HEAD runtime (S1, S2). |
| C-001 | What the core builds now | A | 70 | `launch: {}` and "dispatch mechanism per model not defined yet" (`review-tiers.default.json:25-29`) mean the transport has nothing to run on today (S1). |
| C-002 | Gate for building exchange | A | 62 | B's repeatability argument is real (C4), but the arm comparison also needs C-07 and C-08, so the transport is not the unlock (W4). |
| C-003 | Static kit mechanics | A | 75 | A states a per-profile `kit` key, reflect off, and a cost gate against +59% (pinned r5 rows 281.567 s vs 179.561 / 174.274 s); B states none (S8). |
| C-004 | Launch path and hook placement | A | 75 | B's adapter bypasses `ClaudeProcess` (`process.py:149-152` keeps `--no-session-persistence`) and depends on undecided C-07; B concedes the dependency (S1). |
| C-005 | Between-phase family F1 | A | 55 | B is right that `--resume` passes on gateway ids (C1), but F1's only collab smoke rows both time out (`phase2_timeout` 1) and no swarm run exists. |
| C-006 | Peer-origin tag | B | 55 | Mandatory harness-written sidecar protects the C-02/C-03 quorum counts better than A's "preferred"; A's open-key point (S7) keeps either possible. |
| C-007 | Test and measurement plan | A | 55 | A's matching-control, act-rate and hold-out items decide the build question; B's transport tests (fault injection, replay) are better but test code that need not exist yet (W1). |
| C-008 | Where the decisive measurement runs | A | 58 | B is right no design ran from its commit at the pinned tip (0 `/lib/` paths), but the launcher and served-model record, not a product transport, are the blockers (C4, W4). |
| C-009 | Reading of [POST-BASELINE] results | A | 62 | Same facts; `k` 0 almost everywhere and a relaxed time cap argue for measuring first; B's "the record is itself a finding" argues for the record (C-08), not the transport. |
| C-010 | Message validation, untrusted text | B | 75 | B's forbidden keys, 600-byte cap, located-anchor rule and attacker-text analysis are deeper than A's one sentence; keep as build-time requirements (C3). |
| C-011 | Off-state guarantee mechanism | A | 60 | A's profile key with one legal value is smaller; B's argv-diff test compares new code with new code and cannot see installer or `hooks.json` effects (W1). |
| C-012 | PR review and rf-qa effect | A | 60 | Both keep exchange off; A also adds no lane, while B's own analysis says PR anchors are attacker text and delivery to a read-only reviewer is unshown. |
| X-001 | Build the transport now? | A | 66 | Verified: no launcher, no family with a clean success, no arm separated from its control (S1, S3). |
| X-002 | `--resume` on gateway ids evidenced? | B | 82 | r5 `NOTES.md` S2 PASS for four models and r2 `RESULTS.md` S2 PASS for four models at the pinned tip; A's "not evidenced" is stale (C1). |
| X-003 | Does main-thread-only delivery justify owning the transport? | A | 68 | Both accept the facts (swarm one-message, `reflect-reviewer` no Bash, subagent calls skipped); the product has no main-thread headless reviewer lane yet (S1, S2). |
| X-004 | Hook fits the 0.1 s budget? | B | 62 | Recorded p95 57-85 ms (r5) and 73/81 ms (r2) fit; but over 4-10 calls, so weak (C2, W2). |
| X-005 | Divergence justifies one product copy? | B | 55 | r2 has 0 `agent_id` occurrences while r1, r4, r5 skip subagent calls; true for how to build, not for when (W7). |
| X-006 | Does the `hooks.json` registration keep off inert? | A | 72 | `hooks.json:136-160` is a global PostToolUse registry merged into user settings; B 2.2 and 2.4 conflict until B drops the `hooks.json` registration (S6). |
| X-007 | Is waiting free? | A | 58 | Nothing is lost on the E2 branch and `lib/` is now committed for r3-r5 [POST-BASELINE, pinned count 0]; B's repeatability point and A's own deferral cost (C5b) keep this close. |
| A-001 | Ground truth transfers to the modules | QUALIFY | n/a | Valid for tasklist review only; 16 items, 3 plans, no hold-out, novel findings scored as wrong blockers (`08-e2-evidence-grading.md:134`). |
| A-002 | Off-state byte equality proves inertness | QUALIFY (lean REJECT) | n/a | Misses installer list, `~/.claude/hooks/` copy, `hooks.json` and sync-gate effects (`install_hooks.py:42-65`); A's off state passes a stricter test, B's does not. |
| A-003 | The decision is cheaply revisitable | QUALIFY | n/a | Neither measured it; adding later is additive (open keys) but a shipped orphan script cannot be skipped or removed (`install_hooks.py:40-41`). |

Stale or unverified items I could not settle: the transcripts behind r5's S0/S2 lines are not committed (per B; not checked); the r4 143 and 90 ms figures; the [POST-BASELINE] `k` counts and `OVERRIDE.md` quote (taken from A's variant, not re-read); the r5 and r4 luna act rates other than r2's.

## Round 1, Advocate B (Variant 2 = Proposal B), slot C-12 collaboration-exchange-capability

Status: Complete (see end of file)

Tags: [CODE-VERIFIED] I re-read the file or blob this session; [UNVERIFIED] taken from a research or variant file and not re-read; [POST-BASELINE] read only at E2 commit `c44c98a77` (never the only evidence for a decisive point). Code state HEAD `50d4d2b9d`. E2 pinned tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`.

### Position summary

Build one small, dormant, engine-local exchange package now (one hook script, harness-written board, seal check, `panel-msg/1` validator, `collab` record, a separate raw-id launch adapter), off by default and pinned off by an argv-diff test; the static kit, H1 and H2 ship alongside, so the whole dispute is that delta. My case is narrow: the skeleton already exists four times and has diverged, recorded spikes show hook delivery and `--resume` on gateway ids, and only a product-owned transport lets anyone other than the study producer repeat the exchange-versus-kit comparison. I corrected one defect in my own paper (the hook must NOT be a `hooks.json` entry, see X-006) and I concede that the case weakens sharply if slot C-07 yields no launcher with persistence and per-session `--settings`.

### Steelman of Variant A

Strongest form: the core should not own a transport whose benefit nobody has measured and whose runtime does not exist at HEAD. HEAD's two reviewer runtimes cannot host it: the swarm transport sends one user message and reads text back (`src/superclaude/cli/swarm/transports/openai_compat.py:384-388`, [CODE-VERIFIED]), and the Agent-tool reviewer has no Bash, runs in `permissionMode: plan` and is told it does not coordinate (`src/superclaude/agents/reflect-reviewer.md:5-8,28`, [CODE-VERIFIED]). The only host is a headless `claude -p` main thread with persistence on and per-session settings, and no `"--settings"` literal exists anywhere in `src/superclaude/cli` ([CODE-VERIFIED] by grep this session), so B's adapter would be the first user of that path and its tests would exercise only B's own fixtures. E2's own text says the kit may beat every exchange design (`MR:917`) and that the plan cannot detect the central gain (`MR:1128`) [UNVERIFIED by me, both papers cite it]. The kit is also the control any exchange arm needs, so shipping it first is step one of every path. [POST-BASELINE] data as A reports it (`k = 0` in 15 of 18 r1 role values, the owner relaxing the +35 percent cap so exchange arms could run at all, first counted rows inside the noise) point the same way; I did not re-derive those counts. A keeps a cheap retrofit path (open unknown keys, sidecar, reserved `exchange` key), so waiting is nearly free. What A gets right and B must not dispute: nothing in the product measures exchange today; the transport has no production runtime at HEAD; the deciding experiment can be run from `.dev/` without a product transport; and A adds three tests B lacks (brief lint for read-only lanes, kit cost per panel, catalogue hold-out).

### Strengths claimed

1. **The skeleton exists four times and the copies differ in behaviour.** [CODE-VERIFIED, blobs at the pinned tip.] r5 `bin/hook-posttool.sh` (72 lines) bakes its arguments (`:4-6`), skips any call carrying `agent_id` (`:14-15`), takes an untimed `flock 9` (`:17-18`), seals the transcript before first delivery and fails closed (`:42-53`), emits `additionalContext` JSON. r1 `tools/radar-hook.sh` uses `flock -w 4` (`:22`) and an `agent_id` skip (`:24`). r2 `bin/hooks/receiver-hook.sh`: `grep -c agent_id` returns 0, so that copy cannot tell a subagent call from a main call. The timed versus untimed lock is a real behavioural fork (give up after 4 s versus block behind a stalled sibling). One tested copy removes the fork; A's answer ("described line by line in r09 section 1.3", A 8) leaves four unreconciled copies as the only reference, and r09 itself is [UNVERIFIED] by me. Honest limit: these are throwaway study scripts, so divergence among them proves the design is under-specified, not that a product maintenance burden exists.
2. **Hook delivery and `--resume` have recorded passes on gateway ids, in two independent packages.** [CODE-VERIFIED as recorded lines; the transcripts are not committed, so the runs themselves are not re-run.] r5 `spikes/NOTES.md`: S0 PASS for claude-sonnet-5-5, claude-haiku-5-5, gpt-6-luna with `delivered=1 subagent_calls=0 snapshot_sha_ok=true hook_ms_p95` 59, 57, 85; S2 PASS for those three plus muse-ember-1.0 with `resume_model` equal to `first_model`. r2 `spikes/RESULTS.md`: S0 PASS ember (p95 73 ms) and luna (81 ms), S2 PASS for four models. This is why A's "`--resume` on gateway ids is not evidenced" (A 4.4, citing r09 OQ-2) is stale at the pinned tip. Scope limit that I own: this shows delivery to a main-thread session with Bash tool calls, not to a read-only subagent.
3. **The off state can be made inert, and the repo already has a precedent for an installed-but-unregistered hook script.** [CODE-VERIFIED.] `src/superclaude/cli/install_hooks.py:94-96` ships `launch-level-pre-push.sh` "installed into a worktree's hooks/pre-push by the Orca launcher, never registered in settings.json", and `grep -c launch-level-pre-push src/superclaude/hooks/hooks.json` returns 0. `Makefile:307-319` (`make verify-sync`, "Installer Registration") requires every `scripts/*.sh` to be in `_FRESHNESS_SCRIPTS`. So the correct shape is: script in `src/superclaude/hooks/scripts/`, name added to `_FRESHNESS_SCRIPTS`, NO `hooks.json` entry, activation only through a per-session `--settings` JSON that the adapter writes. Arguments are baked into that command string (r5 `:4-6`), so the installed path is resolved at launch and no `src/superclaude/` path appears in an installed primitive.
4. **A new launch path is required, and the pins prove it must be separate.** [CODE-VERIFIED.] `ClaudeProcess.build_command()` keeps `--no-session-persistence` in both profiles (`src/superclaude/cli/pipeline/process.py:149-152`); `tests/cli/reflect/test_claudeprocess_reflect_children_restricted.py` asserts it stays in the restricted profile (`:111-112`) and pins the full default argv (`:115-125`). No `--settings` exists in the CLI. So exchange cannot be a flag on `ClaudeProcess`; it is a new adapter (axis 6.5 option 2, slot C-07). This is also A's strongest point turned around: because nothing in the product can launch such a session, the only way to test the claim "hooks reach panel reviewers in the product" is to own the adapter.
5. **Nothing at HEAD overlaps, so the build is additive.** [CODE-VERIFIED.] `PostToolUse` has 29 occurrences in 6 text files of `src/superclaude/cli` (`eval/coverage.py`, three eval suite yamls, `eval/suites/README.md`, `install_hooks.py`), none under `cli/review/`, `cli/reflect/` or `cli/swarm/`; `panel-msg` and `additionalContext` have zero hits. `cli/reflect/panel_lint.py:185` is `CONTRACT_VERSION = "1.8.0"` and `cli/review/findings_v2.py:96-97` rejects only `calibrated_confidence`, so an engine-local `cli/review/exchange/` package touches no pinned contract.
6. **Packaging trap avoided.** [CODE-VERIFIED.] `.gitignore:13` is `lib/`. E2's `lib/` folders were untracked at the pinned tip (zero `/lib/` paths for r1 to r5) and were added with `git add -f` later [POST-BASELINE, `PROGRESS-20261114.md:36` as reported in my Proposal B paper; not re-read this round]. A product package named `exchange/` avoids the same silent loss.
7. **Validator and untrusted-text analysis exist only in B.** The `panel-msg/1` table (forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located anchor), harness-authored kinds only, and the observation that a located anchor from a reviewed PR diff is attacker-controlled text echoed into a peer's context (B 5). A mentions only that INV-H "would have to cover" board text (A 5). If exchange is ever built, this analysis is the part that is expensive to rediscover. Honest limit: it is design value, and design can be kept as a document without being built.
8. **Test-coverage position.** B names six structural tests that can run today with no ground truth (off-state argv identity, existing pins unmodified, per-model S0 and S2 on the product launcher, fault injection, hook p95 over 30 calls, single-copy replay with `agent_id` and two parallel calls) plus the pre-registered arm comparison. The replay test would fail on the r2 copy's missing `agent_id` branch, which is the sort of defect the four-copy state hides.

### Weaknesses identified in Variant A

1. **The gate is circular without an owner.** "Not built until an exchange arm beats the kit on a package with real ground truth" (A 1, 6.1) needs a runnable exchange arm. At the pinned tip none of r2 to r5 could run from the commit (`lib/` absent, [CODE-VERIFIED]); at `c44c98a77` three can and r2 still cannot [POST-BASELINE]. All arms run from `.dev/eval-workspaces` with study paths and raw ids. A says the experiment "costs nothing extra under either position" (A 6.1); true only if the study keeps running there, and A names no owner or date for that. Fair counter (A's best): the arms can finish in `.dev/` and do not need a product transport. I answer only that the result then needs a second port into a product launcher, with the served-model check of slot C-08, before it can bind a product decision.
2. **A applies its own principle unevenly.** A refuses to build a transport until gain is measured, yet ships the catalogue and a `kit: on|off` key to spec-review and tasklist as "first candidates for `on`" (A 3.4) on evidence A itself calls n = 2 against 4, one judge, and not the metric of record (A 4.2). A distinguishes by cost (text versus code), which is fair, but the kit's matched-control evidence is also thin and rests on [POST-BASELINE] rows for the favourable direction ("a direction that is not negative", A 4.2). The pinned-tip kit number is +59 percent elapsed (r5 rows, A's own derived ratio) and no gain row exists at the pinned tip.
3. **"No exchange arm has a matching control row" (A 4.2) is contradicted by A's own 4.3.** A 4.3 reports counted rows "collaboration against the same-harness baseline" for all five designs [POST-BASELINE, as A reports]. The statement holds only if "matching control" means the A2 kit arm. A should say so; as written it overstates.
4. **A ships a reserved key that can only be off.** `exchange` with the single legal value `off` (A 3.1 item 6) is config with no implementation, tested only for inertness. It also still needs a profile validator, an off-state byte test and, per `Makefile:307-319`, any new layout item in `verify-sync` (A 5 concedes "INV-K"). A is not zero-footprint; its footprint is smaller and located in profile validation rather than in `hooks/scripts/`.
5. **A leans on UNVERIFIED research for the load-bearing "runtime facts unverified" claim.** E5 (subagent delivery), E12 (external debate-versus-voting literature) and the `--resume` doubt (OQ-2) are [UNVERIFIED] in A's own table. The `--resume` doubt is contradicted by recorded passes (strength 2). The hook-cost doubt ("tens to about 150 ms against a 0.1 s planning budget", A 8) mixes r4's unverified 143 and 90 ms with recorded 57 to 85 ms.
6. **A treats E4 (subagent skip) as evidence there is no runtime.** The skip is deliberate in three copies and absent in r2; it scopes the transport to main-thread sessions, which is the only lane where delivery was recorded. It is an argument for owning one correct copy of the skip, not against the transport.

### Concessions

1. **My `hooks.json` wording was wrong.** Proposal B section 2.2 says the hook is "registered as `~/.claude/hooks/...` in `hooks.json`". `src/superclaude/hooks/hooks.json` already carries a `PostToolUse` block (`:136`), and `install_hooks.py` merges `hooks.json` entries into the user's `~/.claude/settings.json`, so a registered entry would fire in every user session, outside any panel, with no baked arguments. The correct form is the `launch-level-pre-push.sh` precedent (strength 3): script file only, no registration. A's reserved-key route has no such hazard. This is a real defect in B as written; the fix is small.
2. **The transport has no production runtime at HEAD.** Swarm HTTP has no tool loop; the Agent-tool reviewer is skipped by the skeleton's own `agent_id` filter and is read-only; `"--settings"` appears nowhere in `src/superclaude/cli`. B's whole hook half depends on slot C-07 producing a persistence-on launcher with per-session settings. If it does not, B shrinks to validator, sidecar and an F1 second prompt, and A wins X-001.
3. **No benefit is measured, and [POST-BASELINE] data lean against exchange so far.** `k = 0` in most cells, r2's smoke row delivered nothing, kit rows ahead of isolated rows at small n (all as A reports and as I listed in my own paper section 3.F). I do not claim exchange improves findings.
4. **"Four copies cost more than one" is argued from divergence among study scripts, not from a measured maintenance cost.** I concede A's point that the copies are disposable.
5. **A's measurement can run without my transport.** My claim that a product transport is needed to run the deciding comparison is true only for repeatability by others on the product launcher, not for running the experiment at all.
6. **A's extra tests are good and B should adopt them:** brief lint for read-only lanes, kit cost per panel at n of at least 4, catalogue hold-out of at least 4 unseen defects, and the single common act-rate probe. B's variant is silent on the first, second and fourth.
7. **Kit gating belongs to A.** B states no `kit: on|off` key or per-module cost gate (C-003); A's is better specified.

### Shared-assumption responses (A-001, A-002, A-003)

- **A-001 (E2's ground truth transfers to the modules the core serves): QUALIFY.** E2's 16 ground-truth items in 3 plans cover tasklist review only (B 7, A 6.1 both cite r08, [UNVERIFIED] by me); 3 items carry 91 percent of defect-rich catches (A 6.1, [UNVERIFIED]); and both E2 catalogues were induced from the same ten missed issues (A 6.7). So an arm-versus-kit result would be decision-relevant for tasklist and plan-versus-source spec review, plausibly for reflect UC-1, and not for PR review or rf-qa, where no ground truth exists. Neither paper claims otherwise for those modules (both leave exchange off), but both treat "a package with real ground truth" as one thing. A hold-out set is a precondition, not an extra.
- **A-002 (byte-identical argv or brief with the switch off proves inertness): QUALIFY, and it is partly false for B as I first wrote it.** Argv identity covers the launch only. [CODE-VERIFIED] side effects it misses: a new `scripts/*.sh` must be added to `_FRESHNESS_SCRIPTS` (`Makefile:307-319`; `tests/cli/test_install_hooks.py` has per-script membership asserts, e.g. `:1092`, `:1110`) and is then copied to `~/.claude/hooks/` on every `superclaude install` even when off, so a dormant hook file is shipped to every user; a `hooks.json` entry would fire everywhere (concession 1); and any `collab` telemetry field must be absent when off. A's reserved key has its own footprint (profile validator, `verify-sync` layout item, A 5 INV-K). Required off-state tests for either side: no `hooks.json` or merged-settings diff, no board directory, no `--settings`, no new telemetry key, and the installed-file set diff named explicitly in the test so the dormant script is a declared item, not an accident.
- **A-003 (the decision is cheaply revisitable either way): QUALIFY.** Neither paper measured retrofit or maintenance cost (A-003 as stated). My side of the asymmetry: removing a dormant engine-local package is a delete of one directory, one script and one list entry, guarded by an off-state test, so B's downside is bounded and mechanical. A's side: A's retrofit is cheap only if C-01's open unknown keys and the sidecar hold, and the part A defers (launcher, settings, hook) depends on runtime facts still open. Honest limit on mine: a dormant package still accrues test, lint and sync cost until someone deletes it, and "dormant code stays dormant" is exactly the pattern a reviewer should distrust.

### Per-point table (all 25 points)

Winner = who should prevail on that point. Confidence is 50 to 100 percent. "Merge" means both positions should be combined.

| # | Winner | Conf. | One-sentence evidence |
|---|---|---|---|
| S-001 | Merge | 50 | Section order is presentation only; neither order changes any claim. |
| S-002 | A | 55 | A's numbered claim table with a tag per row is easier to audit than B's bullets, though B's tags are equally explicit. |
| S-003 | B | 52 | The partition is the whole dispute; B's core adds one package, one script and one adapter, and A's omits them, but I rate it a near toss-up pending slot C-07. |
| C-001 | A | 55 | What the core builds now: with no `--settings` anywhere in `src/superclaude/cli` and no tool loop in swarm, B's build has no production runtime at HEAD (concession 2). |
| C-002 | A | 60 | "Build after an arm beats the kit" is the more defensible gate, since the experiment can run from `.dev/` (concession 5), though A names no owner for it (weakness 1). |
| C-003 | A | 75 | A specifies the catalogue, `kit: on\|off` and a per-module cost gate; B is silent (concession 7). |
| C-004 | A | 60 | B's adapter must be separate from `ClaudeProcess` (pins at `process.py:149-152` and the restricted-profile test `:111-125`, [CODE-VERIFIED]) and hangs on the open slot C-07; A builds nothing that depends on it. |
| C-005 | A | 55 | F1 needs no hook and `--resume` has recorded gateway passes (strength 2), but no F1 run exists on swarm [UNVERIFIED] and A cites r3's `phase2_timeout` rows (E8, [UNVERIFIED] by me). |
| C-006 | Merge | 60 | Both converge on a harness-written sidecar; A keeps in-line open, B mandates sidecar, and `findings_v2.py:96-97` rejects only `calibrated_confidence` so either works [CODE-VERIFIED]. |
| C-007 | Merge | 55 | B's tests (fault injection, per-model S0 and S2, latency p95, single-copy replay) cover a transport; A's (kit cost n >= 4, hold-out, brief lint, act-rate probe) cover the kit; adopt both (concession 6). |
| C-008 | B | 55 | Where the measurement can run: at the pinned tip no E2 arm ran from the commit (zero `/lib/` paths, [CODE-VERIFIED]); at `c44c98a77` three of five can [POST-BASELINE], so B's point is partly overtaken and A's "nothing extra under either" is partly right. |
| C-009 | A | 62 | Same facts, but A's reading (`k` mostly 0, cap relaxed, no separation) is the more cautious and is not contradicted by B's own listing of the counter-evidence; both are [POST-BASELINE]. |
| C-010 | B | 75 | B has a validator design, forbidden verdict keys and the attacker-controlled-anchor analysis; A only notes INV-H would apply. It matters only if exchange is built. |
| C-011 | A | 55 | A profile key with one legal value is simpler than an adapter parameter, but both need an installed-file-set and settings-merge diff test (A-002). |
| C-012 | A | 52 | A states a kit effect on PR and rf-qa; B states only `exchange: off`; both keep exchange out of read-only lanes, so little separates them. |
| X-001 | A | 55 | Build the transport now: contested; B's narrow form (validator, sidecar, one tested hook script, adapter) is defensible, but without C-07 and any measured gain A's deferral is safer. |
| X-002 | B | 85 | Recorded S2 PASS for four gateway ids (r5 `NOTES.md:23-30`) and four more (r2 `RESULTS.md`, `21:14:38Z` to `21:15:06Z`) at the pinned tip [CODE-VERIFIED lines]; A's doubt cites a research file and is stale. Not re-run. |
| X-003 | A | 55 | Both accept the same facts (delivery recorded on main-thread sessions with Bash, `subagent_calls=0`); main-thread-only scope makes the transport narrower, which favours not owning it yet. |
| X-004 | B | 70 | Recorded p95 of 59, 57, 85 ms (r5 S0) and 73, 81 ms (r2 S0) are under the 0.1 s planning budget [CODE-VERIFIED lines]; A's "about 150 ms" mixes in unverified r4 numbers. These are study-script timings, not a product copy. |
| X-005 | B | 62 | r2 has zero `agent_id` references, r1 uses `flock -w 4` against r5's untimed `flock 9` [CODE-VERIFIED]; but these are disposable study copies (concession 4). |
| X-006 | A | 65 | As written B's "registered in hooks.json" is a defect (a `hooks.json` entry fires in every session; `hooks.json:136` already has `PostToolUse`); fixable by the `launch-level-pre-push.sh` precedent (`install_hooks.py:94-96`, absent from `hooks.json`), which A never needed. |
| X-007 | A | 60 | Waiting is nearly free: the packages stay on the branch, three now have `lib/` [POST-BASELINE], and A's open-key retrofit holds if C-01 holds; B's "not free" point applies mainly to r2. |
| A-001 | Shared: QUALIFY | 70 | Ground truth covers tasklist review only (16 items in 3 plans, [UNVERIFIED] r08); transfers plausibly to spec review and reflect UC-1, not PR review or rf-qa. |
| A-002 | Shared: QUALIFY | 85 | Argv identity does not cover the installed-file set (`Makefile:307-319`, `test_install_hooks.py:1092`), a `hooks.json` entry, or a telemetry key [CODE-VERIFIED]; add explicit diff tests. |
| A-003 | Shared: QUALIFY | 65 | Neither side measured retrofit or maintenance cost; B's removal is mechanical and bounded, A's retrofit depends on C-01's open keys and open runtime facts. |

Net: the only points where I hold B with real confidence are the recorded-evidence points (X-002, X-004, C-010); on the build-now question (S-003, C-001, C-002, C-004, X-001) I rate A at least equal and B only if slot C-07 delivers the launcher. The most useful merge is A's layer plus B's validator, sidecar and one tested hook script, kept unregistered and dormant, with A's three extra tests.

Status: Complete

## Round 2: Rebuttals

## Round 2 rebuttal, Advocate A (Variant 1 = Proposal A), slot C-12 collaboration-exchange-capability

Status: Complete

Tags: [CODE-VERIFIED] I read the file or ran the search this session at HEAD `50d4d2b9d`; [UNVERIFIED] taken from a research or variant file, not re-read; [POST-BASELINE] read only at E2 commit `c44c98a77`, never the only evidence for a decisive point. E2 pinned tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`. Read-only session; I read B's Round 1 (`r1-advocate-B.md`), my Round 1, both variants and the diff analysis. I did not touch the forbidden paths.

### Position after rebuttal

I now concede more than in Round 1. Three of B's points land: (1) my gate "not built until an exchange arm beats the kit" conflates building the measuring instrument with enabling the capability, and is ownerless as written; (2) my installer-cost argument against B's script is much weaker than I made it, because three existing scripts are shipped dormant on purpose; (3) B's validator, sidecar and untrusted-anchor analysis is real value that must not be lost. I still hold that nothing should be built now, because the only product launcher B's hook needs does not exist at HEAD (slot C-07 open, `--settings` appears nowhere in code). My updated resolution is a conditional hybrid (section 5): build B's transport as the instrument for the pre-registered comparison when a launcher decision, a metric of record and a named owner all exist, still off by default.

### 1. Response to B's Weaknesses 1 to 6

#### B-W1: "The gate is circular without an owner"

Re-checked against my own text. [CODE-VERIFIED, `variant-1-original.md` 6.1 and 8]. The gate is not self-referential: it needs an exchange arm that can run, and arms do run from `.dev/eval-workspaces` (B concedes this as "A's best counter"). But B is right on two things.
- Ownerless: 6.1 names a decision rule, a metric slot (X-14) and a power calculation, but no person, date or home for the experiment. "Costs nothing extra under either position" is true only if someone runs it. That is a gap in A, not a rebuttal.
- Instrument versus capability: 6.1 says the build waits for "an exchange arm beats A2". But an arm result produced on the E2 launcher (open Bash, `run-reviewer.sh:48` via synth-05 [UNVERIFIED]) does not bind a product decision until it is repeated on a product launcher with the served model recorded (slot C-08). Under my own text the product transport would then be built after the result it is needed to make repeatable. That ordering is defensible only if the E2 result is read as a trigger to port, which is what A 7 last bullet says; but it leaves the porting step with no home until after the trigger.
Concession: A's gate should be split in two (section 5). Held: the claim "the transport is not the unlock" survives, because the launcher (C-07) and the served-model record (C-08) block the repeat, not the hook script. [CODE-VERIFIED] `review-tiers.default.json:26-29`: gateway note "dispatch mechanism per model not defined yet", `"launch": {}`.

#### B-W2: "A applies its own principle unevenly" (kit shipped on thin evidence)

Partly conceded. [CODE-VERIFIED reading of my own 3.4 and 4.2]. I distinguish by cost (brief text versus code), which is a legitimate rung of the ladder, and the kit sits behind `kit: on|off` with a per-module cost gate; but I agree the kit's benefit evidence is thin (n = 2 against 4, one judge, same ten missed issues for both catalogues). The honest version: the kit is cheap to ship and cheap to turn off, so shipping it default `off` for modules without a hold-out is as defensible as B's dormant transport. I will not claim "first candidates for `on`" for spec-review and tasklist without the hold-out test (my measurement 7). The pinned-tip kit cost is +59 percent elapsed (r5 rows `s4pilot-a2-sl2-r1` 281.567 s against 179.561 and 174.274 s, derived ratio [UNVERIFIED by me this round; recomputed in Round 1]), and no pinned-tip gain row exists. Position changed to: kit ships `kit: off` by default until measurement 2 and 7 pass.

#### B-W3: "No exchange arm has a matching control row" overstated

Concede the wording. [POST-BASELINE, from my own 4.3]. Later commits do have counted rows for collaboration arms against the same-harness baseline. The accurate statement is: no exchange arm has a row matched against the A2 kit arm at a size that separates from noise; E2's own plan says only large effects separate at n = 12 (`MR:1128`) [UNVERIFIED re-read; pinned-tip statement quoted in Round 1]. I should have written "no matched A2 control" and did not.

#### B-W4: "A ships a reserved key that can only be off"

Concede the footprint is not zero. [CODE-VERIFIED, `Makefile:307-327`]. The `verify-sync` Installer Registration block checks only that `src/superclaude/hooks/scripts/*.sh|*.js` equals `_FRESHNESS_SCRIPTS` (both missing and stale entries fail). It does not check profile keys. So my reserved key needs a profile validator, an off-state byte test and (INV-K) a layout item, but it adds nothing to `hooks/scripts/`, `_FRESHNESS_SCRIPTS` or the user's `~/.claude/hooks/`. Smaller and in a different place, not zero. Held: a key with one legal value is a pin, not an implementation, and A-002's stricter test ("no new file under `~/.claude/hooks/`, no `hooks.json` entry, no new run-record key when off") passes for it by construction.

#### B-W5: "A leans on UNVERIFIED research for 'runtime facts unverified'"

Concede two of three. `--resume` on gateway ids is evidenced at the pinned tip (X-002, conceded in Round 1). The "about 150 ms" figure mixes in r4's unverified numbers (X-004 below). Held: delivery to a subagent model remains unshown, the swarm transport sends one user message and no tool loop, and `reflect-reviewer` has no Bash. [CODE-VERIFIED in Round 1: `openai_compat.py:384-388`; `agents/reflect-reviewer.md:5,8,28,59`.] These are code facts, not research claims, and they remain the reason the transport has no host lane at HEAD.

#### B-W6: "E4 (subagent skip) is argued as evidence there is no runtime"

Concede the framing. The skip scopes the transport to main-thread sessions; it is an argument for one correct copy of the skip, not against the transport. But "main-thread headless `claude -p` with persistence on and per-session settings" is a lane with no code at HEAD: `"--settings"` has zero matches in `src/superclaude/**/*.py` [CODE-VERIFIED this session; searched with the flag escaped as `\-\-settings` so the pattern was not read as a tool option]. So the narrowing helps B's hook correctness and still leaves C-07 as the blocker.

### 2. Verifications of the decisive facts (the ones B's merge proposal depends on)

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

### 3. Response to B's per-point wins and its merge proposal

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

### 4. Are B's validator, sidecar and untrusted-anchor analysis preconditions or code?

Preconditions, recorded as a design note (not built). Reasons: the validator and sidecar have no caller without an exchange arm (the validator's kinds F1, F3, F6 are harness-authored, and the only real F6 row I found is quarantined, [CODE-VERIFIED in Round 1]); the forbidden-key table and 600-byte cap are best tested against a real hook output, which does not exist in the product; and a validator written now would be a second unexercised dormant surface. The note is not low-value: it is exactly the content that is expensive to rediscover, so it must be a binding precondition on lifting `exchange: off`. Its minimum contents:
1. `panel-msg/1` per-kind keys, forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, harness-authored kinds only (U-010).
2. Peer-origin tag as a harness-written sidecar keyed by reviewer id and finding id; key name not `origin` (CL-X11); quorum counts over own-origin lines only (U-014, C-02).
3. Untrusted text: an anchor taken from a reviewed PR diff is attacker-controlled and would be echoed to a peer; board files never enter the `review-telemetry` export; an adversarial-anchor test (injection text, 600-byte boundary, forbidden key in a located-anchor field), which B's own test list lacks (my Round 1 W3).
4. Fault injection: seal fails closed, review fails open (corrupt line, missing transcript, lock timeout) (U-012).
5. Single copy of the hook: `agent_id` skip, timed lock, seal before first delivery, replay with parallel calls (X-005).
6. Installer footprint declared as a test item: `_FRESHNESS_SCRIPTS` entry, no `hooks.json` entry, activation only via per-session settings baked by the adapter, no `src/superclaude/` path in installed text, package named `exchange/` because `.gitignore:13` is `lib/` [CODE-VERIFIED in Round 1] (U-009).

### 5. Updated assessment

#### (a) What I now concede
X-002, X-004 (level), X-005 (as evidence of under-specification), C-006 (mandatory sidecar if built), C-008 (in part), C-010, X-006 (settled by B), B-W1 (gate conflates instrument and capability, and has no owner), B-W2 (kit needs the same discipline as the transport), B-W3 (wording), B-W4 (not zero footprint), installer-cost as a decisive argument (V1 to V3).

#### (b) Updated winners and confidence on changed points

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

#### (c) Candidate resolution of the core dispute (build now versus defer)

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

### Evidence limits
- Not re-run: any E2 spike (S0 or S2 lines are recorded; transcripts for r5 not committed per B, not checked).
- Not re-verified this round: the kit +59 percent ratio, r4 143 and 90 ms, r5 and r4 luna act rates, `MR:917` and `MR:1128` quotations, r08 and r09 statements; all remain [UNVERIFIED] by me.
- [POST-BASELINE] items used only as secondary evidence: `k` counts, `OVERRIDE.md` quote, `lib/` counts at `c44c98a77`.
- Whether `make build-plugin` mirrors a new hook script automatically (V4): not read.

## Round 2 rebuttal, Advocate B (Variant 2 = Proposal B), slot C-12 collaboration-exchange-capability

Status: Complete

Tags: [CODE-VERIFIED] I read the file or ran the search this session at HEAD `50d4d2b9d`; [UNVERIFIED] taken from a research, variant or round file and not re-read; [POST-BASELINE] read only after E2 pinned tip `6c0984326cbb8fb06c4a36065de58b171d3f8175`. I read no post-baseline fact for this round. Read-only session. I did not touch the forbidden paths.

### Position after rebuttal
I concede the build-now question. At HEAD there is no launcher for my hook and adapter to run on, no family I would ship has a clean measured success, and the one existing exerciser for hooks cannot see an unregistered per-session hook. A's hybrid (A-layer now, transport built when a launcher decision, a metric of record and an owner exist, enabled only on a measured win) is close to where my own Round 1 concession already pointed. I accept it with amendments (section 3). The remaining disagreement is the order of work around slot C-07 plus four details: the trigger needs an expiry so it cannot silently never fire, the enable rule must be two-sided because "beats A2" may be undetectable at the available n, the `exchange: off` reserved key is itself a ladder question, and the F1 "portable" family is not buildable by reuse (section 1, V6).

One new fact neither paper cited: `--settings` is absent from the Python product code but present in the repo's `ccsession` shell launcher (V5). It does not rescue my build-now case; it narrows "the flag may not exist" to "no panel launcher uses it".

### 1. Facts re-verified this round
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

### 2. Response to A's Weaknesses 1 to 7
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

### 3. A's candidate hybrid, condition by condition
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

### 4. Updated points, resolution, and what I would still build now
#### 4.1 Points whose position changed (Round 1 to now)

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

#### 4.2 Resolution I think the evidence supports

1. Core now: A-layer (H1 to H4; kit catalogue behind `kit: off` until the cost per panel at n of at least 4 and the hold-out pass; brief lint for read-only lanes) plus the design note. Default-off posture for exchange stays; no hook script, `_FRESHNESS_SCRIPTS` entry, adapter, board or validator code.
2. Build trigger: C-07 adjudicated to a launcher with persistence and a per-session activation channel (named by capability), metric of record and decision rule fixed, served-model record landed, named owner and expiry. If C-07 yields no such launcher, the hook half is dropped and only F1 on swarm remains a design question for the swarm slot.
3. Enable trigger: a pre-registered two-sided gain-and-cost rule against A2, module-matched ground truth with a hold-out, all design-note preconditions green. Tasklist review is the only module with ground truth today.

#### 4.3 What I would still build now that does not depend on C-07

- **The design note, as a tracked file with binding force** on lifting `exchange: off`. Minimum content: `panel-msg/1` per-kind keys, forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, harness-authored kinds only; the harness-written sidecar keyed by reviewer id and finding id (key not named `origin`); untrusted-text rules with the adversarial-anchor test; fault-injection list (seal fails closed, review fails open); the single-copy requirements (`agent_id` skip, timed lock, seal before first delivery, parallel-call replay); package named `exchange/` (not `lib/`, `.gitignore:13` [CODE-VERIFIED in R1]); no `src/superclaude/` path in installed text; installer footprint stated as a test item (list entry, no `hooks.json` entry, activation only by the adapter's per-session channel).
- **The stricter off-state test** for the A-layer key and catalogue: no new file under `~/.claude/hooks/`, no `hooks.json` or merged-settings diff, no new run-record key when off, named installed-file-set diff. This has a consumer now.
- **The served-model and act-rate probe record** (slot C-08 if that slot owns it): it has consumers today and needs no transport.
- Not built: the validator as pure functions, the sidecar schema as code, the `collab` record. I looked for a caller and found none at HEAD (no exchange arm, no launcher), so under the ladder they are speculation; a function with only fixture callers is a second dormant surface, which is A's point and I now agree with it.

### Evidence limits

- Not re-run: any E2 spike, hook script or transcript. The S0/S2 lines, r3 `phase2_timeout` rows, the +59 percent kit ratio, `MR:917` and `MR:1128` are [UNVERIFIED] by me this round; they come from my R1 reading and A's files.
- Not read: `make build-plugin`'s implementation (V4), the profile validator for unknown-key handling (section 2, push-back 3), `ccsession`'s `compact-settings` output beyond lines 1240-1265, any post-baseline commit.
- The `--settings` search covered all of `src/superclaude` (Python, shell, markdown); no other directory (tests, docs, plugins) was searched.
- The `--resume` search covered `src/superclaude/**`; the first 40 hits were read and the `pipeline/` directory and the `--session-id`/`--continue` pattern were searched separately. A product-level `--resume` I did not classify cannot be fully excluded, but none of the files I read passes a session id to `claude`.

Status: Complete

---

## Round 2.5: Invariant Probe
Full table in `invariant-probe.md`: 16 findings (2 ADDRESSED, both LOW: INV-001, INV-012; 14 UNADDRESSED: HIGH 2 = INV-005, INV-009, MEDIUM 12). Convergence was BLOCKED by INV-005 and INV-009; MEDIUM items are warnings.

## Round 3: Final Arguments
Not executed: depth=standard.

## Scoring Matrix

Winner and confidence are the orchestrator's synthesis of the two Round 2 final positions (mean of the two advocates' stated confidences, rounded; a point is "agreed" when both advocates name the same winner or the same resolution). No advocate position was changed by the orchestrator.

| Diff Point | Winner | Confidence | Agreed | Tax. | Evidence Summary |
|------------|--------|------------|--------|------|-----------------|
| S-001 | Tie | 50% | yes | L1 | Section order is presentation only; both advocates call it a tie |
| S-002 | Tie | 50% | yes | L1 | Evidence form: both Round 2 positions moved to Tie |
| S-003 | Variant A | 57% | yes | L2 | Partition by trigger, not by build/no-build; no host at HEAD (`review-tiers.default.json:25-29`) |
| C-001 | Variant A | 63% | yes | L2 | `launch: {}`, no `--settings` in `src/superclaude/**/*.py`, swarm one-message transport (`openai_compat.py:384-388`) |
| C-002 | Unresolved (staged hybrid) | 50% | no | L2 | A 52 ("A's gate is ownerless, conflates instrument with capability") vs B "Merge 62 (trigger form)"; both endorse the trigger-form resolution but label the winner differently |
| C-003 | Variant A | 73% | yes | L2 | A specifies `kit` key, per-module cost gate; B silent; both agree kit defaults `off` until cost and hold-out pass |
| C-004 | Variant A | 70% | yes | L2 | Adapter must be separate from `ClaudeProcess` (`process.py:149-152`) and depends on open slot C-07 |
| C-005 | Variant A | 58% | yes | L2 | F1 needs no hook but no session-id path exists and swarm needs a new round-two step (B V6) |
| C-006 | Merge | 63% | yes | L2 | If built, sidecar is mandatory and harness-written; neither builds it now |
| C-007 | Merge | 61% | yes | L2 | Adopt both test lists plus the adversarial-anchor test |
| C-008 | Variant B | 57% | yes | L2 | A product-launcher repeat is still needed to bind a product decision; at pinned tip no E2 arm ran from its commit |
| C-009 | Variant A | 62% | yes | L2 | `k` 0 in most cells and a relaxed time cap argue measure first ([POST-BASELINE] paired with pinned `r5` pilot `k` 0) |
| C-010 | Variant B | 79% | yes | L3 | Validator table, forbidden keys, 600-byte cap, located-anchor and attacker-anchor analysis; to be kept as binding preconditions |
| C-011 | Variant A | 58% | yes | L3 | A's reserved key passes the stricter off-state test by construction; B's argv-diff compares new code with new code |
| C-012 | Variant A | 56% | yes | L2 | Both keep exchange off for PR review and rf-qa; A adds no lane |
| X-001 | Variant A | 63% | yes | L2 | Build the transport now: no (no launcher, no clean measured family, no exerciser) |
| X-002 | Variant B | 82% | yes | L3 | S2 `--resume` PASS for four gateway ids recorded in two packages at the pinned tip; plumbing on the E2 launcher, not benefit |
| X-003 | Variant A | 65% | yes | L3 | Main-thread-only delivery scope plus no such lane at HEAD |
| X-004 | Variant B | 62% | yes | L3 | Recorded 57 to 85 ms fits 0.1 s but over 4 to 10 calls (maxima, not a 30-call p95) |
| X-005 | Variant B | 58% | yes | L3 | r2 hook has no `agent_id` branch; shows skeleton under-specified, not a measured maintenance cost |
| X-006 | Variant A | 62% | yes | L3 | B's "registered in hooks.json" is a defect; fixed by the `launch-level-pre-push.sh` unregistered-script pattern; settled |
| X-007 | Variant A | 57% | yes | L2 | Waiting is free for the packages, not free for repeatability of the measurement |
| A-001 | QUALIFY | n/a | yes | L2 | Ground truth is tasklist review only (16 items, 3 plans, no hold-out); no ground truth for PR review or rf-qa |
| A-002 | QUALIFY | n/a | yes | L3 | Byte equality does not cover the installed-file set, hooks.json, telemetry key; add a named installed-file-set diff test |
| A-003 | QUALIFY | n/a | yes | L2 | Neither side measured retrofit or removal cost; a shipped dormant script leaves inert orphans (`install_hooks.py:40-41`) |

Winner tally (diff points, excluding the three QUALIFY assumptions): Variant A 12 (S-003, C-001, C-003, C-004, C-005, C-009, C-011, C-012, X-001, X-003, X-006, X-007); Variant B 5 (C-008, C-010, X-002, X-004, X-005); Merge 2 (C-006, C-007); Tie 2 (S-001, S-002); Unresolved 1 (C-002).

## Convergence Assessment
- Points resolved: 24 of 25 (C-002 unresolved on labelling; the three QUALIFY assumptions count as agreed because both advocates gave the same response)
- Alignment: 96% (24/25)
- Threshold: 80%
- Taxonomy coverage: L1 (S-001, S-002), L2, L3 all covered; coverage gate passed
- Invariant probe gate: BLOCKED by 2 HIGH-severity UNADDRESSED invariants (INV-005, INV-009); 12 MEDIUM warnings
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement 96% meets the threshold; the invariant gate blocks a CONVERGED declaration)
- Unresolved points: C-002; blocking invariants: INV-005, INV-009
