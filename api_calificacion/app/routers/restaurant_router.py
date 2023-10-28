from fastapi import APIRouter, HTTPException, status

from sqlalchemy.sql import func 

from app.database import DB_DEPENDECY

from app.models.restaurant_model import Restaurant
from app.schemas.restaurant_schema import RestaurantSchema
from app.models.review_model import Review
from app.schemas.review_schema import ReviewSchema


router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(db: DB_DEPENDECY):

    restaurants = (
        db
        .query(*Restaurant.__table__.columns, func.avg(Review.rate).label("rate"))
        .join(Review, isouter=True)
        .group_by(Restaurant.id)
        .all()
    )

    return db.restaurants


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_restaurant(payload: RestaurantSchema, db: DB_DEPENDECY):

    restaurant = Restaurant(**payload.dict())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant


@router.get("/{restaurant_id}", status_code=status.HTTP_200_OK)
async def get_restaurant(restaurant_id: int, db: DB_DEPENDECY):

    restaurant = db.query(Restaurant).get(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant_data = (
        db
        .query(*Restaurant.__table__.columns, func.sum(Review.rate).label("rate"))
        .filter(Restaurant.id==restaurant_id)
        .join(Review, isouter=True)
        .first()
    )

    return restaurant_data


@router.put("/{restaurant_id}", status_code=status.HTTP_201_CREATED)
async def put_restaurant(restaurant_id: int, payload: RestaurantSchema, db: DB_DEPENDECY):
    restaurant = db.query(Restaurant).get(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    restaurant.name = payload.name
    restaurant.description = payload.description
    restaurant.address = payload.address

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant


@router.get("/{restaurant_id}/review/", status_code=status.HTTP_200_OK)
async def get_reviews(restaurant_id: int, db: DB_DEPENDECY):

    restaurant = db.query(Restaurant).get(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    return reviews


@router.post("/{restaurant_id}/review/", status_code=status.HTTP_201_CREATED)
async def add_review(restaurant_id: int, payload: ReviewSchema, db: DB_DEPENDECY):

    restaurant = db.query(Restaurant).get(restaurant_id)
    if restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    review_payload = {
        **payload.dict(),
        "restaurant_id": restaurant_id
    }

    review = Review(**review_payload)
    db.add(review)
    db.commit()
    db.refresh(review)

    return review
