import streamlit as st
import ollama
import os
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
from lib.config.prompt_manager import PromptManager
from lib.utils.select_date import select_event_date
import locale
import datetime
from lib.models.image import ImageProcessor
from lib.utils.process_calendar_extraction import process_calendar_extraction
from lib.models.calendar_event import EventManager
import json


locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Handschrift Erkenner", page_icon="✍️", layout="wide")
st.title("✍️ Handschrift Erkenner")

# Datei Upload
backend = None
st.file_uploader(
    "Lade ein handschriftliches Bild oder PDF hoch",
    type=["jpg", "jpeg", "png", "pdf"],
    key="uploaded_file",
)

if st.session_state["uploaded_file"]:
    image_processor = ImageProcessor(st.session_state["uploaded_file"])
    image_processor.process_file(byte_data_key="file_bytes", MIME_type_key="mime_type")
    if st.session_state["mime_type"] == "application/pdf":
        st.success("PDF-Datei erkannt.")
    else:
        with st.expander("🖼️ Hochgeladenes Bild", expanded=False):
            image = Image.open(st.session_state["uploaded_file"]).convert("RGB")
            st.session_state["preview_image"] = image
            left_co, cent_co, last_co = st.columns(3)
            with cent_co:
                st.image(image, width=300)


# Modell-Auswahl
col1, col2 = st.columns(2)
with col1:
    st.radio(
        "Wähle ein Backend-Modell",
        ["Gemini 2.5 Flash preview (API)", "Ollama (Local)"],
        key="backend",
    )
    ollama_model = None
    if st.session_state["backend"] == "Ollama (Local)":
        try:
            models_info = ollama.list()
            installed_models = [m["model"] for m in models_info.get("models", [])]
            ollama_model = st.selectbox(
                "Wähle ein Ollama Vision-Modell",
                options=installed_models or ["(Keine Modelle installiert)"],
            )
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Ollama-Modelle: {e}")

with col2:
    prompt_manager = PromptManager()
    st.selectbox(
        "Wähle einen Prompt aus",
        prompt_manager.get_prompt_names(),
        key="prompt_name",
    )
    prompt_manager.set_prompt_draft(name=st.session_state["prompt_name"], key="prompt")
    st.session_state["template_specific"] = (
        "Gib jeden Termin im Format der **Google Calendar API** aus.\n\nKeine weiteren Erklärungen oder Zusatztexte."
    )

    if st.session_state["prompt_name"] in ["Calendar"]:
        select_event_date()
    prompt_manager.merge_prompt_components(
        ["prompt"]
        + (["date"] if st.session_state["prompt_name"] in ["Calendar"] else [])
    )

# Expander for prompt selection and editing
with st.expander("🔧 Prompt ändern", expanded=False):
    st.text_area("Prompt an das Modell senden", height=200, key="final_prompt")

if (
    st.session_state["backend"] == "Ollama (Local)"
    and st.session_state.get("mime_type") == "application/pdf"
):
    st.error(
        "PDF-Dateien können nicht mit dem Ollama (Local)-Modell hochgeladen werden."
    )
if all(st.session_state.get(k) for k in ["file_bytes", "mime_type"]) and st.button(
    "Handschrift lesen",
    disabled=(
        backend == "Ollama (Local)"
        and st.session_state["mime_type"] == "application/pdf"
    ),
    on_click=lambda: [
        st.session_state.pop("result", None),
        st.session_state.pop("parsed_events", None),
    ],  # Clear result and parsed_events on prompt change
):

    with st.spinner("Deine Handschrift wird gelesen..."):
        process_calendar_extraction(ollama_model)

# Editierbare Blöcke für Einträge
if "result" in st.session_state and st.session_state["prompt_name"] in [
    "Calendar",
]:

    event_manager = EventManager(st.session_state["result"])
    event_manager.render_editable_event_blocks()
    event_manager.render_upload_button()
    # event_manager.render_json_block()

    # Final JSON output
    if "parsed_events" in st.session_state:
        st.subheader("📝 Finales JSON")
        st.code(
            json.dumps(st.session_state["parsed_events"], indent=2, ensure_ascii=False),
            language="json",
        )
