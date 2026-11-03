# Sysop E2E Test Guide — `ccsession model data publishing` (`5.0.0`)

- **Capability:** publishing a new `ccsession-models.json` (profiles, picker list, tier slot names) to every ccsession install. Every launch asks the fork's master branch for a newer copy, validates it (schema 2, 256 KiB cap, field patterns) and caches it; a check against a candidate file shows what installs would do with it before it is published.
- **Audience:** system operator / administrator
- **Gate:** installs fetch from the fork's master branch, `DEFAULT_URL` = `https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/src/superclaude/skills/ccsession-tag/ccsession-models.json` (`src/superclaude/skills/ccsession-tag/models.py:54-57,298`), on every launch unless `CCSESSION_MODELS_REFRESH=0` (`src/superclaude/skills/ccsession-tag/ccsession:1479-1485`). Publishing therefore means merging a change to master of `IronbellyOrg/IronClaude`, which needs write access to that repo (a GitHub setting outside this repo; who holds it is UNVERIFIED here). Testing needs no privilege: `CCSESSION_MODELS_URL` points one command at a candidate file (`models.py:298`) and `XDG_CACHE_HOME` moves the cache to a throwaway folder (`models.py:129-131`).
- **Source of truth:** `src/superclaude/skills/ccsession-tag/models.py:53-65,129-131,142-209,212-252,255-314,831-838,993-1003,1026-1027`; `src/superclaude/skills/ccsession-tag/ccsession:68-76,92,111-112,671-675,913-916,1422-1435,1479-1485`; `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:172-178`; `src/superclaude/skills/ccsession-tag/README.md:431-470`; `src/superclaude/skills/ccsession-tag/ccsession-models.json:2-3`; `tests/unit/test_ccsession_tag.py:986-989`; `.github/workflows/test.yml:3-7,38-40`; `CHANGELOG.md:160`
- **Est. time:** `Tier A: 2 minutes. Tier B: 10-15 minutes. Tier C: 30 minutes plus PR review time.`

## Preconditions

- IronClaude 5.0.0 installed for your user (`superclaude install` done): `superclaude --version` prints `SuperClaude, version 5.0.0`, and `~/.claude/skills/ccsession-tag/` holds the 5.0.0 ccsession (`models.py`, `ccsession`, `ccsession-models.json` version `2026-10-28.1`).
- Linux with `bash`, `python3`, `grep`, `sed`, `cmp` and `wc` in `/usr/bin` or `/bin`. Tier B runs every command with `PATH=/tmp/e02/bin:/usr/bin:/bin` and nothing else from your environment.
- Network access to `raw.githubusercontent.com` for Step 8 and Tier C. Every other step works offline.
- `/tmp/e02` does not exist (`[ ! -e /tmp/e02 ] && echo OK` prints `OK`).
- For Tier C only: a clone of `IronbellyOrg/IronClaude` with a branch holding your edit to `src/superclaude/skills/ccsession-tag/ccsession-models.json`, `uv`, and the right to open a pull request on the fork.
- **Privilege/gate satisfied.** Tiers A and B need no privilege. Tier C ends with a merge to master of `IronbellyOrg/IronClaude`, done by someone with write access there after review.
- **Safety.**
  - A merge to master changes the model data of every install on its next launch (`README.md:433-439`; `ccsession:1479-1485`). Never push a candidate to master to try it out: Tiers A and B show exactly what installs would do with it.
  - Tier A only reads. Tier B writes only under `/tmp/e02`, with a throwaway `HOME` and cache (`/tmp/e02/home`, `/tmp/e02/cache*`), no workspace env file and `CLAUDE_BIN=/bin/false`: it never starts Claude Code, never starts a gateway shim and never touches your real `~/.cache/ccsession/` or `~/.claude`. The only launches it runs are ones that stop at an unknown profile, before Claude Code would start (`ccsession:913-916`).
  - No step in Tiers A and B starts a Claude Code session. Tier C Step 10 does, if you open the PR with `/sc:pr-submit` (see that step).

