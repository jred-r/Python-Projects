# 🖥️ Minimal HTTP Server in Python

A lightweight, socket-based HTTP server built from scratch using Python’s `socket` module. It supports basic HTTP methods and serves static content from the `static/` directory. Designed for educational purposes & prototyping.

---

## 🚀 Features

- Handles multiple HTTP methods: `GET`, `HEAD`, `POST`, `PUT`, `DELETE`, `OPTIONS`
- Parses raw HTTP requests manually (no external frameworks)
- Returns appropriate status codes and headers
- Serves static HTML content from `static/index.html`
- Gracefully handles timeouts and client disconnects
- Easily extensible for custom routing or middleware

---

## 🧱 Project Structure

```plaintext
.
├── config.py              # Server configuration constants
├── server.py              # Main server class and entry point
├── utils.py               # HTTP request parsing and response generation
├── static/
│   └── index.html         # Default HTML page served for GET requests
└── README.md              # You're reading it!
```

---

## ⚙️ Configuration

Defined in `config.py`:

```python
HOST_ADDRESS = "127.0.0.1"
HOST_PORT = 8080
QUEUE_SIZE = 10
BUFFER_SIZE = 1024
TIME_OUT = 1
PROTOCOL = "HTTP/1.1"
SUPPORTED_METHODS: list[str] = {
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
}
```

---

## 🧩 Core Components

### `Server` Class (`server.py`)
- Initializes and binds a TCP socket
- Accepts incoming connections
- Parses HTTP requests using `parse_http_request`
- Processes requests via `process_request`
- Sends back formatted HTTP responses

### `HttpRequest` Class (`utils.py`)
- Parses raw HTTP headers into structured fields
- Extracts method, path, headers, and body

### `HttpResponse` Class (`utils.py`)
- Constructs HTTP-compliant responses
- Supports status codes, content types, and custom headers

---

## 📦 Supported HTTP Methods

| Method   | Behavior                                                                 |
|----------|--------------------------------------------------------------------------|
| `GET`    | Returns `index.html` if available, else 404                              |
| `HEAD`   | Returns headers only (no body)                                           |
| `POST`   | Echoes received body content                                             |
| `PUT`    | Echoes received body content                                             |
| `DELETE` | Returns confirmation message                                             |
| `OPTIONS`| Returns allowed methods in `Allow` header                                |
| Others   | Returns `405 Method Not Allowed` with supported methods listed           |

---

## ▶️ Running the Server

```bash
python server.py
```

To stop the server:

- Press `Ctrl+C` in the terminal

---

## 🛠️ Extending the Server

You can add custom routing logic inside `process_request()` or enhance the `HttpRequest` class to support query parameters, cookies, etc. For production-grade use, consider integrating with frameworks like Flask or FastAPI.

---

## 📜 License

This project is open-source and available under the MIT License.