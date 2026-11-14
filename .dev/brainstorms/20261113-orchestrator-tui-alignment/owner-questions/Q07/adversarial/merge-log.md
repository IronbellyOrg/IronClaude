# Merge Log: Q7 merged answer

## Metadata

- Base: `variant-2-original.md` (proposal B)
- Plan: `refactor-plan.md` (4 planned changes; review status auto-approved 2026-11-14)
- Source variants: `variant-1-original.md` (proposal A: Changes 1, 2, 3), `variant-3-original.md` (proposal C: Change 4)
- Output: `../merged-answer.md`
- Merge date: 2026-11-14
- Not applied, per the plan's "Changes NOT Being Made" table: A's "pass record reaches master only inside the switch-on PR" (C-002, C-003); C's "move nothing now" (C-002); A and C's "keep OB-06 (d) committed in this PR" (X-002). The base's OB-06 rewording bullet is kept.

## Changes Applied

### Change 1: owner re-reads the files before the authorship sentence

- Status: applied
- Provenance: proposal A, "Answer" ("re-reads and re-confirms in their own words")
- Answer, before: "The owner writes one dated sentence in the ledger confirming that the existing pass record and the 2026-11-08 and 2026-11-12 decision records are theirs, ..."
- Answer, after: "The owner reads each named file (or the byte-identical diff) first, then writes one dated sentence in the ledger that names the existing pass record and the 2026-11-08 and 2026-11-12 decision records and says they are the owner's text."
- What happens next, before: "The owner's sentence and date go into the ledger (XC-01). Its scope: ..."
- What happens next, after: "The owner reads each named file (or the byte-identical diff) first, then writes the dated sentence in the ledger (XC-01). The sentence names the files and says they are the owner's text. Its scope: ..." (scope sentence kept from the base)

### Change 2: the owner commits by default; a named session copies only on an explicit owner ruling

- Status: applied
- Provenance: proposal A ("personally commits"); debate point X-001
- Answer, before: "... and authorizes a records-only pull request, opened now and separate from the switch-on, that copies the sibling-only records to master byte for byte, with no edits, for the owner to review and merge."
- Answer, after: "The owner then personally commits the sibling-only records to master byte for byte, with no edits, in a records-only pull request opened now and separate from the switch-on, ... A session the owner names makes the copy and the commit instead only if the owner writes that a verbatim, byte-checked copy of owner text by a named session is acceptable."
- What happens next, before: "A session the owner names copies ... to a fresh branch from `origin/master`, staging those named paths only, and opens the PR through `/sc:pr-submit` on the fork, under a permission row for that item and action."
- What happens next, after: "By default the owner copies ... to a fresh branch from `origin/master`, staging those named paths only, commits them, and opens the PR through `/sc:pr-submit` on the fork. Only if the owner writes that a verbatim, byte-checked copy of owner text by a named session is acceptable does that named session make the copy and the commit instead, staging the named paths only, under a permission row for that item and action."
- Costs first bullet, before: "An agent session performs the copy and the commit; this sits close to the rule ..."
- Costs first bullet, after: "By default the owner makes the commit, which costs owner time: one branch, one commit and one pull request through `/sc:pr-submit`. If the owner instead rules that a named session may copy, that session performs the copy and the commit; this sits close to the rule ..." (rest of the bullet kept)
- Consistency edit (needed by Changes 1 and 2): unlocks bullet "Smallest owner effort: one sentence plus one merge." became "Owner effort stays small: one reading pass, one sentence, and one commit and merge (or one archive decision)." Unlocks last bullet now says "after the owner re-reads the files".

### Change 3: keep the named-archive alternative

- Status: applied
- Provenance: proposal A, "Answer" ("or archives them in a named place of the owner's choosing")
- Answer, after (inserted): "..., or archives them in a named place of the owner's choosing."
- What happens next, inserted bullet: "Alternatively, the owner names an archive of their choosing instead of master; the ledger records the archive path, and no records-only PR is opened."
- What happens next, before: "The owner merges it." and "The sibling can be cleaned once the merge is verified."
- What happens next, after: "On the master route, the owner merges the PR." and "The sibling can be cleaned once the merge (or the archive) is verified; that also ends the freeze."
- Consistency edit: unlocks first bullet now starts "On the master route, ..."; "What stays unresolved" adds "where an archive would live if the owner prefers an archive to master" (from proposal A's unresolved section).

### Change 4: a dated freeze entry today, with the full inventory

- Status: applied
- Provenance: proposal C, "What happens next" first bullet
- What happens next, inserted as new first bullet: "Today, the ledger (XC-01) gets a dated "do not clean `issue-409-mvp`" entry naming the files at risk: ... `handoff-mvp-brainstorm.md` (read 2026-11-14). The freeze holds until the merge (or the archive) is verified. The entry also records the owner's explicit decision on `handoff-mvp-brainstorm.md`: save it with the other records, or leave it."
- Copy list: adds "(plus `handoff-mvp-brainstorm.md` if the owner chose to save it)".
- What stays unresolved, before: "... whether `handoff-mvp-brainstorm.md` is included."
- What stays unresolved, after: "Whether `handoff-mvp-brainstorm.md` is saved or left is no longer open in advance: the owner decides it explicitly in today's freeze entry." The other two base items were reworded for Change 2 ("a commit of owner text by a named session (this matters only if the owner rules that alternative)"; "which session, if any, the owner names").
- Title updated to name the freeze, the re-read confirmation, the owner commit and the archive alternative.

## Post-Merge Validation

- Heading structure: pass. One H1 title, then the five H2 sections in the base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). Provenance header comments present; one `<!-- Source: ... -->` comment above each section.
- Internal references resolve: pass. Every id, path, commit and line reference in the merged answer (XC-01, OB-06, OB-08, Q24, Q30, `1ae72e1a1`, `f104ca51a`, `release-gates.md:22`, `merged-requirements.md:254`, ADJ line 191, the file names) comes verbatim from the base or from proposal C; none were invented. The freeze bullet's end condition ("merge (or the archive) is verified") matches the cleanup bullet.
- New contradictions introduced: 0. Checked: the costs section no longer says an agent always commits (it says the owner commits by default); the unlocks effort bullet matches the owner's added reading and commit work; the archive route does not claim master availability (unlocks bullet qualified "On the master route"); `handoff-mvp-brainstorm.md` is listed in the freeze inventory and decided there, and is no longer listed as unresolved. No em dashes or en dashes; no person's name.

## Summary

- Planned: 4
- Applied: 4
- Failed: 0
- Skipped: 0
