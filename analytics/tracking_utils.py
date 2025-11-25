from django.contrib.gis.geoip2 import GeoIP2
from config.settings import GEOIP_PATH


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


# BUG: Why doesn't address of db directory work?
def get_client_country(addr):
    print(
        "================================> ",
        GEOIP_PATH,
    )
    g = GeoIP2(path=GEOIP_PATH)
    try:
        return g.country(addr)
    except Exception as e:
        print(e)
        return None