## What you're verifying

- **Which URL forms work.** `_fetch` hands `CCSESSION_MODELS_URL` unchanged to `urllib.request.urlopen` (`models.py:265-267`) and checks no scheme, so `https://`, `http://` and `file://` URLs all work. A `file://` URL needs an absolute path (`file:///tmp/e02/candidate.json`); a plain path without `file://` fails with `failed: ValueError`. This guide therefore checks candidates as `file://` URLs and needs no local web server.
- A candidate is accepted only when it is schema 2 (`models.py:53,146-147`), at most 256 KiB (`models.py:59,268-272`), and every version, profile, model id, label and tier name matches its pattern (`models.py:60-65,142-209`). A rejected, oversized, unreadable or older candidate leaves the install on its current copy (`models.py:270-293`).
- The active copy is the newest `version` among the downloaded cache and the copy shipped with the skill (`models.py:222-239`), so a published change must raise `version` (`README.md:469-470`).
- `refresh()` writes the result to `models.checked` and prints `[ccsession] model list updated to <version>: <+added, -removed>` when the active version changes (`models.py:247-252,296-314`).
- `CCSESSION_MODELS_REFRESH=0` skips the check at launch (`ccsession:1483-1485`); `ccsession --refresh-models` checks anyway (`ccsession:1427-1430`).
- Against the real master URL, the second check is answered `not modified` through the saved ETag (`models.py:257-263,269,290-291`).
- An install older than the 5.0.0 letter tiers rejects 5.0.0-layout data and keeps its own copy (`CHANGELOG.md:160`).

---

## Steps

### Tier A — free smoke on your own install (read-only)

#### Step 1 — Which model data your install uses `[FREE]`

**Do:**

```bash
ccsession --models-status | sed -n 1,4p
```

**Expected result:** (`models.py:993-1002`; `ccsession:1432-1435`)

- `Model data version: <version> (downloaded)` when your cache in `~/.cache/ccsession/` (or `$XDG_CACHE_HOME/ccsession/`) holds the newest valid copy, `(bundled)` when the copy shipped with the skill is newer or the cache is empty or invalid, `(built-in minimum)` when neither is usable (`models.py:129-131,228-239`).
- `Source URL:         https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/src/superclaude/skills/ccsession-tag/ccsession-models.json` (`models.py:54-57,999`). Any other URL means `CCSESSION_MODELS_URL` is set in your shell or in `~/.claude/ccsession.env`, which ccsession sources first (`ccsession:671-675`); your install then does not follow master.
- `Cache:` the `models.json` path in that cache folder.
- `Last check:         <date and time> <status>`, for example `not modified` or `downloaded`, or `never` (`models.py:305-308,995-1002`). A status starting `rejected:`, `too large`, `failed:` or `HTTP` means master currently serves data your install refuses: a FAIL to report.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 2 — The installed code has the 5.0.0 limits `[FREE]`

**Do:**

```bash
M="$HOME/.claude/skills/ccsession-tag/models.py"
grep -n -E '^SUPPORTED_SCHEMA = |^_MAX_BYTES = |^_TIER = |"https://raw.githubusercontent.com/IronbellyOrg|urllib.request.urlopen\(' "$M"
grep -m1 -n '"version"' "$HOME/.claude/skills/ccsession-tag/ccsession-models.json"
```

**Expected result:** these lines, matching the 5.0.0 source (`models.py:53,55,59,64,265`; `ccsession-models.json:3`):

```text
53:SUPPORTED_SCHEMA = 2
55:    "https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/"
59:_MAX_BYTES = 256 * 1024
64:_TIER = re.compile(r"^tier([0-9]{1,2}[a-z]?)$")
265:        with urllib.request.urlopen(
3:  "version": "2026-10-28.1",
```

Other line numbers or values mean the install is not the 5.0.0 copy; the expected results below may not hold.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — candidate checks with throwaway files under /tmp/e02

