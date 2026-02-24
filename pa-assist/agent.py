# agent.py
# This is the brain of your RAG system
# It searches ChromaDB and retrieves relevant chunks

import chromadb
from sentence_transformers import SentenceTransformer
import ollama

# ----------------------------------------
# SETUP — Connect to ChromaDB
# ----------------------------------------
print("🔄 Connecting to ChromaDB...")
import chromadb.api
chromadb.api.client.SharedSystemClient.clear_system_cache()
client = chromadb.PersistentClient(path="data/chromadb")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to all 4 collections
policy_col = client.get_collection("payer_policies")
guidelines_col = client.get_collection("clinical_guidelines")
codes_col = client.get_collection("procedure_codes")
patients_col = client.get_collection("patient_notes")
print("✅ Connected to ChromaDB!")


# ----------------------------------------
# TOOL 1: Search Payer Policies
# ----------------------------------------
def search_payer_policy(procedure: str, payer: str) -> str:
    """
    Searches payer policy database
    Returns most relevant policy chunks
    """
    query = f"{payer} prior authorization policy {procedure}"
    embedding = model.encode([query])[0].tolist()

    results = policy_col.query(
        query_embeddings=[embedding],
        n_results=4
    )

    docs = results["documents"][0]
    return "\n---\n".join(docs)


# ----------------------------------------
# TOOL 2: Search Clinical Guidelines
# ----------------------------------------
def search_guidelines(diagnosis: str, procedure: str) -> str:
    """
    Searches clinical guidelines database
    Returns most relevant guideline chunks
    """
    query = f"clinical guideline {diagnosis} {procedure} medical necessity"
    embedding = model.encode([query])[0].tolist()

    results = guidelines_col.query(
        query_embeddings=[embedding],
        n_results=4
    )

    docs = results["documents"][0]
    return "\n---\n".join(docs)


# ----------------------------------------
# TOOL 3: Search Procedure Codes
# ----------------------------------------
def search_procedure_codes(procedure: str) -> str:
    """
    Searches procedure codes database
    Returns matching CPT/HCPCS codes
    """
    query = f"procedure code {procedure}"
    embedding = model.encode([query])[0].tolist()

    results = codes_col.query(
        query_embeddings=[embedding],
        n_results=2
    )

    docs = results["documents"][0]
    return "\n".join(docs)

# TOOL 4: Search Similar Past Patients
def search_similar_patients(diagnosis: str) -> str:
    query = f"patient {diagnosis} history medications"
    embedding = model.encode([query])[0].tolist()
    results = patients_col.query(
        query_embeddings=[embedding],
        n_results=2
    )
    docs = results["documents"][0]
    return "\n---\n".join(docs)

# ----------------------------------------
# AGENT ROUTER
# LLM decides which tool to use
# ----------------------------------------
def route_query(query: str) -> str:
    """
    Sends query to Llama 3.2
    LLM decides which database to search
    Returns: FDA, PUBMED, or BOTH
    """
    router_prompt = f"""You are a medical prior authorization router.
Given this query: "{query}"

Which database should be searched? Reply with ONLY one word:
- POLICY (for payer rules, coverage criteria, prior auth requirements)
- GUIDELINES (for clinical evidence, medical necessity, treatment protocols)
- BOTH (if query needs both payer policy AND clinical guidelines)

Reply with ONLY one word."""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": router_prompt}]
    )

    decision = response["message"]["content"].strip().upper()

    # Clean up response to get just the keyword
    if "POLICY" in decision:
        return "POLICY"
    elif "GUIDELINES" in decision:
        return "GUIDELINES"
    else:
        return "BOTH"


