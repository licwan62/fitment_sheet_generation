# Fitment Agent Architecture

## Overview

Transform the current PowerShell + Python hybrid into a pure Python CLI agent that non-technical team members can operate by editing just two YAML files.

## User Workflow

```
1. fitment init --template us_edmunds
   → generates requirement.yaml + input_list.yaml

2. Edit requirement.yaml:
   template: us_edmunds
   params:
     market: US
     data_sources: [Edmunds, KBB, NHTSA]
     focus_fields: [dimensions, year_range, generation]

3. Edit input_list.yaml:
   vehicles:
     - make: Chevrolet
       model: Silverado 2500HD
     - make: Ford
       model: F-150

4. fitment run
   → expand → split → enrich → merge → output
```

## Package Structure

```
fitment_agent/
├── pyproject.toml
├── src/fitment_agent/
│   ├── cli.py                   # Typer CLI: run / validate / expand / init
│   ├── config/
│   │   ├── models.py            # Pydantic: RequirementConfig, InputListConfig
│   │   └── loader.py            # YAML load + validate
│   ├── templates/
│   │   ├── base.py              # RequirementTemplate ABC
│   │   ├── registry.py          # Template discovery
│   │   ├── us_edmunds.py        # US template adapter
│   │   ├── eu_autodata.py       # EU template adapter
│   │   └── prompts/             # Bundled .md requirement files
│   ├── vehicle/
│   │   ├── expander.py          # make+model → seed TSV (via LLM)
│   │   ├── tsv_builder.py       # ExpandedVehicle → TSV rows
│   │   └── tsv_splitter.py      # Split large TSV into shards
│   ├── llm/
│   │   ├── protocol.py          # LLMBackend ABC
│   │   ├── openai_api.py        # OpenAI API backend
│   │   └── browser_cdp.py       # OpenClaw/CDP browser backend
│   ├── agent/
│   │   ├── orchestrator.py      # Pipeline coordinator
│   │   ├── shard_worker.py      # Per-shard multi-round agent loop
│   │   ├── signals.py           # Completion/repetition/deviation detection
│   │   ├── messages.py          # Context-aware message builder
│   │   └── state.py             # ShardState enum + transitions
│   ├── merger/
│   │   └── result_merger.py     # Merge shard results
│   └── io/
│       ├── tsv.py               # TSV read/write
│       ├── markdown.py          # Round transcript formatting
│       └── project.py           # Project directory layout
```

## Agent Loop (per shard)

```
INIT → send requirement + TSV
  ↓
WAITING_REPLY
  ↓
EVALUATING_REPLY ──→ COMPLETE (has full table)
  │               ──→ REPEATED (similarity > 0.95)
  │               ──→ DEVIATED (no progress signals)
  │               ──→ MAX_ROUNDS
  │               ──→ CONTINUE (send "下一步")
  │               ──→ FIX (missing format signals)
  │               ──→ REQUEST_FULL_TABLE
  ↓
(loop until terminal state)
```

## LLM Abstraction

```
LLMBackend (ABC)
  ├── OpenAIBackend     # Direct API: reliable, fast, no browser
  └── BrowserCDPBackend # OpenClaw/CDP: fallback for ChatGPT web
```

## Key Design Decisions

1. Async throughout (asyncio) for I/O-bound LLM calls
2. OpenAI API as default backend (more reliable than browser)
3. Vehicle expansion via lightweight LLM call (no hardcoded database)
4. Checkpoint + resume after each shard
5. Rich console output for non-technical users
