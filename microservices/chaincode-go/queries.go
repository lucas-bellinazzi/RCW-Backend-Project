package main

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// QueryPatientsByBloodType returns patients with the specified blood type
func (s *MedicalRecordContract) QueryPatientsByBloodType(ctx contractapi.TransactionContextInterface, bloodType string) ([]*Patient, error) {
	queryString := fmt.Sprintf(`{"selector":{"bloodType":"%s"}}`, bloodType)
	return getQueryResultForQueryString(ctx, queryString)
}

// QueryPatientsByAgeRange returns patients within a specific age range (based on date of birth)
func (s *MedicalRecordContract) QueryPatientsByAgeRange(ctx contractapi.TransactionContextInterface, startDate string, endDate string) ([]*Patient, error) {
	queryString := fmt.Sprintf(`{"selector":{"dateOfBirth":{"$gte":"%s","$lte":"%s"}}}`, startDate, endDate)
	return getQueryResultForQueryString(ctx, queryString)
}

// QueryPatientsByAllergy returns patients with a specific allergy
func (s *MedicalRecordContract) QueryPatientsByAllergy(ctx contractapi.TransactionContextInterface, allergy string) ([]*Patient, error) {
	queryString := fmt.Sprintf(`{"selector":{"allergies":{"$elemMatch":{"$eq":"%s"}}}}`, allergy)
	return getQueryResultForQueryString(ctx, queryString)
}

// QueryPatientsWithCondition returns patients with a certain condition in their medical history
func (s *MedicalRecordContract) QueryPatientsWithCondition(ctx contractapi.TransactionContextInterface, condition string) ([]*Patient, error) {
	queryString := fmt.Sprintf(`{"selector":{"medicalHistory":{"$elemMatch":{"description":{"$regex":"(?i)%s"}}}}}`, condition)
	return getQueryResultForQueryString(ctx, queryString)
}

// getQueryResultForQueryString is a helper function for processing CouchDB queries
func getQueryResultForQueryString(ctx contractapi.TransactionContextInterface, queryString string) ([]*Patient, error) {
	resultsIterator, err := ctx.GetStub().GetQueryResult(queryString)
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var patients []*Patient
	for resultsIterator.HasNext() {
		queryResult, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var patient Patient
		err = json.Unmarshal(queryResult.Value, &patient)
		if err != nil {
			return nil, err
		}
		patients = append(patients, &patient)
	}

	return patients, nil
}
