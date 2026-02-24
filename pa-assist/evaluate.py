# evaluate.py
# Manual evaluation of PA-Assist RAG system
# Scores: Faithfulness + Relevancy (manually calculated)

import json
import os
from agent import run_pa_agent
from letter_generator import generate_pa_letter

# ----------------------------------------
# TEST CASES
# ----------------------------------------
test_cases = [
    {
        "patient_note": """Patient: John Doe, 54M
Diagnosis: Type 2 Diabetes Mellitus
HbA1c: 9.2% poorly controlled
Current medications: Metformin 1000mg twice daily
Multiple hypoglycemic episodes reported.""",
        "procedure": "Continuous Glucose Monitor CGM",
        "diagnosis": "Type 2 Diabetes",
        "payer": "Medicare"
    },
    {
        "patient_note": """Patient: Jane Smith, 32F
Diagnosis: Type 1 Diabetes Mellitus
HbA1c: 8.8% uncontrolled
Current medications: Multiple daily insulin injections
Frequent hypoglycemia episodes.""",
        "procedure": "Insulin Pump Therapy",
        "diagnosis": "Type 1 Diabetes",
        "payer": "Medicaid"
    },
    {
        "patient_note": """Patient: Bob Johnson, 61M
Diagnosis: Type 2 Diabetes Mellitus
Last HbA1c: 10.1% three months ago
Current medications: Glipizide 5mg daily
Requires quarterly monitoring.""",
        "procedure": "HbA1c Blood Test",
        "diagnosis": "Type 2 Diabetes",
        "payer": "UnitedHealthcare"
    },
    {
        "patient_note": """Patient: Mary Wilson, 45F
Diagnosis: Type 2 Diabetes Mellitus
HbA1c: 8.5% poorly controlled
Current medications: Metformin + Sitagliptin
Doctor recommends CGM for better management.""",
        "procedure": "Continuous Glucose Monitor CGM",
        "diagnosis": "Type 2 Diabetes",
        "payer": "Aetna"
    },
    {
        "patient_note": """Patient: David Brown, 58M
Diagnosis: Type 1 Diabetes Mellitus
HbA1c: 9.5% very poorly controlled
Current medications: Insulin injections 4x daily
Multiple emergency hypoglycemia episodes.""",
        "procedure": "Insulin Pump Therapy",
        "diagnosis": "Type 1 Diabetes",
        "payer": "Medicare"
    }
]

# ----------------------------------------
# EVALUATION CRITERIA
# ----------------------------------------
def evaluate_letter(letter: str, result: dict) -> dict:
    """
    Manually checks if letter meets quality criteria
    Returns scores for each criterion
    """
    scores = {}
    letter_lower = letter.lower()

    # ---- FAITHFULNESS CHECKS ----
    # Is the answer grounded in retrieved sources?
    faithfulness_checks = {
        "contains_procedure_code": any(
            code in letter
            for code in ["95251", "E0787", "E0784",
                        "83036", "A9276", "A9277"]
        ),
        "cites_policy_source": any(
            word in letter_lower
            for word in ["medicare", "medicaid",
                        "unitedhealth", "aetna", "cms"]
        ),
        "cites_guidelines": any(
            word in letter_lower
            for word in ["ada", "american diabetes",
                        "standards of care", "guidelines"]
        ),
        "contains_patient_info": any(
            word in letter_lower
            for word in ["hba1c", "diabetes",
                        "insulin", "glucose"]
        ),
        "has_medical_necessity": (
            "medical necessity" in letter_lower or
            "medically necessary" in letter_lower
        )
    }

    # ---- RELEVANCY CHECKS ----
    # Is the letter relevant to the PA request?
    relevancy_checks = {
        "has_all_sections": all(
            section in letter_lower
            for section in [
                "patient", "procedure",
                "clinical", "provider"
            ]
        ),
        "mentions_procedure": (
            result["procedure"].lower()[:10]
            in letter_lower
        ),
        "mentions_payer": (
            result["payer"].lower()
            in letter_lower
        ),
        "has_attestation": (
            "attest" in letter_lower or
            "certify" in letter_lower or
            "signature" in letter_lower
        ),
        "has_diagnosis": (
            result["diagnosis"].lower()[:8]
            in letter_lower
        )
    }

    # Calculate scores
    faith_passed = sum(faithfulness_checks.values())
    faith_total = len(faithfulness_checks)
    faith_score = round(faith_passed / faith_total, 2)

    relev_passed = sum(relevancy_checks.values())
    relev_total = len(relevancy_checks)
    relev_score = round(relev_passed / relev_total, 2)

    scores["faithfulness"] = faith_score
    scores["relevancy"] = relev_score
    scores["faithfulness_details"] = faithfulness_checks
    scores["relevancy_details"] = relevancy_checks

    return scores


