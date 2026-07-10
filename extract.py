import json
import re
import os

path = os.path.expanduser('~/.gemini/antigravity-cli/brain/f62615d2-b175-467c-a776-96348cae5b03/.system_generated/logs/transcript_full.jsonl')
found = False
with open(path) as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'TOOL_RESPONSE':
                content = data.get('content', '')
                if 'File Path: `file:///Users/chandrashekarvijayarenu/code/chowkabara/logic.lua`' in content:
                    lines = content.split('\n')
                    code_lines = []
                    start_parsing = False
                    for l in lines:
                        if start_parsing:
                            if l == 'The above content shows the entire, complete file contents of the requested file.':
                                break
                            m = re.match(r'^\d+:\s?(.*)$', l)
                            if m:
                                code_lines.append(m.group(1))
                            else:
                                code_lines.append(l)
                        elif 'The following code has been modified' in l:
                            start_parsing = True
                    
                    if code_lines:
                        # Find the first one with 292 lines
                        if len(code_lines) >= 290:
                            with open('/Users/chandrashekarvijayarenu/code/chowkabara/logic.lua', 'w') as out:
                                out.write('\n'.join(code_lines))
                            print("Extracted successfully.")
                            found = True
                            break
        except Exception as e:
            pass

if not found:
    print("Not found")
