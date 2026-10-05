"""Example usage for MCP Unified Context Compaction & Rate Limiter."""
from client import MCPContextCompactionRateLimiter

if __name__ == "__main__":
    raw_logs = "trace line 1\ntrace line 2\ntrace line 2\n" * 40
    res = MCPContextCompactionRateLimiter.process_tool_context("server_logs", raw_logs, max_chars=120)
    print("Compression Ratio:", res["compression_ratio_pct"], "%")
    print("Estimated Token Cost:", res["rate_limit_token_cost"])
