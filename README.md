# Fastapi Throttle

[![pypi](https://img.shields.io/pypi/v/fastapi-throttle.svg?style=flat)](https://pypi.python.org/pypi/fastapi-throttle)
[![ci](https://github.com/AliYmn/fastapi-throttle/workflows/CI/badge.svg)](https://github.com/AliYmn/fastapi-throttle/actions?query=workflow:CI)

`fastapi-throttle` is a simple in-memory rate limiter for FastAPI applications. This package allows you to control the number of requests a client can make to your API within a specified time window without relying on external dependencies like Redis. It is ideal for lightweight applications where simplicity and speed are paramount.

## Features
- **Without Redis** : You don’t need to install or configure Redis.
- **In-Memory Rate Limiting**: No external dependencies required. Keeps everything in memory for fast and simple rate limiting.
- **Flexible Configuration**: Easily configure rate limits per route or globally.
- **Python Version Support**: Compatible with Python 3.8 up to 3.12.

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
