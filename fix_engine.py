import re

with open("/Users/chandrashekarvijayarenu/code/pandya.ai/internal/gameauthor/luaengine/hostapi.go", "r") as f:
    content = f.read()

new_get_nodes = """
		tb := L.NewTable()
		for i, nodeStr := range pathDef.Coordinates {
			// nodeStr is "x,y"
			parts := strings.Split(nodeStr, ",")
			if len(parts) == 2 {
				x, errX := strconv.Atoi(parts[0])
				y, errY := strconv.Atoi(parts[1])
				if errX == nil && errY == nil {
					coordTb := L.NewTable()
					coordTb.RawSetString("x", lua.LNumber(x))
					coordTb.RawSetString("y", lua.LNumber(y))
					tb.RawSetInt(i+1, coordTb)
					continue
				}
			}
			tb.RawSetInt(i+1, lua.LString(nodeStr))
		}
		L.Push(tb)
		return 1
"""

content = re.sub(r'tb := L\.NewTable\(\)\s*for i, node := range pathDef\.Coordinates \{\s*tb\.RawSetInt\(i\+1, lua\.LString\(node\)\)\s*\}\s*L\.Push\(tb\)\s*return 1', new_get_nodes.strip(), content)

# Also fix get_node
new_get_node = """
			nodeStr := pathDef.Coordinates[index-1]
			parts := strings.Split(nodeStr, ",")
			if len(parts) == 2 {
				x, errX := strconv.Atoi(parts[0])
				y, errY := strconv.Atoi(parts[1])
				if errX == nil && errY == nil {
					coordTb := L.NewTable()
					coordTb.RawSetString("x", lua.LNumber(x))
					coordTb.RawSetString("y", lua.LNumber(y))
					L.Push(coordTb)
					return 1
				}
			}
			L.Push(lua.LString(nodeStr))
"""

content = re.sub(r'L\.Push\(lua\.LString\(pathDef\.Coordinates\[index-1\]\)\)', new_get_node.strip(), content)

if "strconv" not in content[:500]:
    content = content.replace('"strings"', '"strings"\n\t"strconv"')

with open("/Users/chandrashekarvijayarenu/code/pandya.ai/internal/gameauthor/luaengine/hostapi.go", "w") as f:
    f.write(content)
