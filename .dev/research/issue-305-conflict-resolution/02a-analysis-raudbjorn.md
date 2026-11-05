# Analysis: Raudbjorn/conflict-of-interest (git-conflict-resolver skill)

Source: https://github.com/Raudbjorn/conflict-of-interest at commit 945f5be198516497447411250a606be4e67eaf57 (local clone `/tmp/cr305-repos.Tkozsd/conflict-of-interest`). Focus: git merge-conflict resolution only. Paths below are relative to the clone root. No script was run.

## 1. Summary

The skill has two modes: Resolve, a six-step procedure (detect, categorize, resolve by category, validate, regenerate and continue, summarize), and Split (S1-S3, propose and open stacked PRs). A constitution of three rules overrides the procedure: no markers, no blanket sides, halt on unknown intent.
Deterministic work is done by bash helpers: operation detection, path categorization, mergiraf, stacked-PR similarity, a per-file router, line-combination candidates, a capped cross-file context bundle, history mining, marker/whitespace/typecheck/test validation with a reprompt artifact, and a symbol-based semantic audit. Every helper is advisory except validation.
Model judgment covers `other` files: root cause, one-sentence intent per side, conflict type, the edit itself and a behaviour sentence, all recorded in a per-file Decision Record.
It halts on migrations, submodules, binaries, unresolvable generated specs, unknown intent, more than 300 conflict lines, an `ambiguous` recombination verdict, router halt lanes, an exhausted reprompt budget and unreviewed `SUSPECT` audit output. It recommends aborting at 20+ conflicted files, 5+ consecutive conflicting rebase steps, or the same conflict recurring 3+ times under rerere.

## 2. Itemized behaviours and instructions

### Scope, modes and constitution

- [R-01] Activate when git status shows unmerged paths or a rebase, merge, cherry-pick or revert is paused with conflicts. | source: SKILL.md:4-7
- [R-02] Do not use the skill for abstract git education, blanket --ours/--theirs sweeps, force-push recovery or general PR review. | source: SKILL.md:14-15
- [R-03] Accept the arguments --abort, --continue and --split. | source: SKILL.md:16
- [R-04] Limit Bash to git, gh auth status, gh pr, mergiraf, timeout, the package-manager CLIs and python. | source: SKILL.md:17
- [R-05] Automate mechanical resolution, make judgment explicit, and halt and ask when intent cannot be inferred. | source: SKILL.md:23-24
- [R-06] Read references/design-rationale.md only when the rationale is needed. | source: SKILL.md:26-27
- [R-07] Read constitution.md and treat its rules as overriding every other step of the procedure. | source: SKILL.md:31-35; constitution.md:3
- [R-08] Use Resolve mode by default when an operation is paused with conflicts. | source: SKILL.md:41-42
- [R-09] Use Split mode on --split or on a request to decompose an oversized PR or branch with no active conflict. | source: SKILL.md:43-45
- [R-10] Route to Split mode from the large-conflict gates when a conflict is too large to resolve in place. | source: SKILL.md:45-46
- [R-11] Never continue, commit or stage a final resolution that leaves `<<<<<<<`, `|||||||`, `=======` or `>>>>>>>` in tracked source files. | source: constitution.md:7-13
- [R-12] Allow conflict markers in documentation examples but never in source paths. | source: constitution.md:15
- [R-13] Forbid `git checkout --ours .` by default. | source: constitution.md:19-21
- [R-14] Forbid `git checkout --theirs .` by default. | source: constitution.md:22
- [R-15] Forbid `git reset --hard` during an active conflict operation. | source: constitution.md:23
- [R-16] Forbid `git rebase --skip` without first inspecting the skipped patch. | source: constitution.md:24
- [R-17] Allow bulk operations only for mechanical categories (lockfiles, generated output, snapshots) and only one category at a time. | source: constitution.md:26-27
- [R-18] For `other` files, do not edit unless ours and theirs intent can each be stated in one sentence; otherwise show evidence and ask the user. | source: constitution.md:31-32
- [R-19] When the user overrides a rule, record the override visibly. | source: constitution.md:38
- [R-20] Apply a user override only to the scope it was given for. | source: constitution.md:39
- [R-21] Do not generalize a user override to other files. | source: constitution.md:40
- [R-22] Refuse any override that would leave conflict markers in source code. | source: constitution.md:41

### Step 1: detecting the in-progress operation

- [R-23] Start by running `scripts/conflict-status.sh`. | source: SKILL.md:50-54
- [R-24] The status script detects the operation by checking `.git/rebase-merge`, then `.git/rebase-apply`, then `MERGE_HEAD`, `CHERRY_PICK_HEAD` and `REVERT_HEAD`, and otherwise reports `none`. | source: scripts/conflict-status.sh:45-57
- [R-25] For a rebase it reads step progress from `msgnum`/`next` and `end`/`last` and the branch from `head-name`. | source: scripts/conflict-status.sh:29-39
- [R-26] It counts unmerged paths with `git diff --name-only --diff-filter=U` and prints context, progress, branch and count separated by tabs. | source: scripts/conflict-status.sh:41-43; SKILL.md:56
- [R-27] With no operation and --abort, report "no operation in progress". | source: SKILL.md:60
- [R-28] With no operation and no argument or --continue, report "no conflicts". | source: SKILL.md:61
- [R-29] With an active operation and --abort, run `git <ctx> --abort`. | source: SKILL.md:62
- [R-30] With an active operation and zero unmerged paths, run `git <ctx> --continue`, or `git commit --no-edit` for a merge. | source: SKILL.md:63
- [R-31] With an active operation, unmerged paths and --continue, continue without resolving. | source: SKILL.md:64
- [R-32] With an active operation, unmerged paths and no argument, proceed to Step 2. | source: SKILL.md:65

