# FastAPI Throttle

[![PyPI](https://img.shields.io/pypi/v/fastapi-throttle.svg?style=flat)](https://pypi.python.org/pypi/fastapi-throttle)
[![CI](https://github.com/AliYmn/fastapi-throttle/workflows/CI/badge.svg)](https://github.com/AliYmn/fastapi-throttle/actions?query=workflow:CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi-throttle.svg)](https://pypi.org/project/fastapi-throttle/)
[![License](https://img.shields.io/github/license/AliYmn/fastapi-throttle)](https://github.com/AliYmn/fastapi-throttle/blob/master/LICENSE)

A lightweight, in-memory rate limiter for FastAPI applications that requires no external dependencies.

## Overview

FastAPI Throttle helps you control API request rates without Redis or other external services. It's designed for applications where simplicity and minimal dependencies are priorities.

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

## Configuration

The `RateLimiter` class takes two parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `times`   | int  | Maximum number of requests allowed in the time window |
| `seconds` | int  | Time window in seconds |

## How It Works

The rate limiter:
1. Identifies clients by IP address
2. Stores request timestamps in memory
3. Removes timestamps outside the current time window
4. Counts requests within the window
5. Returns HTTP 429 when limit is exceeded

## Limitations

- **Memory Storage**: Data is lost when the application restarts
- **Single-Server Only**: Not designed for distributed environments
- **IP-Based Identification**: May not work well with shared IPs or proxies
- **Memory Usage**: Can grow with number of unique clients
- **No Rate Limit Headers**: Doesn't include standard rate limit headers in responses

## When to Use

FastAPI Throttle is ideal for:
- Small to medium applications
- Single-server deployments
- Projects where simplicity is valued over advanced features
- Development and testing environments

For high-traffic production applications or distributed systems, consider a Redis-based solution.

## Testing

```bash
pip install pytest pytest-cov httpx
python -m pytest
```

## License

MIT License. See `LICENSE` for details.
