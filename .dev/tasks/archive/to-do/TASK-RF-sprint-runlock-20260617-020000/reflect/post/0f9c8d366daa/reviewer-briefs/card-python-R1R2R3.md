# Reviewer Card — python-expert (scope: R1 / R2 / R3 recovery.py correctness)

| F | Finding | file:line | Severity | Class | Conf |
|---|---------|-----------|----------|-------|------|
| F1 | fd leak + un-released lockfile if os.write raises (no try/finally) | recovery.py:329-330 | MED | latent defect/drift | 0.90 |
| F2 | R1.1 atomic acquisition + bounded retry | recovery.py:294,329-330,292 | — | COMPLIANT | 0.95 |
| F3 | R1.2 CHAIN vs "re-raise"; swallows signal + wrong exit code when _prev non-callable | recovery.py:236-241; spec:34 | MED | necessary (spec divergence) | 0.80 |
| F4 | closure capture (_prev/_lp default-arg) correct | recovery.py:236-241 | — | COMPLIANT | 0.95 |
| F5 | /proc field-22 = index 19; paren/space comm handled | recovery.py:183-185 | — | COMPLIANT (empirically verified) | 0.97 |
| F6 | PID-only degrade when starttime None | recovery.py:210-215 | — | COMPLIANT | 0.95 |
| F7 | byte-exact phase-lock message preserved (held_message=None) | recovery.py:312-315; e2e:146,148 | — | COMPLIANT | 0.97 |
| F8 | phase-lock payload grew starttime key — low risk (no strict reader) | recovery.py:282-286 | LOW | authorized | 0.85 |
| F9 | corrupt-JSON/unlink-race handled; broad OSError swallow hides EACCES diagnostic | recovery.py:302-306,321-326 | LOW | drift (cosmetic) | 0.85 |

Actionable: F1 (wrap write/close in try/finally). Adjudicate: F3 (re-raise when _prev non-callable, or document).
Strongly refutes concerns on atomicity, /proc arithmetic, closure capture, and byte-exact regression surface.
