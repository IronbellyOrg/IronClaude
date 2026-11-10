# Research: contract tests that pin current BMAD behaviour (part 1)
**Investigation type:** Code Tracer
**Scope:** `.github/contract-tests/test-57-catalogue-configure.sh`, `test-46-catalogue-health.sh`, `test-19-catalogue-cli-presence.sh`, `test-49-spec2-evidence.sh`, `test-52-browser-usability-evidence.sh`; workflows under `.github/workflows/` that execute them
**Status:** Complete
**Date:** 2026-11-07
---

## 0. Test-list inventory (part d, early finding)

Glob of `.github/contract-tests/test-*.sh` returns files numbered from test-1 up to test-79 (for example `test-57-catalogue-configure.sh`, `test-64-orca-skills-preinstall.sh`, `test-79-create-error-tail.sh`), plus `test-b1-affordance-matrix.sh` and `test-startup-boot.sh`. Several numbers are shared by two files (test-1, test-2, test-3, test-4, test-5, test-6, test-7, test-8, test-9, test-59, test-73, test-74). Details and the discrepancy with the project index are in the section "Cross-validation (part d)" below.

## 1. test-57-catalogue-configure.sh: helpers and the whole-HOME oracle

Header facts (file lines 1-18) [CODE-VERIFIED by Read]:

| Fact | Evidence |
|---|---|
| Test proves configured state of `ironclaude` and `bmad` and reprofiled-HOME orca fixture; "bmad excluded, OD-1" for the orca-profile installers | test-57:4-11 |
| Needs `--network=none` and `--user=0`; install.sh runs as `coder` via `runuser` | test-57:11-13, 74-79 |
| "Wired into: coder-ci-aidev02-contract.yml -> contract_tests -> In-image contract tests (driver) table row (7th column: --network=none,--user=0)" | test-57:15-16 (header claim; workflow side checked in section 6) |
| Image-baked installer path is `/catalogue/<slug>/install.sh` (`CAT_ROOT="/catalogue"`) | test-57:22, 77-78; preconditions require `/catalogue/bmad/install.sh` at line 60 |

Helper definitions:

| Helper | Lines | Behaviour |
|---|---|---|
| `run_slug HOME SLUG` | 75-79 | chowns HOME to coder, then `runuser -u coder -- env -i HOME=... PATH=... LANG=C.UTF-8 bash /catalogue/<slug>/install.sh` with cwd = HOME, stdin /dev/null, output discarded |
| `record_health` | 83-95 | calls `spec2_health_record "$slug" "$probe" 0 0 5 - image-baked orca ""` from `/usr/local/lib/aidev/spec2-health.sh` in the fixture HOME, then asserts `configured_state=<expected>` and `configured_missing=<missing>` in `${home}/.aidev/status/spec2-health/<slug>.health.v1` (record_matches, lines 96-105) |
| `mk_home NAME` | 126-136 | fixture HOME `${W}/NAME` with `.claude/CLAUDE.md` copied from `/etc/skel`, a `.claude/settings.json` containing a foreign Stop hook and an orca PreToolUse hook, a git seed repo at `${H}/seed` (README.md, one commit), and `.aidev/status/seed-repo-path` pointing at it |
| `snap HOME` | 148-153 | the whole-HOME oracle (see below) |
| `seed_snap DIR` | 154-158 | same as snap but for one directory, excluding only `./.git/index` |
| `porcelain DIR` | 145 | `git -C DIR status --porcelain --untracked-files=all` |

### Part (b): exactly what `snap "${H}"` records

Code at test-57:148-153 [CODE-VERIFIED]:

1. `find . ! -path '*/.git/index' ! -path './.aidev/installed/*' -printf '%y %p %l\n' | sort`: every path under HOME (any depth: files, dirs, symlinks) with type letter and link target, EXCLUDING any `.git/index` and everything under `./.aidev/installed/` (marker files carry a timestamp; comment at lines 146-147).
2. `find . -type f ! -path '*/.git/index' ! -path './.aidev/installed/*' -print0 | sort -z | xargs -0 -r sha256sum`: a content hash of every regular file with the same two exclusions.
3. `cat ./.aidev/installed/*.configured`: the content of any `.configured` marker (kept deliberately, comment line 147).

Because `mk_home` puts the seed repo at `${H}/seed` (test-57:134), the HOME snapshot ALSO covers the seed repo tree (`${H}/seed/**`, including `.git/` internals except `index`). Fixture-created paths in HOME: `.claude/`, `.aidev/status`, `.aidev/installed`, `seed/` (test-57:129-135).

Consequence for the options (derived from the snapshot definition above; nothing was run):

| Write location | Inside `snap "${H}"`? | Reason |
|---|---|---|
| anything under `$HOME` other than `$HOME/.aidev/installed/*` (for example `~/.claude/skills/...`, `~/.claude/settings.json`, `~/.claude/commands/...`, `~/_bmad`, `~/.bmad`) | YES: any new path or changed hash breaks `test "$(snap "${H}")" = "${want}"` | find has no other exclusion |
| `$HOME/.aidev/installed/bmad` (marker) | NO, excluded | `! -path './.aidev/installed/*'` |
| `$HOME/.aidev/installed/*.configured` | content only is recorded (line 152); path excluded from the lists | lines 150-152 |
| anywhere inside `${H}/seed` (for example `seed/_bmad/`, `seed/.claude/skills/bmad-*`) | YES (seed is under HOME), except `seed/.git/index` | mk_home line 134 |
| image-level paths outside HOME (`/usr/local/bin`, `/etc`, `/catalogue`, `/opt`) | NO (not under HOME) | find starts at `.` of HOME |

Key Takeaways (section 1):
- `snap` is a strict whole-HOME comparison; any option that makes `/catalogue/bmad/install.sh` write a new file under HOME (B, D if it writes state, E, F) breaks the no-seed assertion unless the snapshot is amended.
- Options A and C (document only; image-level CLI wrapper outside HOME) do not alter the snapshot at install time. Option C could write into HOME only when the user later runs `bmad`, which this test never does.

## 2. test-57: the BMAD assertions (part a rows, test-57)

Sources read: lines 173-183, 300-349, 395-474 [CODE-VERIFIED]. IMPORTANT fixture semantics: in test-57 "seed" means the git seed repo recorded in `~/.aidev/status/seed-repo-path` (created by `mk_home`, test-57:134-135); the current `bmad` installer configures THAT repo (writes `<seed>/_bmad/_config/manifest.yaml`, test-57:323, 458). "no seed" means the seed-repo-path file is removed (test-57:447), i.e. the case with no repo to configure. This is the exact analogue of "a project that never had BMAD" only when no seed repo is registered.

