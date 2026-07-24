import asyncio

from mavsdk import System


SYSTEM_ADDRESS = "udp://:14540"
TAKEOFF_ALTITUDE = 5
HOLD_SECONDS = 10


async def wait_until_connected(drone: System) -> None:
    print(f"正在連線到模擬器：{SYSTEM_ADDRESS}")
    await drone.connect(system_address=SYSTEM_ADDRESS)

    print("等待無人機連線...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("無人機已連線")
            return


async def main() -> None:
    drone = System()

    try:
        await wait_until_connected(drone)

        print("設定起飛高度...")
        await drone.action.set_takeoff_altitude(TAKEOFF_ALTITUDE)

        print("解鎖中...")
        await drone.action.arm()

        print("起飛中...")
        await drone.action.takeoff()

        print(f"懸停 {HOLD_SECONDS} 秒...")
        await asyncio.sleep(HOLD_SECONDS)

        print("返航中...")
        await drone.action.return_to_launch()

        print("流程完成")
    except Exception as exc:
        print(f"執行失敗：{exc}")


if __name__ == "__main__":
    asyncio.run(main())
