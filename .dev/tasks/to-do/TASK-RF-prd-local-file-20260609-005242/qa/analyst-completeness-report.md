# Adversarial Completeness Gate — Research Coverage Report

**Lens:** completeness (BREADTH)
**Driving spec:** `.dev/specs/prd-local-file-delivery-fix.md`
**Research under review:** `research/01-process-py-file-args.md`, `research/02-prompts-and-siblings.md`, `research/03-template-and-tests.md`, `research-notes.md`
**Posture:** adversarial — assume gaps until proven; every PASS carries file:line evidence that I independently re-verified against live source.
**Date:** 2026-06-09

---

## Verification method

I did not take the research at face value. I re-ran every load-bearing grep and re-read every anchored line range against the live tree. All anchors below were confirmed present at the stated lines (source mtime current as of this run). The research is grounded, not fabricated.

---

## Area-by-area verdicts

### (1) Both `--file` emission sites + the `extra_args` wiring — **PASS**

- Both emissions located and confirmed: `process.py:199` (refs >50 KB branch, `file_args.extend(["--file", str(ref_path)])`) and `process.py:204` (spec branch, `file_args.extend(["--file", spec_path])`). Research 01 §1; independently re-grepped — `grep -rn '"--file"' src/superclaude/cli/prd/` returns exactly these two lines and nothing else.
- Wiring fully traced: `__init__:155` calls `_build_file_args`; `:166` passes `extra_args=file_args` into `super().__init__`. Base `ClaudeProcess` stores it at `pipeline/process.py:63` (`self.extra_args = extra_args or []`) and emits it at `:94` (`cmd.extend(self.extra_args)`). Research 01 §2–§3 establishes that an empty/removed builder makes `:94` a no-op → zero `--file` tokens. This is the complete dataflow from source line to argv.
- The "return `[]` vs delete the method" decision the spec leaves to the implementer (§5.1) is covered: Research 01 §2 confirms both end-states are behaviorally identical at the argv.
- Base `build_env` (`pipeline/process.py:107`, `os.environ.copy()`) confirmed to never inject `CLAUDE_CODE_SESSION_ACCESS_TOKEN` — the root-cause mechanism is covered, not just the symptom.

### (2) Dead-constant safety (grep evidence) — **PASS**

- `_PHASE_ALLOWED_REFS` (def `:95`): sole reference `:191`, inside `_build_file_args`. Re-grepped repo-wide.
- `_FILE_SIZE_THRESHOLD` (def `:115`): sole reference `:198`, inside the method.
- `_SPEC_FILE_STEPS` (def `:121`): code reference `:201` + docstring reference `:180`, both inside the method.
- **Zero test references** to all three — I independently ran `grep -rn '_PHASE_ALLOWED_REFS|_FILE_SIZE_THRESHOLD|_SPEC_FILE_STEPS' tests/` → no hits, confirming Research 01 §4.
- Research 01 §4 correctly notes the `base_step` normalization local also dies with the method. All three constants are proven dead-and-safe-to-delete with evidence. Spec §5.1's "grep before deleting" precondition is fully satisfied by the research.

### (3) prompts.py inline machinery — **PASS**

- `_read_file` (`:42-47`) + `_TRUNCATION_MARKER` (`:34`) bodies captured verbatim and re-read; truncation semantics (`content[:max_bytes] + marker`) confirmed. Research 02 §2.
- `_authoritative_specs_block` (`:120-138`) body captured verbatim; empty-input contract (`if not spec_paths: return ""` covering both `None` and `[]`, no leading whitespace) confirmed and called out as a hard preservation requirement. Research 02 §1.
- **Both call sites** covered: scope-discovery invocation `:247` + interpolation `:257`; investigation invocation `:919` + interpolation `:927`. Both confirmed to pass `spec_paths` and interpolate verbatim → no signature/call-site change needed. Research 02 §3.
- Refs-already-inlined idiom (`build_task_file_prompt`, read `:514-518`, interpolate under `---`-fenced headers `:546-568`) is documented as the exact pattern to mirror — covers spec §3's "refs need no change" claim. Research 02 §4.
- Sibling no-`--file` convention (roadmap/tasklist/validate executors) covered verbatim. Research 02 §5.

### (4) Missing-path / FileNotFoundError design decision — **PASS**

- Research 02 §2 explicitly flags the load-bearing decision: `_read_file` calls `path.read_text(...)` directly and **raises `FileNotFoundError` on a missing path** (re-read `:42-47` — confirmed, no guard). It names the guarded sibling (`_read_required` at `:91-95`) and states the two resolution options (guard with `path.is_file()`/try-except, or migrate fixtures to real temp files).
- Critically, Research 02 §6 ties this directly to the **injection tests** (`TestScopeDiscoverySpecInjection`/`TestInvestigationSpecInjection`) which bind non-existent paths (`/abs/SPEC_A.md`, etc.) — I re-read `test_spec_flag.py:251-266` and confirmed these are literal non-existent paths. The decision is therefore not abstract; the research shows exactly which tests break and why, and that the spec's chosen Option B forces this decision. This is the single most important design call and it is fully surfaced with consequences.

