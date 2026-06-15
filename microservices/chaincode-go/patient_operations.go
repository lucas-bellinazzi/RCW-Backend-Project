package main

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// CreatePatient creates a new patient record in the world state
func (s *MedicalRecordContract) CreatePatient(ctx contractapi.TransactionContextInterface, patientID string, name string,
	dateOfBirth string, bloodType string, allergiesJSON string, medicationsJSON string, doctorID string) error {

	exists, err := s.PatientExists(ctx, patientID)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the patient %s already exists", patientID)
	}

	var allergies []string
	var medications []string

	err = json.Unmarshal([]byte(allergiesJSON), &allergies)
	if err != nil {
		return fmt.Errorf("failed to unmarshal allergies: %v", err)
	}

	err = json.Unmarshal([]byte(medicationsJSON), &medications)
	if err != nil {
		return fmt.Errorf("failed to unmarshal medications: %v", err)
	}

	// Get timestamp from transaction context
	txTimestamp, err := ctx.GetStub().GetTxTimestamp()
	if err != nil {
		return fmt.Errorf("failed to get transaction timestamp: %v", err)
	}
	txTime := time.Unix(txTimestamp.Seconds, int64(txTimestamp.Nanos))

	patient := Patient{
		PatientID:      patientID,
		Name:           name,
		DateOfBirth:    dateOfBirth,
		BloodType:      bloodType,
		Allergies:      allergies,
		Medications:    medications,
		LastUpdated:    txTime,
		DoctorID:       doctorID,
		MedicalHistory: []MedicalEvent{},
	}

	patientJSON, err := json.Marshal(patient)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(patientID, patientJSON)
}

// ReadPatient returns the patient record stored in the world state with given id
func (s *MedicalRecordContract) ReadPatient(ctx contractapi.TransactionContextInterface, patientID string) (*Patient, error) {
	patientJSON, err := ctx.GetStub().GetState(patientID)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if patientJSON == nil {
		return nil, fmt.Errorf("the patient %s does not exist", patientID)
	}

	var patient Patient
	err = json.Unmarshal(patientJSON, &patient)
	if err != nil {
		return nil, err
	}

	return &patient, nil
}

// UpdatePatientInfo updates a patient's basic information
func (s *MedicalRecordContract) UpdatePatientInfo(ctx contractapi.TransactionContextInterface,
	patientID string, name string, bloodType string, allergiesJSON string, medicationsJSON string, doctorID string) error {

	patient, err := s.ReadPatient(ctx, patientID)
	if err != nil {
		return err
	}

	var allergies []string
	var medications []string

	err = json.Unmarshal([]byte(allergiesJSON), &allergies)
	if err != nil {
		return fmt.Errorf("failed to unmarshal allergies: %v", err)
	}

	err = json.Unmarshal([]byte(medicationsJSON), &medications)
	if err != nil {
		return fmt.Errorf("failed to unmarshal medications: %v", err)
	}

	// Get timestamp from transaction context
	txTimestamp, err := ctx.GetStub().GetTxTimestamp()
	if err != nil {
		return fmt.Errorf("failed to get transaction timestamp: %v", err)
	}
	txTime := time.Unix(txTimestamp.Seconds, int64(txTimestamp.Nanos))

	// Update the patient info
	patient.Name = name
	patient.BloodType = bloodType
	patient.Allergies = allergies
	patient.Medications = medications
	patient.LastUpdated = txTime
	patient.DoctorID = doctorID

	patientJSON, err := json.Marshal(patient)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(patientID, patientJSON)
}

// AddMedicalEvent adds a new medical event to a patient's history
func (s *MedicalRecordContract) AddMedicalEvent(ctx contractapi.TransactionContextInterface,
	patientID string, date string, description string, doctorID string, eventType string) error {

	patient, err := s.ReadPatient(ctx, patientID)
	if err != nil {
		return err
	}

	newEvent := MedicalEvent{
		Date:        date,
		Description: description,
		DoctorID:    doctorID,
		Type:        eventType,
	}

	// Get timestamp from transaction context
	txTimestamp, err := ctx.GetStub().GetTxTimestamp()
	if err != nil {
		return fmt.Errorf("failed to get transaction timestamp: %v", err)
	}
	txTime := time.Unix(txTimestamp.Seconds, int64(txTimestamp.Nanos))

	patient.MedicalHistory = append(patient.MedicalHistory, newEvent)
	patient.LastUpdated = txTime

	patientJSON, err := json.Marshal(patient)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(patientID, patientJSON)
}

// GetAllPatients returns all patients found in world state
func (s *MedicalRecordContract) GetAllPatients(ctx contractapi.TransactionContextInterface) ([]*Patient, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var patients []*Patient
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var patient Patient
		err = json.Unmarshal(queryResponse.Value, &patient)
		if err != nil {
			return nil, err
		}
		patients = append(patients, &patient)
	}

	return patients, nil
}

// PatientExists returns true when patient with given ID exists in world state
func (s *MedicalRecordContract) PatientExists(ctx contractapi.TransactionContextInterface, patientID string) (bool, error) {
	patientJSON, err := ctx.GetStub().GetState(patientID)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return patientJSON != nil, nil
}

// GetPatientsByDoctor retrieves all patients for a specific doctor
func (s *MedicalRecordContract) GetPatientsByDoctor(ctx contractapi.TransactionContextInterface, doctorID string) ([]*Patient, error) {
	allPatients, err := s.GetAllPatients(ctx)
	if err != nil {
		return nil, err
	}

	var doctorPatients []*Patient
	for _, patient := range allPatients {
		if patient.DoctorID == doctorID {
			doctorPatients = append(doctorPatients, patient)
		}
	}

	return doctorPatients, nil
}

// DeletePatient deletes a given patient from the world state
func (s *MedicalRecordContract) DeletePatient(ctx contractapi.TransactionContextInterface, patientID string) error {
	exists, err := s.PatientExists(ctx, patientID)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the patient %s does not exist", patientID)
	}

	return ctx.GetStub().DelState(patientID)
}
