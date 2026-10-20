# 學習紀錄

## 2026-10-19｜步驟 0：建立學習專案

### 需求與決定

- 先確認中文桌面路徑，再建立 `mcp-lab`；不修改既有資料夾名稱。
- 目標是理解 MCP 並實作一個能與 client 溝通的 server。
- 採用簡單的術語查詢作為初始 demo 建議。
- 專案可公開到 GitHub；每完成一個實質步驟就記錄、commit、push，不設時間排程。

### 已完成

- 初始化 main 分支。
- 建立 README、六階段學習路線、第一課、demo 規格與備份規則。
- 查閱官方架構、server 教學與 Python SDK 文件。
- 確認本機已有 Git、Python；缺少 pip、Node.js。尚未安裝 SDK，會在實作階段處理環境。

### 備份狀態

- 已建立公開 repository：https://github.com/swenbao/mcp-lab 。
- 初始化文件已完成首次 commit 與 push。
- 備份狀態更新另作一次 commit、push，完成後核對本機 HEAD 與遠端 main。
- 文件的本機 Markdown 連結檢查與 Git 空白檢查通過。

### 尚待討論／驗證

- 使用者對 host、client、server 的理解，留在第一課一起討論。
- demo 題材可依使用者興趣調整。
- 實作時確認 Python/SDK 相容性、選擇目標 host 並鎖定相容版本。

### 下一步

完成 GitHub 首次備份後，從第一課開始：用一次「查術語」的互動畫出各角色，再一起建立最小 stdio server/client。

## 2026-10-20｜第一課討論：從外部服務的接法理解 MCP

### 使用者已表達的理解

- 已閱讀第一課，並透過其他教學資源學習；能用自己的話說明 MCP 是協議，以及統一介面如何減少各個 AI 應用重複串接服務的工作。
- 能描述模型提出工具呼叫、應用程式執行、server 提供功能的大致流程。
- 推測「安裝 MCP server」包含保存連線設定；本機啟動與遠端連線的差異仍待釐清。

### 遇到的問題與教學調整

- 使用者反映現有教材過於抽象、名詞密集；接下來先沿用雲端硬碟等熟悉例子，用日常中文說明，每次只補一個概念。
- 本次回饋需釐清：host 是使用模型的應用程式；host 裡的 MCP client 負責與 server 溝通。模型提出的工具呼叫與 client 發出的 MCP 訊息，是兩段不同的介面。
- MCP 統一 client 與 server 的溝通；server 如何呼叫 Google Drive 等服務的原生 API，仍由 server 的實作者處理。Server 也可以只讀本機資料或做計算，不一定包裝外部 API，也不一定由服務原廠提供。
- 設定通常告訴應用程式如何啟動本機 server，或連到遠端 server；工具名稱、用途與參數格式通常再透過 `tools/list` 向 server 取得。不同工具的參數與可用權限仍有差異。

### 本次範圍與下一步

- 本次先進行概念回饋，未安裝依賴、未實作 server，也未將第一課標記為完成；補充內容是否理解仍待使用者回應。
- 下一步以「同一個服務換接另一個 AI 應用」檢查理解，再安排能看到工具清單、輸入與結果的最小實驗。
- 實作前仍須確認官方 SDK 的實際版本與相容協議，再鎖定依賴。

### 查核來源

