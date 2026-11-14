# Round 1, advocate for Variant 2 (proposal B), persona: architect

## Position summary

The owner should rule the outcome that does not depend on implementation: no program named by git configuration or the inherited environment runs during the sweep's `git status`, with all six channels in scope and every excluded channel named. The mechanism (F1, F2 or both) is an engineering choice whose viability turns on facts nobody has measured yet. On reflection, though, the spec's own acceptance criteria require the owner's ruling to name a shape, so Variant 2 cannot stand as written. Its useful parts are the split between outcome and mechanism, the reason recorded in the PR, and the duty to name excluded channels. They should be grafted onto an owner-named shape.

## Steelman

**Variant 1 (F2, fail closed).** A security fix should have one behaviour that a reviewer can check in a 1003-file PR. Refusing never alters a result: a worktree is either scanned normally or honestly reported `unscanned` (variant-1 "Status results are never altered"). The fix also does not depend on git honouring every override, and the 2026-11-13 measurement showed that one override is not enough ("Passing `-c core.fsmonitor=false` stopped only the fsmonitor hook; the clean filter still ran", question.md line 49). Variant 1 also takes the 2026-11-14 host facts seriously. It counts a program only "when it could run for that worktree's `git status`", so the system git-lfs filter in `/etc/gitconfig` does not mark every worktree `unscanned` (variant-1 next-step 3). The cost is reduced information, and the reduction is visible.

**Variant 3 (combination).** Most worktrees should keep full git facts. A neutralised fsmonitor is a speed-up whose absence should not change what `status` reports. Refusal is kept for the cases where neutralising could make the answer wrong, such as a filter the worktree's attributes select. That combination avoids F2's over-refusal on this host and F1's possible false-changed LFS files (question.md line 18, UNVERIFIED). Its two-sided regression test is the strongest test proposed: it fails if a program runs, and it fails if an altered result is presented as a normal scan (variant-3 next-step 2).

## Strengths claimed

1. **Separation of decision rights matches the record.** ADJ line 206 says: "The design of the fix belongs to the #539 author and the owner; this document states the requirement, not the code." `merged-requirements.md:33` frames SW-01 as a "Requirement (not a fix design)" stated by outcome. Variant 2 keeps the owner on the outcome and keeps the person with the code in front of them on the mechanism.
2. **Each shape's viability depends on facts that are still open.** Three examples. Whether F1 makes LFS files look changed is UNVERIFIED (question.md line 18). Whether F2's rule over-refuses depends on how "could run" is stated (question.md line 17). Whether any listed worktree selects a filter at all is UNVERIFIED (question.md line 16). A shape chosen now is chosen on inference, and implementation is where these facts become checkable.
3. **The ruling names excluded channels.** Variant 2 is the only one that carries SW-01 criterion (4) verbatim: "names any channel it leaves out" (`merged-requirements.md:190`). For channels nobody has listed, that is the only honest commitment: no rule can detect a channel it does not know (see X-001).
4. **An auditable trail.** The author writes the chosen shape and the reason in the PR, and the owner reviews it before merge (SW-05). The decision stays reversible: SW-01 says a fix choice is reversible ("an acceptance is reversible only before merge; a fix choice, yes", `merged-requirements.md:190`).

## Weaknesses identified in other variants

- **Variant 1, X-001:** its claim that "the sweep never runs a configured program, including through a channel nobody listed" contradicts its own rule. The rule refuses only what it detects as able to run, and an unknown channel cannot be detected. A fail-closed default covers doubt about known channels, not unknown ones.
- **Variant 1, the whole-run effect (U-004):** an inherited-environment hit affects the whole run. The session environment routinely carries `GIT_CONFIG_COUNT=2` with credential keys (question.md line 19). Unless the rule separates keys that name programs from keys that do not, F2 refuses the whole sweep from a normal session. Variant 1 names this risk but leaves the distinction to "the rule must itself be right".
- **Variant 3, A-001:** "could change the answer" is a harder judgement than "could run". It needs to know what each neutralised setting does to `status` output, and for included config and environment settings variant 3 itself says "it depends on what they set (UNVERIFIED in general)". If that judgement cannot be made reliably, the combination falls back to F2 with twice the implementation surface (diff-analysis A-001 impact).
- **Variant 3, the spec boundary:** variant 3 admits that it "goes further than the spec's wording, which offered F1 or F2". SW-02 criterion (1) defines the F1 test and the F2 test separately (`merged-requirements.md:191`). A combination needs both tests plus the boundary between them, which is more for a reviewer to check in a 1003-file PR (variant-3 costs).

## Concessions

1. **Variant 2 fails a gating acceptance criterion as written.** SW-01 (1) requires "A dated owner ruling names F1, F2 or F3" (`merged-requirements.md:190`), and the dependency table says "The ruling is the owner's" (`merged-requirements.md:648`). ADJ line 206 also frames the shape as the owner's: "The owner chooses (Q1): (F1) ... or (F2) ...". The owner's 2026-11-13 update states (a2) "which fix shape" as the open owner question (question.md line 6). Variant 2 cites only the half of ADJ line 206 that supports it.
2. **The #539 author is unnamed (Q33, `merged-requirements.md:560`).** Variant 2 hands the decision to a party that does not yet exist, and the ruling cannot then state which shape TB-GIT's test must check. That test differs between F1 and F2 (SW-02 (1)).
3. **No tool may design the fix** (`merged-requirements.md:1064`). Deferring the shape into implementation puts the security-relevant choice into a session the owner has not yet named, in the PR where the change is hardest to review.
4. **Variant 3's two-sided test** (U-003) is better than Variant 2's "covers every in-scope channel". It catches the silent-wrong-result failure that Variant 2's test does not name.

## Shared assumption responses

| Id | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | For the listed channels, whether a program "could run" for a worktree is plausibly decidable from configuration and attributes. The measurement found that `.gitattributes` alone ran nothing and that a program runs only if configuration names it (question.md line 50), so a filter counts only where configuration defines it and attributes select it. Whether the include chain and the environment can be classified with the same certainty is UNVERIFIED. "Could change the answer" (Variant 3) is a stronger claim and is not established by any measurement. The decidability of each shape's rule should be shown by the regression test, not assumed in the ruling. |
| A-002 | ACCEPT (as a required addition) | SW-02 criterion (2) already requires the git-status scope to be kept separate from the contract allow-list and the transcript scans (`merged-requirements.md:191`; INV-039, `merged-requirements.md:1100`). None of the three variants states it. Whichever shape is chosen, the ruling or the SW-02 plan must carry it, or every shape turns a contract in another repository's worktree into "outside root". |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | None (identical) | 95 | All three use the same five sections by design. |
| C-001 | V1 and V3 (tie), over V2 | 80 | SW-01 (1) and the owner's update require the owner to name the shape. |
| C-002 | V1 | 60 | Refusing never alters a result and is a single behaviour; V3 keeps more facts but rests on an unmeasured "could change the answer" judgement. |
| C-003 | V2 | 60 | No variant can detect an unknown channel; naming what the ruling leaves out (SW-01 (4)) is the only honest commitment. V1's and V3's claims about unknown channels overreach. |
| C-004 | V1 | 70 | It turns both host facts into a rule ("could run for this worktree"). V3 states them only as constraints, and V2 only as risks. |
| C-005 | V3 | 80 | The two-sided test catches both a program that runs and a silently altered result. |
| C-006 | V1 | 70 | One behaviour to implement and review inside a 1003-file PR. |
| X-001 | V2 (tie with V3), over V1 | 75 | Neither claims coverage of unlisted channels; V1's claim contradicts its own detection-based rule. |
| X-002 | V1 and V3, over V2 (mine) | 80 | The record makes the shape the owner's: `merged-requirements.md:190` (SW-01 (1)), `:648`, ADJ line 206 "The owner chooses (Q1)". |
| X-003 | V1 | 65 | F2 with the "could run for this worktree" rule does not refuse everything on this host. V3's "F2 fails here" holds only for a literal "defines it" rule. |
| A-001 | V1 | 60 | "Could run" is narrower and more checkable than V3's "could change the answer". V2 postpones the question rather than answering it. |
| A-002 | None (all omit it) | 85 | Must be added to whichever variant is chosen (SW-02 (2), INV-039). |

## Overall

If I were neutral, I would recommend **Variant 1**, at about **60 percent** confidence. The shape would be F2 with the "could run for this worktree" rule, so the system git-lfs filter and benign `GIT_CONFIG_*` credential keys do not refuse everything. I would amend it in four ways:
- Adopt Variant 3's two-sided regression test: it fails if a program runs, and it fails if a worktree that should be refused is scanned.
- Adopt Variant 2's duty to name every excluded channel in the ruling, and to record the reason for the rule in the PR.
- State A-002 explicitly.
- Drop Variant 1's claim about unlisted channels.

Variant 3 is the runner-up. It would win if a later measurement showed that neutralising is reliably harmless for most channels on this host's worktrees, which is UNVERIFIED today. Variant 2 as written is not recommended, because it fails SW-01 criterion (1).