### Abort thresholds and large-conflict gate

- [R-33] Recommend aborting when one rebase step has 20 or more conflicted files. | source: SKILL.md:67-69
- [R-34] Recommend aborting when five or more consecutive rebase steps have conflicts. | source: SKILL.md:70
- [R-35] Recommend aborting when the same conflict reappears three or more times with rerere enabled. | source: SKILL.md:71
- [R-36] Treat the abort thresholds as configurable heuristics, not empirical laws. | source: SKILL.md:73-74
- [R-37] When the unmerged count is 20 or more, run `suggest-pr-split.sh --conflicts --scope both --json` before categorizing. | source: SKILL.md:74-77
- [R-38] If that run returns high-confidence groups, recommend aborting and re-landing as smaller PRs, refactor-baseline first. | source: SKILL.md:77-79
- [R-39] Treat the split recommendation as advisory, and do not treat low-confidence (cross-cutting) groups as safe splits. | source: SKILL.md:79-81

### Step 2: categorization

- [R-40] Run `scripts/categorize-conflicts.sh` on the unmerged paths. | source: SKILL.md:83-87
- [R-41] Use the categories lockfile, migration, submodule, binary, generated, snapshot, notebook, mergiraf and other. | source: SKILL.md:89-90
- [R-42] The categorizer assigns the first match in the order submodule, binary, lockfile, migration, snapshot, notebook, generated, mergiraf, other. | source: scripts/categorize-conflicts.sh:19-40
- [R-43] A path is a submodule when an unmerged index entry has mode 160000. | source: scripts/categorize-conflicts.sh:8-11
- [R-44] A path is binary when `git diff --numstat` reports `-` for both added and deleted. | source: scripts/categorize-conflicts.sh:13-17
- [R-45] A path is a lockfile when its basename is one of 17 fixed names (package-lock.json, yarn.lock, pnpm-lock.yaml, Cargo.lock, uv.lock, flake.lock and others). | source: scripts/lib/path-classifiers.sh:13-21
- [R-46] A path is a migration when it sits under a known migration directory (migrations, alembic/versions, db/migrate, prisma/migrations, Liquibase changelog, sqitch, drizzle and others), is an ORM config such as ormconfig.* or knexfile.*, or has a Flyway/changeset/migration-SQL name. | source: scripts/lib/path-classifiers.sh:23-42
- [R-47] A path is a snapshot when it is under `__snapshots__/` or ends in .snap, .snapshot, .snapshots, .snap.txt or .snap.json. | source: scripts/lib/path-classifiers.sh:60-68
- [R-48] A path is a notebook when it ends in .ipynb. | source: scripts/lib/path-classifiers.sh:70-75
- [R-49] A path is generated when it is under generated/, generated-sources/, dist/, build/ or coverage/, matches *.generated.*, *.gen.*, protobuf or GraphQL output patterns, or is named schema.graphql or schema.json. | source: scripts/lib/path-classifiers.sh:44-58
- [R-50] A path goes to mergiraf when it is a listed build file (Makefile, go.mod, pyproject.toml and others) or has one of the listed source/config extensions, including .md, .json and .yaml. | source: scripts/lib/path-classifiers.sh:77-91
- [R-51] Report the categorization before editing anything. | source: SKILL.md:92

### Step 3a-3h: per-category handling

- [R-52] For lockfiles, accept theirs with `git checkout --theirs <file> && git add <file>` to clear markers. | source: SKILL.md:96-102
- [R-53] Regenerate the accepted lockfiles later in Step 5. | source: SKILL.md:98
- [R-54] For migrations, do not auto-resolve; show both sides and ask the user. | source: SKILL.md:104-106
- [R-55] For migrations, state the operation-specific ours/theirs meaning, especially during a rebase. | source: SKILL.md:106-107
- [R-56] For submodules, halt, show both pinned SHAs and ask which commit the submodule should point to. | source: SKILL.md:109-111
- [R-57] For binary files, halt, show file type and size, and ask whether to keep ours or theirs. | source: SKILL.md:113-115
- [R-58] For generated files, resolve the source spec first and then regenerate the output. | source: SKILL.md:117-119
- [R-59] For generated files, halt when the source spec cannot be identified or both specs changed incompatibly. | source: SKILL.md:119-120
- [R-60] For snapshots, take the side that matches the intended code state and then regenerate the snapshots. | source: SKILL.md:122-124
- [R-61] For snapshots during a rebase, state explicitly that "ours" is upstream and "theirs" is the replayed commit before choosing. | source: SKILL.md:125-126
- [R-62] For notebooks whose conflict is only in `outputs` or `execution_count`, strip the outputs. | source: SKILL.md:128-130
- [R-63] For notebooks whose source cells conflict, treat the file as `other` and run intent inference. | source: SKILL.md:131
- [R-64] For mergiraf files, run `timeout 30 mergiraf solve -- <file> --compact --keep-backup=false`. | source: SKILL.md:133-137; references/mergiraf-integration.md:12-16
- [R-65] If mergiraf exits 124 (timeout), fall through to `other`. | source: SKILL.md:139
- [R-66] If markers remain after mergiraf, fall through to `other`. | source: SKILL.md:139-140; references/mergiraf-integration.md:18
- [R-67] If mergiraf succeeds with no markers left, stage the file. | source: SKILL.md:140
- [R-68] Recommend `git config --global merge.conflictStyle zdiff3` and checking `mergiraf languages` as setup. | source: references/mergiraf-integration.md:5-10
- [R-69] Treat files over roughly 10,000 lines as the main mergiraf timeout risk. | source: references/mergiraf-integration.md:19

