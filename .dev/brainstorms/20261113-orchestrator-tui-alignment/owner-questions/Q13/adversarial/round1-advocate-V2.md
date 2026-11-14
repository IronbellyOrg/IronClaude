# Round 1 advocate statement: Variant 2 (align the observer to the sweep's rule)

Persona: backend (data integrity, fault tolerance). Sources re-read 2026-11-14 in this checkout; anything not opened is marked UNVERIFIED.

## Position summary

Variant 2 is the only answer that makes the two read-only Orca readers read the same binary, which is a data-integrity precondition for the planned observer-versus-sweep id comparison (XC-04). Its cost is one small observer PR and a breakage on `orca`-only hosts that is fixed by setting one variable.

## Steelman

**Variant 1 (yes, the probe makes it safe; record both).** The real hazard named in the code is the GNOME screen reader, and `_find_orca` already defeats it: it accepts a candidate only if `skills list --json` exits 0 and lists a topic named `orca-cli` (`src/superclaude/cli/install_user_setup.py:247-270`, docstring at :250-251). The observer is merged and working, INV-016 found no host with both names diverging, and the fallback keeps the observer alive where only the Orca CLI shim named `orca` exists. Changing nothing and writing down the reason is the cheapest correct answer, and it gives the note a verdict rather than two unexplained rules.

**Variant 3 (no ruling; record both as facts).** The owner should not spend a decision on a divergence nobody has seen (INV-016, LOW, ADDRESSED). XC-05 can be drafted today with the two facts already stated at ADJ line 243, and the note's existing rule "record the Orca build string next to each capture" (ADJ line 233) is a ready detector: if builds ever differ, the owner decides with evidence instead of in advance. It keeps every option open at zero code cost.

## Strengths claimed

1. **It removes the actual source of divergence, which is `ORCA_CLI_COMMAND`, not only the bare name.** The sweep honours the variable (`src/superclaude/cli/sweep/probes.py:200-202`: `os.environ.get("ORCA_CLI_COMMAND") or ORCA_BINARY_DEFAULT`); the observer's discovery is `_find_orca` (`observe/adapter.py:21`, default at `:370`), which reads only the fixed tuple `("orca-ide", "orca")` (`install_user_setup.py:36`) and never the variable (question.md fact 3; a grep of `src/superclaude/cli` finds `ORCA_CLI_COMMAND` only in `sweep/probes.py`). A person who sets the variable today silently gets two programs reading two binaries. Only Variant 2 closes that.
2. **It closes a silent fallback under fault.** `_find_orca` tries `orca-ide` first, and on a probe failure of any kind (`OSError`, `SubprocessError` including the 10-second timeout, bad JSON) it continues to the next name (`install_user_setup.py:257-267`). So a slow or briefly broken `orca-ide` makes the observer quietly read whatever `orca` is, while the sweep stays on `orca-ide`. From a data-integrity view that is the worst kind of divergence: transient, unlogged, and hard to reproduce. Variant 2 turns it into a clean "no Orca found" instead of a different Orca.
3. **It protects the comparison the plan depends on.** XC-04 compares "the observer's `dispatchId` list and a sweep's `row_id` list" on one real Run and records match, partial or mismatch (merged-requirements.md:452). If the two programs can read different binaries, a mismatch cannot be attributed to the join logic versus the binary. One rule makes the XC-04 result interpretable (diff U-002).
4. **One meaning for one variable.** After the change, `ORCA_CLI_COMMAND` means the same thing to both read-only programs (C-003), and a future third caller has one rule to copy instead of two (the gap Variant 3 admits in its "What stays unresolved").
5. **The guard is kept, not dropped.** Variant 2 keeps the `skills list --json` check on the single chosen candidate (variant-2-original.md:5), so the screen-reader protection Variant 1 values is not lost; only the second, unannounced candidate goes.
6. **Scope is bounded and honest.** It leaves the watcher alone because it starts agents and sits outside the observer-sweep contract (variant-2-original.md:11), and it names what it does not fix (A-009 build divergence within one name).

## Weaknesses identified in others

