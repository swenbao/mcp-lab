# 第二課：親眼看見 client 找工具、用工具

先想一個問題：client 的設定只寫了「啟動 server.py」，沒有列出工具，它怎麼知道 server 能做什麼？

這次先讓兩個小程式真的說上話。沒有模型替我們選工具，client 會固定呼叫 `lookup_term`；之後接到 AI 應用時，才讓模型選擇。

## 先跑一次

環境已在這台電腦準備好。打開終端機，貼上：

```bash
cd /home/swenbao/桌面/mcp-lab
.venv/bin/python client.py tool
```

你會看到兩段：

1. `tools/list`：client 問 server 有哪些工具，收到名稱、用途、輸入格式。
2. `tools/call`：client 指定 `lookup_term`，傳入 `{"term": "tool"}`，收到解釋。

最後一段結果應該是：

```text
Server 回覆：
tool：可以被呼叫的功能；呼叫時傳入參數，執行後取得結果。
```

輸入格式中的 `term` 是參數名稱，`string` 表示文字，`required` 表示必填。先看懂這三個地方就好。

## 這兩個檔案各做什麼？

- [server.py](../server.py)：保存術語資料。`lookup_term` 查資料、回傳文字；上面的 `@mcp.tool()` 把它登記成 MCP 工具。
- [client.py](../client.py)：用目前的 Python 啟動另一個 server 程序，再透過 MCP 問工具清單、呼叫工具。它沒有 import server 的查詢函式。

兩個程式都在你的電腦上，透過標準輸入／輸出溝通，這個接法叫 stdio。執行 client 時就會啟動 server；查詢結束便關閉，不必自己另開終端機啟動 server。

這份 client 是學習用的測試程式。它使用官方 SDK 的 `Client`，先替我們驗證溝通；尚未包含聊天介面或模型。

## 換你做一個小修改

先預測結果，再操作：

1. 執行 `.venv/bin/python client.py banana`，看看查不到時 server 怎麼回。
2. 打開 `server.py`，在 `TERMS` 字典加入一筆：`"banana": "香蕉，這是我新增的資料。",`。注意放在大括號內，每筆之間要有逗號。
3. 再執行同一個指令，看看回覆是否改變。

這是修改 server 的資料；工具依然只有一個 `lookup_term`。我們下一個小練習再增加工具。

完成後，用自己的話說兩件事：

- 第二次為什麼查得到 banana？哪個檔案改變了？
- 工具清單的內容，來自 client 裡的設定，還是來自 server 的回覆？

先把終端機輸出貼回對話，我們一起看；不需要先讀懂整份程式。

## 安裝與版本紀錄

若是重新下載的專案，先執行 `python3 scripts/setup_env.py`。[環境紀錄](environment.md)有安裝細節。

本次使用官方 Python SDK `mcp==2.3.0`，實際連線版本會印在畫面上。API 寫法依[官方 Client 文件](https://py.sdk.modelcontextprotocol.io/client/)與[官方 server 範例](https://py.sdk.modelcontextprotocol.io/get-started/first-steps/)，協議細節下一課再看。
