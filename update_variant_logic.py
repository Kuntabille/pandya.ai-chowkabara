import re

with open("logic.lua", "r") as f:
    logic = f.read()

new_get_variant = """local function get_variant()
    local v = game.get_variation and game.get_variation() or "5x5"
    if v == "7x7" then return "7x7" end
    return "5x5"
end"""

logic = re.sub(r'local function get_variant\(\).*?return "5x5"\nend', new_get_variant, logic, flags=re.DOTALL)

with open("logic.lua", "w") as f:
    f.write(logic)
