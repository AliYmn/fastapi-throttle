    # FastAPI Throttle

[![PyPI](https://img.shields.io/pypi/v/fastapi-throttle?logo=pypi&label=PyPI)](https://pypi.org/project/fastapi-throttle/)
[![CI](https://github.com/AliYmn/fastapi-throttle/actions/workflows/ci.yml/badge.svg)](https://github.com/AliYmn/fastapi-throttle/actions?query=workflow%3ACI)
[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi-throttle.svg?label=Python)](https://pypi.org/project/fastapi-throttle/)
[![License: MIT](https://img.shields.io/github/license/AliYmn/fastapi-throttle)](https://github.com/AliYmn/fastapi-throttle/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/fastapi-throttle)](https://pepy.tech/project/fastapi-throttle)
[![Wheel](https://img.shields.io/pypi/wheel/fastapi-throttle)](https://pypi.org/project/fastapi-throttle/)
[![Type Hints](https://img.shields.io/badge/typed-PEP%20561-blue)](https://www.python.org/dev/peps/pep-0561/)

A lightweight, in-memory rate limiter for FastAPI applications that requires no external dependencies.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Limitations](#limitations)
- [When to Use](#when-to-use)
- [Testing](#testing)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

## Overview

FastAPI Throttle helps you control API request rates without Redis or other external services. It's designed for applications where simplicity and minimal dependencies are priorities.

## Requirements

- Python 3.8+
- FastAPI

## Installation

```bash
pip install fastapi-throttle
```

## Quick Start

```python
from fastapi import FastAPI, Depends
from fastapi_throttle import RateLimiter

app = FastAPI()

# Limit to 5 requests per minute
limiter = RateLimiter(times=5, seconds=60)

@app.get("/", dependencies=[Depends(limiter)])
async def root():
    return {"message": "Hello World"}
```

## Features

- **No External Dependencies**: Works without Redis or other services
- **Simple Configuration**: Just specify request count and time window
- **Route-Level Control**: Apply different limits to different endpoints
- **FastAPI Integration**: Works with FastAPI's dependency injection system
- **Custom Keying (optional)**: Provide a `key_func(Request) -> str` to limit by user, API key, path, etc.
- **Proxy-Aware (optional)**: `trust_proxy=True` to use `X-Forwarded-For` when behind proxies/CDNs
- **Rate-Limit Headers (optional)**: Add `X-RateLimit-*` and `Retry-After` for clients

## Usage Examples

### Different Limits for Different Routes

```python
from fastapi import FastAPI, Depends
from fastapi_throttle import RateLimiter

app = FastAPI()

# Public endpoint: 10 requests per minute
public_limit = RateLimiter(times=10, seconds=60)

# Sensitive endpoint: 2 requests per minute
strict_limit = RateLimiter(times=2, seconds=60)

@app.get("/public", dependencies=[Depends(public_limit)])
async def public_endpoint():
    return {"message": "Public endpoint"}

@app.get("/sensitive", dependencies=[Depends(strict_limit)])
async def sensitive_endpoint():
    return {"message": "Sensitive endpoint"}
```

### Using with APIRouter

```python
from fastapi import APIRouter, Depends, FastAPI
from fastapi_throttle import RateLimiter

app = FastAPI()
router = APIRouter(prefix="/api")

# Apply same rate limit to all routes in this router
api_limit = RateLimiter(times=5, seconds=30)

@router.get("/resource", dependencies=[Depends(api_limit)])
async def get_resource():
    return {"data": "Resource data"}

app.include_router(router)
```

### Custom Key Function (limit by user or path)

```python
from fastapi import FastAPI, Depends, Request
from fastapi_throttle import RateLimiter

app = FastAPI()

def user_key(req: Request) -> str:
    # Example: extract user-id from header or auth (for demo only)
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

## Configuration

The `RateLimiter` class parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `times`   | int  | Maximum number of requests allowed in the time window |
| `seconds` | int  | Time window in seconds |
| `detail`  | str  | Optional custom detail message for 429 responses |
| `key_func` | `Callable[[Request], str]` | Optional custom function to compute the rate-limit key |
| `trust_proxy` | bool | If True, tries `X-Forwarded-For` for client identification (default False) |
| `add_headers` | bool | If True, adds `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After` headers |

## How It Works

The rate limiter:
1. Identifies clients by IP address
2. Stores request timestamps in memory
3. Removes timestamps outside the current time window
4. Counts requests within the window
5. Returns HTTP 429 when limit is exceeded

## Notes

- When `add_headers=True`, successful responses (2xx) include `X-RateLimit-Limit` and `X-RateLimit-Remaining`. On 429 responses, only `Retry-After` is included.
- Use `trust_proxy=True` only when running behind a trusted proxy/load balancer that correctly sets `X-Forwarded-For`. The first IP is treated as the client.

## Limitations

- **Memory Storage**: Data is lost when the application restarts
- **Single-Server Only**: Intended for monoliths/single-worker setups (in-memory, no cross-process sync)
- **IP-Based Identification (default)**: With shared IPs/proxies, prefer `key_func` or `trust_proxy`
- **Memory Usage**: Can grow with number of unique clients

## When to Use

FastAPI Throttle is ideal for:
- Small to medium applications
- Single-server deployments
- Projects where simplicity is valued over advanced features
- Development and testing environments

For high-traffic production applications or distributed systems, prefer a distributed rate limiter (e.g., Redis-backed). This package intentionally avoids Redis and focuses on simplicity.

## Testing

```bash
pip install -r requirements.txt
pytest --cov=fastapi_throttle -q
```

## Contributing

- Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
- Make sure tests pass and add tests for new features.
- Follow the existing code style; this repo uses flake8 and pre-commit.

## Roadmap

- Middleware variant in addition to dependency-based limiter
- (Maybe) Pluggable storage interface if a second backend is introduced later

## License

MIT License. See `LICENSE` for details.
