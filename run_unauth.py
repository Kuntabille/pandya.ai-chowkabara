import json
import urllib.request
with open('.agents/mcp_config.json', 'r') as f:
    config = json.load(f)
    env_config = config["mcpServers"]["pandya-dev"]
    sse_url = env_config["url"]

# DO NOT include Authorization header
headers = {}
sse_req = urllib.request.Request(sse_url, headers=headers)
response = urllib.request.urlopen(sse_req)
endpoint = None
for line in response:
    line = line.decode('utf-8').strip()
    if line.startswith("event: endpoint"):
        endpoint = next(response).decode('utf-8').strip()[6:]
        break

if endpoint.startswith("/"):
    base_url = sse_url.split("/mcp/sse")[0]
    if base_url == "":
        base_url = "http://127.0.0.1:8080"
    endpoint = base_url + endpoint

with open('component.tsx', 'r') as f:
    component_code = f.read()
with open('logic.lua', 'r') as f:
    logic_script = f.read()
with open('canvas.json', 'r') as f:
    canvas_json = f.read()

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "simulate_gameplay",
        "arguments": {
            "component_code": component_code,
            "logic_script": logic_script,
            "canvas_json": canvas_json,
            "test_code": """
  await expect(page.locator('.game-container').first()).toBeVisible({ timeout: 5000 });
  const rects = await page.locator('rect').count();
  console.log(`Found ${rects} rects in SVG board`);
  
  // roll the dice
  await page.locator('#main_dice').click();
  await page.waitForTimeout(1000);
  console.log('Dice clicked and waited');
"""
        }
    }
}

post_req = urllib.request.Request(
    endpoint,
    data=json.dumps(payload).encode('utf-8'),
    headers={"Content-Type": "application/json"},
    method="POST"
)
try:
    urllib.request.urlopen(post_req)
except Exception as e:
    print("HTTP ERROR:", e)

for line in response:
    line = line.decode('utf-8').strip()
    if line.startswith("data: "):
        try:
            parsed = json.loads(line[6:])
            if parsed.get("id") == 1:
                print(json.dumps(parsed.get("result", {}), indent=2))
                break
        except Exception:
            pass
