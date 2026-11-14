# QA Report: Task-Research Alignment (cycle 2)

**QA mode:** task-integrity
**Lens:** task-research-alignment
**Date:** 2026-11-08
**Task file:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
**Research dir:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/
**Grounded decision record:** phase-outputs/plans/OQ-1-agent-wait-decision.md

Status: complete. 4 blocking findings, 4 minor findings.

---

## What was checked

- The decision record `phase-outputs/plans/OQ-1-agent-wait-decision.md` (42 lines), read in full, treated as a grounded source.
- The task file (2895 lines): Phase 6 items 6.1 to 6.22 read in full; every line that holds `agent-wait`, `templates`, `FORBIDDEN_TOKENS`, `frozenset`, `Total: <n> deviations`, `eight`, `prompt-wait` or `section 8` located with grep and read in context; the Execution Log, Phase Findings, Open Questions and Follow-Up list read in full.
- DESIGN `docs/designs/orchestrator-mode.md` at HEAD (pre-edit): section headings, the 7.3 allowlist block (lines 515 to 532), and every line that says `agent-wait`, `eight` or `8 templates`.
- SPEC `merged-requirements.md` lines 143, 310, 500, 504, 562 and 619 (the `--agent-wait` passages).
- research/07 lines 117, 127 and 172; BUILD-REQUEST lines 61 to 62 and 96.
- The cycle-1 report `qa/qa-task-research-alignment-report.md`, for context only.

## Confirmed as correct

| Check | Evidence | Result |
|---|---|---|
| N-01: DESIGN line 835 sits in section 13 | DESIGN section 13 starts at line 801 and section 14 at line 837; line 835 is the `1.17` row "The REPORT's WC-14 draft". Item 5.12 pass rule says "section 13" for historical-name hits | PASS |
| 6.1 quotes the record accurately | 24 calls, 0 `index.lock` sightings at 5 ms, 0 failed calls, one idle worktree, Orca 1.4.245, messages `msg_d95a87e312e1` and `msg_6ee5998d0874`, "NOT withdrawn" all match record lines 22 to 37 | PASS |
| `Total: 9 deviations.` only before item 6.3 | hits at task lines 287 to 997 (Phases 2 to 5 and the 6.3 "change from" text) and 2880 (OQ-15, which says "until item 6.3 adds D10") | PASS |
| `Total: 10 deviations.` after item 6.3 | 1000, 1005, 1033, 1047, 1082, 1110, 2595, 2802 | PASS |
| One forbidden token | 998, 1482, 1525 all say `frozenset({"--include-remote"})` or "exactly --include-remote" | PASS |
| Ten templates downstream | 1482 (8.10 Context), 1525 (8.x lens), 1793 (10.3 exact-set pin of ten, positive case for both `--agent-wait` forms, `--agent-wait` dropped from negatives), 2595 (14.23) | PASS, except B-3 |
| Step 1.0a forbidden list | 1259 drops `--agent-wait` and says it is allowed but not run in 1.0a | PASS |
| Phase 12 and 14 lenses | 2163 (12.9) and 2679 (14.35) reflect the allow decision and D10 | PASS |
| Open Questions and Follow-Up | OQ-1 entry (2866) and the `[Closed]` follow-up match the record; record line 41 says `WORKER-CONTRACT.md:110` is not edited, and 6.3 says the same | PASS |
| D10 SPEC citations exist | SPEC 310, 500, 504 and 619 each say `worktree ps` never carries `--agent-wait` or list the `--agent-wait` negative test | PASS (see m-1) |
| Cycle-1 IMPORTANT findings | I-1 (historical-name class in 5.12), I-2 (2.7 per-section rule, line 287), I-3 (`dispatch_status` now at 1433 to 1440), I-4 (5.7 uses the four 1.16a points) are fixed | PASS |

## Findings

### B-1 (blocking): item 6.3 puts the two `--agent-wait` templates at positions 7 and 8, but every later item numbers them 9 and 10

