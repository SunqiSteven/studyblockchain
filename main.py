

'''
 run server

'''

from aiohttp import web

async def Version(request):
    web.Response(text="v1.0.0")
    
app = web.Application()
app.add_routes([web.get('/version',Version)])
web.run_app(app)    




