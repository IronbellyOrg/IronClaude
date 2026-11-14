M1. For each file the plan edits, search `tests/`, `docs/` and the repo root for its path or key strings; open every test file the plan never names.
M2. For each sentence that says all, only, every or none, list what it quantifies over and count the exceptions.
M3. For each acceptance criterion that says every, all or complete, state the finite check that proves it; if none exists, say so.
M4. For each grep or command criterion, run it against the exact text the task tells the implementer to write, not the current file.
M5. For each mapping or decision rule, trace every input value (each reason, each mode) through to its output.
M6. For each value a consumer reads, find the producer row that writes it, in the source document, not the checkout.
M7. When you checked a claim is not too broad, check the other direction: where else in the repository (root files included) is the same claim stated?
M8. When a check fails for one task, apply the same check, clause by clause, to every other task.
M9. Compare each task body's scope with its acceptance criterion's scope and with the source document's scope.
M10. When the plan says a test enforces a rule, list what that test can actually fail on.
