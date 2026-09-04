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
if st.button("🚀 Analyze", use_container_width=True):
if not text.strip():
st.warning("Please enter some text.")
st.stop()
prompt = USER_PROMPT_TEMPLATE.format(text=text)
progress = st.progress(0)
with st.spinner("🧠 AI is analyzing the narrative..."):
progress.progress(30)
response = client.chat.completions.create(
model="gpt-5-mini",
response_format={"type": "json_object"},
messages=[
{
"role": "system",
"content": SYSTEM_PROMPT,
},
{
"role": "user",
"content": prompt,
},
],
)
progress.progress(80)
try:
result = json.loads(response.choices[0].message.content)
progress.progress(100)
st.success("✅ Analysis completed!")
markdown_report = "# Narrative Analysis Report\n\n"
sections = [
("📌 Facts", "facts"),
("📢 Claims", "claims"),
("💭 Opinions", "opinions"),
("❤️ Emotional Language", "emotional_language"),
("⚠️ Missing Context", "missing_context"),
("🔍 Questions for Further Verification", "verification_questions"),
]
for title, key in sections:
items = result.get(key, [])
markdown_report += f"## {title}\n"
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
"📄 Download Markdown Report",
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
