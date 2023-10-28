from fastapi import APIRouter, HTTPException, status

from app.database import DB_DEPENDECY
from app.models.review_model import Review
from app.schemas.review_schema import ReviewSchema


router = APIRouter(
    prefix="/review",
    tags=["review"]
)


@router.get("/{review_id}", status_code=status.HTTP_200_OK)
async def get_review(review_id: int, db: DB_DEPENDECY):

    review = db.query(Review).get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


@router.put("/{review_id}", status_code=status.HTTP_201_CREATED)
async def put_review(review_id: int, payload: ReviewSchema, db: DB_DEPENDECY):
    review = db.query(Review).get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.opinion = payload.opinion
    review.rate = payload.rate

    db.add(review)
    db.commit()
    db.refresh(review)

    return review
