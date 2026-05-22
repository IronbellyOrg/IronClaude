# QA Report — Research Gate

**Topic:** TRACK 1 — FU-001 sprint runner .sprint-exitcode migration
**Date:** 2026-05-18
**Phase:** research-gate
**Fix cycle:** N/A (first pass)
**Assigned files:** 01-file-inventory.md, 02-config-pattern.md, 03-template-examples.md

---

## Overall Verdict: FAIL

Multiple CRITICAL line-number citations in research files 01 and 02 are wrong by 4-40 lines — verified by independent grep against the actual source files. A builder following these citations would Edit the wrong lines. This is a hard-fail: line:column precision is the only reason for cited evidence to exist in the first place. All findings (CRITICAL + IMPORTANT) must be resolved before synthesis / builder hand-off.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — all 3 assigned files exist with Status: Complete + Summary | PASS | `Read` of each file shows `**Status:** Complete` and § Summary (01:line 176; 02:line 422; 03:contains Sources block at line 289). |
| 2 | Evidence density — file paths & line numbers cite real code | **FAIL** | See Issues Found §2. `executor.py:1714` cited as writer site — actual line is **1754** (`grep -n 'sprint-exitcode' executor.py`). 8 of 11 executor.py line citations in research 01 are off by 40 lines. commands.py citations off by 8-10 lines. models.py off by 1-3. |
| 3 | Scope coverage — every key area from scope examined | PASS | executor.py:1754 (writer) ✓, tmux.py:166 (reader) ✓, SprintConfig dataclass at models.py:357 ✓, 40 tracked sentinels enumerated ✓ (`git ls-files` confirms exactly 40), `.gitignore:222` ✓, sc-crash-recovery `bootstrap_scan.sh:90,126` ✓. |
| 4 | Documentation cross-validation — doc claims tagged | PASS (N/A in strict sense) | No external/doc-sourced architectural claims requiring [CODE-VERIFIED]/[CODE-CONTRADICTED] tags — all claims trace to code reads or git ls-files. Doc references at 01 §1 are factual locations of references, not architectural assertions. |
| 5 | Contradiction resolution — no unresolved conflicts | PASS | Research 01 and 02 agree on writer/reader sites, dataclass location, and override path. Both correctly identify 2 source-code touch points. No internal contradictions. |
| 6 | Gap severity — all gaps classified | PARTIAL | Research files don't carry an explicit "Gaps and Questions" section but distribute implicit deferrals across §4.5, §4.6, §5 in research 02. The PRIMARY gap is the line-number drift surfaced in this report. |
| 7 | Depth appropriateness — Standard tier match | PASS | Coverage is file-level + key data-flow trace (writer→reader). Track scope of "migrate 2 source lines + remove 40 tracked files" is well-matched to research depth. Not over-engineered for Standard. |
| 8 | Integration point coverage — CLI flag, env-var resolver, cross-skill update | PASS | commands.py CLI flag path documented (research 02 §4.3); SPRINT_STATE_DIR env-var convention documented (§3 takeaways); sc-crash-recovery cross-skill impact called out in 01 §1 + 01 §5 + 02 §4.6. |
| 9 | Pattern documentation — SprintConfig + env-var conventions | PASS | Research 02 §3 captures env-var convention exhaustively (`os.environ.get(VAR, default)` at CLI layer only). SprintConfig dataclass pattern with `__post_init__` derivation captured at §1 + §4. |
| 10 | Incremental writing compliance | PASS | All three files show structural staging (Scope/Hypothesis → numbered sections → Summary), consistent with iterative writing. No one-shot signs (no abrupt topic jumps, no truncated tables). |

---

