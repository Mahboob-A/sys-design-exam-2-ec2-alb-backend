from urllib.parse import urlparse
from django.conf import settings


def get_current_host(request) -> str:
    """Returns the host url with current scheme
     
     Return: 
        - Host with Port with Scheme 
        - Host    
    """

    scheme = "https" if request.is_secure() else "http"
    host= request.get_host()

    # print("host: ", host)
    if host in ["127.0.0.1", "localhost"]:
        # DJANGO_APP_PORT: 8000
        port = settings.DJANGO_DOCKER_PORT
        return f"{scheme}://{host}:{port}", host
    else:
        return f"{scheme}://{host}", host

    # scheme = request.is_secure() and "https" or "http"
    # if host is localhost, add 8000 as port. else do not add any port.
    # if request.get_host() == "127.0.0.1":
    #     port = 8000
    #     return f"{scheme}://{request.get_host()}:{port}"
    # else:
    #     return f"{scheme}://{request.get_host()}"


def generate_full_url(request, user_instance) -> str:
    """Returns the full instance url of user instance"""

    host = get_current_host(request=request)
    instance_url = user_instance.get_absolute_url()
    return host + instance_url
