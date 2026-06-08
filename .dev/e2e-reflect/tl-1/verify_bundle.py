from pathlib import Path

root = Path('/config/workspace/IronClaude/.claude/worktrees/ReflectInTaskLists/.dev/e2e-reflect/tl-1/bundle')
for phase in [1, 2]:
    p = root / f'phase-{phase}-tasklist.md'
    lines = p.read_text().splitlines()
    heads = [(i + 1, line) for i, line in enumerate(lines) if line.startswith('### T')]
    last = heads[-1]
    checkpoint = [h for h in heads if 'Checkpoint: End of Phase' in h[1]][-1]
    tail = '\n'.join(lines[last[0] - 1 :])
    print(
        f'phase{phase}: last={last[0]} {last[1]} checkpoint={checkpoint[0]} {checkpoint[1]} '
        f'after_checkpoint={last[0] > checkpoint[0]} exempt={"| Tier | EXEMPT |" in tail} '
        f'reflect_path={"**Reflect Report Path:**" in tail} phase_commit_range={"<phase-commit-range>" in tail} '
        f'sc_reflect={"/sc:reflect" in tail} sc_task={"/sc:task" in tail}'
    )
idx = (root / 'tasklist-index.md').read_text()
print('index_pre_column=', 'Pre-Reflect Sign-off' in idx)
print('index_summary=', 'Reflect Pre Summary' in idx and '{pass: 2, partial: 0, fail: 0}' in idx)
print('depth_map_exists=', (root / 'validation/reflect-pre/depth-map.yaml').exists())
