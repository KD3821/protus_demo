import requests
from requests.adapters import HTTPAdapter, Retry


def start_requests_session():
    rs = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    rs.mount('http://', HTTPAdapter(max_retries=retries))
    return rs
