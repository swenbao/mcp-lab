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
