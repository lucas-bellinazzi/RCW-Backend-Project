import json
import asyncio
from pathlib import Path
from hfc.fabric import Client


class FabricClient:
    """
    Fabric client wrapper used by blockchain_repository.py.
    """

    def __init__(
        self,
        ccp_path: str,
        wallet_path: str,
        user_id: str,
        msp_id: str,
        channel_name: str,
        chaincode_name: str,
        contract_name: str,
    ) -> None:

        self.ccp_path = Path(ccp_path)
        self.wallet_path = Path(wallet_path)
        self.user_id = user_id
        self.msp_id = msp_id
        self.channel_name = channel_name
        self.chaincode_name = chaincode_name
        self.contract_name = contract_name

        # Load connection profile
        self.client = Client(net_profile=str(self.ccp_path))

        # Load user identity from wallet
        self._load_identity()

        # Get channel instance
        self.channel = self.client.get_channel(self.channel_name)

    # --------------------------------------------------------
    # Load identity (certificate + private key)
    # --------------------------------------------------------
    def _load_identity(self):
        cert_path = self.wallet_path / f"{self.user_id}.crt"
        key_path = self.wallet_path / f"{self.user_id}.key"

        if not cert_path.exists() or not key_path.exists():
            raise FileNotFoundError(
                f"Identity files not found in wallet: {cert_path}, {key_path}"
            )

        with open(cert_path, "r") as f:
            cert = f.read()

        with open(key_path, "r") as f:
            key = f.read()

        # Register identity inside SDK
        self.client._users[self.user_id] = {
            "cert": cert,
            "private_key": key,
            "mspid": self.msp_id,
        }

    # --------------------------------------------------------
    # Evaluate transaction (read)
    # --------------------------------------------------------
    async def evaluate_transaction(self, fcn: str, args: list[str]):
        # Use contract_name:function format if contract_name is provided
        function_name = f"{self.contract_name}:{fcn}" if self.contract_name else fcn
        
        response = await self.client.chaincode_query(
            requestor=self.user_id,
            channel_name=self.channel_name,
            chaincode_name=self.chaincode_name,
            fcn=function_name,
            args=args,
        )

        try:
            return json.loads(response)
        except Exception:
            return response

    # --------------------------------------------------------
    # Submit transaction (write)
    # --------------------------------------------------------
    async def submit_transaction(self, fcn: str, args: list[str]):
        # Use contract_name:function format if contract_name is provided
        function_name = f"{self.contract_name}:{fcn}" if self.contract_name else fcn
        
        response = await self.client.chaincode_invoke(
            requestor=self.user_id,
            peers=["peer0.org1.example.com"],
            channel_name=self.channel_name,
            chaincode_name=self.chaincode_name,
            fcn=function_name,
            args=args,
            wait_for_event=True,
        )

        try:
            return json.loads(response)
        except Exception:
            return response

    # --------------------------------------------------------
    # Public sync wrappers
    # --------------------------------------------------------
    def evaluate(self, function: str, args: list[str]):
        return asyncio.get_event_loop().run_until_complete(
            self.evaluate_transaction(function, args)
        )

    def submit(self, function: str, args: list[str]):
        return asyncio.get_event_loop().run_until_complete(
            self.submit_transaction(function, args)
        )
