from config import SUPPORTED_METHODS

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
        self.Method = ''
        self.Path = ''
        self.ContentType = ''
        self.Host = ''
        self.Connection = ''
        self.AcceptEncoding = ''
        self.UserAgent = ''
        self.Body = ''
        self.Authorization = ''
        self.Headers = {}

        if headers:
            first_line = headers[0].split(' ')
            if len(first_line) >= 2:
                self.Method = first_line[0]
                self.Path = first_line[1]
            try:
                body_index = headers.index('')
                header_lines = headers[1:body_index]
                self.Body = '\n'.join(headers[body_index + 1:])
            except ValueError:
                header_lines = headers[1:]

            for line in header_lines:
                if ':' in line:
                    header, value = line.split(':', 1)
                    self.Headers[header.strip().lower()] = value.strip()

            # Use dict.get for optional headers
            self.ContentType = self.Headers.get("content-type", '')
            self.Host = self.Headers.get('host', '')
            self.Connection = self.Headers.get('connection', '')
            self.AcceptEncoding = self.Headers.get('accept-encoding', '')
            self.UserAgent = self.Headers.get('user-agent', '')
            self.Authorization = self.Headers.get('authorization', '')

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
    Protocol :str = 'HTTP/1.1'
    ResponseCode : str
    ResponseMessage: str
    
    def __init__(self, content: str, status_code: int = 200, reason: str = "OK", content_type: str = "text/html"):
        self.StatusCode = status_code
        self.Reason = reason
        self.ContentType = content_type
        self.Content = content

    def to_bytes(self) -> bytes:
        response = (
            f"{self.Protocol} {self.StatusCode} {self.Reason}\r\n"
            f"Content-Type: {self.ContentType}\r\n"
            f"\r\n"
            f"{self.Content}"
        )
        return response.encode("utf-8")

def parse_http_request(headers: list[str]) -> HttpRequest:
    return HttpRequest(headers)

def _is_supported(method: str) -> bool :
    return method in SUPPORTED_METHODS

def process_request(request:HttpRequest) -> HttpResponse:
    response : HttpResponse = HttpResponse("")
    match request.Method:
        case 'GET':
            response.ContentType = 'text/html'
            response.ResponseCode = 200
            response.Reason = 'OK'
            with open('static/index.html') as fin:
                response.Content = fin.read()
        case _:
            response.StatusCode = 405
            response.Reason = 'Not Allowed'
            response.ContentType = 'test/html'
            response.Content = SUPPORTED_METHODS
    return response
