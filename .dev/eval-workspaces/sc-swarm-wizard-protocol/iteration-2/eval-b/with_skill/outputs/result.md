# sc-swarm-wizard-protocol — eval-b (with_skill) result

## RESULT block

- **LENS:** `doc-completeness` (plain-language intent: "audit my docs for gaps / staleness")
- **REVIEWERS_DEFAULT:** 3 (lens default for `doc-completeness`; recipe `findings_table_v1`)
- **TRANSPORT:** `stub` (practice/dry-run; no real run performed)
- **DRYRUN_CMD:**
  `uv run superclaude swarm run --lens doc-completeness --target docs/swarm/README.md --output .dev/swarm-runs/doc-completeness-20260619T061408 --transport stub`
- **DRYRUN_VERIFIED:** yes — exit 0; stdout `swarm run: dispatched job (mode=lens, workers=3, results=3)`; `.swarm-state.json` `state == "terminal"`; `return-contract.yaml` present with `status: success`, 3/3 workers; `merged.md` + per-worker `*.final.md` written.
- **NEXT_CMD:** `/sc:document` — the lens's rendered hand-off. Verbatim from the contract:
  `/sc:document --apply <existing-review>,…/doc-completeness-00-…final.md,…01-…final.md,…02-…final.md`
- **NOTES:** see below — the wizard followed all 5 waves, the mandatory stub gate passed, and the Wave 0 ground-truth cross-check surfaced concrete doc staleness in the target README itself.

---

## How the skill drove this (wave trace)

- **Wave 0 (ground & orient):** confirmed `swarm --help` reachable; loaded `refs/cli-contract.md`; cross-checked live `run --help`. `validate-lenses` → `registry OK (8 entries inspected, 7 validated)`. Confirmed `--tui` is a REAL flag on `run --help` and the `--transport` help text wrongly implies an `openai_compat` default while the `--lens` path actually defaults to `stub`.
- **Wave 1 (interview):** embedded answers supplied (goal = audit docs for gaps/staleness; target = README; run type = stub). Goal → `doc-completeness` lens via the mapping table. No `AskUserQuestion` needed.
- **Wave 2 (map/build/validate):** plan = `{lens=doc-completeness, target=docs/swarm/README.md, output=.dev/swarm-runs/doc-completeness-<ts>/, transport=stub, reviewers=3}`. Pre-flight: target exists, 9053 bytes (well above the 50-non-ws-byte IMM-4 floor); exactly one input mode; `--lens` has both `--target` + `--output`; idempotent timestamped output dir. `validate-lenses` passed.
- **Wave 3 (stub dry-run — MANDATORY gate):** ran and verified all three success conditions. PASS.
- **Wave 4 (real run):** SKIPPED by design — task is practice/stub only, no go-ahead for a real run. `status: cancelled`-equivalent for the real leg.
- **Wave 5 (summarize):** parsed `return-contract.yaml` + `.swarm-state.json`; recommended `/sc:document`.

---

## Documentation audit findings (the actual user request)

The stub run proves the pipeline but emits placeholder text, so the real gaps come from cross-checking the README against the live CLI + the verified `cli-contract.md` (empirically re-confirmed this session). The README at `docs/swarm/README.md` is **internally consistent and well-structured, but materially STALE in one major area** plus a few smaller gaps:

### STALE — high severity

1. **"Implementation status" banner (lines 8–15) and "What a run emits today" (lines 94–123) are out of date.** The README states the Wave 2/3 amalgamation writer (M5) is "**not yet wired into the run path**" and that a fresh inline `--lens` run emits "**exactly four** files" with `merged.md` / `return-contract.yaml` / per-worker outputs explicitly NOT emitted. This was empirically falsified THIS run: a fresh inline `--lens doc-completeness … --transport stub` run wrote `merged.md`, `return-contract.yaml`, AND per-worker `*.final.md` + `*.meta.json` (11 files total), reaching `state: terminal` / `status: success`. This matches STALE-DOC-WARNING #3 in the skill's contract ref. **The whole "fresh = 4 files, M5 unwired" framing needs rewriting to the current behavior (fresh inline runs DO amalgamate).**
   - Knock-on: the "Resume mode is different" note (lines 113–119) frames `return-contract.yaml`/`merged.md` as resume-only additions; that distinction is now largely moot for fresh inline runs.

### GAP — medium severity

2. **`--tui` is undocumented in the command surface.** The README's command table (lines 36–54) and the linked `command-reference.md` omit the real `--tui` flag (confirmed present in live `run --help`; STALE-DOC-WARNING #1). A user watching a long run via the README would never learn the live-dashboard option. The "Monitoring Patterns" link should cover `--tui` (TTY-only, fresh-run-only, XOR `--detached`).
3. **Transport default is mis-stated upstream.** Line 86 correctly notes `stub` is "the default for `--lens`", which is GOOD — but it should explicitly warn that the CLI's own `--transport` help text contradicts this (says openai_compat default). Without that note a reader who runs `--help` will be confused about which is authoritative.

### GAP — low severity / verify

4. **`done.json` semantics need a one-line clarifier for inline runs.** The README mentions `done.json` as a "terminal sentinel on the success path" (line 13) and ties it to M5. Per verified contract, `done.json` is NOT written on fresh inline runs (only on detached/resume/`kill`). The doc should state plainly: inline completion = `state==terminal` + `return-contract.yaml`, do not wait on `done.json`.
5. **`--custom-prompt-dir` drift (cross-doc).** Contract ref flags that `user-guide.md` shows `--custom-prompt-dir` as a `run` flag, but there is no such flag (it is a JobSpec field). Not in README directly, but the README links `user-guide.md` as canonical — worth a sweep when fixing the set.

### Strengths (no change needed)

- Lens/recipe catalog (lines 65–79), transport table, exit-code convention (0/1/2), and the `uv run` warning note are all accurate and match the live CLI.
- The 8-subcommand / 7-validated framing matches `validate-lenses` output exactly.

### Recommended next action

`/sc:document` on the merged review to apply fixes — primarily rewriting the "implementation status" + "what a run emits today" sections to current behavior, adding `--tui` to the command surface, and adding the inline-vs-detached `done.json` clarifier. The lens-rendered hand-off command is in the RESULT block above.
