"""Tests for config models and loader."""

import textwrap
from pathlib import Path

import pytest

from fitment_agent.config.models import (
    InputListConfig,
    RequirementConfig,
    TemplateParams,
    VehicleEntry,
)
from fitment_agent.config.loader import load_requirement, load_input_list


# ---------------------------------------------------------------------------
# TemplateParams
# ---------------------------------------------------------------------------

class TestTemplateParams:
    def test_defaults(self):
        p = TemplateParams()
        assert p.market == "US"
        assert p.data_sources == ["Edmunds", "KBB", "NHTSA"]
        assert p.focus_fields == ["dimensions", "year_range", "generation"]
        assert p.extra_instructions == []
        assert p.max_rounds is None
        assert p.chunk_size is None
        assert p.model is None

    def test_custom_values(self):
        p = TemplateParams(market="EU", max_rounds=200, model="gpt-4-turbo")
        assert p.market == "EU"
        assert p.max_rounds == 200
        assert p.model == "gpt-4-turbo"


# ---------------------------------------------------------------------------
# RequirementConfig
# ---------------------------------------------------------------------------

class TestRequirementConfig:
    def test_valid_us(self):
        cfg = RequirementConfig(template="us_edmunds")
        assert cfg.template == "us_edmunds"
        assert isinstance(cfg.params, TemplateParams)

    def test_valid_eu(self):
        cfg = RequirementConfig(template="eu_autodata")
        assert cfg.template == "eu_autodata"

    def test_invalid_template(self):
        with pytest.raises(Exception):
            RequirementConfig(template="jp_goo_net")


# ---------------------------------------------------------------------------
# VehicleEntry
# ---------------------------------------------------------------------------

class TestVehicleEntry:
    def test_minimal(self):
        v = VehicleEntry(make="Ford", model="F-150")
        assert v.make == "Ford"
        assert v.model == "F-150"
        assert v.year_from is None
        assert v.body_styles is None

    def test_full(self):
        v = VehicleEntry(
            make="Chevrolet",
            model="Silverado 2500HD",
            year_from=2001,
            year_to=2024,
            body_styles=["Pickup"],
            generations=["gen1", "gen2"],
            notes="Focus on HD variants",
        )
        assert v.year_from == 2001
        assert v.body_styles == ["Pickup"]
        assert v.generations == ["gen1", "gen2"]


# ---------------------------------------------------------------------------
# InputListConfig
# ---------------------------------------------------------------------------

class TestInputListConfig:
    def test_basic(self):
        cfg = InputListConfig(
            vehicles=[VehicleEntry(make="Ford", model="F-150")]
        )
        assert len(cfg.vehicles) == 1
        assert cfg.prebuilt_tsv is None

    def test_with_prebuilt(self):
        cfg = InputListConfig(
            vehicles=[],
            prebuilt_tsv="./data.tsv",
        )
        assert cfg.prebuilt_tsv == "./data.tsv"


# ---------------------------------------------------------------------------
# Loader (file-based)
# ---------------------------------------------------------------------------

class TestLoader:
    def test_load_requirement(self, tmp_path):
        content = textwrap.dedent("""\
            template: us_edmunds
            params:
              market: US
              data_sources: [Edmunds, KBB]
              max_rounds: 100
        """)
        f = tmp_path / "requirement.yaml"
        f.write_text(content, encoding="utf-8")
        cfg = load_requirement(f)
        assert cfg.template == "us_edmunds"
        assert cfg.params.market == "US"
        assert cfg.params.data_sources == ["Edmunds", "KBB"]
        assert cfg.params.max_rounds == 100

    def test_load_input_list(self, tmp_path):
        content = textwrap.dedent("""\
            vehicles:
              - make: Chevrolet
                model: Silverado 2500HD
              - make: Ford
                model: F-150
                year_from: 2010
        """)
        f = tmp_path / "input_list.yaml"
        f.write_text(content, encoding="utf-8")
        cfg = load_input_list(f)
        assert len(cfg.vehicles) == 2
        assert cfg.vehicles[0].make == "Chevrolet"
        assert cfg.vehicles[1].year_from == 2010

    def test_load_missing_file(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_requirement(tmp_path / "nonexistent.yaml")