#### Step 3 — Build the throwaway env, the helpers and the test files `[LOCAL-WRITE]`

**Do:**

```bash
[ ! -e /tmp/e02 ] || { echo "/tmp/e02 exists: run Cleanup first"; false; }
mkdir -p /tmp/e02/home /tmp/e02/cache /tmp/e02/bin && chmod 700 /tmp/e02
ln -s "$HOME/.claude/skills/ccsession-tag/ccsession" /tmp/e02/bin/ccsession
cp "$HOME/.claude/skills/ccsession-tag/ccsession-models.json" /tmp/e02/shipped.json
cat > /tmp/e02/e2.sh <<'EOF'
e2() {  # clean environment: throwaway HOME and cache, no workspace env file, no Claude
  env -i PATH=/tmp/e02/bin:/usr/bin:/bin HOME=/tmp/e02/home XDG_CACHE_HOME=/tmp/e02/cache \
    AIDEV_AI_DEFAULTS_PATH=/tmp/e02/no-defaults.sh CLAUDE_BIN=/bin/false PYTHONDONTWRITEBYTECODE=1 "$@"
}
check() {  # check <name or URL>: fetch that copy now into the cache ${C:-/tmp/e02/cache}
  case "$1" in *://*) u=$1 ;; /*) u=$1 ;; *) u=file:///tmp/e02/$1.json ;; esac
  e2 XDG_CACHE_HOME="${C:-/tmp/e02/cache}" CCSESSION_MODELS_URL="$u" ccsession --refresh-models |
    sed -n -e '/model list updated/p' -e '/model data check/p' -e '/^Model data version/p'
}
EOF
source /tmp/e02/e2.sh
python3 - <<'EOF'
import copy, json
base = json.load(open("/tmp/e02/shipped.json"))
def new(version):
    d = copy.deepcopy(base)
    d["version"] = version
    return d
def save(name, d):
    with open(f"/tmp/e02/{name}.json", "w") as f:
        json.dump(d, f, indent=2)
d = new("9999-01-01.1"); d["profiles"]["e02test"] = dict(d["profiles"]["claude"], aliases=[]); save("candidate", d)
save("older", new("9999-01-01.0"))
save("lower", new("2000-01-01.1"))
d = new("9999-01-02.1"); d["schema"] = 1; save("schema1", d)
save("badversion", new("9999 01"))
d = new("9999-01-02.2"); d["profiles"]["claude"]["model"] = "$(rm -rf ~)"; save("badmodel", d)
d = new("9999-01-02.3"); d["profiles"]["claude"]["label"] = "Opus `x`"; save("badlabel", d)
d = new("9999-01-02.4"); d["tiers"]["tier1A"] = d["tiers"]["tier1a"]; save("badtier", d)
d = new("9999-01-02.5"); d["picker"]["remove"] = []; save("oldpicker", d)
d = new("9999-01-02.6"); d["pad"] = "x" * 262144; save("big", d)
with open("/tmp/e02/broken.json", "w") as f:
    f.write('{"schema": 2,')
EOF
e2 ccsession --models-status
```

**Expected result:**

- The candidate is the shipped data with `version` `9999-01-01.1` and one added profile, `e02test`. Each other file breaks one rule, or carries a lower version.
- The status block (`models.py:993-1003,1026-1027`):

```text
Model data version: 2026-10-28.1 (bundled)
Source URL:         https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/src/superclaude/skills/ccsession-tag/ccsession-models.json
Cache:              /tmp/e02/cache/ccsession/models.json
Last check:         never
Profiles:           claude, gpt, grok, muse, wonderfull, wonder, qwen, glm
Tier mode:          off (no T<N>_WINDOW in the workspace env)
```

