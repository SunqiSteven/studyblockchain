
import asyncio
import time
import _thread
import random

loop = asyncio.get_event_loop()
async def hello(future):
    await asyncio.sleep(3)
    # await time.sleep(3)
    print("hello")
    # loop.stop()
    # future.set_result('hello result')
    future.set_exception(Exception('22')) 

async def foo():
    print('foo')

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    try:
        future.result()
    except:
        print(future.exception())
    # loop.stop()

# def create():
#     time.sleep(5)
#     future = asyncio.Future()
#     asyncio.ensure_future(slow_operation(future))
#     future.add_done_callback(got_result)

# _thread.start_new_thread(create,())

# future = asyncio.Future()
# asyncio.ensure_future(slow_operation(future))
# future.add_done_callback(got_result)
# print('111')
# future = asyncio.Future()
# asyncio.ensure_future(hello(future))
# future.add_done_callback(got_result)
# print(random.randrange(2**256-1))
# print(random.random())

# try:
#     loop.run_forever()
# finally:
#     loop.close()

# def pool(size):
#     assert size > 10 and size < 20,'invalid size'
#     print('pool logic')


# try:
#     pool(100)
# except AssertionError as err:
#     print(err.message)



import aiohttp

# session = aiohttp.ClientSession()
# time.sleep(3)
# await session.close()
# async with aiohttp.ClientSession() as session:
#     async with session.get("http://127.0.0.1:8080") as resp:
#         print(resp.status)
#         print(await resp.text())

# with open('./version.py') as fd:
    # print(fd.read(2))
# async def request():
#     session = aiohttp.ClientSession() 
#     # print(session)
#     resp = await ClientSession.get("http://127.0.0.1:8080")
#     print(resp.status)
#     text = await resp.text()
#     print(text)
#     await session.close()


# loop.run_until_complete(request())


# print('sunqi {}'.format('sunqi'))

# with open('./keystore.txt','wb') as fd:
#     fd.write('world'.encode('utf-8'))
#     fd.write('hello'.encode('utf-8'))


# async def r():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://httpbin.org/get') as resp:
#             print(resp.status)
#             print(await resp.text())
# import time
# async def foo():
#     # asyncio.sleep(2)
#     time.sleep(3)
#     print('323')
#     return '22'
# try:
#     foo().send(None)
# except StopIteration as err:
#     print(err.value)




