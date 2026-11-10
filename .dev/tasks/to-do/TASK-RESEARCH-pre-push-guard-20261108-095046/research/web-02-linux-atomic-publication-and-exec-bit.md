# Research: Linux atomic file publication without replacement, and git's executable-bit requirement for hooks

**Scope:** web-02 (gaps G-4, G-5, G-8): no-replace publication primitives (link/linkat EEXIST, O_CREAT|O_EXCL, O_TMPFILE + linkat, rename, renameat2 RENAME_NOREPLACE), fchmod/umask, git v2.47.3 `find_hook` X_OK check and `advice.ignoredHook`, atomic executable hook install without replacement. Answers sub-question (e) and the (f) version questions.
**Status:** Complete
**Date:** 2026-11-08
WEB02_SANDBOX_PATH: /tmp/web02-sandbox.pVSjes6U

**WEB SEARCH PROVENANCE:** provider=WebSearch reason=tavily-unavailable (no `mcp__tavily__*` tool is present in this agent's tool set). Primary sources were fetched with WebFetch; git source text was fetched verbatim with a read-only `curl -sS ... | cat -n` (stdout only, no file written) because WebFetch truncates quotations.

---

## Codebase baseline (source of truth): `publish()`

[CODE-VERIFIED] `src/superclaude/hooks/scripts/launch-job-identity.sh` lines 164-174 (read 2026-11-08):

```python
164 def publish(parent, name, value):
165     tmp = '.' + uuid.uuid4().hex
166     fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
167     try:
168         with os.fdopen(fd, 'wb') as out:
169             out.write(json.dumps(value, separators=(',', ':')).encode())
170             out.flush()
171             os.fchmod(out.fileno(), 0o400)
172         os.link(tmp, name, src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
173     finally:
174         os.unlink(tmp, dir_fd=parent)
```

Pattern: unique dot-prefixed temp name -> `O_CREAT|O_EXCL|O_NOFOLLOW` create (mode 0600, then umask) -> write + flush -> `fchmod` 0400 -> `linkat(tmp, name)` without `AT_SYMLINK_FOLLOW` -> always unlink the temp name. A lost race raises `FileExistsError` (EEXIST) from `os.link`; the existing file is untouched. Note: no `os.fsync` on the file or directory, so the pattern is atomic against concurrent readers but not crash-durable (see Durability below). The temp name is visible in the directory between line 166 and line 174.

---

## Area 1: git v2.47.3 `find_hook` (executable-bit check) — HIGH

**Source:** https://github.com/git/git/blob/v2.47.3/hook.c (fetched verbatim from https://raw.githubusercontent.com/git/git/v2.47.3/hook.c). Reliability: official upstream source at the tag matching the installed git 2.47.3.

Verbatim, with line numbers from the v2.47.3 file:

```c
13	const char *find_hook(struct repository *r, const char *name)
14	{
15		static struct strbuf path = STRBUF_INIT;
16	
17		int found_hook;
18	
19		strbuf_reset(&path);
20		strbuf_repo_git_path(&path, r, "hooks/%s", name);
21		found_hook = access(path.buf, X_OK) >= 0;
22	#ifdef STRIP_EXTENSION
23		if (!found_hook) {
24			int err = errno;
25	
26			strbuf_addstr(&path, STRIP_EXTENSION);
27			found_hook = access(path.buf, X_OK) >= 0;
28			if (!found_hook)
29				errno = err;
30		}
31	#endif
32	
33		if (!found_hook) {
34			if (errno == EACCES && advice_enabled(ADVICE_IGNORED_HOOK)) {
35				static struct string_list advise_given = STRING_LIST_INIT_DUP;
36	
37				if (!string_list_lookup(&advise_given, name)) {
38					string_list_insert(&advise_given, name);
39					advise(_("The '%s' hook was ignored because "
40						 "it's not set as executable.\n"
41						 "You can disable this warning with "
42						 "`git config advice.ignoredHook false`."),
43					       path.buf);
44				}
45			}
46			return NULL;
47		}
48		return path.buf;
49	}
50	
51	int hook_exists(struct repository *r, const char *name)
52	{
53		return !!find_hook(r, name);
54	}
```

What this means:
- Line 20: the path is built with `strbuf_repo_git_path(..., "hooks/%s")`, the git-path machinery that also backs `git rev-parse --git-path hooks/<name>`; core.hooksPath and common-dir redirection happen there, not in `find_hook` (see Area 1c). Supports E30/E31 and the installer advice to resolve the target with `git rev-parse --git-path hooks/pre-push`.
- Line 21: the only test is `access(path, X_OK)`. A file that exists but lacks an execute bit for the caller fails with `errno == EACCES`; a missing file fails with `ENOENT`. Either way `find_hook` returns `NULL` (line 46), i.e. "no hook", so the push proceeds. This is the mechanism of the E29 fail-open. [Supports E29.]
- Lines 34-44: the hint is printed only when `errno == EACCES` and `advice.ignoredHook` is enabled, and only once per hook name per process (`advise_given` list). A missing hook (ENOENT) prints nothing. `-c advice.ignoredHook=false` (E29) only suppresses the hint; it does not change the return value (still `NULL`, still fail-open).
- Lines 22-31: the `STRIP_EXTENSION` retry (appending an extension, `.exe`) is compiled in only on builds that define the macro (Windows builds; see Area 1c for the verification status); on the installed Linux build this block is absent. If the retry also fails, the original errno is restored so the advice decision uses the first lookup's errno.
- Consequence for the L2 guard: an executable bit is a hard prerequisite. An installer that leaves the hook at mode 0400/0600 (as `publish()` deliberately does for its JSON payloads) turns the guard into a silent no-op apart from the advisory hint.

### Area 1b: `access(2)` semantics behind line 21 — HIGH

**Source:** https://man7.org/linux/man-pages/man2/access.2.html (official man-pages; reliability high).
- `access()` checks the caller's "real UID and GID", not the effective IDs.
- A denied `X_OK` returns -1 with `errno = EACCES`.
- For root (a privileged process), `X_OK` on a regular file succeeds if "execute permission is enabled for any" of owner, group or other; with no execute bit at all it fails even for root. So mode 0400 fails for everyone, including root.
- Mount option: "MS_NOEXEC flag is honored" since Linux 2.6.20, so a hook on a `noexec` mount fails `X_OK` with EACCES and is skipped (fail-open, with the ignoredHook hint). A read-only mount does not defeat `X_OK` (EROFS applies only to write checks).
- Relation to codebase: extends E29. Two further fail-open causes beyond a missing bit: a `noexec` mount for the hooks directory, and a hook whose execute bit is set only for an owner/group that does not match the pushing user's real UID/GID (e.g. mode 0700 owned by a different user). The installer should verify with `access(path, X_OK)` as the pushing user after publishing (Python: `os.access(path, os.X_OK)`).

### Area 1c: the pre-push call site, hook path redirection, `.exe` fallback and exec failure (v2.47.3) — HIGH

All quoted from the v2.47.3 tag (fetched from raw.githubusercontent.com/git/git/v2.47.3/...; official source, reliability high).

**pre-push does not go through `run_hooks_opt`; it calls `find_hook` directly** — https://github.com/git/git/blob/v2.47.3/transport.c

```c
1293		const char *hook_path = find_hook(the_repository, "pre-push");
1294	
1295		if (!hook_path)
1296			return 0;
...
1305		if (start_command(&proc)) {
1306			finish_command(&proc);
1307			return -1;
1308		}
...
1410		if (!(flags & TRANSPORT_PUSH_NO_HOOK))
1411			if (run_pre_push_hook(transport, remote_refs))
1412				goto done;
```

- Lines 1295-1296 are the literal fail-open: no executable hook means `return 0`, and the push continues. There is no `error_if_missing` option on this path (contrast `hook.c` `run_hooks_opt` lines 155-161, where `error_if_missing` can turn a missing hook into `error("cannot find a hook named %s", ...)`; pre-push never reaches that code). [Supports E29; extends it with the exact line.]
- Line 1410: `TRANSPORT_PUSH_NO_HOOK` (set by `git push --no-verify`) skips the hook entirely. This is a known bypass outside this file's scope (noted for the synthesis, not researched here).
- Lines 1305-1307: if the hook IS found but `start_command` fails, the function returns -1 and the push is aborted (`goto done`), i.e. fail-closed. So an executable but broken hook blocks pushes; a non-executable hook allows them.

**Generic hook runner (for comparison)** — https://github.com/git/git/blob/v2.47.3/hook.c lines 155-161:

```c
155		if (!hook_path && !options->error_if_missing)
156			goto cleanup;
157	
158		if (!hook_path) {
159			ret = error("cannot find a hook named %s", hook_name);
160			goto cleanup;
161		}
```

**Hook directory redirection** — https://github.com/git/git/blob/v2.47.3/path.c

```c
104		{ 0, 1, 1, "hooks" },
...
402		else if (git_hooks_path && dir_prefix(base, "hooks"))
403			replace_dir(buf, git_dir_len + 5, git_hooks_path);
404		else if (repo->different_commondir)
405			update_common_dir(buf, git_dir_len, repo->commondir);
```

- Line 104: `hooks` is in `common_list`, so from a linked worktree `hooks/...` resolves into the common dir. [Supports E30.]
- Lines 402-403: when `core.hooksPath` is set (`git_hooks_path`), the `hooks/` prefix is replaced by it, checked before (and instead of) the common-dir rewrite. A per-worktree `core.hooksPath` (via `extensions.worktreeConfig`) therefore redirects the lookup for that worktree only. [Supports E31.] `git rev-parse --git-path` uses the same git-path machinery, so `git rev-parse --git-path hooks/pre-push`, run from the same worktree with the same config, returns the path `find_hook` will test. (Inference from shared code path; E30/E31 observed it empirically.)
- Docs at the same tag, https://github.com/git/git/blob/v2.47.3/Documentation/config/core.txt lines 499-508: "By default Git will look for your hooks in the `$GIT_DIR/hooks` directory." and "The path can be either absolute or relative. A relative path is taken as relative to the directory where the hooks are run".

**`.exe` fallback platforms** — https://github.com/git/git/blob/v2.47.3/config.mak.uname: `-DSTRIP_EXTENSION=\".exe\"` appears only in the `Windows` block (line 504) and the `MINGW` block (line 696). The `Linux` block (line 49) does not define it, so on Linux the `#ifdef STRIP_EXTENSION` lines 22-31 of `hook.c` are not compiled. (Assumes the installed git was built with upstream's defaults; a distro could pass extra CFLAGS. UNVERIFIED for the specific package, LOW impact.)

**Exec failure inside a found hook** — https://github.com/git/git/blob/v2.47.3/run-command.c

```c
415		/*
416		 * Add SHELL_PATH so in the event exec fails with ENOEXEC we can
417		 * attempt to interpret the command with 'sh'.
418		 */
419		strvec_push(out, SHELL_PATH);
...
850			execve(argv.v[1], (char *const *) argv.v + 1,
851			       (char *const *) childenv);
852			if (errno == ENOEXEC)
853				execve(argv.v[0], (char *const *) argv.v,
854				       (char *const *) childenv);
```

- An executable hook with no `#!` line (ENOEXEC) is re-run with `sh`. A hook whose `#!` interpreter is missing fails exec with ENOENT inside the child; how that maps to the push outcome (start_command failure vs. a non-zero hook exit) was not traced line by line here, but both paths make `run_pre_push_hook` return non-zero and abort the push. Takeaway for the installer: the executable bit is the gate that fails open; content errors fail closed.

**Docs at the same tag:**
- https://github.com/git/git/blob/v2.47.3/Documentation/githooks.txt lines 16-18: "Hooks are programs you can place in a hooks directory to trigger actions at certain points in git's execution. Hooks that don't have the executable bit set are ignored."
- https://github.com/git/git/blob/v2.47.3/Documentation/config/advice.txt lines 58-60: "ignoredHook:: Shown when a hook is ignored because the hook is not set as executable." (git-scm.com/docs/git-config renders the same advice list.) The advice is a hint only; nothing in the docs or source makes a non-executable hook an error.
- githooks.txt lines 238-239 (pre-push): "This hook is called by linkgit:git-push[1] and can be used to prevent a push from taking place."

Version note (f): the X_OK test plus the `advice.ignoredHook` hint is what v2.47.3 ships (installed git 2.47.3, E29 matches the source exactly). I did not trace `find_hook` across older releases; claims about other git versions are UNVERIFIED here.

---

## Area 2: Linux no-replace publication primitives — HIGH

### 2a. `link(2)` / `linkat(2)` — https://man7.org/linux/man-pages/man2/link.2.html (official; high)
- Governing sentence (verbatim): "If newpath exists, it will not be overwritten." Error: `EEXIST` "newpath already exists" (paraphrased by the fetch tool; the error name is exact).
- Cross-mount: `EXDEV` when oldpath and newpath are on different mounts, even if the same filesystem is mounted at both. Temp file and final name must be in the same directory/mount; `publish()` satisfies this (both relative to `parent`).
- `EPERM` if the filesystem does not support hard links (e.g. some FUSE/vfat), if `fs.protected_hardlinks` denies it (Linux 3.6+), or if the source is immutable/append-only.
- Symlinks: since Linux 2.0, `link()` does not dereference a symlink oldpath; `linkat()` follows only with `AT_SYMLINK_FOLLOW` (Linux 2.6.18+). `publish()` passes `follow_symlinks=False` (no `AT_SYMLINK_FOLLOW`), and the temp file was created by itself with `O_EXCL|O_NOFOLLOW`, so the source is a known regular file.
- `AT_EMPTY_PATH` (Linux 2.6.39+) links the file referred to by `olddirfd` directly but needs `CAP_DAC_READ_SEARCH`; the unprivileged alternative is `/proc/self/fd/N` plus `AT_SYMLINK_FOLLOW`.
- NFS: the server may create the link and then fail before replying, so a reported error does not prove the link was not created; check with `stat()`.
- Atomicity: the page makes no explicit "atomic" statement. The no-overwrite rule is enforced by the kernel inside one directory-entry insertion (the name either appears pointing at the complete inode or the call fails with EEXIST); a concurrent reader sees either no file or the complete file, never a partial one, because the content was written before the name existed. This is the standard reasoning behind link-based publishing, but it is an inference, not a man-page quote.
- Relation to `publish()`: SUPPORTS. `os.link` -> `linkat` is the correct no-replace primitive; EEXIST on a lost race is exactly what the codebase observed (file 01).

### 2b. `open(2)` with `O_CREAT|O_EXCL` — https://man7.org/linux/man-pages/man2/open.2.html (official; high)
- Must create the file; if it exists the call fails with `EEXIST`. With `O_CREAT|O_EXCL`, symlinks are not followed: if pathname is a symlink, open fails "regardless of where the symbolic link points."
- NFS: `O_EXCL` is supported only on NFSv3 or later with Linux 2.6 or later; otherwise lock-file schemes built on it race.
- `O_NOFOLLOW`: a symlink as the final component gives `ELOOP` (earlier components are still followed).
- Mode at creation: "(mode & ~umask)" for a file without a default ACL; with a default ACL on the parent, umask is ignored and the ACL governs (umask(2): "the umask is ignored").
- Important limitation: `O_CREAT|O_EXCL` on the FINAL name is no-replace and atomic as a *name claim*, but the file is visible empty/partial while it is being written. A reader (git) could `access(X_OK)` and exec a half-written hook. That is why `publish()` writes to a temp name first and links last. Relation: SUPPORTS the two-step design in `publish()`; direct `O_EXCL` on the final hook name would be no-replace but NOT atomic for readers.

### 2c. `O_TMPFILE` + `linkat` — same open(2) page (official; high)
- Introduced in Linux 3.11. Filesystems: ext2/ext3/ext4, UDF, Minix, tmpfs at 3.11; XFS 3.15; Btrfs and F2FS 3.16; ubifs 4.9. Missing support: `EOPNOTSUPP`; on kernels without `O_TMPFILE`, `EISDIR`/`ENOENT` (callers must check both).
- Requires `O_WRONLY` or `O_RDWR`; mode is applied as with `O_CREAT` (so umask applies).
- "O_TMPFILE | O_EXCL" forbids ever linking the file; without `O_EXCL`, `linkat()` can give it a name. Unprivileged recipe: `linkat(AT_FDCWD, "/proc/self/fd/N", dirfd, "name", AT_SYMLINK_FOLLOW)` (requires mounted /proc); `AT_EMPTY_PATH` needs `CAP_DAC_READ_SEARCH`.
- Lost race: `linkat` fails with `EEXIST` (same as 2a); the unnamed inode disappears when the fd closes, so there is no temp name to clean up and no leftover on crash.
- Python: `os.O_TMPFILE` "only available on Linux Kernel 3.11 or newer" (docs.python.org/3/library/os.html). `os.link(f"/proc/self/fd/{fd}", name, dst_dir_fd=parent, follow_symlinks=True)` maps to `linkat(..., AT_SYMLINK_FOLLOW)`.
- Relation to `publish()`: EXTENDS. Same EEXIST semantics, but removes the visible dot-temp name and the `finally: unlink` step. Costs: depends on /proc and filesystem support; not portable to macOS. `publish()`'s named-temp approach is the portable equivalent and needs no change to be correct.

### 2d. `rename(2)` / `os.rename` / `os.replace` — https://man7.org/linux/man-pages/man2/rename.2.html, https://docs.python.org/3/library/os.html (official; high)
- rename(2): if newpath exists it is atomically replaced, "there is no point at which another process attempting to access newpath will find it missing."
- Python `os.rename`: "If both are files, _dst_ will be replaced silently if the user has permission." (Unix; Windows raises FileExistsError.) "If successful, the renaming will be an atomic operation (this is a POSIX requirement)." `os.replace`: "If _dst_ exists and is a file, it will be replaced silently if the user has permission."
- Relation: CONTRADICTS the requirement "never replace an existing hook file". Plain rename/replace is atomic for readers but silently overwrites; a lost race is not reported at all. Do not use for the installer's final step. (A check-then-rename is a TOCTOU race.)

### 2e. `renameat2(..., RENAME_NOREPLACE)` — rename(2) page (official; high)
- `RENAME_NOREPLACE`: do not overwrite newpath; fail with `EEXIST` if it exists. Cannot be combined with `RENAME_EXCHANGE` (`EINVAL`). `EINVAL` also if the filesystem does not support the flag.
- `RENAME_EXCHANGE`: atomically swap two existing names (`ENOENT` if newpath missing). Not a no-replace primitive; it would put the old hook at the temp name.
- Versions: `renameat2()` syscall Linux 3.15; glibc wrapper 2.28. `RENAME_NOREPLACE` filesystem support: ext4 3.15; btrfs, tmpfs, cifs 3.17; xfs 4.0; ext2, minix, reiserfs, jfs, vfat, bpf and others 4.9. The page gives no overlayfs-specific version (UNVERIFIED for overlayfs).
- Installed kernel 6.8.0-147-generic is far above every listed version (3.15 / 3.17 / 4.0 / 4.9), so the kernel is not a constraint; the remaining risk is a filesystem without support (EINVAL), which the installer must treat as an error, not fall back to plain rename.
- Python: the `os` module exposes no `renameat2`/`RENAME_NOREPLACE` (docs.python.org/3/library/os.html has no such entry); it would need `ctypes` on glibc's `renameat2` or `syscall`. Relation: EXTENDS; equivalent guarantee to link EEXIST, but needs ctypes and adds a filesystem-support failure mode; `os.link` gives the same no-replace guarantee in the stdlib.
- NFS: rename(2) warns that a reported failure does not prove the rename did not happen (server crash plus retried RPC).

### 2f. `fchmod(2)` and umask — https://man7.org/linux/man-pages/man2/chmod.2.html, https://man7.org/linux/man-pages/man2/umask.2.html (official; high)
- umask(2): applies to "open(2), mkdir(2), and other system calls" that create files, computed as `mode & ~umask` (example "0666 & ~022 = 0644"); a default ACL on the parent replaces the umask.
- chmod(2) describes `mode` as the new permission bits and does not mention umask; the umask(2) page lists only creating calls. So `fchmod` sets the mode exactly (subject only to the S_ISGID clearing rule and `EPERM` if the caller does not own the file; `EROFS` on a read-only filesystem). Python docs: "Umask affects creation permissions", `os.fchmod(fd, mode)` "Change the mode of the file given by fd to the numeric mode." (Inference from absence in chmod(2); confirmed by experiment in Area 3.)
- Relation: SUPPORTS `publish()`'s choice to create at 0600 and `fchmod` afterwards. For the hook, the same step must set an executable mode (for example 0755, or 0700 if only the owner pushes), because creating with mode 0755 under a restrictive umask (077 in the batch policy, 022 typical) could drop group/other execute bits; `fchmod` after creation is umask-independent.

### 2g. Durability (man page plus community context) — MEDIUM
- https://man7.org/linux/man-pages/man2/fsync.2.html (official; high): file-level `fsync()` "does not necessarily ensure" the directory entry is durable; "an explicit fsync() on a file descriptor for the directory is also needed."
- LWN "Atomicity vs durability" https://lwn.net/Articles/323412/ and Ts'o on delayed allocation https://lwn.net/Articles/323170/ (reputable kernel journalism; medium-high): atomic name publication and crash durability are separate guarantees; the robust sequence is write temp, `fsync` file, publish name, `fsync` directory. "How to (Not) Lose Your Data", OLS 2009 https://www.kernel.org/doc/mirror/ols2009.pdf describes the same sequence.
- Relation: EXTENDS. `publish()` (lines 164-174) has no `fsync`; it is atomic for concurrent readers but a crash right after line 172 could lose the new name or leave it pointing at unflushed data. For a hook, a lost name after a crash means E29-style fail-open (no hook, push proceeds), so an installer may add `os.fsync(fd)` before `os.link` and `os.fsync(parent)` after it. Option, not a defect in the current JSON use.

### 2h. Community and secondary sources on `O_TMPFILE` + `linkat` — MEDIUM
- GNU C Library manual, Open-time Flags https://snapshots.sourceware.org/glibc/trunk/latest/manual/html_node/Open_002dtime-Flags.html (official glibc docs; high): "The temporary file can later be given a name using `linkat`, turning it into a regular file." The manual frames this as preparing content, permissions and xattrs before the file becomes visible. It reports `EINVAL` when kernel support is absent and `EOPNOTSUPP` when the filesystem lacks support.
  - DISCREPANCY: open(2) BUGS says kernels without `O_TMPFILE` fail with `EISDIR` or `ENOENT` (because old kernels ignore the unknown bit and see `O_DIRECTORY`-like behaviour), while the glibc manual says `EINVAL`. A robust fallback should treat `EISDIR`, `ENOENT`, `EINVAL` and `EOPNOTSUPP` as "O_TMPFILE unavailable". Irrelevant on the installed 6.8 kernel except for filesystems without support.
- Blog "Write files without a cleanup race: O_TMPFILE" https://dixon.cx/blog/write-files-without-cleanup-race-o-tmpfile.html and rust-atomic-write-file issue https://github.com/andreacorbellini/rust-atomic-write-file/issues/6 (blog/forum; low-medium; titles from search results, contents not fetched): community use of `O_TMPFILE` to avoid leftover temp files. Not relied on for any claim.
- google/renameio issue 39 https://github.com/google/renameio/issues/39 surfaced in search; fetch timed out, contents UNVERIFIED and not relied on.

### 2i. overlayfs and `O_TMPFILE` — HIGH (explains an experiment result)
- LKML "[GIT PULL] overlayfs update for 6.10", Miklos Szeredi, 2024-05-22, https://lkml.iu.edu/hypermail/linux/kernel/2405.2/05667.html (maintainer pull request; high): lists "Add tmpfile support" and "ovl: implement tmpfile". So `O_TMPFILE` opened directly on an overlayfs mount needs Linux 6.10 or later.
- The installed kernel 6.8.0-147-generic is BELOW 6.10. Area 3 observed `O_TMPFILE` failing with EOPNOTSUPP (Python prints the alias ENOTSUP, errno 95) on this host's `/` overlay mount, which holds `/tmp`. The open(2) table (Area 2c) does not list overlayfs at all, so this is a gap in the man page rather than a contradiction.
- Consequence: an installer cannot rely on `O_TMPFILE` in container-style environments on pre-6.10 kernels; the named-temp plus `link` pattern (`publish()`) works on overlay (observed in Area 3, steps 3 and 8).

---

## Area 3: Experiment on the installed host (kernel 6.8.0-147-generic, git 2.47.3) — HIGH

Sandbox: `/tmp/web02-sandbox.pVSjes6U` (created with `mktemp -d /tmp/web02-sandbox.XXXXXXXX`, path recorded in the header before running, removed afterwards with `rm -rf -- /tmp/web02-sandbox.pVSjes6U`; a follow-up `ls -d` printed "No such file or directory"). The script `exp.py` was written inside the sandbox; all files, the bare remote and the working repo were inside it. Git ran with `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null HOME=<sandbox>`, so no user or system config or hooksPath applied. The only push target was the local bare repo `<sandbox>/remote<pid>.git`. The first run aborted at step 4 (O_TMPFILE raised `OSError: [Errno 95] Operation not supported`); the script was changed to report and skip O_TMPFILE when unsupported (no retry outside the sandbox) and run again.

Command (second run):

```text
cd /tmp/web02-sandbox.pVSjes6U && uv run --no-project python /tmp/web02-sandbox.pVSjes6U/exp.py /tmp/web02-sandbox.pVSjes6U "$(git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 rev-parse --path-format=absolute --git-common-dir)"
```

The installer function tested in step 8 (`publish_exec`), same shape as `publish()` plus an executable mode and fsync:

```python
def publish_exec(path, data):
    parent = os.open(os.path.dirname(path), os.O_RDONLY | os.O_DIRECTORY)
    name = os.path.basename(path)
    tmp = '.' + name + '.' + os.urandom(8).hex()
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
        try:
            os.write(fd, data)
            os.fchmod(fd, 0o755)
            os.fsync(fd)
        finally:
            os.close(fd)
        try:
            os.link(tmp, name, src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
        finally:
            os.unlink(tmp, dir_fd=parent)
        os.fsync(parent)
    finally:
        os.close(parent)
```

The test hook read stdin lines and exited 1 when the remote ref was `refs/heads/main` or `refs/heads/master`.

Verbatim output (second run; `$SANDBOX` substituted by the script for the sandbox path):

```text
kernel 6.8.0-147-generic python 3.11.15
sandbox fs ('/', 'overlay')
git common dir fs ('/home/coder', 'ext4')
1a create 0755 under umask 077 -> 0o700
1b after fchmod(0755) under umask 077 -> 0o755
2a O_EXCL existing -> EEXIST content b'OLD'
2b O_EXCL on dangling symlink -> EEXIST symlink target still missing: True
3a link onto existing -> FileExistsError EEXIST content b'OLD'
3b link onto absent name -> ok, content b'NEW'
4x O_TMPFILE on overlay -> ENOTSUP (not retried elsewhere: sandbox-only rule)
5 os.rename onto existing -> no error, content b'NEW'
6a renameat2 NOREPLACE onto existing -> rc -1 EEXIST content b'OLD'
6b renameat2 NOREPLACE onto absent -> rc 0 content b'NEW'
6c glibc glibc 2.41
7 access X_OK mode 0o400 -> False
7 access X_OK mode 0o600 -> False
7 access X_OK mode 0o700 -> True
7 access X_OK mode 0o755 -> True
8a hook path $SANDBOX/work728375/.git/hooks/pre-push pre-existing: False
8b installed mode 0o755 X_OK True
8c second install -> FileExistsError EEXIST hook unchanged: True
8d hooks dir entries: ['applypatch-msg.sample', 'commit-msg.sample', 'fsmonitor-watchman.sample', 'post-update.sample', 'pre-applypatch.sample', 'pre-commit.sample', 'pre-merge-commit.sample', 'pre-push', 'pre-push.sample', 'pre-rebase.sample', 'pre-receive.sample', 'prepare-commit-msg.sample', 'push-to-checkout.sample', 'sendemail-validate.sample', 'update.sample']
8e push main rc 1 stderr: L2 guard: push to refs/heads/main refused
error: failed to push some refs to '$SANDBOX/remote728375.git'
8f push feature rc 0
8g push main with hook 0644 rc 0 stderr: hint: The '.git/hooks/pre-push' hook was ignored because it's not set as executable.
hint: You can disable this warning with `git config advice.ignoredHook false`.
To $SANDBOX/remote728375.git
 * [new branch]      main -> main
exit=0
```

What it confirms:
- 1a/1b: creation mode is masked by umask (0755 under umask 077 became 0700); `fchmod` is not (0755 exact). Confirms Area 2f.
- 2a/2b: `O_CREAT|O_EXCL` refuses an existing file and a dangling symlink with EEXIST and does not create the symlink target. Confirms Area 2b.
- 3a/3b and 8c: `link` onto an existing name raises `FileExistsError` (EEXIST) and leaves the existing content untouched. Confirms Area 2a and the codebase's file-01 observation.
- 4x: `O_TMPFILE` is not supported on this host's overlay `/tmp` under kernel 6.8 (Area 2i). Not tested on ext4 because writing outside `/tmp` is not allowed in this task; the git common dir lives on ext4 (`/home/coder`), where open(2) says `O_TMPFILE` has worked since 3.11 (UNVERIFIED on this host).
- 5: `os.rename` silently replaced an existing file. Confirms Area 2d (unsuitable).
- 6a/6b: `renameat2(RENAME_NOREPLACE)` through glibc 2.41's wrapper (>= 2.28) works on overlay with kernel 6.8 and fails with EEXIST without touching the target. The rename(2) page lists no overlayfs version; this run is the evidence for this host only.
- 7: `access(X_OK)` (real uid, non-root here) is false for 0400 and 0600, true for 0700 and 0755. So `publish()`'s 0400 mode would make git skip a hook.
- 8a: in a non-worktree repo with no hooksPath, `git rev-parse --git-path hooks/pre-push` gives `.git/hooks/pre-push`.
- 8d: no leftover temp name in the hooks directory after the install and the refused second install.
- 8e/8f: the executable hook refused `refs/heads/main` (push rc 1, ref not updated) and allowed another branch.
- 8g: after `chmod 0644` the same hook was skipped, the hint text matched `hook.c` lines 39-42 verbatim (with the relative path `.git/hooks/pre-push`), and the push to main succeeded. Reproduces file 04 E29 independently.

---

## Primitive comparison table

| Primitive | Replaces existing target (yes/no) | Atomic for readers | Lost-race error | Kernel or filesystem requirement | Source URL |
|---|---|---|---|---|---|
| `open(final, O_CREAT\|O_EXCL)` writing in place | no | no: the name exists while empty/partial; a reader can see a half-written file | `EEXIST` (also for a symlink at the name) | any Linux; NFS needs NFSv3+ and Linux 2.6+ | https://man7.org/linux/man-pages/man2/open.2.html |
| temp via `O_CREAT\|O_EXCL` + `link`/`linkat(tmp, final)` (the `publish()` pattern) | no ("If newpath exists, it will not be overwritten.") | yes: name appears only after content and mode are set (inference; observed in Area 3) | `EEXIST` (`FileExistsError` in Python) | same mount (`EXDEV` otherwise); filesystem must support hard links (`EPERM` otherwise); NFS reply can be lost | https://man7.org/linux/man-pages/man2/link.2.html |
| `O_TMPFILE` + `linkat(/proc/self/fd/N, final, AT_SYMLINK_FOLLOW)` | no | yes, and no visible temp name | `EEXIST` | Linux 3.11+; ext2/3/4, UDF, Minix, tmpfs 3.11; XFS 3.15; Btrfs, F2FS 3.16; ubifs 4.9; overlayfs 6.10; needs /proc (or `AT_EMPTY_PATH` with `CAP_DAC_READ_SEARCH`); must not add `O_EXCL` | https://man7.org/linux/man-pages/man2/open.2.html, https://lkml.iu.edu/hypermail/linux/kernel/2405.2/05667.html |
| `rename(2)` / `os.rename` / `os.replace` | yes (silently) | yes ("no point at which another process ... will find it missing") | none: the race is lost silently | any; same mount (`EXDEV`) | https://man7.org/linux/man-pages/man2/rename.2.html, https://docs.python.org/3/library/os.html |
| `renameat2(..., RENAME_NOREPLACE)` | no | yes | `EEXIST`; `EINVAL` if the filesystem lacks support | syscall Linux 3.15, glibc wrapper 2.28; ext4 3.15; btrfs, tmpfs, cifs 3.17; xfs 4.0; ext2, minix, reiserfs, jfs, vfat, bpf 4.9; overlayfs not listed (worked on this host, Area 3); not in Python `os` (needs ctypes) | https://man7.org/linux/man-pages/man2/rename.2.html |
| `renameat2(..., RENAME_EXCHANGE)` | swaps (the old file ends up at the temp name) | yes | `ENOENT` if the target is missing | Linux 3.15 plus filesystem support | https://man7.org/linux/man-pages/man2/rename.2.html |
| `fchmod(fd, mode)` (sets mode; not a publication step) | n/a | n/a (do it before the name is published) | `EPERM` if not owner; `EROFS` | any; umask does not apply (observed step 1b) | https://man7.org/linux/man-pages/man2/chmod.2.html, https://man7.org/linux/man-pages/man2/umask.2.html |

Installed kernel 6.8.0-147-generic satisfies every listed kernel minimum except overlayfs `O_TMPFILE` (needs 6.10).

---

## Discrepancies and notes against the codebase and earlier files

1. No contradiction with `publish()` (lines 164-174): link-based publication is the correct no-replace, reader-atomic primitive. The one property that must differ for a hook is the mode: `publish()` sets 0400 (line 171), which `access(X_OK)` rejects (Area 3 step 7), so reusing `publish()` unchanged for a hook would install a guard that git ignores (fail-open, E29).
2. `publish()` has no `fsync` (file or directory). Atomic for readers, not durable across a crash. For a hook, a lost name after a crash is fail-open. Extension, not a contradiction.
3. open(2) BUGS says kernels without `O_TMPFILE` give `EISDIR`/`ENOENT`; the glibc manual says `EINVAL`. Treat all of `EISDIR`, `ENOENT`, `EINVAL`, `EOPNOTSUPP` as "unsupported" if `O_TMPFILE` is ever used.
4. open(2)'s `O_TMPFILE` filesystem list omits overlayfs; LKML shows support from 6.10; this host (6.8, overlay `/tmp`) returned EOPNOTSUPP. Consistent, but it means `O_TMPFILE` is not usable in this environment's `/tmp`.
5. rename(2) lists no overlayfs version for `RENAME_NOREPLACE`; it worked on this host's overlay under 6.8. Host-specific evidence only.
6. The E29 hint text in file 04 matches `hook.c` v2.47.3 lines 39-42 verbatim; the hint appears only for `EACCES`, not for a missing hook. E30/E31 match `path.c` lines 104 and 402-405.
7. The `.exe` fallback (`hook.c` lines 22-31) is Windows/MINGW only per `config.mak.uname`; not active on the installed Linux git (distro build flags UNVERIFIED).

---

## Key External Findings

- git v2.47.3 decides "hook present" solely with `access(path, X_OK)` (`hook.c` line 21). A non-executable or missing hook makes `find_hook` return NULL (line 46), and `transport.c` lines 1295-1296 then `return 0`, so the push proceeds. This is the exact source of the E29 fail-open.
- The `advice.ignoredHook` hint is printed only when `errno == EACCES` and the advice is enabled, once per hook name per process (`hook.c` lines 34-44). Disabling it never changes the outcome. A missing hook prints nothing.
- `access()` uses the real UID/GID; root needs at least one execute bit; a `noexec` mount gives EACCES (access(2)). Wrong owner with mode 0700, or a `noexec` hooks directory, also fails open.
- An executable hook that exits non-zero, or that git cannot start, aborts the push (`transport.c` lines 1305-1307, 1410-1412): content failures fail closed; only the executable-bit and path check fails open.
- `git push --no-verify` sets `TRANSPORT_PUSH_NO_HOOK` and skips the hook (`transport.c` line 1410). Out of scope here; relevant to the L2 threat model.
- The hook path is the git-path `hooks/pre-push`, redirected by `core.hooksPath` (`path.c` lines 402-403) or into the common dir from a linked worktree (`path.c` line 104). `git rev-parse --git-path hooks/pre-push` resolves it the same way.
- No-replace publication primitives: `link`/`linkat` (EEXIST), `O_CREAT|O_EXCL` (EEXIST, but not reader-atomic when writing in place), `O_TMPFILE`+`linkat` (EEXIST, no temp name, filesystem-dependent), `renameat2 RENAME_NOREPLACE` (EEXIST, or EINVAL if unsupported; not in Python `os`). `rename`/`os.replace` always replace and must not be used.
- `renameat2` needs Linux 3.15 and glibc 2.28; `RENAME_NOREPLACE` filesystem support runs from 3.15 (ext4) to 4.9. Overlayfs `O_TMPFILE` needs 6.10. The installed 6.8 kernel meets all of these except overlayfs `O_TMPFILE`, which failed with EOPNOTSUPP on `/tmp` here.
- Creation mode is `mode & ~umask` (unless a default ACL applies); `fchmod` sets the mode exactly. Observed: 0755 at creation under umask 077 gave 0700, while `fchmod(0755)` gave 0755.
- Crash durability needs `fsync(file)` before publishing and `fsync(directory)` after (fsync(2), LWN); `publish()` does neither.
- Observed end to end on git 2.47.3: a hook installed with temp + `fchmod 0755` + `link` blocked a push to `refs/heads/main`, a second install raised EEXIST and left the hook unchanged, and the same hook at 0644 was skipped with the hint while the push to main succeeded.

## Recommendations from External Research

1. Install the pre-push hook with the existing `publish()` shape, changing only the mode and adding fsync: create a dot-prefixed unique temp in the target directory with `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW` at 0600, write, `fchmod` the fd to an executable mode (0755, or 0700 if only the owner pushes), `fsync` the fd, `os.link(tmp, "pre-push", src_dir_fd=..., dst_dir_fd=..., follow_symlinks=False)`, always unlink the temp in `finally`, then `fsync` the directory fd. This is no-replace, reader-atomic, umask-independent and works on overlay and ext4 with the stdlib alone. Verified in Area 3 step 8.
2. Set the executable mode with `fchmod` on the fd, never through the `mode` argument of `open` alone, because umask (or a default ACL) can strip the execute bits git needs.
3. Resolve the target with `git rev-parse --path-format=absolute --git-path hooks/pre-push`, run from the worktree being protected, so `core.hooksPath` (global, local or per-worktree) and the common-dir redirection are honoured. If the directory is missing, fail rather than silently create a different path.
4. Treat `FileExistsError` as "a hook is already there", never as success: compare the existing file with the expected content and check `os.access(path, os.X_OK)` (and `os.stat` owner and mode); report a non-matching or non-executable existing hook as an error, because refusing to replace a non-executable hook leaves pushes unguarded (E29).
5. After installing, verify with `os.access(path, os.X_OK)` as the pushing user and check that the mount is not `noexec`; a hook that fails this check is silently skipped by git.
6. Do not use `os.rename`/`os.replace` for the final step (silent replacement). Do not depend on `O_TMPFILE` (EOPNOTSUPP on overlayfs below 6.10, as on this host's `/tmp`) or on `renameat2` (needs ctypes and can return EINVAL on unsupported filesystems); neither gives an extra guarantee over `link` for this use.
7. Do not set `advice.ignoredHook=false` in the installer or the guard; the hint is the only visible signal that the guard was skipped.
8. For the synthesis: the hook file and its executable bit live in a directory the agent can normally write, and `git push --no-verify` skips hooks entirely. The executable-bit requirement makes L2 easy to disable, so a pre-flight `access(X_OK)` check (or another layer) is needed if L2 is to be relied on.

**Source basis:** official man pages, the git v2.47.3 source and docs, Python docs, the glibc manual, LWN and an LKML maintainer pull request, plus one sandboxed experiment on this host.

