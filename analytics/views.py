from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Analytics
from .serializer import AnalyticsListViewSerializers


# Create your views here.
class AnalyticsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Analytics
    serializer_class = AnalyticsListViewSerializers
    queryset = Analytics.objects.all()


class AnalyticsCodeList(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Analytics
    serializer_class = AnalyticsListViewSerializers

    def get_queryset(self):  # type: ignore
        base62_code = self.kwargs.get("base62_code")
        if base62_code:
            return Analytics.objects.filter(base62_code=base62_code)
        return Analytics.objects.none()
