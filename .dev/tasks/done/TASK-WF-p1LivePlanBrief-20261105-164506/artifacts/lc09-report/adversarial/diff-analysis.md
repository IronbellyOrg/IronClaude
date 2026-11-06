# Diff Analysis: Decision Option Comparison (D1: how a command knows it runs unattended)

## Metadata
- Generated: 2026-11-05T19:27:30+00:00
- Variants compared: 2 (Variant A = `option-a.md`, explicit `--unattended` flag; Variant B = `option-b.md`, the command detects it runs as an Orca worker)
- Total differences found: 18 (plus 3 promoted shared assumptions)
- Categories: structural (2), content (7), contradictions (2), unique (7), shared assumptions (3 promoted of 5)
- Taxonomy tags (L1 surface / L2 structural / L3 state-mechanics) are given per point; diff points counted for convergence: 14 (S 2 + C 7 + X 2 + A 3)

## Structural Differences
| # | Area | Variant A | Variant B | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Section set | 4 sections after the title: Safety, Reliability, How a person works day to day, Implementation cost (5 headings) | Same 4 sections plus a leading "Strongest case for it" section (6 headings); a presentation difference only | Low | L1 |
| S-002 | Citation key | Two keys: `SPEC:N`, `CAPS:N` | Three keys: adds `[G] N` (lines of `orca-ide skills get orchestration` 1.4.237) | Low | L1 |

## Content Differences
| # | Topic | Variant A Approach | Variant B Approach | Severity | Level |
|---|-------|-------------------|-------------------|----------|-------|
| C-001 | Trigger mechanism (interface between brief and command) | Standalone `--unattended` token on the command line; nothing in the environment, conversation or Orca turns it on (A:3) | Command detects it is a worker via `ORCA_TERMINAL_HANDLE` or the live preamble with Task and Dispatch IDs; no flag (B:3) | High | L2 |
| C-002 | Meaning of the 2026-11-02 environment evidence (environment state seen in a non-worker terminal) | Evidence shows detection in general "would misfire"; the explicit flag is immune (A:9) | Same observation, but concludes only the environment-variable route is unsafe; preamble route is "safer for people" (B:13-14) | Medium | L3 |
| C-003 | Forgotten-trigger failure (a worker left in a stalled, waiting state) | Listed as a "known weakness": a forgotten flag stalls the worker, caught only after the fact by the brief template and stall proof (A:19) | Presented as the main argument for detection: it "removes that whole failure class" (B:9) | Medium | L3 |
| C-004 | Testability | Deterministic, checkable by text; AC-1.1 asserts which commands carry an `## Unattended mode` section (A:13) | Not mechanically testable; no token to grep; a wrong guess is invisible until a run stalls or a prompt vanishes (B:17) | High | L2 |
| C-005 | Coupling to Orca (dependency of commands on the caller) | Caller-neutral: names the condition (no person), so `claude -p`, CI or another orchestrator can use it (A:14) | Ties every command to Orca; violates spec non-goal 1 and SA-2; does nothing for other callers with no person (B:18) | High | L2 |
| C-006 | Implementation cost and reversibility | One shared parse rule plus a short section per command; adding a detection trigger later is cheap (A:22-23) | Low per brief, higher per command (detection text naming Orca); AC-C1 grep needs an exception; undoing means touching every command (B:25) | Medium | L2 |
| C-007 | Outward-defaults guard (what a person can lose) | The flag is also the guard that turns outward defaults off (WC-9), so a person cannot lose, for example, auggie-review's posting default by working inside Orca (A:10) | Only notes that a person using the environment route would lose approval prompts and outward defaults (B:13) | Medium | L3 |

