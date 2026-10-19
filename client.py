"""啟動本機 server，取得工具清單，再呼叫一次工具。"""

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


async def main(term: str) -> None:
    async with Client(SERVER, read_timeout_seconds=10) as client:
        print(f"已連到 server，使用協議：{client.protocol_version}")

        print("\n1. 問 server：你有哪些工具？（tools/list）")
        listing = await client.list_tools()
        for tool in listing.tools:
            print(f"工具名稱：{tool.name}")
            print(f"用途：{tool.description}")
            print(f"輸入格式：{json.dumps(tool.input_schema, ensure_ascii=False)}")

        arguments = {"term": term}
        print("\n2. 請 server 執行工具（tools/call）")
        print(f"工具：lookup_term，參數：{json.dumps(arguments, ensure_ascii=False)}")
        result = await client.call_tool("lookup_term", arguments)
        for block in result.content:
            if isinstance(block, TextContent):
                print(f"Server 回覆：{block.text}")
        if result.is_error:
            raise SystemExit("工具執行失敗，請看上方 server 回覆。")

    print("\n本次查詢結束，本機 server 已關閉。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="透過 MCP 查詢術語")
    parser.add_argument("term", nargs="?", default="tool", help="要查詢的英文術語")
    args = parser.parse_args()
    asyncio.run(main(args.term))
