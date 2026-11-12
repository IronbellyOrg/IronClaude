# Handoff: step 4, bmad-architecture (CA, headless, create), orca-observer
**Outputs:** `architecture-orca-observer/` here, identical (`diff -r`, no output) to Coder `_bmad-output/planning-artifacts/orca-observer/architecture/`: ARCHITECTURE-SPINE.md, .memlog.md (37 entries), inputs/, reviews/ (5 files). `spec-orca-observer/` refreshed, identical to Coder `_bmad-output/specs/spec-orca-observer/` (`diff -r`, no output); the spine is its companion ARCHITECTURE-SPINE.md and the spec memlog has 52 entries. Spine `status: draft` (one blocking item open); `lint_spine.py` reports 0 findings after fix cycle 2.

**Invariants:** 20 decisions, AD-1 to AD-20, each with Binds, Prevents and Rule. They cover: the `src/superclaude/cli/observe/` package with one module per role, registered once in `cli/main.py`; an allow-listed read-only adapter (`Runner`/`Discover` seams, 8 MiB cap, killpg); a single-flight collector over one `CycleSource` (live or fixture); one pure merge (AD-19); one `View` with screen and export renderers; a sanitizer with literal rendering; one terminal-policy module owning NO_COLOR, ASCII and width; the key-reader spike with its Textual switch rule; tests mapped to ADs (AD-16); unknown never becomes zero; what R1 leaves out; extension points for stages B and C and the TUIBBS reader.

**Frozen:** snapshot v1 is additive-only (`additionalProperties: false`; a new field needs a reviewed schema edit). `projection.evidence.lastObservedAt` is the evidence timestamp. R1 is read-only toward Orca.

**Conditional:** CD-1 to CD-16 tie decisions to OQ-1 to OQ-15 and UX-OQ-1 to UX-OQ-8. Each has a default and none is resolved. CD-16 names the shared worktreeId on each row (T20 requires it); UX-OQ-8 decides only placement.

**Reviews (cap reached: 2 fix cycles, 3 reviews):**
- Review 1, three lenses, FAIL: rubric walker 11 blocking, web verification 1, adversary 16. All 28 fixed in fix cycle 1.
- Review 2, fresh-context verification (`reviews/review-verification.md`), FAIL: 25 resolved, 3 partial, 1 new. Fix cycle 2 fixed NEW-1 (`one Run only` follows `scope.source=bound`), B9 (`runs_read` owner and k/N rule) and B7/ADV-13 (fixture question path via `CycleResult.fixture_questions`).
- Review 3, final verification (`reviews/review-verification-2.md`), FAIL: those 4 resolved, 1 new.
- **OPEN blocking, NEW-2 (not fixed; no further review allowed):** AD-6 skips rows whose `runId` is UNKNOWN when counting k and renders a plain `read k of unknown Runs since start`. If no row has a `runId`, the header reads `read 0 of unknown Runs` while rows are on screen: unknown shown as zero, against AD-8's `n+? (k unknown)` rule. The AD-16 test expects that output. A likely fix (not applied): render `k+? (u rows with unknown Run)`.

**Recorded conflicts, not resolved:** Popen plus killpg vs `subprocess.run` (adapter-contract.md:14); `Live(screen=True)` vs sprint/tui.py `screen=False`; a render exception exits, while sprint/tui.py continues.

**UNVERIFIED:** the per-call timeout, the uv version, and the first Rich version that reads NO_COLOR. The `read k of unknown Runs since start` wording and the `FixtureQuestion` shape are PROPOSED; many other literals are labelled PROPOSED in the spine.

**Incident:** the web-verification reviewer created and then deleted a `.venv` in this repo (gitignored; `git status` unchanged).

**Not done:** NEW-2; no epics, stories or tasks; nothing committed or pushed; minor review notes recorded but not fixed.
