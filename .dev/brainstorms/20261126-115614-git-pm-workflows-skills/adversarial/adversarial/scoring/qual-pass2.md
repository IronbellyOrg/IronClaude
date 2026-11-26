# Qualitative Scoring, Pass 2 (reverse order: C, B, A)

- Rubric: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` section A.2 (30 binary criteria, Claim-Evidence-Verdict).
- Inputs read in full, in this order: `blind/variant-C.md`, `blind/variant-B.md`, `blind/variant-A.md`, plus the common source `seed-brief.md`.
- Independence: no debate transcript, advocate statement, diff analysis or other file under `debate/` or `scoring/` was read.
- Repository checks (read-only, this worktree, 2026-11-26) were used only to test factual claims. Confirmed: `.claude/commands/sc/git.md` is absent; `commands/sc-git.md` has 79 lines and was last changed by `ff5f73adf`; `git ls-files commands/` lists 21 files; `refs/remotes/origin/HEAD` resolves to `origin/master`; `git.md` has `/sc:git status` (line 59), `commit --smart-commit` (67) and `merge feature-branch --interactive` (75); the launch-level guard has no `submodule` subcommand and denies `UNKNOWN` at every level; the developer guide lists `version-control` and `moderate`; Wave 0 step 5 resolves the ledger path and step 6 opens it.
- Vague-word scan over the three variants (might, should consider, as appropriate, as needed, when applicable, etc., various, appropriate, properly, adequate, useful, where observable, could): Variant C has "when applicable" (line 51), "useful" (line 42) and "where observable" (line 74) in normative text. In A and B, "could" appears only in quoted rationale (A lines 67 and 355, B lines 85 and 463).

Each row reads: criterion id | claim | evidence | verdict.

## Variant C

### Completeness

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| completeness.1 | All explicit source requirements are covered | FR-001 "Deliver a modular `/sc:git`, explicitly authorized local commit boundaries in `/sc:implement`, submodule inspection/update/pointer handling, and discovery of the existing local cleanup route"; FR-008 removes `commands/sc-git.md`; FR-015/FR-016 stage `.dev/tasks/` and never the runtime mirrors; FR-019 Conventional Commit; FR-020 hook refusal reported, never bypassed; FR-014 no commit in a batch; FR-007 push or merge requests stop; FR-009/FR-036 `make verify-sync`; "Decisions for the seed brief's open questions" 1-7 answer all six open questions | MET |
| completeness.2 | Edge cases and failure scenarios are addressed | FR-017 same-file pre-existing edits; FR-018 "An existing index lock, unmerged entries, active merge/rebase, moved HEAD, changed candidate, or another writer causes refusal"; FR-020 hook rewrite, interruption, timeout; FR-022 crash after the commit and before the record; FR-028 partial multi-repository failure | MET |
| completeness.3 | Dependencies and prerequisites are included | FR-009 distribution chain (edit source, mirror into `P`, `make sync-dev`, `make verify-sync`); "Existing integration points are `S/skills/sc-implement-protocol/SKILL.md`, its `refs/ledger.md`, `refs/retry.md`, `refs/managed-workspace.md`"; NFR-006 a missing installed helper blocks only the boundary; NFR-008 no new runtime dependency | MET |
| completeness.4 | Success criteria are defined | "## Acceptance criteria" AC-01 to AC-08, each tied to FRs, e.g. AC-03 "the authorized first commit occurs strictly after the first `complete` and before task two's Q0" | MET |
| completeness.5 | Out-of-scope items are explicit | FR-002 Exclusions "Do not introduce a central command relay, ..., automatic push, merge, PR creation, remote branch deletion, replacement cleanup engine, automatic progress posts..."; Decision 4 "Exclude remote-tip update, module add/remove, URL edits and publication"; Decision 6 "None beyond..." | MET |

### Correctness

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| correctness.1 | No factual errors or hallucinated claims | Spot checks pass: "`D/commands/sc/git.md` ... the file is absent in this checkout" (confirmed absent); legacy copy "contain[s] repeated command prefixes" (confirmed); "`/sc:git status` and `/sc:git commit --smart-commit` surfaces" exist (`git.md:59`, `:67`); "its builder reads plugin sources" (`build_superclaude_plugin.py:16` `PLUGIN_SRC`); "`archive` can write to the evidence repository even without `--apply`" (`worktrees.md:17`); "does not claim ... `implement.md` has an unattended section ... it does not" (argument-hint has no `--unattended`); the cited test files exist. Unchecked items are labelled UNVERIFIED. No error found | MET |
| correctness.2 | Technical approaches are feasible within the stated constraints | FR-006 shared helper enforces repository identity, expected HEAD and paths, while the calling protocol checks authority; FR-015 reuses the existing `git add -- <paths>` and `git commit --only -- <paths>` patterns; FR-022 journal kept outside the ledger grammar; NFR-007 states the trust boundary | MET |
| correctness.3 | Terminology is consistent | "boundary", "grant", "journal", "boundary key" and the closed outcome set `committed`, `already-committed`, `no-change`, `refused`, `failed`, `uncertain` are used identically in FR-021, FR-022, FR-034 and NFR-001; aliases `S`/`P`/`D`/`G` are used consistently | MET |
| correctness.4 | No internal contradictions | None found: the Overview's "No new command-line flag is specified" matches FR-011 "no new flag and no plan field"; FR-016's always-staged evidence matches the risk row "do not quietly narrow the mandatory evidence policy"; FR-011 read-only reconciliation without a grant matches FR-022 "retried only with current-session authority" | MET |
| correctness.5 | Claims are supported by evidence or rationale | FR-003 "Evidence: `docs/developer-guide/branch-protection.md`, `S/core/WORKER-CONTRACT.md`, and `S/core/HOW-WE-WORK.md`"; FR-029 "Evidence: `S/commands/worktrees.md` and `scripts/worktree_cleanup.py`"; each of Decisions 1-7 gives a reason | MET |

### Structure

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| structure.1 | Sections are ordered logically, prerequisites first | Scope, then `/sc:git` structure, then "Authorization model" (FR-010 to FR-012), which comes before both consumers ("Between-task commit behavior", "Submodule operations"), then cleanup, worker contract, NFR, tests, risks, decisions, AC | MET |
| structure.2 | Hierarchy depth is consistent, with no orphaned subsections | Every section is an H2 with bulleted FR/NFR items; there are no H3 headings, so no subsection can be orphaned | MET |
| structure.3 | Concerns are clearly separated between sections | One H2 per concern: structure, authorization, implement boundary, submodules, cleanup reuse, worker/unattended, NFR, tests, risks, decisions, AC | MET |
| structure.4 | Navigation aids are present | Cross-references throughout ("FR-010/011 require a separate current-session grant"; AC-01 "FR-004–009 and FR-036 pass"); the path-notation paragraph | MET |
| structure.5 | Follows the conventions of a requirements specification | Numbered FR/NFR items, risks table, decisions section, acceptance criteria | MET |

### Clarity

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| clarity.1 | Language is unambiguous | Vague qualifiers appear in normative text: FR-025 "including nested inspection when applicable"; FR-021 "retain useful diagnostics"; NFR-007 "must be detected where observable" | NOT MET |
| clarity.2 | Concrete rather than abstract | FR-015 "Stage explicit paths with the existing `git add -- <paths>` pattern"; FR-025 "`git status --porcelain=v2 --ignore-submodules=none`"; FR-021 closed outcome list | MET |
| clarity.3 | Each section has a clear purpose or a one-sentence summary | Each H2 can be summarized in one sentence; several open with a purpose sentence: "Existing integration points are ... Change only that boundary policy"; "The source command currently has no submodule protocol." | MET |
| clarity.4 | Acronyms and domain terms are defined on first use | The path aliases are defined, but core loop and contract terms are used without definition: FR-013 "the next task's Q0 snapshot", FR-034 "Q0-to-complete window", FR-013 "valid scoped user Ruling", FR-032 "WC-9", FR-021 "STOP codes" | NOT MET |
| clarity.5 | Next steps or decision points are clearly identified | "Decisions for the seed brief's open questions" 1-7; AC-01 to AC-08; AC-08 "This specification itself authorizes no implementation, test execution, commit or publication" | MET |

### Risk Coverage

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| risk_coverage.1 | At least 3 risks with a probability and impact assessment | The "Risks and mitigations" table has only the columns Risk and Required mitigation (12 rows); it gives no probability and no impact | NOT MET |
| risk_coverage.2 | A mitigation for each risk | Every row has one, e.g. "Crash after Git writes HEAD produces a duplicate commit / Prepare a stable journal first and reconcile expected parent, boundary key and committed contents" | MET |
| risk_coverage.3 | Failure modes and recovery procedures | FR-020 inspects HEAD and stops before the next Q0; FR-022 durable resume without duplicates; FR-028 "report completed, untouched and failed paths ... Do not reset earlier successes" | MET |
| risk_coverage.4 | External dependencies and their failure scenarios | NFR-003 "Stop rather than hang waiting for unavailable signing credentials or an interactive authentication prompt"; FR-026 "Initialization may fetch from the configured module remote ... reject newly substituted or unapproved remote identities"; NFR-006 missing or mismatched installed helper | MET |
| risk_coverage.5 | A monitoring or validation mechanism for detecting risks | NFR-001 "Verify the committed parent, changed-path set and candidate contents after success; a mismatch is `uncertain`"; NFR-004 local observability; FR-034 fault-injection tests | MET |

### Invariant & Edge Case Coverage

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| invariant_edge_case.1 | Collection boundary conditions | FR-024 "No submodules produces an empty list, not an error"; FR-022 "If nothing changed, record `no-change` and never create an empty commit"; NFR-003 "Bound captured output and disclose truncation" | MET |
| invariant_edge_case.2 | State interactions across component boundaries | FR-013/FR-014 order the ledger `complete` line, HEAD and the next Q0; FR-022 "reconcile a pending journal before selecting the next Q0 and before the existing all-complete short-circuit"; FR-023 journal kept across archive movement | MET |
| invariant_edge_case.3 | Guard-condition gaps | FR-018 refusal on index lock, unmerged entries, merge/rebase, moved HEAD, changed candidate; FR-021 "Reject missing/unknown fields and unsafe paths before staging"; NFR-005 rejects traversal, unsupported encodings and symlink escapes | MET |
| invariant_edge_case.4 | Count divergence (off-by-one, inclusive/exclusive) | FR-034 "Reinvoke twice and assert at most one commit for a boundary key"; FR-022 "duplicate matching commits ... produce `uncertain`"; FR-013 "Apply the same boundary to the last task before final review/archive"; FR-023 the post-commit result "cannot be part of that same commit" | MET |
| invariant_edge_case.5 | Interaction effects when features combine | FR-014 parallel batch combined with commits; FR-016/FR-023 evidence staging, commit and archive; FR-032 attended boundary versus the separate WC-9 worker grant; FR-020 hooks combined with commits | MET |

## Variant B

### Completeness

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| completeness.1 | All explicit source requirements are covered | The four outcomes are covered, but B contradicts the seed constraint "`/sc:git` never pushes, merges or opens PRs": FR-006 keeps `merge <branch> [--interactive]` as the "merge" class; FR-013 "run `git merge <branch>` only after a yes"; §1.3 narrows the exclusion to "merging into a shared or protected branch" | NOT MET |
| completeness.2 | Edge cases and failure scenarios are addressed | FR-020 closed refusal list (`detached`, `in-progress-op`, `index-lock`, `foreign-change`, `head-moved`, `no-snapshot`...); FR-029 death between commit and record (`recovered`); FR-036 dirty and detached submodules | MET |
| completeness.3 | Dependencies and prerequisites are included | FR-019 "standard library only"; NFR-009 "`merge` preview needs git 2.38 or later"; FR-023 helper resolution order; §9.2 the existing tests that must be updated | MET |
| completeness.4 | Success criteria are defined | §13 AC-01 to AC-15, "Each criterion is a command or an observation with a pass condition", e.g. AC-01 "`grep -c '^## Activation' <pkg>/commands/git.md` prints `1`" | MET |
| completeness.5 | Out-of-scope items are explicit | §1.3 "Explicitly out of scope (decided)" table with a reason for each row | MET |

### Correctness

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| correctness.1 | No factual errors or hallucinated claims | Most citations check out (`pyproject.toml:79`, `routing_refresh_cases.json:325`, guard `UNKNOWN` denial, `test_help_text_fixes.py:17/41/92`, 20 remaining legacy files). Two errors: (a) RC-6 says "`git.md` exists in four places: ..., the dev copy, ..." under the header "every repo citation below was read in this checkout", but `.claude/commands/sc/git.md` is absent in this checkout; (b) FR-019/NFR-003 say the helper "writes nothing in the repository" while allowing "`read-tree`/`add`/`write-tree` only under a private `GIT_INDEX_FILE`", and `git add` and `git write-tree` write blob and tree objects into the repository object database whatever index file is used | NOT MET |
| correctness.2 | Technical approaches are feasible within the stated constraints | FR-016 runs the commit as a literal Bash command so the guard sees it; FR-024 Q7b sits after `complete` and before the next Q0, so the HEAD invariants hold; FR-020/FR-021 preflight/verify classification | MET |
| correctness.3 | Terminology is consistent | `Q7b COMMIT`, `commits.md`, `E-COMMIT-REFUSED`, the FR-020 refusal tokens and the FR-021 classification tokens are used identically in FR-030, T-04, T-05 and AC-10 | MET |
| correctness.4 | No internal contradictions | None found: FR-025 "When any member halts, no commit is made for the batch" agrees with the FR-029 resume clause that routes through Q7b; FR-018's undo hint, "printed and never run", agrees with NFR-005 "nothing in this work runs `reset`" | MET |
| correctness.5 | Claims are supported by evidence or rationale | §2 "Each root cause is stated as a falsifiable claim with its evidence"; §11 decisions give "Why" and "Rejected options" | MET |

### Structure

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| structure.1 | Sections are ordered logically, prerequisites first | Path notation, overview, root causes, structure, then authorization with commit mechanics and the helper (§4, §4.1), which come before their dependents §5 (implement step) and §6 (submodules), then cleanup, worker, tests, risks, decisions, NFR, AC | MET |
| structure.2 | Hierarchy depth is consistent, with no orphaned subsections | "## 4. Authorization model" puts FR-011 to FR-018 at H2 level, then has a single "### 4.1 Helper script `commit_plan.py`" with no sibling 4.2: an orphaned subsection | NOT MET |
| structure.3 | Concerns are clearly separated between sections | Separate sections for root causes, structure, authorization, implement step, submodules, cleanup, worker contract, tests, risks, decisions, NFR | MET |
| structure.4 | Navigation aids are present | Alias table; cross-references "(section 11, Q5)", "(FR-029)", "Root cause addressed: RC-2 and RC-3" | MET |
| structure.5 | Follows the conventions of a requirements specification | FR/NFR IDs, test table, risk table with ids, AC list | MET |

### Clarity

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| clarity.1 | Language is unambiguous | The vague-word scan finds no hedging in normative text; "could" appears only in quoted rationale (lines 85, 463) | MET |
| clarity.2 | Concrete rather than abstract | FR-016 exact steps ending in "`git commit --only -F <message-file> -- <paths>`"; FR-028 header regex; FR-020 closed reason list | MET |
| clarity.3 | Each section has a clear purpose or a one-sentence summary | §4, §5 and §6 open with "Root cause addressed: ..."; §2 opens "Each root cause is stated as a falsifiable claim"; §13 opens "Each criterion is a command or an observation with a pass condition" | MET |
| clarity.4 | Acronyms and domain terms are defined on first use | The alias table defines `<name>`, `<pkg>`, `<plugin>`, `<dev>` and `<home>`, and the "(new)" marker is defined; RC-3 explains Q0 ("Q0 pins each task's start tree as `refs/<name>/implement/<slug>/T<id>` and deletes the pin at `complete`"); RC-1 explains S23; RC-2 explains K3 and the launch levels | MET |
| clarity.5 | Next steps or decision points are clearly identified | §11 Q1-Q6 and D-7 decisions; R1 "Recommended follow-up"; AC-01 to AC-15 | MET |

### Risk Coverage

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| risk_coverage.1 | At least 3 risks with a probability and impact assessment | The §10 table has Id, Risk, Root cause, Mitigation and Residual; Residual is a single post-mitigation level (Low/Medium), not a separate probability and impact | NOT MET |
| risk_coverage.2 | A mitigation for each risk | R1 to R13 each have a Mitigation cell | MET |
| risk_coverage.3 | Failure modes and recovery procedures | FR-021 `hook-failed`, `hook-rewrite`, `hook-rewrite-committed`, `recovered`; FR-029 recover mode on resume; FR-030 the task stays `complete` and staged paths stay staged | MET |
| risk_coverage.4 | External dependencies and their failure scenarios | R9 "Plugin-only or partial installs lack the helper"; R11 "Commit-message hook not installed locally"; NFR-009 git floor; FR-034 network fetch from the `.gitmodules` URL; FR-044 launch-level guard levels | MET |
| risk_coverage.5 | A monitoring or validation mechanism for detecting risks | FR-021 `verify` compares against `pre_tree` and "lists dirty tracked paths outside `.dev/` that remain"; T-01 to T-09; AC-08 grep for deletion forms | MET |

### Invariant & Edge Case Coverage

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| invariant_edge_case.1 | Collection boundary conditions | FR-021 `empty` (nothing to commit), recorded while the run continues (FR-030); FR-035 "The commit set is exactly `{<path>}`"; FR-023 preflight "once with no paths" | MET |
| invariant_edge_case.2 | State interactions across component boundaries | FR-024 Q7b keeps HEAD still for retry check 3 and coordinator condition (6); FR-029 pin deletion deferred while the flag is in force; FR-025 the shared `q0-head` across batch members | MET |
| invariant_edge_case.3 | Guard-condition gaps | FR-022 standalone-token rule and the `not-person` refusal; NFR-007 "a missing helper, unparseable helper output, a missing pin or `q0-head`, or an unknown token gives a refusal, never a commit" | MET |
| invariant_edge_case.4 | Count divergence (off-by-one, inclusive/exclusive) | FR-021 "HEAD moved by one commit"; NFR-005 "Each commit point adds at most one commit"; FR-025 "one `Implement-Task:` trailer per member"; AC-09 "exactly two new commits"; AC-04 "`git ls-files commands/ | wc -l` prints `20`" | MET |
| invariant_edge_case.5 | Interaction effects when features combine | FR-044 `--commit-tasks` in guard-launched sessions gives `reason=guard`; FR-037a the status-versus-sweep `--ignore-submodules` trade-off; R12 other packages under `.dev/tasks` entering a task commit | MET |

## Variant A

### Completeness

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| completeness.1 | All explicit source requirements are covered | §1.3 the four in-scope items; FR-004 refuses `merge`, consistent with "never merges" (D7); FR-014 removes `commands/sc-git.md`; FR-016 `make verify-sync`; FR-061 `git add -- .dev/tasks`; FR-064 hook refusal reported, never bypassed; FR-058 no commit inside a batch; FR-009 installed paths; D1-D6 answer each open question | MET |
| completeness.2 | Edge cases and failure scenarios are addressed | FR-054 precondition refusals (`detached-head`, `operation-in-progress`, `index-locked`, `dirty`); FR-058 a halted batch member; FR-064/FR-065 hook rewrite and resume; FR-041 dirty, detached and conflicted submodules | MET |
| completeness.3 | Dependencies and prerequisites are included | §1.5 "Baseline facts (verified in this worktree)" table; NFR-011 git 2.23 or later; NFR-009 `vcs_contract`; FR-015 mirror copy list | MET |
| completeness.4 | Success criteria are defined | §13 AC-01 to AC-15, each with a Check column naming a test | MET |
| completeness.5 | Out-of-scope items are explicit | §1.4 "Explicitly out of scope (decided)": relay, push/fetch/pull/merge/rebase/PR, remote deletion, a second cleanup, level-table change, nested submodules, PM workflows | MET |

### Correctness

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| correctness.1 | No factual errors or hallucinated claims | Spot checks pass: `commands/sc-git.md` has 79 lines and last commit `ff5f73adf` dated 2026-07-22; `origin/HEAD` resolves to `origin/master`; `.gitignore:127-128`; the `vcs` group name is unused in `main.py`; the developer guide lists `version-control`/`moderate`; Wave 0 step 5 (ledger path) and step 6 (open ledger) match FR-054; `archive_workspace.py` raises `E-ARCHIVE-LEDGER`; `commands/sc-README.md` says to edit `plugins/` first and mentions v5.0; the git 2.38.1 `file://` submodule restriction is correct. No error found | MET |
| correctness.2 | Technical approaches are feasible within the stated constraints | Read-only `<cli> vcs` planner plus agent-run argv visible to hooks (NFR-002); ledger `COMMIT:` records changed together with the archive parser (FR-068, FR-069, T-10) | MET |
| correctness.3 | Terminology is consistent | `detached-head`, `protected-branch`, `index-locked`, `E-COMMIT-PRECONDITION`, `E-COMMIT-REFUSED` and the open/pending terms (FR-056) are used identically in FR-032, FR-054, FR-070, T-08 and AC-09 | MET |
| correctness.4 | No internal contradictions | FR-052 "No primitive other than `implement.md`, `sc-implement-protocol` and `HOW-WE-WORK.md` may contain the string `--commit-tasks` ... A static test enforces this" (T-15) contradicts FR-091, which rewrites `WORKER-CONTRACT.md:42` (a core primitive, installed as `<home>/WORKER-CONTRACT.md` per §1.1) to say per-task commits "are delivered as `/sc:implement --commit-tasks`" and that "`--commit-tasks` is refused under `--unattended`" | NOT MET |
| correctness.5 | Claims are supported by evidence or rationale | §1.5 gives an Evidence cell for every baseline fact; D1-D8 each give a "Why:" | MET |

### Structure

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| structure.1 | Sections are ordered logically, prerequisites first | Shared prerequisites come after the sections that depend on them: "## 6. Commit rules shared by `/sc:git commit` and the implement step" (FR-030 to FR-034) follows §2 to §5, which already depend on it (FR-004 cites FR-030; the §3 table cites FR-031, FR-032, FR-034; FR-043 cites FR-032). FR numbering runs FR-050..072, then FR-040..043, then FR-030..034 | NOT MET |
| structure.2 | Hierarchy depth is consistent, with no orphaned subsections | H2 sections with H3 children 1.1-1.5, 2.1-2.5, 4.1-4.7; the other H2s have no children; no lone subsection | MET |
| structure.3 | Concerns are clearly separated between sections | Separate sections for structure, authorization, implement step, submodules, shared rules, cleanup, worker contract, tests, NFR, risks, decisions, AC | MET |
| structure.4 | Navigation aids are present | §1.1 notation table; cross-references "Decision D6 explains why", "See decision D5", "holds §4.3-§4.6" | MET |
| structure.5 | Follows the conventions of a requirements specification | FR/NFR IDs, test table, risk table, AC table | MET |

### Clarity

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| clarity.1 | Language is unambiguous | The vague-word scan finds no hedging in normative text; "could" appears only in rationale (lines 67, 355) | MET |
| clarity.2 | Concrete rather than abstract | FR-061 numbered steps with exact argv shapes; FR-010 named JSON fields; NFR-007 "at most 64 KiB ... at most 200 entries ... at most 40 lines" | MET |
| clarity.3 | Each section has a clear purpose or a one-sentence summary | §2 opens "The design has three layers..."; §3 opens "The person's own typed line is the only thing that authorizes a write." | MET |
| clarity.4 | Acronyms and domain terms are defined on first use | §1.1 defines the path placeholders and FR-056 defines open/pending, but loop and phase terms are used without definition: FR-057 "after Q7 has flushed a `complete` line and before Q8 starts the next task's Q0"; FR-092 "the P4 conversion" and "(WC-4)" | NOT MET |
| clarity.5 | Next steps or decision points are clearly identified | §12 decisions D1-D8; AC table with a Check column | MET |

