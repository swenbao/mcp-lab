# 小範例：讓 LLM 決定要不要呼叫 MCP 工具

問題：把 `client.py` 寫死的工具名稱與參數，交給模型根據一句話決定，會發生什麼事？

這次新增 `llm_client.py`，只做一次工具決策，不加 agent 框架、記憶或多輪聊天。原 server 不用改。

## 填入本機設定

專案根目錄的 `.env` 已建立，請自己填入：

```dotenv
OPENAI_API_KEY=你的API_key
OPENAI_MODEL=gpt-5.4-mini
MCP_SERVER_URL=http://127.0.0.1:8000/mcp
```

`.env` 已由 Git 忽略；GitHub 只有空白 key 的 `.env.example`。程式從檔案載入 key，沒有將它放入模型上下文或 MCP 參數。若是重新下載專案，可自行將 `.env.example` 複製成 `.env`。

預設模型已核對支援 Responses API 和 function calling；實際存取仍取決於 API 帳戶。可修改 `.env` 的模型，或使用 `--model`。API 請求會依帳戶計費；每次範例最多兩次模型請求，停用自動重試。

## 執行

終端機 A 啟動 HTTP server，若已在運行就沿用：

```bash
cd /home/swenbao/桌面/mcp-lab
.venv/bin/python server_http.py
```

終端機 B 執行：

```bash
cd /home/swenbao/桌面/mcp-lab
.venv/bin/python llm_client.py "請查本專案術語表，banana 的解釋是什麼？"
```

若模型選擇用工具，畫面會印出 `LLM 選擇工具`、`LLM 產生參數`、`MCP server 回覆`，最後再印出 `LLM 最終回答`。

再比較：

```bash
.venv/bin/python llm_client.py "你好，跟我打個招呼就好。"
```

這次預期模型直接回答，畫面會明確顯示沒有呼叫 MCP 工具。是否選工具由模型決定，不能把預期輸出當成已實測結果。

## 程式的四個步驟

1. `mcp.list_tools()` 取得 `lookup_term` 的名稱、說明與輸入格式，轉成 OpenAI 的 function tool 定義。此範例只提供目前這個必填文字參數工具，並補上 strict schema 所需的 `additionalProperties: false`。
2. `llm.responses.create(..., tool_choice="auto")` 把問題與工具描述送給模型；模型可以回文字，也可以回 `function_call`。
3. 若有工具呼叫，本機程式取出名稱、JSON 參數，用 `mcp.call_tool(...)` 真正執行。模型回傳一個名稱並不等於工具已執行。
4. 把完整模型輸出與帶有對應 `call_id` 的 `function_call_output` 送回模型。第二次請求指定 `tool_choice="none"`，只整理答案，不繼續循環。

OpenAI 服務不會直接連 `127.0.0.1` 的 MCP 網址。連線與工具執行由你的本機程式處理，工具結果再由它送到 OpenAI。這支程式因此同時包含簡單的 host 流程和 MCP client 的使用。

## 已驗證與尚待驗證

- 已安裝並鎖定 `openai==3.35.1`、`python-dotenv==1.2.4`；原 `mcp==2.3.0` 與其他既有依賴未升級。
- 用真實本機 MCP HTTP server 搭配模擬 OpenAI HTTP 回覆，已驗證完整的工具描述轉換、參數轉送、結果與 call ID 對應、最終文字輸出。
- 已驗證直接回答時不執行 MCP 工具，以及模型若回傳未提供的工具名稱會被拒絕。
- 尚未使用真實 key 呼叫 OpenAI，模型決策、帳戶權限與真實端到端結果需填好 key 後驗證。模擬測試不代表真實模型決策已通過。

原有 `.venv` 已安裝依賴；重建方式仍為 `python3 scripts/setup_env.py`。

來源：[OpenAI 官方 function calling](https://developers.openai.com/api/docs/guides/function-calling)、[預設模型文件](https://developers.openai.com/api/docs/models/gpt-5.4-mini)。
