# Revise 1: orca-worker-contract-spec.md

Prompt followed: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:53-55` (read in full). Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Ids repaired: F-01, F-02, F-03, F-04 (the Reviser brief of `.dev/orca-command-refactor/review/round1.md:212-221`). Medium (M-01 to M-14) and minor (m-01 to m-04) findings were left alone. No spec-panel was run. No verdict is claimed.

Citation forms: `SPEC:N` = line N of the candidate (line numbers are unchanged by the edit; the file is 285 lines before and after); `INV-A:N`, `INV-B:N` = lines of `inventory/commands-a.md`, `commands-b.md`; `R1:N` = line N of `review/round1.md`. Any `sk/`, `cmd/`, `src/` line is not in the sandbox and is UNVERIFIED here except as quoted by an inventory line.

## Byte accounting

| item | bytes |
|---|---|
| candidate before (`history/spec-v1.md` is byte-identical, checked with `cmp`; sha256 `d3cdbe57...25200d`) | 57763 |
| candidate after (sha256 `f3f06d44...f1751`) | 58895 |
| net change | +1132 |

Net per finding is exact (a `wc -c` after each edit; the per-finding nets add up to +1132). Added and deleted are gross counts from a word-level diff of `history/spec-v1.md` against the candidate, split by finding by hand where one line holds edits for two findings; they can be off by a few bytes against the net because of tokenizing.

| finding | bytes added | bytes deleted | net |
|---|---|---|---|
| F-01 | 976 | 265 | +711 |
| F-02 | 298 | 52 | +246 |
| F-03 | 119 | 30 | +89 |
| F-04 | 118 | 32 | +86 |
| total | 1511 | 379 | +1132 |

Edits that touch two findings are split: the P1 Commands cell (`SPEC:159`): F-02 adds 86 (the flag-set label and the six commands), F-04 deletes 22 (`load (usage line only)`), F-01 deletes 10 (`, workflow` from the fixes list, because F-01 removes the workflow fix). The section 3 intro (`SPEC:76`): F-01 net +11, F-02 +74, F-04 +14.

## Disposition per finding

| id | disposition | where applied (candidate lines) | evidence for the choice |
|---|---|---|---|
| F-01 | applied, with one part of the recommendation rejected (below) | WC-4 (`SPEC:62`): location rule rewritten; workflow exception added. Section 2.3 (`SPEC:73`). Section 3 intro "Contract" definition (`SPEC:76`). 3.1 rows: adversarial (`SPEC:83`), cleanup-audit (`SPEC:85`), index-repo (`SPEC:86`), init-lite (`SPEC:87`), tdd (`SPEC:90`), workflow (`SPEC:92`). AC-2.2 (`SPEC:200`). Consequences: AC-1.4 (`SPEC:198`) and SA-4 (`SPEC:149`) lose their workflow-contract clause. | R1:53-61 |
| F-02 | applied | P1 scope sentence and Commands cell (`SPEC:159`); section 3 intro (`SPEC:76`); AC-1.1 population (`SPEC:195`) | R1:87-90 |
| F-03 | applied | AC-C5 (`SPEC:176`), AC-0.3 (`SPEC:193`) | R1:131 (G8 row) |
| F-04 | applied | P1 Commands cell (`SPEC:159`); section 3 intro (`SPEC:76`); AC-1.1 (`SPEC:195`); AC-1.2 (`SPEC:196`) | R1:69-75 |

### F-01 details (every addition cites F-01)

- WC-4 (`SPEC:62`). The location is now "its report directory": the directory passed as `--output-dir` or as a directory-valued `--output`; the directory that holds the file when `--output` is a file (tdd, init-lite); or, for a command with no such flag, the directory its section 3.1 row names. The conflated "`--output` / `--output-dir`" and the `<output-dir>/` prefix are deleted. The title says "known before dispatch (workflow: after the run)". The "every outcome" clause now excepts a workflow stop before its package exists: no directory exists, so no contract is written and WC-5 (`SPEC:63`, "no report exists" maps to `failed`) already gives the outcome.
- Section 2.3 (`SPEC:73`): one clause says workflow's package path is generated, so it is known only after the run.
- Rows, each now naming where the contract goes: adversarial `<output>/adversarial/return-contract.yaml` (already named; now labelled its WC-4 directory; INV-A:35, INV-A:60-61); cleanup-audit `.claude-audit/return-contract.yaml` (fixed directory; INV-A:42); index-repo beside `PROJECT_INDEX.md` (INV-A:53, repo-root location still UNVERIFIED there, which the row's own P1 fix already states); init-lite and tdd in the directory of the `--output <file>` (INV-A:55; INV-B:47); workflow: the old fix "write the contract for pre-creation STOPs too" is replaced by "None" plus the reason, because the inventory records that a pre-creation STOP has no package directory and writes none (INV-B:272, which cites `refs/return-contract.md:39`; that file is UNVERIFIED here). AC-1.4 drops its workflow half for the same reason; SA-4 drops "and workflow" from the defect list; the workflow fix leaves the P1 "fixes to" list.
- AC-2.2 (`SPEC:200`): the pass condition now says where the contract is (for tdd, the directory of `<file>`), so the `/sc:tdd "auth" --unattended --output <file>` example can be run.
- Rejected part of the recommendation (R1:61): a new `--report-dir <dir>` flag. A new flag is a mechanism the finding does not require: the same defect is repaired by deriving the directory from flags the commands already have (INV-A:55 and INV-B:47 show the file-valued `--output`). The reviewer's own source for that flag name is outside the permitted evidence (R1:31, UNVERIFIED).

### F-02 details (every addition cites F-02)

- Narrowed, not expanded: P1 now delivers the flag only on a named flag set of 14 commands: analyze, build, business-panel, design, document, explain, index, test (8 P1 commands of 3.2 without `load`; `SPEC:99-123`) plus adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow (6 ready commands with no gate; `SPEC:83-92`). Every other command gets the flag in the phase that lists it, with its gate conversion, never earlier. The count 14 = 8 + 6 is checked against those rows. The 19 commands R1:87 names as having a later gate conversion are not in the set. The three no-gate P3 commands (save, validate-roadmap, validate-tests) also get the flag in P3, where they are edited anyway; R1:90 allows landing the flag with the phase that changes the command.
- The reviewer's alternative (a gated command refuses `--unattended` until its phase, R1:90) was not used: it adds a behavior to specify and test; landing the flag later adds none.
- AC-1.1 (`SPEC:195`) tests the P1 flag set instead of "every command in sections 3.1-3.2". Section 3 intro (`SPEC:76`) says the section and flag arrive in the phase section 6 lists, not earlier.

### F-03 details (every addition cites F-03)

- Both checks now use `git diff --numstat master...HEAD -- <path> | awk '$2 != 0'`. Column 2 of `--numstat` is the count of deleted lines, so a deleted `---` line and a deleted `- Will Not: push` bullet are counted; the old filter `grep -E '^-[^-]'` could not see them (R1:131, R1:208).
- Checked in this run with a process-substitution `git diff --no-index` on three texts (no file written): a text with the `---` lines and the bullet deleted printed `0 3` under the new check and nothing under the old one; a text with one modified line printed one row under both; a purely additive text printed nothing under both. A modified line still prints, as before; M-14 (Usage-line edits) is a Medium finding and was left alone.

### F-04 details (every addition cites F-04)

- Chosen option: remove `load` from the "every command" sets (R1:75 offers it). The P1 Commands cell now ends "load: Usage-line fix only, no flag or Unattended section"; section 3 intro reads "Every changed command except `load`"; AC-1.1 asserts "neither `load` nor any section-4 command has one"; AC-1.2 runs the live check "on each command in the P1 flag set" so `load` is not live-checked. The `load` row (`SPEC:112`) and the Decision (`SPEC:265`) are unchanged and now agree with all of these (INV-B:65: its only output is context for the current session).

## Self-check

- Every changed line was found with a diff against `history/spec-v1.md`; no other line changed. 17 lines changed (git `--stat`: 17 insertions, 17 deletions).
- Text outside the findings was not touched: Decisions, section 4, section 8, section 9, UNVERIFIED list.
- Not done by design: no re-review, no PASS claimed, no Medium or minor finding repaired.
- Open consequence for the next reviewer to check: the P2 to P4 phase rows now carry the flag landing for their commands only by the section 3 intro and the P1 scope sentence; no per-phase acceptance row (AC-2.1, AC-3.x, AC-4.x) was changed, because none of the four findings names them.
