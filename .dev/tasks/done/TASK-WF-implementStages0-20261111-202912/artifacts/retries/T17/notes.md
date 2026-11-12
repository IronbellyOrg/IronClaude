0f6bc94ef61d927be950167aa9e21f8393183afb
A2 r2-1 F2.1 minor src/superclaude/cli/review/manifest.py:496 ac=scope n,n,n,n publish_files refuses only a shadow effective engine; a manifest whose effective engine is legacy passes the guard and the legacy files would be replaced; the adapter does not publish in legacy mode
A2 r2-1 F2.2 minor src/superclaude/cli/review/manifest.py:446 ac=scope n,n,n,n init on an existing manifest that lacks an engine key ends in an unhandled KeyError (exit 1) instead of a clean refusal; nothing is written
