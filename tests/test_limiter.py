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
