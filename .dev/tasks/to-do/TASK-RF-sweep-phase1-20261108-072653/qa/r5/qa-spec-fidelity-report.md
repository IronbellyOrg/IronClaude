# QA Report: R5 SPEC-fidelity lens (INV-005 sign-off, NFR-014)

**Topic:** R5 edit (item 6.3) of `docs/designs/orchestrator-mode.md` against SPEC section 13 and NFR-014
**Date:** 2026-11-09
**Phase:** fix-cycle gate review (R5 QA gate, SPEC-fidelity lens)
**fix_authorization:** false (no file edited except this report)

## Method

I read the files named in the task. I compared the R5 edit by diffing `artifacts/design-base.md` (1013 lines) with the current DESIGN (1047 lines). Every R5 hunk was checked, and the R4 hunks were ignored. I then read the cited SPEC lines (9, 132, 141-144, 301, 310, 323, 468, 477-514, 562, 619, 627), the decision file, `r5-mechanical.md`, research/07 line 117 and `WORKER-CONTRACT.md` line 110. No `orca` command, no network call and no file write other than this report.

The R5 hunks in the DESIGN are:
- line 66 (GQ-109 row)
- lines 181 and 196 (diagram labels)
- line 221 (section 4 extension rule)
- lines 535-537 and 539 (section 7.3 constants)
- line 555 (M3 decision text)
- line 759 (section 11 test row)
- line 815 (NFR-014 row of section 12)
- line 837 (D10) and line 839 (`Total: 10 deviations.`)
- lines 851 and 895 (section 15.1)
- line 1047 (`### Fix cycle 3` R5 row)

## Evidence summary

- **Decision file** (`OQ-1-agent-wait-decision.md:19-22`):
  - It allows `worktree ps --agent-wait`, "with and without `--json`".
  - Quote: "Allow it, no conditions needed."
  - It keeps the allowlist pin at "ten templates, still seven verbs", keeps the version-scoped claim "unlikely (checked for Orca 1.4.245)", and keeps `--include-remote` forbidden (lines 24-30).
- **Allowlist** (`orchestrator-mode.md:526-537`): exactly ten tuples. Tuples 1-8 are the original eight. Tuples 9-10 are `("worktree","ps","--agent-wait")` and `("worktree","ps","--agent-wait","--json")`.
  - The verb set is still seven.
  - No other verb gained a template.
  - `FORBIDDEN_TOKENS = frozenset({"--include-remote"})` (line 539).
  - Matching is token for token with no prefix match (line 521), so `--agent-wait` on any other verb stays rejected by the exact-set rule.
- **Pin and version claim:**
  - The exact-set pin survives (line 759: "exact-set pin of the ten templates"; line 815).
  - The version claim survives (lines 426, 457, 611-612, 761, 1047).
- **D10 and R5 row quote the decision file correctly:**
  - D10 (line 837) quotes "Allow it, no conditions needed." and gives the date 2026-11-08.
  - The R5 row (line 1047) says "the allowlist pin and the version-scoped claim (Orca 1.4.245) are kept".
