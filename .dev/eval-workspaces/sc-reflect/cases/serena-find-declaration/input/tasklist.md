# STUB — V3-Serena eval scaffold (FR-RV3-LOW.2 + FR-RV3-LOW.3 shared, UC-2). Body fleshed out later.
# 3 tasks, one per diff hunk. The name-collision across Task 1 / Task 2 is the FR-2.4 signal;
# Task 3 is the find_declaration_no_match (FR-2.2) signal.

- Task 1: Harden auth.Validator.validate to check token.is_active().
- Task 2: Harden forms.Validator.validate to reject empty fields.
- Task 3: Add the generated __codegen_stub__ marker (no resolvable declaration).
