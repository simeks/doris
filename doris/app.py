from datetime import datetime, timedelta
import json

import asyncio
import jwt

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

# origins = [
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = "some secret key here pls"

users = [
    ('simon', 'kaka')
]

def current_user(token: str = Depends(oauth2_scheme)) -> str:
    print('Checking token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('user', None)
        if username is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid token'
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail='Invalid token'
        )

@app.post('/api/login')
def login(payload: dict[str, str]):
    for user in users:
        if payload['username'] == user[0] and payload['password'] == user[1]:
            print(f'User {payload["username"]} logged in')
            token_data = {
                'user': payload['username'],
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
            return {
                'token': token
            }
    raise HTTPException(
        status_code=401,
        detail='Incorrect username or password'
    )


@app.post('/api/message')
async def message(payload: dict[str, str], user: str = Depends(current_user)):
    async def event_generator():
        for c in payload['message']:
            yield json.dumps({'chunk': c})
            await asyncio.sleep(1)
    return EventSourceResponse(event_generator())


if __name__ == '__main__':
    import uvicorn
    import sys
    uvicorn.run(
        'app:app',
        host='127.0.0.1',
        port=5000,
        ssl_keyfile='key.pem',
        ssl_certfile='cert.pem',
        log_level='info',
        reload='-d' in sys.argv
    )
