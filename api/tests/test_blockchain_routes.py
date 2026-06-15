import json
from unittest.mock import patch, MagicMock
from werkzeug.exceptions import NotFound


@patch("config.fabric_config.get_fabric_client")
def test_create_batch_success(mock_get_fabric_client, client):
    # Mock fabric client to prevent wallet/network file load errors
    mock_get_fabric_client.return_value = MagicMock()

    payload = {
        "batch_id": "BATCH-TEST-1",
        "product_name": "Test Drug",
        "manufacture_date": "2025-01-01",
        "expiry_date": "2027-01-01",
        "total_quantity": 100,
        "unit_dosage": "100mg",
        "unit_price": 15.5,
        "owner_org_id": "MANUFACTURER_1",
    }

    fake_result = {**payload, "status": "CREATED", "ownerships": []}


    with patch(
        "src.services.blockchain_service.BlockchainService.create_batch",
        return_value=fake_result,
    ):
        response = client.post(
            "/blockchain/batches",
            data=json.dumps(payload),
            content_type="application/json",
        )

    data = response.get_json()
    assert response.status_code == 201
    assert data["success"] is True
    assert data["data"]["batch_id"] == "BATCH-TEST-1"


@patch("config.fabric_config.get_fabric_client")
def test_get_batch_not_found(mock_get_fabric_client, client):
    # Mock fabric client to prevent wallet/network file load errors
    mock_get_fabric_client.return_value = MagicMock()

    with patch(
        "src.services.blockchain_service.BlockchainService.get_batch",
        side_effect=NotFound("Batch not found"),
    ):
        response = client.get("/blockchain/batches/BATCH-NOT-EXISTS")

    data = response.get_json()
    assert response.status_code == 404
    assert data["success"] is False

