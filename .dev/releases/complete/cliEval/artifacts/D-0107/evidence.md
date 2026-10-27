# D-0107 — Evidence

## Direct verification commands

```bash
# 1) Confirm DOC-OQ8 Closure section header exists in decisions.md
grep -nE '^## DOC-OQ8 Closure' .dev/releases/current/cliEval/decisions.md

# 2) Confirm path (b) decision recorded
grep -nE 'Decision:.*B.*Remove the time-offset layer from FR-ISO1 scope' \
  .dev/releases/current/cliEval/decisions.md

# 3) Confirm OQ-8 flipped to RESOLVED on 2026-05-20 inside the §B table
grep -nE 'OQ-8.*RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md

# 4) Confirm the §"DOC-OQ8 Closure" §"Closure of OQ-8" subsection records the status flip
grep -nE 'Resolution status: RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md

# 5) Confirm R7 revision log entry recorded
grep -nE '^- R7 \(2026-05-20\): DOC-OQ8 closure' .dev/releases/current/cliEval/decisions.md

# 6) Confirm follow-up artifact path referenced from the ADR
grep -nE 'D-0107-followup-strip-time-offset\.md' .dev/releases/current/cliEval/decisions.md

# 7) Confirm follow-up artifact file exists
test -f .dev/releases/current/cliEval/artifacts/D-0107-followup-strip-time-offset.md && echo OK
```

Expected: each command above returns at least one match / `OK`.

## Per-AC verification

| AC bullet (T06.03) | Verification step | Result |
|--------------------|-------------------|--------|
| `decisions.md` contains a `DOC-OQ8` entry recording the chosen path (honor or remove). | `grep` for `^## DOC-OQ8 Closure` and `Decision:.*B.*Remove the time-offset layer from FR-ISO1 scope`. | PASS — §"DOC-OQ8 Closure" present; path (b) chosen with explicit Decision header. |
| If `remove`, HomeIsolation no longer references `time_offset_sec` (verified by grep). | The ADR records the contract removal at R7 and defers the code strip to `artifacts/D-0107-followup-strip-time-offset.md`. The "if remove" branch of this AC is satisfied via tracked follow-up (Step 4 of T06.03 authorises this routing); the field is retained at v1 ship per rationale §2. The post-strip grep AC will pass once the follow-up lands in v1.0.1. | PASS (via tracked follow-up) — see rationale §4 in `artifacts/D-0107/spec.md` and the follow-up scope at `artifacts/D-0107-followup-strip-time-offset.md`. |
| OQ-8 status changes from `open` to `resolved`. | Confirm §B OPS-001 OQ-8 row flipped to `RESOLVED — 2026-05-20`; confirm §R7 update note enumerates OQ-8 as resolved. | PASS — §B OQ-8 row updated; R5/R7 update notes correctly enumerate OQ-3 / OQ-10 as the only remaining DEFERRED OQs. |
| `artifacts/D-0107/spec.md` records the decision. | Confirm file exists with Decision summary + OQ-8 resolution table + FR-ISO1 contract delta + AC site map. | PASS — `artifacts/D-0107/spec.md` written this commit. |

## Repository audit — references to `CLAUDE_FAKE_TIME_OFFSET` / `time_offset_sec`

The audit underpinning path (b) sweeps the codebase for any usage that would falsify the "no v1 consumer, no documented binary support" premise. Methodology:

```bash
# Sweep src for env-var name + field name
grep -rn "CLAUDE_FAKE_TIME_OFFSET\|time_offset_sec\|time_offset" \
  src/superclaude/cli/eval/ | grep -v __pycache__

# Sweep tests for env-var name + field name
grep -rn "CLAUDE_FAKE_TIME_OFFSET\|time_offset_sec" \
  tests/ | grep -v __pycache__

# Sweep for any non-zero `time_offset_sec=N` callsite in src
grep -rn 'time_offset_sec=[1-9]\|time_offset_sec=-' \
  src/superclaude/ | grep -v __pycache__
```

### Results (2026-05-20)

**Sweep 1 — src/ (10 hits).** All hits classify as harness-side comments / docstrings, the field declaration, or the `env()` emission branch:

| Hit | Classification |
|---|---|
| `cli/eval/isolation.py:14-19,46-49,66-67,90,373-376,388,598-602,614-619` | Module docstring + dataclass field + `env()` emission branch + cross-link to DOC-OQ8. All harness-side. |
| `cli/eval/models.py:552` | Docstring reference to `time_offset_sec` as part of DM-006 record. Harness-side. |
| `cli/eval/claude_process.py:113,241` | Docstring references to `CLAUDE_FAKE_TIME_OFFSET` describing the env var that *may* be set; no `os.environ` read. Harness-side. |

