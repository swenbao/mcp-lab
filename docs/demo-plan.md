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

## 後續再增加

先讓支援 MCP 的 AI host 使用這個 tool；再加入 `glossary://all` resource 與 `quiz_term` prompt，最後才研究 Streamable HTTP。上述名稱是規劃，尚未實作。
