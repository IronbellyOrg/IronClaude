"""Static selection contracts, not an executable parser or live dispatch test."""

from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "src/superclaude"


def _read(relative: str) -> str:
    return (SRC / relative).read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def _assert_no_native_model_field(section):
    for line in section.splitlines():
        key, separator, _ = line.strip().partition(":")
        assert not (separator and key.strip().strip("\"'") == "model"), line


@pytest.mark.parametrize("selection", ("opus", "sonnet", "haiku", "fable", "default", "inherit"))
@pytest.mark.parametrize("quote", ("", "'", '"'))
def test_native_dispatch_guard_rejects_every_unconditional_model(selection, quote):
    field = f"    model: {quote}{selection}{quote}\n"
    with pytest.raises(AssertionError):
        _assert_no_native_model_field('model_selection: "conditional selection rule"\n' + field)


def test_native_dispatch_guard_allows_explicit_selection_instructions():
    _assert_no_native_model_field('model_selection: "For explicit haiku pass model: haiku; for default omit model"')


def test_builder_default_and_explicit_rotation_contract():
    text = _read("skills/sc-brainstorm-protocol/refs/agent-spec-builder.md")
    rotation = _section(text, "## §Model-Rotation", "## §Instruction-Templates")
    for literal in (
        "assign `default` to every selected persona",
        "quick, standard and deep",
        "Preserve list order and round-robin",
        "Depth never promotes or replaces",
        "explicit --models sonnet,haiku",
        "explicit --models default,opus",
    ):
        assert literal in rotation
    assert "Deep-depth override" not in rotation
    vectors = text.split("## §Round-Trip Test Vectors", 1)[1]
    assert "default:architect,default:refactorer" in vectors
    assert "opus:" not in vectors and "sonnet:" not in vectors
    assert "haiku:" not in vectors
    assert "Strip these characters" in text
    assert "auto_excluded_personas" in text


@pytest.mark.parametrize(
    "path,start,end",
    [
        ("skills/sc-brainstorm-protocol/refs/agent-spec-builder.md", "## §Validation", "## §Token-Budget"),
        ("skills/sc-adversarial-protocol/refs/agent-specs.md", "### Parsing Rules", "### Examples"),
        ("skills/sc-adversarial-protocol/SKILL.md", "    agent_spec_parsing:", "  step_4_common_flags:"),
    ],
)
def test_shared_quote_aware_grammar(path, start, end):
    grammar = _section(_read(path), start, end).lower()
    for literal in ("only outside", "single or double quotes", "default", "fable", "extra segments", "dangling escapes", "trailing text"):
        assert literal in grammar
    assert "decode once" in grammar
    assert "shell-execute" in grammar


def test_builder_serialization_preserves_default_and_escapes_once():
    serialization = _section(
        _read("skills/sc-brainstorm-protocol/refs/agent-spec-builder.md"),
        "## §Serialization", "## §Validation",
    )
    assert r"Escape backslashes first (`\` becomes `\\`), then replace `'` in instructions with `\'`" in serialization
    assert "Decode escapes once in the consumer, never through a shell" in serialization
    assert "`default:architect`" in serialization
    assert "default:architect:'prioritize maintainability'" in serialization


def test_producer_serialization_and_final_output_contract():
    text = _read("skills/sc-brainstorm-protocol/SKILL.md")
    serialization = _section(text, "4. **Serialization with sanitization**", "5. **Token-budget pre-flight**")
    assert "Wrap each instruction in single-quoted strings" in serialization
    assert r"Escape backslashes first, then embedded single-quotes as `\'`" in serialization
    assert "decode once in the consumer, never through a shell" in serialization
    assert "Sanitize all interpolated parameters" in serialization
    output = _section(text, "6. **Final output**", "**Dry-run gate**")
    for selection in ("default:architect:", "default:refactorer:", "default:devops:"):
        assert selection in output


