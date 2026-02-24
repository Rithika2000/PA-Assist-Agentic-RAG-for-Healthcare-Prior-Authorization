# PA-Assist-Agentic-RAG-for-Healthcare-Prior-Authorization

---

## ⚠️ Disclaimer

This project is built for **educational and portfolio 
purposes only.**

- NOT intended for real clinical use
- NOT a substitute for medical advice
- NOT approved for actual prior authorization decisions
- NOT validated for production healthcare environments
- All patient data is 100% synthetic (Synthea)
- No real PHI was used at any point
- Payer policies used are publicly available documents

> Any resemblance to real patients is purely coincidental.
> Always consult a licensed healthcare professional for 
> medical decisions. Prior authorization decisions should 
> always be made by qualified medical and administrative 
> professionals.

---

### Automating Healthcare's $350B Administrative Problem

> An agentic RAG system that generates evidence-backed 
> Prior Authorization letters in minutes by retrieving 
> payer-specific policies and clinical guidelines —
> the same workflow being deployed at UnitedHealth, 
> Aetna and Cigna.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Ollama](https://img.shields.io/badge/LLM-Llama3.2-green)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange)
![LangChain](https://img.shields.io/badge/Framework-LangChain-yellow)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![HIPAA](https://img.shields.io/badge/Design-HIPAA_Conscious-purple)

---

## 🎥 Demo

> Add your demo GIF here after recording
> ![Demo](assets/demo.gif)

---

## Problem

Physicians handle **43 prior authorizations weekly.**
Each one requires:
- Manually searching payer-specific policy documents
- Cross-referencing clinical guidelines
- Writing a formal justification letter
- Waiting days for approval decisions

This costs the US healthcare system **$350B annually**
in administrative overhead.

**PA-Assist solves this in minutes, not days.**

---

## Solution

Input a patient clinical note + procedure → 
PA-Assist autonomously:

1. **Routes** the query to the right knowledge base
2. **Retrieves** matching payer policy chunks
3. **Retrieves** supporting clinical guidelines
4. **Checks** patient eligibility against policy criteria
5. **Generates** a complete, cited PA letter

---

## 🏗️ Architecture
```
Patient Note + Procedure + Payer
              ↓
      Agentic Router (Llama 3.2)
              ↓
    ┌─────────────────────┐
    │   ChromaDB Search   │
    ├──────────┬──────────┤
    │  Payer   │Clinical  │
    │ Policies │Guidelines│
    └──────────┴──────────┘
              ↓
     Eligibility Checker
              ↓
    PA Letter Generator
              ↓
    Professional PA Letter
    (with citations + codes)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Llama 3.2 via Ollama (100% local) |
| Embeddings | all-MiniLM-L6-v2 (HuggingFace) |
| Vector DB | ChromaDB (persistent) |
| Agent Framework | LangChain |
| UI | Streamlit |
| Evaluation | Custom criteria-based framework |
| Patient Data | Synthea (synthetic, no PHI) |

---

## Knowledge Base

| Dataset | Source | Chunks |
|---------|--------|--------|
| Payer Policies | CMS, UHC, Medicaid (public PDFs) | 405 |
| Clinical Guidelines | ADA, CMS guidelines | 131 |
| Procedure Codes | CPT/HCPCS diabetes codes | 12 |
| Patient Records | Synthea synthetic EHR | 35 |
| **Total** | | **583** |

---

## Evaluation

Tested across 5 prior authorization scenarios:
- CGM requests for Type 2 Diabetes
- Insulin Pump for Type 1 Diabetes  
- HbA1c monitoring tests

Across 4 payers: Medicare, Medicaid, 
UnitedHealthcare, Aetna

**All 5 generated letters contained:**
- Correct CPT/HCPCS procedure codes
- Payer-specific policy citations
- ADA/CMS guideline references
- Complete 8-section letter structure
- Medical necessity justification

> Evaluated using custom criteria-based framework
> checking CPT codes, policy citations, guideline
> references and letter structure completeness.

---

## Industry Relevance

This system mirrors production deployments at:

| Company | Use Case |
|---------|----------|
| **Cohere Health** | PA automation platform |
| **Availity** | Health information network |
| **Waystar** | Revenue cycle AI |
| **Optum (UnitedHealth)** | PA AI internally |
| **Epic Systems** | EHR-integrated PA AI |

---

## Quickstart

### Prerequisites
- Mac/Linux
- Python 3.11+
- Ollama installed → https://ollama.ai

### Installation
```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/pa-assist
cd pa-assist

# 2. Install dependencies
python3.11 -m pip install -r requirements.txt

# 3. Pull Llama 3.2
ollama pull llama3.2

# 4. Add your data files to:
# data/payer_policies/  → payer PDF files
# data/guidelines/      → clinical guideline PDFs
# data/patient_notes/   → Synthea JSON files

# 5. Run data pipeline
python3.11 ingest.py
python3.11 embed.py

# 6. Launch app
streamlit run app.py
```

---

## Project Structure
```
pa-assist/
├── data/
│   ├── payer_policies/     # CMS, UHC, Medicaid PDFs
│   ├── guidelines/         # ADA, CMS guideline PDFs
│   ├── patient_notes/      # Synthea FHIR JSON files
│   ├── procedure_codes/    # CPT/HCPCS diabetes codes
│   └── chromadb/           # Vector store (auto-created)
├── output/                 # Generated PA letters
├── ingest.py               # Data loading + chunking
├── embed.py                # Embedding + ChromaDB storage
├── agent.py                # Agentic RAG core
├── letter_generator.py     # PA letter generation
├── evaluate.py             # Evaluation framework
├── app.py                  # Streamlit UI
└── requirements.txt
```

---

## HIPAA Considerations

- **100% local** — Llama 3.2 runs via Ollama on your machine
- **No data transmission** — zero patient data leaves your machine
- **Synthetic patients only** — Synthea generated, no real PHI
- **Public data only** — payer policies from official public sources

---

## Disclaimer

This is a **portfolio/research project** for educational 
purposes only. It is NOT intended for clinical use, does 
not constitute medical advice, and should not be used for 
actual patient care or real prior authorization decisions.
All patient data is fully synthetic (Synthea).

---

## Author

Built by **[Your Name]**

Open to AI/ML Engineering roles in Healthcare AI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/YOUR_USERNAME)

---

## 📄 License

MIT License — free to use and modify
```

---

## 🐢 Step 3 — Update Your Details

Find and replace these 3 things:
```
YOUR_USERNAME  → your GitHub username
YOUR_PROFILE   → your LinkedIn profile URL
[Your Name]    → your actual name
```

Press **`Cmd + S`**

---

## 🐢 Step 4 — Create requirements.txt

Open `requirements.txt` and paste:
```
langchain
langchain-community
langchain-text-splitters
chromadb
sentence-transformers
streamlit
ragas
datasets
requests
pypdf
ollama
pandas
openpyxl
```

Press **`Cmd + S`**

---

## Your Repo Is Now Complete
```
pa-assist/
├── ingest.py          
├── embed.py           
├── agent.py           
├── letter_generator.py 
├── evaluate.py        
├── app.py             
├── requirements.txt   
├── README.md          
└── data/              
