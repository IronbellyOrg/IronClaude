# Hypothesis: the scanner judges a word before it sees the next token, so it misreads `name()` and `{var}>`

**Agent**: root-cause-analyst (troubleshoot-analyst lens; returned as data, persisted by parent on receipt)
**Tier**: 1
**Timestamp**: 2026-11-04T16:49:35Z
**Cause class**: Parser/tokenizer logic error (lookahead missing)
**Claim class**: `static_defect`
**Evidence class**: `runtime_trace`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned
runs-in=src/superclaude/hooks/scripts/block-bare-python.sh:336 (exit 0, finding 2) and src/superclaude/hooks/scripts/block-bare-python.sh:340 (exit 2, finding 1) @ local bash + mawk, this worktree

## Claim
The awk scanner decides what a word is when the word ends, before looking at the next token. In `python3() {...}` the `(` branch calls endword (line 218), which prints `python3` (line 130) before line 219 sees `)`, so a definition is blocked (P5, :340). In `{fd}>/dev/null python3`, line 206 strips only a numeric fd word before `>`, so `{fd}` becomes the command word (lines 126-128) and `python3` is allowed (P4, :336).

## Evidence
- `src/superclaude/hooks/scripts/block-bare-python.sh:218` — `endword(o)` runs before `src/superclaude/hooks/scripts/block-bare-python.sh:219` — `if (substr(s, i + 1, 1) == ")") { i++; need[o] = !noc[o]; wrap[o] = ""; parg[o] = 0; return }`; `src/superclaude/hooks/scripts/block-bare-python.sh:130` has already printed.
- `src/superclaude/hooks/scripts/block-bare-python.sh:206` — `if (inw[o] && wd[o] ~ /^[0-9]+$/) { inw[o] = 0; wd[o] = ""; wq[o] = 0 } else endword(o)`.
- Trace (tier1-observation.md; tasklist rows P5-exact, P4-exact): `cmdword=python3` + `hook_exit=2`; `cmdword={fd}` + `hook_exit=0`; reference rows `2>/dev/null python3 -c 1` and `f() { python3 x.py; }` both `hook_exit=2` (P4-ref, P5-ref).
- behaviour-definition: row 1 (definition runs nothing; only `ready` printed). behaviour-definition: row 2 (`{varname}>` is part of the redirection; fake python3 ran).

## Proposed Fix
(a) In endword, before the command-word check, treat a word followed by `(`, optional blanks, `)` as a function name (no command word; need stays for the body); make the `(` branch accept blanks between `(` and `)` too. (b) At line 206 also accept an unquoted `{NAME}` word as an fd prefix. Mirror byte-for-byte; header and CHANGELOG lines; tests: allow `python3() { uv run python "$@"; }; echo ready` and `pip () { uv pip "$@"; }`; block `{fd}>/dev/null python3 -c 1`, `{in}</dev/null python3 x` and `f ( ) { python3 x; }`; keep `function-body` blocked.

## Confidence
Self-reported: 0.9
- Evidence grounding: 1.0 — lines read; traced words match.
- Runtime check: 1.0 — trace captured by the parent.
- Symptom coverage: 1.0 — both findings plus reference rows.
- Reproducibility fit: 1.0 — deterministic.
- Fix directness: 0.5 — two local edits; lookahead untested.
- Domain coherence: 1.0 — matches bash grammar.

## Risks
A lookahead that fires outside command position or on a later line could hide a real call; endword's END-of-input call has no remaining text, so it cannot match there.

## If I'm wrong, it's probably because...
The lookahead also fires inside a case pattern or array context; then the fix belongs only in the `(` branch.

## Falsification standard
After the fix: exit 0 on `{fd}>/dev/null python3 -c 1` refutes (b); exit 2 on `python3() { uv run python "$@"; }; echo ready` refutes (a); exit 0 on `f() { python3 x.py; }` means the fix broke the constraint.

## Evidence classification
- **Claim class**: static_defect — branch order in the scanner.
- **Evidence class**: runtime_trace.
- **Runtime check performed?**: yes, by the parent.
- **If REFUTE verdict, coverage statement**: Not applicable (AFFIRM).

## Alternatives considered
- Retracting the word in the `(` branch: rejected (line 130 already printed and exited).
- Treating `{` as a keyword prefix: rejected (`{fd}` is a redirection).

## Grounding gaps
- Diagnosability verdict partial (discovery cap). Quoted function names and `{a[1]}>` are left out of the fix.
