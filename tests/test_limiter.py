from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from fastapi_throttle import RateLimiter
import time


def test_rate_limiter():
    app = FastAPI()

    # Define routes with different rate limits
    @app.get("/route1", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
    async def route1():
        return {"message": "This is route 1"}

    @app.get("/route2", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
    async def route2():
        return {"message": "This is route 2"}

    client = TestClient(app)

    # Test for route1
    response = client.get("/route1")
    assert response.status_code == 200
    response = client.get("/route1")
    assert response.status_code == 200
    response = client.get("/route1")
    assert response.status_code == 429  # Third request should hit the rate limit

    # Test for route2
    response = client.get("/route2")
    assert response.status_code == 200
    response = client.get("/route2")
    assert response.status_code == 200
    response = client.get("/route2")
    assert response.status_code == 429  # Third request should hit the rate limit

    # Wait for the rate limit to reset
    time.sleep(5)  # Rate limit duration, ensure this matches the limiter setting

    # Retry the requests after waiting for the limit to reset
    response = client.get("/route1")
    assert response.status_code == 200  # Limit should be reset

    response = client.get("/route2")
    assert response.status_code == 200  # Limit should be reset


def test_add_headers_and_retry_after():
    app = FastAPI()

    limiter = RateLimiter(times=2, seconds=5, add_headers=True)

    @app.get("/limited", dependencies=[Depends(limiter)])
    async def limited():
        return {"ok": True}

    client = TestClient(app)

    # First request should include X-RateLimit headers
    r1 = client.get("/limited")
    assert r1.status_code == 200
    assert r1.headers.get("X-RateLimit-Limit") == "2"
    assert r1.headers.get("X-RateLimit-Remaining") == "1"

    # Second request still 200, remaining becomes 0
    r2 = client.get("/limited")
    assert r2.status_code == 200
    assert r2.headers.get("X-RateLimit-Limit") == "2"
    assert r2.headers.get("X-RateLimit-Remaining") == "0"

    # Third request should hit 429 and include Retry-After
    r3 = client.get("/limited")
    assert r3.status_code == 429
    assert r3.headers.get("Retry-After") is not None
    assert r3.headers["Retry-After"].isdigit()


def test_retry_after_without_add_headers():
    app = FastAPI()

    limiter = RateLimiter(times=1, seconds=5, add_headers=False)

    @app.get("/rl", dependencies=[Depends(limiter)])
    async def rl():
        return {"ok": True}

    client = TestClient(app)
    assert client.get("/rl").status_code == 200
    r2 = client.get("/rl")
    assert r2.status_code == 429
    assert r2.headers.get("Retry-After") is not None


def test_trust_proxy_uses_x_forwarded_for():
    app = FastAPI()

    limiter = RateLimiter(times=1, seconds=10, trust_proxy=True)

    @app.get("/p", dependencies=[Depends(limiter)])
    async def p():
        return {"ok": True}

    client = TestClient(app)

    # Same client but with same first IP should hit the limit on second call
    headers_a = {"X-Forwarded-For": "1.1.1.1, 2.2.2.2"}
    assert client.get("/p", headers=headers_a).status_code == 200
    assert client.get("/p", headers=headers_a).status_code == 429

    # Different first IP should be treated as a different key
    headers_b = {"X-Forwarded-For": "3.3.3.3, 4.4.4.4"}
    assert client.get("/p", headers=headers_b).status_code == 200


def test_custom_key_func_by_user():
    app = FastAPI()

    def user_key(req):
        return req.headers.get("x-user-id", "anon")

    limiter = RateLimiter(times=1, seconds=10, key_func=user_key)

    @app.get("/u", dependencies=[Depends(limiter)])
    async def u():
        return {"ok": True}

    client = TestClient(app)

    # user A limited on second call
    headers_a = {"x-user-id": "A"}
    assert client.get("/u", headers=headers_a).status_code == 200
    assert client.get("/u", headers=headers_a).status_code == 429

    # user B is a different key, first call is allowed
    headers_b = {"x-user-id": "B"}
    assert client.get("/u", headers=headers_b).status_code == 200
