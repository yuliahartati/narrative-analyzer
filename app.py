import io
import json
import streamlit as st

from openai import OpenAI
from docx import Document
from pypdf import PdfReader

from prompts.analyzer_prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)


st.set_page_config(
    page_title="Narrative Analyzer",
    page_icon="🧠",
    layout="wide"
)


st.title("🧠 Narrative Analyzer")

st.write(
    "Analyze articles, posts, or opinions to identify narrative structure, "
    "claims, evidence, assumptions, framing, emotional triggers, missing context, "
    "reasoning risks, alternative interpretations, verification questions, and uncertainty."
)

st.caption(
    "Analytical Assistance — identifies patterns in the supplied material. "
    "It does not independently establish factual truth unless sources are verified."
)


# ---------------------------------------------------------
# OPENAI
# ---------------------------------------------------------

api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "📎 Upload a file",
    type=["txt", "docx", "pdf"],
    help="Supported formats: TXT, DOCX, PDF"
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "text_input" not in st.session_state:
    st.session_state.text_input = ""

if "loaded_file" not in st.session_state:
    st.session_state.loaded_file = None


# ---------------------------------------------------------
# EXTRACT TEXT FROM FILE
# ---------------------------------------------------------

if uploaded_file is not None:

    file_name = uploaded_file.name

    if st.session_state.loaded_file != file_name:

        try:

            file_bytes = uploaded_file.getvalue()

            if file_name.lower().endswith(".txt"):

                extracted_text = file_bytes.decode(
                    "utf-8",
                    errors="replace"
                )

            elif file_name.lower().endswith(".docx"):

                document = Document(
                    io.BytesIO(file_bytes)
                )

                paragraphs = [
                    paragraph.text
                    for paragraph in document.paragraphs
                    if paragraph.text.strip()
                ]

                extracted_text = "\n\n".join(paragraphs)

            elif file_name.lower().endswith(".pdf"):

                reader = PdfReader(
                    io.BytesIO(file_bytes)
                )

                pages = []

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        pages.append(page_text)

                extracted_text = "\n\n".join(pages)

            else:

                extracted_text = ""

            st.session_state.text_input = extracted_text
            st.session_state.loaded_file = file_name

            if not extracted_text.strip():

                st.warning(
                    "The file was uploaded, but no readable text was extracted."
                )

        except Exception as e:

            st.error(
                f"Could not read the uploaded file: {e}"
            )


# ---------------------------------------------------------
# TEXT INPUT
# ---------------------------------------------------------

text = st.text_area(
    "Paste text here or use the uploaded file above",
    height=300,
    key="text_input",
)


# ---------------------------------------------------------
# ANALYZE
# ---------------------------------------------------------

if st.button(
    "🧪 Analyze",
    use_container_width=True
):

    if not text.strip():

        st.warning(
            "Please enter some text or upload a file."
        )

        st.stop()


    prompt = USER_PROMPT_TEMPLATE.format(
        text=text
    )


    progress = st.progress(0)


    with st.spinner(
        "🧠 AI is analyzing the narrative..."
    ):

        progress.progress(30)


        response = client.chat.completions.create(
            model="gpt-5-mini",
            response_format={
                "type": "json_object"
            },
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

        result = json.loads(
            response.choices[0].message.content
        )


        progress.progress(100)


        st.success(
            "✅ Analysis completed!"
        )


        markdown_report = (
            "# Narrative Analysis Report\n\n"
        )


        # -------------------------------------------------
        # NRI 11-FIELD SCHEMA
        # -------------------------------------------------

        fields = [

            (
                "🧭 Narrative Overview",
                "narrative_overview",
                "text"
            ),

            (
                "🎯 Primary Claim",
                "primary_claim",
                "text"
            ),

            (
                "📌 Evidence",
                "evidence",
                "list"
            ),

            (
                "🧩 Assumptions",
                "assumptions",
                "list"
            ),

            (
                "🖼️ Framing",
                "framing",
                "list"
            ),

            (
                "⚠️ Emotional Triggers",
                "emotional_triggers",
                "list"
            ),

            (
                "🕳️ Missing Context",
                "missing_context",
                "list"
            ),

            (
                "⚖️ Reasoning Risks",
                "reasoning_risks",
                "list"
            ),

            (
                "🔀 Alternative Interpretations",
                "alternative_interpretations",
                "list"
            ),

            (
                "🔍 Verification Questions",
                "verification_questions",
                "list"
            ),

            (
                "❓ Uncertainty",
                "uncertainty",
                "list"
            ),
        ]


        # -------------------------------------------------
        # RENDER RESULTS
        # -------------------------------------------------

        for title, key, field_type in fields:

            markdown_report += (
                f"## {title}\n"
            )


            if field_type == "text":

                value = (
                    result.get(key) or ""
                ).strip()


                with st.expander(
                    title,
                    expanded=True
                ):

                    if value:

                        st.markdown(
                            value
                        )

                        markdown_report += (
                            f"{value}\n"
                        )

                    else:

                        st.caption(
                            "Not identified."
                        )

                        markdown_report += (
                            "Not identified.\n"
                        )


            else:

                items = result.get(
                    key,
                    []
                )


                if not isinstance(
                    items,
                    list
                ):

                    items = [
                        str(items)
                    ]


                with st.expander(
                    f"{title} ({len(items)})",
                    expanded=True
                ):

                    if items:

                        for item in items:

                            st.markdown(
                                f"- {item}"
                            )

                            markdown_report += (
                                f"- {item}\n"
                            )

                    else:

                        st.caption(
                            "No items found."
                        )

                        markdown_report += (
                            "No items found.\n"
                        )


            markdown_report += "\n"


        # -------------------------------------------------
        # DOWNLOAD REPORT
        # -------------------------------------------------

        st.download_button(
            "📥 Download Markdown Report",
            markdown_report,
            file_name="narrative_analysis_report.md",
            mime="text/markdown",
            use_container_width=True,
        )


        # -------------------------------------------------
        # ORIGINAL TEXT
        # -------------------------------------------------

        with st.expander(
            "📄 Original Text"
        ):

            st.text(text)


    except Exception:

        st.error(
            "Model did not return valid JSON."
        )

        st.code(
            response.choices[0].message.content
        )
