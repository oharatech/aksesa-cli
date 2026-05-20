from __future__ import annotations

import importlib
import sys

# Alias the kimi_code package to aksesa_cli for compatibility.
sys.modules[__name__] = importlib.import_module("aksesa_cli")
