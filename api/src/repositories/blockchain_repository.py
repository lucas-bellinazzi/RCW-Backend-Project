import json
from typing import Any, Dict, List


class BlockchainRepository:
    def __init__(self, fabric_client):
        self.client = fabric_client

    def _submit(self, function_name: str, args: List[str]):
        return self.client.submit(function_name, args)

    def _evaluate(self, function_name: str, args: List[str]):
        return self.client.evaluate(function_name, args)

    def create_batch(self, dto: Dict[str, Any]):
        args = [
            dto["batch_id"],
            dto["product_name"],
            dto["manufacture_date"],
            dto["expiry_date"],
            str(dto["total_quantity"]),
            dto["unit_dosage"],
            str(dto["unit_price"]),
            dto["owner_org_id"],
        ]
        return self._submit("createBatch", args)

    def transfer_batch(self, dto: Dict[str, Any]):
        args = [
            dto["batch_id"],
            dto["from_org_id"],
            dto["to_org_id"],
            str(dto["quantity"]),
            json.dumps(dto.get("metadata", {})),
        ]
        return self._submit("transferBatch", args)

    def mark_batch_delivered(self, batch_id: str, delivered_to_org_id: str, quantity: int):
        return self._submit("markBatchDelivered", [batch_id, delivered_to_org_id, str(quantity)])

    def get_batch(self, batch_id: str):
        return self._evaluate("getBatch", [batch_id])

    def get_batch_history(self, batch_id: str):
        return self._evaluate("getBatchHistory", [batch_id])
