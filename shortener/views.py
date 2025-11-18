from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect

from django.contrib.gis.geoip2 import GeoIP2

from ua_parser import parse_os, parse_user_agent

from config.settings import GEOIP_PATH

from .base62 import base62_encoder

from .models import Shortener

from .serializer import ShortenerURLCreateRequest
from .serializer import ShortURLDetailSerializer

from drf_spectacular.utils import extend_schema

from analytics.tasks import save_analytics_task


URL_SHORTENER_BASE = "http://short.ly/"


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
            shortener_instance = Shortener.objects.get(
                shortened_url=URL_SHORTENER_BASE + short_code
            )
            referer = request.META.get(
                "HTTP_REFERER", None
            )  # returns None if header is missing
            print(referer)
            user_agent = request.META["HTTP_USER_AGENT"]
            parsed_os = parse_os(user_agent)
            user_os = parsed_os.family if parsed_os else None
            parsed_browser = parse_user_agent(user_agent)
            user_browser = parsed_browser.family if parsed_browser else None
            user_ip = get_client_ip(request)
            user_country = get_client_country(get_client_ip(request))
            save_analytics_task(
                shortener_instance, user_ip, user_browser, user_os, user_country, short_code
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


def get_client_ip(request):
    # It seems we need to do extra work to get the real client IP if behind a proxy.
    # First check if behind a proxy
    print("HTTP_X_FORWARDER_FOR: ", request.META.get("HTTP_X_FORWARDED_FOR"))
    print("REMOTE_ADDR: ", request.META.get("REMOTE_ADDR"))
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs: client, proxy1, proxy2
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


# TODO: Complete this
# This needs address to db
# BUG: Why doesn't address of db directory work?
def get_client_country(addr):
    print(
        "================================> ",
        GEOIP_PATH / "dbip-country-lite-2025-11.mmdb",
    )
    g = GeoIP2(path=GEOIP_PATH / "dbip-country-lite-2025-11.mmdb")
    try:
        return g.country(addr)
    except Exception as e:
        print(e)
        return None
