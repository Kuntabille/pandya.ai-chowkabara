import json
import urllib.request
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def push_to_env(env_name, use_update_game=False, game_id=None):
    print(f"Pushing to {env_name}...")
    with open('.agents/mcp_config.json', 'r') as f:
        config = json.load(f)
        env_config = config["mcpServers"][env_name]
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
            from urllib.parse import urlparse
            parsed = urlparse(sse_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
        endpoint = base_url + endpoint
        
    with open('canvas.json', 'r') as f:
        canvas_json = f.read()
    with open('logic.lua', 'r') as f:
        logic_script = f.read()
    with open('component.tsx', 'r') as f:
        component_code = f.read()

    if use_update_game:
        # In DEV we use relative path, in PROD we used the hardcoded UUID but using relative is better
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "update_game",
                "arguments": {
                    "directory": f"assets/generated/{game_id}",
                    "canvas_json": canvas_json,
                    "logic_script": logic_script,
                    "component_code": component_code
                }
            }
        }
    else:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "create_game",
                "arguments": {
                    "name": "Chowka Bara",
                    "gdl": canvas_json,
                    "lua_script": logic_script,
                    "ui_component_code": component_code
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
    except urllib.error.HTTPError as e:
        print(f"Error pushing to {env_name}: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
        return

    for line in response:
        line = line.decode('utf-8').strip()
        if line.startswith("data: "):
            try:
                parsed = json.loads(line[6:])
                if parsed.get("id") == 1:
                    if "error" in parsed:
                        print(f"Error: {parsed['error']}")
                    else:
                        print("Result:", json.dumps(parsed.get("result", {}), indent=2))
                    break
            except Exception as e:
                pass
    print(f"Done pushing to {env_name}\n")

if __name__ == "__main__":
    push_to_env("pandya-dev", use_update_game=True, game_id="a3449906-c0f5-42d7-9887-0340a8478c88")
    push_to_env("pandya-prod", use_update_game=True, game_id="6f8907ba-e545-4997-8450-7ae1c89fabb6")