# ----------------------------------------
# RUN EVALUATION
# ----------------------------------------
def run_evaluation():
    print("\n🧪 Starting Manual Evaluation...")
    print(f"   Running {len(test_cases)} test cases")
    print("=" * 50)

    all_faithfulness = []
    all_relevancy = []
    results_log = []

    for i, case in enumerate(test_cases):
        print(f"\n📋 Test Case {i+1}/{len(test_cases)}")
        print(f"   Procedure : {case['procedure']}")
        print(f"   Payer     : {case['payer']}")

        try:
            # Run agent
            print(f"   🤖 Running agent...")
            result = run_pa_agent(
                patient_note=case["patient_note"],
                procedure=case["procedure"],
                diagnosis=case["diagnosis"],
                payer=case["payer"]
            )

            # Generate letter
            print(f"   ✍️ Generating letter...")
            letter = generate_pa_letter(result)

            # Evaluate
            scores = evaluate_letter(letter, case)
            all_faithfulness.append(
                scores["faithfulness"]
            )
            all_relevancy.append(scores["relevancy"])

            print(
                f"   📊 Faithfulness : "
                f"{scores['faithfulness']}"
            )
            print(
                f"   📊 Relevancy    : "
                f"{scores['relevancy']}"
            )
            print(f"   ✅ Test case {i+1} complete!")

            results_log.append({
                "test_case": i + 1,
                "procedure": case["procedure"],
                "payer": case["payer"],
                "faithfulness": scores["faithfulness"],
                "relevancy": scores["relevancy"],
                "details": {
                    "faithfulness": scores[
                        "faithfulness_details"
                    ],
                    "relevancy": scores[
                        "relevancy_details"
                    ]
                }
            })

        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    # ----------------------------------------
    # FINAL SCORES
    # ----------------------------------------
    if not all_faithfulness:
        print("❌ No test cases completed!")
        return

    avg_faithfulness = round(
        sum(all_faithfulness) / len(all_faithfulness), 2
    )
    avg_relevancy = round(
        sum(all_relevancy) / len(all_relevancy), 2
    )

    print("\n" + "=" * 50)
    print("🏆 EVALUATION RESULTS")
    print("=" * 50)
    print(f"""
┌─────────────────────────────────┐
│     PA-ASSIST EVAL SCORES       │
├─────────────────────────────────┤
│ Faithfulness     : {avg_faithfulness}          │
│ Answer Relevancy : {avg_relevancy}          │
│ Test Cases       : {len(all_faithfulness)}             │
│ Model            : Llama 3.2    │
│ Embeddings       : MiniLM-L6-v2 │
└─────────────────────────────────┘""")

    # Interpretation
    print("\n📈 Score Interpretation:")
    if avg_faithfulness >= 0.80:
        print(
            f"   Faithfulness {avg_faithfulness}"
            f" → ✅ EXCELLENT"
        )
    elif avg_faithfulness >= 0.60:
        print(
            f"   Faithfulness {avg_faithfulness}"
            f" → ⚠️ GOOD"
        )
    else:
        print(
            f"   Faithfulness {avg_faithfulness}"
            f" → ❌ NEEDS IMPROVEMENT"
        )

    if avg_relevancy >= 0.80:
        print(
            f"   Relevancy {avg_relevancy}"
            f" → ✅ EXCELLENT"
        )
    elif avg_relevancy >= 0.60:
        print(
            f"   Relevancy {avg_relevancy}"
            f" → ⚠️ GOOD"
        )
    else:
        print(
            f"   Relevancy {avg_relevancy}"
            f" → ❌ NEEDS IMPROVEMENT"
        )

    # Save results
    os.makedirs("output", exist_ok=True)
    final_results = {
        "faithfulness": avg_faithfulness,
        "answer_relevancy": avg_relevancy,
        "test_cases": len(all_faithfulness),
        "model": "llama3.2",
        "embedding_model": "all-MiniLM-L6-v2",
        "evaluation_method": "manual_criteria_based",
        "detailed_results": results_log
    }

    with open("output/ragas_scores.json", "w") as f:
        json.dump(final_results, f, indent=2)

    print(
        f"\n💾 Scores saved to: output/ragas_scores.json"
    )
    print("\n✅ Evaluation Complete!")
    print("\n🎯 Add these scores to your README:")
    print(f"""
| Metric            | Score              |
|-------------------|--------------------|
| Faithfulness      | {avg_faithfulness} |
| Answer Relevancy  | {avg_relevancy}    |
| Test Cases        | {len(all_faithfulness)}    |
| LLM               | Llama 3.2          |
| Embedding Model   | all-MiniLM-L6-v2   |
""")
    return final_results


# ----------------------------------------
# RUN
# ----------------------------------------
if __name__ == "__main__":
    run_evaluation()