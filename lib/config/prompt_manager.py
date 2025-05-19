import streamlit as st


class PromptManager:
    """A class for managing and retrieving predefined prompts used for text extraction and interpretation."""

    def __init__(self):
        """Initializes the PromptManager with predefined prompts."""

        # Define the prompt for reading calendar layout
        self.calendar = (
            "Bitte lies den handgeschriebenen Text auf dem Bild einer Tagesplaner-Seite sorgfältig und so genau wie "
            "möglich.\n\n"
            "### Deine Aufgabe:\n"
            "Extrahiere alle relevanten Informationen aus dem Bild und strukturiere sie wie folgt:\n\n"
            "1. Alle **Termine oder Ereignisse** aus dem Zeitplan (inkl. Beschreibung und Notizen).\n"
            "2. **Start- und Endzeit** jedes Termins (so exakt wie möglich).\n"
            "3. Verwende die Inhalte von der linken Seite (Titel + Beschreibung) für `summary` und `description`.\n"
            "4. Ergänze ggf. passende Notizen von der rechten Seite in der `description`.\n"
            "5. Gib jeden Termin im Format der **Google Calendar API** aus.\n\n"
            "{\n"
            '    "summary": "Titel des Termins",\n'
            '    "location": "Ort (optional)",\n'
            '    "description": "Beschreibung oder zusätzliche Informationen",\n'
            '    "start": {\n'
            '        "dateTime": "YYYY-MM-DDTHH:MM:SS+ZEITOFFSET",\n'
            '        "timeZone": "Zeitzone (z.B. Europe/Berlin)"\n'
            "    },\n"
            '    "end": {\n'
            '        "dateTime": "YYYY-MM-DDTHH:MM:SS+ZEITOFFSET",\n'
            '        "timeZone": "Zeitzone (z.B. Europe/Berlin)"\n'
            '    "category": "Kategorie",\n'
            "    }\n"
            "}\n\n"
            "Ordne die Events einer der folgenden Kategorien zu:\n"
            "- **Arbeit**: Berufliche Termine, Meetings und Aufgaben.\n"
            "- **Erledigungen**: Aufgaben oder Besorgungen, die erledigt werden müssen.\n"
            "- **Freunde**: Treffen oder Aktivitäten mit Freunden.\n"
            "- **ÖPVN/Auto/Etc**: Fahrten mit öffentlichen Verkehrsmitteln, Auto oder sonstige Transportmittel.\n"
            "- **Routinen**: Wiederkehrende tägliche oder wöchentliche Abläufe.\n"
            "- **Self-Care**: Aktivitäten zur Selbstfürsorge wie Entspannung oder Wellness.\n"
            "- **Sport**: Sportliche Aktivitäten und Trainingseinheiten.\n"
            "- **Termine**: Geplante Meetings, Verabredungen oder feste Ereignisse mit einem festen Zeitpunkt.\n"
        )

        # Define the prompt for reading text on an image
        self.readText = (
            "Lies die handgeschriebenen Notizen und Aufgaben in diesem Bild und liste diese auf.\n"
            "Extrahiere dabei nur das, was wirklich im Bild zu erkennen ist, ohne Ergänzungen oder Annahmen."
        )

        # Define the prompt for summarizing text on an image
        self.summary = (
            "Fasse den Text auf dem Bild zusammen.\n"
            "Beschränke dich nur auf das, was wirklich im Bild zu sehen ist. "
            "Ergänze keine Informationen und gib nur eine prägnante Zusammenfassung der erkennbaren Inhalte."
        )

        # Define the prompt for describing an image
        self.describe = (
            "Erzähle mir, was auf dem Bild zu sehen ist.\n"
            "Stelle sicher, dass du nur das beschreibst, was wirklich sichtbar ist. "
            "Füge keine Annahmen oder ungenauen Beschreibungen hinzu, sondern beschreibe nur das, was auf dem Bild "
            "direkt erkennbar ist."
        )

        self.prompt_map = {
            "Calendar": self.calendar,
            "Read Text": self.readText,
            "Summary": self.summary,
            "Describe Image": self.describe,
        }

        # Category-to-calendar ID mapping

    def get_prompt_names(self):
        """Returns a list of available prompt names.

        Returns:
            list: A list of strings representing the names of the available prompts.
        """
        return list(self.prompt_map.keys())

    def set_prompt_draft(self, name: str, key: str = "prompt"):
        """
        Sets a specific prompt in Streamlit session state based on the selected prompt name.

        Args:
            name (str): The name of the prompt to set (e.g., "Calendar").
            key (str): The session state key under which the prompt should be stored. Defaults to "prompt".

        Side Effects:
            Updates st.session_state[key] with the corresponding prompt string or an empty string if not found.
        """
        st.session_state[key] = self.prompt_map.get(name, "")

    def merge_prompt_components(
        self,
        composing_key_list: list[str] = ["prompt", "date"],
        key: str = "final_prompt",
    ):
        """
        Merges specified string components from st.session_state into a single string
        and stores the result under the given key.

        Args:
            composing_key_list (list[str]): List of session state keys to merge. Defaults to ["prompt", "date", "template_specific"].
            key (str): The key under which to store the final merged prompt. Defaults to "final_prompt"
        """
        merged = "\n\n".join(
            str(st.session_state.get(k, ""))
            for k in composing_key_list
            if st.session_state.get(k)
        )
        st.session_state[key] = merged
