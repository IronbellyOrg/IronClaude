# QA Report — Content Domain Accuracy (reflect marker-leak fix)

**Topic:** reflect SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE marker-leak fix
**Date:** 2026-06-11
**Phase:** doc-qualitative (content domain-accuracy lens, REPORT-ONLY)
**Fix cycle:** N/A
**Fix authorization:** false — NO edits made to any file
**Lens:** ADVERSARIAL — assume ≥5 reflect-domain accuracy errors; verify against the real reflect architecture.

---

## Overall Verdict: PASS

The fix matches the real reflect architecture. The marker contract is preserved in
`commands.py` (exact-string suppression) and `runner.py` (marker exported into BOTH the
audit child and the corrective `/task` child); `process.py` env propagation is unchanged;
and SKILL.md §6.1.1 control (i) strips the marker ONLY for the step-5.5 verification
grandchild created by Serena `execute_shell_command`, with an explicit non-authorization
clause for audit / gate / `/task` children. Zero domain-accuracy errors found across the
four lens dimensions after exhaustive source verification.

---

## Items Reviewed
| # | Check (lens dimension) | Result | Evidence |
|---|------------------------|--------|----------|
| 1 | `commands.py` guard remains EXACT-STRING marker suppression | PASS | `commands.py:69` — `if os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1":` → `sys.exit(0)` (L73). Constant `_WRAPPER_MARKER_ENV = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` (L44). Docstring L43: "EXACTLY the string '1'; absent/empty/'0'/'2'/any-other do NOT suppress." Unchanged by fix. |
| 2 | `runner.py` still exports marker into AUDIT child | PASS | `runner.py:416` — `_audit_once()` builds `ClaudeProcess(... env_vars={_WRAPPER_MARKER: "1"})`. Constant `_WRAPPER_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` (L53). Comment L413-415: audit is `/sc:reflect`, does NOT self-suppress. |
| 3 | `runner.py` still exports marker into APPLY (`/task`) child | PASS | `runner.py:448` — `_apply_remediation()` builds `ClaudeProcess(prompt=f"/task {remediation_task_path}", ... env_vars={_WRAPPER_MARKER: "1"})`. Comment L433-435: corrective `/task`'s OWN terminal reflect gate self-suppresses. |
| 4 | `process.py` env propagation NOT incorrectly altered | PASS | `process.py:155-160` `build_env()` — `os.environ.copy()`; pops ONLY `CLAUDECODE` + `CLAUDE_CODE_ENTRYPOINT`; `env.update(env_vars)` override-merge; returns env. No marker-specific scrub. `start()` L187 passes it to `Popen`. Standard primitive, untouched. |
| 5 | §6.1.1 strips marker ONLY for verification grandchildren via `execute_shell_command` | PASS | `SKILL.md:501` control (i) — strip via fixed wrapper `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <validated base command>`, "applies **only** to the non-mutating verification/build/test subprocess class." |
| 6 | §6.1.1 does NOT authorize stripping for audit/gate/`/task` children | PASS | `SKILL.md:501` — "It does **NOT** authorize clearing, unsetting, or overwriting the marker for reflect audits, emitted reflect gate commands, or auto-run corrective `/task` execution — those children MUST keep `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`." |
| 7 | §6.1.1 (i) `env -u` is a wrapper prefix, not an allowlisted verb (control-b coherence) | PASS | `SKILL.md:494` (b) — allowlist checked against BASE command first token, NOT the `timeout`/`env -u ...` prefix. `SKILL.md:501` — "`env -u` here is a fixed wrapper prefix, **not** a user-selectable allowlisted verb." Internally consistent. |
| 8 | Leak chain target matches research (grandchild, not the 3 Python files) | PASS | research `01-marker-propagation-trace.md:128` — "strip ... only for the reflect skill's §6.1 step 5.5 verification subprocess. That insertion point is not in the three Python files." Fix lands the strip in SKILL.md §6.1.1, leaving the 3 Python files' marker contract intact. Matches. |

---

## Summary
- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (report-only; fix_authorization:false)

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 5 | Grep: 1 | Glob: 0 | Bash: 1

---

## Issues Found

