# D-0110 — Notes

## Design notes

1. **Why a closure section and not a new ADR.** AC1 is a documentation
   ratification of v1 platform scope (Linux-only), not a new
   architectural decision. The architectural decision implicit in
   "Linux-only for v1" was made at design-spec authoring time
   (design-spec.md:30 and §16 line 812) and is already canonical in the
   spec. Following the convention established by §"DOC-OQ9 Closure"
   (T06.02, R6 — the reciprocal macOS deferral) and §"AC2 Closure"
   (T06.05, R9 — the reciprocal local-only deferral), this lands as a
   closure section appended to the existing ADR log rather than a new
   D-N entry.

2. **Why a single refusal site (`eval doctor`) rather than four
   (`doctor`, `run`, `list`, `describe`).** Three options were
   considered:
   - **(a) doctor-only refusal** — chosen. The doctor is the documented
     entry point per OPS-005 (T06.13). Operators run it first. One
     refusal site means one wording site, one set of tests, and one
     drift surface against `decisions.md`.
   - **(b) refusal in every eval subcommand** — rejected. Four refusal
     sites doubles the drift risk against `NON_LINUX_REFUSAL_TEMPLATE`
     and against the AC1 closure section's wording without changing
     operator outcome (the harness would still fail on macOS — just
     four lines later).
   - **(c) a Click group-level callback** — rejected. Click's group
     `result_callback` runs *after* the subcommand body, so a precheck
     there would not short-circuit. A Click `@click.group` callback
     attached to `eval_group` would short-circuit, but it would also
     refuse `superclaude eval --help`, which is a usability regression
     (operators on macOS should still be able to read the help text
     without a refusal). Option (a) keeps `--help` working everywhere.

3. **Why reuse `HARD_FAIL_EXIT_CODE` (= 2) rather than introduce
   `NON_LINUX_EXIT_CODE`.** A dedicated exit code would let CI tooling
   distinguish "wrong platform" from "missing binary", but the harness
   has no v1 CI integration (AC2 closure, R9) — there is no downstream
   consumer that would branch on the code. The friendly message names
   the cause unambiguously. Adding a code now would also force the
   six-row exit-code table in `docs/eval/exit-codes.md` to grow, and
   the table is already the most edited file in the harness docs.
   Reusing 2 keeps the harness's exit-code surface stable.

4. **Why `_default_platform_probe` indirection rather than calling
   `platform.system()` directly.** Three reasons:
   - Tests need to exercise the Darwin/Windows refusal branches on a
     Linux CI box. Monkey-patching `platform.system()` directly is
     possible but pollutes the standard library; an injectable helper
     scopes the override to `commands.py`.
   - The pattern matches the existing
     `_default_claude_version_probe` / `_default_free_ram_probe` style
     in the same module (commands.py:106, commands.py:239), so the
     code reads consistently.
   - A future macOS landing (per MIG-003 / DOC-OQ9 target 2026-Q3)
     amends a single helper rather than search-and-replace `platform.
     system()` calls across the codebase.

5. **Why the refusal cites AC1 + DOC-OQ9 + decisions.md by literal
   token.** The friendly message is the operator's only entry point
   into the ADR trail. Three tokens are landed:
   - `AC1` — the acceptance criterion ID, searchable in `roadmap.md`.
   - `R-109` — the roadmap row ID, searchable in `decisions.md`.
   - `DOC-OQ9` — the macOS-deferral closure section, the next thing an
     operator will want to read.
   - `.dev/releases/current/cliEval/decisions.md` — the file path so
     the operator does not have to guess. Pinned by
     `test_non_linux_refusal_template_cites_ac1_and_doc_oq9` so a
     future refactor cannot quietly drop these citations.

6. **Why the refusal runs before `--output-dir` scratch-root
   validation.** Scratch-root validation is the second-earliest check
   in the existing doctor body (commands.py:766). A non-Linux operator
   who passes `--output-dir` should see the AC1 refusal first (the
   harness is unusable for them) rather than a scratch-root error
   followed by a platform-incompatibility cascade. Order: (platform
   precheck) → (scratch-root validation) → (capability gates) → (RAM
   precheck) → (coverage gate).

