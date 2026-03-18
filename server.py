import os
from aiohttp import web
from livekit import api

LK_URL = "ws://34.162.117.216:7880"
LK_API_KEY = "devkey"
LK_API_SECRET = "secretpassword"
ROOM_NAME = "helios-dedicated-stream"

async def handle_index(request):
    token = api.AccessToken(LK_API_KEY, LK_API_SECRET) \
        .with_identity("viewer-" + os.urandom(4).hex()) \
        .with_name("Viewer") \
        .with_grants(api.VideoGrants(room_join=True, room=ROOM_NAME)) \
        .to_jwt()
        
    with open('livekit-index.html', 'r') as f:
        html = f.read()
        
    html = html.replace('__TOKEN__', token)
    html = html.replace('__URL__', LK_URL)
    
    return web.Response(text=html, content_type='text/html')

app = web.Application()
app.router.add_get('/', handle_index)

if __name__ == '__main__':
    web.run_app(app, port=8080)