| Test file | Line | Assertion text | What it pins | Options that would break it | Replacement assertion |
|---|---|---|---|---|---|
| test-57 | 173-178 | loop `for slug in bmad ironclaude` ... `expect_rc "first (cold) run ${slug}" 0` | exit 0 of `bmad` cold run in the seeded HOME; feeds the FR-21 30 s budget | None of A-F by themselves; B/D/E/F add runtime to the bmad cold run and count against `BUDGET_MS=30000` (line 31, check at 179-183) | unchanged, unless the option adds measurable time (then re-measure the two-step total) |
| test-57 | 179-183 | `FR-21 proxy: first-run two-step total ${total} ms <= ${BUDGET_MS} ms` | cold-run timing of bmad + ironclaude (sum of the two) | E (a real `bmad install` would need network/npm and write far more; test runs `--network=none`) and F; possibly B/D if install.sh does more work | same assertion; E/F cannot run offline so the install must stay out of install.sh |
| test-57 | 323 | `bmad: <seed>/_bmad/_config/manifest.yaml exists` | seeded configure: install.sh writes the manifest into the seed repo | none of A-F, as long as the existing seed-repo configure is kept | unchanged |
| test-57 | 324 | `bmad: clean seed git status stays empty` (`test -z "$(porcelain "${H}/seed")"`) | seed guard: new `_bmad` content must be git-ignored/excluded so the seed repo stays clean | any option that writes tracked/untracked non-excluded files into the seed repo (E if run against the seed; F) | unchanged for A, B, C, D; for E/F add the exclude rule or assert the new paths are excluded |
| test-57 | 327-329 | `all: ${slug} marker written` (`test -f "${H}/.aidev/installed/${slug}"`) | marker for bmad exists after run 1 | none of A-F | unchanged |
| test-57 | 331-335 | `before="$(snap "${H}")"` then second run; `all: second run leaves owned files byte-identical` | idempotence of the second run of bmad (and ironclaude) in a seeded HOME, whole-HOME snapshot | B (if the second run rewrites the skill file with different bytes or timestamps-in-content), D (if the hook is rewritten), E, F (non-idempotent writes) | unchanged; the new writer must be byte-idempotent, or the replacement is the same snapshot comparison with the new file included in the stable set |
| test-57 | 340-342 | `record_health "configured positive ${slug}" "${H}" "${slug}" healthy Configured` | health state: after install, `bmad` reports `configured_state=Configured` | A-F only if they change how Configured is computed (see test-46 and the probe in the manifest) | unchanged |
| test-57 | 413-419 | `expect_rc "seed with _bmad/: bmad exits 0"`; `seed with _bmad/: repo and info/exclude byte-unchanged` (`seed_snap` equality); `record_health "bare _bmad is not configured" ... Installed-not-Configured` | seed guard: an existing user `_bmad/` (just a `keep` file) in the seed makes the installer leave the repo and `.git/info/exclude` byte-identical, and health is Installed-not-Configured | any option whose install.sh writes inside the seed when `_bmad/` already exists (E, F); B/D do not touch the seed | unchanged for A-D; for E/F the guard must still hold |
| test-57 | 421-427 | `seed tracking .claude/skills/bmad-*: bmad exits 0`; `repo byte-unchanged`; `record_health "tracked BMad skills configure seed" ... Configured` | health state: tracked `.claude/skills/bmad-*` in the seed means Configured, and the installer must not change the repo | B (if the new skill lives in `~/.claude/skills/bmad-*` it is NOT in the seed, so no break; if B instead writes `bmad-*` skills into the seed it would change the repo) | unchanged for A-D; if B/F make "Configured" depend on a user-level skill, add a second `record_health` case for it |
| test-57 | 429-435 | `non-Git seed with manifest: marker written`; `record_health "non-Git seed manifest is not configured" ... Installed-not-Configured` | health state: a manifest in a non-git seed is not Configured | only options that change the Configured rule | unchanged |
| test-57 | 437-444 | `tracked but deleted BMad skill: marker written`; `record_health "deleted tracked BMad skill is not configured" ... Installed-not-Configured` | health state: tracked-but-deleted skill is not Configured | only options that change the Configured rule | unchanged |
| test-57 | 446-448 | `mk_home no-seed`; `rm -f "${H}/.aidev/status/seed-repo-path"`; `want="$(snap "${H}")"` | fixture for the no-seed oracle: HOME with no seed-repo-path | n/a (fixture) | n/a |
| test-57 | 449 | `expect_rc "no seed: bmad exits 0" 0 "${H}" bmad` | exit code 0 when there is no seed | none | unchanged |
| test-57 | 450 | `no seed: bmad writes nothing` (`test "$(snap "${H}")" = "${want}"`) | THE OD-1 pin: with no seed, `/catalogue/bmad/install.sh` creates, changes or deletes nothing under HOME other than `.aidev/installed/*` | B (writes `~/.claude/skills/<new>` inside HOME), D (writes `~/.claude/settings.json` or `~/.claude/hooks/*`), E (`bmad install --directory ~` writes `~/_bmad`, `~/.claude/skills/bmad-*`), F (user-scope install writes under `~` via `global_target_dir`). A and C do not break it (C only if the wrapper is invoked from install.sh and writes into HOME at install time; it is image-level and outside HOME) | If the user-level artifact is written by the install.sh: rename to `no seed: bmad writes only <path list>` and compare `snap` minus a fixed allow-list (or compare against `want` plus an exact expected delta, for example one added file `./.claude/skills/<name>/SKILL.md` with a pinned hash). If the artifact is image-level or created at first use (A, C): keep unchanged |
| test-57 | 451 | `no seed: bmad marker still exists` (`test -f "${H}/.aidev/installed/bmad"`) | marker | none of A-F | unchanged |
| test-57 | 452 | `record_health "seedless BMad marker is not configured" ... bmad healthy Installed-not-Configured` | health state: a seedless HOME stays Installed-not-Configured | B/D/E/F if they cause the probe to see something configured in HOME (depends on the probe; see test-46 section and manifest), otherwise none | keep for A/C; for B/D/E/F decide whether a user-level bootstrap counts as Configured; if not, unchanged; if so, `Configured` with the new missing list |
| test-57 | 454-459 | `dirty seed: bmad configures` ... `dirty seed: git status delta empty` | seed guard on a dirty seed: no new status entries | E/F if they write non-excluded paths into the seed | unchanged for A-D |
| test-57 | 462-465 | `seed with untracked _bmad-output/: user file kept` | seed guard: a user `_bmad-output/prior.md` survives | E/F if they delete or move user output | unchanged |

