# Hypothesis: the awk scanner chooses the wrong command word because it models three bash grammar rules incompletely: ANSI-C escapes, wrapper long options that take an argument, and `[[ ]]` operators

**Agent**: root-cause-analyst (troubleshoot-analyst lens; returned as data, persisted by parent on receipt)
**Tier**: 1
**Timestamp**: 2026-11-04T15:16:29Z
**Cause class**: Other: the tokenizer's model of shell grammar is incomplete (new scanner code from commit 1cfcb765; findings 1-2 bypass the input check, finding 3 is a false positive)
**Claim class**: `mixed` (an awk source defect plus the bash/getopt rules it must mirror)
**Evidence class**: `runtime_trace`
**Verdict direction**: AFFIRM
**Consistency with docs**: aligned. The header (lines 19-28) promises `$'...'` tracking and skipping wrappers "with their options"; neither the header ceilings (37-50) nor CHANGELOG.md:14 lists these cases, so the fix restores the documented contract.
runs-in=src/superclaude/hooks/scripts/block-bare-python.sh:275 @ local bash + awk (SAME-ENV yes)

## Claim
`endword`/`cmdchar`/`qchar` pick the wrong command word in three places. Inside `$'...'`, `qchar` drops only the backslash and never decodes the escape, so the word is `160ython3`. `endword` looks options up in `argopt` by exact token and the table holds only short forms, so `--signal TERM` leaves `TERM` as the timeout duration and `30` as the command word. After the command word `[[`, `cmdchar` treats `(` as a subshell and `|` as a pipe, so `python` inside the `=~` regex becomes a command word. In findings 1-2 the scanner prints nothing and the hook falls to P4 `*) exit 0`; in finding 3 it prints `python` and the hook exits 2.

## Evidence
- `src/superclaude/hooks/scripts/block-bare-python.sh:206` — `if (c == "\\") { i++; addc(o, substr(s, i, 1)); return }` copies the next character literally (`\160` -> `160`). Trace: `cmdword=160ython3`. bash decodes `\NNN` (behaviour-definition: row 1; `ansi-octal: FAKE-PYTHON3 ran: -c 1`).
- `src/superclaude/hooks/scripts/block-bare-python.sh:98` — `if ((wrap[o], w) in argopt) parg[o] = 1`; `:101` — `if (wrap[o] == "timeout") { wrap[o] = "timeout-duration"; return }`; table `:234-239` holds short options only. Trace: `cmdword=30`. Probe: `--signal=TERM` and `-s TERM` give exit 2. A long option without `=` consumes the next word (behaviour-definition: row 2, row 4; timeout-long, nice-long, env-long ran the fake python3).
- `src/superclaude/hooks/scripts/block-bare-python.sh:191` — `pushc("par"); return` runs for `(` after `[[` (need is 0, so `:190` is skipped), opening a new command context. Trace: `cmdword=[[` then `cmdword=python`. bash treats `(`/`|` inside `[[ =~ ]]` as regex text (behaviour-definition: row 3; `dbl-bracket: matched`, no python ran).
- Producer P4 (`src/superclaude/hooks/scripts/block-bare-python.sh:275`, surviving=yes) produced the exit-0 token in findings 1-2; P1-P3 excluded because `:275` was observed taken (tier1-observation.md: every hook_exit matches scanner_out).

## Proposed Fix
One awk change set in `src/superclaude/hooks/scripts/block-bare-python.sh`: (1) in the `qchar` ansi branch decode `\` + 1-3 octal digits, `\x` + 1-2 hex, `\u`/`\U` + 4/8 hex, `a b e E f n r t v`, `cX`, other characters literally; hex/octal helpers (mawk has no strtonum); codes 1-127 via `sprintf("%c", n)` (behaviour-definition: row 5), others `?`. (2) add argument-taking long options per wrapper and consume the next word for `--x` without `=` when it names (or abbreviates) one of them; also handle clustered short options. (3) after the command word `[[`, treat `( ) | & < >` as word characters until the word `]]`; `$(...)` and backticks inside `[[` are still scanned. Copy the script byte-for-byte to `plugins/superclaude/hooks/scripts/block-bare-python.sh`; update header ceilings and CHANGELOG. Tests in `tests/hooks/test_block_bare_python.py`: BLOCKED ANSI forms, long-option forms, abbreviated `--sig`, `[[ -n x ]] && python3 x`, `[[ $(python3 -c 1) ]]`; ALLOWED the `=~` alternation case and `[[ a < b ]] && echo ok`; the 100 KB timing test stays green.

## Confidence
Self-reported: 0.90
- Evidence grounding: 1.0 — each mechanism is a quoted source line plus a trace line.
- Runtime check: 1.0 — trace probe and hook probe outputs captured (tier1-observation.md).
- Symptom coverage: 1.0 — all three findings and both control cases explained.
- Reproducibility fit: 1.0 — deterministic.
- Fix directness: 1.0 — each edit changes the line that chose the wrong word.
- Domain coherence: 1.0 — all three are the scanner diverging from bash/getopt grammar.

## Risks
A newline inside `[[ ]]` could reset the test context (false positive, not a bypass). Abbreviation matching could consume a word after an ambiguous `--x` (only when the wrapper itself would reject the option). A non-byte-identical mirror fails `tests/cli/test_install_hooks.py`.

## If I'm wrong, it's probably because...
The installed awk treats `\` in the program string or `%c` differently, putting the defect in the awk implementation rather than the scanner logic (row 5 observed `%c(112)=p` on mawk 1.3.4).

## Falsification standard
After only these edits, re-run probe.sh: every finding-1/2 row must show `hook_exit=2 scanner_out=python3`, the `=~` row `hook_exit=0`, and the `[[ -n x ]] && python3 x` row `hook_exit=2`; any other result refutes the mechanism/fix pairing.

## Evidence classification
- **Claim class**: mixed — awk source defect judged against bash/getopt semantics (rows 1-5).
- **Evidence class**: runtime_trace — read-only scanner copy printed each chosen word; hook probe shows exit codes.
- **Runtime check performed?**: yes, by the parent (tier1-observation.md 15:03Z, 15:07Z, 15:08Z, 15:16Z).
- **If REFUTE verdict, coverage statement**: Not applicable (AFFIRM).

## Alternatives considered
- Fail-open producers P1-P3: rejected; the scanner ran and `:275` was observed taken.
- Three separate causes: rejected; all are wrong command-word choices in one scanner with one fix site.
- Replace awk with a shell parser: rejected; plan requires awk, no Python, 100 KB under 1 s.

## Grounding gaps
- Diagnosability verdict partial (degraded discovery) — see diagnosability-context.md; mechanisms observed directly.
- GNU time is not installed here; `time --format/--output` names are recalled, not fetched (not load-bearing).
