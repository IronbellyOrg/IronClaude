# Review: rubric walker — ARCHITECTURE-SPINE.md (orca-observer)

Reviewer: independent adversarial rubric walker. Date: 2026-11-09. Status: COMPLETE.

- Target: `_bmad-output/planning-artifacts/orca-observer/architecture/ARCHITECTURE-SPINE.md` (308 lines, not edited)
- Spec: `_bmad-output/specs/spec-orca-observer/` (SPEC.md, rendering-rules.md, snapshot-export-schema.md, adapter-contract.md, acceptance-tests.md, release-gates.md, owner-decisions-and-risks.md, unverified-register.md, stack.md, write-back-future-stage.md)
- Brownfield (read only): `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`
- Inputs: `orca-observer/architecture/inputs/extract-prd-ux.md`, `extract-ironclaude-code.md`

Paths below are shortened: `SPINE` = the target; `spec/` = `_bmad-output/specs/spec-orca-observer/`; `ic/` = the issue-409-mvp worktree.

## Verdict: FAIL

Blocking: 11. Minor: 8.

## Blocking findings

### B1 — Discovery probe runs outside the Runner, so T1 and the forbidden-prefix check cannot see it
- Severity: Blocking
- Section: AD-3, AD-4, AD-5, AD-16
- Evidence: SPINE:86 says `_find_orca` is imported "as is" and is "the only place `skills list --json` runs". `ic/src/superclaude/cli/install_user_setup.py:198-221` runs the probe with `subprocess.run` directly (timeout=10 at :213) and takes no runner. SPINE:92 checks the forbidden-prefix set "before every call", but the probe never goes through it. SPINE:164 patches `subprocess.Popen` and `subprocess.run` to raise in the observer tests, which makes `_find_orca` return `None` (it swallows `SubprocessError`/`OSError`). The production path then cannot be exercised in tests. `spec/acceptance-tests.md:11` (T1) requires the argv log to include the discovery probe.
- Why blocking: the spine contradicts a pinned test and leaves a subprocess call outside the allow-list it claims covers "every call". Two implementers would either wrap or bypass discovery.
- Fix: put discovery behind a seam: either an injectable `discover: Callable[[], str | None]` defaulting to `_find_orca`, or a recording wrapper on the Runner for the probe argv. State that T1 asserts the probe argv through that seam. Also state whether the probe argv goes into the allow-list check (it is in the AD-4 exception list).

### B2 — `source.namespace` is half of row identity but has no defined source
- Severity: Blocking (risk of an invented Orca field)
- Section: AD-7, AD-12, Consistency Conventions (Identity)
- Evidence: SPINE:110 and SPINE:183 make row identity `(source.namespace, dispatchId)`. SPINE:140 emits `source.namespace`. `spec/unverified-register.md:11-17` lists the verified worker-list fields, and none of them is a namespace. SPINE:110 says "only verified worker-list keys are read". `spec/acceptance-tests.md:33` (T39) requires rows from different source namespaces to stay separate.
- Why blocking: parse, view, selection and snapshot all key on a value whose derivation is unstated. If it is read from Orca it is an invented field. If it is derived, adapter, parse and fixtures could each derive it differently.
- Fix: define `source.namespace` as observer-derived (for example from the discovered binary path plus the `--run` scope), mark it PROPOSED, name the module that computes it, and say how T39 fixtures inject two namespaces.

### B3 — No rule keeps the snapshot independent of session filter and hidden-historical state
- Severity: Blocking
- Section: AD-10, AD-11, AD-12, AD-15
- Evidence: SPINE:128 builds `View` from `(result, session, clock)`, and the View carries "the historical-hidden count". SPINE:134 builds `snapshot_json(view)` from that same View. SPINE:158 puts filter text and the show-historical flag in `Session`. `spec/rendering-rules.md:22` says historical rows are "never deleted from the snapshot".
- Why blocking: as written, a user's `/` filter or `h` toggle can drop rows from the exported snapshot, which contradicts the spec. Implementers of view and export will diverge on whether the View holds all rows or only visible ones.
- Fix: add a rule that `snapshot_json` and `record_text` serialize the full row set regardless of `Session` filter and `h` state, by having the View hold all rows plus a visible subset, or by having export take a session-neutral view. Then add a test.

### B4 — Change flags omit added and removed rows, the `changed since` string and restart disclosure
- Severity: Blocking (missing required coverage)
- Section: AD-15
- Evidence: SPINE:158 flags a row only when one of four fields "differs from the baseline". `spec/rendering-rules.md:46` requires changes to cover rows "added, removed or changed", the `changed since HH:MM (k)` string, and the disclosure that a restart starts a new baseline.
- Fix: extend AD-15 to flag added and removed identities against the baseline. Pin the `changed since HH:MM (k)` literal and the restart/new-baseline disclosure, and assign both to `view.py`.

### B5 — CD-6 default writes no file, which contradicts the envelope's per-cycle snapshot write and leaves `e` undefined
- Severity: Blocking (contradiction and missing coverage)
- Section: CD-6, AD-11, Operational envelope, CAP-10
- Evidence: SPINE:285 (CD-6 default): "no file is written until a destination is decided". SPINE:224: "one snapshot write per completed cycle". SPINE:134 binds the `e` key to `record_text` and a file destination from CD-6. `spec/acceptance-tests.md:19` (T27) requires `e` and `--once` to write the export. CAP-10 (spec/SPEC.md:30-65) requires the snapshot to be produced.
- Why blocking: under the default, CAP-10's snapshot is never produced and the `e` key has no defined behaviour. That is an internal contradiction between a CD default and an envelope figure stated as fact.
- Fix: give CD-6 a concrete default, for example a PROPOSED `$XDG_STATE_HOME/superclaude/observe/` path with fixed file names, or "`e` prints `export disabled (destination undecided)`, and the snapshot write is skipped and counted". Make the envelope line conditional on CD-6.

### B6 — CD-9 misreads OQ-5 and its default blocks the golden sample that AD-16 and R0 rely on
- Severity: Blocking (contradiction)
- Section: CD-9, AD-16, R0
- Evidence: SPINE:288 (CD-9 default): "Fixtures stay synthetic; no live-captured sample". Its change column says "OQ-5 allows the redacted live golden sample and T32". SPINE:164 (AD-16) has every test use recorded JSON "from the redacted golden sample". `spec/release-gates.md:9` (R0) requires "a redacted golden `worker-list` fixture". `spec/owner-decisions-and-risks.md:22` (open decision 6, behind OQ-5) is about capturing samples from the candidate `check --all` message read, not from worker-list.
- Why blocking: the default forbids the artifact that the spine's own test seam and the R0 gate require, and the owner question has been rescoped by invention.
- Fix: restrict CD-9's OQ-5 dependency to message-read samples (stage B). State that the redacted worker-list golden fixture is in R0 scope. If that capture also needs owner sign-off, add the sign-off as a separate CONDITIONAL with a synthetic-fixture default, and make AD-16 say "golden sample or the synthetic `base` fixture until decided".

### B7 — CAP-1 / R0 coverage gaps: replaying fixtures, fixture-only question data, and the fixture-mode header
- Severity: Blocking (missing required coverage)
- Section: CAP map, CD-1, AD-7, AD-10
- Evidence:
  - SPINE:280 (CD-1 default) allows no registration block and says R0 "runs only through tests and fixtures". It never says how a reviewer replays the R0 fixture renders: test artifacts, a script, or an unregistered entry point.
  - SPINE:110 says fixture-only fields are loaded "by a separate fixture loader". SPINE:128 lists the View contents, which include no question or requester model, so stage B and C fixture data has no defined path to the render.
  - `spec/rendering-rules.md:17` requires header line 1 with `mode=fixture|live` and the label `SYNTHETIC FIXTURE <variant>, not Orca data` (T50). No AD pins these strings or assigns them to a module.
- Fix: add the fixture-replay mechanism under CD-1 (for example `uv run pytest tests/observe -k render --snapshot-out`, or a dev-only `python -m` entry point; the repo rules prefer the pytest form). Add a fixture question model to the View, marked PROPOSED. Pin both header literals in AD-8, assigned to `view.py`.

### B8 — Cross-cycle merge has no owner module
- Severity: Blocking
- Section: AD-6, AD-7, AD-8
- Evidence: SPINE:110 describes `parse.py` as turning one cycle's JSON into a Snapshot, and applies "newer `observedAt`" only to duplicates within a page. SPINE:116 requires dropped rows to stay, marked `not reobserved`. SPINE:104 keeps only the "last good `Snapshot`" in `CycleResult`. `spec/adapter-contract.md:44` says the newer `projection.liveness.observedAt` wins *across cycles*. `spec/adapter-contract.md:61` (INV-007) covers `not reobserved` retention. `conflict (time went back)` needs the previous cycle's value.
- Why blocking: no module holds the prior-cycle row set, so collector, parse and view implementers will each build, or skip, the merge differently.
- Fix: assign the merge to one function, for example `collector.merge(prev: Snapshot, new: Snapshot) -> Snapshot` or a pure `merge.py`. State its rules: newer observedAt wins, rows missing from the new cycle are retained and marked `not reobserved`, and a backward time is flagged as a conflict. Add a cap on retained rows, PROPOSED.

### B9 — `read k of N Runs since start` and `--run` use are undefined beyond placement
- Severity: Blocking (missing required coverage)
- Section: AD-4, AD-6, CD-10, CAP-4
- Evidence: SPINE:92 allows `"--run", runId` but never says when the collector passes it, how Runs rotate within the 5-call cap, or where k and N are computed. SPINE:289 (CD-10) covers only the string's placement. `spec/release-gates.md:9` requires R0 degraded renders that show `read k of N Runs since start`, and T45 depends on it. `spec/adapter-contract.md:63` requires bound scope to add `one Run only`, which the spine omits.
- Fix: add a rule to AD-6 covering unbound versus per-Run polling, Run rotation order under the cap, and which module counts k and N. Pin `one Run only` in AD-8.

### B10 — CD-16 default contradicts pinned test T20
- Severity: Blocking (contradiction with spec)
- Section: CD-16, AD-10
- Evidence: SPINE:295 (CD-16 default): "The inspector shows it; the row does not". `spec/acceptance-tests.md:17` (T20) requires two rows "each naming" the shared worktreeId, plus `worktree unknown` for unmapped rows. UX-OQ-8 (`extract-prd-ux.md:117`) asks this question, but the spec's acceptance test already fixes the behaviour.
- Fix: make the default "the row names the shared worktreeId (T20)", or keep the default and flag the T20 conflict explicitly as requiring an owner answer before T20 can pass. Pin `worktree unknown`.

### B11 — "optional `scope`" breaks the never-omitted, `UNKNOWN` rule, and its shape is unstated
- Severity: Blocking (contradiction with a pinned rule)
- Section: AD-12
- Evidence: SPINE:140 lists "optional `scope`" and also says "A missing value is the string `UNKNOWN`". `spec/snapshot-export-schema.md:10` says a missing value is the string `UNKNOWN`, never null. `spec/snapshot-export-schema.md:16-30` says `scope` comes "From `result.scope`, optional upstream". Being optional upstream does not make the field omittable in the export. Whether `scope` is the whole object or one string is not stated, so the producer and a Go reader can diverge.
- Fix: emit `scope` always, as the string `UNKNOWN` when upstream omits it. State its JSON type (object pass-through or `scope.source` string) in the schema.

## Minor findings

### M1 — AD-5 "mirrors `_bounded`" overstates the match
- Section: AD-5. Evidence: `ic/src/superclaude/cli/install_mcp.py:769-796`. `_bounded` uses `stderr=DEVNULL` and `communicate(timeout)`, which cannot cap stdout. SPINE:98 adds an 8 MiB cap and a 2 KiB stderr read. Fix: say "extends `_bounded`", and name the streaming read that enforces the cap (incremental `read()` on the stdout pipe, with a separate stderr drain to avoid deadlock).

### M2 — AD-8 narrows a rule and omits several pinned literals
- Section: AD-8. Evidence: SPINE:116 says "`terminalState=released` without `outcome` never renders `done`". `spec/rendering-rules.md:52` attaches no outcome condition. AD-8 does not pin `reported T (page k)`, `reported T1-T2 (changed during read)` (`rendering-rules.md:55`), `filter <expr>: k of n collected` (:56), `x/y shown` or `+N more` (:57), `k historical hidden (h)`, or the footer `shown x/y | collected n / reported T`. `messages UNVERIFIED (not read)` (:18) appears only in AD-18. Note that "changed during read" needs the collector to track `page.total` across pages. Fix: remove the "without outcome" qualifier and list the remaining literals with their owning module. If removing the qualifier is a real behaviour change, raise it to blocking.

