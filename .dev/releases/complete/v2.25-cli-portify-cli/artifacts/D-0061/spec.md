# D-0061: Prompt Splitting (>300 Lines → portify-prompts.md)

## Status: COMPLETE

## Deliverable
`src/superclaude/cli/cli_portify/prompts.py` — `maybe_split_prompt()` function

## Implementation
```python
def maybe_split_prompt(prompt: str, workdir: Path) -> str:
    if len(prompt.splitlines()) > 300:
        workdir.mkdir(parents=True, exist_ok=True)
        prompts_file = workdir / "portify-prompts.md"
        prompts_file.write_text(prompt, encoding="utf-8")
        return f"[Prompt exceeds 300 lines — full prompt written to {prompts_file}]\n\n@{prompts_file}"
    return prompt
```

## Verification
- 301-line prompt → `portify-prompts.md` written to workdir; reference string returned ✓
- 300-line prompt → original prompt returned unchanged; no file written ✓
- `portify-prompts.md` contains full original prompt content ✓
