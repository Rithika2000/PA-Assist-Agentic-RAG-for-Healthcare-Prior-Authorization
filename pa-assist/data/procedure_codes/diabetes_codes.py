# Run this once to create your procedure codes reference
# save as: data/procedure_codes/create_codes.py

import json, os

os.makedirs("pa-assist/data/procedure_codes", exist_ok=True)

diabetes_procedure_codes = [
    {"code": "95251", "type": "CPT",
     "description": "Continuous Glucose Monitor (CGM) — Ambulatory",
     "category": "Diabetes Monitoring"},

    {"code": "E0787", "type": "HCPCS",
     "description": "Insulin Infusion Pump — External",
     "category": "Insulin Delivery"},

    {"code": "A9276", "type": "HCPCS",
     "description": "CGM Sensor — each",
     "category": "Diabetes Monitoring"},

    {"code": "A9277", "type": "HCPCS",
     "description": "CGM Transmitter — each",
     "category": "Diabetes Monitoring"},

    {"code": "A9278", "type": "HCPCS",
     "description": "CGM Receiver — each",
     "category": "Diabetes Monitoring"},

    {"code": "99213", "type": "CPT",
     "description": "Office Visit — Established Patient, Low Complexity",
     "category": "Office Visit"},

    {"code": "99214", "type": "CPT",
     "description": "Office Visit — Established Patient, Moderate Complexity",
     "category": "Office Visit"},

    {"code": "83036", "type": "CPT",
     "description": "HbA1c Blood Test",
     "category": "Lab Test"},

    {"code": "82947", "type": "CPT",
     "description": "Glucose Blood Test — Quantitative",
     "category": "Lab Test"},

    {"code": "E0784", "type": "HCPCS",
     "description": "External Ambulatory Insulin Infusion Pump",
     "category": "Insulin Delivery"},

    {"code": "S1034", "type": "HCPCS",
     "description": "Artificial Pancreas Device System",
     "category": "Advanced Diabetes Tech"},

    {"code": "99490", "type": "CPT",
     "description": "Chronic Care Management — 20 minutes/month",
     "category": "Care Management"},
]

with open("pa-assist/data/procedure_codes/diabetes_codes.json", "w") as f:
    json.dump(diabetes_procedure_codes, f, indent=2)

print(f"Created {len(diabetes_procedure_codes)} procedure codes")
