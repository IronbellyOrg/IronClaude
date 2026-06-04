# STUB — V3-Serena eval scaffold (FR-RV3-LOW.4, UC-2). Body fleshed out in a later iteration.
# 2 tasks: Task 1 conforms to FastAPI's Depends contract (the <ext:...> trigger → search_deps);
# Task 2 uses an un-indexed dep (FR-4.4 degrade path).

- Task 1: Add get_current_user dependency that conforms to FastAPI's Depends() contract.
- Task 2: Wire obscure_pkg.widget() into the user lookup (third-party dep, venv un-indexed).
