"""
OpenStreetMap OAuth support.

This adds support for OpenStreetMap OAuth service. An application must be
registered first on OpenStreetMap and the settings
SOCIAL_AUTH_OPENSTREETMAP_KEY and SOCIAL_AUTH_OPENSTREETMAP_SECRET
must be defined with the corresponding values.

More info: https://wiki.openstreetmap.org/wiki/OAuth
"""
from xml.dom import minidom

from .oauth import BaseOAuth1


class OpenStreetMapOAuth(BaseOAuth1):
    """OpenStreetMap OAuth authentication backend, modified to OpenHistoricalMap"""

    name = "openstreetmap"
    AUTHORIZATION_URL = "https://www.openhistoricalmap.org/oauth/authorize"
    REQUEST_TOKEN_URL = "https://www.openhistoricalmap.org/oauth/request_token"
    ACCESS_TOKEN_URL = "https://www.openhistoricalmap.org/oauth/access_token"
    EXTRA_DATA = [
        ("id", "id"),
        ("avatar", "avatar"),
        ("account_created", "account_created"),
    ]

    def get_user_details(self, response):
        """Return user details from OpenHistoricalMap account"""
        return {
            "username": response["username"],
            "email": "",
            "fullname": "",
            "first_name": "",
            "last_name": "",
        }

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        response = self.oauth_request(
            access_token, "https://www.openhistoricalmap.org/api/0.6/user/details"
        )
        try:
            dom = minidom.parseString(response.content)
        except ValueError:
            return None
        user = dom.getElementsByTagName("user")[0]
        try:
            avatar = dom.getElementsByTagName("img")[0].getAttribute("href")
        except IndexError:
            avatar = None
        return {
            "id": user.getAttribute("id"),
            "username": user.getAttribute("display_name"),
            "account_created": user.getAttribute("account_created"),
            "avatar": avatar,
        }
