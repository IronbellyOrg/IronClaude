# Merge Log: Q1 (a2) and (b)

## Metadata

- Producer: /sc:adversarial, Step 5 (merge executor)
- Merge date: 2026-11-14
- Base: Variant 1 (proposal-A), `variant-1-original.md`
- Plan: `refactor-plan.md` (6 planned changes, overall risk Low, auto-approved 2026-11-14)
- Incorporated sources: `variant-2-original.md` (Variant 2, proposal-B), `variant-3-original.md` (Variant 3, proposal-C), the four amendments all three advocates proposed (`debate-transcript.md`), host facts in `../question.md`
- Output: `../merged-proposal.md`
- Rule carried: the code fix is never specified; outcome level only. Channel names are kept because they name the channels, not the fix.
- Added at the request of the orchestrator: a line at the top of the Answer stating that part (a) is already answered "fix" by the owner (source: `../question.md`, owner update of 2026-11-13).

## Changes Applied

### Change 1: replace the unlisted-channel claim with an auditable promise

- Status: APPLIED
- Target: Answer part (b); What it unlocks, bullet 1
- Before: (b) said all six channels are in scope and "anything the check cannot classify is treated as unsafe"; unlocks bullet 1 claimed the sweep never runs a configured program "including through a channel nobody listed".
- After: (b) says the six channels are a minimum, the ruling names any channel it deliberately leaves out, anything the check cannot classify is refused and reported `unscanned` with its reason, and no claim is made about channels nobody listed. Unlocks bullet 1 now promises only what can be checked: no program a named channel configures runs for a scanned worktree, doubt means "do not scan", and left-out channels are named.
- Provenance tag: Variant 2 (C-003, X-001); V1 advocate concession 1; transcript amendment 1
- Validation: PASS. The overclaim text no longer appears; the Answer and the unlocks bullet now agree.

### Change 2: two-sided regression test

- Status: APPLIED
- Target: What happens next, step 2
- Before: the test failed only if a worktree using an in-scope channel was scanned instead of reported `unscanned`.
- After: the test reproduces the 2026-11-13 probe and fails if any in-scope program runs in a scanned worktree, and fails if a worktree that should be refused is scanned.
- Provenance tag: Variant 3 (U-003, C-005); transcript amendment 2
- Validation: PASS. Stated as outcomes the test must catch; no test code or mechanism specified.

### Change 3: environment counting rule

- Status: APPLIED
- Target: What happens next, step 3 (appended)
- Before: step 3 covered only how a filter counts.
- After: an inherited-environment setting counts only when it names a program `git status` could run (the session's `credential.*` keys name none); a setting that does count affects the whole run, which is then reported, not partly scanned.
- Provenance tag: all advocates (transcript amendment 3); `../question.md` host fact on `GIT_CONFIG_COUNT=2` with `credential.interactive` and `credential.guiPrompt`
- Validation: PASS. Agrees with the existing cost bullet "An inherited-environment hit affects the whole run, not one worktree."

### Change 4: keep the git-status scope separate

- Status: APPLIED
- Target: What happens next, new step 4 (inserted)
- Before: absent.
- After: the ruling states that the git-status scope is kept separate from the contract allow-list and transcript scans, which share the same path list, so the git-status fix does not change what those reads cover.
- Provenance tag: A-002 (all advocates ACCEPT); SW-02 (2); INV-039; transcript amendment 4; `../question.md` fact citing ADJ line 206 and INV-039 (line 469)
- Validation: PASS. Outcome level only.

### Change 5: reasoning recorded in the PR, owner review before merge

- Status: APPLIED
- Target: What happens next, new step 5 (inserted)
- Before: absent.
- After: the #539 author records in the PR description how the ruling was carried out and why, so it is easy to find inside the 1003-file PR, and the owner reviews it before merge (SW-05).
- Provenance tag: Variant 2 (U-002)
- Validation: PASS. The shape stays the owner's (F2 in step 1); only the reasoning record and the review step are taken from Variant 2, consistent with the plan rejecting Variant 2's "leave the shape to the author".

### Change 6: name the runner-up and when it would win

- Status: APPLIED
- Target: What stays unresolved (appended)
- Before: two open items (filter use today; trusted-program exception).
- After: a third item names Variant 3's combination (disable programs by default, refuse only where disabling could change the answer) as the runner-up if a count shows many fsmonitor-only worktrees whose git facts F2 would withhold for no security gain.
- Provenance tag: Variant 3 advocate overall; V1 advocate concession 2; transcript overall recommendation
- Validation: PASS.

## Post-Merge Validation

### Structural integrity

- PASS. One H1 title (kept from the base) and the five required H2 sections in the base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved.
- Provenance header comments present at the top (producer, base, incorporated sources, merge date); each section carries a `<!-- Source: ... -->` comment.
- Numbered steps run 1 to 5 with no gaps.

### Internal references

- PASS. Every id and path in the merged text appears in the plan, a variant, the transcript or `../question.md`: SW-01, SW-02, SW-05, PR #539, `SECURITY.md:168-170`, `/etc/gitconfig`, the 2026-11-13 probe, the 29 listed worktrees, the 1003-file PR, `credential.*`, `GIT_CONFIG_*`. No new ids, paths or line numbers were introduced.

### New contradictions

- None found. Checked pairs: Answer (b) against unlocks bullet 1 (both now limited to named channels plus refuse-on-doubt); step 3 environment rule against cost bullet 3 (both say a counted environment setting affects the whole run); step 5 against step 1 (owner names the shape, author records reasoning); runner-up item against the Answer (the runner-up is conditional on an unmeasured count, not a competing ruling).
- Style checks: no em dashes or en dashes; no flags, functions, argument lists, config keys to set or implementation steps added.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 6 | 6 | 0 | 0 |
