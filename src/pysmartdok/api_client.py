import json
import logging
import threading

import requests
from requests import session

from .exceptions import SmartDokApiError
from .projects import Projects
from .qd import Qd
from .rue import Rue
from .users import Users

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, api_token: str, user_agent: str = "pysmartdok"):
        if api_token is None or api_token == "":
            raise ValueError("api_token must be a valid string")
        self.api_token = api_token
        self.user_agent = user_agent
        self.api_url = "https://api.smartdok.no/"
        self.headers: dict = {}
        self._auth_lock = threading.Lock()
        self.authenticate()
        self.users = Users(self.api_url, self.headers, reauth=self.authenticate)
        self.rue = Rue(self.api_url, self.headers, reauth=self.authenticate)
        self.qd = Qd(self.api_url, self.headers, reauth=self.authenticate)
        self.projects = Projects(self.api_url, self.headers, reauth=self.authenticate)

    def authenticate(self):
        """POST /Authorize/ApiToken and refresh the bearer token in place.

        Session tokens expire after about an hour; subclients call this on
        401 to refresh. Idempotent under concurrent callers: if another
        thread already rotated the token while this caller was waiting on
        the lock, returns immediately without a second auth round-trip.
        """
        expected_auth = self.headers.get("Authorization")
        with self._auth_lock:
            if (
                expected_auth is not None
                and self.headers.get("Authorization") != expected_auth
            ):
                return
            url = self.api_url + "Authorize/ApiToken"
            post_body = json.dumps({"Token": self.api_token})
            response = requests.post(
                url,
                data=post_body,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": self.user_agent,
                },
            )
            if response.status_code >= 300:
                raise SmartDokApiError(
                    "Failed to authenticate with SmartDok API."
                    + " Response code: "
                    + str(response.status_code)
                    + " Response body: "
                    + response.text
                )

            # The session token contains quotes for some reason, we need to remove them for it to be valid
            # session_token = response.text.replace('"', "")
            session_token = response.text
            self.headers["Authorization"] = "Bearer " + session_token
            self.headers["User-Agent"] = self.user_agent
