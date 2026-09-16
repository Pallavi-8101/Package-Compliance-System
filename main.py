import os
import uuid
import json

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from models import Inspection

from services.ocr_service import extract_text
from services.extraction_service import extract_information
from services.compliance_service import check_compliance


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Verishield",
    description="Automated Compliance Checking for Pre-Packaged Commodities",
    version="1.0.0"
)


# Allow React frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():

    return {
        "message": "Verishield Backend is running",
        "status": "online"
    }


@app.get("/api/health")
def health():

    return {
        "status": "online",
        "service": "Verishield"
    }


@app.post("/api/inspect")
async def inspect_package(file: UploadFile = File(...)):

    # Generate unique filename
    extension = os.path.splitext(file.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    image_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Save uploaded image
    contents = await file.read()

    with open(image_path, "wb") as buffer:
        buffer.write(contents)

    # -------------------------
    # STEP 1: OCR
    # -------------------------

    extracted_text = extract_text(image_path)

    # -------------------------
    # STEP 2: INFORMATION EXTRACTION
    # -------------------------

    information = extract_information(
        extracted_text
    )

    # -------------------------
    # STEP 3: COMPLIANCE CHECK
    # -------------------------

    compliance = check_compliance(
        information
    )

    # -------------------------
    # STEP 4: SAVE INSPECTION
    # -------------------------

    db = SessionLocal()

    inspection = Inspection(
        product_name=information["product_name"],
        category="General",
        mrp=information["mrp"],
        net_quantity=information["net_quantity"],
        manufacturer=information["manufacturer"],
        address=information["address"],
        date_info=information["date_info"],
        consumer_care=information["consumer_care"],
        compliance_score=compliance["score"],
        status=compliance["status"],
        violations=json.dumps(
            compliance["violations"]
        ),
        extracted_text="\n".join(
            extracted_text
        )
    )

    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    db.close()

    return {
        "inspection_id": inspection.id,
        "information": information,
        "extracted_text": extracted_text,
        "compliance": compliance
    }


@app.get("/api/inspections")
def get_inspections():

    db = SessionLocal()

    inspections = (
        db.query(Inspection)
        .order_by(Inspection.id.desc())
        .all()
    )

    result = []

    for inspection in inspections:

        result.append({
            "id": inspection.id,
            "product_name": inspection.product_name,
            "category": inspection.category,
            "score": inspection.compliance_score,
            "status": inspection.status
        })

    db.close()

    return result