- [MCP 官方架構說明](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
- [MCP 工具規範](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [VS Code 新增 MCP server 說明](https://code.visualstudio.com/docs/agent-customization/mcp-servers)

## 2026-10-20｜步驟 2a：準備第一個實驗的環境

- 使用者已用自己的話正確回答：換一個支援 MCP 的應用，不必重寫 Google Drive API 接法，因為這段由 server 處理。這是對 client/server 分工的理解證據；不等於所有第一課概念都已驗證。
- 已重新閱讀學習路線與 demo 規格，決定先讓獨立 client 列工具、呼叫術語工具，再由使用者做小修改。
- 查核 PyPI 實際發布版本並安裝 `mcp==2.3.0`；本機 Python 3.14.4，SDK 回報最新支援協議為 `2026-07-28`。
- 本機缺少 pip 與 ensurepip；已在專案 `.venv` 安裝 pip 26.2.1 與 SDK，沒有修改系統 Python。新增重建腳本與環境紀錄，完整鎖定執行依賴版本。
- 驗證：SDK 匯入、版本與 API 簽名確認成功；`pip check` 通過。另在暫存目錄從零執行安裝腳本，確認缺少 pip 時仍能依鎖定清單重建、匯入 SDK，且依賴檢查通過。環境準備完成，尚未宣稱使用者會操作工具或已完成實驗。
- 下一步：寫出最小 stdio server/client，觀察工具清單與呼叫結果。

## 2026-10-20｜步驟 2b：準備可操作的第一個工具範例

### 已完成的程式與教材

- `server.py`：以官方 v2 `MCPServer` 提供唯一工具 `lookup_term(term: str)`，查詢五筆專案內的術語資料。
- `client.py`：用目前 Python 啟動獨立 server 程序，透過 stdio 列出工具及輸入格式，再傳參數呼叫。未直接 import 查詢函式，未接模型或外部 API。
- 新增第二課：先跑查詢，再讓使用者把 `banana` 加入 server 資料並重跑，區分「修改資料」與「新增工具」。小練習尚未代做。
- README 更新為實際可執行的指令；保留使用者練習與理解驗證的待辦。

### 實際驗證

- 連線協議確認為 `2026-07-28`；工具清單只有 `lookup_term`，參數 `term` 是必填字串。
- 正常查詢、大小寫與前後空白正規化、未知術語回覆通過。
- 缺少參數時回傳工具錯誤，同一個 client 後續合法呼叫仍成功。
- 從 `/tmp` 啟動 server 與完整 client CLI 都成功。
- 另以原始 JSON-RPC 訊息檢查 server stdout 是合法 MCP 訊息；stdin 結束後 server 正常退出。SDK client 離開後沒有殘留 server 程序。
- 在開發工具的受限沙箱內遇過 stdio 連線逾時；一般程序環境中的實際 CLI 與上述驗證通過。未為此修改 SDK 或切換協議版本。

### 學習狀態與下一步

- 使用者已正確解釋 server 負責外部 API 接法；本次新範例由 agent 跑通，尚未記錄使用者已操作或理解工具發現流程。
- 下一步由使用者執行 `.venv/bin/python client.py tool`，貼回輸出，再做修改資料的小練習、用自己的話說明觀察。先不增加 resource、prompt 或 HTTP。

## 2026-10-20｜步驟 2c：使用者完成第一次查詢

- 使用者親自在一般終端機執行 `.venv/bin/python client.py`，並貼回完整成功輸出。
- 輸出顯示協議為 `2026-07-28`；工具清單包含 `lookup_term`、中文用途，以及必填字串參數 `term`。
- 未指定命令列術語時，client 使用程式設定的預設值 `tool`；呼叫參數為 `{"term": "tool"}`，收到預期中文解釋，程式正常結束並顯示 server 已關閉。
- 這次確認使用者已成功操作；對工具清單來源與參數格式的理解仍待使用者用自己的話說明。
- 下一步：先查詢不存在的 `banana`，由使用者在 `server.py` 的 `TERMS` 加一筆資料、儲存，再執行相同查詢，比較回覆與工具清單。不要代做此練習，也不提前新增工具。

## 2026-10-20｜步驟 2d：使用者完成新增資料的小練習

- 使用者先執行 `client.py banana`，貼回「找不到術語」的結果；再親手於 `server.py` 的 `TERMS` 新增 banana 資料，儲存後重跑相同指令。
- 使用者貼回的第二次輸出顯示「banana：香蕉，這是我新增的資料。」；工具清單仍只有 `lookup_term`，用途與必填參數 `term` 均未改變。
- 已檢查工作目錄差異，確認僅新增一筆 server 資料，client 未修改。以使用者實際執行輸出及檔案差異驗證本次練習。
- 操作已完成；「新增資料與新增工具的差別」仍待使用者用自己的話解釋，不僅因程式成功就認定已理解。
- 下一步：請使用者說明為什麼結果改變但工具數量不變，再進行新增第二個工具的練習。

## 2026-10-20｜步驟 2e：確認資料／工具差別，討論工具描述的來源

- 使用者已用自己的話正確解釋：`lookup_term` 查詢 `TERMS` 字典，新增 banana 只是增加資料；另外定義並登記工具函式，才會增加工具。第二課這部分的理解已確認。
- 使用者接著提問：decorator 是否把函式包裝後送給 client，以及 client 如何知道有哪些工具。拼法修正為 `@mcp.tool()`。
- 對照本機已安裝的官方 SDK 2.3.0 原始碼與官方 First steps 文件：decorator 在 server 載入函式定義時呼叫 `add_tool`，登記函式，並根據函式名稱、docstring、參數型別等產生工具描述。
- `client.list_tools()` 可發出 MCP `tools/list` 請求；server 回傳名稱、用途、輸入格式等工具描述，SDK 再解析成 Python 物件供 client 程式使用。這份範例的首次清單查詢會向 server 取得描述。
- 函式實作與 `TERMS` 資料留在 server；呼叫時 client 傳工具名稱和參數，server 找到已登記的函式並執行，再回傳結果。Python decorator 是 SDK 的便利寫法，並非 MCP 協議要求的語法。
- 本次僅閱讀程式、更新學習紀錄與 README，沒有修改範例行為。上述工具發現機制仍待使用者確認理解；下一個最小觀察可由使用者修改工具 docstring，重跑後比較「用途」欄位，再新增第二個工具。
- 來源：[官方 Python SDK First steps](https://py.sdk.modelcontextprotocol.io/get-started/first-steps/)，以及本機 SDK 的 `MCPServer.tool`、`ToolManager.add_tool`、`Tool.from_function`、`MCPServer.list_tools` 與 `Client.list_tools`。

## 2026-10-20｜步驟 4a：準備接入 Codex 的操作

- 使用者正確指出修改 docstring 會改變「用途」欄位，並說明 host 會把工具描述提供給模型，使模型能提出工具呼叫；要求往下一步，不再反覆確認已理解的細節。
- 教學節奏調整：跳到真實 AI host 的工具呼叫實驗，先用 Codex CLI；完整 JSON-RPC 格式與第二個工具留待後續需要時學習。
- 已使用 OpenAI Docs 技能核對官方 MCP 設定文件，本機 Codex CLI 為 0.162.1，已確認 `mcp add` / `mcp get` 語法；目前未登記 `mcp_lab`。
- 接入步驟已寫成 `docs/04-use-in-codex.md`：使用者登記 stdio 啟動設定，啟動新的 Codex CLI，檢查 `/mcp`，再要求透過 `lookup_term` 查 banana。
- 相容性檢查：既有 SDK 2.3.0 server 在另一條獨立連線中通過 `2025-11-25` 的 initialize → initialized → tools/list → tools/call → 正常退出；沒有混用不同協議的生命週期，也未變更依賴。
- 尚未變更使用者層級 Codex 設定或啟動模型測試。真正的 host 連線與模型工具呼叫，需使用者操作後依紀錄確認，不能把設定存在或答案正確當作工具成功的證據。
- 下一步：由使用者執行登記指令並在新的 Codex CLI 工作階段測試，貼回實際工具呼叫或連線錯誤。

## 2026-10-20｜方向調整：WSI agent 服務部署與多服務整合

### 使用者補充的目標與理解

- 真實學習目標是把既有 WSI（Whole Slide Image）agent 提供為其他程式可呼叫的服務，未來部署到合作團隊伺服器，並可能和其他 agent／普通服務組合。
- LINE Bot 是可能入口；中央統整程式或 agent 是可能的協調方式。其他服務種類、互叫流程、網路公開範圍均屬構想，尚未確認現有實作。
- 使用者已自行推導：固定流程可直接用一般 API；MCP 可提供共同工具介面；client 不一定包含 LLM，腳本也能直接呼叫。
- 本次釐清：`StdioServerParameters` 只保存啟動參數，進入 `async with Client(...)` 時 SDK 才啟動 server 子程序；HTTP server 則獨立常駐，client 連 URL。原始碼與官方 stdio／HTTP 規範已核對。
- 需補準的邊界：MCP 不要求 server 後面一定有另一層 API，也不要求一個 agent 對應一個 server。系統可同時提供 server 介面與內含 client，但 MCP 不自動設計跨 agent 的工作流程、排程或部署。

### 新進展與規劃

- 討論中使用者貼回 Codex `/mcp` 清單，顯示 `mcp_lab: connected (1 tool)`，確認 host 連線與工具發現已成功；尚未貼回模型工具呼叫，未認定端到端模型操作完成。
- 重整學習路線：本機 HTTP → 假 WSI 服務 → 包裝既有入口 → 依耗時需要設計工作狀態 → 多服務固定流程與模型選擇 → 團隊內網部署 → 使用者入口。
- 新增 `docs/wsi-integration-plan.md`，保留架構構想、普通 API 與 MCP 的取捨、可直接呼叫 Python 函式／既有 API 的差異，以及需要取得的現有專案資料。
- 本次只有文件變更；未修改 demo 程式、未實作 HTTP、未讀取真實 WSI 程式或病患影像、未對外開放服務。下一步先在本機以同一個術語工具觀察 HTTP server 的獨立生命週期。

## 2026-10-20｜本機 HTTP：準備並驗證獨立運行的 server

- 使用者同意進入下一步。已重讀學習路線與 demo 計畫，並核對已鎖定 SDK 2.3.0 的實際 HTTP API 與官方 Client 文件，未變更依賴。
- 新增 `server_http.py`，重用 `server.py` 的工具與資料，只綁定 `127.0.0.1`；預設埠 8000，可用 `--port` 調整。既有 stdio server 入口保留。
- `client.py` 新增 `--url`：提供網址時連到 HTTP server，省略時仍依原設定啟動 stdio 子程序；工具發現與呼叫程式共用。
- 實際 HTTP 驗證通過：協議 `2026-07-28`、工具清單與必填 term 格式、banana 回覆、從 `/tmp` 啟動，以及兩個獨立 client 同時查詢同一個 server。
- 生命週期驗證通過：client 結束後 server 仍存活；停止 server 後 HTTP client 非零退出且無工具結果，沒有啟動替代 server。測試服務已清理。
- 原 stdio CLI 以 banana 重跑成功，仍正常關閉子程序。新增 `docs/03-local-http.md` 與對應文件連結。
- 尚未認定使用者已操作或理解本次實驗；下一步由使用者在兩個終端機啟動 server、查詢兩次、停止 server 後重試，並說明觀察。尚未公開部署或接入真實 WSI 系統。
