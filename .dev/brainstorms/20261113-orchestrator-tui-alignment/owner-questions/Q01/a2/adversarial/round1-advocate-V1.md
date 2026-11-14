# Round 1 advocate statement: Variant 1 (proposal A, refuse and report, fail closed)

Persona: security (vulnerabilities, attack surface, fail-closed behaviour). Mode A, depth quick, Round 1.
Sources read: `question.md`, `a2/adversarial/variant-{1,2,3}-original.md`, `a2/adversarial/diff-analysis.md`, `merged-requirements.md:30-36`, ADJ lines 204-207 and 455-469, `SECURITY.md:160-171`. No code fix is specified here.

## Position summary

When the rule that decides "is this worktree safe to scan" is wrong, Variant 1 (V1) fails in one way that can be seen (too many worktrees reported `unscanned`) or in one way that leaks (a program runs). Variant 3 (V3) adds two more ways to fail: a neutralisation that does not hold, and a result that was changed but is shown as a normal scan. V1 never shows a changed result. It only withholds one. The owner should rule the shape now (V1), take V3's two-sided regression test, and drop V1's claim that it also covers channels nobody listed. Fail closed is a property of the rule the owner states, not something V1 gets automatically.

## Steelman

**Variant 2 (author picks F1 or F2 at implementation time).** The spec and ADJ both say "The design of the fix belongs to the #539 author and the owner" (ADJ line 206), and the spec's recommended answer is "F1 or F2" (`question.md:31`). Whether a shape works on this host depends on details that only show up with the code open: how the system git-lfs filter behaves (`question.md:15-18`), and how the shared path list has to be split (INV-039, ADJ line 469). Ruling the outcome and leaving the shape to the author avoids an owner ruling made on premises that are UNVERIFIED (for example the F1 result for LFS, `question.md:18`). The owner still reviews the shape before merge (V2 step 3), so the decision is moved later, not given away.

**Variant 3 (neutralise by default, refuse where neutralising could change the answer).** V3 is the only variant that names both 2026-11-14 host facts as constraints in the ruling itself (V3 step 3). It also keeps git facts for the common case. fsmonitor is a speed-up, so turning it off should not change what `status` reports (V3 "What it unlocks"), and under V1 a fsmonitor worktree loses its git facts for no security gain. Its two-sided test (fails if any program runs, and fails if an altered result is reported as scanned) is the strongest acceptance criterion any variant proposes (diff U-003, rated High). V3 avoids both known failures: F2 refusing everything on this host, and F1 reporting LFS files as changed (`question.md:17-18`).

## Strengths claimed (V1)

1. **The only failure V1 adds is loud.** V1's results are "never altered: a worktree is either scanned normally or honestly reported as not scanned" (V1 "What it unlocks"). If the "could run" rule is too broad, every worktree shows `unscanned` (V1 "costs", line 22). The coordinator sees that at once, and it hides no wrong data. F1 and the F1 part of V3 can fail silently: the probe showed that one override stopped the fsmonitor hook while "the clean filter still ran" (ADJ line 206; `question.md:49`). A neutraliser is only as good as the list of keys it knows. A key it misses runs with nothing visible to anyone.
2. **It does not depend on git honouring each override.** "Nothing is neutralised, so nothing can be neutralised wrongly" (V1 "What it unlocks"). The measured facts favour this. Six channels ran (`question.md:48`), and the fix "is not one flag" (`question.md:49`).
3. **It already handles the host's system-config fact.** V1 step 3 counts a filter defined in `/etc/gitconfig` "only in a worktree whose attributes select it". That answers the literal-F2 objection in `question.md:17` before anyone raises it.
4. **It treats unknown channels as unsafe.** V1 (b) says "anything the check cannot classify is treated as unsafe." That is the default `SECURITY.md:168` asks for ("assessed based on worst-case configuration"). The six-channel list is already known to be incomplete. The system scope (`/etc/gitconfig`, `question.md:15`) is not one of the six channels named in `question.md:7`. It is only covered if "inherited" is read broadly. Whether a user-level (global) config on this host names a program is UNVERIFIED.
5. **One behaviour, one test target** (diff C-006). This is the smallest thing for a reviewer to check inside a 1003-file PR (V2 and V3 "costs").
6. **It is honest about the blast radius of the environment** (U-004). A program named in the inherited environment affects the whole run, not one worktree. V1 says so up front.

## Weaknesses identified in other variants

**Variant 2.**
- It moves the decision with the largest security effect into a 1003-file PR (V2 "costs"). The SW-01 ruling is then a statement of outcome with no rule that can be tested. Each failure mode is listed as possible (V2 "costs", line 23) and neither is ruled out.
- ADJ line 206 gives the design to "the #539 author **and** the owner". V2 cuts the owner's part down to a review after the code exists, which is the point where changing shape costs the most.
- Who the author is remains open (Q33, V2 "unresolved"). The shape would be chosen by someone not yet named.

