# Swarm run summary — plain-language template (Wave 5)

Fill from `return-contract.yaml` + `.swarm-state.json`. Keep it short, warm, and jargon-free. Lead with
the outcome, then where to look, then the one next step.

```markdown
## 🐝 Swarm run complete — {headline}

**What I ran:** a {reviewers}-reviewer **{lens_plain}** ({lens_id}) on `{target}` via {transport_plain}.

**Outcome:** {status_sentence}
{workers_succeeded} of {workers_requested} reviewers finished{failed_clause}.

**Where the findings are:**
- 📄 Combined findings (read this first): `{merged_path}`
- 🗂️ Each reviewer's notes: `{output_dir}/` ({output_files_count} files)

**Recommended next step:**
> {recommended_next_command}

Want me to run that next step, or try the review again with different settings (more reviewers, a
different focus, or real models)?
```

## Field rendering notes

- `{headline}`: `success` → "looks healthy ✅"; `partial` → "mostly done ⚠️"; `failed` → "didn't complete ❌";
  `cancelled` → "practice run only".
- `{lens_plain}`: the plain phrase from the interview menu (e.g. "bug review", "edge-case hunt").
- `{transport_plain}`: stub → "a safe practice run (placeholder output, not real analysis)";
  openai_compat → "your real models".
- `{status_sentence}`:
  - success → "All reviewers agreed the run completed and produced findings."
  - partial → "Enough reviewers finished to be useful, but some failed — see below."
  - failed → "Too few reviewers finished for a reliable result."
  - cancelled → "The practice run passed; you chose not to run the real one yet."
- `{failed_clause}`: if any failed, " — {workers_failed} failed ({reasons})" where reasons summarize the
  per-worker `status` values (timeout / proxy error / parse error) in plain words.
- For a **stub** run, always add one line: "_This was a practice run, so the findings are placeholder
  text — they prove the pipeline works but aren't a real review._"