## Summary
- Checks passed: 8 / 10 (counting partial)
- Checks failed: 1 CRITICAL (evidence density), 1 PARTIAL (gap severity)
- Critical issues: **2** (line-number drift in 01; line-number drift in 02)
- Important issues: **2** (line-count drift in 01 §4 table; bootstrap_scan.sh discoverability mitigation not fully scoped)
- Minor issues: **1** (research file 02 missing explicit "Gaps and Questions" section heading)
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | 01-file-inventory.md §1 + §2 + §5 | **Sentinel writer line is wrong.** Research cites `executor.py:1714` for the `.sprint-exitcode` writer (4 occurrences across §1, §2, §5). Verified actual location is `executor.py:1754` via `grep -n 'sprint-exitcode' src/superclaude/cli/sprint/executor.py`. Drift = +40 lines. A builder Edit at line 1714 would patch unrelated code (likely a checkpoint manifest write inside the same function). | Replace every occurrence of `executor.py:1714` with `executor.py:1754` in 01 §1 table row, §2 table row "write target via release_dir", §5 first bullet. Re-grep before re-publishing. |
| 2 | CRITICAL | 01-file-inventory.md §2 (lines 62-68) | **Multiple secondary `release_dir` lines in executor.py are wrong.** Research cites `executor.py:1668` (build_manifest), `1669` (manifest_path), `1789` (declared = extract_checkpoint_paths), `1845` (CP-P{phase} path), `1861` (artifacts_dir), `1869` (contaminated.append). Verified actuals via `grep -n 'release_dir' executor.py`: `1708`, `1709`, `1829`, `1885`, `1901`, `1909`. All drifted by +40. Same systemic drift as Issue 1 — research was written against a stale snapshot of executor.py or the file has since grown. | Re-run `grep -n 'release_dir' src/superclaude/cli/sprint/executor.py` and replace every executor.py line citation in 01 §2 with the current value. Add a footnote: "Line numbers as of executor.py rev <sha>". |
| 3 | CRITICAL | 02-config-pattern.md §2 production path + §4.3 | **commands.py line citations drift by 8-10 lines.** Research cites `commands.py:169` (click option name), `:189` (param signature), `:224-228` (override block), `:211` (CLAUDE_MODEL env-var read), `:225-228` (override). Verified actuals: click option `"--release-dir"` is at lines `176-181`, the `release_dir_override` *variable name* at line `177`, the `def run` param `release_dir_override: Path \| None` at line `197`, the override block `if release_dir_override is not None: ... object.__setattr__(...)` at lines `234-237`, and `os.environ.get("CLAUDE_MODEL", "")` at line `220`. Drift = +6 to +10 lines. A builder following research 02 §4.3 instructions to "Add CLI option mirroring the env-var convention used for CLAUDE_MODEL (around line 211)" would land in the wrong block. | Re-grep `release_dir` and `os.environ` in commands.py and replace all line citations in 02 §2 (production path bullets 1-3) and §4.3 step 1 with the current values. |
| 4 | CRITICAL | 02-config-pattern.md §1 SprintConfig field table + post_init lines | **models.py line citations drift by 1-3 lines throughout.** Research cites field block as `models.py:347-396` with `release_dir` at line `358`, `__post_init__` at `398-444`, `work_dir` mirror at `403`, `wiring_gate_mode` derivation at `441-444`. Verified actuals: `release_dir` field at line `358` (CORRECT), but the mirror `object.__setattr__(self, "work_dir", self.release_dir)` is at line `404` (not 403), and the wiring_gate_mode derivation block is at `439-443` (not 441-444). The post_init range is `400-444` not `398-444`. Smaller drift than 01 but still systematically wrong. Research 02 §4.2 instructs a builder to "Append to SprintConfig.__post_init__ (around models.py:444)" — that line is the closing of post_init, so the instruction is borderline correct but the line number is mis-cited as `441-444` (the wiring derivation) above. | Re-grep `release_dir`, `__post_init__`, and `wiring_gate_mode` in models.py and update §1 field table line numbers and §1.__post_init__ subsection bullets to match. |
| 5 | IMPORTANT | 01-file-inventory.md §4 file inventory table | **Line counts in §4 are stale** — research lists `executor.py 2096`, `commands.py 423`, `config.py 501`, `models.py 850`, total `8417`. Verified actuals via `wc -l src/superclaude/cli/sprint/*.py`: `executor.py 2136`, `commands.py 433`, `config.py 503`, `models.py 857`, total `8476`. This is consistent with executor.py having grown ~40 lines since research was authored (which matches the +40 drift in §1, §2, §5 line numbers — explaining the root cause). | Re-run `wc -l` and update the §4 table. Add a one-line note in §4 explaining the line counts are point-in-time. |
| 6 | IMPORTANT | 01-file-inventory.md §5 + 02-config-pattern.md §4.6 | **Cross-skill discoverability mitigation under-scoped.** Research correctly identifies that `bootstrap_scan.sh:90,126` reads `$d/.sprint-exitcode` and that `recent_files ".sprint-exitcode"` (line 126) recursively scans `.dev/releases/**`. After the migration moves sentinels to `.dev/sprint-state/`, the crash-recovery skill would either (a) stop finding any recent sentinels, or (b) require a parallel update to its scan path. Research mentions this as "must remain discoverable" but does not specify whether the crash-recovery update belongs in this track or a separate track, and does not document the exact lines (90, 126) that need parallel patches. | In 01 §5 final bullet or a new "Cross-skill impact" subsection, add: (a) explicit recommendation that `bootstrap_scan.sh:90,126` either be patched in the same release (FU-001) or that the new `state_dir` location remain a discoverable sibling of `release_dir` (e.g., `release_dir.parent / "sprint-state" / release_dir.name`). (b) Note whether this is in-scope or out-of-scope for the current track. The current ambiguity will cause the builder to either silently break crash-recovery or get blocked at the phase gate. |
| 7 | MINOR | 02-config-pattern.md structure | **No explicit "Gaps and Questions" section.** The Research Gate checklist item 6 expects an explicit section listing gaps. Research 02 distributes implicit deferrals across §4.5 (.gitignore "out of strict scope"), §4.6 (override-override re-derivation as open design decision), and §5 (test additions needed). A consolidated "Gaps and Questions" section would make these explicit and gate-checkable. | Add a `## 6. Gaps and Questions` section consolidating: (a) `.gitignore` change scope (in or out), (b) does `--release-dir` override re-derive `state_dir`, (c) cross-skill update for bootstrap_scan.sh (see Issue 6). |