- **Evidence:** item 6.3 action (1), task line 998: "after `("worktree", "ps", "--json"),` add `("worktree", "ps", "--agent-wait"),` and `("worktree", "ps", "--agent-wait", "--json"),`". In DESIGN, `("worktree", "ps", "--json"),` is line 527, template 6, followed by `worktree list` (7) and `worktree current` (8) at lines 528 and 529. After the edit, DESIGN templates 7 and 8 are the two `--agent-wait` forms, and `worktree list` and `worktree current` become 9 and 10.
- **Items that assume the other order:** 6.3 action (4) "step 1.0a still runs only templates 1 to 8"; item 7.16 template list (task lines 1251 to 1258: 7 = `worktree list --json`, 8 = `worktree current --json`) and its step (3) "Templates 1, 2, 6, 7 and 8" (line 1260); item 7.24 lens (line 1316): "every command in readonly-probe.md is one of templates 1 to 8 of DESIGN 7.3"; the Phase 10 conftest item (line 1780): "templates 9 and 10, the two `worktree ps --agent-wait` forms ... get no fixture", with `synthetic-worktree-list.json (7)` and `synthetic-worktree-current.json (8)`.
- **What is wrong:** read against the edited DESIGN, "templates 1 to 8" includes the two `--agent-wait` forms and excludes `worktree list` and `worktree current`. The 7.24 reviewer will report the correctly run `worktree list --json` and `worktree current --json` captures as outside templates 1 to 8 (BLOCKING per its prompt), and 6.3 (4) writes a DESIGN sentence that tells step 1.0a to run the `--agent-wait` forms, which line 1259 says 1.0a does not run.
- **Smallest fix:** in item 6.3 action (1), add the two tuples after `("worktree", "current", "--json"),` (before the closing `)`), so they are templates 9 and 10. The decision record does not fix a position, so this stays within it.

### B-2 (blocking): Phase 6 and 7 gate prompts and the R5 fix-agent scope still describe the old branch (b)

- **Evidence:**
  - Item 7.24 lens, line 1316: "Also check the R5 sentence in DESIGN section 8 keeps --agent-wait out of /sc:sweep and that FORBIDDEN_TOKENS is unchanged. Each breach is BLOCKING." Item 6.3 changes `FORBIDDEN_TOKENS` on purpose (removes `--agent-wait`) and adds no section 8 sentence. This check fails by construction.
  - Items 6.15 (line 1082) and 6.19 (line 1110): the fix agent "edits only DESIGN `docs/designs/orchestrator-mode.md` (the section 8 R5 sentence and the `### Fix cycle 3` R5 row)". The allow branch writes no section 8 sentence; its edits are in 7.3, 11, 13, 15.1 and the GQ-109 row. Any R5 gate finding in those sections (for example B-4) cannot be fixed, so the gate runs to its cycle cap and HALTs.
  - Item 6.9 lens, line 1040: "is it clear that `/sc:sweep` never sends `--agent-wait`, and that the master prompt-wait listing stays outside `/sc:sweep`?" This is the branch (b) premise. A reviewer who reports "DESIGN does not say never" invites the fix agent to add a "never" sentence that contradicts the owner's "Allow it, no conditions needed." (record line 22).
  - Lesser leftovers of the same cause: 6.5 lens (line 1012) "the new section 8 sentence matches the surrounding style"; 6.11 lens (line 1061) "WC-16 with the R5 sentence"; every r5 gate Context (lines 1004 to 1123) lists "the section 8 WC-16 block" as an R5 input.
- **What is wrong:** the ripple update reached the counts but not these prompts. The decision record (lines 19 to 30, 41) names no section 8 sentence and allows the flag; nothing in research or the record grounds "keeps --agent-wait out of /sc:sweep" or "FORBIDDEN_TOKENS is unchanged".
- **Smallest fix:** 7.24: replace the sentence with "Also check that `FORBIDDEN_TOKENS` in DESIGN 7.3 is exactly `{"--include-remote"}` and that step 1.0a ran no `--agent-wait` template." 6.15 and 6.19: scope the fix agent to "DESIGN sections 7.3, 11, 12, 13 and 15.1, the GQ-109 row and the `### Fix cycle 3` R5 row". 6.9: ask whether a developer can tell from DESIGN that both `--agent-wait` templates are allowlisted but not called in Phase 1. 6.5, 6.11 and the Contexts: drop "section 8 sentence", "R5 sentence" and "section 8 WC-16 block".

### B-3 (blocking): item 8.10 Verification still expects 8 `ALLOWED_ORCA` entries

- **Evidence:** item 8.10 (header line 1481), Verification line 1485: "a count of `ALLOWED_ORCA` entries is 8". The same item's Context (line 1482) says "`ALLOWED_ORCA` (exactly 10 templates after item 6.3)", and item 10.3 (line 1793) pins ten.
- **What is wrong:** correct code fails this check, or the executor trims the allowlist to pass it, which then fails 10.3. This is the kind of leftover count the cycle-2 brief asked about.
- **Smallest fix:** change "is 8" to "is 10".

### B-4 (blocking): item 6.3 leaves three DESIGN sentences stating eight templates

