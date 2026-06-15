from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound, BadRequest

from src.models.blockchain_model import CreateBatchDTO, TransferBatchDTO
from src.utils.api_response import ApiResponse


class BlockchainController:
    """
    Blockchain controller with lazy-loading of FabricClient and BlockchainService.
    This prevents pytest and Flask initialization from breaking before Docker/Fabric is up.
    """

    def __init__(self):
        # Lazy-loaded attributes
        self.fabric_client = None
        self.blockchain_service = None

    # ---------------------------------------------------------
    # Lazy initialization utilities
    # ---------------------------------------------------------
    def _ensure_client_and_service(self):
        """
        Initialize FabricClient and BlockchainService only when needed.
        This avoids loading Fabric connection profiles during import time.
        """
        if self.fabric_client is None or self.blockchain_service is None:
            # Import here to avoid circular imports + early initialization
            from config.fabric_config import get_fabric_client
            from src.services.blockchain_service import BlockchainService

            self.fabric_client = get_fabric_client()
            self.blockchain_service = BlockchainService(self.fabric_client)

    # ---------------------------------------------------------
    # Controller Methods
    # ---------------------------------------------------------

    def create_batch(self, data):
        try:
            self._ensure_client_and_service()

            dto = CreateBatchDTO().load(data)
            result = self.blockchain_service.create_batch(dto)

            return ApiResponse.response(True, "Batch created", result, 201)

        except ValidationError as e:
            return ApiResponse.response(False, e.messages, None, 400)

        except BadRequest as e:
            return ApiResponse.response(False, e.description, None, 400)

        except Exception:
            return ApiResponse.response(False, "Error creating batch", None, 500)

    def transfer_batch(self, data):
        try:
            self._ensure_client_and_service()

            dto = TransferBatchDTO().load(data)
            result = self.blockchain_service.transfer_batch(dto)

            return ApiResponse.response(True, "Batch transferred", result, 200)

        except ValidationError as e:
            return ApiResponse.response(False, e.messages, None, 400)

        except BadRequest as e:
            return ApiResponse.response(False, e.description, None, 400)

        except Exception:
            return ApiResponse.response(False, "Error transferring batch", None, 500)

    def mark_batch_delivered(self, data):
        try:
            self._ensure_client_and_service()

            if "batch_id" not in data or "delivered_to_org_id" not in data:
                raise BadRequest("batch_id and delivered_to_org_id are required")

            result = self.blockchain_service.mark_batch_delivered(
                data["batch_id"], data["delivered_to_org_id"]
            )

            return ApiResponse.response(True, "Batch delivered", result, 200)

        except BadRequest as e:
            return ApiResponse.response(False, e.description, None, 400)

        except Exception:
            return ApiResponse.response(False, "Error marking batch delivered", None, 500)

    def get_batch(self, batch_id: str):
        try:
            self._ensure_client_and_service()

            result = self.blockchain_service.get_batch(batch_id)

            return ApiResponse.response(True, "Batch found", result, 200)

        except NotFound:
            return ApiResponse.response(False, "Batch not found", None, 404)

        except BadRequest as e:
            return ApiResponse.response(False, e.description, None, 400)

        except Exception:
            return ApiResponse.response(False, "Error loading batch", None, 500)

    def get_batch_history(self, batch_id: str):
        try:
            self._ensure_client_and_service()

            result = self.blockchain_service.get_batch_history(batch_id)

            return ApiResponse.response(True, "Batch history loaded", result, 200)

        except NotFound:
            return ApiResponse.response(False, "Batch not found", None, 404)

        except BadRequest as e:
            return ApiResponse.response(False, e.description, None, 400)

        except Exception:
            return ApiResponse.response(False, "Error loading history", None, 500)
