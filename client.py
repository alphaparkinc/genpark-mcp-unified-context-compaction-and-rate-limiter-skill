"""MCP Unified Context Compaction & Rate Limiter.
100% Python Standard Library.
"""

class MCPContextCompactionRateLimiter:
    """Manages MCP tool execution rate limits and compresses bloated tool response context."""
    
    @staticmethod
    def process_tool_context(tool_name: str, raw_payload: str, max_chars: int = 1000) -> dict:
        original_len = len(raw_payload)
        lines = [line.strip() for line in raw_payload.splitlines() if line.strip()]
        
        deduped = []
        seen = set()
        for line in lines:
            if line not in seen:
                seen.add(line)
                deduped.append(line)
                
        compacted_text = "\n".join(deduped)
        if len(compacted_text) > max_chars:
            head = compacted_text[: int(max_chars * 0.6)]
            tail = compacted_text[-int(max_chars * 0.3) :]
            compacted_text = f"{head}\n... [TRUNCATED {len(compacted_text) - max_chars} CHARACTERS] ...\n{tail}"
            
        compression_ratio = round((1 - (len(compacted_text) / max(original_len, 1))) * 100, 2)
        return {
            "tool": tool_name,
            "original_length": original_len,
            "compacted_length": len(compacted_text),
            "compression_ratio_pct": max(0.0, compression_ratio),
            "compacted_payload": compacted_text,
            "rate_limit_token_cost": max(1, len(compacted_text) // 4)
        }
