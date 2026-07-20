# Motorcycle Specs migration package

Use `motorcycle_specs_migration_20260720_190554_final.tar.gz` only.

The archive contains the current project working tree, input/configuration files,
page and Qwen caches, indexes, output/progress files, logs, and a consistent
online SQLite checkpoint snapshot. It excludes `.venv`, `.env`, pytest caches,
and Python bytecode.

After cloning/pulling the Git repository on the destination computer, place the
archive in its `migration_packages` directory. From the Git repository root,
verify and overlay the package onto `projects/motorcycle_specs`:

```powershell
Get-FileHash .\migration_packages\motorcycle_specs_migration_20260720_190554_final.tar.gz -Algorithm SHA256
tar -xzf .\migration_packages\motorcycle_specs_migration_20260720_190554_final.tar.gz -C .\projects
cd .\projects\motorcycle_specs
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

Expected SHA-256:

`F062EFB973FAB69AB5E0532A1D453EF1ADDF7052B60B79F23EDEEF20598A5567`

Recreate `.env` securely on the destination computer. Do not commit API keys.

The archive is larger than GitHub's normal 100 MB per-file limit. Transfer it
with cloud storage, removable media, or Git LFS; do not add it to ordinary Git
history. Git can be used separately to synchronize subsequent source changes.