# ----------------------------------------
# ELIGIBILITY CHECKER
# ----------------------------------------
def check_eligibility(
    patient_info: str,
    policy_text: str,
    procedure: str
) -> str:
    """
    Checks if patient meets payer criteria
    Returns eligibility analysis
    """
    prompt = f"""You are a prior authorization specialist.
Review if this patient meets the payer criteria for {procedure}.

Patient Information:
{patient_info}

Payer Policy:
{policy_text}

Provide:
1. Criteria MET by this patient
2. Criteria NOT MET or missing
3. Overall: LIKELY APPROVED / NEEDS MORE INFO / LIKELY DENIED

Be specific and cite the policy text."""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ----------------------------------------
# MAIN PA AGENT
# This is what app.py will call
# ----------------------------------------
def run_pa_agent(
    patient_note: str,
    procedure: str,
    diagnosis: str,
    payer: str
) -> dict:
    """
    Main function that runs the full PA agent
    Returns all results as a dictionary
    """

    print(f"\n🤖 PA Agent Starting...")
    print(f"   Patient: {patient_note[:50]}...")
    print(f"   Procedure: {procedure}")
    print(f"   Diagnosis: {diagnosis}")
    print(f"   Payer: {payer}")

    # Step 1: Route the query
    print(f"\n🧭 Routing query...")
    query = f"{payer} prior authorization {procedure} {diagnosis}"
    decision = route_query(query)
    print(f"   Decision: {decision}")

    # Step 2: Search relevant databases
    policy_context = ""
    guideline_context = ""
    sources_used = []

    if decision in ["POLICY", "BOTH"]:
        print(f"\n🔍 Searching payer policies...")
        policy_context = search_payer_policy(procedure, payer)
        sources_used.append("Payer Policy Database")
        print(f"   ✅ Found relevant policy chunks")

    if decision in ["GUIDELINES", "BOTH"]:
        print(f"\n📚 Searching clinical guidelines...")
        guideline_context = search_guidelines(diagnosis, procedure)
        sources_used.append("Clinical Guidelines Database")
        print(f"   ✅ Found relevant guideline chunks")

    # Always search procedure codes
    print(f"\n💊 Searching procedure codes...")
    code_context = search_procedure_codes(procedure)
    print(f"   ✅ Found procedure codes")

    # Step 3: Search similar past patients
    print(f"\n👥 Searching similar patients...")
    similar_patients = search_similar_patients(diagnosis)
    sources_used.append("Patient Records Database")
    print(f"   ✅ Found similar patient records")


    # Step 4: Check eligibility
    print(f"\n⚖️ Checking eligibility...")
    eligibility = check_eligibility(
        patient_note,
        policy_context,
        procedure
    )
    print(f"   ✅ Eligibility analysis complete")

    print(f"\n✅ PA Agent Complete!")

    return {
        "patient_note": patient_note,
        "procedure": procedure,
        "diagnosis": diagnosis,
        "payer": payer,
        "routing_decision": decision,
        "policy_context": policy_context,
        "guideline_context": guideline_context,
        "similar_patients": similar_patients,
        "code_context": code_context,
        "eligibility_analysis": eligibility,
        "sources_used": sources_used
    }


# ----------------------------------------
# TEST: Run directly to check
# ----------------------------------------
if __name__ == "__main__":
    print("\n🧪 Testing PA Agent...\n")

    # Test case
    result = run_pa_agent(
        patient_note="""Patient: John Doe, 54M
Diagnosis: Type 2 Diabetes Mellitus
HbA1c: 9.2% (poorly controlled)
Current medications: Metformin 1000mg twice daily
Doctor notes: Patient requires CGM for better
glycemic control. Multiple hypoglycemic episodes.""",
        procedure="Continuous Glucose Monitor (CGM)",
        diagnosis="Type 2 Diabetes",
        payer="Medicare"
    )

    print("\n" + "="*50)
    print("📊 AGENT RESULTS")
    print("="*50)
    print(f"Routing Decision : {result['routing_decision']}")
    print(f"Sources Used     : {result['sources_used']}")
    print(f"\n⚖️ ELIGIBILITY ANALYSIS:")
    print(result['eligibility_analysis'])
    print("\n✅ Agent test complete!")
    print("Next step: letter_generator.py")