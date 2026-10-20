# MCP Lab｜MCP 研究與實作

從理解 Model Context Protocol（MCP），到親手做出可以和 client 溝通的 MCP Server。

這是一個循序學習專案：每次只增加一個概念、一個可觀察的結果，完成一個段落就記錄、commit 並 push 到 GitHub。

## 目前進度

- [x] 建立專案資料夾並初始化 Git（main）。
- [x] 整理學習路線、第一課與 demo 規格。
- [x] 建立 [GitHub 公開 repository](https://github.com/swenbao/mcp-lab) 並完成首次 push。
- [x] 實作第一個可連線的 MCP Server 與測試 client，並完成程式驗證。
- [x] 使用者親手執行、修改一筆資料，並解釋觀察結果。
- [ ] 釐清 SDK 如何登記工具，以及 client 如何取得工具描述。

目前已可執行本機 demo。使用者已完成第二課新增資料的操作，並正確說明新增資料和新增工具的差別；接著釐清工具登記與工具清單的來源。

## 先跑一次

這台電腦的環境已準備好：

```bash
cd /home/swenbao/桌面/mcp-lab
.venv/bin/python client.py tool
```

會先看到 server 提供的工具名稱、用途和輸入格式，再看到：

```text
Server 回覆：tool：可以被呼叫的功能；呼叫時傳入參數，執行後取得結果。
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

## 第一個成果

用 Python 和官方 MCP SDK 製作一個本機的「MCP 術語小幫手」。先透過 stdio 讓 client 找到 `lookup_term` 工具、傳入 `tool`，收到繁體中文解釋。不需要模型 API key，也不需要雲端主機。

接著再讓支援 MCP 的 AI 應用程式使用同一個 server；之後視學習進度增加 resource、prompt，最後才考慮 Streamable HTTP。

## 協作方式

教學與筆記使用繁體中文，檔案與程式識別名稱使用英文。每完成一個有意義的步驟，先更新紀錄，再將該步驟的檔案 commit 並 push。沒有固定時間排程。

## 官方資料

- [MCP 架構](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
- [建立 MCP Server](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server)
- [官方 Python SDK](https://py.sdk.modelcontextprotocol.io/)

資料核對日期：2026-10-19。協議與 SDK 會演進，實作時會確認相容版本並鎖定依賴。
