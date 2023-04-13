import random

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, StreamingResponse

import redis
import asyncio

from ..tasks import process_data
from ..tasks.gpu import inference_task

app = FastAPI()

redis_client = redis.Redis(host='redis', port=6379)
def generate_favicon():
    size = 64
    chat_bubble_color = "#1f8ef1"
    gear_color = "#ffffff"

    svg_template = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
        <g>
            <path fill="{chat_bubble_color}" d="M16 3h32c7.2 0 13 5.8 13 13v26c0 7.2-5.8 13-13 13h-6.2L22 58V55H16c-7.2 0-13-5.8-13-13V16c0-7.2 5.8-13 13-13z"/>
            <path fill="{gear_color}" d="M41.4 26.4l2.8-4.9-4.9-.7c-.4-.1-.8-.4-1-1L35.7 15l-4.9 2.8c-.6-.3-1.3-.5-2-.6l-.7-4.9h-5.6l-.7 4.9c-.7.1-1.4.3-2 .6L15 15l-1.6 4.9c-.2.6-.6 1-1 1l-4.9.7 2.8 4.9c-.3.6-.5 1.3-.6 2l-4.9.7v5.6l4.9.7c.1.7.3 1.4.6 2l-2.8 4.9 4.9.7c.4.1.8.4 1 1L15 49l4.9-2.8c.6.3 1.3.5 2 .6l.7 4.9h5.6l.7-4.9c.7-.1 1.4-.3 2-.6l4.9 2.8 1.6-4.9c.2-.6.6-1 1-1l4.9-.7-2.8-4.9c.3-.6.5-1.3.6-2l4.9-.7v-5.6l-4.9-.7c-.1-.7-.3-1.4-.6-2z"/>
            <circle cx="32" cy="32" r="6" fill="{chat_bubble_color}"/>
        </g>
    </svg>
    """

    return svg_template.strip()

@app.get("/favicon.ico", response_class=HTMLResponse)
async def get_favicon():
    colors = ["red", "green", "blue", "yellow", "purple", "orange"]
    color = random.choice(colors)
    size = 64

    # favicon_svg = f"""
    # <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
    #     <rect width="{size}" height="{size}" style="fill:{color}"/>
    #     <circle cx="{size // 2}" cy="{size // 2}" r="{size // 4}" style="fill:white"/>
    #     <circle cx="{size // 2}" cy="{size // 2}" r="{size // 8}" style="fill:{color}"/>
    # </svg>
    # """.strip()


    return Response(content=generate_favicon(), media_type="image/svg+xml")

@app.get('/api/message')
async def message(txt: str):
    print('INCOMING MESSAGE: ', txt)

    pubsub = redis_client.pubsub()
    pubsub.subscribe('results_channel')
    
    process_data.delay(txt)

    async def event_generator():
        while True:
            message = pubsub.get_message()
            if message is None or message['type'] != 'message':
                await asyncio.sleep(0.1)
                continue

            data = message["data"].decode()

            if data == 'STOP':
                break

            yield f'data: {data}\n\n'

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get('/api/gpu')
async def gpu(txt: str):
    print('INCOMING GPU MESSAGE: ', txt)
    
    inference_task.delay(txt)

    return ''

