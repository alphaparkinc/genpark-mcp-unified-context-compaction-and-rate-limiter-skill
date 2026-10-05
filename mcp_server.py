"""MCP server for MCP Unified Context Compaction & Rate Limiter."""
import sys
import json
from client import MCPContextCompactionRateLimiter

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "compact_and_rate_limit_context",
                "description": "Compacts verbose MCP tool output and calculates rate limit consumption",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tool_name": {"type": "string"},
                        "raw_payload": {"type": "string"},
                        "max_chars": {"type": "integer"}
                    },
                    "required": ["tool_name", "raw_payload"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "compact_and_rate_limit_context":
            args = params.get("arguments", {})
            res = MCPContextCompactionRateLimiter.process_tool_context(
                args.get("tool_name", ""),
                args.get("raw_payload", ""),
                args.get("max_chars", 1000)
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
