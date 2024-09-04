import time
from fastapi import Request, HTTPException
from typing import Dict, List


class RateLimiter:
    """
    A simple in-memory rate limiter for FastAPI applications.

    This rate limiter limits the number of requests a client can make within a specified time window.
    The rate limiting is based on the client's IP address and does not require any external storage.

    Attributes:
        times (int): The maximum number of requests allowed per client within the specified period.
        seconds (int): The time window in seconds during which requests are counted.
        requests (Dict[str, List[float]]): A dictionary storing request timestamps for each client IP.
    """

    def __init__(self, times: int, seconds: int) -> None:
        """
        Initializes the RateLimiter instance with the specified request limit and time period.

        Args:
            times (int): The maximum number of requests allowed per client.
            seconds (int): The time period in seconds for rate limiting.
        """
        self.times: int = times
        self.seconds: int = seconds
        self.requests: Dict[str, List[float]] = {}

    async def __call__(self, request: Request) -> None:
        """
        Checks if the incoming request exceeds the allowed rate limit.

        This method is called on each request to the FastAPI route that uses this rate limiter as a dependency.
        If the client has made more requests than allowed within the specified time period, an HTTP 429 exception
        is raised.

        Args:
            request (Request): The incoming HTTP request object.

        Raises:
            HTTPException: If the request rate limit is exceeded, a 429 status code is returned.
        """
        client_ip: str = request.client.host
        current_time: float = time.time()

        # Initialize the client's request history if not already present
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Filter out timestamps that are outside of the rate limit period
        self.requests[client_ip] = [
            timestamp
            for timestamp in self.requests[client_ip]
            if timestamp > current_time - self.seconds
        ]

        # Check if the number of requests exceeds the allowed limit
        if len(self.requests[client_ip]) >= self.times:
            raise HTTPException(status_code=429, detail="Too Many Requests")

        # Record the current request timestamp
        self.requests[client_ip].append(current_time)
