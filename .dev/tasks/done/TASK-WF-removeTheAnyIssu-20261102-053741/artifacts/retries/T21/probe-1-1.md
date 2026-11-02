61710bd91a59d7ae759a5ff33d6cd3dfaeade8fb
family changelog-portify-max-convergence-claim
defect form: CHANGELOG text claims the --max-convergence flag raises the convergence cap; the flag is not wired to ConvergenceEngine.
command: git grep -n -F -e 'max-convergence' -- CHANGELOG.md
before:
CHANGELOG.md:16:- Every review-loop cap above 2 is lowered to 2 fix cycles. The prd CLI's research fix cycles default to 2; cli-portify's convergence defaults to 1 iteration (3 reviews, 2 fix passes), and `--max-convergence` can raise it.
coupled sites: src/superclaude/cli/cli_portify/commands.py:104 help text "You may raise it to allow more iterations." (Task 16 text, outside Task 21; reported to the coordinator)
after:
CHANGELOG.md:16:- Every review-loop cap above 2 is lowered to 2 fix cycles. The prd CLI's research fix cycles default to 2; cli-portify's convergence engine and its `--max-convergence` flag default to 1 iteration (3 reviews, 2 fix passes).
