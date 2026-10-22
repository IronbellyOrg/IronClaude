# Operator direction after Task 1 halt

The operator was asked whether to accept process-group termination plus direct-child reaping for portability, or retain the stricter cleanup requirement. Their exact answer was:

> there is absolutely no reason to overcomplicate anything in order to preserve macOS portability

Implementation interpretation: prioritize straightforward Linux-native behavior instead of adding portability machinery to preserve macOS support. Do not treat this answer as acceptance of a weakened descendant-cleanup guarantee. If Linux-specific cleanup is necessary, automated macOS support may be excluded and documented rather than driving supervision complexity.

This direction supersedes the frozen plan's macOS-portability constraint where necessary. It authorizes a correction under the changed platform direction; it is not an executor-invented Ruling line or a declaration that the already-blocked implementation is compliant. The source snapshot and original plan remain unchanged for provenance. Independent QA must consider this explicit operator direction with the source acceptance criteria.

Task 1 also has a known mypy assignment error to correct. Tasks 2–7 remain paused until the revised implementation is reviewed. The existing Q0 snapshot is retained; no duplicate start record is created.
