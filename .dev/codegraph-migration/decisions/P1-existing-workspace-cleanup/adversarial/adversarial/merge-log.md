# Merge Log

## Metadata
- Base: Variant 1 (`variant-1-original.md`, option-a.md, architect advocate)
- Plan: `refactor-plan.md` (12 changes, auto-approved 2026-10-29T17:05:00Z)
- Executor: merge-executor
- Changes applied: 12 of 12
- Status: SUCCESS
- Output: `../merged-recommendation.md` (decision-record format, 14 H2 sections)
- Timestamp: 2026-10-29T17:10:00Z

## Changes Applied

### Change 1: Serena provenance-tiered exact allowlist
- **Status**: Applied
- **Source**: round2-advocate-b.md §2; invariant-resolutions-proposed.md INV-001; resolution-advocate-{a,b,c}.md
- **Target**: Base step 2 serena matcher (replaced) -> merged §2 (Tier R table) and §3 (Tier K list)
- **Before**: "`serena`: stdio, argv (command + args joined) contains `serena-agent` and `start-mcp-server`, no `env`/`headers`."
- **After**: Tier R = three exact argv rows: (a) registry 050d5ea2..0e7bc31f `uvx` + `--enable-*` form, (b) 5bee1571 `uvx ... --project $(pwd)`, (c) 43112779 `serena start-mcp-server ... --project $(pwd)`, literal `$(pwd)`; Tier K = current pin, bare `--context ide-assistant`, `--project <abs path>`, any other `start-mcp-server` entry, with the INV-001 printed line; non-launcher entries "kept: not a Serena launcher registration". Base stdio + no env/headers guard retained on Tier R. A's QUALIFY (no-shell call style) recorded as satisfied, citing `shell=(sys.platform == "win32")`.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Variant 2 R2 + INV-001/002/003/005 resolutions, Changes 1, 2, 3, 4 -->` (§2); `<!-- Source: Base (original, modified) — Variant 3 handoff + INV-001 Tier K, Changes 1 and 3 -->` (§3)
- **Validation**: Rows checked token-for-token against the orchestrator brief and fault-finder-raw.md INV-001 / invariant-resolutions-proposed.md INV-001. Byte-exact copy from git history and per-row test pinning stated as implementation requirements (plan risk note).

### Change 2: codebase-memory matcher = absolute basename shape
- **Status**: Applied
- **Source**: fault-finder-raw.md INV-002; resolution-advocate-c.md (exact-path request withdrawn)
- **Target**: Base step 2 cbm matcher (replaced) -> merged §2
- **Before**: "`type` stdio (or absent), `args` `[]`, `command` whose basename is `codebase-memory-mcp`, no `env`/`headers`."
- **After**: absolute `command`, basename `codebase-memory-mcp`, `type` stdio or absent, `args` absent or `[]`, `env`/`headers` absent or empty; cites `install_codebase_memory.py:597-603`, `install_mcp.py:866`.
- **Provenance tag**: §2 tag above
- **Validation**: Matches plan integration text exactly.

### Change 3: Binary-existence gate + absolute upstream uninstall hint
- **Status**: Applied
- **Source**: Variant 2 R1/R2 ordering; INV-003; INV-005; resolution-advocate-b.md QUALIFY
- **Target**: Base step 2 + step 5 (modified) -> merged §2 (gate), §3 (kind-B kept), §8 (hint + removal note)
- **Before**: Step 5 printed bare `codebase-memory-mcp uninstall -y` "for kind-B workspaces"; no gate.
- **After**: keep registration when command equals unresolved `Path.home().absolute()/.local/bin/codebase-memory-mcp` and file exists; absolute `"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"` printed whenever that file exists, with the plan's label; other matched entries removed with the self-install note.
- **Provenance tag**: §2, §3, §8 tags
- **Validation**: B's qualify (print whenever the file exists, whatever matched) present in §8.

### Change 4: IronClaude receipt and `.pending` marker cleanup
- **Status**: Applied
- **Source**: Variant 2; A-006; Variant 3 condition; INV-011
- **Target**: Base step 4 never-touch list (exception inserted) -> merged §2 (rule) and §4 (exception line)
- **Before**: Base did not mention the receipt or marker.
- **After**: delete both files only when the binary is absent and each passes the existing predicates (regular, user-owned, single link, `mode & 0o077 == 0`, `O_NOFOLLOW`; `_check_install_directory`); otherwise listed.
- **Provenance tag**: §2 tag; §4 `<!-- Source: Base (original, modified) — step 4 list extended with Change 4 exception and permission/hook note -->`
- **Validation**: Predicate list matches INV-011 resolution and resolution-advocate-b.md row.

