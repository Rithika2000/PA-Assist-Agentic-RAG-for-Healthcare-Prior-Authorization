# ingest.py
# This file reads all your PDFs and JSON files
# and breaks them into small text chunks

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import os
import glob


# ----------------------------------------
# FUNCTION 1: Load Payer Policy PDFs
# ----------------------------------------
def load_payer_policies():
    chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )

    pdf_files = glob.glob("data/payer_policies/*.pdf")

    if not pdf_files:
        print("❌ No PDFs found in data/payer_policies/")
        return chunks

    for pdf_path in pdf_files:
        print(f"   Loading: {os.path.basename(pdf_path)}")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        splits = splitter.split_documents(pages)

        for split in splits:
            split.metadata["source_type"] = "payer_policy"
            split.metadata["filename"] = os.path.basename(pdf_path)

        chunks.extend(splits)

    print(f"✅ Loaded {len(chunks)} chunks from payer policies")
    return chunks


# ----------------------------------------
# FUNCTION 2: Load Clinical Guideline PDFs
# ----------------------------------------
def load_guidelines():
    chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    pdf_files = glob.glob("data/guidelines/*.pdf")

    if not pdf_files:
        print("❌ No PDFs found in data/guidelines/")
        return chunks

    for pdf_path in pdf_files:
        print(f"   Loading: {os.path.basename(pdf_path)}")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        splits = splitter.split_documents(pages)

        for split in splits:
            split.metadata["source_type"] = "clinical_guideline"
            split.metadata["filename"] = os.path.basename(pdf_path)

        chunks.extend(splits)

    print(f"✅ Loaded {len(chunks)} chunks from guidelines")
    return chunks


# ----------------------------------------
# FUNCTION 3: Load Procedure Codes JSON
# ----------------------------------------
def load_procedure_codes():
    chunks = []
    filepath = "data/procedure_codes/diabetes_codes.json"

    if not os.path.exists(filepath):
        print("❌ diabetes_codes.json not found!")
        return chunks

    with open(filepath) as f:
        codes = json.load(f)

    for code in codes:
        text = f"Procedure Code: {code['code']} ({code['type']})\n"
        text += f"Description: {code['description']}\n"
        text += f"Category: {code['category']}"

        chunks.append({
            "text": text,
            "source_type": "procedure_code",
            "code": code["code"]
        })

    print(f"✅ Loaded {len(chunks)} procedure codes")
    return chunks


# ----------------------------------------
# FUNCTION 4: Load Synthea Patient Notes
# ----------------------------------------
def load_patient_notes(limit=50):
    patients = []
    json_files = glob.glob("data/patient_notes/fhir/*.json")[:limit]

    if not json_files:
        print("❌ No JSON files found in data/patient_notes/fhir")
        return patients

    for json_path in json_files:
        with open(json_path) as f:
            try:
                data = json.load(f)
            except:
                continue

        summary = extract_patient_summary(data)
        if summary:
            patients.append({
                "text": summary,
                "source_type": "patient_record",
                "filename": os.path.basename(json_path)
            })

    print(f"✅ Loaded {len(patients)} patient records")
    return patients


def extract_patient_summary(fhir_bundle):
    parts = []

    for entry in fhir_bundle.get("entry", []):
        resource = entry.get("resource", {})
        rtype = resource.get("resourceType", "")

        if rtype == "Patient":
            name = resource.get("name", [{}])[0]
            first = name.get("given", ["Unknown"])[0]
            last = name.get("family", "Unknown")
            gender = resource.get("gender", "unknown")
            birth = resource.get("birthDate", "unknown")
            parts.append(
                f"Patient: {first} {last}, "
                f"{gender}, DOB: {birth}"
            )

        elif rtype == "Condition":
            code = resource.get("code", {})
            condition = code.get("text", "")
            if condition:
                parts.append(f"Condition: {condition}")

        elif rtype == "MedicationRequest":
            med = resource.get(
                "medicationCodeableConcept", {}
            )
            medication = med.get("text", "")
            if medication:
                parts.append(f"Medication: {medication}")

    return "\n".join(parts) if parts else None


# ----------------------------------------
# RUN THIS FILE TO TEST
# ----------------------------------------
if __name__ == "__main__":
    print("\n🔄 Loading all datasets...\n")

    print("📋 Payer Policies:")
    policies = load_payer_policies()

    print("\n📚 Clinical Guidelines:")
    guidelines = load_guidelines()

    print("\n💊 Procedure Codes:")
    codes = load_procedure_codes()

    print("\n👤 Patient Notes:")
    patients = load_patient_notes()

    print("\n" + "="*50)
    print(f"📊 TOTAL SUMMARY:")
    print(f"   Payer Policy Chunks : {len(policies)}")
    print(f"   Guideline Chunks    : {len(guidelines)}")
    print(f"   Procedure Codes     : {len(codes)}")
    print(f"   Patient Records     : {len(patients)}")
    print("="*50)
    print("\n✅ All datasets loaded successfully!")