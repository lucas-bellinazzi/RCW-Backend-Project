package main

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// InitLedger adds sample patients to the ledger
func (s *MedicalRecordContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	// Get timestamp from transaction context
	txTimestamp, err := ctx.GetStub().GetTxTimestamp()
	if err != nil {
		return fmt.Errorf("failed to get transaction timestamp: %v", err)
	}

	// Convert to time.Time
	txTime := time.Unix(txTimestamp.Seconds, int64(txTimestamp.Nanos))

	patients := []Patient{
		{
			PatientID:   "PATIENT1",
			Name:        "Alice Smith",
			DateOfBirth: "1980-05-15",
			BloodType:   "A+",
			Allergies:   []string{"Penicillin", "Peanuts"},
			Medications: []string{"Lisinopril"},
			LastUpdated: txTime,
			DoctorID:    "DOC1",
			MedicalHistory: []MedicalEvent{
				{
					Date:        "2023-01-10",
					Description: "Annual checkup - blood pressure normal",
					DoctorID:    "DOC1",
					Type:        "Consultation",
				},
			},
		},
		{
			PatientID:   "PATIENT2",
			Name:        "Bob Johnson",
			DateOfBirth: "1975-11-23",
			BloodType:   "O-",
			Allergies:   []string{"Sulfa drugs"},
			Medications: []string{"Metformin", "Atorvastatin"},
			LastUpdated: txTime,
			DoctorID:    "DOC2",
			MedicalHistory: []MedicalEvent{
				{
					Date:        "2023-02-15",
					Description: "Diagnosed with Type 2 Diabetes",
					DoctorID:    "DOC2",
					Type:        "Diagnosis",
				},
			},
		},
	}

	for _, patient := range patients {
		patientJSON, err := json.Marshal(patient)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(patient.PatientID, patientJSON)
		if err != nil {
			return fmt.Errorf("failed to put patient record to world state: %v", err)
		}
	}

	return nil
}
