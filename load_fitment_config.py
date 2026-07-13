#!/usr/bin/env python3
"""Load and validate fitment config.yaml, then emit JSON for PowerShell."""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("缺少 PyYAML，请运行: python -m pip install PyYAML") from exc


def require_mapping(value, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} 必须是 YAML mapping")
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()
    path = Path(args.config).resolve()
    if not path.is_file():
        raise ValueError(f"配置文件不存在: {path}")

    with path.open("r", encoding="utf-8-sig") as stream:
        config = yaml.safe_load(stream) or {}
    require_mapping(config, "config")

    if config.get("version", 1) != 1:
        raise ValueError("目前只支持 config version: 1")
    mode = config.get("mode", "work")
    if mode not in {"work", "check", "dry_run"}:
        raise ValueError("mode 只能是 work、check 或 dry_run")

    workspace = require_mapping(config.get("workspace", {}), "workspace")
    traversal = require_mapping(workspace.get("traversal", {}), "workspace.traversal")
    strategy = traversal.get("strategy", "directories")
    if strategy not in {"directories", "glob", "explicit"}:
        raise ValueError("traversal.strategy 只能是 directories、glob 或 explicit")

    contract = require_mapping(config.get("data_contract", {}), "data_contract")
    table = require_mapping(contract.get("full_table", {}), "data_contract.full_table")
    subseries = require_mapping(contract.get("subseries_match", {}), "data_contract.subseries_match")
    if not contract.get("requirement"):
        raise ValueError("缺少 data_contract.requirement")
    if not table.get("columns"):
        raise ValueError("缺少 data_contract.full_table.columns")
    if not subseries.get("columns"):
        raise ValueError("缺少 data_contract.subseries_match.columns")

    for name, definition in (("full_table", table), ("subseries_match", subseries)):
        columns = definition.get("columns", [])
        if not isinstance(columns, list) or any(not isinstance(item, str) or not item.strip() for item in columns):
            raise ValueError(f"data_contract.{name}.columns 必须是非空字符串列表")
        if len(columns) != len(set(columns)):
            raise ValueError(f"data_contract.{name}.columns 不允许重复列名")
        auto_columns = definition.get("auto_empty_columns", [])
        if not isinstance(auto_columns, list):
            raise ValueError(f"data_contract.{name}.auto_empty_columns 必须是列表")
        unknown = [item for item in auto_columns if item not in columns]
        if unknown:
            raise ValueError(f"data_contract.{name}.auto_empty_columns 包含未定义列: {unknown}")

    runtime = require_mapping(config.get("runtime", {}), "runtime")
    if int(runtime.get("max_rounds", 30)) <= 0:
        raise ValueError("runtime.max_rounds 必须大于 0")
    input_files = require_mapping(runtime.get("input_files", {}), "runtime.input_files")
    if input_files.get("order", "name_asc") not in {"name_asc", "name_desc", "modified_asc", "modified_desc"}:
        raise ValueError("runtime.input_files.order 值无效")

    config["_meta"] = {"config_path": str(path), "config_dir": str(path.parent)}
    json.dump(config, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"config.yaml 错误: {exc}", file=sys.stderr)
        raise SystemExit(2)
