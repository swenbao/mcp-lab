# MCP Lab｜MCP 研究與實作

從理解 Model Context Protocol（MCP）、親手做出可以溝通的 server/client，逐步走向既有 WSI agent 的服務部署與多服務整合。

這是一個循序學習專案：每次只增加一個概念、一個可觀察的結果，完成一個段落就記錄、commit 並 push 到 GitHub。

## 目前進度

- [x] 建立專案資料夾並初始化 Git（main）。
- [x] 整理學習路線、第一課與 demo 規格。
- [x] 建立 [GitHub 公開 repository](https://github.com/swenbao/mcp-lab) 並完成首次 push。
- [x] 實作第一個可連線的 MCP Server 與測試 client，並完成程式驗證。
- [x] 使用者親手執行、修改一筆資料，並解釋觀察結果。
- [x] 討論 SDK 如何登記工具，以及 client 如何取得工具描述。
- [x] Codex 已連上 server，顯示一個工具。
- [ ] 觀察一次實際的模型工具呼叫。
- [x] 準備並驗證同一個工具的本機 HTTP 接法。
- [ ] 使用者親手觀察 HTTP server 與 client 的獨立生命週期，再練習 WSI 服務整合。
- [ ] 執行最小 LLM 決策 client，觀察直接回答與 MCP 工具呼叫。

目前已可執行 stdio 與本機 HTTP demo，也已確認 Codex 能發現工具。接下來操作[本機 HTTP 實驗](docs/03-local-http.md)，後續方向見 [WSI 整合規劃](docs/wsi-integration-plan.md)。

## 先跑一次

這台電腦的環境已準備好：

```bash
cd /home/swenbao/桌面/mcp-lab
.venv/bin/python client.py tool
```

會先看到 server 提供的工具名稱、用途和輸入格式，再看到：

```text
Server 回覆：
tool：可以被呼叫的功能；呼叫時傳入參數，執行後取得結果。
```

client 會自行啟動、關閉本機 server。沒有使用語言模型或外部 API。

若是剛下載此 repository，在專案根目錄先執行 `python3 scripts/setup_env.py`；需要 Python 3.10 以上與網路。本次實測 Python 3.14.4、官方 SDK `mcp==2.3.0`、協議 `2026-07-28`，詳細版本與重建方式見[環境紀錄](docs/environment.md)。

## 從這裡開始

1. [學習路線](docs/learning-path.md)：每一課的問題、實作與完成條件。
2. [第一課：MCP 是什麼](docs/01-mcp-basics.md)：先分清楚協議、host、client 與 server。
3. [Demo 規格](docs/demo-plan.md)：MCP 術語小幫手。
4. [學習紀錄](notes/progress.md)：保留每次完成的內容、問題與下一步。
5. [GitHub 備份方式](docs/github-backup.md)：每個完成的段落都 commit、push。
6. [第二課：找工具、用工具](docs/02-first-tool.md)：執行 demo，再親手改一筆資料。
7. [接到 Codex：讓模型選工具](docs/04-use-in-codex.md)：登記本機 server，檢查實際工具呼叫。
8. [WSI 整合方向](docs/wsi-integration-plan.md)：遠端服務、一般 API、MCP 與多服務協作的關係。
9. [本機 HTTP 實驗](docs/03-local-http.md)：兩個終端機，觀察 server 獨立運行與 client 連線。
10. [LLM 決策 client](docs/05-llm-client.md)：在本機 `.env` 填 key，讓模型決定是否呼叫工具。

## 第一個成果

用 Python 和官方 MCP SDK 製作一個本機的「MCP 術語小幫手」。先透過 stdio 讓 client 找到 `lookup_term` 工具、傳入 `tool`，收到繁體中文解釋。不需要模型 API key，也不需要雲端主機。

接著讓支援 MCP 的 AI 應用程式使用同一個 server，並提早練習本機 Streamable HTTP，逐步應用到 WSI 服務整合。Resource、prompt 留在需要時學習。

## 協作方式

教學與筆記使用繁體中文，檔案與程式識別名稱使用英文。每完成一個有意義的步驟，先更新紀錄，再將該步驟的檔案 commit 並 push。沒有固定時間排程。

## 官方資料

- [MCP 架構](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
- [建立 MCP Server](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server)
- [官方 Python SDK](https://py.sdk.modelcontextprotocol.io/)

資料核對日期：2026-10-19。協議與 SDK 會演進，實作時會確認相容版本並鎖定依賴。