## Contradictions
| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Level |
|---|-------------------|-------------------|-------------------|--------|-------|
| X-001 | Is preamble-based detection safe? | "Nothing in the environment, the conversation or Orca turns it on" and "Detection would misfire ... observed rather than hypothetical" (A:3, A:9); the observation is only about the environment variable | "Preamble detection is safer for people (a person's own session has no preamble)" (B:14) | Medium | L2 |
| X-002 | Does detection remove the stalled-worker failure state? (intra-Variant B) | n/a | B:9 "Detection removes that whole failure class" versus B:17 "a wrong guess by the model is invisible until a run stalls or a prompt disappears" and B:14 "relies on the model noticing prose" | High | L3 |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Phase-gating: a command accepts the flag only once its gates are converted, so the flag never promises behaviour the command lacks (A:15) | High |
| U-002 | A | Quoted-argument parse rule (`--unattended` inside a quoted prompt never counts), with a live check AC-2.8 (A:8) | High |
| U-003 | A | Names its own known weakness and the after-the-fact catches (brief template, step-3 stall proof) (A:19) | Medium |
| U-004 | A | Migration path: detection can be added later as an extra trigger without removing the flag (A:23) | Medium |
| U-005 | B | Orca's own role table defines a worker by the live preamble with Task and Dispatch IDs, so detection would reuse Orca's rule (B:8) | Medium |
| U-006 | B | The one repo precedent (`claude --print` headless detection) would not fire for an Orca worker, because Orca launches Claude interactively with the task on the command line (B:19) | Medium |
| U-007 | B | The preamble arrives on the same command line as the task, so the two are hard to tell apart in a test (B:14) | Medium |

## Shared Assumptions
Agreement points scanned: (1) both say environment-variable detection is unsafe; (2) both protect a person's prompts (SA-1); (3) both accept that a missed trigger stalls a worker silently; (4) both treat the trigger as a rule a model applies to text.

| A-NNN | Assumption | Source Agreement | Classification | Promoted | Impact | Level |
|-------|-----------|------------------|----------------|----------|--------|-------|
| A-001 | The single 2026-11-02 observation (variable set, handle absent from `worker-list`) proves the variable is set in non-worker terminals in general; neither checks other Orca profiles, versions, or a stale worker list. The environment state may differ elsewhere | Agreement (1) | UNSTATED | Yes | High | L3 |
| A-002 | A model reliably applies the trigger guard (recognizing a standalone token outside quotes in A; recognizing a live preamble in B) with an acceptable failure rate; neither measures it | Agreement (4) | UNSTATED | Yes | High | L3 |
| A-003 | The two options are mutually exclusive. Neither considers a hybrid: require the flag, but when a live preamble is present and the flag is absent, refuse instead of prompting (this is how `~/.claude/WORKER-CONTRACT.md` "Brief guard" case 1 is written) | Agreement (3) | UNSTATED | Yes | High | L2 |
| A-004 | A person never types the flag (A:8) and a person's own session has no preamble (B:14) | Agreement (2) | STATED (in both) | No | Medium | - |
| A-005 | A stalled waiting worker is reported by Orca as healthy, so it is not noticed (A:19, B:9) | Agreement (3) | STATED (in both) | No | Medium | - |

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-001 | Single observation generalizes to all Orca terminals | High | Promoted: debate |
| A-002 | Model applies the trigger rule reliably | High | Promoted: debate |
| A-003 | Flag and detection are mutually exclusive | High | Promoted: debate |

## Summary
- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 2
- Total unique contributions: 7
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Diff points counted for convergence: 14 (S-001..S-002, C-001..C-007, X-001..X-002, A-001..A-003)
- Taxonomy coverage: L1 = 2 (S-001, S-002); L2 = 6 (C-001, C-004, C-005, C-006, X-001, A-003); L3 = 6 (C-002, C-003, C-007, X-002, A-001, A-002)
- Highest-severity items: C-001, C-004, C-005, X-002, A-001, A-002, A-003
- Variants substantially identical? No (all differences far above the 10% threshold); debate proceeds.
- Citation key for A:N / B:N = line N of `variant-1-original.md` / `variant-2-original.md`.
