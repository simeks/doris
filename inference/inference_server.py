import queue
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import pydantic
import uvicorn

class StreamRequest(pydantic.BaseModel):
    text: str


app = FastAPI()
input_queue: queue.Queue = queue.Queue()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def work_thread():
    pass

@app.on_event('startup')
async def startup():
    print('Starting...')
    threading.Thread(target=work_thread, daemon=True)
    print('Started')

@app.post('/stream')
async def stream(req: StreamRequest):
    def event_stream():
        output_queue = queue.Queue()
        input_queue.put_nowait((req, output_queue))
        while True:
            output = output_queue.get()
            yield f'data: {output}'
        pass
    return StreamingResponse(event_stream(), media_type='text/event-stream')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