7. **Why the platform check uses string equality (`!= "Linux"`)
   rather than `not in {"Linux"}`.** Equality is simpler, the
   precondition is a single value, and a set-membership test would
   imply that the allow-list might grow without further code change.
   Adding macOS in v2 will require an explicit amendment of this
   section (and of `NON_LINUX_REFUSAL_TEMPLATE`) — `!= "Linux"` makes
   that amendment a visible diff.

8. **Why `repr(system)` semantics in the friendly message
   (`'Darwin'` with single quotes, not `Darwin`).** Operators copy
   error messages into search engines and issue trackers. Quoting the
   token visually separates it from the surrounding prose and matches
   the existing `f"{target} not found"` style elsewhere in the doctor.
   The four-token lock test exercises the quoted form so a future
   refactor cannot drop the quotes without a test failure.

## Edge cases considered

- **`platform.system()` returns an empty string.** The check
  `system != "Linux"` triggers the refusal; the friendly message
  renders as `unsupported platform: ''`. Operators with this
  configuration are already broken (the Python install is malformed);
  the refusal short-circuits cleanly without an exception.

- **`platform.system()` raises.** Not a documented failure mode of
  the standard library, but the harness wrapper `_default_platform_
  probe` does not catch — the exception propagates and Click renders
  it. Adding a `try/except` here would mask a real bug (a broken
  Python install) and is out of scope.

- **WSL2 reports `Linux`.** The harness runs on WSL2 unchanged — WSL2
  is, for the harness's purposes, a Linux. No special-casing required.

- **A container running on macOS reports `Linux`.** Same as WSL2: the
  harness runs unchanged inside a Linux container on a macOS host.
  AC1 scopes "Linux-only" to `platform.system()`, not to the bare-
  metal host.

- **`--json` invocation on macOS.** The refusal lands on stderr only;
  stdout is empty. A downstream pipe that expected a JSON payload
  sees EOF — the consumer must handle a non-zero exit code (which it
  has to do anyway for `HARD_FAIL_EXIT_CODE` on Linux). Test
  `test_cli_doctor_refuses_windows_platform` pins this contract.

- **`eval doctor --help` on macOS.** Click renders help text without
  invoking the command body, so the precheck does not fire. macOS
  operators can read the help without a refusal — intentional, per
  rationale 2(c) above.

- **macOS support lands in v2.** The Reject/revise rule applies:
  this section is amended with an `Outcome:` line; the original
  `Resolution:` text stays for audit. The precheck is amended to
  accept `"Darwin"` and `NON_LINUX_REFUSAL_TEMPLATE` is renamed or
  re-scoped. The four lock-string tests are updated in the same
  commit.

- **A future BSD / illumos / Haiku port.** Out of scope for v1 and
  for the v2 MIG-003 follow-up (which names only macOS + CI). A
  hypothetical port would file a new acceptance criterion against the
  AC1 closure section and amend the refusal in the same Reject/revise
  pattern.

## Validation steps performed

1. Read `src/superclaude/cli/eval/commands.py` end-to-end around the
   doctor command body and confirmed the platform precheck is the
   first action inside the function.
2. Confirmed `_default_platform_probe` is module-level (not nested) so
   `monkeypatch.setattr(doctor_module, "_default_platform_probe", ...)`
   re-binds the symbol the doctor reads.
3. Confirmed `NON_LINUX_REFUSAL_TEMPLATE` is exported from
   `src/superclaude/cli/eval/__init__.py` (alphabetically sorted under
   the `N…` entries in `__all__`) so downstream consumers can import
   the constant without reaching into the submodule.
4. Ran the four new tests in `tests/cli/eval/test_doctor.py` — all
   four pass.
5. Ran the full `tests/cli/eval/test_doctor.py` file — 48 tests pass
   (44 pre-existing + 4 new), no regressions.
6. Grepped `.dev/releases/current/cliEval/decisions.md` for the AC1
   tokens and confirmed:
   - R10 revision-log entry is present.
   - §"AC1 Closure" header is present.
   - Decision table, cross-references to DOC-OQ9 / AC2 / MIG-003, and
     `Resolution status: RESOLVED — 2026-05-20` line are all present.
7. Confirmed `README.md` §"Platform support" cross-links the AC1, DOC-
   OQ9, and AC2 closure sections by relative path.
