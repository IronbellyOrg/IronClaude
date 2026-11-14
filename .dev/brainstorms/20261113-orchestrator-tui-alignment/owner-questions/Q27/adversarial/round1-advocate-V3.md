# Round 1 advocate statement: Variant 3 (Proposal C, commit SW-02's plan package in PR #539)

Persona: qa (edge cases, failure scenarios, risk). Depth quick, Round 1 only. All files read 2026-11-14.

## Position summary

Variant 3 is the only proposal whose steps actually run as written: `/sc:implement` refuses a managed plan that lives in a different checkout from the one it runs in, so Variant 1 (the spec's default) fails at its step 2, and Variant 2 reaches level-4 machinery the routing rules forbid without a stated need. Variant 3 keeps plan, ledger and fix in one checkout, needs no Q26 answer, and adds one small package to a PR that already carries 921 `.dev/tasks/to-do/` files. Its real costs are a few untracked reflect files outside the package and the need to keep the exception narrow.

## Steelman of Variant 1

Strongest version: PR #539 is already huge (1003 files) and its review surface should only grow by the fix and its tests, which is what rule A-004 intends ("forbids a new program, collector, JSON key, sidecar or report file, and every program artifact of this alignment work", `merged-requirements.md:978`, rule 5). Rule 3 says program records belong in the coordinator home, and a plan is a record of the program's work. Variant 1 is also the spec's own default for Q27 (`merged-requirements.md:554`), so it costs the owner nothing to accept. What it genuinely gets right: it keeps the #539 diff minimal, it honestly flags the cross-checkout archive question as UNVERIFIED (variant-1 "What it costs or risks"), and it notices the Q26 dependency.

## Steelman of Variant 2

Strongest version: the project rule "When an adequate approved plan already exists, use its existing executor directly; do not rebuild it" (`~/.claude/CLAUDE.md:88`) prefers extending an existing plan to writing a new one, and the sweep task package is the plan that built the code SW-02 changes. Appending a phase keeps the whole Phase 1 history in one place, adds no new `.dev/tasks/` package (so A-004's "no new artifact" holds in letter), and gives the security-sensitive INV-008 fix per-phase reviewer panels. What it genuinely gets right: it takes the spec's first instruction seriously ("first check whether an adequate existing plan covers SW-02", `merged-requirements.md:191` criterion (5)), and it is candid that the existing package "does not plan SW-02 today" and that reopening a Done task muddies its record.

## Key strengths claimed

1. **Variant 3 is executable; Variant 1 is not.** `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:11`: a managed plan must resolve to `<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` "where `<checkout>` is the current git top-level. A copied plan or a plan from another checkout fails here", with STOP `E-MANAGED-INVALID` (`:7`). `/sc:workflow` always writes a managed package in the checkout it runs in (`sc-workflow-protocol/SKILL.md:47`, `:105`). So Variant 3's "run `/sc:workflow` and `/sc:implement` in the #539 checkout" satisfies this; Variant 1's "`/sc:implement <absolute path to that plan>` from the #539 checkout" stops before any task runs. This turns question.md fact 8 and diff U-004 from UNVERIFIED into a verified failure.
2. **One checkout holds all state.** The ledger is always `<pkg>/progress.md` and delegate output lives under `<pkg>/artifacts/` (`managed-workspace.md:31`, `:33`); the archive helper runs with `--root "<checkout>"` (`:54`). With plan and code in the same checkout, every state change (ledger lines, retry artifacts, the `done/` move) happens where the fix is, which is exactly assumption A-002.
3. **No dependency on Q26.** If Q26 is left at its default, "no program file is written on any branch" (`merged-requirements.md:553`), so Variant 1 has nowhere to write the plan and SW-02 stalls. Variant 3 needs only the #539 checkout, which SW-02 already uses ("this checkout, branch `ironbelly/issue-339-orchestrator-mode`", `merged-requirements.md:191`).
4. **It resolves the staging conflict the probe found instead of routing around it.** Probe INV-012 (`invariant-probe.md:20`): the always-staged rule stages the plan in the #539 checkout while a named-files-only commit "must leave untracked, breaking one rule or the other". Rule 15 already names the escape hatch: "the only `.dev/tasks/` package allowed there is SW-02's own, under Q27" (`merged-requirements.md:988`). Variant 3 is that hatch used. In the gitStatus snapshot at the start of this session, no untracked path sits under `.dev/tasks/` in this checkout, so `git add .dev/tasks` there would pick up only SW-02's package (snapshot, not re-checked live).
5. **Correct routing level.** `~/.claude/CLAUDE.md:84` requires a written plan, "normally level 3, not automatic level 4"; `:86` says file count, risk and auditability "never select level 4". Variant 3 is level 3.
6. **Measured precedent and the plain reading of A-004.** A plan package is none of "program, collector, JSON key, sidecar or report file"; PR #539 already carries 921 `.dev/tasks/to-do/` files (question.md fact 5, measured 2026-11-14 with a GET). The spec's own recommended answer to Q27 is "Yes" for this reason (`merged-requirements.md:554`).
7. **Reviewability.** A reader of the merged security fix finds its plan, per-task QA verdicts and final review in the same PR history.

## Weaknesses identified in Variant 1

1. **Step 2 fails mechanically.** See strength 1: `managed-workspace.md:11` rejects a plan from another checkout. The only way to make Variant 1 work is to run `/sc:implement` in the coordinator home, which puts the code change in the wrong checkout and on the wrong branch, contradicting SW-02's location column.
2. **Its "two checkouts are coupled" risk is understated.** It is not just a shared folder: it needs a session in the coordinator home to run `/sc:workflow` (diff A-001). Either the coordinator plans another session's item, or the #539 author opens a second session in a folder the coordinator already occupies; neither is described or authorized.
3. **Hard stall on Q26's default** (`merged-requirements.md:553`). The spec's default for Q27 depends on a non-default answer to Q26, so the two defaults together leave SW-02 with no legal plan location, and SW-02 cannot proceed without a plan under the hard limit (`~/.claude/CLAUDE.md:84`).
4. **Commit uncertainty.** Variant 1 itself says the plan is committed "only when the owner asks, on the coordinator's branch"; a security fix could merge with its plan never committed anywhere.

## Weaknesses identified in Variant 2

1. **Level 4 without a stated need.** `~/.claude/CLAUDE.md:86`: "A twelve-file feature across several sessions still uses level 3 without a concrete MDTM machinery need." Variant 2 names "per-phase reviewer panels" as a benefit but not as a need the owner has stated.
2. **The "existing executor" rule does not apply.** `~/.claude/CLAUDE.md:88` covers "an adequate approved plan". The sweep package does not plan SW-02 (question.md fact 6; Variant 2 concedes it). Appending a phase is writing a new plan inside an old file, so its earlier pre-execution review no longer covers the content being executed.
3. **Reopening a Done task corrupts a record.** The package frontmatter reads `status: "🟢 Done"` (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:7`, read 2026-11-14). Flipping it to Doing on a PR under review makes the shipped Phase 1 look unfinished; it is also an edit to an already-reviewed file in #539, which widens the diff reviewers must reread.
4. **Unknown gate behavior.** Whether `/task`'s gates accept a phase appended after Done is unresolved (Variant 2's own last section). Failure here is discovered only mid-execution on a security fix.
5. **Larger diff, not smaller.** The package already has 764 files in #539; per-phase reviewer outputs add more than a new plan package's few files.

## Concessions

1. Variant 3 understates what the plan run writes outside the package. `/sc:workflow` runs `/sc:reflect --mode pre` as its final step (`sc-workflow-protocol/SKILL.md:89`); reflect's default output is `.dev/reflect/<mode>-<slug>-<timestamp>/` (`sc-reflect-protocol/SKILL.md:88`) and it writes the tracked file `docs/memory/reflect/deviation-patterns-{slug}.md` (`:593`). Neither path is gitignored (`.gitignore` has no `reflect` entry). In the #539 checkout these land as untracked files outside `.dev/tasks/`. Rule 15 says "no program artifact is created there" (`merged-requirements.md:988`). Whether a plan's own advisory reflect report counts as a program artifact is a judgment the owner should make; Variant 3 should say they stay untracked and are never committed under named-paths staging. Its line "those are committed too" applies only to files inside the package.
2. The archive move to `done/` (`managed-workspace.md:36`) adds a rename in #539 if the package was committed in `to-do/` first; the named-paths commit must list both the old and new paths.
3. `/sc:implement` creates local git refs `refs/superclaude/implement/<slug>/T<id>` (`managed-workspace.md:32`) in the #539 clone. They are local and are not pushed by a named-branch push, but they are one more piece of state in that checkout.
4. Variant 1 is right that #539's review surface grows. The growth is small relative to 1003 files, but a reviewer must still be told the package is a plan.
5. Variant 3 says "Nothing material" stays unresolved; points 1 and 2 above are material enough to list.

## Shared assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | True for Variant 3 and Variant 2: the #539 author already works in the #539 checkout, so the planning session writes where the plan lives. False for Variant 1 as written: someone must run a session in the coordinator home, and the spec's one-live-session-per-checkout rule (spec 6.2, cited in diff-analysis A-001; not re-read here) makes that either the coordinator planning another session's item or an unauthorized second session. |
| A-002 | ACCEPT for Variant 3 and Variant 2; REJECT for Variant 1 | Verified, not just assumed: `/sc:implement` requires the managed plan inside the current git top-level (`managed-workspace.md:11`) and keeps the ledger, artifacts and archive under that package (`:31`, `:33`, `:54`). Variant 1 breaks this precondition, so its executor STOPs. |
| A-003 | ACCEPT | `~/.claude/CLAUDE.md:84`: more than one source file or more than 5 edits requires a written plan, and "Direct command selection does not waive the written-plan requirement". SW-02 under F1/F2 touches `probes.py`, at least three tests and the allow-list; under F3 at least 16 text locations (`merged-requirements.md:191`; `invariant-probe.md:19`). |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie | All three use the same five sections and four steps. |
| C-001 | Variant 3 | Only placement inside the #539 checkout satisfies `/sc:implement`'s same-checkout rule (`managed-workspace.md:11`) without reopening a Done record. |
| C-002 | Variant 3 | `/sc:implement` in the same checkout is the level-3 executor and runs; Variant 1's cross-checkout call STOPs, Variant 2's `/task` is unneeded level 4. |
| C-003 | Variant 3 (tie with Variant 2) | Neither depends on Q26; Variant 3 wins the tie because it also avoids level 4. |
| C-004 | Variant 1 | It adds nothing to #539's file set; Variant 3 adds a few files, Variant 2 grows a 764-file package. |
| X-001 | Variant 3 | A plan is literally none of the four forbidden kinds, and rules 5 and 15 explicitly route SW-02's plan to Q27 rather than banning it. |
| X-002 | Variant 3 | It removes the conflict using the hatch rule 15 provides; Variant 1 avoids it only by a placement its executor rejects. |
| X-003 | Variant 3 (tie with Variant 1 on level) | Both are level 3, but only Variant 3's level-3 run actually executes; Variant 2 is level 4 without a stated need (`~/.claude/CLAUDE.md:86`). |
| A-001 | Variant 3 | The #539 author plans where the author already works; no second session in another checkout. |
| A-002 | Variant 3 | All package state changes happen in the checkout that holds the code, which `/sc:implement` requires. |

## Overall pick

Variant 3, amended to state that reflect's out-of-package reports stay untracked in the #539 checkout and that the `done/` rename is committed by named paths.
