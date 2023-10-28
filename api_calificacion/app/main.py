from fastapi import FastAPI

from app.database import engine

from app.models import restaurant_model, review_model

from app.routers import restaurant_router
from app.routers import review_router


app = FastAPI()
app = FastAPI(title="Restaurant Review API")

review_model.Base.metadata.create_all(bind=engine) 
restaurant_model.Base.metadata.create_all(bind=engine) 

app.include_router(restaurant_router.router)
app.include_router(review_router.router)


@app.get("/")
async def home():
    return {
        "name": "Restaurant Review API",
        "version": "1.0.0"
    }