Key Takeaways (section 2):
- Exactly ONE assertion pins "no seed: bmad writes nothing": test-57:450 (fixture 446-448, rc at 449, marker at 451, health at 452).
- The seeded behaviour is already richer than the research question assumes: the existing installer DOES create `_bmad/_config/manifest.yaml` in a registered seed repo (test-57:323, 458). The OD-1 pin concerns only the case where no seed-repo path exists.

### 2.1 Source-of-truth cross-check for test-57 (installer and health rule) [CODE-VERIFIED]

| Claim | Source |
|---|---|
| With no seed recorded, install.sh prints `no seed repo recorded; nothing to configure`, writes only the marker `~/.aidev/installed/bmad`, and exits 0 | `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:21-23, 57-61` |
| With a seed repo and no `_bmad/` and no tracked `.claude/skills/bmad-*`, it appends `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` to the repo's `info/exclude`, runs `NPM_CONFIG_OFFLINE=true timeout 120 bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output --user-name ...`, requires `_bmad/_config/manifest.yaml`, and fails if git status changed | install.sh:24-55 (install command at line 42) |
| bmad has `scope: hybrid`, `install_disposition: image-baked`, `health_check.command: bmad --version` | `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:2-4, 24-25` |
| The "Configured" requirement for bmad is the single token `seed-config` | `templates/VSCode-AIDev02/image/scripts/lib/spec2-health.sh:77` |
| `seed-config` is observed ONLY via the seed repo recorded in `~/.aidev/status/seed-repo-path`: `<seed>/_bmad/_config/manifest.yaml` exists, or a tracked `.claude/skills/bmad-*/SKILL.md` file exists in that git repo | spec2-health.sh:99-113 |
| Readiness derivation hard-codes bmad as `not-selected` when deselected; the reprofile report reader rejects any `bmad` row | spec2-health.sh:562 (readiness) and 516-529 (reader, `slug == "bmad"` is bad) |
| The orca profile lists bmad: `slugs: [claude-code, orca, ironclaude, bmad, mcp-bundle-core]` | `templates/VSCode-AIDev02/image/catalogue/profiles.yaml:18` |

Consequence: a user-level bootstrap (option B or D) or an image-level wrapper (option C) leaves `spec2_health_observed bmad` unchanged. A seedless HOME therefore stays `Installed-not-Configured` (test-57:452) unless the owner also changes spec2-health.sh:99-113. Options E and F write a real `_bmad` tree outside the seed repo, so they also do not flip health unless spec2-health.sh is changed.

## 3. test-46-catalogue-health.sh: BMAD hits

Sources read: lines 833-960, 1085-1200, 1266-1325, 1412-1503, 1730-1850 [CODE-VERIFIED]. Variables: `STARTUP_SH`, `HEALTH_LIB`, `CATALOGUE_DIR` are repo paths (test-46:20-22), so this test runs from the repo checkout against `templates/VSCode-AIDev02/image/...`, not against `/catalogue` in the built image. Every `bmad` directory used in the behaviour fixtures is a SYNTHETIC fixture: its `install.sh` only writes a marker (test-46:849-859, 1136-1142, 1284-1288) and its probe is `exit 0`. The only place test-46 touches the REAL bmad manifest is the marker-proxy scan (lines 1804-1815). So test-46 pins reprofile and readiness semantics for the slug name `bmad` plus one manifest-shape rule; it does NOT pin what the real bmad install.sh writes.

| Test file | Line | Assertion text | What it pins | Options that would break it | Replacement assertion |
|---|---|---|---|---|---|
| test-46 | 847-859 | fixture `profiles.yaml` `orca: slugs: [hc-keep, orca, hc-drop, bmad]` and synthetic `bmad` dir with marker-writing install.sh | fixture setup for the reprofile run | none | none |
| test-46 | 904-908 | `reprofile sub-check: selected boot installs all slugs and publishes a row-less current report` (bmad marker `${rp_inst}/bmad` must exist, line 905) | marker: a selected bmad slug gets its marker; report has no rows | none | none |
| test-46 | 922, 929-933 | `reprofile sub-check: deselection removes exactly orca/hc-drop markers and side markers; bmad marker untouched` (`bmad.side` kept, sha256 of `bmad` marker equal to `rp_bmad`) | reprofile deselection never removes the bmad marker or its side marker (OD-1 "BMad is never removed on deselection") | an option that makes the reprofile/deselect path clean up a user-level BMAD artifact (B or D with a removal rule for `bmad`); also any option that changes `reprofile_*` in spec2-health.sh | none for A, C, E, F. For B/D: keep this assertion as is (the new artifact must also survive deselection) and add a second assertion that the user-level artifact is byte-identical after deselection |
| test-46 | 937-943 | `reprofile sub-check: current report lists deselected non-BMad slugs (...)`; expected rows only `hc-drop` and `orca`, no `bmad` row | the report has no bmad row | an option that adds a bmad leftover/removed row | unchanged |
| test-46 | 947-958 | loop `for slug in bmad hc-drop orca` and `reprofile sub-check: no installer/probe/health/welcome for deselected slugs; user data byte-identical ...` | for a deselected bmad: no health record, no welcome file, installer ran exactly once (`rp_ran` = 1) | an option that makes deselected bmad re-run an installer or write welcome | unchanged |
| test-46 | 1092-1118 | strict reader: `{ cat report-b; rp_row bmad absent none; } > r-bmad` must be rejected (line 1105); pass message `reprofile sub-check: strict reader accepts the current report and rejects stale/malformed/duplicate/bmad/extra/symlink/absent` | the reprofile report reader rejects a bmad row (spec2-health.sh:529) | an option that lets reprofile manage BMAD (would need the reader to accept a bmad row) | invert only if reprofile ever manages bmad: accept `bmad` row; not needed for A-F |
| test-46 | 1134-1135, 1136-1142 | fixture `orca: slugs: [claude-code, orca, hc-drop, ironclaude, bmad]` and synthetic bmad dir | fixture setup | none | none |
| test-46 | 1167 | `ai-pair -> orca sub-check: ai-pair boot installs its three slugs and writes boot-1 records; report rows exactly hc-drop/orca absent (no bmad row)` | the ai-pair boot has no bmad row; orca boot likewise | an option that adds bmad to `ai-pair-programming` or alters rows | unchanged |
| test-46 | 1184-1197 | loop `for slug in bmad claude-code hc-drop ironclaude orca`: every record `state=healthy` with the orca boot invocation id; only claude-code and orca must classify `Configured` (`record_config_ok`, lines 1189-1191) | health state: fixture bmad is `healthy` after an orca boot; it is NOT required to be Configured here | an option that makes bmad fail its probe (`bmad --version`) in the fixture; fixture probe is `exit 0` so no real break | unchanged |
| test-46 | 1284-1288, 1297-1298, 1303-1307 | readiness fixture: bmad dir exists but is NOT in the profile `rd` slugs; expected row `bmad not-selected`; pass message `readiness sub-check: failed/missing-manifest slugs listed non-Configured, project not-applicable, rd-out not-selected matching reprofile.v1, bmad not-selected` | readiness hard-codes deselected `bmad` as `not-selected` even without a reprofile row (spec2-health.sh:562) | an option that makes bmad participate in readiness as a normal slug (changing line 562) | unchanged for A-F |
| test-46 | 1317-1318 | unresolved profile: `rd_rows bmad unknown ...` | readiness for bmad under an unresolved profile is `unknown` | none | unchanged |
| test-46 | 1419, 1437-1446 | direct writer cases `bmad deselected` -> `bmad not-selected` (twice) | same rule as above, at the writer level | same as above | unchanged |
| test-46 | 1479-1499 | `summary sub-check: readiness_summary names non-Configured slugs (bmad included), all/vacuous wording...`; expected string `Catalogue not configured: bmad,rd-u,rd-z` (line 1491, 1497) | the one-line catalogue summary lists a non-Configured `bmad` by name | an option that changes the summary wording for bmad (for example a first-use message) | update the expected string if the wording changes; otherwise unchanged |
| test-46 | 1804-1815 and 1833 | marker-proxy production scan: for every real `${CATALOGUE_DIR}/*/manifest.yaml` (except `test-slug`, `vibe-kanban`) `yq '.health_check.command'` must not be marker-proxy-shaped (regex at lines 1785, 1789, 1792; self-test line 1833 `mp_is_marker_proxy 'bmad --version'` must return not-proxy) | CLI presence / health probe shape: bmad `health_check.command` is `bmad --version` and must not use `test -f`, `[ -e ]`, `stat`, `ls` or mention `.aidev/installed` | an option that replaces the probe with a file check (for example `test -d ~/.claude/skills/bmad-...` for B or D) | keep unchanged: a user-level artifact must NOT be probed with a file-existence command. If a probe is wanted, it must execute the CLI (`bmad --version`) as today |

