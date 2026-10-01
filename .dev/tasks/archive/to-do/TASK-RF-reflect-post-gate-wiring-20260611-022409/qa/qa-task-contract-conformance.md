# QA — Agent A: Contract-Conformance Lens (relayed from inline return)

VERDICT: FAIL (as raw lens output) — but ALL findings adjudicated FALSE POSITIVES by the executor consolidation (`qa-task-consolidated.md`).

## Raw findings + executor adjudication

- **F1 (raised CRITICAL): O2 appends `--output …` not in §2 minimal invocation shape.**
  → REJECTED. `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` is REQUIRED by item 3.1 + research GAP-3 (the wrapper default `<dir>/reflect/post/<sha>/` orphans the declared `**Reflect Report Path:**` + its Acceptance Criterion). `--output` is a real, allowed flag; the §2 "MUST NOT emit" list is `--reflect`/`--max-turns`/`<base>..HEAD` only.
- **F2/F3 (IMPORTANT): forbidden tokens `--reflect`/`--max-turns`/`<base>..HEAD`/`start_commit..HEAD` appear in the emission blocks.**
  → REJECTED. They appear ONLY in negative prohibition prose ("Emit NO `--reflect`…") and base-resolution contrast (`start_commit..HEAD` as the wrong form). Not emitted as command args. Agent A acknowledged "these are negative/prohibitive prose mentions, not actual command arguments."
- **F4/F5 (IMPORTANT): PRE depth tables still permit `quick`.**
  → REJECTED. PRE uses `/sc:reflect --mode pre` (NOT the wrapper `superclaude reflect run`); the contract's `--depth standard|deep` constrains the wrapper. PRE is explicitly OUT OF SCOPE / INTACT; `quick` for PRE is intended (no diff pre-execution).

## Confirmed PASSes (Agent A)
O1 command shape `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` (--base omitted); O2 `--depth deep --fix --no-promote --base <PHASE_N_START_SHA>` byte-identical across both O2 files; §3.2 skip guard verbatim at both O1+O2; `--promote`(O1)/`--no-promote`(O2) per §5; frontmatter keys present.

See `qa-task-consolidated.md` for the full triage.
