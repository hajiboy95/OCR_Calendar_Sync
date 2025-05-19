import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st

load_dotenv()


class CalendarManager:
    """
    Manages the mapping between event categories and Google Calendar IDs,
    and handles uploading calendar events to Google Calendar using a service account.
    """

    def __init__(self):
        """
        Initializes the CalendarManager instance.

        It attempts to load a calendar category map from the environment variable
        'CALENDAR_CATEGORY_MAP'. The map can be in JSON format or a simple key:value,key:value string.

        If no valid map is found, an empty dictionary is used.
        """
        map_path = os.getenv("CALENDAR_CATEGORY_MAP_PATH")

        try:
            with open(map_path, "r", encoding="utf-8") as f:
                self.calendar_category_map = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            st.error(f"❌ Fehler beim Laden der Kalender-Zuordnung: {e}")
            self.calendar_category_map = {}

    def get_calendar_id_for_category(self, category: str) -> str:
        """
        Retrieves the Google Calendar ID associated with the given event category.

        Args:
            category (str): The event category name.

        Returns:
            str: The Google Calendar ID mapped to the category.
                 Returns None if no mapping exists for the category.
        """
        return self.calendar_category_map.get(category)

    def upload_calendar_events(self):
        """
        Uploads calendar events stored in Streamlit's session state ('parsed_events')
        to the appropriate Google Calendars based on their categories.

        Uses a Google service account specified by the environment variable
        'CALENDAR_SERVICE_ACCOUNT_FILE_PATH' to authenticate with the Google Calendar API.

        Each event is inserted into the calendar matching its category.
        If no calendar ID is found for a category, the event is skipped.

        Provides Streamlit UI feedback (success, warning, or error messages) during the process.
        """
        service_account_path = os.getenv("CALENDAR_SERVICE_ACCOUNT_FILE_PATH")
        events = st.session_state.get("parsed_events", [])

        if not service_account_path:
            st.error("❌ Fehlende Umgebungsvariablen für Google Calendar.")
            return

        if not events:
            st.warning("⚠️ Keine Ereignisse zum Synchronisieren.")
            return

        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            service = build("calendar", "v3", credentials=credentials)

            for idx, event in enumerate(events):
                try:
                    # Remove 'id' to avoid conflicts and duplicates on insert
                    event.pop("id", None)
                    category = event.get("category", "Termine")
                    calendar_id = self.get_calendar_id_for_category(category)
                    if not calendar_id:
                        st.warning(
                            f"⚠️ Kein Kalender für Kategorie '{category}' gefunden. Ereignis wird übersprungen."
                        )
                        continue
                    event.pop("category", None)
                    service.events().insert(
                        calendarId=calendar_id, body=event
                    ).execute()
                    st.success(
                        f"✅ Termin `{event['summary']}` erfolgreich synchronisiert."
                    )
                except Exception as e:
                    st.error(
                        f"❌ Fehler bei Termin `{event.get('summary', 'Unbekannt')}`: {e}"
                    )
        except Exception as e:
            st.error(f"❌ Verbindung zu Google Calendar fehlgeschlagen: {e}")
