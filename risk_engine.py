import streamlit as st
from llm_engine import analyze_with_ollama, fallback_analysis

st.set_page_config(page_title="XAIAK RiskBrief AI", page_icon="🧠")

st.title("🧠 XAIAK — RiskBrief AI")
st.caption("Structured risk intelligence from unstructured text (Prototype)")

st.subheader("Paste document / instruction / message")

text_input = st.text_area("Input text", height=200)

if st.button("Analyze Risk"):
    if text_input.strip():
        try:
            result = analyze_with_ollama(text_input)
            st.success("Analyzed using local LLM.")
        except Exception:
            result = fallback_analysis(text_input)
            st.warning("Ollama not running. Using fallback risk engine.")

        st.divider()
        st.subheader("Risk Summary")

        st.write("### Summary")
        st.write(result["summary"])

        st.write("### Risk Score")
        st.progress(result["risk_score"] / 100)

        st.write("Severity:", result["severity"].upper())

        st.write("### Identified Risks")
        for r in result["identified_risks"]:
            st.write("-", r)

        st.write("### Recommended Actions")
        for a in result["recommended_actions"]:
            st.write("-", a)

        st.write("Requires Escalation:", result["requires_escalation"])

    else:

        st.warning("Enter text to analyze.")
