from urllib.parse import urlsplit
from urllib.parse import unquote

path1 = r"BilibiliSuitBuy\buy_suit\http-message\HTTP1.1Message.txt"
path2 = r"BilibiliSuitBuy\buy_suit\http-message\HTTP2.0Message.txt"


def ParseHttpMessage(content: bytes) -> tuple[dict, dict, dict]:
    message_content: list = content.split(b"\r\n")

    request: list = message_content[0].split(b" ")
    url_query: bytes = urlsplit(request[1]).query
    p = [i.split(b"=") for i in url_query.split(b"&")]
    p2 = [[ii.decode() for ii in i] for i in p]
    params = {unquote(i[0]): unquote(i[1]) for i in p2}

    headers_content = message_content[1:len(message_content)-2]
    h = [i.split(b": ") for i in headers_content]
    h2 = [i if len(i) == 2 else [i[0], b""] for i in h]
    h3 = [[ii.decode() for ii in i] for i in h2]
    headers = {unquote(i[0]).lower(): i[1] for i in h3}

    cookies_content: str = headers.get("cookie")
    c1: list = cookies_content.split("; ")
    c2 = [i.split("=") for i in c1]
    cookies = {i[0]: i[1] for i in c2}

    return params, headers, cookies


with open(path2, "rb") as f:
    message_data = f.read()
f.close()

print(ParseHttpMessage(message_data))