### M3 — AD-13 auto-enables ASCII on a non-UTF-8 encoding
- Section: AD-13. Evidence: SPINE:146. `spec/stack.md:25` says only "`--ascii` selects the ASCII path for non-UTF-8 terminals". Fix: mark the encoding auto-detect PROPOSED.

### M4 — AD-1 import diagram leaves the `Key` type and production-runner wiring unplaced
- Section: AD-1. Evidence: the AD-1 diagram has no `keys→view`, `view→keys` or `commands→adapter` edge, and imports "follow the diagram and nothing else". `apply_key(session, key, view)` (SPINE:158) needs a `Key` type that both `keys.py` and `view.py` use, and something has to construct the production Runner. Fix: name the module that owns `Key` (for example a small `types.py`, or `view.py` with a `keys→view` edge) and the module that wires the Runner.

### M5 — AD-12 does not state the dotted-name encoding or the JSON types that may be `UNKNOWN`
- Section: AD-12. Evidence: SPINE:140 lists `stage.worker`, `liveness.verdict` and similar without saying whether these are nested objects or literal dotted keys. `page.hasMore`, `page.total` and `cycle` are boolean, integer and integer when present, but can be the string `UNKNOWN`. Fix: state the nesting rule and the union types in the schema prose.

### M6 — The code extract cites a different checkout
- Section: Sources. Evidence: `inputs/extract-ironclaude-code.md:3` gives the source as `/home/coder/workspaces/IronClaude`, not the issue-409-mvp worktree named as brownfield. I re-checked the cited facts in `ic/` (`main.py:519-564`, `install_user_setup.py:35,198,213`, `install_codegraph.py:43`, `install_mcp.py:769-806`, `sprint/monitor.py:443-475`, `pyproject.toml:16,35-41,54,78-83,114-148`) and they match. Fix: re-cite against the worktree.

### M7 — AD-7 hides the `n unrecognised keys` diagnostic
- Section: AD-7. Evidence: SPINE:110 says "unexpected keys are counted, not shown". `spec/adapter-contract.md:36-38` requires `n unrecognised keys` in the inspector. Fix: "counted and shown in the inspector as `n unrecognised keys`".

### M8 — "a row that drops out stays" versus T12 wording
- Section: AD-8, AD-15. Evidence: SPINE:116 and :158. `spec/acceptance-tests.md:14` (T12) uses `no longer in source window` for any dropped row, not only the selected one. Fix: say which literal goes on the row and which goes on the status line.

## Checked and found correct
- OQ-1 to OQ-15 and UX-OQ-1 to UX-OQ-8 each map to a CD with a default. None is resolved by invention, except the CD-9 and CD-16 issues above (B6, B10).
- Stack versions match PyPI on 2026-11-09: rich 15.0.0, textual 8.2.8, click 8.5.1, jsonschema 4.26.0, pytest 9.2.0, pexpect 4.9.0. The Python 3.10 floor matches `ic/pyproject.toml:16`.
- The AD-12 row field list matches `spec/snapshot-export-schema.md:32-47` exactly. The envelope matches apart from B11.
- The AD-2 registration pattern matches `ic/src/superclaude/cli/main.py:519-564`.
- The AD-5 Runner shape matches `ic/src/superclaude/cli/install_codegraph.py:43`.
- The AD-6 thread and Event shape matches `ic/src/superclaude/cli/sprint/monitor.py:443-475`.
- Package-data shipping matches `ic/pyproject.toml:78-83`, and `--strict-markers` matches `:114`.
- The AD-13 width bands come from the UX source (`inputs/extract-prd-ux.md:90`) and are not invented. The `·`→`.` mapping is sourced, and `▸`→`@` is correctly marked PROPOSED (`:95`).
- AD-17 is consistent with `spec/write-back-future-stage.md`.
- The operational envelope figures (15 s, 5 calls, 45 s STALE, 60 s backoff cap) match AD-6. The exceptions are the per-cycle write (B5) and the 8 MiB / 2 KiB caps, which are spine choices and should be marked PROPOSED.
