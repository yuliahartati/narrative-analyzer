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

st.subheader("1. Input")

uploaded_files = st.file_uploader(
    "📎 Upload one or more files",
    type=["txt", "docx", "pdf"],
    accept_multiple_files=True,
    help="Supported formats: TXT, DOCX, PDF"
)

if uploaded_files:

    st.success(
        f"📎 {len(uploaded_files)} file(s) ready"
    )

    for uploaded_file in uploaded_files:

        st.caption(
            f"• {uploaded_file.name}"
        )

text_input = st.text_area(
    "Or paste text here",
    height=300,
    placeholder="Paste an article, post, statement, opinion, or other text here..."
)

# Detect URLs in pasted text
import re

detected_urls = re.findall(
    r'https?://[^\s<>"\']+',
    text_input
)

if detected_urls:
    st.info(
        f"🔗 {len(detected_urls)} URL detected"
    )

    for url in detected_urls:
        st.caption(f"• {url}")

# =========================================================
# ANALYZE
# =========================================================

if st.button(
    "🧪 Analyze",
    use_container_width=True
):

    combined_text = ""


    # =====================================================
    # PROCESS UPLOADED FILES
    # =====================================================

    if uploaded_files:

        source_blocks = []

        for index, uploaded_file in enumerate(
            uploaded_files,
            start=1
        ):

            file_name = uploaded_file.name
            file_name_lower = file_name.lower()

            file_bytes = uploaded_file.getvalue()

            try:

                # -----------------------------------------
                # TXT
                # -----------------------------------------

                if file_name_lower.endswith(".txt"):

                    extracted_text = file_bytes.decode(
                        "utf-8",
                        errors="replace"
                    )


                # -----------------------------------------
                # DOCX
                # -----------------------------------------

                elif file_name_lower.endswith(".docx"):

                    document = Document(
                        io.BytesIO(file_bytes)
                    )

                    paragraphs = []

                    for paragraph in document.paragraphs:

                        if paragraph.text.strip():

                            paragraphs.append(
                                paragraph.text
                            )

                    extracted_text = "\n\n".join(
                        paragraphs
                    )


                # -----------------------------------------
                # PDF
                # -----------------------------------------

                elif file_name_lower.endswith(".pdf"):

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

                    extracted_text = "\n\n".join(
                        pages
                    )


                else:

                    extracted_text = ""


            except Exception as e:

                st.error(
                    f"Could not read {file_name}: {e}"
                )

                st.stop()


            # -----------------------------------------
            # CHECK FILE CONTENT
            # -----------------------------------------

            if not extracted_text.strip():

                st.warning(
                    f"No readable text found in: {file_name}"
                )

                continue


            # -----------------------------------------
            # KEEP SOURCE IDENTITY
            # -----------------------------------------

            source_blocks.append(
                f"===== SOURCE {index}: {file_name} =====\n\n"
                f"{extracted_text.strip()}"
            )


        # ---------------------------------------------
        # COMBINE ALL FILES
        # ---------------------------------------------

        if source_blocks:

            combined_text = "\n\n".join(
                source_blocks
            )


    # =====================================================
    # ADD PASTED TEXT
    # =====================================================

    if text_input.strip():

        if combined_text.strip():

            combined_text += (
                "\n\n"
                "===== SOURCE: Pasted Text =====\n\n"
                f"{text_input.strip()}"
            )

        else:

            combined_text = text_input.strip()


    # =====================================================
    # VALIDATE INPUT
    # =====================================================

    if not combined_text.strip():

        st.warning(
            "Please paste some text or upload at least one readable file."
        )

        st.stop()


    # =====================================================
    # SHOW INPUT SUMMARY
    # =====================================================

    if uploaded_files:

        st.info(
            f"📚 {len(uploaded_files)} uploaded source(s) "
            "will be analyzed as one combined corpus."
        )


    # =====================================================
    # BUILD PROMPT
    # =====================================================

    prompt = USER_PROMPT_TEMPLATE.format(
        text=combined_text
    )


    # =====================================================
    # ANALYSIS
    # =====================================================

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

    markdown_report = (
        "# Narrative Analysis Report\n\n"
    )


    for title, key, field_type in fields:

        markdown_report += (
            f"## {title}\n\n"
        )


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
    # ORIGINAL COMBINED INPUT
    # =====================================================

    with st.expander(
        "📄 Original Combined Input"
    ):

        st.text(
            combined_text
        )
