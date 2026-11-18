"""Wave 3C: append the blind calibration result to each reviewer card (values copied from the calibrator reports)."""
import pathlib

O = pathlib.Path(".dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116030415")
cal = {
    1: ("opus", "0.84", dict(citation=0.90, coverage=0.65, classification=0.90, risk=0.85, actionability=0.88),
        "27 citations checked, 26 matched; R1-2 cites PSPEC:169 but the text is at PSPEC:434 and 438",
        "tasks 3 and 5 not examined"),
    2: ("opus", "0.75", dict(citation=0.85, coverage=0.55, classification=0.85, risk=0.70, actionability=0.80),
        "14 citations checked, all matched",
        "tasks 1, 4, 5 not examined; R2-1 treats the stage 0 safety-miss definition as settled although S0 marks it proposed"),
    3: ("sonnet", "0.83", dict(citation=0.92, coverage=0.65, classification=0.90, risk=0.80, actionability=0.90),
        "20+ ranges read, none contradicted; overreach: R3-3 'every point that waits', R3-6 'selects nothing', R3-1 did not examine ledger_cmd",
        "task 5 never mentioned"),
}
for n, (cls, c, d, cit, gap) in cal.items():
    p = O / "reviewer-cards" / f"reviewer-{n}-card.md"
    t = p.read_text()
    if "calibrated_confidence" in t:
        continue
    t += (f"\n\n```yaml\ncalibration:\n  calibrator_model_class: {cls}\n  calibrated_confidence: {c}\n  dimensions: {d}\n"
          f"  citation_spot_check: \"{cit}\"\n  coverage_gap: \"{gap}\"\n  inline_fallback: false\n```\n")
    p.write_text(t)
print("ok")
