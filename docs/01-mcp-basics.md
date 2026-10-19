# 第一課：MCP 是什麼？

想像你問 AI：「請查詢我們的術語表，告訴我 tool 是什麼。」AI 應用程式需要一套共同規則，知道術語服務有哪些功能、接受什麼輸入，以及如何取得結果。MCP（Model Context Protocol）就是這樣的標準介面協議。

MCP Server 是實作這套協議、提供資料或操作能力的程式。它可以是同一台電腦上的程序；建立 server 不代表一定要租一台主機。

## 三個角色

| 角色 | 工作 | 本專案的例子 |
| --- | --- | --- |
| Host | 管理 AI 互動及 MCP 連接 | 後續選定的 AI 應用程式 |
| Client | 按 MCP 規則與 server 交換訊息 | 先寫的小型 Python 測試程式；之後是 host 裡的 client |
| Server | 提供功能並處理請求 | 我們的術語查詢程式 |

概念路徑：

```text
你提出問題
  → AI 應用程式（host，包含 client）
  → MCP 訊息
  → 術語小幫手（server）
  → 讀取範例術語表並回傳結果
  → AI 應用程式整理回答
```

第一個實驗會直接用測試 client 取得結果，因此可以先驗證協議通訊，再學模型如何選擇工具。術語查詢本身不需要呼叫語言模型。

## Server 可以提供什麼？

| 能力 | 用途 | 後續實驗 |
| --- | --- | --- |
| Tool | 接受參數並執行功能 | `lookup_term(term="tool")` |
| Resource | 提供可讀取的資料 | 一份完整術語表 |
| Prompt | 提供可重用的提示模板 | 根據術語產生學習測驗的提示 |

tool 的介面會描述名稱、用途與輸入格式。client 可透過 `tools/list` 取得清單，再透過 `tools/call` 呼叫；這和直接 import 一個 Python 函式不同。

## 訊息走哪裡？

- **stdio**：client 啟動本機 server 子程序，透過標準輸入與輸出交換訊息。第一個實驗採用這個方式。server 的除錯日誌應寫到 stderr，避免干擾協議訊息。
- **Streamable HTTP**：使用 HTTP 傳送 MCP 訊息；適合之後研究跨程序服務與遠端連接。本專案先在 localhost 練習。

上述角色、能力與傳輸概念可參考 [官方架構說明](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) 及 [stdio 規範](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)。

## 留意版本

本次閱讀的官方文件是 2026-07-28 版。舊教學常以 `initialize` 描述連線生命週期；這一版改為每個請求攜帶版本與能力資訊，並提供 `server/discover`。實作時會依安裝的 SDK 與目標 host 共同支援的版本選擇流程，讓 SDK 處理協議細節，不把不同年代的範例拼在一起。詳見 [官方 discovery 說明](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture#statelessness-and-discovery)。

## 下次一起回答

1. MCP、MCP Server 和模型，分別是什麼？
2. 為何第一個實驗不需要模型 API key？
3. 如果把術語表換成公開天氣資料，哪個角色負責取得資料？

這些問題是討論起點；目前尚未記錄使用者已完成本課。