### Step 3i: deterministic router for `other` files

- [R-70] Before per-file work on `other` files, run `scripts/meta-route.sh --unmerged-only --json`. | source: SKILL.md:144-149
- [R-71] Record each file's router `route`, `reason` and `confidence` in its Decision Record. | source: SKILL.md:151-152
- [R-72] Use the router to augment and audit judgment, never to replace it. | source: SKILL.md:152-153; references/meta-resolver.md:15-16
- [R-73] The router reads categories from one categorize-conflicts.sh call, balance from parsing the file's markers, the stacked-PR verdict from detect-stacked-pr.sh, and optionally a history score. | source: scripts/meta-route.sh:107-212; references/meta-resolver.md:23-30
- [R-74] Route any non-`other` category to `mechanical` with high confidence. | source: scripts/meta-route.sh:144-145; references/meta-resolver.md:40
- [R-75] Route to `stacked-auto` (high) when every block's stacked verdict is AUTO_HEAD. | source: scripts/meta-route.sh:217-218
- [R-76] Route to `llm-imbalanced` (medium) when any stacked block is ASK. | source: scripts/meta-route.sh:219-220
- [R-77] Route to `halt-decomposition` when ours plus theirs conflict lines exceed 300. | source: scripts/meta-route.sh:79, 221-222
- [R-78] Route to `llm-imbalanced` (medium, modify-delete) when one side is empty. | source: scripts/meta-route.sh:223-224
- [R-79] Route to `llm-imbalanced` (high) when the larger side is at least 3 times the smaller. | source: scripts/meta-route.sh:225-226
- [R-80] Route to `llm-with-history` (medium) when the top history score is 50 or more. | source: scripts/meta-route.sh:80, 227-228
- [R-81] Route to `sbse-recombine` (medium) when the conflict is balanced and has a diff3 base. | source: scripts/meta-route.sh:229-230
- [R-82] Route to `halt-other` when the file has no conflict blocks or only empty blocks. | source: scripts/meta-route.sh:231-234
- [R-83] Route to `llm-imbalanced` with low confidence when no diff3 base is present. | source: scripts/meta-route.sh:235-236
- [R-84] Route to `halt-other` when the worktree file is unreadable. | source: scripts/meta-route.sh:147-148
- [R-85] Route to `halt-other` when detect-stacked-pr.sh exits other than 0/1 or the history search exits other than 0/2. | source: scripts/meta-route.sh:171-211
- [R-86] Exit 12 and halt routing when categorize-conflicts.sh fails. | source: scripts/meta-route.sh:109-111
- [R-87] Expose the thresholds as flags (imbalance 3, large 300, ask 70, auto 95, history 50). | source: scripts/meta-route.sh:79-91
- [R-88] Treat `stacked-auto` only as permission to consider taking the left side; no route is auto-applied and Step 3i.9 still names the action. | source: references/meta-resolver.md:80-82
- [R-89] Have a reviewer compare the prose reasoning with the router verdict and call out drift; frequent disagreement means the heuristic needs updating. | source: references/meta-resolver.md:70-75
- [R-90] Require any new routing row to cite an H-NN heuristic and an I-NN risk entry. | source: references/meta-resolver.md:57-61
- [R-91] When a sub-signal cannot be trusted, route to a HALT lane instead of silently lowering confidence. | source: references/meta-resolver.md:98-99

### Step 3i.1-1a: balance and line-combination candidates

- [R-92] If one side is more than 3 times longer, use LLM analysis. | source: SKILL.md:157-158
- [R-93] If the sides are balanced, prefer line-combination reasoning and lower confidence. | source: SKILL.md:158-159; references/design-rationale.md:26-28
- [R-94] If total conflict content exceeds 300 lines, halt and recommend decomposition with `suggest-pr-split.sh --conflicts --scope both`. | source: SKILL.md:159-160
- [R-95] Fall back to git-imerge when the change cannot be split because all groups are low-confidence or cross-cutting. | source: SKILL.md:161-163
- [R-96] If balanced with a diff3 base and 400 lines or fewer, run `sbse-recombine.sh --file <file> --top 3 --json`. | source: SKILL.md:164-169
- [R-97] The recombiner builds up to 7 candidates: ours-only, theirs-only, left-then-right, right-then-left, union-dedup, intersection and base-plus-additive (base-plus-additive only with a non-empty base). | source: scripts/sbse-recombine.sh:80-119
- [R-98] It scores each candidate as the mean of its line-set Jaccard to ours and to theirs, and sorts by score. | source: scripts/sbse-recombine.sh:218-234
- [R-99] It labels each block none, low-confidence (top below 50), clear-winner, ambiguous or mixed. | source: scripts/sbse-recombine.sh:236-249
- [R-100] It defers blocks over 400 lines or with at least 3x imbalance. | source: scripts/sbse-recombine.sh:187-194
- [R-101] It never writes to the worktree and never applies a candidate. | source: scripts/sbse-recombine.sh:6-7
- [R-102] Treat a `clear-winner` verdict (top at least 95, gap at least 10) as support for an additive or trivial classification. | source: SKILL.md:171-173
- [R-103] Treat an `ambiguous` verdict (top three within 5 points) as a HALT signal and choose by intent, not score. | source: SKILL.md:173-174
- [R-104] On a `deferred` verdict, fall through to the LLM path. | source: SKILL.md:174-175

### Step 3i.2-3: modify-delete and stacked-PR detection