Key Takeaways (section 3):
- No test-46 assertion pins the real bmad install.sh output; they pin the slug-name rules (bmad never removed on deselect, never in reprofile rows, `not-selected` in readiness) and the probe shape.
- The only test-46 assertion that reads real production files is the marker-proxy scan (test-46:1804-1815), which will fail for any new bmad probe that is a file-existence check.
- The count `mp_expected` comes from `profiles.yaml` (test-46:1801-1803), so adding a new catalogue slug for a bootstrap changes `mp_scanned` and `mp_expected` equally; no break unless the new slug has no manifest.

## 4. test-19-catalogue-cli-presence.sh: BMAD-relevant assertions

Sources read: lines 1-60, 170-230, 496-575, 730-840, 1088-1262 [CODE-VERIFIED]. The five literal `bmad` hits are: header provenance (line 11), a comment explaining why the classifier strips quoted text (200), the ECHO-VERB self-test comment (743, 746) and a `first_token '  bmad   --version '` self-test (820). The real bmad slug is exercised by the production scan, not by literal `bmad` strings: the loop over `manifests` (line 1095) reads the real `bmad/manifest.yaml` and `bmad/install.sh` via `CATALOGUE_DIR` (default repo path, line 24; in CI `CATALOGUE_DIR=/catalogue-src`, workflow:1234).

| Test file | Line | Assertion text | What it pins | Options that would break it | Replacement assertion |
|---|---|---|---|---|---|
| test-19 | 1106-1114 | `install_disposition ${declaration} - failing closed before routing` | bmad manifest must declare `install_disposition` as `image-baked` or `runtime-network` (currently `image-baked`, manifest.yaml:4) | none | unchanged |
| test-19 | 1137-1152 | `slug 'bmad': definite disposition contradiction declared=image-baked, advisory-vector=RUNTIME` | CLI presence / seed guard on the installer SHAPE: `classify_install_vector` (lines 192-220) must return IMAGE_BAKED for `bmad/install.sh`. That requires a `command -v` token AND `exit 2` in the comment-and-quote-stripped text and NO unquoted install verb (regex at line 208-209: `npm install/i/add`, `pnpm install/add`, `yarn add`, `npx `, `pipx install`, `pip install`, `apt install`, `cargo install`, `go install`, `uv tool/pip install`, `curl|wget ... | sh`). Current install.sh has `command -v bmad` and `exit 2` on line 18 and its `npm install -g` text sits inside a quoted echo (stripped) | B: if the bootstrap-writing code added to `bmad/install.sh` contains an unquoted install verb, or a multi-line heredoc that spells `npx ` or `npm install` (the quote strip works per line only, line 205), the vector flips to RUNTIME and the scan FAILS with CONTRADICTION. C: not affected (wrapper lives in Dockerfile.coder, not in install.sh). D, E, F: E and F are fine only if the call stays `bmad install ...` (not matched by the regex); a call like `npx bmad-method install` WOULD flip it | unchanged. If the option needs a real install verb, the manifest would have to declare `runtime-network`, which then removes the on-image `bmad --version` check (line 1161-1166) and is NOT recommended |
| test-19 | 1175-1185 | `slug 'bmad': declared image-baked CLI 'bmad' NOT on PATH` / `resolves only as a shell builtin/function/alias` | CLI presence: `type -P bmad` must return an executable FILE on PATH inside the built image | C (a bash function or alias instead of a file would fail with BUILTIN_NOT_FILE; a replaced wrapper must remain an executable file named `bmad` on the default PATH) | unchanged; keep `/usr/local/bin/bmad` an executable file |
| test-19 | 1186-1190 | `slug 'bmad': 'bmad' present at <path> but 'bmad --version' exit != 0` | CLI presence: `bmad --version` exits 0 non-interactively, with no network and no prompt, run as the image user without `NPM_CONFIG_OFFLINE` | C (a wrapper that bootstraps on every invocation, prompts, or needs network/cwd state could make `--version` fail or hang) | unchanged; the wrapper must pass `--version` straight through |
| test-19 | 517-529 | `welcome_message does NOT contain declared invocation 'bmad'` and `... declared help_command 'bmad --help'` (oq1-welcome, oq1-welcome-help) | the bmad `welcome_message` must contain the tokens `bmad` and `bmad --help` (manifest.yaml:17-18 has both) | A and B (if the welcome text is rewritten to describe the new first-use path and drops `bmad --help`), plus any text rewrite | unchanged; any rewritten welcome_message must keep the literal strings `bmad` and `bmad --help` |
| test-19 | 545-550 | `declared invocation 'bmad' does not resolve to an executable file on PATH` (invocation-resolve) | invocation resolves as a PATH executable | C (same as 1175-1185) | unchanged |
| test-19 | 551-561 | `declared help_command 'bmad --help' did not exit 0 non-interactively within 10s` (help-exec): runs `timeout 10s bmad --help </dev/null` | `bmad --help` exits 0 in 10 s with stdin closed | C (wrapper that prompts, installs or needs a project dir on `--help`) | unchanged |
| test-19 | 496-505 | `invocation '...' is a marker/path proxy` / `help_command '...' references a marker/path proxy` | `discoverability.invocation` (`bmad`) and `help_command` (`bmad --help`) must be canonical on-PATH commands, not marker or path shapes | an option that moves the discoverability invocation to a skill path or a marker (for example `~/.claude/skills/...`) | unchanged: keep `invocation: bmad` and `help_command: bmad --help` |
| test-19 | 818-821 | self-test `first_token '  bmad   --version '` = `bmad` | parser self-test using a bmad-shaped string; no repo state | none | none |
| test-19 | 743-753, 760 | ECHO-VERB fixture (synthetic `qux`) must classify IMAGE_BAKED | classifier self-test; the comment names bmad as the origin of the regression | none (synthetic) | none |

