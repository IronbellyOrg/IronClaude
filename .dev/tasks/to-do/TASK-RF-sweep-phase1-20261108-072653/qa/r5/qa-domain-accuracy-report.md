# QA Report: R5 domain-accuracy lens (WC-16, R5 allow edit, contract line 110)

**Topic:** Would a coordinator reading WC-16, the R5 allow edit (the two `--agent-wait` templates in DESIGN 7.3 and D10) and master's sweep paragraph (`WORKER-CONTRACT.md:110`) do one consistent thing on a wake?
**Date:** 2026-11-09
**Phase:** doc-qualitative (domain-accuracy lens), `fix_authorization: false`
**Fix cycle:** N/A

Files read (all by Read in chunks under 150 lines, or by read-only `sed -n` and `grep`): `src/superclaude/core/WORKER-CONTRACT.md` 40-50 and 95-201; `docs/designs/orchestrator-mode.md` 215-222, 466-491, 519-563, 600-613, 612-641, 664-708, plus lines 66, 759, 815, 833, 837, 895, 907, 1046, 1047 by `sed -n`; `OQ-1-agent-wait-decision.md` (41 lines); `r5-mechanical.md` (90 lines); `research/07-reanchor-contract.md` 100-173; SPEC `merged-requirements.md` 132, 143, 247-257, 299-324, 486-515 and the `agent_wait` grep.

## Findings

### F1 (MINOR) WC-16 triggers on "wake"; master's sweep triggers on "wake or timeout"

- Evidence: `WORKER-CONTRACT.md:110` "After every wake or timeout, at most once every 5 minutes". DESIGN `orchestrator-mode.md:679` (WC-16 text) "On every coordinator wake, at most once every 5 minutes". DESIGN `:716` (R2 bullet) "on every wake". WC-16 itself treats an expired wait as a separate event ("When a wait on Orca expires, the coordinator re-arms it").
- Why it matters: the contract's wait runs with `--timeout-ms 300000`, so an idle Run produces mostly timeouts, and those are the passes where silent workers are found. A coordinator that reads "wake" as "a delivery arrived" would run `/sc:sweep` only on deliveries.
- Mitigation already in the text: WC-16 says `/sc:sweep` runs "in the same pass" as "The sweep.", and that sweep does run on a timeout. So a careful reader gets the right answer; the wording is just narrower than line 110.
- Smallest fix: write "On every coordinator wake or timeout" in WC-16 (line 679) and in the R2 bullet (line 716). The pinned phrase `On every coordinator wake` stays a substring, so pin 1 still matches.

### F2 (MINOR) Two sources for `agentWait` and no precedence sentence when a `/sc:sweep` class and a master S-state disagree

- Evidence: master S4 (`WORKER-CONTRACT.md:122`) fires on non-null `agentWait`, read from the prompt-wait listing (`:110`, `worktree ps --agent-wait`). The design reads `agentWait` for rule 4(a) and rule 5 from `worker-show` (DESIGN `:491`; SPEC rule table lines 252-253). The SPEC static note (line 510) says `--agent-wait` is what turns on terminal wait-state reads, so it is not established that `worker-show` carries the same value. Open item 6 (DESIGN `:996`) covers only the field names, not that the two values agree.
- Failure a coordinator could hit: `worker-show` shows `agentWait` null or absent while the master listing shows it set. Master says S4 (L5 within about 5 minutes); `/sc:sweep` says `working` (rule 5) or `could not determine` (rule 9). WC-16 says the coordinator reads the report "before it acts" but never says which view governs. WC-16's last sentences ("The coordinator decides and performs any action under those rules") leave "those rules" unresolved.
- Safe-failure note: if the field is missing, rule 5 cannot match and the row falls to `could not determine`, so the report does not claim `working` falsely. The risk is only a mismatch where both fields exist but differ.
- Smallest fix: one sentence in WC-16: "The states and the ladder under `### Liveness supervision` decide every action; a `/sc:sweep` class never overrides one." Optionally extend open item 6 to "and that it equals the `worktree ps --agent-wait` value".

### F3 (MINOR) "Not called in Phase 1" for the two new templates is asserted three times and pinned nowhere

