from typing import Self


class HTTPRequest:
    def __init__(
        self,
        method: str,
        url: str,
        verion: str = "HTTP/1.1",
        headers: dict = None,
        body: str = None,
    ):
        self.method = method
        self.url = url
        self.verion = verion
        self.headers = headers or {}
        self.body = body

    def to_bytes(self) -> bytes:
        request_link = f"{self.method} {self.url} {self.verion}\r\n"
        headeres = "\r\n".join(f"{key}:{value}" for key, value in self.headers.items())
        return f"{request_link}{headeres}\r\n\r\n".encode() + self.body

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        parts = binary_data.split(b"\r\n\r\n", 1)
        header_part = parts[0].decode()
        body = b""
        if len(parts) > 1:
            body = parts[1]
        else:
            body = b""
        lines = header_part.split("\r\n")
        method, url, version = lines[0].split()
        headers = {}
        for line in lines[1:]:
            if line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return cls(method=method, url=url, version=version, headers=headers, body=body)


class HTTPResponse:
    def __init__(
        self,
        status_cod: str,
        reason: str,
        version: str = "HTTP/1.1",
        headers: dict = None,
        body: str = None,
    ):
        self.version = version
        self.status_code = status_cod
        self.reason = reason
        self.headers = headers or {}
        self.body = body

    def to_bytes(self) -> bytes:
        start_line = f"{self.status_code}{self.reason}{self.version}"
        headeres = "\r\n".join(f"{key}:{value}" for key, value in self.headers.items())
        return f"{start_line}{headeres}\r\n\r\n".encode() + self.body

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        parts = binary_data.split(b"\r\n\r\n", 1)
        header_part = parts[0].decode()
        body = b""
        if len(parts) > 1:
            body = parts[1]
        else:
            body = b""
        lines = header_part.split("\r\n")
        status_cod, respons, version = lines[0].split()
        headers = {}
        for line in lines[1:]:
            if line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return cls(
            status_cod=int(status_cod),
            respons=respons,
            version=version,
            headers=headers,
            body=body,
        )
