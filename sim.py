import json, urllib.request

def main():
    with open('.agents/mcp_config.json', 'r') as f:
        config = json.load(f)
        token = config["mcpServers"]["pandya-dev"]["headers"]["Authorization"].split("Bearer ")[1]
            
    headers = {"Authorization": f"Bearer {token}"}
    
    sse_req = urllib.request.Request("http://127.0.0.1:8080/mcp/sse", headers=headers)
    response = urllib.request.urlopen(sse_req)
    endpoint = None
    for line in response:
        line = line.decode('utf-8').strip()
        if line.startswith("event: endpoint"):
            endpoint = next(response).decode('utf-8').strip()[6:]
            break
            
    if endpoint.startswith("/"):
        endpoint = "http://127.0.0.1:8080" + endpoint
        
    with open('logic.lua', 'r') as f:
        logic_script = f.read()

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "simulate_game_logic",
            "arguments": {
                "lua_script": logic_script,
                "active_variations": ""
            }
        }
    }
    
    post_req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers={**headers, "Content-Type": "application/json"},
        method="POST"
    )
    
    urllib.request.urlopen(post_req)
    for line in response:
        line = line.decode('utf-8').strip()
        if line.startswith("data: "):
            try:
                parsed = json.loads(line[6:])
                if parsed.get("id") == 1:
                    print(json.dumps(parsed.get("result", {}), indent=2))
                    break
            except:
                pass

if __name__ == "__main__":
    main()