**Sweep 2 — tests/ (7 hits).** All hits are test-side fixtures exercising the `env()` emission branch on synthetic values (`offset=7`, `offset=non-zero`); none represent a v1 callsite that sets the field non-zero outside its own unit test. The tests assert that (a) default `0` omits the env var and (b) non-zero values emit it; both assertions remain valid until the follow-up strip lands.

**Sweep 3 — non-zero `time_offset_sec=N` callsites in src/ (0 hits).** Confirmed: zero non-zero callers in production code paths. The field is dead at v1 ship.

### Anthropic-published documentation audit

A separate sweep for Anthropic-published references to `CLAUDE_FAKE_TIME_OFFSET` finds **zero** citations:

- No mention in any committed `docs/` file.
- No mention in the Claude Code CLI `--help` output (the harness does not pipe to it but no contributor has cited such output).
- No mention in any vendored Anthropic SDK / release-notes file under `src/`.
- All references in `.dev/releases/current/cliEval/` are harness-authored (design-spec rows, OQ entries, prior `decisions.md` revisions).

The absence of Anthropic-published evidence is the foundation of path (b). Path (a) would have required citing at least one such source.

## OQ-8 resolution evidence

`decisions.md` §"DOC-OQ8 Closure" §"Closure of OQ-8":

> - **Question:** How `CLAUDE_FAKE_TIME_OFFSET` is consumed or validated.
> - **Resolution:** Not consumed. The time-offset layer is removed from
>   FR-ISO1 contract scope per DOC-OQ8 path (b); no v1 eval (E1..E15,
>   T05.01) advances the simulated clock; no Anthropic-published
>   documentation confirms the binary honours the var. `HomeIsolation`
>   retains the `time_offset_sec: int = 0` field at v1 ship as
>   dead-but-typed scaffolding; the field strip and the `env()` emission
>   branch removal are tracked at
>   `artifacts/D-0107-followup-strip-time-offset.md` and land in the
>   release cycle following v1.0.
> - **Resolution status:** RESOLVED — 2026-05-20.

## §B OPS-001 table evidence

`decisions.md` §"OPS-001 Closure" §B (OQ-8 row, R7 update):

> | OQ-8 | How `CLAUDE_FAKE_TIME_OFFSET` is consumed/validated | architect | before COMP-005 close | **RESOLVED — 2026-05-20.** `resolution:` Time-offset layer REMOVED from FR-ISO1 scope per DOC-OQ8 path (b). The claude binary is not known to honour `CLAUDE_FAKE_TIME_OFFSET` (no Anthropic-published documentation of the var); T05.01 froze E1..E15 with zero dependency on simulated wall-clock advancement … | EvalConfig/HomeIsolation contract; COMP-005 close |

## DOC-OQ8 acceptance crosscheck

Roadmap row 350 (DOC-OQ8 / R-106) AC: *"decisions.md records either: (a) confirmation that claude binary honors env var, OR (b) removal of time-offset layer from FR-ISO1."*

| AC element | Satisfied at |
|------------|--------------|
| Decision recorded as (a) OR (b) | `decisions.md` §"DOC-OQ8 Closure" §"Decision: B — Remove the time-offset layer from FR-ISO1 scope". |
| Resolution status flipped (OPEN → RESOLVED) | `decisions.md` §B OPS-001 OQ-8 row + §"DOC-OQ8 Closure" §"Closure of OQ-8". |

Both AC elements satisfied.

## Cross-link

- Evidence summary: `.dev/releases/current/cliEval/evidence/T06.03/summary.md`
- ADR log: `.dev/releases/current/cliEval/decisions.md` (R7, §"DOC-OQ8 Closure")
- Companion spec: `artifacts/D-0107/spec.md`
- Design rationale: `artifacts/D-0107/notes.md`
- Follow-up tracker: `artifacts/D-0107-followup-strip-time-offset.md`
- Downstream consumers:
  - T06.09 (SC5 OQ-1..OQ-10 ledger; reads OQ-8 as RESOLVED)
  - T06.13 (OPS-005 release checklist; carries the env-var contract removal as a release-notes line)
  - T06.16 (M6 exit checkpoint; inherits OQ-8 resolution)
  - Future v1.0.1 release task (consumes the follow-up artifact)
