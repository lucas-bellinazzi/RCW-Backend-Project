#!/usr/bin/env bash
set -e

# Basic env for Org1
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_MSPCONFIGPATH=${PWD}/fabric-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

CC_NAME="medicinecc"
CC_LABEL="medicinecc_1"
CHANNEL_NAME="mychannel"
SEQUENCE=1

echo "Installing chaincode on peer0.org1..."
peer lifecycle chaincode install ${CC_NAME}.tar.gz

PACKAGE_ID=$(peer lifecycle chaincode queryinstalled | sed -n "s/Package ID: \(.*\), Label: ${CC_LABEL}/\1/p")
echo "Discovered PACKAGE_ID=${PACKAGE_ID}"

echo "Approving chaincode for Org1..."
peer lifecycle chaincode approveformyorg \
  --channelID ${CHANNEL_NAME} \
  --name ${CC_NAME} \
  --version 1.0 \
  --package-id ${PACKAGE_ID} \
  --sequence ${SEQUENCE} \
  --orderer localhost:7050 \
  --tls false

echo "Committing chaincode definition..."
peer lifecycle chaincode commit \
  --channelID ${CHANNEL_NAME} \
  --name ${CC_NAME} \
  --version 1.0 \
  --sequence ${SEQUENCE} \
  --orderer localhost:7050 \
  --peerAddresses localhost:7051 \
  --tls false

echo "Chaincode ${CC_NAME} committed on channel ${CHANNEL_NAME}."