- Evidence: DESIGN `:535-536` comments, `:895` (15.1), WC-16 `:679` ("does not ... run the `worktree ps --agent-wait` listing") and D6 `:833` ("no `--agent-wait` listing"). The test row at `:759` records "zero argv for `worktree list` and `worktree current`" and "a positive case that both `worktree ps --agent-wait` templates ... are accepted", but no zero-argv assertion for the two `--agent-wait` templates.
- Why it matters: `list` and `current` get an explicit zero-argv pin for the same "pinned, not called" status; the two new templates do not. A later change could call the flag while every test stays green, and WC-16's sentence would then be false.
- Smallest fix: in the `:759` cell, change "zero argv for `worktree list` and `worktree current`" to "zero argv for `worktree list`, `worktree current` and both `worktree ps --agent-wait` templates".

### F4 (MINOR) The report line "Orca lock risk: unlikely (checked for Orca 1.4.245)" does not say which calls it covers

- Evidence: DESIGN `:610-612` (report header); SPEC lines 441 and 513. The static trace covers the read verbs; for `--agent-wait` the SPEC says only that it turns on terminal wait-state reads (line 510). OQ-1 evidence is 24 calls on one idle worktree, with the stated limits (shorter locks missed, one idle worktree, Orca 1.4.245).
- Why it matters: master's own listing (`:110`) runs `ps --agent-wait` every 5 minutes against worktrees that hold live workers, and WC-9 (`WORKER-CONTRACT.md:44`) makes a worker that finds `index.lock` report `blocked`. A coordinator can read "unlikely" as covering its own listing. The claim covers only what `/sc:sweep` calls, and `/sc:sweep` does not call the flag.
- Owner decision R5 explicitly keeps the version-scoped claim, so this is an accuracy-of-scope note, not a defect in the edit.
- Smallest fix: none required for the gate; optionally add "(covers the argv this command issues)" to the line, or carry the OQ-1 limits into 7.3.

### F5 (MINOR) Extension-point sentence mixes a general rule with a one-off citation

- Evidence: DESIGN `:221` "a new template in `ALLOWED_ORCA` (only after a capture or a recorded owner decision (R5, 2026-11-08), and never a write verb)". The parenthetical names a decision that has already happened as the condition for a future template. Read literally, R5 alone satisfies it for any later template.
- Smallest fix: "(only after a capture or a recorded owner decision, as R5 (2026-11-08) was, and never a write verb)".

### F6 (MINOR) D10 omits SPEC line 301 ("so there are eight templates")

- Evidence: D10 (`:837`) lists SPEC lines 310, 323, 500, 504, 510, 562, 619 and NFR-003/NFR-014. SPEC line 301 still reads "so there are eight templates", and line 627 still says "seven-verb allowlist pin". The "seven verbs" statements stay true (same verb, extra flag form); line 301 is the only stale count. No coordinator action depends on it.
- Smallest fix: add line 301 to the D10 "deviates from" cell.

## Conflicts checked and found consistent

- Cadence bound: WC-16 `:679` and contract `:110` both say at most once every 5 minutes; WC-16 runs "The sweep." unchanged.
- Heartbeat records: master's sweep updates them (`:110`); WC-16 says `/sc:sweep` does not.
- Prompt-wait listing: master's sweep runs it; WC-16 says `/sc:sweep` does not; the allowlist permits it but no Phase 1 code calls it. The three sources agree on who runs it.
- L1 cap and "costly probes only for triggered workers" (`:110`, `:151`): WC-16 states `/sc:sweep` reads are not L1 probes and the coordinator's own L1 probes stay trigger-limited.
- Stall proof and restart: WC-16 "only Orca's stall proofs make a worker stalled" matches contract `:157`; `/sc:sweep` rule 2 is the narrower subset and the report footnote (DESIGN `:629`) says stalled and fenced are not observed in Phase 1.
- No positive removal advice: `removable` is only `no` or `could not determine` (DESIGN `:419`), worktree `safe_to_close` is never `yes` (`:787`), so WC-16's "recommends nothing" holds and nothing contradicts "Never on silence" (`:182-192`).
- R5 edit: both templates in 7.3, `FORBIDDEN_TOKENS` = `{"--include-remote"}`, GQ-109, D10, 15.1, the NFR-014 row and the test row all say ten templates and allowed. `grep -n -i 'never with'` finds nothing left. Condition 2 (version-scoped claim) and the exact-set pin are retained, as OQ-1 requires. `WORKER-CONTRACT.md` has no working-tree change (`git status` empty for it), matching OQ-1's "not edited".
- Counts: 10 `| D<n> |` rows, "Total: 10 deviations." (line 839), "Total: 23 open items." (line 1015).

