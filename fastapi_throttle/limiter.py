import time
from fastapi import Request, HTTPException, Response
from typing import Callable, Dict, List, Optional


class RateLimiter:
    """
    A simple in-memory rate limiter for FastAPI applications.

    This rate limiter limits the number of requests a client can make within a specified time window.
    The rate limiting is based on the client's IP address and does not require any external storage.

    Attributes:
        times (int): The maximum number of requests allowed per client within the specified period.
        seconds (int): The time window in seconds during which requests are counted.
        requests (Dict[str, List[float]]): A dictionary storing request timestamps for each computed key.
        detail (str): The detail message to be returned to the client if the requests exceed the limit within the specified period.
        key_func (Optional[Callable[[Request], str]]): Optional function to compute a custom rate-limit key.
        trust_proxy (bool): When True, uses X-Forwarded-For to determine client IP (first hop).
        add_headers (bool): When True, adds rate-limit headers to the response.
    """

    def __init__(self, times: int, seconds: int, detail: Optional[str] = None, *, key_func: Optional[Callable[[Request], str]] = None, trust_proxy: bool = False, add_headers: bool = False) -> None:
        """
        Initializes the RateLimiter instance with the specified request limit and time period.

        Args:
            times (int): The maximum number of requests allowed per client.
            seconds (int): The time period in seconds for rate limiting.
            detail (str): The detail message to be returned to the client if rate limit is exceeded.
            key_func (Callable[[Request], str], optional): Custom key function. Defaults to None (client IP based).
            trust_proxy (bool): If True, attempts to use X-Forwarded-For header for client identification.
            add_headers (bool): If True, attaches standard rate limit headers to the response.
        """
        self.times: int = times
        self.seconds: int = seconds
        self.requests: Dict[str, List[float]] = {}
        # Ensure non-None detail without violating typing
        self.detail: str = detail or "Too Many Requests"
        self.key_func: Optional[Callable[[Request], str]] = key_func
        self.trust_proxy: bool = trust_proxy
        self.add_headers: bool = add_headers

    async def __call__(self, request: Request, response: Response) -> None:
        """
        Checks if the incoming request exceeds the allowed rate limit.

        This method is called on each request to the FastAPI route that uses this rate limiter as a dependency.
        If the client has made more requests than allowed within the specified time period, an HTTP 429 exception
        is raised.

        Args:
            request (Request): The incoming HTTP request object.
            response (Response): The outgoing HTTP response object.

        Raises:
            HTTPException: If the request rate limit is exceeded, a 429 status code is returned.
        """
        client = request.client
        # Compute key: custom key_func takes precedence
        if self.key_func is not None:
            try:
                key: str = self.key_func(request)
            except Exception:
                # Fail-safe: do not break request handling if custom key function errors out
                key = "unknown"
        else:
            # Default behavior: determine client IP, optionally trusting proxy headers
            key = "unknown"
            if self.trust_proxy:
                xff = request.headers.get("x-forwarded-for")
                if xff:
                    # First IP in X-Forwarded-For is the original client
                    key = xff.split(",")[0].strip() or key
            if key == "unknown":
                key = client.host if (client and getattr(client, "host", None)) else "unknown"
        current_time: float = time.monotonic()
        window_start: float = current_time - self.seconds

        # Get and prune timestamps inside the window
        existing = self.requests.get(key, [])
        filtered: List[float] = [ts for ts in existing if ts > window_start]
        if not filtered:
            # Small hygiene: if list becomes empty, drop the key to avoid empty buckets
            if key in self.requests:
                del self.requests[key]
            current_count = 0
        else:
            self.requests[key] = filtered
            current_count = len(filtered)

        if current_count >= self.times:
            # Compute Retry-After: time until the oldest timestamp leaves the window
            oldest = min(filtered) if filtered else current_time
            retry_after = int(max(0.0, self.seconds - (current_time - oldest)))
            headers = {"Retry-After": str(retry_after)} if retry_after > 0 else None
            raise HTTPException(status_code=429, detail=self.detail, headers=headers)

        # Record the current request timestamp
        if filtered:
            # Append to existing filtered list
            self.requests[key].append(current_time)
        else:
            # Create a fresh list for this key
            self.requests[key] = [current_time]

        # Optionally attach standard rate limit headers
        if self.add_headers:
            response.headers["X-RateLimit-Limit"] = str(self.times)
            response.headers["X-RateLimit-Remaining"] = str(max(0, self.times - len(self.requests[key])))
