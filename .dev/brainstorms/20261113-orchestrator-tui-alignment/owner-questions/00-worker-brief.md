# Worker brief: owner-question debates (shared by all 7 groups)

Purpose: for each owner question, draft three genuinely different answers, debate them with `/sc:adversarial --depth quick`, and end with a final recommendation, a criticality rating, and a card a person who has never seen this project can answer from. You do NOT answer any question for the owner. You only advise.

ROOT = /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
OUT = ROOT/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions   (write only under OUT/Q<nn>/ and OUT/group-<g>-summary.md, nn = two digits: Q01..Q33)

## Sources (read what the question needs; do not invent facts, ids, paths or line numbers; mark UNVERIFIED)
- The question rows: ROOT/.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md, section 3 "Owner decisions" (lines 516 to 583): decision, recommended answer, default if unanswered, what it gates, wave. Also the "Authority not granted by these questions" list at its end.
- Work items the question gates: the same file, section 2 (per-system tables), section 4 (graph), section 5 (waves), section 6 (the coordinator session), and its Appendix "owner questions".
- Facts and original wording: ROOT/.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md ("ADJ"): glossary Part 0.3 (lines 36 to 98), Part 7 (the 24 original questions, lines 763 to 796), Parts 1 to 6 for evidence. Do not re-open findings listed as withdrawn in ADJ Part 1.3.
- Debate evidence for the question if needed: ROOT/.dev/brainstorms/20261113-orchestrator-tui-alignment/adversarial/adversarial/ (invariant-probe.md, round3-invariants-V1/V2/V3.md, diff-analysis.md).
- Project rules: ROOT/CLAUDE.md and ~/.claude/CLAUDE.md (fork-only PRs; never stage .claude/; .dev/tasks always staged; Orca-only worktrees with --agent; worker contract WC-13). Worker contract: ROOT/src/superclaude/core/WORKER-CONTRACT.md.

## Hard rules
- Read-only everywhere except your output files. No git writes, no gh writes (GET only), no Orca write verbs, nothing posted to any issue or PR.
- Question Q1 (INV-008, the git-config hole): never specify the code fix. Proposals are at the level of outcome and owner option (fix by neutralising, fix by refusing and reporting unscanned, accept with caveats). Facts measured on 2026-11-13: with git 2.47.3 the sweep's `git status` ran a command from `core.fsmonitor`, `filter.<driver>.clean`, `filter.<driver>.process`, `include.path`, per-worktree config and `GIT_CONFIG_*` variables; `-c core.fsmonitor=false` stopped only fsmonitor; a clone cannot ship config; `.gitattributes` alone ran nothing; severity judged Medium in practice on this single-owner, single-host setup.
- Do not claim the watcher-to-orchestrator handoff, an orchestrator that manages work, the #423 knowledge layer, or the TUI decision loop exists. They are unbuilt.
- Plain English everywhere in the files you write for people (final.md and card.md). No em dashes or en dashes. Every internal id (Q, INV, E-, X-, A-, SW-, OB-, WA-, CO-, V2-, XC-, W0 to W5, GRANT, TB-) gets its plain meaning in the same sentence the first time it appears in a file. No project shorthand without a gloss.

## Procedure for each question (do the questions one at a time, in order; finish one fully before starting the next)
1. Write `OUT/Q<nn>/question.md`: the question verbatim from the spec row, the spec's recommended answer, the default if unanswered, what it gates (work items glossed in words), and the facts the question depends on, each with its source.
2. Write three proposals as three files `OUT/Q<nn>/proposal-A.md`, `proposal-B.md`, `proposal-C.md`. They must be genuinely different answers an owner could reasonably pick, not one answer in three wordings. One of the three is the spec's recommended answer (reworded neutrally); one is the conservative option (do less, wait, keep the default, or decline); one is a bolder or different-shaped alternative. Randomise which letter holds which. Do not mark in the files which one the spec recommends. Each proposal file has the same sections: Answer (one or two sentences); What happens next if the owner picks it (concrete); What it unlocks; What it costs or risks; What stays unresolved. Each is the strongest honest version of itself.
3. Invoke the Skill `sc-adversarial-protocol` with: `--compare OUT/Q<nn>/proposal-A.md,OUT/Q<nn>/proposal-B.md,OUT/Q<nn>/proposal-C.md --depth quick --output OUT/Q<nn>/` (Mode A). Quick depth is Round 1 only. Follow the skill as written. If your environment cannot spawn the advocate sub-agents the skill needs, run the quick protocol inline yourself (diff the three, write each proposal's strongest case then critique the other two with evidence, score), and record `fallback_mode: true` and why in the question's final.md. Never skip the step and never present an inline run as a spawned one.
4. Write `OUT/Q<nn>/final.md` with these headings:
   - Debate result: which proposal won and the confidence (percent), whether the three advocates agreed (3 of 3, 2 of 3, split), and the evidence that decided it. Strengths and weaknesses of each proposal, one short paragraph each, with sources.
   - Final recommendation: the recommended answer in plain words, the confidence, and the single strongest reason. Say whether it equals the spec's recommended answer (yes, no, partly) and why if not.
   - What would change the answer: the one fact or event that would make another proposal better.
   - Criticality rating, using exactly this block (one value per line):
     - Security or trust boundary: none | low | high
     - Reversibility: easy | costly | irreversible
     - Who is affected: only this program | other people or repos | public or upstream
     - Needs the owner's own intent, taste or knowledge that no file holds: no | partly | yes
     - Cost if the answer is wrong: low | medium | high
     - Does it grant authority or accept a risk in writing: no | yes
     - Debate: converged | split
     - Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION or NEEDS-HUMAN
     - Reason for the suggested handling in two sentences.
     (The suggestion is advisory; the orchestrating session decides. Rule of thumb: a question is NEEDS-HUMAN if it is high on security, grants authority or accepts a risk in writing, is hard to reverse, affects other people or repos, depends on the owner's intent or taste, or the debate split. Otherwise SAFE-FOR-AGENT-RECOMMENDATION.)
   - Debate record: path to the adversarial folder, fallback_mode true or false.
5. Write `OUT/Q<nn>/card.md`: a self-contained card for a person coming in blind. Sections, in this order: Title (plain words, not the id alone); Question in one sentence; Why you are being asked (what is blocked or at risk, in plain words); Background you need (only what is necessary, every term explained inline, short); Your options (A, B, C relabelled 1, 2, 3 in the order: recommended option first), each with "If you pick this", "Upside", "Downside"; What the debate found (3 to 5 lines); Recommendation and confidence; If you do not answer (the default and its effect); What this answer does not authorize; How to answer (one line the person can type, e.g. "Q1: option 2, and yes to all channels"). Keep each card under about 70 lines.
6. Append one line for the question to `OUT/group-<g>-summary.md`: Q | winner | confidence | converged or split | suggested handling | fallback_mode.

## Final reply
Reply with ONLY: the path of your group summary file, the number of questions finished, and any question you could not finish with the reason. No file bodies.
