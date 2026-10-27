# D-0024 — Implementation notes

**Task:** T02.02
**Date:** 2026-05-20

## Planning observations

1. Repo root had `LICENSE` (MIT, IronClaude/SuperClaude Framework Contributors) but **no** `NOTICE` file. Confirmed via `ls /config/workspace/IronClaude/NOTICE` → `No such file or directory`.
2. `src/superclaude/cli/eval/pty/` did not yet exist (T02.01 has not landed). The `NOTICE` therefore forward-references that path; T02.01's acceptance criteria explicitly require placing the verbatim upstream `LICENSE` and `PROVENANCE.md` at that path before vendored sources land.
3. `design-spec.md:785-787` ("§13 — License compliance") already prescribes the exact mechanism: retain upstream LICENSE verbatim at the vendored path; reference it from a top-level NOTICE. The R4 ADR ratifies that mechanism rather than re-deriving it.
4. `decisions.md` had no prior OQ-4 entry. The natural insertion point was as **D-10** (next sequential ADR ID after D-9), inserted immediately before the OPS-001 Closure section to preserve numerical ordering of the ADR bodies.
5. Sign-off table updated with a single new row for D-10 (status: 🟠 QUEUED FOR SIGN-OFF (R4)), tracking the same maintainer sign-off lifecycle as D-1..D-8.

## Design choices

- **Top-level `NOTICE` vs inline appendix in `LICENSE`:** chose top-level `NOTICE` (Option A in D-10). Rationale: license-scan tooling looks at repo-root NOTICE files, the convention generalizes to future third-party components, and inline appendices mix IronClaude's own copyright with third-party copyrights in one file (confusing for downstream scanners).
- **Attribution clause wording:** declared canonical in §D-10 "Attribution clause" and reproduced in `artifacts/D-0024/spec.md §2`. The wording references the upstream URL, the license name, the vendored path, and both the `LICENSE` and `PROVENANCE.md` files that will land with T02.01. Future edits MUST update both NOTICE and the ADR clause in lockstep.
- **Forward references to T02.01 artifacts:** intentional. The vendored path `src/superclaude/cli/eval/pty/` is the agreed location per design-spec §3 and §13; T02.01's acceptance criteria require LICENSE + PROVENANCE.md at that path. NOTICE pointing forward is correct because OQ-4 is an **entry blocker** for T02.01, not the other way around.
- **Did NOT modify `LICENSE`:** keeping IronClaude's own copyright untouched. The NOTICE is purely additive attribution discipline.

## Failure-mode considerations

- If a future change relocates the vendored ptytest path (away from `src/superclaude/cli/eval/pty/`), the NOTICE and the D-10 attribution clause MUST be re-pointed. T02.03's quarterly review checklist should include this verification.
- If upstream ptytest re-licenses (away from MIT), the NOTICE wording, the verbatim LICENSE at the vendored path, and D-10's "Closure of OQ-4" block all need re-evaluation. PROVENANCE.md fork SHA pin (T02.03) gives us a stable anchor that lets us detect this on resync.
- If a downstream redistributor strips the NOTICE, the verbatim `LICENSE` at the vendored path still independently satisfies the MIT attribution obligation. Defense in depth.

## Out of scope (deferred to other tasks)

- Creating `src/superclaude/cli/eval/pty/LICENSE` — T02.01 (NFR-MAINT1) lands the upstream LICENSE verbatim with the vendored sources.
- Creating `src/superclaude/cli/eval/pty/PROVENANCE.md` — T02.01 / T02.03 land it (T02.01 creates the file; T02.03 extends it with quarterly-review cadence and SHA pin).
- Flipping D-10 to 🟢 APPROVED — maintainer sign-off pass at M1/M2 exit (cross-references SC1, roadmap row 348).
