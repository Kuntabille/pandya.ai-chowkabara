import re

with open("logic.lua.restored", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("import json"):
        continue
    if line.startswith("logic_lua ="):
        continue
    if "EPHEMERAL_MESSAGE" in line or "Created At:" in line or "Completed At:" in line or "File Path:" in line or "Total Lines:" in line or "Showing lines" in line or "The following code" in line or "Total Bytes:" in line:
        break
    if '"""' in line:
        continue
    new_lines.append(line)

with open("logic.lua", "w") as f:
    f.writelines(new_lines)
