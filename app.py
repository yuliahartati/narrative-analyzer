import json
import streamlit as st

from openai import OpenAI

from prompts.analyzer_prompt import (
SYSTEM_PROMPT,
USER_PROMPT_TEMPLATE,
)

st.set_page_config(
page_title="🧠 Narrative Analyzer",
page_icon="🧠",
layout="wide",
)

st.title("🧠 Narrative Analyzer")
st.write(
"Analyze articles, posts, or opinions and separate facts, claims, opinions, emotional language, missing context, and verification questions."
)

api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()
client = OpenAI(api_key=api_key)

text = st.text_area(
"Paste text here",
height=300,
)

if st.button("🧪 Analyze", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text.")
        st.stop()

    prompt = USER_PROMPT_TEMPLATE.format(text=text)

    progress = st.progress(0)

    with st.spinner("🧠 AI is analyzing the narrative..."):

        progress.progress(30)

        response = client.chat.completions.create(
            ...
        )

        progress.progress(80)

    try:
        ...
        
    result = json.loads(response.choices[0].message.content)  

    progress.progress(100)  

    st.success("✅ Analysis completed!")  

    markdown_report = "# Narrative Analysis Report\n\n"  

    # NRI 11-field schema (PRODUCT SPEC §26).  
    # Each entry: (display title, JSON key, field type "text" or "list")  
    fields = [  
        ("🧭 Narrative Overview", "narrative_overview", "text"),  
        ("🎯 Primary Claim", "primary_claim", "text"),  
        ("📌 Evidence", "evidence", "list"),  
        ("🧩 Assumptions", "assumptions", "list"),  
        ("🖼️ Framing", "framing", "list"),  
        ("⚠️ Emotional Triggers", "emotional_triggers", "list"),  
        ("🕳️ Missing Context", "missing_context", "list"),  
        ("⚖️ Reasoning Risks", "reasoning_risks", "list"),  
        ("🔀 Alternative Interpretations", "alternative_interpretations", "list"),  
        ("🔍 Verification Questions", "verification_questions", "list"),  
        ("❓ Uncertainty", "uncertainty", "list"),  
    ]  

    for title, key, field_type in fields:  

        markdown_report += f"## {title}\n"  

        if field_type == "text":  

            value = (result.get(key) or "").strip()  

            with st.expander(title, expanded=True):  

                if value:  
                    st.markdown(value)  
                    markdown_report += f"{value}\n"  
                else:  
                    st.caption("Not identified.")  
                    markdown_report += "Not identified.\n"  

        else:  

            items = result.get(key, [])  

            with st.expander(f"{title} ({len(items)})", expanded=True):  

                if items:  
                    for item in items:  
                        st.markdown(f"- {item}")  
                        markdown_report += f"- {item}\n"  
                else:  
                    st.caption("No items found.")  
                    markdown_report += "No items found.\n"  

        markdown_report += "\n"  

    st.download_button(  
        "📥 Download Markdown Report",  
        markdown_report,  
        file_name="narrative_analysis_report.md",  
        mime="text/markdown",  
        use_container_width=True,  
    )  

    with st.expander("📄 Original Text"):  
        st.text(text)  

except Exception:  

    st.error("Model did not return valid JSON.")  
    st.code(response.choices[0].message.content)            
