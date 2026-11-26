## Flag review for this issue

This issue was filed with the flags the user gave. A check at `deep` depth chose differently; the reasons are below. The issue was not reclassified.

| Flag | User's flag | Worker's choice | Reason for the difference |
|---|---|---|---|
| `--mode` | feature | feature | same |
| `--type` | cli | install | The change sits in the installer flow (`install` in `src/superclaude/cli/main.py:46`, `install_all_skills` in `src/superclaude/cli/install_skills.py:62`), and `install` is the more specific area. `cli` is also defensible: `superclaude update` shares `install_all_skills` (`main.py:401-403`). The adversarial comparison left this point unresolved, and both areas give the same issue type (Feature). |

<!-- sc:issue:create-review -->
