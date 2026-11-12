# Verification review: ARCHITECTURE-SPINE.md fix cycle 1

**Verdict:** FAIL

Reviewer: fresh-context adversarial verifier, 2026-11-08. Inputs: the spine, the three cycle-1 reviews (rubric-walker, web-verification, adversary), `.memlog.md`, the spec package `_bmad-output/specs/spec-orca-observer/`, `inputs/`, and the brownfield code at `IronClaude/issue-409-mvp/src/superclaude/cli/` (read only).

## Verdict

**FAIL.** Of the 28 earlier blocking findings, 25 are RESOLVED, 3 are PARTIAL (B7, B9, ADV-13) and 0 are OPEN. PARTIAL counts as open, so 3 earlier items are still unresolved. The fixes also introduced 1 new blocking defect (NEW-1).

| Count | Value |
|---|---|
| Resolved | 25 |
| Partial (counts as open) | 3 |
| Open | 0 |
| New blocking | 1 |

The most important item is NEW-1, together with B9. AD-6 shows `one Run only` only when the observer itself binds `--run`. The spec requires that text whenever `scope.source` is `bound`. So an unbound observer in a terminal that is bound to a Run would show one Run as if it were the whole fleet, which is the exact risk the spec names. In the same AD, `read k of N Runs since start` is labelled PROPOSED but never defined.

## Prior blocking findings table

Line numbers refer to ARCHITECTURE-SPINE.md as read on 2026-11-08.

### Rubric walker (11)

| ID | Status | Evidence (spine) |
|---|---|---|
| B1 discovery seam | RESOLVED | AD-3 (l.88): "declares `Discover = Callable[[], str \| None]`, defaulting to `_find_orca` ... Tests inject a fake `Discover` that appends the probe argv to the same argv log" |
| B2 namespace | RESOLVED | AD-7 (l.112): "`source.namespace` is not an Orca field: it is derived by the observer (PROPOSED...)" |
| B3 snapshot vs filter | RESOLVED | AD-10 has `all_rows` and `visible_rows`. AD-11: "Both read only `view.all_rows`", with a byte-identical `snapshot_json` test across two sessions. |
| B4 change flags | RESOLVED | AD-15 (l.160): rows are "flagged `*` when it was added, removed, or" changed, with the `changed since HH:MM (k)` count. The restart disclosure is labelled PROPOSED. |
| B5 CD-6 resolved UX-OQ-4 | RESOLVED | CD-6 (l.300): "`e` shows `export disabled (destination undecided)` and each live snapshot write is skipped and counted". The snapshot envelope is now conditional on CD-6. |
| B6 CD-9 scope | RESOLVED | CD-9: "OQ-5 covers message samples only ... golden `worker-list` sample and T32 are R0 scope". AD-16 falls back to the synthetic `base` variant. See the minor note on who captures the sample. |
| B7 fixture data path | **PARTIAL** | Replay is fixed: AD-16 says "R0 replay runs as render tests through `FixtureSource`", and the header literal is assigned. The question data is still missing. AD-16 (l.166) only says "Fixture-only question rows (T7) come from a fixture question model loaded by the fixture loader (PROPOSED)". No field in `CycleResult` (AD-20) or `View` (AD-10) carries that model, so T7 rows have no path from the loader to `build_view` or the render. |
| B8 merge owner | RESOLVED | AD-19: `parse.merge(previous, pages, stopped_by_cap, clock) -> (Snapshot, Coverage)`. Only the collector calls it. |
| B9 Run counting | **PARTIAL** | AD-6 (l.106): "How `read k of N Runs since start` is counted and whether Runs rotate under the cap are PROPOSED (placement is CD-10)". The label is there but nothing defines it. There is no counter owner, no definition of k or N, and no rule for what restarts the count. The R0 degraded header and T45 both need this string. |
| B10 CD-16 resolved UX-OQ-8 | RESOLVED | CD-16 (l.310): "Each row names its shared `worktreeId`, and a row with none reads `worktree unknown`, because T20 requires it". Placement stays open. |
| B11 scope field | RESOLVED | AD-12 (l.142): "`scope` (always emitted: the source object passed through, or the string `UNKNOWN` when absent)" |

### Web verification (1)

| ID | Status | Evidence (spine) |
|---|---|---|
| F1 Windows / POSIX imports | RESOLVED | AD-1 says "`keys.py` is imported lazily ... no module on the `--once` import chain imports a POSIX-only module". AD-5 uses "`os.killpg(SIGKILL)` on POSIX, `proc.kill()` elsewhere" (PROPOSED). AD-14 adds a test that imports `commands.py` with `termios` blocked. Brownfield check: no `termios`, `tty` or `fcntl` import exists anywhere under `superclaude/cli/`, and `main.py` imports only `sys`, `pathlib`, `click` and its deferred subgroups at top level. |