def test_command_examples_and_boundaries_do_not_imply_rotation():
    text = _read("commands/brainstorm.md")
    example = _section(text, "### Cross-domain redesign", "### Blind multi-model comparison")
    assert "5 proposals using the role-permitted configured default" in example
    boundaries = _section(text, "## Boundaries", "## Related Commands")
    assert "rotate only an explicit --models list in its supplied order" in boundaries
    assert "or invent a family rotation when --models is omitted" in boundaries
    for stale in ("3 active aliases", "5 proposals × 3 models", "uses 3 active aliases"):
        assert stale not in text


def test_advocate_consumer_parse_and_validate_contract():
    consumer = _section(
        _read("skills/sc-adversarial-protocol/SKILL.md"),
        "### Advocate Agent Instantiation", "  prompt_generation:",
    )
    for literal in (
        "shared agent_spec_parsing grammar",
        "only outside matching single or double quotes",
        "preserve default marker until dispatch",
        "decode matching quote/backslash escapes once; never shell-execute",
        "Only default, opus, sonnet, haiku, fable",
        "reject inherit, backend IDs and arbitrary gateway aliases",
        "reject empty/extra segments, unmatched quotes, dangling escapes and trailing text",
    ):
        assert literal in consumer


def test_generation_consumes_marker_before_native_dispatch():
    text = _read("skills/sc-adversarial-protocol/SKILL.md")
    generation = text.split("### Mode B Variant Generation", 1)[1]
    assert "For default, omit the native model parameter" in generation
    assert "validated explicit opus, sonnet, haiku or fable alias" in generation
    assert "Preserve this choice on retries and redispatch" in generation
    assert "shared shim rejects disallowed destinations" in generation
    assert 'count_check: "2 ≤ agent_count ≤ 10"' in text


def test_advocacy_assignment_dispatch_and_retry_contract():
    text = _read("skills/sc-adversarial-protocol/SKILL.md")
    dispatch = _section(text, "  task_dispatch_config:", "  mode_a_assignment:")
    assert "If parsed selection is default, omit the native model parameter" in dispatch
    assert "validated explicit opus, sonnet, haiku or fable alias" in dispatch
    assert "every debate round, retry and redispatch" in dispatch
    assert '    model: "{parsed_model}"' not in dispatch
    assignment = _section(text, "  mode_a_assignment:", "  count_validation:")
    assert "without --agents assign default per file" in assignment
    assert "not the current parent model" in assignment
    assert "Preserve a supplied validated list unchanged" in assignment
    mode_a = _section(text, "  step_1_detect_mode:", "  step_3_mode_b_parsing:")
    assert "An optional --agents list is legal in Mode A" in mode_a
    assert "step_3_mode_b_parsing.agent_spec_parsing" in mode_a
    assert "exactly one spec per input file" in mode_a
    reference = _read("skills/sc-adversarial-protocol/refs/agent-specs.md")
    assert "rather than the current parent model" in _section(reference, "### Mode A (Compare)", "### Mode B")
    assert "same selection/persona/instruction and model omission or explicit alias" in reference.split("### Failure Handling", 1)[1]
    command = _section(_read("commands/adversarial.md"), "### Arguments", "## Behavioral Summary")
    assert "one `default` advocate per file" in command
    assert "optional in Mode A" in command


def test_coordinator_and_merge_do_not_choose_families():
    text = _read("skills/sc-adversarial-protocol/SKILL.md")
    for start, end in (
        ("### debate-orchestrator Agent", "### merge-executor Agent"),
        ("### merge-executor Agent", "### Advocate Agents"),
        ("### Merge Executor Dispatch", "### Provenance Annotation System"),
    ):
        section = _section(text, start, end)
        assert "Omit the native model parameter" in section
        assert "configured child default" in section
        assert "opus" not in section and "sonnet" not in section
    merge = _section(text, "### Merge Executor Dispatch", "### Provenance Annotation System")
    assert "Preserve omission on retries and redispatch" in merge
    assert "never inherit the winning advocate's model" in merge


