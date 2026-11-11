# Per-defect fix counts (specs in which the defect is FIXED or DELETED_OK, out of 6 per arm)

| id | sev | base-fresh | stage2 | ab1 | ab2 | ab3 | ab4 | pn1 | pn2 | title |
|---|---|---|---|---|---|---|---|---|---|---|
| D01 | blo | 3 | 3 | 4 | 1 | 6 | 2 | 5 | 3 | P1 gate AC-1.1 (and P1 scope) covers all 37 section 3.1-3.2 commands, including P2-P4 comm |
| D02 | blo | 2 | 3 | 4 | 1 | 4 | 2 | 4 | 1 | P1 makes --unattended accepted on gated/outward commands before their gates and WC-9 switc |
| D03 | blo | 2 | 3 | 3 | 3 | 4 | 5 | 2 | 2 | /sc:load: AC-1.1 and AC-1.2 require a return-contract section and a live contract run that |
| D04 | blo | 0 | 1 | 3 | 0 | 4 | 0 | 5 | 0 | brainstorm and init-lite: 'only changes are the small fixes' and 'every changed command' l |
| D05 | min | 1 | 0 | 1 | 0 | 0 | 1 | 3 | 0 | P1 Commands cell omits 3.1 commands (tdd, troubleshoot, release-split, reflect, init-lite, |
| D06 | blo | 4 | 2 | 3 | 3 | 3 | 4 | 5 | 1 | WC-4 contract path is undefined when --output names a file (tdd, init-lite, spec-panel; AC |
| D07 | blo | 1 | 2 | 5 | 4 | 5 | 6 | 6 | 1 | Adversarial contract path <output>/adversarial/return-contract.yaml contradicts WC-4's <ou |
| D08 | blo | 0 | 0 | 3 | 0 | 2 | 2 | 2 | 0 | Workflow contract path embeds a command-generated id (not known before dispatch) and has n |
| D09 | blo | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | Ready commands with fixed or no output location (cleanup-audit, index-repo, troubleshoot)  |
| D10 | blo | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | Section 3.2 rows that add a 'contract' without an output flag or location (cli-eval, cli-p |
| D11 | blo | 1 | 3 | 2 | 2 | 3 | 4 | 5 | 0 | AC-0.4 requires 7.2 step 3 (contract path and contract status) in P0, before any WC-4 cont |
| D12 | blo | 0 | 2 | 1 | 1 | 3 | 3 | 5 | 0 | AC-0.4 step 4 runs a YAML status/command assertion on the existing (markdown) report file |
| D13 | med | 0 | 3 | 0 | 1 | 3 | 2 | 5 | 0 | Section 2.3 briefs require --unattended, but P0 commands do not have the flag yet and AC-0 |
| D14 | med | 0 | 0 | 0 | 0 | 0 | 1 | 5 | 0 | AC-0.4's 'no Agent-tool wrapper' condition has no check: step 5 only searches for AskUserQ |
| D15 | med | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7.2 step 3's single 15-minute check --wait defeats step 2's worker-show at least every 5 m |
| D16 | med | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7.2 step 2 passes when agentWait is absent (Orca never looked) |
| D17 | med | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7.2 step 6 git-status check has no pre-dispatch baseline, so the phase's own uncommitted e |
| D18 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7.2 step 6 fails for edit-in-place commands; 'documented artifacts' is undefined |
| D19 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7.2 step 5 plain-text search for AskUserQuestion matches mentions, not calls |
| D20 | blo | 0 | 1 | 0 | 0 | 2 | 0 | 1 | 0 | AC-C5 and AC-0.3 additive-edit grep '^-[^-]' misses deleted '- bullet' and '---' lines |
| D21 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | AC-C1 (and other piped checks) written with table-escaped \| : copied raw, the alternation |
| D22 | blo | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 1 | AC-C1 scans src/superclaude/core, where SA-2 allows an Orca example in WORKER-CONTRACT.md  |
| D23 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | AC-C1 checks only four orca subcommands while SA-2 bans any orca/orca-ide command |
| D24 | blo | 1 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | WC-3 relay lets a coordinator's ask reply supply the /sc:implement Ruling or other person- |
| D25 | blo | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | WC-3 answer-as-flag can turn on an outward action that the brief never authorised (WC-9, D |
| D26 | blo | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | WC-3 optional ask path makes the 7.2 live check and AC-2.2/AC-4.1 non-deterministic; 7.2 h |
| D27 | blo | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | cli-portify's three approval gates only resolve as blocked, so AC-2.3's happy path can nev |
| D28 | blo | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | AC-2.2 demands a blocked contract from every P2 command, but several resolve their gate by |
| D29 | blo | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | WC-5 maps an empty, unparseable, status-less or out-of-vocabulary contract to --outcome su |
| D30 | med | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | WC-5 'the report says failed or blocked' is undefined for interim non-contract reports (RE |
| D31 | blo | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | cleanup-audit and index-repo keep fixed output paths, so two workers in one worktree colli |
| D32 | med | 0 | 1 | 0 | 0 | 0 | 0 | 5 | 0 | init-lite's resume behaviour 'Re-run overwrites its marked report' is neither WC-6 option, |
| D33 | med | 0 | 1 | 0 | 0 | 1 | 0 | 4 | 0 | WC-6 'fresh output directory' vs WC-4 coordinator-passed directory: no rule says a retry g |
| D34 | med | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | WC-11 (and WC-10) default-changing rules are not scoped to unattended mode, contradicting  |
| D35 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | index row only asserts knowledge-base mode does not wait, while UNVERIFIED item 6 says sec |
| D36 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 'Ready today' tdd and troubleshoot can still prompt a person with the stated brief flags ( |
| D37 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Live-check ORCA commands carry no --from/--terminal, required when run outside an Orca ter |
| D38 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | AC-4.2 invocation omits the explicit pre-tag choice the post-release row requires, so the  |
| D39 | min | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | AC-4.2 requires the contract to list skipped outward steps, but no WC-4 or row field is de |
| D40 | med | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | AC-4.2 claims no install or VM step ran but only checks git log and the PR list |
| D41 | med | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | SA-3 forbids standalone file changes that the adversarial and workflow P1 fixes make |
| D42 | min | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Section 1.1 says command changes are limited to the worker contract, contradicting the sec |
| D43 | min | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | cli-portify's 'dispatch only inside an IronClaude checkout' change is in neither the contr |
| D44 | min | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | WC-10 splits waits longer than 5 minutes, while AC-4.3 fails any tool call over 240 s |
