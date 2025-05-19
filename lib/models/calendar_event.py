import json
from typing import List, Dict, Optional
import datetime
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st
from dotenv import load_dotenv
import os
from lib.config.calendar_manager import CalendarManager

load_dotenv()


class EventManager:
    """
    A class to manage and edit calendar events stored in Streamlit's session state.
    """

    def __init__(self, response_text: str):
        self.response_text = response_text
        parsed = self.parse_events()
        if "parsed_events" not in st.session_state:
            parsed = self.parse_events()
            if parsed:
                st.session_state["parsed_events"] = parsed
        self.calendar_manager = CalendarManager()

    def extract_json(self) -> Optional[str]:
        try:
            start = self.response_text.index("[")
            end = self.response_text.rindex("]") + 1
            return self.response_text[start:end]
        except ValueError:
            return None

    def parse_events(self) -> Optional[List[Dict]]:
        json_text = self.extract_json()
        if json_text:
            try:
                return json.loads(json_text)
            except json.JSONDecodeError as e:
                st.error(f"❌ Fehler beim Parsen des JSON: {e}")
        return None

    def update_event(
        self,
        idx: int,
        summary: str = None,
        description: str = None,
        start_datetime: str = None,
        end_datetime: str = None,
        timezone: str = None,
        category: str = None,
    ):
        if "parsed_events" in st.session_state and 0 <= idx < len(
            st.session_state["parsed_events"]
        ):
            event = st.session_state["parsed_events"][idx]

            # Update top-level fields if provided
            if summary is not None:
                event["summary"] = summary
            if description is not None:
                event["description"] = description

            # Update nested start time
            if start_datetime is not None:
                event.setdefault("start", {})["dateTime"] = start_datetime
            if timezone is not None:
                event.setdefault("start", {})["timeZone"] = timezone

            # Update nested end time
            if end_datetime is not None:
                event.setdefault("end", {})["dateTime"] = end_datetime
            if timezone is not None:
                event.setdefault("end", {})["timeZone"] = timezone

            if category is not None:
                event["category"] = category

            # Save back to session state
            st.session_state["parsed_events"][idx] = event

    def to_json(self) -> str:
        return json.dumps(
            st.session_state.get("parsed_events", []), indent=2, ensure_ascii=False
        )

    def render_editable_event_blocks(self):
        if (
            "parsed_events" not in st.session_state
            or not st.session_state["parsed_events"]
        ):
            st.info("ℹ️ Keine Termine zum Bearbeiten verfügbar.")
            return

        st.subheader("📅 Bearbeitbare Termine")

        for idx, event in enumerate(st.session_state["parsed_events"]):
            if (
                "start" not in event
                or "end" not in event
                or "dateTime" not in event["start"]
                or "dateTime" not in event["end"]
            ):
                st.warning(
                    f"⚠️ Ereignis #{idx + 1} ist unvollständig und wurde übersprungen."
                )
                continue

            try:
                start_dt = datetime.datetime.fromisoformat(event["start"]["dateTime"])
                end_dt = datetime.datetime.fromisoformat(event["end"]["dateTime"])
            except Exception as e:
                st.warning(
                    f"⚠️ Fehler beim Parsen von Datum/Zeit für Ereignis #{idx + 1}: {e}"
                )
                continue

            timezone = event["start"].get("timeZone", "Europe/Berlin")

            # Initialize session state for widgets if not present
            default_values = {
                f"summary_{idx}": event.get("summary", ""),
                f"description_{idx}": event.get("description", ""),
                f"category_{idx}": event.get("category", ""),
                f"start_date_{idx}": start_dt.date(),
                f"start_time_{idx}": start_dt.time(),
                f"end_date_{idx}": end_dt.date(),
                f"end_time_{idx}": end_dt.time(),
            }
            for key, value in default_values.items():
                if key not in st.session_state:
                    st.session_state[key] = value

            with st.expander(
                f"📌 {st.session_state[f'summary_{idx}'] or 'Ohne Titel'}"
            ):
                summary = st.text_input("Titel", key=f"summary_{idx}")
                description = st.text_area("Beschreibung", key=f"description_{idx}")
                category = st.selectbox(
                    "Kategorie",
                    self.calendar_manager.calendar_category_map.keys(),
                    key=f"category_{idx}",
                )

                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start-Datum", key=f"start_date_{idx}")
                    start_time = st.time_input("Start-Zeit", key=f"start_time_{idx}")
                with col2:
                    end_date = st.date_input("End-Datum", key=f"end_date_{idx}")
                    end_time = st.time_input("End-Zeit", key=f"end_time_{idx}")

                # Combine values from widgets
                start_datetime_obj = datetime.datetime.combine(start_date, start_time)
                end_datetime_obj = datetime.datetime.combine(end_date, end_time)

                # Ensure end is at least 30 min after start
                if end_datetime_obj <= start_datetime_obj:
                    end_datetime_obj = start_datetime_obj + datetime.timedelta(
                        minutes=30
                    )
                    st.warning("⚠️ Endzeitliegt sollte nach der Startzeit liegen.")

                # Convert to isoformat
                start_datetime = start_datetime_obj.isoformat()
                end_datetime = end_datetime_obj.isoformat()

                if st.button("✅ Eintrag aktualisieren", key=f"update_{idx}"):
                    self.update_event(
                        idx=idx,
                        summary=summary,
                        description=description,
                        start_datetime=start_datetime,
                        end_datetime=end_datetime,
                        timezone=timezone,
                        category=category,
                    )
                    st.success(f"✅ Eintrag {idx + 1} wurde aktualisiert.")

    def render_upload_button(self):
        """
        Renders a button to upload current events to Google Calendar.
        """
        if st.button("🔄 Mit Kalender synchronisieren"):
            self.calendar_manager.upload_calendar_events()

    def render_json_block(self):
        """
        Renders a text area with the raw event JSON data for manual editing.
        Allows the user to edit and re-parse the JSON into session state.
        """
        st.subheader("📝 Rohdaten (JSON) bearbeiten")

        raw_json = json.dumps(
            st.session_state.get("parsed_events", []),
            indent=2,
            ensure_ascii=False,
        )

        edited_json = st.text_area("📦 Bearbeite JSON-Daten", raw_json, height=300)

        if st.button("💾 Änderungen speichern"):
            try:
                parsed = json.loads(edited_json)
                if isinstance(parsed, list):
                    st.session_state["parsed_events"] = parsed
                    st.success("✅ JSON erfolgreich gespeichert und geladen.")
                else:
                    st.error("❌ Das JSON muss eine Liste von Ereignissen sein.")
            except json.JSONDecodeError as e:
                st.error(f"❌ Ungültiges JSON: {e}")
