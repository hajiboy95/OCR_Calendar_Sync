import json
import streamlit as st
from lib.backend.ollama_backend import query_ollama
from lib.backend.gemini_backend import query_gemini
from lib.models.calendar_event import EventManager


def process_calendar_extraction(ollama_model: str = None, key: str = "result"):
    """
    Processes the uploaded file and prompt using the selected backend (Ollama or Gemini),
    extracts event data in JSON format, and updates Streamlit session state.

    Args:
        backend (str): Either "Ollama (Local)" or another backend identifier (e.g., "Gemini").
        ollama_model (str, optional): Model name for Ollama backend. Required if using Ollama.
    """
    try:
        # Choose backend
        result = (
            query_ollama(
                st.session_state["final_prompt"],
                st.session_state["file_bytes"],
                st.session_state["mime_type"],
                ollama_model,
            )
            if st.session_state["backend"] == "Ollama (Local)"
            else query_gemini(
                st.session_state["final_prompt"],
                st.session_state["file_bytes"],
                st.session_state["mime_type"],
            )
        )

        if result:
            st.session_state[key] = result
            st.rerun()
    except Exception as e:
        st.error(f"Fehler bei der Verarbeitung: {e}")


def extract_json(text):
    try:
        start = text.index("[")
        end = text.rindex("]") + 1
        return text[start:end]
    except ValueError:
        return None


def set_calendar_events(events: str, key: str = "parsed_events"):
    st.session_state[key] = events
