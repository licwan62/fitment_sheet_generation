from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from .pipeline import run_pipeline
from .utils import project_root

app = typer.Typer(help="Traceable MotorcycleSpecs dimension collector", no_args_is_help=True)
ROOT = project_root()


def execute(stage: str, input: Path, output: Path, config: Path, sheet: Optional[str], resume: bool,
            force_refetch: bool, force_reparse: bool, max_concurrency: Optional[int],
            request_delay_min: Optional[float], request_delay_max: Optional[float], limit: Optional[int],
            start_row: int, trusted_score_threshold: Optional[int], log_level: str) -> None:
    result = run_pipeline(input_path=input, output=output, config_path=config, sheet=sheet, resume=resume,
        force_refetch=force_refetch, force_reparse=force_reparse, max_concurrency=max_concurrency,
        request_delay_min=request_delay_min, request_delay_max=request_delay_max, limit=limit,
        start_row=start_row, trusted_score_threshold=trusted_score_threshold,
        log_level=log_level, stop_after=stage)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command("run")
def run(input: Path = typer.Option(..., exists=True, dir_okay=False), output: Path = typer.Option(ROOT / "output"),
        config: Path = typer.Option(ROOT / "config/config.yaml", exists=True), sheet: Optional[str] = typer.Option(None),
        resume: bool = typer.Option(True, "--resume/--no-resume"), force_refetch: bool = typer.Option(False),
        force_reparse: bool = typer.Option(False), max_concurrency: Optional[int] = typer.Option(None, min=1, max=2),
        request_delay_min: Optional[float] = typer.Option(None, min=0), request_delay_max: Optional[float] = typer.Option(None, min=0),
        limit: Optional[int] = typer.Option(None, min=1), start_row: int = typer.Option(1, min=1),
        trusted_score_threshold: Optional[int] = typer.Option(None, min=0, max=100),
        log_level: str = typer.Option("INFO")):
    execute("export", input, output, config, sheet, resume, force_refetch, force_reparse,
            max_concurrency, request_delay_min, request_delay_max, limit, start_row,
            trusted_score_threshold, log_level)


def stage_command(name: str):
    def command(input: Path = typer.Option(ROOT / "data/input/sample.tsv", exists=True), output: Path = typer.Option(ROOT / "output"),
                config: Path = typer.Option(ROOT / "config/config.yaml", exists=True), sheet: Optional[str] = None,
                resume: bool = True, force_refetch: bool = False, force_reparse: bool = False,
                limit: Optional[int] = None, start_row: int = 1,
                trusted_score_threshold: Optional[int] = typer.Option(None, min=0, max=100),
                log_level: str = "INFO"):
        execute(name, input, output, config, sheet, resume, force_refetch, force_reparse,
                None, None, None, limit, start_row, trusted_score_threshold, log_level)
    command.__name__ = name.replace("-", "_")
    return command


for _name in ("build-index", "match", "fetch", "parse", "summarize", "export"):
    app.command(_name)(stage_command(_name))


@app.command("report")
def report(output: Path = typer.Option(ROOT / "output")):
    path = output / "run_report.json"
    if not path.exists():
        raise typer.BadParameter(f"Report not found: {path}")
    typer.echo(path.read_text(encoding="utf-8"))
