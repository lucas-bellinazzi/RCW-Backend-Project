import os
from src.fabric.fabric_client import FabricClient


def get_fabric_client():
    """
    Initializes and returns a singleton FabricClient instance.
    """

    ccp_path = os.getenv("FABRIC_CCP_PATH")
    wallet_path = os.getenv("FABRIC_WALLET_PATH")
    user_id = os.getenv("FABRIC_USER_ID")
    msp_id = os.getenv("FABRIC_MSP_ID")
    channel = os.getenv("FABRIC_CHANNEL")
    chaincode = os.getenv("FABRIC_CHAINCODE")
    contract = os.getenv("FABRIC_CONTRACT")

    if not all([ccp_path, wallet_path, user_id, msp_id, channel, chaincode, contract]):
        raise RuntimeError("Fabric environment variables missing.")

    return FabricClient(
        ccp_path=ccp_path,
        wallet_path=wallet_path,
        user_id=user_id,
        msp_id=msp_id,
        channel_name=channel,
        chaincode_name=chaincode,
        contract_name=contract,
    )
