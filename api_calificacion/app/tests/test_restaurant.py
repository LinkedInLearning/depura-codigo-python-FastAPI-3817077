from fastapi import status

from app.routers.restaurant_router import Restaurant
from app.routers.review_router import Review


RESTAURANT_PAYLOAD_1 = {
    "name": "Test restaurant",
    "description": "Description test of the retaurant",
    "address": "123 Street",
}
RESTAURANT_PAYLOAD_2 = {
    "name": "Test other restaurant",
    "description": "Description test of the other retaurant",
    "address": "456 Street",
}
REVIEW_PAYLOAD_1 = {"opinion": "Test opinion 1", "rate": 3}
REVIEW_PAYLOAD_2 = {"opinion": "Test opinion 2", "rate": 5}

EXPECTED_RESTAURNAT_NOT_FOUND = {"detail": "Restaurant not found"}


def test_create_restaurant(client, test_db_session):
    """Test create a restaurant"""

    response = client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    response_data = response.json()

    restaurant = test_db_session.query(Restaurant).first()

    assert response.status_code == status.HTTP_201_CREATED
    assert RESTAURANT_PAYLOAD_1["name"] == restaurant.name
    assert RESTAURANT_PAYLOAD_1["name"] == response_data["name"]


def test_get_restaurant_list(client, test_db_session):
    """Test get list of restaurants"""

    response = client.get("/restaurant")
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data == []

    client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    response = client.get("/restaurant")
    response_data = response.json()

    restaurant = test_db_session.query(Restaurant).first()

    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == 1
    assert response_data[0]["name"] == restaurant.name


def test_get_restaurant(client, test_db_session):
    """Test get restaurant by id"""

    client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    client.post("/restaurant", json=RESTAURANT_PAYLOAD_2)

    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD_2["name"])
        .first()
    )

    response = client.get(f"/restaurant/{restaurant.id}")
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert type(response_data) == dict
    assert response_data["id"] == restaurant.id
    assert response_data["name"] == restaurant.name


def test_get_restaurant_not_found(client, test_db_session):
    """Test get restaurant by id fails, id does not exists"""

    restaurant_id = 10
    response = client.get(f"/restaurant/{restaurant_id}")
    response_data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == EXPECTED_RESTAURNAT_NOT_FOUND


def test_update_restaurant(client, test_db_session):
    """Test update restaurant by id"""

    response = client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    response_data = response.json()

    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD_1["name"])
        .first()
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data["id"] == restaurant.id


    response = client.put(f"/restaurant/{restaurant.id}", json=RESTAURANT_PAYLOAD_2)
    response_data = response.json()

    test_db_session.refresh(restaurant)

    assert response.status_code == status.HTTP_201_CREATED
    assert type(response_data) == dict
    assert restaurant.name == RESTAURANT_PAYLOAD_2["name"]
    assert response_data["id"] == restaurant.id
    assert response_data["name"] == restaurant.name


def test_put_restaurant_not_found(client, test_db_session):
    """Test put restaurant by id fails, id does not exists"""

    restaurant_id = 10
    response = client.put(f"/restaurant/{restaurant_id}", json=RESTAURANT_PAYLOAD_1)
    response_data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == EXPECTED_RESTAURNAT_NOT_FOUND


def test_create_restaurant_reviews_not_found(client, test_db_session):
    """Test post restaurant by id fails, id does not exists"""

    restaurant_id = 10
    response = client.post(
        f"/restaurant/{restaurant_id}/review",
        json=REVIEW_PAYLOAD_1
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == EXPECTED_RESTAURNAT_NOT_FOUND


def test_create_restaurant_review(client, test_db_session):
    """Test create restaurant reviews"""

    rest_response = client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    rest_response_data = rest_response.json()

    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD_1["name"])
        .first()
    )

    assert rest_response.status_code == status.HTTP_201_CREATED
    assert rest_response_data["id"] == restaurant.id


    response = client.post(
        f"/restaurant/{restaurant.id}/review",
        json=REVIEW_PAYLOAD_1
    )
    response_data = response.json()

    review = (
        test_db_session
        .query(Review)
        .filter(Review.restaurant_id==restaurant.id)
        .first()
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert REVIEW_PAYLOAD_1["opinion"] == review.opinion
    assert REVIEW_PAYLOAD_1["opinion"] == response_data["opinion"]


def test_get_restaurant_review(client, test_db_session):
    """Test get restaurant reviews"""

    client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD_1["name"])
        .first()
    )

    client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_1)
    client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_2)

    response = client.get(f"/restaurant/{restaurant.id}/review")
    response_data = response.json()

    reviews = (
        test_db_session
        .query(Review)
        .filter(Review.restaurant_id==restaurant.id)
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == reviews.count()


def test_get_restaurant_reviews_not_found(client, test_db_session):
    """Test get restaurant by id fails, id does not exists"""

    restaurant_id = 10
    response = client.get(f"/restaurant/{restaurant_id}/review")
    response_data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_data == EXPECTED_RESTAURNAT_NOT_FOUND


def test_get_restaurant_rate_average(client, test_db_session):
    """Test get restaurant returns expected avg"""

    client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD_1["name"])
        .first()
    )

    client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_1)
    client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_2)

    response = client.get(f"/restaurant/{restaurant.id}")
    response_data = response.json()

    expected_avg = sum([REVIEW_PAYLOAD_1["rate"], REVIEW_PAYLOAD_2["rate"]]) / 2

    assert response.status_code == status.HTTP_200_OK
    assert response_data["rate"] == expected_avg


def test_get_restaurant_list_rate_average(client, test_db_session):
    """Test get restaurant returns expected avg"""

    client.post("/restaurant", json=RESTAURANT_PAYLOAD_1)
    restaurant = (
        test_db_session
        .query(Restaurant)
        .filter(Restaurant.name==RESTAURANT_PAYLOAD_1["name"])
        .first()
    )

    client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_1)
    client.post(f"/restaurant/{restaurant.id}/review", json=REVIEW_PAYLOAD_2)

    response = client.get(f"/restaurant")
    response_data = response.json()

    expected_avg = sum([REVIEW_PAYLOAD_1["rate"], REVIEW_PAYLOAD_2["rate"]]) / 2

    assert response.status_code == status.HTTP_200_OK
    assert response_data[0]["rate"] == expected_avg