# 無人機路線飛行模擬程式開發指南

要讓無人機在模擬軟體中依照設定好的路線（航點，Waypoints）飛行，通常需要三個核心技術：**模擬軟體（Simulator）**、**地面站／通訊協定（GCS / Protocol）**，以及**控制腳本（Scripting）**。

以下整理一套主流、開源，而且業界常用的實作方案。

---

## 推薦技術棧（Tech Stack）

目前最成熟、入門門檻也相對友善的組合是：

* **模擬器**：**SITL（Software In The Loop）** 搭配 **Gazebo** 或 **jMAVSim**。
* **飛控韌體**：**PX4** 或 **ArduPilot**（在電腦中模擬飛控電腦）。
* **通訊協定**：**MAVLink**（無人機與電腦溝通的語言）。
* **控制語言**：**Python**（使用 **DroneKit** 或 **MAVSDK** 套件）。

---

## 核心實作流程

要讓無人機自動巡航，你的程式邏輯主要分為以下幾個步驟：

```text
[ 初始化連線 ] ➔ [ 解鎖並起飛（Arm & Takeoff） ] ➔ [ 依序寫入／傳送航點 ] ➔ [ 執行航線 ] ➔ [ 返航／降落 ]
```

### 1. 建立模擬環境

首先，你需要在電腦上啟動飛控模擬。以 **PX4 + jMAVSim** 為例，在終端機啟動後，你會看到一個虛擬的無人機視窗。此時飛控已經在模擬環境中運作，並監聽本地連接埠，例如 `udp://:14540`。

### 2. 編寫 Python 控制腳本

這裡推薦使用 **MAVSDK-Python**，它的語法現代，而且是異步（Async）寫法，非常適合用來控制無人機。

下面是一個具體的 **Python 概念程式碼**，示範如何設定路線並讓無人機飛行：

```python
import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

async def run():
    # 1. 連線到模擬中的無人機
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("等待無人機連線...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("無人機已連線！")
            break

    # 2. 設定你的路線（航點清單）
    # 參數大致為：(緯度, 經度, 相對高度(米), 速度(m/s), 是否依序前進, 轉向, 其他控制參數...)
    mission_items = [
        MissionItem(22.6273, 120.3014, 10, 5, True, float('nan'), float('nan'), MissionItem.CameraAction.NONE, float('nan'), float('nan'), float('nan'), float('nan'), float('nan')),
        MissionItem(22.6283, 120.3014, 15, 5, True, float('nan'), float('nan'), MissionItem.CameraAction.NONE, float('nan'), float('nan'), float('nan'), float('nan'), float('nan')),
        MissionItem(22.6283, 120.3024, 10, 5, True, float('nan'), float('nan'), MissionItem.CameraAction.NONE, float('nan'), float('nan'), float('nan'), float('nan'), float('nan')),
    ]

    mission_plan = MissionPlan(mission_items)

    # 3. 上傳航線到飛控
    print("正在上傳航線...")
    await drone.mission.upload_mission(mission_plan)

    # 4. 解鎖並起飛
    print("解鎖無人機...")
    await drone.action.arm()

    print("開始執行航線任務...")
    await drone.mission.start_mission()

    # 5. 監控任務進度
    async for mission_progress in drone.mission.mission_progress():
        print(f"目前進度：航點 {mission_progress.current} / 總數 {mission_progress.total}")
        if mission_progress.current == mission_progress.total:
            print("航線執行完畢！")
            break

    # 6. 自動返航並降落
    print("執行自動返航...")
    await drone.action.return_to_launch()

if __name__ == "__main__":
    asyncio.run(run())
```

---

## 給新手的建議步驟

1. **先安裝環境**：如果你使用的是 Windows，強烈建議安裝 **WSL2（Ubuntu）**。因為大部分無人機模擬軟體（例如 PX4、ROS）在 Linux 環境下會更穩定。
2. **先試用圖形化工具**：可以先下載 **QGroundControl（QGC）** 地面站軟體。它有圖形化介面，你可以直接在地圖上規劃路線，看著模擬機飛行，先理解「航點（Waypoint）」的概念。
3. **再導入程式控制**：當你清楚無人機如何透過地圖飛行後，再關閉 QGC，改用上面那段 Python 程式碼連線模擬器，實現用程式碼「自動化」控制。

---

## 下一步怎麼做

下一步不要直接做完整的航點任務，先做最小可運行測試。目標只有一個：確認「連線 → 解鎖 → 起飛 → 降落／返航」整條鏈路能跑通。

建議順序如下：

1. **先把模擬器跑起來**

   用 WSL2 Ubuntu 啟動 PX4 + jMAVSim，確認模擬器有在監聽 `udp://:14540`。

2. **建立最小 Python 專案**

   在 `C:\Users\kodyf\Desktop\drone_simulation_project` 裡建立一個腳本，例如 `connect_and_arm.py`，再建立 Python 虛擬環境。

3. **先只測四個動作**

   * 連線
   * 解鎖
   * 起飛
   * 返航或降落

4. **確認基本流程正常後，再加入航點任務**

   因為航點上傳與任務執行的除錯成本比較高，先把基本通訊打通會更穩定。

下面是一個最小可行的測試腳本：

```python
import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("等待連線...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("已連線")
            break

    print("解鎖中...")
    await drone.action.arm()

    print("起飛中...")
    await drone.action.takeoff()
    await asyncio.sleep(10)

    print("返航中...")
    await drone.action.return_to_launch()

if __name__ == "__main__":
    asyncio.run(run())
```

如果這段程式能正常跑起來，下一步就可以開始做：

* 航點上傳
* 航線執行
* 任務完成後自動返航