## Checks

| ID | Check | Result | Note |
|---|---|---|---|
| C1 | Read contract `### Liveness supervision` lines 95-201 in full | PASS | |
| C2 | Read WC-16 final text (DESIGN 679) and its pins and constraints (684-707) | PASS | |
| C3 | 7.3 holds exactly ten templates, two of them `--agent-wait` | PASS | lines 526-537 |
| C4 | `FORBIDDEN_TOKENS` holds only `--include-remote` | PASS | line 539 |
| C5 | GQ-109 row, D10 row and 15.1 sentence agree with 7.3 | PASS | lines 66, 837, 895 |
| C6 | NFR-014 row (815) and test row (759) say ten templates, positive `--agent-wait` case | PASS | |
| C7 | Section 4 extension-point rule (221) reads coherently | FAIL | F5, MINOR only |
| C8 | WC-16 cadence matches contract line 110 trigger | FAIL | F1, MINOR only |
| C9 | WC-16 and line 110 agree on who updates heartbeat records | PASS | |
| C10 | WC-16 and line 110 agree on who runs the `--agent-wait` listing | PASS | |
| C11 | Allowlist "not called in Phase 1" is enforced by a test, as for list/current | FAIL | F3, MINOR only |
| C12 | `agentWait` has one consistent source across S4, rule 4(a) and rule 5, and WC-16 gives a precedence rule | FAIL | F2, MINOR only |
| C13 | L1 cap and trigger-only costly probes vs `/sc:sweep` reads | PASS | WC-16 says so explicitly |
| C14 | Stall-proof and restart language consistent with contract `:157` | PASS | |
| C15 | "Recommends nothing" vs report fields (`removable`, `safe_to_close`) | PASS | DESIGN 419, 787 |
| C16 | OQ-1 decision text matches what the DESIGN applied (allow, with and without `--json`, no lock-check) | PASS | |
| C17 | Retained parts of the INV-005 sign-off (pin, version-scoped claim, `--include-remote`) still in force in DESIGN | PASS | |
| C18 | Report lock line scoped to the calls it covers | FAIL | F4, MINOR only |
| C19 | No stale "never --agent-wait", "eight" or "seven templates" text in DESIGN | PASS | grep clean |
| C20 | SPEC lines superseded by R5 are all listed in D10 | FAIL | F6, MINOR only |
| C21 | Deviation and open-item totals match the table rows | PASS | 10 and 23 |
| C22 | `WORKER-CONTRACT.md` unedited by this item | PASS | git status empty |

## Self-Audit

**(a) Reliance list:** I relied on no earlier QA report. I read `r5-mechanical.md` only as a list of what to re-check and re-ran the counts (D rows, totals, `never with`, stale "eight") myself.

**(b) Independent semantic checks:**
- WC-16 cadence against contract line 110 -- read both texts side by side (DESIGN 679, contract 110); found the "wake" vs "wake or timeout" gap (F1).
- `agentWait` source across master S4, SPEC rules 4 and 5 and DESIGN 491 -- read contract 122, SPEC 252-253 and 510, DESIGN 491 and 996 (F2).
- Whether the "not called" claim has a test -- read the full test row at DESIGN 759 (F3).
- Whether any report field could read as removal advice -- read DESIGN 419, 787 and 643 (no finding).

**Confidence:** Verified 22/22 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%
**Tool engagement:** Read 7 | Grep 4 | Glob 0 | Bash 4 (read-only `sed -n`, `grep`, `wc`, `git status`, `git diff --stat`, `git log`)
No web research was done; no network call was made; no `orca` command was run.

Not checked: whether `worker-show` really carries `agentWait` (open item 6 needs a live capture, which this gate may not run).

## Summary

6 findings, all MINOR (F1 to F6); none BLOCKING or MAJOR. The three sources give a coordinator one consistent action on a wake: run master's sweep unchanged (including the `--agent-wait` listing), run `/sc:sweep` in the same pass, and act under the S-states and ladder. The gaps are wording: the trigger word, a missing precedence sentence, and an unpinned "not called" claim.

Verdict: PASS
Blocking count: 0
