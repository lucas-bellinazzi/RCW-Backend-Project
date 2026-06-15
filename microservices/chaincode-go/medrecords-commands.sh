#!/bin/bash

# Set environment variables
export FABRIC_CFG_PATH=$PWD/../config/
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
export ORDERER_CA=${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
export ORG2_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt

# Function to initialize the ledger
initLedger() {
  peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
    --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
    --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
    -c '{"function":"InitLedger","Args":[]}'
}

# Function to create a patient
# createPatient() {
#   # Args: patientID, name, dateOfBirth, bloodType, allergiesJSON, medicationsJSON, doctorID
#   peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
#     --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
#     --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
#     -c "{\"function\":\"CreatePatient\",\"Args\":[\"$1\",\"$2\",\"$3\",\"$4\",\"$5\",\"$6\",\"$7\"]}"
# }
# createPatient() {
#   allergies=$(echo "$5" | sed 's/"/\\"/g')
#   medications=$(echo "$6" | sed 's/"/\\"/g')
#   # Args: patientID, name, dateOfBirth, bloodType, allergiesJSON, medicationsJSON, doctorID
#   peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
#   --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
#   --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
#   -c "{\"function\":\"CreatePatient\",\"Args\":[\"$1\",\"$2\",\"$3\",\"$4\",\"$5\",\"$6\",\"$7\"]}"
# }
createPatient() {
  # Escape the JSON arrays properly
  allergies=$(echo "$5" | sed 's/"/\\"/g')
  medications=$(echo "$6" | sed 's/"/\\"/g')
  
  # Args: patientID, name, dateOfBirth, bloodType, allergiesJSON, medicationsJSON, doctorID
  peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
  --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
  --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
  -c "{\"function\":\"CreatePatient\",\"Args\":[\"$1\",\"$2\",\"$3\",\"$4\",\"$allergies\",\"$medications\",\"$7\"]}"
}
# "PATIENT3" "John Doe" "1990-07-22" "B+" "[\"Latex\"]" "[\"Aspirin\"]" "DOC1"
# Function to read a patient
readPatient() {
  # Args: patientID
  peer chaincode query -C mychannel -n medrecords -c "{\"Args\":[\"ReadPatient\",\"$1\"]}"
}

# Function to update patient info
# updatePatientInfo() {
#   # Args: patientID, name, bloodType, allergiesJSON, medicationsJSON, doctorID
#   peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
#     --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
#     --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
#     -c "{\"function\":\"UpdatePatientInfo\",\"Args\":[\"$1\",\"$2\",\"$3\",\"$4\",\"$5\",\"$6\"]}"
# }
updatePatientInfo() {
  # Escape the JSON arrays properly
  allergies=$(echo "$4" | sed 's/"/\\"/g')
  medications=$(echo "$5" | sed 's/"/\\"/g')
  
  # Args: patientID, name, bloodType, allergiesJSON, medicationsJSON, doctorID
  peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
  --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
  --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
  -c "{\"function\":\"UpdatePatientInfo\",\"Args\":[\"$1\",\"$2\",\"$3\",\"$allergies\",\"$medications\",\"$6\"]}"
}

# Function to add a medical event
addMedicalEvent() {
  # Args: patientID, date, description, doctorID, eventType
  peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
    --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
    --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
    -c "{\"function\":\"AddMedicalEvent\",\"Args\":[\"$1\",\"$2\",\"$3\",\"$4\",\"$5\"]}"
}

# Function to get all patients
getAllPatients() {
  peer chaincode query -C mychannel -n medrecords -c '{"Args":["GetAllPatients"]}'
}

# Function to get patients by doctor
getPatientsByDoctor() {
  # Args: doctorID
  peer chaincode query -C mychannel -n medrecords -c "{\"Args\":[\"GetPatientsByDoctor\",\"$1\"]}"
}

# Function to delete a patient
deletePatient() {
  # Args: patientID
  peer chaincode invoke -o localhost:7050 --tls --cafile $ORDERER_CA -C mychannel -n medrecords \
    --peerAddresses localhost:7051 --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \
    --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2_TLS_ROOTCERT_FILE \
    -c "{\"function\":\"DeletePatient\",\"Args\":[\"$1\"]}"
}

# Function to query patients by blood type
queryPatientsByBloodType() {
  # Args: bloodType
  peer chaincode query -C mychannel -n medrecords -c "{\"Args\":[\"QueryPatientsByBloodType\",\"$1\"]}"
}

# Function to query patients by age range (birth date range)
queryPatientsByAgeRange() {
  # Args: startDate, endDate
  peer chaincode query -C mychannel -n medrecords -c "{\"Args\":[\"QueryPatientsByAgeRange\",\"$1\",\"$2\"]}"
}

# Function to query patients by allergy
queryPatientsByAllergy() {
  # Args: allergy
  peer chaincode query -C mychannel -n medrecords -c "{\"Args\":[\"QueryPatientsByAllergy\",\"$1\"]}"
}

# Function to query patients with a certain condition
queryPatientsWithCondition() {
  # Args: condition
  peer chaincode query -C mychannel -n medrecords -c "{\"Args\":[\"QueryPatientsWithCondition\",\"$1\"]}"
}