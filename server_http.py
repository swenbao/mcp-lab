"""使用同一組工具，獨立啟動本機 HTTP server。"""

import argparse

from server import mcp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="啟動本機 MCP HTTP server")
    parser.add_argument("--port", type=int, default=8000, help="本機連接埠（預設 8000）")
    args = parser.parse_args()
    print(f"\n準備啟動 HTTP server：http://127.0.0.1:{args.port}/mcp", flush=True)
    print("保持這個終端機開著；按 Ctrl+C 停止 server。\n", flush=True)
    mcp.run(transport="streamable-http", host="127.0.0.1", port=args.port)
