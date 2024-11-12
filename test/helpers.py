from datetime import datetime, timedelta
from openapi_schema_validator import OAS30Validator
from enum import StrEnum, auto
from logging import warning
import jsonschema
import requests
import os
import pytz
import yaml


class _CaseMatchingStrEnum(StrEnum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Role(_CaseMatchingStrEnum):
    RATINGS_PROVIDER = auto()
    UNAUTHORIZED = auto()


class Header(_CaseMatchingStrEnum):
    Authorization = auto()
    Accept = auto()
    ContentType = "Content-Type"


class TrolieClient:
    def __init__(self, role: Role):
        self.auth_token = TrolieClient.__get_auth_token(role)
        self.__headers = {}
        self.__body = None

    def request(self, relative_path, method="GET") -> "TrolieClient":
        trolie_url = TrolieClient.__get_trolie_url(relative_path)
        if self.auth_token:
            self.__headers["Authorization"] = f"Bearer {self.auth_token}"
        self.__response = requests.request(
            method=method, url=trolie_url, headers=self.__headers
        )
        return self

    def set_body(self, body) -> "TrolieClient":
        self.__body = body
        return self

    def set_header(self, key: Header, value: str) -> "TrolieClient":
        self.__headers[key] = value
        return self

    def ensure_empty_request(self) -> "TrolieClient":
        if existing := self.__headers.pop(Header.ContentType, None):
            warning(f"Removing existing Content-Type header: {existing}")
        if self.__body:
            warning(f"Removing existing body: {self.__body}")
            self.__body = None
        return self

    def get_response_header(self, key: Header) -> str:
        if response := self.__response:
            return response.headers[key]
        return None

    def get_json(self):
        return self.__response.json()

    def get_status_code(self) -> int:
        return self.__response.status_code

    def validate_response(self) -> bool:
        if content_type := self.get_response_header(Header.ContentType):
            if media_type := MediaType(content_type):
                return TrolieMessages.is_valid(
                    message=self.get_json(), media_type=media_type
                )
            else:
                warning(f"Unknown media type: {content_type}")
        else:
            warning("Missing Content-Type header")
        return False

    @staticmethod
    def __get_auth_token(role: Role):
        if role == Role.UNAUTHORIZED:
            return None
        if token := os.getenv(f"{role}_TOKEN"):
            return token
        raise ValueError(f"Missing {role}_TOKEN environment variable")

    @staticmethod
    def __get_trolie_url(relative_path):
        return os.getenv("TROLIE_BASE_URL") + relative_path


class MediaType(StrEnum):
    FORECAST_LIMITS_SNAPSHOT = "application/vnd.trolie.forecast-limits-snapshot.v1+json"
    FORECAST_LIMITS_DETAILED_SNAPSHOT = (
        "application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json"
    )
    FORECAST_LIMITS_SNAPSHOT_OMIT_PSR = "application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false"
    FORECAST_LIMITS_DETAILED_SNAPSHOT_OMIT_PSR = "application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false"


class TrolieMessages:
    @staticmethod
    def is_valid(message, media_type: MediaType):
        with open("openapi.yaml") as f:
            openapi_spec = yaml.safe_load(f)
        switch = {
            MediaType.FORECAST_LIMITS_SNAPSHOT: "forecast-limits-snapshot-elide-psr",
            MediaType.FORECAST_LIMITS_DETAILED_SNAPSHOT: "forecast-limits-detailed-snapshot",
            MediaType.FORECAST_LIMITS_SNAPSHOT_OMIT_PSR: "forecast-limits-snapshot-elide-psr",
            MediaType.FORECAST_LIMITS_DETAILED_SNAPSHOT_OMIT_PSR: "forecast-limits-detailed-snapshot-elide-psr",
        }
        schema = openapi_spec["components"]["schemas"][switch.get(media_type)]
        print(schema)
        rooted_schemas = {
            "components": {"schemas": openapi_spec["components"]["schemas"]}
        }

        ref_resolver = jsonschema.RefResolver.from_schema(rooted_schemas)
        validator = OAS30Validator(schema, resolver=ref_resolver)
        try:
            validator.validate(instance=message)
        except jsonschema.ValidationError as e:
            warning(f"Message failed validation: {e}")
            return False
        return True


def get_period(hours=0):
    tz_name = os.getenv("TZ", "UTC")
    timezone = pytz.timezone(tz_name)
    return (
        (datetime.now(timezone) + timedelta(hours=hours))
        .replace(minute=0, second=0, microsecond=0)
        .isoformat()
    )