def test_selection_labels_provenance_and_blind_copies():
    text = _read("skills/sc-adversarial-protocol/SKILL.md")
    contract = _section(text, "When invoked by another command", "## Agent Delegation")
    assert 'base_variant: "default:architect"' in contract
    assert "not a served backend" in contract
    assert "otherwise report `unknown`" in contract
    assert "variant-{N}-{model}-{persona or 'default'}.md" in contract
    blind = _section(text, "#### Blind Evaluation", "#### Convergence Plateau Detection")
    assert 'patterns: ["default", "opus", "haiku", "sonnet", "fable"' in blind
    assert "not ordinary prose uses of the word default" in blind
    assert "Original artifacts preserved" in blind


def test_cli_eval_create_keeps_three_defaults_and_explicit_specs():
    text = _read("skills/sc-cli-eval-protocol/SKILL.md")
    inputs = _section(text, "## Input Contract", "## Wave 0")
    assert "default,default,default" in inputs
    assert "Preserve an explicit list unchanged" in inputs
    w3 = _section(text, "### W3", "### W4")
    assert "default,default,default" in w3
    assert "including personas, instructions and order" in w3
    assert "Pass that resolved list to either Mode A or Mode B" in w3
    assert "Coordinator and merge calls omit model independently" in w3
    integration = _section(_read("skills/sc-cli-eval-protocol/refs/integration-map.md"), "## /sc:adversarial", "## /sc:document")
    assert "--agents default,default,default" in integration
    assert "explicit list is forwarded unchanged" in integration
    assert "explicit `--agents sonnet:architect,haiku:qa`" in integration
    command = _section(_read("commands/cli-eval.md"), "## Usage", "## Behavioral Summary")
    assert "`default,default,default`" in command
    assert "forwarded unchanged, in order" in command
    assert "[--agents opus,sonnet,haiku]" not in text


@pytest.mark.parametrize("agent", ("auggie-reviewer", "eval-suite-author", "debate-orchestrator", "merge-executor"))
def test_affected_agents_have_no_frontmatter_model_pin(agent):
    text = _read(f"agents/{agent}.md")
    frontmatter = text.split("---", 2)[1]
    assert not any(line.startswith("model:") for line in frontmatter.splitlines())
    if agent != "auggie-reviewer":
        selection = _section(text, "## Model Selection", "## Tools")
        assert "configured default permitted by their Coder role" in selection
        assert "do not substitute a capability-based preference" in selection


@pytest.mark.parametrize(
    "path,start,end,required",
    [
        ("skills/sc-auggie-review-protocol/SKILL.md", "5. For `--depth deep`", "**Exit criteria**", "when `revagent = default`, pass no `model` argument"),
        ("commands/auggie-review.md", "## Options", "## Behavioral Summary", "configured default"),
        ("skills/sc-brainstorm-protocol/SKILL.md", "2. **Model selection**", "3. **Custom instructions**", "Omitted `--models`: assign `default` to every selected persona"),
        ("skills/sc-brainstorm-protocol/refs/agent-spec-builder.md", "## §Model-Rotation", "## §Instruction-Templates", "Depth never promotes or replaces"),
        ("commands/brainstorm.md", "## Options", "## Examples", "`default` for every proposal"),
        ("skills/sc-adversarial-protocol/refs/agent-specs.md", "#### Model (Required)", "#### Persona", "omit the native model parameter"),
        ("skills/sc-adversarial-protocol/SKILL.md", "### Mode B Variant Generation", "### MCP Integration Layer", "For default, omit the native model parameter"),
        ("skills/sc-adversarial-protocol/SKILL.md", "  task_dispatch_config:", "  mode_a_assignment:", "If parsed selection is default, omit the native model parameter"),
        ("skills/sc-adversarial-protocol/SKILL.md", "### debate-orchestrator Agent", "### merge-executor Agent", "Omit the native model parameter"),
        ("skills/sc-adversarial-protocol/SKILL.md", "### merge-executor Agent", "### Advocate Agents", "Omit the native model parameter"),
        ("skills/sc-adversarial-protocol/SKILL.md", "### Merge Executor Dispatch", "### Provenance Annotation System", "Omit the native model parameter"),
        ("commands/adversarial.md", "### Arguments", "## Options", "one `default` advocate per file"),
        ("skills/sc-cli-eval-protocol/SKILL.md", "### W3", "### W4", "default,default,default"),
        ("skills/sc-cli-eval-protocol/SKILL.md", "### W4", "### W5", "without a native `model` parameter"),
        ("skills/sc-cli-eval-protocol/refs/integration-map.md", "## /sc:adversarial", "## /sc:document", "--agents default,default,default"),
        ("commands/cli-eval.md", "## Options", "## Behavioral Summary", "`default,default,default`"),
    ],
)
def test_complete_affected_selection_inventory(path, start, end, required):
    section = _section(_read(path), start, end)
    assert required in section
    for implicit_pin in ("opus preferred", "highest available"):
        assert implicit_pin not in section
    _assert_no_native_model_field(section)


