const express = require("express");
const cors = require("cors");
const morgan = require("morgan");
const path = require("path");
const fs = require("fs");
const { Gateway, Wallets } = require("fabric-network");

// Adjust these paths to your environment if needed
const ccpPath = path.resolve(
  "/home",
  "lucas",
  "fabric",
  "fabric-samples",
  "test-network",
  "organizations",
  "peerOrganizations",
  "org1.example.com",
  "connection-org1.json"
);

const mspId = "Org1MSP";
const adminCertPath = path.resolve(
  "/home",
  "lucas",
  "fabric",
  "fabric-samples",
  "test-network",
  "organizations",
  "peerOrganizations",
  "org1.example.com",
  "users",
  "Admin@org1.example.com",
  "msp",
  "signcerts",
  "cert.pem"
);
const adminKeyDir = path.resolve(
  "/home",
  "lucas",
  "fabric",
  "fabric-samples",
  "test-network",
  "organizations",
  "peerOrganizations",
  "org1.example.com",
  "users",
  "Admin@org1.example.com",
  "msp",
  "keystore"
);

let cachedContract = null;

async function getContract() {
  if (cachedContract) {
    return cachedContract;
  }

  const ccpJSON = fs.readFileSync(ccpPath, "utf8");
  const ccp = JSON.parse(ccpJSON);

  const certificate = fs.readFileSync(adminCertPath, "utf8");
  const keyFiles = fs.readdirSync(adminKeyDir);
  if (!keyFiles || keyFiles.length === 0) {
    throw new Error("No key file found in admin keystore directory");
  }
  const privateKeyPath = path.join(adminKeyDir, keyFiles[0]);
  const privateKey = fs.readFileSync(privateKeyPath, "utf8");

  const wallet = await Wallets.newInMemoryWallet();
  const identity = {
    credentials: {
      certificate,
      privateKey,
    },
    mspId,
    type: "X.509",
  };
  await wallet.put("admin", identity);

  const gateway = new Gateway();
  await gateway.connect(ccp, {
    wallet,
    identity: "admin",
    discovery: { enabled: true, asLocalhost: true },
  });

  const network = await gateway.getNetwork("mychannel");
  const contract = network.getContract("medicalrecords");

  cachedContract = contract;
  return contract;
}

const app = express();
app.use(cors());
app.use(morgan("dev"));
app.use(express.json());

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

// Create patient
app.post("/patients", async (req, res) => {
  try {
    const {
      patientId,
      name,
      dateOfBirth,
      bloodType,
      allergies,
      medications,
      doctorId,
    } = req.body;

    if (!patientId || !name || !dateOfBirth || !bloodType || !doctorId) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const contract = await getContract();
    await contract.submitTransaction(
      "CreatePatient",
      patientId,
      name,
      dateOfBirth,
      bloodType,
      JSON.stringify(allergies || []),
      JSON.stringify(medications || []),
      doctorId
    );

    res.json({ status: "ok", patientId });
  } catch (err) {
    console.error("Error in /patients:", err);
    res.status(500).json({ error: err.message || "Unknown error" });
  }
});

// Read patient
app.get("/patients/:id", async (req, res) => {
  try {
    const contract = await getContract();
    const resultBuffer = await contract.evaluateTransaction(
      "ReadPatient",
      req.params.id
    );
    const resultJson = resultBuffer.toString("utf8");
    const patient = JSON.parse(resultJson);
    res.json(patient);
  } catch (err) {
    console.error("Error in GET /patients/:id:", err);
    res.status(500).json({ error: err.message || "Unknown error" });
  }
});

// Get all patients
app.get("/patients", async (req, res) => {
  try {
    const contract = await getContract();
    const resultBuffer = await contract.evaluateTransaction("GetAllPatients");
    const resultJson = resultBuffer.toString("utf8");
    const patients = JSON.parse(resultJson);
    res.json(patients);
  } catch (err) {
    console.error("Error in GET /patients:", err);
    res.status(500).json({ error: err.message || "Unknown error" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Blockchain gateway listening on port ${PORT}`);
});
