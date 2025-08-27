from config import SUPPORTED_METHODS, PROTOCOL

CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_PLAIN = "text/plain"

STATUS_CODES = {
    200: "OK",
    204: "No Content",
    404: "Not Found",
    405: "Not Allowed",
}


class HttpRequest:
    Method: str
    Path: str
    ContentType: str
    Host: str
    Connection: str
    AcceptEncoding: str
    UserAgent: str
    Body: str
    Authorization: str
    Headers: dict

    def __init__(self, headers: list[str]):
        self.Method = ""
        self.Path = ""
        self.ContentType = ""
        self.Host = ""
        self.Connection = ""
        self.AcceptEncoding = ""
        self.UserAgent = ""
        self.Body = ""
        self.Authorization = ""
        self.Headers = {}

        if headers:
            first_line = headers[0].split(" ")
            if len(first_line) >= 2:
                self.Method = first_line[0]
                self.Path = first_line[1]
            try:
                body_index = headers.index("")
                header_lines = headers[1:body_index]
                self.Body = "\n".join(headers[body_index + 1 :])
            except ValueError:
                header_lines = headers[1:]

            for line in header_lines:
                if ":" in line:
                    header, value = line.split(":", 1)
                    self.Headers[header.strip().lower()] = value.strip()

            # Use dict.get for optional headers
            self.ContentType = self.Headers.get("content-type", "")
            self.Host = self.Headers.get("host", "")
            self.Connection = self.Headers.get("connection", "")
            self.AcceptEncoding = self.Headers.get("accept-encoding", "")
            self.UserAgent = self.Headers.get("user-agent", "")
            self.Authorization = self.Headers.get("authorization", "")

    def __str__(self):
        return (
            f"Headers:\n{self.Headers}\n"
            f"Method: {self.Method}\n"
            f"Path: {self.Path}\n"
            f"ContentType: {self.ContentType}\n"
            f"Host: {self.Host}\n"
            f"Connection: {self.Connection}\n"
            f"AcceptEncoding: {self.AcceptEncoding}\n"
            f"UserAgent: {self.UserAgent}\n"
            f"Authorization: {self.Authorization}\n"
            f"Body:\n{self.Body}\n"
        )


class HttpResponse:
    def __init__(
        self,
        content: str,
        status_code: int = 200,
        content_type: str = CONTENT_TYPE_HTML,
        extra_headers: dict = None,
    ):
        self.StatusCode = status_code
        self.Reason = STATUS_CODES.get(status_code, "")
        self.ContentType = content_type
        self.Content = content
        self.ExtraHeaders = extra_headers or {}

    def to_bytes(self) -> bytes:
        headers = [
            f"{PROTOCOL} {self.StatusCode} {self.Reason}",
            f"Content-Type: {self.ContentType}",
        ]
        for k, v in self.ExtraHeaders.items():
            headers.append(f"{k}: {v}")
        response = (
            "\r\n".join(headers)
            + "\r\n\r\n"
            + (self.Content if self.StatusCode != 204 else "")
        )
        return response.encode("utf-8")


def get_index_content():
    try:
        with open("static/index.html", "rb") as fin:
            return fin.read()
    except FileNotFoundError:
        return None


def parse_http_request(headers: list[str]) -> HttpRequest:
    return HttpRequest(headers)


def process_request(request: HttpRequest) -> HttpResponse:
    method = request.Method.upper()
    allowed = ", ".join(SUPPORTED_METHODS)

    if method == "GET":
        content = get_index_content()
        if content is not None:
            return HttpResponse(
                content.decode("utf-8"),
                200,
                CONTENT_TYPE_HTML,
                extra_headers={"Content-Length": str(len(content))},
            )
        else:
            not_found = "<h1>404 Not Found</h1>"
            return HttpResponse(
                not_found,
                404,
                CONTENT_TYPE_HTML,
                extra_headers={"Content-Length": str(len(not_found.encode("utf-8")))},
            )
    elif method == "HEAD":
        content = get_index_content()
        if content is not None:
            return HttpResponse(
                "",
                200,
                CONTENT_TYPE_HTML,
                extra_headers={"Content-Length": str(len(content))},
            )
        else:
            not_found = "<h1>404 Not Found</h1>"
            return HttpResponse(
                "",
                404,
                CONTENT_TYPE_HTML,
                extra_headers={"Content-Length": str(len(not_found.encode("utf-8")))},
            )
    elif method == "POST":
        body = f"Received POST data: {request.Body}"
        return HttpResponse(
            body,
            200,
            CONTENT_TYPE_PLAIN,
            extra_headers={"Content-Length": str(len(body.encode("utf-8")))},
        )
    elif method == "PUT":
        body = f"PUT request received. Data: {request.Body}"
        return HttpResponse(
            body,
            200,
            CONTENT_TYPE_PLAIN,
            extra_headers={"Content-Length": str(len(body.encode("utf-8")))},
        )
    elif method == "DELETE":
        body = "DELETE request processed."
        return HttpResponse(
            body,
            200,
            CONTENT_TYPE_PLAIN,
            extra_headers={"Content-Length": str(len(body.encode("utf-8")))},
        )
    elif method == "OPTIONS":
        return HttpResponse(
            "",
            204,
            CONTENT_TYPE_PLAIN,
            extra_headers={"Allow": allowed, "Content-Length": "0"},
        )
    else:
        body = f"Allowed methods: {allowed}"
        return HttpResponse(
            body,
            405,
            CONTENT_TYPE_PLAIN,
            extra_headers={
                "Allow": allowed,
                "Content-Length": str(len(body.encode("utf-8"))),
            },
        )