### Change 5: One classifier, fixed action order
- **Status**: Applied
- **Source**: INV-004; INV-013
- **Target**: Base Implementation paragraph (modified) -> merged §7 (Ordering) and §9
- **Before**: Per-name read then remove; no order; no shared classifier.
- **After**: pure `classify_retired_entries() -> list[(name, verdict, reason)]`; fixed order receipt/marker -> cbm -> serena; shared by install, `--list`, `doctor`, `update`.
- **Provenance tag**: §7 `<!-- Source: Base (original, modified) — placement replaced per INV-007, Changes 5 and 7 -->`; §9 `<!-- Source: Base (original, modified) — Implementation paragraph, Changes 5, 6, 7 -->`
- **Validation**: Consistent with §8 read-only surfaces and §12 one-run convergence test.

### Change 6: Safe removal helper
- **Status**: Applied
- **Source**: INV-006; base U-001
- **Target**: Base step 3 + Implementation (modified) -> merged §6 (failure rows) and §9
- **Before**: "name-parameterised version of `_cleanup_user_native_registration`".
- **After**: `_remove_exact_user_entry(name, matcher)`, matcher required, re-match before remove, three post-remove outcomes, never retried; Phase 2 reuses it.
- **Provenance tag**: §6 `<!-- Source: Base (original, modified) — step 6 plus INV-006/007/012 failure classes, Changes 6, 7, 9 -->`; §9 tag
- **Validation**: Sub-second TOCTOU residual carried to §11.

### Change 7: Execution bounds and placement
- **Status**: Applied
- **Source**: INV-007; resolution-advocate-c.md QUALIFY; A-003; resolution-advocate-a.md conditions
- **Target**: Base step 3 timeout + step 6 + placement (replaced) -> merged §6 and §7
- **Before**: `_run_registration_command` with timeout lowered to 10 s; missing CLI "skip with a note".
- **After**: direct exec, `start_new_session=True`, process-group kill, 10 s/call, 15 s step cap, `shutil.which` skip note printing each manual `claude mcp remove <name> --scope user`; slot `main.py:254`, before `main.py:264`, own `try/except Exception`. A's condition (freed time > 15 s, UNVERIFIED) included.
- **Provenance tag**: §6 and §7 tags
- **Validation**: Base "place first" (A R2) appears only in §13 as rejected.

### Change 8: Read-only surfaces
- **Status**: Applied
- **Source**: Variant 3 U-005 (cheaper form); INV-008; INV-009
- **Target**: new subsection -> merged §8 "Read-only surfaces"
- **Before**: none.
- **After**: `install --list` one line per retired name (verdict strings from round2-advocate-c.md §1); `doctor` warns, never fails; `update` prints only the read-only notice.
- **Provenance tag**: `<!-- Source: Variant 3 (U-005, cheaper form) + INV-008/009, Change 8; Base step 5 modified by Change 9 -->`
- **Validation**: Cites `main.py:161-186`, `docs/user-guide/mcp-installation.md:24`.

### Change 9: User-facing messages
- **Status**: Applied
- **Source**: INV-008; INV-012; base step 5
- **Target**: Base step 5 (modified) -> merged §5, §6, §8 "Messages"
- **Before**: printed `uv tool uninstall serena-agent`, bare upstream uninstall, `rm -rf ~/.serena`.
- **After**: one line per action; restart note; cause-specific unknown warnings; data delete commands "only if you no longer need them"; `uv tool uninstall serena-agent` with the Coder label.
- **Provenance tag**: §8 tag; §5 `<!-- Source: Base (original) — keep-indexes policy; delete commands from Change 9 -->`
- **Validation**: Restart text taken verbatim from INV-008 resolution.

### Change 10: Coder and plugin-mirror handoffs
- **Status**: Applied
- **Source**: Variant 3 step 4; INV-009d; INV-014
- **Target**: new section -> merged §10
- **Before**: Base Against bullet only ("bundle re-adds `serena` ... until Coder's own change lands").
- **After**: Coder Phase 2 handoff items; plugin mirror paths into Phase 1 search scope; upstream uninstaller for `~/.local/bin`; no Coder heuristic.
- **Provenance tag**: `<!-- Source: Variant 3 step 4 + INV-009d + INV-014, Change 10 -->`
- **Validation**: Matches plan integration text.

### Change 11: Goal-met-except record and residual risks
- **Status**: Applied
- **Source**: INV-010; round2-advocate-c.md residual statement; invariant-probe.md residuals
- **Target**: new section -> merged §11
- **Before**: Base "For" claimed "Meets the goal on both paths".
- **After**: 7-row exception table with closing conditions; 5 residual risks from the plan; round2-advocate-c.md statement quoted verbatim.
- **Provenance tag**: `<!-- Source: INV-010 + round2-advocate-c.md residual statement + invariant-probe.md residuals, Change 11 -->`
- **Validation**: Base "goal met" claim not carried forward (superseded).