**Variant 1.**
- Its own risk section concedes the core problem: "The observer and the sweep can still read different Orca binaries on one host" (variant-1-original.md:21). It accepts a known integrity gap and offers no detector beyond the note's build-string rule.
- Its verdict answers the wrong hazard. The probe proves "speaks Orca's `skills list`", not "is the same Orca the sweep reads" (variant-1-original.md:22, A-009 open). Diff X-001 is exactly this: sufficient against the screen reader, not against a second Orca.
- It does not address XC-03 or XC-04 at all (diff X-003), so its verdict is given without weighing the one downstream consumer that needs binary sameness.
- It does not mention the timeout fallback in strength 2 above.

**Variant 3.**
- It defers the decision to "after the fact, by comparing recorded build strings" (variant-3-original.md:23). A build string records which build was read, not which binary path; two different installs of the same build would compare equal and hide a real difference. Whether the note's capture also records the path is UNVERIFIED.
- It leaves "which rule a new caller should copy" open by design (variant-3-original.md:27), which is the guidance a contract note exists to give.
- XC-05 is the contract note; Variant 3 makes it a record of a disagreement rather than a contract.

## Concessions

- **Fix without observed failure.** INV-016 says "no host with both names was shown"; Variant 2 changes merged, working code for a divergence not yet seen (variant-2-original.md:22).
- **The bare-name part is the weaker half.** Because `_find_orca` tries `orca-ide` first (`install_user_setup.py:36`), on a healthy host with both names the observer already reads `orca-ide`, the same default as the sweep. The bare-`orca` fallback only matters when `orca-ide` is missing or fails its probe. Most of Variant 2's value comes from honouring `ORCA_CLI_COMMAND` and from ending the silent fallback, not from banning the name as such.
- **Breakage on `orca`-only hosts.** Hosts with only the `orca` shim stop working until the person sets `ORCA_CLI_COMMAND` (variant-2-original.md:23). On this host both names exist (question.md fact 6), but how common `orca`-only hosts are is UNVERIFIED. How the observer reports "no Orca found" to its user (clear error versus empty snapshot) was not checked: UNVERIFIED.
- **Trust surface grows slightly.** Honouring an environment variable adds one more input the observer trusts (see A-001).
- **XC-03 is weaker support than XC-04.** XC-03 is a shared capture run by a session with read verbs (merged-requirements.md:451), not by observer code, so it depends on binary sameness only indirectly. XC-04 is the strong dependency.
- **A narrower hybrid exists.** Honour `ORCA_CLI_COMMAND` first, then `orca-ide`, then a probed `orca` would fix the variable divergence without breaking `orca`-only hosts. It is not one of the three variants, but it is an honest middle ground the merge step may want. It would not close the silent timeout fallback in strength 2.
- **It does not fix A-009** (build divergence within one binary name).

## Shared assumptions

- **A-001 (PATH on the owner's host is trusted): ACCEPT.** "Single owner, single OS user, single host" is a stated contract premise (merged-requirements.md:453, XC-05 contents), so a hostile PATH is out of scope; the same premise covers the one environment variable Variant 2 adds.
- **A-002 (one Orca app per host, so two names reach the same app): QUALIFY.** Plausible on a normal host, but `which orca` and `which orca-ide` resolve to different files here (`~/.config/orca/linux-orca-cli-shim/orca` versus `~/.local/bin/orca-ide`, question.md fact 6) and sameness was not checked; a contract should not rest on an unchecked assumption when one rule removes the need for it.

## Per-point verdicts

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

## Overall ranking and unassigned pick

Ranking: Variant 2, then Variant 1, then Variant 3.

Variant 1 beats Variant 3 because it at least gives the note a verdict and a reason; Variant 3 records a disagreement and leaves future callers without guidance.

Unassigned pick: I would still pick Variant 2, but narrowly, at about 55 to 60 percent over Variant 1. Its decisive parts are honouring `ORCA_CLI_COMMAND` and ending the silent fallback; the ban on the bare name by itself adds little on a healthy host. Variant 1 is the better choice if the owner weights "no change to merged code without an observed failure" above making the XC-04 result interpretable.
