commit 33d7b4f8a012953e73ed625e45dcbea42048248d
Author: jackfish212 <jackfish212@outlook.com>
Date:   Wed May 13 22:07:17 2026 +0800

    chore(release): bump kimi-cli and kimi-code to 1.44.0 (#2262)

diff --git a/tests/utils/test_slash_command.py b/tests/utils/test_slash_command.py
index b5666693..ab6998da 100644
--- a/tests/utils/test_slash_command.py
+++ b/tests/utils/test_slash_command.py
@@ -19,17 +19,10 @@ def check_slash_commands(registry: SlashCommandRegistry[Any], snapshot: Any):
     """Check slash commands match snapshot."""
     import json
 
-    # Use the public list_commands() API and build the alias mapping
-    alias_to_cmd: dict[str, SlashCommand[Any]] = {}
-    for cmd in registry.list_commands():
-        alias_to_cmd[cmd.name] = cmd
-        for alias in cmd.aliases:
-            alias_to_cmd[alias] = cmd
-
     pretty_commands = json.dumps(
         {
-            alias: f"{cmd.slash_name()}: {cmd.description}"
-            for (alias, cmd) in sorted(alias_to_cmd.items())
+            trigger: f"{cmd.display_name(trigger)}: {cmd.description}"
+            for (trigger, cmd) in sorted(registry.iter_command_entries(), key=lambda item: item[0])
         },
         indent=2,
         sort_keys=True,
@@ -37,6 +30,24 @@ def check_slash_commands(registry: SlashCommandRegistry[Any], snapshot: Any):
     assert pretty_commands == snapshot
 
 
+def _noop(app: object, args: str) -> None:
+    pass
+
+
+def test_slash_command_display_name() -> None:
+    cmd = SlashCommand(
+        name="help",
+        description="Show help.",
+        func=_noop,
+        aliases=["h", "?"],
+    )
+
+    assert cmd.display_name() == "/help"
+    assert cmd.display_name("help") == "/help"
+    assert cmd.display_name("h") == "/help (h)"
+    assert cmd.display_name("?") == "/help (?)"
+
+
 def test_parse_slash_command_call():
     """Test parsing slash command calls, focusing on edge cases."""
 
@@ -164,17 +175,17 @@ def test_slash_command_registration(test_registry: SlashCommandRegistry[Any]) ->
         test_registry,
         snapshot("""\
 {
-  "?": "/help (h, ?): Show help.",
+  "?": "/help (?): Show help.",
   "basic": "/basic: Basic command.",
-  "dedup_test": "/dedup_test (dup, dup): Test deduplication.",
-  "dup": "/dedup_test (dup, dup): Test deduplication.",
-  "find": "/search (s, find): Search items.",
-  "h": "/help (h, ?): Show help.",
-  "help": "/help (h, ?): Show help.",
+  "dedup_test": "/dedup_test: Test deduplication.",
+  "dup": "/dedup_test (dup): Test deduplication.",
+  "find": "/search (find): Search items.",
+  "h": "/help (h): Show help.",
+  "help": "/help: Show help.",
   "no_doc": "/no_doc: ",
   "run": "/run: Run something.",
-  "s": "/search (s, find): Search items.",
-  "search": "/search (s, find): Search items.",
+  "s": "/search (s): Search items.",
+  "search": "/search: Search items.",
   "whitespace_doc": "/whitespace_doc: "
 }\
 """),
