# 接到 Codex：讓模型選工具

這次的問題：我們不在 `client.py` 寫死要呼叫什麼，改用一句話提出需求，模型能否透過 MCP 查到 server 的資料？

沿用現有的 `server.py`，先用已安裝的 Codex CLI 作為 host。你寫的 server 不必改；溝通改由 Codex 內建的 MCP client 處理。

## 1. 登記 server

在你剛才執行 demo 的同一台電腦，於終端機執行：

```bash
codex mcp add mcp_lab --env PYTHONUTF8=1 -- \
  /home/swenbao/桌面/mcp-lab/.venv/bin/python \
  /home/swenbao/桌面/mcp-lab/server.py
```

`mcp_lab` 是這個連線設定的名稱；`--` 後面是啟動 server 的指令。兩個路徑分別指定已裝好 SDK 的 Python，以及要執行的 server 檔案。這就是本機 server 的「安裝／新增設定」；這一步登記到 Codex 的設定，不代表模型已成功使用工具。

查看這筆設定：

```bash
codex mcp get mcp_lab
```

這個設定通常保存於執行該指令時 Codex 使用的使用者層級 `config.toml`，一般位置是 `~/.codex/config.toml`；它不在本專案的 Git 備份內。

## 2. 啟動一個新的 Codex CLI 工作階段

```bash
cd /home/swenbao/桌面/mcp-lab
codex
```

若要求登入，使用你平常的 Codex 登入方式。進入後輸入 `/mcp`，確認 `mcp_lab` 已連線且提供 `lookup_term`。`/mcp` 是在 Codex 畫面輸入，不是在 Bash 輸入。

## 3. 用一句話提出需求

在 Codex 裡輸入：

```text
請透過 mcp_lab 的 lookup_term 工具查詢 banana，並回報工具名稱、實際參數，以及 server 回傳的原文。這次只使用 MCP 工具，不要讀檔或執行 Python 指令。
```

先明確指定工具，驗證接通；之後再嘗試自然提問，觀察模型會不會自行選用。若出現工具執行確認，核對名稱與參數後依畫面操作。

驗收看的是實際工具呼叫紀錄：`lookup_term`、參數 `{"term": "banana"}`，以及 server 回傳的文字。僅有一句正確的「香蕉」回答，還不能證明曾經呼叫工具。

把第一次工具呼叫的畫面文字貼回學習對話；有連線錯誤就貼錯誤，我們依實際結果處理。

## 這次換了哪一段？

先前：你執行 `client.py` → 程式固定呼叫 `lookup_term` → server 執行。

這次：你向 Codex 提出需求 → 模型產生工具呼叫 → Codex 的 MCP client 傳送請求 → 同一個 server 執行 → 結果送回模型整理回答。

本課不會執行我們的 `client.py`。實際協議版本由 host 與 server 共同支援的版本決定，不必和先前測試 client 印出的一樣。

## 已核對與尚待驗證

- 2026-10-20 已核對本機 Codex CLI 0.162.1 的 `mcp add` / `mcp get` 指令說明。
- 既有 server 已驗證 `2026-07-28` 連線；另以獨立連線驗證 `2025-11-25` 的完整初始化、列工具與呼叫流程，SDK 未更換。
- 尚未代使用者登記 `mcp_lab`，也尚未完成真實 Codex 模型的工具呼叫；以上步驟由使用者操作後核實。
- 來源：[OpenAI 官方 MCP 設定說明](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)。
