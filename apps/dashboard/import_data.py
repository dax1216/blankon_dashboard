import pandas as pd
import os
from apps.dashboard.models import Booking
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

csv_file_path = settings.BASE_DIR / 'datasets/data.csv'
df = pd.read_csv(csv_file_path)

# Iterate through the DataFrame and create model instances
for index, row in df.iterrows():
    Booking.objects.create(
        hotel_id=row['hotel_id'],
        rpg_status=row['status'],
        room_id=row['room_reservation_id'],
        night_of_stay=row['night_of_stay']
    )

print("CSV data has been loaded into the Django database.")