# 無人機路線飛行模擬專案

這是一個單頁 HTML 版本的專案入口，內容整理自無人機模擬控制筆記。

## 內容

- `index.html`：單頁展示頁
- `drone_simulation.md`：原始整理稿

## 目標

先完成最小可運行測試：

1. 連線
2. 解鎖
3. 起飛
4. 返航／降落

之後再加入：

- 航點上傳
- 航線執行
- 任務完成自動返航

## 本機開啟

直接用瀏覽器打開 `index.html` 即可。

## 第一個可執行腳本

目前已加入 `connect_and_arm.py`，用途是先做最小測試：

1. 連線到模擬器
2. 解鎖
3. 起飛
4. 返航

執行方式：

```powershell
cd C:\Users\kodyf\Desktop\drone_simulation_project
.\.venv\Scripts\Activate.ps1
python connect_and_arm.py
```

前提是：

- 模擬器已經啟動
- 模擬器監聽 `udp://:14540`
- 已安裝 `mavsdk`
