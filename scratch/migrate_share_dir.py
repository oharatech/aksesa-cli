from pathlib import Path

files = [
    "tests/acp/conftest.py",
    "tests/auth/test_oauth_cross_process.py",
    "tests/auth/test_oauth_refresh.py",
    "tests/auth/test_resolve_api_key.py",
    "tests/cli/test_mcp_oauth.py",
    "tests/e2e/test_cli_error_output.py",
    "tests/e2e/test_kimi_empty_tool_call_content_e2e.py",
    "tests/e2e/test_slash_completion_enter_tmux.py",
    "tests/vis/test_app.py",
    "tests_e2e/wire_helpers.py"
]

for f_path in files:
    p = Path(f_path)
    if p.exists():
        content = p.read_text(encoding="utf-8")
        content = content.replace("KIMI_SHARE_DIR", "AKSESA_SHARE_DIR")
        p.write_text(content, encoding="utf-8")
        print(f"Updated {f_path}")
    else:
        print(f"File not found: {f_path}")
