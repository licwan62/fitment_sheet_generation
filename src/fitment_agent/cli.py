"""CLI entry point — the only interface non-technical users interact with."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .agent.orchestrator import PipelineOrchestrator
from .config.loader import load_input_list, load_requirement
from .config.models import (
    InputListConfig,
    RequirementConfig,
    TemplateParams,
    VehicleEntry,
)
from .templates.registry import get_template, list_templates

app = typer.Typer(
    name="fitment",
    help="Vehicle fitment data enrichment agent",
    no_args_is_help=True,
)
console = Console()


# ---------------------------------------------------------------------------
# fitment run
# ---------------------------------------------------------------------------


@app.command()
def run(
    requirement: Path = typer.Option(
        Path("requirement.yaml"), "--requirement", "-r",
        help="Path to requirement.yaml",
    ),
    input_list: Path = typer.Option(
        Path("input_list.yaml"), "--input", "-i",
        help="Path to input_list.yaml",
    ),
    project_dir: Path = typer.Option(
        Path("./work"), "--project-dir", "-p",
        help="Working directory for output",
    ),
    backend: str = typer.Option(
        "openai", "--backend", "-b",
        help="LLM backend: openai or browser",
    ),
    max_rounds: Optional[int] = typer.Option(
        None, "--max-rounds",
        help="Override max rounds per shard",
    ),
    chunk_size: int = typer.Option(
        50, "--chunk-size",
        help="Rows per shard",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Validate and show plan, don't execute",
    ),
    resume: bool = typer.Option(
        False, "--resume",
        help="Resume from last checkpoint",
    ),
) -> None:
    """Run the full enrichment pipeline."""
    # Validate configs
    console.print("[bold]Loading configuration...[/bold]")
    try:
        req_cfg = load_requirement(requirement)
        inp_list = load_input_list(input_list)
    except Exception as exc:
        console.print(f"[red]Configuration error: {exc}[/red]")
        raise typer.Exit(1)

    template = get_template(req_cfg.template)
    console.print(f"  Template: [cyan]{req_cfg.template}[/cyan]")
    console.print(f"  Vehicles: {len(inp_list.vehicles)}")
    console.print(f"  Backend:  {backend}")
    console.print(f"  Chunk:    {chunk_size} rows/shard")
    console.print(f"  Max rounds: {max_rounds or req_cfg.params.max_rounds or 150}")

    if dry_run:
        console.print("\n[bold yellow]Dry run — no execution.[/bold yellow]")
        contract = template.get_data_contract()
        console.print(f"  Output columns: {len(contract.columns)}")
        console.print(f"  Auto-empty columns: {contract.auto_empty_columns}")
        for v in inp_list.vehicles:
            console.print(f"  Vehicle: {v.make} {v.model}")
        return

    # Build backend factory
    backend_factory = _make_backend_factory(backend, req_cfg)

    # Run pipeline
    orchestrator = PipelineOrchestrator(
        requirement_cfg=req_cfg,
        input_list=inp_list,
        project_dir=project_dir,
        backend_factory=backend_factory,
        max_rounds=max_rounds,
        chunk_size=chunk_size,
    )
    result = asyncio.run(orchestrator.run())

    if result.errors > 0:
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# fitment validate
# ---------------------------------------------------------------------------


@app.command()
def validate(
    requirement: Path = typer.Option(Path("requirement.yaml"), "--requirement", "-r"),
    input_list: Path = typer.Option(Path("input_list.yaml"), "--input", "-i"),
) -> None:
    """Validate requirement.yaml and input_list.yaml."""
    try:
        req_cfg = load_requirement(requirement)
        inp_list = load_input_list(input_list)
        console.print("[green]All configurations valid.[/green]")
        console.print(f"  Template: {req_cfg.template}")
        console.print(f"  Vehicles: {len(inp_list.vehicles)}")
    except Exception as exc:
        console.print(f"[red]Validation error: {exc}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# fitment init
# ---------------------------------------------------------------------------


@app.command()
def init(
    template: str = typer.Option(
        "us_edmunds", "--template", "-t",
        help="Template to scaffold",
    ),
    output_dir: Path = typer.Option(
        Path("."), "--output-dir", "-o",
        help="Where to create example files",
    ),
) -> None:
    """Create example requirement.yaml and input_list.yaml."""
    output_dir.mkdir(parents=True, exist_ok=True)

    req_example = _get_requirement_example(template)
    inp_example = _get_input_list_example()

    req_path = output_dir / "requirement.yaml"
    inp_path = output_dir / "input_list.yaml"

    req_path.write_text(req_example, encoding="utf-8")
    inp_path.write_text(inp_example, encoding="utf-8")

    console.print(f"[green]Created:[/green]")
    console.print(f"  {req_path}")
    console.print(f"  {inp_path}")
    console.print("\nEdit these files, then run: [bold]fitment run[/bold]")


# ---------------------------------------------------------------------------
# fitment expand (preview)
# ---------------------------------------------------------------------------


@app.command()
def expand(
    input_list: Path = typer.Option(Path("input_list.yaml"), "--input", "-i"),
    requirement: Path = typer.Option(Path("requirement.yaml"), "--requirement", "-r"),
    output: Path = typer.Option(
        Path("expanded_preview.tsv"), "--output", "-o",
        help="Where to write the expanded TSV preview",
    ),
) -> None:
    """Preview vehicle expansion without running the full pipeline."""
    try:
        req_cfg = load_requirement(requirement)
        inp_list = load_input_list(input_list)
    except Exception as exc:
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(1)

    console.print(f"Expanding {len(inp_list.vehicles)} vehicles...")
    for v in inp_list.vehicles:
        console.print(f"  {v.make} {v.model}")

    # Dry expansion without LLM — just show what would be processed
    console.print("\n[yellow]Note: Full expansion requires LLM. Showing input summary.[/yellow]")
    console.print(f"  Template: {req_cfg.template}")
    console.print(f"  Focus fields: {req_cfg.params.focus_fields}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_backend_factory(backend_name: str, req_cfg: RequirementConfig):
    """Create a callable that returns a fresh LLMBackend instance."""
    if backend_name == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            console.print(
                "[red]OPENAI_API_KEY not set. Export it first:\n"
                "  export OPENAI_API_KEY=sk-...[/red]"
            )
            raise typer.Exit(1)

        model = req_cfg.params.model or "gpt-4o"

        def factory():
            from .llm.openai_api import OpenAIBackend

            return OpenAIBackend(api_key=api_key, model=model)

        return factory

    elif backend_name == "browser":
        console.print(
            "[yellow]Browser backend not yet implemented. "
            "Use --backend openai instead.[/yellow]"
        )
        raise typer.Exit(1)

    else:
        console.print(f"[red]Unknown backend: {backend_name}[/red]")
        raise typer.Exit(1)


def _get_requirement_example(template: str) -> str:
    return f"""\
