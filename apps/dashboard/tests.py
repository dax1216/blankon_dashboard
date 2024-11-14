from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.dashboard.models import Booking, RPGStatus
from apps.dashboard.tasks import retrieve_bookings


@pytest.mark.django_db
@patch("requests.get")
def test_retrieve_bookings(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {
                "hotel_id": 1,
                "room_id": "C303",
                "night_of_stay": (datetime.now() - timedelta(days=1)).date(),
            },
            {
                "hotel_id": 1,
                "room_id": "D404",
                "night_of_stay": (datetime.now() - timedelta(days=1)).date(),
            },
        ],
        "next": None,
    }
    mock_get.return_value = mock_response

    retrieve_bookings()

    assert Booking.objects.count() == 2
    assert Booking.objects.filter(hotel_id=1).exists()


@pytest.mark.django_db
def test_dashboard_view_monthly_summary():
    client = APIClient()
    Booking.objects.create(
        hotel_id=1,
        room_id="A101",
        night_of_stay="2023-10-01",
        rpg_status=RPGStatus.BOOKING,
    )
    Booking.objects.create(
        hotel_id=1,
        room_id="A102",
        night_of_stay="2023-10-01",
        rpg_status=RPGStatus.CANCELLATION,
    )
    Booking.objects.create(
        hotel_id=1,
        room_id="A103",
        night_of_stay="2023-11-01",
        rpg_status=RPGStatus.BOOKING,
    )

    url = reverse("dashboard")
    response = client.get(url, {"hotel_id": 1, "period": "month"})

    assert response.status_code == 200
    assert response.json()["Report"] == "Summary by month"
    assert len(response.json()["results"]) > 0


@pytest.mark.django_db
def test_dashboard_view_day_summary():
    client = APIClient()
    Booking.objects.create(
        hotel_id=1,
        room_id="A101",
        night_of_stay="2023-10-01",
        rpg_status=RPGStatus.BOOKING,
    )
    Booking.objects.create(
        hotel_id=1,
        room_id="A102",
        night_of_stay="2023-10-01",
        rpg_status=RPGStatus.BOOKING,
    )

    url = reverse("dashboard")
    response = client.get(url, {"hotel_id": 1, "period": "day"})

    assert response.status_code == 200
    assert response.json()["Report"] == "Summary by day"
    assert len(response.json()["results"]) > 0
    res = response.json()["results"]
    assert res[0]["booked"] == 2


@pytest.mark.django_db
def test_dashboard_view_year_summary():
    client = APIClient()
    Booking.objects.create(
        hotel_id=1,
        room_id="A101",
        night_of_stay="2023-10-01",
        rpg_status=RPGStatus.BOOKING,
    )
    Booking.objects.create(
        hotel_id=2,
        room_id="A102",
        night_of_stay="2024-10-01",
        rpg_status=RPGStatus.CANCELLATION,
    )

    url = reverse("dashboard")
    response = client.get(url, {"hotel_id": 1, "period": "year"})

    assert response.status_code == 200
    assert response.json()["Report"] == "Summary by year"
    assert len(response.json()["results"]) > 0

    res = response.json()["results"]
    assert res[0]["booked"] == 1
    assert res[0]["cancelled"] == 0

    response = client.get(url, {"hotel_id": 2, "period": "year"})
    res = response.json()["results"]
    assert res[0]["booked"] == 0
    assert res[0]["cancelled"] == 1