Key Takeaways (section 4):
- test-19 never inspects what bmad `install.sh` WRITES; it pins (1) the manifest declaration, (2) the install.sh SHAPE (`command -v` + `exit 2`, no unquoted install verb), (3) `bmad` and `bmad --version` and `bmad --help` working on the built image, (4) the welcome text tokens.
- The only fragile item for option B/D/E/F is the install.sh shape rule at test-19:1137-1152 (and its regex at 208-209); the only fragile item for option C is items (3).
- `bmad` on the image is ALREADY a shell wrapper script, not a symlink: `Dockerfile.coder:133-143` writes `/usr/local/bin/bmad` as `#!/bin/sh` + `exec "<node>" "<cli>" "$@"` [CODE-VERIFIED]. Option C therefore modifies an existing wrapper; test-19 demands only that it stays an executable file passing `--version` and `--help`.

## 5. test-49-spec2-evidence.sh: one bmad hit (file inventory pin)

Sources read: lines 1-40, 270-416 [CODE-VERIFIED]. The single hit is line 310 inside the array `SPEC2_CHANGED_SURFACES` (lines 294-322): `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml`. `one_lifecycle_scan` (lines 345-404) is called at line 647.

| Test file | Line | Assertion text | What it pins | Options that would break it | Replacement assertion |
|---|---|---|---|---|---|
| test-49 | 349-354 | `SCAN-REJECT: listed Spec-2 changed surface missing: <rel>` for the listed `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml` | the bmad manifest file must exist at that exact path (fail-closed inventory) | any option that renames, moves or deletes `bmad/manifest.yaml` | edit `SPEC2_CHANGED_SURFACES` line 310 to the new path |
| test-49 | 355-399, regex at 326 | `SCAN-REJECT: <rel>:<line> unexplained lifecycle-producer shape on a Spec-2 changed surface: <text>` | the bmad manifest (and also `Dockerfile.coder` line 308, `startup.sh` line 321, `spec2-health.sh` line 320, `aienv.skel` line 309, `coder-ci-aidev02-contract.yml` line 306, all listed in the same array) must contain no NON-COMMENT line matching `coder create`, `coder templates push`, `coder delete`, `docker build`/`docker buildx build`, or `terraform apply` | A or B (a welcome message or doc text in `bmad/manifest.yaml` that tells the user to run `docker build`/`coder create`: unlikely); C (Dockerfile.coder: new non-comment line with `docker build` text; the workflow may hold exactly ONE `docker buildx build` line, lines 383-393); D (aienv.skel / startup.sh edits with such text) | unchanged; avoid those strings in non-comment lines of the listed files, or add an allowance only with owner agreement |
| test-49 | 294-322 | note: `bmad/install.sh` is NOT in the list; only `bmad/manifest.yaml` is | an install.sh change in the bmad dir is not scanned | none | none |

Current state check: a Grep count for the five lifecycle patterns in `bmad/manifest.yaml` returned 0 matches [CODE-VERIFIED], so the file passes today.

Key Takeaways (section 5):
- test-49 is a path-existence and forbidden-string pin, not a behaviour pin. It breaks only if `bmad/manifest.yaml` moves or gains lifecycle-command text.
- The array is also the list that any edit to `Dockerfile.coder`, `startup.sh`, `spec2-health.sh` and `aienv.skel` (options C, D, and any health change) must keep free of those five command patterns outside comments.

## 6. test-52-browser-usability-evidence.sh: one bmad hit (profile mapping pin)

Sources read: lines 1-30, 1360-1410 [CODE-VERIFIED]. The single hit, line 1382, sits in a Node fixture block that starts at line 798 (`node --input-type=module - "$REPO_ROOT" <<'ORCA_FIXTURES'`). It reads the real `templates/VSCode-AIDev02/image/catalogue/profiles.yaml` (line 1378) and asserts:

| Test file | Line | Assertion text | What it pins | Options that would break it | Replacement assertion |
|---|---|---|---|---|---|
| test-52 | 1378-1383 | `assert.deepEqual(mappings, { orca: ['claude-code', 'orca', 'ironclaude', 'bmad', 'mcp-bundle-core'], minimal: ['claude-code'] })` | exact profile-to-slug mapping in `profiles.yaml`: two profiles, `orca` with those five slugs in that order, `minimal` with `claude-code` only; the regex needs each profile to have `label:` then `slugs: [...]` on consecutive lines | any option that adds a new catalogue slug to a profile (for example B implemented as a separate slug `bmad-bootstrap`), removes `bmad` from `orca`, or reorders slugs | update the expected object at line 1381-1383 to include the new slug in position |
| test-52 | 1384 | `assert.match(profiles, /^default_profile: orca\s/m)` | default profile is `orca` | none | unchanged |

Current profiles.yaml (grep) [CODE-VERIFIED]: line 14 `default_profile: orca`, line 17-18 `label: "Default"` + `slugs: [claude-code, orca, ironclaude, bmad, mcp-bundle-core]`, lines 20-21 `label: "Minimal (Claude Code only)"` + `slugs: [claude-code]`.

