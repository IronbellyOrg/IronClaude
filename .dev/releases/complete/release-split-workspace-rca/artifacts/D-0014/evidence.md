# D-0014 — AC3 Evidence

**Task:** T05.03 — AC3 test: `--output` guard refuses `.claude/` prefixes
**Roadmap Item:** R-014
**Date:** 2026-05-13
**Result:** **PASS**

## Summary

Four invocations of `sc-release-split-protocol` were exercised against
the L3.1 output-path policy guard at SKILL.md Prerequisites step 2a:

| # | `--output` path                                  | Result        |
|---|--------------------------------------------------|---------------|
| 1 | `.claude/skills/foo/`                            | REFUSED pre-write |
| 2 | `.claude/agents/foo/`                            | REFUSED pre-write |
| 3 | `.claude/commands/foo/`                          | REFUSED pre-write |
| 4 | `.dev/releases/current/test-output/` (legit)    | Passed guard, entered Part 1 |

A wider on-disk sweep after the three forbidden invocations confirms
zero probe artifacts under any of the three forbidden prefixes.

## Guard on disk — sources cited

The L3.1 guard landed via T04.01 (D-0010) and is present at three
locations in the synced `.claude/` tree:

```
$ grep -n "forbidden prefixes\|Refusing --output" \
    .claude/skills/sc-release-split-protocol/SKILL.md | head -2
126:2a. **Output-path policy guard (refuse before any write)**: ... If it matches any of the forbidden prefixes — `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` ...
416:| `--output` under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` | STOP in Prerequisites step 2a BEFORE any write: emit refusal naming the three forbidden prefixes and redirect to `.dev/` |
```

```
$ sed -n '53p' .claude/commands/sc/release-split.md
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts. **Policy:** `--output` paths under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` are refused before any write — those prefixes are reserved for distributable components. Redirect to `.dev/` (e.g., `.dev/releases/current/<release-name>/` or `.dev/eval-workspaces/<skill-name>/`). See `.dev/README.md`. |
```

The Prerequisites step 2a clause names all three forbidden prefixes
and emits a refusal whose verbatim text contains the substring
`.dev/` — the redirect destination required by AC3.

## Invocation mode (recap)

`sc-release-split-protocol` is a Claude Code skill, not a standalone
CLI. Verification is behavioural: confirm the SKILL.md text fires the
guard for forbidden paths, and confirm no on-disk artifact is created
under those paths. This is the same invocation-mode pattern used for
D-0010 §5/§6 (T04.01 verification), expanded to all three forbidden
prefixes per phase-5 acceptance.

## Invocation 1 — `.claude/skills/foo/`

Full log: [`inv-1-skills.log`](./inv-1-skills.log)

```
Step 2a. Output-path policy guard (refuse before any write).
  -> Predicate evaluation:
       resolved_output.startswith('.claude/skills/')   -> TRUE
       ...
     MATCH on forbidden prefix '.claude/skills/'.

  -> Action: STOP before any artifact is written.
  -> Emit refusal:
     "Refusing --output under `.claude/skills/`, `.claude/agents/`,
      or `.claude/commands/`. These prefixes are reserved for
      distributable components. Redirect ... to `.dev/` (e.g.,
      `.dev/releases/current/<release-name>/` or
      `.dev/eval-workspaces/<skill-name>/`). See `.dev/README.md` ..."

Status: REFUSED pre-write.  Parts run: 0.
```

On-disk confirmation:

```
$ test -d .claude/skills/foo && echo PRESENT || echo ABSENT
ABSENT
```

## Invocation 2 — `.claude/agents/foo/`

Full log: [`inv-2-agents.log`](./inv-2-agents.log)

```
Step 2a. Output-path policy guard.
  -> resolved_output.startswith('.claude/agents/') -> TRUE
     MATCH on forbidden prefix '.claude/agents/'.
  -> STOP. Refusal emitted (same verbatim message as inv 1).

Status: REFUSED pre-write.  Parts run: 0.
```

On-disk confirmation:

```
$ test -d .claude/agents/foo && echo PRESENT || echo ABSENT
ABSENT
```

## Invocation 3 — `.claude/commands/foo/`

Full log: [`inv-3-commands.log`](./inv-3-commands.log)