- **Not in the DESIGN:** no probe-result claim (the 24-call probe is not repeated). No lock claim was extended beyond Orca 1.4.245.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | `ALLOWED_ORCA` gained exactly two templates, both `worktree ps --agent-wait` (with and without `--json`), and the count is ten (lines 526-537) | PASS |
| C2 | The verb set stays seven; no new verb, no write verb, no other verb takes `--agent-wait` (exact token-for-token match, line 521) | PASS |
| C3 | `--include-remote` is still forbidden in any argv (line 539; negative test at line 759) | PASS |
| C4 | The exact-set allowlist pin is kept and updated to ten (lines 759, 815, 837) | PASS |
| C5 | The version-scoped claim (Orca 1.4.245, UNVERIFIED fallback, NFR-015) is untouched (lines 426, 611-612, 761, 1047) | PASS |
| C6 | D10 and the R5 row quote the owner decision verbatim and say nothing the decision file does not: no new probe evidence, no waived-condition gloss | PASS |
| C7 | No stale "forbidden" or "never" `--agent-wait` text is left in the DESIGN. All 9 `agent-wait` lines read allow or are the Phase-1-not-used statements (greps at lines 66, 535, 536, 679, 759, 833, 837, 895, 1047) | PASS |
| C8 | No stale "eight templates" or "(8)" text is left in the DESIGN; the only `eight` hit is D10 itself ("ten templates, not eight") | PASS |
| C9 | The deviation count is 10 rows and `Total: 10 deviations.` (line 839); D10 is a row of section 13 | PASS |
| C10 | D10's "SPEC text" cell names every SPEC line that conflicts with the allowance | PASS with MINOR note (F-1) |
| C11 | The step 1.0a capture rules are consistent with the pin (SPEC line 323: a template that fails the capture is dropped) | PASS with MINOR note (F-2) |
| C12 | The test row keeps a negative that pins the "only `worktree ps`" boundary of the allowance | PASS with MINOR note (F-3) |
| C13 | The line 221 extension-point rule does not open the allowlist to anything the owner did not allow | PASS with MINOR note (F-4) |
| C14 | `r5-mechanical.md` agrees with the file on disk: the line numbers 66, 535, 536, 539, 837, 839, 1015, 1047 and the em-dash, TODO and "eight" results | PASS (re-run by grep; counts match) |
| C15 | The edit did not touch `WORKER-CONTRACT.md:110`, which already reads "one prompt-wait listing (`worktree ps --agent-wait`)", or the SPEC (`git status` shows no change under `src/` or `tests/`; the SPEC folder is untracked and unedited by this task) | PASS |

Every check that carries a note has only a MINOR finding, and MINOR findings never fail the gate.

## Findings

No BLOCKING or MAJOR finding. I tried to show widening, a dropped pin or claim, and an over-record, and each attempt failed on the lines cited under C1 to C9. The notes below are MINOR.

### F-1 (MINOR): D10 omits SPEC line 301, which still says "eight templates"

- **Evidence:**
  - SPEC line 301: "The templates use exactly the seven verbs of INV-005 condition 1 (section 13) and no other verb; `task-list` has two forms, so there are eight templates. [SP-01]"
  - D10 (`orchestrator-mode.md:837`) lists "NFR-003 (line 132), NFR-014 (line 143) and SPEC lines 310, 323, 500, 504, 510, 562 and 619" and states "ten templates, not eight".
  - Line 301 is not in the list.
- **Wrong:** the register that exists to list the SPEC text that the design contradicts misses one of the two SPEC statements of "eight templates" (the other is line 143, which is listed). A reader who patches the SPEC from D10 leaves line 301 stale.
- **Smallest fix:** add `301` to the D10 SPEC-text list: "...SPEC lines 301, 310, 323, ...". Use "SPEC lines 301 and 310" for the template count and "310" for the `ps` row.

### F-2 (MINOR): step 1.0a item 11 says "each template" but section 15.1 says only templates 1 to 8 are run

- **Evidence:**
  - `orchestrator-mode.md:895`: "step 1.0a issues only templates 1 to 8 of it ... `worktree ps --agent-wait` is allowed by R5 but is not run in step 1.0a".
  - `orchestrator-mode.md:914`, item 11: "Whether each template accepts its flags as written (exit 0 with parseable output) | NFR-014 pin".
  - SPEC line 323: "Whether every template above takes `--json` exactly as written is UNVERIFIED and is the first thing the step 1.0a capture checks; a template that fails the capture is dropped".
- **Wrong:**
  - Templates 9 and 10 sit in the pinned set but can never be captured, so item 11's "each" is untrue for them.
  - The `--agent-wait --json` combination has no evidence at all in the decision file. The 24-call probe it cites gives no `--json` detail.
  - The DESIGN does not mark the two templates as unverified shape. This is harmless in Phase 1 because the sweep never calls them, but it is a drift from SPEC line 323 that D10 does not name.