- [R-105] If one side is empty, classify as modify-delete and inspect commit order with `git log --oneline --left-right --merge -- <file>`. | source: SKILL.md:176-177
- [R-106] Run `detect-stacked-pr.sh --file <file> --json` on each `other` file. | source: SKILL.md:178-182
- [R-107] The stacked-PR detector marks a block NO_DIFF3 when it has no base section. | source: scripts/detect-stacked-pr.sh:53-54
- [R-108] It marks a block with an empty base AUTO_HEAD at 95% similarity or more, ASK at 70% or more, and DIVERGE below that. | source: scripts/detect-stacked-pr.sh:55-61
- [R-109] It marks a block with a non-empty base NON_EMPTY_BASE and still reports similarity. | source: scripts/detect-stacked-pr.sh:62-64
- [R-110] Similarity is a whitespace-stripped, deduplicated line-set Jaccard percentage. | source: scripts/lib/jaccard.sh:9-35
- [R-111] Treat the 95/70 thresholds as tunable heuristics. | source: references/design-rationale.md:41-43; scripts/detect-stacked-pr.sh:7-8

### Step 3i.4-4a: evidence and cross-file context

- [R-112] Collect evidence before inferring intent with `git log --oneline --left-right --merge -- <file>`, `git show <sha> -- <file>` and both merge-base diffs (HEAD and MERGE_HEAD). | source: SKILL.md:184-191; references/intent-inference.md:14-19
- [R-113] Use those evidence sources before reading only the conflict hunk. | source: references/intent-inference.md:12
- [R-114] Treat descriptive commit messages as the strongest evidence and generic ones such as "fix", "wip" or "update" as red flags. | source: references/intent-inference.md:21-22
- [R-115] Build a capped cross-file context bundle with `prompt-context.sh --file <file> --k 4`. | source: SKILL.md:193-197
- [R-116] Use that bundle, not freeform `git grep`, as the LLM context for intent inference. | source: SKILL.md:199-201
- [R-117] The context script takes identifier seeds from the ours and theirs sections only, skipping the base section, noise keywords and names shorter than 3 characters. | source: scripts/prompt-context.sh:30-59
- [R-118] It caps seeds at 12, including any --symbol seeds. | source: scripts/prompt-context.sh:65, 113-128
- [R-119] It walks `git grep -n -w -F` up to k hops, excluding md, txt, rst, docs, references, lock, svg and png paths. | source: scripts/prompt-context.sh:16, 152-192
- [R-120] It skips hits inside the conflicted file itself. | source: scripts/prompt-context.sh:167-168
- [R-121] It stops at 48 hits or 12,288 bytes and marks the bundle truncated. | source: scripts/prompt-context.sh:65, 169-173
- [R-122] It exits 2 when no seeds can be extracted. | source: scripts/prompt-context.sh:130-138

### Step 3i.5: historical resolution search

- [R-123] For human-authored source/config conflicts that are semantic, structural, competing or of unclear intent, search for similar historical resolutions. | source: SKILL.md:202-204
- [R-124] Do not run the history search for generated files, lockfiles, snapshots, migrations, notebooks, binaries, submodules or vendored output. | source: SKILL.md:204-205
- [R-125] Run `historical-resolution-search.sh --file <file> --top 3 --json`. | source: SKILL.md:207-210
- [R-126] Treat history matches only as advisory evidence that may clarify project intent or show that the repo usually recombines parent lines. | source: SKILL.md:212-214
- [R-127] Treat `no_signal` as normal in squash-only, rebase-only or shallow histories. | source: SKILL.md:215
- [R-128] Never auto-apply a historical result. | source: SKILL.md:216; references/design-rationale.md:35-37
- [R-129] For C/C++ and other high-risk languages, require stronger intent evidence and validation even when historical examples exist. | source: SKILL.md:218-219; references/history-mining.md:47-50
- [R-130] Pass --symbol to bias ranking toward a named symbol. | source: references/history-mining.md:17-20; scripts/historical-resolution-search.sh:25
- [R-131] The history script returns no_signal for shallow repositories. | source: scripts/historical-resolution-search.sh:154-156
- [R-132] It returns no_signal for promisor/partial clones and never fetches data. | source: scripts/historical-resolution-search.sh:158-160; references/history-mining.md:55-56
- [R-133] It requires `git merge-tree --write-tree` and exits 12 without it. | source: scripts/historical-resolution-search.sh:162-169
- [R-134] It defaults to the current unmerged files when no --file is given. | source: scripts/historical-resolution-search.sh:171-175
- [R-135] It inspects up to 200 merge commits, optionally limited by --since, and stops after 20 seconds. | source: scripts/historical-resolution-search.sh:4-7, 392-409
- [R-136] It skips octopus merges and merges whose parents replay without conflict. | source: scripts/historical-resolution-search.sh:411-421; references/history-mining.md:57
- [R-137] It skips historical results identical to either parent. | source: scripts/historical-resolution-search.sh:438-441; references/history-mining.md:58-59
- [R-138] It scores matches by path similarity (35 same path, 20 same basename, 10 same extension), 15 per matched symbol, line Jaccard times 35, recombination ratio times 10 and up to 10 for recency, capped at 100. | source: scripts/historical-resolution-search.sh:453-494
- [R-139] It flags `high_recombination` when the recombination ratio is 0.80 or more. | source: scripts/historical-resolution-search.sh:473-475
- [R-140] Treat a high recombination ratio as support for line-combination reasoning, not proof that auto-resolution is safe. | source: references/history-mining.md:42-43
- [R-141] It emits an inspection command `git show <commit> -- <path>` for each match. | source: scripts/historical-resolution-search.sh:538-539
- [R-142] Keep snippets off by default and use --include-snippets only when the repository's confidentiality rules allow it. | source: references/history-mining.md:65-68
- [R-143] Snippets are bounded to 40 lines and 4,000 characters. | source: scripts/historical-resolution-search.sh:338-350
- [R-144] For rename-heavy conflicts, inspect the returned command before trusting path similarity. | source: references/history-mining.md:60-61
- [R-145] Exit codes are 0 for matches, 2 for no signal, 10 for bad arguments, 11 outside a repo and 12 for missing git features. | source: scripts/README.md:27-29