---

## Actions Taken

None — `fix_authorization: false`. Issues are documented for the orchestrator / fix-cycle agent to resolve.

---

## Confidence

- **Verified:** 10/10 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
- **Tool engagement:** Read: 4 | Grep: 11 (via Bash) | Glob: 0 | Bash: 11
- Every line-number claim was verified via independent grep against the actual source files in `src/superclaude/cli/sprint/`. The 40-file tracked inventory was verified via `git ls-files '*.sprint-exitcode' | wc -l` = 40 ✓. The `.gitignore:222` claim was verified via `grep -n` ✓. The `bootstrap_scan.sh:90,126` claim was verified via `grep -n` ✓. The MDTM template at `.claude/templates/workflow/02_mdtm_template_complex_task.md` was verified to exist (1197 lines).
- **Self-audit:** A user asking "did you actually verify?" can be pointed to: (a) `grep -n 'sprint-exitcode' executor.py` showing line 1754, (b) `grep -n 'release_dir' executor.py` showing the drifted line numbers, (c) `grep -n 'release_dir' commands.py` showing 177/197/234-237, (d) `wc -l` output showing file size drift consistent with the line drift. This is not "looks plausible" — this is "I ran the commands and the research is wrong."

---

## Recommendations

**For the orchestrator (next steps before builder hand-off):**

1. **Spawn a fix-cycle agent** to re-grep every `file:line` citation in research files 01 and 02 against the current `src/superclaude/cli/sprint/` and update in-place. Maximum 3 fix cycles per protocol. This is mechanical — the agent just needs to re-run the greps and update the citations.
2. **Add a freshness footer** to each research file: `Line numbers verified against git rev <sha> at <ISO timestamp>`. This makes the staleness root cause visible if it recurs.
3. **Do not proceed to synthesis / builder** until line-number drift is resolved. A task-builder skill that emits Edit calls against `executor.py:1714` will silently corrupt unrelated code (the line 1714 region is inside the checkpoint manifest writer block, not the sentinel writer).
4. **Cross-skill update for sc-crash-recovery** (Issue 6) must be decided before builder hand-off — either (a) widen scope to include `bootstrap_scan.sh:90,126` patches, or (b) choose a `state_dir` location that bootstrap_scan can still find without code change. Recommend (b) for minimum blast radius: `state_dir = release_dir.parent / "sprint-state" / release_dir.name` keeps it adjacent to the release dir so `recent_files` can still discover it with a small scan-path widening.

**Root cause analysis:** The +40-line drift in executor.py and +10-line drift in commands.py is consistent with the research having been written against a snapshot taken before recent changes landed. The research agent likely cached its initial Read in context and never re-Read after the codebase mutated. This is a known anti-pattern (S1 + S3 in the context-freshness discipline section of CLAUDE.md). The fix-cycle agent should re-Read each file before re-citing.

---

## QA Complete

