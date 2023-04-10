from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import redis
import asyncio

from .workers.celery_app import process_data

app = FastAPI()

redis_client = redis.Redis(host='redis', port=6379)
app.queue_client = redis_client



@app.get('/api/message')
async def message(txt: str):
    pubsub = redis_client.pubsub()
    pubsub.subscribe('results_channel')
    
    process_data.delay(txt)

    async def event_generator(txt):
        while True:
            message = pubsub.get_message()
            if message is None or message['type'] != 'message':
                await asyncio.sleep(0.1)
                continue

            print(message)
            data = message["data"].decode()

            if data == 'STOP':
                break

            yield f'data: {data}\n\n'

    return StreamingResponse(event_generator(txt), media_type="text/event-stream")