### Adversary (16)

| ID | Status | Evidence (spine) |
|---|---|---|
| ADV-01 merge | RESOLVED | AD-19 is the single merge function. |
| ADV-02 coverage owner | RESOLVED | AD-19 returns and owns `Coverage`. |
| ADV-03 session purity | RESOLVED | AD-15: `apply_cycle(session, result, clock)` and `apply_key(session, key, view, clock) -> (Session, Effect)` |
| ADV-04 baseline | RESOLVED | AD-15: `baseline: Mapping[Identity, tuple]`. Added, removed and changed rows are all counted. |
| ADV-05 export rows | RESOLVED | AD-10 and AD-11 export from `all_rows`. |
| ADV-06 snapshot write cadence | RESOLVED | AD-20 `last_written_cycle` means one write per new cycle, skipped and counted until CD-6 is decided. See the minor note on the Textual fallback and `--once`. |
| ADV-07 state precedence | RESOLVED | AD-20: NOT_AVAILABLE > NOT_POLLED > FAILED > STALE > OK. FAILED over STALE is labelled PROPOSED. Uses the AD-5 code set and the AD-12 mapping. |
| ADV-08 staleness owner | RESOLVED | AD-6: "computes no staleness". The `view.py` code derives it from the injected clock (Time convention). |
| ADV-09 unknown sentinel | RESOLVED | `view.py` re-exports `UNKNOWN`, and the known limit is recorded. See the minor note on display words versus the sentinel. |
| ADV-10 literal ownership | RESOLVED | The display literals live in `view.py` (AD-8 and AD-10). |
| ADV-11 ordering | RESOLVED | `source_rank` is used, and `view.py` owns both sort orders. |
| ADV-12 Key type | RESOLVED | `Key` lives in `view.py`, and the diagram has a `keys --> view` edge. |
| ADV-13 fixture wiring | **PARTIAL** | The wiring is fixed. AD-6 defines `Collector(source: CycleSource, clock)` with `LiveSource(runner, discover)` and `FixtureSource(variant)`, plus `run_once()`. The diagram has a `commands --> adapter` edge, and `CycleResult` carries the mode and the variant. The path that delivers fixture extras, meaning the question model for T7, is still missing. This has the same root cause as B7. |
| ADV-14 discovery seam | RESOLVED | AD-3 `Discover` (see B1). |
| ADV-15 sanitizer modes | RESOLVED | AD-9 defines line mode and block mode. A test covers `\n` inside a `dispatchId`. |
| ADV-16 output encoding | RESOLVED | AD-11 writes with `sys.stdout.write` and an explicit `output_encoding`. AD-13 sets `highlight=False`. See the minor note on bytes versus str. |

## New blocking findings

### NEW-1 `one Run only` is tied to the observer's `--run` option instead of `scope.source=bound` (wrong behaviour, introduced by the B9 fix)

- **Spine, AD-6 (l.106):** "Polling is unbound by default: `--run` is added only when the user binds a Run with an observer option, and the header then adds `one Run only`."
- **Spec, adapter-contract.md:63:** "`result.scope.source` (`flag`, `bound` or `all`, per help) is shown in the header; absent reads `scope unknown`; `bound` adds `one Run only`".
- **Spec, owner-decisions-and-risks.md:44, risk table:** "Bound scope shows one Run as the fleet | Missed orchestrators | `scope.source` in the header, `one Run only`, `read k of N Runs since start`".
- **Spec, unverified-register.md:20:** when no `--run` is passed, Orca reports the bound Run as the scope.

**Why this blocks.** The spec takes the trigger from the source (`scope.source == "bound"`), not from the observer's own option. The default case is an unbound observer running in an Orca terminal that is already bound to a Run. That terminal gets `scope.source=bound`, but under AD-6 its header would not show `one Run only`. That is the "one Run shown as the fleet" failure the risk table exists to prevent.

The rule also puts the decision in the wrong module. `commands.py` or `adapter.py` would make it from the CLI option, when `view.py` should derive it from the parsed `scope`.

AD-8's list of display literals also leaves out `one Run only`, so nothing assigns the string an owner.

**Fix needed.** AD-6 or AD-10 should say that `view.py` adds `one Run only` whenever the parsed `scope.source == "bound"`, whatever the observer's options. Add the literal to AD-8. Add a test that builds a `CycleResult` with `scope.source=bound` and no observer `--run`, and asserts the header shows `one Run only`.

## Minor notes

