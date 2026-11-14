# Fix Log: Task-Research Alignment (cycle 2)

**Findings:** qa/qa-task-research-alignment-report-2.md
**Task file:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
**Ground truth:** phase-outputs/plans/OQ-1-agent-wait-decision.md (allow, no conditions; pin and version-scoped claim kept; FORBIDDEN_TOKENS = {"--include-remote"}; D10, `Total: 10 deviations.`; no section 8 R5 sentence)
**Date:** 2026-11-08
**fix_authorization:** true. Only the task file was edited. DESIGN, SPEC, WORKER-CONTRACT.md and code were not touched. No git write was run.

| Finding | Item | Old text (short) | New text (short) | Grep confirmation |
|---|---|---|---|---|
| B-1 | 6.3 step (1) | after `("worktree", "ps", "--json"),` add the two `--agent-wait` tuples | after `("worktree", "current", "--json"),` (the last template, before the closing `)`) add them, "so they are templates 9 and 10" | line 998 hit; old phrase count 0. "templates 1 to 8" (998 step 4, 1316, 1780) and "templates 9 and 10" (1780) now agree with this order |
| B-2 | 7.24 lens | "Also check the R5 sentence in DESIGN section 8 keeps --agent-wait out of /sc:sweep and that FORBIDDEN_TOKENS is unchanged." | "Also check that FORBIDDEN_TOKENS in DESIGN 7.3 is exactly {"--include-remote"}, that ALLOWED_ORCA holds ten templates with the two worktree ps --agent-wait forms as templates 9 and 10, and that step 1.0a ran no --agent-wait template." | line 1316 hit |
| B-2 | 6.5 lens | "the new section 8 sentence matches the surrounding style" | "the two new `ALLOWED_ORCA` templates in 7.3 and the D10 row in section 13 match the surrounding style and cell counts" | `new section 8 sentence`: no hit |
| B-2 | 6.9 lens | "is it clear that `/sc:sweep` never sends `--agent-wait`, and that the master prompt-wait listing stays outside `/sc:sweep`?" | "is it clear that both `worktree ps --agent-wait` templates (9 and 10 of 7.3) are allowlisted by R5 but not called in Phase 1, that step 1.0a runs only templates 1 to 8, and that `FORBIDDEN_TOKENS` holds only `--include-remote`?" | line 1040 hit; `never sends`: no hit |
| B-2 | 6.11 lens | "DESIGN sections 7.3, 8, 11, 12, 15.1 and 18" | "DESIGN sections 7.3, 11, 12, 13 (D10), 15.1 and 18, the GQ-109 row" | line 1054 edited |
| B-2 | 6.12 lens (report labels it 6.11, line 1061) | "WC-16 with the R5 sentence" | "WC-16, the R5 allow edit (the two `--agent-wait` templates in 7.3 and D10)" | `R5 sentence`: no hit |
| B-2 | Contexts of 6.5 to 6.13, 6.16, 6.17, 6.20, 6.21 (13 places) | "(the section 8 WC-16 block, the `### Fix cycle 3` table, and sections 7.3, 11 and 15.1 where `--agent-wait` appears)" | "(sections 7.3, 11, 12 (NFR-014 row), 13 (D10) and 15.1, the GQ-109 row, and the `### Fix cycle 3` table)" | new phrase count 13; `section 8 WC-16 block`: no hit |
| B-2 | 6.15 and 6.19 fix-agent scope | "(the section 8 R5 sentence and the `### Fix cycle 3` R5 row)" | "(the places item 6.3 edits: sections 7.3, 11, 12 (NFR-014 row), 13 (D10) and 15.1, the GQ-109 row, the eight-templates lines of item 6.3 step (8), and the `### Fix cycle 3` R5 row)" | new phrase count 2 (lines 1082, 1110); `section 8 R5 sentence`: no hit |
| B-3 | 8.10 Verification | "a count of `ALLOWED_ORCA` entries is 8" | "... is 10" | line 1485 hit |
| B-4 | 6.3 Action, Output, Verification | no step for DESIGN lines 548, 794, 829 | new step (8): update every DESIGN mention of eight templates to ten, found with `grep -n 'eight\|8 templates' docs/designs/orchestrator-mode.md` (548 M3 paragraph, 794 section 12 NFR-014 row, 829 section 13 `1.0a` row "Only templates 1 to 8 of the allowlist"); Output adds "12 (NFR-014 row)"; Verification adds the grep with "no hit that says the allowlist has eight templates" | line 998 hit. DESIGN at HEAD has the grep hits 530, 548, 738, 794, 829, 873; 530, 738 and 873 are covered by steps (1), (3) and (4) |
| B-4 | 6.4 Context, Action, pass rule | no template-count check | Context adds "12 (NFR-014 row)"; Action adds `grep -n 'eight\|8 templates' docs/designs/orchestrator-mode.md`; pass rule adds "no `eight` or `8 templates` hit says the allowlist has eight templates" | line 1005 hit |
| m-1 | 6.3 step (6) D10 row | "SPEC lines 310, 500, 504 and 619" | "SPEC lines 310, 500, 504, 562 and 619" | line 998 hit |
| m-2 | Key Constraints, line 163 | "Step 1.0a uses only the eight allowlisted Orca read templates" | "The Orca allowlist has ten read templates (eight called in Phase 1 plus the two R5 `worktree ps --agent-wait` forms); step 1.0a uses only templates 1 to 8" | line 163 hit |
| m-3 | `### Open Questions` | no builder-decision entry | new OQ-16: both `--agent-wait` forms are allowlisted (templates 9 and 10) but not called in Phase 1; reopen with evidence | line 2881 hit |
| m-4 | 4.1 | quote style | skipped, as instructed | n/a |

## Checks after editing

- No em dash in any new text: em-dash counts on the edited lines are 0, except the existing `grep -c '—'` commands on lines 998, 1005, 1082 and 1110.
- The YAML frontmatter is unchanged (lines 1 to 12 read back as valid).
- Phase 7 owner HALTs and unrelated items were not touched.
