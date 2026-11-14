# Round 1 advocate statement: Variant 1 (Proposal A)

Advocate: V1. Persona: security (vulnerabilities, attack surface). Focus: all. Depth: quick, Round 1 only.
All file:line citations below were re-read on 2026-11-14 unless marked UNVERIFIED. Paths are relative to the worktree root.

## Position summary

Variant 1 is the best answer: the observer's bare-`orca` fallback is acceptable because every candidate must prove it is Orca before it is used, and the contract note should say so with the reason. From a security view it keeps the one guard that matters (identity proof against the GNOME screen reader), adds no new input channel, changes no merged code, and gives the next Orca caller a stated rule to copy instead of a silent gap.

## Steelman

**Variant 2 (align the observer to the sweep).** The strongest case: two read-only programs that report on the same Orca state should read the same binary, or their reports cannot be compared with confidence (XC-03, XC-04, variant-2 lines 16-17). Dropping the bare name also removes the one case where the observer's probe itself executes a program that is probably not Orca: on a Linux host with no `orca-ide`, `_find_orca` runs `<path to orca> skills list --json` (`src/superclaude/cli/install_user_setup.py:253-264`), which per its own docstring is "usually the GNOME screen reader" (`install_user_setup.py:250-251`). Under V2 that process is never started. It also gives `ORCA_CLI_COMMAND` one meaning across both read-only programs and keeps the probe as validation, so it is not weaker than V1 on identity.

**Variant 3 (no ruling, record both).** The strongest case: INV-016 is LOW and "no host with both names was shown" (question.md fact 4), so spending an owner decision, or a PR, on a divergence never observed is waste. The note's existing rule to record the Orca build string next to each capture (ADJ line 233, as quoted in question.md fact 5; not re-read, UNVERIFIED) is a real detector, so the owner can decide later with evidence instead of now on theory. It also does not block XC-05.

## Strengths claimed

1. **The guard is real and positive, not a name check.** `_find_orca` accepts a candidate only if it exits 0 and its JSON lists a topic named `orca-cli` (`install_user_setup.py:265-269`). A name-only rule (the sweep's `orca_binary()`, `src/superclaude/cli/sweep/probes.py:200-202`) proves nothing about what it runs; the observer's rule proves the program speaks Orca's `skills list`. The probe is bounded: `capture_output=True`, `timeout=10`, `stdin=subprocess.DEVNULL` (`install_user_setup.py:258-264`), and any parse or process error skips the candidate (`install_user_setup.py:266-267`). Accepting the observer's rule accepts the stronger of the two identity checks.
2. **No new input channel.** V1 leaves the observer ignoring `ORCA_CLI_COMMAND` (question.md fact 3; `adapter.py` imports only `_find_orca`, `src/superclaude/cli/observe/adapter.py:21,370`). An environment variable that names an executable is attack surface: whoever controls the environment picks the program run. V2 adds that channel to the observer; V1 does not.
3. **No change to merged, working code.** No regression risk to the observer or its tests, and PR #539 is untouched (variant-1 line 11). Security changes made without an observed failure (INV-016) are a source of regressions in their own right.
4. **Keeps working where `orca` is the legitimate Orca shim.** On this host `which orca` resolves to `/home/coder/.config/orca/linux-orca-cli-shim/orca` (question.md fact 6). V1 does not break orca-only hosts (diff C-004), so operators are not pushed into setting an unvalidated variable just to get the tool running.
5. **It is the only variant that gives a verdict with its reason.** A future third Orca caller reads one sentence: probe before use. That is safer guidance than V3's silence, which lets a new caller copy the unprobed name-only rule or a bare `orca` with no probe at all.
6. **Consistent with the watcher.** The watcher mirrors `_find_orca` (`src/superclaude/cli/issue_watch/launch.py:169-171,193-203`), so V1 means two of the three programs share one rule and only the sweep differs, which ADJ already notes (question.md "Spec's recommended answer").

## Weaknesses identified in others

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

## Concessions

- **The probe executes the candidate.** On a Linux host with GNOME `orca` and no `orca-ide`, the observer runs the screen reader once with `skills list --json` for up to 10 seconds before rejecting it (`install_user_setup.py:253-264`). What the screen reader does with those arguments is UNVERIFIED. V2 avoids that; V1 does not.
- **The probe proves protocol, not build.** It cannot tell two Orca builds apart (A-009), and V1 says so (variant-1 line 22). V2's framing of X-001 is the more precise one.
- **V1 does not address XC-03 and XC-04.** If the shared capture and dispatch-id comparison truly require one binary, V2 has the better argument there (diff X-003, U-002).
- **The observer's `_find_orca` lacks the watcher's absolute-path guard** (`launch.py:193-196` versus `install_user_setup.py:253-256`). V1 as written does not fix it either; it is a gap in all three variants.
- Two rules stay in the codebase (variant-1 line 23).

## Shared assumptions

| Id | Response | Reason |
|----|----------|--------|
| A-001 (PATH is trusted) | QUALIFY | Trusted only for absolute entries: the watcher already rejects non-absolute `which` results (`launch.py:195`) and the observer's `_find_orca` does not (`install_user_setup.py:254-256`), so all three variants inherit that gap. |
| A-002 (one Orca app per host) | QUALIFY | Both names exist on this host but whether they reach the same build was not checked (question.md fact 6); V1 relies on the build-string record to detect a failure of this assumption rather than assuming it holds. |

## Per-point verdicts

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

## Overall ranking and unassigned pick

Ranking: Variant 1, then Variant 2, then Variant 3.

If I were not assigned a variant, I would still pick Variant 1, narrowly over Variant 2: it keeps the stronger identity check, adds no environment-controlled executable to the observer, and gives future callers a stated rule. I would switch to Variant 2 if the owner confirms that XC-03 and XC-04 cannot be trusted without one binary across observer and sweep. Whichever wins, the observer's missing absolute-path check (present in the watcher at `launch.py:195`) deserves its own follow-up, because none of the three variants addresses it.