**Variant 3.**
- **Two leak paths instead of one.** The neutralise branch fails open for any program-bearing key it does not know. The probe already showed overrides are key-specific (ADJ line 206). V3's handling of unlisted channels ("disabled if that is safe, otherwise refused") assumes an unknown channel can be recognised as unknown. A channel nobody listed is by definition not on the disable list.
- **A new integrity failure.** If "could change the answer" is stated too narrowly, an altered `status` result is shown as a normal scan. V3 admits that "a wrong rule either leaks (runs a program) or over-refuses" (V3 "costs"). It leaves out the third failure, a silently wrong result, although its own test (step 2) exists to catch exactly that.
- **"Could change the answer" is harder to decide than "could run".** V3 itself says this is "UNVERIFIED in general" for included config and environment settings (V3 "What it unlocks"). If it cannot be decided, V3 collapses into F2 (diff A-001 impact) and carries the cost of two behaviours for nothing.
- It "goes further than the spec's wording" (V3 "costs").

## Concessions

1. **X-001 is a real overclaim in my variant.** "The sweep never runs a configured program, including through a channel nobody listed" (V1 "What it unlocks") does not hold. A refusal rule can only refuse what it detects. "Treated as unsafe if it cannot be classified" covers a channel the check sees but does not understand. It does not cover a channel the check never looks at. The ruling should drop that sentence and replace it with the outcome rule plus the named channels.
2. **V1 gives up information for no security gain in fsmonitor-only worktrees.** V3 is right that turning fsmonitor off should not change the answer (UNVERIFIED in general). How many of the 29 worktrees this affects is UNVERIFIED (V1 "costs").
3. **V3's two-sided test is better than mine.** V1's test checks only that "such a worktree" is not scanned (diff C-005). It does not prove that no program ran in the worktrees V1 did scan. The test should take V3's "fails if any in-scope program runs" side.
4. **V1 rests on A-001 too.** If "could run for this worktree" cannot be decided, V1 refuses broadly. That is safe, but on this host it could make the sweep useless (V1 "costs", line 22).
5. **The environment rule is under-specified.** The session carries `GIT_CONFIG_COUNT=2` credential keys that name no program (`question.md:19`). V1 names this risk but does not say how "names a program" is judged for environment variables.

## Shared assumption responses

| # | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | It can be decided for the named keys if the check reads the configuration git actually uses (all scopes plus included files), not just the repository file. A filter must also count only where the worktree's attributes select it. A channel nobody listed can never be decided. The ruling should therefore say what happens when the check cannot tell: refuse and report `unscanned` with the reason. Under that rule, if A-001 turns out false, V1 fails safe and visibly, while V3 fails toward its F1 branch. Whether attribute selection can be judged without running git's own machinery is UNVERIFIED. |
| A-002 | ACCEPT | All three variants depend on it, and none states it. INV-039 (ADJ line 469) shows that the shared `paths` list also feeds the contract allow-list and the transcript scans. A refused or narrowed git-status scope that spills into them misreports contracts as "outside root". The SW-01 ruling should say this in one line whichever shape wins. The requirement is cited from diff-analysis ("SW-02 (2)"). I confirmed INV-039 but did not re-read the SW-02 row itself. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (identical) | 50 | The section sets are the same by design of the brief. |
| C-001 | V1 | 65 | The owner states a rule that can be tested now. A choice made at review time inside a 1003-file PR is the costliest moment to change shape. |
| C-002 | V1 | 60 | Withholding a result fails visibly. Neutralising fails silently when a key is missed, and the probe already showed overrides are key-specific. |
| C-003 | V1 | 60 | Defaulting to "do not scan" when in doubt is the correct worst-case default (`SECURITY.md:168`), with the X-001 limit conceded. |
| C-004 | V3 | 60 | V3 writes both host facts into the ruling as constraints. V1 covers only the LFS fact in its rule and leaves the `GIT_CONFIG_*` fact as a risk. |
| C-005 | V3 | 75 | The two-sided test is the only one that catches both a leak and a silently altered result. |
| C-006 | V1 | 70 | One behaviour means fewer ways to fail and less for a reviewer to check. |
| X-001 | V3 | 70 | V3 makes no claim about unlisted channels that it cannot back up. V1's claim is overstated (conceded). |
| X-002 | V1 | 60 | ADJ line 206 names "the #539 author and the owner". The owner ruling the shape and the author designing the code satisfies both. V2 makes the owner a reviewer only. |
| X-003 | V1 | 55 | F2 fails on this host only if the rule is literal. V1 step 3 states the narrower rule, but the environment half is still open (concession 5). |
| A-001 | V1 | 60 | If "could run" cannot be decided, V1 degrades to broad, visible refusal. V3 degrades to F2 at double the cost. V2 leaves the problem to the author. |
| A-002 | none (all omit) | 50 | No variant addresses it. Whichever shape wins, it must be added to the ruling. |

## Overall

If I were neutral, I would recommend **Variant 1**, amended in three ways:
1. Remove the claim about unlisted channels (X-001).
2. Take V3's two-sided regression test (U-003).
3. State in the ruling both host constraints and the separate git-status scope (A-002).

Confidence: **60**. V3 is a close second for the owner who values coordinator information more than having a single failure mode. V2 is weakest from a security standpoint because the SW-01 ruling would contain no rule that can be tested.
