# Diff Analysis: Position Paper Comparison (OAG3, auto_enable default and label creation)

## Metadata
- Generated: 2026-11-20 (session date)
- Variants compared: 2
- Variant 1: OURS (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/position-OURS.md`): default-on after the throwaway run; NG-2 covers the poll cycle only.
- Variant 2: CLAY (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/position-CLAY.md`): `auto_enable` false, a recorded go per repo; strict NG-2 (no GitHub write in setup).
- Total differences found: 19 diff points (structural 3, content 7, contradictions 4, shared assumptions 5); 9 unique contributions are listed for base selection and the merge plan but are not separate debate points
- Categories: structural (3), content (7), contradictions (4), unique (9), shared assumptions (5)
- Taxonomy tag (AD-5) is shown per debated point: L1 surface, L2 structural, L3 state-mechanics.

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Taxonomy | Severity |
|---|------|------------------|------------------|----------|----------|
| S-001 | Section layout and numbered lists | Same six H2 sections; Mechanism is a 5-step numbered list | Same six H2 sections; Mechanism is a 3-step numbered list | L1 | Low |
| S-002 | Wording of the claim and its framing | States the answer as "switches itself on ... after one owner go" with a staging key conceded | States the answer as "`auto_enable` stays false" and "no GitHub write anywhere in setup" | L1 | Low |
| S-003 | Evidence organization (where facts come from) | Facts grounded mostly in planb code lines and tests (`generate.py`, `repos.py`, `defaults.py`, `first_run.py`) | Facts grounded mostly in merged-requirements rows (K24, S17, MC-12) and Clay's design lines; fewer code reads | L2 | Medium |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Taxonomy | Severity |
|---|-------|--------------------|--------------------|----------|----------|
| C-001 | OA-28a: who moves a new repo's config from `enabled: false` to `enabled: true` | `first_run` does it when its six checks pass; after the single S17 throwaway go, every later in-scope repo self-enables, no per-repo go | `first_run` never does it; the owner names the repo in chat, one recorded go per repo | L3 | High |
| C-002 | OA-28b: scope of NG-2 | NG-2 governs the poll cycle (`once`); `first_run`/`repo_init` may create labels once | NG-2 means no GitHub write anywhere in setup; labels by hand, init only checks | L2 | High |
| C-003 | How strong the existing brake chain is | Layered: `allowed_owners`, generation filters (Project, approvers), six checks, closed ship gate, per-issue approval, `worktree_invalid` until Coder 516 | Thin: gate is one constant; guard reads command text only (INV-025); X-001 claim route unverified; 516 not landed so untestable | L3 | High |
| C-004 | Who creates the two labels (trigger, `hold:backlog`) and when | Init creates both once (D09 rule 2); admits planb creates only the trigger label today | By hand; `first_run` only calls the read-only `trigger_label_state` (Clay design D:445 for `hold:backlog`) | L2 | Medium |
| C-005 | Role of the `auto_enable` key | Concedes a staging key may hold the default off until the throwaway run, then flip once | The key is the permanent per-repo switch; default stays false | L2 | Medium |
| C-006 | What `first_run` does at the label step while the key is false | Not stated | Reads only (`trigger_label_state`); label creation waits for the owner | L3 | Medium |
| C-007 | Manual cost versus zero setup (R17, R18) | Zero setup stays true after the first repo; a per-repo go "adds a human step to a path that already needs a human approval" | Accepts the manual go per repo; zero setup is "not zero" for repos after the first | L2 | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Taxonomy | Impact |
|---|-------------------|--------------------|--------------------|----------|--------|
| X-001 | Is the closed ship gate an adequate brake to satisfy "R33 before R18"? | Yes: `GOVERNED_LEVELS_ALLOWED = False` exists in planb (`launch.py:48`), so the D01/D03 condition is met (fact 5) | The gate is "only a constant"; D14 verdict line 58 calls the brake one config default; INV-025 means a claim session can still comment and assign (fact 6) | L3 | Medium |
| X-002 | Does the label write need a fresh owner OK? (conflict inside V1) | Claim: init creates labels "behind the owner's chat OK before the first real run" | Costs section of the same paper: the label is created "without a fresh chat go" the first time `run-all` meets a new in-scope repo | L3 | Medium |
| X-003 | What the pinned argv tests (`test_security_invariants.py:652, 683`) pin | They scan the cycle's argv forms, not init (fact 6) | They "encode" the flat NG-2 sentence, implying a setup write breaches them (fact 3) | L2 | Medium |
| X-004 | Scope of Clay's "name each repo" rule (design D:1125) | Not cited | Cited as Clay's per-repo switch-on rule; the sentence is about the author's live tests of PR B in a test orchestrator repo | L2 | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Reach is bounded in code: `BUILTIN_ALLOWED_OWNERS = ("IronbellyOrg",)`, `foreign_owner` skip (`defaults.py:30`, `repos.py:141`) | High |
| U-002 | V1 | Generation filters (one Project, readable approvers) and failed-check-keeps-off (`generate.py:192-250`, `first_run.py:16-17`) | High |
| U-003 | V1 | The code already splits cycle from init: `trigger_label_state` reads only, `ensure_trigger_label` is "only the first run" (`repo_init.py:93-116`) | High |
| U-004 | V1 | Clay's own design has the poll write `hold:plan` (D:436-445), so a strict setup rule is narrower than Clay's design | Medium |
| U-005 | V1 | Planb creates only the trigger label (`first_run.py:193`); `hold:backlog` creation is not built | Medium |
| U-006 | V1 | Without Coder 516, every repo reports `worktree_invalid` and stays off (MR line 577) | Medium |
| U-007 | V2 | X-001 live check (claim agents share one `Coordinator` worktree) has not been run (MR lines 311, 550) | High |
| U-008 | V2 | "No config is switched on before S17" rule and `run-all --dry-run` as the only pre-S17 form (MR lines 416, 431) | Medium |
| U-009 | V2 | Staged-risk framing: the first repo proves the chain, each later repo is a decision; cost of the key is one defaults key and two tests (MR lines 353, 503) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Taxonomy | Impact | Status |
|-------|------------|------------------|----------------|----------|--------|--------|
| A-001 | The single throwaway-repo run (S17) is a proof of the whole chain, and "passed" is well defined | Both treat S17 as the pivot (V1 fact 9, V2 fact 1) | UNSTATED (no paper defines pass criteria) | L3 | High | Promoted |
| A-002 | Every later in-scope repo has the same shape as the throwaway repo (one Project, readable approvers, a `Coordinator` worktree), so the proof generalizes | Both reason from one repo to all | UNSTATED | L3 | High | Promoted |
| A-003 | Registering a repo in Orca signals the owner's intent to watch it | Both accept `run-all` discovering repos through `orca repo list` | UNSTATED | L2 | Medium | Promoted |
| A-004 | A person will notice and can reverse a self-enabled repo or a stray label quickly (label delete, `enabled: false`, `DISABLED` kill file) | V1 calls the write reversible; V2 relies on the owner naming repos | UNSTATED | L3 | Medium | Promoted |
| A-005 | The planb line numbers cited stay valid after planb is rebased onto post-revert master | Both cite planb lines; MR line 501 expects modify/delete conflicts | UNSTATED | L2 | Low | Promoted |
| (n/a) | The per-issue approval stays the start gate (D01, OA-1) | V1 states it; V2 does not contest it | STATED (not promoted) | | | Documented |
| (n/a) | Coder 516 lands before any real enablement | Both say so in different words | STATED (not promoted) | | | Documented |

## Summary
- Total structural differences: 3
- Total content differences: 7
- Total contradictions: 4
- Total unique contributions: 9
- Total shared assumptions surfaced: 7 (UNSTATED: 5, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, A-001, A-002, U-001, U-002, U-003, U-007
- Taxonomy counts of the 19 debated points: L1 = 2 (S-001, S-002); L2 = 9 (S-003, C-002, C-004, C-005, C-007, X-003, X-004, A-003, A-005); L3 = 8 (C-001, C-003, C-006, X-001, X-002, A-001, A-002, A-004). All three levels have points.
- Total diff points for convergence: S 3 + C 7 + X 4 + A 5 = 19.
- Similarity check: differences are well above the 10 percent threshold (the papers disagree on both sub-questions), so the debate runs.
