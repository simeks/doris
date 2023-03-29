from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import asyncio

app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

@app.post('/api/message')
async def message_stream(request: Request):
    payload = await request.json()
    async def event_generator():
        for c in payload['message']:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            yield {
                "retry": RETRY_TIMEOUT,
                "data": f'{c}'
            }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="info")
