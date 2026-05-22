# D-0107 Follow-up — Strip `time_offset_sec` from `HomeIsolation` (DOC-OQ8 path b)

**Parent task:** T06.03 — DOC-OQ8 time-offset mechanism contract decision
**Sibling artifacts:** `artifacts/D-0107/{spec.md,notes.md,evidence.md}`
**Owner:** RyanW (architect; same owner as the OPS-001 §B OQ-8 row)
**Status:** OPEN — TRACKED-DEFERRED (lands in v1.0.1 / next minor cut after v1)
**Created:** 2026-05-20 (DOC-OQ8 closure follow-up)

---

## 1. Why this follow-up exists

The R7 DOC-OQ8 closure (`decisions.md` §"DOC-OQ8 Closure") records path
(b): the `CLAUDE_FAKE_TIME_OFFSET` env-var contract is removed from
FR-ISO1 scope. Step 4 of T06.03 says: *"If removed, file follow-up
task to strip `time_offset_sec` from `HomeIsolation`."* This artifact
is that follow-up.

The ADR retains the `time_offset_sec: int = 0` field at v1 ship as
dead-but-typed scaffolding to keep the M6 exit gate decoupled from a
STRICT-tier refactor under same-day review. The strip lands in the
next release cycle after v1.0 so v1 callers (none of which set the
field non-zero — see `artifacts/D-0107/evidence.md` §"Repository
audit") have a deprecation hop.

## 2. Scope — what changes when this follow-up lands

### 2.1 Code edits (proposed v1.0.1)

| File | Lines (per audit at 2026-05-20) | Edit |
|---|---|---|
| `src/superclaude/cli/eval/isolation.py` | 14-19 | Remove the `(``CLAUDE_FAKE_TIME_OFFSET``)` clause from the opening module docstring. |
| `src/superclaude/cli/eval/isolation.py` | 44-49 | Remove the entire `4. ``time_offset_sec``` paragraph from the DM-006 record docstring. |
| `src/superclaude/cli/eval/isolation.py` | 64-67 | Remove the `and ``CLAUDE_FAKE_TIME_OFFSET`` only when ``time_offset_sec != 0``` clause from the `env()` description; rephrase to `and ``CLAUDE_SESSION_ID``` only. |
| `src/superclaude/cli/eval/isolation.py` | 90 | Remove the `* DOC-OQ8 (T06.03) — gates ``CLAUDE_FAKE_TIME_OFFSET`` semantics.` cross-link. |
| `src/superclaude/cli/eval/isolation.py` | 373-376 | Remove the `time_offset_sec` field paragraph from the class docstring. |
| `src/superclaude/cli/eval/isolation.py` | 388 | Remove the `time_offset_sec: int = 0` field declaration from the `@dataclass(frozen=True)` body. |
| `src/superclaude/cli/eval/isolation.py` | 595-602 | Remove the third bullet (`* ``CLAUDE_FAKE_TIME_OFFSET`` is present only when …`) from the `env()` docstring. |
| `src/superclaude/cli/eval/isolation.py` | 614-619 | Remove the `if self.time_offset_sec != 0: env["CLAUDE_FAKE_TIME_OFFSET"] = ...` branch from `env()`. |
| `src/superclaude/cli/eval/models.py` | 552 | Remove the `time_offset_sec` reference from the COMP-006 docstring. |
| `src/superclaude/cli/eval/claude_process.py` | 113 | Remove `, optional CLAUDE_FAKE_TIME_OFFSET` from the env-overlay description. |
| `src/superclaude/cli/eval/claude_process.py` | 241 | Remove the `and optional ``CLAUDE_FAKE_TIME_OFFSET``` clause from the docstring. |

### 2.2 Test edits

| File | Edit |
|---|---|
| `tests/cli/eval/test_home_isolation.py` | Remove the `time_offset_sec` non-zero / zero pair of assertions (~lines 348, 359) along with their construction fixtures. |
| `tests/cli/eval/test_home_isolation_extend.py` | Remove the `time_offset_sec` block (module docstring lines 6-17 and the two test cases at ~249 and ~269 that assert env-var emission and omission). |
| `tests/cli/eval/test_isolation_layers_probe.py` | Remove the `CLAUDE_FAKE_TIME_OFFSET` mention in the module docstring (line 8). |
| `tests/cli/eval/test_isolation_dataclass.py` | Remove the `DOC-OQ8 (T06.03)` cross-link line (16). |

### 2.3 Spec / docs edits

| File | Edit |
|---|---|
| `.dev/releases/current/cliEval/design-spec.md:372` | Remove the §8 row `\| **Time offset** \| `CLAUDE_FAKE_TIME_OFFSET` \| Optional; lets evals advance the clock for 30-min freshness tests (E3) \|`. |
| `.dev/releases/current/cliEval/design-spec.md:382` | Remove the `time_offset_sec: int = 0` line from the `HomeIsolation` interface signature. |
| `.dev/releases/current/cliEval/roadmap.md:28,134,136` | Reword the FR-ISO1 / DM-006 lines that mention "time-offset layers". |
| `.dev/releases/current/cliEval/decisions.md` (§"DOC-OQ8 Closure") | Amend with an `Outcome:` line citing the v1.0.1 cut where the strip landed; the original `Resolution:` text stays for audit. |
| Release notes (v1.0.1) | Add a deprecation-completion line: *"v1.0.1 strips the dead-but-typed `time_offset_sec` field per the R7 DOC-OQ8 closure recorded in v1.0."* |

## 3. Risks + sequencing

1. **Positional-arg breakage.** Any v1.0 consumer that constructs
   `HomeIsolation(eval_id, home_root, session_id, time_offset_sec)`
   positionally would break on v1.0.1's field removal. The strip
   should land behind a deprecation warning in a v1.0.1-rc cut and the
   field removal in v1.1, OR — if the v1.0.1 audit shows zero
   positional-arg consumers — directly in v1.0.1.
2. **Test data dependency.** `test_home_isolation_extend.py` (lines
   249, 269) explicitly tests the `env()` emission contract. Removing
   the field invalidates the test; the test must be deleted alongside
   the field, not before.
3. **Pre-existing forks of the harness.** Any external fork that
   already vendors the dead field gets the deprecation warning first.
4. **STRICT-tier review.** The strip touches T02.07 (FR-ISO1), which
   is a STRICT-tier surface. The v1.0.1 release task that consumes
   this follow-up runs through the full Section 5.3.2 review path.

## 4. Acceptance — when this follow-up closes

- All §2.1 / §2.2 / §2.3 edits land.
- `grep -rn 'time_offset_sec\|CLAUDE_FAKE_TIME_OFFSET' src/superclaude/ tests/` returns zero hits.
- `decisions.md` §"DOC-OQ8 Closure" is amended with an `Outcome:` line
  citing the v1.0.1 commit / tag where the strip landed.
- This artifact (`artifacts/D-0107-followup-strip-time-offset.md`) is
  amended with a final `Status: CLOSED — <date>` line; the body stays
  for audit.
- The v1.0.1 release notes name the strip as a completed deprecation
  item.

## 5. Cross-links

- Parent ADR: `decisions.md` §"DOC-OQ8 Closure" (R7, 2026-05-20).
- Parent task: `phase-6-tasklist.md` §T06.03.
- Parent OQ row: `decisions.md` §"OPS-001 Closure" §B (OQ-8 row, R7 update).
- Test surface: `tests/cli/eval/test_home_isolation.py`,
  `tests/cli/eval/test_home_isolation_extend.py`,
  `tests/cli/eval/test_isolation_layers_probe.py`,
  `tests/cli/eval/test_isolation_dataclass.py`.
- Downstream consumer: future v1.0.1 release task (TBD; will reference
  this artifact's §2 line items as its scope).