# Fitment Agent — Requirement Configuration
# Template: {template}
# Edit this file to control HOW the LLM processes vehicle data.

template: {template}

params:
  # Target market
  market: {"US" if template == "us_edmunds" else "EU"}

  # Data source priority (first = highest priority)
  data_sources: {"[Edmunds, KBB, NHTSA]" if template == "us_edmunds" else "[Auto-Data, Car.info, UltimateSpecs]"}

  # Fields to focus enrichment on
  focus_fields: [dimensions, year_range, generation]

  # Additional instructions appended to the requirement
  extra_instructions: []

  # Override defaults (uncomment to use)
  # max_rounds: 150
  # chunk_size: 50
  # model: gpt-4o
"""


def _get_input_list_example() -> str:
    return """\
# Fitment Agent — Vehicle Input List
# Edit this file to specify WHICH vehicles to process.
# Only make + model are required; the agent expands the rest.

vehicles:
  - make: Chevrolet
    model: Silverado 2500HD
    # Optional constraints (uncomment to use):
    # year_from: 2001
    # year_to: 2024
    # body_styles: [Pickup]
    # notes: "Focus on HD variants"

  - make: Ford
    model: F-150

  - make: Toyota
    model: Tacoma

# Or: provide a pre-built TSV file instead of expansion
# prebuilt_tsv: ./my_data.tsv
"""


if __name__ == "__main__":
    app()
