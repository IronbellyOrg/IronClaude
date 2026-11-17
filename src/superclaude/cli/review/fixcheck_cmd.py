"""`superclaude review fixcheck`: mechanical checks over the lines a fix pass edited.

One line per check run, then a totals line. It exits 0 whatever the results, because they go
to the fix log and the verifier decides. Unusable input (a file that cannot be read, or the
wrong number of --base / --lines values) exits 2 with a usage message.
"""

from __future__ import annotations

from pathlib import Path

import click

from superclaude.cli.review import fixcheck as fc


def _lines_for(files: tuple[str, ...], bases: tuple[str, ...], ranges: tuple[str, ...]):
    if len(bases) == len(files) and not ranges:
        for file, base in zip(files, bases):
            try:
                old = Path(base).read_text(encoding="utf-8")
                new = Path(file).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise click.UsageError(f"cannot read {file} or {base}: {exc}") from exc
            yield file, fc.edited_lines(old, new)
    elif len(ranges) == len(files) and not bases:
        for file, text in zip(files, ranges):
            try:
                yield file, fc.parse_range(text)
            except ValueError as exc:
                raise click.UsageError(str(exc)) from exc
    else:
        raise click.UsageError(
            "give one --base or one --lines for every --file, and not both kinds"
        )


@click.command(name="fixcheck")
@click.option("--file", "files", multiple=True, required=True, help="Edited file.")
@click.option(
    "--base", "bases", multiple=True, help="Copy of the file saved before the fix."
)
@click.option("--lines", "ranges", multiple=True, help="Edited lines, START-END.")
def command(
    files: tuple[str, ...], bases: tuple[str, ...], ranges: tuple[str, ...]
) -> None:
    """Run the mechanical checks over the lines a fix pass edited."""
    results: list[fc.CheckResult] = []
    for file, numbers in _lines_for(files, bases, ranges):
        try:
            results.extend(fc.run_checks(file, numbers))
        except (OSError, UnicodeDecodeError) as exc:
            raise click.UsageError(f"cannot read {file}: {exc}") from exc
    for r in results:
        click.echo(
            f"{r.check} {r.file} {r.line} {'PASS' if r.ok else 'FAIL'} {r.detail}"
        )
    failed = sum(not r.ok for r in results)
    click.echo(
        f"fixcheck: {len(results)} checks, {len(results) - failed} passed, {failed} failed"
    )
