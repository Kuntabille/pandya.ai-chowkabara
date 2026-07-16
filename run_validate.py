import json
import urllib.request
import urllib.error
import os

def main():
    if not os.path.exists('.agents/mcp_config.json'):
        print("Error: mcp_config.json file not found.")
        return
        
    with open('.agents/mcp_config.json', 'r') as f:
        config = json.load(f)
        try:
            token_header = config["mcpServers"]["pandya-dev"]["headers"]["Authorization"]
            token = token_header.split("Bearer ")[1]
        except KeyError:
            print("Error: Auth token not found in config.")
            return
        
    with open('canvas.json', 'r') as f:
        gdl = f.read()
    with open('logic.lua', 'r') as f:
        lua_script = f.read()
    with open('component.tsx', 'r') as f:
        ui_code = f.read()
        
    headers = {"Authorization": f"Bearer {token}"}
    
    sse_req = urllib.request.Request("http://localhost:8080/mcp/sse", headers=headers)
    response = None
    try:
        response = urllib.request.urlopen(sse_req)
        endpoint = None
        for line in response:
            line = line.decode('utf-8').strip()
            if line.startswith("event: endpoint"):
                data_line = next(response).decode('utf-8').strip()
                if data_line.startswith("data: "):
                    endpoint = data_line[6:]
                    break
        if not endpoint:
            return
    except Exception as e:
        return
        
    if endpoint.startswith("/"):
        endpoint = "http://localhost:8080" + endpoint
        
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "validate_logic_and_canvas",
            "arguments": {
                "canvas_json": gdl,
                "lua_script": lua_script,
                "ui_component_code": ui_code
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
        with urllib.request.urlopen(post_req) as post_response:
            for line in response:
                line = line.decode('utf-8').strip()
                if line.startswith("data: "):
                    data = line[6:]
                    try:
                        parsed = json.loads(data)
                        if parsed.get("id") == 1:
                            print(json.dumps(parsed, indent=2))
                            break
                    except:
                        pass
    except Exception as e:
        print("Error executing tool:", e)
    finally:
        if response:
            try:
                response.close()
            except:
                pass

if __name__ == "__main__":
    main()
