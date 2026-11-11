# S1 ANALYSIS: incident I1, the Orca worker-contract spec review loop

Produced by `/sc:analyze` (invoked through the Skill tool, skill `sc:analyze`) with the brief: "Review the past incident I1 (evidence listed in phase1/REPORT.md) and recreate the scenario as exactly as possible, with the original run as the baseline. Output a replay package that lets a fresh session re-run the scenario with the same starting document and the same instructions."
Analyst worker: task_812ec12b874e. Date of analysis: 2026-11-08. Static analysis only: no review loop, no `/sc:spec-panel`, no reviewer was run.

## 0. Pointer keys

| Key | Meaning |
|---|---|
| `PJ` | `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs` (one Orca worker per jsonl; line numbers are 1-based jsonl lines) |
| `CO` | coordinator session `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/f4dc0c4a-5b2d-498b-b835-2f310c79d211.jsonl` |
| `FH` | `/home/coder/.claude/file-history` (read-only; copies are in `inputs/`) |
| `BO` | `phase2/S1/baseline-outputs/` (copies of the original reports; original path `.dev/orca-command-refactor/review/`) |
| `B` | `phase2/S1/briefs/` (verbatim briefs, one file per task) |
| `P1` | `phase1/REPORT.md` of the logs team (section I1) |

"Read" below means taken from a file or log line; "re-derived" means computed or classified by this analysis.

## 1. What the incident is (summary)

A 17-task Orca run on 2026-11-02 (03:26Z to 23:03Z; model `claude-opus-5-5`, Claude Code `2.1.316`, branch `ironbelly/OrcaCLICommandRefactor-Specs`, jsonl field `gitBranch`/`version`/`model` in `PJ/1b14f80b...jsonl` L5 and its assistant lines) wrote a planning spec (Task 4), then alternated independent review workers and reviser workers.

- Rounds 1 to 3 (Tasks 5 to 10) are the non-converging loop: three reviews, all FAIL, 24 then 13 then 14 new findings, spec 57,763 to 82,643 to 92,194 bytes.
- The coordinator stopped the loop after round 3 and switched to a constrained process (Tasks 10 to 17); the first and only PASS came at Task 17, which reviewed one changed line.

## 2. Round by round

### 2.0 Setup (Tasks 1 to 4)
| Task | Role | Session | Brief | Output | worker_done |
|---|---|---|---|---|---|
| 1 | inventory A | `9f0fb721` | `B/T01-...-L10-9f0fb721.md` | `inventory/commands-a.md` (Write `PJ/9f0fb721...` L56) | n/a |
| 2 | inventory B | `a1c4ed4e` | `B/T02-...-L10-a1c4ed4e.md` | `inventory/commands-b.md` (Write L65) | n/a |
| 3 | Orca facts | `f7191a1f` | `B/T03-...-L10-f7191a1f.md` | `inventory/orca-capabilities.md` (Write L69) | n/a |
| 4 | **writer** | `1b14f80b` | `B/T04-R0-writer-L10-1b14f80b.md` | spec v1 (Write+Edits `PJ/1b14f80b...` L95-629) | L652 |

Task 4 read the README and all three inventories in full (`PJ/1b14f80b...` L54-L83). The bytes it read are identical to the tracked files in this repo (sha256 compared, see `inputs/SOURCES.md`). No Write/Edit touched README or inventories after 03:43Z in any session of the project (scan of every jsonl in `PJ`, empty result).

### 2.1 Round 1
| Step | Task / session | Brief | Reviewer tool and flags | Severity rule in force | Result |
|---|---|---|---|---|---|
| Review | 5, `699ae853` | `B/T05-R1-reviewer-L11-699ae853.md` (TASK body: `B/task-text/T05-...txt`) | **`Skill` call `sc:spec-panel`, args `@.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`** (`PJ/699ae853...` L56; the loaded command body is the pre-427 text, 0 hits for "Review Loop", only a trailing `ARGUMENTS:` line differs from `ec1babd9`) | The brief asks for "numbered findings list (finding, severity, spec section, evidence path:line) and a PASS or FAIL verdict"; **it states no pass bar**. The reviewer applied a binary any-severity rule and says it comes from "the run's quality rules" (`BO/spec-panel.md:189`). The phrase does not occur in the brief or in any earlier line of the R1 log (first occurrence is the reviewer's own output at `PJ/699ae853...` L255). Source of the rule: UNVERIFIED (probably the worker's global instructions, which the jsonl does not hold). Severity scale used: CRITICAL/MAJOR/MINOR (`BO/spec-panel.md:114`) | FAIL, 24 findings: 3 CRITICAL, 15 MAJOR, 6 MINOR (`BO/spec-panel.md:7-12`; table `:113-141`) |
| Revise | 6, `3bb70411` | `B/T06-R1-reviser-L10-3bb70411.md` | none (reviser) | none stated; "verify each numbered finding ... apply confirmed findings ... one row per finding: applied or rejected" | 24 of 24 applied, none rejected (`PJ/3bb70411...` L738 body; `BO/disposition.md`, 24 rows). Spec 57,763 to 82,643 bytes (+43.1%) |

