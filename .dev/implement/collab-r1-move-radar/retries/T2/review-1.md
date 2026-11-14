start=4166c9ee4d33606af931ae9a0455b22bef4f9f85 tree=2c0be76014b2eb522d5fbf1baf88c709dff51be1
## AC marks

- T2.AC1: unmet [F1.1].
  - sandbox.sh meets its interface. Evidence: archive from the manifest sha at `R1/tools/sandbox.sh:20`. The four leak directories are removed at `R1/tools/sandbox.sh:21`. Own git repo at `R1/tools/sandbox.sh:23`. repo.ok written at `R1/tools/sandbox.sh:24`. Candidate and source are copied at `R1/tools/sandbox.sh:27-28`. Refusal at `R1/tools/sandbox.sh:17`: I checked this live with a scratch SB whose repo.ok holds `deadbeef`. The script printed REFUSE, exited 2 and built nothing.
  - radar-index.sh breaks the `paths` contract of `DESIGN.md:52` ("repo-relative paths named in candidate.md that exist in SB/<pkg>/repo or are created by a Task"). See F1.1.
  - The other radar-index fields match `DESIGN.md:52`. Evidence: Task headings at `R1/tools/radar-index.sh:17`, grep patterns at `R1/tools/radar-index.sh:40-46`, root files at `R1/tools/radar-index.sh:48`.
- T2.AC2: met.
  - `T2.AC2@R1/tests/test_index.py:6-19` covers each T-2 check of `DESIGN.md:372`.
  - I ran `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_index.py -q` from REPO: `1 passed in 0.06s`.
- T2.AC3: met.
  - `R1/spikes/gate0.json:2` records `"G-BASE": "pass"`. The check that decides it is at `R1/spikes/gate0-check.sh:17-30`.
  - I re-checked it independently for all three sandboxes:
    - repo.ok equals each squash commit's first parent (the manifest sha).
    - `.dev/reflect`, `.dev/tasks/done`, `.dev/eval-workspaces` and `.dev/research` are all absent.
    - No directory named after the package exists under `.dev`.
    - `git status` is clean.
  - Repaired-code check of R-03: none of the src/ files that each squash commit added or modified equals its squash version (designSpec 11 checked, alias 8, design 9; 0 equal). `src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md` is absent from the designSpec sandbox, as `DESIGN.md:416` requires.

(`R1` = `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar`)

F1.1 sev=blocking trigger=B1 ac=T2.AC1 at=R1/tools/radar-index.sh:33 anchor="sandbox.sh and radar-index.sh implement the interfaces stated in DESIGN.md section 1.2" chk=y,n,n,n family=index-path-resolution fix=Try the unique-suffix match (line 34) before the parent-directory rule, and treat a token as "created by a Task" only when no existing file resolves it and the token sits inside a `## Task N:` section. Rebuild the three index files and add a shorthand-path case to the T-2 fixture and test. first=A1 origin=new covers="paths that exist in SB/<pkg>/repo or are created by a Task": The parent-directory rule runs before the suffix match. Any shorthand reference to an existing file whose first path component happens to be a root directory is therefore kept as a "created" path. The real index files contain paths that are neither in the sandbox nor created by any Task:
