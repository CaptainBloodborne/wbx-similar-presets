from aiohttp import web
from aiohttp.web_request import Request
# from aiohttp.web_response import Response

from utils.nm_holder_handlers.presets_data_collector import get_nms_info


routes = web.RouteTableDef()


@routes.post("/get-presets")
async def func(request: Request):
    if not request.can_read_body:
        raise web.HTTPBadRequest()

    body = await request.json()

    if "nms" in body:
        presets: list[dict] = await get_nms_info(nms_list=body["nms"])
        return web.json_response(presets)
    else:
        raise web.HTTPBadRequest()


app = web.Application()
# app.on_startup.append(create_database_pool)  # Add the create and destroy pool coroutines to startup and cleanup.
# app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app, port=9000)
