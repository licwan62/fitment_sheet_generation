from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import httpx
import typer

from .config import load_config
from .pipeline import run_pipeline
from .utils import project_root

app = typer.Typer(help="Traceable MotorcycleSpecs dimension collector", no_args_is_help=True)
ROOT = project_root()


def validate_qwen_api_key(qwen: dict, api_key: str) -> None:
    """Verify the key and configured model with one minimal completion request."""
    base_url = str(
        qwen.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    ).rstrip("/")
    model = str(qwen.get("model", "qwen-flash"))
    timeout = min(float(qwen.get("timeout_seconds", 30)), 30)
    try:
        response = httpx.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": "Reply OK"}],
                "max_tokens": 1,
                "temperature": 0,
            },
            timeout=timeout,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status == 401:
            raise typer.BadParameter("Qwen API Key 无效或已失效（HTTP 401）") from exc
        raise typer.BadParameter(f"Qwen API 验证失败（HTTP {status}），请检查模型和接口配置") from exc
    except httpx.HTTPError as exc:
        raise typer.BadParameter(f"无法连接 Qwen API，验证未完成：{exc}") from exc


def ensure_qwen_api_key(config_path: Path, stage: str) -> None:
    if stage == "build-index":
        return
    config = load_config(config_path)
    qwen = config.get("qwen_aliases", {})
    if not qwen.get("enabled", False):
        return
    env_name = str(qwen.get("api_key_env", "DASHSCOPE_API_KEY"))
    key = os.environ.get(env_name, "").strip()
    for attempt in range(3):
        if not key:
            key = typer.prompt(
                f"请输入 Qwen API Key（仅用于本次运行，环境变量 {env_name}）",
                hide_input=True,
                confirmation_prompt=False,
            ).strip()
        if not key:
            typer.echo("Qwen API Key 不能为空", err=True)
            continue
        try:
            validate_qwen_api_key(qwen, key)
        except typer.BadParameter as exc:
            if attempt == 2:
                raise
            typer.echo(f"验证失败：{exc}，请重新输入。", err=True)
            key = ""
            continue
        os.environ[env_name] = key
        typer.echo("Qwen API Key 验证成功，继续执行。")
        return
    raise typer.BadParameter("Qwen API Key 连续三次验证失败")


def execute(stage: str, input: Path, output: Path, config: Path, sheet: Optional[str], resume: bool,
            force_refetch: bool, force_reparse: bool, clear_checkpoint: bool, max_concurrency: Optional[int],
            request_delay_min: Optional[float], request_delay_max: Optional[float], limit: Optional[int],
            start_row: int, trusted_score_threshold: Optional[int], log_level: str) -> None:
    ensure_qwen_api_key(config, stage)
    result = run_pipeline(input_path=input, output=output, config_path=config, sheet=sheet, resume=resume,
        force_refetch=force_refetch, force_reparse=force_reparse,
        clear_checkpoint_before_run=clear_checkpoint, max_concurrency=max_concurrency,
        request_delay_min=request_delay_min, request_delay_max=request_delay_max, limit=limit,
        start_row=start_row, trusted_score_threshold=trusted_score_threshold,
        log_level=log_level, stop_after=stage)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command("run")
def run(input: Path = typer.Option(..., exists=True, dir_okay=False), output: Path = typer.Option(ROOT / "output"),
        config: Path = typer.Option(ROOT / "config/config.yaml", exists=True), sheet: Optional[str] = typer.Option(None),
        resume: bool = typer.Option(True, "--resume/--no-resume"), force_refetch: bool = typer.Option(False),
        force_reparse: bool = typer.Option(False), max_concurrency: Optional[int] = typer.Option(None, min=1, max=2),
        clear_checkpoint: bool = typer.Option(False, "--clear-checkpoint", help="运行前删除 SQLite checkpoint；保留页面缓存和索引"),
        request_delay_min: Optional[float] = typer.Option(None, min=0), request_delay_max: Optional[float] = typer.Option(None, min=0),
        limit: Optional[int] = typer.Option(None, min=1), start_row: int = typer.Option(1, min=1),
        trusted_score_threshold: Optional[int] = typer.Option(None, min=0, max=100),
        log_level: str = typer.Option("INFO")):
    execute("export", input, output, config, sheet, resume, force_refetch, force_reparse, clear_checkpoint,
            max_concurrency, request_delay_min, request_delay_max, limit, start_row,
            trusted_score_threshold, log_level)


def stage_command(name: str):
    def command(input: Path = typer.Option(ROOT / "data/input/sample.tsv", exists=True), output: Path = typer.Option(ROOT / "output"),
                config: Path = typer.Option(ROOT / "config/config.yaml", exists=True), sheet: Optional[str] = None,
                resume: bool = True, force_refetch: bool = False, force_reparse: bool = False,
                clear_checkpoint: bool = typer.Option(False, "--clear-checkpoint", help="运行前删除 SQLite checkpoint；保留页面缓存和索引"),
                limit: Optional[int] = None, start_row: int = 1,
                trusted_score_threshold: Optional[int] = typer.Option(None, min=0, max=100),
                log_level: str = "INFO"):
        execute(name, input, output, config, sheet, resume, force_refetch, force_reparse, clear_checkpoint,
                None, None, None, limit, start_row, trusted_score_threshold, log_level)
    command.__name__ = name.replace("-", "_")
    return command


for _name in ("build-index", "match", "fetch", "parse", "summarize", "export"):
    app.command(_name)(stage_command(_name))


@app.command("report")
def report(output: Path = typer.Option(ROOT / "output")):
    path = output / "logs" / "run_report.json"
    if not path.exists():
        raise typer.BadParameter(f"Report not found: {path}")
    typer.echo(path.read_text(encoding="utf-8"))
