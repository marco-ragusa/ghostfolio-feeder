"""Small shared HTTP client with safe defaults."""

from collections.abc import Iterable

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DEFAULT_TIMEOUT = (5, 30)

_session = Session()
_adapter = HTTPAdapter(
    max_retries=Retry(
        total=2,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
    )
)
_session.mount("http://", _adapter)
_session.mount("https://", _adapter)


def request(
    method: str,
    url: str,
    *,
    allowed_statuses: Iterable[int] = (),
    **kwargs,
) -> Response:
    """Send an HTTP request with pooling, retries, timeouts, and TLS checks."""
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    response = _session.request(method, url, **kwargs)

    if response.status_code not in allowed_statuses:
        response.raise_for_status()

    return response