- `bundled` and `never`: the empty throwaway cache leaves the shipped copy in use (`models.py:228-239`; `ccsession-models.json:2-3`). Tier mode is off because the test points `AIDEV_AI_DEFAULTS_PATH` at a file that does not exist; the model data check does not depend on tier mode.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 4 — A valid candidate through a `file://` URL `[LOCAL-WRITE]`

**Do:**

```bash
check candidate
e2 CCSESSION_MODELS_URL=file:///tmp/e02/candidate.json ccsession --models-status
cmp /tmp/e02/candidate.json /tmp/e02/cache/ccsession/models.json && echo "cache holds the candidate"
wc -c < /tmp/e02/cache/ccsession/models.etag
check candidate
```

**Expected result:**

- The first check prints (`models.py:247-252,289,312-313,831-838`):

```text
[ccsession] model list updated to 9999-01-01.1: +profile e02test
[ccsession] model data check: downloaded
Model data version: 9999-01-01.1 (downloaded)
```

- The status shows `Source URL:         file:///tmp/e02/candidate.json`, `Last check:         <date and time> downloaded` and `e02test` at the end of `Profiles:` (`models.py:305-308,995-1003`).
- `cache holds the candidate`: the accepted bytes are cached unchanged (`models.py:283-288`).
- `0`: a `file://` response carries no ETag, so the saved ETag is empty (`models.py:269,284`).
- The second check prints `[ccsession] model data check: downloaded` and `Model data version: 9999-01-01.1 (downloaded)`, with no `model list updated` line: the version did not change (`models.py:312-313`). A `file://` URL never answers `not modified`; only a server that sends an ETag does (Step 8).

