from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def reconcile_cache(cache_root: Path, checkpoint_path: Path) -> dict[str, int]:
    """Register every valid HTML/metadata pair and refresh portable cache paths."""
    html_dir = cache_root / "html"
    metadata_dir = cache_root / "metadata"
    connection = sqlite3.connect(checkpoint_path, timeout=30)
    existing = {row[0] for row in connection.execute("SELECT url FROM page_cache")}
    stats = {
        "metadata_files": 0,
        "valid_pairs": 0,
        "registered": 0,
        "path_updates": 0,
        "invalid_metadata": 0,
        "missing_html": 0,
    }
    try:
        for metadata_path in metadata_dir.glob("*.json"):
            stats["metadata_files"] += 1
            html_path = html_dir / f"{metadata_path.stem}.html"
            if not html_path.is_file() or html_path.stat().st_size == 0:
                stats["missing_html"] += 1
                continue
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                url = str(metadata["url"])
                required = ("content_hash", "fetched_at", "status_code")
                if not url or any(key not in metadata for key in required):
                    raise ValueError("missing required cache metadata")
            except (OSError, ValueError, KeyError, json.JSONDecodeError):
                stats["invalid_metadata"] += 1
                continue
            stats["valid_pairs"] += 1
            current_path = str(html_path.resolve())
            if metadata.get("cache_path") != current_path:
                metadata["cache_path"] = current_path
                metadata_path.write_text(
                    json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8",
                )
                stats["path_updates"] += 1
            if url not in existing:
                stats["registered"] += 1
                existing.add(url)
            connection.execute(
                """INSERT INTO page_cache(url,cache_path,content_hash,fetched_at,status_code,metadata)
                   VALUES(?,?,?,?,?,?) ON CONFLICT(url) DO UPDATE SET
                   cache_path=excluded.cache_path,content_hash=excluded.content_hash,
                   fetched_at=excluded.fetched_at,status_code=excluded.status_code,
                   metadata=excluded.metadata""",
                (
                    url, current_path, metadata["content_hash"], metadata["fetched_at"],
                    int(metadata["status_code"]), json.dumps(metadata, ensure_ascii=False),
                ),
            )
        connection.commit()
    finally:
        connection.close()
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconcile page files with the SQLite cache index")
    parser.add_argument("--cache", type=Path, default=Path("data/cache"))
    parser.add_argument("--checkpoint", type=Path, default=Path("data/checkpoints/state.sqlite3"))
    args = parser.parse_args()
    print(json.dumps(reconcile_cache(args.cache, args.checkpoint), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
