# Revise report: orca-worker-contract-spec, gate loop (REVISE prompt)

- Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before editing)
- Candidate revised in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Blocking ids revised: GR-B1, GR-B2 (from the Reviser brief in `.dev/orca-command-refactor/review/gate.md:69-71`)
- Not revised (outside the brief): M-1 to M-12, N-1 to N-4 (`review/gate.md:41-61`)
- Spec-panel: not run. No PASS is awarded here; the RE-REVIEW decides.

## Byte accounting

| Measure | Bytes |
|---|---|
| Before (sha256 `d7b701458ccab1292a94ee6f2c84881cfc91dbf20d522f329d407123b072388d`, equal to `gate.md:7`) | 58948 |
| After (sha256 `92a25ab664b0803fb12bd23716793e4aba1f0dc0171d60f876c747679cfcf973`) | 59510 |
| Net change | +562 |

Line count is 285 before and after; every edit changed text inside an existing line.

| Finding id | Applied at (after-revision line numbers) | Bytes added | Bytes deleted | Net |
|---|---|---|---|---|
| GR-B1 | spec:64, WC-6: one sentence added | 193 | 0 | +193 |
| GR-B1 | spec:87, init-lite row, "Resume (WC-6)" cell reworded and "Small fix" cell filled | 203 | 39 | +164 |
| GR-B2 | spec:73, section 2.3: clause on `--unattended` reworded | 296 | 91 | +205 |
| Total | | 692 | 130 | +562 |

Check: 58948 + 562 = 59510. Byte counts were taken from the literal inserted and removed strings.

## Finding rows

| Id | Disposition | Where | Reason |
|---|---|---|---|
| GR-B1 | Applied | spec:64 (WC-6) and spec:87 (init-lite row) | Gate option 1 was taken for the row and option 2 for WC-6 together, because WC-6 says a command "either resumes ... or ... writes each run into a fresh output directory", and init-lite does neither. The init-lite row now records the overwrite as a WC-6 failure, and its "Small fix" cell adds a P1 change: under `--unattended`, refuse to overwrite an existing marked report and write the contract as `blocked`. WC-6 gains the matching clause, which resolves through WC-2 (c). Evidence: the overwrite is at `.dev/orca-command-refactor/inventory/commands-a.md:55` ("a marked report is overwritten on re-run (S:66)"). The retry form is `.dev/orca-command-refactor/inventory/orca-capabilities.md:116`, and the Task-level reopen by `--retry-of` is at `orca-capabilities.md:90`. That a retry reuses the Task's brief, so the `--output` path cannot change on retry, is an inference from those lines, not a checked fact (UNVERIFIED). `cmd/init-lite.md:32` and `sk/sc-init-lite-protocol/SKILL.md:66,70` are cited from the inventory and are UNVERIFIED here: the `src/superclaude` and `skills` files are not in this workspace. |
| GR-B2 | Applied | spec:73 (section 2.3) | Gate option 2 was taken: section 2.3 now says Phase 0 runs omit `--unattended`, because the flag is first accepted in P1 (spec:159), and that AC-0.4 (spec:194) checks those runs as they are. The P0 runs are `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --output <dir>` (spec:158). Section 2.3 also now requires `--unattended` only for a command that accepts it in the phase being run. P2 is the phase in which `troubleshoot` first accepts it (spec:160), so this matches spec:160 and not only spec:159. §7.2 step 1 (spec:180) takes its brief from section 2.3 and so reads the same way. |

## Checks made after editing

- `grep -c ''` gives 285 lines, the same as before; no line was added or removed, so the spec:N citations in `gate.md` still point at the same lines.
- The changed texts are the only edits; no other spec line was touched (the before and after diff is limited to spec:64, spec:73 and spec:87).
- Medium findings M-1 to M-12 and notes N-1 to N-4 were not revised, as the brief requires.
- The added text cites its finding id on each addition (GR-B1 at spec:64 and spec:87; GR-B2 at spec:73), as the REVISE prompt requires.

## Coverage and UNVERIFIED items

- Read in full: `review/gate.md`, the spec (285 lines), `README.md`, and the REVISE prompt section of the prompt file. The inventory files under `inventory/` were read at the cited lines only (`commands-a.md:55`, `orca-capabilities.md:90,116`).
- UNVERIFIED here: `cmd/init-lite.md:32`, `sk/sc-init-lite-protocol/SKILL.md:66,70` and the other `src/superclaude`, `~/.claude` and `.dev/...` paths outside this workspace.
- The retry-reuses-brief inference (see GR-B1 row) is UNVERIFIED.
