import json
import logging

import requests

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
        self.headers = {}
        self.authenticate()
        self.users = Users(self.api_url, self.headers)
        self.rue = Rue(self.api_url, self.headers)
        self.qd = Qd(self.api_url, self.headers)
        self.projects = Projects(self.api_url, self.headers)

    def authenticate(self):
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

        # The session token contains quotes, so we need to remove them
        session_token = response.text.replace('"', "")

        self.headers = {
            "Authorization": "Bearer " + session_token,
            "User-Agent": self.user_agent,
        }
