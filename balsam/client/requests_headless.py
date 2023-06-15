import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import click
import dateutil.parser

from . import urls
from .requests_password import BasicAuthRequestsClient
from .rest_base_client import AuthError
from .requests_client import RequestsClient

logger = logging.getLogger(__name__)


class HeadlessRequestsClient(BasicAuthRequestsClient):

    def refresh_auth(self) -> None:
        # Update from environment
        self.username = os.environ.get('BALSAM_USERNAME') or self.username
        self.password = os.environ.get('BALSAM_PASSWORD') or self.password
        if self.username is None or self.password is None:
            raise ValueError("Cannot refresh_auth without username and password. Please provide these values.")
        self._refresh_auth()

    def interactive_login(self) -> Dict[str, Any]:
        """Initiate interactive login flow
        
        For headless, this must come from the environment
        """
        self.refresh_auth()
        click.echo("Logged In")
        return {"token": self.token, "token_expiry": self.token_expiry}

RequestsClient._client_classes["headless"] = HeadlessRequestsClient
