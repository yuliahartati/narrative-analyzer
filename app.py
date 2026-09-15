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


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Narrative Analyzer",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

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


# =========================================================
# OPENAI
# =========================================================

api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)


# =========================================================
# INPUT
# =========================================================

st.subheader("1. Input Text")

uploaded_file = st.file_uploader(
    "📎 Upload a file",
    type=["txt", "docx", "pdf"],
    help="Supported formats: TXT, DOCX, PDF"
)

if uploaded_file is not None:
    st.success(
        f"📎 File ready: {uploaded_file.name}"
    )

text_input = st.text_area(
    "Or paste text here",
    height=300,
    placeholder="Paste an article, post, statement, opinion, or other text here..."
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🧪 Analyze",
    use_container_width=True
):

    # -----------------------------------------------------
    # GET INPUT
    # -----------------------------------------------------

    text = ""

    # If a file was uploaded, process it ONLY after
    # the Analyze button is pressed.
    if uploaded_file is not None:

        file_name = uploaded_file.name.lower()
        file_bytes = uploaded_file.getvalue()

        try:

            # -------------------------------------------------
            # TXT
            # -------------------------------------------------

            if file_name.endswith(".txt"):

                text = file_bytes.decode(
                    "utf-8",
                    errors="replace"
                )


            # -------------------------------------------------
            # DOCX
            # -------------------------------------------------

            elif file_name.endswith(".docx"):

                document = Document(
                    io.BytesIO(file_bytes)
                )

                paragraphs = []

                for paragraph in document.paragraphs:

                    if paragraph.text.strip():

                        paragraphs.append(
                            paragraph.text
                        )

                text = "\n\n".join(
                    paragraphs
                )


            # -------------------------------------------------
            # PDF
            # -------------------------------------------------

            elif file_name.endswith(".pdf"):

                reader = PdfReader(
                    io.BytesIO(file_bytes)
                )

                pages = []

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:

                        pages.append(
                            page_text
                        )

                text = "\n\n".join(
                    pages
                )


        except Exception as e:

            st.error(
                f"Could not read the uploaded file: {e}"
            )

            st.stop()


        # -------------------------------------------------
        # CHECK EXTRACTED TEXT
        # -------------------------------------------------

        if not text.strip():

            st.error(
                "The uploaded file contains no readable text."
            )

            st.stop()


    # -----------------------------------------------------
    # OTHERWISE USE PASTED TEXT
    # -----------------------------------------------------

    else:

        text = text_input


    # -----------------------------------------------------
    # CHECK INPUT
    # -----------------------------------------------------

    if not text.strip():

        st.warning(
            "Please paste some text or upload a file first."
        )

        st.stop()


    # =====================================================
    # ANALYSIS
    # =====================================================

    prompt = USER_PROMPT_TEMPLATE.format(
        text=text
    )

    progress = st.progress(0)

    with st.spinner(
        "🧠 AI is analyzing the narrative..."
    ):

        progress.progress(20)

        try:

            response = client.chat.completions.create(
                model="gpt-5-mini",
                response_format={
                    "type": "json_object"
                },
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            progress.progress(80)

        except Exception as e:

            progress.empty()

            st.error(
                f"Analysis failed: {e}"
            )

            st.stop()


    # =====================================================
    # PARSE JSON
    # =====================================================

    try:

        result = json.loads(
            response.choices[0].message.content
        )

    except Exception:

        progress.empty()

        st.error(
            "Model did not return valid JSON."
        )

        st.code(
            response.choices[0].message.content
        )

        st.stop()


    progress.progress(100)


    # =====================================================
    # SUCCESS
    # =====================================================

    st.success(
        "✅ Analysis completed!"
    )


    # =====================================================
    # NRI 11-FIELD SCHEMA
    # =====================================================

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


    # =====================================================
    # RENDER RESULTS
    # =====================================================

    markdown_report = "# Narrative Analysis Report\n\n"


    for title, key, field_type in fields:

        markdown_report += f"## {title}\n\n"


        # -------------------------------------------------
        # TEXT FIELD
        # -------------------------------------------------

        if field_type == "text":

            value = result.get(
                key,
                ""
            )

            if value is None:

                value = ""

            value = str(value).strip()


            with st.expander(
                title,
                expanded=True
            ):

                if value:

                    st.markdown(
                        value
                    )

                    markdown_report += (
                        value + "\n\n"
                    )

                else:

                    st.caption(
                        "Not identified."
                    )

                    markdown_report += (
                        "Not identified.\n\n"
                    )


        # -------------------------------------------------
        # LIST FIELD
        # -------------------------------------------------

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

                    markdown_report += "\n"

                else:

                    st.caption(
                        "No items found."
                    )

                    markdown_report += (
                        "No items found.\n\n"
                    )


    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    st.divider()

    st.download_button(
        "📥 Download Markdown Report",
        data=markdown_report,
        file_name="narrative_analysis_report.md",
        mime="text/markdown",
        use_container_width=True
    )


    # =====================================================
    # ORIGINAL TEXT
    # =====================================================

    with st.expander(
        "📄 Original Text"
    ):

        st.text(
            text
    )