def test_plugin_brainstorm_affected_sections_match_source():
    root = SRC.parents[1]
    plugin = (root / "plugins/superclaude/commands/brainstorm.md").read_text(encoding="utf-8")
    source = _read("commands/brainstorm.md")
    for text in (plugin, source):
        assert "[--models default|opus|sonnet|haiku|fable,...]" in _section(text, "## Usage", "## Options")
    def model_row(text):
        return next(line for line in text.splitlines() if line.startswith("| `--models`"))

    assert model_row(plugin) == model_row(source)
    for start, end in (
        ("### Codebase feature discovery", "### Deep incident"),
        ("### Cross-domain redesign", "### Blind multi-model"),
        ("### Blind multi-model", "### Dry-run"),
    ):
        assert _section(plugin, start, end) == _section(source, start, end)
    boundaries = _section(plugin, "## Boundaries", "## Related Commands")
    assert "rotate only an explicit --models list in its supplied order" in boundaries
    assert "or invent a family rotation when --models is omitted" in boundaries
    assert "3 active aliases" not in plugin
    assert "5 proposals × 3 models" not in plugin


def test_readme_separates_saved_child_default_parent_and_backend():
    selection = _section(_read("skills/ccsession-tag/README.md"), "### Native child model selection", "The limit is local to ccsession")
    for literal in (
        "ANTHROPIC_MODEL", "$CLAUDE_CONFIG_DIR/settings.json", "~/.claude/settings.json",
        "role start tier", "Parent-only `--model` and `--tier` choices do not replace",
        "project/local/managed settings", "agent-frontmatter choices still override",
        "`default` specification token", "never a native model alias",
        "shim's role check on the resolved destination", "CLAUDE_CODE_SUBAGENT_MODEL_FORCE",
        "never created by the launcher", "not proof of the served backend",
        "Outside tier mode, native",
    ):
        assert literal in selection


def test_command_surfaces_describe_protocol_marker_not_native_alias():
    brainstorm = _read("commands/brainstorm.md")
    row = next(line for line in brainstorm.splitlines() if line.startswith("| `--models`"))
    assert "`default` for every proposal" in row
    assert "without depth promotion" in row
    assert "omits the native model parameter" in row
    adversarial = _read("commands/adversarial.md")
    for section in (adversarial.split("### Arguments", 1)[1].split("## Options", 1)[0], adversarial.split("## Options", 1)[1]):
        assert "selection[:persona[:quoted-instruction]]" in section
        assert "single/double quotes" in section or "single or double quotes" in section
    protocol = _read("skills/sc-brainstorm-protocol/SKILL.md")
    assert "Coder workspaces no longer set these" not in protocol
    assert "not proof of a served backend or role permission" in protocol
