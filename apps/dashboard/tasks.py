from datetime import date, timedelta

from celery import shared_task
from django.conf import settings

from .models import Booking
from .utils import get_paginated_results


@shared_task
def retrieve_bookings():
    # get bookings from the provider API
    # get bookings based timestamp (yesterday's records)
    d = date.today() - timedelta(days=1)
    url = f"{settings.PROVIDER_API_URL}events/?timestamp__gte={d}&timestamp__lte={d}T23:59:59Z"
    while True:
        res = get_paginated_results(url)

        if res is not None:
            bookings = []
            for booking in res["results"]:
                bookings.append(
                    Booking(
                        hotel_id=booking["hotel_id"],
                        room_id=booking["room_id"],
                        night_of_stay=booking["night_of_stay"],
                    )
                )

            Booking.objects.bulk_create(bookings)

            if not res["next"]:
                break
            else:
                url = res["next"]
        else:
            break
