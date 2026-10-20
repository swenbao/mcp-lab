"""提供一個查術語的 MCP 工具。"""

from mcp.server import MCPServer


mcp = MCPServer("MCP 術語小幫手", log_level="WARNING")

# 這就是 server 使用的資料；第一個小練習會修改這裡。
TERMS = {
    "host": "你使用的 AI 應用程式，負責對話、管理工具與執行流程。",
    "client": "負責按照 MCP 規則，與某個 server 溝通的程式。",
    "server": "接收 MCP 請求，提供資料或執行功能的程式。",
    "tool": "可以被呼叫的功能；呼叫時傳入參數，執行後取得結果。",
    "resource": "server 提供給應用程式讀取的資料。",
    "banana": "香蕉，這是我新增的資料。",
}


@mcp.tool()
def lookup_term(term: str) -> str:
    """查詢 MCP 術語的繁體中文解釋，輸入一個英文術語。"""
    key = term.strip().lower()
    if key in TERMS:
        return f"{key}：{TERMS[key]}"
    return f"找不到術語「{term}」。可查詢：{', '.join(TERMS)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
