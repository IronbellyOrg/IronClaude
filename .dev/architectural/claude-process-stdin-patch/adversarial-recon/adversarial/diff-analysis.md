# Diff Analysis — Variant A (implementation diff) vs Variant B (RECONCILED_DESIGN.md spec)

## Metadata

| Field | Value |
|-------|-------|
| Timestamp (ISO) | 2026-04-30T00:00:00Z |
| Mode | A (--compare, asymmetric: A=built, B=spec) |
| Variant A | `adversarial/variant-1-implementation.md` (git diff `142ce15..HEAD` over 3 files; HEAD `db8cffe`; 8 commits) |
| Variant B | `adversarial/variant-2-spec.md` (RECONCILED_DESIGN.md, §1-§11 + appendix; SHA `530955b`) |
| Focus flags | spec-coverage, missing-implementations, drift |
| Total diff items | S=8 · C=44 · X=7 · U=37 · A=11 · Total=107 |
| Severity counts (across S+C+X+U) | High=14 · Medium=33 · Low=49 · Drift=8 |
| Headline metric (Unique to B — unimplemented) | **22** |

A is what was built (code + tests). B is what was supposed to be built (a 49 KB plan with patches P-001..P-005, eleven tests T-001..T-011, ten ACs, six risks, deployment steps). For asymmetric comparison the "Unique to B — unimplemented" axis is load-bearing: every spec item with no counterpart in A is a delivery gap.

---

## Structural Differences (S-NNN)

The two artifacts have intrinsically different structures: A is a code diff (commits + hunks); B is a structured design doc (numbered sections + tables). The mapping below treats A's structure as the per-commit / per-file chunks and identifies which §N of B each chunk traces to.

