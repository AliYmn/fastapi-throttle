# FastAPI Throttle

[![pypi](https://img.shields.io/pypi/v/fastapi-throttle.svg?style=flat)](https://pypi.python.org/pypi/fastapi-throttle)
[![ci](https://github.com/AliYmn/fastapi-throttle/workflows/CI/badge.svg)](https://github.com/AliYmn/fastapi-throttle/actions?query=workflow:CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi-throttle.svg)](https://pypi.org/project/fastapi-throttle/)
[![License](https://img.shields.io/github/license/AliYmn/fastapi-throttle)](https://github.com/AliYmn/fastapi-throttle/blob/master/LICENSE)

`fastapi-throttle` is a lightweight, in-memory rate limiter for FastAPI applications. This package allows you to control the number of requests a client can make to your API within a specified time window without relying on external dependencies like Redis. It is ideal for lightweight applications where simplicity and speed are paramount.

## 🚀 Features

- **Zero External Dependencies**: No Redis or other external services required
- **Simple In-Memory Storage**: Fast and efficient rate limiting using Python's built-in data structures
- **Flexible Configuration**: Apply rate limits globally or on a per-route basis
- **IP-Based Limiting**: Automatically identifies clients by their IP address
- **Comprehensive Python Support**: Compatible with Python 3.8 up to 3.13
- **Minimal Overhead**: Designed for high performance with minimal impact on response times

## 📦 Installation

Install the package using pip:

```bash
pip install fastapi-throttle
```

## 🔧 Usage

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

### Route-Specific Rate Limiting

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

### Advanced Usage with Router

You can also apply rate limiting to a group of routes using FastAPI's `APIRouter`:

```python
from fastapi import APIRouter, Depends, FastAPI
from fastapi_throttle import RateLimiter

app = FastAPI()
router = APIRouter(prefix="/api")

# Apply rate limiting to all routes in this router
router_limiter = RateLimiter(times=5, seconds=30)

@router.get("/resource1", dependencies=[Depends(router_limiter)])
async def resource1():
    return {"data": "Resource 1 data"}

@router.get("/resource2", dependencies=[Depends(router_limiter)])
async def resource2():
    return {"data": "Resource 2 data"}

app.include_router(router)
```

## ⚙️ Configuration Parameters

The `RateLimiter` class accepts the following parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `times`   | int  | The maximum number of requests allowed per client within the specified period |
| `seconds` | int  | The time window in seconds within which the requests are counted |

## 🛡️ Error Handling

When a client exceeds the rate limit, the limiter will raise an `HTTPException` with status code `429 Too Many Requests`. You can customize the error handling in your FastAPI application as needed.

## 🔍 How It Works

The rate limiter works by:

1. Identifying the client by their IP address
2. Tracking request timestamps in memory
3. Cleaning up old timestamps outside the specified time window
4. Checking if the number of recent requests exceeds the limit
5. Raising an HTTP 429 exception if the limit is exceeded

## 📋 Example Project

Here's a complete example of a FastAPI application with rate limiting:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi_throttle import RateLimiter
import uvicorn

app = FastAPI(title="Rate Limited API")

# Create rate limiters with different configurations
global_limiter = RateLimiter(times=10, seconds=60)  # 10 requests per minute
strict_limiter = RateLimiter(times=2, seconds=10)   # 2 requests per 10 seconds

@app.get("/", dependencies=[Depends(global_limiter)])
async def root():
    return {"message": "Welcome to the rate-limited API"}

@app.get("/public", dependencies=[Depends(global_limiter)])
async def public_endpoint():
    return {"message": "This is a public endpoint with standard rate limiting"}

@app.get("/sensitive", dependencies=[Depends(strict_limiter)])
async def sensitive_endpoint():
    return {"message": "This is a sensitive endpoint with stricter rate limiting"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 429:
        return {"error": "Rate limit exceeded", "retry_after": "Please try again later"}
    return {"error": exc.detail}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🧪 Testing

To run the tests:

```bash
pip install pytest pytest-cov httpx
python -m pytest
```

Or use the provided Makefile:

```bash
make start-test
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Ali Yaman - [@aliymndb](https://twitter.com/aliymndb) - aliymn.db@gmail.com

Project Link: [https://github.com/AliYmn/fastapi-throttle](https://github.com/AliYmn/fastapi-throttle)