This step proves the URL form: `_fetch` accepted a `file://` URL because it passes the URL straight to `urllib.request.urlopen` (`models.py:265-267`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — Bad candidates are refused and the install keeps its copy `[LOCAL-WRITE]`

**Do:**

```bash
for f in schema1 badversion badmodel badlabel badtier oldpicker big broken missing older; do
  echo "== $f"; check "$f"
done
echo "== plain path"; check /tmp/e02/candidate.json
```

**Expected result:** after each `== <name>` line, one `[ccsession] model data check: <status>` line, then `Model data version: 9999-01-01.1 (downloaded)`: the Step 4 copy stays active every time.

| File | Status after `model data check:` | Source |
|---|---|---|
| `schema1` | `rejected: unsupported schema 1` | `models.py:53,146-147` |
| `badversion` | `rejected: missing or invalid version` | `models.py:61,148-149` |
| `badmodel` | `rejected: profile 'claude' has an invalid model` | `models.py:60,161-162` |
| `badlabel` | `rejected: profile 'claude' has an invalid label` | `models.py:62,173-176` |
| `badtier` | `rejected: invalid tier 'tier1A'` | `models.py:64,180-182` |
| `oldpicker` | `rejected: picker.remove was replaced by picker.show` | `models.py:197-199` |
| `big` | `too large` (the file is over 256 KiB) | `models.py:59,268-272` |
| `broken` | `failed: JSONDecodeError` | `models.py:273,292-293` |
| `missing` | `failed: URLError` | `models.py:292-293` |
| `older` | `older than cached` (`9999-01-01.0` is below the cached `9999-01-01.1`) | `models.py:278-282` |
| plain path | `failed: ValueError` (no `file://`) | `models.py:265-267,292-293` |

The `older` row is why a rollback must not lower `version`: installs that already hold the newer copy keep it. Publish the earlier content with a higher version instead.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — The version must be raised `[LOCAL-WRITE]`

**Do:**

```bash
C=/tmp/e02/cache2 check lower
```

**Expected result:**

```text
[ccsession] model data check: downloaded
Model data version: 2026-10-28.1 (bundled)
```

The candidate is valid and cached, but its version `2000-01-01.1` is below the shipped copy's `2026-10-28.1`, so the shipped copy stays active (`models.py:222-239`; `README.md:469-470`). A change published without raising `version` above every shipped and cached copy does nothing on installs.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 7 — The check at launch, and `CCSESSION_MODELS_REFRESH=0` `[LOCAL-WRITE]`

**Do:** each launch names a profile that does not exist, so it stops before Claude Code would start (`ccsession:913-916`), after the launch-time check (`ccsession:1479-1485`):

```bash
L="XDG_CACHE_HOME=/tmp/e02/cache3 CCSESSION_MODELS_URL=file:///tmp/e02/candidate.json"
e2 $L CCSESSION_MODELS_REFRESH=0 ccsession e02-check --profile e02nosuch; echo "exit=$?"
ls -A /tmp/e02/cache3 2>/dev/null | wc -l
e2 $L ccsession e02-check --profile e02nosuch; echo "exit=$?"
ls /tmp/e02/cache3/ccsession
e2 $L CCSESSION_MODELS_REFRESH=0 ccsession --refresh-models | sed -n '/model data check/p'
find /tmp/e02/home -mindepth 1 | wc -l
```

**Expected result:**

- With `CCSESSION_MODELS_REFRESH=0`: no check runs (`ccsession:1483`). `ccsession: unknown profile 'e02nosuch'`, then `Valid profiles: claude, gpt, grok, muse, wonderfull, wonder, qwen, glm, plus any in /tmp/e02/home/.config/ccsession/profiles.d`, `exit=2` (`ccsession:913-916`), and `0`: no cache folder was created.
- Without it: `[ccsession] model list updated to 9999-01-01.1: +profile e02test` comes first, then the same refusal with `e02test` in the valid list, `exit=2`. The launch checked the candidate and used it at once (`ccsession:1483-1485`; `models.py:296-314`). Only the change line prints; the status line needs `CCSESSION_MODELS_VERBOSE` (`models.py:836-837`).
- `models.checked`, `models.etag`, `models.json`: the launch-time check filled the cache (`models.py:283-288,305-308`).
- `[ccsession] model data check: downloaded`: `--refresh-models` checks even with `CCSESSION_MODELS_REFRESH=0`, because it runs before that setting is read (`ccsession:1427-1430,1483`).
- `0`: nothing was written to the throwaway `HOME`.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — The real master URL, and `not modified` `[LOCAL-WRITE]`

Needs network access to `raw.githubusercontent.com`; mark N/A without it.

**Do:**

```bash
M=https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/src/superclaude/skills/ccsession-tag/ccsession-models.json
C=/tmp/e02/cache4 check "$M"
C=/tmp/e02/cache4 check "$M"
cat /tmp/e02/cache4/ccsession/models.etag; echo
```

**Expected result:**

- First check: `[ccsession] model data check: downloaded` and `Model data version: <master's version> (downloaded)`, with a `model list updated` line first when master's version is above `2026-10-28.1`. When this guide was written master served `2026-10-28.1`. `(bundled)` instead of `(downloaded)` means master's version is below the shipped copy's: a FAIL to report, since installs would ignore master.
- Second check: `[ccsession] model data check: not modified`: the saved ETag went out as `If-None-Match` and GitHub answered 304 (`models.py:257-263,290-291`).
- A quoted ETag, for example `"95a9e7ae..."`.
- `rejected: ...`, `too large` or `HTTP <code>` on the first check: master serves data installs refuse. Every install then keeps its current copy (`models.py:270-293`): a FAIL to report.

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

#### Step 9 — An install older than letter tiers keeps its copy `[LOCAL-WRITE]`

Needs a clone of `IronbellyOrg/IronClaude` that has the v5.0.0 history; mark N/A without one.

**Do:**

```bash
REPO=<path to your IronClaude clone>
git -C "$REPO" show fab74603^:src/superclaude/skills/ccsession-tag/models.py > /tmp/e02/old-models.py
grep -n '^_TIER = ' /tmp/e02/old-models.py
e2 XDG_CACHE_HOME=/tmp/e02/cache-old CCSESSION_MODELS_VERBOSE=1 CCSESSION_MODELS_URL=file:///tmp/e02/candidate.json \
  python3 /tmp/e02/old-models.py refresh --wait 10
```

**Expected result:**

- `62:_TIER = re.compile(r"^tier([0-9]{1,2})$")`: before commit `fab74603` (the letter-tier change in 5.0.0) a tier name had no letter.
- `[ccsession] model data check: rejected: invalid tier 'tier1a'`. Data with the 5.0.0 tier layout is refused by older installs, which keep their own copy and keep working (`CHANGELOG.md:160`). Plan any change that older installs must receive with this in mind: they will not receive it.

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

### Tier C — publish a real change through a pull request

Run Tier C only when you are publishing a change; otherwise mark Steps 10-13 N/A. Run it after Tier B and before Cleanup, in a shell where `source /tmp/e02/e2.sh` has been run. Publishing affects every install.

#### Step 10 — Check your edited file before you push `[LOCAL-WRITE]`

**Do:** in your clone, on the branch with your edit, after `git fetch origin`:

```bash
REPO=<path to your IronClaude clone>
F="$REPO/src/superclaude/skills/ccsession-tag/ccsession-models.json"
git -C "$REPO" show origin/master:src/superclaude/skills/ccsession-tag/ccsession-models.json > /tmp/e02/master.json
grep -m1 '"version"' /tmp/e02/master.json "$F"
cp "$F" /tmp/e02/mine.json
C=/tmp/e02/cache-mine check master
C=/tmp/e02/cache-mine check mine
(cd "$REPO" && PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/unit/test_ccsession_tag.py -k "shipped_model_data_is_valid or refresh" -q -p no:cacheprovider)
```

**Expected result:**

- Your `version` is higher than master's (`README.md:469-470`; `models.py:222-239`).
- `check master` accepts master's copy; `check mine` then prints `[ccsession] model list updated to <your version>`, followed by `: <+added, -removed>` when your change adds or removes profiles or `picker.show` ids (the change line lists only those, `models.py:242-252`), then `[ccsession] model data check: downloaded` and `Model data version: <your version> (downloaded)`.
- `4 passed`: the validity gate and the refresh tests pass on your file (`tests/unit/test_ccsession_tag.py:986-989`).
- `rejected: ...`, `too large` or `older than cached`: fix the file before pushing (Step 5).

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

#### Step 11 — Open the pull request on the fork `[EXTERNAL]`

**Do:** push your branch to `origin` (`IronbellyOrg/IronClaude`) and, in Claude Code in your clone, run:

```text
/sc:pr-submit --monitor 3 --head <branch> --title "chore(ccsession): model data <your version>" --body "<what changed and why>"
```

When `/sc:pr-submit` cannot run, use the fallback:

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "chore(ccsession): model data <your version>" --body "<what changed and why>"
```

`/sc:pr-submit` runs in a Claude Code session against your real `~/.claude`. Besides that session's history, the installed hooks write `~/.claude/state/` and `~/.claude/logs/`: the freshness hooks at session start and on each prompt, and `auggie-flag-clear.sh` after auggie tool calls (`src/superclaude/hooks/hooks.json:18,49,104`).

**Expected result:**

- A PR at `https://github.com/IronbellyOrg/IronClaude/pull/<N>`. Any other owner in the URL: close it at once and reopen it with `--repo IronbellyOrg/IronClaude`.
- The `Tests` workflow runs the full test suite on the PR (`.github/workflows/test.yml:3-7,38-40`), including `test_shipped_model_data_is_valid` (`tests/unit/test_ccsession_tag.py:986-989`). UNVERIFIED: whether master's branch protection requires that check to pass before a merge (a GitHub setting outside this repo).

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

#### Step 12 — Fetch the pushed copy over HTTPS, before the merge `[LOCAL-WRITE]`

**Do:**

```bash
SHA=$(git -C "$REPO" rev-parse HEAD)
C=/tmp/e02/cache-pr check "https://raw.githubusercontent.com/IronbellyOrg/IronClaude/$SHA/src/superclaude/skills/ccsession-tag/ccsession-models.json"
```

**Expected result:** the same lines as `check mine` in Step 10, now fetched over HTTPS the way installs fetch master (`models.py:255-293`). A commit SHA in place of `master` serves that commit's file; this was confirmed for the v5.0.0 commit when this guide was written. `HTTP 404` means the commit is not pushed yet.

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

#### Step 13 — Merge, then confirm master serves the new copy `[EXTERNAL]`

**Do:** after review, merge the PR into master. Then:

```bash
M=https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/src/superclaude/skills/ccsession-tag/ccsession-models.json
C=/tmp/e02/cache-live check "$M"
C=/tmp/e02/cache-live check "$M"
```

**Expected result:**

- First check: the `model list updated to <your version>` line, `downloaded`, `Model data version: <your version> (downloaded)`. Second check: `not modified` (Step 8). UNVERIFIED: how long `raw.githubusercontent.com` keeps serving the previous copy after a merge (a GitHub cache outside this repo); if the old version appears, repeat after a few minutes.
- From then on every 5.0.0 install downloads the new copy on its next launch, waiting at most about 2 seconds (`CCSESSION_MODELS_WAIT`, `ccsession:1483-1485`), and prints the change line once (`models.py:312-313`). Running shims re-read the model data on every model-list request, so they need no restart (`local-gateway-alias-proxy.py:172-178`; `README.md:439`). Installs older than letter tiers keep their own copy (Step 9).

**Pass/Fail:** ☐ PASS ☐ FAIL ☐ N/A — notes: `______`

---

## Negative / gate check (recommended)

Verify that nothing reaches every install without the merge, and that bad data never replaces a good copy. A row that behaves otherwise is a finding.

| Try this (without privilege) | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[LOCAL-WRITE]` Point one command at your own file: `check candidate` (Step 4) | Only that command's cache changes. Every other launch still fetches master, because `CCSESSION_MODELS_URL` is read per process and the cache is per user | `models.py:129-131,298` | ☐ |
| `[LOCAL-WRITE]` Serve invalid, oversized, unreadable or unparsable data (Step 5) | Refused with the reason; the install keeps its current copy | `models.py:142-209,268-293` | ☐ |
| `[LOCAL-WRITE]` Roll back by publishing a lower version (Step 5, `older`) | `older than cached`: installs that hold the newer copy keep it; a rollback needs a higher version | `models.py:278-282` | ☐ |
| `[LOCAL-WRITE]` Publish valid data without raising the version (Step 6) | Cached but not used: the shipped or cached copy with the higher version stays active | `models.py:222-239` | ☐ |
| `[EXTERNAL]` A PR whose `ccsession-models.json` fails validation | The `Tests` workflow fails at `test_shipped_model_data_is_valid`. UNVERIFIED: whether branch protection then blocks the merge | `.github/workflows/test.yml:3-7,38-40`; `tests/unit/test_ccsession_tag.py:986-989` | ☐ |
| `[EXTERNAL]` Merge to master from an account without write access to `IronbellyOrg/IronClaude` | Refused by GitHub. UNVERIFIED: a GitHub permission outside this repo | `models.py:54-57` (installs follow master only) | ☐ |

## Cleanup

Nothing in your real `~/.claude` or `~/.cache/ccsession/` was changed by Tiers A and B. Remove the test files:

```bash
cd /tmp && rm -rf /tmp/e02
[ ! -e /tmp/e02 ] && echo "clean"
```

The command removes the throwaway `HOME`, every test cache, the candidate and test files, the copies of master's and your file, and the old `models.py`. A Tier C publish is not undone by Cleanup: to undo it, publish the earlier content with a higher `version` through another PR (Step 5, `older` row).

## Overall result

☐ **PASS** — admin capability works and is correctly gated for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `______`  **Date:** `______`  **Build:** `5.0.0 (d953b983)`
