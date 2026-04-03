# Worker Governance Patterns for AI-Orchestrated Pipelines

**Topic**: Best practices for governing headless AI worker subprocesses, prompt engineering for subprocess workers, and task verification patterns for AI-orchestrated pipelines.

**Date**: 2026-04-03
**Status**: In Progress
**Research Type**: External web research

---

## Research Questions

1. How do AI orchestration frameworks (CrewAI, AutoGen, LangGraph, etc.) verify task completion beyond exit codes?
2. What patterns exist for output parsing, acceptance criteria checking, and LLM-as-judge verification?
3. How should prompts for headless AI workers be engineered to constrain scope and enforce verification?
4. What multi-agent QA patterns exist -- post-task review agents, adversarial verification?

## Context from Codebase

The IronClaude sprint executor spawns headless claude subprocesses with minimal prompts and judges completion by exit code only (exit 0 = pass). Post-task hooks check structural code quality (wiring, format) but not task-specific acceptance criteria. The worker has access to CLAUDE.md governance and skills but the prompt doesn't invoke them. We want to understand how other AI orchestration systems handle this.

---

