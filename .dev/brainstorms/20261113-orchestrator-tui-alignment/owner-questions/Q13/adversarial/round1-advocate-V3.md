# Round 1 advocate statement: Variant 3 (no ruling; record both rules as facts)

Persona: analyzer. Paths are relative to the worktree root unless noted. "ADJ" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. "MR" is `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. "INV" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/invariant-probe.md`.

## Position summary

Variant 3 is the answer that claims no more than the evidence supports: the adjudication itself classified the binary difference as "a note, not a risk row" (ADJ:231), the only gated item (XC-05) needs the facts and not a verdict, and the note's build-string rule (ADJ:233) is the detector that would turn a future verdict into an evidence-based one. It spends no code, no PR and no owner decision on a divergence nobody has observed.

## Steelman

**Variant 1 (yes, the probe makes the fallback safe).** At its strongest, Variant 1 is the spec's own recommended answer (MR:540; ADJ:783), it gives the note a verdict instead of two bare facts, and it is grounded in code: `_find_orca` accepts a candidate only when `skills list --json` exits 0 and lists a topic named `orca-cli` (`src/superclaude/cli/install_user_setup.py:247-270`, re-read this round), which defeats the GNOME screen-reader collision the docstring names (`:250-251`). It changes no code, keeps orca-only hosts working, and is honest about its residual risk (Variant 1 "What it costs or risks": the probe proves Orca, not which build).

**Variant 2 (no, align the observer to the sweep).** At its strongest, Variant 2 is the only variant that makes "which Orca did we read" a single answer for both read-only programs, so the planned shared capture (XC-03) and the JOIN record (XC-04) compare like with like (MR:986 lists both as records that carry a build string). It gives `ORCA_CLI_COMMAND` one meaning; today the sweep honours it (`src/superclaude/cli/sweep/probes.py:200-202`) and the observer does not (no reference to it in `src/superclaude/cli/observe/adapter.py`; the only Orca lookup there is the `_find_orca` import at `:21` used at `:370`). It keeps the probe as a check, so it loses no safety.

## Strengths claimed

1. **It matches the adjudicated severity.** ADJ:231 states "no host with both names was shown, so a note, not a risk row", and INV:23 rates INV-016 ADDRESSED, LOW. A note is exactly what Variant 3 produces. Variants 1 and 2 both escalate a LOW, ADDRESSED item into a ruling.
2. **It does not hold XC-05.** XC-05's listed content is "binary resolution (Q13)" (question.md fact, MR:453). The binary-resolution row already exists verbatim in ADJ:243 (observer "`orca-ide` then `orca`, accepted only if `skills list --json` names `orca-cli`"; sweep "`$ORCA_CLI_COMMAND` else `orca-ide`, never bare `orca`"). Variant 3 copies it and drafts now.
3. **It is the documented default.** MR:540 names "the note records both rules without a verdict" as the default if unanswered. Choosing Variant 3 means the plan proceeds on its own stated fallback with no new inference.
4. **It names a concrete detector instead of a judgment.** The build-string rule "Record the Orca build string next to each capture" (ADJ:233) and MR:986 (recorded at OB-05, SW-08, WA-04, XC-03, OB-03, XC-04) is the evidence that would show divergence. This is the only variant that ties the re-ask trigger to a recorded fact (diff U-003).
5. **The real divergence surface is narrower than Variants 1 and 2 imply, which favours not ruling.** `_ORCA_CLIS = ("orca-ide", "orca")` (`install_user_setup.py:36`, checked this round), so the observer reaches bare `orca` only when `orca-ide` is missing or fails the probe. In that case the sweep, with no `ORCA_CLI_COMMAND`, would call `orca-ide` and fail, so the two programs do not "read different binaries"; one simply does not run. A true split needs `ORCA_CLI_COMMAND` set to something other than what `_find_orca` picks. On this host `which orca` is `/home/coder/.config/orca/linux-orca-cli-shim/orca`, `which orca-ide` is `/home/coder/.local/bin/orca-ide`, and `ORCA_CLI_COMMAND` is unset (checked this round), so both programs read `orca-ide` here. A ruling now would be a ruling on a case with no instance.
6. **No code, no PR, no breakage.** Same as Variant 1 and unlike Variant 2, it leaves orca-only hosts working (diff C-004).

## Weaknesses identified in others

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

## Concessions

- Variant 3 gives no guidance to a future third Orca caller (its own costs section). That is a real gap; Variant 1 fills it.
- It leaves `ORCA_CLI_COMMAND` meaning different things to the two programs without flagging that as a decision (its own costs section; diff C-003).
- Its detector needs work that does not exist yet: the observer records no Orca version today (ADJ:141, E-15). Until OB-05 and XC-03 record build strings (MR:986), divergence is not observable at all, so "re-ask if seen" is weak in the near term.
- Its trigger wording ("a host where the two programs read different Orca binaries or builds") is softer than it looks: question.md fact 6 shows this host now has both names, which supersedes ADJ:231's "no host with both names was shown". The two names resolve to different paths here; whether they reach the same Orca app and build was not checked (question.md fact 6; not checked by me either, since I ran no Orca command).
- The spec recommended "Yes" (MR:540; ADJ:783). Variant 3 is the fallback, not the recommendation.

## Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 (PATH is trusted) | QUALIFY | Acceptable for the owner's own host, and the sweep relies on PATH for `orca-ide` too; but the watcher adds an absolute-path check (`src/superclaude/cli/issue_watch/launch.py:178` docstring) that `_find_orca` lacks, so the note should say the observer accepts a relative `which` result. |
| A-002 (one Orca app per host) | QUALIFY | It only matters when `ORCA_CLI_COMMAND` is set or `orca-ide` is missing, because `_find_orca` tries `orca-ide` first (`install_user_setup.py:36`); on this host the two names are different files and their sameness is UNVERIFIED, which is exactly what the build-string record should settle. |

## Per-point verdicts

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

## Overall ranking and unassigned pick

Ranking as Variant 3's advocate: 3, 1, 2. Variant 3 and Variant 1 share every material effect (no code, orca-only hosts work, same note row); they differ only in whether the note carries the word "accepted". Variant 2 costs a code change and breaks a host class to close a gap that, by the name order in `_find_orca`, exists only when `ORCA_CLI_COMMAND` is set.

Unassigned pick: Variant 1, narrowly. It is the spec's recommendation (MR:540; ADJ:783), it has every practical benefit of Variant 3, and it answers the "which rule should a new caller copy" gap that Variant 3 leaves open. The best final answer would be Variant 1 with Variant 3's detector attached: accept the observer's rule, record both rules with reasons, record the Orca build string at each capture, and re-ask only if those strings diverge or `ORCA_CLI_COMMAND` is in use.