- **Smallest fix:** reword item 11 to "Whether each of templates 1 to 8 accepts its flags as written. Templates 9 and 10 (R5) are not captured, their shape is UNVERIFIED, and Phase 1 never calls them."

### F-3 (MINOR): the `--agent-wait` negative test was removed and nothing replaces it

- **Evidence:**
  - Base test row: negatives "`--include-remote`, `--agent-wait`, `run-list`".
  - Current line 759: negatives "(`check`, `inbox`, `worker-read`, `gate-list`, an extra flag, `--include-remote`, `run-list`)" plus the positive case for both `ps --agent-wait` templates.
  - The owner allowed `--agent-wait` on `worktree ps` only (decision file lines 19-20; SPEC condition 1 "no other Orca verb or flag").
- **Wrong:**
  - The boundary "only on `worktree ps`" is pinned only by the exact-set test and the generic "an extra flag" negative.
  - The old explicit `--agent-wait` negative disappeared, so nothing names the case `worker-list ... --agent-wait` or `worktree list --agent-wait`.
  - The behaviour is correct (line 521: no prefix match), so the risk is a weaker test, not a wider allowlist.
- **Smallest fix:** in line 759 add the negatives "`worker-list --run <run> --json --agent-wait`, `worktree list --json --agent-wait` and `worktree ps --agent-wait --include-remote`", each raising `ValueError` before a subprocess.

### F-4 (MINOR): the section 4 extension-point wording reads as a general door

- **Evidence:**
  - Line 221 (R5 edit): "a new template in `ALLOWED_ORCA` (only after a capture or a recorded owner decision (R5, 2026-11-08), and never a write verb)".
  - NFR-014 (SPEC line 143): "The verb set never changes; the cursor template, when admitted after step 1.0a (section 8), is added to the pin in the same change."
  - Line 877 (M2) already says an allowlist change needs "an owner note".
- **Wrong:**
  - Read literally, the parenthetical makes "a recorded owner decision" a standing extension route, and R5 only an example.
  - It does not widen anything today: R5 is the only recorded decision, and the exact-set pin still fails any unrecorded template.
  - It could be read as allowing a future new read verb, which NFR-014 says never changes.
- **Smallest fix:** "(only after a capture, or the recorded owner decision R5 of 2026-11-08 for the two `worktree ps --agent-wait` templates; a new verb or a write verb is never added)".

### F-5 (MINOR, note only): "not called in Phase 1" is a design statement, not the owner's words

- **Evidence:**
  - Lines 535-536 say "not called in Phase 1", and line 895 says "not run in step 1.0a".
  - The decision file (lines 19-22) says only "allow".
  - D6 (line 833) and the WC-16 text (line 679) say `/sc:sweep` does not run the `--agent-wait` listing.
- **Assessment:**
  - These statements are narrower than the allowance, and they match master's text (`WORKER-CONTRACT.md:110`) and research/07 line 117, where the coordinator, not `/sc:sweep`, runs the listing.
  - They record nothing beyond the decision in a way that widens it.
  - They are design choices, so a future reviewer should not read them as part of the owner's decision.
- **Fix:** none required.

## Self-audit

- If I said "0 issues", this would not be believable. I diffed the R5 hunks against the base and found the five MINOR notes above.
- Tool calls: Read 6, Grep 3, Bash 4 (read-only `grep`, `sed -n`, `diff`, `wc`, `git status`). Each maps to a check above.
- **Confidence:** Verified 15/15 | Unverifiable 0 | Unchecked 0 | Confidence 100%.
- **Tool engagement:** Read: 6 | Grep: 3 | Glob: 0 | Bash: 4.

Verdict: PASS
Blocking count: 0
