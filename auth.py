import base64
import hashlib
import hmac
from furl import furl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
# from urllib.parse import urlparse

def create_date_header():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)


def get_headers_string(signature_headers):
    headers = ""
    for key in signature_headers:
        if headers != "":
            headers += " "
        headers += key
    return headers


def get_signature_string(signature_headers):
    sig_string = ""
    for key, value in signature_headers.items():
        if sig_string != "":
            sig_string += "\n"
        if key.lower() == "request-line":
            sig_string += value
        else:
            sig_string += key.lower() + ": " + value
    return sig_string


def sha1_hash_base64(string_to_hash, secret):
    h = hmac.new(secret.encode('utf-8'), string_to_hash.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(h.digest()).decode("utf-8")


def generate_request_headers(key_id, secret, url, params):
    # Set the authorization header template
    auth_header_template = (
        'hmac username="{}",algorithm="{}",headers="{}",signature="{}"'
    )
    # Set the signature hash algorithm
    algorithm = "hmac-sha256"
    # Set the date header
    date_header = create_date_header()
    # Set headers for the signature hash
    signature_headers = {"date": date_header}

    request_method = "GET"

    # Parse the url so we can remove the base and extract just the path.
    # parsedURL = urlparse(url)
    # path = parsedURL.path
    # if parsedURL.query:
    #     path = path + '?' + parsedURL.query

    parsed_url = furl(url)
    path = parsed_url.pathstr
    if params:
        parsed_url.add(params)
        path += '?' + parsed_url.querystr

    # Build the request-line header
    request_line = request_method + " " + path + " HTTP/1.1"
    # Add to headers for the signature hash
    signature_headers["request-line"] = request_line

    # Get the list of headers
    headers = get_headers_string(signature_headers)
    # Build the signature string
    signature_string = get_signature_string(signature_headers)
    # Hash the signature string using the specified algorithm
    signature_hash = sha1_hash_base64(signature_string, secret)
    # Format the authorization header
    auth_header = auth_header_template.format(
        key_id, algorithm, headers, signature_hash
    )

    request_headers = {"Authorization": auth_header, "Date": date_header}

    return request_headers