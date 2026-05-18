import asyncio

from pornpics import Client, AsyncClient

cl = Client()
asynccl = AsyncClient()

# print(cl.get_gallery("atk-premium-starring-layla-monroe-xxx-gallery-42380000"))
print(asyncio.run(asynccl.get_gallery("atk-premium-starring-layla-monroe-xxx-gallery-42380000")))
