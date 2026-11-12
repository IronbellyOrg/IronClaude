"""`superclaude review manifest`: init, advance and validate the coordinator-owned panel manifest.

The manifest is <out>/panel/manifest.json (see review/manifest.py for the contract). `init` freezes a run (or resumes
it: the same frozen fields reuse the manifest, a changed input tree or policy starts a new invocation), `advance`
commits the next stage or records one reviewer attempt, `validate` checks the file.
"""

from __future__ import annotations

import json
from pathlib import Path

import click
import yaml

from superclaude.cli.review import manifest as mf


def _path(out: str) -> Path:
    return Path(out) / "panel" / "manifest.json"


def _fail(exc: Exception) -> click.ClickException:
    return click.ClickException(f"{type(exc).__name__}: {exc}")


def _read_json(path: str, what: str) -> dict:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise click.ClickException(f"cannot read {what} {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise click.ClickException(f"{what} {path} must be a JSON object")
    return data


def _tree_sha(snapshot: Path) -> str:
    try:
        data = yaml.safe_load(snapshot.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise click.ClickException(f"cannot read snapshot {snapshot}: {exc}") from exc
    for scope in (data, data.get("input_snapshot") if isinstance(data, dict) else None):
        if isinstance(scope, dict) and isinstance(scope.get("input_tree_sha256"), str):
            return scope["input_tree_sha256"]
    raise click.ClickException(f"{snapshot} has no input_tree_sha256")


@click.group(name="manifest")
def command() -> None:
    """Initialise, advance and validate the panel run manifest."""


@command.command("init")
@click.option(
    "--out",
    required=True,
    type=click.Path(file_okay=False),
    help="Reflect output directory.",
)
@click.option("--run-id", required=True)
@click.option(
    "--snapshot",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="artifacts/input-snapshot.yaml.",
)
@click.option("--template-sha256", required=True)
@click.option("--tiers-sha256", required=True)
@click.option("--brief-template-sha256", required=True)
@click.option(
    "--schema-id",
    "schema_ids",
    required=True,
    multiple=True,
    help="A schema id in force; repeatable.",
)
@click.option("--t2-engine-requested", required=True, type=click.Choice(mf.ENGINES))
@click.option("--t2-engine-effective", required=True, type=click.Choice(mf.ENGINES))
def init_cmd(
    out,
    run_id,
    snapshot,
    template_sha256,
    tiers_sha256,
    brief_template_sha256,
    schema_ids,
    t2_engine_requested,
    t2_engine_effective,
) -> None:
    """Freeze a run in <out>/panel/manifest.json, or resume the one that is there."""
    snap = Path(snapshot)
    frozen = {
        "snapshot_ref": snapshot,
        "snapshot_sha256": mf.sha256_file(snap),
        "input_tree_sha256": _tree_sha(snap),
        "template_sha256": template_sha256,
        "tiers_sha256": tiers_sha256,
        "brief_template_sha256": brief_template_sha256,
        "schema_ids": list(schema_ids),
    }
    path = _path(out)
    try:
        if path.exists():
            current = mf.load(path)
            manifest, new = mf.resume(
                current,
                frozen=frozen,
                run_id=run_id,
                engine_requested=t2_engine_requested,
                engine_effective=t2_engine_effective,
            )
            result = "new-invocation" if new else "reused"
        else:
            manifest = mf.new_manifest(
                run_id=run_id,
                frozen=frozen,
                engine_requested=t2_engine_requested,
                engine_effective=t2_engine_effective,
            )
            result = "created"
        if result != "reused":
            mf.save(path, manifest)
    except mf.ManifestError as exc:
        raise _fail(exc) from exc
    click.echo(
        json.dumps(
            {
                "result": result,
                "state": manifest["state"],
                "invocation": manifest["invocation"],
            },
            sort_keys=True,
        )
    )


@command.command("advance")
@click.option("--out", required=True, type=click.Path(file_okay=False))
@click.option("--stage", required=True, type=click.Choice([*mf.STATES[1:], mf.FAILED]))
@click.option(
    "--payload",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help="JSON payload: {outputs: {name: sha256}, ...}.",
)
@click.option(
    "--reviewer-id",
    default=None,
    help="With --attempt-id and --completion: record one reviewer attempt.",
)
@click.option("--attempt-id", default=None)
@click.option("--completion", default=None, type=click.Choice(mf.COMPLETIONS))
@click.option(
    "--publish-from",
    default=None,
    type=click.Path(exists=True, file_okay=False),
    help="published only: stage REPORT.md, return-contract.yaml and audit.log from this directory with temporaries and renames.",
)
@click.option("--reason", default=None, help="With --stage failed.")
def advance_cmd(
    out, stage, payload, reviewer_id, attempt_id, completion, publish_from, reason
) -> None:
    """Commit the next stage, record a reviewer attempt, or mark the run failed.

    `--stage published` without --publish-from and without a payload `outputs` map hashes the three files already
    in --out and rewrites nothing (shadow mode: the legacy writers stay authoritative); a payload `outputs` map is
    recorded as given.
    """
    path = _path(out)
    try:
        manifest = mf.load(path)
        body = _read_json(payload, "payload") if payload else {}
        changed = True
        if stage == mf.FAILED:
            mf.fail(manifest, reason or "unspecified")
        elif reviewer_id or attempt_id or completion:
            if not (reviewer_id and attempt_id and completion):
                raise click.ClickException(
                    "--reviewer-id, --attempt-id and --completion go together"
                )
            changed = mf.record_attempt(
                manifest, stage, reviewer_id, attempt_id, completion, body
            )
        elif stage == "published" and publish_from:
            contents = {
                n: (Path(publish_from) / n).read_bytes() for n in mf.PUBLISH_FILES
            }
            before = manifest["state"]
            mf.publish_files(Path(out), contents, path)
            click.echo(
                json.dumps(
                    {
                        "result": "advanced" if before != "published" else "noop",
                        "state": "published",
                    },
                    sort_keys=True,
                )
            )
            return
        else:
            if stage == "published" and "outputs" not in body:
                body = {**body, "outputs": mf.hash_published_files(Path(out))}
            changed = mf.advance_stage(manifest, stage, body)
        if changed:
            mf.save(path, manifest)
    except mf.ManifestError as exc:
        raise _fail(exc) from exc
    except OSError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(
        json.dumps(
            {"result": "advanced" if changed else "noop", "state": manifest["state"]},
            sort_keys=True,
        )
    )


@command.command("validate")
@click.option("--out", required=True, type=click.Path(file_okay=False))
@click.option(
    "--require-published",
    is_flag=True,
    help="Also fail unless the state is published (a reader's view).",
)
def validate_cmd(out, require_published) -> None:
    """Check <out>/panel/manifest.json; exit 0 when valid, 1 when not."""
    path = _path(out)
    try:
        manifest = mf.load(path)
    except mf.ManifestError as exc:
        click.echo(f"{path}: {exc}")
        raise SystemExit(1) from exc
    errors = mf.validate(manifest)
    if require_published and manifest.get("state") != "published":
        errors.append(f"state is {manifest.get('state')!r}, not 'published'")
    for err in errors:
        click.echo(f"{path}: {err}")
    if errors:
        raise SystemExit(1)
    click.echo(f"{path}: valid manifest (state {manifest['state']})")
