# Voice Notes to Flashcards

Voice Notes to Flashcards is a Streamlit application that turns lecture
recordings and uploaded audio into structured study material with the Google
Gemini API. It produces a transcript, summary, key concepts, editable
flashcards, and a practice quiz from a single audio file.

---
## Live Link
https://voicetoeverything.streamlit.app/

## Features

- Record lecture audio directly in the browser.
- Upload audio files in MP3, WAV, M4A, OGG, or WEBM format.
- Generate an important-content transcript from the lecture.
- Generate an AI-written summary and a list of key concepts.
- Create between 5 and 30 flashcards and select the desired difficulty.
- Review and edit generated flashcards in a table.
- Download the edited flashcards as a CSV file.
- Generate a five-question multiple-choice practice quiz.
- Submit quiz answers and receive a percentage score.
- Browse saved audio items in the study history view.
- Search history by file name or subject and filter it by recording or upload.
- Delete individual history items and their locally stored audio files.
- View dashboard metrics for the current flashcards, quiz questions, and score.

## How the Application Works

1. Select a subject and difficulty in the sidebar.
2. Choose the number of flashcards to generate. The available range is 5 to
	30 cards in increments of 5.
3. Optionally enable summary and quiz generation.
4. Record a lecture or upload an audio file.
5. Select **Generate Study Material**.
6. The application sends the audio and an academic study prompt to the Gemini
	model `gemini-3-flash-preview`.
7. Gemini returns structured JSON containing the transcript, summary, key
	concepts, flashcards, and quiz questions.
8. Review the results in the Summary, Key Concepts, Flashcards, and Quiz tabs.
9. Edit and download flashcards, or submit the quiz to calculate a score.

The application asks Gemini to keep answers concise, create exam-focused
questions, generate five quiz questions, and avoid adding information that is
not supported by the lecture. AI-generated content should still be checked
against the original lecture before it is used for assessment or formal study.

## Technology Stack

- Python
- Streamlit for the user interface
- Google Gemini API through the `google-genai` package
- Pandas for flashcard tables and analysis
- SQLite for local study history
- `python-dotenv` for loading environment variables

## Project Structure

```text
voice_notes_flashcards/
|-- app.py                 # Streamlit user interface and AI workflow
|-- history.py             # SQLite schema and study-history operations
|-- requirements.txt       # Python dependencies
|-- README.md              # Project documentation
`-- audio_history/         # Runtime directory for saved audio files
```

The following files and directories are created or used locally at runtime
and should not be committed:

- `.env` for the Gemini API key
- `.venv/` for the local virtual environment
- `study_history.db` for the SQLite database
- `audio_history/` for saved recordings and uploads
- `__pycache__/` and compiled Python files

## Requirements

- Python 3.10 or newer is recommended.
- A Google Gemini API key.
- A modern web browser with microphone access if you want to record audio.
- Internet access for requests to the Gemini API.

## Installation

Clone the repository and move into the project directory:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd voice_notes_flashcards
```

Create and activate a virtual environment.

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

Create a file named `.env` in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The application loads this value when it starts. If the variable is missing,
the application stops and displays an error. Never commit `.env` or share the
API key publicly.

## Running the Application

Start Streamlit from the project root:

```bash
python -m streamlit run app.py
```

Streamlit normally serves the application at:

```text
http://localhost:8501
```

Open the displayed local URL in your browser. When recording audio, grant the
browser permission to use your microphone.

## Study History and Local Data

The application creates `study_history.db` beside the Python files and
initializes the database automatically. The history table includes metadata
such as the file name, source type, subject, local audio path, creation time,
generated study content, quiz score, and favorite status.

Audio files are copied into `audio_history/` when they are recorded or
uploaded. The History view provides session counts, search, source filtering,
and deletion. Deleting a history item also removes its associated local audio
file when that file is available.

Generated content is held in the active Streamlit session. Persisted content
can be displayed when it has been saved with a history record.

## Security and Privacy

- API credentials are read from an environment file rather than hard-coded.
- Audio is stored locally in `audio_history/`.
- Audio submitted for generation is sent to the configured Google Gemini API.
- Do not upload confidential or personally identifiable recordings unless your
  organization permits processing by the selected AI service.
- Review `.gitignore` before publishing the repository to ensure local data
  and credentials remain excluded.

## Troubleshooting

**The application reports that the Gemini API key is missing**

Confirm that `.env` is in the same directory as `app.py` and that it contains
the exact variable name `GEMINI_API_KEY`.

**Audio recording does not work**

Use a supported browser, allow microphone access, and confirm that the browser
and operating system can detect the intended microphone.

**Generation fails or returns invalid content**

Check the API key, network connection, Gemini account limits, and audio file
format. Large or unclear recordings may also produce incomplete results.

**The application does not start**

Activate the virtual environment and reinstall dependencies with
`python -m pip install -r requirements.txt`.

## Future Improvements

- Add user authentication and cloud-based history.
- Persist generated content and quiz scores consistently for every session.
- Add spaced-repetition scheduling and richer learning analytics.
- Support multilingual transcription and study material generation.
- Add export formats such as PDF and JSON.
- Add automated tests for database operations and AI response validation.

## Author

Margani Siddartha
CSE Student and Developer
