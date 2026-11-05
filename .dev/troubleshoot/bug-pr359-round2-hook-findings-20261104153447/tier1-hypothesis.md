# Hypothesis: the awk scanner breaks three bash parsing rules (an unquoted `[[`, process substitution counted as a word, backticks inside `$(( ))`), so it never reports `python3` and the hook exits 0 at line 326

**Agent**: root-cause-analyst (troubleshoot-analyst lens; returned as data, persisted by parent on receipt)
**Tier**: 1
**Timestamp**: 2026-11-04T15:40:01Z
**Cause class**: Logic error (incomplete grammar model in the parser)
**Claim class**: `static_defect`
**Evidence class**: `runtime_trace`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned (hook header lines 21-25 promise process substitution, $(( )) and [[ ]] handling; the code does not)
runs-in=src/superclaude/hooks/scripts/block-bare-python.sh:326 @ local bash + mawk, this worktree

## Claim
The scanner (1) treats a word that reads `[[` as a test opener even when quoted or escaped; (2) handles `<(...)`/`>(...)` like a subshell, so on close it sets the parent's need=0 and the redirect's skn stays set, swallowing the next word; (3) ignores backticks in arithmetic. In all three no `python3` word is printed, so producer P4 (`*) exit 0`, line 326) allows a command bash runs.

## Evidence
- `src/superclaude/hooks/scripts/block-bare-python.sh:153` — `if (c == "\\") { if (i == n) { i = n + 1; return }; i++; addc(o, substr(s, i, 1)); return }` drops the backslash without marking the word escaped, so `\[\[` reaches `src/superclaude/hooks/scripts/block-bare-python.sh:120` — `if (w == "[[") { tst[o] = 1; need[o] = 0; cmd[o] = w; return }`. behaviour-definition: row 1.
- `src/superclaude/hooks/scripts/block-bare-python.sh:196` — `if (nx == "(") { endword(o); i++; pushc("par"); return }` leaves skn set from the preceding `<`; `src/superclaude/hooks/scripts/block-bare-python.sh:219` — `if (t == "dol" || t == "par" || t == "arr") { d--; if (t == "par" && iscmd(ct[d])) need[d] = 0; return }`. behaviour-definition: row 2.
- `src/superclaude/hooks/scripts/block-bare-python.sh:267` — `function arithchar(s, n, c) {` handles only `(`, `)` and `$(` (line 270), no backtick. behaviour-definition: row 3.
- Trace (tier1-observation.md, trace-probe.out): no command word / `cmdword=printf` / `cmdword=echo`, `hook_exit=0` each; bash with a fake python3 printed `FAKE-PY ran` for all three and for `"[[" a ]]; python3 x`. Surviving producer P4 (`src/superclaude/hooks/scripts/block-bare-python.sh:326`); P1-P3 excluded (exit at :326 observed taken, producers.md).

## Proposed Fix
In the hook (mirrored byte-for-byte): (1) a per-context quoted-word flag set by backslash and quotes, cleared with the word; open the [[ test only for an unquoted, unescaped `[[`; (2) a `psub` context for `<(`/`>(` that clears skn on open (the substitution is the redirect target) and pops on `)` without touching need; (3) `arithchar` pushes a `bt` context on a backtick. Tests: block `\[\[ a \]\]; python3 x`, `"[[" a; python3 x`, `< <(printf "") python3 -c 1`, `2> >(tee l) python3 x`, `echo $(( \`python3 -c 1\` + 1 ))`; keep existing [[ ]] and process-subst cases.

## Confidence
Self-reported: 0.9
- Evidence grounding: 1.0 — cited lines plus matching trace.
- Runtime check: 1.0 — trace and fake-python3 run captured.
- Symptom coverage: 1.0 — all three plus the quoted variant.
- Reproducibility fit: 1.0 — deterministic.
- Fix directness: 1.0 — edits at the lines that lose the information.
- Domain coherence: 1.0 — one scanner.

## Risks
Gating reserved words on unquoted words changes quoted `"case"`/`"if"` handling (matches bash; can only add blocks). psub must stay in iscmd so `diff <(python3 a.py) b.txt` stays blocked. Mirror must stay byte-identical.

## If I'm wrong, it's probably because...
The text reaching awk differs from the probe input, so the miss comes from elsewhere in the scanner.

## Falsification standard
Run the three inputs and `"[[" a; python3 x` through the hook with only these edits: any exit 0 refutes that mechanism; a failing existing test refutes the fix.

## Evidence classification
- **Claim class**: static_defect — lost state at cited lines; bash semantics pinned by behaviour rows 1-3.
- **Evidence class**: runtime_trace.
- **Runtime check performed?**: yes, by the parent (tier1-observation.md).
- **If REFUTE verdict, coverage statement**: Not applicable (AFFIRM).

## Alternatives considered
- jq mangles the command: rejected (trace shows parsed words).
- A fail-open error path: rejected (P1-P3 excluded).

## Grounding gaps
- Diagnosability verdict partial (discovery-tool cap).
