# Adversarial QA — Evidence-Quality Gate

**Lens:** evidence-quality (every research claim must cite a real `file:line`; ~30% spot-checked against actual files).
**Repo:** `/config/workspace/IronClaude` (read-only).
**Research under review:** `.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/research/{01,02,03}`
**Date:** 2026-06-09

---

## Mandated checks

### Check 1 — Are the two `--file` snippets quoted accurately from process.py? PASS

File 01 §1 quotes Branch A (`:191-199`, emission line `:199`) and Branch B (`:201-204`, emission line `:204`).
Verified against `src/superclaude/cli/prd/process.py:191-206` (Read): both snippets are **verbatim accurate**, including indentation, the `_PHASE_ALLOWED_REFS.get(base_step, [])` loop, the `ref_path.is_file()` / `.stat().st_size` / `> _FILE_SIZE_THRESHOLD` guard, the `file_args.extend(["--file", str(ref_path)])` emission at `:199`, the `_SPEC_FILE_STEPS` branch, and `file_args.extend(["--file", spec_path])` at `:204`. `return file_args` at `:206` confirmed. No discrepancy.

### Check 2 — Is "all PRD refs <50KB" verifiable? PASS (with note: not a literal research claim)

The phrase "all PRD refs <50KB" appears in the **QA prompt**, not in the research artifacts (grep for `all.*ref.*50` / `ref.*under.*50` across the research dir returns no such literal claim).

What the research *does* assert is reused-primitive context: `_FILE_SIZE_THRESHOLD = 50_000` is the inline-vs-`--file` cutoff (file 01 §4, `process.py:115` — verified), and Branch A only emits `--file` for refs whose `stat().st_size > 50_000`.

Verifying the underlying fact directly: `wc -c` on `src/superclaude/skills/prd/refs/` — five files, largest `agent-prompts.md` = 22,855 bytes; others 6,032 / 9,114 / 9,545 / 16,528. **All five are < 50,000 bytes.** Consequently Branch A (refs>50KB) never fires for the real shipped refs (no ref exceeds 50KB; `find -size +50000c` returns empty). This is consistent with — and strengthens — the research's framing that the refs branch is effectively dead in practice and that removal is safe. Claim is verifiable and TRUE.

Minor note (file 02 §4, lines 124-133): the excerpt heading says `build_task_file_prompt` "reads each ref file directly via `_read_file`," and the quoted block includes `notes = _read_required(config.task_dir / "research-notes.md", ...)`. That `notes` line is actually `_read_required` (not `_read_file`) and is sourced from `task_dir`, not `skill_refs_dir` — so `research-notes.md` is **not** a `skills/prd/refs/` file (confirmed: it does not exist there). The block is explicitly labeled "representative excerpt," the five true `_read_file(config.skill_refs_dir / ...)` lines below it are accurate, and the substantive claim (refs delivered inline via `_read_file`) holds. Rated **MINOR** (imprecise grouping; does not affect any actionable conclusion).

### Check 3 — Is `grep -rn '"--file"' src/superclaude/cli/prd/` = 2 hits correct? PASS

Ran verbatim. Output:
```
src/superclaude/cli/prd/process.py:199:                    file_args.extend(["--file", str(ref_path)])
src/superclaude/cli/prd/process.py:204:                    file_args.extend(["--file", spec_path])
```
Exactly 2 hits at lines 199 and 204 — matches file 01 §7 (`:188-192`) and the summary (`:200`) precisely. The acceptance-gate "must be 0 after fix" framing is sound.

### Check 4 — Do sibling executors forbid `--file` per real comment lines? PASS

Verified all three module docstrings (Read):
- `roadmap/executor.py:7-9` — "Context isolation: each subprocess receives only its prompt via inline embedding. / No --continue, --session, --resume, or --file flags are passed (FR-003, FR-023). / --file is a cloud download mechanism and does not inject local file content." (file 02 §5 quotes `:7-9` verbatim — exact match.)
- `tasklist/executor.py:9-10` — "Context isolation… / --file is a cloud download mechanism and does not inject local file content." (file 02 cites `:9-10` — exact match.)
- `roadmap/validate_executor.py:10-11` — same two lines (file 02 cites `:10-11` — exact match.)

Corroborating cites in file 01 §7 (`:194`) also verified: `roadmap/executor.py:1107-1108` ("--file is broken (cloud download mechanism, not local file injector)") and `cli_portify/prompts.py:47` ("--file is broken (OQ-008)") both present and accurate. The "sibling executors forbid --file" claim is backed by real comment lines.

---

## Additional 30% spot-check (beyond mandated four)

All verified accurate against source via Read/sed:

| Cited anchor | Claim | Result |
|---|---|---|
| `process.py:169-206` | `_build_file_args` method bounds (`@staticmethod :169`, `def :170`, return `:206`) | PASS |
| `process.py:95` / `:115` / `:121` | constant defs `_PHASE_ALLOWED_REFS` / `_FILE_SIZE_THRESHOLD` / `_SPEC_FILE_STEPS` | PASS (exact) |
| `process.py:133` / `:180` / `:187` | class docstring `--file` line; method docstring `_SPEC_FILE_STEPS` mention; `base_step` normalize local | PASS |
| pipeline `process.py:48` / `:63` / `:94` / `:107-111` | `extra_args` param default; `self.extra_args = extra_args or []`; `cmd.extend(self.extra_args)`; `os.environ.copy()` + pops | PASS (all exact) |
| `prompts.py:34` `_TRUNCATION_MARKER` | `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"` (em-dash) | PASS (exact) |
| `prompts.py:42-47` `_read_file` | full snippet incl. `content[:max_bytes] + _TRUNCATION_MARKER` | PASS (verbatim) |
| `prompts.py:120-138` `_authoritative_specs_block` | full function incl. empty-return `:130-131` and "MUST Read each one IN FULL" wording | PASS (verbatim) |
| `prompts.py:507-524` `build_task_file_prompt` reads | five `_read_file(skill_refs_dir/...)` ref reads | PASS (see MINOR note re `notes`/`_read_required`) |
| `test_spec_flag.py:485-487` | `assert args == ["--file", str(a), "--file", str(b)]` | PASS (exact) |
| `test_spec_flag.py:495-498` | `investigation-3` normalize; `assert "--file" in args` / `assert str(spec) in args` | PASS (exact) |
| `test_spec_flag.py:506/510/515` | three `== []` assertions calling `_build_file_args` | PASS (exact) |

No fabricated or mis-numbered citations found in the spot-check sample (≈12 anchors across all three files, well over 30%).

---

## Findings summary

| Severity | Finding |
|---|---|
| MINOR | File 02 §4 (lines 124-133) groups `notes = _read_required(task_dir/research-notes.md, ...)` under a heading describing `_read_file` ref reads; `research-notes.md` is task_dir-sourced and uses `_read_required`, not a `skills/prd/refs/` file. Excerpt is labeled "representative" and the actionable claim (refs inlined via `_read_file`) is correct. No downstream impact. |

No CRITICAL or IMPORTANT findings. All four mandated claims are accurately cited and independently reproducible. The "2 hits" acceptance grep, the two `--file` snippets, the sibling no-`--file` docstrings, and the underlying ref-size facts all check out. Citations are consistently real and line-accurate.

---

VERDICT: PASS