Key Takeaways (section 6):
- test-52:1381-1383 is the only pin that breaks when a NEW slug joins a profile. Options that stay inside the existing `bmad` slug (A, B inside install.sh, C, D inside install.sh, E, F) do not touch it.
- test-52 runs runner-native before the image build (workflow:832-847), so it fails fast in PR CI before the image is built.

## 7. Consolidated option-impact matrix (derived from sections 1-6)

Legend: X = breaks for certain if the option is implemented as described in the research question; c = breaks only under the stated condition; - = does not touch it. The write locations of options E and F come from the question's wording (`bmad install --directory ~`; upstream `global_target_dir`), not from BMAD source: [UNVERIFIED] (I was limited to `bmad --version/--help` style commands and did not run any).

| Pinned assertion | File:line | A doc only | B user-level skill via bmad install.sh | C image CLI wrapper | D user-level hook | E install --directory ~ | F upstream user-scope install |
|---|---|---|---|---|---|---|---|
| No-seed whole-HOME snapshot ("no seed: bmad writes nothing") | test-57:450 | - | X (any new file under `~/.claude/skills/`) | - | X (any write to `~/.claude/settings.json` or `~/.claude/hooks/`) | X | X |
| Second run byte-identical (whole-HOME snapshot, seeded HOME) | test-57:331-335 | - | c (artifact must be byte-idempotent) | - | c (settings.json rewrite must be idempotent) | c | c |
| Cold-run timing budget 30 s for bmad + ironclaude | test-57:179-183 | - | c (small) | - | c (small) | c (large install) | c (large install) |
| Seedless health stays Installed-not-Configured | test-57:452 | - | - (health reads only the seed; spec2-health.sh:99-113) | - | - | - | - |
| Seed guards (no new git status, `_bmad` present untouched, user output kept) | test-57:324, 418, 426, 459, 465 | - | - | - | - | c (only if the install targets the seed) | c |
| install.sh shape stays IMAGE_BAKED (no unquoted install verb, keeps `command -v` + `exit 2`) | test-19:1137-1152, classifier 192-220 | - | c (any heredoc or command text with `npm install`, `npx `, `pip install` etc.) | - | c | c (if written as `npx ...`) | c |
| `bmad` is an executable file on PATH; `bmad --version` and `bmad --help` exit 0 non-interactively | test-19:1175-1190, 545-561 | - | - | c (wrapper behaviour) | - | - | - |
| Seeded install still works through the wrapper (`bmad install` is run by install.sh:42) | test-57:323, 458 | - | - | c | - | - | - |
| Welcome text keeps tokens `bmad` and `bmad --help` | test-19:517-529 | c (if welcome_message is rewritten) | c | - | c | c | c |
| Discoverability invocation/help are canonical commands (not markers/paths) | test-19:496-505 | - | c (if invocation moved to a skill path) | - | c | - | - |
| Probe `health_check.command` not a file check | test-46:1804-1815 | - | c (if a file-exists probe is added for the skill) | - | c (same) | c | c |
| Deselection leaves bmad marker and side marker untouched; no bmad row in reprofile report | test-46:929-933, 937-943, 1092-1118 | - | c (only with a removal rule for bmad) | - | c | - | - |
| Readiness `bmad not-selected` / summary string `Catalogue not configured: bmad,...` | test-46:1297-1298, 1317-1318, 1437-1446, 1479-1499 | - | c (only if health wording or rule changes) | - | c | c | c |
| bmad manifest path present; no lifecycle-command text in non-comment lines of the listed files | test-49:294-322, 349-399 | c (manifest edit) | c (manifest edit) | c (`Dockerfile.coder` edit) | c (`aienv.skel`, `startup.sh`, `spec2-health.sh` edits) | - | - |
| profiles.yaml mapping exactly `orca` = 5 slugs, `minimal` = `claude-code` | test-52:1378-1384 | - | c (only if a NEW slug is created) | - | c (only if a new slug) | - | - |
| Not in assigned scope: `test-startup-boot.sh` bmad readiness and MOTD strings | test-startup-boot.sh:233, 1099-1137 | - | c [UNVERIFIED] | - | c [UNVERIFIED] | c [UNVERIFIED] | c [UNVERIFIED] |

Additional observations for option D (derived from test-57 source, not run):
- `ic_hooks` (test-57:140) is true for ANY hook command containing `/.claude/hooks/`. Because the run order is bmad then ironclaude (test-57:173), a bmad hook registered under `~/.claude/hooks/` would make the ironclaude assertion at test-57:187 and :407 pass for the wrong reason (a weakening, not a failure). The self-heal fixture (test-57:368-372) deletes every `/.claude/hooks/` entry, so a bmad hook there would be removed and not restored by the ironclaude re-run (test-57:376 still passes because ironclaude re-adds its own).
- Any rewrite of `~/.claude/settings.json` by the bmad installer is inside the whole-HOME snapshot and must preserve the foreign Stop hook, the orca PreToolUse hook and `deniedMcpServers` (assertions test-57:325-326, 337, 364-365, 373, 379).

## 8. Part (c): which workflow and job runs each test

All five tests are run by ONE workflow: `.github/workflows/coder-ci-aidev02-contract.yml` (name "AIDev02 Contract Tests", line 3), job `contract_tests` (display name "AIDev02 contract tests (dind-sidecar)", workflow:492-493), `runs-on: [self-hosted, big]` by default (workflow:498), `timeout-minutes: 20` (workflow:500). [CODE-VERIFIED] by Read and Grep. Triggers (workflow:5-60): pull_request when paths match `templates/VSCode-AIDev02/**`, `templates/VSCode-AIDev02/image/catalogue/**`, `.github/contract-tests/**` and others; push to `main` with no path filter; nightly cron `17 5 * * *`; `workflow_call`; `workflow_dispatch`. Any option that edits files under `templates/VSCode-AIDev02/` or `.github/contract-tests/` therefore triggers the whole gate on its PR.