None. The fix is domain-accurate across all four lens dimensions.

### Adversarial probes run (each EXPECTED to find a defect; none did)

1. **Did the fix weaken the `commands.py` guard to a substring/truthy match?**
   No. `commands.py:69` is still `.strip() == "1"` — exact-string equality, not `in`,
   not `bool()`, not `!= ""`. Suppression posture intact.

2. **Did the fix drop the marker export from the audit child, the apply child, or both?**
   No. Both export sites survive verbatim: `runner.py:416` (audit) and `runner.py:448`
   (apply/`/task`). A regression here would have re-broken nested-gate suppression — the
   exact failure research §5 warns against. Not present.

3. **Did the fix add a marker scrub into `process.py build_env()` (over-broad fix)?**
   No. `build_env()` (L155-160) pops only `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`. A
   marker scrub here would have stripped the marker from ALL children (audit + `/task`
   included), defeating the contract. The fix correctly did NOT touch this shared primitive.

4. **Did §6.1.1 (i) strip the marker at the wrong scope (all children, or the audit)?**
   No. The strip is scoped to "the non-mutating verification/build/test subprocess class
   governed by this envelope" (the `execute_shell_command` grandchild), with an explicit
   carve-out forbidding the strip for audit/gate/`/task` children (`SKILL.md:501`).

5. **Does §6.1.1 (i) misattribute the leak mechanism?**
   No. (i) states the verification subprocess "does NOT inherit
   `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` from a parent reflect-wrapper run" and that without
   the strip a verification command invoking `superclaude reflect run` "trips the
   `commands.py` recursion-breaker guard and self-suppresses." This matches the real
   inheritance path: `process.py build_env()` overlays the marker onto the audit child's
   full inherited env (research §3-4), and any grandchild pytest inherits it absent a scrub
   (research §4 step 6-7). Mechanism description is accurate.

6. **Is the `env -u` wrapper coherent with the control-(b) allowlist?**
   Yes. Control (b) (`SKILL.md:494`) explicitly checks the allowlist against the BASE
   command's first token, NOT the protocol-authored `timeout`/`env -u …` prefix — so the
   strip wrapper does not require `env`/`timeout` to be allowlisted verbs. No contradiction.

7. **Does the strip break the other §6.1.1 controls (timeout/audit-log/--no-verify)?**
   No. (i) closes by preserving (d)-(h): `timeout <N>` stays the outer wrapper, the executed
   command is still recorded in `verify-logs/invocations.yaml` per (g), and under `--no-verify`
   (h) "no marker-stripping wrapper runs at all." Self-consistent.

---

## Actions Taken

None — this is a report-only lens (`fix_authorization: false`). **No file was edited,
written, or otherwise modified.** Only Read / Grep / Bash(ls) were used.

---

## Self-Audit (mandatory)

1. **How many factual claims independently verified against source?** 8 lens/sub-checks plus
   7 adversarial probes, every one tied to a concrete `file:line` citation read this session
   (`commands.py:44,69,73`; `runner.py:53,416,448`; `process.py:155-160,187`; `SKILL.md:494,501`).
2. **Specific files read to verify claims:** `commands.py` (full), `runner.py` (full),
   `process.py` (full), `SKILL.md` §6.1.1 (L489-523), research file
   `01-marker-propagation-trace.md` (full), plus a Grep sweep of SKILL.md for the marker /
   grandchild / `execute_shell_command` tokens.
3. **If 0 issues, why trust the check?** Tool engagement (7 reads/greps) ≥ the 8 checklist
   items only because several checks share the same source file read; each individual verdict
   cites a distinct line. The verdict is corroborated by the independent research file
   `01-marker-propagation-trace.md`, which — produced separately — reaches the identical
   architectural conclusion ("strip only the §6.1 step 5.5 verification subprocess; do not
   remove the marker from runner.py or the guard from commands.py"). Convergence of an
   independent evidence trail with my own line-level reads is why a clean PASS is trustworthy
   here rather than suspect.
4. **Web research performed?** None — all verification was local-file-bound. Tavily not invoked
   (no external lookup required); no fallback occurred.

---

## QA Complete — Verdict: PASS (no edits made)
