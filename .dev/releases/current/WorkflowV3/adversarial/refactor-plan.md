# Refactor Plan

Base: variant-1-opus-architect.md

## Planned Changes
1. Cut `--validate` / `--parallel` to E-LEGACY (V2). Wave 4 always runs schema-min.
2. Adopt V3 STOP codes + output path guard + source.md-first.
3. `--handoff tasklist`: print `/sc:tasklist` recommendation; STOP invoke unless a real roadmap path is passed (do not treat plan.md as tasklist source).
4. Shrink refs from 8 to 5: input-parse (incl STOP), phase-templates, overlap-routing, quality-gates, return-contract. Fold dependency-model into phase-templates; fold output-template into quality-gates or SKILL output section.
5. Drop resume/ledger/deps.yaml from v3 FRs.

## Changes NOT Being Made
- Backend `--overlap` flag (routing is internal).
- Invoking implement automatically (handoff implement = Skill, but user Step 4–6 already runs implement later; default none).
- New agents.
