import requests
from helpers import Role

# OAuth 2.0 configuration
TOKEN_URL = "<<change me>>"
PROJECT_ID = "<<change me>>"
SCOPE = "<<change me>>"


class ZitadelAuthTokenProvider:
    def get_auth_token(self, role: Role) -> str:
        if role == Role.UNAUTHENTICATED:
            return None

        client_id, client_secret = self._get_credentials_for_role(role)

        payload = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret, "scope": SCOPE}

        try:
            response = requests.post(TOKEN_URL, data=payload)
            response.raise_for_status()
            return response.json().get("access_token")

        except requests.exceptions.RequestException as e:
            print(f"Error obtaining bearer token: {e}")
            return None

    def _get_credentials_for_role(self, role: Role):
        if role == Role.RATINGS_PROVIDER:
            return (
                "<<change me>>",  # the client id known to the token provider
                "<<change me>>",  # the client secret known to the token provider
            )
        else:
            raise ValueError(f"Unsupported role: {role}")
