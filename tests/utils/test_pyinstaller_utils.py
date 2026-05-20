from __future__ import annotations

import platform
import sys
from pathlib import Path

from inline_snapshot import snapshot


def test_pyinstaller_datas():
    from aksesa_cli.utils.pyinstaller import datas

    project_root = Path(__file__).parent.parent.parent
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = f".venv/lib/python{python_version}/site-packages"
    rg_binary = "rg.exe" if platform.system() == "Windows" else "rg"
    has_rg_binary = (project_root / "src/aksesa_cli/deps/bin" / rg_binary).exists()
    datas = [
        (
            Path(path)
            .relative_to(project_root)
            .as_posix()
            .replace(".venv/Lib/site-packages", site_packages),
            Path(dst).as_posix(),
        )
        for path, dst in datas
    ]

    datas = [(p, d) for p, d in datas if "web/static" not in d and "vis/static" not in d]

    expected_datas = [
        (
            f"{site_packages}/dateparser/data/dateparser_tz_cache.pkl",
            "dateparser/data",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/INSTALLER",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/METADATA",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/RECORD",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/REQUESTED",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/WHEEL",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/entry_points.txt",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/licenses/LICENSE",
            "fastmcp/../fastmcp-3.2.4.dist-info/licenses",
        ),
        (
            "src/aksesa_cli/CHANGELOG.md",
            "aksesa_cli",
        ),
        ("src/aksesa_cli/agents/default/agent.yaml", "aksesa_cli/agents/default"),
        ("src/aksesa_cli/agents/default/coder.yaml", "aksesa_cli/agents/default"),
        ("src/aksesa_cli/agents/default/explore.yaml", "aksesa_cli/agents/default"),
        ("src/aksesa_cli/agents/default/plan.yaml", "aksesa_cli/agents/default"),
        ("src/aksesa_cli/agents/default/system.md", "aksesa_cli/agents/default"),
        ("src/aksesa_cli/agents/okabe/agent.yaml", "aksesa_cli/agents/okabe"),
        ("src/aksesa_cli/prompts/compact.md", "aksesa_cli/prompts"),
        ("src/aksesa_cli/prompts/init.md", "aksesa_cli/prompts"),
        (
            "src/aksesa_cli/skills/kimi-cli-help/SKILL.md",
            "aksesa_cli/skills/kimi-cli-help",
        ),
        (
            "src/aksesa_cli/skills/skill-creator/SKILL.md",
            "aksesa_cli/skills/skill-creator",
        ),
        ("src/aksesa_cli/tools/agent/description.md", "aksesa_cli/tools/agent"),
        ("src/aksesa_cli/tools/ask_user/description.md", "aksesa_cli/tools/ask_user"),
        (
            "src/aksesa_cli/tools/dmail/dmail.md",
            "aksesa_cli/tools/dmail",
        ),
        ("src/aksesa_cli/tools/background/list.md", "aksesa_cli/tools/background"),
        ("src/aksesa_cli/tools/background/output.md", "aksesa_cli/tools/background"),
        ("src/aksesa_cli/tools/background/stop.md", "aksesa_cli/tools/background"),
        (
            "src/aksesa_cli/tools/file/glob.md",
            "aksesa_cli/tools/file",
        ),
        (
            "src/aksesa_cli/tools/file/grep.md",
            "aksesa_cli/tools/file",
        ),
        (
            "src/aksesa_cli/tools/file/read.md",
            "aksesa_cli/tools/file",
        ),
        (
            "src/aksesa_cli/tools/file/read_media.md",
            "aksesa_cli/tools/file",
        ),
        (
            "src/aksesa_cli/tools/file/replace.md",
            "aksesa_cli/tools/file",
        ),
        (
            "src/aksesa_cli/tools/file/write.md",
            "aksesa_cli/tools/file",
        ),
        ("src/aksesa_cli/tools/plan/description.md", "aksesa_cli/tools/plan"),
        ("src/aksesa_cli/tools/plan/enter_description.md", "aksesa_cli/tools/plan"),
        ("src/aksesa_cli/tools/shell/bash.md", "aksesa_cli/tools/shell"),
        (
            "src/aksesa_cli/tools/think/think.md",
            "aksesa_cli/tools/think",
        ),
        (
            "src/aksesa_cli/tools/todo/set_todo_list.md",
            "aksesa_cli/tools/todo",
        ),
        (
            "src/aksesa_cli/tools/web/fetch.md",
            "aksesa_cli/tools/web",
        ),
        (
            "src/aksesa_cli/tools/web/search.md",
            "aksesa_cli/tools/web",
        ),
    ]
    if has_rg_binary:
        expected_datas.append((f"src/aksesa_cli/deps/bin/{rg_binary}", "aksesa_cli/deps/bin"))

    assert sorted(datas) == sorted(expected_datas)


def test_pyinstaller_hiddenimports():
    from aksesa_cli.utils.pyinstaller import hiddenimports

    assert sorted(hiddenimports) == snapshot(
        [
            "aksesa_cli._build_info",
            "aksesa_cli.cli.export",
            "aksesa_cli.cli.info",
            "aksesa_cli.cli.mcp",
            "aksesa_cli.cli.plugin",
            "aksesa_cli.cli.vis",
            "aksesa_cli.cli.web",
            "aksesa_cli.tools",
            "aksesa_cli.tools.agent",
            "aksesa_cli.tools.ask_user",
            "aksesa_cli.tools.background",
            "aksesa_cli.tools.display",
            "aksesa_cli.tools.dmail",
            "aksesa_cli.tools.file",
            "aksesa_cli.tools.file.glob",
            "aksesa_cli.tools.file.grep_local",
            "aksesa_cli.tools.file.plan_mode",
            "aksesa_cli.tools.file.read",
            "aksesa_cli.tools.file.read_media",
            "aksesa_cli.tools.file.replace",
            "aksesa_cli.tools.file.utils",
            "aksesa_cli.tools.file.write",
            "aksesa_cli.tools.plan",
            "aksesa_cli.tools.plan.enter",
            "aksesa_cli.tools.plan.heroes",
            "aksesa_cli.tools.shell",
            "aksesa_cli.tools.test",
            "aksesa_cli.tools.think",
            "aksesa_cli.tools.todo",
            "aksesa_cli.tools.utils",
            "aksesa_cli.tools.web",
            "aksesa_cli.tools.web.fetch",
            "aksesa_cli.tools.web.search",
            "setproctitle",
        ]
    )


def test_pyinstaller_hiddenimports_include_lazy_cli_subcommands():
    from aksesa_cli.cli._lazy_group import LazySubcommandGroup
    from aksesa_cli.utils.pyinstaller import hiddenimports

    expected_hiddenimports = {
        module_name
        for module_name, _attribute_name, _help_text in LazySubcommandGroup.lazy_subcommands.values()
    }

    assert expected_hiddenimports <= set(hiddenimports)
