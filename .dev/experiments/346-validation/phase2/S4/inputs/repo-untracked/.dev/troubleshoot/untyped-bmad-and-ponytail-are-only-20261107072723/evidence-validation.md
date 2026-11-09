# Evidence Validation Report

(Returned by evidence-validator; persisted by parent on receipt; condensed, tables verbatim where load-bearing.)

**Report under validation**: .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md.draft
**Timestamp**: 2026-11-07T07:51:22Z
**Total citations**: 29 (18 location-level items in `## Evidence`, 11 in prose of other sections)
**Verified**: 29
**Dropped**: 0
**Passed through (command, no reexec)**: 0
**Suggested report status**: partial (rule A5 fired; not a citation failure)

## Verified citations (all re-read at the cited range)

1-4 bmad/install.sh:23, :58-60, :42 and bmad/manifest.yaml:12-14; 5-8 owner-decisions.md:5, gap-closure .memlog.md:32 and :32-33, gap-closure SPEC.md:77; 9-10 catalogue-bundle SPEC.md:174 and :141 (verified textually); 11-13 profiles.yaml:18, :21, :20-21; 14-15 startup.sh:1169 and :1184; 16-18 user_settings_defaults.json:36, install_user_setup.py:384 and :398-399; 19 installed_plugins.json:64-68; 20-21 ironclaude/install.sh:26-29 and :143-146; 22 Dockerfile.coder:139; 23 docs/operations/upstream-monitor.md:62; 24 .github/upstream-monitor/releases.json:113; 25-27 templates/VSCode-AIDev02/README.md:100, :241, :308; 28 test-57-catalogue-configure.sh (oracle at :450 "no seed: bmad writes nothing", :452 `Installed-not-Configured`); 29 test-startup-boot.sh (oracle at :2210-2224).

## Dropped citations

None.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | - | - | headline is UNDETERMINED, no enum token; max calibrated 0.58; producers.md:2 `producer-count: n/a` |
| A2 | skipped | - | - | `assertion_skipped: A2 (diff_path)`: diff_path null |
| A3 | no | - | - | draft Date 07:49:32Z earlier than draft mtime 07:51:14Z, not T00:00:00Z |
| A4 | no | - | - | "Pipeline hardening not applicable" matches contract value `not_applicable` |
| A5 | yes | `consensus_on_unobserved` | partial | candidate-fixes.md:7 "consensus on the sequence", :11 Wave 4 skipped; calibration files state `evidence_class: source_static`; Tier 1 asserts a dynamic claim ("not retried"); mitigated: consensus limited to a documentation-only sequence and the claim is labelled static reading only; status already partial |
| A6 | no | - | - | no Reference-context cells; tasklist total-rows=0 |
| A7 | no | - | - | RUN-SITE unknown (not pending-producers); producers.md has zero producer rows |
| A8 | no | - | - | OBSERVE-VIA nobody; failing arm not a CI job |
| A9 | no | - | - | no literal Reference-context value or reference-arm capture |
| A10 | no | - | - | capability-verdict n/a |

## Notes (condensed)

1. Claim-support stretch (advisory): catalogue-bundle SPEC.md:141 (BMad in repos cloned after boot and Orca worktrees) and :174 (Orca worktrees via tracked install or hook) are not exact statements about first-use creation in an arbitrary project; gap-closure SPEC.md:77 and .memlog.md:32-33 are the stronger support; wording should say "closely related documented non-goal / scope expansion" and name the catalogue-bundle SPEC. (Applied by the parent to Summary, Proposed Fix, Files that MUST NOT change and Alternatives.)
2. Uncited Diagnosis bullets were all checked and hold: bmad-help/SKILL.md:25-26 (one skill, generalised); install_user_setup.py:426-431 and :444 (plugin shortfall returns True, `all(ok ...)`; install.sh exit-code path not traced); no Ponytail code in templates (all hits are comment tags). (Applied: evidence items 15-17 added.)
3. Header wording about the calibrated cards was ambiguous (four cards were calibrated). (Applied.)
4. Duration did not match run-directory timestamps. (Applied: Duration now measured from Wave 0.)
5. audit.log was incomplete relative to the report. (Parent appends Wave 1.5 to 5 entries.)
6. No upstream agent had a citation dropped; every calibrator reported all spot-checks matching.
7. Not re-checked: self-review.md; no cited command was run (allow_command_reexec=false).

## Suggested status reasoning

Dropped citations 0; A5 contributes partial; no A6/A7 failure; A8 did not fire, so blocked does not apply. Result: partial.
