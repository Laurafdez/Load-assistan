import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from app.schemas.load import LoadBase
from app.core.config import settings

# FastAPI test client
client = TestClient(app)

# Required header with valid API key
headers = {"X-API-Key": settings.AUTH_API_KEY}


@pytest.fixture
def mock_load_data():
    """
    Returns a sample list of load records with various urgency levels and delivery times.
    """
    return [
        LoadBase(
            load_id="L001",
            origin="Chicago",
            destination="Dallas",
            pickup_datetime=datetime(2025, 8, 4, 10, 0),
            delivery_datetime=datetime(2025, 8, 7, 8, 0),
            equipment_type="Dry Van",
            loadboard_rate=1150.0,
            notes="Normal load",
            weight=14000.0,
            commodity_type="Clothing",
            num_of_pieces=12,
            miles=960.0,
            dimensions="40x48x60",
        ),
        LoadBase(
            load_id="L002",
            origin="Chicago",
            destination="Dallas",
            pickup_datetime=datetime(2025, 8, 4, 11, 0),
            delivery_datetime=datetime(2025, 8, 5, 12, 0),
            equipment_type="Dry Van",
            loadboard_rate=1200.0,
            notes="Urgent - ASAP",
            weight=15000.0,
            commodity_type="Electronics",
            num_of_pieces=10,
            miles=980.0,
            dimensions="40x48x60",
        ),
        LoadBase(
            load_id="L003",
            origin="Chicago",
            destination="Dallas",
            pickup_datetime=datetime(2025, 8, 4, 9, 0),
            delivery_datetime=datetime(2025, 8, 6, 16, 0),
            equipment_type="Dry Van",
            loadboard_rate=1100.0,
            notes="",
            weight=13000.0,
            commodity_type="Furniture",
            num_of_pieces=15,
            miles=1000.0,
            dimensions="40x48x72",
        ),
    ]


def test_prioritized_loads_on_exact_match(monkeypatch, mock_load_data):
    """
    If the API returns multiple loads from strict filters,
    they should be ordered by urgency and then by delivery time.
    """

    def mock_filter_loads_from_db(db, filters):
        return mock_load_data

    monkeypatch.setattr(
        "app.api.v1.routes.load.filter_loads_from_db", mock_filter_loads_from_db
    )

    response = client.get(
        "/api/v1/loads",
        params={"origin": "Chicago", "destination": "Dallas"},
        headers=headers,
    )

    assert response.status_code == 200
    loads = response.json()
    assert len(loads) == 3

    # First should be the urgent one
    assert "urgent" in loads[0]["notes"].lower()
    assert loads[0]["load_id"] == "L002"

    # Confirm delivery_datetime ordering afterward
    delivery_dates = [datetime.fromisoformat(l["delivery_datetime"]) for l in loads]
    assert delivery_dates == sorted(delivery_dates)


def test_fallback_logic_when_strict_filters_fail(monkeypatch, mock_load_data):
    """
    When the strict query returns no matches, fallback should return relaxed matches.
    """

    calls = []

    def mock_filter_loads_from_db(db, filters):
        calls.append(1)
        return [] if len(calls) == 1 else mock_load_data

    monkeypatch.setattr(
        "app.api.v1.routes.load.filter_loads_from_db", mock_filter_loads_from_db
    )

    response = client.get(
        "/api/v1/loads",
        params={"origin": "Chicago", "pickup_datetime_from": "2025-08-10T00:00:00"},
        headers=headers,
    )

    assert response.status_code == 200
    loads = response.json()
    assert len(loads) == 3
    assert "urgent" in loads[0]["notes"].lower()


def test_no_loads_returned_when_no_matches(monkeypatch):
    """
    When no loads match either strict or relaxed filters, API should return an empty list.
    """

    def mock_filter_loads_from_db(db, filters):
        return []

    monkeypatch.setattr(
        "app.api.v1.routes.load.filter_loads_from_db", mock_filter_loads_from_db
    )

    response = client.get(
        "/api/v1/loads",
        params={"origin": "Nowhere"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == []
