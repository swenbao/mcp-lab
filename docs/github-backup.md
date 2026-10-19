# GitHub 備份方式

## 已確認的工作習慣

使用者需要的是互動過程中的雲端備份。每完成一個實質步驟，或新增一份有內容的文件，就提交並推送；不使用每小時、每日或其他時間排程。

每一個實質步驟可以包含相關程式與相應筆記，不需要將每次打字或存檔各自做成一個 commit。

## 每次操作

在 repository 根目錄執行：

```bash
git status --short
git diff
# 更新 notes/progress.md，並明確選取這次完成的檔案：
git add README.md notes/progress.md
git diff --cached
git commit -m "docs: record learning progress"
git push origin main
```

上面的 git add 是例子，實際依當次變更選擇檔案。公開 repo 的內容應是專案程式與可公開的學習紀錄；帳密、token 與私人資料不放進去。

## 確認備份

```bash
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

本機 HEAD 與遠端 main 的 commit SHA 一致，才表示該次 commit 已備份。未 commit 的檔案不會因為 push 而上傳。

如果登入失效、網路中斷或 push 失敗，保留本機 commit，向使用者說明狀態，問題解除後補推。遇到遠端衝突先查明原因，不使用 force push 覆寫雲端內容。

## 換一個聊天繼續

讓新的聊天使用這個專案資料夾，先閱讀 `AGENTS.md` 與 `notes/progress.md`。備份規則已寫在專案內，後續協作者可以接續執行。
