from pathlib import Path

import yaml

import httpx
import pytest
import typer

from moto_dimension_crawler.cli import ensure_qwen_api_key, validate_qwen_api_key


def write_config(path: Path, *, enabled: bool, env_name: str = "QWEN_API_KEY") -> None:
    path.write_text(yaml.safe_dump({
        "qwen_aliases": {"enabled": enabled, "api_key_env": env_name},
    }), encoding="utf-8")


def test_missing_qwen_key_is_prompted_and_kept_in_process(tmp_path, monkeypatch):
    config = tmp_path / "config.yaml"
    write_config(config, enabled=True)
    monkeypatch.delenv("QWEN_API_KEY", raising=False)
    monkeypatch.setattr("moto_dimension_crawler.cli.typer.prompt", lambda *args, **kwargs: "secret-test-key")
    monkeypatch.setattr("moto_dimension_crawler.cli.validate_qwen_api_key", lambda *args: None)

    ensure_qwen_api_key(config, "export")

    assert __import__("os").environ["QWEN_API_KEY"] == "secret-test-key"


def test_existing_qwen_key_does_not_prompt(tmp_path, monkeypatch):
    config = tmp_path / "config.yaml"
    write_config(config, enabled=True)
    monkeypatch.setenv("QWEN_API_KEY", "already-set")
    validated = []
    monkeypatch.setattr("moto_dimension_crawler.cli.validate_qwen_api_key", lambda qwen, key: validated.append(key))
    monkeypatch.setattr(
        "moto_dimension_crawler.cli.typer.prompt",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("should not prompt")),
    )

    ensure_qwen_api_key(config, "export")
    assert validated == ["already-set"]


def test_build_index_does_not_need_qwen_key(tmp_path, monkeypatch):
    config = tmp_path / "config.yaml"
    write_config(config, enabled=True)
    monkeypatch.delenv("QWEN_API_KEY", raising=False)
    monkeypatch.setattr(
        "moto_dimension_crawler.cli.typer.prompt",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("should not prompt")),
    )

    ensure_qwen_api_key(config, "build-index")


def test_invalid_key_is_reprompted_before_continuing(tmp_path, monkeypatch):
    config = tmp_path / "config.yaml"
    write_config(config, enabled=True)
    monkeypatch.setenv("QWEN_API_KEY", "expired-key")
    monkeypatch.setattr("moto_dimension_crawler.cli.typer.prompt", lambda *args, **kwargs: "replacement-key")
    checked = []

    def validate(_qwen, key):
        checked.append(key)
        if key == "expired-key":
            raise typer.BadParameter("Qwen API Key 无效或已失效（HTTP 401）")

    monkeypatch.setattr("moto_dimension_crawler.cli.validate_qwen_api_key", validate)

    ensure_qwen_api_key(config, "export")

    assert checked == ["expired-key", "replacement-key"]
    assert __import__("os").environ["QWEN_API_KEY"] == "replacement-key"


def test_validate_qwen_api_key_reports_401(monkeypatch):
    request = httpx.Request("POST", "https://example.test/chat/completions")
    response = httpx.Response(401, request=request)
    monkeypatch.setattr("moto_dimension_crawler.cli.httpx.post", lambda *args, **kwargs: response)

    with pytest.raises(typer.BadParameter, match="HTTP 401"):
        validate_qwen_api_key({"base_url": "https://example.test"}, "bad-key")