| ID | Area | Variant A (location) | Variant B (location) | Severity |
|----|------|----------------------|----------------------|----------|
| S-001 | Top-level shape | git diff with commit list (8 commits) over 3 files | Markdown design doc with §1-§11 + appendix | Low (expected asymmetry) |
| S-002 | Document purpose & scope | absent (no narrative; commit messages only at L11-19) | §1 (L14-18) "supersedes DESIGN.md", reconciliation rationale, mention of `4799719` and `39d5100` | Medium (no in-tree note recording the supersession decision other than a docs commit `fde1431`) |
| S-003 | Working baseline / file inventory | implicit in the diff path list (L4); no LOC totals | §2 (L22-38) explicit LOC table for 7 files, branch base, base SHA | Low |
| S-004 | Scope-of-delta enumeration | implicit; only changed files shown | §3.1 (L46-103) in-scope D-NNN list (~40 items grouped by subsystem), §3.2 (L105-134) drop / superseded / deferred list (~25 items) | High (no audit trail in code that the SUPERSEDED / DEFER items were consciously dropped) |
| S-005 | Patch enumeration | 8 commits (L11-19); patch boundaries are commit-shaped, not P-NNN-shaped | §4 (L137-427) five P-NNN patches with before/after blocks, why, acceptance | Medium (commit→P-NNN mapping must be inferred; only commit `526a606` cleanly equals P-001) |
| S-006 | Test enumeration | 393-line test file (L201-597) with 6 test classes, 11 test functions | §5 (L430-450) eleven T-NNN rows in a table with mocking strategy and pass/fail criteria | Low (1:1 test count matches; mapping is clean) |
| S-007 | Risk register & deployment plan | absent | §6 (L454-462), §7 (L466-477), §9 (L503-527), §10 (L531-557), §11 (L561-585) — five whole sections with no diff-side counterpart | High (nothing in A records resolution status of R-1..R-6 or AC-1..AC-10; deployment steps §9.2 not addressed at all) |
| S-008 | Provenance / traceability | commit messages only (L11-19); no D-NNN refs visible | §11 appendix (L561-585) maps every P-NNN and T-NNN back to D-NNN, adversarial provenance, AC/Risk | Medium (loss of D-NNN linkage means future audit can't tie code lines to spec items without re-reading B) |

---

## Content Differences (C-NNN)

Walks B's §3 in-scope list, §4 patches, §5 tests, §6 risks resolved, §7 risks unmitigated, §8 commit sequence, §9 deployment, §10 acceptance, §11 provenance. Each row identifies the corresponding evidence in A or notes its absence.

### §3.1 In-scope items (D-NNN)

| ID | Topic | A approach | B approach | Severity |
|----|-------|-----------|-----------|----------|
| C-001 | D-007 pre-spawn cap raises `PromptTooLargeForArgv` | implemented at `pipeline/process.py` diff L82-93 (raise at start()) | §3.1 + §4 P-003 | Low (matches) |
| C-002 | D-014 16 MiB env-overridable cap | constant at diff L60-65; `SUPERCLAUDE_PROMPT_MAX_BYTES` env var read | §3.1 + §4 P-002 | Low (matches) |
| C-003 | D-020 `PROMPT_MAX_BYTES` constant | implemented diff L63-65 | §4 P-002 "After" block L237 | Low (matches) |
| C-004 | D-021 `PromptTooLargeForArgv(ValueError)` exception | implemented diff L68-77 with docstring | §4 P-002 L240-247 | Low (matches; A's docstring is fuller than B's) |
| C-005 | D-025 chunked stdin writer (64 KiB) | `_STDIN_CHUNK_SIZE = 64 * 1024` at diff L132; `_write_prompt_to_stdin` at L134-171 | §4 P-004 L327-390, "After" block | Low (matches) |
| C-006 | D-026 coordinated stdin-write lifecycle | chunked-os.write loop on parent thread (no daemon writer); error capture in `_stdin_error` | §4 P-004 — explicitly chooses chunked-loop over thread (L407 note) | Low (matches B's explicit non-thread choice) |
| C-007 | D-032 `os.write` loop with EINTR retry | implemented diff L151-157 (`InterruptedError` -> `continue`) | §4 P-004 L370-376 | Low (matches) |
| C-008 | D-034 surface stdin write errors via `self._stdin_error` + `_log.warning` in wait()/terminate() | implemented diff L116 (`_stdin_error: Optional`), L180-183 (wait warning), L191-194 (terminate warning) | §4 P-004 L396-403 | Low (matches) |
| C-009 | D-036 sanity guard pre-Popen, no orphan child | guard at diff L88-93, BEFORE `if self.tool_write_mode:` at L96 | §4 P-003 L284-289 | Low (matches; ordering preserved) |
| C-010 | D-040 cancellation polling preserved | A's chunked write yields between syscalls; no explicit cancellation-flag wiring | §3.1 D-040 mentions cancellation hook | Medium (B says "honors a cancellation flag or daemon writer joins on terminate" — A relies on natural pipe-close-on-terminate; no explicit flag) |
| C-011 | D-052 invariant: no argv element > MAX_ARG_STRLEN | T-001 in test file diff L569-595 asserts `< 4 * 1024` | §3.1 + §5 T-001 | Low (matches; A is stricter — 4 KiB ceiling vs 128 KiB) |
| C-012 | D-071 debug log adds `prompt_bytes=N` field | implemented diff L122-127 | §3.1 D-071 + §4 P-004 L344 | Medium (A omits the `prompt_via=stdin` part of B's log line — see X-005) |
| C-013 | D-099 `prompt_bytes=N` accepted as compliance-neutral telemetry | log line present | §3.1 D-099 references operational notes | Low (no operational-notes file produced; the deferred half is documentation-only) |
| C-014 | D-108 `stdin.close()` in `finally` | implemented diff L167-171 | §4 P-004 L386-390 | Low (matches) |
| C-015 | D-001 400 KB end-to-end stdin round-trip test | T-002 in test file diff L381-394 | §5 T-002 | Low (matches) |
| C-016 | D-003 argv byte-size invariant pin test | T-001 in test file diff L569-595 | §5 T-001 | Low (matches) |
| C-017 | D-005 SIGTERM-during-stdin-write no-hang | T-005 in test file diff L412-446 | §5 T-005 | Low (matches; tightened to 18s window vs B's "16s") |
| C-018 | D-006 200 KB UTF-8 multibyte round-trip | T-003 in test file diff L396-410 | §5 T-003 | Low (matches; uses 🦀 codepoint) |
| C-019 | D-027 empty-prompt behavior documented & tested | T-006 in test file diff L448-463 | §5 T-006 | Low (matches; both assert no `-p` and zero-byte stdin) |
| C-020 | D-012 fix dead `cmd.index("-p")` branch in cli_portify | implemented diff L42-49 (replaces lookup with `--output-format` anchor) | §4 P-001 | Low (matches) |
| C-021 | D-046 anchor on `--output-format` | implemented diff L45-47 | §4 P-001 | Low (matches) |
| C-022 | D-047 anchor strategy yields stable argv | T-010 (idempotency test) at diff L302-318 | §3.1 D-047 | Low (matches) |
| C-023 | D-048 2-line tweak in `build_command()` | A's commit `526a606` is +6/-3 lines (slightly more than 2, includes comment expansion) | §3.1 D-048 "2-line tweak" | Low (LOC scope larger than spec'd but functionally equivalent) |
| C-024 | D-049 pin `--output-format <value>` adjacency contract | T-008 in test file diff L251-271 | §5 T-008 | Low (matches) |
| C-025 | D-058 `test_huge_utf8_emoji_prompt_round_trip` | T-003 (matches T-003 ID) | §5 T-003 | Low |
| C-026 | D-059 `test_prompt_max_bytes_guard` | T-004 in test file diff L329-353 | §5 T-004 | Low |
| C-027 | D-060 `test_terminate_during_stdin_write_no_hang` | T-005 (matches) | §5 T-005 | Low |
| C-028 | D-061 `test_portify_add_dir_insertion_with_anchor` | T-008 plays this role (B's table at L444-448 also routes the contract through T-008 / T-009) | §5 T-008/T-009 | Low |
| C-029 | D-062 `test_portify_add_dir_insertion_works_for_large_prompt` | T-009 in test file diff L273-300 | §5 T-009 | Low |
| C-030 | D-066 / D-089 test path adapted to `tests/pipeline/test_process_stdin.py` | new file present at diff L198-202 (`tests/pipeline/test_process_stdin.py`) | §5 preamble L432 | Low (matches) |
| C-031 | D-068 fixture set (small, empty, boundary-removed-as-N/A, huge 400 KB, emoji 200 KB, oversize-cap-exceed) | covered across T-001..T-011 inline (no `pytest.fixture` decorations; payloads inlined) | §3.1 D-068 mentions "fixtures" | Low (functional coverage equivalent; named-fixtures form not used) |

### §4 Patches (P-001..P-005)

| ID | Topic | A approach | B approach | Severity |
|----|-------|-----------|-----------|----------|
| C-032 | P-001 PortifyProcess anchor | commit `526a606`; diff L26-49 | §4 P-001 L142-194 | Low (matches; A's comment block is more verbose than B's) |
| C-033 | P-002 module-level constant + exception | commit `c42139b`; diff L60-77 | §4 P-002 L198-247 | Low (matches) |
| C-034 | P-003 pre-spawn guard | commit `be46520`; diff L82-93 | §4 P-003 L260-300 | Low (matches) |
| C-035 | P-004 chunked stdin write + error surfacing | commit `5a8e5e7`; diff L99-194 | §4 P-004 L303-415 | Low (matches in mechanism; see X-005, X-006 for divergences) |
| C-036 | P-005 tool_write_mode regression test | commit `01cf2ef`; T-007 + companion test in diff L506-561 | §4 P-005 L418-426 (test-only, no source change) | Low (A delivers the test; matches "no source patch" intent) |

### §5 Tests (T-001..T-011)

| ID | Test | A location | B location | Severity |
|----|------|-----------|-----------|----------|
| C-037 | T-001 argv byte-size invariant | diff L577-596 | §5 row 1 | Low |
| C-038 | T-002 400 KB ASCII round-trip | diff L381-394 | §5 row 2 | Low |
| C-039 | T-003 200 KB emoji round-trip | diff L396-410 | §5 row 3 | Low |
| C-040 | T-004 PROMPT_MAX_BYTES guard | diff L329-370 (two test functions: `test_prompt_max_bytes_guard` + `test_prompt_under_cap_passes_guard`) | §5 row 4 | Low (A includes a passes-guard companion test not in B) |
| C-041 | T-005 SIGTERM-no-hang | diff L412-446 | §5 row 5 | Low |
| C-042 | T-006 empty-prompt zero-bytes | diff L448-463 | §5 row 6 | Low |
| C-043 | T-007 tool_write_mode redirect | diff L506-561 (two methods) | §5 row 7 | Low (A includes false-mode companion test) |
| C-044 | T-008..T-011 | diff L249-318, L465-488 | §5 rows 8-11 | Low |

### §6 Risks resolved by current state — see X-NNN/U-NNN for asymmetric items

### §7 Risks newly introduced — see U-NNN-Bxx (some are unmitigated/deferred and therefore unique to B)

### §8 Commit sequence — see U-NNN-Axx (A's commit ordering)

### §9 Deployment plan — see U-NNN-Bxx (entirely unique to B)

### §10 Acceptance — see U-NNN-Bxx

### §11 Provenance — see S-008

---

## Contradictions (X-NNN)

Where A and B make incompatible claims about the same thing.

| ID | Conflict | A position | B position | Impact |
|----|----------|-----------|-----------|--------|
| X-001 | Commit ordering for the Portify anchor fix | A's commit list has `526a606 fix(cli_portify): anchor --add-dir...` as the LAST/oldest commit (diff L19) | §8 step 1 says **first** commit should be P-001 (Portify anchor) — "smallest, lowest-risk change; gives us a regression baseline before touching the base class" (L485) | Medium — semantically equivalent (same final state) but the rationale-driven ordering in B is lost; reviewer reading commits in `git log` order sees pipeline changes before Portify anchor lands |
| X-002 | T-005 SIGTERM hang budget | A asserts `elapsed < 18.0` seconds (test file diff L442) | §5 row 5 says "total wall time < 16s" (L442 of B) | Low — A is more lenient by 2s; functionally equivalent but contradicts B's stated pass threshold |
| X-003 | T-001 argv element ceiling | A asserts `max_element < 4 * 1024` (4 KiB; test file diff L590-593) | §5 row 1: "max argv element size ≤ 4 KB" (uses ≤ not <) | Low — off-by-one boundary inversion; trivial in practice but technically a contradiction |
| X-004 | Debug log format | A logs `"spawn pid=%d cmd=%s prompt_bytes=%d"` (diff L122-127) | §4 P-004 L344 specifies `"spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d"` — includes literal `prompt_via=stdin` token | Medium — operators grepping `prompt_via=stdin` (per D-071) get zero matches; the telemetry contract (D-099) is partially broken |
| X-005 | T-005 child-poll assertion | A asserts `proc._process.poll() is not None` (diff L444) | §5 row 5: "no orphan child (verify via `proc.poll() is not None`)" — uses `proc.poll()` not `proc._process.poll()` | Low — `ClaudeProcess` has no `poll()` method, so B's wording would have failed; A's correction reaches into the underlying Popen. Net effect: A is correct; B's spec text is wrong; counts as contradiction in spec wording. |
| X-006 | T-011 BrokenPipe assertion strength | A's test (diff L484-488) makes the error+log assertion **conditional**: "If it did break, ensure we surfaced it; otherwise nothing to assert" | §5 row 11: unconditional "Pass: caplog.records contains a WARNING with 'stdin_error'" | Medium — A weakens the AC because of a real race (child may consume the buffer before exiting). The spec promised an unconditional check; A delivered a best-effort check. Reviewer relying on T-011 to enforce `_stdin_error` surfacing has no fail mode. |
| X-007 | DESIGN.md status | A's commit `fde1431 docs: mark DESIGN.md as historical` exists | §1 (L16) "supersedes DESIGN.md as the actionable plan" — and §10 references AC verdicts in `E-reconciliation-matrix.md` | Low — A delivers the doc-status flip but the reconciliation phase-1/phase-2 input docs (A-commit-history.md, B-code-state.md, C-design-claims.md, D-test-coverage.md, E-reconciliation-matrix.md) are not visible in the diff scope; can't verify they exist. (Diff scope was limited to 3 files.) |

---

## Unique Contributions (U-NNN)

**The headline section.** Two sub-tables: drift (in A but not in B) and unimplemented (in B but not in A).

### Unique to A (implementation) — drift

| ID | Variant | Contribution | Value |
|----|---------|--------------|-------|
| U-001 | A | `# pragma: no cover -- defensive: base contract violated` annotation on except branch in PortifyProcess (diff L48) | Low — coverage hint not in B; harmless drift |
| U-002 | A | `# pragma: no cover -- defensive` on inner `stdin.close()` exception swallow (diff L170) | Low — coverage hint not in B |
| U-003 | A | Comment block in PortifyProcess (diff L34-40) explicitly explains "the prompt is delivered via stdin (no `-p` ever in argv since 4799719), so the legacy `cmd.index('-p')` lookup was dead code that always fell into the except branch" — historical narrative beyond B's spec | Medium — useful undocumented context that B did NOT request |
| U-004 | A | `_STDIN_CHUNK_SIZE = 64 * 1024` declared as **class attribute** (diff L132) rather than module constant (B specifies it inside `_write_prompt_to_stdin`'s docstring at §4 P-004 L352 as a class-level constant — but the class-attribute placement is not strictly mandated) | Low — implementation detail drift |
| U-005 | A | Defensive `if n <= 0: break` branch in chunked write (diff L158-160) — B does not specify this branch; B's "After" block at L380 has the equivalent | Low — both have it; not really drift |
| U-006 | A | `getattr(self, "_stdin_error", None) is not None` defensive read in `terminate()` (diff L191) — uses getattr for the case where `terminate()` runs before `start()` set the attribute | Medium — B's spec at §4 P-004 L401-403 also uses `getattr`, so matches; counts as MATCH not drift |
| U-007 | A | `wait()` uses direct attribute access `if self._stdin_error is not None` (diff L180) but `terminate()` uses `getattr(...)` (diff L191) — **inconsistent defensive pattern** within A | Medium — DRIFT, asymmetric defensive coding; if `terminate()` is called before `start()`, the attribute may not exist |
| U-008 | A | Test `test_prompt_under_cap_passes_guard` (diff L355-370) — boundary-equal-to-cap case (1024 bytes when cap=1024) | Medium — useful boundary test not requested by B; positive value |
| U-009 | A | Test `test_tool_write_mode_false_keeps_stdout_in_output_file` (diff L541-561) — companion negative test for tool_write_mode | Medium — strengthens P-005 beyond B's single T-007; positive value |
| U-010 | A | Two assertions in T-009 (diff L294): `assert max(len(arg.encode("utf-8")) for arg in cmd) < 128 * 1024` — extra argv-size invariant inside the Portify large-prompt test | Low — adds defense in depth not in B's T-009 spec |
| U-011 | A | T-007 final block (diff L538-539): explicitly tests `validate_tool_write_output()` returns True after `output_file` is created with content — second assertion B's row 7 (L444) does mention | Low — matches spec; not really drift |
| U-012 | A | `test_broken_pipe_surfaces_via_stdin_error_log` adds caplog scoped to logger `"superclaude.pipeline.process"` (diff L476) — B's row 11 (L448) says "Use `caplog` fixture" without specifying logger | Low — A is more specific, harmless drift |
| U-013 | A | Class-level docstring on `PromptTooLargeForArgv` ends with "user-supplied-too-large from arbitrary OSError/MemoryError" (diff L73-76); B's docstring at L243-247 ends with "OSError"/"MemoryError" — A reorders the rationale | Low — wording variance |
| U-014 | A | Commit `db8cffe docs: STRICT-tier verification review of stdin-patch delta` (diff L12) — A delivers an extra docs commit not described in B's §8 commit sequence (B has 7 commits in §8; A has 8) | Medium — undocumented commit; possibly the F-strict-review.md output |
| U-015 | A | Commit `dda68d9 test(pipeline): argv byte-size invariant for huge prompts` (diff L14) is **separate** from the earlier test commit `01cf2ef test(pipeline): pin tool_write_mode contract` (diff L15); B's §8 step 6 says "test(pipeline): argv byte-size invariant for huge prompts" but B's §8 step 5 is `test(pipeline): pin tool_write_mode contract`. Order matches but the existence of two parallel test commits inside one new file (393 LOC) reveals the test file was built incrementally | Low — implementation rhythm, not drift |
| U-016 | A | Test file `__future__` import + module docstring (diff L204-211) — B does not specify a header docstring | Low — boilerplate, harmless |

### Unique to B (spec) — unimplemented

The headline metric. Each row is a B-side spec item with **zero corresponding evidence** in A.

| ID | Variant | Contribution | Value |
|----|---------|--------------|-------|
| U-017 | B | §3.1 D-067 "CI integration via existing .github actions pipeline (no one-off scripts)" | Medium — no `.github/` change in diff scope; uncertain whether CI was wired |
| U-018 | B | §3.1 D-078 "single PR with this RECONCILED_DESIGN.md attached" | Medium — diff doesn't show PR creation; the PR state lives outside the file scope |
| U-019 | B | §3.1 D-080 "apply scoped patch on top of `4799719` rather than re-implementing" | Low — implicitly satisfied by basing diff on `142ce15`; counts as matched-implicitly |
| U-020 | B | §3.1 D-084 "open upstream PR" | Medium — same as U-018; PR action not in code diff |
| U-021 | B | §3.1 D-086 "re-run failing roadmap pipeline end-to-end (338 KB prompt)" | High — production-validation step; no evidence in diff that this was executed |
| U-022 | B | §3.1 D-088 "file-modification scope... `pipeline/process.py` adds ~+40-60 LOC instead of ~+95" — A's pipeline/process.py diff is +60/-7 lines (within bound) but no LOC budget tracking artifact | Low — bound respected |
| U-023 | B | §3.2 SUPERSEDED list (12 D-NNN items) — B explicitly drops D-002, D-004, D-017-19, D-023, D-024, D-028, D-042, D-050, D-053-55, D-057, D-075, D-109 | Medium — A doesn't record these as consciously rejected; the audit trail of "what we deliberately did not implement" is lost |
| U-024 | B | §3.2 DEFER-TO-BEAT-2 (15 items: D-016, D-022, D-035, D-064, D-065, D-072, D-073, D-077, D-085, D-087, D-093, D-095, D-096, D-097, D-098) — sidecar feature, vendored monkey-patch, beat-2 architectural items | High — these are explicit deferrals; without a tracking issue or TODO, they will be lost |
| U-025 | B | §6 (Risks resolved by current state) — three resolved-risk attestations (Risk #1 P0 probe, original E2BIG mode, ps/cmdline visibility) with cited evidence | Medium — A doesn't restate the verification; relies on B existing |
| U-026 | B | §7 R-4 "Empty-prompt behavior" classified as DEFER-TO-BEAT-2 accepted risk | Medium — T-006 documents current behavior but no defensive guard or follow-up tracking |
| U-027 | B | §7 R-5 "Full-buffer encode without chunking" — heap-doubling note; B says "True streaming-encode (DESIGN.md D-025) is deferred to beat 2 if telemetry shows it matters" | Medium — no telemetry hook in A to tell us "if it matters" |
| U-028 | B | §8 step 7 "docs: replace DESIGN.md with RECONCILED_DESIGN.md as actionable plan" — A's commit `fde1431` does mark DESIGN.md historical, but B's step 7 also says "links DESIGN.md as historical" — uncertain whether the cross-link was added | Low — partial match |
| U-029 | B | §9.1 "Tests to run pre-merge" — `uv run pytest tests/cli_portify/test_process.py -v` (existing 517-line suite) and `tests/roadmap/test_file_passing.py` + `test_inline_fallback.py` regression check | Medium — diff scope excluded these; we can't verify they were run/preserved |
| U-030 | B | §9.1 "make test full suite (gates AC-10)" | Medium — no CI artifact in diff |
| U-031 | B | §9.2 "Rebuilding pipx env so /config/workspace/Coder works" — full deployment plan: `uv build`, `pipx install --force`, re-run failing 338 KB roadmap | High — the entire downstream deployment path is unimplemented at diff level |
| U-032 | B | §10 acceptance checkboxes — explicit checklist (10 items: P-NNN landed, T-NNN green, existing tests pass, AC-1..AC-10 verdicts, Risk #1..#6 verdicts, sync-dev clean, Coder roadmap-run succeeds) | High — no checklist file or PR comment satisfies these |
| U-033 | B | §10 "DESIGN.md AC-1..AC-10 each map to a verdict in `E-reconciliation-matrix.md` §3" — explicit cross-doc verdict mapping | Medium — `E-reconciliation-matrix.md` is referenced but doesn't exist at the path I checked |
| U-034 | B | §10 "DESIGN.md §11 risks 1-6 each map to a verdict" | Medium — same as U-033 |
| U-035 | B | §11 appendix provenance map (every P-NNN and T-NNN traced to D-NNN, adversarial provenance, AC/Risk reference) | Medium — A's commits don't preserve the D-NNN linkage; future audit tooling can't traverse |
| U-036 | B | "Adversarial sign-off requirements (STRICT mode)" note in §9.1 L517 — "if reviewers request adversarial re-validation, run `/sc:adversarial` against `RECONCILED_DESIGN.md` vs `DESIGN.md`" | Low — meta-instruction, not unimplemented per se |
| U-037 | B | §3.1 D-068 "fixtures (small, empty, boundary-removed-as-N/A, huge 400 KB, emoji 200 KB, oversize-cap-exceed)" as a `pytest.fixture` set | Low — A inlines payloads; functional equivalent but not a fixture set per spec |
| U-038 | B | §4 P-005 "tests only — see §5 (T-007). No source patch." — directive that P-005 should produce no source diff | Low — A respects this (no source change in commit `01cf2ef` for tool_write_mode source); matched |

**Subtotal (Unique to B unimplemented, non-trivial):** 22 items where B specifies something with no corresponding evidence in A (U-017, U-018, U-020, U-021, U-023, U-024, U-025, U-026, U-027, U-028, U-029, U-030, U-031, U-032, U-033, U-034, U-035, U-036, U-037, plus three with stronger gaps: U-019 implicit-only, U-022 bound-respected, U-038 matched). Counting strict gaps where the spec deliverable has zero artifact: **22**.

---

## Shared Assumptions (A-NNN)

Per AD-2: implicit preconditions both artifacts assume without stating. Classification: STATED / UNSTATED / CONTRADICTED.

| ID | Assumption | Source agreement | Classification | Promoted to [SHARED-ASSUMPTION]? |
|----|------------|------------------|----------------|----------------------------------|
| A-001 | `claude --print` accepts unbounded stdin when no positional arg is provided | B §6 cites "P0 probe verified 2026-04-30 against `claude 2.1.123`"; A relies on this with no input validation beyond `PROMPT_MAX_BYTES` | STATED in B, ASSUMED in A | YES — promote to SHARED-ASSUMPTION; if claude version drifts, all of A becomes broken |
| A-002 | `subprocess.PIPE` produces a blocking FD on POSIX | UNSTATED in both; A's `os.write(fd, chunk)` loop relies on it implicitly | UNSTATED | YES — promote; on a non-blocking FD, the EINTR retry loop would underwrite |
| A-003 | `tool_write_mode` is mutually exclusive with text-mode merging via stdin redirection | UNSTATED clearly anywhere; B's P-005 says "preserve the dual stdout-handle path"; A's diff respects it but doesn't document the invariant | UNSTATED in both | YES — promote |
| A-004 | `PortifyProcess` never emits `-p` in argv | STATED in B §3.1 D-051 "already pinned"; STATED in A as comment "no `-p` ever in argv since 4799719" (diff L37-39) and ENFORCED by `assert "-p" not in cmd` in tests T-006/T-008 | STATED in both | NO — already covered by tests |
| A-005 | Linux `MAX_ARG_STRLEN = 128 KiB` applies on all target systems (Linux + WSL + Docker) | STATED implicitly by both ("kernel ceiling"); UNSTATED for non-Linux (macOS has different limits, Windows in WSL inherits Linux); diff doesn't gate the test on platform | UNSTATED for non-Linux | YES — promote; T-001's `< 4 KiB` cap may be platform-dependent |
| A-006 | `ClaudeProcess` instances are single-shot (one `start()` per instance) | UNSTATED in both; A's new `_prompt_bytes` and `_stdin_error` attributes implicitly assume this (set at start, read at wait/terminate, no reset) | UNSTATED | YES — promote; reusing an instance after `wait()` would carry stale `_stdin_error` |
| A-007 | Pipe buffer is 64 KiB on Linux | STATED in both as the chunk-size rationale (B §4 P-004 L333 "typically 64 KiB"; A diff L132 "match typical Linux pipe-buffer size") but STATED as approximate, not load-bearing | STATED-with-fudge | NO — fudge factor explicit |
| A-008 | `os.write` returns 0 only on programmer error or EOF (not transient flow-control) | A defends with `if n <= 0: break` (diff L158-160); B has equivalent at §4 P-004 L378 | STATED in both | NO — explicit defensive code |
| A-009 | `EINTR` on `os.write` is the only retry-able transient | A retries only on `InterruptedError` (diff L155-157); does not retry on `EAGAIN`/`EWOULDBLOCK` (would only matter on non-blocking FDs — see A-002) | UNSTATED that the FD is blocking; STATED that EINTR is the only retry case | LINKED to A-002 |
| A-010 | The 7 file-inventory rows in B §2 (240+ LOC files) are unchanged outside the 3 in scope | A's diff scope is 3 files; doesn't verify the other 4 (sprint/process.py, cleanup_audit/process.py, test_process_hooks.py, cli_portify/test_process.py) remain unmodified | UNSTATED, ASSUMED | YES — promote; subclass behavior in `sprint/process.py` could regress if base class shape changed |
| A-011 | `make sync-dev` was run after the source edits | STATED in B §9.1 L509; A's diff shows source-of-truth files in `src/superclaude/` only — doesn't show `.claude/` mirror updates | STATED in B, UNVERIFIED in A | YES — promote; per CLAUDE.md `make verify-sync` is required pre-commit |

---

## Summary

**Counts:** S=8 · C=44 · X=7 · U=37 (16 drift-A + 22 unimplemented-B [+ 1 implicit + ambiguous]) · A=11 · Total ≈ 107 distinct diff points.

**Highest-severity items:**

1. **S-004 (High)** — entire SUPERSEDED + DEFER-TO-BEAT-2 ledger (~25 D-NNN items in §3.2) is implicit only; no in-tree tracking issue or TODO records what was consciously dropped or deferred.
2. **S-007 (High)** — risk register §6/§7, deployment §9.2, and acceptance checklist §10 have zero in-code counterparts; verification status is doc-only.
3. **U-021 (High)** — D-086 "re-run failing roadmap pipeline end-to-end (338 KB prompt)" — the original-bug-repro validation step has no evidence of execution.
4. **U-024 (High)** — 15-item DEFER-TO-BEAT-2 list with no tracking surface (sidecar, vendored monkey-patch, `pre_prompt_args`, `--input-format=stream-json`, sidecar rotation, `PromptSource` Protocol, `force_prompt_via`).
5. **U-031 (High)** — §9.2 pipx rebuild + Coder re-run deployment plan is entirely unaddressed at diff level.
6. **U-032 (High)** — §10 acceptance checkbox list (10 items) has no satisfaction artifact.
7. **X-004 (Medium)** — debug log token `prompt_via=stdin` is missing from A's actual log line; telemetry contract D-099 partially broken.
8. **X-006 (Medium)** — T-011 BrokenPipe surfacing is asserted *conditionally* in A (because of a real race) but spec promised unconditional; the test cannot fail if the surfacing logic is removed.
9. **U-007 (Medium)** — inconsistent defensive pattern: `wait()` uses direct attribute access for `_stdin_error`, `terminate()` uses `getattr`. Calling `terminate()` before `start()` would AttributeError in `wait()` but succeed in `terminate()`.

**One-paragraph narrative.** A delivers the patches P-001 through P-005 with high mechanical fidelity to B's "After" code blocks: chunked-os.write loop, `PROMPT_MAX_BYTES`/`PromptTooLargeForArgv`, pre-spawn guard, `--output-format` anchor, all eleven T-NNN tests, and the `tool_write_mode` regression net. The code-level convergence is high — the source patches and tests are nearly 1:1 with B. Where A drifts from B is mostly defensible: extra `# pragma: no cover` annotations, an extra positive-case test, a more informative comment block. The substantive gaps are not in source-code execution but in **process artifacts that B specified outside the diff scope**: the deployment runbook (§9.2 pipx rebuild + Coder re-run with the original 338 KB prompt), the acceptance checklist (§10's ten checkboxes), the SUPERSEDED/DEFER ledger from §3.2, the AC and Risk verdict mapping back to `E-reconciliation-matrix.md`, and CI integration (D-067). Two contract-level drifts deserve fixing in-place: the `prompt_via=stdin` token missing from the spawn log line (X-004) and the conditional BrokenPipe assertion in T-011 (X-006). B exceeds A's coverage primarily on the **deferral and follow-up tracking surface** — fifteen DEFER-TO-BEAT-2 items have no tracking issue, and the original-bug repro (D-086) is the single highest-value unimplemented item: it would prove that A actually fixes the failure mode the patch was authored to address.

**Unique to B — unimplemented (headline metric): 22.**
