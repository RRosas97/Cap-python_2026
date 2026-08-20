from fastapi import FastAPI
from routers import login, orders_route, users
from schemas.item_class import Item

app = FastAPI()

app.include_router(login.router)
app.include_router(users.router)
app.include_router(orders_route.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/show_message")
async def show_message(message):
    return {"message": message}


@app.post("/items")
async def create_Item(item: Item):
    item.name = item.name.upper()
    return item
