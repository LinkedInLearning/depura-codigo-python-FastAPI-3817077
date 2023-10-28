from fastapi import status

from app.routers.restaurant_router import Restaurant
from app.routers.review_router import Review


RESTAURANT_PAYLOAD = {
    "name": "Test restaurant",
    "description": "Description test of the retaurant",
    "address": "123 Street",
}
REVIEW_PAYLOAD_1 = {"opinion": "Test opinion 1", "rate": 3}
REVIEW_PAYLOAD_2 = {"opinion": "Test opinion 2", "rate": 5}

EXPECTED_REVIEW_NOT_FOUND = {"detail": "Review not found"}


def test_get_review(client, test_db_session):
    """Test get review by id"""

    client.post("/restaurant", json=RESTAURANT_PAYLOAD)
    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD["name"])
        .first()
    )

    client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_1)
    review = (
        test_db_session
        .query(Review)
        .filter(Review.opinion==REVIEW_PAYLOAD_1["opinion"])
        .first()
    )
    assert review is not None

    response = client.get(f"/review/{review.id}")
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert REVIEW_PAYLOAD_1["opinion"] == review.opinion
    assert REVIEW_PAYLOAD_1["opinion"] == response_data["opinion"]


def test_get_review_not_found(client, test_db_session):
    """Test get review by id fails, id does not exists"""

    review_id = 10
    response = client.get(f"/review/{review_id}")
    response_data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == EXPECTED_REVIEW_NOT_FOUND


def test_put_review(client, test_db_session):
    """Tesst updated review by id"""

    client.post("/restaurant", json=RESTAURANT_PAYLOAD)
    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD["name"])
        .first()
    )

    post_response = client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_1)
    post_response_data = post_response.json()
    review = (
        test_db_session
        .query(Review)
        .filter(Review.opinion==REVIEW_PAYLOAD_1["opinion"])
        .first()
    )
    assert review is not None
    assert REVIEW_PAYLOAD_1["opinion"] == review.opinion
    assert REVIEW_PAYLOAD_1["opinion"] == post_response_data["opinion"]


    response = client.put(f"/review/{review.id}", json=REVIEW_PAYLOAD_2)
    response_data = response.json()

    test_db_session.refresh(review)

    assert response.status_code == status.HTTP_201_CREATED
    assert REVIEW_PAYLOAD_2["opinion"] == review.opinion
    assert REVIEW_PAYLOAD_2["opinion"] == response_data["opinion"]


def test_put_review_not_found(client, test_db_session):
    """Test put review by id fails, id does not exists"""

    review_id = 10
    response = client.put(f"/review/{review_id}", json=REVIEW_PAYLOAD_1)
    response_data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == EXPECTED_REVIEW_NOT_FOUND