| Test | Workflow step | Workflow line | How it is run | Needs the built image? |
|---|---|---|---|---|
| test-57-catalogue-configure.sh | step "In-image contract tests (driver)", table row | `coder-ci-aidev02-contract.yml:1241` | `docker run --rm --network=none --user=0 -v <contract-tests>:/contract-tests:ro --entrypoint bash $IMAGE_TAG /contract-tests/test-57-catalogue-configure.sh`, stderr merged, log `artifacts/test-57-catalogue-configure.log` (7th column `--network=none,--user=0`, parsed at workflow:1212-1213) | YES: it runs the image-baked `/catalogue/<slug>/install.sh`, `/usr/local/lib/aidev/spec2-health.sh`, `/etc/aidev02/ironclaude-provenance`, `/usr/bin/orca-ide` and the image `bmad`/`superclaude` binaries (preconditions test-57:59-63). Not runnable standalone on a host |
| test-46-catalogue-health.sh | same step, table row | `coder-ci-aidev02-contract.yml:1237` | `docker run --rm -v /repo:ro,-v evidence ... -e REPO_ROOT=/repo,RESULT_FILE=/evidence/health.txt` inside the image, stderr merged | PARTIAL: it executes inside the built image container (so image tools such as `yq` and `jq` must exist) but the files under test come from the `/repo` mount (`STARTUP_SH`, `HEALTH_LIB`, `CATALOGUE_DIR`, test-46:20-22). It can also run on a host checkout |
| test-19-catalogue-cli-presence.sh | same step, table row | `coder-ci-aidev02-contract.yml:1234` | `docker run ... -v /catalogue-src:ro -e CATALOGUE_DIR=/catalogue-src,EVIDENCE_DIR=/evidence`, stderr merged | YES for the CLI half (`type -P bmad`, `bmad --version`, `bmad --help` must work on the built image, test-19:1175-1190, 545-561); the manifest and install.sh text come from the mounted repo catalogue. The header says a host smoke path exists (test-19:19-21) so on a host the CLI half would see the host PATH [UNVERIFIED as run] |
| test-49-spec2-evidence.sh | same step, table row | `coder-ci-aidev02-contract.yml:1240` | `docker run ... -v /repo:ro -e REPO_ROOT=/repo,RESULT_FILE=/evidence/spec2-evidence-static.txt` | NO in substance: a static scan of repo files (test-49:294-322); it runs in the image container only because the driver table does so. Header: "No lifecycle producer is EVER executed here" (test-49:11) |
| test-52-browser-usability-evidence.sh | step "T52 - browser usability evidence (runner-native, pre-build)" | `coder-ci-aidev02-contract.yml:832-847` | `bash .github/contract-tests/test-52-browser-usability-evidence.sh` on the runner with `RESULT_FILE=artifacts/test-52-evidence/...`; positioned "after T51 and before Buildx/image" (workflow:828-831) | NO: runner-native, pre-build (Node plus repo files). Other modes of the same script (`--browser-preflight`, `--check-editor`, `--prepare-orca`, `--collect-orca`) are called from `coder-ci-validate.yml:561, 591, 1028` and `coder-ci-aidev02-contract.yml:190, 206` but those modes do not run the profile assertion at test-52:1378-1384 [the profile assertion sits in the `ORCA_FIXTURES` node block of the default mode, test-52:798, 1378; which exact modes reach line 798 is UNVERIFIED] |

Other workflows that mention these scripts: `orca-upstream-monitor.yml:352-353` only `git add`s test-52 as one of the files an Orca bump PR edits (it does not run it); no other workflow in `.github/workflows/` runs test-57, test-46, test-19 or test-49 (Grep for `test-(57|46|19|49)` outside the contract workflow found no matches in workflow files; the 7 files matching the wider pattern `contract-tests` run other tests such as test-51, test-17 and test-startup-boot) [CODE-VERIFIED].

`test-startup-boot.sh` (not assigned) is run by `coder-ci-validate.yml:276-277, 301, 912, 1085` and `coder-ci-orca-boot.yml:265` and contains 35 case-insensitive `bmad` hits (Grep count), including `NOT_CONFIGURED: BMad on a blank seed (installed, not configured)` (line 233) and fixtures expecting `Catalogue not configured: bmad` (lines 1121-1137). Those assertions pin the same "Installed-not-Configured on a blank seed" state seen from the MOTD side. [UNVERIFIED which of them an option would break; assigned elsewhere]

## 9. Part (d): cross-validation of the project index test count

Claim (documentation): `docs/generated/PROJECT_INDEX.md` says `contract-tests/ # T1-T55 oracles` (line 13), `Contract gate ... image build + T1-T55` (line 36) and `build + T1-T55` (line 65) [CODE-CONTRADICTED].

What the code shows:
- Glob `.github/contract-tests/test-*.sh` returns files up to `test-79-create-error-tail.sh`, including `test-57-catalogue-configure.sh`, `test-58-motd-trigger-paths.sh`, `test-59-central-defaults-push.sh`, `test-59-home-workspaces-dir.sh`, `test-60-llm-gateway-env.sh`, `test-62` to `test-79`, plus unnumbered `test-b1-affordance-matrix.sh` and `test-startup-boot.sh`.
- Numbers 30 and 61 have no file (Glob `test-{30,61,80,81,82}*` returned nothing). Numbers 80 and above do not exist.
- Several numbers are shared by two scripts: 1, 2, 3, 4, 5, 6, 7, 8, 9, 59, 73, 74 (for example `test-59-central-defaults-push.sh` and `test-59-home-workspaces-dir.sh`; `test-74-claude-md-block.sh` and `test-74-orca-clean-stop.sh`).
- The contract workflow itself wires tests beyond 55: for example `test-57` at line 1241, `test-56`, `test-58`, `test-59` at lines 1345-1349, and the table row for `test-71`, `test-73`, `test-74`, `test-77` at lines 1242-1245. A workflow comment at line 635 still says "(T50..T55)" for the pre-build group and line 924 "pre-build gates (T50..T55 above)", which is true for that group only.
- The index header says it was "Generated: 2026-09-25 against origin/main 1ace9c30" (PROJECT_INDEX.md line 3); the repo now holds tests added after that generation.

Finding: the project index understates the suite (T1-T55 versus tests up to T79, with 12 duplicated numbers and two unnumbered scripts). [STALE DOC]. Practical consequence for the final report: do not use "T1-T55" as the boundary of pinned tests; the BMAD pins above live in tests 19, 46, 49, 52 and 57, and test-startup-boot.sh holds more.

## Gaps and Questions

UNVERIFIED items (7):
1. [UNVERIFIED] Where options E (`bmad install --directory ~`) and F (upstream `global_target_dir` user-scope install) actually write. The matrix in section 7 uses the wording of the research question. I ran no `bmad` command (binding scope guard allowed only `--version`, `install --help`, `--list-tools`, `--list-options` and I did not need them for test tracing). Agent 01/02 findings should confirm the paths before the final report relies on the "X" marks in the E and F columns.
2. [UNVERIFIED] Whether `test-startup-boot.sh` (35 `bmad` hits, run by `coder-ci-validate.yml` and `coder-ci-orca-boot.yml`) would break under any option. It was not in my assigned files; its MOTD and readiness strings (lines 233, 1099-1137) pin `Catalogue not configured: bmad` and `slug=bmad state=Installed-not-Configured`. It must be covered by part 2 or by the final report.
3. [UNVERIFIED] Other contract tests that may pin the bmad slug, `Dockerfile.coder`, `profiles.yaml` or catalogue file lists without the literal word `bmad` in the assigned files (candidates by name only: `test-1-catalogue-shape.sh`, `test-2-manifest-schema.sh`, `test-44-catalogue-disposition.sh`, `test-47-catalogue-discoverability.sh`, `test-67-image-inputs-cover-copies.sh`). A Grep count shows 121 case-insensitive `bmad` occurrences in 6 files under `.github/contract-tests` (test-46: 38, test-57: 41, test-startup-boot: 35, test-19: 5, test-49: 1, test-52: 1), so test-44, test-47, test-1 and test-2 and test-67 contain NO literal `bmad`; whether they iterate over the catalogue generically (and would see a changed `bmad/` directory or a new slug) is not verified.
4. [UNVERIFIED] The contents of `slug-configuration.md` ("Contract: slug-configuration.md Verification", test-57:6). The file exists at `_bmad-output/specs/spec-orca-catalogue-bundle/slug-configuration.md` (Glob) but I did not read it; I relied on the test code instead.
5. [UNVERIFIED] Whether the tests pass today. I ran none of them (scope guard). All "what it pins" statements come from reading the assertion code.
6. [UNVERIFIED] Which invocation modes of `test-52-browser-usability-evidence.sh` reach the `ORCA_FIXTURES` block (test-52:798) that holds the profile mapping pin at line 1378-1384. The workflow step at `coder-ci-aidev02-contract.yml:832-847` runs it with no argument; the `case "${1:-}"` at test-52:23-24 handles the named modes before. I did not trace the no-argument path from line 24 to 798.
7. [UNVERIFIED] Exact number of files in `.github/contract-tests/` (Glob output of the first query was complete for `test-*.sh` but I did not count it; the second query was truncated at 100 of 111 entries).

Other questions for the final report:
- The "no seed" case is "no repo registered in `~/.aidev/status/seed-repo-path`", not "a repo without BMAD". The existing installer already creates `_bmad` in a registered seed repo (install.sh:24-55). The user-facing question "first use in a project that never had BMAD" is a different case from what test-57:446-452 covers: it is the case between test-57:323 (seed repo configured at startup) and a user-created project elsewhere (not in any fixture). A new test row would be needed for the new behaviour in either case.
- [CODE-CONTRADICTED] claims: (1) PROJECT_INDEX.md "T1-T55" (see section 9). No other CODE-CONTRADICTED claims found.
- Health and Configured for a user-created project: `spec2_health_observed bmad` only inspects the registered seed repo (spec2-health.sh:99-113), so no option B to F can make health report Configured for a different project; if the owner wants it, spec2-health.sh and test-57 `record_health` rows must change together.

## Stale Documentation Found

| Item | Doc location | Status | Evidence |
|---|---|---|---|
| "contract-tests T1-T55" and "image build + T1-T55" | `docs/generated/PROJECT_INDEX.md:13, 36, 65` | **[STALE DOC]** [CODE-CONTRADICTED]: tests exist up to test-79 with duplicates and two unnumbered scripts | Glob of `.github/contract-tests/test-*.sh`; workflow lines 1241-1245, 1345-1349 |
| test-57 header "Wired into: coder-ci-aidev02-contract.yml -> contract_tests -> In-image contract tests (driver) table row (7th column: --network=none,--user=0)" | `test-57-catalogue-configure.sh:15-16` | [CODE-VERIFIED] current | workflow:1241 and the 7th-column parse at workflow:1212-1213 |
| test-52 header "Wired into ... T52 - browser usability evidence (runner-native, pre-build)" | `test-52-browser-usability-evidence.sh:9` | [CODE-VERIFIED] current | workflow:832 |
| test-46, test-19, test-49 headers "table row" wiring | test-46:10, test-19:10, test-49:13 | [CODE-VERIFIED] current | workflow:1237, 1234, 1240 |
| test-57 header "orca-profile installers (bmad excluded, OD-1)" | `test-57-catalogue-configure.sh:10-11` | consistent with code: `spec2-health.sh:562` and test-46 fixtures treat bmad specially; the reprofile reader rejects a bmad row (spec2-health.sh:529) | [CODE-VERIFIED] |
| bmad `welcome_message` says "If this workspace has a seed repo, BMad is already set up there ... For any other repo, run from its root: bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output" | `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14` | consistent with install.sh:24-55 and the owner decision context; it is the current "option A" user path | [CODE-VERIFIED] |
| Dockerfile comment "/usr/local/bin/bmad is a wrapper, not a symlink" | `Dockerfile.coder:134-135` | [CODE-VERIFIED] by the RUN lines 137-143 | Dockerfile.coder:142 |
| `test-19.sh:200` comment "bmad's `... npm install -g bmad-method@6.9.0 ...`" in the install.sh FAIL message | test-19:199-201 | [CODE-VERIFIED]: install.sh:18 contains that text inside a double-quoted echo | install.sh:18 |

## Summary

Five contract tests pin BMAD behaviour, all run by one job (`contract_tests` in `coder-ci-aidev02-contract.yml`; test-52 runner-native before the image build, the other four inside the built image). Only ONE assertion pins "no seed: bmad writes nothing": `test-57-catalogue-configure.sh:450`, which compares a whole-HOME snapshot (`snap`, lines 148-153) that covers everything under `$HOME` except `.aidev/installed/*` and any `.git/index`, including the seed repo at `${H}/seed`. Options B, D, E and F that write inside HOME on the no-seed path break it for certain and need a new allow-listed delta assertion; options A and C do not touch it, but C is constrained by test-19 (`bmad` must stay an executable file on PATH whose `--version` and `--help` exit 0, and `install.sh` must keep its `command -v` plus `exit 2` shape with no unquoted install verb) and by test-49's lifecycle-string scan of `Dockerfile.coder`. Tests 46, 49 and 52 pin slug-name rules, a probe shape rule, a file-path inventory and the exact profile mapping (a NEW slug breaks test-52:1381-1383), not what the bmad installer writes. The project index claim "T1-T55" is stale (tests run to T79), and `test-startup-boot.sh` (35 bmad hits, outside my assigned files) also pins the Installed-not-Configured state and must be covered elsewhere.