### Step 3i.6-10: intent, classification and resolution

- [R-146] Name the structural root cause of the conflict. | source: SKILL.md:220
- [R-147] Infer ours and theirs intent in one sentence each. | source: SKILL.md:221; references/intent-inference.md:3-6
- [R-148] If either intent is unknown, HALT using the HALT schema. | source: SKILL.md:222; references/intent-inference.md:8
- [R-149] Classify the conflict as trivial, additive, competing, structural, modify-delete or semantic. | source: SKILL.md:223
- [R-150] For a trivial conflict (adjacent edits split artificially), combine both. | source: references/intent-inference.md:28
- [R-151] For an additive conflict, keep both sides in a deliberate order. | source: references/intent-inference.md:29
- [R-152] For a competing conflict, pick or synthesize by intent. | source: references/intent-inference.md:30
- [R-153] For a structural conflict (move/rename versus edit), apply the edit to the moved or renamed location. | source: references/intent-inference.md:31
- [R-154] For a delete-versus-edit conflict, determine which intent supersedes. | source: references/intent-inference.md:32
- [R-155] For a semantic conflict (no marker, behaviour clash), run the semantic audit. | source: references/intent-inference.md:33
- [R-156] Before staging an `other` resolution, write one sentence describing behaviour after the merge; if you cannot, you do not yet understand it. | source: references/intent-inference.md:37-38; SKILL.md:328
- [R-157] Resolve the file, remove markers, stage it and produce a Decision Record. | source: SKILL.md:224

### Step 4: validation, reprompt loop and semantic audit

- [R-158] Run `validate-and-reprompt.sh --typecheck '<cmd>' --test '<focused-test-cmd>' --max-iterations 1`. | source: SKILL.md:228-233
- [R-159] The validator fails with exit 1 when any tracked file outside md, txt, rst, docs and references contains a conflict-marker line. | source: scripts/validate-resolution.sh:9, 36-42
- [R-160] --include-path re-includes one of the default-excluded patterns in the marker scan. | source: scripts/validate-resolution.sh:11-21, 27
- [R-161] The validator fails with exit 2 when `git diff --check --cached` reports whitespace errors. | source: scripts/validate-resolution.sh:44-50
- [R-162] The validator runs the typecheck command via `bash -lc` and fails with exit 3. | source: scripts/validate-resolution.sh:52-59
- [R-163] The validator runs the test command via `bash -lc` and fails with exit 4. | source: scripts/validate-resolution.sh:61-68
- [R-164] The wrapper treats only exit codes 1-4 as retryable and passes any other code straight through. | source: scripts/validate-and-reprompt.sh:94-98
- [R-165] On success the wrapper deletes its state and reprompt files and exits 0. | source: scripts/validate-and-reprompt.sh:89-92
- [R-166] On a retryable failure within budget, the wrapper writes `.git/conflict-resolver/reprompt.md` with the exit code, reason, last 60 output lines, involved files and the exact rerun command, records the iteration in a state file, and exits 5. | source: scripts/validate-and-reprompt.sh:100-190
- [R-167] The wrapper refuses state or reprompt paths outside `.git/conflict-resolver/`. | source: scripts/validate-and-reprompt.sh:52-67
- [R-168] The reprompt tells the model to preserve the intent recorded in the Decision Record. | source: scripts/validate-and-reprompt.sh:174-175
- [R-169] The reprompt tells the model not to introduce changes unrelated to the failure. | source: scripts/validate-and-reprompt.sh:176
- [R-170] The reprompt tells the model to HALT and show the conflict and artifact to the user if the same failure recurs. | source: scripts/validate-and-reprompt.sh:178-179
- [R-171] On exit 5, read the reprompt artifact, re-resolve the named files and re-invoke the wrapper. | source: SKILL.md:235-237
- [R-172] When the retry budget (default 1) is exhausted, the wrapper exits with the underlying code and the model must HALT. | source: SKILL.md:237-238; scripts/validate-and-reprompt.sh:100-103
- [R-173] The wrapper never calls an LLM or the network; Claude is the orchestrator. | source: SKILL.md:238-239; scripts/validate-and-reprompt.sh:9-14
- [R-174] After validation, run `scripts/semantic-audit.sh`. | source: SKILL.md:241-245
- [R-175] Review any `SUSPECT` output before continuing. | source: SKILL.md:247
- [R-176] The audit picks the other ref from MERGE_HEAD, CHERRY_PICK_HEAD, REVERT_HEAD or REBASE_HEAD and uses `git merge-base HEAD <other>` as the base. | source: scripts/semantic-audit.sh:24-39
- [R-177] The audit extracts symbol names from added or removed definition lines in each side's diff over 22 source-language globs, dropping keywords and names of 2 characters or fewer. | source: scripts/semantic-audit.sh:41-53
- [R-178] The audit flags a symbol as SUSPECT when one side changed its definition, the other side's diff mentions it, and the current tree still references it outside docs. | source: scripts/semantic-audit.sh:59-71
- [R-179] The audit exits 1 when suspects exist and 2 when no operation is active. | source: scripts/semantic-audit.sh:30-32, 107
- [R-180] Treat signature, type/schema, dependency, constant/env var and public API changes, and one side refactoring while the other adds callers, as high-suspicion semantic changes. | source: references/semantic-conflicts.md:6-13
- [R-181] Use the manual recipe of both merge-base diffs plus `git grep` for a symbol when going beyond the script. | source: references/semantic-conflicts.md:27-34

