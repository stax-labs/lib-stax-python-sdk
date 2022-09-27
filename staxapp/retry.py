import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

N_RETRIES = 5
BACKOFF_FACTOR = 1.0
RETRY_STATUSES = (429, 500, 502, 504)
DEFAULT_ALLOWED_METHODS = ("GET", "PUT", "DELETE", "OPTIONS")


def requests_retry_session(
    retries=N_RETRIES,
    backoff_factor=BACKOFF_FACTOR,
    status_list=RETRY_STATUSES,
    allowed_methods=DEFAULT_ALLOWED_METHODS,
    session=None,
):
    """
    Initialises a retry requests session with configured exponential backoff
    https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_list,
        allowed_methods=allowed_methods,
        # Do not raise Retry Exception for backwards compatibility, return last response so ApiException raised
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session
