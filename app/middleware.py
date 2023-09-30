from fastapi.responses import JSONResponse
from fastapi import Request

async def marg_bar_america(request: Request, call_next):

    ip = str(request.client.host)

    if ip == "1.1.1.1":
        return JSONResponse(content="DOWN WITH USA",status_code=400)

    response = await call_next(request)
    return response
