# Refactoring Plan: Q7 merged answer

## Overview
- Base variant: variant-2-original.md (proposal B)
- Incorporated variants: proposal A (three changes), proposal C (one change)
- Planned changes: 4
- Overall risk: Low to Medium (Change 2 modifies the base's central mechanism)
- Merged output path: ../merged-answer.md (in the Q07 folder)

## Planned Changes

### Change 1: owner re-reads the files before the authorship sentence
- Source: proposal A, "Answer" ("re-reads and re-confirms in their own words") and A's advocate on A-001.
- Target: base "Answer" and the first bullet of "What happens next".
- Approach: modify. The owner reads each file (or the byte-identical diff) first, then writes the dated sentence; the sentence names the files and says they are the owner's text.
- Rationale: debate points C-004 (A, 60%) and A-001 (A, 65%); B's advocate concession 3. The two sibling commits carry an automated co-author trailer (`git log` of `1ae72e1a1`, `f104ca51a`, read 2026-11-14), so authorship cannot be read from git.
- Risk: Low.

### Change 2: the owner makes the commit by default; a named session copies only on an explicit owner ruling
- Source: proposal A ("personally commits"), debate point X-001 (A, 60%; B's own advocate voted A).
- Target: base "Answer" and the second bullet of "What happens next"; "What it costs or risks" first bullet.
- Approach: modify. Default: the owner commits the records-only branch. Alternative, only if the owner writes that a verbatim, byte-checked copy of owner text by a named session is acceptable: that session copies and commits, staging the named paths only.
- Rationale: the rule "agents may cite, never write" (`release-gates.md:22`) and OB-01 (3) (merged-requirements.md:249).
- Risk: Medium (changes who acts).

### Change 3: keep the named-archive alternative
- Source: proposal A "Answer"; OB-01 (1) "or in a named archive the owner chose".
- Target: base "Answer" and "What happens next".
- Approach: insert.
- Rationale: A-002 (A, 80%, unanimous).
- Risk: Low.

### Change 4: a dated freeze entry today, with the full inventory
- Source: proposal C, "What happens next" first bullet (inventory including `handoff-mvp-brainstorm.md`).
- Target: base "What happens next" (new first bullet) and "What stays unresolved".
- Approach: insert. The freeze holds until the merge (or archive) is verified; `handoff-mvp-brainstorm.md` is decided explicitly (save or leave).
- Rationale: U-003; C-005 (the freeze starts today, before any PR exists); C's advocate verdict.
- Risk: Low.

## Base weaknesses addressed
| Issue | Better variant | Fix |
|---|---|---|
| A one-line confirmation can cover text the owner never re-read | A | Change 1 |
| An agent commit of owner text sits against the written rule | A | Change 2 |
| Master is the only destination | A | Change 3 |
| No protection between today and the PR | C | Change 4 |

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002, C-003 | A: pass record reaches master only inside the switch-on PR | Leaves it on one disk while the switch-on may be parked (A's advocate concession 1; unanimous C-002) |
| C-002 | C: move nothing now | Prolongs the single-disk loss risk (merged-requirements.md:264); C's own advocate voted against it |
| X-002 | A and C: keep OB-06 (d) "committed in this PR" | Majority chose "already on master and cited"; the rewording is recorded as an owner decision inside this answer |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | One owner reading pass | Remove |
| 2 | Medium | Owner time if the owner commits | Owner may rule the alternative |
| 3 | Low | Adds a choice | Remove |
| 4 | Low | One ledger entry | Remove |

## Review Status
Auto-approved, 2026-11-14 (non-interactive).