The R1 reviewer ran two read-only experiments (regex checks) and read-only `--help` calls to prove findings 6 and 7 (`BO/spec-panel.md:184-193`, Decisions table).

### 2.2 Round 2
| Step | Task / session | Brief | Reviewer tool and flags | Severity rule in force | Result |
|---|---|---|---|---|---|
| Review | 7, `aff19d65` | `B/T07-R2-reviewer-L11-aff19d65.md` | The brief says "run /sc:spec-panel @... --mode critique --focus requirements,architecture" (same flags as R1). **No `Skill` call exists in this session**: the reviewer `Read` `~/.claude/commands/sc/spec-panel.md` (`PJ/aff19d65...` L39) and applied the panel by hand, saying "the command names no skill, so it runs from its own file" (`BO/spec-panel-round2.md:16`). It also checked the 24 R1 resolutions and every changed citation. | **Binary: "any finding of any severity is FAIL"** (brief; echoed `BO/spec-panel-round2.md:276`) | FAIL, 13 new findings (1 CRITICAL, 9 MAJOR, 3 MINOR) plus 2 overstated citations that are N6 and N13 (`BO/spec-panel-round2.md:7-9`, table `:249-264`) |
| Revise | 8, `66468bab` | `B/T08-R2-reviser-L10-66468bab.md` | none | none; adds "do not reopen settled round-1 fixes unless a finding requires it" | 15 of 15 applied (`PJ/66468bab...` L552; `BO/disposition-round2.md`). Spec 82,643 to 92,194 bytes (+11.6%) |

### 2.3 Round 3
| Step | Task / session | Brief | Reviewer tool and flags | Severity rule in force | Result |
|---|---|---|---|---|---|
| Review | 9, `1c9a7ec8` | `B/T09-R3-reviewer-L11-1c9a7ec8.md` | Same as round 2: brief says run `/sc:spec-panel` with the same flags; **no `Skill` call**; reviewer `Read` the command file (`PJ/1c9a7ec8...` L142; `BO/spec-panel-round3.md:17`) | Binary: any finding of any severity is FAIL (`BO/spec-panel-round3.md:273`) | FAIL, 14 new findings (0 CRITICAL, 8 MAJOR, 6 MINOR) (`BO/spec-panel-round3.md:6-8`, `:244-260`) |
| Revise | 10, `458bdc00` | `B/T10-R3-reviser-L10-458bdc00.md` | none | none; guardrails: add no rule/flag/field/check unless a finding names it missing, end strictly smaller than 92,194 bytes, three coordinator-chosen simplifications S1 to S3 | M1 to M14 plus S1 to S3 dispositioned (`BO/disposition-round3.md`; `PJ/458bdc00...` L634 body: S1-S3 applied; 9 of M1-M14 applied with one-clause edits, M1 only in part; M5, M6, M7, M8, M11 superseded by S1-S3). The reviser's own fresh-context diff check of its result returned FAIL with 8 defects, all fixed in place and not re-verified (same L634 body). Spec 92,194 to 89,089 bytes (-3.4%), 405 lines |

### 2.4 How the loop ended, and why
- After round 3 the coordinator wrote: "The review loop is not converging ... each round finds about as many new problems as it fixes. The spec grew from 58 KB to 92 KB, and the reviewer traced most of the new findings to text the previous revision added ... The pass bar is strict: any finding of any severity fails the review" (`CO` L3303, 2026-11-02T14:13:47Z).
- After the owner asked to evaluate a revert (`CO` L3319), the coordinator chose a targeted rollback plus one constrained round with a stop rule ("if that review still fails, stop running rounds; you decide D1-D5") (`CO` L3356, 14:17:32Z). The owner approved (`CO` L3372, 14:35:15Z); Task 10 started 14:36Z.
- The stop was a human/coordinator decision, not a mechanical cap. No rule in the original framework capped the loop at 3 (the cap that PR 427 writes into `/sc:spec-panel` did not yet exist).

### 2.5 Constrained stage (Tasks 11 to 17), supplemental baseline
Reviewers here were told NOT to run `/sc:spec-panel` (Tasks 11, 13, 15, 17 briefs: "do NOT run /sc:spec-panel" / "do not run /sc:spec-panel"). PR 427 cannot affect these.

