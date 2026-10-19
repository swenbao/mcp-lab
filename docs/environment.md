# Python 環境紀錄

這份是安裝紀錄，先不用把套件管理當成這一課的學習內容。

## 已確認的版本

2026-10-20 查核 PyPI 與官方 SDK 文件，並在本機安裝驗證：

- Python：3.14.4；SDK 要求 Python 3.10 以上。
- 官方套件：`mcp==2.3.0`，包含 `mcp-types==2.3.0`。
- SDK 支援的最新協議：`2026-07-28`；實際 stdio client/server 連線也確認選用此版本。
- 使用 v2 的 `MCPServer` 與 `Client`，不混入 v1 的 `FastMCP` / `ClientSession` 教學寫法。
- 所有已解析的執行依賴版本記在根目錄 `requirements.lock`。這是本次 Linux / Python 3.14 環境的版本鎖定清單，不是跨平台相容保證或雜湊鎖檔。

## 重建環境

在專案根目錄執行：

```bash
python3 scripts/setup_env.py
.venv/bin/python -m pip check
```

第一次安裝需要網路。腳本會建立 `.venv`；若缺少 pip，從 PyPI 下載固定版本的 pip wheel、核對 PyPI 提供的 SHA-256，再安裝到 `.venv`。本機系統缺少 pip 與 ensurepip，因此採用這個方式，沒有變更系統 Python。

`.venv` 已由 Git 忽略；GitHub 保存的是程式與依賴清單。

開發工具的受限沙箱內曾出現 stdio 連線逾時；切到一般程序環境後，實際連線與完整驗證通過。使用者執行方式為一般終端機中的 `.venv/bin/python client.py tool`。

## 來源

- [PyPI：MCP 2.3.0](https://pypi.org/project/mcp/2.3.0/)
- [官方 Python SDK：Client](https://py.sdk.modelcontextprotocol.io/client/)
- [官方 Python SDK：v2 說明](https://py.sdk.modelcontextprotocol.io/whats-new/)
