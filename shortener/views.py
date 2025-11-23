from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect

from ua_parser import parse_os, parse_user_agent

from config.settings import URL_SHORTENER_BASE

from .base62 import base62_encoder

from .models import Shortener

from .serializer import ShortenerURLCreateRequest
from .serializer import ShortURLDetailSerializer

from drf_spectacular.utils import extend_schema

from analytics.tasks import save_analytics_task
from analytics.tracking_utils import get_client_country, get_client_ip


class ShortenerURLCreateView(APIView):
    @extend_schema(
        request=ShortenerURLCreateRequest,
        responses={201: ShortURLDetailSerializer},
        description="Adding new URL",
    )
    def post(self, request):
        Shortener_instance = Shortener.objects.create(
            original_url=request.data["original_url"],
            base62_code=base62_encoder(Shortener.objects.count() + 1),
            shortened_url=URL_SHORTENER_BASE
            + base62_encoder(Shortener.objects.count() + 1),
        )
        Shortener_instance.save()
        response_serializer = ShortURLDetailSerializer(Shortener_instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ShortenerRedirectView(APIView):
    def get(self, request, short_code):
        try:
            shortener_instance = Shortener.objects.get(base62_code=short_code)
            referer = request.META.get(
                "HTTP_REFERER", None
            )  # returns None if header is missing
            print(shortener_instance)
            print(referer)
            user_agent = request.META["HTTP_USER_AGENT"]
            parsed_os = parse_os(user_agent)
            user_os = parsed_os.family if parsed_os else None
            parsed_browser = parse_user_agent(user_agent)
            user_browser = parsed_browser.family if parsed_browser else None
            user_ip = get_client_ip(request)
            user_country = get_client_country(get_client_ip(request))
            save_analytics_task(
                shortener_instance,
                user_ip,
                user_browser,
                user_os,
                user_country,
                short_code,
            )
            print("Analytics created")
            print("Redirecting to: ", shortener_instance.original_url)
            return redirect(shortener_instance.original_url)
        except Shortener.DoesNotExist:
            return Response(
                {"detail": "Short URL not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ShortenerListURLsView(ListAPIView):
    model = Shortener
    serializer_class = ShortURLDetailSerializer
    queryset = Shortener.objects.all()


class ShortenerRetrieveURLView(RetrieveAPIView):
    model = Shortener
    serializer_class = ShortURLDetailSerializer
    queryset = Shortener.objects.all()
    lookup_field = "base62_code"
