from fastapi import FastAPI
from .user.api import user_router
from .item.api import item_router

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)




@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon
