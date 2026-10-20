"""以 stdio 啟動 server，或用 HTTP 連到已啟動的 server，再呼叫工具。"""

import argparse
import asyncio
import json
from pathlib import Path
import sys

from mcp import Client, StdioServerParameters
from mcp.types import TextContent


# 這段設定回答「用什麼指令啟動哪一個 server」。
# 工具清單則是在連線後向 server 取得，沒有寫死在這裡。
SERVER = StdioServerParameters(
    command=sys.executable,
    args=[str(Path(__file__).resolve().with_name("server.py"))],
    env={"PYTHONUTF8": "1"},
)


async def main(term: str, url: str | None = None) -> None:
    # 給 URL 時只連線，不啟動 server 子程序。
    target = url if url is not None else SERVER
    if url is not None:
        print(f"\n透過 HTTP 連線：{url}")
    async with Client(target, read_timeout_seconds=10) as client:
        print(f"已連到 server，使用協議：{client.protocol_version}")

        print("\n1. 問 server：你有哪些工具？（tools/list）\n")
        listing = await client.list_tools()
        for tool in listing.tools:
            print(f"工具名稱：{tool.name}")
            print(f"用途：{tool.description}")
            print(f"輸入格式：\n{json.dumps(tool.input_schema, ensure_ascii=False, indent=2)}")

        arguments = {"term": term}
        print("\n2. 請 server 執行工具（tools/call）\n")
        print("工具：lookup_term")
        print(f"參數：{json.dumps(arguments, ensure_ascii=False)}")
        result = await client.call_tool("lookup_term", arguments)
        for block in result.content:
            if isinstance(block, TextContent):
                print(f"\nServer 回覆：\n{block.text}")
        if result.is_error:
            raise SystemExit("工具執行失敗，請看上方 server 回覆。")

    if url is None:
        print("\n本次查詢結束，本機 server 已關閉。\n")
    else:
        print("\n本次查詢結束，client 已離線；HTTP server 由另一個終端機繼續運行。\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="透過 MCP 查詢術語")
    parser.add_argument("term", nargs="?", default="tool", help="要查詢的英文術語")
    parser.add_argument("--url", help="HTTP MCP 網址；省略時使用原本的 stdio 接法")
    args = parser.parse_args()
    asyncio.run(main(args.term, args.url))
