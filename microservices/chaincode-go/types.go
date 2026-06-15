package main

import "time"

// Patient represents a medical patient record
type Patient struct {
	PatientID      string         `json:"patientId"`
	Name           string         `json:"name"`
	DateOfBirth    string         `json:"dateOfBirth"`
	BloodType      string         `json:"bloodType"`
	Allergies      []string       `json:"allergies"`
	Medications    []string       `json:"medications"`
	LastUpdated    time.Time      `json:"lastUpdated"`
	DoctorID       string         `json:"doctorId"`
	MedicalHistory []MedicalEvent `json:"medicalHistory"`
}

// MedicalEvent represents a single medical event in a patient's history
type MedicalEvent struct {
	Date        string `json:"date"`
	Description string `json:"description"`
	DoctorID    string `json:"doctorId"`
	Type        string `json:"type"` // Consultation, Treatment, Surgery, etc.
}
