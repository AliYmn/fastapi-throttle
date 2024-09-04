from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from fastapi_throttle import RateLimiter
import time


def test_rate_limiter():
    app = FastAPI()

    # Routes with rate limiting
    @app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
    async def root():
        return {"message": "Hello, World!"}

    @app.get("/route1", dependencies=[Depends(RateLimiter(times=3, seconds=10))])
    async def route1():
        return {"message": "This is route 1"}

    @app.get("/route2", dependencies=[Depends(RateLimiter(times=5, seconds=15))])
    async def route2():
        return {"message": "This is route 2"}

    client = TestClient(app)

    # Test for the root route
    response = client.get("/")
    assert response.status_code == 200
    response = client.get("/")
    assert response.status_code == 200
    response = client.get("/")
    assert response.status_code == 429

    # Test for route1
    response = client.get("/route1")
    assert response.status_code == 200
    response = client.get("/route1")
    assert response.status_code == 200
    response = client.get("/route1")
    assert response.status_code == 200
    response = client.get("/route1")
    assert response.status_code == 429

    # Test for route2
    response = client.get("/route2")
    assert response.status_code == 200
    response = client.get("/route2")
    assert response.status_code == 200
    response = client.get("/route2")
    assert response.status_code == 200
    response = client.get("/route2")
    assert response.status_code == 200
    response = client.get("/route2")
    assert response.status_code == 200
    response = client.get("/route2")
    assert response.status_code == 429

    # Wait for the rate limit to reset
    time.sleep(10)

    # Test again after waiting for the limit to reset
    response = client.get("/")
    assert response.status_code == 200  # Limit should be reset

    response = client.get("/route1")
    assert response.status_code == 200  # Limit should be reset

    response = client.get("/route2")
    assert response.status_code == 200  # Limit should be reset