- **Evidence (DESIGN at HEAD):** line 548 (section 7.3, M3 paragraph) "the owner sign-off for INV-005 condition 1 names exactly these seven verbs and eight templates (NFR-014)"; line 794 (section 12) "| NFR-014 | `ALLOWED_ORCA` eight templates (7.3) |"; line 829 (section 13, `1.0a` row) "Only the eight allowlisted templates". Item 6.3 edits the closing comment at line 530 and the 15.1 sentence at 873 but none of these three, and its step (5) finds sentences only through `grep -n 'agent-wait'`, which does not hit them. Item 6.4's checks do not count templates.
- **What is wrong:** after 6.3, DESIGN contradicts itself on the template count; the record says "It now has ten templates, still seven verbs" (line 28). The 6.6 internal-consistency lens (which names "NFR-014 in section 12") and the 6.10 numbers lens ("Recount: the ten `ALLOWED_ORCA` templates") will flag these, and per B-2 the fix agent may not edit those places. Result: a predictable R5 gate HALT, or a false count left in DESIGN for the Phase 8 and 10 implementers.
- **Smallest fix:** add to 6.3: "(8) Change line 548 to say the sign-off now covers seven verbs and ten templates (R5, owner 2026-11-08); change the section 12 NFR-014 row to `ALLOWED_ORCA` ten templates (7.3); change the section 13 `1.0a` row to `Only templates 1 to 8 of the allowlist`." Add a check to 6.3 and 6.4 that `grep -n 'eight templates\|eight allowlisted' docs/designs/orchestrator-mode.md` returns no hit.

### m-1 (minor): the D10 row omits SPEC line 562

The D10 row (item 6.3 action (6)) cites "NFR-014 and SPEC lines 310, 500, 504 and 619". SPEC line 562 (GQ-109 row: "`--include-remote` and `--agent-wait` are forbidden") is also overridden by the decision and is the row DESIGN's own GQ-109 line cites. Add 562.

### m-2 (minor): Key Constraints still says "the eight allowlisted Orca read templates"

Task line 163: "Step 1.0a uses only the eight allowlisted Orca read templates". After R5 the allowlist has ten; say "templates 1 to 8 of the allowlist".

### m-3 (minor): "not called in Phase 1" is a builder decision, not part of the record

Item 6.3's comment `# allowed by R5 (owner 2026-11-08), not called in Phase 1`, line 1259 ("not run in step 1.0a") and line 1780 ("get no fixture") are consistent with DESIGN, whose sweep reads `worktree ps --json` only. The decision record says only that the sweep MAY run the flag. This is reasonable scoping, not fabrication, but it is not listed as a builder decision in Open Questions (compare OQ-11 and OQ-14). Add one line to OQ-1 saying Phase 1 allowlists both forms but calls neither.

### m-4 (minor, carried from cycle 1): item 4.1 anchor quote style

Item 4.1 still quotes `The guard's 'join completed' condition fails` with single quotes; DESIGN line 497 uses double quotes. A `grep -F` with the task text misses the anchor. Outside the cycle-2 edits.

## Research-alignment checklist summary

1. Key findings to items: the R5 decision record maps to items 6.1 to 6.4 and to the downstream counts; the research/07 sweep paragraph (line 117) is cited in 6.1 and the r5 gate inputs. Covered, with B-1 and B-4 as defects in how 6.3 applies it.
2. Every key finding has an acting item: yes for R5; cycle-1 gaps I-1 to I-4 are closed.
3. Fabrication: no fabricated file, line or SPEC citation found. SPEC 310, 500, 504, 619 and DESIGN 66, 527 to 532, 738 and 873 exist and say what the task claims. The branch (b) prompt text in B-2 is not grounded in the current record.
4. Edge cases in Verify clauses: the record's kept conditions (allowlist pin, version-scoped claim, `--include-remote` forbidden) are in 6.1, 6.8 and 6.13. Missing: a template-count check in 6.3 and 6.4 (B-4), and the right count in 8.10 (B-3).
5. Dependency order: Phase 6 runs before Phase 7 and every code item; OQ-15 correctly explains that D6 holds the R4 cadence change so the total stays 9 until 6.3. Ordering is correct; B-1 is a numbering defect, not an ordering one.

## Verdict

VERDICT: FAIL

- Blocking: B-1 (template position in 6.3 contradicts the 1 to 8 and 9 and 10 numbering used by 6.3 (4), 7.16, 7.24 and the Phase 10 conftest item), B-2 (branch (b) leftovers in 7.24, the 6.15 and 6.19 fix-agent scope, and 6.9), B-3 (8.10 expects 8 entries), B-4 (DESIGN lines 548, 794 and 829 keep "eight templates").
- Minor: m-1 to m-4.

All four blocking fixes are small text edits to items 6.3, 6.9, 6.15, 6.19, 7.24 and 8.10, and none needs a new owner decision.