### Change 12: Acceptance tests
- **Status**: Applied
- **Source**: Base "4-6 unit tests plus one CLI integration test", expanded
- **Target**: Base Implementation (modified) -> merged §12
- **Before**: "About 4-6 unit tests plus one CLI integration test (temp HOME, stub `claude`)."
- **After**: classifier table test, helper tests, bound tests, CLI integration test, `update.sh` contract (`tests/cli/test_update_script.py:13-18`).
- **Provenance tag**: `<!-- Source: Base (original, modified) — "4-6 unit tests plus one CLI integration test", expanded by Change 12 -->`
- **Validation**: Every plan test item present.

### Non-change content
- §13 Rejected alternatives: one line per row of the plan's "Changes NOT Being Made" table (8 rows, all present).
- §14 Debate summary: scores, convergence and gate status from base-selection.md, debate-transcript.md, invariant-probe.md.
- Base "Against" bullets and stale-primitive paragraph: folded into §9 (acceptance-search allowlist), §10 and §11 (non-`--force` correction), per base-selection.md "Strengths to Preserve" item 6.
- §4 permission note ("IronClaude ships no permission entries ... only the `hooks.json:47` matcher, refreshed under `--force`"): taken from the orchestrator brief and diff-analysis.md:26; the "no permission entries" half is not independently verified by this executor.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS (one H1; 14 H2 numbered 1-14; no skipped levels; bold run-in labels only below H2)
- Section ordering: PASS (matches the requested order 1-14)
- Provenance tags: 14 of 14 H2 sections preceded by a `<!-- Source: ... -->` tag; 3-line provenance header present

### Reference Integrity
- Total internal references: 16 (7 "Section N" cross-references; 9 file links: `../context.md`, `adversarial/base-selection.md`, `adversarial/debate-transcript.md`, `adversarial/invariant-probe.md`, `adversarial/invariant-resolutions-proposed.md`, `adversarial/resolution-advocate-{a,b,c}.md` (counted once), `adversarial/refactor-plan.md`, `adversarial/merge-log.md`, plus round2-advocate-c.md by name)
- Resolved: 16
- Broken: 0 (existence checked on disk; `merge-log.md` is this file)

### Contradiction Re-scan
- New contradictions introduced: 0
- Checked: placement (only "end slot" stated; "first" appears only as rejected); serena matcher (substring form appears only as rejected); upstream uninstall (only the absolute form is recommended; bare form named only as never used); `--force` scope (step not gated on `--force`, while stale-text cleanup and the goal claim are `--force`-only; consistent); receipt deletion vs kind-B keep (both gated on the same binary existence; consistent).
- Inherited inconsistency in the inputs (not introduced, not resolved by this merge): INV-011's resolution text says a command path differing from the current unresolved HOME form is reported "kept: path differs from current HOME", while Change 3 says every matched entry other than the current-HOME `~/.local/bin` path with the binary present is removed. The merge follows Change 3 (the plan). An old-HOME `~/.local/bin/codebase-memory-mcp` entry is therefore removed. Escalated to the orchestrator for a decision; no text was improvised.
- Not added (outside plan): round2-advocate-c.md §2 condition "print the exact removed argv and tell the user how to register Serena themselves" for Tier R removals; Change 9 only specifies "one line per action".

## Summary
- Planned: 12
- Applied: 12
- Failed: 0
- Skipped: 0
- Merged document: `../merged-recommendation.md`, 187 lines (target 180-260)
- Final status: SUCCESS, with one inherited input inconsistency (INV-011 vs Change 3) and one unadopted advocate condition flagged above

## Orchestrator Post-Merge Resolution (2026-10-29T17:20:00Z)

Both flagged items were decided by the orchestrator (debate-orchestrator role) and applied to `../merged-recommendation.md`:

1. **INV-011 vs Change 3 (old-HOME `~/.local/bin` entry):** INV-011's resolution was unanimously accepted in the resolution round (`resolution-advocate-{a,b,c}.md`) and is the more conservative rule, so it takes precedence. Section 2 "Binary gate" now keeps an entry whose command is `<other home>/.local/bin/codebase-memory-mcp` and reports "kept: path differs from current HOME"; Section 12 gained a matching classifier test row. Provenance: inline "orchestrator post-merge fix".
2. **Advocate C's Tier R condition:** C accepted automatic Tier R removal on condition that the removed argv and a re-registration command are printed (round2-advocate-c.md §2). Adopted as an additional message line in Section 8 (re-registration example uses IronClaude's option order, `install_mcp.py:1142-1159`).

Re-validation after the fixes: heading hierarchy unchanged (1 H1, 14 H2); references unchanged (16 resolved, 0 broken); contradiction re-scan: 0 new, 0 inherited remaining.

**Final status: SUCCESS (no open inconsistencies).**
