# letter_generator.py
# This file generates the Prior Authorization letter
# using the context retrieved by agent.py

import ollama
from datetime import date


# ----------------------------------------
# MAIN FUNCTION: Generate PA Letter
# ----------------------------------------
def generate_pa_letter(agent_result: dict) -> str:
    """
    Takes agent results and generates
    a professional PA letter using Llama 3.2
    """

    # Build the prompt with all retrieved context
    prompt = f"""You are a medical prior authorization 
specialist writing a formal letter.

Generate a complete Prior Authorization Request Letter
using the information below.

PATIENT INFORMATION:
{agent_result['patient_note']}

PROCEDURE REQUESTED:
{agent_result['procedure']}

PRIMARY DIAGNOSIS:
{agent_result['diagnosis']}

INSURANCE PAYER:
{agent_result['payer']}

RETRIEVED PAYER POLICY:
{agent_result['policy_context'][:1500]}

RETRIEVED CLINICAL GUIDELINES:
{agent_result['guideline_context'][:1500]}

PROCEDURE CODES:
{agent_result['code_context']}

SIMILAR PAST PATIENTS (use to strengthen medical necessity):
{agent_result.get('similar_patients', 'None found')[:500]}

ELIGIBILITY ANALYSIS:
{agent_result['eligibility_analysis'][:500]}

Write a formal PA letter with these exact sections:

1. DATE AND HEADER
   - Today's date
   - To: {agent_result['payer']} Prior Authorization Department
   - From: Treating Physician
   - Re: Prior Authorization Request

2. PATIENT INFORMATION
   - Patient name, DOB, diagnosis

3. PROCEDURE REQUESTED
   - Procedure name and CPT/HCPCS code

4. CLINICAL INDICATION
   - Why this procedure is needed
   - Patient symptoms and history

5. MEDICAL NECESSITY JUSTIFICATION
   - Reference clinical guidelines
   - Explain why this is medically necessary

6. PAYER CRITERIA MET
   - List each criteria from payer policy
   - Show how patient meets each one

7. SUPPORTING EVIDENCE
   - Cite specific guidelines retrieved
   - Reference policy sections

8. PROVIDER ATTESTATION
   - Standard closing statement
   - Physician signature line

Make it professional, specific, and cite
the retrieved sources. Use formal medical language."""

    print("✍️ Generating PA letter with Llama 3.2...")
    print("   This takes 1-2 minutes, please wait...")

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    letter = response["message"]["content"]
    print("✅ PA letter generated!")
    return letter


# ----------------------------------------
# SAVE LETTER TO FILE
# ----------------------------------------
def save_letter(letter: str, filename: str = None):
    """
    Saves the generated letter to a text file
    """
    import os
    os.makedirs("output", exist_ok=True)

    if filename is None:
        today = date.today().strftime("%Y%m%d")
        filename = f"output/pa_letter_{today}.txt"

    with open(filename, "w") as f:
        f.write(letter)

    print(f"💾 Letter saved to: {filename}")
    return filename


# ----------------------------------------
# TEST: Run directly to check
# ----------------------------------------
if __name__ == "__main__":
    print("\n🧪 Testing Letter Generator...\n")

    # Import and run agent first
    from agent import run_pa_agent

    # Run agent with test case
    print("🤖 Running PA Agent first...")
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

    # Generate letter
    print("\n✍️ Generating PA Letter...")
    letter = generate_pa_letter(result)

    # Save letter
    saved_path = save_letter(letter)

    # Print letter
    print("\n" + "="*50)
    print("📄 GENERATED PA LETTER")
    print("="*50)
    print(letter)
    print("="*50)
    print(f"\n✅ Letter saved to: {saved_path}")
    print("Next step: app.py")