### Step 5: regenerate and continue

- [R-182] Regenerate package-lock.json with `npm install`. | source: SKILL.md:255
- [R-183] Regenerate pnpm-lock.yaml with `pnpm install`. | source: SKILL.md:256
- [R-184] Regenerate yarn.lock with `yarn install`. | source: SKILL.md:257
- [R-185] Regenerate bun.lockb or bun.lock with `bun install`. | source: SKILL.md:258
- [R-186] Regenerate npm-shrinkwrap.json with `npm shrinkwrap`. | source: SKILL.md:259
- [R-187] Regenerate Cargo.lock with `cargo generate-lockfile`. | source: SKILL.md:260
- [R-188] Regenerate poetry.lock with `poetry lock --no-update`. | source: SKILL.md:261
- [R-189] Regenerate uv.lock with `uv lock`. | source: SKILL.md:262
- [R-190] Regenerate pdm.lock with `pdm lock`. | source: SKILL.md:263
- [R-191] Regenerate Gemfile.lock with `bundle install`. | source: SKILL.md:264
- [R-192] Regenerate composer.lock with `composer install`. | source: SKILL.md:265
- [R-193] Regenerate mix.lock with `mix deps.get`. | source: SKILL.md:266
- [R-194] Regenerate Package.resolved with `swift package resolve`. | source: SKILL.md:267
- [R-195] Regenerate pubspec.lock with `dart pub get` or `flutter pub get`. | source: SKILL.md:268
- [R-196] Regenerate packages.lock.json with `dotnet restore`. | source: SKILL.md:269
- [R-197] Regenerate flake.lock with `nix flake lock`. | source: SKILL.md:270
- [R-198] Continue a rebase with `git rebase --continue`. | source: SKILL.md:276
- [R-199] Finish a merge with `git commit --no-edit`. | source: SKILL.md:277
- [R-200] Continue a cherry-pick with `git cherry-pick --continue`. | source: SKILL.md:278
- [R-201] Continue a revert with `git revert --continue`. | source: SKILL.md:279
- [R-202] Loop back to Step 1 if more conflicts appear after continuing. | source: SKILL.md:281

### Step 6 and record-keeping

- [R-203] Produce a Markdown summary with a per-category table of Auto, User and Halted counts. | source: SKILL.md:285-293
- [R-204] Include lockfiles regenerated, semantic audit result, constitutional overrides and any decomposition recommended in the summary. | source: SKILL.md:295-298
- [R-205] Add a fenced JSON summary with operation, branch, categories, semantic_audit.suspects and overrides. | source: SKILL.md:301-309
- [R-206] For every file, write a Decision Record with category, router route, evidence sources checked, historical resolutions checked, ours intent, theirs intent, root cause, confidence, conflict type, action and behaviour after resolution. | source: SKILL.md:313-329
- [R-207] A confidence of `none` in the Decision Record means HALT. | source: SKILL.md:325
- [R-208] Allowed actions in the record are auto-resolved, user-directed, HALT or decompose-recommended. | source: SKILL.md:327
- [R-209] Add a fenced JSON block per file with file, category, confidence, action and conflict_type. | source: SKILL.md:331-339

### HALT schema

- [R-210] A HALT message names the file, the operation, the step N/M and the branch. | source: SKILL.md:343-346
- [R-211] A HALT message lists the commit messages and ancestor diffs checked for both sides. | source: SKILL.md:348-352
- [R-212] A HALT message gives the best read of what each side appears to do. | source: SKILL.md:354-356
- [R-213] A HALT message offers take ours, take theirs and synthesize, each with its outcome. | source: SKILL.md:358-361
- [R-214] Prefer abstention to a wrong merge, since an unresolved conflict is cheaper than silent code loss. | source: SKILL.md:364; README.md:22-24; references/design-rationale.md:19-21

### Recurring conflicts, rerere and git-imerge

- [R-215] Use rerere for long rebases but review every replayed resolution. | source: references/recurring-conflicts.md:5-6
- [R-216] Use `git config rerere.enabled true`, `git rerere status` and `git rerere diff` to manage rerere. | source: references/recurring-conflicts.md:10-14
- [R-217] When the same conflict reappears three or more times, assume the resolution depends on commit context, abort and use a safer strategy. | source: references/recurring-conflicts.md:16-17
- [R-218] Do not combine rerere.autoupdate assumptions with git-imerge, which disables rerere while it runs. | source: references/recurring-conflicts.md:21-24
- [R-219] Escalate to git-imerge when many consecutive rebase steps conflict, the same conflict repeats with different correct answers, or a large branch mixes refactors and behaviour changes. | source: references/recurring-conflicts.md:26-30
- [R-220] When a large branch mixes refactors and behaviour changes, prefer splitting the refactor into its own preliminary PR. | source: references/recurring-conflicts.md:32-34

### Split mode: proposing boundaries (S1)

