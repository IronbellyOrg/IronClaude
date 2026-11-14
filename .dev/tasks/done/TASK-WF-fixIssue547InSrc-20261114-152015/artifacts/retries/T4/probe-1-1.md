d74617ddffa12304cba21c44149e1f39d6ea0e18
## family shortcut-comment (probe for r1-1)
defect form: a known limit stated only in prose, not as a # shortcut: comment
command: grep -n shortcut: src/superclaude/cli/sweep/probes.py
before: 269:    # shortcut: subprocess.run buffers the whole output and the 8 MiB limit is checked after the 341:    # shortcut: same as ``_orca``: run buffers the output; see the note there (owner ruling 2026-11-12). 
coupled sites: _filter_blocks_status only
## family named-constants (probe for r1-1)
defect form: ALLOWED_GIT indexed inline instead of named constants
command: grep -nE 'ALLOWED_GIT\[[123]\]' src/superclaude/cli/sweep/probes.py
before: 988:    drivers = _filter_drivers(_git(path, *ALLOWED_GIT[1], timeout=timeout, binary=True)) 991:    tracked = _git(path, *ALLOWED_GIT[2], timeout=timeout, binary=True) 995:        path, *ALLOWED_GIT[3], timeout=timeout, stdin=tracked, binary=True 
coupled sites: _filter_blocks_status only
after: 270:    # shortcut: subprocess.run buffers the whole output and the 8 MiB limit is checked after the 342:    # shortcut: same as ``_orca``: run buffers the output; see the note there (owner ruling 2026-11-12). 989:    # shortcut: a filter named only in a submodule's own config is not seen here; the status 
after: 81:CONFIG_LIST, LS_FILES, CHECK_ATTR = ALLOWED_GIT[1], ALLOWED_GIT[2], ALLOWED_GIT[3] 991:    drivers = _filter_drivers(_git(path, *CONFIG_LIST, timeout=timeout, binary=True)) 994:    tracked = _git(path, *LS_FILES, timeout=timeout, binary=True) 997:    attrs = _git(path, *CHECK_ATTR, timeout=timeout, stdin=tracked, binary=True).split( 
