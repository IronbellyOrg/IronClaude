# Pre-remediation line anchors (HEAD 7c4b26b0)

## executor.py
436:            skip_until_idx = 0
442:                            skip_until_idx = i
445:                    skip_until_idx = len(_STAGE_A_STEPS)
447:                if idx < skip_until_idx:
566:        prompt = self._build_prompt(builder_name, step_id=step_id)
718:        _STAGE_B_ORDER = [
724:        if resume_from in _STAGE_B_ORDER:
725:            resume_idx = _STAGE_B_ORDER.index(resume_from)
728:            return _STAGE_B_ORDER.index(substage) >= resume_idx
733:            p.name[:2].isdigit() for p in research_dir.glob("*.md")
1068:    def _build_prompt(self, builder_name: str, step_id: str | None = None) -> str:
1089:        except TypeError:
1096:        except TypeError:
1100:        except TypeError:

## prompts.py + gates.py
src/superclaude/cli/prd/gates.py:7:  1. Reusable checks: _check_verdict_field, _check_no_placeholders
src/superclaude/cli/prd/gates.py:36:def _check_verdict_field(content: str) -> bool | str:
src/superclaude/cli/prd/gates.py:243:    return _check_verdict_field(content)
src/superclaude/cli/prd/gates.py:349:                _check_verdict_field,
src/superclaude/cli/prd/gates.py:397:                _check_verdict_field,
src/superclaude/cli/prd/prompts.py:338:    existing_note = ""
src/superclaude/cli/prd/prompts.py:346:            existing_note = (
src/superclaude/cli/prd/prompts.py:366:{existing_note}
src/superclaude/cli/prd/prompts.py:535:def _parse_agent_block(notes: str, agent_idx: int) -> dict:
src/superclaude/cli/prd/prompts.py:572:def build_investigation_prompt(  # type: ignore[no-redef]
src/superclaude/cli/prd/prompts.py:591:        agent = _parse_agent_block(notes, agent_idx) or {
src/superclaude/cli/prd/prompts.py:604:        return _render_investigation_prompt(
src/superclaude/cli/prd/prompts.py:611:    return _render_investigation_prompt(*args, **{
src/superclaude/cli/prd/prompts.py:617:def _render_investigation_prompt(
src/superclaude/cli/prd/prompts.py:692:def build_web_research_prompt(  # type: ignore[no-redef]
src/superclaude/cli/prd/prompts.py:712:        agent = _parse_agent_block(notes, agent_idx) or {
src/superclaude/cli/prd/prompts.py:725:        return _render_web_research_prompt(
src/superclaude/cli/prd/prompts.py:731:    return _render_web_research_prompt(*args, **{
src/superclaude/cli/prd/prompts.py:737:def _render_web_research_prompt(
src/superclaude/cli/prd/prompts.py:901:def build_synthesis_prompt(  # type: ignore[no-redef]
src/superclaude/cli/prd/prompts.py:931:        return _render_synthesis_prompt(
src/superclaude/cli/prd/prompts.py:937:    return _render_synthesis_prompt(*args, **{
src/superclaude/cli/prd/prompts.py:943:def _render_synthesis_prompt(
src/superclaude/cli/prd/prompts.py:1112:    existing_note = ""
src/superclaude/cli/prd/prompts.py:1125:                existing_note = (
src/superclaude/cli/prd/prompts.py:1144:{existing_note}

## commands.py
23:    Examples:
95:    Examples:
171:def resume(
188:    Examples:
