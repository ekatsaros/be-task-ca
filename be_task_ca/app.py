from fastapi import FastAPI
from .user.api import user_router
from .item.api import item_router

app = FastAPI(
    title="Test API",
    description="API for e-commerce platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users"
        },
        {
            "name": "items",
            "description": "Operations with items"
        }
    ]
)
app.include_router(user_router)
app.include_router(item_router)




@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon
