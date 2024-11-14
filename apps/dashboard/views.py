from rest_framework.views import APIView
from .models import Booking, RPGStatus
from django.db.models import Count, Q
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.db.models.functions import TruncMonth, TruncDay, TruncYear


class DashboardView(APIView):
    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(name='hotel_id', description='Filter by hotel ID', required=True, type=int),
            OpenApiParameter(
                name='period',
                description="Grouping level for summary (day, month, or year)",
                required=False,
                type=str,
                enum=["day", "month", "year"],
                default="month"
            ),
        ],
        # override default docstring extraction
        description='Show summary of bookings and cancellations for a hotel.',
        # provide Authentication class that deviates from the views default
        auth=None,
    )
    def get(self, request, *args, **kwargs):
        hotel_id = request.GET.get('hotel_id')
        period = request.GET.get('period', 'month')

        if period == 'month':
            period_func = TruncMonth('night_of_stay')
        elif period == 'day':
            period_func = TruncDay('night_of_stay')
        elif period == 'year':
            period_func = TruncYear('night_of_stay')
        else:
            period_func = TruncMonth('night_of_stay')

        summary = (
            Booking.objects.filter(hotel_id=hotel_id)
            .annotate(date_trunc=period_func)  # Truncate to month and add to select list
            .values('date_trunc')
            .annotate(
                booked=Count('id', filter=Q(rpg_status=RPGStatus.BOOKING)),
                cancelled=Count('id', filter=Q(rpg_status=RPGStatus.CANCELLATION))
            )
            .order_by('date_trunc')
        )
        response_data = [
            {
                'date': item['date_trunc'],
                'booked': item['booked'],
                'cancelled': item['cancelled']
            }
            for item in summary
        ]

        return JsonResponse({'Report': f'Summary by {period}', 'results': response_data})




