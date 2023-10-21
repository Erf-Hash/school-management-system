from fastapi.responses import JSONResponse
from fastapi import Request

async def block_unknown_ip_addresses(request: Request, call_next):

    ip = str(request.client.host)

    if ip == "1.1.1.1":
        return JSONResponse(status_code=400)

    response = await call_next(request)
    return response
