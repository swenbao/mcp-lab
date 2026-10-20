# 本機 HTTP：server 先跑著，client 再連過去

問題：client 結束之後，server 能不能繼續等下一個人來查詢？

這次沿用 `lookup_term` 與你新增的 banana 資料，只改連線方式。兩個終端機都在同一台電腦上，不需要模型或額外帳號。

## 終端機 A：先啟動 server

```bash
cd /home/swenbao/桌面/mcp-lab
.venv/bin/python server_http.py
```

保持這個終端機開著。它會顯示準備啟動的網址 `http://127.0.0.1:8000/mcp`，然後持續運行，不會馬上回到命令提示符。

若看到 `address already in use`，代表 8000 埠已被其他程式使用，可改跑 `.venv/bin/python server_http.py --port 8001`，並將下方 client 網址的 8000 一起換成 8001。

## 終端機 B：連到網址，查兩次

```bash
cd /home/swenbao/桌面/mcp-lab
.venv/bin/python client.py banana --url http://127.0.0.1:8000/mcp
.venv/bin/python client.py host --url http://127.0.0.1:8000/mcp
```

每次都會列工具並查詢；banana 應回覆你新增的文字。每次 client 結束後，終端機 A 的 server 都繼續運行。這兩次是不同的 client 程序，連到同一個 HTTP server 程序。

## 停止 server，再查一次

在終端機 A 按 `Ctrl+C`，再到終端機 B 執行相同的 HTTP 查詢。

這次預期連線失敗，可能看到 SDK 的錯誤堆疊。Client 不會替你啟動一個新的 HTTP server；回到 A 重新啟動後，查詢才會恢復。

先完成這三段，貼回查詢輸出與停止 server 後的結果，說明你觀察到的生命週期差別。

## 程式改了哪裡？

[server_http.py](../server_http.py)匯入原本的 `mcp` 物件，因此工具和資料只有一份。匯入 `server.py` 時，不會執行它的 `if __name__ == "__main__"` 區塊；HTTP 入口自己呼叫：

```python
mcp.run(transport="streamable-http", host="127.0.0.1", port=args.port)
```

[client.py](../client.py)根據有沒有 `--url` 選擇：

```python
target = url if url is not None else SERVER
async with Client(target, read_timeout_seconds=10) as client:
```

- 給 `StdioServerParameters`：SDK 啟動本機子程序，透過 stdin/stdout 溝通。
- 給 HTTP URL：SDK 連到已運行的服務，不啟動 server 子程序。

後面的 `list_tools()` 與 `call_tool()` 不必改。這是同一套工具透過另一個傳輸方式提供服務。

`127.0.0.1` 代表這台電腦本身，`8000` 是連接埠，`/mcp` 是 MCP 請求入口；它不是一般網頁。現在只接受本機連線，還不是給其他電腦使用的部署。

HTTP server 啟動後，修改 Python 檔案要停止並重新啟動才會載入；這個範例沒有自動重載。原 stdio client 每次會啟動新的 server，所以每次都讀到新的程式。

## 驗證與版本

2026-10-20 使用鎖定的官方 SDK `mcp==2.3.0`，本機 HTTP 實測協議 `2026-07-28`。已驗證工具清單、banana 查詢、兩個獨立 client 共用 server、client 結束後 server 存活，以及 server 停止後查詢失敗。原本 stdio 模式也已重跑成功。

依據[官方 Client 文件](https://py.sdk.modelcontextprotocol.io/client/)與本機該版本的 `MCPServer.run_streamable_http_async` API。依賴沒有更換，不手寫或混用其他版本的握手流程。
