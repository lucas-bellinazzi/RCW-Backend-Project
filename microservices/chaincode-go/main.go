package main

import (
	"log"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

func main() {
	medicalRecordContract := new(MedicalRecordContract)
	
	cc, err := contractapi.NewChaincode(medicalRecordContract)
	if err != nil {
		log.Panicf("Error creating medical records chaincode: %v", err)
	}
	
	if err := cc.Start(); err != nil {
		log.Panicf("Error starting medical records chaincode: %v", err)
	}
}