- [R-221] Propose split groups with `suggest-pr-split.sh --base <base> --head <head> --json` before any conflict, or `--conflicts --scope both --json` inside an oversized conflict. | source: SKILL.md:371-378
- [R-222] Present groups in merge order: refactor-baseline, then schema/migration, then source, then ui/test. | source: SKILL.md:380-381
- [R-223] State each group's confidence. | source: SKILL.md:381
- [R-224] Flag low-confidence (cross-cutting) groups as structural-only boundaries and do not present them as safe. | source: SKILL.md:382-383
- [R-225] If every group is low-confidence, recommend keeping the change whole or using git-imerge. | source: SKILL.md:383-384
- [R-226] The split script works in conflicts mode (flag or active operation) or range mode (--base/--head), and exits 2 when neither applies. | source: scripts/suggest-pr-split.sh:112-123
- [R-227] In conflicts mode it analyzes unmerged files, the incoming range or both, per --scope. | source: scripts/suggest-pr-split.sh:146-150, 197-207
- [R-228] It groups files by top-level module, using two path segments under src, packages, apps, lib and similar roots. | source: scripts/suggest-pr-split.sh:40-56
- [R-229] It puts renames with similarity of 90 or more into a refactor-baseline group and flags weaker renames as low confidence. | source: scripts/suggest-pr-split.sh:228-236
- [R-230] It classifies each file into a layer (lockfile, migration, generated, test, ui, config, docs, source) and orders groups by layer. | source: scripts/suggest-pr-split.sh:13-38
- [R-231] It rates a group high for one layer, medium for two and low for three or more or a weak rename. | source: scripts/suggest-pr-split.sh:258-267
- [R-232] It downgrades refactor-baseline when a refactored module also carries behaviour changes. | source: scripts/suggest-pr-split.sh:251-256
- [R-233] It warns on low-confidence groups, groups crossing 3+ layers, groups over 400 LOC and scope `both`. | source: scripts/suggest-pr-split.sh:272-289
- [R-234] It is read-only and never creates branches or PRs. | source: scripts/suggest-pr-split.sh:6
- [R-235] Resolve in place when a conflict fits the Step 3 flow, decompose when the change is too big to review or two big features overlap, and use git-imerge when a large branch must land as-is. | source: references/pr-decomposition.md:16-20
- [R-236] Do not treat decomposition and git-imerge as substitutes. | source: references/pr-decomposition.md:22-23
- [R-237] Put pure renames, moves and reformatting into a preliminary PR, and downgrade confidence when the same files also carry behaviour changes. | source: references/pr-decomposition.md:27-31
- [R-238] Land lower layers first (contracts/schema/migration, shared infrastructure, implementation, consumers/UI, cleanup), keeping generated output with its spec and tests with their implementation. | source: references/pr-decomposition.md:32-35
- [R-239] Split independent subfeatures by user-visible capability rather than directory count. | source: references/pr-decomposition.md:36-37
- [R-240] Use ownership, CODEOWNERS and co-change only as supporting signals that never override dependency direction. | source: references/pr-decomposition.md:38-40
- [R-241] Every split must leave the tree buildable/typecheckable on its own. | source: references/pr-decomposition.md:41-43
- [R-242] Treat low-confidence groups as starting points, verify dependencies or keep the change whole, since abstaining beats a wrong split. | source: references/pr-decomposition.md:58-61
- [R-243] Use the git surgery recipes (diff --stat a group, switch -c plus restore --source to carve paths, cherry-pick commits, rebase --onto to retarget). | source: references/pr-decomposition.md:70-86
- [R-244] Treat ~400 LOC per PR and ~25 lines of churn as prompts to consider splitting, not hard cutoffs. | source: references/pr-decomposition.md:133-139
- [R-245] When decomposed PRs are later re-merged, prefer structural merge over hand-concatenation. | source: references/pr-decomposition.md:141-147
- [R-246] Optionally use git-deps or Viezly to find independent clusters in entangled changes. | source: references/pr-decomposition.md:149-154
- [R-247] Avoid mixing formatting/refactors with behaviour changes. | source: references/pr-decomposition.md:158
- [R-248] Never hand-resolve lockfiles; regenerate them from manifests. | source: references/pr-decomposition.md:159
- [R-249] Do not split generated output away from its source spec. | source: references/pr-decomposition.md:160
- [R-250] Do not split tests away from the implementation they validate. | source: references/pr-decomposition.md:161
- [R-251] Do not drop old APIs or columns before all consumers are migrated. | source: references/pr-decomposition.md:162
- [R-252] Do not squash-merge a parent stack PR without rebasing or retargeting its children. | source: references/pr-decomposition.md:163
- [R-253] Do not split so small that no reviewer can understand the behaviour in isolation. | source: references/pr-decomposition.md:164

### Split mode: stacked PRs (S2-S3)

- [R-254] Dry-run the stack with `open-stacked-prs.sh --base <trunk> --head <head> --group "<branch>:<paths>"`. | source: SKILL.md:386-391
- [R-255] The stack script is dry-run by default and only prints the git/gh plan. | source: SKILL.md:393-394; scripts/open-stacked-prs.sh:139-154
- [R-256] It synthesizes new commits from path groups and does not preserve original commit topology unless the user supplied commit-aligned groups. | source: SKILL.md:394-395; references/pr-decomposition.md:117-118
- [R-257] Show the dry-run plan and get explicit user confirmation before re-running with `--execute --remote <name>`. | source: SKILL.md:399-400; references/pr-decomposition.md:94-97
- [R-258] With --execute, the script requires an explicit --remote that exists. | source: scripts/open-stacked-prs.sh:120-122
- [R-259] It refuses a dirty working tree unless --allow-dirty is passed. | source: scripts/open-stacked-prs.sh:123-125
- [R-260] It refuses to execute from main, master or trunk unless --allow-protected is passed. | source: scripts/open-stacked-prs.sh:126-130
- [R-261] It requires gh to be installed and authenticated. | source: scripts/open-stacked-prs.sh:131-132
- [R-262] It refuses duplicate, existing local or existing remote target branch names. | source: scripts/open-stacked-prs.sh:111-118, 133-136
- [R-263] For each group it creates the branch from the previous base, restores the group's paths from head, commits, pushes with -u and opens a PR against the previous branch. | source: scripts/open-stacked-prs.sh:162-175
- [R-264] --draft opens the PRs as drafts. | source: scripts/open-stacked-prs.sh:65, 160
- [R-265] --from-json reads suggest-pr-split groups via python3 and names branches `split/<id>`. | source: scripts/open-stacked-prs.sh:85-99
- [R-266] Verify each split compiles/typechecks on its own before opening the next PR. | source: SKILL.md:403-404
- [R-267] Retarget each child PR to the trunk as its parent merges with `gh pr edit <n> --base <trunk>`. | source: SKILL.md:404-405; references/pr-decomposition.md:122
- [R-268] Stack dependent splits so each PR targets its parent branch rather than the trunk. | source: references/pr-decomposition.md:90-92
- [R-269] On GitHub, track stack state in a draft tracking PR or a description checklist, since there is no native dependency enforcement. | source: references/pr-decomposition.md:129

