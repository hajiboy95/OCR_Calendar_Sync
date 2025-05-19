# 🧠 OCR_Calendar_Sync

**OCR_Calendar_Sync** is an intelligent tool that extracts calendar events from PDFs or images using OCR-powered Large Language Models (LLMs), and syncs them directly to your Google Calendar.

## 📦 Project Structure

```bash
📦LLM_Calendar_Sync
 ┣ 📂lib
 ┃ ┣ 📂backend
 ┃ ┃ ┣ 📜gemini_backend.py
 ┃ ┃ ┗ 📜ollama_backend.py
 ┃ ┣ 📂config
 ┃ ┃ ┣ 📜calendar_manager.py
 ┃ ┃ ┗ 📜prompt_manager.py
 ┃ ┣ 📂models
 ┃ ┃ ┣ 📜calendar_event.py
 ┃ ┃ ┗ 📜image.py
 ┃ ┗ 📂utils
 ┃ ┃ ┣ 📜process_calendar_extraction.py
 ┃ ┃ ┗ 📜select_date.py
 ┣ 📜.env_example
 ┣ 📜calendar_categories_example.json
 ┣ 📜LICENSE
 ┣ 📜README.md
 ┣ 📜main.py
 ┗ 📜requirements.txt
```

## 🚀 Features

* 🧠 **LLM-powered Extraction**: Parse event details (date, time, location, etc.) from PDFs or images using Google Gemini or local Ollama models.
* 📅 **Smart Event Creation**: Automatically formats extracted data into Google Calendar-compatible events.
* ☁️ **Google Calendar Integration**: Syncs events directly to your calendar via the Google Calendar API.
* 🔁 **Multiple Calendar Support**: Use category-based mapping to route events to different calendars.
* 🖼️ **Flexible Input Formats**: Upload PDFs or image files (JPG, PNG).
  ⚠️ *Note: PDF extraction is not yet supported with Ollama models.*

## 🛠️ Setup Instructions

### 0. Create an `.env` File

Before running the project, you'll need to create a `.env` file with your API keys and configuration.

You can use the provided `.env_example` as a starting point:

1. **Rename** `.env_example` to `.env`
2. **Edit** the file and fill in the required values (e.g. your Gemini API key, service account path, calendar IDs, etc.).  
   A more detailed explanation of how to obtain and configure these values is provided in the following steps.

### 1. 🔐 Gemini API Key Setup

If you're using Gemini (Google's LLM), create an API key at [Google AI Studio](https://makersuite.google.com/app/apikey) and add it to your `.env` file like so:

```env
GEMINI_API_KEY="your_api_key_here"
```

### 2. 📅 Google Calendar API Access (Service Account)

> Required for syncing events to your calendar

#### Step-by-Step Setup

1. **Enable Calendar API**

   * Go to [Google Cloud Console](https://console.cloud.google.com/)
   * Create/select a project.
   * Navigate to **APIs & Services > Library**
   * Search and enable **Google Calendar API**

2. **Create a Service Account**

   * Go to **APIs & Services > Credentials**
   * Click **Create Credentials > Service Account**
   * Complete the setup and save the generated `.json` file
   * Add the path to your `.env` file:

     ```env
     CALENDAR_SERVICE_ACCOUNT_FILE_PATH=path/to/your-service-account.json
     ```

3. **Share Your Calendar with the Service Account**

   * Open [Google Calendar](https://calendar.google.com/)
   * Click the gear icon ⚙️ > **Settings**
   * Select your calendar (e.g., *LLM\_Sync\_App*) in the left menu
   * Scroll to **Share with specific people**
   * Add your service account email (e.g., `xyz@project.iam.gserviceaccount.com`)
     ✅ Give **"Make changes to events"** permission

4. **Setting Up the Calendar Category Mapping**

Before using the calendar sync functionality, you’ll need to provide a mapping between human-readable calendar names (used in your app) and actual Google Calendar IDs.

You can use the provided `calendar_categories_example.json` file as a starting point:

1. You can use `calendar_categories_example.json` as a draft for your calendar categories file.
2. **Edit** the file and replace the placeholder values with your actual calendar names and IDs.
   >💡 You can find the Calendar ID in your [Google Calendar settings](https://calendar.google.com/calendar/u/0/r/settings), under the section labeled **Calendar ID**.

3. **Reference** this file in your `.env` by setting the `CALENDAR_CATEGORY_MAP_PATH` variable:

### 3. 🔄 Category-Based Calendar Mapping (Optional)

To route different types of events to specific calendars, define a category-to-calendar mapping in your environment configuration:

```env
CALENDAR_CATEGORY_MAP={"Work": "work_id@group.calendar.google.com", "Private": "myemail@gmail.com"}
```

> ✅ **Note:** At least one category is required. This can simply point to your main calendar if you don't need multiple categories.

> ⚠️ **Important:** Each calendar listed must be **shared with your service account**, as described in the setup instructions.

Additionally, update the relevant prompt in `lib/config/prompt_manager.py` to reflect the calendar categories you've defined. This allows the system to recognize and properly route events based on their category.

## 🧪 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## ⚙️ Running the App

Start the Streamlit app:

```bash
streamlit run main.py
```

## ⚠️ Notes

* PDFs currently **only work with Gemini**, not with Ollama.
* Ensure that your `.env` file is properly named (not `.env_example`) and all required variables are set.
* You must **pull supported Ollama models** before use if you want to run them locally.

## 📝 License

MIT License © 2025