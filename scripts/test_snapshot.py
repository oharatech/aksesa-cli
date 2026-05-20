from inline_snapshot import snapshot
import json

pretty = json.dumps({"test_cmd": "/test_cmd: First version."}, indent=2, sort_keys=True)
print("json.dumps:", repr(pretty))

# Try snapshot with explicit value
s1 = snapshot("""\

{

  "test_cmd": "/test_cmd: First version."

}\

""")
print("snapshot explicit:", repr(s1))
print("equal:", pretty == s1)

# Try snapshot with no argument
s2 = snapshot()
print("snapshot empty:", repr(s2))
print("type:", type(s2))
