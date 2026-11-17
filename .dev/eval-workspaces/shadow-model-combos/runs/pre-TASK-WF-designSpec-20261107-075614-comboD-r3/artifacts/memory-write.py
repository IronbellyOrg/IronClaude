import pathlib, re
RID = "pre-TASK-WF-designSpec-20261107-075614-comboD-r3"
LP = pathlib.Path(".superclaude/memory/reflect/last-pass-brainstorm-reflect-panel.md")
DP = pathlib.Path("docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md")
last = f"""# last-pass: brainstorm-reflect-panel ({RID}, 2026-11-13)

- Run: .dev/eval-workspaces/shadow-model-combos/runs/{RID} (UC-1 pre, tier 2 pinned, engine shadow, plan TASK-WF-designSpec-20261107-075614 vs its design spec; model combination D).
- Outcome: status success. Panel sonnet/haiku/opus, 3/3 collected and 3/3 first-parse valid findings blocks, 16/16 findings calibrated, convergence 1.00 (judge unknown), evidence validator 111/111 founded 0 dropped (zero-drop flag). 16 card findings -> 17 merged (0 blocking, 2 MAJOR non-blocking, 15 MINOR).
- Decisive event: both reviewer-raised blockers (Wave 0 bullet test wording; cycle-id minted in two tasks) were downgraded to MINOR when advocates re-read plan 137 and Task 1 criterion O1. The two MEDIUM items came from the invariant probe, not the reviewers (per-cycle applied_edits source; fold cycle_id update rule).
- Identity: reviewer 3 (opus class) self-reported gpt-6-luna against its claude-opus-5-5 pin (the OPUS alias of this run); no dispatch collapse, class passed explicitly on every Agent call.

"""
dev = f"""## {RID} (UC-1, shadow panel)
- Plan-defect class (recurring, 6th+ sighting): spec items stated and carried into task prose but unasserted by any acceptance criterion: `auto_merge_armed` in engage notes, `original_is_draft` after a first skip, `--to ready` no-op, CI-fix engage case, release-failure retry, engage-failure message text, "printed once" for the off line. Same family as "constraints without matching AC do not gate".
- Spec-gap class (new): a rule the spec leaves unstated and the plan inherits (source of the per-cycle `applied_edits`; when the fold sets `cycle_id`). Only the invariant probe found these (MEDIUM, UNADDRESSED); no reviewer did. Plan audits should ask "where does this input come from" for every function argument the spec names.
- Reviewer-severity class (positive, 3rd sighting of the rule): trace the criterion's own narrowing sentence before filing a blocker. Plan 137 narrows the Wave 0 test to gate wording, so it is passable; Task 1 criterion O1 forces one minting place, so the cycle-id overlap is wording, not a second mint. Both MAJOR/blocking claims fell in debate.
- Citation-line class: reviewer 2 (haiku class) cited four spec lines that did not hold the quoted text (369, 280, 270, 268); verify-citations flagged all four mechanically before the debate; the merge replaced them (333, 234, 232). Quote-not-found is the cheap early catch.
- Corpus class: the package was already executed and its feature landed (commit 0b8a5801d, #428); attribute code claims to base e8db2fe6, and tell reviewers post-execution files are off limits. One reviewer still saw two post-execution test file names in a grep; the probe agent read working-tree code for import facts.
- Reflect mechanics: one-sentence-prompt specs give 0 Pass-1 IDs => parsed-sparse => tier 2 (this spec is a long design doc, still 0 Pass-1 IDs because it uses FR-n and F-n labels the ID regex does not match).
- Shadow-panel mechanics: 3/3 first-parse findings blocks when the dispatch prompt shows the literal heading, the opening fence line and one example line and asks for the return in a fixed order; the orchestrator copied the JSON lines verbatim. Calibrators return `per_finding` in a fenced yaml block; writing it as a bare indented mapping after the findings fence gave 16/16 calibration coverage.
- Model-identity note (combination D): the OPUS alias served gpt-6-luna and its self-report said so; the HAIKU alias served claude-haiku-5-5; the SONNET alias self-reported claude-gw-tier1b. `panel_parity` stays true because it records the class rotation, not the served model.

"""
LP.parent.mkdir(parents=True, exist_ok=True)
old = LP.read_text() if LP.exists() else ""
entries = re.split(r"(?m)^(?=# last-pass: )", old)
entries = [e for e in entries if e.strip()][:19]
LP.write_text(last + "".join(entries))
old = DP.read_text() if DP.exists() else ""
entries = re.split(r"(?m)^(?=## pre-)", old)
entries = [e for e in entries if e.strip()][:19]
DP.write_text(dev + "".join(entries))
print("last-pass entries", len(re.findall(r"(?m)^# last-pass: ", LP.read_text())), "deviation entries", len(re.findall(r"(?m)^## pre-", DP.read_text())))