## 3. Caveats

The Step 1 row "active, unmerged > 0, --continue: continue without resolving" (SKILL.md:64) contradicts constitution Rule 1 (constitution.md:7-8), and git itself refuses to continue while paths are unmerged.
The evidence commands diff against MERGE_HEAD (SKILL.md:189-190, references/intent-inference.md:17-18). MERGE_HEAD does not exist during a rebase, cherry-pick or revert. The scripts use REBASE_HEAD, CHERRY_PICK_HEAD and REVERT_HEAD; the prose does not.
Which git versions accept `git log --merge` during a rebase, cherry-pick or revert was not checked here.
semantic-audit.sh and suggest-pr-split.sh use `git merge-base HEAD <other>` as the base. For a cherry-pick or revert the real base is the picked commit's parent, so the audited range can be wrong (scripts/semantic-audit.sh:36-39).
Step 4 (typecheck and tests) runs before Step 5 regenerates lockfiles. Validation therefore runs against the accepted "theirs" lockfile. Nothing re-validates after regeneration, and nothing says to `git add` the regenerated lockfile before continuing (SKILL.md:226-281).
Some lockfile commands are questionable. `poetry lock --no-update` may be rejected by Poetry 2.x (not checked here). `composer install`, `bundle install`, `mix deps.get` and `dotnet restore` install from an existing lockfile rather than regenerate it. `flutter` is not in allowed-tools (SKILL.md:17, 261-269).
The package-manager installs and the user's typecheck/test commands run code from the incoming side (install scripts, test code), and the skill gives no trust prompt for this (SKILL.md:228-233, 251-270).
allowed-tools does not list the skill's own `${CLAUDE_SKILL_DIR}/scripts/*.sh`, so every helper call may need a permission prompt. Meanwhile `Bash(python *)` is very broad (SKILL.md:17).
Lockfile "accept theirs" gets no rebase ours/theirs warning, though during a rebase "theirs" is the replayed commit. Only migrations and snapshots get that warning (SKILL.md:96-107, 122-126).
"Strip outputs" for notebooks and "regenerate" for generated files and snapshots give no command or tool (SKILL.md:117-131).
Files mergiraf resolves cleanly are staged with no intent check or review; only the later semantic audit looks at them (SKILL.md:139-140).
No script tracks the abort thresholds "5 consecutive conflicting rebase steps" and "same conflict 3+ times under rerere". The model must count across steps by itself (SKILL.md:67-71).
Thresholds drift between documents. SKILL.md says "more than 3x" but the router and sbse use at least 3x (scripts/meta-route.sh:225, scripts/sbse-recombine.sh:191). The router's 300-line total excludes base lines. sbse's 400-line bound is unreachable through the router, which halts above 300.
SKILL.md calls meta-route.sh without --history-search (SKILL.md:148), so the `llm-with-history` route never fires in the documented flow.
Docs and code disagree on detect-stacked-pr.sh errors. references/meta-resolver.md:93 says the stacked signal is "treated as absent". scripts/meta-route.sh:188-191 actually routes the file to halt-other.
The sbse `clear-winner` verdict needs a mean Jaccard of at least 95 to both sides. That happens only when the sides are nearly identical. For genuinely different sides, the score favours union-like candidates and says nothing about correctness (scripts/sbse-recombine.sh:221-246).
validate-resolution.sh scans every tracked file outside docs for markers. Unrelated fixtures that contain markers therefore fail validation (scripts/validate-resolution.sh:37).
validate-resolution.sh excludes *.md from the marker scan, yet .md files are routed to mergiraf. Markers left in Markdown such as a README would pass validation unnoticed (scripts/validate-resolution.sh:9, scripts/lib/path-classifiers.sh:87).
The `git diff --check --cached` whitespace gate can fail on whitespace errors the incoming side brought in, triggering spurious reprompts (scripts/validate-resolution.sh:44-50).
open-stacked-prs.sh runs a bare `gh pr create` with no `--repo` (scripts/open-stacked-prs.sh:172). On a fork, gh defaults that command to the parent repo, which breaks this project's fork-only PR rule. Its protected-branch check also only knows main, master and trunk (scripts/open-stacked-prs.sh:127-130).
open-stacked-prs.sh carves groups with `git restore --source=<head> -- <paths>`. Whether deleted paths, or the old side of a rename, are carried over was not checked here (scripts/open-stacked-prs.sh:169).
Whether `git diff --numstat` on an unmerged binary path really prints `-` `-`, which binary detection depends on, was not checked here (scripts/categorize-conflicts.sh:13-17).
Migration detection also catches config files (ormconfig.*, knexfile.*, data-source.ts) and the whole drizzle/ directory. Those files always go to ask-the-user (scripts/lib/path-classifiers.sh:30-33).
The empirical claims were not checked here: Merge-Bench below 60%, 87% line-combination, Rover k=4 +17.72%, and the AgenticFlict 25-line churn figure. They come from docs/research-synthesis.md (references/design-rationale.md:19-22, references/pr-decomposition.md:135-136, 143).
