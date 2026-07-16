import json
import urllib.request
with open('.agents/mcp_config.json', 'r') as f:
    config = json.load(f)
    env_config = config["mcpServers"]["pandya-dev"]
    token = env_config["headers"]["Authorization"].split("Bearer ")[1]
    sse_url = env_config["url"]

headers = {"Authorization": f"Bearer {token}"}
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

test_code = """
import { test, expect } from '@playwright/experimental-ct-react';
import { CustomGameBoard } from './tempComponent';

test('should render', async ({ mount, page }) => {
  const state = {
    variables: { variation: "5x5", phase: "roll", message: "Test" },
    pieces: [],
    currentPlayerIndex: 1
  };
  
  const component = await mount(
    <CustomGameBoard state={state} onMove={() => {}} playerId="1" />
  );
  
  await expect(component).toBeVisible();
});
"""

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "validate_ui_components",
        "arguments": {
            "component_code": component_code,
            "test_code": test_code
        }
    }
}

post_req = urllib.request.Request(
    endpoint,
    data=json.dumps(payload).encode('utf-8'),
    headers={**headers, "Content-Type": "application/json"},
    method="POST"
)
try:
    urllib.request.urlopen(post_req)
except Exception as e:
    pass

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
