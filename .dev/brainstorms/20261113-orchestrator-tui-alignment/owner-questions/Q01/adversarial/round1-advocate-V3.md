# Round 1 advocate statement: Variant 3 (proposal C, accept the risk with caveats, no code change)

Persona: architect (structure, dependencies, long-term impact). Mode A, depth quick, Round 1.
Sources opened for this statement: `../question.md`; the three variant files; `diff-analysis.md`; `merged-requirements.md` (lines 28-35, 190-194, 452, 528, 560-575, 881-889); ADJ `alignment-findings-adjudicated.md` (lines 134, 137, 206, 456, 460, 469, 771, 817); `invariant-probe.md` (lines 12, 19, 26); `SECURITY.md:166-170`; `src/superclaude/core/HOW-WE-WORK.md:335,406`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md:3,15`.

## Position summary

Variant 3 is the only answer that leaves the system's structure untouched: no edit to the owner-signed one-entry allow-list (NFR-014), no re-cut of the shared `paths` list (INV-039), no change to three pinned tests (INV-009), and it makes every "read-only" claim honest in the same PR. Its premise (one owner, one host, every session already permission-free, a clone cannot ship config) is the most completely stated of the three. Its cost is real and I state it plainly: it leaves the JOIN lane (XC-04) structurally blocked, because the spec forbids running the unfixed sweep for it.

## Steelman

### Variant 1 (accept now, fix in a tracked follow-up with a hard trigger)

Strongest version: Variant 1 separates two concerns that the spec itself separates (SW-01 ruling versus SW-02 implementation, `merged-requirements.md:33`): it keeps a security-sensitive allow-list change out of a 1003-file PR so it gets its own focused review (ADJ line 134, E-08), and it still commits the program to closing the hole before the events that change the risk (XC-04, any unattended or scheduled sweep, a second user or host). It gets V3's merge speed without V3's dead end on XC-04. That is a genuinely better dependency shape than mine for the JOIN lane.

Critique: (1) Its own trigger may already be met at merge. `HOW-WE-WORK.md:406` makes the coordinator run `/sc:sweep` "on every wake, at most once every 5 minutes"; a coordinator wake loop is a scheduled sweep in all but name, so "before any unattended or scheduled sweep" arguably means "before merge", which collapses V1 into V2 with an extra round of edits (interpretation; whether a coordinator wake counts as "scheduled" is not defined in the sources). (2) It touches the same 16-plus texts twice (V1 "Costs": "caveat now, un-caveat later"), one of them a mirror that must stay byte-equal (`invariant-probe.md:19`). (3) Its trigger is "a promise in a table, not a mechanical gate" (V1's own words); V3's void conditions are the same kind of promise but there is only one artifact to keep true, not two.

### Variant 2 (fix before merge, neutralise or refuse, cover every channel)

Strongest version: Variant 2 matches the spec's own recommended answer (F1 or F2, about 70 percent, `merged-requirements.md:528`; ADJ line 771) and is the only variant under which every downstream node, including XC-04, unblocks on master code (`merged-requirements.md:452` (4), `:889`). It makes the 16-plus claims true rather than qualified, and a fix is reversible where an acceptance is not after merge (SW-01 undo column, `merged-requirements.md:190`). Its "names any channel it deliberately leaves out" clause (U-005) is the best answer to A-001. Of the three it leaves the cleanest long-term contract for the v2 layer and every future reader.

Critique: (1) Structural blast radius inside the merge: an edit to an exact one-entry allow-list under owner signature (`probes.py:64-67`, NFR-014), three pinned tests (`test_probes_allowlist.py:503`, `test_readonly.py:85,156,453`, INV-009), and a separation of the git-status scope from the shared `paths` that also feeds the contract allow-list and transcript scans (`probes.py:1255-1263`, `:1301`, INV-039, ADJ line 469), all inside a 1003-file PR (E-08). (2) Its next-step list never states the premise the ruling relies on, which SW-01 (2) requires of every ruling (`merged-requirements.md:190`: "The ruling states which premise it relies on (`SECURITY.md:L166-L170` versus INV-011 ...)"). (3) The neutralise route "depends on git honouring every override" (V2's own words) and the measured fact that `-c core.fsmonitor=false` left the clean filter running (ADJ line 206) shows how easy it is to believe a hole is closed when it is not; a fix that misses a channel still prints "read-only" with no caveat, which is a worse failure mode than an honest caveat (`merged-requirements.md:1153`).

## Strengths claimed

1. **No change to owner-signed structure.** F3 requires no edit to `ALLOWED_GIT`, the exact one-entry allow-list under NFR-014 (ADJ line 206; `merged-requirements.md:571`: "Q1's risk choice does not authorize arbitrary git allow-list edits"). It avoids the three pinned-test edits (INV-009, ADJ line 460) and the `paths` separation that would change pinned `worktrees[]` and `sources[]` rows (INV-039, ADJ line 469). From an architecture view these are coupled invariants; V3 is the only answer that disturbs none of them.
2. **Most complete premise, as SW-01 (2) requires.** V3 names one owner, one OS user, one host; that "a clone cannot ship config, and a `.gitattributes` file alone ran nothing" (`question.md:32`); and that every launched session already runs with permission checks off (ADJ line 137, E-11: "`--dangerously-skip-permissions`"). V1 names a subset; V2 names none.
3. **Honest claims immediately, in one pass.** Every grep-found "read-only" or "changes nothing" statement gets a caveat in the same PR (SW-02 F3 branch, `merged-requirements.md:191`), at least 16 locations (`invariant-probe.md:19`), with the mirror kept byte-equal. Today `HOW-WE-WORK.md:335` says "it changes nothing else" and `sc-sweep-protocol/SKILL.md:3` says "changes nothing"; under V3 those become true-as-qualified on the day of merge, and there is no second pass to forget.
4. **Self-describing expiry (U-004).** The ledger row carries the condition that voids the acceptance (second user, second host, untrusted config). That turns a silent assumption (A-004 in diff-analysis) into a recorded, checkable one, which the spec's decision-lifetime rule then enforces ("A changed answer voids the unsent drafts ...", `merged-requirements.md:566`).
5. **Smallest author workload while Q33 is open.** Text edits only; no test design (SW-02 (1)-(5) collapse to the grep-and-caveat branch). Under A-002 (no named #539 author yet, Q33 at `merged-requirements.md:560`), V3 is the least sensitive to who does the work.
6. **Silence is not acceptance (C-006).** The ruling names each measured channel as accepted, so part (b) of Q1 is answered explicitly, not by default.

## Weaknesses identified in other variants

1. **V2: owner-signed allow-list and shared `paths` changed inside the largest PR in the program.** Evidence above (INV-009, INV-039, E-08). This raises the review burden exactly where a mistake is a security mistake.
2. **V2: premise omitted.** SW-01 (2) applies to every ruling, not only acceptances (`merged-requirements.md:190`). V2's next steps state only the allow-list authorisation (SW-01 (3)).
3. **V2: a partial fix fails silently.** The adopted test idea originally covered only fsmonitor and `.clean` (`invariant-probe.md:12`); the spec had to add a `.process` falsifier (`merged-requirements.md:1153`). A V2 that misses a channel removes the caveats and leaves the claims false; V3's failure mode is visible text.
4. **V1: double edit over a byte-equal mirror** (`invariant-probe.md:19`; V1 "Costs").
5. **V1: trigger likely fires at merge.** `HOW-WE-WORK.md:406` (coordinator runs `/sc:sweep` every wake, at most every 5 minutes) versus V1's trigger "before any unattended or scheduled sweep". Interpretation, not a sourced ruling.
6. **V1: XC-04 still waits.** V1 concedes it ("the slowest downstream lane gains nothing"), so V1 pays V3's caveat cost and V2's fix cost.

## Concessions

1. **XC-04 is structurally blocked under V3.** `merged-requirements.md:452` (4): JOIN runs "on master code (never the unfixed sweep)"; `:889`: "JOIN never runs the unfixed sweep". `:35`: "a two-key test alone never declares a sweep run (JOIN, XC-04) safe", and under F3 there is no test at all. V3 offers no route and the spec provides no exception. This is a permanent dead edge in the dependency graph unless a later fix arrives, at which point V3 has become V1 without V1's plan. This is V3's largest weakness.
2. **The risk is exercised often, not occasionally.** `HOW-WE-WORK.md:406` makes the sweep run on every coordinator wake, fanned out across every listed worktree (at least 18 of 29 share one config, ADJ line 206). My premise that the sweep "grants no privilege a session does not already have" is about privilege; it does not deny that the sweep adds a frequent, automatic trigger. diff-analysis X-003 is right that my own risk section qualifies my premise.
3. **The project's security policy leans the other way.** `SECURITY.md:168-170` says vulnerabilities are "assessed based on worst-case configuration", that agent coordination issues are "evaluated for privilege escalation potential", and configuration-file vulnerabilities "considered for credential exposure risk". V3's premise relies on the E-11 counterweight, not on that text. SW-01 (2) makes the owner choose between them; V3 picks the counterweight.
4. **The caveat permanently weakens the contract** for the v2 knowledge layer and any future consumer (V3's own "Costs"). The sweep is a shipped CLI command (`src/superclaude/cli/sweep/commands.py:216,245` carry the claim, `invariant-probe.md:19`), so the caveat travels with every install; how many hosts install this fork is UNVERIFIED.
5. **Reversal after merge is a new fix PR** (SW-01 undo, `merged-requirements.md:190`). V3 does not dodge V2's cost; it defers it with no trigger.
6. **"Nothing is accepted by silence" depends on the channel list being complete** (A-001). An unlisted channel would be accepted by silence, which is the exact thing V3 claims to avoid. V2's "names any channel it leaves out" handles this better.

## Shared assumption responses

| Id | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The list is the measured set (`question.md:30`), not a proven complete set; `.process` was found only by a documentation read (`invariant-probe.md:12`). Other git config locations (for example submodule config) are UNVERIFIED as channels. For a fix, an omission is a hole; for an acceptance, it is an under-description. Either way every ruling should add a catch-all clause or V2's "names any channel it leaves out". |
| A-002 | ACCEPT | Q33 is open (`merged-requirements.md:560`) and gates SW-02, SW-03 and SW-05 pushes. All three variants stall on it; V3 has the smallest workload but still needs an author for 16-plus edits and the post. |
| A-003 | QUALIFY | Partly false in V3's favour: this session's own startup context includes a `gitStatus` snapshot, so the harness runs a `git status` in a worktree at session start (which flags it uses, and whether it honours the same config, is UNVERIFIED). Partly true against V3: the sweep is marginal in breadth and frequency, running in every listed worktree on every coordinator wake (`HOW-WE-WORK.md:406`). The sweep is not the only exposure, but it is the widest automatic one. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (all identical) | 50 | Same five sections by design of the brief; no difference to judge. |
| C-001 | V2 | 65 | Closing before the merge that turns the sweep into a recurring every-wake run (`HOW-WE-WORK.md:406`) avoids an exposure window V1 and V3 open. |
| C-002 | V2 | 75 | True claims beat caveated claims long term; V3 is honest, V1 edits twice. |
| C-003 | V2 | 90 | Only V2 unblocks XC-04 on master; V3 leaves it dead (`merged-requirements.md:452`, `:889`). |
| C-004 | V3 | 75 | SW-01 (2) requires a premise; V3 states the fullest one, V2 states none. |
| C-005 | V2 | 80 | A fix is reversible; an acceptance is not after merge (SW-01 undo column). |
| C-006 | V2 | 65 | "Names any channel it leaves out" protects against an unlisted channel; V3's list risks acceptance by silence. |
| X-001 | V1 | 55 | Same merge speed as V3 for most lanes, and XC-04 has a planned route instead of a dead end; V2 is slower to merge. |
| X-002 | V2 | 60 | Given every-wake fan-out and `SECURITY.md:168-170`'s worst-case lens, "not acceptable" is the safer default; V3's premise is defensible but owner-dependent. |
| X-003 | V1 | 55 | The sweep adds no privilege (V3 right) but adds a frequent automatic trigger (V2 right); V1's "temporary exposure worth tracking" fits both. |
| A-001 | V2 | 70 | Only V2 commits to naming excluded channels. |
| A-002 | V3 | 55 | All stall on Q33; V3 has the least author work while it is open. |
| A-003 | V3 | 55 | Only V3 states the premise that the sweep may not be the marginal exposure; still qualified by the sweep's fan-out. |

## Overall

If I were neutral, I would recommend **Variant 2** to the owner, confidence **62**. V3 is the structurally least invasive answer and the most honest about its premise, and it is the right choice only if the owner is willing to also rule an exception or a later fix for XC-04, which none of the sources provide. Because the spec hard-forbids the unfixed sweep for JOIN (`merged-requirements.md:452`, `:889`) and the merged sweep runs on every coordinator wake across every listed worktree (`HOW-WE-WORK.md:406`), V3 leaves a permanent blocked edge and a recurring exposure; V2 closes both at the cost of an allow-list and test change inside #539. V1 is the reasonable middle path if the owner wants the fix reviewed outside the 1003-file PR, provided the owner states whether a coordinator wake counts as a "scheduled sweep" under V1's trigger.