### Risk Coverage

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| risk_coverage.1 | At least 3 risks with a probability and impact assessment | The §11 table has #, Risk, Mitigation and Residual; Residual is narrative text, with no probability and no impact | NOT MET |
| risk_coverage.2 | A mitigation for each risk | Each of the 14 rows has a Mitigation cell | MET |
| risk_coverage.3 | Failure modes and recovery procedures | FR-064 refusal classification plus a 40-line log; FR-065 "On a resume after `E-COMMIT-REFUSED`, R0 plans again from the current tree" | MET |
| risk_coverage.4 | External dependencies and their failure scenarios | NFR-009 helper and skill version coupling (`helper-missing`); Risk 8 an automated sync re-creating `commands/sc-git.md`; T-07 "Git 2.38.1 and later blocks `file://` submodules ... (UNVERIFIED on the CI image)"; FR-093 launch-level guard | MET |
| risk_coverage.5 | A monitoring or validation mechanism for detecting risks | T-10 ledger parity test; T-13 `rules.py` versus prose parity; NFR-009 `vcs_contract` check; FR-071 a summary line per `COMMIT: sha=` record | MET |

### Invariant & Edge Case Coverage

| Id | Claim | Evidence | Verdict |
|---|---|---|---|
| invariant_edge_case.1 | Collection boundary conditions | FR-010 `dirty` "capped at 200, with `truncated`"; FR-060 the `nothing` result; FR-058 batch of up to 3 members; FR-040 `nested-not-inspected` | MET |
| invariant_edge_case.2 | State interactions across component boundaries | FR-056 to FR-059 the open/pending sets keep HEAD equal to `q0-head` for retry check 3 and Ruling condition (6); FR-068/FR-069 ledger grammar together with the archive helper | MET |
| invariant_edge_case.3 | Guard-condition gaps | FR-004 STOP on a missing name, both or neither message flag, an unknown operation, or being outside a work tree; FR-011 the runner raises on any non-allowed argv | MET |
| invariant_edge_case.4 | Count divergence (off-by-one, inclusive/exclusive) | FR-056 pending "(b) that line comes after the first `COMMIT: on` line"; T-01 "tasks completed before `COMMIT: on` are excluded"; FR-055 "written once per ledger"; FR-021 "One authorizing line authorizes one operation" | MET |
| invariant_edge_case.5 | Interaction effects when features combine | FR-067 a Ruling combined with the commit step; FR-093 guard levels combined with the commit step; D8 the managed package versus all of `.dev/tasks`; Risk 7 | MET |

