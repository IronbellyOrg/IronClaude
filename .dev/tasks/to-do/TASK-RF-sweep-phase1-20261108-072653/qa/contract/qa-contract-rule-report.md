# QA Report - Contract gate, contract-rule lens (T266)

**Topic:** WC-16 Coordinator loop insertion (item 12.1), never-as-worker line 23 (item 12.2), pins (12.3), guide R7 (12.4)
**Date:** 2026-11-12
**Phase:** task-integrity / code gate (report-only, fix_authorization: false)
**Fix cycle:** N/A (first review)

---

## Scope

Lens: contract rule. Files read from disk on 2026-11-12: `src/superclaude/core/WORKER-CONTRACT.md` (lines 20-24, 268-282; full `git diff`), `docs/designs/orchestrator-mode.md` lines 664-713 (section 8, revised), `tests/skills/test_worker_contract.py` (full `git diff`), the developer-guide `git diff`, `phase-outputs/test-results/{step-1.17-checks.md,step-1.19-pytest.txt,r7-check.md,phase12-validation.md}`, `phase-outputs/plans/OQ-1-agent-wait-decision.md`, `OQ-3-GQ-11-rule-id-decision.md`, and `research/07-reanchor-contract.md` lines 1-173 (sections (d) and (e) included).

## Findings

No BLOCKING or MAJOR finding. Three MINOR notes (never fail the gate, not rechecked later).

| id | severity | evidence | what is wrong | smallest fix |
|----|----------|----------|---------------|--------------|
| F1 | MINOR | `step-1.17-checks.md:25-32` (Check 2) | `grep -c '^### WC-14'` is 0 at HEAD and 0 now, because WC-14 is a bullet (`WORKER-CONTRACT.md:63`, `- **WC-14. No turn ends between chain steps.**`), not a `###` heading. The check passes vacuously and proves nothing about WC-14. I verified the real claim myself in C8 (WC-14 lines at :63, :124, :213 are byte-identical to HEAD; the chain line moved 289 to 293 only because 4 lines were inserted above it). | None needed for the gate; a future record should grep `WC-14\.` instead. |
| F2 | MINOR | `step-1.17-checks.md:56-63` (Check 5) | Byte-identity is compared on non-blank lines only (`grep -v '^$'`), so blank-line framing was not covered by the producer's check. I closed that gap in C1 and C3 with a full `cmp` and a context read; both hold. | None needed. |
| F3 | MINOR | `step-1.17-checks.md:39` and `:42` | One line says "4 insertions", another "added=2" (non-blank lines only, blank lines are excluded by the regex). The numbers are consistent once the regex is read, but the record does not say so. At the time of the record the diff had 0 removals; item 12.2 later added the one line-23 change. | None needed. |

## Check details

Method: one private batch under `/tmp/ironclaude-batch.*` (extracted text copies only, removed on exit) plus `git diff`, `grep`, `cmp`, `uv run pytest`, `uv run ruff`. No repository file other than this report was written.

### C1. WC-16 block is byte-identical to the fenced text in revised DESIGN section 8

- DESIGN fence markers: `docs/designs/orchestrator-mode.md:676` (opening ```` ```markdown ````) and `:680` (closing); fenced body is lines 677-679 (heading, blank, paragraph).
- Contract block: `WORKER-CONTRACT.md:275-277` (the one `^### WC-16. Coordinator loop$` line, 275, through 277).
- `cmp` of the two 3-line extracts: `IDENTICAL`; both are 1839 bytes; `diff` empty; no trailing whitespace or CR in the contract block (`grep -nP '[ \t]+$|\r'` printed nothing).
- Result: PASS.

### C2. Fenced text is the same text the owner approved and the same as the earlier DESIGN copy

- `revisions/chat-output-exception-20261109-133150/baseline/design.md` block extracted the same way: 1839 bytes, `cmp` IDENTICAL to current DESIGN lines 677-679; whole section 8 (`## 8.` to `## 9.`) has an empty diff between that copy and current DESIGN.
- `OQ-3-GQ-11-rule-id-decision.md:14` cites the proposed text at `docs/designs/orchestrator-mode.md:674-680`; on disk that span is the "Final text." paragraph (674) through the closing fence (680). The cited span matches.
- `OQ-3` lines 3 and 36-37: `status: RESOLVED`, option (a) "New WC-16 rule, not amending WC-1", owner decision 2026-11-09. Item 12.1's gate holds.
- Result: PASS.

### C3. Placement and blank-line framing

- `grep -n` on the contract: `271:### Fan-in rule (several workers, then one merge)`, `275:### WC-16. Coordinator loop`, `279:### Worked example: gate hit, answer, new Task`.
- Fan-in paragraph is line 273 (starts "For N input Tasks feeding one merge Task", ends "...to the person."); line 274 blank; WC-16 heading 275; blank 276; block 277; blank 278; Worked example 279. Exactly one blank line on each side (read with `cat -A`).
- Result: PASS.

### C4. Ident on the heading line; one heading

- Heading text is exactly `### WC-16. Coordinator loop`; `grep -c '^### WC-16'` is 1; `grep -n 'WC-16'` on the contract shows only line 275.
- `_check_rule` (`test_worker_contract.py:755-762`, per research/07 section (d)) needs the ident on the first-phrase line: `"WC-16": ("WC-16", ["WC-16. Coordinator loop", ...])` puts `WC-16` and the heading phrase on the same line.
- Result: PASS.

### C5. No lock sentence

- `sed -n 275,277p ... | grep -oiE '\b[a-z]*lock[a-z]*\b'` prints one word only: `blocked` ("a failed or blocked result it cannot retry under WC-6"). No `lock`, `locks`, `index.lock` or WC-9 retry wording in the block. DESIGN line 682 also states "The text holds no lock sentence".
- Result: PASS.

### C6. No code span starting `uv`, `make` or `bash`

- All code spans in the block: `` `### Liveness supervision` ``, `` `/sc:sweep` `` (x6), `` `worktree ps --agent-wait` ``. `grep -cE '`(uv|make|bash)\b'` is 0; `grep -c 'superclaude sweep'` is 0.
- `_check_repo_setup_gated` (research/07 section (e), :813-828) therefore has nothing to flag; the full contract test file passes (C11).
- Result: PASS.

### C7. Line 23 changed only by adding `/sc:sweep`

- `git diff -U0 --word-diff=porcelain`: the only changed token on line 23 is `` `/sc:spawn` `` becoming `` `/sc:spawn`, `/sc:sweep` ``; the rest of the line is unchanged context.
- Hunk header `@@ -23 +23 @@`: one line in, one line out. `grep -c 'Never-as-worker list'` is 1 now and 1 at HEAD; the line is still one physical line.
- Command order on line 23: agent, git, help, issue, pm, spawn, sweep, swarm-wizard, pr-submit; matches DESIGN lines 703-705.
- Result: PASS.

### C8. Nothing else in the contract moved or changed

- `git diff --numstat`: `5  1`; hunks are only `@@ -23 +23 @@` and `@@ -274,0 +275,4 @@` (the 4 lines are heading, blank, paragraph, blank).
- Lines 110 ("The sweep.") and 151 (L1 probe row) are identical to HEAD (`diff` of `git show HEAD:... | sed -n '110p;151p'` against the file: SAME), so `RULE_PHRASES["liveness-sweep-and-states"]` and `["liveness-ladder-and-restart"]` are untouched.
- WC-14 mentions: HEAD `:63, :124, :213, :289`; now `:63, :124, :213, :293`; the last is the same chain line shifted by 4. No text changed.
- Result: PASS.

### C9. The four pin phrases occur in the block

- `WC-16. Coordinator loop` 1, `On every coordinator wake` 1, `it is never posted` 1, `It never stops watching on its own` 1 (each counted with `grep -cF` on lines 275-277).
- Result: PASS.

### C10. The five test-pin edits match DESIGN section 8 "Pins" (lines 684-690)

From `git diff -- tests/skills/test_worker_contract.py`: (1) `"WC-16"` entry after `"WC-15"` and before `"heartbeats"` with the four DESIGN phrases; (2) `"never-as-worker"` phrase now two adjacent strings whose concatenation is `` `/sc:agent`, ..., `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers ``, equal to the contract line 23 fragment; (3) `"/sc:sweep",` appended to `NEVER_AS_WORKER` after `"/sc:pr-submit"`; (4) test renamed to `test_never_as_worker_list_names_every_listed_command`, body unchanged; (5) `assert "sweep" not in UNATTENDED_COMMANDS` after the `"load"` assertion. Counts: `grep -c '"WC-14": ('` = 1, `grep -c '"WC-16": ('` = 1, `grep -c 'names_all_seven_commands'` = 0. No pin was deleted.
- Result: PASS.

### C11. Tests and lint re-run now

- `uv run pytest tests/skills/test_worker_contract.py -q`: 742 passed. Targeted `-k "WC-16 or never-as-worker or never_as_worker or sweep or load_usage or rule_check_fails"`: 72 passed.
- `uv run pytest tests/skills tests/core -q`: 2008 passed in 52.74s.
- `uv run ruff check tests/skills/test_worker_contract.py`: All checks passed. `uv run ruff format --check`: 1 file already formatted.
- Result: PASS.

### C12. Saved evidence agrees with disk

- `step-1.19-pytest.txt:753` "742 passed"; contains `test_contract_states_rule[WC-16] PASSED` (line 16), `[never-as-worker] PASSED` (54), `test_rule_check_fails_when_rule_removed[WC-16] PASSED` (374), `test_never_as_worker_check_fails_when_command_removed[/sc:sweep] PASSED` (450). `phase12-validation.md:56` "2008 passed" equals my re-run. The item 12.3 write-verb grep over `sweep.md` and `sc-sweep-protocol/SKILL.md` printed no line (re-run by me: no output), so no `WRITE_VERB_CLASSIFICATION` row is needed.
- Result: PASS.

### C13. Routing row R7 (developer guide copy)

- `git diff --stat`: 1 insertion, 1 deletion; the only change is `` `/sc:spawn` and `` to `` `/sc:spawn`, `/sc:sweep` and `` on guide line 991. Command order extracted from guide line 991 equals the order on contract line 23 (printed side by side, identical). `r7-check.md:27-30` records the same.
- Result: PASS.

### C14. Decision records consistent with the WC-16 text

- OQ-3 is RESOLVED to option (a) (see C2). OQ-1 (`OQ-1-agent-wait-decision.md:19-23`) is RESOLVED "allow" for the `worktree ps --agent-wait` listing as an allowed Orca command, and says Phase 1 never runs it and `WORKER-CONTRACT.md:110` is not edited; WC-16's sentence that `/sc:sweep` "does not update heartbeat records or run the `worktree ps --agent-wait` listing" describes the added read, not the master sweep, and does not contradict it.
- Result: PASS.

### C15. No stale second copy of the list in live sources

- `git ls-files | grep -i WORKER-CONTRACT` lists only `src/superclaude/core/WORKER-CONTRACT.md` (plus an old spec under `.dev/orca-command-refactor/`); Glob finds no `plugins/` or `.claude/` mirror (only the untracked `.venv` install copy). A repo-wide grep for the old fragment outside `.dev/tasks`, `.git`, `.venv` hits only `.dev/implement/.../retries/*/prompt-*.md` run logs, not live docs.
- Result: PASS.

## Checks

| Check | Result |
|-------|--------|
| C1 | PASS |
| C2 | PASS |
| C3 | PASS |
| C4 | PASS |
| C5 | PASS |
| C6 | PASS |
| C7 | PASS |
| C8 | PASS |
| C9 | PASS |
| C10 | PASS |
| C11 | PASS |
| C12 | PASS |
| C13 | PASS |
| C14 | PASS |
| C15 | PASS |

## Confidence and tool engagement

- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 11 | Glob: 1 | Grep: 0 (all grep ran inside Bash batches) | Bash: 9 (including 2 pytest runs, 1 ruff pair, 2 private batches under /tmp deleted by trap) | Edit/Write: this report only. Web: none.
- Limit noted, not blocking: DESIGN (`docs/designs/orchestrator-mode.md`) is untracked, so "revised DESIGN" is the file on disk (mtime 2026-11-09 14:15). It was also compared with the 2026-11-09 13:35 baseline copy. The owner's exact approval minute is not in the record, only the date and the OQ-3 line-range citation (674-680), which matches the current file.

Verdict: PASS
Blocking count: 0
