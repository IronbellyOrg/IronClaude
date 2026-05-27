# Refactor Plan — case 4 rerun

## Overview

- Base variant: Variant 1 (architect, parallel-run)
- Incorporated variants: Variant 2 (refactorer, hard-cutover discipline)
- Planned changes: 3
- Overall risk: Low
- Review status: auto-approved

## Planned Changes

### Change 1: Bound the parallel-run window with an explicit calendar target and accountable owner

- Source variant: Variant 2 (refactorer)
- Rationale: Variant 1's biggest risk is indefinite parallel-run. Variant 2's bounded calendar discipline directly mitigates this without changing the parallel-run model.
- Effect on merged spec: adds an explicit "end-date target + accountable owner" requirement to the Non-Functional Requirements section.

### Change 2: Adopt the concept-map doc as a permanent artifact

- Source variant: Variant 2 (refactorer)
- Rationale: pytest → vitest concept mapping is high-value and useful beyond the migration window. Keeping it in-repo as a permanent reference benefits future test authors.
- Effect on merged spec: adds a functional requirement for a committed concept-map doc.

### Change 3: Use a single config-only cutover PR pattern at the final flip

- Source variant: Variant 2 (refactorer)
- Rationale: A config-only cutover PR is small, low-risk, and revertible — strictly better than threading the cutover through a behavior PR.
- Effect on merged spec: refines the final cutover PR description in the functional requirements.