## Verdict table

| Variant | Criterion | Verdict |
|---|---|---|
| A | completeness.1 | MET |
| A | completeness.2 | MET |
| A | completeness.3 | MET |
| A | completeness.4 | MET |
| A | completeness.5 | MET |
| A | correctness.1 | MET |
| A | correctness.2 | MET |
| A | correctness.3 | MET |
| A | correctness.4 | NOT MET |
| A | correctness.5 | MET |
| A | structure.1 | NOT MET |
| A | structure.2 | MET |
| A | structure.3 | MET |
| A | structure.4 | MET |
| A | structure.5 | MET |
| A | clarity.1 | MET |
| A | clarity.2 | MET |
| A | clarity.3 | MET |
| A | clarity.4 | NOT MET |
| A | clarity.5 | MET |
| A | risk_coverage.1 | NOT MET |
| A | risk_coverage.2 | MET |
| A | risk_coverage.3 | MET |
| A | risk_coverage.4 | MET |
| A | risk_coverage.5 | MET |
| A | invariant_edge_case.1 | MET |
| A | invariant_edge_case.2 | MET |
| A | invariant_edge_case.3 | MET |
| A | invariant_edge_case.4 | MET |
| A | invariant_edge_case.5 | MET |
| B | completeness.1 | NOT MET |
| B | completeness.2 | MET |
| B | completeness.3 | MET |
| B | completeness.4 | MET |
| B | completeness.5 | MET |
| B | correctness.1 | NOT MET |
| B | correctness.2 | MET |
| B | correctness.3 | MET |
| B | correctness.4 | MET |
| B | correctness.5 | MET |
| B | structure.1 | MET |
| B | structure.2 | NOT MET |
| B | structure.3 | MET |
| B | structure.4 | MET |
| B | structure.5 | MET |
| B | clarity.1 | MET |
| B | clarity.2 | MET |
| B | clarity.3 | MET |
| B | clarity.4 | MET |
| B | clarity.5 | MET |
| B | risk_coverage.1 | NOT MET |
| B | risk_coverage.2 | MET |
| B | risk_coverage.3 | MET |
| B | risk_coverage.4 | MET |
| B | risk_coverage.5 | MET |
| B | invariant_edge_case.1 | MET |
| B | invariant_edge_case.2 | MET |
| B | invariant_edge_case.3 | MET |
| B | invariant_edge_case.4 | MET |
| B | invariant_edge_case.5 | MET |
| C | completeness.1 | MET |
| C | completeness.2 | MET |
| C | completeness.3 | MET |
| C | completeness.4 | MET |
| C | completeness.5 | MET |
| C | correctness.1 | MET |
| C | correctness.2 | MET |
| C | correctness.3 | MET |
| C | correctness.4 | MET |
| C | correctness.5 | MET |
| C | structure.1 | MET |
| C | structure.2 | MET |
| C | structure.3 | MET |
| C | structure.4 | MET |
| C | structure.5 | MET |
| C | clarity.1 | NOT MET |
| C | clarity.2 | MET |
| C | clarity.3 | MET |
| C | clarity.4 | NOT MET |
| C | clarity.5 | MET |
| C | risk_coverage.1 | NOT MET |
| C | risk_coverage.2 | MET |
| C | risk_coverage.3 | MET |
| C | risk_coverage.4 | MET |
| C | risk_coverage.5 | MET |
| C | invariant_edge_case.1 | MET |
| C | invariant_edge_case.2 | MET |
| C | invariant_edge_case.3 | MET |
| C | invariant_edge_case.4 | MET |
| C | invariant_edge_case.5 | MET |

## Dimension subtotals

| Variant | completeness | correctness | structure | clarity | risk_coverage | invariant_edge_case | Total (of 30) |
|---|---|---|---|---|---|---|---|
| A | 5 | 4 | 4 | 4 | 4 | 5 | 26 |
| B | 4 | 4 | 4 | 5 | 4 | 5 | 26 |
| C | 5 | 5 | 5 | 3 | 4 | 5 | 27 |

## Totals

- Variant A: 26/30 criteria met (qual_score 0.867)
- Variant B: 26/30 criteria met (qual_score 0.867)
- Variant C: 27/30 criteria met (qual_score 0.900)

Edge case floor: every variant scores 5/5 on Invariant & Edge Case Coverage, so all three are eligible as base.
