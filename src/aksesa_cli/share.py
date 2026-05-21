from __future__ import annotations

import os
from pathlib import Path


def get_share_dir() -> Path:
    """Get the share directory path."""
    if raw_dir := os.getenv("AKSESA_SHARE_DIR") or os.getenv("KIMI_SHARE_DIR"):
        share_dir = Path(raw_dir)
    else:
        share_dir = Path.home() / ".aksesa"
    share_dir.mkdir(parents=True, exist_ok=True)
    return share_dir
