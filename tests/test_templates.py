"""Tests for template registry and adapters."""

import pytest

from fitment_agent.templates.registry import get_template, list_templates
from fitment_agent.templates.base import DataContract, RequirementTemplate
from fitment_agent.templates.us_edmunds import UsEdmundsTemplate
from fitment_agent.templates.eu_autodata import EuAutodataTemplate


class TestRegistry:
    def test_list_templates(self):
        names = list_templates()
        assert "us_edmunds" in names
        assert "eu_autodata" in names

    def test_get_us(self):
        t = get_template("us_edmunds")
        assert isinstance(t, UsEdmundsTemplate)

    def test_get_eu(self):
        t = get_template("eu_autodata")
        assert isinstance(t, EuAutodataTemplate)

    def test_get_unknown(self):
        with pytest.raises(ValueError, match="Unknown template"):
            get_template("nonexistent")


class TestUsEdmundsTemplate:
    def setup_method(self):
        self.template = UsEdmundsTemplate()
        self.params = {"data_sources": ["Edmunds", "KBB", "NHTSA"]}

    def test_requirement_text(self):
        text = self.template.get_requirement_text(self.params)
        assert len(text) > 100
        assert "Edmunds" in text

    def test_data_contract(self):
        contract = self.template.get_data_contract()
        assert isinstance(contract, DataContract)
        assert len(contract.columns) == 27
        assert "主车型" in contract.columns
        assert "迭代状态" in contract.columns
        assert "对应尺码" in contract.auto_empty_columns

    def test_build_initial_prompt(self):
        prompt = self.template.build_initial_prompt(
            "requirement text here",
            "header\tcol1\nval1\tval2",
            "test_file.tsv",
        )
        assert "test_file.tsv" in prompt
        assert "requirement text here" in prompt

    def test_continue_message(self):
        msg = self.template.get_continue_message()
        assert "下一步" in msg

    def test_completion_signals(self):
        signals = self.template.get_completion_signals()
        assert len(signals) > 0
        assert any("完成" in s for s in signals)


class TestEuAutodataTemplate:
    def setup_method(self):
        self.template = EuAutodataTemplate()
        self.params = {"data_sources": ["Auto-Data", "Car.info"]}

    def test_requirement_text(self):
        text = self.template.get_requirement_text(self.params)
        assert len(text) > 50

    def test_data_contract(self):
        contract = self.template.get_data_contract()
        assert "Ktype" in contract.columns
        assert "DIMENSION_GROUP_ID" in contract.columns
        assert "CacheStatus" in contract.auto_empty_columns

    def test_instructions(self):
        contract = self.template.get_data_contract()
        assert len(contract.instructions) > 0
        assert any("Ktype" in i for i in contract.instructions)
