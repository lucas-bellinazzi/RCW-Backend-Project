# Blockchain Application for Drug Traceability

This repository contains the backend and blockchain components for a drug traceability system designed to ensure the authenticity and secure tracking of pharmaceuticals throughout the supply chain.

## Project Architecture

The project consists of three main modules:
1. **API Gateway (Flask)**: Handles user authentication, organization management, inventory, and acts as the interface to the Hyperledger Fabric network.
2. **Blockchain Gateway (Node.js)**: A lightweight Express microservice configured to interact with the Hyperledger Fabric network.
3. **Smart Contracts (Go)**: Chaincode logic implemented for Hyperledger Fabric.

---

## Requirements

To run this project locally, you will need:
- **Python 3.11+**
- **Node.js v18+ & Yarn / npm**
- **Docker & Docker Compose**
- **PostgreSQL Database**
- **Hyperledger Fabric binaries and configtx/cryptogen tools** (for generating network materials)

---

## Execution Instructions

### 1. Database Setup & Configuration
1. Create a PostgreSQL database named `rcw` (or your preferred name).
2. Create an `.env` file in the `api` folder based on `.env.example`:
   ```bash
   cp api/.env.example api/.env
   ```
3. Update the `DATABASE_URI_POSTGRES` variable with your credentials:
   ```env
   DATABASE_URI_POSTGRES=postgresql://<username>:<password>@localhost:5432/rcw
   ```

### 2. Python Flask API Setup
1. Navigate to the `api` directory:
   ```bash
   cd api
   ```
2. Create and activate a Python virtual environment:
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **Linux / macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations to create the tables:
   ```bash
   flask db upgrade
   ```
5. Seed the database with mock test data (organizations, users, inventory):
   ```bash
   python seed_database.py
   ```
6. Start the API development server:
   ```bash
   flask run --port=5000
   ```

### 3. Running Unit Tests
To run the automated tests and verify the routes (using mocked blockchain connections):
```bash
cd api
pytest
```

### 4. Setting up the Hyperledger Fabric Blockchain
To start the network using Docker Compose:
1. Ensure the network crypto materials and genesis block are placed in `./fabric-network` (see the "Current Codebase Limitations" section below).
2. Start the containers:
   ```bash
   docker-compose up -d
   ```
3. Deploy the chaincode on the peer by executing the scripts:
   ```bash
   bash scripts/package_chaincode.sh
   bash scripts/deploy_chaincode.sh
   ```

### 5. Node.js Blockchain Gateway Setup
1. Navigate to the gateway directory:
   ```bash
   cd microservices/blockchain-gateway-nodejs
   ```
2. Install dependencies:
   ```bash
   yarn install  # or: npm install
   ```
3. Start the gateway server:
   ```bash
   npm start
   ```

---

## Current Codebase Limitations & Gaps

During analysis, the following structural gaps were identified. You must resolve these before deploying the network to production:

1. **Chaincode Mismatch:**
   * The **Flask API** ([api/src/repositories/blockchain_repository.py](api/src/repositories/blockchain_repository.py)) is built to track drug batches (`createBatch`, `transferBatch`, `markBatchDelivered`, etc.).
   * However, the chaincode inside `microservices/chaincode-go` is designed for a **Patient Medical Records** application (`CreatePatient`, `ReadPatient`, etc.). 
   * You will need to implement or replace the Go chaincode to match the `createBatch` drug traceability API endpoints.

2. **Missing `fabric-network` Files:**
   * The `docker-compose.yml` mounts files from the `./fabric-network` directory (crypto certificates, MSP, orderer genesis block).
   * These folders are not included in the git repository and must be generated locally using Hyperledger Fabric's `cryptogen` and `configtxgen` tools prior to booting up the Docker containers.

3. **PostgreSQL Docker Integration:**
   * The `docker-compose.yml` does not contain a PostgreSQL database service. You must run Postgres locally or add a `postgres` service to the docker-compose configuration.

4. **Hardcoded User Paths:**
   * The Node.js gateway ([microservices/blockchain-gateway-nodejs/index.js](microservices/blockchain-gateway-nodejs/index.js)) contains hardcoded Linux filesystem paths pointing to `/home/lucas/fabric/...`. Adjust these to variables or relative workspace paths for cross-platform deployment.
