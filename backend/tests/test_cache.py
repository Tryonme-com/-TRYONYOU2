import pytest
from fastapi.testclient import TestClient
from main import app
import jules_engine
from unittest.mock import AsyncMock, MagicMock

client = TestClient(app)

@pytest.mark.asyncio
async def test_recommendation_caching(monkeypatch):
    # Mock the AI engine response
    mock_response = MagicMock()
    mock_response.text = "Caching works!"

    mock_generate = AsyncMock(return_value=mock_response)
    monkeypatch.setattr("jules_engine.model.generate_content_async", mock_generate)

    # Clear cache before test
    jules_engine._recommendation_cache.clear()

    payload = {
        "height": 175.0,
        "weight": 68.0,
        "event_type": "Gala",
        "body_shape": "Athletic",
        "fit_preference": "Fitted"
    }

    # First call - should trigger AI
    response1 = client.post("/api/recommend", json=payload)
    assert response1.status_code == 200
    assert response1.json()["recommendation"] == "Caching works!"
    assert mock_generate.call_count == 1

    # Second call - should use cache
    response2 = client.post("/api/recommend", json=payload)
    assert response2.status_code == 200
    assert response2.json()["recommendation"] == "Caching works!"
    assert mock_generate.call_count == 1  # Still 1
