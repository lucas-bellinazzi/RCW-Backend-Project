#!/usr/bin/env bash
set -e

# This script packages the medicine chaincode

CC_LABEL="medicinecc_1"
CC_NAME="medicinecc"
CC_LANG="node"
CC_PATH="../blockchain/chaincode/medicine"

echo "Packaging chaincode ${CC_NAME}..."

peer lifecycle chaincode package ${CC_NAME}.tar.gz \
  --path ${CC_PATH} \
  --lang ${CC_LANG} \
  --label ${CC_LABEL}

echo "Chaincode package created: ${CC_NAME}.tar.gz"