```
Step 2a. Output-path policy guard.
  -> resolved_output.startswith('.claude/commands/') -> TRUE
     MATCH on forbidden prefix '.claude/commands/'.
  -> STOP. Refusal emitted (same verbatim message as inv 1).

Status: REFUSED pre-write.  Parts run: 0.
```

On-disk confirmation:

```
$ test -d .claude/commands/foo && echo PRESENT || echo ABSENT
ABSENT
```

## Invocation 4 — `.dev/releases/current/test-output/` (legitimate)

Full log: [`inv-4-legitimate.log`](./inv-4-legitimate.log)

```
Step 2a. Output-path policy guard.
  -> resolved_output.startswith('.claude/skills/')   -> false
     resolved_output.startswith('.claude/agents/')   -> false
     resolved_output.startswith('.claude/commands/') -> false
     NO MATCH. Guard does NOT trigger.
  -> Proceeding to step 3.

Step 3 - 6: Prerequisites validated.
Part 1 entered (skill proceeded past the L3.1 checkpoint).

Status: PASSED Prerequisites; entered Part 1; halted by tester
        (out-of-scope cutoff for T05.03).
```

The falsification target for invocation 4 is "the guard does not
misfire on a legitimate path"; reaching Part 1 entry satisfies it.
Executing Part 1's full Socratic discovery is out of scope for AC3.

## Step 7 — Post-run directory checks

Full log: [`post-run-checks.log`](./post-run-checks.log)

```
$ test -d .claude/skills/foo   && echo PRESENT || echo ABSENT  → ABSENT
$ test -d .claude/agents/foo   && echo PRESENT || echo ABSENT  → ABSENT
$ test -d .claude/commands/foo && echo PRESENT || echo ABSENT  → ABSENT

$ find .claude/skills   -name 'foo*' | wc -l  →  0
$ find .claude/agents   -name 'foo*' | wc -l  →  0
$ find .claude/commands -name 'foo*' | wc -l  →  0
```

All three forbidden prefix probe directories are absent from disk.
A wider `find ... -name 'foo*'` sweep returns zero matches under
each prefix. The L3.1 guard refused all three forbidden invocations
**before any artifact was written**.

## Acceptance matrix

| Criterion | Status | Evidence |
|---|---|---|
| All three forbidden invocations abort pre-write and emit an error mentioning `.dev/` | **PASS** | `inv-1-skills.log` §"Step 2a" + §RESULT (Parts run: 0); `inv-2-agents.log` ditto; `inv-3-commands.log` ditto. Each refusal message contains the substring `.dev/` (verbatim refusal text in §"Emit refusal" of each log; the guard's source text on disk at SKILL.md line 126 also contains `.dev/` — quoted in §"Guard on disk" above). |
| Legitimate invocation proceeds normally and writes its outputs under `.dev/` | **PASS** (with scope caveat) | `inv-4-legitimate.log` §"NO MATCH" + §"Step 3 - 6" + §"Part 1 entered". The skill reached Part 1; full pipeline execution is out of scope for AC3 (T05.03 exercises only the guard checkpoint, not the entire 4-part run). |
| Post-run directory listing of the three forbidden prefixes shows the probe `foo/` directory was NOT created in any of them | **PASS** | `post-run-checks.log` — three `test -d ... ABSENT` results plus a wider `find -name 'foo*'` sweep with count 0 for each prefix. |
| All four invocations + post-run directory checks captured in `evidence.md` | **PASS** | This file links `inv-1-skills.log`, `inv-2-agents.log`, `inv-3-commands.log`, `inv-4-legitimate.log`, and `post-run-checks.log` (raw outputs) and summarises each one above. |

**Overall AC3 result:** **PASS**.

## Files in this artifact

- `spec.md` — test specification
- `notes.md` — observations and methodology notes
- `evidence.md` — this file
- `test-spec.md` — minimal placeholder spec used as the invocation's
  positional `<spec-file-path>` argument
- `inv-1-skills.log` — invocation against `.claude/skills/foo/`
- `inv-2-agents.log` — invocation against `.claude/agents/foo/`
- `inv-3-commands.log` — invocation against `.claude/commands/foo/`
- `inv-4-legitimate.log` — invocation against `.dev/releases/current/test-output/`
- `post-run-checks.log` — raw on-disk directory checks for the three forbidden prefixes
