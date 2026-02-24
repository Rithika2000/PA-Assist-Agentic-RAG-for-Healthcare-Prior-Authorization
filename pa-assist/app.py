# app.py
# This is the website UI for your PA Agent
# Run with: streamlit run app.py

import streamlit as st
from agent import run_pa_agent
from letter_generator import generate_pa_letter, save_letter

# ----------------------------------------
# PAGE SETUP
# ----------------------------------------
st.set_page_config(
    page_title="PA-Assist | Prior Auth Agent",
    page_icon="🏥",
    layout="wide"
)

# ----------------------------------------
# HEADER
# ----------------------------------------
st.title("🏥 PA-Assist: Prior Authorization Agent")
st.caption(
    "Automates Prior Authorization letters using "
    "Payer Policies + Clinical Guidelines | "
    "Powered by Llama 3.2 + RAG"
)

# Disclaimer
st.warning(
    "⚠️ DISCLAIMER: This is a portfolio/research "
    "project for educational purposes only. NOT "
    "intended for real clinical use."
)

st.divider()

# ----------------------------------------
# SIDEBAR
# ----------------------------------------
with st.sidebar:
    st.header("📊 System Status")
    st.success("✅ Payer Policy DB: Active")
    st.success("✅ Clinical Guidelines DB: Active")
    st.success("✅ Llama 3.2: Running Locally")
    st.success("✅ ChromaDB: Connected")

    st.divider()

    st.header("📚 Knowledge Base")
    st.info("🏥 Disease Focus: Diabetes")
    st.info("💊 Procedures: CGM, Insulin Pump")
    st.info("🏦 Payers: Medicare, Medicaid, UHC")

    st.divider()

    st.caption("🔒 100% Local — No data leaves your Mac")
    st.caption("Built with LangChain + ChromaDB + Ollama")

# ----------------------------------------
# SAMPLE CASES BUTTONS
# ----------------------------------------
st.subheader("💡 Try a Sample Case:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🩸 Diabetes CGM", use_container_width=True):
        st.session_state["patient_note"] = """Patient: John Doe, 54M
Diagnosis: Type 2 Diabetes Mellitus
HbA1c: 9.2% (poorly controlled)
Current medications: Metformin 1000mg twice daily
Doctor notes: Patient requires CGM for better
glycemic control. Multiple hypoglycemic episodes."""
        st.session_state["procedure"] = \
            "Continuous Glucose Monitor (CGM)"
        st.session_state["diagnosis"] = "Type 2 Diabetes"
        st.session_state["payer"] = "Medicare"

with col2:
    if st.button("💉 Insulin Pump", use_container_width=True):
        st.session_state["patient_note"] = """Patient: Jane Smith, 32F
Diagnosis: Type 1 Diabetes Mellitus
HbA1c: 8.8% (uncontrolled)
Current medications: Multiple daily insulin injections
Doctor notes: Patient requires insulin pump for
better glycemic control. Frequent hypoglycemia."""
        st.session_state["procedure"] = \
            "Insulin Pump Therapy"
        st.session_state["diagnosis"] = "Type 1 Diabetes"
        st.session_state["payer"] = "Medicaid"

with col3:
    if st.button("🔬 HbA1c Test", use_container_width=True):
        st.session_state["patient_note"] = """Patient: Bob Johnson, 61M
Diagnosis: Type 2 Diabetes Mellitus
Last HbA1c: 10.1% (3 months ago)
Current medications: Glipizide 5mg daily
Doctor notes: Requires HbA1c monitoring
every 3 months per ADA guidelines."""
        st.session_state["procedure"] = \
            "HbA1c Blood Test"
        st.session_state["diagnosis"] = "Type 2 Diabetes"
        st.session_state["payer"] = "UnitedHealthcare"

st.divider()

# ----------------------------------------
# INPUT FORM
# ----------------------------------------
st.subheader("📋 Enter Patient Information")

col1, col2 = st.columns(2)

with col1:
    payer = st.selectbox(
        "Insurance Payer",
        ["Medicare", "Medicaid",
         "UnitedHealthcare", "Aetna", "Cigna"],
        index=["Medicare", "Medicaid",
               "UnitedHealthcare", "Aetna",
               "Cigna"].index(
            st.session_state.get("payer", "Medicare")
        )
    )

    procedure = st.text_input(
        "Procedure Requested",
        value=st.session_state.get("procedure", ""),
        placeholder="e.g. Continuous Glucose Monitor"
    )

    diagnosis = st.text_input(
        "Primary Diagnosis",
        value=st.session_state.get("diagnosis", ""),
        placeholder="e.g. Type 2 Diabetes"
    )

with col2:
    patient_note = st.text_area(
        "Clinical Note",
        value=st.session_state.get("patient_note", ""),
        height=200,
        placeholder="""Patient: Name, Age/Gender
Diagnosis: 
Current medications: 
Doctor notes: """
    )

# ----------------------------------------
# GENERATE BUTTON
# ----------------------------------------
st.divider()

generate_btn = st.button(
    "🚀 Generate Prior Authorization Letter",
    type="primary",
    use_container_width=True
)

if generate_btn:
    # Validate inputs
    if not all([patient_note, procedure, diagnosis, payer]):
        st.error("❌ Please fill in all fields!")
    else:
        # Run Agent
        with st.spinner(
            "🤖 Agent searching payer policies "
            "and guidelines..."
        ):
            result = run_pa_agent(
                patient_note=patient_note,
                procedure=procedure,
                diagnosis=diagnosis,
                payer=payer
            )

        # Generate Letter
        with st.spinner(
            "✍️ Generating PA letter with Llama 3.2..."
        ):
            letter = generate_pa_letter(result)

        # Save letter
        saved_path = save_letter(letter)

        st.success("✅ Prior Authorization Letter Generated!")

        # ----------------------------------------
        # RESULTS TABS
        # ----------------------------------------
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 PA Letter",
            "⚖️ Eligibility Analysis",
            "🧭 Agent Routing",
            "🔎 Retrieved Sources"
        ])

        with tab1:
            st.subheader("Generated Prior Authorization Letter")
            st.text_area(
                "",
                letter,
                height=600
            )
            # Download button
            st.download_button(
                label="📥 Download Letter as TXT",
                data=letter,
                file_name="prior_auth_letter.txt",
                mime="text/plain",
                use_container_width=True
            )

        with tab2:
            st.subheader("Eligibility Analysis")
            st.write(result["eligibility_analysis"])

        with tab3:
            st.subheader("Agent Routing Decision")
            st.info(
                f"🧭 Agent routed to: "
                f"**{result['routing_decision']}**"
            )
            st.write("**Sources Used:**")
            for source in result["sources_used"]:
                st.success(f"✅ {source}")

        with tab4:
            with st.expander("📋 Payer Policy Retrieved"):
                st.text(result["policy_context"])
            with st.expander("📚 Guidelines Retrieved"):
                st.text(result["guideline_context"])
            with st.expander("💊 Procedure Codes"):
                st.text(result["code_context"])
            with st.expander("👥 Similar Past Patients"):
                 st.text(result.get("similar_patients", "None found"))