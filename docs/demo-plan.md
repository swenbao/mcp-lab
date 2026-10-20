# Demo：MCP 術語小幫手

## 為什麼選這個？

內容小、容易看懂，也方便比對輸入與結果。第一版只使用專案內的範例資料，不需要外部 API、帳號、資料庫或模型費用。主題也能直接幫助我們學習 MCP。

這是初始建議；開始實作前可以依興趣更換題材，但保留同樣簡單的通訊目標。

## 第一版範圍

- Python + 官方 MCP SDK；實作時確認版本、建立虛擬環境並鎖定依賴。
- 一個 stdio server、一個獨立程序的測試 client。
- 一個工具 `lookup_term(term: str)`。
- 五個初始術語：`host`、`client`、`server`、`tool`、`resource`。
- 輸出以文字內容顯示術語及繁體中文定義；暫不加入資料寫入功能。

## 預期互動

```text
Client：這個 server 有哪些工具？
Server：lookup_term，必填參數 term 是字串。
Client：呼叫 lookup_term，term = "tool"。
Server：tool：接受參數並執行功能的介面，例如查詢資料。
```

這是概念對話，不是可直接傳送的完整 JSON-RPC 訊息。

## 驗收條件

1. client 透過 MCP 連線並列出 `lookup_term`，包含必填字串參數的 schema。
2. 查詢 `tool` 可取得對應定義；前後空白與英文字母大小寫會正規化。
3. 未知術語回覆清楚的「找不到術語」及可查詢清單，不讓程序崩潰。
4. 缺少必要參數時回報錯誤，之後合法呼叫仍可成功。
5. 從不同工作目錄啟動，仍能找到專案內資料。
6. client 結束後能正常清理 server 子程序；stdout 只有協議訊息。
7. README 記錄確實測試成功的安裝與執行指令。

## 目前狀態與後續方向（2026-10-20）

術語 demo 已實作並由使用者親手執行；使用者另加入 banana 作為第六筆資料。Codex 已顯示 server 連線成功、發現一個工具；實際模型工具呼叫仍待驗證。

使用者提出真實目標：WSI agent 的服務部署與多服務整合。下一步沿用術語工具改成本機 Streamable HTTP，再做假的 WSI 工具、包裝真實 WSI 入口，逐步走向服務組合與團隊伺服器部署。完整規劃見[學習路線](learning-path.md)與[WSI 整合方向](wsi-integration-plan.md)。

`glossary://all` resource 與 `quiz_term` prompt 保留為選修，不作為前往 WSI 整合的必經步驟。本機 HTTP 已準備並驗證，詳見[操作說明](03-local-http.md)；WSI 工具與對外部署尚未實作。
