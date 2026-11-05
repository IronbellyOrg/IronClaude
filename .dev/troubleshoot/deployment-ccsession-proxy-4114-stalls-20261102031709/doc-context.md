# Documentation Context Card

**Generated**: 2026-11-02T03:22:20Z
**Wave**: 1.5
**Scope**: src/superclaude/skills/ccsession-tag/

## Release context

- **Release**: None found
- **Artifacts**: .dev/specs/ccsession-native-install.md (line 48 puts the shim's runtime behaviour out of scope), .dev/specs/ccsession-native-install-design.md (line 307 lists the shim as a non-goal), .dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md (line 15: several Orca sessions share one shim)
- **Summary**: No release artifact sets a shim lifecycle rule; the ccsession specs explicitly exclude the shim. The Orca e2e evidence shows sharing one shim across Orca sessions is the normal, tested mode.
- **Confidence**: 0.9 (that nothing constrains the fix)

## Architectural docs consulted

- `src/superclaude/skills/ccsession-tag/README.md` — verdict: `current` — ccsession starts one shim per settings/port, shared by every session; it "keeps running until you stop it" (README.md:415-418) and "ccsession never stops a running shim by itself" (README.md:504-505); no time limit once a reply starts (README.md:332-335); no log location documented.
- `src/superclaude/skills/ccsession-tag/SKILL.md` — verdict: `current` — points to README.md; no lifecycle content.

## Restrictions / decisions that constrain the fix

- `src/superclaude/skills/ccsession-tag/ccsession:762` (setup_shim) — "Never stop another shim ... a started reply must never be cut off."
- `src/superclaude/skills/ccsession-tag/ccsession:718` (shim_listener_pid) — the shim is found by its script path when lsof is absent: the command line must still contain the script path.
- `src/superclaude/skills/ccsession-tag/ccsession:799` (start block) — the shim inherits the launching env.
- `src/superclaude/skills/ccsession-tag/ccsession:814` (health wait) — attach only to a shim whose health matches.
- `src/superclaude/skills/ccsession-tag/README.md:36` (portability) — macOS or Linux; no `setsid` binary on macOS; `ccsession:351` precedent: use python3 when a util-linux command is missing; bash 3.2 (`ccsession:1179`).
- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:70` (logging) — persistent logging stays opt-in (GW_PROXY_LOGFILE).

## Re-frame signals

- The documented contract (README.md:415-418, 504-505; ccsession:762) says a shared shim keeps running until the user stops it and a started reply is never cut off. The observed death of the shim when its launching terminal closes violates that contract: this is a code defect, not documented behaviour.
- A fix must detach the shim without the `setsid` binary (macOS), keep the script path in its command line, keep the inherited env, and keep logging opt-in.
