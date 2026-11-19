cf0807971cd4e75cae1f7a055ccac076149c16eb
family stale-docstring: a docstring in render.py still says the shown row keeps the per-row reason text.
search: grep -n -F -e "reason unknown" src/superclaude/cli/observe/render.py
before: 3 hits at 533 (stale), 540, 618 (both accurate)
coupled sites: none other
after: 3 hits at 534, 540, 618, all accurate