| Task | Session | Brief | Tool | Severity rule | Result |
|---|---|---|---|---|---|
| 11 diff-only review | `d534b6de` | `B/T11-...-L10-d534b6de.md` | diff review, no panel | binary any severity | FAIL, 7 findings: 3 MAJOR, 4 MINOR (`BO/final-diff-review.md:108-109`); spec 89,089 B |
| 12 combined revision | `eadb62ac` | `B/T12-...` | none | review rule "findings are blocking or minor; only blocking fail (PR #343)" | spec 89,089 to 115,819 B (owner decisions D1-D5 etc. added; `PJ/eadb62ac...` L1064) |
| 13 review | `02c0d4b8` | `B/T13-...` | changed-line review | blocking/minor (PR #343) | FAIL: 2 blocking (B1, B2), 11 minor (`BO/round4-review.md:94-133`) |
| 14 fix 1 | `99f9f18e` | `B/T14-...` | none | PR #343 | spec 116,538 B |
| 15 recheck | `4799e7cc` | `B/T15-...` | changed-line recheck | PR #343 | FAIL: 1 blocking (N1) (`BO/round4-review.md:198`) |
| 16 fix 2 | `0d628073` | `B/T16-...` | none | PR #343 | spec 116,815 B |
| 17 final recheck | `b510a293` | `B/T17-...` | one-line recheck | PR #343 | **PASS (with notes)** (`BO/round4-review.md:247`) |

## 3. Findings of this analysis (severity-rated)

| # | Severity for the replay | Finding | Evidence |
|---|---|---|---|
| F1 | HIGH | **Only the R1 review used `/sc:spec-panel` through the Skill tool.** R2 and R3 reviewers read the command file and followed it by hand; Tasks 11 to 17 did not use it at all. PR 427 can only act in 3 of the 7 reviews, and in R2/R3 only if the worker reads the 427 text. | `PJ/699ae853...` L56; `PJ/aff19d65...` L39; `PJ/1c9a7ec8...` L142; Skill/Agent scan of all 7 review sessions returned one hit |
| F2 | HIGH | **The briefs for R2, R3 and the reviser rounds embed outcomes of the original run** (counts "24 round-1 findings", ids "N1-N13", "M1-M14", file names, the byte count 92,194, and in Task 10 three simplifications S1 to S3 chosen by the coordinator after reading R3). A fresh run that finds a different set of findings cannot reuse them literally. | `B/task-text/T07`, `T08`, `T09`, `T10` |
| F3 | HIGH | **Repo evidence drifts a lot between the original base and 95f2c6e4.** The original ran on `2cb683f5` (branch created from it 2026-10-30; fast-forwarded to `c118b5a5` only at 15:25:37Z on 11-02, after Task 11). Between `2cb683f5` and `95f2c6e4`: 25 of 45 command files changed; 19 of the 37 `cmd/*.md` files named in spec v1 changed; files mentioning "orca" under commands/skills/core/agents (excluding ccsession-tag) went 0 to 6; `src/superclaude/core/WORKER-CONTRACT.md` now exists. The spec's own evidence line E5 ("no command, skill, agent or core file calls Orca today", v1 line 25) is false at 95f2c6e4. Reviewers check `path:line` citations against live files, so a naive re-run at 95f2c6e4 produces citation findings that have nothing to do with loop convergence. | `git reflog show ironbelly/OrcaCLICommandRefactor-Specs` (entries `2cb683f5 @{2026-10-30 15:35:15}`, `c118b5a5 @{2026-11-02 15:25:37}`); `git grep` counts; `inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:25` |
| F4 | MEDIUM | R1's pass bar ("any finding of any severity is FAIL") was not in the brief; its source is unlogged. | `PJ/699ae853...` L255 (first occurrence), `BO/spec-panel.md:189` |
| F5 | MEDIUM | PR 427's rules and the original briefs conflict: 427 bullet 7 says a brief "may not grade a minor finding as blocking"; the R2/R3 briefs say any severity fails. With verbatim briefs and 427 loaded, the grading changes. This is the effect under test, but it also means the treatment arm is not "the same instructions" in effect. | `inputs/tool-text/spec-panel-427.diff` (bullets 2, 3, 7); `B/task-text/T07`, `T09` |
| F6 | MEDIUM | 427's main lever (diff-scoped `--re-review <prior-findings-file> --baseline <saved-copy>`) is never passed by the original briefs, and without both flags "the run is a first review of the full document". Under verbatim briefs 427 acts only through grading, verdict-line, `review: N of 3` header and cap text. | `inputs/tool-text/spec-panel-427.diff` (bullets 1, 4, 5) |
| F7 | MEDIUM | The installed `~/.claude/commands/sc/spec-panel.md` on this machine is the pre-427 text (identical to `ec1babd9` and `2cb683f5`). R2/R3-style reviewers read that path. A replay that only runs `make sync-dev` puts 427 in the project `.claude/` copy, which an R2/R3-style reviewer reading `~/.claude/...` would NOT load. | `cmp` of `inputs/tool-text/spec-panel-pre427-ec1babd9.md` with `~/.claude/commands/sc/spec-panel.md` (identical); `PJ/aff19d65...` L39 |
| F8 | LOW | Commit `2327fbd3` (P2, after 427) adds an `--unattended` section to `spec-panel.md` (472 to 486 lines). It applies only when `--unattended` is passed, which no original brief does; it is a text difference only. | `git diff 95f2c6e4 2327fbd3 -- src/superclaude/commands/spec-panel.md` |
| F9 | LOW | Live Orca CLI output (build `1.4.237-aidev02.0e4491a95e92`) that reviewers cited cannot be frozen; the capabilities inventory quotes it. | `BO/spec-panel-round3.md:19` (method note), `inputs/.../orca-capabilities.md` |
| F10 | INFO | Every shared input and every spec snapshot v1 to v6 is byte-recoverable and verified. | `inputs/SOURCES.md` |

## 4. Does PR 427 apply to this scenario?

Yes, partly. The original review step is `/sc:spec-panel` in R1 (Skill call) and R2/R3 (command file read and followed). PR 427 (`95f2c6e4`) changes only that command (plus `plugins/` mirror, the routing guide and two release guides): `src/superclaude/commands/spec-panel.md` 462 to 472 lines, new `## Review Loop` section with 7 rules and a new `--re-review ... --baseline ...` usage form. Reach:

- Acts on: R1, R2, R3 reviews (3 of 7 reviews).
- Cannot act on: the writer (Task 4), the revisers (Tasks 6, 8, 10; 427 bullet 6 only governs a reviser that reads a 427 report's "Reviser brief", which the pre-427 reports lack), and Tasks 11 to 17 (briefs forbid the panel).
- With verbatim original briefs 427 acts only through rules 2 (grading), 3 (last line `verdict: PASS|FAIL`), 4 (`review: N of 3` header, cap of 3 reviews/2 fix cycles) and 7 (briefs may not widen scope or grade minor as blocking). The diff-scoped re-review (rules 1, 5) needs the flags the briefs do not pass (see F6). The 427-flag variant is therefore a separate labelled arm (REPLAY.md, Arm B).

## 5. Recommendations (actionable)

1. Replay the core loop only (Tasks 5 to 9: three reviews, two revisions); the cap of 3 reviews coincides with 427's own cap. Run Task 10 and later only as an optional extension.
2. Pin the evidence tree to `2cb683f5` and overlay only the 427 diff on `spec-panel.md` (Arm T-pinned), in addition to or instead of the literal D4 worktree on `95f2c6e4+` (Arm T-literal). The overlay is verified: applying `inputs/tool-text/spec-panel-427.diff` onto the `2cb683f5` file reproduces the `95f2c6e4` file byte for byte. Needs a coordinator decision because D4 says "master at or after 95f2c6e4".
3. Make "427 text was loaded" an explicit validity check on every review (report ends with `verdict: PASS|FAIL`, header `review: N of 3`); discard the arm if absent (F7).
4. Use CRITICAL+MAJOR as the common "blocking-grade" proxy for both arms, since the original rounds used a binary rule and 427 uses its own (see `baseline-metrics.json`, `proxy_definition`).

## 6. Decisions

| Decision | Options | Rationale |
|---|---|---|
| Treat Tasks 5 to 9 as the replay core | whole 17-task run; core only | the non-convergence is in rounds 1 to 3; Tasks 11 to 17 do not use the panel |
| Copy shared inputs from the tracked tree, not from `~/.claude` | file-history only; git tree | no file-history copy exists for the final shared inputs; the tracked files are byte-identical to what Task 4 read (sha256 equal for all four) |
| Take the starting document from `FH/3bb70411.../2d815cfd5e9a74d2@v1` | git `spec-v1-draft.md`; file-history | both are identical (cmp); the file-history one is the original location |
| Classify R3 origins from the reviewer's `Origin:` tags | independent re-derivation of each cause | the tags are the reviewer's own text; I only grouped them (strict: names a specific earlier fix; partial; pre-existing) |

## 7. UNVERIFIED items

- Source of R1's binary pass bar (F4).
- Whether a 427-loaded worker applies rules 2 and 3 when `--re-review` is absent (the section's bullet 1 only defines the no-flag case as "a first review of the full document"; bullets 2 and 3 read as general).
- The exact working-tree state of the original worktree (untracked files besides `.dev/orca-command-refactor/`). R3 reports a `git status --porcelain=v1 -uall --ignored` listing with only `.dev` untracked and ignored caches (`BO/spec-panel-round3.md:21`), which is consistent with a clean tree at `2cb683f5`.
- The Orca CLI version on the replay machine (not checked; not required for the analysis).
- Per-finding re-derivation of R2's "all 13 introduced or exposed by the revision" (taken from the reviewer, `BO/spec-panel-round2.md:250`).
