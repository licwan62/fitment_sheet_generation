"""Tests for CLI commands."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from fitment_agent.cli import app

runner = CliRunner()


class TestInit:
    def test_creates_files(self, tmp_path):
        result = runner.invoke(app, ["init", "--template", "us_edmunds", "--output-dir", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "requirement.yaml").exists()
        assert (tmp_path / "input_list.yaml").exists()
        assert "Created" in result.output

    def test_eu_template(self, tmp_path):
        result = runner.invoke(app, ["init", "--template", "eu_autodata", "--output-dir", str(tmp_path)])
        assert result.exit_code == 0
        content = (tmp_path / "requirement.yaml").read_text()
        assert "eu_autodata" in content


class TestValidate:
    def test_valid_files(self, tmp_path):
        # Create valid files
        runner.invoke(app, ["init", "--output-dir", str(tmp_path)])
        result = runner.invoke(app, [
            "validate",
            "--requirement", str(tmp_path / "requirement.yaml"),
            "--input", str(tmp_path / "input_list.yaml"),
        ])
        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_invalid_file(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("invalid: yaml: content: [", encoding="utf-8")
        result = runner.invoke(app, [
            "validate",
            "--requirement", str(bad),
            "--input", str(bad),
        ])
        assert result.exit_code == 1


class TestDryRun:
    def test_dry_run(self, tmp_path):
        # Create valid files
        runner.invoke(app, ["init", "--output-dir", str(tmp_path)])
        result = runner.invoke(app, [
            "run",
            "--requirement", str(tmp_path / "requirement.yaml"),
            "--input", str(tmp_path / "input_list.yaml"),
            "--dry-run",
        ])
        assert result.exit_code == 0
        assert "Dry run" in result.output
        assert "Template" in result.output
        assert "Vehicles" in result.output

    def test_dry_run_shows_columns(self, tmp_path):
        runner.invoke(app, ["init", "--output-dir", str(tmp_path)])
        result = runner.invoke(app, [
            "run",
            "--requirement", str(tmp_path / "requirement.yaml"),
            "--input", str(tmp_path / "input_list.yaml"),
            "--dry-run",
        ])
        assert "Output columns" in result.output


class TestHelp:
    def test_main_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "run" in result.output
        assert "validate" in result.output
        assert "init" in result.output

    def test_run_help(self):
        result = runner.invoke(app, ["run", "--help"])
        assert result.exit_code == 0
        assert "--requirement" in result.output
        assert "--input" in result.output
        assert "--dry-run" in result.output
