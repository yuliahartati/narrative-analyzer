import os
import json
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Narrative Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Narrative Analyzer")
st.write(
    "Analyze articles, posts, or opinions and separate facts, claims, opinions, emotional language, missing context, and verification questions."
)

api_key = st.secrets.get("OPENAI_API_KEY", None)

if not api_key:
    st.error("OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

text = st.text_area(
    "Paste text here",
    height=300,
)

if st.button("Analyze"):

    if not text.strip():
        st.warning("Please enter some text.")
        st.stop()

    prompt = f"""
Analyze the following text.

Return ONLY valid JSON.

Schema:

{{
"facts": [],
"claims": [],
"opinions": [],
"emotional_language": [],
"missing_context": [],
"verification_questions": []
}}

Text:

{text}
"""

    with st.spinner("Analyzing..."):

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert narrative analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

    try:
        result = json.loads(response.choices[0].message.content)

        st.subheader("Facts")
        st.write(result["facts"])

        st.subheader("Claims")
        st.write(result["claims"])

        st.subheader("Opinions")
        st.write(result["opinions"])

        st.subheader("Emotional Language")
        st.write(result["emotional_language"])

        st.subheader("Missing Context")
        st.write(result["missing_context"])

        st.subheader("Questions for Further Verification")
        st.write(result["verification_questions"])

    except Exception:

        st.error("Model did not return valid JSON.")

        st.code(response.choices[0].message.content)
