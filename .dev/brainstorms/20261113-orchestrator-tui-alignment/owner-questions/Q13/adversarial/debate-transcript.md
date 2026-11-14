# Adversarial Debate Transcript: Q13

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% (11 of 11 scored points have a majority)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned general-purpose sub-agents (Variant 1 persona security, Variant 2 persona backend, Variant 3 persona analyzer). No failures. Advocates were told not to run any Orca command.
- Protocol: sc-adversarial-protocol, loaded by Skill call at Q11 in this session and applied as written.
- Variant map: Variant 1 = proposal-A (yes, probe makes it safe; record both with a verdict); Variant 2 = proposal-B (no, align the observer to the sweep's rule); Variant 3 = proposal-C (no ruling; record both as facts)

## Unassigned picks
- Advocate V1: Variant 1 (would switch to Variant 2 if the owner confirms the dispatch-id comparison cannot be trusted without one binary).
- Advocate V2: Variant 2, narrowly (55 to 60 percent over Variant 1); its decisive parts are honouring `ORCA_CLI_COMMAND` and ending the silent fallback.
- Advocate V3: Variant 1, narrowly, with Variant 3's build-string detector attached.
- Result: 2 of 3 pick Variant 1; 1 of 3 picks Variant 2.

## Orchestrator spot-checks of new evidence raised in Round 1
- `src/superclaude/cli/install_user_setup.py:247-270` (re-read at question time): any probe error (`OSError`, `SubprocessError` including the 10-second timeout, bad JSON) skips to the next name, so a slow or broken `orca-ide` makes the observer use `orca` without any log. Confirmed (Advocate V2 strength 2).
- `src/superclaude/cli/issue_watch/launch.py:178-196`: the watcher skips a non-absolute `which` result, because it would run a file in the current directory; the observer's `_find_orca` has no such check. Confirmed (Advocate V1 finding; a gap in all three variants).
- `grep` of `src/superclaude/cli` outside `sweep/`: no use of `ORCA_CLI_COMMAND`. On this host the variable is unset. Confirmed (Advocates V2, V3).
- Consequence (Advocate V3 strength 5): because `orca-ide` is tried first, the observer and the sweep read different binaries only when `ORCA_CLI_COMMAND` is set, or when `orca-ide` is missing or fails its probe.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (agreed) | 95% | Same sections. |
| C-001 | L3 | 1 | 2 | 1 | Variant 1 | 65% | A verdict backed by a verified identity probe; rejecting the fallback adds no guard the probe lacks. |
| C-002 | L2 | 1 | 2 | 1,3 | Variant 1 (with 3) | 72% | No code change for a LOW, unobserved divergence (INV-016). |
| C-003 | L3 | 2 | 2 | 1 | Variant 2 | 65% | One meaning of `ORCA_CLI_COMMAND` is cleaner; Variant 1 at least documents the split. |
| C-004 | L3 | 1 | 1 | 1,3 | Variant 1 (with 3) | 85% | Keep `orca`-only hosts working. |
| C-005 | L2 | 1 | 2 | 1 | Variant 1 | 62% | Verdict plus reasons guides the next caller. |
| X-001 | L3 | 2 | 2 | 2 | Variant 2 | 90% | Unanimous: the probe proves "is Orca", not "is the same Orca". |
| X-002 | L2 | 1 | 2 | 1,3 | Variant 1 (with 3) | 68% | No divergence shown; on this host both read `orca-ide`. |
| X-003 | L2 | 2 | 2 | 3 | Variant 2 | 65% | Only Variant 2 weighs the dispatch-id comparison (XC-04); Variant 3 answers it with the build-string record. |
| A-001 | L3 | QUALIFY | ACCEPT | QUALIFY | agreed: QUALIFY | 75% | PATH trusted on a single-owner host, but the observer accepts relative `which` results. |
| A-002 | L3 | QUALIFY | QUALIFY | QUALIFY | agreed: QUALIFY | 90% | Only matters when the variable is set or `orca-ide` fails; build strings should settle it. |
| U-001 | n/a | 1 | 1 | 1 | Variant 1 (valid) | 65% | The `orca` shim exists on this host; `orca-ide`-absent Orca terminals are UNVERIFIED. |
| U-002 | n/a | 2 | 2 | 2 | Variant 2 (valid) | 70% | Binary sameness matters for XC-04. |
| U-003 | n/a | 1,3 | 3 | 3 | Variant 3 (valid) | 65% | Build-string record as the re-ask trigger. |

## Convergence Assessment
- Points resolved: 11 of 11
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 1, L2 4, L3 6; all covered
- Invariant gate: not applied (quick)
- Status: CONVERGED
- Unresolved points: none on scored points; overall pick 2 of 3 for Variant 1

## Round 1: Advocate Statements

The three statements follow verbatim.


---

### Round 1 advocate statement: Variant 1 (Proposal A)

Advocate: V1. Persona: security (vulnerabilities, attack surface). Focus: all. Depth: quick, Round 1 only.
All file:line citations below were re-read on 2026-11-14 unless marked UNVERIFIED. Paths are relative to the worktree root.

#### Position summary

Variant 1 is the best answer: the observer's bare-`orca` fallback is acceptable because every candidate must prove it is Orca before it is used, and the contract note should say so with the reason. From a security view it keeps the one guard that matters (identity proof against the GNOME screen reader), adds no new input channel, changes no merged code, and gives the next Orca caller a stated rule to copy instead of a silent gap.

#### Steelman

**Variant 2 (align the observer to the sweep).** The strongest case: two read-only programs that report on the same Orca state should read the same binary, or their reports cannot be compared with confidence (XC-03, XC-04, variant-2 lines 16-17). Dropping the bare name also removes the one case where the observer's probe itself executes a program that is probably not Orca: on a Linux host with no `orca-ide`, `_find_orca` runs `<path to orca> skills list --json` (`src/superclaude/cli/install_user_setup.py:253-264`), which per its own docstring is "usually the GNOME screen reader" (`install_user_setup.py:250-251`). Under V2 that process is never started. It also gives `ORCA_CLI_COMMAND` one meaning across both read-only programs and keeps the probe as validation, so it is not weaker than V1 on identity.

**Variant 3 (no ruling, record both).** The strongest case: INV-016 is LOW and "no host with both names was shown" (question.md fact 4), so spending an owner decision, or a PR, on a divergence never observed is waste. The note's existing rule to record the Orca build string next to each capture (ADJ line 233, as quoted in question.md fact 5; not re-read, UNVERIFIED) is a real detector, so the owner can decide later with evidence instead of now on theory. It also does not block XC-05.

#### Strengths claimed

1. **The guard is real and positive, not a name check.** `_find_orca` accepts a candidate only if it exits 0 and its JSON lists a topic named `orca-cli` (`install_user_setup.py:265-269`). A name-only rule (the sweep's `orca_binary()`, `src/superclaude/cli/sweep/probes.py:200-202`) proves nothing about what it runs; the observer's rule proves the program speaks Orca's `skills list`. The probe is bounded: `capture_output=True`, `timeout=10`, `stdin=subprocess.DEVNULL` (`install_user_setup.py:258-264`), and any parse or process error skips the candidate (`install_user_setup.py:266-267`). Accepting the observer's rule accepts the stronger of the two identity checks.
2. **No new input channel.** V1 leaves the observer ignoring `ORCA_CLI_COMMAND` (question.md fact 3; `adapter.py` imports only `_find_orca`, `src/superclaude/cli/observe/adapter.py:21,370`). An environment variable that names an executable is attack surface: whoever controls the environment picks the program run. V2 adds that channel to the observer; V1 does not.
3. **No change to merged, working code.** No regression risk to the observer or its tests, and PR #539 is untouched (variant-1 line 11). Security changes made without an observed failure (INV-016) are a source of regressions in their own right.
4. **Keeps working where `orca` is the legitimate Orca shim.** On this host `which orca` resolves to `/home/coder/.config/orca/linux-orca-cli-shim/orca` (question.md fact 6). V1 does not break orca-only hosts (diff C-004), so operators are not pushed into setting an unvalidated variable just to get the tool running.
5. **It is the only variant that gives a verdict with its reason.** A future third Orca caller reads one sentence: probe before use. That is safer guidance than V3's silence, which lets a new caller copy the unprobed name-only rule or a bare `orca` with no probe at all.
6. **Consistent with the watcher.** The watcher mirrors `_find_orca` (`src/superclaude/cli/issue_watch/launch.py:169-171,193-203`), so V1 means two of the three programs share one rule and only the sweep differs, which ADJ already notes (question.md "Spec's recommended answer").

#### Weaknesses identified in others

**Variant 2.**
- It adds `ORCA_CLI_COMMAND` as an executable selector to the observer (variant-2 line 10). The probe is kept, so a hostile value still has to answer `skills list` with an `orca-cli` topic, but the probe itself executes the value, so the variable is still a code-execution channel for whoever sets the environment. Net attack surface grows.
- It breaks orca-only hosts "until the person sets `ORCA_CLI_COMMAND`" (variant-2 line 23). The natural fix for an operator is `ORCA_CLI_COMMAND=orca`, which reintroduces the bare name by another route, so the security gain is partly illusory.
- It does not fix the gap it is closest to: the observer's `_find_orca` has no absolute-path check, unlike the watcher, which skips a non-absolute path because "the launch runs with `cwd` set to the worktree and would execute a file of that name in it" (`launch.py:177-181,195`). V2 keeps that probe as is, so a relative `PATH` entry still lets `orca-ide` resolve to a file in the current directory. (Whether the observer ever runs with a relative `PATH` entry is UNVERIFIED.)
- It does not fix build divergence within one name (A-009), which is the comparability risk it cites (variant-2 line 29).
- It costs a PR on a divergence never shown (INV-016).

**Variant 3.**
- No verdict means no rule for the next caller (variant-3 line 21). From a security view, an undocumented choice between "probe first" and "trust the name" is the worst state: the cheaper, unprobed pattern is the one people copy.
- It leaves `ORCA_CLI_COMMAND` meaning different things to two programs "unflagged as a decision" (variant-3 line 22).
- Divergence is found only after the fact (variant-3 line 23). V1 uses the same build-string detector but also states which rule is accepted.

#### Concessions

- **The probe executes the candidate.** On a Linux host with GNOME `orca` and no `orca-ide`, the observer runs the screen reader once with `skills list --json` for up to 10 seconds before rejecting it (`install_user_setup.py:253-264`). What the screen reader does with those arguments is UNVERIFIED. V2 avoids that; V1 does not.
- **The probe proves protocol, not build.** It cannot tell two Orca builds apart (A-009), and V1 says so (variant-1 line 22). V2's framing of X-001 is the more precise one.
- **V1 does not address XC-03 and XC-04.** If the shared capture and dispatch-id comparison truly require one binary, V2 has the better argument there (diff X-003, U-002).
- **The observer's `_find_orca` lacks the watcher's absolute-path guard** (`launch.py:193-196` versus `install_user_setup.py:253-256`). V1 as written does not fix it either; it is a gap in all three variants.
- Two rules stay in the codebase (variant-1 line 23).

#### Shared assumptions

| Id | Response | Reason |
|----|----------|--------|
| A-001 (PATH is trusted) | QUALIFY | Trusted only for absolute entries: the watcher already rejects non-absolute `which` results (`launch.py:195`) and the observer's `_find_orca` does not (`install_user_setup.py:254-256`), so all three variants inherit that gap. |
| A-002 (one Orca app per host) | QUALIFY | Both names exist on this host but whether they reach the same build was not checked (question.md fact 6); V1 relies on the build-string record to detect a failure of this assumption rather than assuming it holds. |

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | tie | 90% | All three use the same five sections. |
| C-001 | 1 | 70% | The fallback is gated by a positive identity probe (`install_user_setup.py:265-269`); rejecting it removes function without adding a guard the probe lacks. |
| C-002 | 1 | 60% | No change to a merged, working program for a LOW finding with no shown host (INV-016); V3 ties on this but without a verdict. |
| C-003 | 2 | 55% | One meaning of `ORCA_CLI_COMMAND` is cleaner, though it adds an executable selector to the observer; V1 at least documents the difference. |
| C-004 | 1 (tie with 3) | 75% | Keeping orca-only hosts working avoids pushing operators to set `ORCA_CLI_COMMAND=orca` unchecked. |
| C-005 | 1 | 70% | Both rules plus a verdict and reason gives the next caller a safe rule to copy. |
| X-001 | 2 | 55% | V2's "sufficient against the screen reader, not against a different Orca" is the precise statement; V1 states the same limit only as a cost. |
| X-002 | 1 | 65% | No divergence shown (INV-016); the build-string record is the cheaper detector. |
| X-003 | 2 | 70% | Only V2 addresses whether the comparison needs one binary; V1 is silent. |
| U-001 | 1 | 70% | The orca shim on this host (question.md fact 6) is a real case V2 breaks. |
| U-002 | 2 | 65% | Tying binary sameness to XC-03 and XC-04 is V2's best and most useful contribution. |
| U-003 | tie (1 and 3) | 60% | Both use the ADJ line 233 build-string rule as the detector; V1 adds a verdict on top. |

#### Overall ranking and unassigned pick

Ranking: Variant 1, then Variant 2, then Variant 3.

If I were not assigned a variant, I would still pick Variant 1, narrowly over Variant 2: it keeps the stronger identity check, adds no environment-controlled executable to the observer, and gives future callers a stated rule. I would switch to Variant 2 if the owner confirms that XC-03 and XC-04 cannot be trusted without one binary across observer and sweep. Whichever wins, the observer's missing absolute-path check (present in the watcher at `launch.py:195`) deserves its own follow-up, because none of the three variants addresses it.

---

### Round 1 advocate statement: Variant 2 (align the observer to the sweep's rule)

Persona: backend (data integrity, fault tolerance). Sources re-read 2026-11-14 in this checkout; anything not opened is marked UNVERIFIED.

#### Position summary

Variant 2 is the only answer that makes the two read-only Orca readers read the same binary, which is a data-integrity precondition for the planned observer-versus-sweep id comparison (XC-04). Its cost is one small observer PR and a breakage on `orca`-only hosts that is fixed by setting one variable.

#### Steelman

**Variant 1 (yes, the probe makes it safe; record both).** The real hazard named in the code is the GNOME screen reader, and `_find_orca` already defeats it: it accepts a candidate only if `skills list --json` exits 0 and lists a topic named `orca-cli` (`src/superclaude/cli/install_user_setup.py:247-270`, docstring at :250-251). The observer is merged and working, INV-016 found no host with both names diverging, and the fallback keeps the observer alive where only the Orca CLI shim named `orca` exists. Changing nothing and writing down the reason is the cheapest correct answer, and it gives the note a verdict rather than two unexplained rules.

**Variant 3 (no ruling; record both as facts).** The owner should not spend a decision on a divergence nobody has seen (INV-016, LOW, ADDRESSED). XC-05 can be drafted today with the two facts already stated at ADJ line 243, and the note's existing rule "record the Orca build string next to each capture" (ADJ line 233) is a ready detector: if builds ever differ, the owner decides with evidence instead of in advance. It keeps every option open at zero code cost.

#### Strengths claimed

1. **It removes the actual source of divergence, which is `ORCA_CLI_COMMAND`, not only the bare name.** The sweep honours the variable (`src/superclaude/cli/sweep/probes.py:200-202`: `os.environ.get("ORCA_CLI_COMMAND") or ORCA_BINARY_DEFAULT`); the observer's discovery is `_find_orca` (`observe/adapter.py:21`, default at `:370`), which reads only the fixed tuple `("orca-ide", "orca")` (`install_user_setup.py:36`) and never the variable (question.md fact 3; a grep of `src/superclaude/cli` finds `ORCA_CLI_COMMAND` only in `sweep/probes.py`). A person who sets the variable today silently gets two programs reading two binaries. Only Variant 2 closes that.
2. **It closes a silent fallback under fault.** `_find_orca` tries `orca-ide` first, and on a probe failure of any kind (`OSError`, `SubprocessError` including the 10-second timeout, bad JSON) it continues to the next name (`install_user_setup.py:257-267`). So a slow or briefly broken `orca-ide` makes the observer quietly read whatever `orca` is, while the sweep stays on `orca-ide`. From a data-integrity view that is the worst kind of divergence: transient, unlogged, and hard to reproduce. Variant 2 turns it into a clean "no Orca found" instead of a different Orca.
3. **It protects the comparison the plan depends on.** XC-04 compares "the observer's `dispatchId` list and a sweep's `row_id` list" on one real Run and records match, partial or mismatch (merged-requirements.md:452). If the two programs can read different binaries, a mismatch cannot be attributed to the join logic versus the binary. One rule makes the XC-04 result interpretable (diff U-002).
4. **One meaning for one variable.** After the change, `ORCA_CLI_COMMAND` means the same thing to both read-only programs (C-003), and a future third caller has one rule to copy instead of two (the gap Variant 3 admits in its "What stays unresolved").
5. **The guard is kept, not dropped.** Variant 2 keeps the `skills list --json` check on the single chosen candidate (variant-2-original.md:5), so the screen-reader protection Variant 1 values is not lost; only the second, unannounced candidate goes.
6. **Scope is bounded and honest.** It leaves the watcher alone because it starts agents and sits outside the observer-sweep contract (variant-2-original.md:11), and it names what it does not fix (A-009 build divergence within one name).

#### Weaknesses identified in others

**Variant 1.**
- Its own risk section concedes the core problem: "The observer and the sweep can still read different Orca binaries on one host" (variant-1-original.md:21). It accepts a known integrity gap and offers no detector beyond the note's build-string rule.
- Its verdict answers the wrong hazard. The probe proves "speaks Orca's `skills list`", not "is the same Orca the sweep reads" (variant-1-original.md:22, A-009 open). Diff X-001 is exactly this: sufficient against the screen reader, not against a second Orca.
- It does not address XC-03 or XC-04 at all (diff X-003), so its verdict is given without weighing the one downstream consumer that needs binary sameness.
- It does not mention the timeout fallback in strength 2 above.

**Variant 3.**
- It defers the decision to "after the fact, by comparing recorded build strings" (variant-3-original.md:23). A build string records which build was read, not which binary path; two different installs of the same build would compare equal and hide a real difference. Whether the note's capture also records the path is UNVERIFIED.
- It leaves "which rule a new caller should copy" open by design (variant-3-original.md:27), which is the guidance a contract note exists to give.
- XC-05 is the contract note; Variant 3 makes it a record of a disagreement rather than a contract.

#### Concessions

- **Fix without observed failure.** INV-016 says "no host with both names was shown"; Variant 2 changes merged, working code for a divergence not yet seen (variant-2-original.md:22).
- **The bare-name part is the weaker half.** Because `_find_orca` tries `orca-ide` first (`install_user_setup.py:36`), on a healthy host with both names the observer already reads `orca-ide`, the same default as the sweep. The bare-`orca` fallback only matters when `orca-ide` is missing or fails its probe. Most of Variant 2's value comes from honouring `ORCA_CLI_COMMAND` and from ending the silent fallback, not from banning the name as such.
- **Breakage on `orca`-only hosts.** Hosts with only the `orca` shim stop working until the person sets `ORCA_CLI_COMMAND` (variant-2-original.md:23). On this host both names exist (question.md fact 6), but how common `orca`-only hosts are is UNVERIFIED. How the observer reports "no Orca found" to its user (clear error versus empty snapshot) was not checked: UNVERIFIED.
- **Trust surface grows slightly.** Honouring an environment variable adds one more input the observer trusts (see A-001).
- **XC-03 is weaker support than XC-04.** XC-03 is a shared capture run by a session with read verbs (merged-requirements.md:451), not by observer code, so it depends on binary sameness only indirectly. XC-04 is the strong dependency.
- **A narrower hybrid exists.** Honour `ORCA_CLI_COMMAND` first, then `orca-ide`, then a probed `orca` would fix the variable divergence without breaking `orca`-only hosts. It is not one of the three variants, but it is an honest middle ground the merge step may want. It would not close the silent timeout fallback in strength 2.
- **It does not fix A-009** (build divergence within one binary name).

#### Shared assumptions

- **A-001 (PATH on the owner's host is trusted): ACCEPT.** "Single owner, single OS user, single host" is a stated contract premise (merged-requirements.md:453, XC-05 contents), so a hostile PATH is out of scope; the same premise covers the one environment variable Variant 2 adds.
- **A-002 (one Orca app per host, so two names reach the same app): QUALIFY.** Plausible on a normal host, but `which orca` and `which orca-ide` resolve to different files here (`~/.config/orca/linux-orca-cli-shim/orca` versus `~/.local/bin/orca-ide`, question.md fact 6) and sameness was not checked; a contract should not rest on an unchecked assumption when one rule removes the need for it.

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 2 | 65% | Rejecting the silent fallback removes a fault-triggered divergence; the screen-reader guard alone does not justify a second binary. |
| C-002 | 2 | 55% | A small observer change buys a consistent read path; Variants 1 and 3 save code but keep the gap. Close call given INV-016. |
| C-003 | 2 | 80% | One meaning of `ORCA_CLI_COMMAND` for both readers; only Variant 2 delivers it (`probes.py:202` versus `install_user_setup.py:36`). |
| C-004 | 1 | 70% | Variants 1 and 3 keep `orca`-only hosts working; Variant 2 breaks them until the variable is set. Variant 1 wins on stating it as a reason. |
| C-005 | 2 | 60% | A single rule for the two read-only programs is a contract; Variant 1's verdict is next best; Variant 3 gives no guidance. |
| X-001 | 2 | 75% | The probe proves "is Orca", not "is the same Orca"; Variant 1 itself concedes this (variant-1-original.md:22). |
| X-002 | 2 | 55% | The divergence is cheap to remove and costly to diagnose after XC-04 runs; but no failure has been shown, so moderate. |
| X-003 | 2 | 80% | XC-04 compares observer and sweep ids on one Run (merged-requirements.md:452); only Variant 2 addresses it. |
| U-001 | 1 | 70% | A real benefit inside Orca terminals that Variant 2 gives up. |
| U-002 | 2 | 80% | Ties binary sameness to the comparison that needs it. |
| U-003 | 3 | 55% | A usable after-the-fact detector, weakened because a build string may not distinguish two installs of one build (UNVERIFIED). |

#### Overall ranking and unassigned pick

Ranking: Variant 2, then Variant 1, then Variant 3.

Variant 1 beats Variant 3 because it at least gives the note a verdict and a reason; Variant 3 records a disagreement and leaves future callers without guidance.

Unassigned pick: I would still pick Variant 2, but narrowly, at about 55 to 60 percent over Variant 1. Its decisive parts are honouring `ORCA_CLI_COMMAND` and ending the silent fallback; the ban on the bare name by itself adds little on a healthy host. Variant 1 is the better choice if the owner weights "no change to merged code without an observed failure" above making the XC-04 result interpretable.

---

### Round 1 advocate statement: Variant 3 (no ruling; record both rules as facts)

Persona: analyzer. Paths are relative to the worktree root unless noted. "ADJ" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. "MR" is `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. "INV" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/invariant-probe.md`.

#### Position summary

Variant 3 is the answer that claims no more than the evidence supports: the adjudication itself classified the binary difference as "a note, not a risk row" (ADJ:231), the only gated item (XC-05) needs the facts and not a verdict, and the note's build-string rule (ADJ:233) is the detector that would turn a future verdict into an evidence-based one. It spends no code, no PR and no owner decision on a divergence nobody has observed.

#### Steelman

**Variant 1 (yes, the probe makes the fallback safe).** At its strongest, Variant 1 is the spec's own recommended answer (MR:540; ADJ:783), it gives the note a verdict instead of two bare facts, and it is grounded in code: `_find_orca` accepts a candidate only when `skills list --json` exits 0 and lists a topic named `orca-cli` (`src/superclaude/cli/install_user_setup.py:247-270`, re-read this round), which defeats the GNOME screen-reader collision the docstring names (`:250-251`). It changes no code, keeps orca-only hosts working, and is honest about its residual risk (Variant 1 "What it costs or risks": the probe proves Orca, not which build).

**Variant 2 (no, align the observer to the sweep).** At its strongest, Variant 2 is the only variant that makes "which Orca did we read" a single answer for both read-only programs, so the planned shared capture (XC-03) and the JOIN record (XC-04) compare like with like (MR:986 lists both as records that carry a build string). It gives `ORCA_CLI_COMMAND` one meaning; today the sweep honours it (`src/superclaude/cli/sweep/probes.py:200-202`) and the observer does not (no reference to it in `src/superclaude/cli/observe/adapter.py`; the only Orca lookup there is the `_find_orca` import at `:21` used at `:370`). It keeps the probe as a check, so it loses no safety.

#### Strengths claimed

1. **It matches the adjudicated severity.** ADJ:231 states "no host with both names was shown, so a note, not a risk row", and INV:23 rates INV-016 ADDRESSED, LOW. A note is exactly what Variant 3 produces. Variants 1 and 2 both escalate a LOW, ADDRESSED item into a ruling.
2. **It does not hold XC-05.** XC-05's listed content is "binary resolution (Q13)" (question.md fact, MR:453). The binary-resolution row already exists verbatim in ADJ:243 (observer "`orca-ide` then `orca`, accepted only if `skills list --json` names `orca-cli`"; sweep "`$ORCA_CLI_COMMAND` else `orca-ide`, never bare `orca`"). Variant 3 copies it and drafts now.
3. **It is the documented default.** MR:540 names "the note records both rules without a verdict" as the default if unanswered. Choosing Variant 3 means the plan proceeds on its own stated fallback with no new inference.
4. **It names a concrete detector instead of a judgment.** The build-string rule "Record the Orca build string next to each capture" (ADJ:233) and MR:986 (recorded at OB-05, SW-08, WA-04, XC-03, OB-03, XC-04) is the evidence that would show divergence. This is the only variant that ties the re-ask trigger to a recorded fact (diff U-003).
5. **The real divergence surface is narrower than Variants 1 and 2 imply, which favours not ruling.** `_ORCA_CLIS = ("orca-ide", "orca")` (`install_user_setup.py:36`, checked this round), so the observer reaches bare `orca` only when `orca-ide` is missing or fails the probe. In that case the sweep, with no `ORCA_CLI_COMMAND`, would call `orca-ide` and fail, so the two programs do not "read different binaries"; one simply does not run. A true split needs `ORCA_CLI_COMMAND` set to something other than what `_find_orca` picks. On this host `which orca` is `/home/coder/.config/orca/linux-orca-cli-shim/orca`, `which orca-ide` is `/home/coder/.local/bin/orca-ide`, and `ORCA_CLI_COMMAND` is unset (checked this round), so both programs read `orca-ide` here. A ruling now would be a ruling on a case with no instance.
6. **No code, no PR, no breakage.** Same as Variant 1 and unlike Variant 2, it leaves orca-only hosts working (diff C-004).

#### Weaknesses identified in others

**Variant 1.**
- Its verdict "accepted" rests on the probe, but its own costs section concedes the probe "proves the program speaks Orca's `skills list`, not which Orca build it is" (A-009 open, ADJ:141). So the "yes" answers the screen-reader question, not the question X-001 actually asks (whether the observer and sweep read the same Orca). It asserts more than it proves.
- U-001 ("inside Orca terminals `orca` is the Orca CLI shim and `orca-ide` may or may not be present") is only half verified: the shim path on this host supports the first half; the claim that `orca-ide` is sometimes absent inside Orca terminals is UNVERIFIED in any cited source. And because `orca-ide` is tried first (`install_user_setup.py:36`), the fallback only matters on such a host.
- "Both are accepted" fixes a rule a future third caller will copy, before the build-string records exist to test it.

**Variant 2.**
- It changes merged, working code and tests for a divergence ADJ:231 and INV:23 rate LOW and unobserved. Its own costs section says so.
- It breaks orca-only hosts until the person sets `ORCA_CLI_COMMAND` (its own cost line; diff C-004).
- It does not fix the stated motive. Its own "What stays unresolved" admits build divergence within one name (A-009) is not fixed. Strength 5 above shows the two programs already read the same binary unless `ORCA_CLI_COMMAND` is set, so the code change buys protection against one env-var case.
- It splits the observer from the watcher, which it leaves on `_find_orca`. ADJ:783 says "The watcher uses the same rule, so only the sweep differs"; Variant 2 converts one difference into two.
- Its PR #539 queue claim and the "owner's grant row" process are UNVERIFIED here (no `gh` calls were made).

#### Concessions

- Variant 3 gives no guidance to a future third Orca caller (its own costs section). That is a real gap; Variant 1 fills it.
- It leaves `ORCA_CLI_COMMAND` meaning different things to the two programs without flagging that as a decision (its own costs section; diff C-003).
- Its detector needs work that does not exist yet: the observer records no Orca version today (ADJ:141, E-15). Until OB-05 and XC-03 record build strings (MR:986), divergence is not observable at all, so "re-ask if seen" is weak in the near term.
- Its trigger wording ("a host where the two programs read different Orca binaries or builds") is softer than it looks: question.md fact 6 shows this host now has both names, which supersedes ADJ:231's "no host with both names was shown". The two names resolve to different paths here; whether they reach the same Orca app and build was not checked (question.md fact 6; not checked by me either, since I ran no Orca command).
- The spec recommended "Yes" (MR:540; ADJ:783). Variant 3 is the fallback, not the recommendation.

#### Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 (PATH is trusted) | QUALIFY | Acceptable for the owner's own host, and the sweep relies on PATH for `orca-ide` too; but the watcher adds an absolute-path check (`src/superclaude/cli/issue_watch/launch.py:178` docstring) that `_find_orca` lacks, so the note should say the observer accepts a relative `which` result. |
| A-002 (one Orca app per host) | QUALIFY | It only matters when `ORCA_CLI_COMMAND` is set or `orca-ide` is missing, because `_find_orca` tries `orca-ide` first (`install_user_setup.py:36`); on this host the two names are different files and their sameness is UNVERIFIED, which is exactly what the build-string record should settle. |

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 1 | 60% | A verdict backed by a verified probe and the spec's recommendation beats none; Variant 3's "no verdict" is defensible only because the case is unobserved. |
| C-002 | 1 and 3 (tie) | 80% | No code change for a LOW, ADDRESSED, unobserved divergence (ADJ:231; INV:23). |
| C-003 | 1 | 55% | Documenting the `ORCA_CLI_COMMAND` split as an accepted decision beats leaving it as an unflagged fact; Variant 2 unifies it but at code cost for one env-var case. |
| C-004 | 1 and 3 (tie) | 85% | Both keep orca-only hosts working; Variant 2 breaks them until the variable is set. |
| C-005 | 1 | 55% | Verdict plus reasons serves a future reader better; Variant 3 is safer only if the owner wants to wait for build-string evidence. |
| X-001 | 2 | 60% | Variant 2 states the probe's limit most precisely (sufficient against the screen reader, not against a different Orca); Variant 1 concedes the same in its costs; Variant 3 does not judge. |
| X-002 | 1 and 3 (tie) | 75% | No divergence has been shown; on this host both programs read `orca-ide` with the variable unset. |
| X-003 | 3 | 50% | Variant 2 raises the real need, but recording the build string at XC-03 and XC-04 (MR:986; ADJ:233) meets it without code; low confidence because that recording is not built yet. |
| U-001 | 1 | 55% | Useful but only half verified; matters only where `orca-ide` is absent. |
| U-002 | 2 | 60% | Correctly links binary sameness to XC-03 and XC-04, the highest-value contribution in the set. |
| U-003 | 3 | 70% | The only variant that names a recorded fact as the trigger for revisiting. |

#### Overall ranking and unassigned pick

Ranking as Variant 3's advocate: 3, 1, 2. Variant 3 and Variant 1 share every material effect (no code, orca-only hosts work, same note row); they differ only in whether the note carries the word "accepted". Variant 2 costs a code change and breaks a host class to close a gap that, by the name order in `_find_orca`, exists only when `ORCA_CLI_COMMAND` is set.

Unassigned pick: Variant 1, narrowly. It is the spec's recommendation (MR:540; ADJ:783), it has every practical benefit of Variant 3, and it answers the "which rule should a new caller copy" gap that Variant 3 leaves open. The best final answer would be Variant 1 with Variant 3's detector attached: accept the observer's rule, record both rules with reasons, record the Orca build string at each capture, and re-ask only if those strings diverge or `ORCA_CLI_COMMAND` is in use.
