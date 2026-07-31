"""Template registry — discovers and instantiates requirement templates."""

from __future__ import annotations

from .base import RequirementTemplate
from .eu_autodata import EuAutodataTemplate
from .us_edmunds import UsEdmundsTemplate

_REGISTRY: dict[str, type[RequirementTemplate]] = {
    "us_edmunds": UsEdmundsTemplate,
    "eu_autodata": EuAutodataTemplate,
}


def get_template(name: str) -> RequirementTemplate:
    """Return an instance of the named template."""
    cls = _REGISTRY.get(name)
    if cls is None:
        available = ", ".join(_REGISTRY.keys())
        raise ValueError(f"Unknown template '{name}'. Available: {available}")
    return cls()


def list_templates() -> list[str]:
    return list(_REGISTRY.keys())
