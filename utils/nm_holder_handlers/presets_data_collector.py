from aiohttp import ClientSession, ClientTimeout, TCPConnector
import os
import asyncio


async def get_nms_info(nms_list: list[int]):
    timeout = ClientTimeout(total=600)
    conn = TCPConnector(limit=20)

    NM_HOLDER = os.environ.get("NM_HOLDER")

    results = list()

    async with ClientSession(timeout=timeout, connector=conn) as session:
        pending = [asyncio.create_task(get_presets(session=session, nm_id=nm, url=NM_HOLDER)) for nm in nms_list]

        done, pending = await asyncio.wait(pending, timeout=300)

        print(f'Pending task count: {len(pending)}')
        for pending_task in pending:
            pending_task.cancel()

        for done_task in done:
            task_result = done_task.result()
            results.append(task_result)
            print(f"Finished with {task_result}")

    return results



async def get_presets(session: ClientSession, nm_id: int, url: str):
    headers = {
        "Content-Type": "application/json",
    }
    print(f"Start getting info for {nm_id}")

    async with session.get(url, params={"nmid": f"{nm_id}"}, headers=headers) as response:
        return await response.json(encoding="utf-8", content_type="text/plain")