### (5) Exact existing tests to change — **PASS (and exceeds spec)**

- `TestSpecFileAttach` (`test_spec_flag.py:477-515`) — the class the spec names — is fully inventoried: hard-asserting tests at `:485-487` and `:495-498` break; the three `== []` tests at `:506/:510/:515` reference a removed symbol. Helper `_spec_config` (`:465`) scoped as local-only. Research 01 §6, Research 03 §2.
- **Coverage beyond the spec (a strength, not a gap):** the spec §7/§8 only names `TestSpecFileAttach`, but Research 02 §6 discovered that the **injection** classes (`TestScopeDiscoverySpecInjection` `:250-312`, `TestInvestigationSpecInjection` `:315-363`) bind non-existent spec paths and will throw `FileNotFoundError` under Option B's content-inlining unless guarded or migrated to real `tmp_path` specs. It also identifies the phrasing locks (`"AUTHORITATIVE SPECIFICATIONS"`, `"MUST Read each one IN FULL"`) and the byte-identity snapshot test (`:267-308`) that survives a format change only if the missing-path issue is resolved. The empty-contract lock `test_helper_empty_returns_empty_string` (`:310-312`) is identified as must-keep-passing. This is more complete than the spec's own test plan.
- New tests (spec §7.1–7.4) are mapped to concrete construction patterns (`_spec_config`, `tmp_path`, `PrdConfig` dataclass, staticmethod call). Research 03 §2.
- `test_e2e.py` correctly cleared (mocks `PrdClaudeProcess`, no change needed). The 100 KB prompt-ceiling invariant (`test_prompts.py:160-246`) and the `_read_file` truncation lock (`:249-277`) are flagged as a sizing risk + a do-not-touch primitive. Research 02 §6b.

### (6) Sync/verify behavior for a cli-only change — **PASS**

- Research 03 §3 establishes from the `Makefile` (`sync-dev:109`, `verify-sync:166`) that both targets cover skills/agents/commands/hooks/templates **only** and never touch `src/superclaude/cli/`. Therefore `make sync-dev` is a no-op for this change and `make verify-sync` is clean regardless. The research correctly reframes spec §8's `make sync-dev && make verify-sync` as a drift guard, not a propagation step, and explicitly warns the builder not to add items expecting cli files under `.claude/`. Substantive verification is correctly identified as `uv run pytest` + the `grep ... --file` guard. Complete and correct.

### (7) Docstrings to update — **PASS**

- Module docstring: `:4` ("phase-aware `--file` arg scoping") and `:11` (`GAP-003: Phase-aware --file arg scoping`) — re-read `process.py:1-12`, confirmed verbatim.
- Class docstring: `:133` ("Phase-aware `--file` arg construction (GAP-003)") — re-read `:130-136`, confirmed.
- prompts.py docstring staleness: Research 02 §1 flags `_authoritative_specs_block`'s docstring line ("Phase 1 (paths-only): the block carries paths, not inlined content.") as needing update under Option B — confirmed present at the tail of the `:120-138` docstring. This is a docstring the spec §5.2 implies but does not explicitly enumerate; research caught it.
- In-method comments that vanish with the method (`:94`, `:115`, `:119`, `:154`, `:171-185`) are inventoried. Research 01 §5. Complete.

---

## Adversarial probes that found no gap

- **Is there a `--file` site outside `_build_file_args`?** Re-grepped `src/superclaude/cli/prd/` — only `:199`/`:204`. No.
- **Does any test assert on base `extra_args` plumbing directly?** Re-grepped `tests/cli/prd/` for `extra_args` — zero hits. Covered (Research 01 §6).
- **Are the named constants referenced in any non-`.py` surface or docs that would dangle?** The dead-code claim rests on `.py` grep; constants are private module-level (`_`-prefixed) and not part of any public/exported contract — no plausible external reference surface. Acceptable.
- **Does the spec name a test target the research missed?** Spec names `test_spec_flag.py TestSpecFileAttach`; research covers it AND the broader injection suite the spec omitted. No miss; over-coverage.
- **Is the empty-input / byte-identity regression contract covered?** Yes — Research 02 §6 maps the byte-identity test (`:267-308`) and the empty-contract test (`:310-312`) and explains their survival conditions.

---

## Residual notes (informational, NOT gaps — already surfaced by the research)

1. The missing-path design decision (Area 4) is a genuine implementer choice the research correctly leaves open with both options stated; it is surfaced, which is the completeness bar. (Resolving it is the builder's/implementer's job, not research's.)
2. The 100 KB prompt-ceiling sizing risk under multi-spec inlining (Research 02 §6b) is a flagged consideration, not a coverage hole; the spec §9 scopes large-spec digest out and current specs are <50 KB.

Both are documented in the research, so neither constitutes a breadth gap.

---

## VERDICT: PASS

Every area required to implement the spec — both `--file` sites + wiring, dead-constant safety with grep evidence, the prompts.py inline machinery and both call sites, the FileNotFoundError design decision, the exact tests to change (including injection classes the spec itself omitted), cli-only sync/verify semantics, and all docstrings — has grounded, file:line-anchored research coverage that I independently re-verified against live source. No breadth gap found. Research is implementation-ready.
