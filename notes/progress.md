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
