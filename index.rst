# Fastapi Throttle

[![pypi](https://img.shields.io/pypi/v/fastapi-throttle.svg?style=flat)](https://pypi.python.org/pypi/fastapi-throttle)
[![ci](https://github.com/AliYmn/fastapi-throttle/workflows/CI/badge.svg)](https://github.com/AliYmn/fastapi-throttle/actions?query=workflow:CI)

`fastapi-throttle` is a simple in-memory rate limiter for FastAPI applications. This package allows you to control the number of requests a client can make to your API within a specified time window without relying on external dependencies like Redis. It is ideal for lightweight applications where simplicity and speed are paramount.

## Features
- **Without Redis** : You don’t need to install or configure Redis (monolith/single-worker focus).
- **In-Memory Rate Limiting**: No external dependencies required. Keeps everything in memory for fast and simple rate limiting.
- **Flexible Configuration**: Easily configure rate limits per route or globally.
- **Python Version Support**: Compatible with Python 3.8 up to 3.12.
- **Custom Keying (optional)**: Provide a key function to limit by user, API key, path, etc.
- **Proxy-Aware (optional)**: `trust_proxy=True` to read `X-Forwarded-For` behind proxies/CDNs.
- **Rate-Limit Headers (optional)**: Add `X-RateLimit-*` and `Retry-After` headers for clients.

## Installation

To install the package, use pip:

```bash
pip install fastapi-throttle
```

## Usage
Here’s how you can use fastapi-throttle in your FastAPI application:

### Basic Example
```python
from fastapi import FastAPI, Depends
from fastapi_throttle import RateLimiter

app = FastAPI()

# Apply rate limiting globally
@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def root():
    return {"message": "Hello, World!"}
```

## Route-Specific Rate Limiting
You can apply different rate limits to different routes as needed:

```python
from fastapi import FastAPI, Depends
from fastapi_throttle import RateLimiter

app = FastAPI()

# Apply different rate limits to different routes
@app.get("/route1", dependencies=[Depends(RateLimiter(times=3, seconds=10))])
async def route1():
    return {"message": "This is route 1"}

@app.get("/route2", dependencies=[Depends(RateLimiter(times=5, seconds=15))])
async def route2():
    return {"message": "This is route 2"}
```

## Configuration
- times: The maximum number of requests allowed per client within the specified period.
- seconds: The time window in seconds within which the requests are counted.
- detail: Optional custom detail message for 429 responses.
- key_func: Optional callable `key_func(Request) -> str` to compute a custom key (e.g., user id).
- trust_proxy: If True, use the first IP from `X-Forwarded-For` when present (default False).
- add_headers: If True, add `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After`.

## Example with Custom Configuration
Here is an example where you use custom rate limiting per endpoint:

```python
from fastapi import FastAPI, Depends
from fastapi_throttle import RateLimiter

app = FastAPI()

@app.get("/custom", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def custom():
    return {"message": "This is a custom route with its own rate limit."}
```

## Advanced Examples

### Custom key function (limit by user or path)
```python
from fastapi import FastAPI, Depends, Request
from fastapi_throttle import RateLimiter

app = FastAPI()

def user_key(req: Request) -> str:
    return req.headers.get("x-user-id", req.client.host or "unknown")

limiter = RateLimiter(times=10, seconds=60, key_func=user_key)

@app.get("/data", dependencies=[Depends(limiter)])
async def data():
    return {"ok": True}
```

### Behind proxy/CDN (trust X-Forwarded-For)
```python
from fastapi import FastAPI, Depends
from fastapi_throttle import RateLimiter

app = FastAPI()

proxy_limit = RateLimiter(times=5, seconds=30, trust_proxy=True)

@app.get("/proxy", dependencies=[Depends(proxy_limit)])
async def proxy_route():
    return {"ok": True}
```

### Standard rate-limit headers
```python
from fastapi import FastAPI, Depends
from fastapi_throttle import RateLimiter

app = FastAPI()

headers_limit = RateLimiter(times=5, seconds=60, add_headers=True)

@app.get("/limited", dependencies=[Depends(headers_limit)])
async def limited():
    return {"message": "Check X-RateLimit-* headers"}
```