None of these causes the FAIL.

1. **B6 sample capture.** CD-9 puts the live golden `worker-list` sample in R0, but R0 is described as offline only. The spine does not say who captures the sample or when.
2. **T50 header words.** These are labelled PROPOSED, but they are spec wording (rendering-rules:17). The label is over-cautious; it does not invent anything.
3. **ADV-06 follow-on.** No rule says the Textual fallback keeps the per-cycle snapshot write. The `--once` snapshot behaviour is also not stated beyond printing `record_text`.
4. **ADV-09 follow-on.** It is not explicit whether `View` holds raw values plus the `UNKNOWN` sentinel, display words, or both. Renderers need both.
5. **ADV-11 follow-on.** The sort rank of retained rows (dropped and kept with `reobserved=False`) is not stated.
6. **CAP-9 vs AD-11.** `record_text` reads `all_rows`, while CAP-9 says "same view the screen shows". The spine marks this PROPOSED; the owner should confirm it.
7. **AD-11 bytes vs str.** AD-11 encodes the text to bytes and then calls `sys.stdout.write`, which takes a str. Use `sys.stdout.buffer.write`, or write the str after setting `errors=`.
8. **AD-14 terminal restore.** It says "restores the saved attributes" without naming `termios.tcgetattr` / `tcsetattr(TCSADRAIN)` (web-verification F7).
9. **F2 no_color.** The false case of `no_color` is not passed explicitly to `Console`.
10. **AD-5 codes.** `cycle overran (Ns)` (AD-6) is not in the AD-5 failure-code set.
11. **AD-10 words.** `unknown (absent in source)` is not in AD-10's list of unknown words.
12. **M8.** The T12 wording is still loose.
13. **AD-8 literals.** `one Run only` is missing from the AD-8 literal list. This is folded into NEW-1.

## Self-Audit

The verdict is FAIL, so a Self-Audit is not required. This section is kept for traceability.

**Binding rules**
- **Rule 1 (R1 read-only toward Orca): holds.** AD-17, the adapter allowlist and the argv-log test.
- **Rule 2 (Python + Rich, additive-only JSON snapshot, spike first, Textual only if the spike fails): holds.** AD-12 and AD-14 plus CD-7.
- **Rule 3 (no invented Orca fields): holds.** Observer-derived values carry PROPOSED or UNVERIFIED labels, for example `source.namespace` in AD-7 and the backoff and output-cap labels.
- **Rule 4 (owner questions not resolved): holds.** I checked CD-1 to CD-16. CD-9's narrowing matches open owner decision 6. CD-16's default is justified by T20 and leaves placement open. CD-14 follows recorded owner decision 1.
- **Rule 5 (unknown never becomes zero): holds.** AD-8 and AD-10, plus the `UNKNOWN` sentinel in AD-12.
- **Rule 6 (every AD has Binds, Prevents and Rule): holds.** All of AD-1 to AD-20 have all three.

**Capability Map.** Every row cites ADs that cover the capability. I found no wrong citation.

**Brownfield claims, all confirmed by reading the code.**
- `install_user_setup.py`, around line 198: `_find_orca` runs `subprocess.run([...,"skills","list","--json"], capture_output=True, timeout=10, stdin=DEVNULL)`, and `_ORCA_CLIS = ("orca-ide","orca")`.
- `install_mcp.py:769` `_bounded`: `Popen` with `start_new_session=True`, then `communicate(timeout)`, then `os.killpg`. It has no output cap, so the 8 MiB cap is correctly marked as new.
- `install_codegraph.py:43`: `Runner = Callable[[list, float], tuple]`.
- `sprint/monitor.py:443-472`: `OutputMonitor` uses a `threading.Event` and a daemon thread.
- `sprint/tui.py:119-123`: `Live(..., screen=False)`. The spine records its own deviation to `screen=True`.
- `main.py:519-561`: the deferred `add_command` imports.
- `swarm/schema.py`: uses `Draft7Validator.check_schema`.
- `pyproject.toml`: python `>=3.10`, rich `>=13`, click `>=8`, jsonschema `>=4`, pytest `>=7`, and `--strict-markers`.
- No `termios`, `tty` or `fcntl` import exists under `cli/`.

**Contradiction hunt across ADs.** The only cross-AD and spec conflict I found is NEW-1. The spine itself records three deviations from the brownfield or spec wording, and I accept them: Popen versus `subprocess.run`, `screen=True`, and exiting on a render exception.

**Limits of this audit.**
- I did not execute any code. The constraint forbids uv, pip and pytest in the IronClaude repo.
- I did not verify version facts on the web again.
- Line numbers are from the 2026-11-08 read.
